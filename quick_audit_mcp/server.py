"""Quick Audit local MCP tools.

This stdio MCP server intentionally contains only the integration gaps that are
not cleanly covered by official hosted MCPs:

- Google Sheets Quick Audit Tracker writes
- gated Gmail auto-send
- Google Places business resolution / place details
- Google PageSpeed Insights mobile checks

Gmail draft creation and Drive file persistence are handled by the official
Google Workspace connectors enabled on the Claude Routine, not by this server.
"""

from __future__ import annotations

import base64
import json
import os
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv
from googleapiclient.discovery import build
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, HttpUrl, field_validator

from quick_audit_mcp import auth

load_dotenv()

mcp = FastMCP("quick-audit-tools")

GOOGLE_OAUTH_SCOPES = [
    # Recommended lowest practical scope for specific spreadsheet/file access.
    "https://www.googleapis.com/auth/drive.file",
    # Needed by Sheets API writes against the Quick Audit Tracker.
    "https://www.googleapis.com/auth/spreadsheets",
    # Needed only when ENABLE_GMAIL_SEND=true and auto-send is explicitly used.
    "https://www.googleapis.com/auth/gmail.send",
]

DEFAULT_PLACE_FIELDS = ",".join(
    [
        "places.id",
        "places.name",
        "places.displayName",
        "places.formattedAddress",
        "places.location",
        "places.businessStatus",
        "places.googleMapsUri",
        "places.websiteUri",
        "places.nationalPhoneNumber",
        "places.internationalPhoneNumber",
        "places.rating",
        "places.userRatingCount",
        "places.types",
    ]
)

DEFAULT_PLACE_DETAIL_FIELDS = ",".join(
    [
        "id",
        "name",
        "displayName",
        "formattedAddress",
        "location",
        "businessStatus",
        "googleMapsUri",
        "websiteUri",
        "nationalPhoneNumber",
        "internationalPhoneNumber",
        "rating",
        "userRatingCount",
        "types",
        "regularOpeningHours",
    ]
)


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def _credentials():
    """Return Google credentials via the headless-safe loader (see auth.py).

    Cloud routines must use a service account (GOOGLE_SERVICE_ACCOUNT_JSON /
    GOOGLE_APPLICATION_CREDENTIALS) or a pre-authorized token file; interactive
    OAuth is opt-in only and never runs in the cloud.
    """

    return auth.get_credentials(GOOGLE_OAUTH_SCOPES)


def _google_service(service_name: str, version: str):
    return build(service_name, version, credentials=_credentials(), cache_discovery=False)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _validate_recipients(recipients: Iterable[str]) -> list[str]:
    clean = [r.strip() for r in recipients if r and r.strip()]
    if not clean:
        raise ValueError("At least one recipient is required.")

    max_recipients = int(os.getenv("QUICK_AUDIT_MAX_SEND_RECIPIENTS", "5"))
    if len(clean) > max_recipients:
        raise ValueError(f"Recipient count {len(clean)} exceeds limit of {max_recipients}.")

    allowed_domains = _split_csv(os.getenv("QUICK_AUDIT_ALLOWED_SEND_DOMAINS"))
    if allowed_domains:
        invalid = [r for r in clean if r.split("@")[-1].lower() not in allowed_domains]
        if invalid:
            raise ValueError(
                "Recipient domain not allowed by QUICK_AUDIT_ALLOWED_SEND_DOMAINS: "
                + ", ".join(invalid)
            )
    return clean


class SheetsAppendInput(BaseModel):
    values: list[list[Any]] = Field(..., description="Rows to append, each row as a list of cell values.")
    spreadsheet_id: str | None = Field(
        default=None,
        description="Spreadsheet ID. Defaults to GOOGLE_SHEETS_SPREADSHEET_ID.",
    )
    range_name: str = Field(
        default_factory=lambda: os.getenv("QUICK_AUDIT_TRACKER_APPEND_RANGE", "Audits!A:Z"),
        description="A1 notation append range.",
    )

    @field_validator("values")
    @classmethod
    def values_must_have_rows(cls, value: list[list[Any]]) -> list[list[Any]]:
        if not value:
            raise ValueError("values must include at least one row")
        return value


class SheetsUpdateInput(BaseModel):
    range_name: str = Field(..., description="A1 notation target range, e.g. Audits!A2:K2.")
    values: list[list[Any]] = Field(..., description="2D values array to write.")
    spreadsheet_id: str | None = Field(default=None)


class GmailSendInput(BaseModel):
    to: list[str] = Field(..., description="Recipient email addresses.")
    subject: str = Field(..., min_length=1)
    body_text: str = Field(..., min_length=1)
    cc: list[str] = Field(default_factory=list)
    bcc: list[str] = Field(default_factory=list)


class PlaceSearchInput(BaseModel):
    query: str = Field(..., description="Business name/address query, e.g. 'BlitzMetrics Phoenix AZ'.")
    max_results: int = Field(5, ge=1, le=20)
    language_code: str = "en"
    region_code: str | None = None
    included_type: str | None = None


class PlaceDetailsInput(BaseModel):
    place_id: str = Field(..., description="Standalone place ID, not the full places/{id} resource name.")
    language_code: str = "en"


class PageSpeedInput(BaseModel):
    url: HttpUrl
    strategy: str = Field("mobile", pattern="^(mobile|desktop)$")
    categories: list[str] = Field(default_factory=lambda: ["performance", "seo", "accessibility", "best-practices"])

    @field_validator("categories")
    @classmethod
    def validate_categories(cls, categories: list[str]) -> list[str]:
        allowed = {"performance", "seo", "accessibility", "best-practices"}
        invalid = sorted(set(categories) - allowed)
        if invalid:
            raise ValueError(f"Invalid PageSpeed categories: {invalid}")
        return categories


def _score(category: dict[str, Any] | None) -> int | None:
    if not category or category.get("score") is None:
        return None
    return round(float(category["score"]) * 100)


def _audit_display_value(audit: dict[str, Any] | None) -> Any:
    if not audit:
        return None
    return audit.get("displayValue") or audit.get("numericValue")


def _crux_percentile(loading_experience: dict[str, Any], metric_name: str) -> Any:
    metric = (loading_experience or {}).get("metrics", {}).get(metric_name, {})
    return metric.get("percentile")


@mcp.tool()
def append_quick_audit_tracker_row(payload: SheetsAppendInput) -> dict[str, Any]:
    """Append one or more rows to the Quick Audit Tracker Google Sheet."""

    spreadsheet_id = payload.spreadsheet_id or _require_env("GOOGLE_SHEETS_SPREADSHEET_ID")
    service = _google_service("sheets", "v4")
    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=payload.range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body={"values": payload.values},
        )
        .execute()
    )
    return {
        "spreadsheet_id": spreadsheet_id,
        "range": payload.range_name,
        "updated_range": result.get("updates", {}).get("updatedRange"),
        "updated_rows": result.get("updates", {}).get("updatedRows"),
        "status": "ok",
    }


@mcp.tool()
def update_quick_audit_tracker_range(payload: SheetsUpdateInput) -> dict[str, Any]:
    """Update a specific A1 range in the Quick Audit Tracker Google Sheet."""

    spreadsheet_id = payload.spreadsheet_id or _require_env("GOOGLE_SHEETS_SPREADSHEET_ID")
    service = _google_service("sheets", "v4")
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=payload.range_name,
            valueInputOption="USER_ENTERED",
            body={"values": payload.values},
        )
        .execute()
    )
    return {
        "spreadsheet_id": spreadsheet_id,
        "updated_range": result.get("updatedRange"),
        "updated_rows": result.get("updatedRows"),
        "status": "ok",
    }


@mcp.tool()
def send_gmail_message(payload: GmailSendInput) -> dict[str, Any]:
    """Send a Gmail message only when ENABLE_GMAIL_SEND=true and safety checks pass."""

    if not _env_bool("ENABLE_GMAIL_SEND", default=False):
        raise PermissionError(
            "Gmail auto-send is disabled. Set ENABLE_GMAIL_SEND=true only after QA and sender safeguards are approved."
        )

    to = _validate_recipients(payload.to)
    cc = _validate_recipients(payload.cc) if payload.cc else []
    bcc = _validate_recipients(payload.bcc) if payload.bcc else []

    message = EmailMessage()
    message["To"] = ", ".join(to)
    if cc:
        message["Cc"] = ", ".join(cc)
    if bcc:
        message["Bcc"] = ", ".join(bcc)
    message["Subject"] = payload.subject
    message.set_content(payload.body_text)

    encoded = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    service = _google_service("gmail", "v1")
    result = service.users().messages().send(userId="me", body={"raw": encoded}).execute()
    return {"message_id": result.get("id"), "thread_id": result.get("threadId"), "status": "sent"}


@mcp.tool()
def resolve_business_place(payload: PlaceSearchInput) -> dict[str, Any]:
    """Resolve a business query to Google Places candidates and place IDs."""

    api_key = _require_env("GOOGLE_PLACES_API_KEY")
    body: dict[str, Any] = {
        "textQuery": payload.query,
        "languageCode": payload.language_code,
        "maxResultCount": payload.max_results,
    }
    if payload.region_code:
        body["regionCode"] = payload.region_code
    if payload.included_type:
        body["includedType"] = payload.included_type

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": DEFAULT_PLACE_FIELDS,
    }
    with httpx.Client(timeout=20.0) as client:
        response = client.post("https://places.googleapis.com/v1/places:searchText", headers=headers, json=body)
        response.raise_for_status()
        data = response.json()

    places = data.get("places", [])
    return {
        "query": payload.query,
        "count": len(places),
        "places": places,
    }


@mcp.tool()
def get_place_details(payload: PlaceDetailsInput) -> dict[str, Any]:
    """Fetch details for a Google Places place ID."""

    api_key = _require_env("GOOGLE_PLACES_API_KEY")
    place_id = payload.place_id.removeprefix("places/")
    params = {"languageCode": payload.language_code}
    headers = {
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": DEFAULT_PLACE_DETAIL_FIELDS,
    }
    url = f"https://places.googleapis.com/v1/places/{place_id}?{urlencode(params)}"
    with httpx.Client(timeout=20.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()


@mcp.tool()
def run_pagespeed_insights(payload: PageSpeedInput) -> dict[str, Any]:
    """Run PageSpeed Insights and return normalized mobile/desktop performance data."""

    api_key = os.getenv("PAGESPEED_API_KEY")
    params: list[tuple[str, str]] = [("url", str(payload.url)), ("strategy", payload.strategy)]
    for category in payload.categories:
        params.append(("category", category))
    if api_key:
        params.append(("key", api_key))

    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    with httpx.Client(timeout=60.0) as client:
        response = client.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

    lighthouse = data.get("lighthouseResult", {})
    categories = lighthouse.get("categories", {})
    audits = lighthouse.get("audits", {})
    loading_experience = data.get("loadingExperience", {})
    origin_loading_experience = data.get("originLoadingExperience", {})

    normalized = {
        "url": str(payload.url),
        "strategy": payload.strategy,
        "scores": {
            "performance": _score(categories.get("performance")),
            "seo": _score(categories.get("seo")),
            "accessibility": _score(categories.get("accessibility")),
            "best_practices": _score(categories.get("best-practices")),
        },
        "lab_metrics": {
            "largest_contentful_paint": _audit_display_value(audits.get("largest-contentful-paint")),
            "cumulative_layout_shift": _audit_display_value(audits.get("cumulative-layout-shift")),
            "total_blocking_time": _audit_display_value(audits.get("total-blocking-time")),
            "speed_index": _audit_display_value(audits.get("speed-index")),
            "first_contentful_paint": _audit_display_value(audits.get("first-contentful-paint")),
        },
        "field_data_75th_percentile": {
            "page_lcp_ms": _crux_percentile(loading_experience, "LARGEST_CONTENTFUL_PAINT_MS"),
            "page_inp_ms": _crux_percentile(loading_experience, "INTERACTION_TO_NEXT_PAINT"),
            "page_cls": _crux_percentile(loading_experience, "CUMULATIVE_LAYOUT_SHIFT_SCORE"),
            "origin_lcp_ms": _crux_percentile(origin_loading_experience, "LARGEST_CONTENTFUL_PAINT_MS"),
            "origin_inp_ms": _crux_percentile(origin_loading_experience, "INTERACTION_TO_NEXT_PAINT"),
            "origin_cls": _crux_percentile(origin_loading_experience, "CUMULATIVE_LAYOUT_SHIFT_SCORE"),
        },
        "core_web_vitals_assessment": {
            "page": loading_experience.get("overall_category"),
            "origin": origin_loading_experience.get("overall_category"),
        },
        "lighthouse_version": lighthouse.get("lighthouseVersion"),
        "fetch_time": lighthouse.get("fetchTime"),
    }
    return normalized


@mcp.tool()
def health_check() -> dict[str, Any]:
    """Return local configuration status without exposing secret values."""

    token_file = os.getenv("GOOGLE_OAUTH_TOKEN_FILE")
    return {
        "auth_mode": auth.auth_mode(),
        "service_account_configured": bool(
            os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON") or os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        ),
        "oauth_token_file_exists": bool(token_file) and Path(token_file).exists(),
        "sheets_spreadsheet_id_configured": bool(os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")),
        "places_api_key_configured": bool(os.getenv("GOOGLE_PLACES_API_KEY")),
        "pagespeed_api_key_configured": bool(os.getenv("PAGESPEED_API_KEY")),
        "gmail_send_enabled": _env_bool("ENABLE_GMAIL_SEND", default=False),
        "allowed_send_domains": _split_csv(os.getenv("QUICK_AUDIT_ALLOWED_SEND_DOMAINS")),
    }


if __name__ == "__main__":
    mcp.run()
