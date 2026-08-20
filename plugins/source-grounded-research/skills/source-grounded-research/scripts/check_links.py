#!/usr/bin/env python3
"""Scan Markdown or HTML reports for link-quality problems.

Offline mode checks clickable links, bare URLs, and truncated URLs.
--verify performs a lightweight GET/HEAD request and records final URLs and titles.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s\"'<>()[\]{}]+", re.IGNORECASE)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\((https?://[^)\s]+)\)")
AUTO_LINK_RE = re.compile(r"<(https?://[^>]+)>")
HTML_LINK_RE = re.compile(r"(?:href|src)=[\"'](https?://[^\"']+)[\"']", re.IGNORECASE)
USER_AGENT = "source-grounded-research-link-checker/1.0"


def clean_url(url: str) -> str:
    return url.rstrip(".,;:!?，。；：！？")


def collect(text: str) -> tuple[list[str], set[str], list[tuple[str, str]]]:
    all_urls = [clean_url(url) for url in URL_RE.findall(text)]
    clickable = {clean_url(url) for url in MD_LINK_RE.findall(text)}
    clickable.update(clean_url(url) for url in AUTO_LINK_RE.findall(text))
    clickable.update(clean_url(url) for url in HTML_LINK_RE.findall(text))
    labeled: list[tuple[str, str]] = []
    labeled.extend((clean_url(url), label) for label, url in re.findall(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", text))
    labeled.extend((clean_url(url), label) for label, url in re.findall(r"<a[^>]*href=[\"'](https?://[^\"']+)[\"'][^>]*>(.*?)</a>", text, re.I | re.S))
    return all_urls, clickable, labeled


def verify(url: str, timeout: int) -> tuple[str, int | None, str, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            sample = response.read(64 * 1024)
            content_type = response.headers.get_content_type()
            charset = response.headers.get_content_charset() or "utf-8"
            title = ""
            if "html" in content_type:
                decoded = sample.decode(charset, errors="replace")
                match = re.search(r"<title[^>]*>(.*?)</title>", decoded, re.I | re.S)
                if match:
                    title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", match.group(1)))).strip()
            return url, response.status, response.geturl(), title
    except urllib.error.HTTPError as exc:
        return url, exc.code, exc.geturl(), str(exc)
    except Exception as exc:  # noqa: BLE001 - report URL-specific failures
        return url, None, "", str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--verify", action="store_true", help="Fetch every clickable URL")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8", errors="replace")
    all_urls, clickable, labeled = collect(text)
    bare_urls = sorted(set(url for url in all_urls if url not in clickable))
    truncated = sorted(set(url for url in all_urls if "..." in url))
    print(f"File: {args.file}")
    print(f"Clickable links: {len(clickable)}")
    print(f"Bare URLs: {len(bare_urls)}")
    for url in bare_urls[:20]:
        print(f"  - {url}")
    print(f"Truncated URLs: {len(truncated)}")
    for url in truncated:
        print(f"  - {url}")

    problems = len(bare_urls) + len(truncated)
    if args.verify and clickable:
        print(f"\nVerifying {len(clickable)} links...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            results = list(executor.map(lambda url: verify(url, args.timeout), sorted(clickable)))
        bad = 0
        for original, status, final, title in results:
            if status is None or status >= 400:
                bad += 1
                print(f"  [FAIL] {original} -> {status or title}")
            else:
                print(f"  [{status}] {original} -> {final}{(' | ' + title[:80]) if title else ''}")
        print(f"Verified: {len(clickable) - bad}/{len(clickable)}")
        problems += bad

        for url, label in labeled:
            matching = next((row for row in results if row[0] == url), None)
            if matching and matching[3] and label.strip().lower() not in matching[3].lower():
                print(f"  [WARN] link text may not match page title: {label!r} -> {matching[3]!r}")

    print(f"\nConclusion: {problems} blocking link problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
