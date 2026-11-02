"""Review-routing arms for Study B. Pure numpy; no data access.

Conventions: P is an (N, C) probability matrix, y_ref the (N,) reference labels.
Higher uncertainty score = more uncertain = reviewed first.
"""
import numpy as np

SCORE_KINDS = ("entropy", "margin", "least_confidence")


def uncertainty_scores(P, kind):
    P = np.asarray(P, dtype=float)
    if kind == "entropy":
        return -(P * np.log(np.clip(P, 1e-12, 1.0))).sum(axis=1)
    if kind == "margin":
        s = np.sort(P, axis=1)
        return -(s[:, -1] - s[:, -2])
    if kind == "least_confidence":
        return -P.max(axis=1)
    raise ValueError(f"unknown score kind: {kind}")


def select_for_review(P, y_ref, k, arm, rng):
    """Indices of the k items sent to review. Ties are broken at random (rng)."""
    n = P.shape[0]
    if not 0 <= k <= n:
        raise ValueError("k must be in [0, N]")
    if arm == "none" or k == 0:
        return np.array([], dtype=int)
    tiebreak = rng.random(n)
    if arm == "random":
        return rng.permutation(n)[:k]
    if arm in SCORE_KINDS:
        key = uncertainty_scores(P, arm)
    elif arm == "oracle":
        key = (P.argmax(axis=1) != np.asarray(y_ref)).astype(float)
    else:
        raise ValueError(f"unknown arm: {arm}")
    order = np.lexsort((tiebreak, -key))  # primary: -key (desc), secondary: random
    return order[:k]


def final_labels(pred, reviewed_idx, reviewer_labels):
    out = np.array(pred, copy=True)
    out[reviewed_idx] = np.asarray(reviewer_labels)[reviewed_idx]
    return out


def draw_single_annotator(M, n, rng):
    """One judgment per item drawn uniformly from that item's judgments.
    M: (N, J) padded with -1; n: (N,) number of valid judgments per item."""
    j = np.floor(rng.random(M.shape[0]) * n).astype(int)
    return M[np.arange(M.shape[0]), j]
