# MCP Integration Audit — Quick Audit / MAA Workflow

## Required integration matrix

| Requirement | Completion status | Implementation decision |
|---|---:|---|
| Ahrefs API | Complete | Use official hosted Ahrefs MCP at `https://api.ahrefs.com/mcp/mcp`. |
| Google Sheets | Complete | Implemented through local `quick-audit-tools` MCP wrapper using the Sheets API and exact Quick Audit Tracker spreadsheet ID. |
| Gmail drafts | Complete | Use official Google Gmail MCP. It supports draft creation and thread/search workflows. |
| Gmail auto-send | Complete, gated | Implemented in local wrapper with `ENABLE_GMAIL_SEND=false` by default, max-recipient guard, and optional domain allowlist. |
| Google Drive | Complete | Use official Google Drive MCP with `drive.file` scope for file creation/upload. |
| Google Places | Complete | Implemented in local wrapper using Places API Text Search and Place Details. |
| PageSpeed Insights | Complete | Implemented in local wrapper using PageSpeed Insights v5 API. |
| Anthropic Claude API | Complete | Moved to `.env.example` as `ANTHROPIC_API_KEY`; it is runtime configuration, not an MCP server. |
| Least-privilege and safety docs | Complete | See `security-and-scopes.md`. |

## Why this architecture is safer

The workflow uses official hosted MCPs where they exist and are sufficient:

- Ahrefs MCP for Ahrefs data.
- Google Gmail MCP for Gmail search/thread/draft creation.
- Google Drive MCP for Drive file actions.

It uses one custom local MCP only for integration gaps:

- Sheets writes are not currently covered by the official Workspace MCP list.
- Gmail auto-send is intentionally not part of the official Gmail MCP draft-focused workflow.
- Places and PageSpeed are Google APIs, not official Workspace MCP products.

This avoids inventing unofficial remote MCPs while keeping the custom code small, auditable, and testable.

## Expected tool ownership

| Tool/action | Owner |
|---|---|
| DR, referring domains, organic keywords, top pages, competitors | Ahrefs MCP |
| Create cover-note draft | Google Gmail MCP |
| Create team-alert draft | Google Gmail MCP |
| Auto-send approved team alert | Local `quick-audit-tools.send_gmail_message` |
| Save audit `.md` | Google Drive MCP |
| Save grading notes `.md` | Google Drive MCP |
| Save audit `.pdf` | Google Drive MCP |
| Append/update Quick Audit Tracker | Local `quick-audit-tools.append_quick_audit_tracker_row` / `update_quick_audit_tracker_range` |
| Resolve business to Place ID | Local `quick-audit-tools.resolve_business_place` |
| Pull place details | Local `quick-audit-tools.get_place_details` |
| Run mobile PageSpeed | Local `quick-audit-tools.run_pagespeed_insights` |
| Claude agent runtime | `ANTHROPIC_API_KEY` in runtime secrets |
