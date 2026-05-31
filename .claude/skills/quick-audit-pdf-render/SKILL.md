---
name: quick-audit-pdf-render
description: Render a Quick Audit audit-spec JSON file into the styled prospect-facing PDF.
---

# Quick Audit PDF Render Skill

## Inputs

- `audit-spec-json` path.
- Output PDF path.

## Script

Use:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/render-audit-pdf.py \
  --spec /tmp/<business-slug>-audit.json \
  --out /tmp/<business-slug>-quick-audit-v1.pdf
```

`${CLAUDE_SKILL_DIR}` resolves to this skill's directory regardless of the working directory, so the
command works whether the system runs as a plugin or from a cloned-repo routine.

## Rules

- Do not use the generic PDF skill as fallback.
- If rendering fails, fix the JSON spec and rerun.
- The renderer is the single source of truth for visual styling.
