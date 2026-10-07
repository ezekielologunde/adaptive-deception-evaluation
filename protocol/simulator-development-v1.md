# Cyberwheel development matrix v1

Freeze before collection. This refines pilot-v0 after successful installation and source inspection. It is a development experiment, not a test of a new estimator.

Pinned Cyberwheel: 6e535b50eea991ed48bb9eeb46b4b267090cc897. Python 3.10.20, CPU-only PyTorch. Minimal simulator dependency environment recorded separately; no claim that all upstream optional tools are installed.

Network: upstream 15-host network. Each independent world has eight 40-step encounters. Each encounter resets native network and ART state. Separate author-written memory records successful impact observations against previously discovered host identities. The modified target selector prioritizes remembered, currently discovered, unimpacted targets; otherwise it uses native ServerDowntime. It never uses a decoy flag, real-asset label or future outcome. This is a transparent heuristic, not a trained attacker or a realistic adversary model.

Cross memory-reset/retention with stable/rotated aliases for retained memory. Alias rotation affects the memory lookup only, not real network addresses or native ART state; do not call it a deployed moving-target defense. These controls separate memory availability from identity linkage. Host existence checks prevent references to removed hosts, as native target selection also does. The receiver's simulator state is available to execution but not used as an oracle for target ranking.

Every policy deploys three decoys in the same selected subnet at steps 0,1,2, then no-ops. Logging policy chooses the subnet uniformly. Three candidate stochastic policies use probabilities (0.6,0.2,0.2), (0.2,0.6,0.2), (0.2,0.2,0.6) in upstream subnet order. Names dmz/server/user are verified against actual action targets in analysis, not assumed from numeric indices. Three deployments enforce equal configured budgets. Actual successes and resulting counts are audited.

Eight worlds per memory/alias/policy cell, 128 world attempts, 1024 encounters and 40960 simulator steps if all succeed. Logging seeds are disjoint from target online rollouts. Candidate policies share seeds for paired comparison; worlds, not encounters, are the independent units. No inferential population claim from this small pilot.

One macro-action is sampled per encounter, with its known propensity saved. Sequential per-decision importance sampling multiplies ratios from the start of the world through each encounter. A deliberately history-discarding per-encounter estimate is a diagnostic comparator, not a valid estimator of the persistent-history target by default. Self-normalized variants report effective sample sizes at each time. No clipping or arbitrary confidence claims. Online means include Monte Carlo standard errors across worlds.

Primary pilot checks: source and trace integrity, propensity validity, memory transition consistency, equal deployment budgets, no privileged decoy signal in the custom selector, reset/rotation negative-control equivalence, and whether support degeneracy prevents useful selection. Success is a functioning and honest experiment, not a favorable result.

Native UUID generation is replaced only during simulated deployment by a seeded 128-bit identifier generator; original function is restored in finally. This makes identifiers reproducible and is disclosed. Python's native random stream remains for native simulator/attacker behavior; defender macro-action and UUID streams use separate Random instances. Upstream source files remain unchanged. Outputs are exclusive-create and retain failures.
