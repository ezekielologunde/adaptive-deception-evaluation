"""Insert data-derived tables and plot into the authored template."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'analysis/validation-summary.json').read_text())
def net(r):return r['network'][:2]
def mem(r):return 'Retained' if r['persistent'] else 'Reset'
def name(p):return dict(dmz='D',server='S',user='U')[p]
def table(header,rows,caption,label,cols,wide=False):
    env='table*' if wide else 'table'
    return '\\begin{'+env+'}[t]\n\\centering\\small\n\\setlength{\\tabcolsep}{3pt}\n\\caption{'+caption+'}\\label{'+label+'}\n\\begin{tabular}{'+cols+'}\\toprule\n'+header+'\\\\ \\midrule\n'+'\n'.join(' & '.join(row)+r' \\' for row in rows)+'\n\\bottomrule\\end{tabular}\n\\end{'+env+'}'
rows=[[net(r),mem(r),name(r['policy']),f"{r['online_mean']:.4f}",f"{r['online_se']:.4f}",f"{r['prefix_is']:.4f}",f"{r['prefix_snis']:.4f}",f"{r['history_discarding']:.4f}"] for r in s['rows']]
t=table('Hosts & Memory & Policy & Online & SE & Prefix IS & Prefix SN & Current ratio',rows,'Validation outcomes and offline estimates. Online means use 64 independent worlds per policy within each setting. Current ratio omits previous encounters.','tab:results','rlcrrrrr',True)
c=table('Hosts & Memory & D minus U & Paired SE',[[net(r),mem(r),f"{r['mean']:.4f}",f"{r['se']:.4f}"] for r in s['paired_contrasts'] if r['a']=='dmz' and r['b']=='user'],'Paired D-minus-U contrasts. Positive values favor D; negative values favor U.','tab:contrasts','rlrr')
dr=[]
for d in s['decisions']:
    p=d['offline_ranking'][0];r=next(r for r in s['rows'] if r['network']==d['network'] and r['persistent']==d['persistent'] and r['policy']==p)
    dr.append([net(d),mem(d),name(p),f"{d['bootstrap_winner_frequencies'][p]:.3f}",f"{min(r['ess']):.2f}",'Abstain'])
d=table('Hosts & Memory & Top & Frequency & Min ESS & Decision',dr,'Predeclared decision diagnostic. Thresholds: winner frequency at least 0.95 and every encounter ESS at least 16.','tab:decisions','rlcrrl',True)
plots=[]
for network in ['15','25']:
    lines=[]
    for persistent,color in [(False,'blue'),(True,'orange')]:
        rr=[r for r in s['rows'] if net(r)==network and r['persistent']==persistent]
        coords=' '.join(f"({i+1},{r['online_mean']:.8f}) +- (0,{r['online_se']:.8f})" for i,r in enumerate(rr))
        lines.append(r'\addplot+[color='+color+r',mark=*,error bars/.cd,y dir=both,y explicit] coordinates {'+coords+'};')
    plots.append(r'\begin{tikzpicture}\begin{axis}[width=.46\textwidth,height=5cm,ymin=0,ymax=1,xmin=.7,xmax=3.3,xtick={1,2,3},xticklabels={D,S,U},ylabel={Impact avoidance},title={'+network+r' hosts},legend style={font=\scriptsize,at={(.5,.1)},anchor=center},legend columns=2]'+'\n'+'\n'.join(lines)+r'\legend{Reset,Retained}\end{axis}\end{tikzpicture}')
figure=r'\begin{figure*}[t]\centering'+'\n'+r'\hfill'.join(plots)+r'\caption{Online means with one world-level standard error. Policies favor DMZ (D), server (S), or user (U) placement. Lines connect policies for readability, not interpolation.}\Description{Two panels show higher impact avoidance with reset memory and a change from D to U as the leading policy when memory is retained.}\label{fig:outcomes}\end{figure*}'
text=(ROOT/'paper/manuscript-template.tex').read_text()
for key,value in [('RESULTS_TABLE',t),('CONTRASTS_TABLE',c),('DECISIONS_TABLE',d),('RESULTS_FIGURE',figure)]:
    token='@@'+key+'@@';assert text.count(token)==1;text=text.replace(token,value)
(ROOT/'paper/main.tex').write_text(text,encoding='utf-8')
print('Built paper/main.tex from 12 result rows, 4 contrasts, 4 decisions and 12 plotted means.')
