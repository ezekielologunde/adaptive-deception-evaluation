# Native simulator falsification: order and carryover

Freeze before collection. This is development evidence, not a main validation or a novelty claim. The exact constructed screen showed that classical Bayesian planning already solves the small known-model problem. The next gate asks whether a meaningful effect survives native simulator dynamics without assuming damage by construction.

Two four-encounter prefixes: D,D,U,U and U,U,D,D. Each encounter deploys three decoys in the named subnet, so both prefixes use identical counts and budget. A third prefix, none, skips experimental exposure. After the prefix, run four evaluation encounters under each stochastic D/S/U policy from validation-v1. Suffix policies have independent policy-specific outcomes but share seed schedules for paired comparisons. Native 15- and 25-host networks.

Three memory laws: reset every encounter; persistent successful-target counts; counts multiplied by 0.5 at the start of each encounter (before successes are added). All use the previously documented observed-success prioritization rule. Decay is a distinct sensitivity control, not a realistic validated attacker-learning model. No decoy oracle labels enter the custom selector.

16 worlds per network/memory/prefix/suffix-policy cell, world seeds 70000..70015, unused in prior collection. Total 864 worlds. Prefix encounters use slots 0..3; evaluation encounters use slots 4..7 even when prefix is none. Macro-action draws are independently seeded by world and slot, so prefix length does not shift evaluation randomness. Decoy identifiers and native reset randomness use separate declared seed offsets. Four local CPU processes.

Primary outcomes: world-average suffix impact avoidance; paired difference between DDUU and UUDD for each suffix policy; and each ordered prefix versus no prefix. Prefix harm is separately reported as mean impact fraction, not added to suffix outcomes with an arbitrary weight. All prefix traces retained. No change to earlier data or manuscript.

Gate controls: under reset memory all suffix traces must match exactly for all three prefix choices at a fixed world/network/suffix policy. Ordered prefixes must have the same placement counts and budget. Audit all memory decay and success updates, outcome labels, action propensities, and original-target impacts independently. Do not treat shared-seed branches as independent observations. Report means and paired standard errors, no multiplicity-unadjusted discovery claim or selective reporting.

If no practically clear order effect appears, do not assume irreversible or important carryover. Even an observed effect does not establish novelty over switchback experimental design, policy regret, or dual control. A viable next contribution would require a specified estimation or collection method with an advantage under unknown dynamics and a matched strong comparator, beyond illustrating a known problem.
