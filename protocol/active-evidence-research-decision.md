# Research decision after the active-evidence screens

Date: 2026-10-07. The user authorized continued research focused on an actual new contribution. The previous five-page manuscript is preserved as preliminary work; it is not upgraded to a novel-method paper.

## What has been eliminated

Do not develop a generic planner that trades off information and attacker learning and call that novel. It reduces to established Bayesian dual control when the state/model is known. Do not use low conditional selection regret alone: a test can damage the comparator policies and make choosing among them look easier. That decomposition is an audit device, not a claimed new regret theorem. Do not claim a better test ordering from the small native pilot: order contrasts are uncertain.

The constructed 108-case screen and the 864-world native study are distinct. The former assumes damage and proves only implementation properties by exact enumeration. The latter measures outcomes in Cyberwheel with reset, count, and decaying count memory. Both are development evidence. No held-out novelty validation or published-method reproduction has been completed in this phase.

## Current research question

Can a defender decide whether to collect another policy-evaluation episode using observable telemetry when the attacker's cross-policy conditioning is hidden, while retaining useful policy-selection accuracy and limiting harm to subsequent deployment?

The potential contribution must be an identifiable improvement under imperfect knowledge, such as a justified uncertainty bound or an efficient acquisition method with an explicit approximation guarantee. A new cyber example of a known POMDP solution is insufficient. At present this is a candidate question, not a cleared novelty claim.

## Formal target for a proposed method

Let h be the observed history and b the posterior or compatible-model set for hidden attacker state. An acquisition action a produces observation y and changes hidden state m to m'. A stop decision selects a deployment policy pi. Compare expected cumulative acquisition loss plus deployment loss over a prespecified remaining horizon. Keep the no-testing counterfactual, reached-state oracle selection regret, and irreversible conditioning loss separate in reporting. Without restrictions on the hidden dynamics, a universal guarantee is not credible; any claim must state a finite model class, mixing/forgetting restriction, or calibrated transition-error assumption.

The exact screen supplies the finite known-model Bayesian oracle and a standard one-step approximation. A proposed new method must be distinguished from these mathematically before implementation. When memory is observable, state augmentation is a strong baseline. When memory is hidden, model fitting must use only defender-visible telemetry and training seeds, never simulator oracle labels used for scoring.

## Required next comparison and stopping criteria

1. Obtain and reproduce the published A-OPS reference on its own fixed-value setting before adapting it. Record deviations when persistent state is added; do not call a surrogate or ablation its reproduction.
2. Compare against state-aware Bayesian/model-predictive control with matched model knowledge, plus a robust or ensemble version under misspecification. Search robust dual control and active testing with hidden dynamics before claiming a new acquisition rule.
3. Fit conditioning models on an explicitly separate development corpus. Hold out network configurations and an attacker mechanism, not only random seeds. Existing count and decaying-count rules share a mechanism and do not constitute broad attacker diversity.
4. Prespecify total deployment horizon, acquisition budget, harm metric, model-mismatch levels, and independent logging populations. Report selection utility and harm jointly; never reward a method simply for abstaining everywhere.
5. Stop the algorithmic novelty route if the proposed method is equivalent to an existing planner, improves only against stationary/uniform baselines, uses oracle memory unavailable to competitors, or loses its advantage under model mismatch. Preserve replication results but do not produce another nominally new paper.

No final paper or large HPC sweep should substitute for passing this gate. The measured studies fit local CPU resources. HPC becomes useful only for a justified multi-model, multi-seed evaluation, not as evidence of novelty.

## Reference acquisition completed

Update: reduced reference execution is now complete. See analysis/aops-reference-report.md. Three 20-round runs and an exact pilot replay passed trajectory audits. A source discrepancy in the independent-arm conditional scale was isolated; leave reference outcomes unchanged and require a corrected sensitivity baseline before comparative claims. GP math checks passed. The task below is partially satisfied at reduced scale, not at full Figure14 scale.

The authors' public A-OPS repository was acquired at commit 5c7b24515adadbaf89feb84232190bad96221c04. Its 76-policy cartpole example contains 380,000 return samples and actions on 1,000 states. Restricted loading, schema/finiteness checks, source hashes, and 1,520 exact sampling-interface comparisons passed (data/aops-source-audit.json). This is a reliable reference acquisition, not a cybersecurity dataset or algorithm reproduction. The notebook uses older TensorFlow dependencies and seeds NumPy but not Python's policy-subset sampling. A reproducible reference run needs an isolated environment and a documented seed deviation. Full GP fitting and Figure 14 reproduction remain outstanding.
