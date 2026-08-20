#!/usr/bin/env python3
"""Fetch source pages for local inspection without treating page text as instructions.

Usage:
  python fetch_sources.py URL [URL ...] --out evidence
  python fetch_sources.py URL --out evidence --attachments

The script uses the Python standard library only. It saves page metadata and text;
attachments are downloaded only when explicitly requested.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


USER_AGENT = "source-grounded-research/1.0 (+https://github.com/)"
ATTACHMENT_EXTENSIONS = (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".zip")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.text_parts: list[str] = []
        self.links: list[tuple[str, str]] = []
        self._in_title = False
        self._skip_depth = 0
        self._link_href: str | None = None
        self._link_text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if tag == "title":
            self._in_title = True
        if tag in {"script", "style", "noscript", "template", "svg"}:
            self._skip_depth += 1
        if tag == "a" and attrs_map.get("href"):
            self._link_href = attrs_map["href"]
            self._link_text = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag in {"script", "style", "noscript", "template", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "a" and self._link_href:
            self.links.append((self._link_href, " ".join(self._link_text).strip()))
            self._link_href = None
            self._link_text = []

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        clean = re.sub(r"\s+", " ", data).strip()
        if not clean:
            return
        if self._in_title:
            self.title_parts.append(clean)
        self.text_parts.append(clean)
        if self._link_href is not None:
            self._link_text.append(clean)


def request(url: str, timeout: int) -> tuple[str, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        final_url = response.geturl()
        content_type = response.headers.get_content_type()
        raw = response.read()
        encoding = response.headers.get_content_charset() or "utf-8"
    return final_url, content_type, raw.decode(encoding, errors="replace")


def safe_name(title: str, url: str) -> str:
    candidate = title.strip() or urllib.parse.urlparse(url).path.rsplit("/", 1)[-1] or "source"
    candidate = re.sub(r"[^\w\-. ]+", "_", html.unescape(candidate), flags=re.UNICODE)
    return candidate.strip(" ._")[:80] or "source"


def download_attachment(url: str, output_dir: Path, timeout: int) -> Path:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        data = response.read()
        path_name = urllib.parse.urlparse(response.geturl()).path.rsplit("/", 1)[-1] or "attachment.bin"
    path_name = re.sub(r"[^\w\-.]+", "_", path_name, flags=re.UNICODE)
    path = output_dir / path_name
    path.write_bytes(data)
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("urls", nargs="+", help="Source page URLs")
    parser.add_argument("--out", type=Path, required=True, help="Directory for captured source text")
    parser.add_argument("--attachments", action="store_true", help="Download linked attachments explicitly")
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    failures = 0
    for url in args.urls:
        try:
            final_url, content_type, body = request(url, args.timeout)
            title = ""
            links: list[tuple[str, str]] = []
            if "html" in content_type:
                page = PageParser()
                page.feed(body)
                title = " ".join(page.title_parts).strip()
                links = page.links
                text = "\n".join(page.text_parts)
            else:
                text = body
            path = args.out / f"{safe_name(title, final_url)}.txt"
            path.write_text(
                f"Title: {title}\nOriginal URL: {url}\nFinal URL: {final_url}\nContent-Type: {content_type}\n\n{text}\n",
                encoding="utf-8",
            )
            print(f"[OK] {url}\n     title: {title or '(untitled)'}\n     saved: {path}")
            if args.attachments:
                for href, label in links:
                    absolute = urllib.parse.urljoin(final_url, href)
                    if urllib.parse.urlparse(absolute).path.lower().endswith(ATTACHMENT_EXTENSIONS):
                        try:
                            attachment = download_attachment(absolute, args.out, args.timeout)
                            print(f"     attachment: {attachment} ({label})")
                        except Exception as exc:  # noqa: BLE001 - report individual failures and continue
                            print(f"     attachment failed: {absolute} ({exc})")
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            failures += 1
            print(f"[FAIL] {url}\n      {exc}", file=sys.stderr)
    print(f"\nCompleted: {len(args.urls) - failures}/{len(args.urls)} sources")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
