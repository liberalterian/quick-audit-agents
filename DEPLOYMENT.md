# Quick Audit System — Deployment & Configuration Guide

**Runtime:** Claude Code Routine (cloud, API-triggered)  
**Trigger caller:** Zapier  
**Version:** v2.1.0

---

## Architecture overview

```
SPP Form Submit
      │
      ▼
  Zapier Zap
  (Webhook → HTTP POST)
      │
      ▼  POST /v1/claude_code/routines/<trig_id>/fire
  Claude Routine
  "Quick Audit Runner"
      │
      ├─ quick-audit-orchestrator-agent (main session, CLAUDE.md-directed)
      │       ├─ quick-audit-intake skill
      │       ├─ quick-audit-agent subagent
      │       │       ├─ quick-audit-enrichment
      │       │       ├─ quick-audit-grading
      │       │       ├─ quick-audit-report
      │       │       └─ quick-audit-pdf-render
      │       ├─ qualification-agent subagent
      │       │       └─ quick-audit-qualification
      │       └─ routing-agent subagent
      │               └─ quick-audit-routing
      │
      ▼
  Google Drive (PDF + .md)
  Gmail Draft (prospect-facing)
  Google Sheets Tracker writeback
  Conditional team alert email
```

---

## Part 1 — Claude Routine setup

### 1.1 Create the routine

1. Open [claude.ai/code](https://claude.ai/code) → **Routines** → **New Routine**.
2. **Name:** `Quick Audit Runner`
3. **Trigger type:** API
4. **Repository:** connect this repo via the Claude GitHub App.  
   Grant read access to `main`. The app auto-loads `CLAUDE.md` on every run.
5. **Prompt (keep it short — CLAUDE.md does the directing):**
   ```
   Read CLAUDE.md and run the Quick Audit pipeline on the intake payload in the trigger `text` field. Follow all output rules; emit RUN COMPLETE.
   ```
6. **Build / Setup Command:**
   ```
   bash scripts/setup.sh
   ```
   This installs Python deps (mcp, httpx, pydantic, python-dotenv, google-api-python-client, google-auth, google-auth-oauthlib, reportlab) and runs the import smoke-check.

### 1.2 Cloud environment settings

| Setting | Value |
|---|---|
| Network access | Trusted (widens to Custom/Full if `places.googleapis.com` or `pagespeedonline.googleapis.com` is blocked) |
| Timeout | 30 min (audits run 10–20 min end-to-end) |

### 1.3 Required ENV variables (set in Routine settings, never committed)

| Variable | Description |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Full JSON of the service-account key, base64-encoded or raw string — auth.py reads it. Alternatively set `GOOGLE_APPLICATION_CREDENTIALS` to a mounted path. |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | ID of the Quick Audit Tracker Google Sheet |
| `GOOGLE_PLACES_API_KEY` | Google Places API key |
| `PAGESPEED_API_KEY` | PageSpeed Insights API key |
| `AHREFS_MCP_KEY` | Ahrefs MCP bearer token |
| `ENABLE_GMAIL_SEND` | **`false`** — keep draft-only until send is explicitly approved |

**Optional ENV variables:**

| Variable | Default | Purpose |
|---|---|---|
| `GOOGLE_IMPERSONATE_SUBJECT` | unset | Gmail send via domain-wide delegation |
| `QUICK_AUDIT_TRACKER_APPEND_RANGE` | `Audits!A:Z` | Tracker tab + range |
| `GOOGLE_DRIVE_AUDIT_FOLDER_ID` | unset | Drive folder for PDF + .md output |
| `GOOGLE_DRIVE_SHARED_DRIVE_ID` | unset | Shared Drive ID if not My Drive |
| `ENABLE_GMAIL_SEND` | `false` | Flip to `true` only after send approval |

> **Never set `ANTHROPIC_API_KEY` as an MCP env var.** It is a Routine-level runtime credential managed by Anthropic's infrastructure.

### 1.4 Connectors

Enable all three in Routine settings → **Connectors**:

- **Google Gmail** — authenticate with the service account or OAuth flow  
- **Google Drive** — same credential as Gmail  
- **Ahrefs** — API key connector

Remove any unused connectors.

---

## Part 2 — Zapier configuration

### 2.1 Zap overview

**Trigger:** SPP form submission (Webhook or native SPP integration)  
**Action:** HTTP POST to the Routine `/fire` endpoint

### 2.2 Required secrets in Zapier

Store both values as **Zapier Storage** or **Secret Manager** entries — do not hardcode in the Zap:

| Zapier variable | Value |
|---|---|
| `QUICK_AUDIT_ROUTINE_FIRE_URL` | `https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire` — copy from the Routine's API trigger page |
| `QUICK_AUDIT_ROUTINE_TOKEN` | Bearer token shown on the same Routine trigger page |

### 2.3 Zap action — HTTP POST (Webhooks by Zapier)

**Method:** POST  
**URL:** `{{QUICK_AUDIT_ROUTINE_FIRE_URL}}`

**Headers:**

```
Authorization: Bearer {{QUICK_AUDIT_ROUTINE_TOKEN}}
anthropic-beta: experimental-cc-routine-2026-04-01
anthropic-version: 2023-06-01
Content-Type: application/json
```

**Body (raw JSON):**

```json
{
  "text": "{\"event-type\":\"quick-audit-intake\",\"submission-id\":\"{{submission_id}}\",\"business-name\":\"{{business_name}}\",\"website\":\"{{website}}\",\"primary-city\":\"{{primary_city}}\",\"state\":\"{{state}}\",\"annual-revenue-band\":\"{{annual_revenue_band}}\",\"contact-name\":\"{{contact_name}}\",\"contact-email\":\"{{contact_email}}\",\"contact-phone\":\"{{contact_phone}}\",\"tracker-row-id\":\"{{tracker_row_id}}\",\"partner-id\":\"default\"}"
}
```

Map each `{{placeholder}}` to the corresponding SPP field in Zapier's field mapper. The `text` value must be a **stringified JSON string** — not a nested object. The Routine parses `text` verbatim.

### 2.4 Field mapping (SPP → Zapier → payload)

| Payload key | SPP field | Required |
|---|---|---|
| `submission-id` | SPP submission ID | Yes |
| `business-name` | Business name | Yes |
| `website` | Primary website URL | Yes |
| `primary-city` | Primary city | Yes |
| `state` | State (select) | Yes |
| `annual-revenue-band` | Annual revenue (range select) | Yes |
| `contact-name` | Contact name | Yes |
| `contact-email` | Contact email | Yes |
| `contact-phone` | Contact phone | Optional |
| `tracker-row-id` | Row ID if pre-written to Tracker; omit or use submission-id | Optional |
| `partner-id` | `"default"` unless multi-tenant | Optional |

### 2.5 Zap — store the session URL

After the fire succeeds, the response body includes `session_id` and `session_url`. Add a second Zap action to write these back to the Tracker row (Google Sheets → Update Row) so you can monitor the run.

### 2.6 Revenue band values (must match exactly)

SPP select options must match the strings the Qualification Agent reads:

```
<$500K
$500K-1M
$1M-1.5M
$1.5M-2M
$2M-5M
$5M-10M
$10M+
```

---

## Part 3 — Google Sheets Tracker setup

### 3.1 Create the tab

Add a tab named **`Audits`** to the Maps Visibility Master Sheet (or create a dedicated sheet). Set `GOOGLE_SHEETS_SPREADSHEET_ID` to that sheet's ID.

### 3.2 Column schema

| Column | Set by |
|---|---|
| Submission ID | Zap / intake |
| Submitted At | Zap / intake |
| Business Name | Intake |
| Website | Intake |
| City, State | Intake |
| Contact Name | Intake |
| Contact Email | Intake |
| Contact Phone | Intake |
| Place ID | Audit agent (Step 1) |
| GBP Primary Category | Audit agent (Step 1) |
| Enrichment Status | Audit agent (`pending` → `enriching` → `ready` → `failed`) |
| Enrichment JSON URL | Audit agent (Step 7) |
| Audit Status | Audit agent (`pending` → `rendering` → `complete` → `failed`) |
| Quick Audit .md URL | Audit agent (Step 9) |
| Top 3 What-To-Fix-First | Audit agent |
| Qualification Status | Qualification agent (`pending` → `complete` → `error`) |
| Decision | Qualification agent (`HARD_PASS` / `SOFT_FAIL` / `HARD_FAIL`) |
| Hard Fail Reasons | Qualification agent |
| Soft Fail Signals | Qualification agent |
| Revenue (self-reported) | Intake |
| Routed | Routing agent (`y`/`n`) |
| Routed At | Routing agent |
| Session URL | Zap writeback |
| Notes | Manual |

### 3.3 Share permissions

Grant the service account **Editor** access to the sheet and the Drive folder used for output.

---

## Part 4 — First-run validation checklist

Run this after initial setup before turning on the production Zap.

- [ ] Fire with `examples/sample-intake-payload.md` content — Routine returns a `session_url`
- [ ] Open the session URL — confirm run completes without a red error banner
- [ ] `health_check.auth_mode == service_account` in the run log
- [ ] Ahrefs, Gmail, and Drive connectors show green in the session
- [ ] Grading Notes file created (internal, not shipped to prospect)
- [ ] Audit markdown + PDF created in Drive
- [ ] Gmail **draft** created with PDF attached, addressed to the test contact email
- [ ] Tracker row shows `Audit Status: complete`, `Qualification Status: complete`, `Routed: y`
- [ ] Audit contains **exactly 13 sections** ending at the Glossary — no "Glass Half Full" section, no per-pillar "Revenue translation:" paragraphs
- [ ] Glossary has **exactly 8 terms**: NAP, DR, E-E-A-T, GBP, Knowledge Panel, Local Pack/Map Pack, LSA, Schema
- [ ] `ENABLE_GMAIL_SEND` is `false` — no live send occurred

Read the full run transcript. Green status means "no infra error" — it does not mean the audit content is correct. Spot-check the audit against `tests/golden/expert-services/ExpertServicesUtah_Quick-Audit_v1.md` (C 51 overall, v2 format).

---

## Part 5 — Activating live send

When you're ready to send to real prospects:

1. Set `ENABLE_GMAIL_SEND=true` in Routine ENV variables.
2. Do one supervised live run — confirm the prospect email lands correctly.
3. Update this doc noting the date send was enabled.

---

## Part 6 — Operating cadence

| Cadence | Task |
|---|---|
| Per-run | Check Tracker row for complete statuses + session URL |
| Daily | Review Failures tab — any row without `Audit Status: complete` within 30 min is a failure candidate |
| Weekly | Spot-check one delivered audit against the v2 format golden |
| Monthly | Review SOFT_FAIL rate. If SOFT_FAIL : HARD_PASS > 3:1, the qualification bands need tightening |

---

## Part 7 — Failure handling

| Failure | Behavior |
|---|---|
| Audit agent fails before enrichment | Qualification agent does not run. Tracker row logged. Manual recovery: retry or notify prospect. |
| Enrichment ready, qualification errors | Audit still ships with hard-fail cover-note language. Logged for review. |
| Routing timeout | Routing agent retries hourly. After 24h with no progress, row escalates in Notes column. |
| Missing optional data source (Ahrefs, PSI) | Noted inline in the audit; run continues. Does not block shipment. |
| Non-US business (state field mismatch) | Agent sends polite "not available in your region" email. Tracker row logged as hard-fail. |

---

## Part 8 — Local development / testing

```bash
# Install deps
bash scripts/setup.sh

# Run automated tests
pytest tests/automated/

# Validate MCP config
python quick_audit_mcp/scripts/validate_mcp_config.py

# Manual fire (local curl)
# Copy sample-zapier-routine-request.md and replace env vars
curl -X POST "$QUICK_AUDIT_ROUTINE_FIRE_URL" \
  -H "Authorization: Bearer $QUICK_AUDIT_ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "..."}'
```

Use `examples/apparel-junction-intake.md` or `examples/expert-services-intake.md` as test payloads.

---

## Part 9 — Secret rotation

Rotate these credentials independently — no code changes required, just update the values in their respective stores:

| Secret | Stored in | Rotation |
|---|---|---|
| `QUICK_AUDIT_ROUTINE_TOKEN` | Zapier secret store | Rotate in Routine → regenerate → update Zapier |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Routine ENV | Rotate key in GCP → update Routine ENV |
| `GOOGLE_PLACES_API_KEY` | Routine ENV | Rotate in GCP Console |
| `PAGESPEED_API_KEY` | Routine ENV | Rotate in GCP Console |
| `AHREFS_MCP_KEY` | Routine ENV + Connector | Rotate in Ahrefs dashboard |
