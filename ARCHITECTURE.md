# Architecture

## Runtime architecture

```text
SPP or intake form
  -> Zapier or intake backend
  -> Google Sheet Tracker row
  -> Claude Routine API trigger
  -> quick-audit-orchestrator-agent
      -> quick-audit-intake
      -> quick-audit-agent
          -> quick-audit-enrichment
          -> quick-audit-grading
          -> quick-audit-report
          -> quick-audit-pdf-render
              -> scripts/render-audit-pdf.py
      -> qualification-agent
          -> quick-audit-qualification
      -> routing-agent
          -> quick-audit-routing
  -> Drive artifacts + Gmail drafts/sends + Tracker writeback
```

## Agent responsibilities

### quick-audit-orchestrator-agent

Owns run control, state transitions, validation, delegation, failure handling, and final run-complete output.

### quick-audit-agent

Owns enrichment, grading, audit synthesis, audit-spec JSON creation, and PDF render coordination.

### qualification-agent

Consumes the intake and enrichment record. Applies the downstream qualification rubric. Does not re-pull data and does not alter audit grades.

### routing-agent

Owns final delivery: Drive upload, Gmail draft/send, team alert routing, and Tracker writeback.

## Skill responsibilities

See `skills/skill-index.md`.

## Artifact flow

```text
intake-payload
  -> run-context
  -> enrichment-record
  -> grading-notes
  -> audit-markdown
  -> audit-spec-json
  -> audit-pdf
  -> qualification-record
  -> routing-record
  -> final-tracker-state
```

## Data source strategy

- Ahrefs SEO data: Ahrefs MCP.
- Gmail draft creation: Google Gmail MCP.
- Drive file persistence: Google Drive MCP.
- Google Places business lookup: direct Google Places API unless a trusted Places MCP is explicitly wired.
- Tracker writeback: direct Google Sheets API unless a trusted Sheets MCP is explicitly wired.
- Google Maps documentation assistance: Google Maps Code Assist MCP, docs only.

## Failure principles

- A missing optional data source does not block audit shipment.
- Data unavailable must be called out in the relevant section and the Grading Notes file.
- Do not fabricate competitor numbers, rankings, review counts, follower counts, projections, or CPC/CPL assumptions.
- Do not silently fall back to the generic PDF skill; fix the JSON spec or renderer issue.
