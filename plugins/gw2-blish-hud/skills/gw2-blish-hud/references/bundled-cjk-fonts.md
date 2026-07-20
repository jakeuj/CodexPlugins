# Bundled CJK Fonts for Blish HUD

## Selection Rule

Prefer a bundled font when Blish HUD must render CJK consistently without depending on fonts installed in Windows. Verify that the license permits copying the font, embedding it with software, modifying or subsetting it, and distributing generated font assets.

Source Han Sans is a strong default for Traditional Chinese. Adobe releases it under SIL Open Font License 1.1 and provides Taiwan-specific artifacts. Re-check the current release and license before shipping; the verified release in July 2026 was version 2.005R, published June 18, 2025.

## Choose the Source Han Sans Artifact

Use the Taiwan region-specific static OTFs for an existing or legacy bitmap-atlas generator:

- `SubsetOTF/TW/SourceHanSansTW-Regular.otf`
- `SubsetOTF/TW/SourceHanSansTW-Bold.otf`

The Taiwan subset folder contains seven static weights. Adobe recommends region-specific subset OTFs when only one region is needed or when the deployer is unsure which format to select. These files contain Taiwan glyph forms and are smaller and simpler than the full language-specific variable font.

Distinguish these variable TTF choices:

- `Variable/TTF/SourceHanSansTC-VF.ttf`: language-specific Traditional Chinese with broad Pan-CJK character coverage and localized-form support.
- `Variable/TTF/Subset/SourceHanSansTW-VF.ttf`: Taiwan region-specific glyph subset in one variable font.

Do not assume a `.ttf` extension means a static font. Both files above are variable fonts. Use one only when the selected rasterizer or runtime renderer supports its `wght` axis and produces tested, deterministic metrics and glyphs. Avoid `HW` artifacts unless half-width ASCII is an explicit design requirement.

Source Han Sans provides weights rather than native italic faces. Decide whether CJK italic requests should use regular glyphs, synthetic oblique, or another licensed face; test metrics and record the choice.

## Apply OFL 1.1 Correctly

Source Han Sans may be used, copied, embedded, modified, redistributed, and bundled with software. It may not be sold by itself.

Include Adobe's copyright notice and the complete `LICENSE.txt` with every distributed copy of the font or derivative font asset. Keep the original or modified font asset under OFL 1.1; this does not require unrelated Blish HUD source code to use OFL.

The license reserves the font name `Source`. It defines changing formats as a modified version. Conservatively treat a generated bitmap font, subset, or other converted reusable font asset as a modified version: give its primary user-facing font name a project-specific value such as `BlishHudCjkTW`, retain attribution, and do not imply Adobe endorsement.

Do not make legal conclusions from the repository license badge alone. Read the distributed `LICENSE.txt`, retain it in the package, and report unresolved naming or redistribution questions before release.

## Integrate with the Existing Bitmap Pipeline

Dropping an OTF or TTF file into `Content` is insufficient. Existing Blish HUD UI fonts are MonoGame Extended `BitmapFont` assets loaded from `.fnt` metadata and atlas PNG pages.

For a precompiled atlas:

1. Select a static face and explicit pixel size.
2. Build a reproducible codepoint list from translated resources plus approved dynamic coverage.
3. Generate `.fnt` and every atlas page with recorded tool version, anti-aliasing, padding, outline, and variation settings.
4. Register all pages in `Content.mgcb` and package the OFL notice and copyright.
5. Measure decoded texture memory, not only compressed PNG or source-font file size.

Do not generate every Source Han Sans glyph for every existing Blish HUD size and style without a memory budget. The current font matrix contains many variants, and a CJK atlas can require dozens or hundreds of pages per variant. Prefer the smallest verified UI matrix, culture-specific lazy loading, or runtime caching.

Resource-only subsetting is incomplete when UI includes GW2 API values, account or character names, user input, and third-party module strings. Add a defined missing-glyph fallback or broader approved coverage and test with dynamic text.

## Prefer Runtime Caching for Broad Coverage

For broad CJK coverage, load the bundled font from a private or custom font collection and rasterize glyphs or text runs on demand. Bound the cache by memory, dispose GPU textures, and rebuild them after graphics-device resets.

Do not install the font globally or require administrator access. Keep the bundled file private to the application. Preserve shaping, fallback, kerning, measurement, wrapping, DPI, and weight selection when introducing a renderer abstraction.

Use the existing Menomonia bitmap font for supported Latin text when retaining the GW2 visual style matters. A mixed-font fallback needs consistent measurement and baseline handling; switching fonts only during drawing can break wrapping and clipping.

## Verification

- Test Traditional Chinese Taiwan glyph forms, punctuation, Bopomofo, Latin/CJK mixing, and every selected weight.
- Test API names, module strings, user input, missing glyphs, and fallback behavior.
- Compare measured bounds with rendered bounds for wrapping, clipping, baseline, alignment, outline, and scaling.
- Inspect release artifacts for `LICENSE.txt`, copyright attribution, derivative naming, font version, and unintended source files.
- Record source font size, atlas page count, compressed package size, decoded GPU memory, cache limits, and device-reset behavior.

## Official Sources

- [Source Han Sans release download guide](https://github.com/adobe-fonts/source-han-sans/tree/release)
- [Taiwan static subset OTFs](https://github.com/adobe-fonts/source-han-sans/tree/release/SubsetOTF/TW)
- [Taiwan subset variable TTF](https://github.com/adobe-fonts/source-han-sans/blob/release/Variable/TTF/Subset/SourceHanSansTW-VF.ttf)
- [Traditional Chinese language-specific variable TTF](https://github.com/adobe-fonts/source-han-sans/blob/release/Variable/TTF/SourceHanSansTC-VF.ttf)
- [Source Han Sans LICENSE](https://github.com/adobe-fonts/source-han-sans/blob/release/LICENSE.txt)
- [SIL Open Font License 1.1](https://openfontlicense.org/open-font-license-official-text/)
