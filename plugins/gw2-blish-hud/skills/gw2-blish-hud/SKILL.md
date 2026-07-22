---
name: gw2-blish-hud
description: Develop, audit, diagnose, and maintain Guild Wars 2 Blish HUD core, modules, and Pathing/TacO marker packs, especially for Traditional Chinese. Use when Codex needs to edit .resx resources, map AppCulture or Gw2Sharp Locale values, inspect ResourceManager and satellite assemblies, remove hard-coded UI strings, package localized .bhm modules, design or translate .taco/XML route packs, coordinate an upstream rights-holder translation workflow, evaluate TmfLib and bh- vendor attributes, define BCP 47 fallback or Marker Pack Repo metadata, support CJK glyphs and fonts, audit translation coverage, or troubleshoot mixed-language text, missing glyphs, culture fallback, and live language refresh.
---

# GW2 Blish HUD

## Working Defaults

- Write user-facing Chinese in Traditional Chinese unless the target repo already uses another convention or the user asks otherwise.
- Preserve resource keys, identifiers, product names, API values, formatting placeholders, XML whitespace semantics, and deliberate line breaks.
- Treat UI culture, GW2 Web API locale, game-client region, and Chinese script variant as separate concepts. Do not equate `Locale.Chinese` with `zh-TW` without evidence.
- Prefer the current workspace as the edit target. Use forks or upstream repositories for comparison unless the user explicitly chooses them as the target.
- Preserve unrelated user changes and generated assets. Inspect before editing.

## Start Here

1. Classify the workspace.
   - Core repo: expect `Blish HUD.sln`, `Blish HUD/Blish HUD.csproj`, `Blish HUD/Strings/`, and `Blish HUD/Content/Content.mgcb`.
   - Module repo: expect a module `.csproj`, `manifest.json`, and usually `ref/`.
   - Route-pack repo: expect `.taco` archives or marker/category XML, `.trl` trails, textures, and possibly pack-building scripts without a module `.csproj`.
2. Confirm the target and baseline with `pwd`, `git status --short --branch`, `git remote -v`, and the relevant branch or tag.
3. Locate localization surfaces with `rg --files` and `rg -n` before changing anything.
4. Read [references/localization-architecture.md](references/localization-architecture.md) for any resource, culture, module packaging, or font task.
5. Read [references/pathing-pack-localization.md](references/pathing-pack-localization.md) before translating a route pack or changing Pathing, TmfLib, pack optimization, or Marker Pack Repo localization.
6. Read [references/windows-font-rendering.md](references/windows-font-rendering.md) before proposing Microsoft JhengHei, another installed Windows font, DirectWrite, GDI+, `.spritefont`, or a rasterized Windows-font asset.
7. Read [references/bundled-cjk-fonts.md](references/bundled-cjk-fonts.md) before selecting Source Han Sans, another bundled CJK font, a variable font, or a distributable bitmap atlas.
8. Run the resource audit before and after `.resx` translation work:

```bash
python3 /Users/jakeuj/.codex/skills/gw2-blish-hud/scripts/audit_resx.py "Blish HUD/Strings" --culture zh --show-keys
```

Use `--culture zh-TW` when the project intentionally uses region-specific files. Use `--strict` in CI or when incomplete localization must fail.

## Choose the Work Path

### Audit or Diagnose

1. For `.resx` work, run `audit_resx.py` against the smallest relevant strings root. For route-pack work, inspect the archive, XML attributes, build inputs, and active loader version instead.
2. Inspect culture selection, resource lookup, pack-content selection, hard-coded strings, and font coverage independently.
3. Explain whether English text comes from resource fallback, a missing resource key, a hard-coded literal, an untranslated pack attribute, a module without a satellite assembly, or a font-rendering failure.
4. Do not implement a fix when the user asked only for diagnosis or review.

### Add or Update Core Translation

1. Edit the culture-specific sibling of the neutral resource, such as `OverlayService.zh.resx` or `OverlayService.zh-TW.resx`.
2. Add new keys to the neutral `.resx` first. Regenerate its strongly typed `.Designer.cs` with the repo's established generator when available; avoid hand-editing generated code.
3. Replace hard-coded UI literals with strongly typed resource accessors or the existing `ResourceManager` pattern.
4. Preserve composite-format placeholders such as `{0}` and `{1:N0}` exactly. Preserve intentional newlines unless layout testing proves a change is needed.
5. Keep the existing culture-file convention unless the user requests a migration. Do not rename all `.zh.resx` files to `.zh-TW.resx` as a side effect of a small translation task.

### Change Culture Selection or Live Refresh

1. Trace `OverlayService.UserLocale`, `AppCulture`, `DefaultThreadCurrentUICulture`, and `UserLocaleChanged` together.
2. Resolve numeric LCIDs rather than trusting comments. In this codebase, `30724` / `0x7804` represents neutral `zh`, not `zh-CN` or `zh-TW`.
3. Inspect `Gw2WebApi/ManagedConnection.cs` before changing the setting: the same selection may also alter GW2 API request locale.
4. Decide whether existing controls must be rebuilt, rebound, or explicitly refreshed after `UserLocaleChanged`; changing the default UI culture only affects subsequent resource lookups.
5. Add a restart requirement only when live refresh cannot be implemented safely.

### Localize a Module

1. Follow the module's existing resource namespace and strongly typed resource pattern.
2. Build the module and verify that the output contains `<culture>/<Module>.resources.dll`.
3. Verify that the `.bhm` package contains that culture directory; Blish HUD loads module resource assemblies from inside the package.
4. Test fallback when the requested culture is absent. Do not assume core translations localize third-party module text.

### Localize a Pathing Route Pack

1. Separate module UI resources, in-pack route content, and Marker Pack Repo metadata; they use different data models and release paths.
2. For a solution that works with current Pathing, keep one structural source plus a translation catalog and build one archive per locale, such as `pack.en.taco` and `pack.zh-Hant.taco`.
3. Preserve GUIDs, category namespaces, coordinates, map IDs, asset paths, and trail data across locale builds. Translate only user-facing fields.
4. Publish locale archives as distinct repo entries and enable only one locale at a time. Do not place complete localized XML copies in one archive expecting Pathing to choose one automatically.
5. When a rights holder offers an upstream contributor role, treat it as a maintenance workflow, not as a license. Confirm the author can authorize bundled content, record durable permission or license evidence, attribution, version scope, and third-party exclusions before publishing a separate archive.
6. Prefer an author-owned `zh-Hant` or `zh-TW` branch/release asset for upstream maintenance. Submit translation PRs only after the scope is agreed; do not assume contributor access authorizes forks, redistribution, or third-party assets.
7. For one archive that follows the selected language, design a backward-compatible Pathing change. Prefer base attributes plus locale-suffixed `bh-` attributes for the first iteration; keep external JSON or XLIFF catalogs for a later coordinated Pathing/TmfLib optimizer change.
8. Treat `zh-Hant`, `zh-Hans`, `zh-TW`, UI culture, and GW2 API `Locale.Chinese` as distinct. Provide a pack-language override when the host cannot represent the desired script reliably.
9. Avoid Lua-based translation except as a disposable prototype; scripts load too late, are optional, and do not provide a stable pack-localization contract.

### Add CJK Font Support

1. Choose between an installed Windows font and a bundled redistributable font. Read the matching font reference before editing assets or code.
2. Confirm which font faces, sizes, styles, measurement calls, wrapping paths, and draw paths are actually used.
3. For the existing bitmap pipeline, treat `.fnt`, every referenced atlas PNG, and `Content.mgcb` as one atomic change. Record the font source, license, glyph range, generator settings, atlas dimensions, page count, and memory impact.
4. Prefer the Taiwan region-specific static Source Han Sans OTFs for a legacy atlas generator. Treat the linked TTF release artifacts as variable fonts and use them only after confirming the selected renderer or generator supports their axes and output deterministically.
5. Preserve the bundled font's license, copyright notice, naming restrictions, and derivative license in release artifacts. Do not assume an open font permits omission of its license or unrestricted derivative naming.
6. Do not derive the glyph set only from core `.resx` files when API values or module strings can introduce new characters. Define and test fallback behavior for missing dynamic glyphs.
7. For a bundled runtime path, load the font from a private or custom font collection and use a bounded glyph or text cache. Do not require system installation or mutate the user's font registry.
8. For a Windows system-font path, detect the installed family at runtime and render through a Windows text API. Add a measurement-and-drawing abstraction because existing controls depend on `BitmapFont.MeasureString` and bitmap glyph drawing; changing only a family name is insufficient.
9. Treat a friendly font name in MonoGame `.spritefont` as a build-machine dependency. The content pipeline rasterizes it into a texture atlas before runtime; it does not make Blish HUD use the installed font on the player's PC.
10. Never copy Microsoft font files or distribute a per-glyph bitmap font converted from a Windows font without an appropriate additional license. Do not globally replace all font variants with large CJK atlases unless the decoded texture-memory tradeoff is measured and intentional.

## Verification

- For `.resx` work, run `audit_resx.py` and resolve placeholder mismatches and malformed XML before building.
- Build the smallest relevant project and inspect culture output directories and satellite assembly names.
- Treat a non-Windows `net472` or MonoGame build failure as environment evidence, not automatically as a code defect; identify what still requires Windows or CI verification.
- Smoke-test startup, language selection, reopening existing views, restart persistence, fallback strings, formatted messages, API-backed text, module UI, and every affected font style.
- For a Windows system-font path, verify runtime family detection, fallback behavior, text measurement, wrapping, clipping, stroke or shadow effects, DPI scaling, and graphics-device reset behavior.
- For a bundled CJK font, inspect the package for its required copyright and license, verify static or variable format support, and test glyphs originating outside core resources.
- For route packs, inspect the archive contents and verify that exactly one intended locale is active, structural IDs are unchanged, localized attributes fall back deterministically, optimized packs preserve localization data, and runtime language changes cannot be dropped during an active load.
- For upstream collaboration, verify that the chosen branch or release contains one language variant, the rights holder owns the release decision, and contributor access has not been mistaken for a content license.
- Report untranslated keys, hard-coded English, unsupported glyphs, generated-file drift, licensing uncertainty, and unverified runtime behavior explicitly.

## Handoff

- Summarize the selected culture convention and why it was preserved or changed.
- List translated resource groups and remaining fallback groups.
- State whether the change affects only core UI, API locale, modules, or font assets.
- For Pathing work, state separately whether the change affects module UI, route-pack content, Marker Pack Repo metadata, Pathing, or TmfLib; record the locale fallback order and archive compatibility.
- State whether CJK text uses a licensed bundled asset or a Windows runtime renderer, and name the fallback path.
- Record the exact font artifact, version, weight, glyph-set source, derivative name, and license file included in the release.
- Provide the exact audit and build commands run, with any remaining manual checks.

## Resources

- Read [references/localization-architecture.md](references/localization-architecture.md) for the code map, resource fallback model, module packaging, font pipeline, and common failure modes.
- Read [references/pathing-pack-localization.md](references/pathing-pack-localization.md) for current pack-loading constraints, immediate per-locale packaging, a backward-compatible `bh-` attribute proposal, PR scope, and verification.
- Read [references/windows-font-rendering.md](references/windows-font-rendering.md) for Microsoft JhengHei availability, runtime-rendering architecture, licensing boundaries, fallback, and verification.
- Read [references/bundled-cjk-fonts.md](references/bundled-cjk-fonts.md) for Source Han Sans selection, OFL compliance, static and variable formats, atlas sizing, runtime caching, and fallback.
- Run `scripts/audit_resx.py` to compare neutral and localized `.resx` key sets and validate values.
