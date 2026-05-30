# MCP Connection Test

## Purpose

Verify required MCP servers are discoverable and authenticated.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Start Claude Code in the project.
2. Approve project `.mcp.json` servers if prompted.
3. Run `/mcp`.
4. Authenticate Ahrefs, Gmail, and Drive.
5. Run harmless read/list tests only.

## Pass criteria

- Ahrefs, Gmail, and Drive appear connected.
- Gmail can list labels or drafts.
- Drive can list or search files in the authorized account.
- Ahrefs can answer a harmless domain overview query.

## Fail criteria

- Any required server is missing.
- OAuth cannot complete.
- Gmail or Drive permissions are broader than expected or insufficient for required actions.

