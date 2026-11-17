# Study B: review routing on CIFAR-10H

Code for Phase II/III of *Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets*.
Protocol: [`phase2_experiment_plan.md`](../../research-workflow/phase-2-experiment-plan/phase2_experiment_plan.md). Reports: [Phase III](../../research-workflow/phase-3-coding-baseline-validation/phase3_coding_and_baseline_validation.md) and [Phase III addendum (model-arm results)](../../research-workflow/phase-3b-model-arm-results/phase3b_model_arm_results.md).

## Status
| Part | Status |
|------|--------|
| Unit tests (19) | Run, all pass (`results/test_log.txt`) |
| Label-only baseline on real CIFAR-10H | Run (`results/label_only.json`) |
| Model arm with **fallback features** (gradient + colour, 372-d) | **Run**, 10 seeds (`results_model_fallback/`). Weak model, 60% accuracy. |
| Model arm with **ResNet-18 features** (pre-specified backbone) | **Not run.** Use `Study_B_Colab.ipynb`. Its torch cells were never executed by the author. |
| Colab notebook, non-torch cells | Executed end to end in a fresh folder; identical output (`results/notebook_dry_run_log.txt`) |

## Quick start: Google Colab (recommended)
1. Upload `Study_B_Colab.ipynb` to Colab, set Runtime > T4 GPU, then Runtime > Run all.
2. Read the printed H2 line and download `outputs.zip`.

## Run locally
Python 3, numpy, pandas, scikit-learn, scipy, matplotlib (torch + torchvision only for `extract_features.py`).
```bash
git clone https://github.com/jcpeterson/cifar-10h.git
mkdir -p data_c10h && cp cifar-10h/data/cifar10h-counts.npy data_c10h/ && unzip cifar-10h/data/cifar10h-raw.zip -d data_c10h/raw
python run_tests.py
python run_label_only.py --c10h data_c10h --out results
python validate_digits.py                      # pipeline check on bundled digits; NOT a result
# ResNet-18 model arm (needs torch)
python extract_features.py --limit 500 --out timing.npz
python extract_features.py --out feats.npz
python run_model_arm.py --features feats.npz --c10h data_c10h --out results_model
# fallback (numpy only; needs a local copy of the CIFAR-10 python batches)
python run_fallback.py --cifar PATH_TO/cifar-10-batches-py --c10h data_c10h --out results_model_fallback
```

## Files
`routing.py` arms and scores | `stats.py` paired bootstrap | `labels.py` CIFAR-10H loader | `experiment.py` all arms x budgets x reviewers x seeds | `model.py` classifier | `load_cifar10_safe.py` pickle loader that cannot run code | `features_fallback.py` numpy features | `extract_features.py` ResNet-18 features | `run_*.py` runners | `tests/` 19 tests.

## Data and licence
CIFAR-10H is CC BY-NC-SA 4.0 (Peterson, Battleday, Griffiths, Russakovsky, ICCV 2019); it is **not** included. CIFAR-10 images are not included either. Tables in `results*/` derived from CIFAR-10H carry the same licence. They were computed from the raw annotator file with 16 low-attention annotators excluded (this reproduces the published `counts.npy` exactly). The fallback run used a third-party copy of CIFAR-10 (see addendum Section 2); the Colab notebook uses the official torchvision download.
