---
name: publish-skill-to-marketplace
description: Package an existing or newly described Codex skill into the best matching local plugin and expose it through a repository or personal marketplace. Use when asked to publish, convert, bundle, or add a skill to a Codex plugin marketplace; decide whether the skill belongs in an existing plugin; create a new plugin with $plugin-creator; or create a missing skill with $skill-creator before packaging it.
---

# Publish Skill to Marketplace

Package one skill without disturbing unrelated plugins or the source skill.

## Inputs and defaults

- Accept an invoked skill, skill name, or absolute skill directory.
- Accept a new skill name plus a concrete description and examples when no source skill exists.
- Accept optional target plugin, repository root, and marketplace path overrides.
- Default the repository root to `git rev-parse --show-toplevel` and the marketplace to `<repo-root>/.agents/plugins/marketplace.json`.
- Resolve an existing skill in this order: explicit path or invoked-skill path, `<repo-root>/.agents/skills/<name>`, `$CODEX_HOME/skills/<name>`, then `~/.codex/skills/<name>`.

Before changing a plugin or marketplace, load and follow `$plugin-creator`. Before creating or materially revising a skill, load and follow `$skill-creator`.

## Inspect candidates

Run the bundled inventory helper before choosing a plugin:

```bash
python3 <publish-skill-root>/scripts/package_skill.py inventory \
  --repo-root <repo-root> \
  --marketplace <marketplace.json> \
  --skill <skill-directory>
```

Omit `--skill` when the requested skill has not been created yet; compare candidates against the supplied name and description instead.

If inventory reports `"marketplace_exists": false`, treat the candidate set as empty and continue with a new plugin scaffold. Let `$plugin-creator` create the marketplace; do not hand-write it.

Consider only writable local plugins returned by the helper. Inspect each plugin's name, manifest description, keywords, and bundled skill frontmatter.

- Honor an explicitly selected plugin only when it is a returned local marketplace plugin.
- Treat a plugin as a clear match only when it shares a specific platform, product, publishing surface, or subject domain with the skill.
- Never match solely because both entries use a generic category such as `Productivity`, both write text, or both use the same language.
- Choose the only clear match. Ask the user when multiple candidates remain plausible. Create a new plugin when none clearly match.
- Do not modify URL, Git, npm, cached, missing, or otherwise non-local candidates.

## Resolve or create the skill

For an existing skill:

1. Read its complete `SKILL.md` and inventory the complete skill tree.
2. Inspect `source_skill.portability_issues` from the inventory output. Review every match and plan packaged-copy changes for execution or resource paths tied to the source skill root, `~/.codex/skills`, or `$CODEX_HOME/skills`.
3. Inspect `agents/openai.yaml` when present. Read only references or scripts required by the skill's routing instructions or the current packaging decision; do not load unrelated references or assets merely to copy them.
4. Run `quick_validate.py` from `$skill-creator` against the source directory.
5. Keep the source directory unchanged.

When the skill does not exist:

1. Require a normalized name plus enough description or examples to define its behavior. Ask for missing product intent instead of inventing it.
2. Use the proposed name and description to choose the target plugin.
3. Run `$skill-creator`'s `init_skill.py` with the target plugin's `skills/` directory as `--path` and create only the needed resources.
4. Replace every placeholder, generate `agents/openai.yaml`, implement any resources, and validate the new skill before packaging continues.

## Package into a plugin

For a new plugin, run `$plugin-creator`'s scaffold with explicit repository paths:

```bash
python3 <plugin-creator-root>/scripts/create_basic_plugin.py <plugin-name> \
  --path <repo-root>/plugins \
  --marketplace-path <marketplace.json> \
  --with-skills \
  --with-marketplace
```

Do not pass `--marketplace-name` for an existing marketplace. After scaffolding, replace the generic manifest values with real metadata derived from the skill and repository conventions. Keep `name` equal to the outer folder, use `0.1.0` for a new plugin, point `skills` to `./skills/`, include no more than three starter prompts, and omit assets, legal URLs, apps, and MCP fields unless they actually exist.

For an existing plugin, preserve its manifest and marketplace metadata. Ensure only that `skills` resolves to `./skills/`. After adding a new skill, use `$plugin-creator`'s `update_plugin_cachebuster.py`; do not rewrite its marketplace entry.

Copy an existing source skill with the helper:

```bash
python3 <publish-skill-root>/scripts/package_skill.py copy \
  --source <skill-directory> \
  --plugin-root <plugin-directory>
```

The helper copies the complete skill tree while excluding common caches and compares file contents plus executable state. If the destination is identical, accept the no-op result. If it differs, stop and ask whether to replace or merge; never overwrite it implicitly.

When inventory reports portability issues, change only the packaged copy after copying. Resolve skill-bundled resources from `<plugin-root>/skills/<skill-name>/...` or an equivalent runtime-resolved skill root; resolve plugin-level resources from `<plugin-root>/...`. Never rely on the repository working directory. Review matches instead of blindly rewriting prose or examples, and run every affected script. On later publishes, preserve intentional packaged-only adaptations by reviewing the source/destination diff and merging rather than replacing.

## Validate and hand off

1. Validate every packaged skill with `$skill-creator`'s `quick_validate.py`.
2. Confirm every reported portability issue was intentionally rewritten or explicitly retained, and verify no packaged execution path still depends on the source skill location.
3. Validate the plugin with `$plugin-creator`'s `validate_plugin.py`.
4. Parse the marketplace and manifest as JSON, confirm the marketplace path resolves inside the selected root, and ensure plugin name, folder, and entry match.
5. Update existing repository plugin lists or usage documentation when present.
6. Run `python3 <publish-skill-root>/scripts/test_package_skill.py`, any relevant repository tests, and `git diff --check`.
7. Do not install, register, or share the marketplace unless the user explicitly requests it.
8. When a marketplace entry was created or updated, finish with URL-encoded Codex app View and Share links using the absolute marketplace path.
