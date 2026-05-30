# Custom Wrapper MVP Plan

## Decision

Yes, a custom MVP wrapper is needed.

Do not create separate custom MCPs for Sheets, Gmail-send, Places, and PageSpeed. Instead, create one local `quick-audit-tools` MCP with a narrow surface area.

## Reasoning

1. Google Workspace MCP covers Gmail drafts and Drive file actions, but not every action required by the Quick Audit workflow.
2. Sheets writes must target a specific tracker spreadsheet and should be protected by workflow-specific validation.
3. Gmail auto-send is high-risk and should be gated separately from normal draft creation.
4. Places and PageSpeed are direct Google APIs, not Workspace MCP products.
5. A single local wrapper reduces configuration sprawl and makes the dangerous actions easy to review.

## MVP tool list

### `append_quick_audit_tracker_row`

Purpose: append completed audit metadata to the tracker.

Inputs:

- `spreadsheet_id`, optional; defaults to `GOOGLE_SHEETS_SPREADSHEET_ID`
- `range_name`, optional; defaults to `Audits!A:Z`
- `values`, required 2D row array

### `update_quick_audit_tracker_range`

Purpose: update a known tracker row/range after grading, PDF generation, or email draft completion.

Inputs:

- `spreadsheet_id`, optional
- `range_name`, required A1 range
- `values`, required 2D array

### `send_gmail_message`

Purpose: allow auto-send only after explicit workflow approval.

Safety gates:

- `ENABLE_GMAIL_SEND=true` required
- max recipients enforced by `QUICK_AUDIT_MAX_SEND_RECIPIENTS`
- optional allowed domain list enforced by `QUICK_AUDIT_ALLOWED_SEND_DOMAINS`

### `resolve_business_place`

Purpose: resolve client/business query to Google Places candidates and Place IDs.

Inputs:

- business/address query
- max result count
- optional language, region, included type

### `get_place_details`

Purpose: fetch structured place details from a known Place ID.

Inputs:

- standalone place ID
- optional language code

### `run_pagespeed_insights`

Purpose: run PageSpeed Insights v5 against a URL using mobile by default.

Outputs:

- Lighthouse scores
- lab metrics
- Core Web Vitals 75th percentile field data where available
- page/origin CWV assessment

## Phase 1 implementation

Already included in this package:

- `mcp/quick_audit_tools/server.py`
- `.mcp.json`
- `.env.example`
- validation script
- test stubs

## Phase 2 hardening

Before production auto-send:

1. Add structured audit IDs to every tool call.
2. Log every write/send action to a separate immutable audit log.
3. Add dry-run mode to all write/send tools.
4. Add tests with mocked Google API responses.
5. Require human approval before switching `ENABLE_GMAIL_SEND=true`.
6. Add row schema validation for the tracker columns.
7. Add retry/backoff for transient API failures.
