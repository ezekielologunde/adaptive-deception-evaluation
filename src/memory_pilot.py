"""Development study in pinned Cyberwheel. No network/emulator operations."""
import argparse
import contextlib
import hashlib
import importlib
import io
import json
import random
import subprocess
import time
from pathlib import Path
from simulator_smoke import make_environment, ROOT, UPSTREAM

POLICIES={'logging':[1/3]*3,'dmz':[.6,.2,.2],'server':[.2,.6,.2],'user':[.2,.2,.6]}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()

def run_world(seed,policy,persistent,rotate,episodes=8):
    with contextlib.redirect_stderr(io.StringIO()),contextlib.redirect_stdout(io.StringIO()):
        env=make_environment(seed)
    from cyberwheel.red_agents.strategies.server_downtime import ServerDowntime
    module=importlib.import_module('cyberwheel.blue_actions.actions.DeployDecoyHost')
    original_id=module.generate_id
    memory={}
    decision_rng=random.Random(seed+100000)
    alias_salt='stable'
    def alias(name):return digest([alias_salt,name])
    class RememberSuccessfulTargets:
        @classmethod
        def select_target(cls,agent):
            # Only discovered host identifiers and observed prior impact successes.
            candidates=[name for name,h in agent.history.hosts.items()
                        if not h.impacted and name in agent.network.hosts
                        and memory.get(alias(name),0)>0]
            if candidates:
                best=max(memory[alias(name)] for name in candidates)
                candidates=sorted(n for n in candidates if memory[alias(n)]==best)
                return agent.network.hosts[random.choice(candidates)]
            return ServerDowntime.select_target(agent)
    rows=[]
    try:
        for episode in range(episodes):
            if not persistent:memory={}
            alias_salt=str(episode) if rotate else 'stable'
            before=dict(memory)
            # Network/ordinary ART history reset; separate memory is retained as declared.
            env.reset(seed=seed*100+episode)
            env.red_agent.strategy=RememberSuccessfulTargets
            ids=random.Random(seed*100+episode+900000)
            module.generate_id=lambda seed=None: format(ids.getrandbits(128),'032x')
            probs=POLICIES[policy]
            choice=decision_rng.choices(range(3),weights=probs)[0]
            targets=set(env.network.server_hosts.data_set)-set(env.network.decoys)
            impacts=set(); trace=[]
            for step in range(40):
                action=choice+1 if step<3 else 0
                _,_,done,truncated,info=env.step({'blue':action})
                observed=dict(action=info['red_action'],target=info['red_action_dst'],success=bool(info['red_action_success']))
                if observed['action']=='impact' and observed['success']:
                    key=alias(observed['target'])
                    memory[key]=memory.get(key,0)+1
                    if observed['target'] in targets:impacts.add(observed['target'])
                trace.append(dict(step=step,blue_action=action,blue_success=bool(info['blue_action_success']),
                    observed=observed,oracle_decoy_interaction=bool(info['decoy_attacked'])))
            assert targets
            rows.append(dict(episode=episode,seed=seed*100+episode,choice=choice,propensity=probs[choice],
                probabilities=probs,action_mask=[True,True,True],memory_before=before,memory_after=dict(memory),
                history_digest=digest(trace),trace=trace,protected_targets=sorted(targets),
                impacted_targets=sorted(impacts),protection=1-len(impacts)/len(targets),
                decoys=len(env.network.decoys),truncated=bool(truncated)))
    finally:
        module.generate_id=original_id
        env.close()
    return dict(seed=seed,policy=policy,persistent=persistent,rotate_alias=rotate,episodes=rows)

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--worlds',type=int,default=8)
    args=p.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    freeze=dict(status='development pilot, not confirmatory research',worlds_per_cell=args.worlds,
        code_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        upstream_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=UPSTREAM,text=True).strip(),
        policies=POLICIES,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (args.output/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    start=time.perf_counter(); failures=[]; count=0
    for persistent in [False,True]:
        for rotate in [False,True]:
            for policy in POLICIES:
                for i in range(args.worlds):
                    # Matched seeds within cell comparisons; logs and target rollouts independent.
                    seed=1000+i+(10000 if policy!='logging' else 0)
                    name=f'{int(persistent)}-{int(rotate)}-{policy}-{i:03d}'
                    try: result=run_world(seed,policy,persistent,rotate)
                    except Exception as e:
                        result=dict(status='failed',exception=type(e).__name__,message=str(e));failures.append(name)
                    (args.output/(name+'.json')).write_text(json.dumps(result,sort_keys=True)+'\n')
                    count+=1
                print('Completed cell',persistent,rotate,policy,flush=True)
    manifest={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in args.output.glob('*.json')}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(attempts=count,failures=failures,seconds=time.perf_counter()-start)))

if __name__=='__main__':main()
