# Google Places API Reference

## Why direct API is used

The verified Google Maps Code Assist MCP endpoint is for Google Maps Platform documentation and code samples. It is not a business-data Places API server. Therefore production business identity resolution should use the Google Places API directly unless the team wires a trusted internal Places MCP.

## Required operations

1. Text Search to resolve business name + city + state to candidate places.
2. Place Details to pull address, phone, website, categories/types, rating, user rating count, business status, hours, and reviews where available.

## Required environment variable

- `GOOGLE-MAPS-API-KEY` or equivalent secret configured in the Routine environment.

## Suggested fields

Use field masks to avoid over-fetching and unexpected cost. Minimum useful fields include:

- `id`
- `displayName`
- `formattedAddress`
- `nationalPhoneNumber`
- `internationalPhoneNumber`
- `websiteUri`
- `rating`
- `userRatingCount`
- `businessStatus`
- `types`
- `primaryType`
- `regularOpeningHours`
- `photos`
- `reviews`

## Test

Run `tests/google-places-direct-api-test.md` before production.
