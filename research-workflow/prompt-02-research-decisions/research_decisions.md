# research_decisions.md

**Project:** Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets
**Goal:** Convert a completed literature review into an implementation-based research paper
**Log opened:** 2026-10-21 | **Current stage:** 0 (Intake) -> 1 (Gap identification)

---

## 0. Conventions

**Evidence tags** (applied to every substantive statement):

- **VERIFIED** - confirmed in a file, source, or output that has been shown and read.
- **INFERRED** - a reasoned conclusion from verified material; the reasoning is stated.
- **UNKNOWN** - no evidence yet; the file, output, or check that would resolve it is named.

**Decision status:** ADOPTED (settled in the project brief) | PROPOSED (needs confirmation) | OPEN (needs evidence before deciding).

**Entry template:** ID - Decision - Reason - Source/Evidence (with tag) - Next action.

**Standing rules:** no invented papers, datasets, repository links, code execution, experiments, or metrics. Every number in the final manuscript must trace to an output that was actually produced and shown.

---

## 1. Source review: scope as read from the attached PDF

Everything below was read from the attached file only. Nothing outside it has been checked.

| # | Item | Tag |
|---|------|-----|
| S1 | IEEE-style two-column paper: Abstract, 8 numbered sections (I-VIII), 3 tables, 2 figures, 3 numbered equations, 79 references. | VERIFIED |
| S2 | Type: narrative review. No search protocol, databases, date range, inclusion/exclusion criteria, or screening process is stated. Whether one was followed is not visible in the file. | VERIFIED (absent from text); protocol existence UNKNOWN |
| S3 | No research questions, hypotheses, or experiments are stated. | VERIFIED |
| S4 | Section map: I Introduction; II Theoretical and statistical frameworks for ground truth (annotation as measurement, IAA metrics); III Medical imaging and computational pathology (SAM/MedSAM, annotation throughput, HybridMS); IV Genomics and clinical text (scRNA-seq LLM annotation, clinical trial data cleaning); V Astrophysics and geospatial remote sensing (galaxy morphology only); VI Psychology and ergonomics (fatigue, automation bias/anchoring); VII Label-noise mitigation (active learning, confident learning); VIII Conclusion. | VERIFIED |
| S5 | Domains in the abstract: computational pathology, single-cell transcriptomics, clinical trial management, geospatial remote sensing, astrophysics. | VERIFIED |
| S6 | Domains with body content: medical imaging and pathology, scRNA-seq, clinical trial data cleaning, galaxy morphology. Geospatial remote sensing has no body subsection. | VERIFIED |
| S7 | Central thesis in the conclusion: AI assistance speeds labeling and reduces fatigue and inter-observer variability, but adds automation bias and anchoring risk; best strategy is stated to rely on active learning and confident learning. | VERIFIED (what the text says); strength of support see E6 |
| S8 | Metrics defined: Cohen's kappa, Fleiss' kappa, Krippendorff's alpha, STAPLE, Dice (DSC), IoU. | VERIFIED |
| S9 | Source authorship/provenance: the title page lists one author. Whether this is the researcher's own work, co-authored work, or a shared draft is not stated in the file. | UNKNOWN - confirm (see D-004) |

---

## 2. Evidence audit

### 2.1 Findings

| ID | Finding | Where | Tag | Action |
|----|---------|-------|-----|--------|
| E1 | **Citation-claim mismatches inside the document.** (a) Sec. III-B cites [7] (brain tumour segmentation benchmarking) as "a benchmark study" of annotation peripherals and cites [1] (statistical framework for human labeling) for the 29.9-minute / 24% mouse-annotation result; the reference list shows the pathology pilot study as [9]. (b) Sec. VII-A cites ActiveAED as [23], but [23] in the list is a conformal-in-the-loop paper; ActiveAED is [71]. (c) Active-learning principle is cited to [21], which is a retinal-image confident-learning paper. | III-B, VII-A, refs | VERIFIED (mismatch between text and list); correct source UNKNOWN | Re-map each claim to its true source after opening the source |
| E2 | **Uncited references.** I found no in-text citation for [24]-[79] (56 of 79 entries). This includes the geospatial references [51]-[56] and the automation-bias-in-pathology paper [63]. | Sections I-VIII | VERIFIED (from the text provided) | Decide per reference: cite, or remove |
| E3 | **Uncited quantitative claims.** The oral-lesion kappa = 0.90, the "substantial label noise in curated benchmarks" claim (abstract), and the VLM/VQA transition statement (Sec. V-A) carry no citation. | Abstract, II-B, V-A | VERIFIED | Source each or delete |
| E4 | **Reference list quality.** Most entries use placeholder authors ("Author Team N", "A. T. N") instead of real author names. Titles often include site suffixes (e.g., "pdf", "researchgate", "mdpi", "scribd"). Duplicates: [13], [43], [44] share one title and arXiv ID; [14] and [48] share one title and arXiv ID. Some URLs look malformed: [3] has non-hexadecimal characters in what looks like a UUID; [53] has a broken GitHub path; [55] has a truncated DOI; [63] has an arXiv ID of unusual shape. | References | VERIFIED (as printed); whether URLs resolve UNKNOWN | Rebuild the list from the real source pages |
| E5 | **Citation years.** Every entry is dated 2026, but several arXiv IDs encode earlier months (e.g., 2408.xxxxx, 2504.xxxxx, 2508.xxxxx, 2503.xxxxx). The year appears to be access year, not publication year. | References | INFERRED (arXiv IDs encode YYMM) | Replace with true publication years/venues |
| E6 | **Weak sources behind key psychology claims.** The 30% fatigue error rate cites a vendor blog [18]; fatigue [17] is a company blog; "Weight of Advice" [20] is a document-hosting upload; several IAA definitions rest on vendor or aggregator pages ([3], [26], [28]). | VI, II | VERIFIED (sources as listed); weakness INFERRED | Replace with primary or peer-reviewed sources |
| E7 | **Construct mismatch with the title.** The Dice values in Table II mostly compare model outputs (zero-shot SAM, MedSAM, nnU-Net) against reference masks. That is model accuracy, not accuracy of an AI-assisted human workflow versus a manual workflow. Workflow-level comparisons in the text are [9] (time, variability), [10] (time, Likert grade), [11] (Dice, time) and [13] (error rate, throughput), and they use different outcome measures. | III, IV, Table II | INFERRED from the text | Define "labeling accuracy" before choosing experiments (see D-007) |
| E8 | **Table II cells without support.** "Efficiency gain: High" for SAM and MedSAM and "None" for nnU-Net have no numbers in the text. The nnU-Net row says "Lumbar/Glioma, DSC 0.99", but the text gives 0.99 for lumbar structures only; the glioma passage reports 0.894 as an upper bound for SAM with precise boxes. | Table II, III-A | VERIFIED (text vs table) | Correct or remove |
| E9 | **Overreach in the conclusion.** (a) "Decrease inter-observer variability" rests on one pilot study [9]. (b) "Successfully mitigate annotation fatigue" - no fatigue measurement across sessions is reported. (c) "Replacing subjective manual literature reviews" appears to refer to manual cell-type annotation; the wording does not match the body. (d) "Optimal strategy relies heavily on active and confident learning" - the body presents no comparison against alternatives. (e) Sec. III-B explains higher AI-assisted Likert grades as AI uncovering boundary details that fatigue hides - a causal explanation not tested in the text. | III-B, VIII | INFERRED | Soften wording or add evidence |
| E10 | **Imprecise technical statement.** Table I describes Dice/IoU as "harmonic mean of precision and recall". By the review's own equations (2)-(3), that holds for Dice only, not IoU. | Table I | VERIFIED (against eqs. 2-3) | Fix |
| E11 | **Small effects reported without uncertainty.** HybridMS vs MedSAM: Dice 0.9538 vs 0.9435 (difference 0.0103). GB-SAM vs U-Net: 0.885 vs 0.857 (difference 0.028). No confidence intervals, test statistics, or seed counts appear in the review. Whether the sources report them is unknown. | III-A, III-C | VERIFIED (differences computed from review values); source reporting UNKNOWN | Check sources; plan uncertainty reporting in own experiment |
| E12 | **Domain imbalance.** Abstract promises geospatial remote sensing; body has none. Genomics body = scRNA-seq only. Astronomy figures (87%, about 97%) are model-vs-expert-label results, not human-vs-AI-assisted comparisons. | Abstract, IV, V | VERIFIED / INFERRED | Narrow or rebalance scope |
| E13 | **Figures 1 and 2** contain small numeric tables (time effort, kappa, Dice, query counts) with no source in the captions. The values cannot be read reliably at the resolution provided. They may be illustrative. | Figs. 1-2 | UNKNOWN | Provide figure source files or confirm they are illustrative |
| E14 | **Structure.** The abstract stops after defining the HITL paradigm and states no findings. The introduction begins mid-thought, continuing the abstract's last sentence. | Abstract, I | VERIFIED | Fix when the manuscript is rebuilt |
| E15 | **Arithmetic spot-checks.** Octozi: 54.67 / 8.48 = 6.447, reported as 6.44 (truncated rather than rounded; check the source). Pathology: 29.9 -> 13.6 minutes is a 54.5% reduction. | IV-B, III-B | VERIFIED (computed) | None beyond source check |

### 2.2 Claim register (numbers to verify against source files)

All entries are **UNKNOWN** until the cited source has been opened and the number located in it.

| ID | Claim as written in the review | Cited as |
|----|--------------------------------|----------|
| C1 | Fleiss' kappa 0.383 (internal) and 0.255 (external), eleven ICU consultants | [2] |
| C2 | Oral potentially malignant disorders, expert kappa = 0.90 | uncited |
| C3 | MedSAM training set: 1,570,263 image-mask pairs, 10 modalities, 30+ cancer types | [5] |
| C4 | Lumbar MRI: SAM Dice 0.64 (discs), 0.83 (vertebrae); MedSAM 0.79, 0.88; nnU-Net 0.99 | [6] |
| C5 | BraTS 2023: SAM/SAM 2 up to 0.894 Dice with precise box prompts | [7] |
| C6 | CRAG: GB-SAM 0.885 with 25% of data vs U-Net 0.857 | [8] |
| C7 | WSI annotation: mouse 29.9 min / 24%; touchpad 47.5 min / 45%; SAM-assisted 13.6 min / 2% | [1] and [9] (see E1) |
| C8 | AICL: 2.8x less effort than clinical staff editing, 8.7x less than expert from scratch; Likert 8.4 vs 7.8 | [10] |
| C9 | HybridMS: Dice 0.9538 vs MedSAM 0.9435; time down 82% (60% on challenging cases) | [11] |
| C10 | LLM cell-typing benchmark across 34 datasets; outperforms SingleR, Cellmarker2.0, ScType | [12] |
| C11 | Octozi: throughput 6.03x; cleaning errors 54.67% -> 8.48% | [13] |
| C12 | Zoobot lopsided-galaxy accuracy 87%; YOLOv5 edge-on detection about 97% | [15], [16] |
| C13 | Prolonged manual annotation: error rates up to 30% | [18] |
| C14 | Active learning reduces annotation budget by up to 99% | [22] |

---

## 3. Decision log

### Adopted (from the project brief)

**D-001 - Evidence-tagging protocol**
- Decision: every substantive statement is tagged VERIFIED, INFERRED, or UNKNOWN.
- Reason: keeps claims traceable and prevents unverified material from entering the manuscript.
- Source: project brief. Status: ADOPTED.
- Next action: apply to all later stages.

**D-002 - Staged workflow**
- Decision: gap identification -> literature-to-experiment mapping -> feasibility -> research questions -> verified baseline -> coding -> experimental evaluation -> manuscript and reproducibility.
- Reason: each stage produces evidence the next stage depends on.
- Source: project brief. Status: ADOPTED.
- Next action: proceed to Stage 1.

**D-003 - No fabrication**
- Decision: no invented papers, datasets, repository links, code execution, experiments, or metrics. Any result in the paper must come from an output that was run and shown.
- Reason: research integrity and reproducibility.
- Source: project brief. Status: ADOPTED.
- Next action: request source files or outputs whenever evidence is missing.

### Proposed (need confirmation)

**D-004 - Confirm provenance of the source review**
- Decision: record who authored the review and how the extension paper will credit it.
- Reason: the title page lists one author (S9); authorship and reuse permission affect how the new paper is framed and submitted.
- Source: S9 (UNKNOWN). Status: PROPOSED.
- Next action: researcher confirms ownership/co-authorship and any supervisor or course requirements.

**D-005 - Rebuild the reference list before any reuse**
- Decision: do not carry the existing reference list into the new manuscript. Rebuild it from the actual source pages with real authors, venues, years, and working links; keep only references that are cited and verified.
- Reason: E1-E6 (mismatched citations, placeholders, duplicates, uncited entries, weak sources, wrong years).
- Source: E1-E6 (VERIFIED as printed). Status: PROPOSED.
- Next action: verify load-bearing sources first: [2], [5], [6], [9], [10], [11], [13], [63].

**D-006 - Describe the review honestly as a narrative review**
- Decision: the extension paper presents the review as a narrative synthesis and does not claim systematic-review methodology.
- Reason: no search protocol is stated (S2).
- Source: S2. Status: PROPOSED.
- Next action: if a search protocol exists, provide it; otherwise adopt this wording.

**D-007 - Define "labeling accuracy" before designing experiments**
- Decision: operationalize accuracy as agreement between the final labels from each workflow (manual vs AI-assisted) and an adjudicated reference, reported with uncertainty, alongside time and annotator-agreement outcomes.
- Reason: the review mostly reports model-vs-reference accuracy (E7), which does not answer the title's question; outcome measures differ across studies (Dice, error %, Likert, kappa, minutes).
- Source: E7 (INFERRED). Status: PROPOSED.
- Next action: confirm in Stage 1; then check which public datasets provide both adjudicated references and multi-annotator labels (not yet identified; UNKNOWN).

### Open (need evidence)

| ID | Question | Evidence needed |
|----|----------|-----------------|
| O-1 | Primary research question and hypotheses | Stage 1 gap analysis; supervisor expectations |
| O-2 | Which domain(s) and dataset(s) to use (the review spans four; one or two is likely feasible) | Compute and time limits; dataset licences and label availability |
| O-3 | Source of "manual" labels: existing multi-annotator labels, or new annotation | Dataset documentation; whether human annotators can be recruited |
| O-4 | Is a new experiment required, or is a smaller replication acceptable | Course brief or supervisor |
| O-5 | Compute environment (CPU/GPU, Colab, local, cluster) | Researcher input |
| O-6 | Deadline, venue, format, length | Researcher input / rubric |

---

## 4. Provisional gap candidates (INFERRED - to be tested in Stage 1)

| ID | Candidate gap | Basis |
|----|---------------|-------|
| G1 | Few studies in the review directly compare AI-assisted and manual workflows against a common reference with accuracy as the primary outcome. | E7 |
| G2 | No common accuracy scale across domains; outcomes are Dice, error rate, Likert grade, kappa, and time. | E7, C-register |
| G3 | Automation-bias and anchoring evidence relies on weak sources; the one computational-pathology study on it ([63]) is listed but never cited. | E2, E6 |
| G4 | Reported gains are small in places and carry no stated uncertainty. | E11 |

These are candidates only. None becomes a research gap until the supporting sources are opened and read.

---

## 5. Evidence requests

1. Confirmation of authorship and provenance of the source review (D-004).
2. PDFs, or permission to fetch and read, the load-bearing sources: [2], [5], [6], [9], [10], [11], [13], [63].
3. Source files or data behind Figures 1 and 2, or confirmation that the values are illustrative (E13).
4. Deadline, venue or rubric, expected length (O-6).
5. Compute environment (O-5).
6. Any datasets, labeled samples, annotation tools, or code already in hand.
7. Whether a new experiment is required or a replication is enough (O-4).

---

## 6. Next actions

| # | Action | Stage | Depends on |
|---|--------|-------|------------|
| N1 | Confirm D-004 to D-007 or amend them | 0 | Researcher |
| N2 | Open the load-bearing sources and mark each claim C1-C14 VERIFIED or not | 1 | Evidence request 2 |
| N3 | Turn gap candidates G1-G4 into evidence-backed gaps | 1 | N2 |
| N4 | Map each confirmed gap to a testable experiment | 2 | N3 |
| N5 | Feasibility check against data, compute, time | 3 | O-2, O-5, O-6 |
| N6 | Draft research questions and hypotheses | 4 | N4, N5 |

---

*Log entries are appended as decisions are made. Superseded entries are marked, not deleted.*
