# Routine API Trigger Test

## Purpose

Verify Zapier or curl can start the Claude Routine with the expected headers and `text` body.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Set Routine URL and token in environment.
2. Run the sample curl request.
3. Confirm HTTP success response.
4. Copy returned session URL to the Tracker test row.

## Pass criteria

- Response includes session ID or session URL.
- Routine receives the payload text.
- No authentication or beta-header error occurs.

## Fail criteria

- 401/403 from token failure.
- 400 from missing beta header.
- Routine starts but cannot parse intake JSON.

