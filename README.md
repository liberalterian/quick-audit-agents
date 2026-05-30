# Quick Audit System

Production-oriented Claude Code / Claude Routine package for running the Quick Audit workflow.

## What this package does

The system accepts a structured local-service prospect intake payload, enriches the business using public and connected data sources, grades the business across Dennis Yu's six-pillar Quick Audit format, creates the customer-facing audit markdown, renders the styled PDF, qualifies the prospect against the downstream MVS rubric, drafts or sends routing emails, uploads artifacts to Drive, and writes the final state back to the Tracker.

## Production runtime

The production runtime is an **API-triggered Claude Routine**. SPP or another intake source writes the Tracker row, then Zapier or the intake backend sends the payload to the Routine API trigger. The Routine runs in Anthropic-managed Claude Code cloud infrastructure and invokes the modular agents and skills in this repository.

## Critical implementation correction

Claude Code plugin skills should use `SKILL.md` inside each skill directory. Earlier drafts used lowercase `skill.md`; this package corrects that. Keep the filename exactly `SKILL.md`.

## Directory map

See `manifest.md` for the complete file inventory.

## Primary components

- `agents/quick-audit-orchestrator-agent.md` — Routine-level orchestrator.
- `agents/quick-audit-agent.md` — Audit enrichment, grading, report generation, and PDF render coordination.
- `agents/qualification-agent.md` — Applies downstream qualification rubric.
- `agents/routing-agent.md` — Uploads artifacts, drafts/sends messages, and writes final Tracker state.
- `skills/` — Modular skills for intake, enrichment, grading, report generation, PDF rendering, qualification, routing, and legacy fallback.
- `tests/` — Deployment and regression tests.
- `examples/` — Copy-ready sample payloads and expected records.
- `references/` — Architecture and integration references, including MCP and direct API decisions.
- `.mcp.json` — Project-scoped MCP configuration for verified remote MCP endpoints used by the system.

## Integration strategy

The package uses verified remote MCP endpoints where they exist:

- Ahrefs MCP for SEO and link data.
- Google Workspace MCP servers for Gmail and Drive.
- Google People MCP as an optional identity/contact helper.
- Google Maps Code Assist MCP as a documentation helper, not as a Places data source.

Google Sheets Tracker writeback and Google Places business lookup are not represented as official remote MCP servers in the verified Google Workspace MCP docs used for this package. For production, use direct APIs with scoped credentials or wire trusted internal MCP servers. See `references/mcp-configuration-guide.md`, `references/google-places-api-reference.md`, and `references/google-sheets-tracker-writeback-reference.md`.

## Setup checklist

1. Install or enable Claude Code on the web and create a Claude Routine.
2. Add this repository to the Routine.
3. Set the Routine prompt to `agents/quick-audit-orchestrator-agent.md`.
4. Add the API trigger and store the Routine URL/token in Zapier or your intake backend.
5. Approve/authenticate MCP servers from `.mcp.json` where used.
6. Configure Google Maps Platform and Google Sheets API credentials for direct API calls.
7. Configure environment variables listed in `references/integration-environment-reference.md`.
8. Run the tests in `tests/` before processing live submissions.

## Non-negotiable output rules

- The audit ends at the Glossary.
- Do not add a Glass Half Full section.
- Do not add per-pillar Revenue Translation paragraphs.
- Every numeric assertion must trace to an enrichment signal, calibration anchor, or explicitly marked unavailable source.
- The PDF renderer is the single source of truth for styled PDF presentation.
