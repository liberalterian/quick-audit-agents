# Claude Routine API Reference

## Production trigger

Use an API trigger on one Claude Routine named `Quick Audit Runner`.

## Request shape

The Routine fire endpoint starts a new Claude Code session and accepts run-specific context in the `text` field.

## Required headers

- `Authorization: Bearer <routine-token>`
- `anthropic-beta: experimental-cc-routine-2026-04-01`
- `anthropic-version: 2023-06-01`
- `Content-Type: application/json`

## Response handling

Store the returned session ID and session URL in the Tracker row.

## Warning

Routine API is experimental. Keep this reference checked during updates and re-run `tests/routine-api-trigger-test.md` after API version changes.
