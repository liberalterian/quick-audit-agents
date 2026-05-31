---
name: legacy-quick-audit
description: Phase 1 Cowork-compatible fallback for running the older monolithic Quick Audit flow. Use only when the modular Routine path is unavailable or explicitly requested.
---

# Legacy Quick Audit Fallback Skill

This skill preserves the Phase 1 behavior while delegating PDF rendering to `quick-audit-pdf-render`.

## Use when

- The Claude Routine path is unavailable.
- A human operator needs to process pending Tracker rows manually.
- A regression comparison against the original monolithic flow is required.

## Do not use when

- Running normal production API-triggered audits.
- Testing modular agent contracts.

## Non-negotiables

- No Glass Half Full section.
- No per-pillar Revenue Translation paragraphs.
- Use the shared renderer script.
- Do not duplicate renderer logic.
