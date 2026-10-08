"""Package the verified manuscript and full verification inputs; no publication."""
import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'deliverables';dest.mkdir(exist_ok=True)
stem='attacker_memory_acm'
for suffix,source in [('tex',ROOT/'paper/main.tex'),('pdf',ROOT/'paper/build/main.pdf')]:shutil.copyfile(source,dest/f'{stem}.{suffix}')
validation=json.loads((ROOT/'analysis/manuscript-verification.json').read_text())
validation['research_checks']=json.loads((ROOT/'analysis/verification.json').read_text())
validation['status']='completed bounded research draft; not journal novelty clearance or submission'
validation['compiler']='Tectonic; built-in compiler sandbox setup failed; cache populated for missing math fonts before offline build'
validation['source_hash_matches_compilation']=json.loads((ROOT/'paper/build/receipt.json').read_text())['source_sha256']==validation['source_sha256']
assert validation['source_hash_matches_compilation']
qa=ROOT/'analysis/delivery-qa.json'
validation['delivery_qa']=json.loads(qa.read_text()) if qa.exists() else {'status':'pending clean rebuild and final visual review'}
(dest/'validation.json').write_text(json.dumps(validation,indent=2)+'\n')
readme='''# ACM manuscript and complete verification evidence

Compile main.tex in Overleaf with a current TeX Live distribution. The source is self-contained (acmart, TikZ, pgfplots). This is a completed bounded research draft, not a claim of journal acceptance or established algorithmic novelty.

Author: Ezekiel Ologunde, Independent Researcher, Boston, MA, USA; ologunde@bu.edu. Original work remains unlicensed. Third-party source checkouts and paper PDFs are not included.

validation.json contains automated and delivery checks. verification/repository contains full original simulation traces, frozen protocols, source hashes, analysis programs, manuscript template, and environment lock. Read its REPRODUCE.md. Run analysis using Python 3.10 and NumPy; acquire the pinned Cyberwheel source only if collecting new simulation worlds. The verification scripts are independently written checks, not an independent investigator's replication.

The PDF was built with a pinned isolated compiler; Overleaf's hosted environment itself was not tested. The research repository is https://github.com/ezekielologunde/adaptive-deception-evaluation .
'''
with zipfile.ZipFile(dest/'attacker_memory_overleaf.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    z.write(ROOT/'paper/main.tex','main.tex');z.writestr('README.md',readme);z.write(dest/'validation.json','validation.json')
    for folder in ['src','protocol','analysis']:
        for p in sorted((ROOT/folder).rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.suffix in ['.py','.json','.md']:
                z.write(p,'verification/repository/'+p.relative_to(ROOT).as_posix())
    for p in [ROOT/'README.md',ROOT/'REPRODUCE.md',ROOT/'THIRD_PARTY_NOTICES.md',ROOT/'requirements-simulator-lock.txt',ROOT/'data/runtime-provenance.json',ROOT/'data/source-audit-v0.json',ROOT/'paper/main.tex',ROOT/'paper/manuscript-template.tex']:
        z.write(p,'verification/repository/'+p.relative_to(ROOT).as_posix())
    for name in ['receipt.json','stdout.txt','stderr.txt']:
        z.write(ROOT/'paper/build'/name,'verification/compiler/'+name)
        if (ROOT/'paper/clean-build'/name).exists():z.write(ROOT/'paper/clean-build'/name,'verification/clean-compiler/'+name)
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.iterdir() if p.is_file() and p.name!='SHA256.json'}
(dest/'SHA256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps(hashes,indent=2))
