# Reproduce the adaptive-memory study

## A-OPS reference execution

Use a separate environment so the simulator dependencies remain unchanged:

```powershell
uv venv --python 3.9.25 .venv-aops
uv pip install --python .venv-aops/Scripts/python.exe -r requirements-aops-lock.txt
.venv-aops/Scripts/python.exe src/verify_aops_math.py
.venv-aops/Scripts/python.exe src/audit_aops_independent_arm.py
.venv/Scripts/python.exe src/analyze_aops_reference.py
.venv/Scripts/python.exe src/report_aops_reference.py
```

Acquire the pinned A-OPS source as described below first. The last two commands validate/report saved results without rerunning training. For a new collection use run_aops_reference.py with a new output directory. The archived calls were `--output analysis/aops-reference-pilot-v1 --rounds 5`, `--output analysis/aops-reference-development-v1 --start 1 --experiments 3 --rounds 20`, and `--output analysis/aops-reference-replay-v1 --rounds 5`. Never overwrite the archived outputs. See protocol/aops-reference-v1.md and analysis/aops-reference-report.md for seed, resource, dependency, and upstream-comparator caveats. Reduced execution is not full published-figure reproduction.

## Active-evidence development phase

Verify the new saved results without recollecting or overwriting frozen data:

```powershell
.venv/Scripts/python.exe src/verify_active_evidence.py
.venv/Scripts/python.exe src/analyze_carryover_order.py
.venv/Scripts/python.exe src/report_carryover_order.py
```

The exact screen runner is src/active_evidence_screen.py; the native runner is src/carryover_order.py. Each intentionally refuses to overwrite its output directory. Recollection must use a separate checkout without the archived output directory, while preserving the published evidence. Frozen revisions and file hashes are recorded in each output's freeze.json. The two studies are development diagnostics, not held-out validation of a proposed new algorithm.

Acquire and audit the public reference dataset separately:

```powershell
git clone https://github.com/google-deepmind/active_ops.git data/source-cache/active_ops
git -C data/source-cache/active_ops checkout --detach 5c7b24515adadbaf89feb84232190bad96221c04
.venv/Scripts/python.exe src/audit_aops_data.py
```

The audit uses the existing NumPy environment and does not execute the upstream notebook or GP optimizer. Data are attributed to Konyushkova et al., Active Offline Policy Selection, NeurIPS 2021, DeepMind, under CC BY 4.0 as stated upstream; code is Apache-2.0. Third-party data/source are acquired from upstream and not vendored here. No full A-OPS algorithm or published figure reproduction is claimed.

Use Python 3.10.20. The verified environment is Windows with CPU PyTorch. Other platforms have not been execution-tested. Original project material remains unlicensed; third-party terms are separate.

## Acquire upstream source

Run from this repository:

```powershell
git clone https://github.com/ORNL/cyberwheel.git data/source-cache/cyberwheel
git -C data/source-cache/cyberwheel checkout --detach 6e535b50eea991ed48bb9eeb46b4b267090cc897
uv venv --python 3.10.20
uv pip install --python .venv/Scripts/python.exe --extra-index-url https://download.pytorch.org/whl/cpu --index-strategy unsafe-best-match -r requirements-simulator-lock.txt
```

The lock records exact installed versions, not distribution hashes. The pinned source checkout is imported directly. Optional upstream training and visualization extras are not used. Compare tracked source bytes against data/runtime-provenance.json if reproducing on a platform with different Git line-ending settings. Analysis uses NumPy and does not import Cyberwheel.

## Verify the released data

```powershell
.venv/Scripts/python.exe src/analyze_validation.py
.venv/Scripts/python.exe src/verify_validation.py
.venv/Scripts/python.exe src/build_manuscript.py
.venv/Scripts/python.exe src/verify_manuscript.py
```

The optional --inventory flag inventories the locally acquired activeNS and CoADAM checkouts. For that inventory acquire the pinned revisions recorded in data/runtime-provenance.json. No MATLAB execution is required. The flag refuses to overwrite the released historical provenance file; normal verification does not require those additional checkouts.

## New collection

```powershell
.venv/Scripts/python.exe src/memory_study.py --output analysis/my-reproduction --worlds 64
```

The collector refuses to overwrite an existing output directory. It runs four local CPU processes and saves every attempted world, including failures. The released analyzer currently targets analysis/validation-v1 and asserts the frozen 64-world design; adapt a copy for a new collection and label the deviation. Never overwrite the original raw evidence. No remote targets, emulator, HPC scheduler, credentials, or GPU are involved.

The raw corpus schema records network, world seed, memory law, policy, eight encounters, macro-action and probability, memory before/after, 40 native-action observations, original protected targets, impacted targets, outcome, and trace digest. A world is the statistical sampling unit. Seeds are paired across candidate policies and settings, not independent across all 1,024 files.

## Manuscript

paper/main.tex is self-contained. Compile with an up-to-date ACM acmart installation including TikZ and pgfplots. The delivered ZIP has main.tex, README.md, validation.json, and verification material. Its figures and tables come from released verified summaries. The separate repository contains the full raw corpus; the ZIP contains the checks and numerical evidence needed to inspect the manuscript.

The local PDF used a pinned Tectonic compiler in a network-disabled Docker container. Compiler receipts retain the command and source hash. The built-in editor compiler failed during Windows sandbox setup, so that preview is not claimed verified. See delivery validation for clean rebuild and visual inspection status.
