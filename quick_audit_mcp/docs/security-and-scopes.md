# Security, OAuth Scopes, and Least-Privilege Notes

## Default stance

Use read-only or file-scoped access wherever possible. Only enable send/write permissions for the smallest workflow surface area needed.

## Ahrefs

Use the official Ahrefs hosted MCP endpoint:

```text
https://api.ahrefs.com/mcp/mcp
```

Authentication should be completed through the client-supported OAuth/auth flow.

## Gmail

### Drafts

Use the official Google Gmail MCP with:

```text
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.compose
```

This is the right default for cover notes and team alerts because drafts require review before sending.

### Auto-send

Use local wrapper only:

```text
https://www.googleapis.com/auth/gmail.send
```

Safety requirements:

- Keep `ENABLE_GMAIL_SEND=false` by default.
- Use recipient domain allowlists when possible.
- Keep low max-recipient limits.
- Log every sent message.
- Prefer draft-first behavior unless the workflow explicitly requires auto-send.

## Google Drive

Use official Google Drive MCP with:

```text
https://www.googleapis.com/auth/drive.file
```

This lets the app see, edit, create, and delete only the specific Drive files used with the app. Use it for audit Markdown files, grading notes, and PDFs.

Avoid full `drive` scope unless a later production requirement proves it is necessary.

## Google Sheets

Preferred minimal practical setup:

```text
https://www.googleapis.com/auth/drive.file
https://www.googleapis.com/auth/spreadsheets
```

Important limitation: Sheets API scopes are spreadsheet-file scoped, not individual tab scoped. Use a dedicated Quick Audit Tracker spreadsheet and protect sensitive ranges in the sheet itself.

## Google Places

Use API key authentication through:

- Text Search (New): `https://places.googleapis.com/v1/places:searchText`
- Place Details (New): `https://places.googleapis.com/v1/places/{PLACE_ID}`

Security requirements:

- Restrict API key by API and, where possible, by application/environment.
- Request only needed fields via `X-Goog-FieldMask` to control cost and data exposure.

## PageSpeed Insights

Use API key authentication through:

```text
https://www.googleapis.com/pagespeedonline/v5/runPagespeed
```

The wrapper should default to mobile strategy and return normalized scores/metrics instead of dumping full raw Lighthouse JSON into agent context.

## Anthropic

`ANTHROPIC_API_KEY` is runtime configuration. It should not be represented as an MCP server.

Store it in deployment secrets or `.env` only. Never commit real keys.
