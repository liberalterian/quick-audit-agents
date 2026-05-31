#!/usr/bin/env bash
# Quick Audit System — environment setup for the Claude Routine cloud container (and local dev).
#
# Wire this as the Routine "Build/Setup Command":   bash scripts/setup.sh
# It installs the MCP-server dependencies and the PDF renderer dependency, then
# runs a fail-fast import smoke check so a broken environment never reaches the agent loop.
set -euo pipefail

echo "[setup] python: $(python3 --version)"
python3 -m pip install --upgrade pip >/dev/null

echo "[setup] installing MCP server dependencies (quick_audit_mcp/requirements.txt)"
python3 -m pip install -r quick_audit_mcp/requirements.txt

echo "[setup] installing PDF renderer dependency (reportlab)"
python3 -m pip install "reportlab>=4.0.0"

echo "[setup] import smoke check (catches the SDK-name-collision regression)"
python3 -c "import quick_audit_mcp.server; import reportlab; print('imports ok')"

# Optional: run the automated test suite when pytest is available (non-fatal if absent).
if python3 -c "import pytest" 2>/dev/null; then
  echo "[setup] running automated tests"
  python3 -m pytest -q quick_audit_mcp/tests tests/automated || {
    echo "[setup] WARNING: automated tests failed" >&2
    exit 1
  }
fi

echo "[setup] done"
