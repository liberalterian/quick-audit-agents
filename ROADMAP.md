# Roadmap

## Phase 1 — Stabilize local fallback

- Keep `legacy-quick-audit` as a fallback wrapper for Phase 1 Cowork compatibility.
- Verify it delegates PDF rendering to `quick-audit-pdf-render` instead of duplicating renderer logic.

## Phase 2 — Production Claude Routine deployment

- Create the API-triggered Claude Routine.
- Attach this repository.
- Set the Routine prompt to the orchestrator agent.
- Configure MCP connectors and direct API credentials.
- Run `tests/routine-api-trigger-test.md` and `tests/end-to-end-cloud-smoke-test.md`.

## Phase 3 — Integration hardening

- Replace any local-only assumptions with cloud-safe direct API calls.
- Add a browser worker only if live SERP/GBP/Ads Transparency fallback quality requires it.
- Add explicit retry and error row handling for Google APIs and Drive uploads.

## Phase 4 — Delivery automation

- Keep HARD_FAIL emails as drafts until the team explicitly approves auto-send.
- Auto-send HARD_PASS and SOFT_FAIL prospect notes only after Gmail send capability is verified.
- Keep team alerts draft-first until review cadence is stable.

## Phase 5 — Multi-tenant routing

- Add partner config source.
- Route Drive folders, Gmail footers, team recipients, and rubrics by `partner-id`.
- Add partner-specific tests.

## Phase 6 — Continuous eval loop

- Add golden output comparisons.
- Add regression tests for format drift.
- Add quarterly re-grade diffs and anchor expansion governance.
