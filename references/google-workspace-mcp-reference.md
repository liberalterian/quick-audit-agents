# Google Workspace MCP Reference

## Official remote endpoints used

- Gmail: `https://gmailmcp.googleapis.com/mcp/v1`
- Google Drive: `https://drivemcp.googleapis.com/mcp/v1`
- Google Calendar: `https://calendarmcp.googleapis.com/mcp/v1`
- Google Chat: `https://chatmcp.googleapis.com/mcp/v1`
- People API: `https://people.googleapis.com/mcp/v1`

This package includes Gmail, Drive, and People in `.mcp.json` because Quick Audit needs Gmail and Drive. Calendar and Chat are not required by the production path.

## Production use

Configure OAuth in Claude/Claude Code/Routine connectors. Do not commit OAuth client secrets.

## Required Quick Audit tools

- Gmail: create draft email.
- Drive: create/upload/read files.
- People: optional contact/profile support.

## Sheets note

Google Sheets is not listed in the verified official remote MCP endpoint list used for this package. Use the Google Sheets API or a trusted internal Tracker MCP for Tracker updates.
