# Google SEO Starter Checklist

Source: Google Search Central, "Search Engine Optimization (SEO) Starter Guide"
URL: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-10.
Additional source: Google Search Central, "Use valid HTML to specify page metadata"
URL: https://developers.google.com/search/docs/crawling-indexing/valid-page-metadata
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.

This is a concise, paraphrased working checklist. Re-open the official page for exact current wording, linked subguides, and any recently changed recommendations.

Related references in this skill:

- `helpful-content.md`: people-first content, E-E-A-T, YMYL, content freshness, AI/automation disclosure, "who/how/why" transparency.
- `robots-txt.md`: robots.txt creation, syntax, crawl blocking, user-agent matching, caching, useful rule patterns.
- `page-metadata.md`: Google-supported meta tags, robots/googlebot directives, snippet controls, unsupported metadata.
- `links-and-outbound.md`: outbound link qualification, paid/affiliate links, user-generated links, `nofollow`, `sponsored`, `ugc`.
- `amp.md`: AMP guidelines, canonical/AMP pairing, validation, Search Console monitoring, AMP removal.
- `mobile-first-indexing.md`: mobile-first indexing, mobile/desktop parity, dynamic serving, separate mobile URLs.
- `javascript-seo.md`: JavaScript rendering, SPA routes, app shell pages, lazy loading.
- `generative-ai-search.md`: AI Overviews, AI Mode, generative AI search visibility.
- `technical-seo-maintenance.md`: site maintenance, migrations, resources, crawl/index strategy.

## Audit Order

1. Confirm Google can discover and access the site.
2. Confirm important pages are indexable and expose the same useful content to Googlebot that users see.
3. Confirm the intended canonical URL for each important page.
4. Improve titles, descriptions, headings, images, and internal links for users first.
5. Improve content quality and search appearance eligibility.
6. Monitor with Search Console and iterate over weeks, not minutes.

## Discovery And Indexing

- Check whether Google already knows the site with a `site:` query, then verify important pages through Search Console when available.
- Make important content discoverable through normal links. A sitemap helps discovery but does not replace a crawlable site structure.
- Submit a sitemap for important URLs when the site is new, large, frequently updated, or has pages that are hard to discover through links.
- Make CSS, JavaScript, images, and other resources needed to understand the page accessible to Googlebot.
- If content varies by region, remember Google generally crawls from a US location; verify the crawler view is acceptable.
- For mobile-first indexing, verify that the mobile version exposes equivalent primary content, metadata, headings, structured data, images, videos, and crawlable resources.
- Use the Search Console URL Inspection Tool for live-page indexing diagnostics.

## Robots, Noindex, And Removals

- Use `robots.txt` to control crawling, not as the primary mechanism for removing an already-known URL from search results.
- Read `robots-txt.md` before changing crawl-blocking rules; robots.txt scope is protocol/host/port-specific and syntax conflicts can have site-wide effects.
- Use page-level `noindex` or supported removal workflows when the goal is excluding content from Google Search.
- Check `X-Robots-Tag` headers as well as HTML robots meta tags.
- Do not block resources needed for Google to render or understand the page.

## URL Structure And Canonicalization

- Prefer descriptive, human-readable URLs over opaque IDs when choosing new URLs.
- For large sites, group topically similar pages in directories so users and crawlers can understand structure.
- Reduce duplicate content where it creates confusing user experiences or wastes crawl effort.
- Choose one canonical URL for duplicate or near-duplicate content; align redirects, canonical tags, sitemap URLs, internal links, OG/Schema URLs, and Search Console submissions.
- Do not overvalue keywords in the domain name or URL path; choose names that make sense for users and the business.

## Site Organization And Links

- Use clear navigation so users and crawlers can reach important pages.
- Link contextually between related pages.
- Write anchor text that describes the destination. Avoid vague anchors when a descriptive phrase would help users.
- For outbound links, qualify paid or affiliate links with `rel="sponsored"`, user-generated links with `rel="ugc"`, and otherwise use `rel="nofollow"` only when the site should not be associated with or followed through that link.

## Titles And Snippets

- Keep search-critical metadata inside a valid HTML `<head>`.
- In `<head>`, use only valid elements: `title`, `meta`, `link`, `script`, `style`, `base`, `noscript`, and `template`.
- Treat invalid `<head>` children such as `img` or `iframe` as high-risk: Google may ignore any later metadata in the same `<head>`.
- Place title, robots directives, canonical links, hreflang links, meta description, and structured data before any unavoidable non-standard markup.
- Write a unique, clear, concise, accurate title for each important page.
- A page title can include the site or business name and other useful context when it helps users.
- Write a short, unique page-level meta description that summarizes the page's most relevant points.
- Google may generate snippets from visible page content instead of the meta description, so the page body itself must contain useful summary text.

## Images And Videos

- Use high-quality images near text that explains their relevance.
- Add concise, descriptive `alt` text that explains the image's relationship to the page content.
- Make image URLs crawlable.
- For video-focused pages, use high-quality video, place it on a relevant standalone page, and provide descriptive titles and descriptions.

## Content Quality

- Create helpful, reliable, people-first content.
- Read `helpful-content.md` when the work requires a page-level content quality audit, E-E-A-T/YMYL judgment, content refresh recommendation, or AI/automation transparency decision.
- Make content easy to read and navigate.
- Keep important pages unique enough that users can tell why each page exists.
- Update content when accuracy or usefulness depends on freshness.
- Promote content through appropriate channels, but avoid manipulative or spammy promotion.

## Things Not To Optimize For

- Meta keywords: Google Search does not use the keywords meta tag.
- Keyword stuffing: excessive repetition harms users and can violate spam policies.
- Arbitrary content length: there is no magic minimum or maximum word count.
- Duplicate content panic: duplicate accessible URLs are inefficient and confusing, but not automatically a manual action.
- Heading count/order as a ranking trick: semantic headings help accessibility and readability; do not treat heading order or count as a magic SEO lever.
- E-E-A-T as a direct ranking factor: use it as a quality lens, not as a mechanical field to optimize.

## Useful Official Follow-Ups

- Search Essentials: https://developers.google.com/search/docs/essentials
- Search Console getting started: https://support.google.com/webmasters/answer/9128668
- Sitemaps: https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview
- Robots.txt: https://developers.google.com/crawling/docs/robots-txt/create-robots-txt
- Meta tags Google supports: https://developers.google.com/search/docs/crawling-indexing/special-tags
- Valid page metadata: https://developers.google.com/search/docs/crawling-indexing/valid-page-metadata
- Canonicalization: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- AMP on Google Search: https://developers.google.com/search/docs/crawling-indexing/amp
- Mobile-first indexing: https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing
- Title links: https://developers.google.com/search/docs/appearance/title-link
- Snippets and meta descriptions: https://developers.google.com/search/docs/appearance/snippet
- Images: https://developers.google.com/search/docs/appearance/google-images
- Structured data gallery: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
