# Architecture

## Runtime architecture

```text
SPP or intake form
  -> Zapier or intake backend
  -> Google Sheet Tracker row
  -> Claude Routine API trigger (/fire, payload in the `text` field)
  -> main session loads CLAUDE.md and acts as quick-audit-orchestrator-agent
      -> quick-audit-intake (skill)
      -> quick-audit-agent (subagent)
          -> quick-audit-enrichment
          -> quick-audit-grading
          -> quick-audit-report
          -> quick-audit-pdf-render
              -> .claude/skills/quick-audit-pdf-render/scripts/render-audit-pdf.py
      -> qualification-agent (subagent)
          -> quick-audit-qualification
      -> routing-agent (subagent)
          -> quick-audit-routing
  -> Drive artifacts + Gmail drafts + Tracker writeback
```

Subagents cannot spawn subagents, so the orchestrator must run as the **main session** (via the
routine prompt + `CLAUDE.md`). Each subagent runs its skills inline.

## Agent responsibilities

- **quick-audit-orchestrator-agent** — run control, validation, delegation, failure handling, final RUN COMPLETE.
- **quick-audit-agent** — enrichment, grading, audit synthesis, audit-spec JSON, PDF render coordination.
- **qualification-agent** — applies the MVS rubric to the same enrichment record; does not re-pull or alter grades.
- **routing-agent** — Drive upload, Gmail draft, conditional team alert, Tracker writeback.

## Skill responsibilities

See `.claude/skills/skill-index.md`.

## Artifact flow

```text
intake-payload -> run-context -> enrichment-record -> grading-notes -> audit-markdown
  -> audit-spec-json -> audit-pdf -> qualification-record -> routing-record -> final-tracker-state
```

## Data source strategy

- **Ahrefs SEO data** — Ahrefs hosted MCP (`.mcp.json`).
- **Gmail draft creation** — Google Gmail **connector** (claude.ai connector on the routine).
- **Drive file persistence** — Google Drive **connector**.
- **Google Places business lookup** — local `quick-audit-tools` server (Places API, service-account/API key).
- **Tracker writeback (Sheets)** — local `quick-audit-tools` server (Sheets API, service account).
- **PageSpeed** — local `quick-audit-tools` server.

(There are no public `gmailmcp`/`drivemcp` MCP endpoints; Gmail/Drive are connectors, not `.mcp.json` servers.)

## Failure principles

- A missing optional data source does not block audit shipment — note "data unavailable" and continue.
- Never fabricate competitor numbers, rankings, review/follower counts, projections, or CPC/CPL.
- Do not fall back to a generic PDF skill; fix the JSON spec or renderer issue.
- On any failure, still write a Tracker failure note.
