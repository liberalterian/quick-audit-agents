---
name: quick-audit-routing
description: Upload artifacts, create Gmail drafts or sends, create team alerts, and write final Tracker state.
---

# Quick Audit Routing Skill

## Inputs

- Audit markdown.
- Audit PDF.
- Grading Notes markdown.
- Qualification decision.
- Tracker row ID.
- Partner config.

## Actions

1. Upload artifacts to Drive.
2. Create prospect Gmail draft with PDF attached.
3. If HARD-PASS or SOFT-FAIL, create team alert draft.
4. Write final Tracker state.
5. Return routing record.

## Delivery mode

Default is draft-first. Do not auto-send until Gmail send has passed production tests.
