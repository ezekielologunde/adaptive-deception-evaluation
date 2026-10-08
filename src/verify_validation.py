"""Mutation controls, scalar estimator replication, and paired identity controls."""
import copy,json,statistics,hashlib,subprocess,sys,platform,importlib.metadata
from pathlib import Path
from analyze_validation import check_world,digest
ROOT=Path(__file__).resolve().parents[1]
root=ROOT/'analysis/validation-v1'
freeze=json.loads((root/'freeze.json').read_text());summary=json.loads((ROOT/'analysis/validation-summary.json').read_text())
w=json.loads((root/'15-1-dmz-000.json').read_text());mutations=[]
for kind in ['propensity','impact','memory','target','reward']:
    bad=copy.deepcopy(w);e=bad['episodes'][0]
    if kind=='propensity':e['propensity']+=.01
    if kind=='impact':e['impacted_targets']=[]
    if kind=='memory':e['memory_after']['invented']=1
    if kind=='target':e['trace'][0]['blue_target']='wrong';e['history_digest']=digest(e['trace'])
    if kind=='reward':e['protection']+=.01
    try:check_world(bad,freeze['policies'])
    except AssertionError:mutations.append(kind)
    else:raise AssertionError('Undetected mutation '+kind)
replicated=0
for row in summary['rows']:
    logs=[json.loads(p.read_text()) for p in sorted(root.glob(f"{row['network'][:2]}-{int(row['persistent'])}-logging-*.json"))]
    rewards=[];weights=[]
    for world in logs:
        weight=1;wr=[];rr=[]
        for ep in world['episodes']:
            weight*=freeze['policies'][row['policy']][ep['choice']]/ep['propensity'];wr.append(weight);rr.append(ep['protection'])
        weights.append(wr);rewards.append(rr)
    pdis=sum(sum(w*r for w,r in zip(ws,rs)) for ws,rs in zip(weights,rewards))/(64*8)
    snis=sum(sum(weights[j][i]*rewards[j][i] for j in range(64))/sum(ws[i] for ws in weights) for i in range(8))/8
    assert abs(pdis-row['prefix_is'])<1e-12 and abs(snis-row['prefix_snis'])<1e-12
    replicated+=2
pilot=ROOT/'analysis/simulator-development-v1';worlds=[json.loads(p.read_text()) for p in pilot.glob('*.json') if p.name not in ['manifest.json','freeze.json']]
lookup={(w['persistent'],w['rotate_alias'],w['policy'],w['seed']):w for w in worlds};controls=0
for key,a in lookup.items():
    if not key[0] and not key[1]:
        for alt in [(False,True),(True,True)]:
            b=lookup[(*alt,*key[2:])]
            assert [e['protection'] for e in a['episodes']]==[e['protection'] for e in b['episodes']]
            assert [e['trace'] for e in a['episodes']]==[e['trace'] for e in b['episodes']]
            controls+=1
result=dict(mutations_detected=mutations,scalar_estimates_replicated=replicated,paired_identity_controls=controls,validation_steps=summary['steps'])
(ROOT/'analysis/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
if '--inventory' not in sys.argv:raise SystemExit(0)
assert not (ROOT/'data/runtime-provenance.json').exists(), 'Refusing to overwrite historical runtime provenance'
provenance=dict(python=sys.version,platform=platform.platform(),dependencies={d.metadata['Name']:d.version for d in importlib.metadata.distributions()},upstreams={})
for name in ['cyberwheel','activeNS','CoADAM']:
    path=ROOT/'data/source-cache'/name
    paths=subprocess.check_output(['git','ls-files'],cwd=path,text=True).splitlines()
    provenance['upstreams'][name]=dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=path,text=True).strip(),tracked_files={f:hashlib.sha256((path/f).read_bytes()).hexdigest() for f in paths if (path/f).is_file()})
(ROOT/'data/runtime-provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
