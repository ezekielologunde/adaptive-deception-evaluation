"""Audit raw world traces and compute declared development estimators."""
import argparse,hashlib,json,math,statistics
from collections import defaultdict
from pathlib import Path

def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def audit(root):
    manifest=json.loads((root/'manifest.json').read_text())
    for name,expected in manifest.items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,name
    freeze=json.loads((root/'freeze.json').read_text());groups=defaultdict(list);failures=[];checked=0
    for path in sorted(root.glob('*.json')):
        if path.name in ['freeze.json','manifest.json']:continue
        world=json.loads(path.read_text())
        if world.get('status')=='failed':failures.append(path.name);continue
        memory={}
        for i,ep in enumerate(world['episodes']):
            if not world['persistent']:memory={}
            assert ep['memory_before']==memory
            assert ep['episode']==i and len(ep['trace'])==40
            assert ep['history_digest']==digest(ep['trace'])
            probs=freeze['policies'][world['policy']]
            assert ep['probabilities']==probs and abs(sum(probs)-1)<1e-12
            assert ep['propensity']==probs[ep['choice']] and ep['propensity']>0
            assert ep['decoys']==3
            impacts=set()
            for step,t in enumerate(ep['trace']):
                assert t['step']==step
                assert t['blue_action']==(ep['choice']+1 if step<3 else 0)
                assert t['blue_success']
                obs=t['observed']
                if obs['action']=='impact' and obs['success']:
                    alias=digest([str(i) if world['rotate_alias'] else 'stable',obs['target']])
                    memory[alias]=memory.get(alias,0)+1
                    if obs['target'] in ep['protected_targets']:impacts.add(obs['target'])
            assert sorted(impacts)==ep['impacted_targets']
            assert abs(ep['protection']-(1-len(impacts)/len(ep['protected_targets'])))<1e-12
            assert ep['memory_after']==memory
            checked+=1
        groups[(world['persistent'],world['rotate_alias'],world['policy'])].append(world)
    results=[]
    for persistent in [False,True]:
        for rotate in [False,True]:
            logs=groups[persistent,rotate,'logging']
            for policy,probs in freeze['policies'].items():
                if policy=='logging':continue
                online=groups[persistent,rotate,policy]
                vals=[statistics.mean(ep['protection'] for ep in w['episodes']) for w in online]
                weights=[[1.]*8 for _ in logs];rewards=[];naive=[]
                for j,w in enumerate(logs):
                    rs=[]
                    cumulative=1.
                    for k,ep in enumerate(w['episodes']):
                        ratio=probs[ep['choice']]/ep['propensity'];cumulative*=ratio
                        weights[j][k]=cumulative;rs.append(ep['protection']);naive.append(ratio*ep['protection'])
                    rewards.append(rs)
                pdis=statistics.mean(sum(w*r for w,r in zip(ws,rs))/8 for ws,rs in zip(weights,rewards))
                sn=[];ess=[]
                for k in range(8):
                    ws=[w[k] for w in weights];den=sum(ws)
                    sn.append(sum(ws[j]*rewards[j][k] for j in range(len(logs)))/den)
                    ess.append(den**2/sum(x*x for x in ws))
                results.append(dict(persistent=persistent,rotate_alias=rotate,policy=policy,
                    online_worlds=len(vals),online_mean=statistics.mean(vals),
                    online_se=statistics.stdev(vals)/math.sqrt(len(vals)) if len(vals)>1 else None,
                    prefix_is=pdis,prefix_self_normalized=statistics.mean(sn),
                    history_discarding_diagnostic=statistics.mean(naive),ess_by_encounter=ess))
    return dict(status='development pilot; no confidence or novelty claim',files_verified=len(manifest),
                qualifying_worlds=sum(map(len,groups.values())),encounters_verified=checked,failures=failures,rows=results)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=audit(a.root);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
