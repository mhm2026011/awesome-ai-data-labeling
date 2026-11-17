"""Classifier on cached features: hyperparameter choice on a held-out split of the TRAIN set, then
per-seed training on a random 80% of the train set. The test set is never touched here."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


def choose_C(Xtr, ytr, grid=(0.01, 0.1, 1.0), val_frac=0.2, seed=0, max_iter=300):
    rng = np.random.default_rng([seed, 99])
    perm = rng.permutation(len(ytr)); nv = int(len(ytr) * val_frac)
    va, tr = perm[:nv], perm[nv:]
    sc = StandardScaler().fit(Xtr[tr])
    best, best_acc, table = None, -1, {}
    for C in grid:
        clf = LogisticRegression(C=C, max_iter=max_iter).fit(sc.transform(Xtr[tr]), ytr[tr])
        acc = float((clf.predict(sc.transform(Xtr[va])) == ytr[va]).mean()); table[C] = acc
        if acc > best_acc: best, best_acc = C, acc
    return best, table


def probs_by_seed(Xtr, ytr, Xte, seeds, C, frac=0.8, max_iter=300):
    out = []
    for s in seeds:
        rng = np.random.default_rng([s, 5])
        idx = rng.permutation(len(ytr))[: int(frac * len(ytr))]
        sc = StandardScaler().fit(Xtr[idx])
        clf = LogisticRegression(C=C, max_iter=max_iter).fit(sc.transform(Xtr[idx]), ytr[idx])
        P = np.zeros((Xte.shape[0], int(ytr.max()) + 1))
        P[:, clf.classes_] = clf.predict_proba(sc.transform(Xte))
        out.append(P)
    return out


def expected_calibration_error(P, y, bins=15):
    conf = P.max(1); correct = (P.argmax(1) == y).astype(float)
    edges = np.linspace(0, 1, bins + 1); ece = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        m = (conf > lo) & (conf <= hi)
        if m.any(): ece += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(ece)
