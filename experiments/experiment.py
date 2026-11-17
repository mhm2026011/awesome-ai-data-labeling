"""Run all arms x budgets x reviewers x seeds from per-seed probability matrices."""
import numpy as np
from routing import SCORE_KINDS, select_for_review, final_labels, draw_single_annotator
from stats import paired_bootstrap_ci

ARMS = ("random",) + SCORE_KINDS + ("oracle",)
REVIEWERS = ("perfect", "single")


def run_experiment(probs_by_seed, y_ref, M, n, budgets=(0.05, 0.10, 0.20, 0.40), seed_base=1000):
    """Returns dict with per-item correctness arrays, shape (S, N) bool:
    res[('none',)], res[('manual',)], res[(reviewer, arm, b)]."""
    y_ref = np.asarray(y_ref)
    N = len(y_ref)
    S = len(probs_by_seed)
    res = {("none",): np.zeros((S, N), bool), ("manual",): np.zeros((S, N), bool)}
    for r in REVIEWERS:
        for a in ARMS:
            for b in budgets:
                res[(r, a, b)] = np.zeros((S, N), bool)
    for s, P in enumerate(probs_by_seed):
        pred = P.argmax(axis=1)
        rng_draw = np.random.default_rng([seed_base, s, 1])
        single = draw_single_annotator(M, n, rng_draw)        # shared by all arms in this seed
        reviewer_labels = {"perfect": y_ref, "single": single}
        res[("none",)][s] = pred == y_ref
        res[("manual",)][s] = single == y_ref
        for b in budgets:
            k = int(round(b * N))
            for a in ARMS:
                # same rng stream per (seed, arm, budget) so reruns are identical
                rng_sel = np.random.default_rng([seed_base, s, 2, ARMS.index(a), int(round(b * 1000))])
                idx = select_for_review(P, y_ref, k, a, rng_sel)
                for r in REVIEWERS:
                    fin = final_labels(pred, idx, reviewer_labels[r])
                    res[(r, a, b)][s] = fin == y_ref
    return res


def summarise(res, budgets, n_boot=2000, seed=0):
    """Table rows: accuracy (mean over seeds, seed min/max) and paired difference vs random."""
    rows = []
    base = res[("none",)]
    rows.append(dict(reviewer="-", arm="none", budget=0.0, acc=float(base.mean()),
                     seed_min=float(base.mean(1).min()), seed_max=float(base.mean(1).max())))
    man = res[("manual",)]
    rows.append(dict(reviewer="-", arm="manual", budget=1.0, acc=float(man.mean()),
                     seed_min=float(man.mean(1).min()), seed_max=float(man.mean(1).max())))
    for (key, arr) in res.items():
        if len(key) != 3:
            continue
        r, a, b = key
        accs = arr.mean(1)
        row = dict(reviewer=r, arm=a, budget=b, acc=float(accs.mean()),
                   seed_min=float(accs.min()), seed_max=float(accs.max()))
        if a != "random":
            d = arr.mean(0) - res[(r, "random", b)].mean(0)           # seed-averaged, per item
            m, lo, hi = paired_bootstrap_ci(d, n_boot=n_boot, seed=seed)
            row.update(diff_vs_random=m, ci_lo=lo, ci_hi=hi)
        d0 = arr.mean(0) - base.mean(0)
        m0, lo0, hi0 = paired_bootstrap_ci(d0, n_boot=n_boot, seed=seed)
        row.update(diff_vs_none=m0, ci0_lo=lo0, ci0_hi=hi0)
        rows.append(row)
    return rows
