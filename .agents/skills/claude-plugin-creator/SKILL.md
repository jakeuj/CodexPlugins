---
name: claude-plugin-creator
description: Create, scaffold, review, or port Claude Code plugins using Anthropic's plugin-dev create-plugin workflow. Use when Codex needs to build `.claude-plugin/plugin.json`, Claude Code plugin skills, agents, hooks, MCP integrations, settings, or marketplace-ready plugin structure.
---

# Claude Plugin Creator

Use this skill to create or update Claude Code plugins from this repo. It adapts
Anthropic's `plugin-dev:create-plugin` workflow into a Codex skill and keeps the
original plugin-dev material under `references/plugin-dev/`.

## Reference Map

Load only the reference files needed for the requested component:

- End-to-end plugin creation workflow:
  `references/plugin-dev/commands/create-plugin.md`
- Plugin layout, manifest fields, and component patterns:
  `references/plugin-dev/skills/plugin-structure/SKILL.md`
- Creating Claude Code skills:
  `references/plugin-dev/skills/skill-development/SKILL.md`
- Creating Claude Code agents:
  `references/plugin-dev/skills/agent-development/SKILL.md`
- Creating hooks:
  `references/plugin-dev/skills/hook-development/SKILL.md`
- Creating MCP integrations:
  `references/plugin-dev/skills/mcp-integration/SKILL.md`
- Creating plugin-local settings:
  `references/plugin-dev/skills/plugin-settings/SKILL.md`
- Maintaining legacy `commands/` slash-command files:
  `references/plugin-dev/skills/command-development/SKILL.md`
- Agent prompts for review/generation reference:
  `references/plugin-dev/agents/`

The copied plugin-dev material is Apache-2.0 licensed; keep
`references/plugin-dev/LICENSE` with it.

## Workflow

1. Clarify the plugin purpose, target user, and expected trigger phrases unless
   the request is already specific.
2. Read `references/plugin-dev/commands/create-plugin.md` for the full workflow
   when creating a complete plugin.
3. Read `plugin-structure/SKILL.md` before choosing directories, manifest
   fields, or component types.
4. Decide which Claude Code components are needed:
   - `skills/<name>/SKILL.md` for reusable knowledge or user-invoked workflows.
   - `agents/*.md` for autonomous review/generation roles.
   - `hooks/hooks.json` plus hook scripts for event-driven automation.
   - `.mcp.json` for MCP servers.
   - `.claude/*.local.md` patterns for user settings.
   - `commands/*.md` only when maintaining legacy command layout.
5. Read the matching component reference before writing files.
6. Create or update `.claude-plugin/plugin.json` and any requested components.
7. Validate with `claude plugin validate <plugin-path>` when the Claude CLI is
   available.

## Repo Conventions

- For plugins in this repository, place Claude Code plugins under
  `plugins/<plugin-name>/`.
- If the plugin should also work in Codex, keep or add
  `.codex-plugin/plugin.json` separately; Claude uses `.claude-plugin/plugin.json`.
- If the plugin should be installable from Claude Code marketplace, update the
  root `.claude-plugin/marketplace.json`.
- If the plugin should appear in the Codex marketplace, update
  `.agents/plugins/marketplace.json`.
- Prefer Claude Code `skills/<name>/SKILL.md` for new user-invoked workflows.
  Use `commands/` only for existing legacy command plugins.

## Validation

After creating or changing a plugin, run:

```bash
claude plugin validate <plugin-path>
```

After changing this skill itself, run:

```bash
python3 /Users/jakeuj/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/claude-plugin-creator
```
