# Sample Zapier Routine Request

```bash
curl -X POST "$QUICK-AUDIT-ROUTINE-FIRE-URL" \
  -H "Authorization: Bearer $QUICK-AUDIT-ROUTINE-TOKEN" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "{\"event-type\":\"quick-audit-intake\",\"submission-id\":\"qa-test-0001\",\"business-name\":\"Example Services\",\"website\":\"https://example-services.test\",\"primary-city\":\"Denver\",\"state\":\"CO\",\"annual-revenue-band\":\"$2M–5M\",\"contact-name\":\"Jane Owner\",\"contact-email\":\"jane@example-services.test\",\"contact-phone\":\"+13035550100\",\"tracker-row-id\":\"tracker-row-0001\",\"partner-id\":\"default\"}"
  }'
```
