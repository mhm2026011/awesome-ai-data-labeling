"""Label-only baseline: reconcile raw file with counts.npy, manual arm, noise floor, reference sensitivity."""
import argparse, json, sys, pathlib
import numpy as np, pandas as pd
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from labels import load_raw, attention_accuracy, build_judgments, counts_from_judgments, reference_labels, N_ITEMS
from routing import draw_single_annotator

ap = argparse.ArgumentParser(); ap.add_argument("--c10h", default="data_c10h"); ap.add_argument("--out", default="results")
_a = ap.parse_args(); D = pathlib.Path(_a.c10h); OUT = pathlib.Path(_a.out); OUT.mkdir(exist_ok=True)
df = load_raw(D / "raw" / "cifar10h-raw.csv")
counts_ref = np.load(D / "cifar10h-counts.npy").astype(int)
out = {}

print("rows", len(df), "attention rows", int(df.is_attn_check.sum()), "idx range", df.cifar10_test_test_idx.min(), df.cifar10_test_test_idx.max())
att = attention_accuracy(df)
out["attention"] = dict(n_annotators_with_checks=int(att.size), n_below_75=int((att < 0.75).sum()),
                        min=float(att.min()), median=float(att.median()))
excl = att.index[att < 0.75].tolist()
print("annotators with attention acc < 0.75:", len(excl))

# G-4: which exclusion rule reproduces counts.npy exactly?
variants = {"no_exclusion": [], "exclude_attn_below_75": excl}
recon = {}
for name, ex in variants.items():
    M, n = build_judgments(df, ex)
    C = counts_from_judgments(M)
    recon[name] = dict(exact_match=bool((C == counts_ref).all()), items_differing=int((C != counts_ref).any(1).sum()),
                       total_judgments=int(n.sum()), n_min=int(n.min()), n_max=int(n.max()))
    print(name, recon[name])
out["reconciliation"] = recon
out["counts_npy_total"] = int(counts_ref.sum())

use = "exclude_attn_below_75" if recon["exclude_attn_below_75"]["exact_match"] else ("no_exclusion" if recon["no_exclusion"]["exact_match"] else None)
out["rule_that_reproduces_counts"] = use
if use is None:
    json.dump(out, open(OUT / "label_only.json", "w"), indent=2)
    print("G-4 FAILED: no rule reproduces counts.npy; stopping."); sys.exit(2)

M, n = build_judgments(df, variants[use])
y = reference_labels(df)
assert (y >= 0).all()
plur = counts_ref.argmax(1)
ties = int(((counts_ref == counts_ref.max(1, keepdims=True)).sum(1) > 1).sum())
out["reference"] = dict(plurality_equals_original=float((plur == y).mean()), n_disagree=int((plur != y).sum()), plurality_ties=ties)

# manual arm: one random judgment per item, 1000 draws
accs_o, accs_p = [], []
for s in range(1000):
    d = draw_single_annotator(M, n, np.random.default_rng([7, s]))
    accs_o.append((d == y).mean()); accs_p.append((d == plur).mean())
q = lambda a: dict(mean=float(np.mean(a)), sd=float(np.std(a, ddof=1)), p2_5=float(np.percentile(a, 2.5)), p97_5=float(np.percentile(a, 97.5)))
out["manual_single_draw_vs_original"] = q(accs_o); out["manual_single_draw_vs_plurality"] = q(accs_p)

# panel majority vs original
out["panel_plurality_acc_vs_original"] = float((plur == y).mean())

# noise floor: per-annotator accuracy vs original label over items they labelled
d = df[(df.is_attn_check == 0) & (~df.annotator_id.isin(variants[use])) & (df.cifar10_test_test_idx >= 0)]
pa = d.assign(ok=(d.chosen_label == d.true_label)).groupby("annotator_id").agg(acc=("ok", "mean"), n=("ok", "size"))
out["per_annotator"] = dict(n_annotators=int(len(pa)), items_per_annotator_min=int(pa.n.min()), items_per_annotator_median=float(pa.n.median()),
                            items_per_annotator_max=int(pa.n.max()), acc_mean=float(pa.acc.mean()), acc_sd=float(pa.acc.std(ddof=1)),
                            acc_p5=float(pa.acc.quantile(.05)), acc_p50=float(pa.acc.median()), acc_p95=float(pa.acc.quantile(.95)))
# per-item single-label accuracy (how often a random judgment is right) and items with low agreement
item_acc = np.array([(M[i, :n[i]] == y[i]).mean() for i in range(N_ITEMS)])
out["item_level"] = dict(mean=float(item_acc.mean()), items_below_50pct=int((item_acc < .5).sum()), items_below_80pct=int((item_acc < .8).sum()), items_all_correct=int((item_acc == 1).sum()))
json.dump(out, open(OUT / "label_only.json", "w"), indent=2)
pa.to_csv(OUT / "per_annotator_accuracy.csv")
np.save(OUT / "item_accuracy_single_judgment.npy", item_acc)
print(json.dumps({k: out[k] for k in out if k not in ("attention", "reconciliation")}, indent=2))
