# Outcome recovery: overlap and testbed gate

Date: 2026-10-09. Status: targeted literature and source audit. No experiments or new-method claims.

## Additional closest work

[Coppock, Gerber, Green and Kern (2017)](https://alexandercoppock.com/coppock_etal_2017.pdf), DOI 10.1017/pan.2016.6, sections 2.1-2.4: randomized follow-up of initially missing outcomes, with bounds when follow-up also fails, already addresses the proposed basic recovery design. Their outcome-stability condition matters: follow-up must measure the same outcome, not alter it. Population generalization is a separate problem. Full-text setup and derivation passages were inspected; no numerical reproduction was performed.

[Levis et al. (2024)](https://doi.org/10.1002/sim.10298), sections 3.1-3.2 and discussion: identification requires noninformative successful second-stage recovery conditional on observed covariates and treatment, plus positive recovery probabilities. Random selection alone does not ensure noninformative recovery failure. The paper explicitly identifies resource allocation as future work. Its research data are not shared. Publisher full text was inspected after the PMC route returned a browser challenge.

[Active Offline Policy Selection (2021)](https://proceedings.neurips.cc/paper_files/paper/2021/file/cec2346566ba8ecd04bfd992fd193fb3-Paper.pdf) addresses budgeted additional policy evaluation. This differs from recovering outcomes of completed episodes, but means generic active evaluation is not a new framing. Abstract refreshed here; the repository contains the earlier reduced reference execution.

## Consequence

The simple randomized-audit candidate maps to established two-phase sampling. Adding missing follow-up labels, sensitivity bounds, or a cybersecurity setting does not by itself establish a distinct method. Do not promote the candidate protocol in the preceding assumption matrix to a cleared experiment plan.

## Testbed source inspection

Verified local Cyberwheel HEAD: `6e535b50eea991ed48bb9eeb46b4b267090cc897`. MIT license header inspected. No code copied or executed during this audit.

- `cyberwheel/detectors/detectors/example_detectors.py`: includes whole-batch random alert retention, decoy-only filtering, and a perfect-alert pass-through. These demonstrate controllable observations, not a validated model of operational log loss.
- `cyberwheel/reward/decoy_reward.py`: contains an alert-dependent shaped reward. Its presence does not prove that our selected runner uses it.
- `cyberwheel/cyberwheel_envs/cyberwheel_rl.py` uses `RLReward`; `cyberwheel/reward/rl_reward.py` selects reward functions through configuration. Therefore auditing a legacy reward class alone cannot establish the current experiment's outcome semantics.

Three channels must remain separate: observations available to the defender, training reward, and independently defined protected-asset harm. Removing alerts can change defender actions and harm. Masking an already completed episode's outcome only changes evaluation evidence. These are different interventions and must not be pooled.

## Candidate empirical contribution requirements

A useful study would need evidence that a realistic observation or recovery mechanism changes a substantive defense decision in a way existing evaluations have not characterized. An arbitrary masking curve applied to simulator truth is only a methodological illustration.

Required evidence before revival:
1. Trace the actual runner and configured reward functions to an explicit asset-harm endpoint.
2. Identify a defensible mechanism for telemetry loss and independent recovery, with operational evidence and public provenance. Do not equate perfect simulator state access with deployable forensic recovery.
3. Compare closest cyber evaluation studies on this exact endpoint and mechanism. Lack of a keyword match is not evidence of a gap.
4. Specify the additional empirical knowledge sought and the result that would reject it. Use established estimators as baselines rather than rename them.

Decision: no-go for the generic new estimator or audit-method claim. Keep the narrower empirical possibility unapproved pending these requirements. No HPC launch, new dataset claim, or manuscript promotion is justified by this audit.
