"""Record exact source bytes from pinned public checkouts without running them."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SOURCES={
    'cyberwheel':dict(url='https://github.com/ORNL/cyberwheel.git',
        commit='6e535b50eea991ed48bb9eeb46b4b267090cc897',license='MIT',files=[
        'README.md','LICENSE','pyproject.toml','requirements.txt',
        'cyberwheel/cyberwheel_envs/cyberwheel_rl.py',
        'cyberwheel/red_agents/art_agent.py','cyberwheel/blue_agents/random_blue_agent.py']),
    'activeNS':dict(url='https://github.com/yashchandak/activeNS.git',
        commit='46e74eb0d633ca9220f44cfb6a5bff9fef89ee0e',license='Apache-2.0',files=[
        'README.md','LICENSE','environment.yml','Src/OPE/hybrid.py',
        'Src/OPE/passive.py','Src/OPE/stationary.py','Src/OPE/Regression.py'])}

def main():
    result={}
    for name,meta in SOURCES.items():
        checkout=ROOT/'data/source-cache'/name
        revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=checkout,text=True).strip()
        assert revision==meta['commit']
        entries={}
        for path in meta['files']:
            body=subprocess.check_output(['git','show',revision+':'+path],cwd=checkout)
            entries[path]=dict(sha256=hashlib.sha256(body).hexdigest(),bytes=len(body),
                url='https://raw.githubusercontent.com/'+meta['url'].split('github.com/')[1][:-4]+'/'+revision+'/'+path)
        result[name]=dict(url=meta['url'],commit=revision,license=meta['license'],files=entries)
    out=ROOT/'data/source-audit-v0.json'
    out.write_text(json.dumps(dict(status='source audit only; third-party implementations not executed',sources=result),indent=2)+'\n')
    print(sum(len(x['files']) for x in result.values()),'canonical Git source files hashed')

if __name__=='__main__':
    main()
