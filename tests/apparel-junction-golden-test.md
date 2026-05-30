# Apparel Junction Golden Test

## Purpose

Confirm the system can reproduce the Apparel Junction calibration structure and grade bands.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Run the known Apparel Junction intake.
2. Compare pillar scores to anchor values.
3. Confirm document structure matches v2.
4. Confirm Grading Notes cite anchor reasoning.

## Pass criteria

- Overall grade is D.
- Pillar grades are within acceptable anchor tolerance.
- No Glass Half Full or Revenue Translation sections.
- Grading Notes include signals, anchor, grade, rationale.

## Fail criteria

- Overall grade drifts materially without justification.
- Output reverts to v1 format.
- Grading Notes are missing or shallow.

