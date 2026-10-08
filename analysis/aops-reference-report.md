# A-OPS reference execution, October 7, 2026

This is a reduced execution of the authors' unchanged algorithm on their public cartpole data. It is not a full Figure 14 reproduction, a cyber result, or a novelty claim.

Three development experiments used 50 policies and 20 rounds per agent, with all 1,000 Adam steps per GP update retained. A five-round timing pilot and its fresh-process repeat are separate. The fixed resource rule selected this scale because the initial cold pilot projected more than 30 minutes for ten 100-round experiments. Later warm timings were faster; neither observations nor seeds were discarded.

## Descriptive endpoint results

Simple regret is relative to the best empirical mean among each selected policy set. Lower is better. These three policy subsets share the same public finite dataset; they are not three independent domains. Standard errors below describe variation across runs, not population reward uncertainty.

| Method | Run 1 | Run 2 | Run 3 | Mean | SE |
|---|---:|---:|---:|---:|---:|
| Ind+Uniform+OPE | 0.000000 | 10.570566 | 3.523722 | 4.698096 | 3.107442 |
| Ind+UCB+OPE | 0.000000 | 4.007982 | 3.984634 | 2.664206 | 1.332120 |
| GP+Uniform+OPE | 0.000000 | 3.427116 | 3.523722 | 2.316946 | 1.158809 |
| A-ops | 0.000000 | 5.274832 | 2.942856 | 2.739229 | 1.526113 |
| FQE only | 10.570566 | 10.570566 | 10.086306 | 10.409146 | 0.161420 |

A-OPS reduced regret relative to FQE-only in all three runs. It did not dominate the other active methods. This sample is too small and too short for a reliable method ranking; no significance claim is made.

## Verification and limitations

Verified 11 manifest hashes and 280 recorded pulls, including the pilot and duplicate replay. Every reward belongs to the selected policy's public sample array. Every recommendation regret was recomputed with float64 means; maximum difference from upstream float32 values was 4.909706114e-06. Pilot policy identities, decisions, rewards, recommendations, and regrets matched exactly in the fresh process. The replay is a reproducibility check, not an additional independent trial.

Separate mathematical checks verified nine kernel entries, three GP posterior means, three posterior variances, and two UCB decision properties. These check the fixed-hyperparameter posterior, not independent equivalence of the entire optimizer. See aops-math-verification.json.

The independent-arm source does not implement the variance conditional stated in its own iid Gaussian model: beta is updated using half the mean squared residual, while that conditional uses half the summed squared residual. Nine numerical cases found agreement in all three single-observation controls and disagreement in all six multiple-observation cases. This affects SingleBayesArm, not the separate GP class. Original source remains unchanged; the scope and effect on published claims have not been established. See aops-independent-arm-audit.json. A future comparative study must include a clearly labeled corrected sensitivity baseline before interpreting rankings involving the independent-arm methods.

## Reproducibility boundaries

The protocol was committed before collection. Python and TensorFlow seeds were added because upstream only seeds NumPy. Core versions match upstream; protobuf 3.19.6 resolves the old runtime, with all transitive versions recorded. Notebook/plotting dependencies were omitted. CPU execution emitted a CUDA initialization diagnostic but completed with zero recorded run failures. No HPC job was submitted.

Run receipts preserve original CRLF lock-file hashes. Commit 79b8c78 initially normalized the lock in Git; dbda717 restores the exact bytes under -text attributes. Package versions did not change. Reproduce using the final archive, not solely the initial freeze commit for lock-file byte comparison.

Primary reference: [authors' source and dataset](https://github.com/google-deepmind/active_ops/tree/5c7b24515adadbaf89feb84232190bad96221c04). Code is Apache-2.0; data are CC BY 4.0 as stated upstream, attributed to Konyushkova et al., Active Offline Policy Selection, NeurIPS 2021, DeepMind. Third-party source/data are acquired separately.

## Research decision

The stationary reference is now executable and auditable at reduced scale. This does not clear novelty for an acquisition rule. Require a model-knowledge-matched state-aware comparator and a specific distinction from existing dual-control, ROGUE, and action-dependent evaluation methods before launching a cyber superiority study. Preserve the prior manuscript unchanged.
