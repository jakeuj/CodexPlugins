# Blish HUD Localization Architecture

## Repository Map

- `Blish HUD/Strings/**/*.resx`: neutral and culture-specific core strings.
- `Blish HUD/Strings/**/*.Designer.cs`: strongly typed accessors generated from neutral resources.
- `Resources.Designer.t4`: repository-level resource accessor template.
- `Blish HUD/GameServices/OverlayService.cs`: `AppCulture`, culture mapping, and `UserLocaleChanged`.
- `Blish HUD/GameServices/Gw2WebApi/ManagedConnection.cs`: applies the same locale selection to GW2 API requests.
- `Blish HUD/GameServices/Modules/ModuleManager.cs`: resolves module dependencies and culture-specific resource assemblies from `.bhm` packages.
- `Blish HUD/build/BlishHUD.targets`: copies build output and packages it into `.bhm`; satellite directories must already be in output.
- `Blish HUD/Content/Content.mgcb`: MonoGame content registrations.
- `Blish HUD/Content/fonts/**/*.fnt` and atlas PNG files: precompiled bitmap fonts used by the overlay.
- `Blish HUD/GameServices/ContentService.cs`: resolves and lazily caches bitmap-font faces, sizes, and styles.

## Resource Lookup Model

The neutral `.resx` is the exhaustive English fallback embedded in the main assembly. Culture-specific siblings compile into satellite assemblies in culture-named directories. Strongly typed accessors call `ResourceManager.GetString`; when the selected resource or key is missing, .NET probes parent cultures and then the neutral resource.

Keep these distinctions explicit:

- `.zh.resx`: neutral Chinese resource.
- `.zh-Hant.resx`: Traditional Chinese script resource.
- `.zh-TW.resx`: Taiwan-specific Traditional Chinese resource.
- `CultureInfo.GetCultureInfo(30724)`: neutral `zh`, despite the historical inline comment that calls it `zh-CN`.
- `Gw2Sharp.WebApi.Locale.Chinese`: GW2 API language choice, not a guarantee of Taiwan terminology or Traditional Chinese data.

Use the repo's current convention for incremental fixes. For a deliberate redesign, prefer an explicit UI culture such as `zh-TW` and consider decoupling UI culture from API locale.

## Adding Resource Keys

1. Add a stable English key and value to the neutral `.resx`.
2. Regenerate the neutral strongly typed designer using the established Visual Studio or template workflow.
3. Add the same key to supported culture files.
4. Replace the hard-coded UI literal with the generated accessor.
5. Validate placeholder and newline parity.

Localized files normally do not need their own designer. A translated value can intentionally be absent; ResourceManager then falls back to neutral English.

## Runtime Language Changes

`OverlayService` stores `AppCulture`, maps the enum to `CultureInfo`, sets `CultureInfo.DefaultThreadCurrentUICulture`, and raises `UserLocaleChanged`. This changes later resource lookups. Text copied into an existing control remains unchanged until the control is rebound, rebuilt, or restarted.

Search for subscribers before promising live switching:

```bash
rg -n "UserLocaleChanged|DefaultThreadCurrentUICulture|CurrentUICulture" "Blish HUD"
```

Also trace `ManagedConnection`: changing `UserLocale` updates the GW2 API connection locale.

## Module Satellite Assemblies

A localized module normally builds a culture directory such as:

```text
bin/<configuration>/<target-framework>/
├── ExampleModule.dll
└── zh/
    └── ExampleModule.resources.dll
```

`BlishHUD.targets` packages the full output directory. At runtime, `ModuleManager` resolves non-invariant resource assemblies from `<culture>/<assembly>.resources.dll` inside the `.bhm`. If a module does not ship the requested satellite assembly or still hard-codes text, core translation cannot fix it.

## Bitmap Font Pipeline

Blish HUD uses MonoGame Extended bitmap fonts. Runtime rendering reads glyph metadata from `.fnt` and pixels from precompiled atlas PNGs; replacing a `.ttf` alone has no effect.

Read [windows-font-rendering.md](windows-font-rendering.md) before proposing an installed font such as Microsoft JhengHei UI, a DirectWrite renderer, or a `.spritefont` conversion. A friendly family name in `.spritefont` is resolved on the content build machine and rasterized before runtime; it does not select that font from the player's Windows installation.

Read [bundled-cjk-fonts.md](bundled-cjk-fonts.md) before bundling Source Han Sans or another redistributable font. Font-file size does not predict atlas memory: every generated size, weight, glyph, and atlas page contributes decoded texture memory.

For every affected font variant:

1. Verify the Unicode codepoints required by translated UI and module content.
2. Generate `.fnt` and all referenced atlas pages with reproducible settings.
3. Register every new PNG page in `Content.mgcb`.
4. Verify atlas dimensions, page count, texture format, line height, baseline, offsets, wrapping, clipping, and stroke rendering.
5. Test regular, bold, italic, tooltip, heading, notification, and large-title paths.
6. Measure distribution size and estimated decoded texture memory; large CJK atlases can be cheap on disk but expensive after upload to the GPU.

## Failure Map

- English string among Chinese UI: missing localized key, missing culture file, hard-coded literal, or module fallback.
- Squares or missing characters: active bitmap font lacks the codepoint or the required atlas page was not built.
- Windows has Microsoft JhengHei but text still has missing glyphs: the existing Blish HUD path loads precompiled `BitmapFont` assets and never asks Windows to render that text.
- `.spritefont` builds locally but the release has licensing or portability problems: the font was a build-time dependency and the generated atlas is still a rasterized font asset.
- Variable TTF works in one tool but not the release pipeline: the legacy generator did not support or deterministically instantiate the variation axis; use a tested static face.
- Core translations render but API or module names show squares: the atlas glyph set was derived only from core resource strings and lacks dynamic characters.
- Correct after restart only: existing controls cached text and do not react to `UserLocaleChanged`.
- Core translated but module English: module lacks its own resource satellite or uses hard-coded text.
- Format exception: placeholders differ between neutral and translated values.
- Correct UI but unexpected API names: UI culture and GW2 API locale are coupled.
- Build succeeds but packaged module is English: culture directory was not included in `.bhm`.
- Large memory regression: oversized, always-loaded, or duplicated bitmap atlases.
