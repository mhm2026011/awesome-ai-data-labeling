"""Load CIFAR-10 python batches WITHOUT executing arbitrary pickle code.
Only numpy array reconstruction and plain containers are allowed; anything else raises."""
import io, pickle
import numpy as np

_ALLOWED = {
    ("numpy._core.multiarray", "_reconstruct"), ("numpy.core.multiarray", "_reconstruct"),
    ("numpy", "ndarray"), ("numpy", "dtype"),
    ("numpy._core.multiarray", "scalar"), ("numpy.core.multiarray", "scalar"),
    ("builtins", "dict"), ("builtins", "list"), ("builtins", "tuple"), ("builtins", "set"),
    ("_codecs", "encode"),
}


class _Safe(pickle.Unpickler):
    def find_class(self, module, name):
        if (module, name) in _ALLOWED:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked global {module}.{name}")


def load_batch(path):
    with open(path, "rb") as f:
        d = _Safe(io.BytesIO(f.read()), encoding="bytes").load()
    X = np.asarray(d[b"data"], dtype=np.uint8).reshape(-1, 3, 32, 32)
    y = np.asarray(d[b"labels"], dtype=np.int64)
    names = [x.decode() if isinstance(x, bytes) else str(x) for x in d.get(b"filenames", [])]
    return X, y, names


def load_cifar10(folder):
    import pathlib
    p = pathlib.Path(folder)
    Xs, ys = [], []
    for i in range(1, 6):
        X, y, _ = load_batch(p / f"data_batch_{i}"); Xs.append(X); ys.append(y)
    Xte, yte, nte = load_batch(p / "test_batch")
    return np.concatenate(Xs), np.concatenate(ys), Xte, yte, nte
