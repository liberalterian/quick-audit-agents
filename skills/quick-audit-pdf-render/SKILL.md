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
python3 skills/quick-audit-pdf-render/scripts/render-audit-pdf.py   --spec /tmp/<business-slug>-audit.json   --out /tmp/<business-slug>-quick-audit-v1.pdf
```

## Rules

- Do not use the generic PDF skill as fallback.
- If rendering fails, fix the JSON spec and rerun.
- The renderer is the single source of truth for visual styling.
