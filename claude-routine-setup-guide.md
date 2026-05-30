# Claude Routine Setup Guide

## Goal

Create one API-triggered Claude Routine named `Quick Audit Runner`.

## Routine configuration

- Repository: this repository.
- Prompt: paste or reference `agents/quick-audit-orchestrator-agent.md`.
- Trigger: API.
- Environment: Python 3, `reportlab`, `curl`, `jq`, and network access to the public enrichment and Google/Ahrefs endpoints.
- Connectors/MCP: approve/authenticate `.mcp.json` servers or configure equivalent Claude connectors in the Routine UI.

## API trigger request

The Routine fire endpoint expects an authenticated POST with the run-specific intake payload in the `text` field.

```json
{
  "text": "{\"event-type\":\"quick-audit-intake\",\"submission-id\":\"qa-0001\",\"business-name\":\"Example Services\",\"website\":\"https://example.com\",\"primary-city\":\"Denver\",\"state\":\"CO\",\"annual-revenue-band\":\"$2M–5M\",\"contact-name\":\"Jane Owner\",\"contact-email\":\"jane@example.com\",\"contact-phone\":\"+13035550100\",\"tracker-row-id\":\"row-42\",\"partner-id\":\"default\"}"
}
```

## Required secret storage

Store these outside the repo:

- Routine fire URL.
- Routine bearer token.
- Google OAuth credentials for Google Workspace MCP connectors.
- Google Maps Platform API key for Places API.
- Google Sheets writeback credentials.
- Optional Ahrefs authentication handled through MCP OAuth/login.

## First-run validation

1. Fire the Routine with `examples/sample-intake-payload.md` content.
2. Confirm the Routine returns a session URL.
3. Confirm Tracker row gets `routine-session-url`.
4. Confirm artifact creation reaches Drive.
5. Confirm Gmail draft creation works.
6. Confirm no final audit contains Glass Half Full or per-pillar Revenue Translation sections.
