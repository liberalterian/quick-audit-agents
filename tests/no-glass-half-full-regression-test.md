# No Glass Half Full Regression Test

## Purpose

Prevent stale v1 structure from reappearing.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Search generated audit markdown for `Glass Half Full`.
2. Search generated PDF text if extractable.
3. Search report-generation prompts/templates.

## Pass criteria

- No customer-facing audit includes Glass Half Full.
- Legacy fallback also respects v2 structure.

## Fail criteria

- Any generated v2 audit contains a Glass Half Full section.

