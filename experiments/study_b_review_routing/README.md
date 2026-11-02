# Study B: review routing on CIFAR-10H

Code for Phase II/III of *Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets*.
Protocol: [`research-workflow/phase-2-experiment-plan`](../../research-workflow/phase-2-experiment-plan/phase2_experiment_plan.md). Validation report: [`research-workflow/phase-3-coding-baseline-validation`](../../research-workflow/phase-3-coding-baseline-validation/phase3_coding_and_baseline_validation.md).

## Status
| Part | Status |
|------|--------|
| Unit tests (15) | Run, all pass (`results/test_log.txt`) |
| Label-only baseline on real CIFAR-10H | Run (`results/label_only.json`) |
| Pipeline check on bundled digits | Run; **not** a Study B result |
| `extract_features.py` (torch) | **Never executed** |
| Model arm on real CIFAR-10 images | **Not run yet** |

## Set up
Python 3, numpy, pandas, scikit-learn, scipy (torch + torchvision only for `extract_features.py`).

```bash
git clone https://github.com/jcpeterson/cifar-10h.git
mkdir -p data_c10h && cp cifar-10h/data/cifar10h-counts.npy data_c10h/ && unzip cifar-10h/data/cifar10h-raw.zip -d data_c10h/raw
python run_tests.py
python run_label_only.py --c10h data_c10h --out results
python validate_digits.py
# model arm (needs torch; run on your machine or a notebook)
python extract_features.py --limit 500 --out timing.npz     # timing test
python extract_features.py --out feats.npz
python run_model_arm.py --features feats.npz --c10h data_c10h --out results_model
```

## Data and licence
CIFAR-10H is CC BY-NC-SA 4.0 (Peterson, Battleday, Griffiths, Russakovsky, ICCV 2019). It is **not** included here; clone it from its public repository. Tables in `results/` derived from it carry the same licence. They were computed from the raw annotator file with 16 low-attention annotators excluded (this reproduces the published `counts.npy` exactly).
