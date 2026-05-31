"""MVS qualification aggregation guard (automates tests/qualification-rubric-test-cases.md).

This encodes the aggregation RULE from `.claude/skills/quick-audit-qualification/evals/
mvs-qualification-rubric.md` as a reference implementation so the expected outcomes are pinned.
(The agent performs qualification at runtime; this test guards the rule, not the agent.)
"""

import pytest


def aggregate(criteria: dict[str, str]) -> str:
    """criteria values are 'hard_pass' | 'soft_fail' | 'hard_fail'."""
    vals = set(criteria.values())
    if "hard_fail" in vals:
        return "HARD-FAIL"
    if "soft_fail" in vals:
        return "SOFT-FAIL"
    return "HARD-PASS"


CASES = [
    ({"revenue": "hard_pass", "reviews": "hard_pass", "gbp": "hard_pass"}, "HARD-PASS"),
    ({"revenue": "soft_fail", "reviews": "hard_pass", "gbp": "hard_pass"}, "SOFT-FAIL"),
    ({"revenue": "hard_pass", "reviews": "soft_fail", "gbp": "hard_pass"}, "SOFT-FAIL"),
    ({"revenue": "hard_fail", "reviews": "hard_pass", "gbp": "hard_pass"}, "HARD-FAIL"),
    ({"revenue": "soft_fail", "reviews": "soft_fail", "gbp": "hard_fail"}, "HARD-FAIL"),
]


@pytest.mark.parametrize("criteria,expected", CASES)
def test_aggregation(criteria, expected):
    assert aggregate(criteria) == expected


def test_hard_fail_dominates_soft_fail():
    assert aggregate({"a": "soft_fail", "b": "hard_fail"}) == "HARD-FAIL"
