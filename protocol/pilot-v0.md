# Development pilot and future experiment contract

This is a development plan, not a preregistered confirmatory study. Changes after viewing pilot results must be disclosed in a separately frozen main protocol.

## First diagnostic

Use a fully specified two-state illustrative model to verify that resetting attacker knowledge can change a policy ranking. This is a constructed software/estimand check, not Cyberwheel, public empirical data, a learned attacker or a novel scientific finding.

State 0 means unaware; state 1 means aware. A decoy action protects with probabilities 0.9 and 0.1 respectively. The alternative protects with probability 0.5 in either state. A decoy causes an unaware attacker to become aware with probability 0.4. The alternative causes an aware attacker to forget with probability 0.05. All other transitions retain state. Compare independent action probabilities 0.1, 0.5 and 0.9, starting unaware, for 100 encounters. Compute expected mean protection under reset-every-encounter and persistent-memory models. Independently check forward propagation against recursive backward value calculation, including zero learning and one-encounter controls. No fitted parameters, OPE claims, uncertainty intervals or empirical generalization.

## Simulator pilot after the gate

Cyberwheel is the first candidate, pinned by commit. Use simulator-only interfaces, no emulator or external targets. Add a distinct attacker-memory wrapper with auditable serialization. Network reset and attacker-memory reset are separate operations. First use transparent fixed and observation-driven adaptation policies, rather than generating executable attack programs.

Log episode and persistent-world IDs, seeds, step, observable history digest, policy revision, available-action mask, selected action, conditional selection probability after masking, attacker-memory revision, raw asset compromise/impact, decoy events, cost, truncation and errors. Privileged state goes only to a separately labeled oracle record. Capture failed and infeasible actions. A decoy interaction is not asset protection.

Candidate defender policies: no-deception baseline, random deployment, fixed-budget rules, and a learned policy frozen before evaluation. Compare equal action budgets. Build logging support deliberately; probability zero for a target action requires abstention or a clearly bounded estimand, never an invented propensity.

Baselines: matched-history online Monte Carlo reference; importance sampling and self-normalized importance sampling; an explicitly history-aware model baseline; OPEN where its assumptions are satisfied. Doubly robust and nonstationary estimators require implementation and assumption checks before inclusion. Do not label a generic regression as OPEN.

Separate development, policy training, estimator fitting, selection and final testing. Hold out independent attacker-world trajectories and network scenarios, not random transitions from a shared history. Maintain separate randomness streams for defender actions, attacker behavior and environment outcomes. Reset versus persistent memory is a paired intervention, not two independent samples.

Primary outcomes: selected-policy regret relative to an online reference with uncertainty, false selection of a harmful policy, and abstention frequency. Secondary: estimation error, interval coverage, importance-weight support/effective sample size, protected-asset compromise and action cost. Measure online reference Monte Carlo error. Cluster resampling by independent attacker world, not individual transitions.

Hypotheses to refine before freezing: H1, resetting knowledge changes policy rankings in some tested regimes; H2, adequate action support alone does not ensure accurate prediction under a changed attacker-learning law; H3, adaptation-aware evaluation or abstention improves selection reliability at a measurable loss of decision coverage. These are candidate tests, not claims of novel theory or predicted victories.

## Data and compute

Public simulator source plus reproducibly generated, synthetic interaction data is the primary route. No suitable public defender-trajectory dataset with all required propensities and persistent-state boundaries has yet been verified. IDS classification CSVs do not supply intervention outcomes. Public Trident data remain a candidate only after schema, access and license checks.

Local PC: source audit, analytical controls, small simulator smoke tests and estimator verification. ASA-X: independent trajectory batches, policy training and held-out evaluation only after local measurement. CPU workers may dominate simulator throughput; reserve GPU training only if profiling supports it. Do not request maximal resources simply because available.

ASA-X queue limits, GPU type/memory, software, storage, array syntax and scheduler access must be refreshed live. Historical queue values are not current verification. No HPC job is authorized by an unverified resource template alone, and none has been submitted for this project.

Main sample sizes and resource requests remain unset until pilot variance, runtime and dependency checks are available. Freeze them before confirmatory collection; do not choose seeds or budgets to manufacture significance.
