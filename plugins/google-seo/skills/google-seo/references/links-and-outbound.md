# Links And Outbound Qualification

Source: Google Search Central, "Qualify your outbound links to Google"
URL: https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links
Source page last updated: 2025-12-10 UTC. Checked from Codex on 2026-06-12.

Use this reference when auditing outbound links, paid links, affiliate or sponsored placements, user-generated links, untrusted external links, or whether `nofollow`, `sponsored`, or `ugc` is appropriate.

## Crawlable Link Baseline

- Use normal crawlable `<a href="...">` links for links that Google should discover and parse.
- Regular editorial links do not need a `rel` attribute.
- Anchor text should describe the destination for users first.
- These `rel` values apply to crawlable `<a>` elements. `nofollow` can also appear as a robots directive, but that is a page-level crawling/indexing signal.

## Outbound Link Relationship Values

- Use `rel="sponsored"` for advertisements, paid placements, affiliate links, or other compensated links. `nofollow` is still acceptable for paid links, but `sponsored` is the clearer signal.
- Use `rel="ugc"` for user-generated content links, such as comments, forum posts, profiles, and community submissions.
- Consider removing `ugc` only for trusted contributors with a consistent history of high-quality contributions.
- Use `rel="nofollow"` when `sponsored` or `ugc` does not fit and the site owner would rather Google not associate the site with the linked page or crawl it from that link.
- Combine values when needed, such as `rel="ugc nofollow"` or `rel="sponsored nofollow"`.

## Important Limits

- Links marked with `nofollow`, `sponsored`, or `ugc` generally are not followed from that link, but the target URL may still be discovered through sitemaps, internal links, or links from other sites.
- Do not use outbound-link `rel` attributes to control crawling of URLs on the same site. Use `robots.txt` disallow when the goal is to prevent fetching an internal URL.
- Do not use `nofollow` to prevent indexing of a URL. Allow crawling and use `noindex` when the goal is to keep a page out of Search results.
- Avoid blanket `nofollow` on all outbound links when some are normal editorial citations; qualify only the relationship that needs qualification.

## Audit Notes

- Check templates, CMS plugins, comment systems, affiliate modules, ad widgets, author bios, and imported content for missing or excessive `rel` values.
- Treat unqualified paid links as a high-risk issue because they can look like attempts to pass ranking credit.
- Treat missing `ugc` on open user-submitted links as a spam-risk issue, especially on forums, comments, profile pages, and guestbook-style features.
