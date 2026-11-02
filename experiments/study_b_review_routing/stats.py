"""Paired bootstrap over items."""
import numpy as np


def paired_bootstrap_ci(d, n_boot=2000, alpha=0.05, seed=0, chunk=200):
    """d: (N,) per-item difference (arm A correct minus arm B correct, seed-averaged).
    Returns (mean, lo, hi) percentile interval of the resampled mean."""
    d = np.asarray(d, dtype=float)
    n = d.shape[0]
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot)
    for s in range(0, n_boot, chunk):
        m = min(chunk, n_boot - s)
        idx = rng.integers(0, n, size=(m, n))
        means[s:s + m] = d[idx].mean(axis=1)
    lo, hi = np.percentile(means, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(d.mean()), float(lo), float(hi)
