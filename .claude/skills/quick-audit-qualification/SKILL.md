---
name: quick-audit-qualification
description: Apply the downstream MVS qualification rubric to an enriched prospect.
---

# Quick Audit Qualification Skill

## Inputs

- Intake context.
- Enrichment record.
- `evals/mvs-qualification-rubric.md`.

## Output

```json
{
  "decision": "HARD-PASS | SOFT-FAIL | HARD-FAIL",
  "hard-fail-reasons": [],
  "soft-fail-signals": [],
  "criteria": {}
}
```

## Rule

Qualification is independent of audit pillar grades.
