# Google Workspace Reference

## How Gmail and Drive are accessed (connectors, not `.mcp.json` HTTP servers)

There are **no** public `gmailmcp.googleapis.com` / `drivemcp.googleapis.com` MCP endpoints. Earlier
drafts invented those URLs; they have been removed from `.mcp.json`. In production, Gmail and Drive are
the official **Google Workspace connectors** (claude.ai integrations) enabled on the Routine:

- **Gmail** — create prospect cover-note + team-alert **drafts**.
- **Google Drive** — create/upload/read the audit `.md`, `.pdf`, and grading-notes files.
- **Google People** — optional contact/profile support (enable only if needed).

Enable these under **Settings → Connectors** on claude.ai (or in the routine's Connectors tab) and
complete OAuth there. Do not commit OAuth client secrets.

## What stays in `.mcp.json`

Only servers with a verified endpoint or local code:
- **Ahrefs** — hosted MCP `https://api.ahrefs.com/mcp/mcp`.
- **quick-audit-tools** — the local `quick_audit_mcp` server (Sheets writeback, Places, PageSpeed, gated Gmail send).

## Sheets note

Google Sheets has no official Workspace MCP/connector for writes, so Tracker writeback uses the
Google Sheets API via the local `quick-audit-tools` server (service-account auth).
