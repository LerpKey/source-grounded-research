# Contributing

Thank you for helping improve Source-Grounded Research.

## Good contributions

- add a source-selection rule that generalizes across domains;
- add a realistic benchmark prompt and a scored result;
- improve a script with a standard-library-only implementation;
- document a failure mode without weakening evidence standards;
- add an example where the skill changes the research outcome or auditability.

## Pull request checklist

- Keep all skill instructions and user-facing documentation in English.
- Keep the core `SKILL.md` concise and move detailed variants into `references/`.
- Include or update a fixture when changing validation scripts.
- If changing the HTML renderer, regenerate the committed HTML demo from its Markdown source and verify both the Markdown and generated HTML links.
- Run the package validator and report checks locally.
- Do not add secrets, private source material, or downloaded executables.
- Explain whether the change affects triggering, evidence quality, output structure, or tooling.

## Reporting issues

Please include the host agent, prompt, expected behavior, actual behavior, relevant source type, and a minimal reproduction when possible. Do not paste private or sensitive research material.
