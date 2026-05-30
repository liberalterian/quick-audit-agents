# Quick Audit MCP Package

This package completes the MCP integration gaps for the Quick Audit / MAA workflow.

## What is included

- `.mcp.json` with:
  - Official Ahrefs hosted MCP endpoint
  - Official Google Gmail MCP for draft creation and thread search
  - Official Google Drive MCP for writing audit Markdown/PDF artifacts
  - Local `quick-audit-tools` MCP wrapper for gaps not covered by official remote MCPs
- `.env.example` with runtime secrets and safety gates
- `mcp/quick_audit_tools/server.py` custom local wrapper for:
  - Google Sheets Quick Audit Tracker writes
  - gated Gmail auto-send
  - Google Places business resolution and place details
  - PageSpeed Insights mobile performance checks
- Docs covering the implementation plan, scopes, setup, and safety gates
- Basic config validation script and tests

## Why a local custom wrapper is required

The official Google Workspace MCP servers currently cover Gmail draft creation and Drive file actions, but not Google Sheets writes or Gmail auto-send. Google Places and PageSpeed Insights are public Google APIs, not official Workspace MCP servers. For production reliability, these gaps belong in one small local custom MCP wrapper rather than multiple invented or unofficial servers.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the env template:

```bash
cp .env.example .env
```

Fill in your Google OAuth and API credentials.

## Validate config

```bash
python scripts/validate_mcp_config.py .mcp.json
```

## Run local MCP server manually

```bash
python -m mcp.quick_audit_tools.server
```

## Gmail auto-send safety

`ENABLE_GMAIL_SEND=false` by default. Leave it disabled while testing. When enabled, the `send_gmail_message` tool still enforces recipient limits and optional allowed domains.
