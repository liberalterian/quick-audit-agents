# Sample Zapier Routine Request

Shell/env variable names use underscores (dashes are invalid in shell variable names). The fire URL
is the official per-routine endpoint `https://api.anthropic.com/v1/claude_code/routines/<trig_id>/fire`,
stored in `$QUICK_AUDIT_ROUTINE_FIRE_URL`. The intake JSON is a stringified value inside `text`.

```bash
curl -X POST "$QUICK_AUDIT_ROUTINE_FIRE_URL" \
  -H "Authorization: Bearer $QUICK_AUDIT_ROUTINE_TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "{\"event-type\":\"quick-audit-intake\",\"submission-id\":\"qa-test-0001\",\"business-name\":\"Example Services\",\"website\":\"https://example-services.test\",\"primary-city\":\"Denver\",\"state\":\"CO\",\"annual-revenue-band\":\"$2M-5M\",\"contact-name\":\"Jane Owner\",\"contact-email\":\"jane@example-services.test\",\"contact-phone\":\"+13035550100\",\"tracker-row-id\":\"tracker-row-0001\",\"partner-id\":\"default\"}"
  }'
```
