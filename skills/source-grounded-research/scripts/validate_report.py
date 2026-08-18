#!/usr/bin/env python3
"""Run conservative structural checks for a source-grounded Markdown report."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


LINK_RE = re.compile(r"\[[^\]]+\]\(https?://[^)\s]+\)|<https?://[^>]+>", re.I)
BARE_URL_RE = re.compile(r"(?<![<(])https?://[^\s)\]>]+", re.I)
NUMBER_RE = re.compile(r"(?<![\w])(?:\$|€|£)?\d[\d,.]*(?:\s?%|\s?(?:million|billion|thousand))?", re.I)
PLACEHOLDER_RE = re.compile(r"\[(?:TBD|TODO|SOURCE NEEDED|CITATION NEEDED|UNKNOWN)\]|\b(?:TBD|TODO|FIXME)\b", re.I)
FACT_LABELS = (
    "verified fact", "according to", "reported", "found that", "shows that",
    "官方确认", "官方报道", "报道声称", "报道中的直接主张", "页面显示", "可以确认",
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat heuristic warnings as failures")
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8", errors="replace")
    issues: list[tuple[str, int, str]] = []

    if not re.search(r"^#\s+", text, re.M):
        issues.append(("ERROR", 1, "missing report title"))
    if not re.search(r"bottom line|executive summary|summary|结论|结论速览|直接结论|摘要", text, re.I):
        issues.append(("WARN", 1, "no conclusion-first summary section found"))
    if not re.search(r"^##\s+.*(?:Sources|References|来源|参考资料|来源台账)", text, re.I | re.M):
        issues.append(("WARN", 1, "no Sources or References section found"))

    for line_no, line in enumerate(text.splitlines(), start=1):
        if PLACEHOLDER_RE.search(line):
            issues.append(("ERROR", line_no, "unresolved placeholder"))
        if "..." in line and "http" in line:
            issues.append(("ERROR", line_no, "truncated URL"))

        stripped = line.strip()
        if (
            not stripped
            or stripped.startswith("#")
            or stripped.startswith("|")
            or stripped.startswith("```")
            or stripped.startswith("- **")
            or stripped.startswith("**As of:")
            or stripped.startswith("**查证日期")
            or stripped.startswith("**查证对象")
        ):
            continue
        has_link = bool(LINK_RE.search(line))
        has_number = bool(NUMBER_RE.search(line))
        looks_factual = has_number or any(marker in stripped.lower() for marker in FACT_LABELS)
        if args.strict and looks_factual and not has_link:
            issues.append(("WARN", line_no, "material-looking claim has no inline evidence link"))

    # Detect URLs that are not Markdown autolinks or link destinations.
    for match in BARE_URL_RE.finditer(text):
        url = match.group(0).rstrip(".,;:!?，。；：！？")
        before_two = text[max(0, match.start() - 2):match.start()]
        before_one = text[max(0, match.start() - 1):match.start()]
        if before_two != "](" and before_one != "<" and url not in ("https://example.com",):
            issues.append(("ERROR", text.count("\n", 0, match.start()) + 1, "bare URL: " + url))

    errors = 0
    warnings = 0
    for level, line_no, message in issues:
        print(f"{level} line {line_no}: {message}")
        errors += level == "ERROR"
        warnings += level == "WARN"
    print(f"\nReport checks: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
