# Adaptive deception and policy evaluation

Status: Proposed. Historical candidate design, not a preregistration or proven novelty claim. Source: independent research portfolio dated 2026-10-04.

**Research question:** Can offline estimates select a deception policy that reduces protected-asset compromise in subsequent randomized trials, including against attackers that adapt to the decoys?

**Existing coverage:** Adaptive honeypots are a mature research theme, including [RL-driven ICS honeypots](https://doi.org/10.1109/tmlcn.2026.3684465). [Beyond Guesswork](https://d197for5662m48.cloudfront.net/documents/publicationstatus/309682/preprint_pdf/c6473aa83f39b7573fb1d95484942626.pdf) develops deception measurement concepts. [NCSC trials](https://www.ncsc.gov.uk/blog-post/cyber-deception-trials-what-weve-learned-so-far) reinforce the importance of operational context. Do not claim the first adaptive decoy or the first outcome-based evaluation.

**Proposed difference:** A dataset with known behavior-policy action probabilities and a blinded comparison between offline policy-value estimates and later online outcomes. The specific overlap with off-policy evaluation in security remains unresolved, so this has lower novelty confidence than projects 1-3.

**Build and experiment:** Randomize among safe decoy actions in a contained range. Log state, chosen action, probability of that action, policy version, attacker family, protected-asset outcome, censorship and timestamps. Compare static, random, rule-based and learned policies. Evaluate importance-weighted and doubly robust estimates against independent online rollouts. Hold out attacker policies and scenarios.

**Metrics:** Protected-asset compromise, detection delay, action cost, estimator bias, interval coverage and effective sample size. Session length is a secondary metric. Test failure under weak policy overlap and adversary adaptation. Predefine the reward independently of the learned policy and account for repeated attacker sessions.

**Stop or narrow:** Passive SSH logs without logged action probabilities and interventions cannot substantiate causal policy improvement. Network IDS CSVs cannot substitute for deception trajectories. If offline support is inadequate, report non-identifiability rather than a policy ranking.
