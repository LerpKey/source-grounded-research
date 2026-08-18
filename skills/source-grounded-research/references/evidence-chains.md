# Evidence Chains Across Institutions, Policies, and News

Use this reference when the user asks how a policy was created or implemented, how an institution relates to another, how a public claim travelled through the media, or why a reported event should be trusted.

## Contents

- [Core model](#core-model)
- [Policy implementation chain](#policy-implementation-chain)
- [News provenance chain](#news-provenance-chain)
- [Chain quality rules](#chain-quality-rules)
- [Reusable tables](#reusable-tables)

## Core model

An evidence chain is a map of nodes and relationships, not a decorative timeline.

- A **node** is a document, institution, person, event, decision, service, claim, or outcome.
- An **edge** explains how two nodes are related: enacted by, delegated to, operationalized by, reported by, quoted from, challenged by, corrected by, or evaluated by.
- A **source** supports a node, an edge, or both. Record which one it supports.
- A **gap** is a missing or weakly supported node or edge. Keep it visible instead of drawing a plausible line through it.

Use two layers when needed:

1. **Substantive evidence layer:** what happened, what rule exists, what result was measured, or what someone actually said.
2. **Institutional or publication layer:** who had authority, who implemented the rule, who first published the claim, who repeated it, and who later corrected or challenged it.

The two layers answer different questions. A newspaper can establish that a claim was published, but publication alone does not prove the underlying event. A regulator can establish that an investigation opened, but an opening notice does not establish a breach.

## Policy implementation chain

Use this form for a law, regulation, public program, institutional policy, or cross-jurisdiction comparison:

```text
legal or policy origin
  → authority and scope
  → delegated rule-making or guidance
  → implementation duty or operational mechanism
  → compliance, inspection, or enforcement
  → monitoring, evaluation, appeal, or revision
```

The chain is often a branching graph rather than a single line. Add branches for devolved governments, courts, regulators, local implementers, funding bodies, or affected groups when they materially change the result.

For every stage, record:

| Field | Question |
|---|---|
| Node | What document, body, action, or outcome is being mapped? |
| Actor | Who created, authorized, implemented, enforced, challenged, or evaluated it? |
| Relationship | What is the exact link to the previous node? |
| Legal or institutional force | Binding law, secondary legislation, code, guidance, proposal, contract, practice, or commentary? |
| Date and jurisdiction | When and where does the node apply? |
| Evidence | Which source directly establishes the node or edge? |
| Gap | What is not established, delayed, contested, or outside scope? |

Do not collapse these stages:

- A bill, an enacted statute, and a policy announcement are not interchangeable.
- Guidance may explain a legal duty without creating the duty itself.
- A regulator’s investigation shows that scrutiny began, not that a breach occurred.
- A consultation or planned milestone is not an implemented rule.
- A reported improvement is not proof that the policy caused the improvement unless the evaluation supports that causal claim.

For non-UK systems, replace the labels with the local equivalents. In a Chinese policy chain, the nodes may include national, provincial, municipal, and county documents. In the UK, the relevant structure may instead involve Parliament, a department, a regulator, devolved administrations, local authorities, courts, and regulated entities. The method follows function and authority, not a fixed national hierarchy.

## News provenance chain

Use this form for breaking news, a disputed report, a viral claim, or a story whose wording changed as it travelled:

```text
event or underlying evidence
  → originating person, institution, document, data, image, or recording
  → first public report or wire copy
  → later outlet coverage and attribution
  → affected-party response or denial
  → correction, update, investigation, or final finding
```

Separate three questions:

1. **Did an outlet publish this?** The outlet’s page can prove publication, date, headline, and wording.
2. **What evidence did the outlet rely on?** Trace quotes, documents, images, witnesses, datasets, and named or unnamed sources.
3. **Is the underlying claim established?** Seek the original evidence, independent corroboration, or a later finding.

Record provenance details that are easy to lose:

- first publication time and later update time;
- whether a later article is a rewrite, syndication, wire copy, or independent reporting;
- the exact source of each quotation or number;
- whether an image, video, or document is original, reused, cropped, translated, or unverified;
- the response from the person or organization affected;
- whether the story remains an allegation, an open investigation, a confirmed event, or a corrected claim.

Never count several articles as independent confirmation if they all cite the same wire story, official statement, anonymous source, or social-media post. They may show reach or editorial uptake, but they do not add independent evidentiary weight.

When a source is inaccessible, preserve the source-of-source description and mark the limitation. Do not reconstruct an unseen original from search snippets or a later article’s paraphrase.

## Chain quality rules

### Strong links

- The source directly identifies the actor, action, date, and relationship.
- The source has authority appropriate to the claim and a clear publication identity.
- The link is supported by a document, record, dataset, direct observation, or attributable statement.
- A second source is genuinely independent or adds a distinct evidentiary layer.

### Weak links

- A search result, headline, repost, or social post is used as if it were the original source.
- A source says that an inquiry, allegation, or proposal exists, but the report writes it as a settled outcome.
- Several outlets repeat the same statement and are described as corroboration.
- A policy announcement is used to prove implementation or impact.
- Two events are adjacent in time and the report calls one the cause of the other without causal evidence.

### Required labels

Use labels such as `Verified fact`, `Reported claim`, `Official position`, `Allegation`, `Open investigation`, `Synthesis`, `Inference`, `Unknown`, and `Correction or update`. A chain should show where certainty changes rather than assigning one confidence score to the entire graph.

## Reusable tables

### Generic chain table

| Node or edge | Actor / role | Relationship | Date / status | Evidence | Gap or confidence |
|---|---|---|---|---|---|
| [Document, event, claim] | [Who] | [What link] | [When / current status] | [Inline source] | [What remains unknown] |

### Policy chain table

| Stage | Instrument or actor | Legal / institutional force | What it establishes | What it does not establish | Source |
|---|---|---|---|---|---|
| Origin | [Law, decision, program] | [Binding / proposed / etc.] | [Supported claim] | [Boundary] | [Inline source] |
| Implementation | [Regulator / provider / local body] | [Guidance / duty / practice] | [Supported claim] | [Boundary] | [Inline source] |
| Review | [Audit / court / evaluation] | [Finding / challenge / update] | [Supported claim] | [Boundary] | [Inline source] |

### News provenance table

| Time / stage | Source or actor | Role in the story | Direct evidence or attribution | Independent? | Status / limitation |
|---|---|---|---|---|---|
| [Time] | [Original source / outlet] | [Event / first report / response] | [What it directly supports] | [Yes / no / unclear] | [Gap or update] |

End every chain with a short **chain judgment**: which links are directly established, which are derivative, which are disputed, and what evidence would close the most important gap.
