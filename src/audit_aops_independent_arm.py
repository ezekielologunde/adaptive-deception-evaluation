"""Check reference variance conditional against its documented Gaussian model.

No reference code is modified. This concerns SingleBayesArm, not the GP.
"""
import json
import pathlib
import sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'data/source-cache/active_ops'))
import arm_model

rows = []
for observations in [[1.], [1., 2., 3.], [1., 2., 3.]*3]:
    for mu in [0., 2., 4.]:
        model = arm_model.SingleBayesArm(0.,1000.,1.,1000.,False)
        for value in observations:
            model.update(value)
        shape, scale = model._sigma2_cond_on_mu(mu)
        # Gaussian likelihood exp(-sum((x-mu)^2)/(2*sigma2)) times IG prior.
        expected_shape = 1.+len(observations)/2
        expected_scale = 1000.+sum((x-mu)**2 for x in observations)/2
        assert abs(shape-expected_shape)<1e-10
        rows.append(dict(n=len(observations), observations=observations, mu=mu,
                         reference_scale=scale, gaussian_conditional_scale=expected_scale,
                         matches=bool(np.isclose(scale,expected_scale,rtol=0,atol=1e-10))))
result = dict(source_revision='5c7b24515adadbaf89feb84232190bad96221c04',
              source_method='arm_model.SingleBayesArm._sigma2_cond_on_mu',
              tested_conditionals=len(rows), matches=sum(r['matches'] for r in rows), rows=rows,
              conclusion='The scale uses mean squared residual rather than summed squared residual. This differs from the documented iid Gaussian conditional when n>1 and residuals are nonzero. No upstream modification or published-result invalidation is asserted.')
(ROOT/'analysis/aops-independent-arm-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
