# Agent Skill Architecture Audit

## Conclusion

The previous monolithic `quick-audit` skill mixed orchestration, enrichment, grading, report writing, PDF rendering, qualification, routing, and Tracker writeback. That made it hard to test, hard to reuse, and easy for stale instructions to persist.

The production architecture should use an orchestrator agent plus granular skills.

## Production call graph

```text
quick-audit-orchestrator-agent
  -> quick-audit-intake
  -> quick-audit-agent
      -> quick-audit-enrichment
      -> quick-audit-grading
      -> quick-audit-report
      -> quick-audit-pdf-render
  -> qualification-agent
      -> quick-audit-qualification
  -> routing-agent
      -> quick-audit-routing
```

## Fallback path

`legacy-quick-audit` remains available for Phase 1 Cowork compatibility and emergency manual runs. It must not fork renderer logic. It calls `quick-audit-pdf-render` for PDF output.

## Known architecture decisions

- Qualification consumes enrichment; it does not duplicate enrichment.
- PDF rendering is JSON-driven and centralized.
- Google Places and Tracker writeback use direct APIs unless trusted MCP servers are added.
- The Routine is a single production entry point; do not split the main flow into multiple separate Routines until operational need exists.
