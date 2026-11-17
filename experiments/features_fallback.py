"""Fallback features that need only numpy: HOG-style gradient histograms + coarse colour means.
Used ONLY because torch/pretrained weights were unavailable in the authoring workspace (deviation D-028).
Output dimension: 324 (gradient blocks) + 48 (colour) = 372. Input: uint8 (N,3,32,32)."""
import numpy as np


def hog_color_features(X, chunk=5000):
    out = []
    for s in range(0, len(X), chunk):
        x = X[s:s + chunk].astype(np.float32)
        n = len(x)
        gray = 0.299 * x[:, 0] + 0.587 * x[:, 1] + 0.114 * x[:, 2]
        gx = np.zeros_like(gray); gy = np.zeros_like(gray)
        gx[:, :, 1:-1] = gray[:, :, 2:] - gray[:, :, :-2]
        gy[:, 1:-1, :] = gray[:, 2:, :] - gray[:, :-2, :]
        mag = np.sqrt(gx ** 2 + gy ** 2)
        ang = np.mod(np.arctan2(gy, gx), np.pi)
        b = np.minimum((ang / np.pi * 9).astype(int), 8)
        cells = np.zeros((n, 4, 4, 9), np.float32)
        for k in range(9):
            cells[..., k] = (mag * (b == k)).reshape(n, 4, 8, 4, 8).sum(axis=(2, 4))
        blocks = []
        for i in range(3):
            for j in range(3):
                v = cells[:, i:i + 2, j:j + 2, :].reshape(n, 36)
                blocks.append(v / np.sqrt((v ** 2).sum(1, keepdims=True) + 1e-6))
        col = x.reshape(n, 3, 4, 8, 4, 8).mean(axis=(3, 5)).reshape(n, 48) / 255.0
        out.append(np.concatenate(blocks + [col], axis=1))
    return np.concatenate(out).astype(np.float32)
