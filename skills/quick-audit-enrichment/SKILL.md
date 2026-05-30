---
name: quick-audit-enrichment
description: Collect public and connected-source data needed for the Quick Audit signal list.
---

# Quick Audit Enrichment Skill

## Mission

Build one enrichment record for the prospect. Do not synthesize the audit in this skill.

## Data pulls

1. Google Places identity resolution using direct Places API or a trusted Places MCP if available.
2. Website fetch and technical extraction.
3. PageSpeed Insights mobile run.
4. Social channel inventory across Facebook, Instagram, TikTok, YouTube, LinkedIn company, LinkedIn personal/founder, Pinterest, and Nextdoor.
5. Ahrefs MCP enrichment for DR, referring domains, backlinks, organic keywords, organic traffic estimate, top keywords, and competitors.
6. Brand SERP snapshot.
7. Local pack and service-city scan.
8. Ads transparency snapshot when accessible.

## Output

A structured enrichment JSON record. Every numeric assertion must carry a source label.

## Data unavailable

If a source fails, write `data-unavailable` for that source and continue unless the failure prevents identity resolution entirely.
