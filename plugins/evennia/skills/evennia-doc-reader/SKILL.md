---
name: evennia-doc-reader
description: Read and study the official Evennia MUD documentation by browsing pages sequentially using the "next" navigation. Use when the user wants to learn Evennia, read the official docs, study game creation concepts, or follow the documentation from beginning to end. Triggers on requests like "read the Evennia docs", "learn Evennia", "browse Evennia documentation", "go through the Evennia manual", or when the user asks to study game development using Evennia.
---

# Evennia Doc Reader

Sequentially read and study the official Evennia documentation hosted at https://www.evennia.com/docs/latest/.

## How Evennia Docs Work

- Sphinx-generated docs with sequential "prev/next" navigation
- Base URL: `https://www.evennia.com/docs/latest/`
- Each page has `<link rel="next" href="...">` in the `<head>` pointing to the next chapter
- The next link stops at the last page (no more `rel="next"` element)

## Workflow

### 1. Fetch a Page

```bash
curl -sL "https://www.evennia.com/docs/latest/<page>.html"
```

### 2. Extract Next Page URL

From the HTML head, find the next link:

```bash
curl -sL "<url>" | grep 'rel="next"' | sed -E 's/.*href="([^"]+)".*/\1/'
```

The output is a relative filename (e.g., `Evennia-Introduction.html`). Construct the full URL as `<base>/<filename>`.

### 3. Extract Page Content

Strip HTML and extract readable body text:

```bash
curl -sL "<url>" | sed -n '/class="body"/,/class="related"/p' | sed 's/<[^>]*>//g' | sed '/^[[:space:]]*$/d'
```

This captures the main content between the `body` and `related` containers, with all HTML tags removed.

### 4. Study and Save Notes

- Read the extracted content carefully
- Save key information to `docs_study/` as organized markdown notes
- Organize notes by topic section matching the doc structure (e.g., `docs_study/setup.md`, `docs_study/concepts.md`)
- Include code examples, commands, and configuration details verbatim

### 5. Navigate to Next

- If `next` link exists → go to step 1 with the new URL
- If `next` link does not exist → you've reached the end

## Page Index

Before starting, build a page index and save it to `docs_study/INDEX.md`. Read the Table of Contents from `index.html` and list all chapters with their filenames and URLs.

## Tips

- Run `curl -sI "<url>" | head -5` to verify a page returns HTTP 200 before fetching content
- Some pages may be large; if content is truncated, process in sections by targeting specific heading anchors
- After finishing all pages, write a learning summary to `docs_study/SUMMARY.md`
- The `docs_study/` directory is relative to the repo root
