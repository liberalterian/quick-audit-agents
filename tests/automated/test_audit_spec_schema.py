"""Audit-spec JSON schema guard (automates tests/audit-spec-schema-test.md).

Validates the sample spec shape the renderer expects: top-level keys, known block types, and no
section after the Glossary (id 13).
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "examples" / "sample-audit-spec-json.md"

KNOWN_BLOCK_TYPES = {
    "h3", "paragraph", "spacer", "grade_banner", "stat_callout",
    "data_table", "callout", "bullets", "centered",
}


def _load_spec() -> dict:
    text = SAMPLE.read_text(encoding="utf-8")
    m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    assert m, "no JSON block in sample-audit-spec-json.md"
    return json.loads(m.group(1))


def test_top_level_keys():
    spec = _load_spec()
    assert {"meta", "exec_summary", "sections"}.issubset(spec)


def test_required_meta_fields():
    meta = _load_spec()["meta"]
    for field in ("business_name", "business_location_label", "issue_date", "order_number"):
        assert field in meta and meta[field], f"missing meta.{field}"


def test_block_types_known_and_no_section_after_glossary():
    spec = _load_spec()
    for section in spec.get("sections", []):
        sid = str(section.get("id", ""))
        assert sid != "13" or section is spec["sections"][-1], "a section appears after the Glossary"
        for block in section.get("blocks", []):
            assert block.get("type") in KNOWN_BLOCK_TYPES, f"unknown block type: {block.get('type')}"
