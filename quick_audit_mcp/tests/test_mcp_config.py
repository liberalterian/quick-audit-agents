from __future__ import annotations

import json
from pathlib import Path

# Repo root is two levels up from quick_audit_mcp/tests/.
ROOT = Path(__file__).resolve().parents[2]
MCP_JSON = ROOT / ".mcp.json"


def _servers() -> dict:
    return json.loads(MCP_JSON.read_text(encoding="utf-8"))["mcpServers"]


def test_mcp_json_contains_required_servers():
    assert {"ahrefs", "quick-audit-tools"}.issubset(_servers())


def test_local_server_launches_renamed_module():
    qat = _servers()["quick-audit-tools"]
    # Guards against the `mcp/` SDK-shadow regression.
    assert "quick_audit_mcp.server" in qat["args"]
    assert qat["command"] in {"python", "python3"}


def test_ahrefs_endpoint_expected():
    assert _servers()["ahrefs"]["args"][1] == "https://api.ahrefs.com/mcp/mcp"


def test_gmail_send_not_enabled_by_default():
    assert _servers()["quick-audit-tools"]["env"]["ENABLE_GMAIL_SEND"] == "false"


def test_no_oauth_scope_arrays_or_enabled_flag():
    for name, cfg in _servers().items():
        oauth = cfg.get("oauth", {})
        assert "enabled" not in oauth, f"{name} carries undocumented oauth.enabled"
        assert not isinstance(oauth.get("scopes"), list), f"{name} oauth.scopes must be a string"


def test_no_duplicate_server_urls():
    urls = [c["url"] for c in _servers().values() if c.get("url")]
    assert len(urls) == len(set(urls)), "duplicate server urls in .mcp.json"
