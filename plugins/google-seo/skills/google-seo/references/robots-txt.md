# Robots.txt For Google Crawling

Source: Google Crawling Infrastructure, "How to write and submit a robots.txt file"
URL: https://developers.google.com/crawling/docs/robots-txt/create-robots-txt
Source page last updated: 2025-11-21 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Crawling Infrastructure, "How Google interprets the robots.txt specification"
URL: https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec
Source page last updated: 2026-04-14 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Crawling Infrastructure, "Update your robots.txt file"
URL: https://developers.google.com/crawling/docs/robots-txt/submit-updated-robots-txt
Source page last updated: 2025-11-21 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Crawling Infrastructure, "Useful robots.txt rules"
URL: https://developers.google.com/crawling/docs/robots-txt/useful-robots-txt-rules
Source page last updated: 2026-03-27 UTC. Checked from Codex on 2026-06-12.

Use this reference when creating, auditing, updating, or troubleshooting `robots.txt`, crawl blocking, `Allow`/`Disallow` rules, user-agent matching, `Sitemap` lines, robots.txt caching, Search Console robots.txt report behavior, or useful crawl-control rule patterns.

## What Robots.txt Controls

- Use `robots.txt` to control which URLs crawlers may fetch. It controls crawling, not indexing, ranking, access control, or privacy.
- If there is no `robots.txt`, or no matching blocking rule, crawling is allowed by default.
- URLs blocked by `robots.txt` can still be indexed from external signals, usually without indexed page content or a snippet.
- Do not use `robots.txt` when the goal is removing a URL from Search results; use crawlable `noindex`, authentication, deletion with an appropriate status code, or Google's removal tools.
- Do not rely on `robots.txt` for private content. The file is public and may reveal sensitive paths; use authentication or authorization instead.
- Do not block CSS, JavaScript, image, video, or API resources Google needs to render and understand pages that should be indexed.

## File Location And Format

- Put one file named `robots.txt` at the root of the site host it controls, for example `https://www.example.com/robots.txt`.
- Rules apply only to the same protocol, host, and port where the file is served. Subdomains, alternate protocols, and non-standard ports need their own files.
- `robots.txt` files in subdirectories are not valid crawl-control files.
- Use UTF-8 plain text. Avoid word processors that may add proprietary formatting or unexpected characters.
- Google ignores invalid lines and content after the 500 KiB file-size limit.
- `Sitemap:` values must be fully qualified URLs. Multiple `Sitemap:` lines are allowed, and sitemap URLs do not need to be on the same host as the robots.txt file.

## Supported Fields

- Google supports `User-agent`, `Allow`, `Disallow`, and `Sitemap`.
- Other fields such as `crawl-delay` are ignored by Google.
- Field names are case-insensitive, but `Allow` and `Disallow` path values are case-sensitive.
- A group begins with one or more `User-agent` lines and contains `Allow` or `Disallow` rules.
- The `*` user agent matches most crawlers, but various AdsBot crawlers must be named explicitly when they need rules.
- `Sitemap` is not part of a user-agent group; it may be followed by any crawler that supports sitemaps.

## Matching And Precedence

- Path values are relative to the root of the same protocol, host, and port, and must start with `/`.
- Google supports `*` as a wildcard for zero or more valid characters and `$` for the end of the URL.
- A trailing `*` is usually redundant: `/fish*` is equivalent to `/fish`.
- Directory blocks should end with `/`, for example `Disallow: /calendar/`; without the slash, a rule may also match URLs such as `/calendar.html`.
- Matching is case-sensitive.
- For a crawler, Google uses the most specific matching user-agent group. Specific user-agent groups and the global `*` group are not combined.
- If the same specific user agent appears in multiple groups, Google combines those specific groups internally.
- For URL rules, the longest matching path wins. If conflicting rules are equally specific, Google uses the least restrictive rule.

## Status Codes, Redirects, And Cache

- `2xx`: Google processes the robots.txt content.
- `3xx`: Google follows at least five redirect hops, then treats unresolved redirect chains as no robots.txt restrictions.
- `4xx`, except `429`: Google treats the site as if no valid robots.txt file exists, so there are no crawl restrictions.
- `429` and `5xx`: treat as crawl-risk conditions. Google may stop crawling temporarily, use a cached good version, and keep retrying.
- DNS, network, timeout, invalid response, reset, interrupted connection, and chunking errors are treated like server errors.
- Google generally caches robots.txt for up to 24 hours, but cache duration may be longer when refresh is not possible. `Cache-Control: max-age` may affect cache lifetime.
- After updating robots.txt, Google will normally discover changes automatically; use Search Console's robots.txt report Request a recrawl function only when the cache needs faster refresh.

## Testing And Update Workflow

1. Fetch the live file, for example `curl https://example.com/robots.txt -o robots.txt`.
2. Edit in a plain text editor and keep UTF-8 encoding.
3. Upload the file to the root of the correct protocol/host/port.
4. Verify in a private browser window or with `curl` that the public URL returns the expected text and status code.
5. Use Search Console's robots.txt report for accessible live files, or Google's open source robots.txt library for local parser testing.
6. If the site is hosted by a CMS or site builder, use the platform's search visibility controls when direct root-file access is unavailable.

## Useful Rule Patterns

```txt
# Allow all crawlers; equivalent to no robots.txt for crawl control.
User-agent: *
Disallow:

# Block the entire site from crawling.
User-agent: *
Disallow: /

# Block a directory and its contents.
User-agent: *
Disallow: /calendar/

# Block all crawling except a public directory.
User-agent: *
Disallow: /
Allow: /public/

# Block a file type for Googlebot.
User-agent: Googlebot
Disallow: /*.gif$

# Block all images from Google image surfaces.
User-agent: Googlebot-Image
Disallow: /

Sitemap: https://www.example.com/sitemap.xml
```

## Audit Notes

- Treat accidental `Disallow: /` as a blocker.
- Check both root robots files when `www`/apex, HTTP/HTTPS, m-dot, CDN, staging, or non-standard ports exist.
- Check whether blocked resources are required for rendering, lazy loading, structured data generation, images, or videos.
- If robots.txt changes do not appear to work, check the live response status, redirects, cache timing, Search Console robots.txt report, and whether the URL is under the same protocol/host/port as the robots file.
- If a blocked URL still appears in Search, remember that blocking crawl prevents Google from seeing page-level `noindex`; use the correct removal or deindexing mechanism.
