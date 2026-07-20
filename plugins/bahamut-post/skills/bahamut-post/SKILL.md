---
name: bahamut-post
description: Create, rewrite, or convert articles for Bahamut/Gamer.com.tw forum posting. Use when the user asks for a 巴哈、巴哈姆特、Gamer.com.tw, forum, or board post/article/guide formatted for Bahamut's editor/source mode, especially when output must use [div], [b], [hr], [ol], and [li] tags, preserve line breaks, produce source code such as [div][b]Title[/b][/div], or repair pasted Bahamut markup that collapsed newlines.
---

# Bahamut Post

## Output Contract

- Output the final post as a single `text` fenced code block unless the user explicitly asks for raw unfenced text.
- Put only Bahamut-ready markup inside the artifact. Do not add explanations before or after when the user asks for a ready-to-post draft.
- Use Taiwan Traditional Chinese by default. Keep game, software, command, API, and file-path terms in English when clearer.

## Supported Markup

- Treat Bahamut article source as simplified/limited HTML-like markup where tags are written with square brackets.
- Wrap every visible paragraph, heading, note, and command line in `[div]...[/div]`.
- Use `[div][b]Title[/b][/div]` for the main title and for major section headings when emphasis is useful.
- Use `[b]...[/b]` only inside a wrapping block such as `[div]...[/div]` or `[li]...[/li]`; keep tags properly nested and paired.
- Use `[div align=left|center|right]...[/div]` only when alignment is requested. Default to plain `[div]`.
- Use `[hr]` between major sections. `[hr]` is self-closing; do not emit `[/hr]`.
- Use `[ol]` and `[li]...[/li]` for numbered lists. Put each `[li]` on its own line.
- Use `[ul]` and `[li]...[/li]` only when the user asks for unordered bullets.
- Use plain text for emphasis, such as `重點：`, `注意：`, `Q：`, and `A：`.
- Encode literal square brackets that are not Bahamut tags as `&#91;` and `&#93;` when they could be interpreted as tags, for example `&#91;selfcheck&#93;`.

## Optional Source Tags

- Use `[b]` freely for titles, headings, and short labels when it improves readability, as long as each bold span is inside `[div]` or `[li]`.
- Use style tags such as `[font=...]`, `[size=1..7]`, `[color=#rrggbb]`, `[bgcolor=#rrggbb]`, `[i]`, `[u]`, and `[s]` only when the user explicitly wants styled text.
- Use `[url=https://...]label[/url]` for links only when the user asks for embedded links.
- Use `[img=https://...]` for images only when the user provides or requests an image URL. `[img=...]` is self-closing; do not emit `[/img]`.
- Use `[table]`, `[tr]`, and `[td]` only when the user asks for a table. A table needs `table > tr > td`; common attributes include `width`, `height`, `cellspacing`, `cellpadding`, `border`, `align`, `bgcolor`, `colspan`, and `valign`.
- Use `[h1]`, `[h2]`, `[h3]`, `[tab]`, `[movie=...]`, and `[em=number]` only when specifically requested. For normal technical guides, prefer `[div]` headings and plain text.

## Avoid

- Do not put bare `[b]...[/b]` lines outside a block tag. Prefer `[div][b]...[/b][/div]`.
- Do not use Markdown bold, Markdown headings, Markdown bullets, raw HTML, or bare text outside tags unless the user explicitly asks for a stylized source-mode article.
- Do not use Markdown code fences inside the Bahamut artifact.
- Do not leave command blocks as bare lines. Bahamut may concatenate them.
- Do not rely on blank lines for spacing. Use `[hr]` or separate `[div]` lines.
- Do not add unsupported HTML attributes such as `id`; Bahamut source cleanup may remove or convert invalid markup.

## Conversion Rules

- Convert a title to `[div][b]Title[/b][/div]`, followed by `[hr]` when it starts the article.
- Convert headings to `[div][b]一、Section Title[/b][/div]` or similar `[div][b]...[/b][/div]` headings.
- Convert paragraphs to one `[div]...[/div]` per paragraph.
- Convert ordered lists to:

```text
[ol]
[li]First item[/li]
[li]Second item[/li]
[/ol]
```

- Convert code or shell snippets to one `[div]...[/div]` per line. Preserve line order exactly.
- Prefer one-line commands when practical. If using shell continuation backslashes, put each continued line in its own `[div]`.
- Convert inline paths, keys, and commands to plain text. Do not use backticks inside the Bahamut artifact unless the user specifically wants them.
- When converting Markdown links, either output plain `label：URL` in a `[div]` or use `[url=URL]label[/url]` if embedded links are requested.

## Final Check

Before replying, scan the artifact and ensure:

- Every visible content line is wrapped in a deliberate Bahamut tag, usually `[div]`, `[hr]`, `[ol]`, `[/ol]`, `[ul]`, `[/ul]`, or `[li]`.
- No Markdown fence, Markdown list marker, raw HTML, bare `[b]...[/b]` outside `[div]`/`[li]`, or unwrapped command line remains inside the artifact unless explicitly requested.
- Shell commands are split into separate `[div]` lines rather than concatenated.
- Literal diagnostic bracket text such as `[selfcheck]` is encoded if it is not an intended Bahamut tag.
