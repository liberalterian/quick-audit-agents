# Skill Index

This file maps each skill to its responsibility.

| Skill | Responsibility | Called by |
|---|---|---|
| `quick-audit-intake` | Validate and normalize intake payloads. | Orchestrator |
| `quick-audit-enrichment` | Collect GBP/Places, website, PageSpeed, social, Ahrefs, SERP, and ads signals. | Quick Audit Agent |
| `quick-audit-grading` | Apply anchored-reasoning grading and create Grading Notes. | Quick Audit Agent |
| `quick-audit-report` | Produce audit markdown and audit-spec JSON. | Quick Audit Agent |
| `quick-audit-pdf-render` | Render the styled PDF using `scripts/render-audit-pdf.py`. | Quick Audit Agent, Legacy fallback |
| `quick-audit-qualification` | Apply downstream qualification rubric. | Qualification Agent |
| `quick-audit-routing` | Upload artifacts, create emails, and write Tracker state. | Routing Agent |
| `legacy-quick-audit` | Phase 1 Cowork-compatible fallback wrapper. | Orchestrator/human |
