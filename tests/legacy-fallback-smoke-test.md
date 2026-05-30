# Legacy Fallback Smoke Test

## Purpose

Confirm `legacy-quick-audit` can run without duplicating renderer logic.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Invoke `legacy-quick-audit` manually in a test session.
2. Process one test row.
3. Confirm it calls the shared renderer script.
4. Confirm output still follows v2 structure.

## Pass criteria

- Fallback completes.
- Shared renderer is used.
- V2 structure is preserved.

## Fail criteria

- Fallback contains stale v1 sections.
- Fallback uses a separate renderer.

