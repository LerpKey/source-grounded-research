#!/usr/bin/env python3
"""Render a source-grounded Markdown report as a standalone HTML document.

This intentionally implements a small, safe Markdown subset with the Python
standard library only. Markdown remains the canonical, auditable source.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


FENCE_RE = re.compile(r"^\s*```\s*([\w+-]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
UL_RE = re.compile(r"^\s*[-*+]\s+(.+)$")
OL_RE = re.compile(r"^\s*\d+[.)]\s+(.+)$")
LINK_RE = re.compile(r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)")
AUTOLINK_RE = re.compile(r"<((?:https?://)[^>\s]+)>")
CODE_RE = re.compile(r"`([^`\n]+)`")
STRONG_RE = re.compile(r"(\*\*|__)(.+?)\1")
EM_RE = re.compile(r"(?<!\w)(\*|_)([^*_\n]+)\1(?!\w)")
TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")


def safe_href(url: str) -> str:
    """Allow only web links suitable for a research report."""

    if re.match(r"^https?://", url, re.I):
        return html.escape(url, quote=True)
    return "#"


def inline_markdown(value: str) -> str:
    """Convert a small inline Markdown subset while escaping all input."""

    tokens: list[str] = []

    def stash(fragment: str) -> str:
        tokens.append(fragment)
        return f"\x00{len(tokens) - 1}\x00"

    def link_repl(match: re.Match[str]) -> str:
        label = html.escape(match.group(1), quote=False)
        href = safe_href(match.group(2))
        return stash(f'<a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>')

    def auto_repl(match: re.Match[str]) -> str:
        url = match.group(1)
        href = safe_href(url)
        escaped = html.escape(url, quote=False)
        return stash(f'<a href="{href}" target="_blank" rel="noopener noreferrer">{escaped}</a>')

    def code_repl(match: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(match.group(1), quote=False)}</code>")

    raw = value
    raw = LINK_RE.sub(link_repl, raw)
    raw = AUTOLINK_RE.sub(auto_repl, raw)
    raw = CODE_RE.sub(code_repl, raw)
    escaped = html.escape(raw, quote=False)
    escaped = STRONG_RE.sub(lambda m: f"<strong>{m.group(2)}</strong>", escaped)
    escaped = EM_RE.sub(lambda m: f"<em>{m.group(2)}</em>", escaped)
    for index, token in enumerate(tokens):
        escaped = escaped.replace(f"\x00{index}\x00", token)
    return escaped


def plain_title(value: str) -> str:
    """Extract readable title text for the HTML title element."""

    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def split_table_row(line: str) -> list[str]:
    row = line.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def render_table(lines: list[str]) -> str:
    header = split_table_row(lines[0])
    body = [split_table_row(line) for line in lines[2:]]
    parts = ["<table>", "<thead><tr>"]
    parts.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    parts.append("</tr></thead>")
    if body:
        parts.append("<tbody>")
        for row in body:
            cells = row + [""] * max(0, len(header) - len(row))
            parts.append("<tr>")
            parts.extend(f"<td>{inline_markdown(cell)}</td>" for cell in cells[: len(header)])
            parts.append("</tr>")
        parts.append("</tbody>")
    parts.append("</table>")
    return "".join(parts)


def render_body(markdown: str) -> tuple[str, str]:
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    parts: list[str] = []
    title = "Research report"
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            language = fence.group(1)
            index += 1
            code_lines: list[str] = []
            while index < len(lines) and not FENCE_RE.match(lines[index]):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            class_attr = f' class="language-{html.escape(language, quote=True)}"' if language else ""
            parts.append(f"<pre><code{class_attr}>{html.escape(chr(10).join(code_lines), quote=False)}</code></pre>")
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1 and title == "Research report":
                title = plain_title(text)
            parts.append(f"<h{level}>{inline_markdown(text)}</h{level}>")
            index += 1
            continue

        if line.strip() in {"---", "***", "___"}:
            parts.append("<hr>")
            index += 1
            continue

        if (
            index + 1 < len(lines)
            and "|" in line
            and TABLE_SEPARATOR_RE.match(lines[index + 1])
        ):
            table_lines = [line, lines[index + 1]]
            index += 2
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                table_lines.append(lines[index])
                index += 1
            parts.append(render_table(table_lines))
            continue

        blockquote: list[str] = []
        if line.lstrip().startswith(">"):
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                blockquote.append(re.sub(r"^\s*>\s?", "", lines[index]))
                index += 1
            parts.append(f"<blockquote>{'<br>\n'.join(inline_markdown(item) for item in blockquote)}</blockquote>")
            continue

        list_match = UL_RE.match(line) or OL_RE.match(line)
        if list_match:
            ordered = bool(OL_RE.match(line))
            items: list[str] = []
            while index < len(lines):
                current = OL_RE.match(lines[index]) if ordered else UL_RE.match(lines[index])
                if not current:
                    break
                items.append(current.group(1))
                index += 1
            tag = "ol" if ordered else "ul"
            parts.append(f"<{tag}>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + f"</{tag}>")
            continue

        paragraph: list[str] = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip():
            next_line = lines[index]
            if (
                HEADING_RE.match(next_line)
                or FENCE_RE.match(next_line)
                or UL_RE.match(next_line)
                or OL_RE.match(next_line)
                or next_line.lstrip().startswith(">")
                or next_line.strip() in {"---", "***", "___"}
            ):
                break
            if index + 1 < len(lines) and "|" in next_line and TABLE_SEPARATOR_RE.match(lines[index + 1]):
                break
            paragraph.append(next_line.strip())
            index += 1
        parts.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")

    return "\n".join(parts), title or "Research report"


def document(markdown: str, title: str | None = None) -> str:
    body, detected_title = render_body(markdown)
    final_title = title or detected_title
    safe_title = html.escape(final_title, quote=False)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="generator" content="source-grounded-research render_report.py">
<title>{safe_title}</title>
<style>
:root {{ color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; line-height: 1.65; color: #172033; background: #f4f6fa; }}
body {{ margin: 0; }}
main.report {{ max-width: 1100px; margin: 2rem auto; padding: 2.5rem 3rem; background: #fff; box-shadow: 0 12px 38px rgba(25, 38, 65, .10); }}
h1, h2, h3, h4, h5, h6 {{ line-height: 1.25; color: #102a43; margin-top: 1.7em; }}
h1 {{ margin-top: 0; font-size: 2.25rem; border-bottom: 3px solid #2b6cb0; padding-bottom: .35em; }}
h2 {{ border-bottom: 1px solid #dbe4f0; padding-bottom: .25em; }}
a {{ color: #1d5fa7; }}
table {{ width: 100%; border-collapse: collapse; margin: 1.2rem 0; font-size: .95rem; }}
th, td {{ border: 1px solid #d8e0eb; padding: .65rem .75rem; vertical-align: top; text-align: left; }}
th {{ background: #edf3fa; color: #17324d; }}
tr:nth-child(even) td {{ background: #fafbfd; }}
blockquote {{ margin: 1.2rem 0; padding: .75rem 1rem; border-left: 4px solid #72a7d8; background: #f1f7fc; color: #334e68; }}
code {{ padding: .1em .3em; border-radius: 4px; background: #eef2f7; }}
pre {{ overflow-x: auto; padding: 1rem; border-radius: 6px; background: #172033; color: #f4f7fb; }}
pre code {{ padding: 0; background: transparent; color: inherit; }}
hr {{ border: 0; border-top: 1px solid #d8e0eb; margin: 2rem 0; }}
@media (max-width: 760px) {{ main.report {{ margin: 0; padding: 1.25rem; box-shadow: none; }} table {{ display: block; overflow-x: auto; white-space: normal; }} h1 {{ font-size: 1.8rem; }} }}
@media print {{ :root {{ background: #fff; }} main.report {{ max-width: none; margin: 0; padding: 0; box-shadow: none; }} a {{ color: inherit; text-decoration: none; }} a::after {{ content: " (" attr(href) ")"; font-size: .8em; word-break: break-all; }} }}
</style>
</head>
<body>
<main class="report">
{body}
</main>
</body>
</html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Markdown report to render")
    parser.add_argument("--output", type=Path, help="HTML output path; defaults to the input stem with .html")
    parser.add_argument("--title", help="Override the HTML document title")
    args = parser.parse_args()

    if not args.input.is_file():
        parser.error(f"input file not found: {args.input}")
    output = args.output or args.input.with_suffix(".html")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document(args.input.read_text(encoding="utf-8"), args.title), encoding="utf-8")
    print(f"Rendered: {args.input} -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
