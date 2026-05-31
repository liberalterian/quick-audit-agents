"""Grade-fidelity guard: the Apparel Junction calibration anchor grades must stay intact.

Parses the imported v1 grading-notes golden and asserts the six pillar scores and the Overall.
If the fixture is corrupted or replaced, fidelity comparison silently loses its anchor — this catches that.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "tests" / "golden" / "apparel-junction" / "ApparelJunction_Grading-Notes_v1.md"

EXPECTED = [42, 55, 38, 40, 35, 18]  # Footprint, Reviews, Social, Website, Brand Search, Keywords


def test_pillar_scores_match_anchor():
    text = GOLDEN.read_text(encoding="utf-8")
    scores = [int(m) for m in re.findall(r"\*\*Grade:\*\*\s+[A-F]\s+\((\d+)/100\)", text)]
    assert scores == EXPECTED, f"anchor pillar scores drifted: {scores}"


def test_overall_is_d_38():
    text = GOLDEN.read_text(encoding="utf-8")
    assert round(sum(EXPECTED) / 6) == 38
    assert re.search(r"=\s*\*\*38\*\*\s*(?:->|→)\s*\*\*D\*\*", text)
