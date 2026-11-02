# Literature-to-Experiment Bridge

**Project:** Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets
**Stage:** 2 (Literature-to-experiment mapping) | **Log date:** 2026-10-23
**Inputs:** the attached literature review; `gap_matrix.md` (Prompt 1, gaps G1-G5); `research_decisions.md` (Prompt 2, decisions D-001 to D-007, open items O-1 to O-6)

**Tags:** VERIFIED = read in a source page that was opened in this stage (URL listed in Section 8). INFERRED = my reasoning, stated. UNKNOWN = not checked; the check is named.
**Standing rules (D-003):** no invented papers, datasets, links, code runs or metrics. Nothing below was executed. No result is claimed.
**Scope of checking:** only repository pages, model cards, dataset pages and abstracts were read. No original paper was read in full, so every method detail marked INFERRED or UNKNOWN still needs the paper itself.

> **Placeholders not filled.** The prompt left [HARDWARE] and [TIME AVAILABLE] blank. The recommendation in Section 6 assumes **one free-tier notebook GPU or an ordinary laptop CPU, and about 4 part-time weeks**. Both are UNKNOWN. Replace them (O-5, O-6) and Section 6 should be re-checked.

---

## 1. Three methods selected from the review

Selection rule: the method must (a) appear in the review, (b) serve a ranked gap (G3, G4, G1), (c) have verified or plausibly verifiable public code and data, and (d) run without training a large model.

| # | Method | Review ref | Gap served | Why selected |
|---|--------|-----------|-----------|--------------|
| M1 | Confident Learning (label-error detection) | [21] (a retinal-image application; originating paper not in the list) | G4, G3 | Verified, installable code; directly tests the review's "optimal strategy" claim and its uncited claim on systematic errors. |
| M2 | MedSAM (promptable pre-labeler) | [5], also [4], [6] | G1, G5 | Verified weights and code; the review's central AI-assisted method; used here only as a fixed, off-the-shelf pre-labeler. |
| M3 | ActiveAED / uncertainty-based review routing | [71] (cited in text as [23]); budget claim from [22] | G3 | The review's uncertainty-routing claim; code access NOT verified, so only a simplified loop is realistic (see 2.3). |

**Considered and not selected**

| Method | Review ref | Reason excluded |
|--------|-----------|-----------------|
| HybridMS | [11] | Source page found (DOI 10.1038/s41598-025-24990-w) but no code link was seen in the pages read. Code access UNKNOWN. Re-implementing a multi-component clinical framework without code is not an MVE. |
| Octozi | [13] | Commercial-style platform description; no code or data seen. UNKNOWN. |
| LLM cell-typing benchmark | [12] | Needs paid LLM access and 34 datasets; outside the assumed resources. |
| Zoobot / YOLOv5 galaxy models | [15], [16] | Model-vs-label accuracy, not workflow comparison (E12); code and data not checked. UNKNOWN. |

---

## 2. Method-to-paper mapping

### 2.1 M1 - Confident Learning

| Item | Entry | Tag |
|------|-------|-----|
| Original paper | Northcutt, Jiang and Chuang, "Confident Learning: Estimating Uncertainty in Dataset Labels", JAIR 2021. The cleanlab README names it as the paper behind the package. It is **not** in the review's reference list; the review cites a retinal-image application [21] instead. | VERIFIED (named in README); absence from list VERIFIED (E1) |
| Algorithm | Estimates which labels are likely wrong from out-of-sample predicted class probabilities and flags them. Entry point shown in the README: `from cleanlab.filter import find_label_issues`; also `CleanLearning(...).find_label_issues(data, labels)`. | VERIFIED (API names); algorithm internals UNKNOWN until paper is read |
| Dataset(s) | Not tied to one. Candidates in 3 below. | n/a |
| Code access | Official repo `github.com/cleanlab/cleanlab`, installable with pip/conda per README; docs at docs.cleanlab.ai. | VERIFIED (README) |
| Weights | None needed; works with any classifier that gives probabilities. | VERIFIED (README: "works with any classifier") |
| Noise-injection helper | `cleanlab.benchmarking.noise_generation.generate_noise_matrix_from_trace` appears in the README. Whether it supports the model-correlated noise needed for G4 is UNKNOWN. | VERIFIED (exists); fit UNKNOWN |
| Licence | Forks of the README state GNU AGPL v3. The official repo's licence file was not opened. | VERIFIED (via fork READMEs); official file UNKNOWN |
| Evaluation metric | Detection precision and recall of flagged items against known injected errors; downstream accuracy. | PROPOSED (my design) |
| Known limitations | Needs out-of-sample probabilities, so cross-validation is required. The original theory is stated for class-conditional noise; whether it holds for model-correlated noise is the open G4 question. | INFERRED from general knowledge of the method; check in the JAIR paper |
| Compute | Detection step is a post-processing of probabilities; the cost is in producing cross-validated probabilities. Frozen features plus a linear classifier would be cheap. Actual time not measured. | INFERRED; UNKNOWN until smoke test |

### 2.2 M2 - MedSAM

| Item | Entry | Tag |
|------|-------|-----|
| Original paper | Ma et al., "Segment anything in medical images", Nature Communications 2024 (DOI 10.1038/s41467-024-44824-z, cited by the Zenodo weights record). Review lists it as [5] (PMC10803759). | VERIFIED (DOI via Zenodo record); that [5] is this paper is INFERRED from title match |
| Algorithm | SAM fine-tuned for medical images, prompted with a bounding box. Per the model card, prompt encoder frozen, image encoder and mask decoder updated, ViT-Base backbone. | VERIFIED (model card, third-party port) |
| Dataset(s) | Training data is large and public-source per the model card. The count differs: the model card says 1,090,486 image-mask pairs; the review says 1,570,263 (C3). Likely different versions. | VERIFIED (both numbers as printed); reason UNKNOWN. Check in the paper. |
| Code access | Official repo `github.com/bowang-lab/MedSAM`. README shows command-line inference with an `--box` flag, a Colab tutorial and a GUI. | VERIFIED (README text on forks and model card link) |
| Weights access | Zenodo record "Pretrained Model Weights for MedSAM", 375.0 MB, published 2024-02-21. README says to download the checkpoint and place it at `work_dir/MedSAM/medsam_vit_b`. A Hugging Face port exists (`flaviagiammarino/medsam-vit-base`, third-party). | VERIFIED |
| Licence | Model card states code and checkpoints are Apache-2.0, linking the repo LICENSE. Second-hand. | VERIFIED (second-hand); repo file UNKNOWN |
| Evaluation metric | Dice / IoU against a reference mask; for classification-style use, not applicable. | VERIFIED (review Sec. II, eqs. 2-3) |
| Known limitations | Needs a box prompt per target (README interface). The review reports a domain gap for zero-shot SAM [4] and that precise boxes are hard to obtain in practice [7]. Performance on my chosen dataset is UNKNOWN. | VERIFIED (interface); review limitations VERIFIED as printed, sources UNKNOWN |
| Compute | Checkpoint is 375 MB. GPU memory and per-image time not found. A Colab tutorial exists, which suggests a notebook GPU is workable. | VERIFIED (size, tutorial); VRAM and speed UNKNOWN |

### 2.3 M3 - ActiveAED / uncertainty-based routing

| Item | Entry | Tag |
|------|-------|-----|
| Original paper | Weber and Plank, "ActiveAED: A Human in the Loop Improves Annotation Error Detection", Findings of ACL 2023 (ACL Anthology 2023.findings-acl.562; arXiv 2305.20045). This matches review entry [71], not [23]. | VERIFIED (several index pages) |
| Algorithm | An annotation-error detection method that repeatedly queries a human for error corrections inside its prediction loop. The review adds that it uses the Area-under-the-Margin metric; the abstract does not mention it. | VERIFIED (abstract); AUM link UNKNOWN |
| Dataset(s) | Evaluated on eight datasets across five NLP tasks; gains up to six points average precision on seven of them. All are text tasks. | VERIFIED (abstract) |
| Code access | **No code link was found** in the pages read. | UNKNOWN |
| Weights | Not applicable or unknown. | UNKNOWN |
| Evaluation metric | Average precision of error ranking. | VERIFIED (abstract) |
| Known limitations | Text-only evidence. It needs a model retrained in a loop. No image or scientific-dataset evidence appears in the abstract. | VERIFIED (abstract); loop cost INFERRED |
| Compute | Not stated in pages read. | UNKNOWN |
| Realistic implementation | A faithful reproduction is not assured. What is realistic is a generic uncertainty-sampling loop (entropy or margin) as the "uncertainty routing" arm. That tests the review's claim in G3 but is **not** a reproduction of ActiveAED and must not be described as one. | INFERRED |
| Budget claim [22] | "Up to 99%" budget reduction, cited by the review to [22] (conflict text corpora, arXiv 2402.01577). Source not opened. | UNKNOWN |

---

## 3. Datasets that could supply "manual" and reference labels

| Dataset | What was read | Fit | Tag |
|---------|---------------|-----|-----|
| CIFAR-10H | Soft labels for the 10,000-image CIFAR-10 test set; 511,400 human classifications from 2,571 Mechanical Turk workers; about 51 judgments per image (range 47-63); each worker labelled 200 images. The TFDS entry exposes `human_labels`, `annotator_ids` and `soft_label`, download 172.92 MiB. Homepage `github.com/jcpeterson/cifar-10h`. | Smallest working baseline for G1, G3, G4. **Natural images, not a scientific dataset.** Licence not seen. | VERIFIED (counts and fields); licence UNKNOWN |
| LIDC-IDRI | 1,018 CT cases; four radiologists; two-phase annotation without forced consensus; hosted on TCIA; third-party page states CC BY 3.0. | Scientific, multi-annotator, segmentation. Needs DICOM and XML handling (TCIA recommends pylidc); heavier than CIFAR-10H. | VERIFIED (description); licence second-hand; effort INFERRED |
| Galaxy Zoo [14] | Not opened. | Multi-volunteer votes exist in principle. Data access and format UNKNOWN. | UNKNOWN |

Consequence (INFERRED): a first experiment on CIFAR-10H can validate the pipeline and answer the budget and noise questions, but it cannot support a claim about **scientific** datasets. A scientific second domain (LIDC-IDRI, or another dataset I have not verified) is needed before the title's claim can be made.

---

## 4. Comparison of three experimental studies

All three are **simulation studies on existing labels**. None involves human participants (O-3 assumed "existing multi-annotator labels"). A simulated reviewer is a weaker proxy for a human study (as stated in `gap_matrix.md`, G1).

| | **A. Reproduction + extension** | **B. Controlled comparison** | **C. Targeted modification** |
|---|---|---|---|
| Gap | G4 (also feeds G3) | G3, with G1 arms (G5 as noise floor) | G4 + the human-label-variation point in [1] |
| Method(s) | M1 | M1 optional, M2 optional, M3-style loop | M1 with one changed component |
| Smallest working baseline | Take a labelled set, inject random class-conditional label noise at a few rates, get cross-validated probabilities, run `find_label_issues`, report precision and recall of the flagged set against the known injected errors. | On CIFAR-10H test items: fixed classifier on frozen features gives pre-labels. Arms: model-only; random review at budget b; fixed-fraction review; uncertainty-ranked review at budget b. Reviewer = reference label (upper bound). Accuracy vs b with seed intervals. | Same detection pipeline as A, run on CIFAR-10H: compare plain flagging with a version that withholds flags on items whose annotator disagreement (from the 51 judgments) is high. |
| Testable question | Does detection quality hold up when the injected errors are model-correlated rather than random (G4)? | Under a fixed correction budget, does uncertainty routing beat random and fixed-fraction review on final label accuracy (G3)? Does model-assisted labeling beat a single manual annotator (G1)? | Does disagreement-aware flagging cut false flags on ambiguous items without losing real errors? Rationale from the review itself: disagreement is often valid, not noise [1]. |
| Reproduction element | Reproduces M1 detecting random noise before extending. Matching the JAIR paper's numbers is a separate task (UNKNOWN). | None; M3 is not reproduced (no code). | None. |
| Compute | Low (INFERRED): frozen features, linear model, repeated seeds. | Low (INFERRED): same, plus a loop. | Low (INFERRED). |
| Data burden | Any labelled set; CIFAR-10H convenient. | CIFAR-10H (172.92 MiB per TFDS). | CIFAR-10H. |
| Risk | Defining model-correlated noise realistically; a simple definition may just restate the assumption. | Reviewer is perfect, so effects are upper bounds; CIFAR-10H is not scientific. | Ground truth for "real error" on CIFAR-10H is itself contested; needs a clear definition. |
| Evidence required | Paper read; noise definition justified; precision/recall with CI over seeds. | Budget-accuracy curves with paired bootstrap CI over seeds; definition of reference label fixed beforehand. | Same as A plus a stated ambiguity threshold chosen before looking at results. |
| Tests review's claim | Uncited Table III claim on systematic errors (E2, E3). | Conclusion's "optimal strategy" claim (E9d). | Sec. II-A framing from [1]. |

No new architecture is proposed. Study C changes one decision rule inside an existing method and has a stated rationale; it is the only one that modifies anything.

---

## 5. Literature-to-experiment mapping table

| Gap | Review passage / ref | Original paper (to open) | Method | Dataset | Code / weights access | Metric | Smallest baseline | Planned test |
|-----|---------------------|--------------------------|--------|---------|------------------------|--------|-------------------|--------------|
| G3 | Sec. III-C [11]; VII-A [22]; Sec. VIII | [22] arXiv 2402.01577 (not opened); ActiveAED Weber and Plank 2023 [71] | Uncertainty-ranked review (generic loop; not ActiveAED itself) | CIFAR-10H first; second domain UNKNOWN | Generic loop: own code. ActiveAED code: UNKNOWN. | Accuracy vs correction budget, seeds, paired bootstrap CI | Frozen-feature classifier plus random-review arm | Uncertainty vs random vs fixed-fraction at equal budget (Study B) |
| G4 | Table III; Sec. VII-B; Intro [1] | Northcutt et al. JAIR 2021 (not in review list) | Confident Learning via cleanlab | CIFAR-10H or any labelled set | VERIFIED: cleanlab repo, pip | Detection precision and recall; downstream accuracy | `find_label_issues` on random injected noise | Random vs model-correlated noise (Study A); disagreement-aware flagging (Study C) |
| G1 | Sec. III-A, Table II; [9], [10], [11], [13] | Ma et al. Nat Commun 2024 [5] | MedSAM as fixed pre-labeler (scientific segmentation arm) | LIDC-IDRI (needs verification of usable slices and masks) | VERIFIED: repo, Zenodo 375 MB weights | Dice/IoU vs reference; time or query count as cost | Zero-shot box-prompted MedSAM vs a single radiologist's mask vs consensus | Later stage; not in the MVE (needs box prompts and DICOM handling) |
| G1 (classification form) | same | n/a | Single-annotator label vs model vs model + routed review | CIFAR-10H | VERIFIED: data fields | Accuracy vs reference label, CI | Single random annotator label per item vs reference | Study B extra arms |
| G5 | Sec. III-A [8]; III-C [11]; [27] | [27] PubMed 37008654 (not opened) | Annotator-to-annotator spread | CIFAR-10H (per-annotator labels), LIDC-IDRI (four readers) | Data VERIFIED | Pairwise agreement distribution vs model differences | Pairwise annotator accuracy spread | Fold into Study B as noise-floor line |

---

## 6. Recommended minimum viable research experiment

**Recommendation: Study B, with the G1 arms and the G5 noise-floor line included, on CIFAR-10H.**
Status: PROPOSED. Needs your confirmation (D-008).

**Assumed resources (UNKNOWN, replace):** notebook GPU or laptop CPU; about 4 part-time weeks.

**Why B and not A or C (INFERRED):**
- It tests the review's own headline claim (the conclusion's statement on active learning) which currently has no comparison in the body.
- It needs no code that has not been verified; arms are plain loops over a fixed model.
- All required labels exist in CIFAR-10H (reference label, per-annotator labels).
- A and C depend on an unsettled definition of model-correlated noise or of "real error", which is a larger design risk.

**What it can and cannot claim**
- Can claim: under a perfect-reviewer simulation on one natural-image set, how routing rules compare at equal budget, and how a single human annotator compares with a model on the same items.
- Cannot claim: anything about scientific datasets, human reviewers' anchoring behaviour, or time savings. Those need LIDC-IDRI or another verified dataset, and a human study (G2).

**Proposed design (all choices PROPOSED)**

| Element | Choice |
|---------|--------|
| Items | CIFAR-10H test set (10,000 images, 10 classes) |
| Reference label | To decide: original CIFAR-10 label, or the plurality of the human judgments. Fix before running. |
| Manual arm | One annotator's label per item, drawn at random from `human_labels`; repeated over seeds |
| Model arm | Frozen pretrained backbone (to choose) plus linear classifier trained on CIFAR-10 training images; model pre-label per item |
| Assisted arms | Review budget b in a small grid (for example 5, 10, 20, 40 percent): random, fixed-fraction, uncertainty (entropy or margin) |
| Reviewer | Reference label (upper bound). Optional second reviewer: a randomly drawn annotator label (imperfect). |
| Outcome | Accuracy against the reference; query count as cost |
| Uncertainty | 10 or more seeds; paired bootstrap CI on differences (seed count to confirm after a smoke test) |
| Noise floor | Annotator-to-annotator accuracy spread, plotted beside the arm differences (G5) |
| Stop rule | Report all arms, including those where uncertainty routing does not win |

**Phased plan (assumed 4 weeks)**

| Week | Work | Output |
|------|------|--------|
| 1 | Complete Section 7 checks; load CIFAR-10H; smoke test on 500 items to measure time | Verified-inputs note; timing |
| 2 | Frozen features and baseline classifier; model-only and manual arms | Baseline numbers (to be produced, none exist yet) |
| 3 | Routing arms and budget grid; seeds; CIs | Budget-accuracy curves |
| 4 | Noise-floor line; limitations; write-up skeleton | Results table and caveats |

If timing in week 1 shows the grid does not fit, cut the budget grid or seed count rather than add a model.

**Stretch (only after B is done):** Study A on the same features, then a scientific second domain.

---

## 7. What you must personally verify before coding

| # | Check | Why | Resolves |
|---|-------|-----|----------|
| V1 | Open the cleanlab repo and read the licence file; note that the AGPL text seen was in fork READMEs. | Decides whether you can publish code that links it and under what terms. | M1 licence |
| V2 | Open the MedSAM repo licence, and confirm the Zenodo weights file against the repo's download link. | The Apache-2.0 statement was second-hand. | M2 licence, weights |
| V3 | Read the MedSAM paper's training-data count and compare with 1,570,263 (review) and 1,090,486 (model card). | The review's C3 figure conflicts with a third-party card. | C3 |
| V4 | Read the JAIR Confident Learning paper: noise assumptions, and what "out-of-sample probabilities" requires. | Needed before extending to model-correlated noise. | M1 limitations |
| V5 | Open the ActiveAED paper and PDF; search for a code link and for any use of AUM. | No code link was found; the review's AUM claim is unconfirmed. | M3 code, E1b |
| V6 | Open [22] (arXiv 2402.01577): is "up to 99%" in that paper, and under what setting? | Claim C14 is the only support for the budget claim. | C14 |
| V7 | Check the CIFAR-10H repo licence and its terms of use. | Not seen in any page read. | Dataset licence |
| V8 | Decide the reference label (CIFAR-10 label or human plurality) and write it down before any run. | Choosing after seeing results would bias the outcome. | Study B design |
| V9 | Confirm your hardware and your deadline; replace the assumptions. | Section 6 depends on them. | O-5, O-6 |
| V10 | Ask your supervisor whether a simulation study on a non-scientific dataset is acceptable as a first stage, and whether the final paper must include a scientific dataset. | The title says "scientific datasets"; the MVE alone does not meet it. | O-2, O-4 |
| V11 | If a scientific second domain is wanted: open the LIDC-IDRI collection page, check access terms and the DICOM annotation format, and test loading one case. | Effort and licence only second-hand. | G1 segmentation arm |
| V12 | Pin package versions and record the random seeds from the first run. | Reproducibility rule (D-003). | All |
| V13 | Confirm authorship and reuse of the source review (D-004) and the rebuilt reference list (D-005). | Still open from Stage 0. | D-004, D-005 |

---

## 8. Sources opened in this stage

| What | URL | Used for |
|------|-----|----------|
| MedSAM repo README (forks of the official repo) | github.com/Alighieri1231/MedSAM; github.com/Wzhjerry/MedSAM | Interface, install steps, Colab tutorial |
| MedSAM model card (third-party port) | huggingface.co/flaviagiammarino/medsam-vit-base | Backbone, training count 1,090,486, Apache-2.0 statement |
| MedSAM weights record | zenodo.org/records/10689643 | 375.0 MB, DOI of paper, repo URL |
| cleanlab README | github.com/cleanlab/cleanlab (README) and forks | API names, paper reference, AGPL text, noise helper |
| ActiveAED abstract | aclanthology.org/2023.findings-acl.562; arxiv.org/pdf/2305.20045 | Authors, venue, datasets, claim |
| HybridMS article | ncbi.nlm.nih.gov/pmc/articles/PMC12639002/ | Existence, DOI; no code link seen |
| CIFAR-10H | github.com/jcpeterson/cifar-10h; tensorflow.org/datasets/catalog/cifar10_h; paperswithcode.com/dataset/cifar-10h | Counts, fields |
| LIDC-IDRI | wiki.cancerimagingarchive.net/x/0IwvB | Description, four radiologists |

---

## 9. Decision log additions (continuing `research_decisions.md`)

| ID | Decision | Status | Next action |
|----|----------|--------|-------------|
| D-008 | Adopt Study B (budgeted routing, with G1 arms and G5 noise floor) as the MVE | PROPOSED | Researcher confirms; V8-V10 |
| D-009 | Treat all first-stage work as simulation on existing labels; no claim about human behaviour | PROPOSED | Confirm with supervisor (V10) |
| D-010 | Do not describe any generic uncertainty loop as a reproduction of ActiveAED | PROPOSED | Revisit if V5 finds code |
| D-011 | Fix the reference-label definition before the first run | PROPOSED | V8 |
| D-012 | Treat the Confident Learning source as the JAIR paper, not review ref [21] | PROPOSED | Add to rebuilt list (D-005) after V4 |

**Next actions:** N1 confirm D-004 to D-012; N2 run Section 7 checks; N3 smoke test (Stage 3 feasibility); N4 draft research question and hypotheses (Stage 4) from the confirmed experiment.

---

*Bridge: original papers (Sec. 2) -> selected method (Sec. 1) -> executable baseline (Sec. 4, 6) -> planned test (Sec. 5, 6). Log entries are appended as decisions are made.*
