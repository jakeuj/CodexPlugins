---
name: google-seo
description: Use for Google Search SEO audits, SEO implementation reviews, Search Console-oriented troubleshooting, crawl/indexing checks, sitemap/robots.txt/canonical/AMP/mobile-first indexing/meta description/title/image/link/content quality reviews, helpful content and people-first content reviews, E-E-A-T/YMYL quality checks, JavaScript SEO for SPA/app shell/rendered HTML issues, AI Overviews/AI Mode/generative AI search guidance, technical SEO maintenance, site migration, and planning website changes based on Google Search Central guidance. Trigger when the user asks to inspect or improve a site's SEO, Google visibility, indexing, snippets, search appearance, content quality, helpful content, people-first content, E-E-A-T, YMYL, robots.txt rules, crawl blocking, AMP pages, mobile sites, mobile-first indexing, JavaScript rendering, AI search visibility, or references Google Search Central SEO docs.
---

# Google SEO

Use this skill to audit or improve websites against Google Search Central guidance. Prefer official Google Search Central documentation for current details, and browse official Google sources when the user asks for latest guidance, Search Console behavior, ranking/search appearance details, generative AI search, JavaScript SEO, or a specific Google doc URL.

## Workflow

1. Define the target:
   - Identify live URLs, repo/build artifacts, CMS settings, and whether Search Console access is available.
   - If only public access is available, inspect status codes, rendered HTML, `robots.txt`, sitemap, canonical signals, titles, descriptions, headings, images, links, and structured data.
2. Prioritize blockers first:
   - Crawl/index blockers: DNS/TLS failures, 4xx/5xx, blocked resources, accidental `noindex`, bad robots rules, redirect loops, broken canonical targets.
   - Discovery: internal links, sitemap availability, Search Console sitemap submission, important pages omitted from navigation or sitemap.
   - URL identity: duplicate URLs, inconsistent canonical URL, `www`/apex/http/https conflicts, old sitemap URLs, redirect strategy.
3. If the site depends on JavaScript, compare initial HTML with rendered HTML:
   - Look for app shell pages where the HTTP response lacks the indexable body content.
   - Check crawlable links, canonical stability, real HTTP status handling, lazy-loaded content, and whether important resources are blocked.
   - Prefer Browser/rendered-page validation or Search Console URL Inspection for final JavaScript conclusions.
4. Review search appearance:
   - Unique, accurate page titles.
   - Useful page-level `meta name="description"`; remember Google may choose snippets from page content instead.
   - Images near relevant text, descriptive `alt`, crawlable image URLs, appropriate social preview images when the platform needs them.
   - Structured data only when it accurately represents visible page content and matches a supported feature.
5. Review content and site organization:
   - Helpful, reliable, people-first content that satisfies the page's intent.
   - Content that shows useful originality, depth, evidence, experience, and a clear reason to exist for a specific audience.
   - Warning signs of search-engine-first content, such as thin aggregation, mass production without care, fake freshness, arbitrary word-count targeting, or writing outside the site's real audience only for traffic.
   - Descriptive URLs and sensible grouping for large sites.
   - Clear navigation and contextual internal links with meaningful anchor text.
   - Duplicate content handled by choosing one canonical URL where needed.
6. Report in priority order:
   - `Blocker`: prevents crawling, indexing, or serving the intended canonical page.
   - `High`: causes wrong URL identity, weak discovery, missing page-level metadata, or poor snippets on important pages.
   - `Medium`: improves clarity, image/video discovery, internal linking, structured data eligibility, or long-term maintainability.
   - `Low`: optional enhancements that should not distract from content quality and crawlability.

## Use The Reference

Read `references/seo-starter-checklist.md` when doing an audit, writing an SEO fix plan, or deciding whether a proposed change aligns with Google's starter guidance.

Read `references/helpful-content.md` when auditing content quality, people-first content, E-E-A-T, YMYL pages, content refreshes, traffic drops that may involve content usefulness, AI/automation disclosure, thin aggregation, fake freshness, or "who/how/why" content transparency.

Read `references/robots-txt.md` when creating, auditing, updating, or troubleshooting `robots.txt`, crawl blocking, robots syntax, `Allow`/`Disallow`, user-agent matching, `Sitemap` lines in robots.txt, robots.txt caching, Search Console robots.txt report behavior, or useful crawl-control rule patterns.

Read `references/page-metadata.md` when auditing or implementing Google-supported `meta` tags, robots/googlebot directives, `X-Robots-Tag`, meta descriptions, viewport, Search Console verification, snippet controls such as `data-nosnippet`, or unsupported metadata such as meta keywords.

Read `references/links-and-outbound.md` when auditing outbound links, paid or affiliate links, user-generated links, untrusted external links, anchor qualification, or deciding whether `rel="sponsored"`, `rel="ugc"`, or `rel="nofollow"` is appropriate.

Read `references/amp.md` when auditing or implementing AMP pages, AMP/non-AMP canonical pairing, AMP validation, AMP rich result eligibility, AMP Cache/update issues, AMP Search Console monitoring, or AMP removal.

Read `references/mobile-first-indexing.md` when auditing mobile-first indexing, mobile/desktop content parity, dynamic serving, separate mobile URLs such as m-dot sites, mobile metadata/structured-data/media parity, mobile crawl/render access, or mobile Search Console messages.

Read `references/javascript-seo.md` when a site uses client-side rendering, SPA routes, app shell HTML, JavaScript-generated links/metadata/structured data, web components, lazy loading, or when initial HTML and rendered HTML may differ.

Read `references/generative-ai-search.md` when the user asks about AI Overviews, AI Mode, generative AI search visibility, "AEO", "GEO", agentic experiences, or whether AI-specific optimization changes SEO priorities.

Read `references/technical-seo-maintenance.md` when the work involves technical SEO maintenance, resources blocked by robots, sitemap strategy, `hreflang`, migrations, crawl budget, infinite scroll, HTTPS/mobile/page experience, or Search Console monitoring.

Use the plugin-relative `skills/google-seo/scripts/basic_seo_probe.py` for quick public URL checks. Resolve `<plugin-root>` as the directory that contains `.codex-plugin/plugin.json`, then run:

```bash
python3 <plugin-root>/skills/google-seo/scripts/basic_seo_probe.py https://example.com/ https://example.com/article
```

The script is a first-pass, non-rendered HTML probe only. It does not replace Search Console URL Inspection, Browser/rendered-page testing, structured data validation, log analysis, or manual content review.

## Guardrails

- Do not promise rankings or timelines. Google explicitly frames SEO as helping search engines understand content and users decide whether to visit.
- Do not chase myths: avoid meta keywords, keyword stuffing, arbitrary word counts, domain-keyword tricks, and cosmetic heading-count rules.
- Do not recommend mass publishing, mass pruning, date-only refreshes, or content automation as ranking shortcuts; evaluate whether each page helps a real audience.
- Do not treat AI-generated or AI-assisted content as automatically bad; evaluate usefulness, accuracy, purpose, and whether disclosure of automation would help users.
- Do not sell "AEO/GEO hacks" as a separate shortcut for Google generative AI search; apply sound SEO, useful content, and accessible technical foundations.
- Do not add structured data that is not supported, not accurate, or not visible to users.
- Do not block pages in `robots.txt` when the actual goal is removing them from search results; choose the appropriate Google-supported removal/noindex mechanism.
- Treat social metadata as adjacent to SEO: useful for sharing previews, but separate from Google's snippet generation.
