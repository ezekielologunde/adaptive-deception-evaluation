"""Independent exhaustive policy-tree verification of the constructed screen."""
from pathlib import Path
from functools import lru_cache
import itertools,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'analysis/active-evidence-screen-v1'
manifest=json.loads((folder/'manifest.json').read_text())
for name,h in manifest.items():assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==h
freeze=json.loads((folder/'freeze.json').read_text())
for name,h in freeze['files'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
rows=json.loads((folder/'results.json').read_text());checked=0;policies=0
for d,k in itertools.product([0.,.02,.08,.2],[0.,.5,1.]):
    def q(theta,a,x):return max(0.,[.9,.4][int(theta!=a)]-d*(x[a]+k*x[1-a]))
    @lru_cache(None)
    def trees(x,b):
        # Each pair contains exact expected net value under type 0 and type 1.
        # No posterior update or Bellman maximization is imported from the runner.
        options=[(10*q(0,a,x),10*q(1,a,x)) for a in (0,1)]
        if b:
            for a in (0,1):
                nx=tuple(z+int(j==a) for j,z in enumerate(x));children=trees(nx,b-1)
                probs=[q(theta,a,x) for theta in (0,1)]
                for fail,success in itertools.product(children,repeat=2):
                    options.append(tuple((1-probs[t])*(fail[t]-1)+probs[t]*success[t] for t in (0,1)))
        return options
    for b in [1,2,3]:
        options=trees((0,0),b);policies+=len(options)
        for p in [.25,.5,.75]:
            r=next(r for r in rows if (r['prior'],r['damage'],r['transfer'],r['budget'])==(p,d,k,b))
            value=max((1-p)*v[0]+p*v[1] for v in options)
            assert abs(value-r['methods']['bayes']['net_value'])<1e-10
            for v in r['methods'].values():assert abs(9-v['net_value']-v['probe_loss']-v['selection_regret']-v['state_degradation'])<1e-10
            checked+=1
out=dict(independent_optima_verified=checked,policy_vectors_enumerated=policies,loss_decompositions=checked*5,raw_hashes_verified=len(manifest),frozen_source_hashes_verified=len(freeze['files']),interpretation='Correct implementation of established finite Bayesian planning, not an original algorithm')
(ROOT/'analysis/active-evidence-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
