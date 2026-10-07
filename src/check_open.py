"""Interface/numerical controls for upstream OPEN, not paper reproduction."""
import hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'data/source-cache/activeNS'))
import numpy as np
import torch
from Src.OPE.hybrid import OPEN_2
from Src.OPE.stationary import WIS

out=ROOT/'analysis/open-controls-v0.json'
if out.exists():raise SystemExit('Refusing to overwrite controls')
torch.set_num_threads(1)
rows=[];start=time.perf_counter()
for reward in [0.,1.]:
    torch.manual_seed(7);np.random.seed(7)
    data=np.ones((100,1,2));data[:,:,1]=reward
    model=OPEN_2(p=3)
    prediction=model.predict(data,3).tolist()
    rows.append(dict(reward=reward,predictions=prediction,
                     max_error=max(abs(x-reward) for x in prediction)))
data=np.array([[[1.,0.]],[[2.,1.]],[[.5,.5]]])
wis=WIS().predict(data,1).item()
assert abs(wis-2.25/3.5)<1e-12
result=dict(status='interface controls only; published experimental replication pending',
    open_constant_controls=rows,wis=wis,wis_independent_check=True,
    seconds=time.perf_counter()-start,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
