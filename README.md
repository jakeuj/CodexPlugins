# Plugins

**English** · [繁體中文](README.zh-Hant.md)

This repository contains a curated collection of Codex plugins for personal use.

Each plugin lives under `plugins/<name>/` with a required
`.codex-plugin/plugin.json` manifest and optional companion surfaces such as
`skills/`, `.app.json`, `.mcp.json`, plugin-level `agents/`, `commands/`,
`hooks.json`, `assets/`, and other supporting files.

The default Codex marketplace lives at `.agents/plugins/marketplace.json` and
points at the standard `plugins/` directory.

Claude Code marketplace metadata lives at `.claude-plugin/marketplace.json` so
the repository can also be added with:

```bash
/plugin marketplace add jakeuj/CodexPlugins
```

## Current Plugins

- [`evennia`](./plugins/evennia/) — Evennia MUD game development skills — 28 comprehensive skills covering typeclasses, commands, attributes, tags, scripts, locks, channels, command sets, objects, rooms, exits, characters, accounts, prototypes, default commands, help system, EvMenu, EvEditor, nicks, coding utils, sessions, signals, ticker/monitor/on-demand handlers, REST API, and web admin.
- [`bahamut-post`](./plugins/bahamut-post/) — Create, rewrite, convert, and repair Traditional Chinese Bahamut/Gamer.com.tw forum posts with editor-safe source markup.
- [`gw2-blish-hud`](./plugins/gw2-blish-hud/) — Develop, audit, and localize Guild Wars 2 Blish HUD, modules, and Pathing/TacO marker packs, especially for Traditional Chinese and CJK support.
- [`google-seo`](./plugins/google-seo/) — Audit and improve crawlability, indexing, search appearance, JavaScript SEO, mobile-first indexing, and people-first content using Google Search Central guidance.

## Publishing a Skill to the Marketplace

Use the repository skill `$publish-skill-to-marketplace` to inspect the current
marketplace, add a skill to one clearly matching local plugin, or create a new
plugin with the built-in `$plugin-creator` when no suitable plugin exists.

```text
Use $publish-skill-to-marketplace to add $bahamut-post to this repository's marketplace.
```

When the requested skill does not exist yet, provide its name, behavior, and a
few concrete examples. The workflow uses the built-in `$skill-creator` to create
and validate it before packaging.

## Creating a New Plugin

1. In Codex, use the built-in `$plugin-creator` skill to scaffold a plugin
   under this repository's `plugins/` directory:

```text
Use $plugin-creator to create <plugin-name> under this repository's plugins/ directory.
```

2. Edit `plugins/<name>/.codex-plugin/plugin.json` to fill in Codex metadata.

3. Add `plugins/<name>/.claude-plugin/plugin.json` if the plugin should also be
   installable from Claude Code.

4. Add skills, assets, or other companion files under `plugins/<name>/`.

5. If the plugin should appear in this repository's Codex marketplace, ask the
   built-in skill to add it:

```text
Use $plugin-creator to add plugins/<plugin-name> to this repository's .agents/plugins/marketplace.json.
```
