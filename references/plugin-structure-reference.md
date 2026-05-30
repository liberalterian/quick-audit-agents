# Plugin Structure Reference

## Required plugin manifest path

Use:

```text
.claude-plugin/plugin.json
```

## Skill discovery

Claude Code skills are directories under `skills/` containing `SKILL.md`.

## Agent discovery

Agents live under `agents/` as markdown files with YAML frontmatter.

## MCP discovery

Project-scoped MCP servers live in root `.mcp.json`.

## This package correction

Earlier package drafts used lowercase `skill.md`. This package uses `SKILL.md` to match Claude Code plugin conventions.
