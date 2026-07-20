# Windows System Fonts for Blish HUD

## Verified Baseline

As of July 2026, Microsoft's Windows typography documentation lists Microsoft JhengHei and Microsoft JhengHei UI on supported Windows versions. The family covers Traditional Chinese and Bopomofo; Windows guidance maps `zh-TW` UI to Microsoft JhengHei UI. Prefer the UI family for overlay controls when it is installed.

Relevant Windows files include `msjh.ttc`, `msjhbd.ttc`, and `msjhl.ttc`. Treat filenames as diagnostic evidence only. Resolve the family through the system font collection rather than opening or copying these files.

Traditional Chinese supplemental fonts can also be delivered through the Windows capability `Language.Fonts.Hant~~~und-HANT~0.0.1.0`. Still detect the family at runtime: corporate images, Windows Server, stripped installations, Wine, and CrossOver may differ from a normal Taiwan Windows desktop.

## Licensing Boundary

Microsoft's public font FAQ allows Windows applications to use fonts installed system-wide to display text on screen. It does not grant permission to copy or redistribute the Windows font files.

The same FAQ explicitly distinguishes rendered text from a converted font: converting a Windows font into a bitmap font for inclusion in a game or application does not change the font's rights. Do not ship `msjh*.ttc`, a generated per-glyph atlas, or another reusable rasterized derivative without an appropriate additional license.

Runtime rendering of complete strings or layout runs for display, with local ephemeral caching, stays aligned with ordinary application use. Do not turn that cache into a distributable glyph set. Treat this as implementation guidance from public documentation, not legal advice; re-check current official terms before release.

## Why Existing Blish HUD Cannot Select It Directly

`ContentService.GetFont` returns MonoGame Extended `BitmapFont` instances loaded from `fonts\\...` content assets. `Content.mgcb` imports `.fnt` metadata and atlas PNGs through `BitmapFontImporter`. The active renderer therefore knows only the glyphs already present in those assets.

MonoGame `.spritefont` does not provide runtime system-font selection. Its friendly `FontName` is resolved where content is built, then the content pipeline serializes a texture atlas for runtime loading. Using `Microsoft JhengHei UI` there would create a build-time dependency and a rasterized font asset, which must still be licensed for distribution.

Existing controls also call `BitmapFont.MeasureString` and draw individual bitmap glyphs. A system-font implementation needs compatible measurement, wrapping, and drawing behavior; replacing one font-name string is insufficient.

## Choose an Implementation

### Use a Windows Runtime Renderer

Prefer DirectWrite for a production Windows path. Resolve `Microsoft JhengHei UI` through the DirectWrite system font collection, shape and lay out complete text runs, render them locally, upload the result to MonoGame `Texture2D`, and cache by text plus every layout-affecting input.

Include at least text, family, size, weight, style, width, alignment, culture, DPI, and effect parameters in the cache key. Dispose GPU resources and rebuild them after graphics-device resets. Bound the cache by memory or least-recently-used eviction.

GDI+ or `System.Drawing` can prove the integration, but DirectWrite is the preferred architecture for shaping, fallback, metrics, and modern Windows text rendering. Do not assume per-character rendering will preserve kerning, shaping, or fallback; cache complete runs or layout fragments.

Introduce a renderer abstraction with operations equivalent to measure, layout or wrap, and draw. Adapt affected controls incrementally. Keep the current `BitmapFont` renderer as a fallback and for unchanged Latin UI.

### Use a Licensed Bundled Bitmap Font

Keep the existing `.fnt` and PNG pipeline when cross-platform behavior, offline reproducibility, or unchanged control code matters more than using the Windows font. Choose an open or separately licensed CJK font whose terms permit the generated atlas to be distributed.

Generate all required weights and styles, register every atlas page, and test texture memory. This is the appropriate path for a precompiled CJK glyph atlas; Microsoft JhengHei is not the default source for that asset.

Read [bundled-cjk-fonts.md](bundled-cjk-fonts.md) for Source Han Sans artifact selection, OFL obligations, variable-font compatibility, and runtime-cache guidance.

## Runtime Detection and Fallback

Use the DirectWrite system font collection in production. For a quick diagnostic on Windows, this read-only PowerShell probe can enumerate the family:

```powershell
Add-Type -AssemblyName System.Drawing
$fonts = New-Object System.Drawing.Text.InstalledFontCollection
$fonts.Families.Name | Where-Object { $_ -like "Microsoft JhengHei*" }
```

If the UI family is unavailable, try an explicitly approved system-family fallback, then the existing Blish HUD bitmap font for supported characters. For full CJK coverage outside Windows, use a bundled font or atlas with verified redistribution rights. Optionally explain how to install the Traditional Chinese font capability, but do not silently mutate Windows features.

## Verification

- Test regular, bold, italic, headings, tooltips, notifications, and mixed Latin/CJK text.
- Compare measurement with drawing for wrapping, clipping, ellipsis, alignment, line height, and baseline.
- Test Traditional Chinese punctuation, Bopomofo, supplementary characters, emoji fallback, and GW2/API-provided names.
- Test multiple DPI settings, overlay scaling, device reset, cache eviction, and repeated language switching.
- Test the missing-family fallback on a machine or environment without Microsoft JhengHei UI.
- Confirm release artifacts contain no Microsoft font files or generated reusable glyph atlas derived from them.

## Official Sources

- [Microsoft JhengHei font family](https://learn.microsoft.com/en-us/typography/font-list/microsoft-jhenghei)
- [Windows 11 font list](https://learn.microsoft.com/zh-tw/typography/fonts/windows_11_font_list)
- [International fonts and language mapping](https://learn.microsoft.com/en-us/windows/apps/design/globalizing/loc-international-fonts)
- [Windows language and region Features on Demand](https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/features-on-demand-language-fod?view=windows-11)
- [Microsoft font redistribution FAQ](https://learn.microsoft.com/en-us/typography/fonts/font-faq)
- [MonoGame SpriteFont tutorial](https://docs.monogame.net/articles/tutorials/building_2d_games/16_working_with_spritefonts/index.html)
- [MonoGame content pipeline overview](https://docs.monogame.net/articles/getting_to_know/whatis/content_pipeline/CP_Overview.html)
- [MonoGame SpriteFont XML schema](https://docs.monogame.net/articles/getting_to_know/whatis/content_pipeline/CP_SpriteFontSchema.html)
