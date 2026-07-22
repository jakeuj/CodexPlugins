# Technical SEO Maintenance

Source: Google Search Central, "Maintaining your website's SEO"
URL: https://developers.google.com/search/docs/fundamentals/get-started
Source page last updated: 2025-12-18 UTC. Checked from Codex on 2026-06-10.

Use this reference when maintaining an existing site, planning migrations, troubleshooting crawl/index problems, or reviewing technical SEO beyond first-pass starter checks.

## Crawl And Index Control

- Understand Google's crawl, index, and serving pipeline before debugging Search behavior.
- Make pages and resources Google should crawl accessible to anonymous users.
- Do not block important CSS, JavaScript, image, or API resources needed to understand a page.
- For mobile-first indexing, audit the mobile response and mobile resources because Google commonly indexes and ranks from the smartphone-crawled version.
- Use URL Inspection rendered view when blocked resources or JavaScript rendering may affect how Google sees a page.
- Use `robots.txt` to prevent crawling; read `robots-txt.md` for syntax, protocol/host/port scope, cache behavior, and rule precedence. Do not use it as the primary tool to prevent indexing.
- Use `noindex`, authentication, or supported removal workflows when the actual goal is exclusion from Search.
- Keep URLs crawlable when Google must discover page-level robots meta or `X-Robots-Tag` rules; `robots.txt` disallow can prevent Google from seeing those directives.
- If a `noindex` page remains in results, verify Google has recrawled the URL, can access the URL, and received the expected HTML meta tag or `X-Robots-Tag`; use URL Inspection recrawl requests and the Page Indexing report for confirmation.

## Sitemaps

- Use sitemaps to signal important URLs and metadata such as update frequency.
- Sitemaps help discovery and prioritization; they do not force Google to crawl only listed URLs.
- For large or rapidly changing sites, keep the most important and recently updated URLs represented in sitemaps.
- Align sitemap URLs with canonical URLs, redirects, internal links, and Search Console submissions.

## Duplicate Content And Canonical Pages

- Understand which page should be canonical before changing redirects, canonical tags, sitemap URLs, or internal links.
- Duplicate content is mainly a crawl/index clarity and user-experience problem; fix the canonical signal rather than treating every duplicate URL as a penalty.
- Keep canonical signals consistent across HTML, HTTP redirects, internal links, sitemap URLs, and structured metadata.
- For paired AMP/non-AMP pages, keep the canonical page's `rel="amphtml"` and the AMP page's `rel="canonical"` aligned with the intended canonical URL; read `amp.md` before changing AMP templates or removing AMP.

## International, Pagination, And Infinite Scroll

- For multilingual or multi-regional sites, use `hreflang` where appropriate and verify localized URLs are crawlable.
- Multi-page content needs prominent crawlable next/previous navigation for users and crawlers.
- Infinite scroll should provide a paginated or otherwise crawlable path to content that must be indexed.

## Migrations

- For permanent URL moves, use `301`; for temporary moves, use `302`.
- Removed pages should return a real `404` or other appropriate status, not a soft 404.
- Site migrations need redirects, sitemap updates, and the relevant Search Console migration workflow.
- Monitor indexing, crawl errors, and traffic after migration; do not judge success from the first crawl only.
- When removing only AMP versions, remove `rel="amphtml"` from canonical non-AMP pages and redirect old AMP URLs to the canonical non-AMP URLs; do not leave empty invalid AMP documents.

## Links, Crawl Budget, And Protected Actions

- Keep important links crawlable.
- Use `rel="sponsored"` for paid or affiliate outbound links, `rel="ugc"` for user-generated outbound links, and `rel="nofollow"` for other untrusted outbound links when appropriate.
- Do not use outbound-link `rel` attributes as a substitute for internal crawl control or deindexing; use `robots.txt` to prevent fetching and crawlable `noindex` to prevent indexing.
- For very large sites, prioritize important and recently updated URLs in sitemaps.
- Block URLs that change state, such as comment posting, account creation, or cart actions.
- In `robots.txt`, confirm state-changing URL blocks do not also block CSS, JavaScript, image, or API resources required to render indexable pages.

## User Experience And Search Appearance

- Use HTTPS.
- Keep pages mobile-friendly; read `mobile-first-indexing.md` when desktop and mobile HTML, URLs, metadata, structured data, media, or status codes can differ.
- Monitor Core Web Vitals and PageSpeed Insights when performance is part of the issue.
- Use structured data only when it matches visible page content and a supported feature.
- Manage titles, snippets, favicons, dates, and snippet controls through supported Google mechanisms.
- Use Search Console reports to monitor ongoing performance and indexing health.
