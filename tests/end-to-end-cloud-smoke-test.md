# End-to-End Cloud Smoke Test

## Purpose

Validate that the API-triggered Claude Routine can process one safe test intake from trigger to final Tracker writeback.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Use `examples/sample-intake-payload.md` with a safe test domain or controlled business record.
2. Fire the Routine with `examples/sample-zapier-routine-request.md`.
3. Store the session URL in the Tracker row.
4. Let the Routine complete.
5. Inspect Drive, Gmail Drafts, and Tracker state.

## Pass criteria

- Routine session starts successfully.
- Audit markdown, PDF, Grading Notes, and enrichment record are created.
- Prospect draft exists with PDF attached.
- Tracker row shows complete statuses and Routine session URL.
- Final output includes RUN COMPLETE.

## Fail criteria

- Routine fails to start.
- Any required artifact is missing.
- Tracker row is not updated.
- PDF rendering falls back to a generic renderer.

