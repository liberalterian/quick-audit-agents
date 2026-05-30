# Google Sheets Tracker Writeback Reference

## Why direct API is used

The verified official Google Workspace MCP endpoint list used for this package did not include Google Sheets. The Quick Audit Tracker still needs deterministic row reads/writes, so production should use direct Google Sheets API credentials or a trusted internal Tracker MCP.

## Required operations

- Read Tracker tab rows.
- Find rows by `tracker-row-id` or `submission-id`.
- Update milestone columns.
- Add missing columns only when explicitly allowed.
- Write failure notes and Routine session URL.

## Recommended authentication

Use a service account or delegated OAuth flow scoped to the single Tracker spreadsheet. Do not use broad Drive-wide credentials if sheet-specific access is enough.

## Required environment variables

- `GOOGLE-SHEETS-SPREADSHEET-ID`
- `GOOGLE-SHEETS-TRACKER-TAB`
- `GOOGLE-APPLICATION-CREDENTIALS` or equivalent secret store path.

## Test

Run `tests/google-sheets-tracker-writeback-test.md` before production.
