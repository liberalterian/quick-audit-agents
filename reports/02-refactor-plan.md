# Quick Audit System — Comprehensive Refactor Plan

**Companion to:** `01-audit-report.md`
**Goal:** A production-ready, cloud-deployable, fidelity-verifiable multi-agent Quick Audit system that runs unattended inside an API-triggered Claude Routine, faithful to Dan Pasker's original v1 system (Daniel Goodrich's bundle replicating Dennis Yu / BlitzMetrics).
**Scope of this document:** plan only — no code has been changed. Each item lists the exact files to touch and why.

---

## Context — why this refactor

The audit found the design is sound but the package **cannot run unmodified in a cloud routine** (4 critical defects), **contradicts its own rules** (dash-case over-application, unsatisfiable test), carries **version/identity drift**, and **lacks the golden artifacts** needed to prove fidelity. Your pasted Gemini blueprint and the official Claude Code docs agree on the fix shape: put the system's intelligence in the *repository* (`.claude/` config dirs + a `CLAUDE.md` orchestrator directive + a `scripts/setup.sh`), keep the routine web form minimal, and trigger via the API `/fire` endpoint. This plan executes that, plus the correctness fixes.

**Guiding principles**
1. Make it *load* in a cloned-repo cloud session (the C-3 fix governs everything else).
2. Don't break v1 fidelity — preserve the source docs, renderer, and the exact grade anchors.
3. Reduce files only where it removes duplication or pointer-only noise; never delete fidelity-bearing material.
4. Follow the **official** routine contract (`text` field) over third-party blog illustrations.

---

## A. Target repository structure (the big move)

Adopt the Gemini/official hybrid layout. **Move config into `.claude/`** so a cloned repo auto-discovers it without a plugin install, keep the plugin manifest for optional `/plugin` installs, and add the orchestrator directive + setup script.

```
quick-audit-system/
├── CLAUDE.md                      # NEW — orchestrator directive (auto-loaded in routine session)
├── .claude/
│   ├── skills/                    # MOVED from skills/  (auto-discovered)
│   │   ├── quick-audit-intake/SKILL.md
│   │   ├── quick-audit-enrichment/SKILL.md
│   │   ├── quick-audit-grading/{SKILL.md,evals/,references/}
│   │   ├── quick-audit-report/{SKILL.md,templates/,references/}
│   │   ├── quick-audit-pdf-render/{SKILL.md,scripts/}
│   │   ├── quick-audit-qualification/{SKILL.md,evals/}
│   │   ├── quick-audit-routing/SKILL.md
│   │   └── legacy-quick-audit/SKILL.md
│   └── agents/                    # MOVED from agents/  (auto-discovered; NOTE: .claude/agents, not Gemini's .claude/plugins)
│       ├── quick-audit-orchestrator-agent.md
│       ├── quick-audit-agent.md
│       ├── qualification-agent.md
│       └── routing-agent.md
├── .claude-plugin/plugin.json     # KEEP — for optional /plugin install path
├── .mcp.json                      # KEEP (fixed — see §C)
├── scripts/
│   └── setup.sh                   # NEW — installs python deps + reportlab (routine setup command)
├── quick_audit_mcp/               # RENAMED from mcp/ (see C-1); the MCP server package
│   ├── __init__.py
│   ├── server.py
│   ├── auth.py                    # NEW — service-account / token loader (see C-2)
│   ├── pyproject.toml, requirements.txt, .env.example
│   ├── docs/  scripts/  tests/
├── references/                    # KEEP source-docs (fidelity); consolidate micro-references (see §D)
│   └── source-docs/               # UNCHANGED — v1/v2 design docs (fidelity baseline)
├── examples/                      # KEEP + add Apparel Junction + Expert Services intake payloads
├── tests/                         # KEEP markdown tests (fixed) + NEW tests/golden/ + tests/automated/
└── README.md  ARCHITECTURE.md  CHANGELOG.md  ROADMAP.md  MANIFEST.md
```

> **Important divergence from the Gemini blueprint:** Gemini wrote `.claude/plugins/` for "agent definitions." The official subagents docs put project agents in **`.claude/agents/`**. Use `.claude/agents/`. (`.claude/plugins/` is not an auto-discovered agent location.) Keep `.claude-plugin/plugin.json` for the `/plugin install` route, which is a *separate* mechanism.

> **Skills note:** Gemini describes skills as "`.js`/`.ts` or conversational." These skills are conversational `SKILL.md` markdown — that's correct and supported; no JS conversion needed.

---

## B. Critical fixes (must land before any cloud run)

### Fix C-1 — Rename the MCP package so it stops shadowing the SDK
- Rename directory `mcp/` → `quick_audit_mcp/`; ensure `quick_audit_mcp/__init__.py` exists.
- `.mcp.json`: change the stdio server to use `${CLAUDE_PLUGIN_ROOT}` (plugin install) or a repo-root-relative module that no longer collides:
  ```json
  "quick-audit-tools": {
    "type": "stdio",
    "command": "python3",
    "args": ["-m", "quick_audit_mcp.server"],
    "env": { ... }
  }
  ```
- Update `pyproject.toml` (`pythonpath`, package name), `validate_mcp_config.py` assertions, `test_mcp_config.py` `ROOT`, and `docs/setup.md` / `README.md` run commands (`python -m quick_audit_mcp.server`).
- **Add an import smoke test** to `tests/` that actually does `import quick_audit_mcp.server` (the current test never imports it, which is how C-1 hid).

### Fix C-2 — Headless-safe Google auth
- Add `quick_audit_mcp/auth.py` with a **service account** path (preferred for cloud) using `google.oauth2.service_account.Credentials`, selected when `GOOGLE_APPLICATION_CREDENTIALS` (or an inline `GOOGLE_SERVICE_ACCOUNT_JSON` secret) is present; fall back to a **pre-seeded refresh-token** file for local dev. **Never** call `flow.run_local_server()` when a no-browser env is detected.
- Sheets/Drive: share the Tracker spreadsheet + Drive folder with the service-account email. (Gmail send via service account requires domain-wide delegation; keep Gmail **drafts on the official Gmail MCP** and treat auto-send as a later, separately-approved capability — consistent with ROADMAP Phase 4.)
- `health_check`: add `auth_mode` (`service_account` | `token` | `none`) so the MCP-connection test can verify headless readiness without secrets.

### Fix C-3 — Make the system load in a cloned-repo routine
- Move `skills/` → `.claude/skills/` and `agents/` → `.claude/agents/` (§A).
- Author **`CLAUDE.md`** as the orchestrator directive (§E) so the routine prompt can stay one line ("Read CLAUDE.md and run the Quick Audit pipeline on the payload in the trigger `text`.").
- Keep `.claude-plugin/plugin.json` for the optional install path, and document both launch modes in README.

### Fix C-4 — `scripts/setup.sh`
```bash
#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install --upgrade pip
pip install -r quick_audit_mcp/requirements.txt   # mcp, httpx, pydantic, dotenv, google-* 
pip install reportlab                               # renderer
python -c "import quick_audit_mcp.server; import reportlab"  # fail fast
echo "setup ok"
```
Wire as the routine **Build/Setup Command** (`bash scripts/setup.sh`). Update `claude-routine-setup-guide.md` and `integration-environment-reference.md` to list the **full** dependency set, not just reportlab.

---

## C. `.mcp.json` correctness (H-4)

- Normalize every `oauth.scopes` to a **space-separated string**; delete the undocumented `"enabled": true`.
- Remove the duplicate **`gmail-drafts`** server (keep one `google-gmail`).
- **Verify the Google MCP endpoints actually exist** before relying on them; if they don't, drop them and use direct APIs via the local server (the README already concedes Sheets/Places aren't official MCPs). Document the decision in `mcp-configuration-guide.md`.
- Make `validate_mcp_config.py` assert *shape* (string scopes, no `enabled`, no duplicate URLs) rather than echoing the current values, so it can actually catch regressions.

---

## D. File reduction & consolidation (≈87 → ≈72, structure-first)

**Consolidate (merge into a parent, then delete the stubs):**
- Fold `references/automation-architecture-reference.md`, `calibration-anchors.md`, `system-source-map.md`, `gct-positioning-reference.md` into **one** `references/README.md` "source map + positioning + anchors" page (they're 1–3 lines each pointing at source-docs). *Net −3 files.*
- Replace the 16 duplicated test "Preconditions" blocks with a single `tests/README.md` "Common preconditions" section referenced by each test. *No file-count change but removes ~48 duplicated lines.*
- Merge `mcp/.../docs/custom-wrapper-plan.md` + `mcp-integration-audit.md` into one `quick_audit_mcp/docs/architecture.md` (overlapping content). *Net −1.*

**Keep (do NOT delete — fidelity / progressive disclosure):**
- All five `references/source-docs/*` (the v1/v2 design docs — the fidelity baseline).
- All `examples/` (copy-ready; cheap because they only load when referenced).
- The renderer scripts (the styling source of truth).

**Add (small, high-value):**
- `CLAUDE.md`, `scripts/setup.sh`, `quick_audit_mcp/auth.py`, `tests/golden/`, `tests/automated/`, `examples/apparel-junction-intake.md`, `examples/expert-services-intake.md`, root `.gitignore`.

Net effect: fewer pointer files, deduped tests, but the *fidelity surface is preserved*. The real win is **structural** (the `.claude/` move), not raw count.

---

## E. `CLAUDE.md` orchestrator directive (new — the linchpin)

Because routine frontmatter on an agent file doesn't auto-apply, `CLAUDE.md` becomes the always-loaded instruction. It should:
1. State the mission and the **hard output rules** (no Glass Half Full, no per-pillar Revenue Translation, exactly 8 glossary terms, sourced numbers only, end at Glossary).
2. Define the execution order and **explicitly instruct the main session to act as `quick-audit-orchestrator-agent`** and delegate to `quick-audit-agent` / `qualification-agent` / `routing-agent` (subagents run skills inline; the orchestrator is the main session so nesting is legal — H-5).
3. Tell it to **read the relevant `references/source-docs/*` before grading and report-writing** (closes M-3: thin skills + un-loaded source docs).
4. Pin the **calibration anchors** (Apparel Junction D 38: 42/55/38/40/35/18; RiteWay A ~90) and the **format golden** (Expert Services v2, Dennis's PDF).
5. Mandate the **live Knowledge-Panel enrichment step** (the v1 lesson from `ExpertServicesUtah_Grading-Notes_v1.md:220` — promote it from failure-mode to default step).
6. Parse the intake from the trigger **`text`** field (official contract), not a `payload` object.

Keep it lean (it stays in context all session) and let it point to skills/source-docs for detail.

---

## F. Skill/agent content hardening (M-3, M-4, M-8)

- In each grading/report skill, replace "See source doc for full content" with an explicit instruction to **load** the source doc (e.g., a `!`cat references/source-docs/quick-audit-grading-approach-v1.md`` dynamic-injection block, or list it in the orchestrator's reading step). Thin guidance + un-loaded reference = drift.
- `quick-audit-pdf-render/SKILL.md`: change the script path to `python3 ${CLAUDE_SKILL_DIR}/scripts/render-audit-pdf.py …`.
- Fix the renderer docstring USAGE line to the dash-case filename.
- Enrichment skill: add the **live Knowledge-Panel / GBP review-count step** as a required step (not a fallback).
- Agents: confirm the orchestrator keeps the `Agent` tool (omit `tools` to inherit, or add `Agent(quick-audit-agent, qualification-agent, routing-agent)` explicitly). Note that plugin-loaded agents ignore `hooks`/`mcpServers`/`permissionMode` — none are used here, so safe.

---

## G. Dash-case sanity (H-1, H-2)

- Rewrite `dash-case-path-regression-test.md` to **exclude** Python package paths: e.g., `find . -name '*_*' -not -path './quick_audit_mcp/*' -not -name '*.py'`. State that Python identifiers must use underscores.
- Convert all documented env var names to underscores everywhere (`integration-environment-reference.md`, tests, examples) and align to the server's actual names.
- Fix `sample-zapier-routine-request.md` to `"$QUICK_AUDIT_ROUTINE_FIRE_URL"` / `"$QUICK_AUDIT_ROUTINE_TOKEN"` and the official `/fire` URL shape with the `text` body (it already uses `text` — keep that, fix the var names).

---

## H. Versioning & docs hygiene (M-1, M-2, L-1…L-4)

- Pick **one** version (recommend `2.1.0` for this refactor) and set it in `plugin.json` + CHANGELOG; rename the dir away from an embedded version or accept dir≠manifest but document it. Keep `quick_audit_mcp/pyproject.toml` on its own internal version, clearly scoped.
- Regenerate `MANIFEST.md` from the actual tree (include `quick_audit_mcp/**`; fix lowercase filename references). Consider auto-generating it in `setup.sh` to prevent future drift.
- Add a root `.gitignore`: `.env`, `secrets/`, `__pycache__/`, `*.pyc`, `/tmp/*.json`, `*-audit*.pdf` outputs, `.venv/`.
- Single-source the routine beta header in one reference; others link to it.

---

## I. Fidelity import (H-3) — bridge to the testing plan

Copy from `\\wsl.localhost\Ubuntu-22.04\home\liberalterian\Projects\QuickAudit-System-v1\` into `tests/golden/`:
- `04_reference/Apparel_Junction_Quick_Audit.pdf` → `tests/golden/format-reference/` (canonical **format** golden).
- `05_sample_outputs/ApparelJunction_*` → `tests/golden/apparel-junction/` (**grade** golden; mark its `.md` as *v1-format, not a v2 format target* — it contains Glass Half Full + Revenue Translation + 13 glossary terms).
- `05_sample_outputs/ExpertServicesUtah_*` → `tests/golden/expert-services/` (**v2 format + grade** golden).
- Add matching intake payloads to `examples/`.
Full comparison methodology in `03-testing-and-deployment-plan.md`.

---

## J. Phased execution sequence (maps to ROADMAP)

| Phase | Outcome | Items |
|---|---|---|
| **0 — Unblock** (½–1 day) | Server imports; loads in cloned repo | C-1, C-3 (move), C-4 (setup.sh), root `.gitignore` |
| **1 — Headless auth** (1 day) | Sheets/Drive/Places/PageSpeed work in cloud | C-2 + `health_check` `auth_mode` |
| **2 — Config correctness** (½ day) | `.mcp.json` connects cleanly | C/H-4, validator shape-check, import smoke test |
| **3 — Fidelity infra** (½ day) | Golden files + payloads in repo | I, H-3, examples |
| **4 — Content hardening** (1 day) | Skills load source docs; CLAUDE.md live; live-GBP step | E, F |
| **5 — Hygiene & dedupe** (½ day) | Versions/MANIFEST/dash-case fixed; files consolidated | D, G, H |
| **6 — Verify** | Run the full test plan incl. golden diffs | see `03-…` |

This refactor satisfies the existing ROADMAP Phases 1–3 (stabilize fallback, production routine, integration hardening) and lays the deterministic base for Phases 4–6 (delivery automation, multi-tenant, eval loop).

---

## K. Explicitly out of scope (call out, don't silently drop)
- Building a browser-worker service for live SERP/GBP/Ads-transparency (ROADMAP Phase 3 option) — recommend deferring; let those signals degrade to "data unavailable" initially.
- Enabling Gmail auto-send — keep `ENABLE_GMAIL_SEND=false`; drafts-first until QA sign-off (ROADMAP Phase 4).
- Multi-tenant partner routing (ROADMAP Phase 5) — the intake already carries `partner-id`; wire later.
