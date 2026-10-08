"""Independent trace audit and frozen world-level validation analysis."""
import hashlib,json,itertools,math,statistics
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def check_world(w,policies):
    memory={}
    assert len(w['episodes'])==8 and not w['rotate_alias']
    for i,e in enumerate(w['episodes']):
        if not w['persistent']:memory={}
        assert e['memory_before']==memory and e['episode']==i
        assert len(e['trace'])==40 and e['history_digest']==digest(e['trace'])
        assert e['probabilities']==policies[w['policy']]
        assert e['propensity']==policies[w['policy']][e['choice']]
        assert e['action_mask']==[True]*3 and e['decoys']==3
        impacts=set()
        for j,t in enumerate(e['trace']):
            assert t['step']==j and t['blue_success']
            assert t['blue_action']==(e['choice']+1 if j<3 else 0)
            if j<3:assert t['blue_target']==['dmz_subnet','server_subnet1','user_subnet1'][e['choice']]
            o=t['observed']
            if o['action']=='impact' and o['success']:
                key=digest(['stable',o['target']]);memory[key]=memory.get(key,0)+1
                if o['target'] in e['protected_targets']:impacts.add(o['target'])
        assert sorted(impacts)==e['impacted_targets']
        assert abs(e['protection']-(1-len(impacts)/len(e['protected_targets'])))<1e-12
        assert memory==e['memory_after']

def main():
    root=ROOT/'analysis/validation-v1';manifest=json.loads((root/'manifest.json').read_text())
    for name,h in manifest.items():assert sha(root/name)==h,name
    freeze=json.loads((root/'freeze.json').read_text())
    for key,path in [('source_sha256','src/memory_study.py'),('protocol_sha256','protocol/validation-v1.md'),('smoke_source_sha256','src/simulator_smoke.py')]:assert sha(ROOT/path)==freeze[key]
    groups={};failures=[]
    for path in sorted(root.glob('*.json')):
        if path.name in ['freeze.json','manifest.json']:continue
        w=json.loads(path.read_text())
        if w.get('status')=='failed':failures.append(path.name);continue
        check_world(w,freeze['policies'])
        groups.setdefault((w['network'],w['persistent'],w['policy']),[]).append(w)
    assert not failures,failures
    assert len(groups)==16 and all(len(v)==64 for v in groups.values())
    for (_,_,policy),worlds in groups.items():
        base=30000 if policy=='logging' else 40000
        assert sorted(w['seed'] for w in worlds)==list(range(base,base+64))
    rng=np.random.default_rng(20261008);rows=[];decisions=[];contrasts=[]
    for network,persistent in itertools.product(['15-host-network.yaml','25-host-network.yaml'],[False,True]):
        logs=groups[network,persistent,'logging'];boot=rng.integers(0,64,(1000,64));bs=[];means={};cell=[]
        for policy in ['dmz','server','user']:
            online=sorted(groups[network,persistent,policy],key=lambda w:w['seed'])
            assert [w['seed'] for w in online]==list(range(40000,40064))
            values=np.array([np.mean([e['protection'] for e in w['episodes']]) for w in online]);means[policy]=values
            reward=np.array([[e['protection'] for e in w['episodes']] for w in logs])
            ratio=np.array([[freeze['policies'][policy][e['choice']]/e['propensity'] for e in w['episodes']] for w in logs])
            weight=np.cumprod(ratio,axis=1);ess=weight.sum(0)**2/(weight**2).sum(0)
            snis=float(np.mean((weight*reward).sum(0)/weight.sum(0)))
            boot_values=np.mean((weight[boot]*reward[boot]).sum(1)/weight[boot].sum(1),axis=1);bs.append(boot_values)
            row=dict(network=network,persistent=persistent,policy=policy,online_mean=float(values.mean()),online_se=float(values.std(ddof=1)/8),prefix_is=float((weight*reward).mean()),prefix_snis=snis,history_discarding=float((ratio*reward).mean()),ess=ess.tolist(),bootstrap_interval=np.quantile(boot_values,[.025,.975]).tolist())
            rows.append(row);cell.append(row)
        scores=np.array(bs).T;ties=np.isclose(scores,scores.max(1)[:,None],rtol=0,atol=1e-12);freq=(ties/ties.sum(1)[:,None]).mean(0)
        winner=int(np.argmax([r['prefix_snis'] for r in cell]));eligible=freq[winner]>=.95 and min(cell[winner]['ess'])>=16
        decisions.append(dict(network=network,persistent=persistent,bootstrap_winner_frequencies=dict(zip(['dmz','server','user'],freq.tolist())),offline_ranking=sorted([r['policy'] for r in cell],key=lambda p:next(r['prefix_snis'] for r in cell if r['policy']==p),reverse=True),selection=cell[winner]['policy'] if eligible else 'abstain',online_ranking=sorted(means,key=lambda p:means[p].mean(),reverse=True)))
        for a,b in itertools.combinations(means,2):
            d=means[a]-means[b];contrasts.append(dict(network=network,persistent=persistent,a=a,b=b,mean=float(d.mean()),se=float(d.std(ddof=1)/8)))
    result=dict(worlds=1024,encounters=8192,steps=327680,files_verified=len(manifest),failures=failures,rows=rows,decisions=decisions,paired_contrasts=contrasts)
    (ROOT/'analysis/validation-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(decisions=decisions,contrasts=contrasts),indent=2))
if __name__=='__main__':main()
