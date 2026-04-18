#!/usr/bin/env python3
"""Block I segment 1: run BM25 / S1 / S4 / BGE-reranker over 5 datasets.

Writes:
  - results/block1/{dataset}_{scorer}_ranks.json  (per-query reranked doc_id list)
  - contributes rows to block1_baselines.csv via block1_aggregate.py

Notes:
  - Candidate pool = BM25 top-100 per query (built by block1_build_pools.py).
  - BM25 "ranks" = original candidate order (BM25 top-100 already sorted).
  - BGE uses HTTP endpoint with batched calls (1 request per query, 100 docs).
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import requests

INPUTS = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/inputs_block1")
OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/results/block1")
OUT.mkdir(parents=True, exist_ok=True)

DATASETS = ["nfcorpus", "scifact", "fiqa", "arguana", "trec-covid"]

BGE_URL = "http://192.168.31.22:8081/v1/rerank"
TOKEN_RE = re.compile(r"\w+", re.UNICODE)


def byte_vec(text: str) -> np.ndarray:
    b = text.encode("utf-8", errors="ignore")
    if not b:
        return np.zeros(256, dtype=np.float32)
    arr = np.frombuffer(b, dtype=np.uint8)
    v = np.bincount(arr, minlength=256).astype(np.float32)
    n = np.linalg.norm(v)
    if n > 0:
        v /= n
    return v


def ngram_set(text: str, n: int):
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a, b):
    if not a and not b:
        return 0.0
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def run_bm25(data):
    """BM25 = original candidate order (pool is already BM25 top-100 sorted)."""
    t0 = time.time()
    ranks = []
    for item in data:
        ranks.append({
            "query_id": item["query_id"],
            "order": [c["doc_id"] for c in item["candidates"]],
        })
    return ranks, time.time() - t0


def run_s1(data):
    t0 = time.time()
    ranks = []
    for item in data:
        q_text = item["query"]
        cands = item["candidates"]
        qv = byte_vec(q_text)
        scores = np.array([float(np.dot(qv, byte_vec(c["text"]))) for c in cands])
        order_idx = np.argsort(-scores, kind="stable")
        ranks.append({
            "query_id": item["query_id"],
            "order": [cands[i]["doc_id"] for i in order_idx],
        })
    return ranks, time.time() - t0


def run_s4(data):
    t0 = time.time()
    ranks = []
    for item in data:
        q_text = item["query"]
        cands = item["candidates"]
        q3 = ngram_set(q_text, 3)
        scores = np.array([jaccard(q3, ngram_set(c["text"], 3)) for c in cands])
        order_idx = np.argsort(-scores, kind="stable")
        ranks.append({
            "query_id": item["query_id"],
            "order": [cands[i]["doc_id"] for i in order_idx],
        })
    return ranks, time.time() - t0


def bge_call(q, docs, timeout=120, retries=3):
    payload = {"query": q, "documents": docs, "model": "bge-reranker"}
    last_exc = None
    for attempt in range(retries):
        try:
            r = requests.post(BGE_URL, json=payload, timeout=timeout)
            if r.status_code != 200:
                last_exc = RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
                time.sleep(1.0 * (attempt + 1))
                continue
            return r.json()
        except Exception as e:
            last_exc = e
            time.sleep(1.0 * (attempt + 1))
    raise last_exc


def run_bge(data, progress_name="bge"):
    t0 = time.time()
    ranks = []
    fails = 0
    n = len(data)
    for i, item in enumerate(data):
        cands = item["candidates"]
        docs = [c["text"] for c in cands]
        try:
            resp = bge_call(item["query"], docs)
            results = resp["results"]  # each has index, relevance_score
            order_idx = sorted(range(len(results)),
                               key=lambda k: -results[k]["relevance_score"])
            # note: results already carry index field; map via results[k]["index"]
            # after sort, we need candidate indices, not result positions:
            # each results entry tells us that candidate at results[k]["index"]
            # has score relevance_score. So:
            scored = [(r["index"], r["relevance_score"]) for r in results]
            scored.sort(key=lambda x: -x[1])
            order_ids = [cands[idx]["doc_id"] for idx, _ in scored]
        except Exception as e:
            fails += 1
            print(f"  [{progress_name}] FAIL qid={item['query_id']} err={e}", flush=True)
            order_ids = [c["doc_id"] for c in cands]  # fallback BM25 order
        ranks.append({"query_id": item["query_id"], "order": order_ids})
        if (i + 1) % 50 == 0 or (i + 1) == n:
            print(f"  [{progress_name}] {i+1}/{n}  elapsed={time.time()-t0:.1f}s fails={fails}",
                  flush=True)
    fail_rate = fails / n if n else 0.0
    return ranks, time.time() - t0, fail_rate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scorers", nargs="+",
                    default=["bm25", "s1", "s4", "bge"],
                    choices=["bm25", "s1", "s4", "bge"])
    ap.add_argument("--datasets", nargs="+", default=DATASETS)
    args = ap.parse_args()

    for ds in args.datasets:
        inp_path = INPUTS / f"{ds}_stage1_input.json"
        if not inp_path.exists():
            print(f"[{ds}] SKIP (no input yet): {inp_path}")
            continue
        data = json.load(open(inp_path))
        print(f"[{ds}] loaded {len(data)} queries", flush=True)

        for scorer in args.scorers:
            out_path = OUT / f"{ds}_{scorer}_ranks.json"
            if out_path.exists():
                print(f"  [{ds}/{scorer}] exists, skip")
                continue
            print(f"  [{ds}/{scorer}] running ...", flush=True)
            if scorer == "bm25":
                ranks, dt = run_bm25(data); fail_rate = 0.0
            elif scorer == "s1":
                ranks, dt = run_s1(data); fail_rate = 0.0
            elif scorer == "s4":
                ranks, dt = run_s4(data); fail_rate = 0.0
            elif scorer == "bge":
                ranks, dt, fail_rate = run_bge(data, progress_name=f"{ds}/bge")
                if fail_rate > 0.10:
                    print(f"  [{ds}/bge] HIGH FAILURE RATE {fail_rate:.1%} -- halting", flush=True)
                    sys.exit(2)
            json.dump({"dataset": ds, "scorer": scorer, "runtime_s": dt,
                       "n_queries": len(ranks), "fail_rate": fail_rate,
                       "ranks": ranks}, open(out_path, "w"))
            print(f"  [{ds}/{scorer}] done {dt:.1f}s fails={fail_rate:.1%} -> {out_path}", flush=True)


if __name__ == "__main__":
    main()
