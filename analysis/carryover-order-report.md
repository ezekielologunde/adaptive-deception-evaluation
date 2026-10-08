# Native carryover screening results

Development population only: 864 worlds, 230,400 audited simulator steps, no failures. All 192 reset-memory suffix trajectory controls matched exactly. No pooled analysis with earlier validation.

Each contrast uses 16 paired worlds. Values are impact-avoidance fractions; negative values favor the second prefix. DDUU and UUDD contain the same two DMZ and two user-subnet deployment encounters. None means no prior testing. Each evaluation suffix uses four encounters.

| Hosts | Memory | Suffix policy | Prefix comparison | Mean difference | Paired SE |
|---|---|---|---|---:|---:|
| 15 | reset | dmz | DDUU minus UUDD | 0.00000 | 0.00000 |
| 15 | reset | dmz | DDUU minus none | 0.00000 | 0.00000 |
| 15 | reset | dmz | UUDD minus none | 0.00000 | 0.00000 |
| 15 | reset | server | DDUU minus UUDD | 0.00000 | 0.00000 |
| 15 | reset | server | DDUU minus none | 0.00000 | 0.00000 |
| 15 | reset | server | UUDD minus none | 0.00000 | 0.00000 |
| 15 | reset | user | DDUU minus UUDD | 0.00000 | 0.00000 |
| 15 | reset | user | DDUU minus none | 0.00000 | 0.00000 |
| 15 | reset | user | UUDD minus none | 0.00000 | 0.00000 |
| 15 | count | dmz | DDUU minus UUDD | -0.02187 | 0.03505 |
| 15 | count | dmz | DDUU minus none | -0.28125 | 0.06053 |
| 15 | count | dmz | UUDD minus none | -0.25938 | 0.04963 |
| 15 | count | server | DDUU minus UUDD | -0.03125 | 0.02882 |
| 15 | count | server | DDUU minus none | -0.22187 | 0.04978 |
| 15 | count | server | UUDD minus none | -0.19063 | 0.03932 |
| 15 | count | user | DDUU minus UUDD | -0.05312 | 0.06731 |
| 15 | count | user | DDUU minus none | -0.22187 | 0.05419 |
| 15 | count | user | UUDD minus none | -0.16875 | 0.05437 |
| 15 | decay | dmz | DDUU minus UUDD | -0.04687 | 0.02519 |
| 15 | decay | dmz | DDUU minus none | -0.30625 | 0.04871 |
| 15 | decay | dmz | UUDD minus none | -0.25938 | 0.04792 |
| 15 | decay | server | DDUU minus UUDD | -0.03750 | 0.02602 |
| 15 | decay | server | DDUU minus none | -0.23125 | 0.04630 |
| 15 | decay | server | UUDD minus none | -0.19375 | 0.03870 |
| 15 | decay | user | DDUU minus UUDD | -0.05625 | 0.06706 |
| 15 | decay | user | DDUU minus none | -0.22500 | 0.05323 |
| 15 | decay | user | UUDD minus none | -0.16875 | 0.05437 |
| 25 | reset | dmz | DDUU minus UUDD | 0.00000 | 0.00000 |
| 25 | reset | dmz | DDUU minus none | 0.00000 | 0.00000 |
| 25 | reset | dmz | UUDD minus none | 0.00000 | 0.00000 |
| 25 | reset | server | DDUU minus UUDD | 0.00000 | 0.00000 |
| 25 | reset | server | DDUU minus none | 0.00000 | 0.00000 |
| 25 | reset | server | UUDD minus none | 0.00000 | 0.00000 |
| 25 | reset | user | DDUU minus UUDD | 0.00000 | 0.00000 |
| 25 | reset | user | DDUU minus none | 0.00000 | 0.00000 |
| 25 | reset | user | UUDD minus none | 0.00000 | 0.00000 |
| 25 | count | dmz | DDUU minus UUDD | -0.05938 | 0.03784 |
| 25 | count | dmz | DDUU minus none | -0.13594 | 0.03291 |
| 25 | count | dmz | UUDD minus none | -0.07656 | 0.03404 |
| 25 | count | server | DDUU minus UUDD | -0.05625 | 0.03256 |
| 25 | count | server | DDUU minus none | -0.12656 | 0.02666 |
| 25 | count | server | UUDD minus none | -0.07031 | 0.03317 |
| 25 | count | user | DDUU minus UUDD | -0.04844 | 0.02505 |
| 25 | count | user | DDUU minus none | -0.08594 | 0.01963 |
| 25 | count | user | UUDD minus none | -0.03750 | 0.02500 |
| 25 | decay | dmz | DDUU minus UUDD | -0.02344 | 0.02882 |
| 25 | decay | dmz | DDUU minus none | -0.13906 | 0.03010 |
| 25 | decay | dmz | UUDD minus none | -0.11563 | 0.03686 |
| 25 | decay | server | DDUU minus UUDD | -0.03125 | 0.02809 |
| 25 | decay | server | DDUU minus none | -0.13281 | 0.02444 |
| 25 | decay | server | UUDD minus none | -0.10156 | 0.03457 |
| 25 | decay | user | DDUU minus UUDD | -0.03594 | 0.02592 |
| 25 | decay | user | DDUU minus none | -0.09375 | 0.01746 |
| 25 | decay | user | UUDD minus none | -0.05781 | 0.02745 |

All 24 retained-memory exposure-versus-none means are negative, ranging from -0.30625 to -0.03750. These related settings share seeds and mechanisms; they are not 24 independent replications. No multiplicity-adjusted discovery claim is made.

The order effects are smaller and uncertain. Every displayed retained-memory order contrast has magnitude less than twice its paired SE. This is a descriptive scale check, not an equivalence test or proof of no effect. The current study does not justify recommending one prefix ordering.

The no-prefix comparison skips four experimental encounters. It isolates a simulator conditioning effect on later encounters using matched suffix randomness; it is not evidence that collecting zero data always maximizes total deployment utility. Prefix harm is retained separately in the JSON summary, and no arbitrary information-versus-harm utility was optimized here.

Novelty gate: practical carryover is present in this wrapper, but carryover itself and Bayesian control are established. Do not write another manuscript claiming a new memory-aware planner. A substantive next result must address acquisition decisions with unknown, partially observed conditioning and outperform or complement a matched state-aware baseline. This report documents premise testing, not novelty clearance.
