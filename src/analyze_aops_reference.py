"""Audit recorded reference trajectories without importing the learning code."""
import hashlib
import io
import json
import math
import pathlib
import random
import statistics
import numpy as np
from audit_aops_data import NumericUnpickler

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCE = ROOT/'data/source-cache/active_ops'


def main():
    source_audit = json.loads((ROOT/'data/aops-source-audit.json').read_text())
    for name, expected in source_audit['tracked_file_sha256'].items():
        assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() == expected
    rewards = NumericUnpickler(io.BytesIO((SOURCE/'data/full_reward_samples.pkl').read_bytes())).load()
    opes = NumericUnpickler(io.BytesIO((SOURCE/'data/ope_values.pkl').read_bytes())).load()
    datasets = {}
    hashes, checked, max_error = 0, 0, 0.
    for name in ['pilot','development','replay']:
        folder = ROOT/f'analysis/aops-reference-{name}-v1'
        manifest = json.loads((folder/'manifest.json').read_text())
        for file, expected in manifest.items():
            assert hashlib.sha256((folder/file).read_bytes()).hexdigest() == expected
            hashes += 1
        freeze = json.loads((folder/'freeze.json').read_text())
        for file, expected in freeze['files'].items():
            assert hashlib.sha256((ROOT/file).read_bytes()).hexdigest() == expected
        assert not json.loads((folder/'receipt.json').read_text())['failures']
        experiments = [json.loads(f.read_text()) for f in sorted(folder.glob('experiment-*.json'))]
        assert len(experiments) == freeze['arguments']['experiments']
        for experiment in experiments:
            keys = experiment['policies']
            expected_keys = sorted(dict(random.Random(experiment['seed']).sample(list(opes.items()),50)))
            assert keys == expected_keys
            means = np.array([np.mean(rewards[k],dtype=np.float64) for k in keys])
            fqe = means.max()-means[np.argmax([opes[k] for k in keys])]
            assert abs(fqe-experiment['fqe_regret'])<1e-3
            rows = experiment['rows']
            assert len(rows) == freeze['arguments']['rounds']*4
            names = ['Ind+Uniform+OPE','Ind+UCB+OPE','GP+Uniform+OPE','A-ops']
            for index,row in enumerate(rows):
                assert row['step']==index//4 and row['agent']==names[index%4]
                assert 0<=row['arm']<50 and 0<=row['recommended']<50
                assert np.any(rewards[keys[row['arm']]]==row['reward'])
                regret = means.max()-means[row['recommended']]
                error = abs(regret-row['regret'])
                assert error<1e-3
                max_error = max(max_error,error)
                checked += 1
        datasets[name] = experiments
    left,right = datasets['pilot'][0],datasets['replay'][0]
    assert left['policies']==right['policies'] and left['rows']==right['rows'] and left['fqe_regret']==right['fqe_regret']
    results = {}
    for name in names+['FQE only']:
        values = [e['fqe_regret'] if name=='FQE only' else next(r['regret'] for r in reversed(e['rows']) if r['agent']==name) for e in datasets['development']]
        results[name] = dict(final_regrets=values,mean=statistics.mean(values),se=statistics.stdev(values)/math.sqrt(len(values)))
    differences = {}
    aops = results['A-ops']['final_regrets']
    for name,values in results.items():
        if name=='A-ops':continue
        ds = [a-b for a,b in zip(aops,values['final_regrets'])]
        differences[name] = dict(aops_minus_comparator=ds,mean=statistics.mean(ds),paired_se=statistics.stdev(ds)/math.sqrt(len(ds)))
    result = dict(status='Reduced reference execution, not full published figure reproduction or novelty evidence',
        manifest_hashes_checked=hashes,recorded_pulls_checked=checked,max_float64_regret_difference=max_error,
        replay_exact=True,development_experiments=3,rounds=20,policies_per_experiment=50,
        independent_arm_caveat='Upstream conditional-scale discrepancy retained; see aops-independent-arm-audit.json',
        final_regrets=results,paired_differences=differences,
        timing_rule=dict(pilot_seconds=left['seconds'],projected_ten_by_100_seconds=left['seconds']*20*10,threshold_seconds=1800,selected='three by 20'))
    (ROOT/'analysis/aops-reference-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
