# Feasibility assessment, 2026-10-07

Decision: advance to a bounded simulator/estimator pilot, not main collection or a novelty claim. The development protocol and diagnostic implementation were committed at d105baeb9060269e548ef4983b04737bbe9c1ec7 before the diagnostic ran.

## Completed

- Located and reused the existing roadmap repository rather than creating a duplicate project.
- Refreshed the initial primary-literature comparison. Identified OPEN as a necessary prior-art baseline and adaptive-adversary benchmarks as substantial overlap.
- Acquired two pinned public source checkouts and recorded 14 canonical Git-file hashes. No third-party source was executed or republished.
- Inspected Cyberwheel's environment step/reset and ART-agent reset. The selected reset path clears history. The evaluation info exposes action/outcome fields; it does not itself provide the logging policy's conditional probabilities. A wrapper must compute those probabilities when sampling, not infer them later from action frequency.
- Inspected OPEN's input contract: its hybrid estimator consumes trajectory-by-horizon arrays of importance ratios and rewards. Its README paths omit the Src/ prefix; the checked implementation is Src/OPE/hybrid.py. It must be reproduced as published before use as a named comparator.
- Ran 36 analytical cases using independently written forward and backward recursions. All matched to numerical tolerance; one-encounter and zero-learning controls passed. Raw outputs and source/protocol hashes are in memory-diagnostic-v0.json.

## Interpretation of the diagnostic

The illustrative model can reverse the ranking of frequent and infrequent decoy use when knowledge persists. This follows from explicitly chosen transition/reward parameters. It is a check that the intended comparison is mathematically distinct, not evidence about real attackers, learned policies, Cyberwheel performance or a novel phenomenon. Do not use its numbers as experimental findings in a journal manuscript.

## Unresolved gates

1. Complete the closest-paper review, especially Co-ADAM (full-page retrieval failed) and safe/performative policy selection. No claim that the exact combination is absent from the literature is justified yet.
2. Install and smoke-test the pinned simulator in an isolated Python 3.10 environment. The source declares Python ~3.10; requirements.txt pins gymnasium 0.28.1 while pyproject.toml requests ^1.1.0. Resolve and record the actual compatible environment rather than silently mixing both specifications. No working installation is claimed.
3. Implement a separate, observable-history-driven persistent-memory wrapper and demonstrate independent serialization, resets and policy-support logging. Do not add hidden-state oracle information to candidate estimators.
4. Reproduce OPEN's reference behavior and explicitly check whether the chosen attacker update rule satisfies its structural assumptions. If not, label the setting a stress test rather than an unfair baseline failure.
5. Obtain pilot runtime and variability before choosing sample sizes, HPC allocations or a final protocol. ASA-X has not been queried or used in this project.

The remaining gate is substantive. A full manuscript or large training sweep now would be premature. The prospective contribution is reliable selection and calibrated abstention under a specified deployment history, if existing methods and benchmarks leave that question unresolved.
