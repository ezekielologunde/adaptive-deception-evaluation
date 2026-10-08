"""Exact constructed-model screening, with a classical Bayesian optimum baseline."""
from functools import lru_cache
from pathlib import Path
import hashlib,itertools,json,math,subprocess
ROOT=Path(__file__).resolve().parents[1]

def probability(theta,action,x,damage,transfer):
    return max(0.,(.9 if theta==action else .4)-damage*(x[action]+transfer*x[1-action]))

def branch(p,action,x,damage,transfer):
    q0=probability(0,action,x,damage,transfer);q1=probability(1,action,x,damage,transfer)
    for y in (0,1):
        l0=q0 if y else 1-q0;l1=q1 if y else 1-q1
        mass=(1-p)*l0+p*l1
        if mass>0:yield y,mass,p*l1/mass

def increment(x,a):return tuple(v+int(i==a) for i,v in enumerate(x))
def expected(p,a,x,d,k):return (1-p)*probability(0,a,x,d,k)+p*probability(1,a,x,d,k)
def terminal(p,x,d,k):
    vals=[10*expected(p,a,x,d,k) for a in (0,1)]
    a=max(range(2),key=lambda j:vals[j]);return vals[a],a

def planner(d,k,stationary=False):
    @lru_cache(None)
    def solve(p,x,b):
        stop,_=terminal(p,x,d,k);values=[stop]
        if b:
            for a in (0,1):
                nx=x if stationary else increment(x,a)
                values.append(sum(m*(-(1-y)+solve(post,nx,b-1)[0]) for y,m,post in branch(p,a,x,d,k)))
        choice=max(range(len(values)),key=lambda j:values[j])
        return values[choice],choice-1 # -1 means stop; exact tie prefers stop
    return solve

def evaluate(p,d,k,b,method):
    exact=planner(d,k);stationary=planner(d,k,True)
    def walk(belief,x,left):
        if not left or method=='stop':actions=[(-1,1.)]
        elif method=='uniform':actions=[(0,.5),(1,.5)]
        else:
            solver=stationary if method=='stationary' else exact
            actions=[(solver(belief,x,1 if method=='one_step' else left)[1],1.)]
        result=[0.]*6
        for a,pa in actions:
            if a==-1:
                value,selected=terminal(belief,x,d,k)
                oracle=10*sum(m*max(probability(theta,j,x,d,k) for j in (0,1)) for theta,m in [(0,1-belief),(1,belief)])
                entropy=-sum(m*math.log2(m) for m in [belief,1-belief] if m>0)
                v=[value,0.,0.,oracle-value,9.-oracle,entropy]
                result=[r+pa*z for r,z in zip(result,v)]
            else:
                for y,m,post in branch(belief,a,x,d,k):
                    v=walk(post,increment(x,a),left-1);v[1]+=1-y;v[2]+=1
                    result=[r+pa*m*z for r,z in zip(result,v)]
        return result
    v=walk(p,(0,0),b)
    out=dict(zip(['terminal_value','probe_loss','expected_probes','selection_regret','state_degradation','posterior_entropy'],v))
    out['net_value']=v[0]-v[1]
    assert abs((9-out['net_value'])-(v[1]+v[3]+v[4]))<1e-10
    if method=='bayes':assert abs(out['net_value']-exact(p,(0,0),b)[0])<1e-10
    return out

def main():
    out=ROOT/'analysis/active-evidence-screen-v1';out.mkdir(exist_ok=False)
    files=['src/active_evidence_screen.py','protocol/active-evidence-screen-v1.md']
    freeze=dict(revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),files={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},status='constructed exact diagnostic; not new algorithm or native simulator evidence')
    (out/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
    rows=[]
    for p,d,k,b in itertools.product([.25,.5,.75],[0.,.02,.08,.2],[0.,.5,1.],[1,2,3]):
        cell={method:evaluate(p,d,k,b,method) for method in ['stop','uniform','stationary','one_step','bayes']}
        assert all(cell['bayes']['net_value']>=v['net_value']-1e-10 for v in cell.values())
        if d==0:assert abs(cell['bayes']['net_value']-cell['stationary']['net_value'])<1e-10
        rows.append(dict(prior=p,damage=d,transfer=k,budget=b,methods=cell))
    (out/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.json')}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(cases=len(rows),method_cases=len(rows)*5,stationary_strictly_worse=sum(r['methods']['stationary']['net_value']<r['methods']['bayes']['net_value']-1e-9 for r in rows),one_step_strictly_worse=sum(r['methods']['one_step']['net_value']<r['methods']['bayes']['net_value']-1e-9 for r in rows))))
if __name__=='__main__':main()
