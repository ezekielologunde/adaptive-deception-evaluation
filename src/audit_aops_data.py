"""Audit pinned public A-OPS data without unrestricted pickle loading.

This is a data/interface audit, not reproduction of the A-OPS algorithm.
"""
import hashlib
import importlib.util
import io
import json
import pathlib
import pickle
import pickletools
import subprocess

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/source-cache/active_ops'
REVISION = '5c7b24515adadbaf89feb84232190bad96221c04'


class NumericUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        allowed = {
            ('numpy', 'dtype'): np.dtype,
            ('numpy', 'ndarray'): np.ndarray,
            ('numpy.core.multiarray', '_reconstruct'): np.core.multiarray._reconstruct,
        }
        if (module, name) not in allowed:
            raise pickle.UnpicklingError(f'Unapproved global: {module}.{name}')
        return allowed[module, name]


def main():
    revision = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == REVISION
    assert not subprocess.check_output(['git', '-C', str(SOURCE), 'status', '--porcelain'], text=True).strip()
    files = subprocess.check_output(['git', '-C', str(SOURCE), 'ls-files'], text=True).splitlines()
    hashes = {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() for name in files}
    objects, opcodes = {}, {}
    for name in ['actions', 'full_reward_samples', 'ope_values']:
        raw = (SOURCE / 'data' / (name + '.pkl')).read_bytes()
        ops = list(pickletools.genops(raw))
        opcodes[name] = sorted({str(arg) for op, arg, _ in ops if op.name == 'GLOBAL'})
        objects[name] = NumericUnpickler(io.BytesIO(raw)).load()
    rewards, opes, actions = [objects[k] for k in ['full_reward_samples', 'ope_values', 'actions']]
    keys = sorted(rewards)
    assert len(keys) == 76 and set(keys) == set(opes) == set(actions['policy_keys'])
    assert sorted(actions['policy_keys'].values()) == list(range(76))
    arrays = [np.asarray(rewards[k]) for k in keys]
    assert all(a.shape == (5000,) and a.dtype.kind in 'fi' and np.isfinite(a).all() for a in arrays)
    action_array = np.asarray(actions['actions'])
    assert action_array.shape == (1000, 76, 1) and np.isfinite(action_array).all()
    assert all(np.isfinite(opes[k]) for k in keys)
    spec = importlib.util.spec_from_file_location('aops_bandit', SOURCE / 'bandit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    world = module.MAB(opes)
    world.load_reward_samples(rewards)
    # Verify reference interface against independently sampled source arrays.
    # The same RNG seed must select the same fixed sample, with no state update.
    for index, key in enumerate(keys):
        np.random.seed(91000 + index)
        expected = np.random.choice(rewards[key], size=20)
        np.random.seed(91000 + index)
        actual = np.array([world.pull(index) for _ in range(20)])
        assert np.array_equal(actual, expected)
    out = dict(source_url='https://github.com/google-deepmind/active_ops', revision=revision,
               code_license='Apache-2.0', data_license='CC-BY-4.0 per upstream README',
               attribution='Konyushkova et al., Active Offline Policy Selection, NeurIPS 2021; DeepMind',
               tracked_file_sha256=hashes, pickle_globals=opcodes,
               policies=76, reward_samples_per_policy=5000, reward_samples_total=380000,
               action_shape=list(action_array.shape), matched_reference_pulls=1520,
               status='Data and bandit interface verified; GP fitting and A-OPS algorithm not yet reproduced',
               scope='Cartpole public reference data, not cybersecurity or adaptive-attacker observations')
    (ROOT / 'data/aops-source-audit.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k not in ['tracked_file_sha256', 'pickle_globals']}, indent=2))


if __name__ == '__main__':
    main()
