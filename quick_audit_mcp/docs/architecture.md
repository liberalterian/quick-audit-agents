# Quick Audit MCP — Architecture & Integration Decisions

(Consolidates the former `custom-wrapper-plan.md` and `mcp-integration-audit.md`.)

## Decision

One small local stdio MCP server (`quick_audit_mcp`) covers only the integration gaps. Do **not**
invent separate or unofficial remote MCPs.

## Integration ownership

| Capability | Owner |
|---|---|
| DR, referring domains, organic keywords, top pages, competitors | **Ahrefs hosted MCP** (`https://api.ahrefs.com/mcp/mcp`, in `.mcp.json`) |
| Create prospect / team Gmail **drafts** | **Google Gmail connector** (claude.ai connector enabled on the routine) |
| Save audit `.md` / `.pdf` / grading notes to Drive | **Google Drive connector** (claude.ai connector) |
| Append/update the Quick Audit Tracker (Sheets) | local `quick-audit-tools.append_quick_audit_tracker_row` / `update_quick_audit_tracker_range` |
| Resolve business → Place ID; pull place details | local `quick-audit-tools.resolve_business_place` / `get_place_details` |
| Mobile PageSpeed | local `quick-audit-tools.run_pagespeed_insights` |
| Gated Gmail auto-send (off by default) | local `quick-audit-tools.send_gmail_message` |
| Claude agent runtime | `ANTHROPIC_API_KEY` (routine runtime config, not an MCP server) |

> **Correction vs. earlier drafts:** there are no public `gmailmcp.googleapis.com` /
> `drivemcp.googleapis.com` MCP endpoints. Gmail drafts and Drive are **claude.ai connectors**, not
> `.mcp.json` HTTP servers. Earlier drafts listed those invented URLs; they have been removed.

## Why a single local wrapper

1. Sheets writes target a specific tracker spreadsheet and need workflow-specific validation.
2. Gmail auto-send is high-risk and must be gated separately from normal drafts.
3. Places and PageSpeed are direct Google APIs, not Workspace connectors.
4. One small, auditable surface beats several invented servers.

## Tools (MVP, implemented)

`append_quick_audit_tracker_row`, `update_quick_audit_tracker_range`, `send_gmail_message` (gated),
`resolve_business_place`, `get_place_details`, `run_pagespeed_insights`, `health_check`.
See `server.py` for input models and `security-and-scopes.md` for scopes.

## Auth (cloud-safe)

Service account (preferred) → cached token → opt-in interactive OAuth. See `auth.py` and `setup.md`.
The server never opens a browser in the cloud.

## Phase-2 hardening (before production auto-send)

1. Structured audit IDs on every tool call.
2. Immutable audit log of every write/send.
3. Dry-run mode for write/send tools.
4. Tests with mocked Google API responses.
5. Human approval gate before `ENABLE_GMAIL_SEND=true`.
6. Tracker row-schema validation.
7. Retry/backoff for transient API failures.
