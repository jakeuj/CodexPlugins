# Mobile-First Indexing And Mobile Sites

Source: Google Search Central, "Mobile site and mobile-first indexing best practices"
URL: https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.

Use this reference when auditing mobile-first indexing, mobile/desktop parity, dynamic serving, separate mobile URLs such as m-dot sites, mobile rendering, mobile structured data, or Search Console messages about mobile indexing.

## Core Model

- Google uses the mobile version of a site's content, crawled with the smartphone agent, for indexing and ranking.
- A mobile version is not required to be included in Google Search, but it is strongly recommended.
- Prefer responsive design when choosing a mobile setup; it uses the same URL and HTML with different display rules, making content and metadata parity simpler.
- For dynamic serving and separate mobile URLs, audit both desktop and mobile responses because they may serve different HTML, metadata, resources, structured data, or status codes.
- For dynamic serving, verify user-agent handling and the `Vary: User-Agent` response header so crawlers and caches understand that device-specific HTML may be served.

## Mobile Crawl And Render Access

- Let Google access and render mobile page content and resources, including CSS, JavaScript, images, videos, and API responses needed for the page.
- Use equivalent robots `meta` tags on desktop and mobile versions. A mobile-only `noindex` or `nofollow` can prevent indexing or link/image discovery under mobile-first indexing.
- Do not require user actions such as swiping, clicking, or typing to load primary text, images, videos, or links.
- Do not block mobile-only resource URLs in `robots.txt` when those resources are needed for Google to understand or index the page.

## Content And Metadata Parity

- Keep primary mobile content equivalent to desktop content. If mobile intentionally has less content, expect possible traffic loss because Google indexes from the mobile version.
- Mobile layout may use accordions or tabs to save space, as long as the content remains present and accessible.
- Use the same clear, meaningful headings on mobile and desktop.
- Keep page titles and meta descriptions equivalent across desktop and mobile versions.
- Keep structured data present on both versions. If implementation must be prioritized, start with `Breadcrumb`, `Product`, and `VideoObject` where relevant.
- Use correct structured data URLs for the served version; mobile pages with separate URLs should use the corresponding mobile URLs where appropriate.

## Images, Videos, And Ads

- Provide high-quality mobile images in supported formats and supported tags.
- Keep important image URLs stable. If desktop and mobile use different image URLs, expect possible temporary image traffic loss while Google learns the mobile image URLs.
- Use the same descriptive `alt` text, image titles, captions, filenames, and surrounding text quality on mobile and desktop.
- Use stable video URLs, supported video formats, and supported tags such as `video`, `embed`, or `object`.
- Keep video structured data equivalent across desktop and mobile, and place important videos where users can easily find them on mobile.
- Avoid mobile ad placements that crowd out the primary content or create a poor user experience; follow Better Ads standards.

## Separate Mobile URLs

- For m-dot or other separate mobile URLs, keep the desktop URL as canonical and mark the mobile URL as the alternate.

```html
<!-- desktop page -->
<link rel="canonical" href="https://www.example.com/page">
<link rel="alternate" media="only screen and (max-width: 640px)" href="https://m.example.com/page">

<!-- mobile page -->
<link rel="canonical" href="https://www.example.com/page">
```

- Verify both desktop and mobile properties in Search Console so messages and reports are visible for both versions.
- Ensure each distinct desktop page has an equivalent mobile page. Do not redirect many desktop URLs to the same mobile home page or generic mobile URL.
- Avoid URL fragments in separate mobile URLs; fragment URLs are generally not indexable.
- Keep error status behavior equivalent across desktop and mobile versions.
- Make sure mobile hosts have enough capacity for increased crawl rate after mobile-first indexing.
- Use compatible `robots.txt` rules for desktop and mobile hosts.

## Hreflang With Separate URLs

- Keep `hreflang` clusters separated by device URL type: mobile URLs should point to mobile alternate-language URLs, and desktop URLs should point to desktop alternate-language URLs.
- Continue using the desktop canonical pattern alongside device-specific `hreflang` links.

## Troubleshooting Checklist

- Missing structured data on mobile: add equivalent markup and validate rendered mobile pages with URL Inspection or Rich Results Test.
- Mobile-only `noindex` or `nofollow`: align robots meta tags across versions unless exclusion is intentional.
- Missing, blocked, low-quality, unstable, or undescribed mobile images: check image availability, robots rules, formats, dimensions, alt text, and surrounding content.
- Missing mobile titles or descriptions: make mobile metadata equivalent to desktop metadata.
- Mobile URL is an error page or has a fragment: provide an equivalent mobile URL with a crawlable, indexable URL and correct status code.
- Duplicate mobile target or desktop-to-mobile-home redirects: map each desktop URL to its matching mobile URL.
- Mobile page quality issues: check content parity, headings, ad placement, image context, and videos.
- Video issues: verify supported formats/tags, stable URLs, equivalent structured data, and visible placement on mobile.
- Hostload issues: verify mobile host capacity and crawl health in Search Console.
