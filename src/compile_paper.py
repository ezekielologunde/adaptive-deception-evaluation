"""Compile with the already verified portable compiler in an isolated container."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True)
p.add_argument('--output',type=Path,required=True);p.add_argument('--compiler-dir',type=Path,required=True)
p.add_argument('--populate-cache',action='store_true',help='Allow official bundle downloads into this dedicated compiler cache')
a=p.parse_args();source=a.source.resolve();out=a.output.resolve();compiler=a.compiler_dir.resolve()
assert hashlib.sha256((compiler/'tectonic').read_bytes()).hexdigest()=='a98aa59ad5c1df39a6c9e56cbfc5088f2b11d6c179c0130b97998e4bd46a46da'
out.mkdir(parents=True,exist_ok=True)
cmd=['docker','run','--rm',*(['--network','none'] if not a.populate_cache else []),'--read-only','--cap-drop','ALL','--security-opt','no-new-privileges',
     '--cpus','2','--memory','2g','--pids-limit','64','--tmpfs','/tmp:rw,exec,size=536870912',
     '--env','HOME=/tmp','--env','XDG_CACHE_HOME=/tex-cache',
     '--mount',f'type=bind,source={compiler},target=/compiler,readonly',
     '--mount',f'type=bind,source={compiler / "cache"},target=/tex-cache'+('' if a.populate_cache else ',readonly'),
     '--mount',f'type=bind,source={source.parent},target=/input,readonly',
     '--mount',f'type=bind,source={out},target=/output',
     'python@sha256:0dd364ba7e10242f07755449e3a3d0e35f9efd987952737b90def6709ab0c5ce',
     'sh','-c',f'cp /compiler/tectonic /tmp/tectonic && chmod +x /tmp/tectonic && /tmp/tectonic --keep-logs --outdir /output /input/{source.name}']
run=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
(out/'stdout.txt').write_text(run.stdout,encoding='utf-8');(out/'stderr.txt').write_text(run.stderr,encoding='utf-8')
receipt=dict(command=cmd,exit_code=run.returncode,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
pdf=out/source.with_suffix('.pdf').name
if run.returncode==0:receipt['pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
(out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(run.stdout,run.stderr)
raise SystemExit(run.returncode)
