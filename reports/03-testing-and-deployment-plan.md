# Quick Audit System — Testing & Deployment Plan

**Companion to:** `01-audit-report.md`, `02-refactor-plan.md`
**Covers:** (1) how to run every markdown test in `tests/`, (2) fidelity comparison against Dan Pasker's original v1 system, (3) automated test additions, (4) a step-by-step cloud deployment guide.

> All 16 files in `tests/` are **manual / agent-executable checklists** (Purpose → Preconditions → Steps → Pass criteria → Fail criteria). They are run by a human operator or by Claude in a session — there is no test runner for them. The Python suite under `quick_audit_mcp/tests/` is the only automated piece today. This plan keeps the markdown suite, fixes its two defects, and adds real automation around it.

---

## Part 1 — How to use the `tests/` markdown suite

### 1.1 Execution model
Each test is run one of two ways:
- **Operator-driven:** a person reads Steps and checks Pass/Fail against the live system.
- **Agent-driven (recommended for regression):** paste the test file into a Claude Code session in the repo and say *"Execute this test against the current system and report PASS/FAIL per criterion with evidence."* Because the tests are structured, Claude can run the Steps (fire curl, run the renderer, grep output) and self-report.

Fix first (from the refactor): the duplicated **Preconditions** block becomes one `tests/README.md#common-preconditions` that every test references. Common preconditions are: repo cloned/loaded; `bash scripts/setup.sh` has run; credentials/secrets configured; for cloud tests, the routine exists with an API trigger.

### 1.2 Test groups, run order, and what each verifies

**Group A — Infrastructure / connectivity (run first, every deploy)**
| Test | Verifies | How to run |
|---|---|---|
| `mcp-connection-test.md` | Ahrefs/Gmail/Drive MCPs connect & authenticate; quick-audit-tools server starts | `/mcp` in a session; run harmless list/read calls; **add:** confirm `health_check.auth_mode != none` |
| `routine-api-trigger-test.md` | `/fire` accepts the POST with headers + `text` body; returns session id/url | the curl from §4.4; expect 200 + `claude_code_session_id` |
| `google-places-direct-api-test.md` | Places Text Search + Place Details via the server | call `resolve_business_place` then `get_place_details`; **fix:** env var is `GOOGLE_PLACES_API_KEY` (not `GOOGLE-MAPS-API-KEY`) |
| `google-sheets-tracker-writeback-test.md` | Tracker row append/update writes to the right row only | `append_quick_audit_tracker_row` / `update_quick_audit_tracker_range` against a **test** spreadsheet |

**Group B — Artifact correctness (run on any content/renderer change)**
| Test | Verifies | How to run |
|---|---|---|
| `audit-spec-schema-test.md` | spec JSON has `meta`/`exec_summary`/`sections`, known block types, nothing after Glossary | validate `examples/sample-audit-spec-json.md` shape (automate via §3.3) |
| `pdf-renderer-smoke-test.md` | renderer produces a non-empty styled PDF with cover + Exec Summary | run `render-audit-pdf.py --spec … --out …`; **fix path to** `${CLAUDE_SKILL_DIR}` form |
| `grading-notes-completeness-test.md` | six pillars each have signals + anchor + grade + rationale; overall math; hard-caps + data-unavailable present | open Grading Notes, check against `evals/anchored-grading-rubric.md` |

**Group C — Format-fidelity regressions (the v2 discipline)**
| Test | Verifies |
|---|---|
| `no-glass-half-full-regression-test.md` | no customer audit contains "Glass Half Full" (grep md + PDF text + templates) |
| `source-doc-consistency-test.md` | output section order/grading flow still match `source-docs`; changelog records intentional drift |
| `dash-case-path-regression-test.md` | naming convention — **MUST be fixed first** to exclude `quick_audit_mcp/**` and `*.py` (H-1), else it false-fails |

**Group D — Logic / pipeline behavior**
| Test | Verifies |
|---|---|
| `qualification-rubric-test-cases.md` | MVS aggregation (any hard-fail→HARD-FAIL; soft-fail→SOFT-FAIL; all pass→HARD-PASS); independence from pillar grades |
| `routing-delivery-test.md` | Drive upload, draft contents+attachment, no team alert on HARD-FAIL, Grading Notes never sent to prospect, Tracker writeback |
| `legacy-fallback-smoke-test.md` | `legacy-quick-audit` runs, calls the shared renderer, keeps v2 structure |

**Group E — End-to-end & golden (run before go-live and on releases)**
| Test | Verifies |
|---|---|
| `expert-services-smoke-test.md` | cold-submission produces all artifacts, sourced, no fabrication — **now backed by the real Expert Services payload** |
| `apparel-junction-golden-test.md` | reproduces Apparel Junction structure + grade bands — **now backed by the real golden** (see Part 2) |
| `end-to-end-cloud-smoke-test.md` | full trigger→Tracker writeback in the cloud routine, RUN COMPLETE emitted |

**Recommended sequence:** A → B → C → D → E. A failure in A blocks the rest.

### 1.3 Defects to fix in the suite before relying on it
1. `dash-case-path-regression-test.md` — exclude Python paths (H-1).
2. `google-places-direct-api-test.md` — `GOOGLE_PLACES_API_KEY` (H-2).
3. Provide the missing fixtures: add `examples/apparel-junction-intake.md` and `examples/expert-services-intake.md`; import `tests/golden/` (H-3).
4. Replace 16× duplicated Preconditions with `tests/README.md` reference (M-7).

---

## Part 2 — Fidelity comparison against the original (Dan Pasker's v1 system)

**Source of truth:** `\\wsl.localhost\Ubuntu-22.04\home\liberalterian\Projects\QuickAudit-System-v1\` — imported to `tests/golden/`. The original was built by/for **Dan Pasker** (stakeholder/owner), authored by Daniel Goodrich, replicating Dennis Yu / BlitzMetrics' published audit.

### 2.1 The critical split (verified from the golden files)
Fidelity is **two different comparisons**, because the v1 sample outputs are not uniform:

| Golden artifact | Use as golden for | Do NOT use for |
|---|---|---|
| `ApparelJunction_Grading-Notes_v1.md` | **Grades** (Footprint 42, Reviews 55, Social 38, Website 40, Brand Search 35, Keywords 18 → **D 38**) | — |
| `ApparelJunction_Quick-Audit_v1.md` | (reference only) | **Format** — it is v1-style: contains "Glass Half Full" (line 437), per-pillar "Revenue translation:" (lines 107,154,…), **13** glossary terms |
| `Apparel_Junction_Quick_Audit.pdf` (Dennis) | **Canonical format** (section order, no GHF/RT, 8 glossary) | — |
| `ExpertServicesUtah_Grading-Notes_v1.md` | **Grades** (40/75/45/55/45/45 → **C 51**) + the live-GBP regrade lesson | — |
| `ExpertServicesUtah_Quick-Audit_v1.md` | **v2 format golden** (no GHF, no RT, **8** glossary terms) + **grades** | — |
| `ExpertServicesUtah_Quick-Audit_v1.pdf` | rendered-PDF visual reference | — |

> **Do not "fix" a new v2 run to match the Apparel Junction markdown's extra sections.** If a v2 audit reproduces Glass Half Full or Revenue Translation, that's a *regression*, not fidelity — the original v1 markdown had them and v2 deliberately stripped them.

### 2.2 Grade-fidelity test (calibration / golden)
**Goal:** a faithful run reproduces the anchor grades within tolerance.
1. Run the pipeline on `examples/apparel-junction-intake.md`.
2. Compare the produced Grading Notes pillar scores to the golden: **exact match expected** for Apparel Junction (it is the calibration anchor — the v1 notes themselves state "every grade matches Dennis's published values exactly").
3. For Expert Services (a cold run, not an anchor): expect **overall within ±1 letter / ±5 points** and per-pillar within one band; the *reasoning structure* (5–10 signals + anchor + rationale) must be present.
4. **PASS:** Apparel Junction overall = D, pillars = 42/55/38/40/35/18 (±2 each, overall must round to D 38). Expert Services overall = C (49–55).
5. **FAIL:** overall letter drifts without a documented data difference; pillar missing signals/anchor/rationale.

### 2.3 Format-fidelity test
Compare a fresh v2 audit (and the Expert Services golden) against Dennis's PDF / v2 rules:
- Section order exactly 01→13, **ends at Glossary** (no section after).
- **Zero** occurrences of "Glass Half Full" and "Revenue translation:" (grep).
- Glossary has **exactly 8** terms (NAP, DR, E-E-A-T, GBP, Knowledge Panel, Local Pack/Map Pack, LSA, Schema).
- Required per-pillar tables/callouts present (NAP table, review stat callout + competitor table, social channel inventory, website architecture table, brand SERP table, Ahrefs stat callout + keyword tables) per `source-docs/quick-audit-output-template-v2.md`.
- Cover page metadata + page-numbered footer + grade color boxes (renderer).
- **PASS:** all of the above; **FAIL:** any forbidden section appears, glossary ≠ 8, or a required pillar structure is missing.

### 2.4 Renderer-fidelity (regression) test
- Run `render-audit-pdf.py` on the **Expert Services golden spec** (rebuild it from `build-audit-spec-example.py`, whose docstring says it exists "to verify the generalized renderer produces the same PDF as the hardcoded v1 script").
- Compare the output PDF to `tests/golden/expert-services/ExpertServicesUtah_Quick-Audit_v1.pdf`: same page count, same section headers, same palette (deep teal #1B4D5C / med teal #22698A / amber #F5A623), grade color mapping (A teal, B med-teal, C amber, D burnt-orange, F red).
- Automate the structural part by extracting PDF text and diffing headings (see §3.4); visual styling is a human spot-check.

### 2.5 Process-fidelity (the v1 lesson)
The Expert Services notes record that skipping the live Knowledge-Panel navigation caused a one-letter miss (Reviews C 55 → B 75 after live check). **Test:** confirm the v2 enrichment step performs the live GBP review-count/Knowledge-Panel check as a *default step* and that Reviews grades reflect live counts. Build the CLAUDE.md/enrichment change from `02-…` §F, then verify.

---

## Part 3 — Automated tests to add (`tests/automated/`)
Today only `quick_audit_mcp/tests/test_mcp_config.py` is automated (and it doesn't import the server). Add, runnable via `pytest`:
1. **`test_server_imports.py`** — `import quick_audit_mcp.server` (catches C-1 forever).
2. **`test_mcp_config_shape.py`** — assert `oauth.scopes` is a string, no `"enabled"` key, no duplicate URLs, required servers present (replaces the echo-style assertions in `validate_mcp_config.py`).
3. **`test_audit_spec_schema.py`** — JSON-schema-validate spec files: top-level keys, known block `type`s, no section after `id:"13"` (automates `audit-spec-schema-test.md`).
4. **`test_forbidden_sections.py`** — grep generated/sample audit `.md` for "Glass Half Full" / "Revenue translation" / glossary-term-count==8 (automates Group C).
5. **`test_qualification_aggregation.py`** — table-drive the MVS rules from `mvs-qualification-rubric.md` (automates `qualification-rubric-test-cases.md`).
6. **`test_renderer_smoke.py`** — render the Expert Services spec to a temp PDF; assert exit 0, non-empty, page count matches golden.
7. **`test_grades_golden.py`** — parse Apparel Junction Grading Notes the pipeline produces and assert the six anchor scores.

Wire `pytest quick_audit_mcp/tests tests/automated` into `scripts/setup.sh`'s verify step and (optionally) a GitHub Action so the routine never deploys a broken build.

---

## Part 4 — Step-by-step deployment guide (API-triggered Claude Routine)

Reconciles the Gemini blueprint (repo structure, `CLAUDE.md`, `setup.sh`) with the **official** routines contract (`/fire` endpoint, `text` payload). Prerequisite: complete refactor Phases 0–5 (`02-…`).

### 4.1 Repository prep (one-time)
1. Land the `.claude/` layout, `CLAUDE.md`, `scripts/setup.sh`, renamed `quick_audit_mcp/`, fixed `.mcp.json`, imported `tests/golden/`.
2. Run locally: `bash scripts/setup.sh && pytest quick_audit_mcp/tests tests/automated` — all green.
3. Commit and push to GitHub.

### 4.2 Google credentials (headless — C-2)
1. Create a **service account**; download its JSON key.
2. Enable APIs: Sheets, Drive, Places, PageSpeed (Gmail draft stays on the official Gmail MCP).
3. Share the **Tracker spreadsheet** and the **Drive audit folder** with the service-account email.
4. Store the key as a routine **env var** (`GOOGLE_SERVICE_ACCOUNT_JSON` or `GOOGLE_APPLICATION_CREDENTIALS`), plus `GOOGLE_SHEETS_SPREADSHEET_ID`, `GOOGLE_PLACES_API_KEY`, `PAGESPEED_API_KEY`, `AHREFS_MCP_KEY`. Keep `ENABLE_GMAIL_SEND=false`.

### 4.3 Create the routine (claude.ai/code/routines → New routine → **Remote**)
- **Task prompt (short, dynamic):** *"Read CLAUDE.md and run the Quick Audit pipeline. The intake payload is the JSON string in the trigger `text` field. Follow all output rules; emit RUN COMPLETE."*
- **Repository:** link the GitHub repo (install the Claude GitHub App on it).
- **Environment:** Network access **Trusted** (add Google/Ahrefs/PageSpeed/Places hosts if blocked — Trusted already allows Google APIs; verify `places.googleapis.com`, `pagespeedonline` reachable, else set Custom/Full). **Setup command:** `bash scripts/setup.sh`. Add the env vars from 4.2.
- **Connectors:** include only Ahrefs + Google Gmail + Google Drive MCPs the run needs; remove the rest.
- **Trigger:** Add trigger → **API** → Save → **Generate token** (copy once) → copy the `/fire` URL.

### 4.4 Fire it (official contract — note: `text`, not `payload`)
```bash
curl -X POST "https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire" \
  -H "Authorization: Bearer $QUICK_AUDIT_ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text":"{\"event-type\":\"quick-audit-intake\",\"submission-id\":\"qa-test-0001\",\"business-name\":\"Example Services\",\"website\":\"https://example-services.test\",\"primary-city\":\"Denver\",\"state\":\"CO\",\"annual-revenue-band\":\"$2M-5M\",\"contact-name\":\"Jane Owner\",\"contact-email\":\"jane@example-services.test\",\"tracker-row-id\":\"tracker-row-0001\",\"partner-id\":\"default\"}"}'
```
> The intake JSON is **stringified inside `text`** — the routine does not parse a structured `payload`. (Gemini's `payload`/`https://claude.ai` example is illustrative; use the above.) Expect `{"claude_code_session_id":...,"claude_code_session_url":...}`.

### 4.5 First-run validation (gates go-live)
Run in order and require PASS:
1. `routine-api-trigger-test.md` → 200 + session URL.
2. `mcp-connection-test.md` → all MCPs connected; `health_check.auth_mode == service_account`.
3. `end-to-end-cloud-smoke-test.md` on a **safe test domain** → audit `.md` + PDF + Grading Notes + enrichment created; prospect **draft** with PDF; Tracker row complete + session URL; **RUN COMPLETE** emitted; **no** Glass Half Full / Revenue Translation.
4. Fidelity gates: `apparel-junction-golden-test.md` (grade match) + format-fidelity (§2.3).
5. Confirm in the run transcript that the orchestrator delegated to the three sub-agents (green status ≠ success — read the transcript).

### 4.6 Wire the real trigger & guardrails
- Point Zapier (or the intake backend) at the `/fire` URL with the token in a secret store; map the SPP form → `text` JSON.
- Keep drafts-first (`ENABLE_GMAIL_SEND=false`) until the Gmail-send activation checklist (`quick_audit_mcp/docs/setup.md` §8) is signed off.
- Store the routine URL/token, service-account key, and spreadsheet ID outside the repo (root `.gitignore` covers `.env`/`secrets/`).
- Daily routine-run cap applies; one-off test fires don't count. Green run status only means "no infra error" — always read the transcript on first runs.

### 4.7 Rollback / safety
- Pause the routine (Repeats toggle) to stop all triggers without deleting config.
- Branch-push is restricted to `claude/`-prefixed branches by default — leave it that way (no need for unrestricted pushes here).
- If a run misbehaves, the session is inspectable at its `claude_code_session_url`; fix forward in the repo and re-fire.

---

## Appendix — Quick test-to-criteria map (for CI dashboards)
| Layer | Markdown test | Automated equivalent (Part 3) |
|---|---|---|
| Import/health | mcp-connection | test_server_imports, health_check.auth_mode |
| Config | (validator) | test_mcp_config_shape |
| Spec | audit-spec-schema | test_audit_spec_schema |
| Format | no-glass-half-full, source-doc-consistency | test_forbidden_sections |
| Logic | qualification-rubric | test_qualification_aggregation |
| Render | pdf-renderer-smoke | test_renderer_smoke |
| Grades | apparel-junction-golden | test_grades_golden |
| E2E | end-to-end-cloud | (manual cloud fire) |
