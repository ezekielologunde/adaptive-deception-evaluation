"""Headless reference driver. Algorithm classes are imported unchanged upstream.

Follows Active_ops_experiment.ipynb (DeepMind, Apache-2.0); public data
attributed to Konyushkova et al., NeurIPS 2021, CC BY 4.0.
"""
import argparse
import copy
import hashlib
import importlib.metadata
import io
import json
import os
import pathlib
import platform
import random
import subprocess
import sys
import time

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_NUM_INTRAOP_THREADS'] = '2'
os.environ['TF_NUM_INTEROP_THREADS'] = '1'
ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/source-cache/active_ops'
sys.path.insert(0, str(SOURCE))
import numpy as np
import tensorflow as tf
import scipy.spatial
import agents
import arm_model
import bandit
import kernel
import multiarm_model
from audit_aops_data import NumericUnpickler


def load(name):
    return NumericUnpickler(io.BytesIO((SOURCE / 'data' / (name + '.pkl')).read_bytes())).load()


def run(experiment, rounds, all_opes, rewards, actions, distances):
    start = time.perf_counter()
    seed = 805 + experiment
    np.random.seed(seed)
    random.seed(seed)
    tf.random.set_seed(seed)
    selected = dict(random.sample(list(all_opes.items()), k=50))
    world = bandit.MAB(selected)
    world.load_reward_samples(rewards)
    means = np.array([np.mean(rs) for rs in world.rewards])
    best = means.max()
    prior = dict(use_prior=False, alpha=1., beta=200.)
    kwargs = [dict(prior_mean=0., prior_std=1000., alpha=1., beta=1000., sample=False, steps=10, burnin=0) for _ in range(50)]
    independent = multiarm_model.IndependentMultiArmModel(50, arm_model.SingleBayesArm, arm_kwargs=kwargs)
    d = kernel.select_experiment_distances(selected, actions['policy_keys'], distances)
    k = kernel.ActionDistanceMatern12(d, lengthscale=np.median(d), bias_variance=10., variance_prior=prior)
    gp = multiarm_model.MVNormal(50, offset=0., kernel=k, observation_noise_variance=1000.,
        optimizer_config=dict(optimizer_name='Adam', learning_rate=.001, steps_per_update=1000, kwargs=dict(beta1=.9, beta2=.999)),
        observation_noise_variance_prior=prior)
    for a in range(50):
        independent.update(a, world.opes[a])
        gp.update(a, world.opes[a])
    models = {'Ind+Uniform+OPE': agents.UniformAgent(copy.deepcopy(independent)),
              'Ind+UCB+OPE': agents.UCBAgent(copy.deepcopy(independent), exploration_coef=5),
              'GP+Uniform+OPE': agents.UniformAgent(copy.deepcopy(gp)),
              'A-ops': agents.UCBAgent(copy.deepcopy(gp), exploration_coef=5)}
    rows = []
    for step in range(rounds):
        for name, agent in models.items():
            arm = int(agent.select_action())
            reward = float(world.pull(arm))
            agent.update(arm, reward)
            recommended = int(agent.best_arm)
            regret = float(best - means[recommended])
            assert np.isfinite(regret) and regret >= 0
            rows.append(dict(step=step, agent=name, arm=arm, reward=reward, recommended=recommended, regret=regret))
        if (step + 1) % 5 == 0:
            print(json.dumps(dict(experiment=experiment, completed_rounds=step+1, seconds=time.perf_counter()-start)), flush=True)
    return dict(experiment=experiment, seed=seed, policies=sorted(selected),
                fqe_regret=float(best-means[np.argmax(world.opes)]), rows=rows, seconds=time.perf_counter()-start)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    p.add_argument('--start', type=int, default=0)
    p.add_argument('--experiments', type=int, default=1)
    p.add_argument('--rounds', type=int, default=5)
    args = p.parse_args()
    out = ROOT / args.output
    out.mkdir(exist_ok=False)
    audit = json.loads((ROOT/'data/aops-source-audit.json').read_text())
    for name, expected in audit['tracked_file_sha256'].items():
        assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() == expected
    files = ['src/run_aops_reference.py', 'src/audit_aops_data.py', 'protocol/aops-reference-v1.md', 'requirements-aops-lock.txt']
    freeze = dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(), upstream=audit['revision'],
        files={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}, arguments=vars(args), python=platform.python_version(),
        packages={n:importlib.metadata.version(n) for n in ['numpy','scipy','tensorflow','tensorflow-probability','dm-sonnet','protobuf']})
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    failures = []
    try:
        opes, rewards, actions = [load(n) for n in ['ope_values','full_reward_samples','actions']]
        distances = np.mean([scipy.spatial.distance.cdist(a,a,metric='euclidean') for a in actions['actions']],axis=0)
        for experiment in range(args.start,args.start+args.experiments):
            result = run(experiment,args.rounds,opes,rewards,actions,distances)
            (out/f'experiment-{experiment:03d}.json').write_text(json.dumps(result,indent=2)+'\n')
    except Exception as exc:
        failures.append(dict(type=type(exc).__name__,message=str(exc)))
        raise
    finally:
        (out/'receipt.json').write_text(json.dumps(dict(failures=failures),indent=2)+'\n')
        (out/'manifest.json').write_text(json.dumps({f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in out.glob('*.json')},indent=2)+'\n')


if __name__ == '__main__':
    main()
