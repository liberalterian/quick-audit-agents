# Quick Audit — Output Template v2

**Supersedes:** `MVS_QuickAudit-Output-Template_v1.md`. v2 replaces the strict deduction-grading model with anchored-reasoning grading per `QuickAudit-Grading-Approach_v1.md`, and adds a companion Grading Notes file.

**Purpose:** Drop-in replacement for Section 2 (System Prompt — Output Format) of `MVS_QuickAudit-Agent-Definition_v1.md`. Matches Dennis's Apparel Junction Quick Audit structure with anchored-reasoning grading.

**How to use:** Every audit run produces two files:
- `<BusinessName>_Quick-Audit_v1.md` → renders to PDF, ships to prospect.
- `<BusinessName>_Grading-Notes_v1.md` → internal, persists for quarterly re-grade.

Both files land in `$WORK_DIR/Claude Outputs/QuickAudit/Audits/`.

---

## What changed in v2

- **Grading.** No deduction arithmetic. The agent enumerates signals → anchors to a known example → assigns letter + 0-100 → writes one paragraph of rationale, per pillar. See `QuickAudit-Grading-Approach_v1.md`.
- **New file: Grading Notes.** A companion `.md` that captures the signal list + anchor + rationale per pillar. This is internal — it does not ship to the prospect. It travels with the audit for quarterly re-grade comparison.
- **Visible signal list per pillar in the audit body.** The prospect-facing audit still has to show the work — a structured "what we found" table per pillar with concrete data points. The Grading Notes file holds the grade rationale; the audit body holds the customer-facing observation.

Everything else from v1 (voice rules, section ordering, cover page, projection table format, engagement-tier copy, glossary, PDF render instructions) carries forward unchanged.

---

## Voice and tone rules (unchanged)

- Plain English. No puffery.
- Concrete numbers always. Never guess.
- Foundation strength gets named first.
- Fixes are doable. Owner + time estimate on each.
- No defensive language. State findings.

---

## Cover Page (PDF only, unchanged from v1)

```
QUICK AUDIT  |  DIGITAL & SOCIAL

{Business Name}
{Business Descriptor}  |  {City, State}

PREPARED FOR
{Contact Name}
{Contact Role}, {Business Name}
{Full Address}
{Phone}    {Website}

PREPARED BY
BlitzMetrics    Local Service Spotlight
Issued: {Date}      Order #{ORDER_NUMBER}

{Auditor Name}    {Auditor Email}    {Brand Domain}

Six checks. One page-one verdict. Then the fix.
```

`ORDER_NUMBER` = first 8 uppercase hex chars of a UUID4. Persist to Tracker row.

---

## The Grading Notes file (new in v2)

Filename: `<BusinessName>_Grading-Notes_v1.md`. Lives alongside the main audit. Not shipped to prospect.

### Structure

```markdown
# {Business Name} — Quick Audit Grading Notes v1

**Audited:** {date}
**Auditor:** {auditor name}
**Order #:** {ORDER_NUMBER}
**Linked audit:** {BusinessName}_Quick-Audit_v1.md

---

## Pillar 1 — Footprint & Listings

**Signals observed**
- {signal 1: data point + source}
- {signal 2}
- {signal 3}
- ...
(5-10 concrete signals)

**Anchor**
{Which calibration example was used. E.g., "Closer to Apparel Junction's Footprint D — slightly better because Apple Maps is verified."}

**Grade:** {LETTER} ({N}/100)

**Rationale**
{3-5 sentences citing specific signals and the anchor. This is the working reasoning, not customer-facing copy.}

---

## Pillar 2 — Reviews & Reputation
{same structure}

---

## Pillar 3 — Social Media
{same structure}

---

## Pillar 4 — Website Performance
{same structure}

---

## Pillar 5 — Brand Search
{same structure}

---

## Pillar 6 — Keyword Rankings
{same structure}

---

## Overall

Average: ({N₁} + {N₂} + {N₃} + {N₄} + {N₅} + {N₆}) / 6 = **{N_avg}** → **{LETTER}**

**Sanity check:** {One sentence — does the Overall match the business's overall gut profile? If not, which pillar should be re-examined?}

---

## Hard caps applied (if any)

{List any pillars where a §3 hard cap from the Grading Approach was applied, with the reason.}

---

## Data unavailable (if any)

{List any signals that couldn't be collected and which pillar's grade was affected.}
```

### Quarterly re-grade additions

When re-auditing the same business at +90/+180/+270 days, **append** new pillar blocks to the same file — don't overwrite. Each new pass references the prior signal list and rationale in its own Anchor block ("Prior Footprint was D — these three D-signals are now closed; new grade B").

The file becomes a longitudinal record of the engagement.

---

## Audit body — section ordering (unchanged from v1)

1. Executive Summary
2. Business Snapshot
3. Footprint & Listings
4. Reviews & Reputation
5. Social Media
6. Website Performance
7. Brand Search
8. Keyword Rankings
9. The 90-Day Plan
10. What to Expect by Day 90
11. Next Steps
12. Appendix
13. Glossary

The document ends at the Glossary. There is no Glass Half Full section, and no closing strengths bullets. Strengths get woven into the Executive Summary lede, the Business Snapshot narrative, and the "Why this is good news" subsections — never as a separate appended section. Dennis's reference does not have one; ours must not either.

---

## Audit body — per-pillar structure

Each pillar (sections 03-08) follows this pattern. The grade comes from the Grading Notes process; the audit body just shows it.

```markdown
# 0{N} {PILLAR NAME}

## {Question subhead — e.g., 'Is the basic information consistent?'}

> **{LETTER}  Grade: {Pillar}**
> {One-sentence customer-facing read of the finding.}

### What we found

{Structured presentation of the concrete signals — table, stat callout, or formatted list depending on the pillar. This is the customer-facing version of the signals enumerated in the Grading Notes. Concrete numbers. Specific platforms.}

### Why this matters

{2-3 sentences tying the gap to a business outcome. Cite Google's algorithm signals, first-impression risk, conversion data — whatever's relevant.}

### Fixes

- **{Action}.** {Detail. Owner.} {Time/cost.}
- **{Action}.** ...
{5-8 concrete fixes.}
```

**Do not append a "Revenue translation:" paragraph after the Fixes block.** Dennis's reference does not have these. Dollar leverage gets implied through the Executive Summary bottom-line, the "Where the upside really sits" callout under Day-90, and concrete numbers inside the Fixes bullets themselves ("$30-60 CPL target," "10-20% Maps ranking lift") — never as a separate paragraph per pillar.

### Pillar-specific tables and callouts

These structures are required where indicated. They are how Dennis's format presents the signal list to the customer:

**Footprint (Section 03):** NAP table — Source / Phone / Hours / Status.

**Reviews (Section 04):** Stat callout (4 cells: star avg, lifetime reviews, Google reviews, reviews in last 12 months) + Competitor benchmark table (5-6 peers: Shop / Google reviews / Stars / Website / Snapshot) + Review-response observations subsection.

**Social (Section 05):** Channel inventory table (8 rows: FB, IG, LinkedIn co, LinkedIn personal, TikTok, YouTube, Pinterest, Nextdoor — Status / Followers / Last activity / Verdict) + Quick-win content engine subsection + Personal-brand play subsection.

**Website (Section 06):** Architecture table (Property / What it is / Problem) + Platform commentary paragraph + On-page SEO bulleted gap list (7 bullets matching Dennis's reference: no homepage video, anonymous blog author, meta-keywords stuffing, no testimonials/portfolio above the fold, no service-city landing pages, no clear CTA, AI-generic blog content). Do not auto-append an 8th "PageSpeed data unavailable" bullet — PSI status, if relevant, gets noted in the data-unavailable handling block, not as a visible bullet in the gap list.

**Brand Search (Section 07):** Brand SERP table (Result / Verdict) + Knowledge Panel fix subsection.

**Keyword Rankings (Section 08):** Ahrefs stat callout (4 cells: DR, ranking keywords, org visits/mo, referring domains) + "What you actually rank for" table (Keyword / Position / Volume / Page) + "Keywords you should own" table (Target keyword / Local intent / Current rank / Difficulty) + "Why this is good news" subsection.

---

## Section 01 — Executive Summary (unchanged from v1)

Lede paragraph (5-7 sentences) → Overall Grade block → Six Pillar Grades → Quick Reference Scores → Bottom line. See v1 for full structure.

The Overall Grade and pillar grades come from the Grading Notes file. The Quick Reference Scores are the 0-100 numbers from the grading process. The "one-sentence finding" under each pillar grade is the customer-facing translation of the rationale in the Grading Notes.

---

## Section 02 — Business Snapshot (unchanged from v1)

Facts table + narrative paragraph on what makes the business unusual.

---

## Section 09 — The 90-Day Plan (unchanged from v1)

Tier 1 (Days 0-30) / Tier 2 (Days 30-60) / Tier 3 (Days 60-90), each as a table: # / Action / Owner / Effort / Expected impact.

---

## Section 10 — What to Expect by Day 90 (unchanged from v1)

Projection table with ranges across Today / Day 30 / Day 60 / Day 90 for 8 KPIs. Range-based, never single-point. Use the cohort framing or the fallback framing depending on what's available.

---

## Section 11 — Next Steps (unchanged from v1)

Three engagement tiers verbatim (DIY / Done-with-you / Done-for-you) + Dennis's contact footer.

The Done-with-you tier includes a retainer-band line: `"Typical engagement: 90 days, $X-X-XX retainer band, KPI-based check-ins every 30 days."` Keep the `$X-X-XX` placeholder visible — do not silently delete it. If the engagement has a real range to quote, substitute the actual numbers; otherwise the placeholder stays so the reader sees it as a fillable field.

---

## Section 12 — Appendix (unchanged from v1)

Methodology paragraph + Sources & tools table.

**Methodology paragraph (verbatim from Dennis's reference):**

> This Quick Audit follows BlitzMetrics' six-check framework: Footprint, Reviews & Reputation, Social, Website, Brand Search, Keyword Rankings. Data was pulled on {date range}, from live sources. Scoring uses a 0-100 weighted index across roughly 40 individual signals per pillar.

Do not append a clause about "anchored reasoning against a published calibration set" — the grading methodology stays in the internal Grading Notes file, not the customer-facing Appendix.

**Sources & tools table — only list sources actually pulled.** Do not list PageSpeed Insights (or any other tool) as a source if no data was collected from it. The "data unavailable" handling for PSI lives in §Data-unavailable handling below, not as a row in the sources table.

---

## Section 13 — Glossary

Canonical glossary block — 8 terms matching Dennis's reference exactly: NAP, DR (Domain Rating), E-E-A-T, GBP, Knowledge Panel, Local Pack / Map Pack, LSA, Schema / Structured Data. Plus the footer paragraph: "Prepared by BlitzMetrics — Local Service Spotlight. This audit is informational and reflects publicly observable data as of {date range}. We're happy to walk through any finding live."

Do not add PSI, CWV, CallRail, CTR, or CPC. The reference doesn't have them, and we don't either.

---

## PDF render — instructions for the `pdf` skill (unchanged from v1)

- Page-numbered footer.
- Cover page from metadata block.
- Grade letters rendered as colored boxes (A green / B blue / C yellow / D orange / F red).
- Pillar grade boxes rendered as colored callouts matching the same scheme.
- Stat callouts rendered as outlined boxes, not tables.
- Section numbers (01, 02, ...) larger than section titles.
- Subheading questions in italic gray.

Plain-PDF acceptable for v1 ship if styling doesn't land on the first pass. Content correctness is the gate; visual polish iterates.

---

## Data-unavailable handling

- Explicitly note unavailability in the relevant pillar — one sentence, no separate bullet in the gap list (e.g., Section 06 prose may say "PageSpeed data is unavailable in this audit run" inline, not as an extra bullet).
- No fabricated numbers anywhere. Every numeric assertion in the audit body must trace to a real pull captured in Grading Notes — never assert "81 connections," "336 backlinks," "11-50-person team," or any other specific count without a logged source.
- Grading approach handles unavailability per its own rules (skip the signal, grade on what's observable, note in Grading Notes).
- 90-Day Plan includes a "re-quantify with real data" item where applicable.

---

## File outputs per audit (summary)

| File | Audience | Location | Lifecycle |
|---|---|---|---|
| `<Business>_Quick-Audit_v1.md` | Prospect (via PDF render) | `Audits/` | One file per audit run; versioned if regenerated |
| `<Business>_Quick-Audit_v1.pdf` | Prospect (shipped) | `Audits/` + Drive | One file per audit run |
| `<Business>_Grading-Notes_v1.md` | Internal | `Audits/` | One file per business; appended on re-grade, not overwritten |

The cover-note email attaches the PDF. The Grading Notes file does not leave the internal folder.
