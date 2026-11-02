# Research Gap Matrix

**Project:** Comparative Analysis of AI-Assisted and Manual Data Labeling Accuracy Across Scientific Datasets
**Source analysed:** the attached literature review (section, table and reference numbers below are as printed in it)

**Tags:** VERIFIED = read in the review text. INFERRED = my reasoning from that text. UNKNOWN = not yet checked against the original publications.
**Novelty:** no novelty is claimed for any gap. A separate literature search is required first.

---

## 1. Gap matrix

| ID | Gap | Passage / reference in the review | Reported in the review (VERIFIED) | Inference (INFERRED) | Experimental question | Evidence that would test it |
|----|-----|-----------------------------------|-----------------------------------|----------------------|-----------------------|-----------------------------|
| G1 | Matched comparison of AI-assisted vs manual labels against a common reference | Sec. III-A, Table II; workflow studies [9], [10], [11], [13] | Table II mostly reports model-vs-reference Dice. The workflow studies each use a different outcome: time and variability [9], Likert grade [10], Dice and time [11], error rate [13]. | The review does not show accuracy of an AI-assisted workflow vs a manual workflow on the same items with the same reference. | On a dataset with an adjudicated reference and several independent annotations, how does agreement with the reference differ between manual labels, model-only labels, and model pre-labels with correction? What does each cost in effort? | Dice/IoU or kappa vs the reference with paired bootstrap confidence intervals; time or query count as cost. Correction step is a human study or a simulation (a weaker proxy). |
| G2 | Size of the anchoring effect, and when it reverses the benefit of AI assistance | Sec. VI-B [19], [20]; Table III (mitigations) | Sec. VI-B describes a paradox of AI accuracy and complacency and the Weight of Advice. Table III lists synthetic-error injection and blind review, uncited. | No effect size is given and the mitigations are untested. | Over a grid of AI accuracy and advice-weighting values, where does assisted accuracy fall below manual accuracy? Does synthetic-error injection move that point? | Simulation sweep with parameters taken from empirical sources (candidates: [19], [20], [63]). Without empirical parameters it only restates assumptions. |
| G3 | Budgeted uncertainty-driven review vs simple baselines | Sec. III-C [11]; Sec. VII-A [22]; Sec. VIII | [11] reports a Dice gain of about 0.01 with large time savings. [22] reports up to a 99% budget reduction, from a conflict-text corpus. The conclusion says the optimal strategy relies heavily on active and confident learning. | The body gives no comparison against random or fixed-fraction review, and one text-domain result supports a general claim. | Under a fixed correction budget, does uncertainty-based routing beat random routing and fixed-fraction review on final label accuracy, across more than one domain? | Budget-vs-accuracy curves over several seeds with confidence intervals, using existing ground truth as the oracle. |
| G4 | Systematic AI-style label errors vs random manual-style errors | Table III; Sec. VII-B; Introduction [1] | Table III says automation bias encodes AI hallucination systematically into ground truth. Sec. VII-B presents Confident Learning as a way to find label errors. | No detection precision or recall is reported, and it is not tested whether detectors built for random noise catch errors correlated with a model's mistakes. | Do Confident-Learning-style detectors find model-correlated label errors as well as random errors at the same rate? How does each noise type affect downstream accuracy? | Inject both noise types into a benchmark; report detection precision and recall and downstream accuracy over several seeds. |
| G5 | Whether reported gains exceed the human noise floor | Sec. II-B; Sec. III-A [8]; Sec. III-C [11]; [27] (listed, never cited) | Quoted gaps are small: HybridMS +0.0103 Dice [11]; GB-SAM +0.028 over U-Net [8]. | The review never compares these gaps with the spread between human annotators. | On multi-annotator segmentation data, how large are annotator-to-annotator Dice differences, and do model differences of the reported size fall inside that range? | Pairwise annotator Dice distribution with bootstrap intervals on model differences. |

---

## 2. Methods, datasets and limitations (basis for the gaps)

**Central methods (VERIFIED).** Agreement metrics: Cohen's kappa, Fleiss' kappa, Krippendorff's alpha, STAPLE, Dice, IoU (Sec. II). AI-assisted segmentation: zero-shot SAM, MedSAM, GB-SAM, SAM-assisted annotation, AICL, HybridMS (Sec. III). Supervised baseline: nnU-Net. Text and omics: LLM and multi-agent cell-type annotation (Sec. IV-A); Octozi data cleaning (Sec. IV-B). Astronomy: Zoobot, YOLOv5, VLM/VQA (Sec. V-A). Label-noise control: uncertainty-based active learning, ActiveAED/AUM, Confident Learning (Sec. VII).

**Datasets (VERIFIED as named; label availability UNKNOWN).** Named: BraTS 2023 [7], CRAG [8], Galaxy Zoo [14], Pan-STARRS [16]. Described only: lumbar spine MRI [6], whole-slide pathology pilot [9], CT hemorrhage [10], tuberculosis chest X-ray [11], 34 scRNA-seq datasets [12], ICU consultant data [2], clinical-trial cleaning study [13].

**Limitations.** The review has no limitations section of its own and states no search protocol, research questions or experiments (VERIFIED). The limitations it reports are of the studied methods: zero-shot SAM domain gap [4]; SAM needs precise box prompts [7]; nnU-Net needs large labeled sets (Table II); subjective manual scRNA-seq annotation [12]; error-prone manual cleaning [13]; crowdsourcing cannot scale [14]; majority voting hides disagreement [1]; no single super expert [2]; fatigue [17], [18]; anchoring and complacency [19], [20]; residual label noise (Sec. VII-B); AI assistance is "not a panacea" (Sec. VIII).

**Unresolved (VERIFIED).** Out-of-distribution shift is named in the Introduction and in the Sec. VII heading, but no analysis follows; [76]-[79] are never cited. **Unresolved (INFERRED).** No common accuracy measure across domains, no uncertainty on quoted gaps, no measured size of automation bias.

---

## 3. Ranking of three gaps

Resources are UNKNOWN. Scores (1-5, higher is better) are provisional (INFERRED), assuming public datasets, modest compute and no human-annotator recruitment.

| Rank | Gap | Significance | Resources | Feasibility | Total | Rationale |
|------|-----|--------------|-----------|-------------|-------|-----------|
| 1 | G3 | 4 | 5 | 5 | 14 | Tests the review's own conclusion; runs on small public datasets. |
| 2 | G4 | 4 | 4 | 4 | 12 | Tests an uncited claim using noise injection and standard code. |
| 3 | G1 | 5 | 3 | 3 | 11 | Matches the title's question; depends on a dataset with per-annotator labels (not checked). Ties G5 on total; ranked higher on significance. |

Not ranked: G5 (11) and G2 (9). G5 can be folded into the G1 evaluation as its noise-floor measure. G2 needs verified empirical parameters first.

---

## 4. Claims to verify against the original publications

| Ref | Check |
|-----|-------|
| [9] | 29.9 vs 13.6 min and 24% vs 2% variability; number of annotators and slides; the reference title calls it a pilot. |
| [11] | Whether the 0.0103 Dice gain is tested, and against which baseline. |
| [13] | Error rates, unit of cleaning error, 6.03x throughput. |
| [10] | What graders rated, whether blinded; the review's explanation that AI uncovers boundary details hidden by fatigue is untested in its text. |
| [22] | Whether the 99% figure is from this paper and generalizes beyond conflict text corpora. |
| [2] | Kappa 0.383 and 0.255; eleven consultants. |
| [6], [7], [8] | Dice values; that nnU-Net 0.99 is lumbar only. |
| [19], [20], [63] | Whether they report anchoring effect sizes usable for G2. |
| ActiveAED / AUM | Cited as [23] in the text; the list has it at [71]. Confirm source and claim. |
| Confident Learning | Cited as [21], a retinal-image application. Check whether the originating paper is in the list. |
| Uncited items | Oral-lesion kappa 0.90; "substantial label noise in curated benchmarks"; Sec. V-A VLM/VQA statement. |

All numbers the review attributes to its sources are UNKNOWN until confirmed in the originals.
