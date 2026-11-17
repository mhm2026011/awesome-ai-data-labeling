"""Build fallback features from CIFAR-10 python batches (safe loader) and run the Study B model arm.
Usage: python run_fallback.py --cifar DIR --c10h DIR --out DIR [--seeds 10] [--boot 2000]"""
import argparse, pathlib, subprocess, sys, time
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from load_cifar10_safe import load_cifar10
from features_fallback import hog_color_features

ap = argparse.ArgumentParser()
ap.add_argument("--cifar", required=True); ap.add_argument("--c10h", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--seeds", type=int, default=10); ap.add_argument("--boot", type=int, default=2000)
a = ap.parse_args(); out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
Xtr, ytr, Xte, yte, _ = load_cifar10(a.cifar)
t0 = time.time(); Ftr = hog_color_features(Xtr); Fte = hog_color_features(Xte)
print(f"features {Ftr.shape} {Fte.shape} in {time.time()-t0:.0f}s")
np.savez_compressed(out / "feats_fallback.npz", Xtr=Ftr, ytr=ytr, Xte=Fte, yte=yte)
subprocess.run([sys.executable, "-I", str(pathlib.Path(__file__).parent / "run_model_arm.py"), "--features", str(out / "feats_fallback.npz"),
                "--c10h", a.c10h, "--out", str(out), "--seeds", str(a.seeds), "--boot", str(a.boot)], check=True)
