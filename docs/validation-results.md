# Validation Results

**Snapshot date:** 2026-08-19

This page summarizes the local forward tests used while rebuilding `source-grounded-research`. The public repository includes selected Markdown result reports so readers can inspect the output style and evidence discipline. Raw prompts, baselines, private multilingual outputs, fixtures, and HTML demos remain local.

## Test matrix

| Group | Cases | Result |
|---|---|---|
| English forward tests | EU AI Act, Artemis II, public libraries vs. community broadband | Completed; reports used for quality review |
| Chinese forward tests | Artemis II, EU AI Act, AI-industry claim verification | Completed privately to check cross-language robustness |
| Policy-chain test | UK Online Safety Act: statute → Ofcom guidance and duties → enforcement → monitoring | Strict chain validation passed |
| News-chain test | Ofcom/TikTok investigation: official event → media coverage → company response → unresolved status | Strict chain validation passed |
| HTML test | Policy-chain Markdown rendered to standalone responsive HTML | Rendered successfully; links preserved; no JavaScript |

## Public result reports

- [UK Online Safety Act policy chain](uk-online-safety-policy-chain.md)
- [UK TikTok investigation news chain](uk-tiktok-investigation-news-chain.md)
- [Public libraries and digital access](public-libraries-digital-access.md)
- [EU AI Act transparency reference report](eu-ai-act-reference-report.md)

## What was checked

- Agent Skill package structure and frontmatter: passed.
- Python script compilation: passed.
- Strict report validation: passed on the published reports.
- Policy and news evidence-chain validation: passed.
- Live link checks: policy chain 6/6, news chain 4/4, libraries 2/2, EU AI Act 7/7.
- HTML smoke test: standalone output, responsive layout, preserved evidence links, and no executable JavaScript.

## How to reproduce

```bash
python skills/source-grounded-research/scripts/validate_report.py docs/uk-online-safety-policy-chain.md --strict --chain-type policy
python skills/source-grounded-research/scripts/validate_report.py docs/uk-tiktok-investigation-news-chain.md --strict --chain-type news
python skills/source-grounded-research/scripts/validate_report.py docs/public-libraries-digital-access.md --strict
python skills/source-grounded-research/scripts/validate_report.py docs/eu-ai-act-reference-report.md --strict
python skills/source-grounded-research/scripts/check_links.py docs/uk-online-safety-policy-chain.md --verify
```

For a visual companion, render any validated Markdown report with the optional HTML renderer:

```bash
python skills/source-grounded-research/scripts/render_report.py \
  docs/uk-online-safety-policy-chain.md \
  --output docs/uk-online-safety-policy-chain.html
```

The generated HTML is a local demonstration artifact and is not part of the tracked release package.

## Publication boundary

The published documents are representative outputs, not a claim that every future report will be correct automatically. Researchers must still inspect sources, dates, relevance, uncertainty, and the limits of each conclusion. Private reports, raw evaluation prompts, without-skill comparisons, local fixtures, and generated HTML remain ignored by Git.
