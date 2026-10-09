# Literature-first re-entry screen: uncertainty and abstention

Date: 2026-10-09. Status: targeted screening, NOT novelty clearance or an experiment preregistration. The October 7 closure remains in force for the prior novel-method route. The user authorized a fresh literature investigation; no old results or manuscript are replaced.

## Finding

The broad proposal, abstain from deception deployment under uncertainty, is insufficiently distinct. Safe fallback, selective action, risk-aware engagement and partially observed planning have established prior art. A different cybersecurity application alone does not establish novelty. No compute experiment was launched during this screen.

## Primary-source evidence ledger

| Source | Evidence examined on October 9 | Coverage relevant to the candidate | What remains unchecked |
|---|---|---|---|
| [Adaptive Honeypot Engagement through Reinforcement Learning of Semi-Markov Decision Processes](https://arxiv.org/abs/1906.12182) | Author abstract page | Adaptive engagement with risk/cost considerations already exists | Full decision/action semantics and experiments need renewed full-text extraction |
| [Safe Policy Improvement with Baseline Bootstrapping](https://www.microsoft.com/en-us/research/publication/safe-policy-improvement-baseline-bootstrapping/) | Author institution publication page | Improvement relative to a baseline is established | Exact assumptions and applicability to sequential deception require full-text review |
| [Policy Learning with Abstention, v3](https://arxiv.org/abs/2510.19672v3) | Abstract and version history | Disagreement-based abstention, default/expert deferral, distributional robustness and safe improvement | Sequential endogenous attacker changes not resolved by abstract; venue comment is chronologically unusual, so do not assert venue without corroboration |
| [Non-Exchangeable Conformal Risk Control](https://arxiv.org/abs/2310.01262v2) | Abstract and version history | Weighted risk control under distribution drift | Inspect theorem assumptions and nonexchangeability penalty before claiming arbitrary adaptive-attacker validity |
| [CAP: Conformalized Abstention Policies](https://proceedings.mlr.press/v304/tayebati26a.html) | Official proceedings page | Context-dependent abstention and risk management are already studied outside cyber deception | Full selective-risk definition and calibration conditions require extraction |

Recent cyber leads also surfaced: Hawkeyes (10.1016/j.comnet.2025.111982), posterior-conditioned multi-agent cyber defense (10.1016/j.artint.2026.104606), and Co-ADAM (10.1038/s41598-026-60920-0). These remain leads, not verified exclusion evidence. Direct opening of the posterior-conditioned DOI failed in this session. Do not transfer search-snippet performance claims into the manuscript.

Queries covered cyber deception uncertainty/abstention, safe policy improvement and baseline bootstrapping, and nonexchangeable conformal risk control. This is a targeted public-web screen, not a systematic review or exhaustive search. Failure to find a matching paper is not proof of absence.

## Narrower candidate to assess, not a claimed gap

Working question: when defender interventions change later attacker behavior and some protected-asset outcomes arrive late or remain unobserved, what evidence permits a useful decision to deploy a candidate deception policy rather than retain a specified baseline?

The possible contribution is an assumption/identifiability boundary or a validated evaluation procedure, not a renamed abstention threshold. The earlier project already studied attacker memory and evaluation harm. To reopen method development, demonstrate an additional result caused specifically by outcome observation/delay, beyond adding another latent state to a POMDP.

Candidate hypotheses, conditional on a passed literature gate:
- H1: A naive risk certificate that omits unresolved outcomes can understate deployment harm under explicitly modeled outcome-dependent missingness. This is expected from missing-data theory and is not itself a novelty claim.
- H2: A specified conservative partial-identification rule can reduce false certifications while retaining nonzero deployment coverage against established missing-data and safe-improvement baselines. No such new rule or guarantee has yet been derived.
- Null/practical failure: equal-observation prior methods match the candidate, or useful deployment coverage collapses to zero. Preserve that result rather than relabeling it a discovery.

## Required next review before experiments

1. Read full texts for the five primary sources and trace their closest references on partial identification, informative censoring, delayed bandit feedback and safe off-policy evaluation.
2. Build an assumption matrix: unit of independence, action support, attacker memory, missingness mechanism, outcome delay, fallback action, marginal versus selective risk, and permitted adaptation.
3. State an explicit result or algorithmic distinction and map it against the repository's existing POMDP equivalence. If only state augmentation is needed, reject a new-method claim.
4. Reproduce the closest applicable comparator under its own assumptions before extending it. Freeze counterexamples, outcomes and comparisons before collection.

## Data and compute plan

Reuse the pinned ORNL Cyberwheel source and prior artifact manifests only as development infrastructure. Existing traces are not fresh validation data. No new dataset downloaded in this screen. Passive IDS CSVs and ordinary honeypot logs cannot identify intervention effects without suitable action/observation information. Before selecting public logs, verify license, action propensities, observation masks and protected-asset outcomes.

If a distinct contribution survives: generate reproducible open-testbed trajectories with observed-only decision histories, controlled outcome delays/missingness, held-out attacker families and independent trajectory clusters. Keep hidden states solely for oracle evaluation, never policy inputs. Compare no-change baseline, existing safe-improvement method under matched information, robust planning and any new candidate. Measure false certification, coverage, compromise, cost and uncertainty at the trajectory level.

Local work: literature, mathematical counterexamples, schema tests and small comparator reproduction. ASA-X: independent simulation replicas only after protocol freeze and live queue/resource verification. No HPC job submitted. A full ACM/Overleaf manuscript is premature at this gate.

## Decision

Reject the broad novelty framing. Continue only the assumption-level literature assessment of delayed/partially observed outcomes. Novelty remains unestablished. Do not reopen the old experiment loop merely because compute is available.
