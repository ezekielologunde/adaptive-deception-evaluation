"""Constructed estimand check only, not empirical cyber-defense evidence."""
import hashlib
import json
from functools import lru_cache
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def forward(p, horizon, learn=0.4, forget=0.05, reset=False):
    aware = total = 0.0
    for _ in range(horizon):
        if reset:
            aware = 0.0
        total += p * (0.9 * (1-aware) + 0.1 * aware) + (1-p)*0.5
        aware = (1-aware)*p*learn + aware*(1-(1-p)*forget)
    return total/horizon

def backward(p, horizon, learn=0.4, forget=0.05, reset=False):
    @lru_cache(None)
    def value(left, state):
        if not left:
            return 0.0
        if reset:
            state = 0
        result = 0.0
        for action, prob in [(0, 1-p), (1, p)]:
            reward = 0.5 if action == 0 else [0.9, 0.1][state]
            flip = (learn if action else 0) if state == 0 else (0 if action else forget)
            future = (1-flip)*value(left-1, state) + flip*value(left-1, 1-state)
            result += prob*(reward+future)
        return result
    return value(horizon, 0)/horizon

def main():
    output = ROOT/'analysis/memory-diagnostic-v0.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite a retained diagnostic')
    rows = []
    checks = 0
    for horizon in [1, 8, 100]:
        for learn in [0.0, 0.4]:
            for p in [0.1, 0.5, 0.9]:
                for reset in [False, True]:
                    a = forward(p, horizon, learn=learn, reset=reset)
                    b = backward(p, horizon, learn=learn, reset=reset)
                    assert abs(a-b) < 1e-12
                    if horizon == 1 or learn == 0:
                        assert abs(a - (0.5 + 0.4*p)) < 1e-12
                    checks += 1
                    rows.append(dict(horizon=horizon,learning_probability=learn,
                                     decoy_probability=p,reset_memory=reset,
                                     forward=a,backward=b))
    record = dict(status='constructed diagnostic; no empirical or novelty claim',
                  code_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  protocol_sha256=hashlib.sha256((ROOT/'protocol/pilot-v0.md').read_bytes()).hexdigest(),
                  independently_computed_cases=checks,rows=rows)
    output.write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in record.items() if k!='rows'},indent=2))
    for reset in [True,False]:
        group=[r for r in rows if r['horizon']==100 and r['learning_probability']==0.4 and r['reset_memory']==reset]
        print('reset' if reset else 'persistent',[(r['decoy_probability'],round(r['forward'],6)) for r in group])

if __name__=='__main__':
    main()
