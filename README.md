# Source-Grounded Research

[![skills.sh](https://skills.sh/b/LerpKey/source-grounded-research)](https://skills.sh/LerpKey/source-grounded-research)

> Answers can sound right while being impossible to audit. Source-Grounded Research turns research into a visible chain from claim to source to conclusion.

Repository: [github.com/LerpKey/source-grounded-research](https://github.com/LerpKey/source-grounded-research)

Source-Grounded Research is an open Agent Skill for fact-finding, market research, public-interest analysis, policy research, comparisons, due diligence, and evidence-aware report writing. It makes the research process more defensible without forcing every topic into a government, party, bureaucratic, or academic template.

## Install

Project name: **Source-Grounded Research**

- Recommended repository name: `source-grounded-research`
- Skill ID: `source-grounded-research`

```bash
npx skills add LerpKey/source-grounded-research --skill source-grounded-research
```

For Codex, Claude Code, Cursor, GitHub Copilot, and other compatible agents, use the same repository source and select the target agent when prompted. The skill ID stays `source-grounded-research` even if you choose a different repository name.

## Choose the depth

For a focused question:

```text
Fact-check this claim. Use primary sources where possible, cite each material claim inline, and state what remains uncertain.
```

For a complete report:

```text
Write a full research dossier in English. Include an executive summary, scope and method, subject profiles, an evidence chain or timeline, original evidence, comparison tables where useful, synthesis, limitations, and a complete source ledger. Verify every important link.
```

The skill can also handle:

- “Fact-check this claim and show the original evidence.”
- “Research the market and write a report for an executive decision.”
- “Compare these products using current first-party documentation and independent tests.”
- “Trace how a policy is implemented across institutions or jurisdictions.”
- “Map a UK policy from statute to regulator guidance, implementation, enforcement, and evaluation.”
- “Trace this news claim from the underlying event to the first report, later coverage, affected-party response, and corrections.”
- “Synthesize the literature on this topic and identify evidence gaps.”

## What it produces

Markdown is the canonical format because it is portable, reviewable, easy to translate, and GitHub-friendly. A complete report does not require HTML. HTML is an optional companion when a long report, timeline, visual comparison, print layout, or interactive presentation makes the result easier to understand.

To create the optional HTML companion after validating the Markdown:

```bash
python skills/source-grounded-research/scripts/render_report.py \
  path/to/validated-report.md \
  --output path/to/validated-report.html
```

The renderer is standard-library-only, self-contained, print-friendly, and JavaScript-free. Keep the `.md` file as the source of truth.

Typical outputs include:

- an executive summary and direct answer;
- scope, definitions, and method;
- evidence-backed profiles and findings;
- an explicit evidence chain or timeline when the topic involves relationships, origins, authority, implementation, or change over time;
- a policy implementation chain or news provenance chain when the question depends on how authority, evidence, or a claim travelled;
- short original excerpts or precise document references for high-impact claims;
- comparison tables with consistent dimensions;
- a fact/inference/uncertainty synthesis;
- limitations and open questions;
- a compact source ledger with complete links.

## Chain modes

Use a chain when the answer depends on how authority, evidence, or a claim travelled:

- **Policy implementation chain:** law or policy origin → delegated authority → guidance and operational duties → compliance or enforcement → monitoring and evaluation.
- **News provenance chain:** event or primary evidence → originating source → first report or wire copy → later coverage → affected-party response → correction or unresolved status.

The skill records the role and legal/media status of each node. Repeated articles that share the same source are treated as reach, not independent confirmation.

## Validation snapshot

The repository keeps the release package small while publishing a curated set of Markdown results under [`docs/`](docs/). Raw prompts, without-skill baselines, side-by-side comparisons, private multilingual outputs, fixtures, and HTML demos remain local and are intentionally excluded from Git.

Latest local validation included:

| Check | Result |
|---|---|
| English forward tests | 3 focused tests: EU AI Act, Artemis II, libraries vs. community broadband |
| Chinese forward tests | 3 focused tests: Artemis II, EU AI Act, AI-industry claim verification |
| Policy-chain example | UK Online Safety Act: statute → Ofcom guidance and duties → enforcement → monitoring |
| News-chain example | Ofcom/TikTok investigation: official event → Reuters/Guardian coverage → company response → unresolved status |
| HTML smoke test | Markdown rendered to standalone, responsive, JavaScript-free HTML; evidence links preserved |
| Package checks | Skill format, Python compilation, strict report checks, chain checks, and live link checks passed |

These results are a release snapshot, not a promise that future research will always produce the same conclusions. Re-run the local checks after changing the skill.

### Public result reports

- [Validation results and test matrix](docs/validation-results.md)
- [UK Online Safety Act policy chain](docs/uk-online-safety-policy-chain.md)
- [UK TikTok investigation news chain](docs/uk-tiktok-investigation-news-chain.md)
- [Public libraries and digital access](docs/public-libraries-digital-access.md)
- [EU AI Act transparency reference report](docs/eu-ai-act-reference-report.md)

## Compatibility and boundaries

The package follows the open Agent Skills format: a `SKILL.md` file plus optional references and scripts. It is tool-agnostic and uses whatever search, browser, document, and file capabilities the host agent provides.

If an agent cannot browse or inspect a source, the skill must say so. It must never invent citations or claim that a link was verified when it was not.

External pages and downloaded files are treated as untrusted content. The skill does not run downloaded executables, expose secrets, or take external actions without authorization. These boundaries are documented in `SKILL.md`.

## Validate locally

```bash
python skills/source-grounded-research/scripts/check_links.py path/to/report.md --verify
python skills/source-grounded-research/scripts/validate_report.py path/to/report.md --strict
# For a policy or news chain, add --chain-type policy or --chain-type news.
```

Raw evaluation materials remain local during development. The linked documents are selected, reproducible result reports intended to show how the skill handles different research shapes without publishing every prompt, baseline, or private test output.

## Contributing

Contributions are welcome, especially new source-quality patterns, regression prompts, fixture-based tests, and examples that demonstrate genuine improvements. Keep test artifacts and private research outputs out of the release package.

If this skill helps you produce more trustworthy research, please consider starring the repository. A star is useful feedback and helps other researchers discover the project; it is not a substitute for testing or reviewing the work.

## License

MIT. See [LICENSE](LICENSE).
