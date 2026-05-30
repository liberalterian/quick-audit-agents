# Dash-Case Path Regression Test

## Purpose

Ensure generated package paths avoid underscores.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Run `find . -name '*_*'`.
2. Inspect any results.
3. Allow only external dependency cache paths outside repo, if any.

## Pass criteria

- No repository file or directory name contains `_`.
- Python scripts use dash-case names.

## Fail criteria

- Any repo path contains an underscore.

