#!/usr/bin/env python3
"""exp016 phase1: AUC matrix for 6 parameter-free similarity metrics x 7 datasets.

Pure diagnostic, no tuning, no learning.
Seed: 20260412
"""
import os
import sys
import json
import time
import random
import re
from pathlib import Path
from multiprocessing import Pool

import numpy as np
from rapidfuzz.distance import Levenshtein
from rank_bm25 import BM25Okapi

SEED = 20260412
BASE = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic")
RESULTS = BASE / "results"
RAW = RESULTS / "raw"
RESULTS.mkdir(exist_ok=True, parents=True)
RAW.mkdir(exist_ok=True, parents=True)

BEIR = Path("/home/amd/HEZIMENG/legal-assistant/beir_data")
D7 = BASE / "data" / "codesearchnet"

DATASETS = [
    ("nfcorpus", BEIR / "nfcorpus", 1000),
    ("scifact", BEIR / "scifact", 10_000_000),
    ("fiqa", BEIR / "fiqa", 1000),
    ("arguana", BEIR / "arguana", 1000),
    ("trec-covid", BEIR / "trec-covid", 10_000_000),
    ("quora", BEIR / "quora", 1000),
    ("codesearchnet", D7, 1000),
]

METRICS = ["s1_byte_cos", "s2_char_jac", "s3_2gram_jac", "s4_3gram_jac", "s5_lev", "s6_bm25"]
NEG_K = 99
LEV_TRUNC = 2000
WORKERS = 64
TOKEN_RE = re.compile(r"\w+", re.UNICODE)


# ---------- metric implementations (deterministic, no params) ----------
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


def char_set(text: str):
    return set(text)


def ngram_set(text: str, n: int):
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    inter = len(a & b)
    uni = len(a | b)
    return inter / uni if uni else 0.0


def lev_sim(q: str, d: str) -> float:
    qq = q[:LEV_TRUNC]
    dd = d[:LEV_TRUNC]
    m = max(len(qq), len(dd))
    if m == 0:
        return 1.0
    return 1.0 - Levenshtein.distance(qq, dd) / m


def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())


# ---------- data loading ----------
def load_corpus(path: Path):
    ids, texts = [], []
    with open(path / "corpus.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            title = obj.get("title") or ""
            body = obj.get("text") or ""
            text = (title + " " + body).strip()
            ids.append(obj["_id"])
            texts.append(text)
    return ids, texts


def load_queries(path: Path):
    ids, texts = [], []
    with open(path / "queries.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            ids.append(obj["_id"])
            texts.append((obj.get("text") or "").strip())
    return ids, texts


def load_qrels(path: Path):
    """Return dict: qid -> list of (docid, score) with score>0 sorted desc by score."""
    qrels = {}
    with open(path / "qrels" / "test.tsv", "r", encoding="utf-8") as f:
        header = f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            qid, did, sc = parts[0], parts[1], parts[2]
            try:
                sc = int(sc)
            except ValueError:
                try:
                    sc = int(float(sc))
                except Exception:
                    continue
            if sc <= 0:
                continue
            qrels.setdefault(qid, []).append((did, sc))
    for q in qrels:
        qrels[q].sort(key=lambda x: -x[1])
    return qrels


# ---------- per-query workers ----------
_GLOBAL = {}


def init_worker(corpus_texts_share, bm25_obj, doc_byte_vecs, doc_char_sets,
                doc_2g_sets, doc_3g_sets):
    _GLOBAL["corpus_texts"] = corpus_texts_share
    _GLOBAL["bm25"] = bm25_obj
    _GLOBAL["byte_vecs"] = doc_byte_vecs
    _GLOBAL["char_sets"] = doc_char_sets
    _GLOBAL["g2"] = doc_2g_sets
    _GLOBAL["g3"] = doc_3g_sets


def score_query(args):
    q_text, pos_idx, neg_idx = args
    corpus_texts = _GLOBAL["corpus_texts"]
    bm25 = _GLOBAL["bm25"]
    byte_vecs = _GLOBAL["byte_vecs"]
    char_sets = _GLOBAL["char_sets"]
    g2 = _GLOBAL["g2"]
    g3 = _GLOBAL["g3"]

    cand = [pos_idx] + list(neg_idx)

    # S1
    qv = byte_vec(q_text)
    s1 = np.array([float(np.dot(qv, byte_vecs[i])) for i in cand], dtype=np.float64)

    # S2
    qset = set(q_text)
    s2 = np.array([jaccard(qset, char_sets[i]) for i in cand], dtype=np.float64)

    # S3
    q2 = ngram_set(q_text, 2)
    s3 = np.array([jaccard(q2, g2[i]) for i in cand], dtype=np.float64)

    # S4
    q3 = ngram_set(q_text, 3)
    s4 = np.array([jaccard(q3, g3[i]) for i in cand], dtype=np.float64)

    # S5
    s5 = np.array([lev_sim(q_text, corpus_texts[i]) for i in cand], dtype=np.float64)

    # S6 BM25 -- get scores for all corpus, then pick cand
    q_tokens = tokenize(q_text)
    all_scores = bm25.get_scores(q_tokens) if q_tokens else np.zeros(len(corpus_texts))
    s6 = np.array([float(all_scores[i]) for i in cand], dtype=np.float64)

    return s1, s2, s3, s4, s5, s6


def auc_and_dprime(pos_vals: np.ndarray, neg_vals: np.ndarray):
    """pos_vals shape (N,), neg_vals shape (N, K). Per-query AUC mean, plus dprime over pooled."""
    N, K = neg_vals.shape
    # per-query AUC: (K - count(neg >= pos) ties handled by 0.5)
    aucs = []
    for i in range(N):
        p = pos_vals[i]
        n = neg_vals[i]
        greater = np.sum(n > p)
        equal = np.sum(n == p)
        # rank of pos: ties count as 0.5
        auc = (K - greater - 0.5 * equal) / K
        aucs.append(auc)
    auc_mean = float(np.mean(aucs))
    mu_p = float(np.mean(pos_vals))
    sd_p = float(np.std(pos_vals))
    mu_n = float(np.mean(neg_vals))
    sd_n = float(np.std(neg_vals))
    denom = np.sqrt((sd_p ** 2 + sd_n ** 2) / 2.0)
    dprime = float((mu_p - mu_n) / denom) if denom > 0 else 0.0
    return auc_mean, dprime, mu_p, sd_p, mu_n, sd_n


# ---------- per-dataset pipeline ----------
def run_dataset(name, path, n_queries_cap, rng):
    t0 = time.time()
    print(f"\n[{name}] loading corpus/queries/qrels ...", flush=True)
    doc_ids, doc_texts = load_corpus(path)
    q_ids, q_texts_all = load_queries(path)
    qrels = load_qrels(path)

    qid2text = dict(zip(q_ids, q_texts_all))
    did2idx = {d: i for i, d in enumerate(doc_ids)}
    N_corpus = len(doc_ids)
    print(f"[{name}] |corpus|={N_corpus} |queries_with_qrels|={len(qrels)}", flush=True)

    # select queries: those with at least one relevant doc existing in corpus
    eligible = []
    for qid, rels in qrels.items():
        if qid not in qid2text:
            continue
        # find highest-score doc present in corpus
        pos_did = None
        for did, _sc in rels:
            if did in did2idx:
                pos_did = did
                break
        if pos_did is None:
            continue
        eligible.append((qid, pos_did))
    print(f"[{name}] eligible queries: {len(eligible)}", flush=True)

    # sample
    rng.shuffle(eligible)
    if len(eligible) > n_queries_cap:
        eligible = eligible[:n_queries_cap]
    skipped_no_neg = 0

    # precompute per-doc data structures (expensive ones cached)
    print(f"[{name}] precomputing doc features ...", flush=True)
    t_pc = time.time()
    byte_vecs = np.stack([byte_vec(t) for t in doc_texts])
    char_sets = [set(t) for t in doc_texts]
    g2_sets = [ngram_set(t, 2) for t in doc_texts]
    g3_sets = [ngram_set(t, 3) for t in doc_texts]
    print(f"[{name}] doc features done in {time.time()-t_pc:.1f}s", flush=True)

    print(f"[{name}] building BM25 on {N_corpus} docs ...", flush=True)
    t_bm = time.time()
    tokenized_corpus = [tokenize(t) for t in doc_texts]
    bm25 = BM25Okapi(tokenized_corpus)
    print(f"[{name}] BM25 built in {time.time()-t_bm:.1f}s", flush=True)

    # build per-query job: (q_text, pos_idx, neg_idx_array)
    jobs = []
    used_queries = []
    all_doc_indices = np.arange(N_corpus)
    for qid, pos_did in eligible:
        pos_idx = did2idx[pos_did]
        # exclude all relevant docs for this query (score>0)
        rel_set = {did2idx[d] for d, _ in qrels[qid] if d in did2idx}
        # sample 99 non-relevant
        # use set difference via mask
        if N_corpus - len(rel_set) < NEG_K:
            skipped_no_neg += 1
            continue
        # efficient sampling: sample with replacement-like rejection
        mask = np.ones(N_corpus, dtype=bool)
        for ridx in rel_set:
            mask[ridx] = False
        candidates = all_doc_indices[mask]
        # sample 99 using rng
        chosen = rng.choice(candidates, size=NEG_K, replace=False)
        jobs.append((qid2text[qid], pos_idx, chosen))
        used_queries.append(qid)

    print(f"[{name}] running {len(jobs)} queries across {WORKERS} workers ...", flush=True)
    t_run = time.time()

    N = len(jobs)
    pos_mat = np.zeros((6, N), dtype=np.float64)
    neg_mat = np.zeros((6, N, NEG_K), dtype=np.float64)

    with Pool(processes=WORKERS, initializer=init_worker,
              initargs=(doc_texts, bm25, byte_vecs, char_sets, g2_sets, g3_sets)) as pool:
        for i, res in enumerate(pool.imap(score_query, jobs, chunksize=4)):
            for m_idx, arr in enumerate(res):
                pos_mat[m_idx, i] = arr[0]
                neg_mat[m_idx, i, :] = arr[1:]
            if (i + 1) % 100 == 0:
                print(f"  [{name}] {i+1}/{N} ({(time.time()-t_run):.1f}s)", flush=True)

    print(f"[{name}] scored {N} queries in {time.time()-t_run:.1f}s", flush=True)

    # save raw and compute metrics
    rows = []
    for m_idx, m_name in enumerate(METRICS):
        pos_v = pos_mat[m_idx]
        neg_v = neg_mat[m_idx]
        np.savez(RAW / f"{name}_{m_name}.npz", pos=pos_v, neg=neg_v)
        auc, dpr, mu_p, sd_p, mu_n, sd_n = auc_and_dprime(pos_v, neg_v)
        rows.append({
            "dataset": name,
            "metric": m_name,
            "n_queries": N,
            "auc": auc,
            "d_prime": dpr,
            "mu_pos": mu_p,
            "sigma_pos": sd_p,
            "mu_neg": mu_n,
            "sigma_neg": sd_n,
        })
        print(f"  [{name}/{m_name}] AUC={auc:.4f} d'={dpr:.3f}", flush=True)

    print(f"[{name}] total {time.time()-t0:.1f}s; skipped_no_neg={skipped_no_neg}", flush=True)
    return rows, skipped_no_neg


def main():
    random.seed(SEED)
    np.random.seed(SEED)
    rng = np.random.default_rng(SEED)

    all_rows = []
    skipped_info = {}
    t_all = time.time()
    for name, path, ncap in DATASETS:
        try:
            rows, skipped = run_dataset(name, path, ncap, rng)
            all_rows.extend(rows)
            skipped_info[name] = skipped
        except Exception as e:
            print(f"[{name}] FAILED: {e}", flush=True)
            import traceback
            traceback.print_exc()

    # write CSV
    import csv
    csv_path = RESULTS / "auc_matrix.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=[
            "dataset", "metric", "n_queries", "auc", "d_prime",
            "mu_pos", "sigma_pos", "mu_neg", "sigma_neg"])
        w.writeheader()
        for r in all_rows:
            w.writerow(r)
    print(f"\nWrote {csv_path}")

    # markdown summary
    md_path = RESULTS / "phase1_summary.md"
    write_summary(md_path, all_rows, skipped_info, time.time() - t_all)
    print(f"Wrote {md_path}")
    print(f"\nTOTAL elapsed: {time.time()-t_all:.1f}s")


def judge(auc):
    if auc < 0.55:
        return "near-random"
    if auc < 0.70:
        return "weak"
    if auc < 0.85:
        return "medium"
    return "strong"


def write_summary(path, rows, skipped_info, elapsed):
    # pivot: rows per dataset, columns per metric
    ds_order = [d[0] for d in DATASETS]
    data = {d: {m: None for m in METRICS} for d in ds_order}
    nq = {}
    for r in rows:
        data[r["dataset"]][r["metric"]] = r["auc"]
        nq[r["dataset"]] = r["n_queries"]

    lines = []
    lines.append("# Phase 1 诊断 AUC 矩阵 (exp016)")
    lines.append(f"\n总耗时: {elapsed:.1f}s  seed={SEED}  workers={WORKERS}\n")
    lines.append("## AUC 矩阵 (每 query 正例 vs 99 负例平均 AUC)\n")
    header = "| dataset | n_q | " + " | ".join(METRICS) + " | best |"
    sep = "|" + "---|" * (len(METRICS) + 3)
    lines.append(header)
    lines.append(sep)
    for d in ds_order:
        if all(v is None for v in data[d].values()):
            continue
        vals = [data[d][m] for m in METRICS]
        best_m = METRICS[int(np.argmax([v if v is not None else -1 for v in vals]))]
        row = f"| {d} | {nq.get(d,'-')} | " + " | ".join(
            f"{v:.4f}" if v is not None else "-" for v in vals) + f" | **{best_m}** |"
        lines.append(row)

    lines.append("\n## d' 矩阵\n")
    dp = {d: {m: None for m in METRICS} for d in ds_order}
    for r in rows:
        dp[r["dataset"]][r["metric"]] = r["d_prime"]
    lines.append(header.replace(" best ", ""))
    lines.append(sep[: -4])
    for d in ds_order:
        if all(v is None for v in dp[d].values()):
            continue
        vals = [dp[d][m] for m in METRICS]
        lines.append(f"| {d} | {nq.get(d,'-')} | " + " | ".join(
            f"{v:.3f}" if v is not None else "-" for v in vals) + " |")

    lines.append("\n## 每数据集最高 AUC 判读\n")
    lines.append("| dataset | best metric | AUC | 判读 |")
    lines.append("|---|---|---|---|")
    for d in ds_order:
        if all(v is None for v in data[d].values()):
            continue
        vals = [data[d][m] for m in METRICS]
        bi = int(np.argmax([v if v is not None else -1 for v in vals]))
        v = vals[bi]
        lines.append(f"| {d} | {METRICS[bi]} | {v:.4f} | {judge(v)} |")

    lines.append("\n## 判读阈值\n")
    lines.append("- AUC<0.55: 几乎无区分度 (near-random)\n- [0.55,0.70): 弱 (weak)\n- [0.70,0.85): 中 (medium)\n- >=0.85: 强 (strong)\n")

    lines.append("\n## 跳过/异常\n")
    for d, s in skipped_info.items():
        lines.append(f"- {d}: skipped_no_neg={s}")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
