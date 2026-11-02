# Research workflow: from literature review to executable experiment

Each folder holds the markdown source and the PDF of one stage. Evidence tags used throughout: **VERIFIED** (read or run, output saved), **INFERRED** (reasoning stated), **UNKNOWN** (check named).

| Stage | Folder | What it contains | Status |
|-------|--------|------------------|--------|
| Prompt 1 | [`prompt-01-gap-matrix`](prompt-01-gap-matrix/) | Gap matrix G1-G5 from the review, ranking, claims to verify | Done |
| Prompt 2 | [`prompt-02-research-decisions`](prompt-02-research-decisions/) | Source audit (E1-E15), claim register, decision log D-001 to D-007 | Done |
| Prompt 3 | [`prompt-03-literature-to-experiment`](prompt-03-literature-to-experiment/) | Three methods mapped to papers, code and data access; Studies A/B/C; MVE recommendation; checks to verify before coding | Done |
| Prompt 4 | [`prompt-04-feasibility-novelty`](prompt-04-feasibility-novelty/) | Search strings, novelty matrix, resource-access check, go/no-go, fallbacks | Done; novelty searches not yet run |
| Phase II | [`phase-2-experiment-plan`](phase-2-experiment-plan/) | Pre-specified protocol: hypotheses, arms, reference rule, statistics, validation gates | Done |
| Phase III | [`phase-3-coding-baseline-validation`](phase-3-coding-baseline-validation/) | AI-coding log, 8 validation gates, label-only baseline on real CIFAR-10H | Done except the model arm |

Code: [`experiments/study_b_review_routing`](../experiments/study_b_review_routing/).

**Not yet done:** the model arm on CIFAR-10 images (needs one run outside the authoring workspace), the novelty searches S1-S5, and the manuscript.
