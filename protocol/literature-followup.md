# Prior-art follow-up and publication boundary

Review date: 2026-10-07. Targeted primary-source review, not a systematic review or proof of novelty.

The original research-plan and decision document are preserved as historical records. Two feasibility gates remained incomplete when the fixed validation proceeded: full publisher text for CoADAM could not be retrieved, and OPEN interface controls were insufficient reproduction. The study was narrowed to an audited empirical artifact, not cleared as a new estimation method.

| Source | Evidence inspected | Overlap and boundary |
|---|---|---|
| [OPEN, NeurIPS 2022](https://proceedings.neurips.cc/paper_files/paper/2022/file/3bf80b34f731313b8292f4578e820c90-Paper-Conference.pdf) | Primary PDF and pinned activeNS source; interface controls in analysis/open-controls-v0.json | Action-dependent nonstationarity is established. Its future forecasting target differs from the finite-world mean here. No reproduced published performance comparison. |
| [Liu et al., AISTATS 2023](https://proceedings.mlr.press/v206/liu23d.html) | Proceedings abstract and metadata | Regression-assisted DR and historical-data reuse are established; not implemented in this study. |
| [Vo et al., ICML 2026](https://proceedings.mlr.press/v306/vo26b.html) | Primary proceedings and linked formulation | Strategic response and policy-dependent covariate shift already addressed. One-shot disclosure setting differs from repeated simulator memory. |
| [Doroudi et al., UAI 2017](https://cs.stanford.edu/people/ebrun/pdfs/doroudi2017uai.pdf) | Primary PDF | Fair/safe IS policy selection is established. No novelty claim for abstention. |
| [Trident, 2026 preprint](https://arxiv.org/html/2608.04317v1) | Primary manuscript | Adaptive red policies, decoy avoidance, and multi-environment trajectories already covered. Required defender propensities have not been validated in its dataset. |
| [CoADAM source](https://github.com/Usmanjibril09/CoADAM) | Pinned README, coevolutionary_trainer.m and Phase5_Baselines.m | Baselines explicitly use method-specific attacker fine-tuning. No first adaptive-deception evaluation claim. MATLAB not run; publisher full text remained inaccessible. |

Runtime provenance records all tracked-file hashes for inspected repositories. CoADAM source was inspected locally but is not redistributed. Its README license assertion was not used as permission to copy it into the release.

Supported contribution: generated benchmark traces pairing logged placement probabilities with memory transitions, observed impacts, and separate online reference worlds, plus a finite-network ranking sensitivity. Not supported: a new OPE algorithm, learned defense superiority, calibrated safety guarantees, universal winning subnet, first adaptive benchmark, or a production security claim.

The full manuscript is a research draft. Before journal submission, expand beyond one memory heuristic and one logging dataset per setting, reproduce a matched efficient comparator, complete the closest-artifact review, and obtain independent scientific review. More hardware use or larger sample counts alone do not establish novelty.
