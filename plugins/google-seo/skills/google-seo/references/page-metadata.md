# Page Metadata And Google-Supported Tags

Source: Google Search Central, "`meta` tags and attributes that Google supports"
URL: https://developers.google.com/search/docs/crawling-indexing/special-tags
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Robots `meta` tag, `data-nosnippet`, and `X-Robots-Tag` specifications"
URL: https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
Source page last updated: 2026-03-24 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Block Search indexing with `noindex`"
URL: https://developers.google.com/search/docs/crawling-indexing/block-indexing
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.

Use this reference when auditing or implementing page-level metadata, robots directives, snippet controls, Search Console verification, viewport, SafeSearch labels, or HTML attributes that affect indexing and search appearance.

## Placement And Parsing

- Put Google-relevant metadata in a valid HTML `<head>`.
- Keep search-critical tags before any invalid or non-standard `<head>` markup.
- Google reads HTML and XHTML-style `meta` tags, but unsupported tags are ignored.
- With the exception of `google-site-verification`, `meta` tag letter case is generally not important.
- Avoid injecting or changing SEO-critical `meta` tags with JavaScript when possible; if unavoidable, validate rendered HTML with URL Inspection or a rendered-page test.

## Supported Meta Tags To Check

- `description`: Provides a page summary that Google may use for snippets. The visible page body still needs useful summary text because Google may choose a different snippet.
- `robots`: Applies crawl, indexing, and serving directives to compliant search engines.
- `googlebot`: Applies directives to Google text results. Use `googlebot-news` for Google News-specific behavior.
- `google`: Supports Google-specific values such as `notranslate` and `nopagereadaloud`.
- `google-site-verification`: Verifies Search Console ownership on a top-level page. Match the provided `name` and `content` values exactly, including case.
- `Content-Type` / `charset`: Defines content type and character encoding. Prefer UTF-8 and quote `content` values on `http-equiv` metadata.
- `refresh`: Can redirect users, but prefer server-side `301` or `302` redirects for SEO and user clarity.
- `viewport`: Helps browsers render mobile pages and is a mobile-friendliness signal.
- `rating`: Labels sexually explicit adult content for SafeSearch filtering.

## Robots Directives

- `all`: Default behavior; no indexing or serving restriction.
- `noindex`: Do not show the page, media, or resource in Search results after Google crawls it and sees the directive.
- `nofollow`: Do not follow links on the page for discovery.
- `none`: Equivalent to `noindex, nofollow`.
- `nosnippet`: Do not show a text snippet or video preview. It also prevents the page content from being used as direct input for Google AI Overviews and AI Mode.
- `indexifembedded`: Allow indexing when the page is embedded in another page; only works together with `noindex`.
- `max-snippet:[number]`: Limit text snippet length. `0` is equivalent to `nosnippet`; `-1` lets Google choose.
- `max-image-preview:none|standard|large`: Control image preview size.
- `max-video-preview:[number]`: Limit video preview seconds. `0` permits at most a static image; `-1` means no limit.
- `notranslate`: Do not offer translated title link and snippet.
- `noimageindex`: Do not index images on the page.
- `unavailable_after:[date/time]`: Stop showing the page after a valid date/time.
- Treat `noarchive`, `nocache`, and `nositelinkssearchbox` as obsolete for Google Search.

## Combining Robots Rules

- Combine multiple rules in a comma-separated `content` value or with multiple robots `meta` tags.
- For conflicting rules, assume the most restrictive rule applies.
- For crawler-specific combinations, Googlebot uses the sum of negative rules from generic `robots` and `googlebot` tags.
- `name` and `content` values are case-insensitive for robots directives.
- Google Search can respect robots `meta` tags outside `<head>`, but still prefer valid `<head>` placement for maintainability and consistency.

## Blocking Indexing With Noindex

- Use `<meta name="robots" content="noindex">` in HTML to block indexing for all search engines that support `noindex`.
- Use `<meta name="googlebot" content="noindex">` when the intent is Google-specific web search behavior.
- Use `X-Robots-Tag: noindex` or `X-Robots-Tag: none` for HTTP-level control, especially for PDFs, images, videos, or other non-HTML resources.
- Do not specify `noindex` in `robots.txt`; Google does not support that as an indexing directive.
- Keep the URL crawlable and accessible until Google has seen the `noindex`; if `robots.txt` blocks the URL or the crawler cannot access it, Google may keep the URL in Search based on external links or previous knowledge.
- Expect removal from Search after Google recrawls and processes the directive. Use URL Inspection to request recrawl, and use the supported removals workflow when urgent temporary removal is needed.
- Debug with URL Inspection to verify the HTML or response headers Googlebot received, then monitor Search Console's Page Indexing report for pages where Google extracted `noindex`.

## X-Robots-Tag

- Use `X-Robots-Tag` HTTP headers for non-HTML resources such as PDFs, images, and videos, or for server-level rules across URL patterns.
- Any rule valid in robots `meta` can also be used in `X-Robots-Tag`.
- Multiple `X-Robots-Tag` headers may be sent, or rules may be comma-separated.
- A header may target a user agent, for example `X-Robots-Tag: googlebot: nofollow`; untargeted rules apply to all crawlers.

## Supported Attributes And Snippet Controls

- Use normal `href` and `src` attributes so Google can discover links, images, and other resources.
- Use supported `rel` attributes for qualifying links, such as untrusted, user-generated, or sponsored outbound links.
- Use `data-nosnippet` on `div`, `span`, or `section` to exclude page fragments from snippets when needed.
- Treat `data-nosnippet` as a boolean attribute: any value, including `false`, excludes that element.
- Keep `data-nosnippet` markup valid and properly closed; invalid markup may exclude more text than intended.
- Avoid adding or removing `data-nosnippet` from existing nodes with JavaScript. If JavaScript creates the node, include `data-nosnippet` when initially adding it.
- Verify snippet-related controls in Search Console when the search appearance outcome matters.

## Structured Data Interaction

- Robots snippet limits control automatically extracted previews, but rich result structured data can still be used when it is present and eligible.
- `max-snippet` can limit `article.description` and description values for other creative-work structured data.
- Structured data inside a `data-nosnippet` element can still be used for search results; remove or change structured data itself when it should not be exposed.

## Unsupported Or Obsolete Signals

- Do not optimize `meta name="keywords"`; Google ignores it for indexing and ranking.
- Do not rely on HTML `lang` attributes as Google Search's language signal; Google detects language from visible text.
- Do not rely on `rel="next"` or `rel="prev"` for indexing; Google no longer uses these link values.
- Do not use `meta name="google" content="nositelinkssearchbox"`; the sitelinks search box control is obsolete.

## Audit Notes

- Check both HTML meta tags and HTTP `X-Robots-Tag` headers for robots directives.
- Use `X-Robots-Tag` for non-HTML files when index or snippet control is needed.
- Do not disallow a URL in `robots.txt` when Google must crawl it to see `noindex`, snippet limits, or other robots rules.
- If a noindexed URL remains in Search, check crawlability, last crawl timing, visible rendered metadata, HTTP headers, and Search Console Page Indexing state before changing unrelated SEO signals.
- Keep CMS-generated metadata, canonical links, structured data URLs, sitemap URLs, and rendered metadata aligned.
