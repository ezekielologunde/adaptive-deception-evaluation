"""Native order/carryover diagnostic, separate from frozen validation-v1."""
import contextlib,io,random,importlib,json,hashlib,subprocess,time
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
from simulator_smoke import make_environment,ROOT,UPSTREAM

PREFIX={'DDUU':[0,0,2,2],'UUDD':[2,2,0,0],'none':[]}
POLICIES={'dmz':[.6,.2,.2],'server':[.2,.6,.2],'user':[.2,.2,.6]}
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()
def run(seed,network,law,prefix,policy):
    with contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):env=make_environment(seed,network)
    from cyberwheel.red_agents.strategies.server_downtime import ServerDowntime
    mod=importlib.import_module('cyberwheel.blue_actions.actions.DeployDecoyHost');original=mod.generate_id
    memory={}
    class Strategy:
        @classmethod
        def select_target(cls,agent):
            candidates=[n for n,h in agent.history.hosts.items() if not h.impacted and n in agent.network.hosts and memory.get(n,0)>0]
            if candidates:
                best=max(memory[n] for n in candidates)
                return agent.network.hosts[random.choice(sorted(n for n in candidates if memory[n]==best))]
            return ServerDowntime.select_target(agent)
    schedule=[('prefix',i,c) for i,c in enumerate(PREFIX[prefix])]+[('evaluation',i,None) for i in range(4,8)]
    rows=[]
    try:
        for phase,slot,choice in schedule:
            if law=='reset':memory={}
            if law=='decay':memory={n:c*.5 for n,c in memory.items()}
            before=dict(memory);env.reset(seed=seed*100+slot);env.red_agent.strategy=Strategy
            ids=random.Random(seed*100+slot+900000);mod.generate_id=lambda seed=None:format(ids.getrandbits(128),'032x')
            probs=[float(j==choice) for j in range(3)] if phase=='prefix' else POLICIES[policy]
            if choice is None:choice=random.Random(seed*100+slot+2000000).choices(range(3),weights=probs)[0]
            targets=set(env.network.server_hosts.data_set)-set(env.network.decoys);impacts=set();trace=[]
            for step in range(40):
                a=choice+1 if step<3 else 0
                _,_,done,truncated,info=env.step({'blue':a})
                obs=dict(action=info['red_action'],target=info['red_action_dst'],success=bool(info['red_action_success']))
                if obs['action']=='impact' and obs['success']:
                    memory[obs['target']]=memory.get(obs['target'],0)+1
                    if obs['target'] in targets:impacts.add(obs['target'])
                trace.append(dict(step=step,blue_action=a,blue_target=info['blue_action_target'],blue_success=bool(info['blue_action_success']),observed=obs))
            rows.append(dict(phase=phase,slot=slot,choice=choice,probabilities=probs,propensity=probs[choice],memory_before=before,memory_after=dict(memory),protected_targets=sorted(targets),impacted_targets=sorted(impacts),protection=1-len(impacts)/len(targets),decoys=len(env.network.decoys),trace=trace,digest=digest(trace)))
    finally:mod.generate_id=original;env.close()
    return dict(seed=seed,network=network,law=law,prefix=prefix,policy=policy,episodes=rows)

def main():
    root=ROOT/'analysis/carryover-order-development-v1';root.mkdir(exist_ok=False)
    freeze=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),upstream=subprocess.check_output(['git','rev-parse','HEAD'],cwd=UPSTREAM,text=True).strip(),files={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['src/carryover_order.py','src/simulator_smoke.py','protocol/carryover-order-development-v1.md']},policies=POLICIES,prefixes=PREFIX)
    (root/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n');start=time.perf_counter();failures=[]
    with ProcessPoolExecutor(max_workers=4) as pool:
        jobs={}
        for network in ['15-host-network.yaml','25-host-network.yaml']:
            for law in ['reset','count','decay']:
                for prefix in PREFIX:
                    for policy in POLICIES:
                        for i in range(16):jobs[pool.submit(run,70000+i,network,law,prefix,policy)]=f'{network[:2]}-{law}-{prefix}-{policy}-{i:02d}'
        for i,f in enumerate(as_completed(jobs),1):
            name=jobs[f]
            try:result=f.result()
            except Exception as e:result=dict(status='failed',exception=type(e).__name__,message=str(e));failures.append(name)
            (root/(name+'.json')).write_text(json.dumps(result,sort_keys=True)+'\n')
            if i%96==0:print('Completed',i,flush=True)
    (root/'receipt.json').write_text(json.dumps(dict(attempts=len(jobs),failures=failures,seconds=time.perf_counter()-start),indent=2)+'\n')
    (root/'manifest.json').write_text(json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in root.glob('*.json')},indent=2)+'\n')
    print((root/'receipt.json').read_text())
if __name__=='__main__':main()
