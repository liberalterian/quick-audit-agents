# Golden Fixtures (v1 originals)

Imported from the original system (`QuickAudit-System-v1`, owner/stakeholder **Dan Pasker**;
"Prepared by Daniel Goodrich", replicating Dennis Yu / BlitzMetrics' published Quick Audit). Used to
prove fidelity of the v2 system. See methodology in `reports/03-testing-and-deployment-plan.md` Part 2.

## CRITICAL: fidelity is two different comparisons (grades vs. format)

| File | Golden for | NOT a golden for |
|---|---|---|
| `apparel-junction/ApparelJunction_Grading-Notes_v1.md` | **Grades** — 42/55/38/40/35/18 → **D 38** | — |
| `apparel-junction/ApparelJunction_Quick-Audit_v1.md` | reference only | **Format** — this is a v1 document: it has a "Glass Half Full" section, per-pillar "Revenue translation:" paragraphs, and 13 glossary terms |
| `format-reference/Apparel_Junction_Quick_Audit.pdf` | **Canonical format** (Dennis's published PDF) | — |
| `expert-services/ExpertServicesUtah_Grading-Notes_v1.md` | **Grades** — 40/75/45/55/45/45 → **C 51** + the live-GBP regrade lesson | — |
| `expert-services/ExpertServicesUtah_Quick-Audit_v1.md` | **v2 format + grades** (8 glossary terms, no GHF/RT) | — |
| `expert-services/ExpertServicesUtah_Quick-Audit_v1.pdf` | rendered-PDF visual reference | — |

**Do not** make a new v2 run reproduce the Apparel Junction markdown's extra sections — that would
be a regression, not fidelity. Match grades to the grading notes and format to Dennis's PDF / the
Expert Services v2 markdown.
