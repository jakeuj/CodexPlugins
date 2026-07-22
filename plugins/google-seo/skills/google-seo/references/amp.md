# AMP And Google Search

Source: Google Search Central, "AMP on Google Search guidelines"
URL: https://developers.google.com/search/docs/crawling-indexing/amp
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Understand how AMP works in search results"
URL: https://developers.google.com/search/docs/crawling-indexing/amp/about-amp
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Enhance AMP content for Google Search"
URL: https://developers.google.com/search/docs/crawling-indexing/amp/enhance-amp
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Validate AMP content for Google Search"
URL: https://developers.google.com/search/docs/crawling-indexing/amp/validate-amp
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Remove your AMP pages from Google Search"
URL: https://developers.google.com/search/docs/crawling-indexing/amp/remove-amp
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.

Use this reference when auditing AMP pages, AMP/non-AMP canonical pairing, AMP validation, AMP Search Console reports, AMP rich result eligibility, AMP Cache/update issues, or AMP removal.

## Core Decisions

- AMP is not required for Google Search. Treat AMP as a page technology choice; normal Google-friendly site guidelines still apply.
- AMP itself is not a ranking factor; speed is a ranking factor, and Google applies the same standard regardless of page technology.
- AMP pages can appear in mobile rich results and carousels when eligible, but structured data never guarantees rich result display.
- AMP is not mobile-only. Build AMP with responsive design; AMP can display on desktop, but desktop AMP does not get AMP-specific Google Search features.

## Content, URLs, And Validity

- Follow the AMP HTML specification and keep AMP pages valid when they should be eligible for AMP-related Google Search features.
- Users should be able to experience the same content and complete the same actions on AMP pages as on their corresponding canonical pages, where possible.
- Use an AMP URL pattern that clearly belongs to the main site, such as a same-site `/amp/` path or related AMP subdomain. Avoid unrelated domains that confuse users.
- If structured data is present, follow Google's structured data policies and keep equivalent structured data on both canonical and AMP duplicates.

## Discovery And Canonical Pairing

- Make AMP discoverable with explicit page links:

```html
<!-- canonical non-AMP page -->
<link rel="amphtml" href="https://www.example.com/article/amp">

<!-- AMP page -->
<link rel="canonical" href="https://www.example.com/article/">
```

- For canonical AMP setups with a single AMP version, the AMP page can be its own canonical.
- Google Search requires an AMP page to link to a canonical page. The canonical can be the AMP page itself or a non-AMP version.
- Keep the canonical page, AMP page, and structured-data URLs crawlable when they should appear in Search. Check `robots.txt`, robots `meta`, and `X-Robots-Tag` for accidental blocks or `noindex`.
- Align AMP canonical signals with sitemap URLs, internal links, redirects, structured data URLs, and `hreflang` patterns.

## Validation And Monitoring

- Use the AMP Test Tool to confirm AMP validity for Google Search.
- Use the Rich Results Test when AMP pages include structured data for supported rich result features.
- Use the Search Console AMP status report to monitor site-wide AMP template or implementation issues.
- If AMP pages do not appear, check canonical/AMP link pairing, AMP guideline compliance, crawlability, indexing timing, Search feature availability by country, and structured data validity.
- Google may need time to index AMP content. If indexed AMP content must be refreshed immediately in serving, update the Google AMP Cache.

## Serving Notes

- AMP selected from Google Search may be served through the Google AMP Viewer or as a signed exchange where supported.
- Signed exchange can show the publisher's URL and support first-party cookies, analytics, and customization; Google Search prefers signed exchange over the AMP Viewer when supported.
- Desktop AMP pages are not currently served from the Google AMP Cache or AMP Viewer; canonical AMP pages behave like standard Search results.

## Removing AMP

- Decide whether the goal is removing all versions of a page or only the AMP version while keeping the canonical non-AMP page live.
- To remove only a paired AMP page, remove `rel="amphtml"` from the canonical non-AMP page, then redirect the removed AMP URL to the canonical non-AMP URL with `301` or `302`.
- Do not remove AMP by leaving an empty or invalid file. Google may continue serving the oldest valid AMP version it has available.
- To remove all versions quickly, remove both AMP and non-AMP pages, use the appropriate Google removal workflow, update the Google AMP Cache, and monitor Search Console.
- When disabling AMP in a CMS, confirm whether the CMS redirects old AMP URLs to canonical non-AMP pages and watch the indexed AMP page trend in Search Console.
