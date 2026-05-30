# Quick Audit — System Overview

**Prepared by:** Daniel Goodrich
**Date:** May 29, 2026
**Status:** Phase 1 complete (Cowork-scheduled, runs on operator machine); cloud trigger + Gmail auto-send are the known gaps

---

## TL;DR

The Quick Audit is a standalone system that takes a single inbound prospect submission, produces a Dennis-format Quick Audit PDF in the Local Service Spotlight palette, optionally qualifies the prospect against a downstream rubric (MVS by default), drafts the prospect cover note + a team alert in Gmail, and writes everything back to the Tracker — all autonomously. Two sample audits are in the bundle: **Apparel Junction** (validated pillar-by-pillar against Dennis's published PDF as the calibration anchor) and **Expert Services Utah** (first cold-submission test, Overall C 51).

The system was developed inside the MVS engagement but is decoupled from it: nothing about the audit itself depends on MVS, and the qualification step is pluggable (MVS today, AI Builder or partner-specific rubrics later). The audit can feed any downstream program — MVS is just the primary current consumer.

Today it runs as a daily Cowork scheduled task on the operator's machine, which means the machine has to be awake. The cloud trigger and the Gmail auto-send are the two known gaps to build.

---

## 1. The end-to-end flow

Seven stages from prospect click to qualified-lead handoff:

### Stage 1 — Intake
- Prospect fills out a form at `blitzmetrics.com/quick-audit` (or any white-label clone: `localservicespotlight.com`, `hvacgrowth.co`, `rooflaunchmarketing.com`, etc.).
- The form is hosted on SPP (the existing serviceprovider.app stack that already collects invoices for the operation).
- A Zapier zap watches the form and writes the intake row to the Quick Audit Tracker tab in the Maps Visibility Master Sheet (Google Sheets) with `Audit Status = pending`.
- The intake collects: business name, website, primary city, state, annual revenue band, contact name, contact email, contact phone (optional).

### Stage 2 — Trigger
- Today: the daily Cowork scheduled task (`SCHEDULED/quick-audit/SKILL.md`) scans the Tracker for `pending` rows and processes each one. The 3-business-day SLA in the prospect cover note gives the daily cadence enough buffer.
- Cloud target: the Zapier zap fires the audit-runner webhook in parallel with writing the Tracker row, so audits ship within minutes of submission instead of within a day. This is gap #1 in Section 3.

### Stage 3 — Enrichment (8 sub-steps)
Per row, the agent runs an autonomous data pull:
1. **Identity resolution** — Google Places lookup → Place ID → GBP details (category, phone, address, claim status, review count, average rating, photos, posts, hours, verification).
2. **Web enrichment** — fetch homepage → capture CMS, SSL, mobile meta, all JSON-LD schema types, GA4/GTM/Google Ads conversion ID, Meta Pixel, CallRail, chat widgets, blog post count + author, fragmented-domain detection (subdomains, DBAs).
3. **PageSpeed Insights** — curl the PSI API for mobile performance score + LCP/INP/CLS + top issues. Retry once; fall back to Claude in Chrome navigation of pagespeed.web.dev.
4. **Social inventory** — search + fetch for all 8 channels (Facebook, Instagram, TikTok, YouTube, LinkedIn co + personal, Pinterest, Nextdoor). Capture handle, follower count, last post date, bio NAP. Missing channels are marked "Not found" — never skipped silently.
5. **Ahrefs enrichment** — via the Ahrefs MCP, pull DR, referring domains, backlinks, organic keywords, top pages, organic competitors. Use subdomains mode.
6. **Brand SERP snapshot** — search "{business_name} {primary_city}". Capture top 10, Knowledge Panel state, video carousel, FAQ rich result, image pack, page-1 risk items (1-star directory results, "Not Rated" badges).
7. **Local pack + service-city scan** — derive 3-5 head keywords ("{service} {city}"), search each, capture top 3-8 local pack results, identify "Keywords you should own (but don't)" candidates.
8. **Ads transparency snapshot** — fetch Google + Meta ad libraries; fall back to Claude in Chrome if JS-rendered.

All enrichment lands as a JSON blob in `/tmp/` and gets uploaded to Drive for the Tracker reference column.

### Stage 4 — Grade (anchored reasoning, not deduction)
For each of six pillars (Footprint, Reviews, Social, Website, Brand Search, Keyword Rankings), the agent:
- **(A)** Enumerates 5-10 concrete signals (e.g., "GBP phone: (801) 224-8118 — matches Millcreek tracker, not website header").
- **(B)** Anchors to a calibration example: Apparel Junction (Overall D, the published Dennis audit) or RiteWay Heating (Overall A, the internal A-tier reference).
- **(C)** Assigns a letter A-F and a 0-100 score by judgment.
- **(D)** Writes a 3-5 sentence rationale citing specific signals and the anchor.
- **(E)** Captures all four to `<BusinessName>_Grading-Notes_v1.md`, an internal artifact that does not ship to the prospect.

Hard-cap floors apply for catastrophic gaps (no GBP → Footprint capped at F; website unreachable → Website + Keyword Rankings capped at F; etc.). The grading methodology is documented in `QuickAudit-Grading-Approach_v1.md` Section 4.

**Why anchored reasoning and not a deduction formula:** strict formulas read as defensible but break down on industry context (TikTok is critical for an apparel shop, irrelevant for a B2B law firm), holistic fit (one weird gap shouldn't drag an otherwise-A business to B by summed penalties), and Dennis's actual workflow (his grades are judgment calls, not summed deductions). We preserved what formulas were trying to enforce — reproducibility, defensibility — by requiring the signal list + anchor + paragraph rationale on every grade.

### Stage 5 — Synthesis
With six pillar grades in hand, the agent writes the customer-facing audit body to markdown:
- 13 sections (Executive Summary, Business Snapshot, six pillars, 90-Day Plan, Day-90 projections, Next Steps, Appendix, Glossary).
- Three structural rules that match Dennis's reference exactly: no "Glass Half Full" closer, no per-pillar "Revenue translation" paragraph, exactly 8 glossary terms.
- 90-Day Plan as three tier tables (Tier 1: shop-runnable in 30 days; Tier 2: ~20 hours of focused work + a developer; Tier 3: BlitzMetrics Content Factory takes over).
- Day-90 projection table as ranges, never single-point ("Numbers reflect ranges typical of local service businesses that complete similar implementation paths. Treat as directional, not contractual.").
- Owner column on plan rows uses "BlitzMetrics" to match Dennis's voice.

The agent simultaneously builds a structured `audit-spec.json` from the same in-memory synthesis data (the .md and .json are siblings, not derived from each other — single source of truth).

### Stage 6 — Render
The agent invokes the BlitzMetrics-styled PDF renderer via bash:
```
python3 "$WORK_DIR/Claude Outputs/QuickAudit/render_audit_pdf.py" \
    --spec /tmp/<slug>_audit.json \
    --out  "$WORK_DIR/Claude Outputs/QuickAudit/Audits/<Business>_Quick-Audit_v1.pdf"
```
The renderer produces Dennis's structure (cover page with accent band, large numbered section headers, colored grade boxes, stat callouts, page-numbered footer) in the Local Service Spotlight palette: deep teal `#1B4D5C` primary, medium teal `#22698A`, amber `#F5A623` accent, pale tint `#EAF2F8` callouts. Grade mapping: A→deep teal, B→medium teal, C→amber, D→burnt orange, F→red.

### Stage 7 — Qualify, deliver, write back
- Apply the qualification rubric (Agent Definition §5). The rubric is configurable; MVS is the default. Each criterion (LSA-eligible vertical, home-service vertical, annual revenue band, review count + rating, GBP claimed, ≥2 years established) produces hard_pass / soft_fail / hard_fail. Aggregation: any hard_fail → HARD_FAIL; any soft_fail → SOFT_FAIL; all hard_pass → HARD_PASS.
- Upload all three files (audit .md, audit .pdf, grading notes .md) to Google Drive folder `Maps Visibility / Quick Audits / <BusinessName>/`.
- Create a Gmail draft for the prospect cover note with the PDF attached. The draft sits in Drafts for human review and send — the Gmail MCP exposed today supports `create_draft` but not auto-send. This is gap #2 in Section 3.
- If HARD_PASS or SOFT_FAIL, create the team alert Gmail draft to `dylan@localservicespotlight.com` and `668sierra@gmail.com`. Same draft-not-send constraint applies.
- Write back to the Tracker row: Place ID, GBP primary category, Drive URLs (audit MD, audit PDF, grading notes), Order Number, Overall Grade, Top 3 What-To-Fix-First (Tier 1 rows 1-3 of the 90-Day Plan), Decision, Hard Fail Reasons (if applicable), Soft Fail Signals (if applicable), `Routed = yes`, `Routed At = now`.

---

## 2. What's built today

### The skill (entry point)
- **`SCHEDULED/quick-audit/SKILL.md`** — the daily-run prompt the scheduler triggers. Reads the three design docs at the start of every run (so updates to the design docs propagate without redeploying the skill), iterates through `pending` Tracker rows, runs the 16-step workflow per row, ships the PDFs to Drive, drafts the Gmail messages, updates the Tracker.

### The design docs (referenced at every run)
- **`QuickAudit-Agent-Definition_v2.md`** — 16-step operational workflow, qualification rubric, voice/tone rules (the "do" and "don't" lists that prevent puffery and fabrication), failure-mode handling, routing email templates, lede-pattern selection (Pattern A / B / C / D for the Executive Summary opening). Written to be platform-agnostic — same prompt runs under Cowork or any cloud agent runtime.
- **`QuickAudit-Output-Template_v2.md`** — section ordering (13 sections, ends at Glossary), per-pillar structure (grade banner + what we found + why this matters + fixes), Grading Notes file structure, voice/tone rules, PDF render instructions.
- **`QuickAudit-Grading-Approach_v1.md`** — anchored-reasoning grading workflow, hard-cap floors, letter band definitions (A 85-100, B 70-84, C 50-69, D 30-49, F 0-29), the two calibration anchors (Apparel Junction D, RiteWay A).
- **`QuickAudit-Automation-Plan_v1.md`** — architecture source of truth: intake-zap contract, Tracker schema, cloud-migration considerations. Some sections still reference the original MVS-only framing; the operational truth is in the three docs above.

### The renderer
- **`render_audit_pdf.py`** — generalized JSON-driven PDF renderer. Reads an `audit-spec.json` written by the agent at synthesis time, produces the styled PDF using `reportlab` (zero external dependencies beyond reportlab itself, which is already pip-installed in standard Python environments).
- Block-typed schema: `h3`, `paragraph`, `spacer`, `grade_banner`, `stat_callout`, `data_table`, `callout`, `bullets`, `centered`. The schema is fully documented in the module docstring at the top of the file.
- ~700 lines of Python, no external API calls during render.

### The calibration anchors
- **Apparel Junction (Overall D, 38/100)** — published by Dennis on May 28, 2026. Our markdown replication (`ApparelJunction_Quick-Audit_v1.md`) was validated pillar-by-pillar against Dennis's PDF; every grade, every data point, every benchmark number matches exactly. This is the D-tier reference.
- **RiteWay Heating, Cooling & Plumbing (Overall A, ~90/100)** — 67-year HVAC + plumbing operation in Tucson AZ, 12,680 Google reviews at 4.9★, DR 35, BBB A+ since 1976. This is the A-tier reference.

### Sample audits produced by the system
- **`ApparelJunction_Quick-Audit_v1.md`** + Grading Notes — the calibration replication (D 38).
- **`ExpertServicesUtah_Quick-Audit_v1.pdf`** + .md + Grading Notes — first cold-submission test, Overall C 51. Plumbing/HVAC/Electrical, Utah. 22 pages, full Dennis structure, LSS palette.

---

## 3. Known gaps to build

### Gap #1 — Cloud trigger (so the operator machine doesn't have to be awake)
Today the audit runs as a daily Cowork scheduled task on the operator's machine. The pipeline is written to be runtime-agnostic — the same skill + design docs run unmodified under Cowork or any cloud agent runtime. What needs to be built is a cloud-hosted runtime that can (a) accept the webhook from the intake zap with the JSON payload, (b) provision the agent environment (public internet, ephemeral `/tmp`, `curl`, `jq`, Python 3 with `reportlab`, the MCPs in §4), (c) invoke the agent with the payload as the initial event, (d) emit a session-complete signal. The runtime choice is open and not prescribed here.

A side note for the runtime: three enrichment substeps use Claude in Chrome today (live GBP Knowledge Panel, Ads Transparency, PSI fallback). If the chosen runtime lacks headless-browser support, those signals fall back to "data unavailable" — the audit still ships, just with some signal regression. Either accept the gap or wire a browser-worker service the cloud agent can call out to.

### Gap #2 — Gmail auto-send (so the prospect cover note ships without manual review)
The Gmail MCP exposed in the current Cowork session supports `create_draft` but not `send_message`. So today the agent creates two Gmail drafts (prospect cover note + conditional team alert) that sit in Drafts for a human to review and click Send. To close the gap: either swap in a Gmail MCP that ships a send tool, or extend the current one with a `gmail.send`-scoped capability. The workflow flips from `create_draft` to `send` in one place per draft; no other changes required.

The HARD_FAIL prospect emails are arguably better as drafts long-term (a human gut-check before telling a prospect "you don't qualify" is healthy). The HARD_PASS and SOFT_FAIL emails — which are warm "we'll be in touch" notes — are the ones that hurt from manual queuing.

### Gap #3 — Multi-tenancy / white-label routing
The team alert recipients (`dylan@localservicespotlight.com`, `668sierra@gmail.com`) and the cover-note "Reach Dennis directly" footer are hardcoded today. For Sigrun, S&C Digital, or other white-label partners to fire their own audits, the intake payload needs a partner identifier, and the agent needs to swap recipients + footer per partner. The simplest implementation: a partner-config Sheet keyed by partner identifier, read once per audit.

---

## 4. Integration dependencies

What needs to exist in the runtime environment to make the audit ship:

### MCPs / API connectors
| Service | Purpose | Scopes |
|---|---|---|
| Ahrefs API | DR, referring domains, organic keywords, top pages, competitors | `site-explorer-*`, `keywords-explorer-*` (read-only) |
| Google Sheets | Read/write Quick Audit Tracker | Edit on the specific Spreadsheet ID |
| Gmail | **Today:** create drafts (cover note + team alert) — **needed:** `gmail.send` for auto-send | currently `create_draft` only; see Gap #2 |
| Google Drive | Save audit .md, Grading Notes .md, audit .pdf | Write on BlitzMetrics shared drive (or per-partner Drive for white-label) |
| Google Places | Resolve business → Place ID; pull GBP details | Read-only |
| Google PageSpeed Insights | Mobile performance, LCP/INP/CLS | Public API, no auth |
| Anthropic Claude API | The agent itself | Standard API key |

### Webhook plumbing
- Intake form (SPP) → Zapier zap → write Tracker row (already in place) → POST to the agent-runner webhook with the intake JSON (the new piece for cloud deployment, gap #1).

### Output destinations
- Google Drive (PDFs and .md files persist here for human review + Tracker links).
- Gmail Drafts (today) → Gmail Sent (when Gap #2 closes).
- Google Sheets (Tracker row writeback at every milestone).

### Calibration corpus
- Apparel Junction Quick Audit PDF (Dennis's published reference) — bundled.
- Two anchored examples in the Grading Approach (Apparel Junction D, RiteWay A) — bundled.
- Additional anchors get added to `QuickAudit-Grading-Approach_v1.md` §6 as audits accumulate that fill underrepresented bands (e.g., a mid-C example).

---

## 5. Voice, format, and grading philosophy

What "good" output looks like:

### Voice rules (from Agent Definition §7)
- Real numbers, never qualitative hand-waving. "DR 21, 206 referring domains, 3 ranking keywords, 1 visit/mo" — not "weak organic profile."
- Name competitors with their numbers. "DFW Ink — 144 reviews / 4.5★" — not "the leading competitor."
- Day-90 projections use range framing. "Numbers reflect ranges typical of local service businesses that complete similar implementation paths. Treat as directional, not contractual." Never single-point projections.
- Concrete owners and timing in the 90-Day Plan. "Office mgr, 2 hrs" — not "the team should consider."
- Open every pillar with foundation strength before naming the gap.
- Every numeric assertion in the audit body must trace to a live pull captured in Grading Notes, or to the Apparel Junction reference when calibrating. No bare numbers like "81 connections" or "336 backlinks" without a logged source.

### Forbidden vocabulary
"Highlighting," "underscoring," "showcasing," "stands as," "serves as," "marking a pivotal moment," "vibrant," "rich" (figurative), "nestled," "in the heart of," "boasts a," "commitment to," "represents a shift," "evolving landscape," "rooted in," weasel attributions ("experts argue," "industry reports suggest") without specific sources, trailing participial padding ("...creating a lively community within its borders").

### Format rules
- Document ends at the Glossary. No "Glass Half Full" closer.
- No per-pillar "Revenue translation" paragraphs.
- Glossary has exactly 8 terms (NAP, DR, E-E-A-T, GBP, Knowledge Panel, Local Pack, LSA, Schema).
- 90-Day Plan owners use "BlitzMetrics" (not "LSS").
- Next Steps Tier 2 keeps the "$X-X-XX retainer band" placeholder visible.

These rules came from a head-to-head comparison of our system's Apparel Junction output against Dennis's published Apparel Junction PDF (in the bundle as `Apparel_Junction_Quick_Audit.pdf`). The diff was clean except for the structural additions noted above; we stripped them so the format matches Dennis exactly.

---

## 6. What's in the bundle (`quick-audit-v1.1.0.zip`)

```
    ...
```

Total size: ~500 KB.
