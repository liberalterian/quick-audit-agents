# Setup Guide

## 1. Google Cloud APIs

Enable these APIs in the Google Cloud project used for the workflow:

```bash
gcloud services enable \
  gmail.googleapis.com \
  gmailmcp.googleapis.com \
  drive.googleapis.com \
  drivemcp.googleapis.com \
  sheets.googleapis.com \
  places.googleapis.com \
  pagespeedonline.googleapis.com \
  --project=YOUR_PROJECT_ID
```

## 2. OAuth consent and client

Create an OAuth Desktop App client for local development and save the downloaded JSON to:

```text
./secrets/google-oauth-client.json
```

The first local run of `quick-audit-tools` will open an OAuth browser flow and write a token cache to:

```text
./secrets/google-oauth-token.json
```

## 3. Environment

```bash
cp .env.example .env
```

Fill in:

- `ANTHROPIC_API_KEY`
- `GOOGLE_OAUTH_CLIENT_ID`
- `GOOGLE_OAUTH_CLIENT_SECRET`
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_PLACES_API_KEY`
- `PAGESPEED_API_KEY`

## 4. Install package dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 5. Validate config

```bash
python scripts/validate_mcp_config.py .mcp.json
```

## 6. Test the local MCP server

```bash
python -m mcp.quick_audit_tools.server
```

Then connect from your MCP client.

## 7. Auth official remote MCPs

Use your client’s MCP auth command/UI for:

- `ahrefs`
- `google-gmail`
- `google-drive`

For Claude Code, the equivalent Ahrefs command is:

```bash
claude mcp add ahrefs https://api.ahrefs.com/mcp/mcp -t http
```

## 8. Gmail send activation checklist

Do not enable auto-send until all are true:

- Draft-only flow tested successfully.
- Recipient allowlist is configured.
- Max recipients is low.
- You have a test account or test recipient group.
- Audit log exists for sent email actions.

Then set:

```bash
ENABLE_GMAIL_SEND=true
```
