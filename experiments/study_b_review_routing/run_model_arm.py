"""Study B model arm. Input: features npz with Xtr, ytr, Xte, yte (CIFAR-10 train / test in ORIGINAL order).
Usage: python run_model_arm.py --features feats.npz --c10h /path/to/data_c10h --out results_dir [--seeds 10] [--boot 2000]
Gate G-8: yte must equal the CIFAR-10 test labels stored in the CIFAR-10H raw file; otherwise stop."""
import argparse, json, pathlib, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from labels import load_raw, attention_accuracy, build_judgments, counts_from_judgments, reference_labels
from model import choose_C, probs_by_seed, expected_calibration_error
from experiment import run_experiment, summarise
from report_tables import rows_to_df

BUDGETS = (0.05, 0.10, 0.20, 0.40)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--features", required=True); ap.add_argument("--c10h", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, default=10); ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args(); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    c10h = pathlib.Path(a.c10h)
    f = np.load(a.features); Xtr, ytr, Xte, yte = f["Xtr"], f["ytr"], f["Xte"], f["yte"]
    df = load_raw(c10h / "raw" / "cifar10h-raw.csv")
    counts_ref = np.load(c10h / "cifar10h-counts.npy").astype(int)
    att = attention_accuracy(df); excl = att.index[att < 0.75].tolist()
    M, n = build_judgments(df, excl)
    assert (counts_from_judgments(M) == counts_ref).all(), "G-4 failed: raw file does not reproduce counts.npy"
    y_orig = reference_labels(df)
    assert len(yte) == len(y_orig) and (yte == y_orig).all(), "G-8 failed: feature test labels differ from CIFAR-10H true_label"
    plur = counts_ref.argmax(1)
    t0 = time.time(); C, grid = choose_C(Xtr, ytr); print("chosen C", C, grid, f"{time.time()-t0:.0f}s")
    t0 = time.time(); P = probs_by_seed(Xtr, ytr, Xte, range(a.seeds), C); print(f"trained {a.seeds} seeds in {time.time()-t0:.0f}s")
    summary = dict(C=C, C_grid_val_acc=grid, ece_seed0=expected_calibration_error(P[0], y_orig),
                   model_acc_per_seed=[float((p.argmax(1) == y_orig).mean()) for p in P])
    for tag, ref in (("primary_original_label", y_orig), ("sensitivity_human_plurality", plur)):
        res = run_experiment(P, ref, M, n, BUDGETS)
        t = rows_to_df(summarise(res, BUDGETS, n_boot=a.boot)); t.to_csv(out / f"results_{tag}.csv", index=False)
        print("\n==", tag); print(t[t.budget.isin([0.0, 0.2, 1.0])].round(4).to_string(index=False))
    json.dump(summary, open(out / "model_summary.json", "w"), indent=2); print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
