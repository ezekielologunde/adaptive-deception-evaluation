# Active evidence collection: pre-experiment screening protocol

Date: 2026-10-07. Status: constructed decision-theoretic diagnostic, not a cybersecurity effectiveness experiment. Preserve the previous simulator study and manuscript unchanged.

## Question and prior-art gate

Can evidence collection improve terminal policy choice enough to justify the persistent changes it causes? A-OPS already provides active offline policy selection, SaVeR addresses safe evaluation data collection, and Bayesian dual control already accounts for information and physical-state changes. Merely adding memory to a Bayesian planner is not a new algorithm. Carryover-aware experimental design and policy regret also predate this project.

This screen tests a necessary engineering premise: ignoring persistent effects can produce worse total value even when policy-selection error looks small. It cannot establish novelty, and an exact Bayesian planner is the strong comparator, not a proposed original method. If a candidate is mathematically the same planner under renamed variables, reject its algorithmic novelty claim.

## Fully specified model

Unknown type theta is binary with prior P(theta=1) in {0.25,0.5,0.75}. Two candidate defenses j=0,1 have initial success probabilities 0.9 when j=theta and 0.4 otherwise. Public exposure counts x=(x0,x1) start at zero. A probe of j observes Bernoulli success with probability q_j(theta,x)=max(0,base_j(theta)-d*(x_j+k*x_other)). It then increments x_j, irrespective of success. The learner observes its own count state and outcomes but not theta.

Damage coefficient d in {0,0.02,0.08,0.2}; transfer coefficient k in {0,0.5,1}; maximum probe budget B in {1,2,3}. This gives 108 fixed parameter cases. No fitted Cyberwheel parameters or real-world interpretation of these values. Both observation and transition models are known to the methods; only theta is uncertain. Transfer effects are model assumptions, not discoveries.

After stopping, select the defense with largest posterior expected q at the reached state, with lower-index tie breaking. Terminal payoff is 10*q for the selected defense; the model deliberately holds the state fixed during terminal deployment. Each probe incurs realized loss 1-y. Objective: expected terminal payoff minus cumulative probe losses. A stop option is available to adaptive methods. Budget is a cap, not a requirement to spend.

Compare: immediate stop; uniform random probing until budget exhausted; an exact stationary-planning ablation that holds physical state fixed inside its lookahead; a state-aware one-step-lookahead heuristic with early stopping; and exact finite-horizon Bayesian dynamic programming. The stationary ablation uses actual current state and the same likelihood information, but ignores future state changes during planning. It is not an implementation of A-OPS, SaVeR, or any published method. The one-step heuristic is standard approximate planning, not claimed novel.

Evaluate all observation branches exactly, without Monte Carlo. Report expected terminal value, probe loss, number of probes, posterior entropy, selection regret relative to a type-aware oracle at the reached state, and degradation of that oracle relative to the untouched state. Their sum with probe loss must equal total loss relative to the untouched type-aware oracle. Smaller conditional selection regret alone must not be described as safer if it results from degrading every defense.

Controls: all methods with B=0 equal immediate stop; d=0 makes exact stationary planning and exact state-aware planning equal in value; full-horizon Bayesian optimum weakly dominates feasible comparators; probabilities sum to one; decomposition holds branchwise and in expectation. Independently enumerate deterministic depth-one policies and verify the exact planner. Report the whole grid, including failures and cases with no benefit. Do not tune parameters after inspecting output.

## Decision after screening

A successful diagnostic justifies developing a state-continuity benchmark or a genuinely new computational/certification contribution. It does not justify a manuscript asserting a new dual-control method. Before main collection, specify the additional contribution, match published baselines to their assumptions, and test multiple attacker families plus model misspecification. No large HPC run or new paper is authorized by the screen's success alone as evidence of novelty.
