#!/usr/bin/env python3
"""Basic public SEO probe for a small list of URLs.

This intentionally uses only the Python standard library. It is a first-pass,
non-rendered HTML check for common crawl/index/search appearance signals.
Use rendered-page tooling for JavaScript SEO conclusions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Iterable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


class HeadParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.in_title = False
        self.ignore_depth = 0
        self.h1_count = 0
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.script_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        if tag == "title":
            self.in_title = True
            self.ignore_depth += 1
        elif tag in {"script", "style", "noscript", "template", "svg"}:
            self.ignore_depth += 1
            if tag == "script":
                self.script_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "a":
            self.anchors.append(values)
        elif tag == "img":
            self.images.append(values)

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        elif self.ignore_depth == 0:
            text = " ".join(data.split())
            if text:
                self.text_parts.append(text)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
            self.ignore_depth = max(0, self.ignore_depth - 1)
        elif tag in {"script", "style", "noscript", "template", "svg"}:
            self.ignore_depth = max(0, self.ignore_depth - 1)

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())

    @property
    def body_text(self) -> str:
        return " ".join(self.text_parts)

    def meta_content(self, key: str, value: str) -> str:
        for item in self.meta:
            if item.get(key) == value:
                return item.get("content", "")
        return ""

    def canonical(self) -> str:
        for item in self.links:
            rel = item.get("rel", "").lower().split()
            if "canonical" in rel:
                return item.get("href", "")
        return ""


def fetch(url: str, timeout: int) -> tuple[int | str, str, dict[str, str], bytes]:
    request = Request(url, headers={"User-Agent": "CodexGoogleSeoProbe/1.0"})
    try:
        with urlopen(request, timeout=timeout) as response:
            headers = {key.lower(): value for key, value in response.headers.items()}
            return response.status, response.geturl(), headers, response.read()
    except HTTPError as exc:
        headers = {key.lower(): value for key, value in exc.headers.items()}
        return exc.code, url, headers, exc.read()
    except URLError as exc:
        return "ERR", url, {}, str(exc).encode("utf-8", "replace")


def same_origin_urls(urls: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    origins: list[str] = []
    for url in urls:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            continue
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if origin not in seen:
            seen.add(origin)
            origins.append(origin)
    return origins


def visible_text_length(text: str) -> int:
    return len(re.sub(r"\s+", " ", text).strip())


def warnings_for_page(url: str, parser: HeadParser, status: int | str) -> list[str]:
    warnings: list[str] = []
    parsed = urlparse(url)

    if parsed.fragment:
        warnings.append("Input URL contains a fragment; fragments are not sent in HTTP requests.")
        if parsed.fragment.startswith(("/", "!", "#")) or "/" in parsed.fragment:
            warnings.append("Fragment looks like client-side routing; prefer History API URLs for indexable views.")

    hash_routes = [
        anchor.get("href", "")
        for anchor in parser.anchors
        if anchor.get("href", "").startswith(("#/", "#!"))
    ]
    if hash_routes:
        warnings.append(f"Found {len(hash_routes)} hash-route links; verify SPA routing is crawlable.")

    text_len = visible_text_length(parser.body_text)
    if status == 200 and parser.script_count >= 3 and text_len < 500:
        warnings.append("Initial HTML has little visible text and several scripts; compare with rendered HTML for app shell risk.")

    if status == 200 and not parser.title:
        warnings.append("Missing title in initial HTML.")
    if status == 200 and not parser.meta_content("name", "description"):
        warnings.append("Missing meta description in initial HTML.")
    if status == 200 and parser.h1_count == 0:
        warnings.append("No H1 found in initial HTML; verify rendered headings if JavaScript injects content.")

    return warnings


def analyze_url(url: str, timeout: int) -> dict[str, object]:
    status, final_url, headers, body = fetch(url, timeout)
    content_type = headers.get("content-type", "")
    result: dict[str, object] = {
        "url": url,
        "status": status,
        "final_url": final_url,
        "content_type": content_type,
        "non_rendered_html_only": True,
    }

    if "html" not in content_type:
        return result

    html = body.decode("utf-8", "replace")
    parser = HeadParser()
    parser.feed(html)
    robots = parser.meta_content("name", "robots") or parser.meta_content("name", "googlebot")
    missing_alt = [img.get("src", "") for img in parser.images if not img.get("alt")]
    result.update(
        {
            "title": parser.title,
            "meta_description": parser.meta_content("name", "description"),
            "canonical": parser.canonical(),
            "robots_meta": robots,
            "og_description": parser.meta_content("property", "og:description"),
            "h1_count": parser.h1_count,
            "body_text_length": visible_text_length(parser.body_text),
            "anchor_count": len(parser.anchors),
            "script_count": parser.script_count,
            "image_count": len(parser.images),
            "images_missing_alt": len(missing_alt),
            "sample_missing_alt": missing_alt[:5],
            "warnings": warnings_for_page(url, parser, status),
        }
    )
    return result


def analyze_origin(origin: str, timeout: int) -> dict[str, object]:
    checks: dict[str, object] = {"origin": origin}
    for path in ("/robots.txt", "/sitemap.xml"):
        status, final_url, headers, body = fetch(urljoin(origin, path), timeout)
        text = body.decode("utf-8", "replace")
        checks[path] = {
            "status": status,
            "final_url": final_url,
            "content_type": headers.get("content-type", ""),
            "mentions_sitemap": "sitemap:" in text.lower(),
        }
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe basic public SEO signals for URLs.")
    parser.add_argument("urls", nargs="+", help="Absolute URLs to inspect")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of readable text")
    args = parser.parse_args()

    data = {
        "note": "This is a non-rendered initial HTML probe. Use rendered-page validation for JavaScript SEO.",
        "origins": [analyze_origin(origin, args.timeout) for origin in same_origin_urls(args.urls)],
        "pages": [analyze_url(url, args.timeout) for url in args.urls],
    }

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(data["note"])
    print()

    for origin in data["origins"]:
        print(f"Origin: {origin['origin']}")
        for path in ("/robots.txt", "/sitemap.xml"):
            item = origin[path]
            print(f"  {path}: {item['status']} {item['content_type']}")
        print()

    for page in data["pages"]:
        print(f"URL: {page['url']}")
        print(f"  Status: {page['status']} final={page['final_url']}")
        if "title" in page:
            print(f"  Title: {page['title'] or '[missing]'}")
            print(f"  Meta description: {page['meta_description'] or '[missing]'}")
            print(f"  Canonical: {page['canonical'] or '[missing]'}")
            print(f"  Robots meta: {page['robots_meta'] or '[none]'}")
            print(f"  OG description: {page['og_description'] or '[missing]'}")
            print(f"  H1 count: {page['h1_count']}")
            print(f"  Body text length: {page['body_text_length']}")
            print(f"  Anchors: {page['anchor_count']} scripts={page['script_count']}")
            print(f"  Images: {page['image_count']} missing_alt={page['images_missing_alt']}")
            for warning in page["warnings"]:
                print(f"  Warning: {warning}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
