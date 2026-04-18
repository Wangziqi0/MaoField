#!/usr/bin/env python3
"""Block IV Step 1: precompute BGE-M3 embeddings for top-20 candidates of
nfcorpus / scifact / fiqa.

Output:
  results/block4/embeddings_{ds}.npz with fields:
    - ids: ndarray[N] of str  (text id, prefixed q: or d:)
    - vecs: ndarray[N, 1024] float32
"""
import json, time, sys, os
import numpy as np
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

EXP17 = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics")
INPUTS = EXP17 / "inputs_block1_top20"
OUT = EXP17 / "results/block4"
OUT.mkdir(parents=True, exist_ok=True)

URL = "http://192.168.31.22:8080/v1/embeddings"
MODEL = "bge-m3"
TIMEOUT = 60
MAX_FAIL_RATE = 0.05

DATASETS = ["nfcorpus", "scifact", "fiqa"]


def truncate(s, n=500):
    return s[:n] if s else ""


def collect_texts(ds):
    """Returns dict id -> text, where id is 'q:<qid>' or 'd:<docid>'."""
    p = INPUTS / f"{ds}_top20_input.json"
    qs = json.load(open(p))
    out = {}
    for q in qs:
        out[f"q:{q['query_id']}"] = truncate(q["query"])
        for c in q["candidates"]:
            key = f"d:{c['doc_id']}"
            if key not in out:
                out[key] = truncate(c["text"])
    return out


def embed_one(text):
    """One text -> 1024 vec or None on error."""
    try:
        r = requests.post(URL, json={"input": [text], "model": MODEL}, timeout=TIMEOUT)
        r.raise_for_status()
        d = r.json()
        return np.asarray(d["data"][0]["embedding"], dtype=np.float32)
    except Exception as e:
        return None


def run_dataset(ds, workers=16):
    texts = collect_texts(ds)
    out_file = OUT / f"embeddings_{ds}.npz"
    if out_file.exists():
        z = np.load(out_file, allow_pickle=True)
        if len(z["ids"]) == len(texts):
            print(f"[{ds}] cached, skip ({len(texts)} items)")
            return 0.0, 0.0
    ids = list(texts.keys())
    print(f"[{ds}] embedding {len(ids)} texts (workers={workers})...", flush=True)
    vecs = [None] * len(ids)
    fails = 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(embed_one, texts[i]): idx for idx, i in enumerate(ids)}
        done = 0
        for fut in as_completed(futs):
            idx = futs[fut]
            v = fut.result()
            if v is None:
                fails += 1
            else:
                vecs[idx] = v
            done += 1
            if done % 500 == 0 or done == len(ids):
                el = time.time() - t0
                print(f"  [{ds}] {done}/{len(ids)} fails={fails} ({el:.1f}s, {done/el:.1f}/s)", flush=True)
    fail_rate = fails / len(ids)
    if fail_rate > MAX_FAIL_RATE:
        print(f"[{ds}] FAIL rate {fail_rate:.2%} > {MAX_FAIL_RATE:.2%}, abort")
        sys.exit(1)
    # zero-fill failed
    for i, v in enumerate(vecs):
        if v is None:
            vecs[i] = np.zeros(1024, dtype=np.float32)
    arr = np.stack(vecs, axis=0)
    # L2 normalize
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms
    np.savez_compressed(out_file, ids=np.asarray(ids), vecs=arr)
    el = time.time() - t0
    print(f"[{ds}] done {el:.1f}s fails={fails} ({fail_rate:.2%}) -> {out_file}")
    return el, fail_rate


if __name__ == "__main__":
    sel = sys.argv[1:] if len(sys.argv) > 1 else DATASETS
    total = 0.0
    for ds in sel:
        el, fr = run_dataset(ds)
        total += el
    print(f"TOTAL embedding time: {total:.1f}s")
