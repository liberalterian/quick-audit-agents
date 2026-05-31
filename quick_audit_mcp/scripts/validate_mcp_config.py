#!/usr/bin/env python3
"""Validate the Quick Audit `.mcp.json` config SHAPE (not just its current values).

This checks structural correctness that actually catches regressions:
- required servers are present,
- the local server launches the correctly-named module (no `mcp` SDK shadowing),
- any `oauth.scopes` is a space-separated string (not a JSON array),
- no server carries the undocumented `oauth.enabled` field,
- no two servers share the same `url` (duplicate-server smell),
- Gmail auto-send is disabled by default in the local server env.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED_SERVERS = {"ahrefs", "quick-audit-tools"}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_mcp_config.py PATH_TO_MCP_JSON", file=sys.stderr)
        return 2

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    servers = data.get("mcpServers", {})
    errors: list[str] = []

    missing = REQUIRED_SERVERS - set(servers)
    if missing:
        errors.append(f"missing required server(s): {', '.join(sorted(missing))}")

    qat = servers.get("quick-audit-tools", {})
    if "quick_audit_mcp.server" not in qat.get("args", []):
        errors.append("quick-audit-tools must launch module 'quick_audit_mcp.server'")
    if qat.get("command") not in {"python", "python3"}:
        errors.append("quick-audit-tools command should be python/python3")
    if qat.get("env", {}).get("ENABLE_GMAIL_SEND") != "false":
        errors.append("ENABLE_GMAIL_SEND must default to 'false'")

    seen_urls: dict[str, str] = {}
    for name, cfg in servers.items():
        oauth = cfg.get("oauth", {})
        if "enabled" in oauth:
            errors.append(f"{name}: drop undocumented oauth.enabled field")
        if isinstance(oauth.get("scopes"), list):
            errors.append(f"{name}: oauth.scopes must be a space-separated string, not a list")
        url = cfg.get("url")
        if url:
            if url in seen_urls:
                errors.append(f"duplicate url {url} on '{name}' and '{seen_urls[url]}'")
            seen_urls[url] = name

    if errors:
        for e in errors:
            print(f"INVALID: {e}", file=sys.stderr)
        return 1

    print("MCP config validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
