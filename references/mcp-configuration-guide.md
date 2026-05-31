# MCP Configuration Guide

## Verified configuration facts

Claude Code supports project-scoped MCP servers in `.mcp.json` (checked into version control, approved
before use). HTTP servers use `type: "http"` + `url`. `oauth.scopes` is a **space-separated string**
(not a JSON array); there is no documented `oauth.enabled` field. Env-var expansion is supported in
`command`, `args`, `env`, `url`, `headers` (use `${VAR:-default}` so an unset var doesn't fail parsing).

## Servers in this repo's `.mcp.json`

### Ahrefs (hosted MCP)
- Launched via `npx mcp-remote https://api.ahrefs.com/mcp/mcp` with a bearer header from `AHREFS_MCP_KEY`.
- Purpose: DR, referring domains, keywords, competitors. `alwaysLoad: true`.

### quick-audit-tools (local stdio)
- `python3 -m quick_audit_mcp.server` (package renamed from `mcp/` so it does not shadow the `mcp` SDK).
- Tools: Sheets Tracker writeback, Places resolve/details, PageSpeed, gated Gmail send, `health_check`.
- Auth: service account (cloud) / token / opt-in interactive (see `quick_audit_mcp/auth.py`).

## NOT in `.mcp.json` — use connectors / direct APIs

- **Gmail drafts** and **Google Drive** — official Google Workspace **connectors** enabled on the routine
  (no `gmailmcp`/`drivemcp` googleapis MCP endpoints exist; the earlier invented URLs were removed).
- **Google Sheets writes** — no official MCP; handled by the local server via the Sheets API.
- **Google Places business data** — direct Places API via the local server.

## Security rule

Never commit OAuth client secrets, API keys, service-account JSON, or routine bearer tokens
(see the repo-root `.gitignore`).
