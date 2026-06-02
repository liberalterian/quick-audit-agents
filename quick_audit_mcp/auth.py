"""Headless-safe Google credential loading for the Quick Audit MCP server.

A Claude Routine runs in an unattended cloud container with no browser, so the
previous interactive `InstalledAppFlow.run_local_server()` path could never
complete there. This module resolves credentials in a cloud-safe order and only
ever launches a browser when interactive OAuth is *explicitly* opted in.

Resolution order (first configured wins):
  1. Service account  — GOOGLE_SERVICE_ACCOUNT_JSON (inline JSON) or
                        GOOGLE_APPLICATION_CREDENTIALS (path to a key file).
                        Preferred for cloud. Optional domain-wide delegation via
                        GOOGLE_IMPERSONATE_SUBJECT (only needed to send Gmail as a user).
  2. Cached user token — GOOGLE_OAUTH_TOKEN_FILE (authorized_user JSON), auto-refreshed.
  3. Interactive OAuth — ONLY when QUICK_AUDIT_ALLOW_INTERACTIVE_OAUTH=true and a
                        client-secrets file exists. Never runs in the cloud.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Sequence

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials


def _env_bool(name: str) -> bool:
    return (os.getenv(name) or "").strip().lower() in {"1", "true", "yes", "on"}


def _sa_inline() -> str | None:
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    return raw if raw and raw.strip().startswith("{") else None


def _sa_path() -> str | None:
    p = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    return p if p and Path(p).exists() else None


def _token_path() -> str | None:
    p = os.getenv("GOOGLE_OAUTH_TOKEN_FILE")
    return p if p and Path(p).exists() else None


def auth_mode() -> str:
    """Report how credentials WOULD be obtained, for health_check. No secret I/O."""
    if _sa_inline() or _sa_path():
        return "service_account"
    if _token_path():
        return "token"
    if _env_bool("QUICK_AUDIT_ALLOW_INTERACTIVE_OAUTH") and os.getenv("GOOGLE_OAUTH_CLIENT_SECRETS_FILE"):
        return "interactive"
    return "none"


def _maybe_delegate(creds):
    subject = os.getenv("GOOGLE_IMPERSONATE_SUBJECT")
    if subject and hasattr(creds, "with_subject"):
        return creds.with_subject(subject)
    return creds


def get_credentials(scopes: Sequence[str]):
    """Return Google credentials using the first configured, cloud-safe method."""
    scopes = list(scopes)

    # 1. Service account (preferred, headless)
    inline = _sa_inline()
    if inline:
        info = json.loads(inline)
        return _maybe_delegate(service_account.Credentials.from_service_account_info(info, scopes=scopes))
    sa_file = _sa_path()
    if sa_file:
        return _maybe_delegate(service_account.Credentials.from_service_account_file(sa_file, scopes=scopes))

    # 2. Cached, refreshable user token
    token_file = _token_path()
    if token_file:
        creds = Credentials.from_authorized_user_file(token_file, scopes)
        if creds.valid:
            return creds
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Best-effort cache write-back. In the cloud the token file may be a
            # read-only secret mount; a failed write must not break valid creds.
            try:
                Path(token_file).write_text(creds.to_json(), encoding="utf-8")
            except OSError:
                pass
            return creds
        raise RuntimeError(
            f"Cached token at {token_file} is invalid and cannot be refreshed. "
            "Re-provision it locally and ship it as a routine secret."
        )

    # 3. Interactive OAuth — explicit opt-in only; never reached in the cloud
    if _env_bool("QUICK_AUDIT_ALLOW_INTERACTIVE_OAUTH"):
        client_secrets = os.getenv(
            "GOOGLE_OAUTH_CLIENT_SECRETS_FILE", "./secrets/google-oauth-client.json"
        )
        if not Path(client_secrets).exists():
            raise FileNotFoundError(f"Missing OAuth client secrets file: {client_secrets}")
        from google_auth_oauthlib.flow import InstalledAppFlow  # imported only on the browser path

        flow = InstalledAppFlow.from_client_secrets_file(client_secrets, scopes)
        creds = flow.run_local_server(port=0)
        token_out = os.getenv("GOOGLE_OAUTH_TOKEN_FILE", "./secrets/google-oauth-token.json")
        Path(token_out).parent.mkdir(parents=True, exist_ok=True)
        Path(token_out).write_text(creds.to_json(), encoding="utf-8")
        return creds

    raise RuntimeError(
        "No Google credentials configured. Set GOOGLE_SERVICE_ACCOUNT_JSON or "
        "GOOGLE_APPLICATION_CREDENTIALS (recommended for cloud routines), or provide a "
        "pre-authorized GOOGLE_OAUTH_TOKEN_FILE. Interactive OAuth requires "
        "QUICK_AUDIT_ALLOW_INTERACTIVE_OAUTH=true and a local desktop session."
    )
