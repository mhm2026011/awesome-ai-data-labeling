import sys, pathlib, pickle, os, tempfile
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import numpy as np
from load_cifar10_safe import load_batch
from features_fallback import hog_color_features


class _Evil:
    def __init__(self, marker): self.marker = marker
    def __reduce__(self): return (os.system, (f"touch {self.marker}",))


def test_safe_loader_blocks_code_execution():
    d = tempfile.mkdtemp(); marker = os.path.join(d, "pwned"); p = os.path.join(d, "evil_batch")
    pickle.dump({b"data": _Evil(marker), b"labels": [0]}, open(p, "wb"), protocol=2)
    try:
        load_batch(p); raised = False
    except pickle.UnpicklingError:
        raised = True
    assert raised and not os.path.exists(marker)


def test_safe_loader_reads_valid_batch():
    d = tempfile.mkdtemp(); p = os.path.join(d, "ok_batch")
    pickle.dump({b"data": np.arange(2 * 3072, dtype=np.uint8).reshape(2, 3072), b"labels": [1, 2], b"filenames": [b"a.png", b"b.png"]},
                open(p, "wb"), protocol=2)
    X, y, names = load_batch(p)
    assert X.shape == (2, 3, 32, 32) and X.dtype == np.uint8 and list(y) == [1, 2] and names == ["a.png", "b.png"]


def test_features_shape_flat_and_edge():
    flat = np.full((1, 3, 32, 32), 128, np.uint8)
    f = hog_color_features(flat)
    assert f.shape == (1, 372) and float(np.abs(f[:, :324]).max()) == 0.0
    edge = flat.copy(); edge[:, :, :, 16:] = 255          # vertical edge -> horizontal gradient
    g = hog_color_features(edge)
    assert float(np.abs(g[:, :324]).max()) > 0.1 and np.isfinite(g).all()


def test_features_deterministic_and_batch_invariant():
    rng = np.random.default_rng(0); X = rng.integers(0, 256, (12, 3, 32, 32), dtype=np.uint8)
    a = hog_color_features(X, chunk=5); b = hog_color_features(X, chunk=12)
    assert np.array_equal(a, b)
