"""Exact illustrative missing-outcome check, not a novel theorem or empirical study."""
from fractions import Fraction as F
import json
from pathlib import Path
worlds=[]
for risk,observe_harm,observe_safe in [(F(1,10),F(1,2),F(1,2)),(F(2,5),F(1,8),F(3,4))]:
    visible_harm=risk*observe_harm
    visible_safe=(1-risk)*observe_safe
    missing=1-visible_harm-visible_safe
    assert all(0<p<1 for p in [observe_harm,observe_safe])
    assert (visible_harm,visible_safe,missing)==(F(1,20),F(9,20),F(1,2))
    worlds.append(dict(true_harm=str(risk),observation_given_harm=str(observe_harm),observation_given_safe=str(observe_safe),observed_harm_mass=str(visible_harm),observed_safe_mass=str(visible_safe),missing_mass=str(missing),complete_case_harm=str(visible_harm/(visible_harm+visible_safe)),better_than_baseline=risk<F(1,5)))
assert worlds[0]['better_than_baseline'] and not worlds[1]['better_than_baseline']
report={'scope':'Exact constructed illustration of standard nonidentification; no novelty claim','baseline_harm':'1/5','worst_case_harm_interval':['1/20','11/20'],'worlds':worlds,'interpretation':'Identical visible outcomes and positive observation probabilities do not identify whether deployment improves on baseline. No informative proxy, known missingness mechanism or randomized audit labels are assumed.'}
Path('analysis/missing-outcome-identifiability-check.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
