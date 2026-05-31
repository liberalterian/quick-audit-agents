# Setup Guide

## 1. Google Cloud APIs

Enable the APIs the server actually calls (there are **no** `gmailmcp`/`drivemcp` Google APIs —
Gmail drafts and Drive are claude.ai connectors, not googleapis MCP endpoints):

```bash
gcloud services enable \
  sheets.googleapis.com \
  places.googleapis.com \
  pagespeedonline.googleapis.com \
  gmail.googleapis.com \
  drive.googleapis.com \
  --project=YOUR_PROJECT_ID
```

## 2. Credentials (headless-safe — see `auth.py`)

**Cloud routine (recommended): a service account.**
1. Create a service account; download its JSON key.
2. Share the **Quick Audit Tracker spreadsheet** and the **Drive audit folder** with the
   service-account email (so Sheets/Drive calls are authorized without a browser).
3. Provide the key to the server as `GOOGLE_SERVICE_ACCOUNT_JSON` (inline JSON) or
   `GOOGLE_APPLICATION_CREDENTIALS` (path). Gmail-send as a user additionally needs domain-wide
   delegation + `GOOGLE_IMPERSONATE_SUBJECT` (keep send disabled until approved).

**Local dev (no service account): a pre-authorized token**, or set
`QUICK_AUDIT_ALLOW_INTERACTIVE_OAUTH=true` and provide `GOOGLE_OAUTH_CLIENT_SECRETS_FILE` to run the
one-time browser flow, which writes `GOOGLE_OAUTH_TOKEN_FILE`. Never enable interactive OAuth in the cloud.

## 3. Environment

```bash
cp quick_audit_mcp/.env.example quick_audit_mcp/.env
```

Fill in `AHREFS_MCP_KEY`, one Google auth option, `GOOGLE_SHEETS_SPREADSHEET_ID`,
`GOOGLE_PLACES_API_KEY`, `PAGESPEED_API_KEY`.

## 4. Install dependencies

```bash
bash scripts/setup.sh          # installs requirements + reportlab, runs the import smoke check
```

## 5. Validate config

```bash
python quick_audit_mcp/scripts/validate_mcp_config.py .mcp.json
```

## 6. Run the local MCP server

```bash
python -m quick_audit_mcp.server
```

Then connect from your MCP client. (Launch from the repo root.)

## 7. Hosted MCP + connectors

- **Ahrefs** (hosted MCP) — configured in `.mcp.json`; authenticate via your client's MCP auth.
  Claude Code equivalent: `claude mcp add ahrefs https://api.ahrefs.com/mcp/mcp -t http`.
- **Gmail drafts** and **Google Drive** — enable the official Google Workspace **connectors** in the
  Claude Routine (Settings → Connectors), not as `.mcp.json` HTTP servers.

## 8. Gmail send activation checklist

Do not enable auto-send until all are true:

- Draft-only flow tested successfully.
- Recipient allowlist (`QUICK_AUDIT_ALLOWED_SEND_DOMAINS`) configured.
- `QUICK_AUDIT_MAX_SEND_RECIPIENTS` is low.
- A test account/recipient group exists.
- An audit log of sent messages exists.

Then set `ENABLE_GMAIL_SEND=true`.
