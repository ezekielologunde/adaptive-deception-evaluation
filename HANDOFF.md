# Research handoff

## Current disposition: novel-method route closed

The user approved one final bounded contribution gate and closure if it failed. The written gate is protocol/final-contribution-gate.md. The proposed hidden-conditioning acquisition rule maps to established Bayesian belief-state planning; robustness variants overlap robust POMDP literature. No distinct approximation, guarantee, identification result, or validated empirical contribution has been specified. This is a failure to establish the candidate's contribution, not proof that every future approach is impossible. No held-out trial was run because the agreed prerequisite failed. Preserve all prior code/data/manuscripts; do not silently resume experiments or call this publication-ready. The GitHub repository stays editable. Reopening requires the concrete evidence listed in the decision.

Next unstarted topic in portfolio order: zkp-remediation-assurance. It is still a proposal, with novelty unchecked. Start there with threat model and closest literature, not a manuscript. Older "next" instructions below are historical and superseded by this disposition.

## Historical milestones

## Newest: published reference execution completed at reduced scale

Read analysis/aops-reference-report.md and protocol/aops-reference-v1.md. The unchanged upstream A-OPS GP algorithm ran in .venv-aops (Python 3.9.25, TF 2.7.0, TFP .14.1, Sonnet2, NumPy1.21.4). Main simulator environment was preserved. Three 20-round/50-policy development runs, one five-round pilot, and its fresh-process repeat completed with no recorded failures. All 280 pulls/regrets verified; replay exactly matches. Fixed-hyperparameter GP math checked independently. All 1,000 optimizer iterations retained. The cold pilot triggered the frozen reduced-scale rule; do not claim full Figure14 reproduction.

Important source caveat: SingleBayesArm._sigma2_cond_on_mu omits sample count in the residual scale relative to its documented iid Gaussian model. Six multiple-observation checks disagree; three single-observation controls agree. Unchanged reference results preserve this behavior. This concerns independent-arm comparators, not the separate GP. Do not claim the paper is invalid or that this discrepancy is our novel contribution. A future ranking must include a labeled corrected sensitivity version and matched random streams. Source/raw audits and report are saved. Dependency lock CRLF byte preservation was corrected in dbda717 after the freeze; versions never changed.

Next scientific work: formalize a specific hidden-conditioning assumption and decision target, compare with robust dual control and ROGUE (additional primary-source overlaps now documented), and develop only if a substantive distinction survives. A 2026 under-review safe dual-control paper already combines information value and harm budgets under perfectly observed state. Hidden state alone is a POMDP distinction, not novelty proof. No new manuscript or HPC sweep before this contribution test.

## Latest phase, October 7: active evidence collection

Read protocol/active-evidence-research-decision.md first. The generic information-versus-conditioning planner is established dual control, not a new method. Completed 108 exact constructed cases (540 method cases), independently enumerating 981,864 type-conditioned policy vectors to verify all 108 optima. Completed 864 native Cyberwheel worlds, 230,400 steps, zero failures, across reset/count/decaying-count memory. All 24 retained-memory prefix-vs-none means were negative; order differences were uncertain. Reset controls matched in 192 full suffix trace comparisons. Development evidence only; no held-out novelty claim.

Frozen commits: 70484f7 (exact screen) and 78c46ab (native order screen). Do not edit frozen runners or protocols. Results and independent checks are in analysis/active-evidence-* and analysis/carryover-order-*. Preserve the prior manuscript/package.

Acquired google-deepmind/active_ops at 5c7b24515adadbaf89feb84232190bad96221c04 under ignored data/source-cache. Source/data hashes and attribution: data/aops-source-audit.json. Restricted numeric unpickler audited 76 policies, 380,000 rewards, and 1,000 states of actions. All 1,520 reference sampling checks matched. This is not A-OPS algorithm reproduction. Next: isolate its older TensorFlow dependencies, freeze a reference execution protocol, explicitly seed Python and NumPy (upstream seeds only NumPy), and reproduce the baseline before adapting anything. A reduced pilot must not be described as full Figure 14 reproduction. Do not change the main simulator environment. Require a mathematical distinction from robust/dual-control planning before inventing an acquisition method or launching an HPC sweep.

## Earlier manuscript phase

Active project: adaptive deception policy evaluation. Author: Ezekiel Ologunde, Independent Researcher, Boston, MA, USA; ologunde@bu.edu. No corresponding-author designation. Original work remains unlicensed.

User authorized proceeding with the recommended next direction. The prior autonomous-pentest-authorization study is complete as a bounded replication and remains separate. Do not manufacture novelty by renaming an established method or adding arbitrary datasets.

Completed: fixed 1,024-world validation in pinned Cyberwheel, 8,192 encounters, 327,680 native simulator steps, zero failed worlds. Collection took approximately 209 seconds on four local CPU processes. Preserve the frozen raw data and code. The earlier 128-world development study, 36-case constructed diagnostic, failed import smoke test, and limited OPEN interface controls remain separate evidence.

Result: DMZ preference leads with reset memory; user-subnet preference leads with retained memory on both supplied networks. Prefix SN point-estimate winners match the highest online means, but the predeclared frequency/ESS gate abstains in every setting. The four settings are related, not independent estimates of selection reliability.

Verification: 1,025 raw/freeze hashes, 327,680 traced steps, 24 scalar-replicated estimates, five detected semantic mutations, 64 paired development identity-control trajectories, and one exact fresh-process world replay. Paper tables and plots have separate parsing checks. See analysis/ and deliverables/validation.json for final build status.

Research priorities before a general journal contribution: independent logging datasets for selection error/coverage/regret, at least two additional attacker-memory mechanisms, a validated comparator with matched estimand, and completion of closest-artifact full-text review. Freeze any new protocol and seeds before additional collection. Do not inflate novelty by adding arbitrary models, industries, or more compute. Continue autonomously within authorized work and ask only for genuinely missing decisions.

Source checkouts are ignored under data/source-cache. Pinned revisions and hashes are in data/source-audit-v0.json. No public interaction dataset with the required defender propensities has yet been validated. Use reproducible generated data under an open testbed if the data audit remains negative.

Main artifact: paper/main.tex and the generated delivery trio. The manuscript is a completed bounded research draft, not an asserted journal-ready novel algorithm. No HPC job or journal submission occurred. The built-in compiler failed during sandbox setup; use the isolated compiler receipt and final clean rebuild checks. Keep other open manuscript tabs untouched.

Read protocol/literature-followup.md for deviations from the initial feasibility gate. CoADAM artifact reviewed, publisher full text inaccessible. OPEN was excluded before validation due to incomplete interface reproduction and a different estimand, not declared defective. Source checkouts are ignored; full tracked-file hashes and exact revisions are in data/runtime-provenance.json.
