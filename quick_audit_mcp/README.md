# Quick Audit MCP (`quick_audit_mcp`)

Local **stdio** MCP server for the integration gaps not covered by hosted MCPs or claude.ai connectors:

- Google Sheets Quick Audit Tracker writes — `append_quick_audit_tracker_row`, `update_quick_audit_tracker_range`
- Gated Gmail auto-send — `send_gmail_message` (disabled by default)
- Google Places — `resolve_business_place`, `get_place_details`
- PageSpeed Insights — `run_pagespeed_insights`
- `health_check` (reports config presence + `auth_mode`, no secrets)

Gmail **drafts** and Google **Drive** persistence are handled by the official Google Workspace
**connectors** enabled on the Claude Routine (or your Claude Code session), not by this server.
Ahrefs uses its hosted MCP (`https://api.ahrefs.com/mcp/mcp`), configured in the repo-root `.mcp.json`.

> The package is named **`quick_audit_mcp`** (not `mcp`) so it does not shadow the `mcp` SDK that
> `server.py` imports. It is launched as `python -m quick_audit_mcp.server` **from the repo root**.

## Install & run (local)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r quick_audit_mcp/requirements.txt
cp quick_audit_mcp/.env.example quick_audit_mcp/.env   # then fill in
python -m quick_audit_mcp.server
```

In the cloud routine, `scripts/setup.sh` installs dependencies — no manual venv needed.

## Auth (headless-safe)

See `auth.py`. Resolution order: **service account** (`GOOGLE_SERVICE_ACCOUNT_JSON` /
`GOOGLE_APPLICATION_CREDENTIALS`, recommended for cloud) → cached **`GOOGLE_OAUTH_TOKEN_FILE`** →
**interactive OAuth** (opt-in only). The server never opens a browser unless
`QUICK_AUDIT_ALLOW_INTERACTIVE_OAUTH=true`, so it is safe in an unattended routine.

## Validate config & test

```bash
python quick_audit_mcp/scripts/validate_mcp_config.py .mcp.json
pytest quick_audit_mcp/tests tests/automated      # run from repo root
```

## Gmail auto-send safety

`ENABLE_GMAIL_SEND=false` by default. When enabled, `send_gmail_message` still enforces a recipient
cap (`QUICK_AUDIT_MAX_SEND_RECIPIENTS`) and an optional domain allowlist (`QUICK_AUDIT_ALLOWED_SEND_DOMAINS`).
Keep it disabled until the activation checklist in `docs/setup.md` is signed off.
