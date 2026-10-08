"""Audit native order experiment and retain every paired contrast."""
import json,hashlib,itertools,statistics,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
root=ROOT/'analysis/carryover-order-development-v1'
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def main():
    manifest=json.loads((root/'manifest.json').read_text())
    for p,h in manifest.items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==h
    freeze=json.loads((root/'freeze.json').read_text())
    for p,h in freeze['files'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
    worlds={};steps=0
    for path in root.glob('*.json'):
        if path.name in ['manifest.json','freeze.json','receipt.json']:continue
        w=json.loads(path.read_text());assert w.get('status')!='failed',path.name
        memory={};prefix=[]
        for e in w['episodes']:
            if w['law']=='reset':memory={}
            elif w['law']=='decay':memory={n:v/2 for n,v in memory.items()}
            assert memory==e['memory_before']
            if e['phase']=='prefix':prefix.append(e['choice']);probs=[float(j==e['choice']) for j in range(3)]
            else:probs=freeze['policies'][w['policy']]
            assert e['probabilities']==probs and e['propensity']==probs[e['choice']]
            assert e['decoys']==3 and len(e['trace'])==40 and digest(e['trace'])==e['digest']
            impacts=set()
            for i,t in enumerate(e['trace']):
                assert i==t['step'] and t['blue_success'] and t['blue_action']==(e['choice']+1 if i<3 else 0)
                if i<3:assert t['blue_target']==['dmz_subnet','server_subnet1','user_subnet1'][e['choice']]
                o=t['observed']
                if o['success'] and o['action']=='impact':
                    memory[o['target']]=memory.get(o['target'],0)+1
                    if o['target'] in e['protected_targets']:impacts.add(o['target'])
                steps+=1
            assert memory==e['memory_after'] and sorted(impacts)==e['impacted_targets']
            assert abs(e['protection']-(1-len(impacts)/len(e['protected_targets'])))<1e-12
        assert prefix==freeze['prefixes'][w['prefix']]
        assert [e['slot'] for e in w['episodes'] if e['phase']=='evaluation']==[4,5,6,7]
        key=(w['network'],w['law'],w['prefix'],w['policy'],w['seed']);assert key not in worlds;worlds[key]=w
    assert len(worlds)==864
    controls=0;contrasts=[];means=[]
    for net,law,policy in itertools.product(['15-host-network.yaml','25-host-network.yaml'],['reset','count','decay'],['dmz','server','user']):
        vals={}
        for prefix in ['DDUU','UUDD','none']:
            ws=[worlds[net,law,prefix,policy,seed] for seed in range(70000,70016)]
            vals[prefix]=[statistics.mean(e['protection'] for e in w['episodes'] if e['phase']=='evaluation') for w in ws]
            harms=[statistics.mean(1-e['protection'] for e in w['episodes'] if e['phase']=='prefix') for w in ws] if prefix!='none' else []
            means.append(dict(network=net,law=law,policy=policy,prefix=prefix,mean=statistics.mean(vals[prefix]),se=statistics.stdev(vals[prefix])/4,prefix_mean_impact=statistics.mean(harms) if harms else None))
        for a,b in [('DDUU','UUDD'),('DDUU','none'),('UUDD','none')]:
            diffs=[u-v for u,v in zip(vals[a],vals[b])]
            contrasts.append(dict(network=net,law=law,policy=policy,a=a,b=b,mean=statistics.mean(diffs),paired_se=statistics.stdev(diffs)/4,world_differences=diffs))
        if law=='reset':
            for seed in range(70000,70016):
                baseline=[e['trace'] for e in worlds[net,law,'none',policy,seed]['episodes'] if e['phase']=='evaluation']
                for prefix in ['DDUU','UUDD']:
                    assert baseline==[e['trace'] for e in worlds[net,law,prefix,policy,seed]['episodes'] if e['phase']=='evaluation'];controls+=1
    result=dict(status='development diagnostic, no novelty or multiplicity-adjusted discovery claim',worlds=len(worlds),steps_verified=steps,raw_hashes_verified=len(manifest),reset_trace_controls=controls,means=means,contrasts=contrasts)
    (ROOT/'analysis/carryover-order-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['means','contrasts']},indent=2))
    print(json.dumps([r for r in contrasts if r['a']=='DDUU' and r['b']=='UUDD' and r['law']!='reset'],indent=2))
if __name__=='__main__':main()
