# Reproducible Evaluation Runbook

## Goal

Measure whether the skill improves auditability and evidence discipline, not merely prose style.

## Procedure

1. Start two fresh agent contexts.
2. Give both contexts the same prompt from [benchmark-prompts.md](benchmark-prompts.md).
3. Do not provide the baseline context with the skill instructions.
4. Load `source-grounded-research` explicitly in the enhanced context.
5. Keep the same topic, source window, output format, and approximate research budget.
6. Save the raw reports as `without-skill.md` and `with-skill.md`.
7. Run the structural and link checks on both reports.
8. Score both reports using [rubric.md](rubric.md).
9. Record unexpected failures and add a regression fixture before changing the skill.

## Local checks

From the repository root:

```bash
python skills/source-grounded-research/scripts/check_links.py examples/public-libraries-digital-access/with-skill.md --verify
python skills/source-grounded-research/scripts/validate_report.py examples/public-libraries-digital-access/with-skill.md --strict
```

For offline fixtures, omit `--verify`. A failed live link is a report limitation to investigate, not a reason to silently replace the source with an unverified summary.

## Interpretation

Report the dimension scores, not only a total. A good result should show fewer unsupported claims, clearer boundaries, better source-to-claim alignment, and more explicit uncertainty. If the enhanced report merely adds links without improving claim precision, treat that as a failed iteration.
