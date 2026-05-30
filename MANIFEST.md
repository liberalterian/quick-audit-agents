# Manifest

Generated package: `quick-audit-production-package`

## Root

- `.mcp.json` — Project-scoped MCP configuration for verified remote MCP endpoints.
- `.claude-plugin/plugin.json` — Claude Code plugin manifest.
- `readme.md` — Setup and overview.
- `changelog.md` — Current change history.
- `architecture.md` — System architecture.
- `roadmap.md` — Development strategy.
- `claude-routine-setup-guide.md` — Claude Routine setup and API trigger instructions.
- `agent-skill-architecture-audit.md` — Agent/skill relationship evaluation.
- `manifest.md` — This file.

## Agents

- `agents/quick-audit-orchestrator-agent.md`
- `agents/quick-audit-agent.md`
- `agents/qualification-agent.md`
- `agents/routing-agent.md`

## Skills

- `skills/skill-index.md`
- `skills/quick-audit-intake/SKILL.md`
- `skills/quick-audit-enrichment/SKILL.md`
- `skills/quick-audit-grading/SKILL.md`
- `skills/quick-audit-grading/evals/anchored-grading-rubric.md`
- `skills/quick-audit-grading/references/grading-approach-guide.md`
- `skills/quick-audit-report/SKILL.md`
- `skills/quick-audit-report/templates/quick-audit-output-template.md`
- `skills/quick-audit-report/templates/grading-notes-template.md`
- `skills/quick-audit-report/templates/audit-spec-json-template.md`
- `skills/quick-audit-report/references/quick-audit-format-guide.md`
- `skills/quick-audit-pdf-render/SKILL.md`
- `skills/quick-audit-pdf-render/scripts/render-audit-pdf.py`
- `skills/quick-audit-pdf-render/scripts/build-audit-spec-example.py`
- `skills/quick-audit-qualification/SKILL.md`
- `skills/quick-audit-qualification/evals/mvs-qualification-rubric.md`
- `skills/quick-audit-routing/SKILL.md`
- `skills/legacy-quick-audit/SKILL.md`

## References

- `references/automation-architecture-reference.md`
- `references/gct-positioning-reference.md`
- `references/calibration-anchors.md`
- `references/system-source-map.md`
- `references/mcp-configuration-guide.md`
- `references/google-workspace-mcp-reference.md`
- `references/ahrefs-mcp-reference.md`
- `references/google-places-api-reference.md`
- `references/google-sheets-tracker-writeback-reference.md`
- `references/claude-routine-api-reference.md`
- `references/plugin-structure-reference.md`
- `references/integration-environment-reference.md`
- `references/source-docs/quick-audit-agent-definition-v2.md`
- `references/source-docs/quick-audit-output-template-v2.md`
- `references/source-docs/quick-audit-grading-approach-v1.md`
- `references/source-docs/quick-audit-automation-plan-v1.md`
- `references/source-docs/system-overview-v1.md`

## Examples

- `examples/sample-intake-payload.md`
- `examples/sample-enrichment-record.md`
- `examples/sample-qualification-output.md`
- `examples/sample-run-complete-event.md`
- `examples/sample-audit-spec-json.md`
- `examples/sample-zapier-routine-request.md`
- `examples/sample-tracker-row.md`
- `examples/sample-grading-notes.md`
- `examples/sample-drive-folder-layout.md`

## Tests

- `tests/end-to-end-cloud-smoke-test.md`
- `tests/routine-api-trigger-test.md`
- `tests/mcp-connection-test.md`
- `tests/google-places-direct-api-test.md`
- `tests/google-sheets-tracker-writeback-test.md`
- `tests/audit-spec-schema-test.md`
- `tests/pdf-renderer-smoke-test.md`
- `tests/apparel-junction-golden-test.md`
- `tests/expert-services-smoke-test.md`
- `tests/no-glass-half-full-regression-test.md`
- `tests/grading-notes-completeness-test.md`
- `tests/qualification-rubric-test-cases.md`
- `tests/routing-delivery-test.md`
- `tests/legacy-fallback-smoke-test.md`
- `tests/dash-case-path-regression-test.md`
- `tests/source-doc-consistency-test.md`
