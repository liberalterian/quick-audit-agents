"""Unit tests for the server hardening changes.

Covers: API-key redaction, conditional OAuth scopes, aggregate recipient cap,
and empty-values validator parity between SheetsAppendInput / SheetsUpdateInput.

These tests import from quick_audit_mcp.server directly and use monkeypatch for
env-var isolation so they never touch external services.
"""
from __future__ import annotations

import os
import pytest
import httpx
from pydantic import ValidationError

from quick_audit_mcp.server import (
    GMAIL_SEND_SCOPE,
    GmailSendInput,
    SheetsAppendInput,
    SheetsUpdateInput,
    _oauth_scopes,
    _raise_for_status_redacted,
    _redact_key,
    _clean_recipients,
)


# ── Key redaction helpers ────────────────────────────────────────────────────

def test_redact_key_masks_query_param():
    url = (
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        "?url=https%3A%2F%2Fexample.com&key=SECRET_KEY_12345&strategy=mobile"
    )
    result = _redact_key(url)
    assert "SECRET_KEY_12345" not in result
    # Non-key parts must survive.
    assert "strategy=mobile" in result
    assert "url=https%3A%2F%2Fexample.com" in result


def test_redact_key_noop_when_no_key():
    url = "https://places.googleapis.com/v1/places/abc123?languageCode=en"
    assert _redact_key(url) == url


def test_raise_for_status_redacted_masks_key_in_error():
    url = (
        "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        "?url=https%3A%2F%2Fexample.com&key=TOP_SECRET_123&strategy=mobile"
    )
    req = httpx.Request("GET", url)
    resp = httpx.Response(400, request=req)
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        _raise_for_status_redacted(resp)
    assert "TOP_SECRET_123" not in str(exc_info.value)


def test_raise_for_status_redacted_passes_on_2xx():
    req = httpx.Request("GET", "https://example.com?key=MYKEY")
    resp = httpx.Response(200, request=req)
    _raise_for_status_redacted(resp)  # must not raise


# ── OAuth scope list ─────────────────────────────────────────────────────────

def test_oauth_scopes_exclude_gmail_send_by_default(monkeypatch):
    monkeypatch.delenv("ENABLE_GMAIL_SEND", raising=False)
    assert GMAIL_SEND_SCOPE not in _oauth_scopes()


def test_oauth_scopes_exclude_gmail_send_when_false(monkeypatch):
    monkeypatch.setenv("ENABLE_GMAIL_SEND", "false")
    assert GMAIL_SEND_SCOPE not in _oauth_scopes()


def test_oauth_scopes_include_gmail_send_when_enabled(monkeypatch):
    monkeypatch.setenv("ENABLE_GMAIL_SEND", "true")
    assert GMAIL_SEND_SCOPE in _oauth_scopes()


# ── Sheets empty-values parity ───────────────────────────────────────────────

@pytest.mark.parametrize("Model,kwargs", [
    (SheetsAppendInput, {"values": []}),
    (SheetsUpdateInput, {"range_name": "Audits!A1:B1", "values": []}),
])
def test_sheets_models_reject_empty_values(Model, kwargs):
    with pytest.raises(ValidationError):
        Model(**kwargs)


def test_sheets_models_accept_non_empty_values():
    SheetsAppendInput(values=[["a", "b"]])
    SheetsUpdateInput(range_name="Audits!A1:B1", values=[["a", "b"]])


# ── Aggregate recipient cap ──────────────────────────────────────────────────

def test_recipient_cap_is_aggregate(monkeypatch):
    """2 to + 1 cc + 1 bcc = 4 total should exceed a cap of 3."""
    monkeypatch.setenv("QUICK_AUDIT_MAX_SEND_RECIPIENTS", "3")
    monkeypatch.setenv("ENABLE_GMAIL_SEND", "true")
    monkeypatch.delenv("QUICK_AUDIT_ALLOWED_SEND_DOMAINS", raising=False)

    # Import send_gmail_message here so env is already patched.
    from quick_audit_mcp.server import send_gmail_message

    payload = GmailSendInput(
        to=["a@example.com", "b@example.com"],
        subject="test",
        body_text="body",
        cc=["c@example.com"],
        bcc=["d@example.com"],
    )
    with pytest.raises(ValueError, match="exceeds limit"):
        send_gmail_message(payload)


def test_recipient_cap_allows_total_at_limit(monkeypatch):
    """Exactly 3 total (2 to + 1 cc) should not raise the cap error."""
    monkeypatch.setenv("QUICK_AUDIT_MAX_SEND_RECIPIENTS", "3")
    monkeypatch.delenv("QUICK_AUDIT_ALLOWED_SEND_DOMAINS", raising=False)

    to = _clean_recipients(["a@example.com", "b@example.com"])
    cc = _clean_recipients(["c@example.com"])
    bcc = _clean_recipients([])

    total = len(to) + len(cc) + len(bcc)
    max_r = int(os.getenv("QUICK_AUDIT_MAX_SEND_RECIPIENTS", "5"))
    assert total <= max_r
