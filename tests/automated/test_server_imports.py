"""Regression guard for the SDK-name-collision bug (audit finding C-1).

The local package is named `quick_audit_mcp` (NOT `mcp`) so it does not shadow the
`mcp` SDK that server.py imports. If someone reintroduces a top-level `mcp/` package,
or breaks the module path, these imports fail here instead of silently at routine runtime.
"""

import importlib


def test_import_auth():
    importlib.import_module("quick_audit_mcp.auth")


def test_import_server_and_sdk_resolves():
    server = importlib.import_module("quick_audit_mcp.server")
    # FastMCP came from the real `mcp` SDK, proving no local shadowing.
    assert server.mcp is not None
    # The headless loader is wired in.
    assert hasattr(server.auth, "get_credentials")
    assert hasattr(server.auth, "auth_mode")
