# Expert Services Smoke Test

## Purpose

Validate a cold-submission style audit produces complete artifacts without relying on a golden answer.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Run the Expert Services sample/cold test payload if available.
2. Inspect enrichment coverage.
3. Inspect PDF render.
4. Inspect qualification output.

## Pass criteria

- All artifacts are generated.
- Any unavailable data is called out.
- Report is coherent and sourced.

## Fail criteria

- Fabricated numbers appear.
- Missing artifact.
- Hard failure is not recorded in Tracker.

