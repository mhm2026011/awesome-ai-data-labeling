"""Extract frozen ResNet-18 (ImageNet) features for CIFAR-10 train and test. RUN ON YOUR MACHINE.
NOT TESTED in the authoring workspace (torch/torchvision were not installable there).
Usage: python extract_features.py --out feats.npz [--size 224] [--batch 256] [--root ./cifar_data]
Check before use: torchvision weights licence/terms (UNKNOWN to the author)."""
import argparse, json, time
import numpy as np, torch, torchvision
from torchvision import transforms, models


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="feats.npz"); ap.add_argument("--root", default="./cifar_data")
    ap.add_argument("--size", type=int, default=224); ap.add_argument("--batch", type=int, default=256)
    ap.add_argument("--limit", type=int, default=0, help="if >0, only this many train and test images (timing test)")
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    w = models.ResNet18_Weights.IMAGENET1K_V1
    net = models.resnet18(weights=w); net.fc = torch.nn.Identity(); net.eval().to(dev)
    tf = transforms.Compose([transforms.Resize(a.size), transforms.ToTensor(),
                             transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    def run(train):
        ds = torchvision.datasets.CIFAR10(a.root, train=train, download=True, transform=tf)
        if a.limit: ds = torch.utils.data.Subset(ds, range(a.limit))
        dl = torch.utils.data.DataLoader(ds, batch_size=a.batch, shuffle=False, num_workers=2)
        X, Y = [], []
        with torch.no_grad():
            for xb, yb in dl:
                X.append(net(xb.to(dev)).cpu().numpy().astype(np.float32)); Y.append(yb.numpy())
        return np.concatenate(X), np.concatenate(Y)

    t0 = time.time(); Xtr, ytr = run(True); t1 = time.time(); Xte, yte = run(False); t2 = time.time()
    np.savez_compressed(a.out, Xtr=Xtr, ytr=ytr, Xte=Xte, yte=yte)
    meta = dict(device=dev, torch=torch.__version__, torchvision=torchvision.__version__, size=a.size,
                train_seconds=t1 - t0, test_seconds=t2 - t1, n_train=len(ytr), n_test=len(yte))
    json.dump(meta, open(a.out + ".meta.json", "w"), indent=2); print(meta)


if __name__ == "__main__":
    main()
