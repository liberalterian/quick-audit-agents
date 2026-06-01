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
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Full JSON string of the GCP service-account key. The local `quick-audit-tools` MCP server (`auth.py`) reads this to authenticate Sheets writeback, Places lookups, and PageSpeed calls. In cloud environments, paste the raw JSON value or base64-encode it depending on how your Routine's secret store handles multiline strings. Alternatively, set `GOOGLE_APPLICATION_CREDENTIALS` to a mounted file path if you prefer ADC-style auth. |
| `GOOGLE_SHEETS_SPREADSHEET_ID` | The ID portion of the Quick Audit Tracker Google Sheet URL (`https://docs.google.com/spreadsheets/d/<ID>/edit`). The local MCP server writes all Tracker columns to this sheet. The service account must have Editor access. |
| `GOOGLE_PLACES_API_KEY` | A Google Cloud API key with the **Places API (New)** enabled. Used by the local MCP server to resolve business name + city → Place ID and pull GBP details (category, claim status, review count, hours, phone). Restrict the key to the Places API and the Routine's egress IP range if possible. |
| `PAGESPEED_API_KEY` | A Google Cloud API key with the **PageSpeed Insights API** enabled. Used by the local MCP server to fetch mobile performance score and Core Web Vitals for the prospect's homepage. Can share a GCP project with the Places key but should be a separate key for easier rotation and quota tracking. |
| `AHREFS_MCP_KEY` | Bearer token for the Ahrefs hosted MCP (`https://api.ahrefs.com/mcp/mcp`). Passed via the `AHREFS_AUTH_HEADER` env var in `.mcp.json`. Used to pull domain rating, referring domains, organic keyword count, and estimated traffic during enrichment. |
| `ENABLE_GMAIL_SEND` | Controls whether the gated Gmail send tool in the local MCP server will actually deliver email. Set to **`false`** to keep everything in Drafts until live send is explicitly approved (see Part 5). The Gmail connector still creates drafts regardless of this value — this flag gates only the send action. |

**Optional ENV variables:**

| Variable | Default | Purpose |
|---|---|---|
| `GOOGLE_IMPERSONATE_SUBJECT` | unset | Email address to impersonate when sending Gmail via domain-wide delegation. Only needed if the service account uses DWD rather than a standard OAuth flow. |
| `QUICK_AUDIT_TRACKER_APPEND_RANGE` | `Audits!A:Z` | Sheet tab name and column range the MCP server appends to. Change this if you rename the Tracker tab. |
| `GOOGLE_DRIVE_AUDIT_FOLDER_ID` | unset | Google Drive folder ID where the audit `.md` and `.pdf` are saved. If unset, files are saved to the authenticated account's root Drive. |
| `GOOGLE_DRIVE_SHARED_DRIVE_ID` | unset | Shared Drive ID for the output folder. Required only if the target folder lives in a Shared Drive rather than My Drive. |

> **Never set `ANTHROPIC_API_KEY` as an MCP env var.** It is a Routine-level runtime credential managed by Anthropic's infrastructure.

### 1.4 Connectors

Enable all of the following in Routine settings → **Connectors** and complete the OAuth flow for each. These are official Google Workspace connectors — they are not configured in `.mcp.json`.

- **Google Gmail** — creates prospect cover-note drafts and team-alert drafts
- **Google Drive** — uploads and reads audit `.md`, `.pdf`, and grading-notes files
- **Google People** — optional contact/profile support; enable if the routing agent needs to look up contact records

The local `quick-audit-tools` MCP server handles **Sheets writeback**, **Places lookups**, and **PageSpeed** directly via API — those do not need connectors.

Remove any unused connectors.

---

## Part 2 — Testing with curl (before updating the Zap)

Validate the Routine end-to-end before wiring Zapier. This lets you confirm auth, MCP connectivity, and output format without touching the live Zap.

```bash
# Install deps (first time)
bash scripts/setup.sh

# Run automated tests
pytest tests/automated/

# Validate MCP config
python quick_audit_mcp/scripts/validate_mcp_config.py

# Fire the Routine directly with a test payload
# Set these in your shell first:
#   export QUICK_AUDIT_ROUTINE_FIRE_URL="https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire"
#   export QUICK_AUDIT_ROUTINE_TOKEN="<token from Routine trigger page>"
curl -X POST "$QUICK_AUDIT_ROUTINE_FIRE_URL" \
  -H "Authorization: Bearer $QUICK_AUDIT_ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "..."}'
```

Use `examples/apparel-junction-intake.md` or `examples/expert-services-intake.md` as your test payload content. See the full first-run validation checklist in Part 4 for what to verify after each test fire.

---

## Part 3 — Zapier configuration

### 3.1 Zap overview

**Trigger:** SPP form submission (Webhook or native SPP integration)  
**Action:** HTTP POST to the Routine `/fire` endpoint

### 3.2 Required secrets in Zapier

Store both values as **Zapier Storage** or **Secret Manager** entries — do not hardcode in the Zap:

| Zapier variable | Value |
|---|---|
| `QUICK_AUDIT_ROUTINE_FIRE_URL` | `https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire` — copy from the Routine's API trigger page |
| `QUICK_AUDIT_ROUTINE_TOKEN` | Bearer token shown on the same Routine trigger page |

### 3.3 Zap action — HTTP POST (Webhooks by Zapier)

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

### 3.4 Field mapping (SPP → Zapier → payload)

> **Before saving the Zap:** open the SPP service configuration and confirm each field name below matches the actual field key or label SPP sends in the webhook payload. SPP field names can vary between service configurations and the names below reflect the intended setup — verify them before going live.

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

### 3.5 Zap — store the session URL

After the fire succeeds, the response body includes `session_id` and `session_url`. Add a second Zap action to write these back to the Tracker row (Google Sheets → Update Row) so you can monitor the run.

### 3.6 Revenue band values (must match exactly)

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

## Part 4 — Google Sheets Tracker setup

### 4.1 Create the tab

Add a tab named **`Audits`** to the Maps Visibility Master Sheet (or create a dedicated sheet). Set `GOOGLE_SHEETS_SPREADSHEET_ID` to that sheet's ID.

### 4.2 Column schema

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

### 4.3 Share permissions

Grant the service account **Editor** access to the sheet and the Drive folder used for output.

---

## Part 5 — First-run validation checklist

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

## Part 6 — Activating live send

When you're ready to send to real prospects:

1. Set `ENABLE_GMAIL_SEND=true` in Routine ENV variables.
2. Do one supervised live run — confirm the prospect email lands correctly.
3. Update this doc noting the date send was enabled.

---

## Part 7 — Operating cadence

| Cadence | Task |
|---|---|
| Per-run | Check Tracker row for complete statuses + session URL |
| Daily | Review Failures tab — any row without `Audit Status: complete` within 30 min is a failure candidate |
| Weekly | Spot-check one delivered audit against the v2 format golden |
| Monthly | Review SOFT_FAIL rate. If SOFT_FAIL : HARD_PASS > 3:1, the qualification bands need tightening |

---

## Part 8 — Failure handling

| Failure | Behavior |
|---|---|
| Audit agent fails before enrichment | Qualification agent does not run. Tracker row logged. Manual recovery: retry or notify prospect. |
| Enrichment ready, qualification errors | Audit still ships with hard-fail cover-note language. Logged for review. |
| Routing timeout | Routing agent retries hourly. After 24h with no progress, row escalates in Notes column. |
| Missing optional data source (Ahrefs, PSI) | Noted inline in the audit; run continues. Does not block shipment. |
| Non-US business (state field mismatch) | Agent sends polite "not available in your region" email. Tracker row logged as hard-fail. |

---

## Part 9 — Secret rotation

Each credential lives in exactly one place. Rotating means updating the value there — no code changes, no redeployment. The reason for rotating each one is different, so the cadence and trigger vary:

| Secret | Stored in | How to rotate | Why / when to rotate |
|---|---|---|---|
| `QUICK_AUDIT_ROUTINE_TOKEN` | Zapier secret store | Regenerate in Routine → API trigger page, then update the Zapier storage value | Rotate if the token is exposed, if you off-board someone who had access to the Zap, or on a 90-day schedule. A new token is issued immediately; the old one stops working as soon as you save the new one. |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Routine ENV | Create a new key in GCP → IAM → Service Accounts → Manage Keys, update the Routine ENV value, then delete the old key in GCP | Rotate if the key is exposed or if GCP policy requires periodic rotation. Sheets, Places, and PageSpeed all use this credential, so update before deleting the old key or runs will fail mid-audit. |
| `GOOGLE_PLACES_API_KEY` | Routine ENV | Regenerate or create a new key in GCP Console → APIs & Services → Credentials, update Routine ENV | Rotate if the key appears in logs, is exposed in a client-side context, or if GCP sends an abuse alert. Places API keys are not scoped to a user — rotation is low-risk and fast. |
| `PAGESPEED_API_KEY` | Routine ENV | Same as Places key above | Same triggers as Places. Can be rotated independently since it's a separate key. |
| `AHREFS_MCP_KEY` | Routine ENV + Ahrefs Connector | Regenerate in Ahrefs dashboard → API keys, update both the Routine ENV value and the Connector credential in Routine settings | Rotate if the key is exposed or if an Ahrefs team member who held the key leaves. Both the ENV var and the Connector must be updated — the ENV feeds `.mcp.json` and the Connector is the fallback auth path. |
