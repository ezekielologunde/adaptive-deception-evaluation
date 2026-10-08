# Manuscript

main.tex is the self-contained five-page ACM sigconf, nonacm research draft. manuscript-template.tex is the authored source with numeric insertion markers; src/build_manuscript.py fills them from verified results. The final PDF and Overleaf package are in ../deliverables.

The paper reports a bounded simulator result, not a novel estimator, journal acceptance, or production efficacy. It includes two figures, three tables, seven primary source/artifact references, the confirmed author identity, and explicit limitations. src/verify_manuscript.py independently checks the rendered-source numbers; analysis/delivery-qa.json and analysis/visual-review.json record the clean compilation and page inspection.

The built-in compiler failed during sandbox setup. A pinned Tectonic build and clean rebuild succeeded, with identical extracted PDF text and all fonts embedded. Nonfatal font diagnostics, underfull warnings, and a 1.44199pt final-column balancing warning remain disclosed. No visible clipping was found. Overleaf's hosted service itself was not tested.
