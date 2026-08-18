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

CHAIN_RULES = {
    "policy": {
        "heading": r"^##\s+.*(?:policy implementation|implementation) chain",
        "terms": (
            (r"statutory|legal|binding", "legal or binding force"),
            (r"regulator|guidance|implementation", "regulator, guidance, or implementation stage"),
            (r"enforcement|evaluation|scrutiny", "enforcement or evaluation stage"),
            (r"gap|unknown|not established|limitation", "explicit gap or limitation"),
        ),
    },
    "news": {
        "heading": r"^##\s+.*(?:news provenance|provenance|news source) chain",
        "terms": (
            (r"source|outlet|reported|publication", "source or publication role"),
            (r"independent|shared|syndicat|same source", "independence or shared-source assessment"),
            (r"response|correction|update|status", "response, correction, update, or status"),
            (r"gap|unknown|not established|limitation|unresolved", "explicit gap or unresolved claim"),
        ),
    },
    "generic": {
        "heading": r"^##\s+.*(?:evidence|relationship|provenance|implementation).*chain",
        "terms": (
            (r"node|actor|relationship|edge|stage", "node or relationship vocabulary"),
            (r"source|evidence", "source or evidence field"),
            (r"gap|unknown|not established|limitation", "explicit gap or limitation"),
        ),
    },
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat heuristic warnings as failures")
    parser.add_argument(
        "--chain-type",
        choices=sorted(CHAIN_RULES),
        help="Require an explicit evidence-chain structure for a policy, news, or generic chain report",
    )
    args = parser.parse_args()
    text = args.file.read_text(encoding="utf-8", errors="replace")
    issues: list[tuple[str, int, str]] = []

    if not re.search(r"^#\s+", text, re.M):
        issues.append(("ERROR", 1, "missing report title"))
    if not re.search(r"bottom line|executive summary|summary|结论|结论速览|直接结论|摘要", text, re.I):
        issues.append(("WARN", 1, "no conclusion-first summary section found"))
    if not re.search(r"^##\s+.*(?:Sources|References|来源|参考资料|来源台账)", text, re.I | re.M):
        issues.append(("WARN", 1, "no Sources or References section found"))

    if args.chain_type:
        rules = CHAIN_RULES[args.chain_type]
        if not re.search(rules["heading"], text, re.I | re.M):
            issues.append(("ERROR", 1, f"missing {args.chain_type} evidence-chain heading"))
        for pattern, label in rules["terms"]:
            if not re.search(pattern, text, re.I):
                issues.append(("ERROR", 1, f"chain missing {label}"))
        if not LINK_RE.search(text):
            issues.append(("ERROR", 1, "chain report has no clickable evidence link"))

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
