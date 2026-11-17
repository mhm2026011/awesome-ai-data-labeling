# Phase III Addendum - Model Arm Run (fallback features) and Colab Notebook

**Project:** Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets
**Log date:** 2026-11-17 | **Supersedes the status rows** of `phase3_coding_and_baseline_validation.md` (Sections 0 and 7 said the model arm was not run; that is no longer true, with the caveat below).
**Implements:** `phase2_experiment_plan.md` (D-018 to D-023). Evidence tags as before: VERIFIED (run here, output saved), INFERRED (reasoning stated), UNKNOWN (check named).

> **One deviation changes how to read everything below.** The pre-specified backbone (frozen ResNet-18) could not be run in the authoring workspace: torch and the pretrained weights are unreachable here. The model arm was therefore run with the plan's documented fallback, **hand-built gradient and colour features plus logistic regression** (372 dimensions). That classifier reaches only **0.6002** accuracy, far below a single human annotator. Results are real but describe a **weak-model regime**. The pre-specified ResNet-18 run is packaged as a Google Colab notebook and has **not** been run.

---

## 0. Status

| Part | Status | Evidence |
|------|--------|----------|
| Unit tests | **19 of 19 pass** (15 earlier + 4 for the safe loader and fallback features) | `results/test_log.txt` |
| CIFAR-10 images | **Obtained** from a third-party GitHub copy and validated (Section 2) | Section 2 |
| Model arm, fallback features, 10 seeds, both reference rules | **Run** | `results_model_fallback/` |
| Pre-specified H2 test | **Answered for the fallback model** (Section 5) | `results_primary_original_label.csv` |
| Model arm with ResNet-18 (pre-specified backbone) | **Not run.** Notebook ready; its torch cells were never executed | `Study_B_Colab.ipynb` |
| Colab notebook | Syntax-checked; all non-torch cells **executed end to end** in a fresh folder with identical output to the direct run | `results/notebook_dry_run_log.txt` |
| Scientific second dataset | Not done (V10, V11) | - |
| Manuscript | Not done | - |

---

## 1. What was run

| Item | Value | Tag |
|------|-------|-----|
| Features | Gradient-orientation histograms (4x4 cells of 8x8 pixels, 9 bins, 2x2 block normalisation: 324 dims) plus 4x4 colour means (48 dims) = 372 dims, from 50,000 train and 10,000 test images | VERIFIED |
| Classifier | Standardised multinomial logistic regression, 300 iterations | VERIFIED |
| Hyperparameter choice | C chosen from {0.01, 0.1, 1.0} on a held-out 20% of the **train** set: validation accuracies 0.5841, 0.5907, 0.5895; chose **C = 0.1** | VERIFIED |
| Seeds | 10; each trains on a random 80% of the train set, and draws its own random-arm order and single-annotator labels | VERIFIED |
| Test set use | Test labels and features used only for evaluation | VERIFIED (code path R5 in the Phase III report) |
| Bootstrap | 2,000 paired resamples over the 10,000 items | VERIFIED |
| Timing (2 CPU cores, no GPU) | Features for 60,000 images 6 s; choosing C 14 s; training 10 seeds 41 s. Bootstrap time not measured. | VERIFIED |
| Convergence | No warning lines in the run log | VERIFIED |
| Model-only accuracy | **0.6002** (seed range 0.5966 to 0.6022); calibration error 0.0106 (seed 0) | VERIFIED |

---

## 2. CIFAR-10 images: provenance and validation

The official download hosts were unreachable. The images came from a **third-party GitHub copy** of the Python-format batches (`0Colin/cifar-10-batches-py`, commit 48ece5ce, 17 Oct 2019). It is not the official source, so it was validated before use.

| Check | Result | Tag |
|-------|--------|-----|
| Loaded without executing pickle code (allowlist loader; a test confirms a malicious pickle is blocked) | Pass | VERIFIED |
| Shapes and class balance | 50,000 train (5,000 per class), 10,000 test (1,000 per class) | VERIFIED |
| **Gate G-8:** test labels equal CIFAR-10H `true_label` | **0 mismatches of 10,000** | VERIFIED |
| Test filenames equal CIFAR-10H `image_filename` | **10,000 of 10,000** | VERIFIED |
| Train images match the official release | **Cannot be checked here** (no independent reference). The test split matching is strong evidence for the test batch only. | UNKNOWN |
| Official checksum | Not compared | UNKNOWN |

**What to do:** the Colab notebook downloads CIFAR-10 from the official source through torchvision, so a ResNet-18 run removes this dependency. Cite the original CIFAR-10 report in the paper (standard citation: Krizhevsky, 2009, "Learning Multiple Layers of Features from Tiny Images"; verify the details yourself). Do not redistribute the images; they are not in the zip.

---

## 3. Deviations and decisions

| ID | Item | Status |
|----|------|--------|
| D-028 | Fallback features instead of the pre-specified ResNet-18 backbone, because torch and weights were unreachable. The plan (Section 4) and the feasibility file (Section 7) both list a backbone fallback. Hypotheses, arms, budgets, reference rule and primary contrast are **unchanged**. | PROPOSED; forced by access |
| D-029 | Use the third-party CIFAR-10 copy for the fallback run only; the ResNet run should use the official download | PROPOSED |
| D-030 | Every result is labelled with its backbone. The fallback result is not presented as the study result if the ResNet run is done. | PROPOSED |
| D-031 | The Colab notebook is the reproducibility artefact for the ResNet run. Its torch cells are untested. | PROPOSED |

---

## 4. Validation gates on the real run

| Gate | Check | Result |
|------|-------|--------|
| G-2 | Perfect reviewer, oracle arm equals 1 - max(E - k, 0)/N, averaged over seeds | **Holds at all four budgets** (0.6502, 0.7002, 0.8002, 0.9995 expected and observed) |
| G-4 | Raw file rebuilds `counts.npy` exactly | Pass (the runner asserts it before computing anything) |
| G-8 | Features' test labels equal CIFAR-10H | Pass (runner asserts; also shown in Section 2) |
| G-6 | Determinism | Direct run and the notebook dry run gave byte-identical result files |

---

## 5. Results (primary reference: original CIFAR-10 label)

Reference accuracies: model only **0.6002**; one random annotator, no model **0.9514** (seed range 0.9490 to 0.9527).

### 5.1 Single-annotator reviewer (primary)

| Budget | Arm | Accuracy | Seed range | Gain over random (paired 95% interval) |
|---|---|---|---|---|
| 0.05 | random | 0.6182 | 0.6142 to 0.6226 | - |
| 0.05 | **entropy** | 0.6334 | 0.6300 to 0.6355 | +0.0152 (+0.0123 to +0.0183) |
| 0.05 | margin | 0.6319 | 0.6280 to 0.6341 | +0.0137 (+0.0118 to +0.0158) |
| 0.05 | least_confidence | 0.6341 | 0.6319 to 0.6362 | +0.0159 (+0.0133 to +0.0188) |
| 0.05 | oracle | 0.6467 | 0.6428 to 0.6494 | +0.0285 (+0.0269 to +0.0301) |
| 0.10 | random | 0.6351 | 0.6304 to 0.6376 | - |
| 0.10 | **entropy** | 0.6623 | 0.6592 to 0.6651 | +0.0272 (+0.0231 to +0.0313) |
| 0.10 | margin | 0.6622 | 0.6593 to 0.6660 | +0.0272 (+0.0243 to +0.0302) |
| 0.10 | least_confidence | 0.6651 | 0.6621 to 0.6686 | +0.0300 (+0.0263 to +0.0338) |
| 0.10 | oracle | 0.6933 | 0.6899 to 0.6957 | +0.0583 (+0.0559 to +0.0606) |
| 0.20 | random | 0.6710 | 0.6685 to 0.6755 | - |
| 0.20 | **entropy** | 0.7187 | 0.7153 to 0.7212 | +0.0477 (+0.0424 to +0.0530) |
| 0.20 | margin | 0.7202 | 0.7171 to 0.7226 | +0.0492 (+0.0448 to +0.0536) |
| 0.20 | least_confidence | 0.7233 | 0.7200 to 0.7257 | +0.0523 (+0.0470 to +0.0573) |
| 0.20 | oracle | 0.7862 | 0.7838 to 0.7891 | +0.1152 (+0.1118 to +0.1189) |
| 0.40 | random | 0.7402 | 0.7370 to 0.7440 | - |
| 0.40 | **entropy** | 0.8146 | 0.8129 to 0.8160 | +0.0743 (+0.0685 to +0.0801) |
| 0.40 | margin | 0.8211 | 0.8201 to 0.8222 | +0.0809 (+0.0754 to +0.0863) |
| 0.40 | least_confidence | 0.8233 | 0.8220 to 0.8251 | +0.0831 (+0.0774 to +0.0884) |
| 0.40 | oracle | 0.9719 | 0.9693 to 0.9731 | +0.2316 (+0.2262 to +0.2373) |

### 5.2 Perfect reviewer (upper bound)

| Budget | Arm | Accuracy | Seed range | Gain over random (paired 95% interval) |
|---|---|---|---|---|
| 0.05 | random | 0.6208 | 0.6162 to 0.6250 | - |
| 0.05 | **entropy** | 0.6371 | 0.6336 to 0.6389 | +0.0163 (+0.0132 to +0.0195) |
| 0.05 | margin | 0.6351 | 0.6314 to 0.6369 | +0.0143 (+0.0123 to +0.0164) |
| 0.05 | least_confidence | 0.6380 | 0.6361 to 0.6398 | +0.0173 (+0.0145 to +0.0203) |
| 0.05 | oracle | 0.6502 | 0.6466 to 0.6522 | +0.0295 (+0.0278 to +0.0311) |
| 0.10 | random | 0.6402 | 0.6355 to 0.6418 | - |
| 0.10 | **entropy** | 0.6700 | 0.6682 to 0.6721 | +0.0298 (+0.0255 to +0.0341) |
| 0.10 | margin | 0.6685 | 0.6665 to 0.6710 | +0.0284 (+0.0254 to +0.0315) |
| 0.10 | least_confidence | 0.6725 | 0.6700 to 0.6751 | +0.0323 (+0.0283 to +0.0363) |
| 0.10 | oracle | 0.7002 | 0.6966 to 0.7022 | +0.0600 (+0.0576 to +0.0626) |
| 0.20 | random | 0.6809 | 0.6790 to 0.6846 | - |
| 0.20 | **entropy** | 0.7330 | 0.7308 to 0.7351 | +0.0521 (+0.0464 to +0.0577) |
| 0.20 | margin | 0.7333 | 0.7300 to 0.7343 | +0.0524 (+0.0478 to +0.0571) |
| 0.20 | least_confidence | 0.7373 | 0.7342 to 0.7391 | +0.0564 (+0.0508 to +0.0618) |
| 0.20 | oracle | 0.8002 | 0.7966 to 0.8022 | +0.1193 (+0.1159 to +0.1233) |
| 0.40 | random | 0.7594 | 0.7553 to 0.7634 | - |
| 0.40 | **entropy** | 0.8412 | 0.8385 to 0.8433 | +0.0818 (+0.0754 to +0.0882) |
| 0.40 | margin | 0.8464 | 0.8447 to 0.8484 | +0.0871 (+0.0814 to +0.0927) |
| 0.40 | least_confidence | 0.8490 | 0.8473 to 0.8507 | +0.0897 (+0.0838 to +0.0956) |
| 0.40 | oracle | 0.9995 | 0.9966 to 1.0000 | +0.2401 (+0.2343 to +0.2460) |

### 5.3 Reference-rule sensitivity (human plurality as reference)

Model only 0.5990; one annotator 0.9533. Primary contrast under this reference: **+0.0480** (+0.0428 to +0.0535), against +0.0477 (+0.0424 to +0.0530) under the primary reference. Full table: `results_sensitivity_human_plurality.csv`. The choice of reference rule does not change any conclusion in Section 6 (INFERRED from the two tables).

Plots (from the notebook flow): `accuracy_vs_budget.png`, `entropy_minus_random.png`.

---

## 6. Outcome of each pre-specified hypothesis (fallback model only)

| ID | Outcome | Basis |
|----|---------|-------|
| H1 (perfect reviewer: uncertainty beats random at every budget) | **Holds**: all 12 perfect-reviewer interval lower bounds for entropy, margin and least confidence are above zero. Expected, and a pipeline check, not a finding. | VERIFIED (CSV) |
| **H2 (primary: single reviewer, entropy minus random, b = 0.20)** | **Supported.** Difference **+0.0477**, 95% paired bootstrap interval **+0.0424 to +0.0530**; the interval excludes zero. | VERIFIED |
| H3 (single-annotator review falls below model-only at some budget) | **Not observed.** Every single-reviewer arm at every budget is above model-only (smallest interval lower bound +0.0170). This is expected here and **not informative**: the model is at 0.6002 and one annotator at 0.9514, so reviewed items almost always move toward the truth. H3 can only be tested with a model that is closer to or better than a single annotator. | VERIFIED (CSV); reasoning INFERRED |
| H4 (model-versus-annotator gap larger than annotator spread) | The gap is 0.3511 accuracy (annotator minus model); the between-annotator SD is 0.0287. The gap is about 12 times that SD. This follows from the weak features, so it says nothing about modern models. | VERIFIED numbers; reading INFERRED |

**Descriptive observations (INFERRED, not tested):**
- At b = 0.20 an imperfect single reviewer costs 0.0143 accuracy against a perfect one for the same entropy routing (0.7187 against 0.7330), and the routing gain over random is 0.0477 against 0.0521. Whether that difference between 0.0477 and 0.0521 is more than noise was not tested.
- The three uncertainty scores give similar gains at b = 0.20 (0.0477 entropy, 0.0492 margin, 0.0523 least confidence). Entropy was fixed as primary in advance and happens to be the lowest of the three here; differences between scores were not tested.
- Random review with a single annotator at b = 0.20 gains 0.0708 over model-only, and entropy routing gains 0.1185, i.e. about 1.7 times as much.

---

## 7. What this supports and what it does not

| Supports | Does not support |
|----------|------------------|
| With a weak feature-based classifier on CIFAR-10H, sending the most uncertain images to a single crowd annotator beats sending random images, at each budget tested | Any statement about a strong modern classifier (the regime that matters for AI-assisted labeling) |
| The simulation pipeline, gates and reference-rule sensitivity work on real data | Any claim about **scientific** datasets (title), time savings, fatigue, or anchoring |
| A direct, reproducible baseline to compare the ResNet-18 run against | Novelty (searches S1 to S5 are still not run) |

**Threats specific to this run:** weak model (accuracy 0.6002); third-party copy of the training images (Section 2); one dataset; simulated reviewer that never sees the pre-label; logistic regression capped at 300 iterations (no warnings seen).

---

## 8. What remains

1. **Run `Study_B_Colab.ipynb` on a Colab GPU** (Runtime > Run all). It follows the pre-specified plan with ResNet-18 features. Its first torch cell is a 500-image timing test. If torch or the weights fail, Section 6 of the notebook provides the CPU fallback, which reproduces this addendum's setting.
2. Send back `outputs.zip` from the notebook. The H2 row there becomes the headline result; this addendum's fallback result becomes a secondary baseline (D-030).
3. Interpretation rules are unchanged: H2 is judged only on the single / entropy / random / b = 0.20 row; a null or negative result is reported as the result.
4. Still open: backbone licence (torchvision ResNet-18 weights, not read), scientific second dataset (V10, V11), searches S1 to S5 (D-015), authorship of the source review (D-004), supervisor confirmation of D-018 to D-031.

---

## 9. Files

| File | Purpose |
|------|---------|
| `experiments/study_b_review_routing/Study_B_Colab.ipynb` | Google Colab notebook (35 cells; embeds all code, runs the full ResNet-18 plan) |
| `.../results_model_fallback/` | Model-arm outputs: two result CSVs, `model_summary.json`, run log, plots |
| `.../load_cifar10_safe.py`, `features_fallback.py`, `run_fallback.py`, `tests/test_extra.py` | New code for this run |
| `.../results/test_log.txt`, `notebook_dry_run_log.txt` | Test and notebook evidence |

---

*Bridge: ... validated code and label-only baseline (Phase III) -> **model-arm run with fallback features and Colab notebook (this file)** -> ResNet-18 run (yours) -> results and manuscript (Phase IV).*
