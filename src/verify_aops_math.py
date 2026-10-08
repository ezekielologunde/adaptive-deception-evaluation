"""Independent numerical checks for the unchanged reference GP and UCB."""
import json
import pathlib
import run_aops_reference as reference
import numpy as np
import gp_models
import kernel
import agents


def main():
    distances = np.abs(np.arange(3)[:, None] - np.arange(3)[None, :]).astype(np.float32)
    k = kernel.ActionDistanceMatern12(distances, variance=2., lengthscale=1.5, bias_variance=.4)
    gp = gp_models.GaussianProcess(3, k, .3, .7)
    indices = np.array([0, 0, 2, 1, 2])
    observations = np.array([1., .8, -.5, .3, -.2])
    gp.add(indices[:, None], observations)
    prediction = gp.index(np.arange(3)[:, None], latent_function=True)
    covariance = 2 * np.exp(-distances.astype(float)/1.5) + .4
    cross = covariance[:, indices]
    noisy = covariance[np.ix_(indices, indices)] + .7*np.eye(len(indices))
    expected_mean = .3 + cross @ np.linalg.solve(noisy, observations-.3)
    expected_var = np.diag(covariance - cross @ np.linalg.solve(noisy, cross.T))
    np.testing.assert_allclose(prediction.mean().numpy(), expected_mean, rtol=2e-5, atol=2e-6)
    np.testing.assert_allclose(prediction.stddev().numpy()**2, expected_var, rtol=2e-5, atol=2e-6)
    np.testing.assert_allclose(k.matrix(np.arange(3)[:, None], np.arange(3)[:, None]).numpy(), covariance, rtol=2e-5, atol=2e-6)

    class Model:
        steps = np.array([2, 2, 2])
        mean = np.array([.9, .4, .2])
        stddev = np.array([.01, .2, .02])
    agent = agents.UCBAgent(Model(), exploration_coef=5)
    assert agent.select_action() == 1 and agent.best_arm == 0
    out = dict(gp_posterior_means_checked=3, gp_posterior_variances_checked=3,
               kernel_entries_checked=9, ucb_checks=2, tolerance=dict(rtol=2e-5, atol=2e-6),
               status='Fixed-hyperparameter GP posterior and UCB checks passed; not independent verification of GP optimizer or whole algorithm')
    (reference.ROOT/'analysis/aops-math-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
