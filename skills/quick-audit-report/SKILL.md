---
name: quick-audit-report
description: Generate the customer-facing audit markdown and structured audit-spec JSON from graded Quick Audit data.
---

# Quick Audit Report Skill

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
