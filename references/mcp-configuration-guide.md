# MCP Configuration Guide

## Verified configuration facts

Claude Code supports project-scoped MCP server configuration in `.mcp.json`. Project-scoped servers are designed to be checked into version control and require approval before use. HTTP remote servers should use `type: "http"` and `url`. Claude Code supports environment variable expansion in `.mcp.json` for fields such as `command`, `args`, `env`, `url`, and `headers`.

## Servers included in `.mcp.json`

### Ahrefs

- Endpoint: `https://api.ahrefs.com/mcp/mcp`
- Transport: HTTP
- Purpose: SEO, backlinks, keyword, and competitor data.
- Authentication: authenticate through the MCP flow after adding/approving the server.

### Gmail

- Endpoint: `https://gmailmcp.googleapis.com/mcp/v1`
- Transport: HTTP
- Purpose: search/read Gmail and create prospect/team drafts.
- Scopes in config: Gmail readonly and compose.

### Google Drive

- Endpoint: `https://drivemcp.googleapis.com/mcp/v1`
- Transport: HTTP
- Purpose: create/read files and persist audit artifacts.
- Scopes in config: Drive readonly and file access.

### Google People

- Endpoint: `https://people.googleapis.com/mcp/v1`
- Transport: HTTP
- Purpose: optional profile/contact verification.

### Google Maps Code Assist

- Endpoint: `https://mapscodeassist.googleapis.com/mcp`
- Transport: HTTP
- Purpose: Google Maps Platform documentation lookup only.
- Important: this is not a Google Places business-data MCP.

## Not included as verified remote MCP servers

### Google Sheets

The verified Google Workspace MCP documentation used for this package did not expose a Google Sheets remote MCP endpoint. For production Tracker writeback, use direct Google Sheets API credentials or a trusted internal Tracker MCP.

### Google Places business data

Google Maps Code Assist is documentation-focused. For business lookup and Place Details, use direct Google Places API or a trusted internal Places MCP.

## Security rule

Never commit OAuth client secrets, API keys, service account JSON, or Routine bearer tokens.
