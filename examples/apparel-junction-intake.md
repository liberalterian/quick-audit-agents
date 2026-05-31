# Apparel Junction Intake (golden calibration payload)

Drives the grade-fidelity golden test. A faithful run must reproduce the Apparel Junction anchor
grades — pillars 42 / 55 / 38 / 40 / 35 / 18 → Overall **D 38** (see
`tests/golden/apparel-junction/ApparelJunction_Grading-Notes_v1.md`). Format must follow v2 (NOT the
v1 sample markdown, which contains Glass Half Full + Revenue Translation + 13 glossary terms).

```json
{
  "event-type": "quick-audit-intake",
  "submission-id": "qa-golden-apparel-junction",
  "business-name": "Apparel Junction",
  "website": "https://appareljunction.com",
  "primary-city": "Arlington",
  "state": "TX",
  "annual-revenue-band": "$1M-2M",
  "contact-name": "Jonathan Astie",
  "contact-email": "sales@appareljunction.com",
  "contact-phone": "+18172646564",
  "tracker-row-id": "golden-aj-row",
  "partner-id": "default"
}
```
