# Expert Services Intake (golden v2 cold-run payload)

Drives the v2 format + grade fidelity test. Expected: pillars 40 / 75 / 45 / 55 / 45 / 45 → Overall
**C 51**, with v2-compliant format (no Glass Half Full, no Revenue Translation, 8 glossary terms). See
`tests/golden/expert-services/`. The live Knowledge-Panel review-count check is mandatory (skipping it
caused the documented one-letter miss).

```json
{
  "event-type": "quick-audit-intake",
  "submission-id": "qa-golden-expert-services",
  "business-name": "Expert Services",
  "website": "https://expertservicesutah.com",
  "primary-city": "Orem",
  "state": "UT",
  "annual-revenue-band": "$2M-5M",
  "contact-name": "Owner / Operations Lead",
  "contact-email": "info@expertservicesutah.com",
  "contact-phone": "+13854465727",
  "tracker-row-id": "golden-es-row",
  "partner-id": "default"
}
```
