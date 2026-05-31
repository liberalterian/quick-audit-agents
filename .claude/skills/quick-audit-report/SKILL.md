---
name: quick-audit-report
description: Generate the customer-facing audit markdown and structured audit-spec JSON from graded Quick Audit data.
---

# Quick Audit Report Skill

## Read first

Load `references/source-docs/quick-audit-output-template-v2.md` before writing — it holds the exact
section structure, the required per-pillar tables/callouts, the voice rules, the 8-term glossary, and
the range-based projection format. Match it exactly. Note: the v1 sample in
`tests/golden/apparel-junction/` contains Glass Half Full + Revenue Translation + 13 glossary terms —
that is a v1 document; do NOT copy its format.

## Inputs

- Validated intake context.
- Enrichment record.
- Pillar grades.
- Grading Notes path.
- Templates in `templates/`.

## Outputs

- `<business-slug>-quick-audit-v1.md`
- `<business-slug>-audit.json`

## Required structure

1. Executive Summary
2. Business Snapshot
3. Footprint & Listings
4. Reviews & Reputation
5. Social Media
6. Website Performance
7. Brand Search
8. Keyword Rankings
9. The 90-Day Plan
10. What to Expect by Day 90
11. Next Steps
12. Appendix
13. Glossary

## Forbidden

- No Glass Half Full section.
- No per-pillar Revenue Translation paragraphs.
- No unsourced numeric claims.
