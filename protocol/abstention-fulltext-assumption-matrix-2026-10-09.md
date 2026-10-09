# Assumption audit and contribution decision

Date: 2026-10-09. Targeted review, not exhaustive systematic review. No novelty established. This extends the re-entry screen; the October 7 closure of the old method remains valid.

## Closest-work matrix

| Primary source | Evidence inspected | Relevant assumptions or scope | Consequence for our proposal |
|---|---|---|---|
| [Policy Learning with Abstention](https://arxiv.org/html/2510.19672v3), section 2 | Full-text setup and theorem passages | IID observational samples, unconfoundedness, overlap, bounded outcomes, finite policy complexity; nuisance estimation separation | Abstention and default-policy improvement are established. Sequential attacker adaptation requires additional justification. |
| [Non-Exchangeable Conformal Risk Control](https://arxiv.org/html/2310.01262v2), section 3 | Full-text bound and weighting discussion | Bounded monotone loss; expected-risk bound contains a weighted distribution-shift penalty | Does not supply unconditional nominal-risk control under arbitrary attacker changes. Expected risk and risk conditional on deployment must be distinguished. |
| [Offline Policy Evaluation and Optimization Under Confounding](https://proceedings.mlr.press/v238/kausik24a.html) | PDF setup and main results | Distinguishes memoryless, general-memory, and global confounders; sensitivity and additional estimation assumptions | Attacker memory alone is not a new contribution. Specify which dependence class applies. |
| [Off-Policy Evaluation for Missingness-Aware Policies](https://proceedings.mlr.press/v306/wei26v.html), [full text](https://arxiv.org/html/2606.20206v1), sections 2, 3, 7 | Assumptions, identification argument, limitations | IID finite-horizon trajectories, structured missingness, future-state shadow information, positivity and bridge/completeness requirements | Direct overlap with missing-reward evaluation. Sensitivity to these assumptions is already named as future work. Merely implementing that suggestion is not a first-method claim. |
| [SPIBB](https://proceedings.mlr.press/v97/laroche19a/laroche19a.pdf), sections 2.1-2.3 | Full-text definitions and safety constraints | Finite discounted MDP, bounded rewards, logged transitions, baseline policy, statistical uncertainty sets | Baseline fallback and approximate improvement are established. Missing outcomes require a justified estimator, not silent deletion. |
| [Off-Policy Evaluation under Nonignorable Missing Data](https://proceedings.mlr.press/v267/wang25dt.html) | Official abstract; linked PDF retrieval failed | Monotone informative missingness, weighted estimation and inference | Bias from informative missingness is already studied. Exact identification assumptions remain to be extracted from full text. |
| [CAP](https://proceedings.mlr.press/v304/tayebati26a.html) | Official proceedings abstract only | Learned context-dependent abstention in LLM/VLM prediction | Generic learned abstention is occupied. Full calibration assumptions remain unchecked. Bibliographic year is 2025 despite the 26a URL suffix. |

Unreviewed passages are not evidence of absence. No reproduction of these methods has been completed in this review. Recent cyber-specific leads in the earlier screen remain pending. Search terms included off-policy evaluation audit missing outcomes, policy evaluation missing not at random sensitivity analysis, and baseline bootstrapping.

## Exact feasibility diagnostic

Run `python src/check_missing_outcome_identifiability.py` from this repository. Output: `analysis/missing-outcome-identifiability-check.json`.

Two constructed binary-outcome populations have identical observed masses: harmful and observed = 0.05, safe and observed = 0.45, missing = 0.50. True harm is 0.10 in world A and 0.40 in world B. With a known baseline risk of 0.20, the correct decision differs. Observation probabilities are strictly positive in both populations. Complete-case harm is 0.10 in both.

This is an exact-arithmetic illustration of established nonidentification, not a novel theorem or experimental result. Without further restrictions the binary risk interval is [0.05, 0.55]. Under strict positivity, the endpoints are limiting bounds rather than necessarily attainable. No informative proxy, known observation mechanism, or recovered audit labels is supplied. Therefore it does not refute shadow-variable methods under their assumptions. Equal observed logs cannot distinguish these two constructed worlds.

## Decision

Reject a new-method claim for generic uncertainty-aware deception, missing-outcome abstention, or an existing method applied to honeypot logs. Keep the old research artifacts intact. Do not launch HPC experiments or prepare a positive-results manuscript from this screen.

The defensible next candidate is an empirical question: **How much independently recovered outcome evidence is needed to make deception-policy deployment decisions reliable when telemetry loss depends on compromise?** This is a candidate study, not a cleared literature gap. Randomized auditing and weighting are established ideas, and their combination is not itself claimed as novel.

## Candidate protocol specification, conditional on clearance

- Population: independently reset open-testbed episodes; test generalization across separately held-out attacker families and topologies. State the simulator-to-real-world limitation explicitly.
- Intervention: a frozen defender policy versus a frozen baseline. Use randomized assignment for the initial study rather than falsely treating passive IDS records as causal intervention data.
- Outcome: protected-asset compromise by a fixed horizon. Decoy engagement is a secondary outcome, not a substitute for asset protection.
- Observation: instrument outcome-dependent telemetry loss separately from compromise. Simulator truth is available only to scoring and to explicitly budgeted audits. Audits recover labels after the episode and cannot affect the attack trajectory.
- Estimand: difference in episode compromise probability between policy and baseline, within each declared environment distribution. Audit recovery fixes outcome information, not action confounding or out-of-support policy evaluation.
- Comparators: complete-case estimate (diagnostic only), worst-case missing-outcome bounds, random-audit inverse-probability estimator, and applicable published missing-outcome estimator after faithful reproduction. Compare with the same audit budget and information.
- Primary outputs: false certification of a harmful policy, fraction of policies certified, interval coverage, audit cost, and decision error. Report independent episode counts and uncertainty, not transition counts as independent samples.
- Conditions: sweep missingness strength, audit budget, proxy informativeness, and held-out attacker behavior. Freeze a discovery/confirmation split before observing comparisons. Account for selection across candidate policies.
- Rejection: if established equal-information methods resolve the question, or only generic MNAR bias appears, record a replication or engineering result and abandon the novelty claim. Do not search seeds for significance.

## Remaining gates

1. Review active outcome acquisition, two-phase sampling, randomized audits, and safe-policy evaluation together. Extract closest full-text assumptions, including the unavailable 2025 PDF.
2. Verify the open testbed exposes a meaningful protected-asset outcome and a realistic observation channel. Verify source license and pinned revision before copying anything.
3. State a concrete unresolved empirical question compared with existing experiments. A new dataset name is insufficient.
4. Freeze protocol, sample-size rationale, baseline implementation checks and test split before substantive experiments. Local feasibility work first; ASA-X only if the frozen workload benefits from it.

No new data was downloaded and no HPC job was submitted. This document is a contribution gate and candidate specification, not a publication-ready finding.
