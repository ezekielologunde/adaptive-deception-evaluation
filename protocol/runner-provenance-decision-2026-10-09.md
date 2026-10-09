# Runner provenance and re-entry decision

Date: 2026-10-09. This audit checks existing evidence; it is not a new confirmatory experiment.

## Executed validation

`python src/audit_outcome_provenance.py` independently recomputes saved impact sets and protection values from each episode's trace. All 1,024 world files, 8,192 episodes and 327,680 trace steps were examined with zero discrepancies. Input SHA-256 values and counts are in `analysis/outcome-provenance-audit.json`.

This confirms arithmetic consistency only. The trace and reported endpoint share simulator provenance. This does not validate real-world compromise, independent sensing, or detector visibility.

## Actual source path

1. `src/simulator_smoke.py:make_environment` loads `art_agent_vs_rl_blue.yaml`, sets 40 steps, and creates `CyberwheelRL(..., evaluation=True)`.
2. The pinned configuration specifies `RLReward`, `reward_red_delay`, `reward_decoy_hits`, and `perfect_detector.yaml`. No training is invoked by this audit.
3. `src/memory_study.py:run_world` chooses a placement category from fixed probabilities once per encounter, deploys for three steps, then uses no-op actions. Returned observations and rewards are discarded. Thus these defender policies are not observation-responsive learned policies, despite the environment's RL naming.
4. `CyberwheelRL.step` writes red action, target and success directly from `red_agent_result` into evaluation `info`. The runner labels these fields `observed`, but that name does not establish defender visibility.
5. Protection equals one minus the fraction of original server targets with a successful native impact in the trace. Reward is not substituted for this endpoint. Attacker-memory updates also use the action-result fields.

Interpretation: the old study evaluates stochastic placement under a specified attacker-memory heuristic. It does not evaluate adaptive sensing, incomplete defender telemetry or retrospective forensic recovery. Existing data must not be relabeled to imply those capabilities. The original artifacts remain unchanged.

## Additional overlap

[Morris, Procter and Wallbank (2025), Evaluating Reinforcement Learning Agents for Autonomous Cyber Defence](https://doi.org/10.1002/ail2.125), introduction and sections 2.3-2.3.1, already distinguishes defensive effectiveness from reward and includes information-availability perturbations in its evaluation design. Those passages were inspected in publisher full text. Therefore adding noisy observations and a separate protection metric is not, by itself, a novel research question. This review does not claim every proposed missing-outcome design is covered by that paper.

## Completed decision for this re-entry attempt

The generic method proposals fail the contribution gate: abstention, audit recovery, baseline fallback and partial-observation robustness have direct prior art. The present runner also cannot test the suggested responsive-defender mechanism. Accordingly, this re-entry attempt does not justify a new method paper or HPC campaign.

The next useful activity is topic selection across alternatives, rather than another masking sweep in this runner. A successor must have: a full-text-supported unresolved question; suitable public evidence or an explicit open-testbed mechanism; a comparison against the strongest matching method; an observable falsification criterion; and a feasible path beyond a renamed established result. This is a change in research direction, not a claim that all adaptive-deception research is exhausted.
