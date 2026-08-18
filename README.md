# Source-Grounded Research

> Answers can sound right while being impossible to audit. Source-Grounded Research turns research into a visible chain from claim to source to conclusion.

Source-Grounded Research is an open Agent Skill for fact-finding, market research, public-interest analysis, policy research, comparisons, due diligence, and evidence-aware report writing. It makes the research process more defensible without forcing every topic into a government, party, bureaucratic, or academic template.

## Install

Install the skill with the open skills CLI:

```bash
npx skills add OWNER/REPOSITORY --skill source-grounded-research
```

For Codex, Claude Code, Cursor, GitHub Copilot, and other compatible agents, use the same repository source and select the target agent when prompted. The exact command depends on the final GitHub owner and repository name.

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
- “Synthesize the literature on this topic and identify evidence gaps.”

## What it produces

Markdown is the canonical format because it is portable, reviewable, easy to translate, and GitHub-friendly. A complete report does not require HTML. HTML is an optional companion when a long report, timeline, visual comparison, print layout, or interactive presentation makes the result easier to understand.

Typical outputs include:

- an executive summary and direct answer;
- scope, definitions, and method;
- evidence-backed profiles and findings;
- an explicit evidence chain or timeline when the topic involves relationships, origins, authority, implementation, or change over time;
- short original excerpts or precise document references for high-impact claims;
- comparison tables with consistent dimensions;
- a fact/inference/uncertainty synthesis;
- limitations and open questions;
- a compact source ledger with complete links.

## Examples

The repository includes a reproducible example on public libraries and digital access:

- [baseline without the skill](examples/public-libraries-digital-access/without-skill.md);
- [evidence-first report with the skill](examples/public-libraries-digital-access/with-skill.md);
- [side-by-side comparison](examples/public-libraries-digital-access/comparison.md);
- [the benchmark prompt](examples/public-libraries-digital-access/prompt.md).
- [a full current-affairs reference report](examples/reference-report-eu-ai-act-2026-08.md).

The baseline is intentionally illustrative and should not be treated as a deliverable. The enhanced report shows the expected evidence discipline.

## Compatibility and boundaries

The package follows the open Agent Skills format: a `SKILL.md` file plus optional references and scripts. It is tool-agnostic and uses whatever search, browser, document, and file capabilities the host agent provides.

If an agent cannot browse or inspect a source, the skill must say so. It must never invent citations or claim that a link was verified when it was not.

External pages and downloaded files are treated as untrusted content. The skill does not run downloaded executables, expose secrets, or take external actions without authorization. See [SECURITY.md](SECURITY.md).

## Validate locally

```bash
python skills/source-grounded-research/scripts/check_links.py examples/public-libraries-digital-access/with-skill.md --verify
python skills/source-grounded-research/scripts/validate_report.py examples/public-libraries-digital-access/with-skill.md --strict
```

The full evaluation process is documented in [evals/runbook.md](evals/runbook.md).

## Contributing

Contributions are welcome, especially new source-quality patterns, regression prompts, fixture-based tests, and examples that demonstrate genuine improvements. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

If this skill helps you produce more trustworthy research, please consider starring the repository. A star is useful feedback and helps other researchers discover the project; it is not a substitute for testing or reviewing the work.

## License

MIT. See [LICENSE](LICENSE).
