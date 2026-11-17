import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from routing import uncertainty_scores, select_for_review, final_labels, draw_single_annotator
from stats import paired_bootstrap_ci
from experiment import run_experiment, ARMS


def approx(x, tol=1e-12):
    class A:
        def __eq__(self, o): return abs(o - x) <= tol
    return A()


def toy():
    # 4 items, 3 classes; known uncertainty ordering
    P = np.array([[0.98, 0.01, 0.01],    # most confident
                  [0.50, 0.45, 0.05],    # margin 0.05, entropy ~0.86
                  [0.34, 0.33, 0.33],    # max entropy
                  [0.70, 0.20, 0.10]])  # margin 0.50, entropy ~0.80
    return P


def test_entropy_order_known():
    s = uncertainty_scores(toy(), "entropy")
    assert np.argmax(s) == 2 and np.argmin(s) == 0


def test_margin_order_known():
    s = uncertainty_scores(toy(), "margin")
    assert np.argmax(s) == 2          # margin 0.01
    assert np.argmin(s) == 0


def test_least_conf_order_known():
    s = uncertainty_scores(toy(), "least_confidence")
    assert np.argmax(s) == 2 and np.argmin(s) == 0


def test_select_top_uncertain():
    rng = np.random.default_rng(0)
    idx = select_for_review(toy(), np.zeros(4, int), 2, "entropy", rng)
    assert set(idx) == {2, 1}


def test_select_sizes_and_unique():
    P = np.random.default_rng(1).dirichlet(np.ones(5), 200)
    y = P.argmax(1)
    for arm in ARMS:
        idx = select_for_review(P, y, 37, arm, np.random.default_rng(2))
        assert len(idx) == 37 and len(set(idx)) == 37


def test_oracle_reviews_errors_first():
    P = np.array([[0.9, 0.1], [0.9, 0.1], [0.1, 0.9], [0.1, 0.9]])
    y = np.array([1, 0, 1, 1])          # items 0 and 1: pred 0; item 0 wrong (y=1), item 1 right
    idx = select_for_review(P, y, 1, "oracle", np.random.default_rng(0))
    assert list(idx) == [0]


def test_tie_breaking_is_random_but_seeded():
    P = np.tile([0.5, 0.5], (50, 1))
    a = select_for_review(P, np.zeros(50, int), 10, "entropy", np.random.default_rng(5))
    b = select_for_review(P, np.zeros(50, int), 10, "entropy", np.random.default_rng(5))
    c = select_for_review(P, np.zeros(50, int), 10, "entropy", np.random.default_rng(6))
    assert list(a) == list(b) and list(a) != list(c)


def test_final_labels():
    out = final_labels(np.array([0, 0, 0]), np.array([1]), np.array([9, 9, 9]))
    assert list(out) == [0, 9, 0]


def test_draw_single_annotator_uses_valid_slots():
    M = np.array([[3, 4, -1], [7, -1, -1]])
    n = np.array([2, 1])
    rng = np.random.default_rng(0)
    for _ in range(200):
        d = draw_single_annotator(M, n, rng)
        assert d[0] in (3, 4) and d[1] == 7


def _synthetic(N=2000, C=5, seed=0):
    rng = np.random.default_rng(seed)
    y = rng.integers(0, C, N)
    logits = rng.normal(size=(N, C)); logits[np.arange(N), y] += 1.5
    P = np.exp(logits); P /= P.sum(1, keepdims=True)
    # annotator judgments: 20 per item, 90% correct
    J = 20
    M = np.where(rng.random((N, J)) < 0.9, y[:, None], rng.integers(0, C, (N, J)))
    n = np.full(N, J)
    return P, y, M, n


def test_gate_G2_oracle_closed_form_perfect_reviewer():
    P, y, M, n = _synthetic()
    res = run_experiment([P], y, M, n, budgets=(0.1, 0.4))
    N = len(y); E = int((P.argmax(1) != y).sum())
    for b in (0.1, 0.4):
        k = int(round(b * N))
        expect = 1 - max(E - k, 0) / N
        assert res[("perfect", "oracle", b)].mean() == approx(expect)


def test_gate_G3_full_budget_perfect_is_one():
    P, y, M, n = _synthetic()
    res = run_experiment([P], y, M, n, budgets=(1.0,))
    for a in ARMS:
        assert res[("perfect", a, 1.0)].mean() == 1.0


def test_gate_H1_entropy_beats_random_perfect_reviewer_synthetic():
    P, y, M, n = _synthetic()
    res = run_experiment([P, P, P], y, M, n, budgets=(0.2,))
    assert res[("perfect", "entropy", 0.2)].mean() > res[("perfect", "random", 0.2)].mean()


def test_random_arm_perfect_reviewer_gain_near_expected():
    P, y, M, n = _synthetic(N=4000)
    S = 20
    res = run_experiment([P] * S, y, M, n, budgets=(0.2,))
    base = res[("none",)].mean()
    gain = res[("perfect", "random", 0.2)].mean() - base
    expected = 0.2 * (1 - base)                 # fraction of errors caught at random
    assert abs(gain - expected) < 0.01


def test_gate_G5_bootstrap_known_difference_and_null():
    rng = np.random.default_rng(0)
    d = (rng.random(5000) < 0.6).astype(float) - (rng.random(5000) < 0.5).astype(float)
    m, lo, hi = paired_bootstrap_ci(d, n_boot=1000, seed=1)
    assert lo < 0.1 < hi and lo > 0                # true diff 0.1, interval excludes 0
    z = np.zeros(5000)
    m, lo, hi = paired_bootstrap_ci(z, n_boot=500, seed=1)
    assert lo == 0 and hi == 0
    d0 = (rng.random(5000) < 0.5).astype(float) - (rng.random(5000) < 0.5).astype(float)
    m, lo, hi = paired_bootstrap_ci(d0, n_boot=1000, seed=1)
    assert lo < 0 < hi


def test_gate_G6_determinism():
    P, y, M, n = _synthetic()
    a = run_experiment([P, P], y, M, n, budgets=(0.2,))
    b = run_experiment([P, P], y, M, n, budgets=(0.2,))
    for k in a:
        assert np.array_equal(a[k], b[k])
