# Pathing Route-Pack Localization

## Separate the Three Layers

- Module UI: localize Pathing's menus, settings, and status text through `.resx` resources and satellite assemblies.
- Route-pack content: localize category names and marker text stored in marker-pack XML.
- Marker Pack Repo metadata: localize the download catalog's name, description, and categories through its JSON schema and UI resolver.

Do not treat a localized Blish HUD or Pathing module as proof that route-pack content is localized. Diagnose and release each layer independently.

## Confirm the Active Implementation

Before designing a change, inspect the checked-out versions rather than relying on these landmarks blindly:

- `PackInitiator`: creates `PackReaderSettings`, registers the `bh-` vendor prefix, calls `LoadMapAsync`, and finalizes the shared collection.
- TmfLib `Pack.LoadAllAsync` and `LoadMapAsync`: determine which XML files are loaded.
- TmfLib `PathableCategoryBuilder` and attribute collections: determine whether unknown attributes survive parsing and inheritance.
- Pathing `StandardMarker` partials: consume `tip-name`, `tip-description`, `text`, `title`, `info`, and `copy-message`.
- TmfLib `PackWriter`: determines whether optimization preserves explicit attributes and arbitrary catalog files.
- `MarkerPackPkg`: models remote repo metadata separately from archive content.

In the Pathing 1.13.1-era design, no locale is passed to `LoadMapAsync`; every matching XML in an archive is loaded. Category and marker consumers resolve one base value, and Marker Pack Repo metadata uses single strings. A localized module fork changes UI resources but does not create a route-pack localization contract.

### Evidence to Recheck in a Local Checkout

In Pathing `1.13.1`, verify these points before claiming current behavior:

- `PackInitiator.cs`: registers `bh-` and calls `Pack.LoadMapAsync(mapId, sharedCollection, readerSettings)` without a locale argument.
- `UI/Controls/NodeTree/PathingCategoryNode.cs`: constructs category UI from one `PathingCategory.DisplayName` value.
- `manifest.json`: identifies the checked module version; do not infer behavior from a different release.

Together these show that adding an English and a zh-TW copy of the same routes to one archive is not automatic localization. Both sets can load; duplicate POIs, duplicate categories, manual toggles, or last-write behavior are possible. Treat that outcome as a compatibility risk until tested against the active TmfLib version.

## Choose the Delivery Strategy

Use separate locale archives for an immediate compatible release:

```text
source XML + translation catalog
  -> pack.en.taco
  -> pack.zh-Hant.taco
```

- Generate archives from one structural source instead of maintaining complete XML copies manually.
- Preserve GUIDs, category namespaces, coordinates, map IDs, trail data, and asset paths across builds.
- Translate category `DisplayName` and user-facing marker fields only.
- Publish each archive as a distinct package entry and enable only one locale.
- Test both Pathing and TacO when compatibility is claimed.

Do not put `route.en.xml` and `route.zh-Hant.xml` in one archive expecting automatic selection. Current loaders may load both, producing duplicate POIs, conflicting categories, or last-write behavior. Separate in-archive namespaces are acceptable only when the user intentionally chooses language categories and the duplication cost is documented.

## Collaborate with a Rights Holder

When a pack author offers a contributor role or proposes a `zh-TW` category:

1. Explain that a category is not a runtime language selector in current Pathing. Do not duplicate full marker trees in one archive as a localization mechanism.
2. Prefer one structural source plus a translation catalog, with the author publishing a single-language `zh-Hant`/`zh-TW` branch or release asset. Use PRs for the text-only changes.
3. Keep contributor access, upstream publishing, and legal permission separate. A repository invitation enables collaboration; it does not establish authority over third-party assets or authorize an independent fork/release.
4. Before publishing outside the author-controlled release path, obtain durable evidence covering translation and public redistribution, exact version scope, attribution, and third-party exclusions.
5. If automatic in-pack language selection is still desired, open a Pathing design issue first. It needs a module and likely TmfLib contract; it cannot be implemented safely by a route-pack-only PR.

Use this concise reply when appropriate, adapting it to the author and pack:

> I can help maintain a Traditional Chinese variant upstream. Current Pathing does not select route-pack text by UI language, so duplicating the English and zh-TW marker trees in one package would load both instead of switching automatically. I suggest an author-owned `zh-TW` branch or release asset containing one complete language variant, with translation updates contributed through PRs. Before publishing any separate archive, we should also confirm the applicable license or permission and any third-party exclusions.

## Design a Single-Archive Pathing Extension

Open a design issue before establishing a public format contract. For the first implementation, prefer localized vendor attributes that retain a neutral or English base value:

```xml
<MarkerCategory
  name="route"
  DisplayName="Route"
  bh-displayname-zh-Hant="路線" />

<POI
  info="Turn left at the bridge."
  bh-info-zh-Hant="在橋邊左轉。"
  tip-name="Next stop"
  bh-tip-name-zh-Hant="下一站" />
```

Treat the spelling above as a proposal until maintainers approve it. Normalize base-attribute matching case-insensitively, canonicalize locale tags, and retain base values so readers that ignore `bh-` extensions still have usable text.

Account for TmfLib name normalization: when `bh-` is registered as a vendor prefix, `NanoXmlBase.CleanName` strips that prefix and lowercases the remaining attribute name. For example, the in-memory name may be `tip-name-zh-hant`, not the original XML spelling. Match against a known base-field list and canonicalized locale candidates; do not split only on the final `-`, because both base names and BCP 47 tags contain hyphens. Reconfirm this behavior against the active TmfLib version before implementation.

Resolve locales in a documented order, for example:

```text
zh-TW -> zh-Hant -> zh -> base value
en-US -> en -> base value
```

Implement script aliases such as `zh-TW` to `zh-Hant` explicitly; do not assume the host's enum or `CultureInfo` hierarchy represents the desired script on every target runtime.

Initially limit localization to text-bearing fields: category `DisplayName`; marker `tip-name`, `tip-description`, `text`, `title`, `info`, and `copy-message`. Treat `copy` as opt-in because packs often use it for waypoints or commands rather than prose. Do not localize operational attributes, identifiers, texture paths, GUIDs, or coordinates.

Apply selected localized values after all pack `LoadMapAsync` calls and before Pathing creates runtime entities from the shared collection. Resolve inherited category attributes before promoting a localized value. Subscribe to the host locale-change event, but also provide an explicit pack-language setting with `Auto`, `zh-Hant`, `zh-Hans`, and BCP 47 values. Queue a pending reload if a language change arrives while packs are loading; a reload method that returns early during `IsLoading` can otherwise lose the change.

Prefer attributes for the first version because existing readers can ignore the vendor extension and the optimizer can preserve explicit attributes. Add `i18n/*.json`, PO, or XLIFF catalogs only after Pathing and TmfLib/PackWriter explicitly preserve, load, and validate arbitrary localization resources.

## Keep Repo Metadata Separate

The archive filename or `MarkerPackPkg.Name` may be what Pathing shows in pack-management UI. Localizing in-pack `DisplayName` does not localize the download card. Add localized name, description, and category dictionaries to the repo schema and update display, search, fallback, caching, and backward compatibility in a separate change.

## Verify and Report

- Test exact locale, script alias, parent language, missing translation, and base fallback.
- Test inherited category text and marker-level overrides.
- Compare locale builds to ensure only intended text and package metadata differ.
- Optimize and reopen the archive; verify localized attributes and assets survive.
- Switch language before, during, and after pack loading; verify the final state uses the latest choice.
- Verify unchanged GUIDs and namespaces preserve category toggles and user state.
- Report separately what works today, what requires a Pathing PR, what requires TmfLib changes, and what requires Marker Pack Repo coordination.
