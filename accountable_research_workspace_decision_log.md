# Accountable Research Workspace & Decision Log (`research_decisions.md`)

- **Student Name:** Abhay Kumar Awasthi
- **Enrollment No.:** MHM2026011
- **Institution:** Indian Institute of Information Technology, Prayagraj (IIIT-A)
- **Email:** MHM2026011@iiita.ac.in
- **Course:** AI Tools for Research (Submission: Prompt 01 & Prompt 02)
- **Completed Literature Review Title:** *Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets*

---

## 1. Evidence Tracking Rules (Prompt 01 Setup)

- **`[VERIFIED]`**: Facts, metrics, or limitations directly present in my literature review or checked from the original paper / working code.
- **`[INFERRED]`**: My own reasoning, hypothesis, or experimental plan based on the literature that still needs to be tested through code.
- **`[UNKNOWN]`**: Details missing from my review (such as incomplete reference info, dataset splits, or unrun code) that I must check manually.

---

## 2. Summary of My Literature Review Scope (Prompt 01 Deliverable)

In my first paper, I reviewed how scientific data labeling is shifting from purely manual expert annotation to Human-in-the-Loop (HITL) AI-assisted labeling across four main areas `[VERIFIED]`:

1. **Ground Truth & Agreement Metrics (Section II):** I discussed the Human Label Variation (HLV) framework by Chew et al. [1], which explains that annotator disagreement is not always random noise, but comes from four sources: instance difficulty, annotator bias, situational noise, and relational alignment `[VERIFIED]`. For example, 11 ICU doctors in Sylolypavan et al. [2] only reached fair internal agreement (Fleiss' $\kappa = 0.383$) and minimal external agreement ($\kappa = 0.255$), whereas intraoral image labeling reached $\kappa = 0.90$ [25] `[VERIFIED]`. I also covered Cohen's $\kappa$, Fleiss' $\kappa$, Krippendorff's $\alpha$, STAPLE, Dice (DSC), and IoU (Table I) `[VERIFIED]`.
2. **Medical Imaging & Pathology (Section III):** I compared zero-shot SAM [4], domain-adapted MedSAM (trained on 1.57M image-mask pairs across 10 modalities and >30 cancer types [5]), Granular Box Prompts (GB-SAM [8]), and fully supervised nnU-Net [6, 7] `[VERIFIED]`. I also looked at time savings in Whole Slide Imaging (WSI, cutting time from 29.9 min with mouse / 47.5 min with touchpad to 13.6 min with SAM [9]), volumetric CT hemorrhage labeling (AICL, 2.8x–8.7x faster [10]), and uncertainty-based HybridMS for chest X-rays (DSC 0.9538, 82% faster [11]) `[VERIFIED]`.
3. **Genomics & Clinical Text Cleaning (Section IV):** I reviewed how LLMs and multi-agent tools (DeepCellSeek, CASSIA, GPT-5, Claude-4.1, Kimi-k2, Grok-4) outperform traditional tools like SingleR, CellMarker2.0, and ScType across 34 scRNA-seq datasets [12, 38], and how the Octozi tool improved clinical trial data cleaning speed by 6.03x while reducing errors from 54.67% to 8.48% [13] `[VERIFIED]`.
4. **Astrophysics & Remote Sensing (Section V):** I covered how Galaxy Zoo crowdsourcing is being replaced by deep models like Zoobot (87% accuracy on lopsided spiral galaxies [15]), YOLOv5 (~97% detection of edge-on galaxies in Pan-STARRS [16]), and Vision-Language Models [14] `[VERIFIED]`.
5. **Human Psychology & Noise Cleaning (Sections VI & VII):** I examined manual annotation fatigue (which can push error rates up to 30% [17, 18]) versus AI automation bias and the anchoring effect measured by Weight of Advice (WoA [19, 20, 63]) `[VERIFIED]`. Finally, I reviewed Active Learning (cutting labeling budgets up to 99% [21, 22]), ActiveAED using Area-under-the-Margin (AUM [23, 71]), and Confident Learning (CL [21, 74, 75]) `[VERIFIED]`.

---

## 3. Portable Research Decision Log (`research_decisions.md` Table)

| Date / Step | Decision Taken | Why I Made This Decision | Evidence & Status | Next Action |
| :--- | :--- | :--- | :--- | :--- |
| **21-10-2026**<br>Prompt 01 | Check and fix reference details from my first paper before starting the implementation study. | In my review PDF, Refs [3] and [6]–[79] got exported with placeholder author names ("Author Team X" / "A. T. X") and year "2026", even though the links point to real 2022–2025 arXiv/PMC papers. | `[VERIFIED]` issue in my review PDF; real author names `[UNKNOWN]` until opened. | Open the exact PMC/arXiv links for the 3–5 core papers I choose and write down real authors and years. |
| **21-10-2026**<br>Prompt 01 | Do not use the small metric tables inside Fig. 1 and Fig. 2 as my experimental baseline numbers. | Fig. 1 shows (Manual: 29 min, AI: 13 min, Kappa: 0.42, DSC: 0.78, FP: -47%) and Fig. 2 shows (Cycles 1–4). These were summary diagrams for the review, not raw results from one specific dataset. | `[VERIFIED]` in Fig. 1 & 2; exact source dataset `[UNKNOWN]`. | Use only properly cited benchmark results from Table II and the main text for baseline validation. |
| **21-10-2026**<br>Prompt 01 | Focus my implementation study on publicly available datasets and code that run on Google Colab (T4 GPU). | Recruiting real doctors or hospital staff for a live annotation timing study is not possible within the course timeline, so human label noise or box imperfection must be tested reproducibly in code. | `[INFERRED]` practical constraint; Colab GPU access `[VERIFIED]`. | Extract 5 testable research gaps in Prompt 02 and rank the top 3 by feasibility. |
| **21-10-2026**<br>Prompt 01 | Maintain this portable `research_decisions.md` log file for all literature-to-experiment decisions. | Recording every decision with its reason, source evidence, and epistemic label (`[VERIFIED]`, `[INFERRED]`, `[UNKNOWN]`) ensures full accountability and prevents relying on unverified assumptions. | `[VERIFIED]` Prompt 01 requirement. | Use this decision log to guide the gap extraction in Prompt 02. |

---

## 4. Extracted Evidence-Based Research Gaps (Prompt 02 Summary Matrix)

| Gap ID & Title | Review Passage & Reported Limitation `[VERIFIED]` | My Inference `[INFERRED]` | Testable Experimental Question | Evidence & Protocol to Test It |
| :--- | :--- | :--- | :--- | :--- |
| **Gap 1:** Sensitivity of MedSAM vs. SAM to Imperfect (Jittered) Bounding-Box Prompts | Sec. III-A (p. 2–3, Table II, Refs [6, 7, 8]): SAM/SAM 2 reach high Dice scores (0.894 on BraTS 2023) only with "perfectly precise bounding box prompts," which doctors cannot consistently draw in daily work [7]. | Tired clinicians draw boxes that are slightly shifted, loose, or cropped. The review does not measure how fast MedSAM vs. SAM degrades as box jitter increases or whether simple box padding recovers accuracy. | *How much does segmentation accuracy (DSC and IoU) drop in MedSAM vs. zero-shot SAM when bounding-box prompts are shifted/scaled by 5%, 10%, 20%, and 30%, and does 10% box-margin expansion recover accuracy?* | Run pretrained `MedSAM` and `SAM` weights on a public 2D medical dataset (Chest X-ray TB [11] or CRAG pathology [8]) with seeded box perturbations. |
| **Gap 2:** Area-Under-the-Margin (ActiveAED) vs. Confident Learning for Catching Label Noise | Sec. VII-A & VII-B (p. 4–5, Fig. 2, Refs [21, 23, 71, 74]) describe ActiveAED (using AUM during training [23, 71]) and Confident Learning (using out-of-fold probabilities [21, 74]), without comparing them on the same noisy scientific dataset. | Basic entropy sampling confuses genuinely ambiguous cases (HLV instance difficulty [1]) with mislabeled samples. AUM or Confident Learning should separate real label errors from hard edge cases better than entropy. | *Under controlled label noise rates of 10%, 20%, and 30% (matching manual fatigue rates in [18]), how do AUM (ActiveAED), Confident Learning, and Predictive Entropy compare in finding corrupted labels and improving test F1?* | Test on a public scientific dataset (MedMNIST or scRNA-seq cell typing [12]) across 5 random seeds; measure Error Detection Precision@K, Recall@K, and post-cleaning Macro-F1. |
| **Gap 3:** Combining Uncertainty Sampling with Confident Learning Under a Fixed Review Budget | Sec. III-C (HybridMS [11]) and Sec. VII (Fig. 1 & Fig. 2 [21, 22]) combine active uncertainty filtering (Sub-process A) and Confident Learning purification (Sub-process B), but no ablation compares their combined vs. isolated effect. | Uncertainty sampling picks low-confidence boundary items while Confident Learning flags high-confidence wrong labels. Splitting a fixed human review budget (e.g., 20%) between both should beat either single strategy. | *When human correction is capped at 10%, 20%, or 30% of a noisy dataset, does a 50/50 hybrid of Uncertainty Sampling + Confident Learning yield higher downstream test accuracy than pure Uncertainty Sampling, pure CL, or Random selection?* | Train a classifier on a benchmark with 20% noisy pre-labels; compare 4 routing strategies across 5 seeds. |
| **Gap 4:** Selective Blind Review to Reduce Anchoring Bias (Weight of Advice) in AI Pre-Labeling | Sec. VI-B (p. 4, Table III, Refs [19, 20, 63]) states that high AI accuracy makes human reviewers complacent and anchored to AI predictions (Weight of Advice, WoA). Table III suggests "blind review of low-confidence predictions" without empirical numbers. | We can simulate an anchored human reviewer in code (who copies the AI pre-label with probability proportional to WoA $\alpha \in \{0.3, 0.6, 0.9\}$) and test if hiding AI pre-labels when model entropy is high prevents AI errors from entering ground truth. | *In a simulated HITL labeling pipeline with human anchoring bias (WoA $\alpha$) and 15% manual fatigue noise, how much does confidence-thresholded blind review improve final dataset Cohen's $\kappa$ and downstream accuracy compared to showing AI pre-labels on all items?* | Simulate 3 review protocols across 5 seeds; measure final label Cohen's $\kappa$ against clean truth and downstream classifier Macro-F1. |
| **Gap 5:** Soft Probabilistic Label Training vs. Hard Majority Voting Under High Rater Disagreement | Sec. II-A & II-B (p. 1–2, Refs [1, 2]) show that clinical experts often disagree (11 ICU doctors had Fleiss' $\kappa = 0.383$ internally and $\kappa = 0.255$ externally [2]), and Chew et al. [1] warn that majority voting hides valid case ambiguity. | Training a classifier on soft label probabilities (or Dawid-Skene posteriors) instead of hard majority vote on low-agreement data ($\kappa \approx 0.38$) should improve model calibration (ECE) and performance on ambiguous cases. | *On a multi-annotator dataset with low inter-annotator agreement (Fleiss' $\kappa < 0.45$), does training on soft rater probability distributions improve Expected Calibration Error (ECE), Brier score, and Macro-F1 compared to hard majority voting?* | Compare Hard Majority Vote, Dawid-Skene, and Soft Cross-Entropy training across 5 seeds; evaluate Macro-F1, ECE, and Brier score. |

---

## 5. Top 3 Ranked Gaps by Significance, Resources & Feasibility

1. **Rank #1 (Most Practical): Gap 2 (with Gap 3)** — *Comparing ActiveAED (AUM), Confident Learning, and Entropy for Label Error Cleaning under Fixed Review Budgets.*
   - **Significance:** High (directly tests the core purification loop shown in Fig. 1 and Fig. 2 of my review [21, 23, 71]).
   - **Resources & Feasibility:** Very High (uses open-source `cleanlab` and PyTorch AUM on MedMNIST / PBMC3k; runs in 1–2 hours on a single Google Colab T4 GPU across 5 seeds).
2. **Rank #2 (Best for Medical Vision): Gap 1** — *Bounding-Box Prompt Jitter Sensitivity & Margin Padding in MedSAM vs. Zero-Shot SAM.*
   - **Significance:** High (directly addresses the clinical limitation in Sec. III-A [6, 7, 8] where clinicians cannot draw pixel-perfect boxes).
   - **Resources & Feasibility:** High (inference-only experiment using official `SAM` and `MedSAM` weights on 2D Chest X-ray TB [11] or CRAG [8] images; takes ~1 hour on Colab GPU).
3. **Rank #3 (Best for Theory / HLV): Gap 5** — *Soft Probabilistic Labels vs. Hard Majority Voting under Low Rater Agreement ($\kappa \approx 0.38$).*
   - **Significance:** Medium-High (directly tests the HLV framework in Sec. II-A [1, 2]).
   - **Resources & Feasibility:** Very High (fast training in PyTorch/scikit-learn; clean calibration plots for ECE, Brier score, and Macro-F1).

> **Disclaimer on Novelty (Prompt 02 Requirement):** These five candidate gaps and top-three rankings represent computationally testable problems derived from the limitations reported in my literature review. No claim of publication-level novelty is made at this stage without conducting a separate, dedicated literature search.