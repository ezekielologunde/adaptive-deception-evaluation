# Reproduce the adaptive-memory study

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
