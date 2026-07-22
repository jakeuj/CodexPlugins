# JavaScript SEO

Source: Google Search Central, "Understand the JavaScript SEO basics"
URL: https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
Source page last updated: 2026-03-04 UTC. Checked from Codex on 2026-06-10.
Additional source: Google Search Central, "Fix Search-related JavaScript problems"
URL: https://developers.google.com/search/docs/crawling-indexing/javascript/fix-search-javascript
Source page last updated: 2025-12-18 UTC. Checked from Codex on 2026-06-12.
Additional source: Google Search Central, "Fix lazy-loaded content"
URL: https://developers.google.com/search/docs/crawling-indexing/javascript/lazy-loading
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.

Use this reference when a site depends on JavaScript rendering, SPA routing, app shell HTML, JavaScript-generated metadata or structured data, web components, or lazy-loaded content.

## Core Model

- Google processes JavaScript pages through crawling, rendering, and indexing.
- Googlebot first fetches the URL and checks `robots.txt`; blocked URLs or blocked JavaScript/CSS will not be rendered in the way the site expects.
- Google extracts links from the initial HTML, may queue a page for rendering, then uses rendered HTML for indexing and more link discovery.
- A `200` page is generally eligible for rendering unless robots meta/header directives say not to index it.
- Server-side rendering or prerendering remains a strong default because it improves speed for users and crawlers, and not every bot runs JavaScript.
- Googlebot and the Web Rendering Service prioritize crawling and may skip requests that do not contribute to essential page content; do not treat client-side analytics as complete evidence of Googlebot rendering behavior.

## Audit Checks

- Compare initial HTML and rendered HTML before concluding that Google can see a page.
- Verify important content, navigation links, title, meta description, canonical, robots directives, and structured data are visible or stable after rendering.
- Confirm JavaScript, CSS, and API resources needed for page content are not blocked by `robots.txt` and are accessible to anonymous users.
- Use Search Console URL Inspection, Rich Results Test, or a browser-rendered view to inspect rendered HTML for final conclusions.
- When debugging a suspected JavaScript indexing problem, inspect rendered DOM, loaded resources, and JavaScript console errors before changing SEO metadata.
- Use Search Console Crawl Stats for Googlebot/WRS activity signals; analytics beacons and error-reporting calls may be skipped or filtered by WRS.
- For lazy-loaded content, verify that important text, images, videos, and links appear in rendered HTML when they enter the viewport.

## Troubleshooting Flow

- Start with Search Console URL Inspection or Rich Results Test for the exact affected URL.
- Compare what the tool renders against the expected user-visible content, links, metadata, structured data, and robots directives.
- Capture JavaScript runtime errors for real users and crawlers when practical, but remember parse errors may not be caught by a global `window.onerror` handler.
- Re-test with the same Google tool after each fix; do not close the issue based only on a local browser test.

## Links And Routing

- Use crawlable HTML links: `<a href="https://example.com/path">` or root-relative equivalents.
- JavaScript may inject links into the DOM, but the resulting links still need normal `href` attributes.
- For SPA routing, use the History API instead of hash fragments for distinct indexable views.
- Treat `/#/products` or `#!/products` routes as suspicious for SEO unless there is a deliberate fallback strategy.

## Browser APIs, State, And Network Assumptions

- Expect Googlebot to decline user permission prompts. Do not require camera, location, notifications, or similar permissions before showing indexable content.
- Do not rely on `localStorage`, `sessionStorage`, or cookies to persist required state across WRS page loads.
- Serve essential content over HTTP(S) fetchable resources. WebSocket or WebRTC-only content needs an HTTP fallback.
- Use feature detection, fallbacks, or polyfills for critical APIs; if an unsupported feature gates content, prefer SSR/prerendering or a simpler accessible fallback.

## Canonical And Metadata

- Prefer canonical tags in initial HTML.
- If JavaScript sets the canonical URL, it must not conflict with the original HTML canonical.
- If canonical cannot be emitted in initial HTML, JavaScript may inject it, but validate rendered HTML.
- JavaScript can set or change title and meta description, but rendered validation is required.

## Status Codes And Soft 404s

- Use meaningful HTTP status codes whenever the server can do so.
- Client-side rendered SPAs can accidentally return `200` for missing content, creating soft 404s.
- For missing SPA content, either redirect to a URL that returns a real `404`, or add `noindex` to the error page.
- Do not include `noindex` in original HTML for pages that should be indexed and expect JavaScript to remove it; Google may skip rendering once it sees `noindex`.
- Treat client-side error views, empty search results, deleted product pages, and failed API responses as soft-404 candidates during audits.

## Caching, Structured Data, And Web Components

- Use content fingerprinting for JavaScript and CSS filenames so Googlebot does not use stale cached assets after deploys.
- Assume WRS may ignore cache headers; filename-level content hashes are safer than relying on short cache lifetimes after deployments.
- JavaScript can generate JSON-LD structured data, but test it with rendered-page tools.
- Google can render web components and flatten shadow/light DOM, but only content visible in rendered HTML is indexable.
- For web components, verify expected content appears in rendered HTML. Components that do not expose light DOM content through slots may hide content from indexing.

## Images And Lazy Loading

- Lazy-load non-critical or initially non-visible content only; avoid lazy-loading content that is likely visible as soon as the page opens.
- Use browser-native lazy loading for images/iframes, IntersectionObserver, or a library that loads data as content enters the viewport.
- Do not require user-only actions such as scrolling, clicking, swiping, or typing before important content loads; Google Search does not interact with the page.
- Validate lazy-loaded text, images, and videos with rendered HTML inspection when discovery matters.
- For images and videos, check that the final rendered `<img>` or `<video>` element has the discoverable URL in `src`.

## Infinite Scroll And Paginated Loading

- Make infinite scroll indexable by supporting paginated loading for each chunk of content.
- Give each chunk a persistent, unique URL whose content is stable across visits.
- Prefer absolute page identifiers such as `?page=12`; avoid relative URLs such as `?date=yesterday` for indexable chunks.
- Link sequentially to individual page URLs so crawlers can discover the full paginated set without performing scroll actions.
- When scrolling makes a new chunk the primary visible content, update the visible URL with the History API so refresh, share, and direct links resolve to the same chunk.

## Paywalls

- JavaScript-only hiding is not a reliable access-control model. If content is gated, only provide the full content after subscription or entitlement is confirmed.
- Keep paywall SEO checks separate from structured data eligibility; visible content, access control, and any paywalled structured data must agree.
