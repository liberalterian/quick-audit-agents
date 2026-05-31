# Quick Audit System

Production Claude Code / Claude Routine package for running the Quick Audit workflow — a six-pillar
local-SEO audit for US local-service businesses in the Dennis Yu / BlitzMetrics (Local Service
Spotlight) format. Originally built as the v1 Cowork-scheduled system (owner/stakeholder **Dan
Pasker**); this package is the modular, cloud-deployable v2.

## What it does

Accepts a structured prospect intake payload → enriches the business (GBP/Places, website, PageSpeed,
social, Ahrefs, brand SERP) → grades six pillars by anchored reasoning → writes the customer-facing
audit markdown → renders the styled PDF → qualifies against the MVS rubric → drafts routing emails →
uploads artifacts to Drive → writes final state to the Tracker.

## Production runtime

An **API-triggered Claude Routine**. SPP/intake writes the Tracker row; Zapier (or the intake backend)
POSTs the payload to the routine `/fire` endpoint as a **stringified JSON in the `text` field**. The
routine runs in Anthropic-managed cloud infrastructure, clones this repo, runs `scripts/setup.sh`,
loads `CLAUDE.md`, and the main session acts as the orchestrator.

## Repository layout

```
CLAUDE.md                      # orchestrator directive (auto-loaded each run)
.claude/skills/                # the 8 modular skills (auto-discovered)
.claude/agents/                # the 4 agents (orchestrator, audit, qualification, routing)
.claude-plugin/plugin.json     # plugin manifest (optional /plugin install path)
.mcp.json                      # Ahrefs hosted MCP + local quick-audit-tools server
scripts/setup.sh               # installs deps + import smoke (routine Build/Setup Command)
quick_audit_mcp/               # local MCP server (Sheets, Places, PageSpeed, gated Gmail send)
references/  references/source-docs/   # integration refs + the v1/v2 design docs (fidelity baseline)
examples/  tests/  tests/golden/  tests/automated/   # samples + manual + automated + golden fixtures
reports/                       # audit report, refactor plan, testing & deployment plan
```

See `MANIFEST.md` for the full inventory.

## Integration strategy

- **Ahrefs** — hosted MCP (`.mcp.json`).
- **Gmail drafts + Google Drive** — official Google Workspace **connectors** enabled on the routine
  (there are no public `gmailmcp`/`drivemcp` MCP endpoints).
- **Sheets writeback, Google Places, PageSpeed, gated Gmail send** — the local `quick_audit_mcp`
  server, using a **service account** (headless-safe; no browser OAuth in the cloud).

## Setup checklist

1. Create an API-triggered Claude Routine (Remote) and attach this repo.
2. Routine prompt (brief): *"Read CLAUDE.md and run the Quick Audit pipeline on the intake payload in the trigger `text` field. Emit RUN COMPLETE."*
3. Set the Build/Setup Command to `bash scripts/setup.sh`.
4. Enable the Gmail + Drive connectors; authenticate Ahrefs.
5. Add routine ENV vars (service-account JSON, spreadsheet ID, Places/PageSpeed/Ahrefs keys) — see
   `references/integration-environment-reference.md`.
6. Add the API trigger; store the fire URL + token in your intake backend.
7. Run `tests/` (Groups A–E) per `reports/03-testing-and-deployment-plan.md` before live submissions.

## Non-negotiable output rules

- Audit ends at the Glossary (13 sections); no "Glass Half Full"; no per-pillar "Revenue Translation";
  glossary = exactly 8 terms; every number traces to a logged source; projections are ranges.
- The PDF renderer is the single source of truth for styling.

## Reports

`reports/01-audit-report.md` (quality audit), `reports/02-refactor-plan.md`, and
`reports/03-testing-and-deployment-plan.md` (test usage, fidelity comparison vs. the original, and the
step-by-step deployment guide).
