"""Format-fidelity regression: the v2 output must NOT contain v1-only sections.

Runs against the v2 format golden (Expert Services). The Apparel Junction markdown is a v1
document and is intentionally NOT checked here (it legitimately contains the forbidden sections).
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V2_GOLDEN = ROOT / "tests" / "golden" / "expert-services" / "ExpertServicesUtah_Quick-Audit_v1.md"

CANONICAL_GLOSSARY = {
    "NAP", "DR", "E-E-A-T", "GBP", "Knowledge Panel", "Local Pack", "LSA", "Schema",
}
V1_EXTRA_GLOSSARY = {"PSI", "CWV", "CallRail", "CTR", "CPC"}


def _text() -> str:
    return V2_GOLDEN.read_text(encoding="utf-8")


def test_no_glass_half_full():
    assert "glass half full" not in _text().lower()


def test_no_per_pillar_revenue_translation():
    assert "revenue translation" not in _text().lower()


def test_ends_at_glossary():
    t = _text()
    assert "GLOSSARY" in t
    tail = t[t.rindex("GLOSSARY"):]
    # Nothing structural after the glossary (no new "# NN SECTION" header).
    assert not re.search(r"\n#\s+\d{2}\s+[A-Z]", tail)


def test_glossary_is_eight_canonical_terms():
    t = _text()
    for term in CANONICAL_GLOSSARY:
        assert term in t, f"missing canonical glossary term: {term}"
    for extra in V1_EXTRA_GLOSSARY:
        # the v1 extras must not appear as glossary rows in v2 output
        assert f"| {extra} " not in t, f"v1-only glossary term present: {extra}"
