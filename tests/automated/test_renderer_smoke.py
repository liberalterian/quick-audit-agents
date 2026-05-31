"""Renderer smoke test: a minimal valid spec produces a non-empty PDF.

Invokes the renderer as a subprocess (its filename uses a hyphen, so it is not importable as a
module). Skips cleanly if reportlab is not installed in the current environment.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
RENDERER = ROOT / ".claude" / "skills" / "quick-audit-pdf-render" / "scripts" / "render-audit-pdf.py"

MINIMAL_SPEC = {
    "meta": {
        "business_name": "Smoke Test Co",
        "business_descriptor": "Plumbing",
        "business_location_label": "Denver, CO",
        "contact_name": "Jane Owner",
        "address_lines": ["123 Main St, Denver, CO"],
        "phone": "(303) 555-0100",
        "website": "smoketest.example",
        "issue_date": "May 30, 2026",
        "order_number": "SMOKE001",
        "auditor_org": "BlitzMetrics  &bull;  Local Service Spotlight",
        "auditor_contact_line": "Local Service Spotlight  &bull;  dennis@blitzmetrics.com",
        "footer_brand_line": "Smoke Test Co Quick Audit  |  Prepared by BlitzMetrics",
    },
    "exec_summary": {
        "lede": "Smoke test lede.",
        "overall_grade": {"letter": "C", "name": "Functional", "oneliner": "Test."},
        "pillars": [{"letter": "C", "title": "1. Footprint", "text": "ok"}],
        "scores": [{"pillar": "Footprint & Listings", "score": "60 / 100"}],
        "bottom_line": "Bottom line.",
    },
    "sections": [],
}


def test_renderer_produces_pdf(tmp_path):
    pytest.importorskip("reportlab")
    assert RENDERER.exists(), f"renderer not found at {RENDERER}"
    spec = tmp_path / "spec.json"
    out = tmp_path / "out.pdf"
    spec.write_text(json.dumps(MINIMAL_SPEC), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(RENDERER), "--spec", str(spec), "--out", str(out)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"renderer failed: {result.stderr}"
    assert out.exists() and out.stat().st_size > 1000, "PDF missing or too small"
