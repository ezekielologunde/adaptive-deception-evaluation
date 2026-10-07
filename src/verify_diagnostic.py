"""Check retained analytical results and frozen source integrity."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'analysis/memory-diagnostic-v0.json').read_text())
for name,key in [('src/diagnose_memory.py','source_sha256'),('protocol/pilot-v0.md','protocol_sha256')]:
    body=(ROOT/name).read_bytes()
    assert hashlib.sha256(body).hexdigest()==r[key]
    committed=subprocess.check_output(['git','show',r['code_revision']+':'+name],cwd=ROOT)
    assert body==committed
assert len(r['rows'])==r['independently_computed_cases']==36
for row in r['rows']:
    p=row['decoy_probability']; n=row['horizon']; learn=row['learning_probability']
    # Closed-form stationary two-state chain, independent of both recursions.
    rise=p*learn; fall=(1-p)*0.05
    rate=rise+fall
    average_awareness=0 if row['reset_memory'] or rise==0 else (rise/rate)*(1-(1-(1-rate)**n)/(n*rate))
    expected=0.5+0.4*p-0.8*p*average_awareness
    assert abs(expected-row['forward'])<1e-12
    assert abs(expected-row['backward'])<1e-12
print('36 cases verified against closed form; source and pre-run Git freeze match')
