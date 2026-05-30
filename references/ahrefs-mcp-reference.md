# Ahrefs MCP Reference

## Endpoint

`https://api.ahrefs.com/mcp/mcp`

## Claude Code setup command

```bash
claude mcp add ahrefs https://api.ahrefs.com/mcp/mcp -t http
```

## Purpose in Quick Audit

- Domain Rating.
- Referring domains.
- Backlinks.
- Organic keywords.
- Organic traffic estimate.
- Top organic keywords/pages.
- Competitor snapshots.

## Important constraint

Ahrefs states that its external MCP server is intended for MCP-compatible AI clients and interactive AI-driven workflows, not as a general-purpose programmatic API. For scripts or standalone API clients, use the Ahrefs public API instead.
