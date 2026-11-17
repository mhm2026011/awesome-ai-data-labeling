"""Gate G-7: end-to-end pipeline check on scikit-learn's bundled digits (no download).
NOT a Study B result. Reviewer judgments are SYNTHETIC (20 per item, each correct with prob 0.9,
otherwise a uniformly random class) so that the 'single annotator' path can be exercised."""
import sys, pathlib, json, os
import numpy as np
from sklearn.datasets import load_digits
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from model import choose_C, probs_by_seed, expected_calibration_error
from experiment import run_experiment, summarise
from report_tables import rows_to_df

X, y = load_digits(return_X_y=True)
rng = np.random.default_rng(0); perm = rng.permutation(len(y)); half = len(y) // 2
tr, te = perm[:half], perm[half:]
C, table = choose_C(X[tr], y[tr], grid=(0.001, 0.01, 0.1), max_iter=500)
P = probs_by_seed(X[tr], y[tr], X[te], seeds=range(10), C=C, max_iter=500)
yte = y[te]; N = len(yte)
rr = np.random.default_rng(1)
M = np.where(rr.random((N, 20)) < 0.9, yte[:, None], rr.integers(0, 10, (N, 20))); n = np.full(N, 20)
res = run_experiment(P, yte, M, n, budgets=(0.05, 0.10, 0.20, 0.40))
rows = summarise(res, (0.05, 0.10, 0.20, 0.40), n_boot=500)
df = rows_to_df(rows)
OUT = pathlib.Path(os.environ.get("STUDY_B_OUT", "results")); OUT.mkdir(exist_ok=True)
df.to_csv(OUT / "validate_digits.csv", index=False)
print("chosen C", C, table); print("test items", N, "model-only acc", round(df[df.arm == "none"].acc.iloc[0], 4),
      "ECE", round(expected_calibration_error(P[0], yte), 4))
print(df[df.budget.isin([0.2])][["reviewer", "arm", "budget", "acc", "diff_vs_random", "ci_lo", "ci_hi"]].round(4).to_string(index=False))
# gate checks
base = 1 - ((np.stack([p.argmax(1) for p in P]) != yte).mean(1))     # per-seed baseline accuracy
for b in (0.05, 0.10, 0.20, 0.40):
    k = int(round(b * N)); E = (np.stack([p.argmax(1) for p in P]) != yte).sum(1)
    expect = (1 - np.maximum(E - k, 0) / N).mean()
    got = float(res[("perfect", "oracle", b)].mean())
    assert abs(expect - got) < 1e-12, (b, expect, got)
print("G-2 closed form holds on digits for all budgets")
