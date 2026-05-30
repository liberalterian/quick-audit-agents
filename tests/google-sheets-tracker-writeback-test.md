# Google Sheets Tracker Writeback Test

## Purpose

Verify Tracker read/write works through direct Google Sheets API or trusted internal MCP.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Use a test spreadsheet.
2. Create a row with `submission-id=qa-test-0001`.
3. Read the row.
4. Write milestone columns.
5. Write final complete state.
6. Verify values in the sheet.

## Pass criteria

- Row lookup is deterministic.
- Values write to the correct row only.
- Failure notes can be written.
- Routine session URL can be stored.

## Fail criteria

- Writes affect the wrong row.
- Credentials have unnecessary Drive-wide access.
- Missing columns are created without explicit permission.

