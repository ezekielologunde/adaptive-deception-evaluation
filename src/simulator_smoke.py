"""Run only Cyberwheel's in-process simulator with a small fixed workload."""
import json
import sys
import time
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
UPSTREAM=ROOT/'data/source-cache/cyberwheel'
sys.path.insert(0,str(UPSTREAM))

def make_environment(seed=7,network_name='15-host-network.yaml'):
    import yaml
    # Upstream's utils exports must initialize before network classes.
    import cyberwheel.utils
    from cyberwheel.network.network_base import Network
    from cyberwheel.utils import get_service_map, set_seed
    from cyberwheel.cyberwheel_envs.cyberwheel_rl import CyberwheelRL
    configs=UPSTREAM/'cyberwheel/data/configs'
    args=SimpleNamespace(**yaml.safe_load((configs/'environment/art_agent_vs_rl_blue.yaml').read_text()))
    args.num_steps=40
    args.agent_config={side:yaml.safe_load((configs/(''+side+'_agent')/name).read_text())
                       for side,name in args.agents.items()}
    set_seed(seed)
    network=Network.create_network_from_yaml(str(configs/'network'/network_name))
    args.service_mapping={network.name:get_service_map(network)}
    return CyberwheelRL(args,network=network,evaluation=True)

def main():
    out=ROOT/'analysis/simulator-smoke-v1.json'
    if out.exists():raise SystemExit('Refusing to overwrite smoke evidence')
    start=time.perf_counter()
    result={'status':'started','seed':7,'steps':[]}
    try:
        env=make_environment()
        obs,_=env.reset(seed=7)
        result['action_mask']=env.action_mask['blue']
        for step in range(40):
            # One actual decoy deployment, then native no-op actions.
            action=1 if step==0 else 0
            obs,reward,done,truncated,info=env.step({'blue':action})
            result['steps'].append({k:info[k] for k in ['red_action','red_action_success','blue_action','blue_action_success','decoy_attacked','blue_reward','red_reward']})
        result['status']='passed'
        result['hosts']=len(env.network.hosts)
        result['decoys']=len(env.network.decoys)
        result['observed_impacts']=[name for name,h in env.red_agent.history.hosts.items() if h.impacted]
        env.close()
    except Exception as e:
        result.update(status='failed',exception=type(e).__name__,message=str(e))
        raise
    finally:
        result['elapsed_seconds']=time.perf_counter()-start
        out.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='steps'},indent=2))

if __name__=='__main__':main()
