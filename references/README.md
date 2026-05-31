# References

Pointers into the source-of-truth design docs plus the key calibration facts. (Consolidates the
former `system-source-map.md`, `calibration-anchors.md`, `gct-positioning-reference.md`, and
`automation-architecture-reference.md`.)

## Source map — v1/v2 design docs (the fidelity baseline)

- Agent definition: `references/source-docs/quick-audit-agent-definition-v2.md`
- Output template: `references/source-docs/quick-audit-output-template-v2.md`
- Grading approach: `references/source-docs/quick-audit-grading-approach-v1.md`
- Automation plan / architecture source: `references/source-docs/quick-audit-automation-plan-v1.md`
  (production architecture is summarized in `ARCHITECTURE.md`)
- System overview: `references/source-docs/system-overview-v1.md`

## Calibration anchors

- **Apparel Junction** — Overall **D 38** (pillars 42 / 55 / 38 / 40 / 35 / 18). D-tier reference.
- **RiteWay Heating, Cooling & Plumbing** — Overall **A ~90**. A-tier reference.

Full per-pillar reasoning: `references/source-docs/quick-audit-grading-approach-v1.md` §6.
Golden artifacts (grades + format): `tests/golden/`.

## Positioning (GCT)

Goals, Content, Targeting — produce useful Quick Audits, generate concrete audit/report/routing
content, targeting US local-service businesses that benefit from Maps Visibility work.

## Other references in this folder

- `mcp-configuration-guide.md` — MCP servers + connector strategy
- `claude-routine-api-reference.md` — `/fire` endpoint, headers, `text` contract
- `ahrefs-mcp-reference.md`, `google-workspace-mcp-reference.md`
- `google-places-api-reference.md`, `google-sheets-tracker-writeback-reference.md`
- `plugin-structure-reference.md`, `integration-environment-reference.md`
