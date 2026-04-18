#!/usr/bin/env python3
"""Convert embeddings_{ds}.npz to embeddings_{ds}.json (id -> [1024 floats])
for the Rust solver to consume."""
import json, sys, numpy as np
from pathlib import Path

OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block4")

for ds in sys.argv[1:] or ["nfcorpus", "scifact", "fiqa"]:
    z = np.load(OUT / f"embeddings_{ds}.npz", allow_pickle=True)
    ids = z["ids"]; vecs = z["vecs"]
    obj = {str(i): v.tolist() for i, v in zip(ids, vecs)}
    out_path = OUT / f"embeddings_{ds}.json"
    with open(out_path, "w") as f:
        json.dump(obj, f)
    print(f"[{ds}] {len(obj)} -> {out_path}")
