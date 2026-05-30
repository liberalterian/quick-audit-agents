# Integration Environment Reference

## Required runtime commands

- `python3`
- `pip`
- `curl`
- `jq`

## Required Python packages

- `reportlab`

## Required environment variables or secret-store entries

- `GOOGLE-MAPS-API-KEY`
- `GOOGLE-SHEETS-SPREADSHEET-ID`
- `GOOGLE-SHEETS-TRACKER-TAB`
- `GOOGLE-APPLICATION-CREDENTIALS` or equivalent secure credential reference
- `DRIVE-ROOT-FOLDER-ID`
- `DEFAULT-PARTNER-ID`
- `QUICK-AUDIT-ROUTINE-FIRE-URL` outside the Routine caller
- `QUICK-AUDIT-ROUTINE-TOKEN` outside the Routine caller

## Optional environment variables

- `BROWSER-WORKER-URL`
- `PARTNER-CONFIG-SHEET-ID`
- `GMAIL-AUTO-SEND-ENABLED`
- `HARD-FAIL-AUTO-SEND-ENABLED`

## Do not commit

- API keys.
- OAuth client secrets.
- Service account JSON.
- Routine bearer tokens.
- Real prospect data.
