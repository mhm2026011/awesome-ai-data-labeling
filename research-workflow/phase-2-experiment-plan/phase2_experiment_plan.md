# Phase II - Experiment Plan (pre-specified protocol)

**Project:** Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets
**Phase:** II (Experiment plan) | **Written:** 2026-10-28, **before** any accuracy was computed | **Due:** 30 Oct 2026
**Inputs:** `gap_matrix.md`, `research_decisions.md`, `literature_to_experiment_bridge.md` (D-008 to D-012), `feasibility_novelty_matrix.md` (D-013 to D-017)

**Tags:** VERIFIED = read in a file or page opened in this project. INFERRED = my reasoning, stated. UNKNOWN = not checked; the check is named. PROPOSED = a design choice that needs your confirmation.
**Standing rules (D-003):** no invented papers, links, runs or metrics.

> **What I looked at before writing this plan.** Only the file structure of CIFAR-10H: the file names, the 13 column names, the row count, and that `cifar10h-counts.npy` has 10,000 rows with 47 to 63 judgments each. I computed no accuracy and no agreement. Every rule below that could favour an outcome (reference label, primary contrast, budget) is fixed here first.

---

## 1. Verified inputs that shape the plan

| Item | Finding | Tag |
|------|---------|-----|
| CIFAR-10H licence | **Resolved:** `LICENSE.txt` in the repository states Creative Commons BY-NC-SA 4.0 (non-commercial; credit; indicate changes; share-alike). Cloned commit 389f22d (23 Mar 2026). Closes V7 and D-016. | VERIFIED |
| CIFAR-10H files | `cifar10h-counts.npy` and `cifar10h-probs.npy` (10,000 x 10), `cifar10h-raw.zip` -> `cifar10h-raw.csv`: 539,910 rows x 13 columns (annotator_id, trial_index, is_attn_check, true_category, chosen_category, true_label, chosen_label, correct_guess, cifar10_test_test_idx, image_filename, subcategory, reaction_time, time_elapsed); 2,571 annotator IDs; no missing values. | VERIFIED |
| Row count vs documented count | The dataset page states 511,400 classifications; the raw file has 539,910 rows, so it must include attention-check trials and possibly excluded workers. The code must reproduce `counts.npy` from the raw file as a validation check (Section 8). | VERIFIED (numbers); explanation INFERRED |
| CIFAR-10 images | **Not reachable from this workspace** (host returned a proxy refusal). Needed for the model arm. | VERIFIED (refusal) |
| Deep-learning packages | **torch and torchvision cannot be installed here** (pip found no matching distribution). scikit-learn 1.9.1, pandas, scipy, numpy are present. Hardware here: 2 CPU cores, 7 GB RAM, no GPU. | VERIFIED |
| Consequence | The label-only parts (manual arm, noise floor, reference-rule comparison) and the routing code can be run and validated here. The **model arm on real CIFAR-10 images must be run on your machine or a notebook**. | INFERRED |

---

## 2. Research question and hypotheses

**Question (from D-013, tightened):** On the 10,000 CIFAR-10 test images, when a classifier pre-labels every image and a human then corrects a fixed fraction b of them, how much does it matter **which** images are sent to the human, and does the answer change when the human is a single imperfect annotator instead of a perfect reviewer?

**Why the reviewer type matters (INFERRED).** With a perfect reviewer, the gain from routing is just how many of the model's errors land in the reviewed set. Any reasonable uncertainty score will beat random there, so a positive result would confirm what is expected and not be a finding. With a single annotator, the images the model finds hardest are also the ones where people disagree (CIFAR-10H's own purpose), so the benefit of routing may shrink or even reverse. That is the open part.

| ID | Hypothesis | Role | What would count against it |
|----|-----------|------|-----------------------------|
| H1 | Perfect reviewer: entropy-ranked review gives higher final accuracy than random review at every budget b. | Pipeline check, upper bound. Not claimed as a finding. | Any budget where the paired CI includes zero or is negative: treat as a bug until traced. |
| **H2 (primary)** | Single-annotator reviewer: entropy-ranked review at b = 0.20 gives higher final accuracy than random review at b = 0.20. | Primary test | Paired 95% CI of the difference includes zero or is below zero. A null or negative result is a reportable outcome. |
| H3 | Single-annotator review of the most uncertain items can **lower** accuracy below model-only at some budget (humans worse than the model on the hardest items). | Secondary, exploratory | Not observed at any budget. |
| H4 | The accuracy difference between the classifier and a single random annotator is larger than the annotator-to-annotator spread. | Secondary (G5 noise floor) | Difference lies inside the spread. |

H2 is the only confirmatory test. All others are descriptive and reported with intervals, no p-value hunting.

---

## 3. Definitions (fixed)

- **Items:** the 10,000 CIFAR-10 test images, indexed by `cifar10_test_test_idx`.
- **Reference label r_i (primary):** the original CIFAR-10 test label (`true_label` in the raw file). *Reason:* it is independent of the annotators being evaluated. **Sensitivity analysis:** the human plurality label (argmax of `counts`; ties broken by the lower class index, reported as a count of ties). Both are fixed now. Which is better is contested (the "Pervasive Label Errors" paper is only known to me by title, so I make no claim about CIFAR-10 test errors).
- **Pre-label:** the classifier's argmax class, with probability vector p_i.
- **Budget b:** fraction of items sent to review, k = round(b x 10,000). Grid: 0.05, 0.10, 0.20, 0.40. **Primary budget: 0.20.**
- **Reviewer types:**
  - *Perfect:* returns r_i.
  - *Single annotator (primary):* returns one label drawn uniformly at random from the item's raw judgments (attention-check trials removed).
- **Final label:** the reviewer's label for reviewed items, the pre-label for the rest.
- **Outcome:** accuracy of final labels against r_i.

### Arms

| Arm | Selection rule for the k reviewed items | Notes |
|-----|-----------------------------------------|-------|
| none | nobody reviewed | Model-only baseline |
| random | k items uniformly at random | The control |
| entropy | k items with highest predictive entropy | **Primary uncertainty score** |
| margin | k items with smallest gap between top two probabilities | Secondary |
| least-confidence | k items with lowest top probability | Secondary |
| oracle | the model's actual errors first, then random | Ceiling for the perfect reviewer; not achievable |
| manual | no model; one annotator's label per item | G1 arm |

**Change from Stage 2 (D-018, PROPOSED):** "fixed-fraction review" is dropped. In Stage 2 it was never defined apart from random, and any fixed-fraction rule that ignores the model has the same expected accuracy as random review. Keeping it would add an arm that cannot differ. If you meant a different rule (for example a confidence threshold), say so and I will add it.

**Change from Stage 2 (D-019, PROPOSED):** the single-annotator reviewer moves from optional to primary, for the reason in Section 2.

---

## 4. Model arm

| Element | Choice | Tag |
|---------|--------|-----|
| Features | Frozen pretrained image backbone, one forward pass over 50,000 train and 10,000 test images, cached | PROPOSED |
| Candidate backbone | A small ImageNet-pretrained ResNet from torchvision, images resized to the backbone's input size | PROPOSED; **weights licence and download are UNKNOWN** (not opened; check before use) |
| Classifier | Multinomial logistic regression on the cached features, trained on the CIFAR-10 training set only | PROPOSED |
| Calibration | None in the primary analysis. Report expected calibration error as a descriptive number. | PROPOSED |
| Leakage rule | The test set is never used for training, model selection, or choosing hyperparameters. Hyperparameters are chosen on a held-out 10,000 split of the training set. | PROPOSED |
| Seeds | 10 seeds. Each seed: classifier trained on a random 80% of the training set; random-arm draws; single-annotator draws. | PROPOSED |
| Backbone fallback | If the torchvision weights cannot be used, train a small CNN from scratch on CIFAR-10 (more compute, lower reproducibility) or use another openly licensed backbone after reading its licence | INFERRED |

---

## 5. Statistics

- **Primary estimate:** mean difference in final accuracy, entropy minus random, single-annotator reviewer, b = 0.20, averaged over seeds.
- **Uncertainty:** paired bootstrap over test items (2,000 resamples), with arms evaluated on the same resampled items; 95% percentile interval. Seeds are reported separately as a spread (min, median, max), because item resampling and seed variation are different sources of noise.
- **No multiplicity correction** on descriptive results; the single confirmatory test is H2.
- **Noise floor (H4):** per-annotator accuracy against r_i, over the items each annotator saw (about 200 each per the dataset page), reported as mean, SD and 5th/95th percentiles; and the spread of single-annotator accuracy across 1,000 random one-label-per-item draws.
- **Stop rule:** all arms and budgets are reported, including losses. No arm is dropped after seeing results. Any change to this plan after the first model-arm run is logged as a deviation with the reason.

---

## 6. What this experiment can and cannot support

| Can support | Cannot support |
|-------------|----------------|
| How routing rules compare at equal budget on one natural-image set, with a perfect and with a single-annotator reviewer | Any claim about **scientific** datasets (title) - needs a second domain (V10) |
| Whether a model beats a single crowd annotator on these items, relative to annotator spread | Time savings, fatigue, or anchoring: the reviewer is simulated and never sees the model's label |
| A null result is informative | That uncertainty routing works for text or segmentation |

**Threats to validity (INFERRED):**
1. The simulated reviewer does not see the pre-label, so it cannot be anchored by it (G2 is untouched). Results are optimistic for AI-assisted review.
2. CIFAR-10H annotators were crowd workers on 32x32 images, not domain experts.
3. A reviewer's drawn label is independent of earlier draws; a real person has habits.
4. The reference label may itself be wrong for some images; the sensitivity analysis shows how much it matters.
5. One classifier family. A different backbone could change the ranking quality.
6. Feature extraction and the 80% training subsample capture only part of classifier variance.

---

## 7. Resources, time and what must run where

| Task | Where | Time (INFERRED) |
|------|-------|-----------------|
| Label-only analysis (manual arm, noise floor, reference sensitivity), routing logic tests, pipeline check on a small bundled dataset | **This workspace (done in Phase III)** | Minutes |
| CIFAR-10 download, feature extraction, model arm, 10 seeds, bootstrap | **Your machine or a notebook** | Feature extraction dominates; **unmeasured**. Time one 500-image batch first. |
| Write-up | You | 1 to 2 days |

Deadline reality (INFERRED): Phase II and III are due 30 Oct. The model arm needs one notebook session; if you cannot run it by then, hand in the plan, the validated code, the label-only baseline and an explicit statement that the model arm is pending.

---

## 8. Phase III validation gates (pass before any model-arm number is trusted)

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G-1 | Routing functions on hand-made probabilities with known answers | All unit tests pass |
| G-2 | Perfect-reviewer accuracy with `oracle` arm | Equals the closed-form value min(1, base acc + k/N) |
| G-3 | Perfect reviewer, b = 1.0 | Accuracy = 1.0 for every arm |
| G-4 | Raw file -> counts | Reconstructed counts equal `cifar10h-counts.npy` exactly after attention-check and exclusion rules; if not, stop and trace |
| G-5 | Bootstrap | On a constructed pair with a known difference the interval covers it; with identical arms it covers zero |
| G-6 | Determinism | Same seed gives identical output |
| G-7 | End-to-end pipeline on a real classifier with a bundled dataset (no download) | Runs, results consistent with G-2/G-3, clearly labelled as **not a Study B result** |

---

## 9. Decision log additions

| ID | Decision | Status | Next action |
|----|----------|--------|-------------|
| D-018 | Drop the undefined "fixed-fraction" arm | PROPOSED | You confirm or define it |
| D-019 | Single-annotator reviewer becomes the primary reviewer | PROPOSED | You confirm |
| D-020 | Reference label = original CIFAR-10 label; human plurality as sensitivity | PROPOSED | You confirm **before** the model arm runs (closes V8) |
| D-021 | Primary contrast: entropy vs random, single-annotator reviewer, b = 0.20; H2 only confirmatory test | PROPOSED | You confirm |
| D-022 | CIFAR-10H licence CC BY-NC-SA 4.0: results and code that adapt it must say what changed and carry the same licence; non-commercial use only | VERIFIED (licence text) | Check your course or venue allows this |
| D-023 | Model arm to run outside this workspace; label-only parts and code validated here | PROPOSED | You run it; send me the output files |

**Still open from earlier stages:** backbone and its licence (V-new), the scientific second dataset (V10, V11), hardware and exact deadline (O-5, O-6), authorship of the source review (D-004).

---

*Bridge: original papers -> selected method -> executable baseline -> planned test -> novelty and feasibility gate -> **pre-specified protocol (this file)** -> validated code (Phase III).*
