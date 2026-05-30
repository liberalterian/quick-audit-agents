# Qualification Rubric Test Cases

## Purpose

Validate MVS qualification aggregation logic.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Test all-hard-pass case.
2. Test revenue soft-fail only.
3. Test reviews soft-fail only.
4. Test any hard-fail case.
5. Test multiple soft-fails without hard-fail.

## Pass criteria

- Any hard fail returns HARD-FAIL.
- Any soft fail without hard fail returns SOFT-FAIL.
- All hard pass returns HARD-PASS.

## Fail criteria

- Soft fail overrides hard fail.
- Pillar grades affect qualification.
- Missing reasons/signals in output.

