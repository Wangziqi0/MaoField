#!/usr/bin/env python3
"""phase 4 batch A: build BM25 top-100 candidate pool for NFCorpus and SciFact.

Same tokenization as phase1_auc.py. Doc text = title+' '+body, truncated to 500 chars.
"""
import json
import re
import time
from pathlib import Path

from rank_bm25 import BM25Okapi

BEIR = Path("/home/amd/HEZIMENG/legal-assistant/beir_data")
OUT = Path("/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/results/phase4")
OUT.mkdir(parents=True, exist_ok=True)

TOKEN_RE = re.compile(r"\w+", re.UNICODE)
TRUNC = 500
TOP_K = 100


def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())


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
    qrels = {}
    with open(path / "qrels" / "test.tsv", "r", encoding="utf-8") as f:
        f.readline()
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
            qrels.setdefault(qid, {})[did] = sc
    return qrels


def build(name: str):
    t0 = time.time()
    path = BEIR / name
    print(f"[{name}] loading ...", flush=True)
    doc_ids, doc_texts = load_corpus(path)
    q_ids, q_texts = load_queries(path)
    qrels = load_qrels(path)
    qid2text = dict(zip(q_ids, q_texts))
    did2idx = {d: i for i, d in enumerate(doc_ids)}
    print(f"[{name}] |corpus|={len(doc_ids)} |queries_with_qrels|={len(qrels)}", flush=True)

    print(f"[{name}] building BM25 ...", flush=True)
    tokenized = [tokenize(t) for t in doc_texts]
    bm25 = BM25Okapi(tokenized)
    print(f"[{name}] BM25 built in {time.time()-t0:.1f}s", flush=True)

    eligible_qids = [qid for qid in qrels.keys() if qid in qid2text]
    eligible_qids.sort()
    print(f"[{name}] eligible queries: {len(eligible_qids)}", flush=True)

    out_list = []
    for i, qid in enumerate(eligible_qids):
        q_text = qid2text[qid]
        q_tokens = tokenize(q_text)
        if not q_tokens:
            continue
        scores = bm25.get_scores(q_tokens)
        # top-100 indices
        top_idx = scores.argsort()[::-1][:TOP_K]
        cands = []
        for idx in top_idx:
            text = doc_texts[idx][:TRUNC]
            cands.append({"doc_id": doc_ids[idx], "text": text})
        # qrels with score>0 (already filtered)
        out_list.append({
            "query_id": qid,
            "query": q_text,
            "candidates": cands,
            "qrels": qrels[qid],
        })
        if (i + 1) % 50 == 0:
            print(f"  [{name}] {i+1}/{len(eligible_qids)}", flush=True)

    out_path = OUT / f"{name}_stage1_input.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out_list, f, ensure_ascii=False)
    print(f"[{name}] wrote {out_path}  (n={len(out_list)}, {time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    for name in ["nfcorpus", "scifact"]:
        build(name)
