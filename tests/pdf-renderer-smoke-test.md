# PDF Renderer Smoke Test

## Purpose

Verify the renderer script can create a styled PDF from a valid spec.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Create `/tmp/sample-audit.json` using `examples/sample-audit-spec-json.md`.
2. Run `python3 skills/quick-audit-pdf-render/scripts/render-audit-pdf.py --spec /tmp/sample-audit.json --out /tmp/sample-audit.pdf`.
3. Confirm PDF exists and is non-empty.

## Pass criteria

- Command exits 0.
- PDF file exists.
- PDF has cover page and Executive Summary.

## Fail criteria

- Renderer import error.
- Missing reportlab.
- Empty or corrupted PDF.

