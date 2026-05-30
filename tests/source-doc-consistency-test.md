# Source Doc Consistency Test

## Purpose

Ensure generated modular docs remain consistent with source reference docs.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Compare output section order against source template.
2. Compare grading flow against grading approach source.
3. Compare automation responsibilities against architecture source.
4. Record intentional changes in changelog.

## Pass criteria

- Intentional changes are documented.
- No stale v1 output rules are present in production docs.

## Fail criteria

- Current docs contradict source-of-truth v2 rules.
- Changelog omits a major architectural change.

