#!/usr/bin/env python3
"""Validate the Quick Audit MCP JSON config shape.

This does not guarantee every MCP client supports every field. It verifies that
this package includes the required server names and the critical endpoints/tools.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_SERVERS = {
    "ahrefs",
    "google-gmail",
    "google-drive",
    "quick-audit-tools",
}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_mcp_config.py PATH_TO_MCP_JSON", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    servers = data.get("mcpServers", {})

    missing = REQUIRED_SERVERS - set(servers)
    if missing:
        print(f"Missing required MCP server(s): {', '.join(sorted(missing))}", file=sys.stderr)
        return 1

    assert servers["ahrefs"].get("url") == "https://api.ahrefs.com/mcp/mcp"
    assert servers["google-gmail"].get("url") == "https://gmailmcp.googleapis.com/mcp/v1"
    assert servers["google-drive"].get("url") == "https://drivemcp.googleapis.com/mcp/v1"
    assert servers["quick-audit-tools"].get("command") == "python"
    assert "mcp.quick_audit_tools.server" in servers["quick-audit-tools"].get("args", [])

    gmail_scopes = set(servers["google-gmail"].get("oauth", {}).get("scopes", []))
    drive_scopes = set(servers["google-drive"].get("oauth", {}).get("scopes", []))

    assert "https://www.googleapis.com/auth/gmail.compose" in gmail_scopes
    assert "https://www.googleapis.com/auth/drive.file" in drive_scopes

    print("MCP config validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
