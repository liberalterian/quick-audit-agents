# Audit Spec Schema Test

## Purpose

Validate that audit-spec JSON conforms to renderer expectations before PDF rendering.

## Preconditions

- Claude Routine exists or local Claude Code session is available.
- Repository files are present.
- Required credentials are configured for the test.

## Steps

1. Generate audit-spec JSON.
2. Confirm top-level keys: `meta`, `exec_summary`, `sections`.
3. Confirm required `meta` fields.
4. Confirm every section block has a known `type`.
5. Confirm no section appears after Glossary.

## Pass criteria

- JSON parses.
- Required top-level keys exist.
- Renderer block types are valid.
- Section order is correct.

## Fail criteria

- JSON parse failure.
- Unknown block type.
- Missing cover-page metadata.
- Glass Half Full section appears.

