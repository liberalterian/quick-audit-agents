# Integration Environment Reference

All variable names use **underscores** (dashes are invalid in shell/env variable names) and match the
names the code actually reads (`quick_audit_mcp/server.py`, `auth.py`, `.env.example`).

## Required runtime commands

- `python3` (>= 3.10)
- `pip`
- `curl`
- `jq`

## Required Python packages

Installed by `scripts/setup.sh` (do not assume only `reportlab`):

- `mcp` (MCP SDK)
- `httpx`
- `pydantic`
- `python-dotenv`
- `google-api-python-client`
- `google-auth`
- `google-auth-oauthlib`
- `reportlab` (PDF renderer)

## Required environment variables / secret-store entries

- `AHREFS_MCP_KEY`
- One Google auth option:
  - `GOOGLE_SERVICE_ACCOUNT_JSON` **or** `GOOGLE_APPLICATION_CREDENTIALS` (recommended for cloud), or
  - `GOOGLE_OAUTH_TOKEN_FILE` (pre-authorized token for local dev)
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_PLACES_API_KEY`
- `PAGESPEED_API_KEY`
- `QUICK_AUDIT_ROUTINE_FIRE_URL` and `QUICK_AUDIT_ROUTINE_TOKEN` (stored in the trigger caller, e.g. Zapier)

## Optional environment variables

- `GOOGLE_IMPERSONATE_SUBJECT` (only for Gmail send via domain-wide delegation)
- `QUICK_AUDIT_TRACKER_APPEND_RANGE` (default `Audits!A:Z`)
- `QUICK_AUDIT_ALLOWED_SEND_DOMAINS`, `QUICK_AUDIT_MAX_SEND_RECIPIENTS`
- `GOOGLE_DRIVE_AUDIT_FOLDER_ID`, `GOOGLE_DRIVE_SHARED_DRIVE_ID`
- `DEFAULT_PARTNER_ID`, `PARTNER_CONFIG_SHEET_ID` (multi-tenant, future)
- `ENABLE_GMAIL_SEND` (keep `false` until approved)

## Runtime configuration (not an MCP variable)

- `ANTHROPIC_API_KEY` — the Routine/agent runtime credential. Set at the routine level, never as an
  MCP-server env var and never committed.

## Do not commit

- API keys, OAuth client secrets, service-account JSON, routine bearer tokens, real prospect data.
  (See the repo-root `.gitignore`.)
