# Final contribution gate and closure decision

Date: 2026-10-07. Decision: **do not continue the current novel-method route**. Preserve this repository as a bounded simulator study and a reduced reference-reproduction artifact. No files, datasets, or manuscript packages are deleted. This is a research-scope decision, not a claim that no future contribution in adaptive deception is possible.

The user approved a final bounded feasibility test: first substantiate a distinct contribution, then run a held-out comparison only if that first gate passes. The first gate failed. Therefore no new held-out experiment, HPC sweep, or manuscript was produced in this closure phase. A failed contribution gate is not an experimentally rejected hypothesis about every possible method.

## Candidate examined

Using only defender-visible telemetry, infer hidden attacker conditioning and choose whether another policy-evaluation episode is worth its potential harm to later deployment. Candidate variants considered in the existing plan were Bayesian lookahead, a harm penalty or budget, an uncertainty-set version, and an efficient approximation. No new approximation, bound, identification result, or demonstrably distinctive algorithm had been specified.

## Explicit mapping to established planning

For this mapping assume a finite network state space, bounded attacker memory, finitely many evaluation actions and observations, a finite evaluation budget B, a finite deployment horizon H, and a specified finite family of dynamics models with a prior. These are modeling assumptions for the comparison, not established properties of real attackers. Let z=(x,m,theta), where x is network state, m is unobserved attacker memory, and theta indexes the unknown dynamics model. Theta is fixed within a trajectory in this version. A changing type can instead be included in a larger Markov state when its transition law is specified.

The evaluator receives only history h of its own actions and telemetry. Its information state is b(z)=Pr(z|h). An evaluation action a has a joint next-state/telemetry kernel K_a(z',o|z), which includes any cross-policy conditioning. The update is

    P(o|b,a) = sum_z,z' b(z) K_a(z',o|z)
    b'(z') = sum_z b(z) K_a(z',o|z) / P(o|b,a)

for observations of positive probability. No realized hidden memory is supplied to the evaluator. Observed costs can be included in o. With expected acquisition cost C(b,a), and J_H(pi,z) the expected cumulative deployment reward for a committed candidate policy pi over H steps from z, define

    G(b) = max_pi sum_z b(z) J_H(pi,z)
    V_0(b) = G(b)
    V_k(b) = max { G(b), max_a [-C(b,a) + sum_o P(o|b,a) V_(k-1)(b')] }.

J_H must propagate attacker-state changes during deployment. Replacing it by H times a single fixed-state success probability would be an extra approximation, not a general solution. If evaluation consumes a shared total time budget, include remaining time in the state and reduce it on each action. Committing a policy is represented by entering a deployment mode that follows that policy for H steps, then an absorbing terminal state. Evaluation episodes can be expanded into primitive transitions, including elapsed time, rather than assumed instantaneous.

This construction preserves observable histories, action-conditioned transition probabilities, acquisition losses, and deployment rewards. Induction on the remaining evaluation budget gives the displayed belief-state recursion. Consequently, the stated Bayesian candidate is a standard finite-horizon partially observable control problem with a stop/commit action. The mapping is an application of established machinery, not a new theorem.

This equivalence concerns the *specified formulation*. It does not say that all problems expressible as POMDPs lack research value. A new scalable solver, a justified special-case bound, an identification result, or a convincing independently validated empirical contribution could still be publishable. None has been established for the present candidate.

## Closest primary evidence

| Source and inspected portion | Relevant coverage | Limit on inference |
|---|---|---|
| [Ross, Chaib-draa and Pineau, Bayes-Adaptive POMDPs, NeurIPS 2007 proceedings](https://papers.nips.cc/paper_files/paper/2007/file/3b3dbaf68507998acd6a5a5254ab2d76-Paper.pdf), sections 3-4 | Joint learning and planning with unknown transition/observation parameters and partial state observations; belief approximations and lookahead | Their count-based model has specific assumptions. It does not by itself reproduce the cyber setting, but rules out generic hidden-state Bayesian learning as our distinction. |
| [Osogami, Robust partially observable Markov decision process, ICML 2015](https://proceedings.mlr.press/v37/osogami15.pdf), sections 2 and 3.2 | Robust value iteration and belief updates for uncertain transition-observation parameters | Its uncertainty structure matters. We do not interchange fixed-model uncertainty and stagewise adversarial uncertainty, or assert its exact algorithm solves every proposed cyber model. |
| [Cubuktepe et al., Robust Policy Synthesis for Uncertain POMDPs via Convex Optimization, IJCAI 2020](https://www.ijcai.org/proceedings/2020/0569.pdf), introduction and section 4 | Robust policy synthesis, finite-memory representation, and structured probability uncertainty | The method restricts the policy/uncertainty classes. Robustness plus hidden state is not sufficient novelty; a particular efficient extension could be. |

Earlier overlap with A-OPS, SaVeR, dual control, OPEN, ROGUE, policy regret, and carryover-aware designs remains documented in active-evidence-prior-art.md. This is a targeted contribution assessment, not an exhaustive proof that the literature contains every possible variant.

## Gate results

| Required evidence before another experiment | Assessment |
|---|---|
| An explicit method or result beyond the existing belief-state formulation | Not supplied; the candidate remains a research question |
| Distinct algorithmic step, guarantee, or computational claim | Not established |
| A fair empirical superiority hypothesis that can be tied to that distinction | Not ready to freeze |
| A reason to expect another network, dataset, or GPU sweep to resolve the conceptual gap | Not established |

The existing screen's advantage over a stationary ablation does not answer these requirements. The native simulator carryover effect is useful bounded evidence, but does not establish a new general phenomenon or estimator. The upstream independent-arm discrepancy remains an implementation-audit observation, not a substitute novel-method contribution.

## Disposition and reopening criteria

Retain the prior manuscript as a bounded draft, the generated datasets, frozen protocols, negative findings, and reproduction scripts. Do not submit or market the project as a novel algorithm. Keep the repository accessible and editable; no GitHub archive setting is requested or applied. Mark it closed for active novel-method development in the project index.

Reopen only with a concrete artifact: a mathematically specified method or claim, a comparison against the closest applicable approach showing the nontrivial distinction, and a falsifiable evaluation plan. A different title, additional dataset, larger model, or more compute is insufficient by itself. These criteria are not a demand that all research be algorithmic; a separately justified empirical or benchmark contribution could support a different project scope.

The next unstarted topic in the existing portfolio order is private remediation assurance with ZKP. It remains a proposal, not a novelty-cleared successor. Its first milestone should be a literature-backed threat model and contribution assessment before implementation or manuscript drafting.
