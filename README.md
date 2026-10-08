# Adaptive deception and policy evaluation

**Status: completed bounded simulator study and full research draft.** A frozen validation collected 1,024 worlds, 8,192 encounters, and 327,680 steps with no failed worlds. The highest online policy mean changed from DMZ-favoring placement under reset memory to user-subnet-favoring placement under retained memory in both supplied networks. The predeclared offline evidence rule abstained in all four settings. This is an empirical evaluation artifact, not a new estimator or a production defense claim.

Read the [manuscript source](paper/main.tex), [numerical results](analysis/validation-summary.json), [fixed protocol](protocol/validation-v1.md), [verification](analysis/verification.json), and [reproduction instructions](REPRODUCE.md). The [delivery folder](deliverables/) holds the ACM PDF, TeX, and Overleaf ZIP. Full generated traces are in analysis/validation-v1; the smaller development population remains separate.

The [updated overlap review](protocol/literature-followup.md) explains the contribution boundary and unresolved journal-readiness gaps. No exclusive novelty, peer review, acceptance, or journal submission is asserted. Independent review, additional attacker families, and repeated logging populations remain important before claiming a general benchmark contribution.

[Research protocol and prior-art leads](protocol/research-plan.md). This plan comes from the October 4, 2026 independent research portfolio. Its literature assessment must be refreshed before implementation and submission.

## Research identity and publication route

Author: **Ezekiel Ologunde**. Affiliation: **Independent Researcher**, with no institutional affiliation. Author email: ologunde@bu.edu. Location: Boston, MA, USA. No corresponding-author designation. Intended route: a suitable ACM journal, selected after assessing the completed contribution. No journal has accepted this work and no publisher metadata or DOI is assigned.

## Repository workflow

Keep research questions and hypotheses in `protocol/`; put code in `src/`, tests in `tests/`, and analyses in `analysis/`. Store redistributable datasets with provenance in `data/`, including source URL, retrieval date, version, license, SHA-256, schema, and role in the study. For restricted or large data, publish an acquisition script and manifest instead of copying files. Never commit credentials, private participant records, or copyrighted downloaded papers.

Freeze each experimental plan and code revision before collection. Retain failed and excluded runs with reasons. Publish analysis and result artifacts as work progresses. Keep manuscript drafts in `paper/`, clearly versioned; deposit the author-permitted final paper after journal-policy review. A planned experiment is not a result, and public code is not peer-reviewed acceptance.

Original work is intentionally unlicensed pending an author decision. Preserve applicable third-party notices. No dataset or final paper is claimed to exist merely because its directory is present.
