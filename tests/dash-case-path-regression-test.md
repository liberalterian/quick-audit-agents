# Dash-Case Path Regression Test

## Purpose

Keep authored content paths (skills, agents, references, examples, docs) in dash-case, **without**
flagging the Python package — Python identifiers and modules MUST use underscores, so
`quick_audit_mcp/**` and any `*.py` are explicitly exempt.

## Common preconditions

See `tests/README.md#common-preconditions`.

## Steps

1. Run, from the repo root:
   ```bash
   find . -name '*_*' \
     -not -path './.git/*' \
     -not -path './quick_audit_mcp/*' \
     -not -path './.venv/*' \
     -not -name '*.py' \
     -not -name 'pytest.ini'
   ```
2. Inspect any results.
3. The only expected `_` paths are the Python package (`quick_audit_mcp/`), `*.py` files, and the
   imported v1 golden fixtures under `tests/golden/` (their original filenames are preserved on purpose).

## Pass criteria

- No authored content file/dir (skills, agents, references, examples, top-level docs) contains `_`.
- Python package paths and `*.py` files are allowed to (and must) use underscores.
- `tests/golden/**` original v1 filenames are allowed (they reproduce the original artifacts verbatim).

## Fail criteria

- A skill/agent/reference/example/doc path uses an underscore.
- A `.py` file or the `quick_audit_mcp/` package is renamed to dash-case (this breaks importability).
