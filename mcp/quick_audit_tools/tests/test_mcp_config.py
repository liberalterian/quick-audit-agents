from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mcp_json_contains_required_servers():
    data = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    servers = data["mcpServers"]
    assert {"ahrefs", "google-gmail", "google-drive", "quick-audit-tools"}.issubset(servers)


def test_remote_endpoints_are_expected():
    data = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    servers = data["mcpServers"]
    assert servers["ahrefs"]["url"] == "https://api.ahrefs.com/mcp/mcp"
    assert servers["google-gmail"]["url"] == "https://gmailmcp.googleapis.com/mcp/v1"
    assert servers["google-drive"]["url"] == "https://drivemcp.googleapis.com/mcp/v1"


def test_gmail_send_not_enabled_by_default():
    data = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    env = data["mcpServers"]["quick-audit-tools"]["env"]
    assert env["ENABLE_GMAIL_SEND"] == "false"


def test_google_drive_uses_file_scope():
    data = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    scopes = data["mcpServers"]["google-drive"]["oauth"]["scopes"]
    assert "https://www.googleapis.com/auth/drive.file" in scopes
    assert "https://www.googleapis.com/auth/drive" not in scopes
