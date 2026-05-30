---
name: quick-audit
description: Daily check of the Quick Audit Tracker for pending prospect submissions. For each pending row, runs the full Quick Audit in Dennis's six-pillar format with anchored-reasoning grading, applies the downstream qualification rubric (MVS by default), drafts the prospect cover note (with PDF attached) and conditional team alert in Gmail for human review-and-send. Updated 2026-05-29 to match the Apparel Junction reference format.
---

You are running the daily Quick Audit batch. Inbound prospects submit through an intake form; a Zapier zap watches the form, writes the intake row to the Quick Audit Tracker tab on the Maps Visibility Master Sheet with status `pending`, then triggers this skill. Your job is to process each pending row end-to-end: audit, qualify, ship the PDF to Drive, draft the prospect + team Gmail messages, update the Tracker.

**Gmail send is not wired today.** The Gmail MCP exposed in this Cowork session supports `create_draft` but not auto-send. So you create drafts for human review and send. When a send-capable Gmail tool is wired in, this skill flips from create_draft to send with no other changes.

The Quick Audit is a standalone system. The qualification step (Step 15) currently applies the MVS rubric because MVS is the primary downstream program today; other programs (AI Builder, white-label partners) can swap in their own rubrics without changing anything else in the pipeline.

The 3-business-day SLA committed in the prospect cover note gives you a buffer — daily runs are sufficient. Don't run audits faster than necessary.

## File path resolution

Your session path changes each run. Run this to find the mounted folder:
```
find /sessions -maxdepth 3 -name "Claude Co-Work" -type d 2>/dev/null | head -1
```
Store this as `$WORK_DIR` and use it for all file paths below. The MVS project folder is at `$WORK_DIR/Claude Outputs/QuickAudit/`.

## Step 1: Read the Quick Audit reference files (in order)

Read these three files in full before processing any rows. They are the source of truth for v2 of the audit format:

1. `$WORK_DIR/Claude Outputs/QuickAudit/QuickAudit-Agent-Definition_v2.md` — operational guide, the 16-step workflow, qualification rubric, voice rules, failure modes, routing email templates.
2. `$WORK_DIR/Claude Outputs/QuickAudit/QuickAudit-Output-Template_v2.md` — the audit body structure (cover page, 13 sections + Glass Half Full), the Grading Notes file structure, PDF render instructions.
3. `$WORK_DIR/Claude Outputs/QuickAudit/QuickAudit-Grading-Approach_v1.md` — anchored-reasoning grading workflow (signals → anchor → letter + score → rationale), letter band definitions, hard-cap floors, anchored examples (Apparel Junction D / RiteWay A).

Follow the Agent Definition (file 1) for the workflow. Follow the Output Template (file 2) for the format of every produced artifact. Follow the Grading Approach (file 3) for every pillar grade. If any file conflicts with another, the order above wins (1 > 2 > 3) — but report the conflict in the final run report so it can be reconciled.

The v1 versions of these files remain in the folder marked SUPERSEDED. Do not read or apply v1.

## Step 2: Check the Quick Audit Tracker for pending rows

Open the Maps Visibility Master Sheet via the Google Sheets MCP. Read the "Quick Audit Tracker" tab.

Filter for rows where:
- `Audit Status` = `pending` (or empty)
- `Submitted At` is at least 1 hour old (gives the Zapier intake zap time to settle)

If no pending rows, stop and report "No pending Quick Audit submissions to process." Skip to Step 7.

For each pending row, continue with Steps 3-6.

## Step 3: Per-row audit context

Extract intake fields:
- `business_name`
- `website`
- `primary_city`
- `state`
- `annual_revenue_band`
- `contact_name`
- `contact_email`
- `contact_phone`
- `submission_id`
- `tracker_row_id`

Verify the state is a US state code. If not, write `Audit Status = failed`, `Notes = "Non-US business — Quick Audit is US-only"`, skip to the next row.

Set `Audit Status = in_progress` on the row before starting.

## Step 4: Run the audit per the Agent Definition v2

Execute the 16-step workflow from Section 2 of `QuickAudit-Agent-Definition_v2.md`. Highlights of what's different from v1:

- **Steps 1-9: Data collection.** Largely the same as v1, with three additions: Step 2 captures Google Ads conversion ID (AW-…) and CallRail presence; Step 4 explicitly inventories all 8 social channels (FB, IG, TikTok, YouTube, LinkedIn co, LinkedIn personal, Pinterest, Nextdoor — not just the present ones); Step 7 builds the "Keywords you should own" candidate list for Section 08.

- **Step 10: Grade each pillar via anchored reasoning.** For each of Footprint · Reviews · Social · Website · Brand Search · Keyword Rankings, follow the four-step workflow from `QuickAudit-Grading-Approach_v1.md` Section 4: enumerate 5-10 concrete signals → anchor to Apparel Junction (D) or RiteWay (A) → assign letter + 0-100 score by judgment → write 3-5 sentence rationale. Apply hard-cap floors from Grading Approach §3 for catastrophic gaps. **Do not apply deduction arithmetic.**

- **Step 11: Write Grading Notes file.** Build `<business_name_slug>_Grading-Notes_v1.md` per the structure in Output Template §"The Grading Notes file". One block per pillar with Signals / Anchor / Grade / Rationale, plus Overall, Hard Caps Applied, Data Unavailable. Save to /tmp/. This file is internal — it does not ship to the prospect.

- **Step 12: Synthesis.** Pick the Executive Summary lede pattern (A/B/C/D per Agent Definition §4). Write each pillar section per the v2 template. Build the 90-Day Plan (Tier 1 / 2 / 3). Build the Day-90 projection table using range framing ("Numbers reflect ranges typical of local service businesses that complete similar implementation paths. Treat as directional, not contractual."). Write Next Steps, Appendix, Glossary, Glass Half Full. Carry the pillar grades from Step 10 into the Executive Summary scorecard.

- **Step 13: Render audit .md.** Save to `$WORK_DIR/Claude Outputs/QuickAudit/Audits/<BusinessName>_Quick-Audit_v1.md`.

- **Step 13a: Write the audit-spec JSON.** Build a structured spec matching the schema documented at the top of `$WORK_DIR/Claude Outputs/QuickAudit/render_audit_pdf.py`. The spec is a single JSON object with three top-level keys:
  - `meta` — cover-page + footer metadata (`business_name`, `business_descriptor`, `business_location_label`, `contact_name`, optional `contact_role`, `address_lines` list, `phone`, `website`, `issue_date`, `order_number`, `auditor_org`, `auditor_contact_line`, `footer_brand_line`).
  - `exec_summary` — lede paragraph, `overall_grade` (letter + name + oneliner), `pillars` (6 rows: letter + title + text), `scores` (6 rows: pillar + score), `bottom_line` paragraph. Drives the Section 01 page automatically.
  - `sections` — list of section dicts for Business Snapshot through Glossary (ids 02 through 13). Each section: `id`, `title`, optional `question`, `blocks` (a list of typed blocks).

  Block types: `h3`, `paragraph`, `spacer` (height in points), `grade_banner` (letter + pillar + oneliner — use at top of each pillar section), `stat_callout` (list of [number, label] pairs), `data_table` (header + rows + optional col_widths in inches), `callout` (head + body list), `bullets` (items list), `centered` (text + optional color + size).

  Build the spec from the same in-memory synthesis data used to write the .md in Step 13 — both files are derived from the same source, so they cannot drift. Save to `/tmp/<business_name_slug>_audit.json`.

- **Step 14: Render PDF.** Run the BlitzMetrics-styled renderer via bash:
  ```
  python3 "$WORK_DIR/Claude Outputs/QuickAudit/render_audit_pdf.py" \
      --spec /tmp/<business_name_slug>_audit.json \
      --out  "$WORK_DIR/Claude Outputs/QuickAudit/Audits/<BusinessName>_Quick-Audit_v1.pdf"
  ```
  The renderer produces Dennis's structure (cover page with accent band, numbered section headers, colored grade boxes, stat callouts, page-numbered footer) in the Local Service Spotlight palette (deep teal `#1B4D5C`, medium teal `#22698A`, amber `#F5A623`, pale tint `#EAF2F8`). Grade-color mapping: A→deep teal, B→medium teal, C→amber, D→burnt orange, F→red. No styling decisions at audit time — the renderer is the single source of truth for visual presentation.

  If the renderer fails (malformed JSON, missing required field), the error message points at the offending block. Fix the spec and re-run; do not fall back to the generic `pdf` skill (it produces unstyled output that does not match the BlitzMetrics format).

- **Step 15: Qualification.** Apply the rubric in Agent Definition §5. This is independent of pillar grades.

Phase 1 advantage: Claude in Chrome is available in this Cowork context. Use it for Ads Transparency (Step 8 of the agent definition), GBP knowledge panel JS-rendered content (Step 1), and PSI when the API is blocked (Step 3). Phase 2 (Managed Agents) will need a different solution for browser fallback.

**HARD STOP — GBP NOT FOUND:**
The audit still proceeds — Footprint pillar hard-caps at F per Grading Approach §3. Executive Summary lede goes Pattern A. Ship the report.

**HARD STOP — WEBSITE UNREACHABLE:**
Same handling. Lede Pattern A. Website Performance and Keyword Rankings hard-cap at F.

**HARD STOP — AHREFS MCP FAILS:**
Proceed. Keyword Rankings pillar grades on what's observable from manual SERP scans + GBP signals. Note "Ahrefs DR / refdomains data unavailable" in Section 08. Pillar is not capped at F.

## Step 5: Deliver

Upload all three files to Google Drive in the folder `Maps Visibility / Quick Audits / <BusinessName>/` (create folder if missing):
- `<BusinessName>_Quick-Audit_v1.md` (the audit body)
- `<BusinessName>_Quick-Audit_v1.pdf` (the prospect deliverable)
- `<BusinessName>_Grading-Notes_v1.md` (internal — do not share externally)

Capture all three Drive URLs.

Create a Gmail draft addressed to the prospect with the cover-note text (subject/body per Agent Definition §6) and the PDF attached. The draft lives in Drafts for human review and send — the Gmail MCP wired today exposes `create_draft` but not auto-send. When a send-capable Gmail tool is added, this step flips from create_draft to send with no other changes.

If decision = HARD_PASS or SOFT_FAIL, create a Gmail draft for the team alert per Agent Definition §6. Recipients: `dylan@localservicespotlight.com`, `668sierra@gmail.com`. Subject prefix `[MVS Qualified]` or `[MVS Marginal]`. Body templates from companion plan document. Same draft-not-send constraint applies.

**HARD STOP — GMAIL DRAFT CREATION FAILS:**
Mark `Audit Status = email_failed`, `Notes = "<error message>"`. Do NOT retry from this scheduled task — the PDF has already shipped to Drive and the failure needs human review. Continue to Step 6.

## Step 6: Update Tracker

Write back to the row:
- `Place ID`
- `GBP Primary Category`
- `Enrichment JSON URL` (Drive)
- `Quick Audit MD URL` (Drive)
- `Quick Audit PDF URL` (Drive)
- `Grading Notes URL` (Drive)
- `Order Number`
- `Overall Grade` (letter + score, e.g., "D (38)")
- `Top 3 What-To-Fix-First (titles)` — first three rows of Tier 1 in the 90-Day Plan, action titles only, comma-separated
- `Audit Status` = `complete`
- `Qualification Status` = `complete`
- `Decision` = HARD_PASS / SOFT_FAIL / HARD_FAIL
- `Hard Fail Reasons` (if applicable)
- `Soft Fail Signals` (if applicable)
- `Routed` = `yes`
- `Routed At` = current timestamp

If any prior HARD STOP fired, still complete these writes — the audit shipped with partial data, the Tracker should reflect that.

If the Tracker doesn't yet have columns for `Quick Audit PDF URL`, `Grading Notes URL`, `Order Number`, or `Overall Grade`, create them on first run (Google Sheets MCP can add columns). Flag in the final report so Daniel knows the schema changed.

## Step 7: Final report

```
RUN COMPLETE — <date>
Pending rows found: <N>
Processed: <M>
Skipped (non-US or already complete): <S>
Email failures: <E>

For each processed row:
  - <Business Name> (<City, State>)
    Order #: <ORDER_NUMBER>
    Overall Grade: <LETTER> (<score>/100)
    Decision: <HARD_PASS | SOFT_FAIL | HARD_FAIL>
    Quick Audit PDF: <Drive URL>
    Grading Notes: <Drive URL>
    Email sent: yes
    Team alert: <yes/no>
```

If any row landed in `Audit Status = failed` or `email_failed`, list them at the bottom with error messages.

If there were no pending rows:
```
RUN COMPLETE — <date>
No pending Quick Audit submissions to process.
```

## Important notes

- Process all pending rows in a single run. Volume is low enough that daily processing handles the queue easily.
- If a row's status is anything other than `pending` or empty, leave it alone.
- Don't fabricate data. Grading Approach §3 handles unavailability (skip the signal, grade on observable, note in Grading Notes).
- The v1 versions of the reference files (`MVS_QuickAudit-Agent-Definition_v1.md`, `MVS_QuickAudit-Output-Template_v1.md`, `MVS_QuickAudit-Grading-Rubric_v1.md`) are marked SUPERSEDED. Do not read or apply them. (These files retain their MVS prefix as historical artifacts.)
- Companion plan: `QuickAudit-Automation-Plan_v1.md` is the architecture source of truth (Sheet schema, intake-zap contract, cloud-migration considerations). If it conflicts with this SKILL.md on workflow specifics, the SKILL.md wins for v2 format details, the plan wins for architecture.
- This skill currently runs as a daily-scheduled Cowork task on the operator's machine. A cloud-triggered deployment (so the audit ships within minutes of submission, with no local-machine dependency) is the next architectural step. The Agent Definition v2 was written to be portable to a cloud agent runtime when one is chosen.
