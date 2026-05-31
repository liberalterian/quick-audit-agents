# Quick Audit System — Code / Context / Agent / Skill Audit Report

**Audited package:** `quick-audit-system-v2.0.0` (Claude Code plugin, API-triggered Claude Routine)
**Audit date:** 2026-05-30
**Auditor:** Claude Code (Opus 4.8), full read of all 87 tracked files
**Fidelity baseline:** `QuickAudit-System-v1/` (Daniel Goodrich's v1 bundle replicating Dennis Yu / BlitzMetrics' published Quick Audit), owner/stakeholder: **Dan Pasker**
**Method:** Every file read in full and quoted; no inference where a fact could be verified. Claude Code behavior cross-checked against the official docs for routines, skills, subagents, MCP, and workflows.

---

## 1. Executive summary

The package is a **well-conceived, cleanly-separated modular design** that is **not yet production-deployable as written**. The architecture (orchestrator → audit → qualification → routing, with seven granular skills + a small custom MCP server) is sound and faithful in spirit to the v1 system. The custom MCP server is genuinely good code. But there are **4 deployment-blocking defects**, several **self-contradictions between the package's own rules and its own files**, pervasive **version/identity drift**, and — most important for your "true to the original" goal — the **golden fidelity artifacts were never imported**, so the package currently has no way to prove it matches the original output.

**Overall readiness grade: D+ (≈ 48/100).** Strong bones, real authority in the design docs, undercut by mechanical defects that would each stop a cloud run. Every issue below is fixable; most in under a day. See `02-refactor-plan.md`.

| Dimension | Grade | One-line |
|---|---|---|
| Architecture & separation of concerns | B+ | Clean agent/skill split; correct "qualification consumes enrichment, doesn't duplicate" discipline. |
| Cloud-routine deployability | D | Won't run unmodified: plugin discovery, headless OAuth, package-name collision, missing deps. |
| MCP server code quality | A− | FastMCP + pydantic + send-gating + least-privilege; only minor issues. |
| Skill/agent content fidelity to v1 | C | Rules captured, but skills are too thin to reproduce v1 output without the source docs, which aren't auto-loaded. |
| Tests | C− | Coherent manual suite, but one test is unsatisfiable, fixtures are missing, and nothing diffs against the original. |
| Docs consistency & hygiene | D | Version drift (0.4.0 / 2.0.5 / v2.0.0), MANIFEST omits the whole Python package, dash-case over-applied to env vars/Python. |
| Fidelity infrastructure | F | Golden outputs + reference PDF not in repo; "golden tests" reference fixtures that don't exist. |

---

## 2. What the system is (verified)

A Claude Code **plugin** packaging the "Quick Audit" workflow as an **API-triggered Claude Routine** running in Anthropic cloud. Flow ([ARCHITECTURE.md:5](../ARCHITECTURE.md)):

```
SPP/intake form → Zapier → Google Sheet Tracker row → Routine API trigger
→ quick-audit-orchestrator-agent
   → quick-audit-intake
   → quick-audit-agent → {enrichment, grading, report, pdf-render → render-audit-pdf.py}
   → qualification-agent → quick-audit-qualification
   → routing-agent → quick-audit-routing
→ Drive artifacts + Gmail drafts/sends + Tracker writeback
```

Domain: six-pillar local-SEO "Quick Audit" for US local-service businesses, in **Dennis Yu / BlitzMetrics — Local Service Spotlight** format. Output discipline (carried from v1): no "Glass Half Full" closer, no per-pillar "Revenue Translation," every numeric claim sourced, no fabrication. The JSON-spec-driven reportlab renderer is the single source of truth for PDF styling.

**Component inventory (verified counts):** 1 plugin manifest, 1 `.mcp.json` (6 servers), 4 agents, 8 skills (+ evals/references/templates/scripts), 1 Python MCP server (6 tools), 16 manual markdown tests, 9 examples, 12 reference docs + 5 large `source-docs/` (the v1/v2 design docs). 87 tracked files total.

---

## 3. Critical findings (deployment-blocking)

### C-1 — Local package directory `mcp/` collides with the `mcp` SDK
`server.py` imports the MCP SDK as `from mcp.server.fastmcp import FastMCP` ([server.py:31](../mcp/quick_audit_tools/server.py)), but the code lives under a top-level directory literally named **`mcp/`** with **no `mcp/__init__.py`**. `.mcp.json` launches it as `python -m mcp.quick_audit_tools.server` ([.mcp.json:64-70](../.mcp.json)). Run from the repo root (as the cloud routine will), Python resolves `mcp` to the **local** directory and the SDK import breaks (or, if site-packages wins, `mcp.quick_audit_tools` is not found). Either way the stdio server fails to start.
**Severity: Critical.** Verified by code reading; the existing `test_mcp_config.py` never imports `server.py`, so it masks this.

### C-2 — Interactive OAuth can't run headless in the cloud routine
`_credentials()` falls back to `flow.run_local_server(port=0)` ([server.py:126-127](../mcp/quick_audit_tools/server.py)) — an interactive browser consent flow. A cloud Routine has no browser, so on first run (no cached token) every Sheets/Places/PageSpeed/Gmail-send tool throws. A pre-provisioned, refreshable token or a **service account** must be shipped as a secret. No mechanism for that exists today.
**Severity: Critical.**

### C-3 — Skills/agents won't be discovered in a cloned-repo routine
Skills live in `skills/` and agents in `agents/` (the **plugin** layout). Per the skills docs, a non-plugin project auto-discovers skills only under **`.claude/skills/`** and agents under **`.claude/agents/`**; plugin-layout dirs load only when the repo is **installed/enabled as a plugin** — and there is **no `marketplace.json`** and no install step in the routine. A routine that just clones the repo will not see these. README step 3 ("set the Routine prompt to `agents/quick-audit-orchestrator-agent.md`") also doesn't make the agent's frontmatter (model, `skills` preload, `maxTurns`) take effect — that requires `--agent`, which the routine form doesn't expose.
**Severity: Critical.** This is the single biggest "will it even run?" risk. Your pasted Gemini blueprint resolves it: move to `.claude/` layout + a `CLAUDE.md` orchestrator directive + `scripts/setup.sh`. See `02-refactor-plan.md` §A.

### C-4 — Renderer/MCP dependencies are not installed in the routine environment
`claude-routine-setup-guide.md:12` and `integration-environment-reference.md:9-12` list only `reportlab` (plus `curl`/`jq`). But the MCP server needs `httpx`, `pydantic`, `python-dotenv`, `google-api-python-client`, `google-auth`, `google-auth-oauthlib`, `mcp` ([requirements.txt](../mcp/quick_audit_tools/requirements.txt)). With no setup script installing these, the server import fails even after C-1 is fixed.
**Severity: Critical.**

---

## 4. High-severity findings

### H-1 — `dash-case-path-regression-test.md` is unsatisfiable against the repo's own code
The test demands "**No repository file or directory name contains `_`**" and runs `find . -name '*_*'` ([dash-case-path-regression-test.md:15-26](../tests/dash-case-path-regression-test.md)). But the Python package **requires** underscores: `mcp/quick_audit_tools/`, `__init__.py`, `server.py`-adjacent `test_mcp_config.py`, `validate_mcp_config.py`, `pyproject.toml`. The "dash-case everything" rule (valid for skills/dirs) was wrongly globalized. The test would fail on the package the same changelog added.
**Severity: High** (a regression test that can never pass erodes trust in the whole suite).

### H-2 — Dash-case applied to env vars and shell variables (invalid + mismatched)
`integration-environment-reference.md:17-23` lists env names like `GOOGLE-MAPS-API-KEY`, `GOOGLE-SHEETS-SPREADSHEET-ID`, `DRIVE-ROOT-FOLDER-ID`. `google-places-direct-api-test.md:15` sets `GOOGLE-MAPS-API-KEY`. `sample-zapier-routine-request.md:4-6` uses `$QUICK-AUDIT-ROUTINE-FIRE-URL` / `$QUICK-AUDIT-ROUTINE-TOKEN`. **Dashes are illegal in POSIX env/shell variable names** (`$QUICK` expands, then literal `-AUDIT...`). They also don't match the server's real names (`GOOGLE_PLACES_API_KEY`, `GOOGLE_SHEETS_SPREADSHEET_ID` in [server.py](../mcp/quick_audit_tools/server.py) / [.env.example](../mcp/quick_audit_tools/.env.example)). The copy-ready Zapier example would silently send empty URL/token.
**Severity: High** (ships broken copy-paste artifacts).

### H-3 — Golden fidelity artifacts are absent from the repo
The v1 `system-overview-v1.md:185-209` lists a bundle containing **Dennis's published `Apparel_Junction_Quick_Audit.pdf`** and the **sample outputs** (`ApparelJunction_*`, `ExpertServicesUtah_*`). Only the **design docs** were copied into `references/source-docs/`. Consequently `apparel-junction-golden-test.md` and `expert-services-smoke-test.md` reference fixtures that **don't exist in this repo** ("Run the Expert Services sample/cold test payload *if available*"). No original-vs-new comparison is currently possible.
**Status:** You have now supplied these at `\\wsl.localhost\Ubuntu-22.04\home\liberalterian\Projects\QuickAudit-System-v1\` — the refactor plan imports them as `tests/golden/`. **Severity: High until imported.**

### H-4 — `.mcp.json` OAuth shape is non-standard and inconsistent
Per the MCP docs, the `oauth` object uses `clientId`, `callbackPort`, `scopes` as a **space-separated string**, `authServerMetadataUrl`. In `.mcp.json`: `google-gmail`/`gmail-drafts`/`google-people` use `scopes` as a **JSON array** and an undocumented `"enabled": true` field ([.mcp.json:20-56](../.mcp.json)); only `google-drive` uses the correct space-separated string ([.mcp.json:44](../.mcp.json)). `google-gmail` and `gmail-drafts` are **duplicate servers on the same URL** ([.mcp.json:17-39](../.mcp.json)). The `gmailmcp.googleapis.com`, `drivemcp.googleapis.com`, `mapscodeassist.googleapis.com` endpoints are **self-admittedly unverified** (README:42, mcp-configuration-guide). The `validate_mcp_config.py` "passes" only because it asserts the config matches itself — it does not verify the endpoints exist.
**Severity: High** (likely connection failures; false confidence from the validator).

### H-5 — Orchestrator delegates to agents that are themselves subagents (nesting)
The design has `quick-audit-orchestrator-agent` → `quick-audit-agent`/`qualification-agent`/`routing-agent`. **Subagents cannot spawn subagents.** This only works if the orchestrator runs as the **main session** (`--agent` / routine prompt acting as orchestrator) AND retains the `Agent` tool. The orchestrator's frontmatter omits `tools` (so it inherits `Agent` — OK), but combined with C-3, the practical risk is that in a plain cloned-repo routine the orchestrator is *not* loaded as an agent at all, so neither its delegation nor its `skills` preload happens.
**Severity: High** (architecture only holds under a specific, currently-undocumented launch mode).

---

## 5. Medium-severity findings

- **M-1 Version drift (3 different versions).** `plugin.json` `version: "0.4.0"` ([plugin.json:5](../.claude-plugin/plugin.json)); CHANGELOG newest entry `[2.0.5]` ([CHANGELOG.md:7](../CHANGELOG.md)); directory `quick-audit-system-v2.0.0`; `pyproject.toml` `version = "0.1.0"`. Pick one scheme.
- **M-2 MANIFEST omits the entire Python MCP package.** `MANIFEST.md` lists root/agents/skills/references/examples/tests but **not** `mcp/quick_audit_tools/**` (server, docs, scripts, tests, pyproject, requirements, .env.example). It also lists lowercase `readme.md`/`changelog.md`/`architecture.md` while files are uppercase ([MANIFEST.md:9-13](../MANIFEST.md)).
- **M-3 Skills are too thin to reproduce v1 output unaided.** Each `SKILL.md` is 400–1,100 bytes and defers to `references/source-docs/*` ("See … for the full source document") — but those source docs are **not auto-loaded** (no `!`-injection, not in `skills` preload). The real fidelity lives in the 30–44 KB source docs and the renderer, not in the skills. Without explicitly pulling them in, a run grades/writes from thin guidance.
- **M-4 PDF skill uses a bare relative script path.** `python3 skills/quick-audit-pdf-render/scripts/render-audit-pdf.py …` ([quick-audit-pdf-render/SKILL.md:18](../skills/quick-audit-pdf-render/SKILL.md)) assumes CWD = repo root. Skills should use `${CLAUDE_SKILL_DIR}/scripts/render-audit-pdf.py` (docs-recommended) to be CWD-independent.
- **M-5 Golden test fixtures and a referenced anchor payload don't exist.** No Apparel Junction or Expert Services **intake payload** is in `examples/`; only `sample-intake-payload.md` (Example Services). `build-audit-spec-example.py` embeds an Expert Services spec, but there's no Apparel Junction spec/markdown in this repo.
- **M-6 `.env.example` defines `ENABLE_GMAIL_SEND` twice** (lines 5 and 27) ([.env.example](../mcp/quick_audit_tools/.env.example)) — harmless but sloppy; the second wins.
- **M-7 16 tests duplicate an identical 3-line "Preconditions" block** verbatim — consolidation candidate (a shared header).
- **M-8 Renderer USAGE docstring shows the v1 path** (`python3 render_audit_pdf.py …`, [render-audit-pdf.py:10](../skills/quick-audit-pdf-render/scripts/render-audit-pdf.py)) — underscore filename that no longer matches the dash-case shipped file.

---

## 6. Low-severity / hygiene

- **L-1** `.gitignore` at repo root is **empty (0 bytes)** — secrets hygiene relies entirely on the package-level `mcp/quick_audit_tools/.gitignore`. A root `.gitignore` should exclude `.env`, `secrets/`, `__pycache__`, `*.pdf` outputs, `/tmp` artifacts.
- **L-2** `README.md` and `MANIFEST.md` cross-link to lowercase filenames; works on case-insensitive FS, breaks on Linux (the cloud routine).
- **L-3** Several reference files are 1–3 lines that only point at source-docs (`automation-architecture-reference.md`, `calibration-anchors.md`, `system-source-map.md`, `gct-positioning-reference.md`) — consolidation candidates.
- **L-4** `claude-routine-api-reference.md` correctly pins the `experimental-cc-routine-2026-04-01` beta header — good, but it's duplicated in three places (reference, setup guide, sample request); single-source it.

---

## 7. What is genuinely good (keep)

- **MCP server design.** FastMCP + pydantic models with validators ([server.py:165-223](../mcp/quick_audit_tools/server.py)); Gmail send hard-gated behind `ENABLE_GMAIL_SEND` with recipient-count and domain allowlist enforcement ([server.py:296-320](../mcp/quick_audit_tools/server.py)); PageSpeed output normalized rather than dumping raw Lighthouse JSON ([server.py:374-428](../mcp/quick_audit_tools/server.py)); `health_check` reports config presence without leaking secrets ([server.py:431-447](../mcp/quick_audit_tools/server.py)); Drive limited to `drive.file`; least-privilege documented in `security-and-scopes.md`. This is production-grade once C-1/C-2 are fixed.
- **Architecture discipline.** Qualification is independent of pillar grades; PDF rendering is centralized and JSON-driven; legacy fallback explicitly forbidden from forking renderer logic ([agent-skill-architecture-audit.md:25-34](../agent-skill-architecture-audit.md)).
- **Output-rule fidelity to v1.** The "no Glass Half Full / no Revenue Translation / sourced numbers only" rules are consistently restated across agents, skills, templates, and tests.
- **Coherent manual test taxonomy** and copy-ready `examples/`.

---

## 8. Fidelity analysis vs. the original system (now that golden files are available)

The v1 golden outputs reveal a **subtle but critical split** the package half-captures:

1. **Grades are the calibration anchors and match exactly.** `ApparelJunction_Grading-Notes_v1.md:182` → `(42+55+38+40+35+18)/6 = 38 → D`; `ExpertServicesUtah_Grading-Notes_v1.md:185` → `(40+75+45+55+45+45)/6 = 50.8 → 51 → C`. These are the numbers a faithful v2 run must reproduce.
2. **The Apparel Junction sample `.md` is a v1-format document — it VIOLATES v2 rules.** It contains a `# Glass Half Full` section (`ApparelJunction_Quick-Audit_v1.md:437`), per-pillar `**Revenue translation:**` paragraphs (lines 107, 154, 186, 221, 251, 299), and **13 glossary terms** (lines 417–431) — v2 mandates none of these and "exactly 8." So Apparel Junction is the golden for **grades only**, not for **format**.
3. **The Expert Services sample `.md` IS v2-format-compliant** — no Glass Half Full, no Revenue Translation, **8 glossary terms** (lines 466–475). It is the correct golden for **v2 format**. Dennis's published `Apparel_Junction_Quick_Audit.pdf` is the canonical format reference.
4. **The Expert Services notes also encode a process lesson** ([ExpertServicesUtah_Grading-Notes_v1.md:220](#)): the live Knowledge-Panel navigation that drove a Reviews regrade (C 55 → B 75, Overall → C 51) "should be promoted from a Failure Mode to a default Step." v2's enrichment skill doesn't yet make this a hard step.

**Implication:** the package's repeated "match the source template" tests are only safe if they compare against **Dennis's PDF / the Expert Services v2 output**, never the Apparel Junction v1 markdown for format. The testing plan (`03-…`) encodes this split explicitly.

---

## 9. File-count assessment (consolidation signal for the refactor)

87 files is **not excessive for what this is**, but ~20 are 1–3-line pointer files or duplicated blocks. Net recommendation (detailed in `02-refactor-plan.md` §D): **consolidate ~10–14 micro-references and dedupe test preconditions; do NOT delete the source-docs or examples** (they carry the fidelity and are cheap via progressive disclosure). Target ≈ 70–75 files, with the *structure* changed (move to `.claude/`) more than the *count*.

---

## 10. Prioritized fix list (full plan in `02-refactor-plan.md`)

| # | Severity | Fix |
|---|---|---|
| C-1 | Critical | Rename `mcp/` → `quick_audit_mcp/`; update `.mcp.json` args + `${CLAUDE_PLUGIN_ROOT}`; add `__init__.py`. |
| C-2 | Critical | Replace interactive OAuth with a service account / pre-seeded refreshable token injected as a routine secret. |
| C-3 | Critical | Move to `.claude/skills/` + `.claude/agents/`, add `CLAUDE.md` orchestrator directive (per Gemini blueprint). |
| C-4 | Critical | Add `scripts/setup.sh` installing `requirements.txt` + `reportlab`; wire as routine setup command. |
| H-1 | High | Scope the dash-case test to non-Python paths; stop forbidding `_` in `*.py`/package dirs. |
| H-2 | High | Convert all env/shell var names to underscores; fix the Zapier sample to use `$QUICK_AUDIT_ROUTINE_FIRE_URL` etc. |
| H-3 | High | Import the v1 golden artifacts into `tests/golden/`. |
| H-4 | High | Normalize `oauth.scopes` to space-separated strings, drop `enabled`, remove duplicate Gmail server, verify endpoints. |
| H-5 | High | Document the orchestrator-as-main-session launch contract; confirm `Agent` tool availability. |
| M-1…M-8, L-1…L-4 | Med/Low | Version single-source, MANIFEST regen, `${CLAUDE_SKILL_DIR}` paths, root `.gitignore`, dedupe references/preconditions. |
