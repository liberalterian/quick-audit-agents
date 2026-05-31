# Claude Routine Setup Guide

## Goal

Create one API-triggered Claude Routine named `Quick Audit Runner` that runs this repo unattended.

## Routine configuration

- **Repository:** this repository (install the Claude GitHub App on it).
- **Prompt (brief, dynamic):**
  > Read CLAUDE.md and run the Quick Audit pipeline on the intake payload in the trigger `text` field. Follow all output rules; emit RUN COMPLETE.
  Do NOT paste an agent file as the prompt — `CLAUDE.md` is auto-loaded and directs the orchestration.
- **Trigger:** API.
- **Cloud environment:**
  - **Build/Setup Command:** `bash scripts/setup.sh` (installs the MCP deps + reportlab and runs the import smoke check).
  - **Network access:** Trusted (verify `places.googleapis.com`, `pagespeedonline.googleapis.com`, Ahrefs reachable; widen to Custom/Full if blocked).
  - **ENV variables:** service-account JSON (`GOOGLE_SERVICE_ACCOUNT_JSON` or `GOOGLE_APPLICATION_CREDENTIALS`), `GOOGLE_SHEETS_SPREADSHEET_ID`, `GOOGLE_PLACES_API_KEY`, `PAGESPEED_API_KEY`, `AHREFS_MCP_KEY`, `ENABLE_GMAIL_SEND=false`. See `references/integration-environment-reference.md`.
- **Connectors:** enable the **Google Gmail** and **Google Drive** connectors; authenticate **Ahrefs**. Remove unused connectors.

## API trigger request (official contract)

POST to the per-routine `/fire` endpoint. The intake payload is a **stringified JSON in `text`**
(the routine does not parse a structured `payload`). See `examples/sample-zapier-routine-request.md`.

```json
{ "text": "{\"event-type\":\"quick-audit-intake\",\"submission-id\":\"qa-0001\", ...}" }
```

Headers: `Authorization: Bearer <token>`, `anthropic-beta: experimental-cc-routine-2026-04-01`,
`anthropic-version: 2023-06-01`, `Content-Type: application/json`.

## Required secret storage (outside the repo)

- Routine fire URL + bearer token.
- Google **service-account** key JSON (shared with the Tracker spreadsheet + Drive folder).
- Google Places + PageSpeed API keys; Ahrefs key.

## First-run validation

1. Fire with `examples/sample-intake-payload.md` content → routine returns a session URL.
2. `health_check.auth_mode == service_account`; Ahrefs/Gmail/Drive connected.
3. Audit markdown + PDF + Grading Notes + enrichment created; prospect **draft** with PDF attached.
4. Tracker row shows complete statuses + the session URL.
5. No final audit contains "Glass Half Full" or per-pillar "Revenue Translation".
6. Read the run transcript — green status only means "no infra error", not task success.
