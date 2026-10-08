"""Read the final TeX independently of its builder and verify numerical content."""
import re,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
text=(ROOT/'paper/main.tex').read_text();s=json.loads((ROOT/'analysis/validation-summary.json').read_text())
tables={}
for block in re.findall(r'\\begin\{table\*?\}.*?\\end\{table\*?\}',text,re.S):
    label=re.search(r'\\label\{([^}]+)\}',block).group(1)
    body=block.split(r'\midrule',1)[1].split(r'\bottomrule',1)[0]
    tables[label]=[[v.strip() for v in row.strip().split('&')] for row in body.split(r'\\') if row.strip()]
policy={'D':'dmz','S':'server','U':'user'};cells=0
assert [len(tables[k]) for k in ['tab:results','tab:contrasts','tab:decisions']]==[12,4,4]
for row in tables['tab:results']:
    n,m,p,*values=row
    r=next(x for x in s['rows'] if x['network'].startswith(n+'-') and x['persistent']==(m=='Retained') and x['policy']==policy[p])
    for v,k in zip(values,['online_mean','online_se','prefix_is','prefix_snis','history_discarding']):assert v==format(r[k],'.4f');cells+=1
for n,m,v,se in tables['tab:contrasts']:
    r=next(x for x in s['paired_contrasts'] if x['network'].startswith(n+'-') and x['persistent']==(m=='Retained') and x['a']=='dmz' and x['b']=='user')
    assert v==format(r['mean'],'.4f') and se==format(r['se'],'.4f');cells+=2
for n,m,p,f,e,decision in tables['tab:decisions']:
    d=next(x for x in s['decisions'] if x['network'].startswith(n+'-') and x['persistent']==(m=='Retained'))
    r=next(x for x in s['rows'] if x['network']==d['network'] and x['persistent']==d['persistent'] and x['policy']==policy[p])
    assert policy[p]==d['offline_ranking'][0] and f==format(d['bootstrap_winner_frequencies'][policy[p]],'.3f') and e==format(min(r['ess']),'.2f') and decision.lower()==d['selection'];cells+=4
coords=re.findall(r'\(([123]),([0-9.]+)\) \+- \(0,([0-9.]+)\)',text)
assert len(coords)==12
for (i,y,e),r in zip(coords,s['rows']):assert y==format(r['online_mean'],'.8f') and e==format(r['online_se'],'.8f')
labels=re.findall(r'\\label\{([^}]+)\}',text);refs=re.findall(r'\\ref\{([^}]+)\}',text)
assert len(labels)==len(set(labels)) and set(refs)<=set(labels)
assert '\u2014' not in text and '@@' not in text
for value in ['Ezekiel Ologunde','Independent Researcher','Boston','USA','ologunde@bu.edu']:assert value in text
result=dict(source_sha256=hashlib.sha256((ROOT/'paper/main.tex').read_bytes()).hexdigest(),numeric_table_cells=cells,plot_means_and_errors=12,unique_labels=len(labels),references_resolved=len(refs),status='passed')
(ROOT/'analysis/manuscript-verification.json').write_text(json.dumps(result,indent=2)+'\n');print(result)
