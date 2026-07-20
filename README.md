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

## Creating a New Plugin

1. Scaffold a plugin directory:

```bash
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py <plugin-name>
```

2. Edit `plugins/<name>/.codex-plugin/plugin.json` to fill in Codex metadata.

3. Add `plugins/<name>/.claude-plugin/plugin.json` if the plugin should also be
   installable from Claude Code.

4. Add skills, assets, or other companion files under `plugins/<name>/`.

5. If the plugin should appear in your personal Codex marketplace, run with
   `--with-marketplace`:

```bash
python3 .agents/skills/plugin-creator/scripts/create_basic_plugin.py <plugin-name> --with-marketplace
```
