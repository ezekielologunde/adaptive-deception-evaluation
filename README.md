# Adaptive deception and policy evaluation

**Current disposition: closed for active novel-method development, October 7, 2026.** The [final contribution assessment](protocol/final-contribution-gate.md) did not establish a distinct method beyond existing partially observable planning. The agreed stopping rule was applied before another experiment. This does not prove that no future contribution is possible. The simulator study, reduced A-OPS reproduction, data, and earlier bounded manuscript remain available as research/portfolio artifacts. No novel-algorithm, journal-readiness, or acceptance claim is made. The GitHub repository remains editable.

## Preserved milestones

**Runner provenance audit, October 9:** [all 8,192 saved episodes passed endpoint recomputation](protocol/runner-provenance-decision-2026-10-09.md). This is internal consistency, not new validation data. The placement policies ignore returned observations and use simulator evaluation metadata for scoring, so the old results cannot support the proposed missing-telemetry study. This re-entry attempt did not clear the contribution gate.

**October 9 literature re-entry:** the [assumption matrix](protocol/abstention-fulltext-assumption-matrix-2026-10-09.md) and [outcome-recovery audit](protocol/audit-recovery-overlap-2026-10-09.md) identify substantial overlap with abstention, missing-outcome evaluation and two-phase sampling. The exact missing-outcome example is a feasibility illustration, not a discovery. The generic new-method route remains closed; the narrower empirical candidate has not passed its evidence gate. No new HPC experiment was launched.

**Reference milestone:** [A-OPS now executes in an isolated, version-pinned environment](analysis/aops-reference-report.md). Three 20-round experiments, a five-round pilot, and a fresh-process replay completed. All 280 recorded pulls were audited and the replay matched exactly. This is a reduced reference execution, not full Figure 14 reproduction. A mathematical discrepancy in the upstream independent-arm comparator is documented separately; the GP posterior checks passed. No new-method superiority or novelty is established.

**Current research, October 7: active evaluation under attacker conditioning.** A new 108-case exact diagnostic and 864-world Cyberwheel development study are complete. Established Bayesian planning solves the constructed diagnostic; no new algorithm is claimed. Prior evaluation reduced subsequent protection in all 24 retained-memory prefix comparisons, while 192 reset-memory trace controls matched exactly. These are related development comparisons, not independent discoveries. Test-order differences remain uncertain.

Read the [research decision](protocol/active-evidence-research-decision.md), [closest prior art](protocol/active-evidence-prior-art.md), [exact diagnostic](analysis/active-evidence-screen-report.md), and [native carryover report](analysis/carryover-order-report.md). The public A-OPS example dataset, sampling interface, and reduced learning execution have been audited. The candidate contribution concerns useful, harm-aware evaluation with hidden attacker conditioning; novelty remains unestablished. The earlier manuscript below is preserved separately.

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
