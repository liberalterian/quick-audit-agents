# Google Places Direct API Test

## Purpose

Verify direct Google Places lookup works because no verified official Places data MCP is bundled.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Set `GOOGLE_PLACES_API_KEY` (the exact variable the server reads — there is no dash-case env var).
2. Run a Text Search for a known test business.
3. Use the returned place ID to call Place Details.
4. Confirm field mask returns expected fields.

## Pass criteria

- Text Search returns candidate places.
- Place Details returns display name, address, phone/website where available, rating, user rating count, and business status.
- API key is not logged.

## Fail criteria

- Missing field mask.
- API key committed to repo.
- Response does not include enough identity data to resolve the business.

