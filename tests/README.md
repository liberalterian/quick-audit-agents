# Tests

Two layers:

- **Markdown checklists** (this directory) — run by an operator or by Claude in a session
  (paste a test and ask Claude to execute it and report PASS/FAIL per criterion). Grouped and
  sequenced in `reports/03-testing-and-deployment-plan.md` Part 1.
- **Automated** (`tests/automated/` + `quick_audit_mcp/tests/`) — `pytest` from the repo root:
  ```bash
  pytest quick_audit_mcp/tests tests/automated
  ```
- **Golden fixtures** (`tests/golden/`) — the v1 originals for fidelity comparison. See
  `tests/golden/README.md` for the grade-vs-format split.

## Common preconditions

Every markdown checklist assumes these unless it says otherwise (referenced as
`tests/README.md#common-preconditions`):

1. The repository is cloned/loaded (routine cloud session or local Claude Code).
2. `bash scripts/setup.sh` has run successfully (deps installed, import smoke passed).
3. Required credentials/secrets are configured (see `references/integration-environment-reference.md`).
4. For cloud tests: the routine exists with an API trigger; the fire URL + token are available.
5. Use **test** spreadsheets/domains/recipients — never live prospect data.

## Run order

Infrastructure (A) → Artifact correctness (B) → Format regressions (C) → Logic (D) →
End-to-end & golden (E). A failure in group A blocks the rest. Full mapping in `reports/03`.
