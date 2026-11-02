"""Load CIFAR-10H raw annotator data and rebuild per-item judgments."""
import numpy as np
import pandas as pd

N_ITEMS, N_CLASSES = 10000, 10


def load_raw(csv_path):
    return pd.read_csv(csv_path)


def attention_accuracy(df):
    a = df[df.is_attn_check == 1]
    return a.groupby("annotator_id").correct_guess.mean()


def build_judgments(df, excluded_annotators=()):
    """Return (M, n): M (N,J) padded with -1, n (N,) counts. Attention-check
    trials and excluded annotators removed."""
    d = df[(df.is_attn_check == 0) & (~df.annotator_id.isin(list(excluded_annotators)))]
    d = d[(d.cifar10_test_test_idx >= 0) & (d.cifar10_test_test_idx < N_ITEMS)]
    d = d.sort_values(["cifar10_test_test_idx", "annotator_id", "trial_index"])
    n = np.bincount(d.cifar10_test_test_idx.values, minlength=N_ITEMS)
    J = int(n.max())
    M = -np.ones((N_ITEMS, J), dtype=int)
    pos = d.groupby("cifar10_test_test_idx").cumcount().values
    M[d.cifar10_test_test_idx.values, pos] = d.chosen_label.values
    return M, n


def counts_from_judgments(M):
    C = np.zeros((M.shape[0], N_CLASSES), dtype=int)
    for c in range(N_CLASSES):
        C[:, c] = (M == c).sum(axis=1)
    return C


def reference_labels(df):
    """Original CIFAR-10 test label per item, from the raw file's true_label."""
    d = df[(df.is_attn_check == 0) & (df.cifar10_test_test_idx >= 0)]
    g = d.groupby("cifar10_test_test_idx").true_label.agg(["min", "max"])
    if (g["min"] != g["max"]).any():
        raise ValueError("true_label is inconsistent within an item")
    y = np.full(N_ITEMS, -1, dtype=int)
    y[g.index.values] = g["min"].values
    return y
