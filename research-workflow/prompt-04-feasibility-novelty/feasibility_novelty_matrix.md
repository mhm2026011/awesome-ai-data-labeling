# Feasibility, Novelty and Resource-Access Plan

**Project:** Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets
**Stage:** 3 (Feasibility and novelty verification) | **Log date:** 2026-10-23
**Inputs:** the literature review; `gap_matrix.md` (Prompt 1); `research_decisions.md` (Prompt 2); `literature_to_experiment_bridge.md` (Prompt 3, decisions D-008 to D-012)

**Tags:** VERIFIED = read in a page opened in this stage (Section 9 lists them). INFERRED = my reasoning, stated. UNKNOWN = not checked; the check is named.
**Standing rules (D-003):** no invented papers, DOIs or URLs; no code run; no result claimed. Neighbouring works below appear only if a page or abstract was read. Titles seen only in a README are marked as such.
**Novelty:** no novelty is claimed. Section 4 says what a claim would need.

> **Placeholders not filled.** The prompt left [IDEA], [HARDWARE] and [WEEKS] blank. I used the Stage 2 recommendation (Study B on CIFAR-10H) as [IDEA], and the Stage 2 assumptions for the rest: **one free-tier notebook GPU or a laptop CPU, 4 part-time weeks**. Hardware and weeks are UNKNOWN (O-5, O-6). Replace them and Section 6 should be re-estimated.

---

## 1. Candidate study as stated (from D-008, PROPOSED)

Study B: budgeted review-routing comparison on CIFAR-10H, with single-annotator and model-only arms (G1) and an annotator noise-floor line (G5). Arms: model-only; random review; fixed-fraction review; uncertainty-ranked review. Reviewer = reference label. Outcome = accuracy against the reference at each budget, with seed intervals.

**Narrowed experimental question (PROPOSED, D-013):**
> On the 10,000 CIFAR-10 test images, with a frozen-feature classifier supplying pre-labels, and a perfect reviewer correcting a fixed fraction b of items, does reviewing the b most uncertain items (entropy or margin) give higher final label accuracy than reviewing b random items? How large is that difference compared with the accuracy spread between individual human annotators?

What was removed from the Stage 2 version: the MedSAM arm, the LIDC-IDRI arm, the Confident Learning arm and the imperfect-reviewer arm. They move to stretch work.

---

## 2. Search plan: how to check novelty

**Status of the searches.** Section 3 lists searches I ran; they returned only a few pages I could read, so they are a start, not a literature search. The strings below were **not** all run. Run them in the databases you can access (for example Google Scholar, arXiv listing search, ACL Anthology, Semantic Scholar, IEEE Xplore, PubMed for medical variants) and record the date, the hit count and what you screened.

### 2.1 Scholarly search strings

| # | Target | String (adapt operators to the database) |
|---|--------|------------------------------------------|
| S1 | Review routing with uncertainty vs random | `("active learning" OR "uncertainty sampling") AND ("human review" OR "label correction" OR "relabeling") AND ("random baseline" OR "random sampling")` |
| S2 | Budgeted correction of model pre-labels | `("pre-annotation" OR "model-assisted labeling" OR "AI-assisted annotation") AND ("correction budget" OR "review budget" OR "annotation budget")` |
| S3 | Prioritised label-error review | `("label error" OR "annotation error" OR "mislabeled") AND ("ranking" OR "prioritization") AND ("human verification" OR "human in the loop")` |
| S4 | Use of CIFAR-10H as an evaluation set | `"CIFAR-10H" AND ("human labels" OR "annotator" OR "label noise" OR "active learning")` |
| S5 | Human annotator accuracy vs model on same items | `("human annotators" OR "crowd workers") AND ("model" OR "classifier") AND ("same items" OR "agreement with reference") AND ("single annotator" OR "majority vote")` |
| S6 | Annotator noise floor | `("inter-annotator" OR "annotator variability") AND ("model improvement" OR "performance gap") AND ("noise floor" OR "within annotator spread" OR "ceiling")` |
| S7 | Weak active learning baselines | `("active learning" AND ("fails to outperform" OR "no better than") AND "random")` |
| S8 | Multi-annotator re-labelling | `("multiple annotators" OR "crowdsourcing") AND ("re-label" OR "relabel") AND "active learning"` |
| S9 | Scientific-domain variants (stretch) | `("active learning" OR "human-in-the-loop") AND ("medical image" OR "histopathology" OR "astronomy" OR "single-cell") AND "annotation cost"` |
| S10 | Reproducibility of AL evaluations | `"active learning" AND ("evaluation protocol" OR "reproducibility" OR "benchmark")` |

### 2.2 Categories of neighbouring work to inspect

1. Active-learning evaluation studies that compare against random sampling (training-set selection).
2. Work on **review routing**: choosing which model pre-labels a human should correct (not the same task as choosing training data; confirm).
3. Label-error detection and ranking, including benchmarks with human-checked errors in test sets.
4. Studies that release or use per-annotator labels (CIFAR-10H and similar) and report annotator-level accuracy.
5. Multi-annotator and re-labelling active learning.
6. Studies of single human annotators vs models on the same items.
7. Reviews of human-in-the-loop annotation (to see whether your review's "optimal strategy" claim has support elsewhere).
8. Domain studies in medical imaging, pathology, astronomy and omics (needed before any "scientific datasets" claim).

### 2.3 Screening record (you complete)

For each hit keep: database, query, date, title, authors, venue, year, DOI or URL **as shown by the database**, include/exclude and why. Do not carry any item into the manuscript unless you opened it.

---

## 3. Novelty / feasibility matrix

Only contributions I read on an opened page are listed as VERIFIED. Everything else is UNKNOWN.

| # | Published method | VERIFIED contribution (source) | Limitation (VERIFIED unless stated) | Proposed difference (INFERRED) | Evidence still missing |
|---|------------------|--------------------------------|--------------------------------------|--------------------------------|------------------------|
| 1 | Peterson et al., "Human uncertainty makes classification more robust" (ICCV 2019) | Introduced CIFAR10H, human label distributions for every CIFAR-10 test image. Training on them closed a gap between networks and human uncertainty, improved generalisation to shifted test sets and robustness to adversarial attacks. (arXiv abstract page 1908.07086v1; dataset README) | Used the labels for **training** soft-label classifiers, not for simulating a human review step. | Use the per-annotator labels to build a manual arm and a noise floor, and as a review simulation. | Whether other work already uses CIFAR-10H this way (S4, S5). |
| 2 | "Parting with Illusions about Deep Active Learning" (arXiv 1912.05361; authors not read on the pages opened, so none are named here) | Re-implemented recent deep active learning methods under more realistic settings; reports that gains over random sampling are small or inconsistent, especially at low budgets, and shrink with augmentation or semi-supervised learning; proposes a better evaluation protocol. (arXiv PDF abstract) | Concerns which samples to add to **training**, not which model pre-labels to review. Findings are for training-set selection on image classification and segmentation. | Test the same question for **correction routing**. A null result would be consistent with this paper; I must not assume the result either way. | Whether that paper's protocol (arXiv abstract only) should be adopted for seeds and budgets; author list and venue to be taken from the paper itself. |
| 3 | ActiveLab (arXiv 2301.11856) | Active learning for several imperfect annotators; decides between re-labelling and labelling new items; works with any classifier; compared with "a wide variety" of active-learning methods on image and tabular data. (arXiv abstract) | Abstract does not name the baselines, datasets, or code location. Setting needs repeat labels per item. | Single reviewer with perfect labels, no re-labelling decision. A narrower, simpler question. | Datasets and baselines (read the paper); whether it includes a random-review baseline; code (UNKNOWN). |
| 4 | "Deep Active Learning for Data Mining from Conflict Text Corpora" (arXiv 2402.01577) = review ref [22] | Active learning to fine-tune an encoder-only language model for extracting finer conflict dynamics; reports performance similar to gold-standard human coding with human labeling reduced by up to 99%. (arXiv abstract) | Abstract states no baseline, metric or conditions for the 99%. "Up to" suggests a best case. Text domain only. | Image classification; fixed budget grid; random and fixed-fraction comparators with intervals. | Corpus, baseline and conditions behind 99% (read the paper). Claim C14 stays UNKNOWN until then. |
| 5 | ActiveAED (Weber and Plank, ACL Findings 2023) = review ref [71] | Detects annotation errors by repeatedly querying a human for corrections in the prediction loop; evaluated on eight datasets over five tasks; improves on the state of the art on seven, up to six points average precision. (Stage 2 abstract pages) | All text tasks. **Code not found** (a dedicated search this stage returned nothing relevant). | Not reproduced. Study B uses a generic uncertainty loop, which tests the review's claim, not this method. | Code link in the paper or author pages; whether it uses AUM (review states so). |
| 6 | Confident Learning / cleanlab (Northcutt, Jiang, Chuang, JAIR 2021) | The package implements confident learning to find and quantify label issues; supports multi-annotator consensus and active-learning suggestions. (cleanlab README, Stage 2) | Needs out-of-sample probabilities (INFERRED). Theory assumptions for model-correlated noise not read. | Not part of the narrowed Study B; stretch (Study A or C). | JAIR paper read (V4). |
| 7 | "Pervasive Label Errors in Test Sets Destabilize Machine Learning Benchmarks" (NeurIPS 2021) | **Title only**, seen in the cleanlab README citation list. Contribution not read. | UNKNOWN | Possible neighbour for label errors in the CIFAR-10 test set, which CIFAR-10H uses. | Open the paper; check whether CIFAR-10 test labels are discussed and how that affects choosing a reference label (V8). |

**Reading of the matrix (INFERRED).** The nearest verified work either uses the data for training (row 1), studies training-set selection (row 2), or needs repeat labels (row 3). That suggests Study B is a small, specific evaluation, but the matrix cannot show that nobody has done it. The searches in Section 2 can.

**What a novelty claim would need:** S1-S5 run and screened, no hit that already compares uncertainty vs random review at fixed budgets on per-annotator data, and the screening record kept. Until then use the wording "this study tests the claim in [review] on ..." and avoid "first" or "novel".

---

## 4. Resource-access check

| Resource | Needed for | Status | Evidence | Tag |
|----------|-----------|--------|----------|-----|
| CIFAR-10H data files | Core | Accessible in principle. README lists `cifar10h-counts.npy` (10,000 x 10 counts, about 50 judgments per image), `cifar10h-probs.npy` and `cifar10h-raw.zip` (annotator-level CSV with annotator ID, trial index, true and chosen labels, reaction time, test-set index). Labels follow CIFAR-10 test order. TFDS also lists the dataset (172.92 MiB). | GitHub README; TFDS page | VERIFIED (files); download not tested |
| CIFAR-10H licence | Core | README does not state terms; page lists a LICENSE.txt that I did not read. | README fetch | **UNRESOLVED** |
| CIFAR-10H citation requirements | Core | README asks to cite three works (ICCV 2019; Nature Communications 2020; CogSci 2020). | README | VERIFIED |
| CIFAR-10 images and labels | Core (training set for the classifier) | Not opened this stage. Reference to TFDS CIFAR-10H says its train split is identical to CIFAR-10. | TFDS page (Stage 2) | VERIFIED (statement); CIFAR-10 licence UNKNOWN |
| Pretrained frozen backbone | Core | Not chosen, not checked. No model has been named, so no weights, licence or size is verified. | n/a | **UNRESOLVED** |
| Per-annotator coverage | Manual arm, noise floor | Raw file has annotator IDs. Each worker labelled 200 images, so one "annotator" covers only 200 items; a per-item "one annotator" draw is possible, a per-annotator accuracy over all 10,000 items is not. | Stage 2 dataset pages; README columns | VERIFIED (design facts); consequence INFERRED |
| Benchmark protocol for review-routing | Core | **No standard protocol found.** The only protocol-related source read is the evaluation critique in row 2. | Section 3 | **UNRESOLVED** (D-014: define and pre-register own protocol) |
| cleanlab package | Stretch | Official AGPL-3.0, latest version 2.7.1 released 27 Feb 2025 (Snyk advisor page). README gives the API. | Snyk page; Stage 2 README | VERIFIED (licence, version, via third-party index); repo LICENSE file not opened |
| ActiveLab code | Optional | Abstract mentions none; cleanlab docs list a multiannotator module in search results (page not opened). | arXiv abstract; search listing only | **UNRESOLVED** |
| ActiveAED code | Not needed for Study B | Not found. | Search this stage | UNRESOLVED |
| MedSAM repo and weights | Stretch only | Verified in Stage 2 (repo, 375 MB Zenodo weights); Apache-2.0 second-hand. | Stage 2 | VERIFIED / licence second-hand |
| LIDC-IDRI | Stretch only | Four-radiologist annotations on TCIA; access terms not read first-hand. | Stage 2 | licence **UNRESOLVED** |
| Compute and time | Core | See Section 5. | n/a | UNKNOWN |

**Unresolved availability claims (flag list):** CIFAR-10H licence; pretrained backbone and its licence; CIFAR-10 licence; benchmark protocol; ActiveLab and ActiveAED code; LIDC-IDRI terms; MedSAM licence file; cleanlab LICENSE file (index page used).

---

## 5. Computational and time estimate

No code has been run. All numbers below are scale estimates to be replaced by the week-1 smoke test. I did not look up any timings.

**Assumed resources:** one free-tier notebook GPU or a laptop CPU (UNKNOWN); 4 part-time weeks (UNKNOWN).

| Step | Scale (INFERRED) | What drives it | Measure in week 1 |
|------|------------------|----------------|-------------------|
| Feature extraction: 50,000 train + 10,000 test images with a small pretrained backbone | One pass over 60,000 small images. Likely feasible on a notebook GPU; on CPU it is the dominant cost and may take a long session. | Backbone size, image resize, batch size | Time on 500 images; extrapolate |
| Linear classifier on frozen features | Seconds to minutes | Feature dimension, solver | Time one fit |
| Arms and budget grid | Each arm is ranking and indexing on 10,000 probability vectors; negligible compared with feature extraction | Seeds x budgets x arms | Time one full grid run |
| Paired bootstrap intervals | Cheap on 10,000 items | Resamples count | Time at 1,000 and 10,000 resamples |
| Storage | CIFAR-10H download is 172.92 MiB per TFDS; features for 60,000 images are small compared with raw images | Feature dimension | Check disk |
| Writing, checks, figures | Human time, not compute | Your pace | Track hours |

**Time budget (assumed 4 weeks):** week 1 verification and smoke test; week 2 baselines; week 3 routing arms and intervals; week 4 noise floor, limitations, draft. Feature extraction is done once and cached, so it should not recur across seeds (INFERRED).

**If measured time is too high:** cache features first; reduce seeds, budget points or bootstrap resamples; use a smaller backbone; as a last resort use a subset of test items, and state that in the paper. Do not add models.

---

## 6. Go / no-go decision

**Decision (PROPOSED): GO for the narrowed Study B as a verification-first project; NO-GO on any novelty claim until S1-S5 are run.**

| Criterion | Assessment | Basis |
|-----------|------------|-------|
| Question is answerable with data in hand | Yes, if CIFAR-10H downloads and a backbone is chosen | Data files VERIFIED; download not tested |
| Compute fits assumed resources | Probably | INFERRED; unmeasured |
| Code dependency | None for the core arms (own loops); no unverified code needed | INFERRED |
| Licence clarity | **Not resolved** for CIFAR-10H and the backbone | README silent; backbone not chosen |
| Novelty | Unknown; nearest verified work differs in setting (training vs review routing; repeat labels) but a search is outstanding | Section 3 |
| Fit with the title | **Partial.** CIFAR-10H is natural images; "scientific datasets" is not met | Stage 2; V10 |

**Conditions to convert "GO" to final (all PROPOSED):**
1. CIFAR-10H LICENSE.txt read and compatible with your use (blocker for publishing derived results).
2. A backbone and its licence chosen and recorded.
3. Reference-label rule written down before any run (V8).
4. Week-1 timing shows the grid fits.
5. Supervisor confirms a non-scientific first stage is acceptable, or a scientific second dataset is added (V10).
6. S1-S5 run and screened; wording adjusted to what they show.

**No-go triggers:** CIFAR-10H terms forbid your use; a screened paper already compares uncertainty vs random review on per-annotator data with the same design (then switch to a replication framing or to Study A/C); timing shows the core grid cannot finish in the available weeks.

---

## 7. Fallbacks

| If unavailable | Fallback | Cost / caveat | Tag |
|----------------|----------|---------------|-----|
| CIFAR-10H (download or licence) | Use CIFAR-10 with **simulated** annotators drawn from a stated noise model | Weaker: simulated humans are an assumption, and the noise-floor line loses meaning. Report as simulation only. | INFERRED |
| Chosen pretrained backbone or its weights | A different openly licensed backbone, or train a small CNN from scratch on CIFAR-10 | Check the new licence. From-scratch training adds compute time and changes the accuracy level. | INFERRED; licences UNKNOWN |
| Any pretrained weights (none usable) | Classical features plus a linear model | Lower accuracy; routing effects may differ. | INFERRED |
| cleanlab (licence or install) | Not needed for Study B; skip Study A/C or write the thresholding by hand | Loses the verified implementation for the stretch | INFERRED |
| ActiveLab / ActiveAED code | Keep the generic uncertainty loop; describe it as such (D-010) | No reproduction claim | VERIFIED rule (D-010) |
| A usable scientific multi-annotator dataset | LIDC-IDRI (four radiologists) or another dataset you verify yourself | Heavier data handling; terms to read | Stage 2; UNRESOLVED |
| Everything blocked | Reduce to a methods-and-protocol paper: the audit, the protocol and the pre-registration, with no result | Honest but a smaller contribution | INFERRED |

---

## 8. Decision log additions (continuing the log)

| ID | Decision | Status | Next action |
|----|----------|--------|-------------|
| D-013 | Adopt the narrowed question in Section 1 for Study B | PROPOSED | Confirm after V8-V10 |
| D-014 | Pre-register an own review-routing protocol (seeds, budgets, reference rule, interval method) because no standard was found | PROPOSED | Write before first run |
| D-015 | Make no novelty claim until searches S1-S5 are run and screened | PROPOSED | Run searches, keep the record |
| D-016 | Treat CIFAR-10H licence as a blocker for release of derived results | PROPOSED | Read LICENSE.txt |
| D-017 | Defer MedSAM, LIDC-IDRI and Confident Learning arms to stretch | PROPOSED | Revisit after core results |

**Next actions:** N1 confirm D-004 to D-017; N2 read CIFAR-10H LICENSE.txt and choose a backbone with its licence; N3 run S1-S5 and record; N4 week-1 smoke test (timing); N5 draft research question and hypotheses (Stage 4) after the go/no-go conditions are met.

---

## 9. Sources opened in this stage

| What | Page | Used for |
|------|------|----------|
| Conflict-text active learning abstract | arxiv.org/abs/2402.01577 | Rows 4, C14 status |
| ActiveLab abstract | arxiv.org/abs/2301.11856v1 | Row 3 |
| Deep active learning evaluation critique | arxiv.org/pdf/1912.05361 | Row 2 |
| CIFAR-10H abstract | arxiv.org/abs/1908.07086v1 | Row 1 |
| CIFAR-10H repository README | github.com/jcpeterson/cifar-10h | Files, citations, licence gap |
| cleanlab package index | snyk.io/advisor/python/cleanlab | Licence AGPL-3.0, version 2.7.1 |
| Earlier pages (Stage 2) | see `literature_to_experiment_bridge.md`, Section 8 | Rows 5-6, MedSAM, LIDC-IDRI |
| Search listings only (not opened) | cleanlab multiannotator docs; PapersWithCode and similar | Pointers, not evidence |

---

*Bridge continued: original papers -> selected method -> executable baseline -> planned test -> **novelty and feasibility gate (this file)**. Log entries are appended as decisions are made.*
