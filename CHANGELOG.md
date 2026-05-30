# Changelog

All notable changes to this project will be documented in this file.

This project follows a practical changelog format based on Keep a Changelog, with version entries organized by Added, Changed, Fixed, Security, and Known Limitations.

## [2.0.5] - 2026-05-30

### Added

* Added root-level `.mcp.json` for the Quick Audit / MAA workflow.
* Added official Ahrefs hosted MCP configuration using the Ahrefs Streamable HTTP endpoint.
* Added official Google Gmail MCP configuration for Gmail read and draft creation workflows.
* Added official Google Drive MCP configuration for saving audit artifacts with file-scoped Drive access.
* Added local `quick-audit-tools` MCP wrapper for workflow gaps not covered by official remote MCP servers.
* Added Google Sheets write tools for the Quick Audit Tracker:

  * `append_quick_audit_tracker_row`
  * `update_quick_audit_tracker_range`
* Added gated Gmail auto-send support through the local wrapper:

  * `send_gmail_message`
  * Disabled by default with `ENABLE_GMAIL_SEND=false`
  * Includes recipient count validation and optional allowed-domain restrictions.
* Added Google Places tools for resolving businesses and fetching place details:

  * `resolve_business_place`
  * `get_place_details`
* Added Google PageSpeed Insights tool:

  * `run_pagespeed_insights`
  * Supports mobile and desktop strategy checks.
  * Normalizes Lighthouse scores, lab metrics, field data, and Core Web Vitals assessment.
* Added `health_check` MCP tool for validating runtime configuration without exposing secret values.
* Added `.env.example` with required runtime variables for:

  * Ahrefs
  * Google OAuth
  * Google Sheets
  * Google Places
  * PageSpeed Insights
  * Anthropic runtime API key
  * Gmail send safety settings
* Added `requirements.txt` and `pyproject.toml` for local Python package setup.
* Added validation script:

  * `scripts/validate_mcp_config.py`
* Added tests:

  * `tests/test_mcp_config.py`
* Added documentation:

  * `docs/setup.md`
  * `docs/security-and-scopes.md`
  * `docs/custom-wrapper-plan.md`
  * `docs/mcp-integration-audit.md`
* Added package-level `README.md` describing installation, validation, local MCP startup, and safety defaults.
* Added `.gitignore` entries for local environment files, secrets, tokens, caches, and virtual environments.

### Changed

* Changed the MCP architecture from a generic server list to a workflow-specific Quick Audit / MAA integration stack.
* Clarified that the package should be merged into the existing audit/agent workflow repo as an internal module rather than treated as a separate repo by default.
* Centralized non-official or unsupported MCP needs into one local `quick-audit-tools` wrapper instead of relying on invented or unofficial external MCP servers.
* Moved Anthropic Claude API usage out of `.mcp.json` server definitions and into runtime environment configuration.
* Split responsibilities between:

  * Official remote MCP servers for Ahrefs, Gmail drafts, and Drive file access.
  * Local wrapper tools for Sheets writes, Gmail auto-send, Places, and PageSpeed.
* Updated security model to prefer least-privilege scopes and explicit send gating.

### Fixed

* Fixed the prior MCP integration gap for Google Sheets write access.
* Fixed the Gmail gap where draft creation existed but auto-send was not available.
* Fixed the Drive artifact persistence gap by adding Drive file-scoped MCP configuration.
* Fixed the Places integration gap by adding direct Places API wrapper tools for business resolution and place details.
* Fixed the PageSpeed integration gap by adding a local wrapper around the PageSpeed Insights API.
* Fixed the architectural mistake of treating Anthropic Claude API as an MCP server.
* Fixed ambiguity around whether this package should live as a separate repo or inside the main workflow repo.

### Security

* Gmail auto-send is disabled by default.
* Gmail sending requires `ENABLE_GMAIL_SEND=true`.
* Gmail sending supports allowed recipient domains through `QUICK_AUDIT_ALLOWED_SEND_DOMAINS`.
* Gmail sending enforces a configurable recipient limit through `QUICK_AUDIT_MAX_SEND_RECIPIENTS`.
* Google Drive is configured around file-scoped access instead of broad Drive access where possible.
* Runtime secrets are moved to `.env` and excluded from version control.
* OAuth token files and Google client secret files are excluded from version control.
* `health_check` reports whether credentials are configured without exposing secret values.
* Documentation now includes MCP trust boundaries, OAuth scope notes, API key restrictions, and operational safety guidance.

### Known Limitations

* Live API calls were not tested in the generation environment because credentials were not available.
* Google Sheets, Gmail send, Places, and PageSpeed require valid Google credentials or API keys before runtime validation.
* Gmail auto-send should remain disabled until manual QA, sender identity checks, and recipient safeguards are approved.
* The local MCP wrapper is an MVP implementation intended for integration testing before production hardening.
* Production deployment should add structured logging, retries, rate-limit handling, observability, and stricter input validation.


## [2.0.4] - 2026-05-30 — Production support package for Routine deployment

### Added

- Added complete `tests/` package covering cloud smoke tests, MCP connection checks, routine API trigger validation, PDF schema validation, routing delivery, qualification rubric cases, legacy fallback, and format regressions.
- Added complete `examples/` package with sample intake, enrichment, qualification, audit-spec JSON, Zapier Routine request, Tracker row, grading notes, Drive folder layout, and run-complete event examples.
- Added complete `references/` package with MCP configuration guidance, Claude Routine API notes, Google Workspace MCP notes, Ahrefs MCP notes, Google Places direct API reference, Google Sheets Tracker writeback reference, plugin structure notes, source map, and integration environment variables.
- Added root `.mcp.json` with verified remote MCP endpoints for Ahrefs, Gmail, Google Drive, Google People, and Google Maps Code Assist.
- Added official plugin manifest at `.claude-plugin/plugin.json`.
- Added Python renderer scripts to `skills/quick-audit-pdf-render/scripts/` using dash-case filenames.
- Added source-doc copies under `references/source-docs/` with dash-case filenames.

### Changed

- Corrected skill filenames to `SKILL.md` because Claude Code plugin skills are discovered from directories containing `SKILL.md`.
- Preserved dash-case naming across generated package paths.
- Clarified that `legacy-quick-audit` is a fallback wrapper, not the primary production path.
- Clarified that Claude Routine is the production cloud runtime; the local Cowork scheduled flow is Phase 1 fallback only.
- Updated MCP strategy to avoid inventing unsupported Google Sheets or Places MCP endpoints.
- Updated Tracker/integration strategy: Sheets writeback and Places lookup are production direct-API integrations unless a trusted internal MCP server is explicitly added.

### Fixed

- Restored missing Python scripts from earlier package drafts.
- Removed stale v1 output-format assumptions from the production path: no Glass Half Full closer and no per-pillar Revenue Translation paragraphs.
- Removed ambiguity around Google Maps Code Assist: it is a documentation RAG MCP, not a business-data Places API MCP.

## [2.0.3] - 2026-05-30 — Dash-case modular package

### Added

- Added dash-case skill directories.
- Added `legacy-quick-audit` fallback skill.
- Added full agent split: orchestrator, audit, qualification, and routing.

### Changed

- Renamed generated paths from snake-case to dash-case.

## [2.0.2] - 2026-05-30 — Claude Routine cloud runtime revision

### Added

- Reframed cloud runtime around API-triggered Claude Routine.
- Added Routine setup guide and trigger contract.

## [2.0.1] - 2026-05-30 — Initial modular architecture draft

### Added

- Initial README, architecture, roadmap, changelog, agent definitions, and modular skill plan.
