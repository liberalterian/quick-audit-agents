# Manifest

Package: `quick-audit-system` v2.1.0. Inventory of tracked files (regenerated after the routine
cloud-deployment refactor).

## Root

- `CLAUDE.md` — orchestrator directive (auto-loaded each routine run).
- `README.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `CHANGELOG.md`, `MANIFEST.md`
- `claude-routine-setup-guide.md`, `agent-skill-architecture-audit.md`
- `.mcp.json` — Ahrefs hosted MCP + local `quick-audit-tools` server.
- `.claude-plugin/plugin.json` — plugin manifest (optional `/plugin` install path).
- `.gitignore`, `pytest.ini`
- `scripts/setup.sh` — routine Build/Setup Command.

## Agents (`.claude/agents/`)

- `quick-audit-orchestrator-agent.md`, `quick-audit-agent.md`, `qualification-agent.md`, `routing-agent.md`

## Skills (`.claude/skills/`)

- `skill-index.md`
- `quick-audit-intake/SKILL.md`
- `quick-audit-enrichment/SKILL.md`
- `quick-audit-grading/SKILL.md` (+ `evals/anchored-grading-rubric.md`, `references/grading-approach-guide.md`)
- `quick-audit-report/SKILL.md` (+ `templates/{quick-audit-output-template,grading-notes-template,audit-spec-json-template}.md`, `references/quick-audit-format-guide.md`)
- `quick-audit-pdf-render/SKILL.md` (+ `scripts/render-audit-pdf.py`, `scripts/build-audit-spec-example.py`)
- `quick-audit-qualification/SKILL.md` (+ `evals/mvs-qualification-rubric.md`)
- `quick-audit-routing/SKILL.md`
- `legacy-quick-audit/SKILL.md`

## Local MCP server (`quick_audit_mcp/`)

- `server.py`, `auth.py`, `__init__.py`
- `pyproject.toml`, `requirements.txt`, `.env.example`, `.gitignore`, `README.md`
- `scripts/validate_mcp_config.py`
- `tests/test_mcp_config.py`
- `docs/{setup.md,security-and-scopes.md,architecture.md}`

## References (`references/`)

- `README.md` (source map + anchors + positioning)
- `mcp-configuration-guide.md`, `claude-routine-api-reference.md`, `integration-environment-reference.md`
- `ahrefs-mcp-reference.md`, `google-workspace-mcp-reference.md`, `google-places-api-reference.md`,
  `google-sheets-tracker-writeback-reference.md`, `plugin-structure-reference.md`
- `source-docs/` — `quick-audit-agent-definition-v2.md`, `quick-audit-output-template-v2.md`,
  `quick-audit-grading-approach-v1.md`, `quick-audit-automation-plan-v1.md`, `system-overview-v1.md`

## Examples (`examples/`)

- `sample-intake-payload.md`, `sample-enrichment-record.md`, `sample-grading-notes.md`,
  `sample-qualification-output.md`, `sample-audit-spec-json.md`, `sample-run-complete-event.md`,
  `sample-tracker-row.md`, `sample-drive-folder-layout.md`, `sample-zapier-routine-request.md`

## Tests (`tests/`)

- `README.md` (common preconditions + run order)
- Manual checklists: `end-to-end-cloud-smoke-test.md`, `routine-api-trigger-test.md`,
  `mcp-connection-test.md`, `google-places-direct-api-test.md`, `google-sheets-tracker-writeback-test.md`,
  `audit-spec-schema-test.md`, `pdf-renderer-smoke-test.md`, `apparel-junction-golden-test.md`,
  `expert-services-smoke-test.md`, `no-glass-half-full-regression-test.md`,
  `grading-notes-completeness-test.md`, `qualification-rubric-test-cases.md`, `routing-delivery-test.md`,
  `legacy-fallback-smoke-test.md`, `dash-case-path-regression-test.md`, `source-doc-consistency-test.md`
- Automated (`tests/automated/`): `test_server_imports.py`, `test_forbidden_sections.py`,
  `test_grades_golden.py`, `test_renderer_smoke.py`
- Golden fixtures (`tests/golden/`): `README.md`, `format-reference/Apparel_Junction_Quick_Audit.pdf`,
  `apparel-junction/ApparelJunction_{Grading-Notes,Quick-Audit}_v1.md`,
  `expert-services/ExpertServicesUtah_{Grading-Notes,Quick-Audit}_v1.md` + `…_v1.pdf`

## Reports (`reports/`)

- `01-audit-report.md`, `02-refactor-plan.md`, `03-testing-and-deployment-plan.md`
