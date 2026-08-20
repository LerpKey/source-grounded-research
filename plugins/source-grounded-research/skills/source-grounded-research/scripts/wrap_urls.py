#!/usr/bin/env python3
"""Convert bare HTTP(S) URLs into Markdown autolinks without changing existing links."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


URL_RE = re.compile(r"https?://[^\s<>\"'()\[\]]+", re.I)


def wrap(text: str) -> tuple[str, int]:
    changes = 0
    output: list[str] = []
    for line in text.splitlines(keepends=True):
        if re.search(r"^\s*```", line) or "](" in line or "href=" in line.lower():
            output.append(line)
            continue
        def replace(match: re.Match[str]) -> str:
            nonlocal changes
            url = match.group(0).rstrip(".,;:!?，。；：！？")
            suffix = match.group(0)[len(url):]
            changes += 1
            return f"<{url}>{suffix}"
        output.append(URL_RE.sub(replace, line))
    return "".join(output), changes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8", errors="replace")
    converted, changes = wrap(text)
    if args.in_place:
        args.file.write_text(converted, encoding="utf-8")
        destination = args.file
    elif args.out:
        args.out.write_text(converted, encoding="utf-8")
        destination = args.out
    else:
        print(converted, end="")
        destination = None
    if destination:
        print(f"Converted {changes} URL(s) in {destination}")
    else:
        print(f"Converted {changes} URL(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
