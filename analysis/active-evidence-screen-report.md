# Exact active-evidence screening results

This is a constructed model with assumed damage, not native cyber evidence or a novel algorithm. All 108 Bayesian optima were verified by independent exhaustive policy-tree enumeration (981,864 type-conditioned policy vectors).

| Damage | Cases | Stationary below Bayesian optimum | Stationary below immediate stop | One-step below optimum |
|---|---:|---:|---:|---:|
| 0 | 27 | 0 | 0 | 0 |
| 0.02 | 27 | 15 | 10 | 8 |
| 0.08 | 27 | 24 | 22 | 0 |
| 0.2 | 27 | 27 | 27 | 0 |

The state-aware optimum improves over immediate stop in 53 of 108 constructed cases. Thus this screen does not merely reward refusing every experiment. The one-step approximation is suboptimal in 8 cases, with maximum net-value gap 0.040. These grid fractions are descriptive, not population success rates.

The largest stationary-planning loss relative to the optimum occurs at prior 0.25, damage 0.2, full cross-transfer and budget 3 (a post hoc illustrative case, not a separately confirmed finding). Immediate stop yields 7.75 expected net value. Stationary planning yields 5.285 while reducing conditional selection regret from 1.25 to 0.6425. The apparent improvement in choosing a defense hides degradation of the defenses being compared.

Interpretation: explicit state consequences matter in this assumed model, but the exact solution is classical Bayesian decision-tree planning. No algorithmic novelty survives that reduction. Native relevance is being tested separately using equal-budget prefix ordering; no new manuscript is warranted by this diagnostic.
