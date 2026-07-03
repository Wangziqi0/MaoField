#!/usr/bin/env python3
"""Build a MaoField RAG FAISS index on node36 using node22 HTTP embeddings.

Node36 owns file scope, chunking, metadata, FAISS writing, verification, and
promotion.  Node22 only serves temporary bge-m3 embeddings through llama.cpp.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

import faiss
import numpy as np

sys.path.insert(0, "/media/amd/raid1/rag")
import chunk_md  # noqa: E402


def collect_files(args: argparse.Namespace) -> list[str]:
    if args.file_list:
        with open(args.file_list, "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip()]
    if os.path.isfile(args.input):
        return [args.input]
    return list(chunk_md.iter_md_files(args.input))


def chunks(seq: list[str], size: int) -> Iterable[list[str]]:
    for start in range(0, len(seq), size):
        yield seq[start:start + size]


def post_json(url: str, payload: dict, timeout: int) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def embed_batch(endpoint: str, model: str, texts: list[str], timeout: int, retries: int) -> np.ndarray:
    url = endpoint.rstrip("/") + "/v1/embeddings"
    payload = {"model": model, "input": texts}
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            out = post_json(url, payload, timeout)
            items = out.get("data", [])
            if len(items) != len(texts):
                raise RuntimeError(f"embedding count mismatch: got {len(items)} expected {len(texts)}")
            if all("index" in item for item in items):
                items = sorted(items, key=lambda item: int(item["index"]))
            vecs = np.asarray([item["embedding"] for item in items], dtype="float32")
            if vecs.ndim != 2:
                raise RuntimeError(f"unexpected embedding shape {vecs.shape}")
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            return vecs / norms
        except (urllib.error.URLError, TimeoutError, RuntimeError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2 * attempt, 10))
    raise RuntimeError(f"embedding request failed after {retries} attempts: {last_error}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RAG index with node22 HTTP embeddings.")
    parser.add_argument("input", nargs="?", default="", help="single markdown file or directory")
    parser.add_argument("--file-list", help="one markdown path per line")
    parser.add_argument("--index-dir", required=True)
    parser.add_argument("--endpoint", default="http://192.168.31.22:18080")
    parser.add_argument("--model", default="bge-m3-temp")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument(
        "--max-input-chars",
        type=int,
        default=3000,
        help="truncate text sent to the HTTP embedding server; metadata keeps the original chunk text",
    )
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--target", type=int, default=450)
    parser.add_argument("--overlap", type=int, default=60)
    args = parser.parse_args()

    index_dir = Path(args.index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "kb.faiss"
    meta_path = index_dir / "kb_meta.jsonl"

    files = collect_files(args)
    print(f"[1/4] files={len(files)}")

    t0 = time.time()
    records: list[dict] = []
    for fp in files:
        try:
            records.extend(chunk_md.chunk_file(fp, args.target, args.overlap))
        except Exception as exc:
            print(f"[warn] chunk failed {fp}: {exc}", file=sys.stderr)
    print(f"[2/4] chunks={len(records)} chunk_seconds={time.time() - t0:.1f}")
    if not records:
        raise SystemExit("no chunks")

    texts = [record["text"] for record in records]
    if args.max_input_chars > 0:
        texts_for_embedding = [text[:args.max_input_chars] for text in texts]
    else:
        texts_for_embedding = texts
    batches = list(chunks(texts_for_embedding, args.batch_size))
    vec_parts: list[np.ndarray] = []
    t0 = time.time()
    print(
        f"[3/4] remote_embed endpoint={args.endpoint} "
        f"model={args.model} batch={args.batch_size} batches={len(batches)}"
    )
    for idx, batch in enumerate(batches, 1):
        vec_parts.append(embed_batch(args.endpoint, args.model, batch, args.timeout, args.retries))
        if idx == 1 or idx % 10 == 0 or idx == len(batches):
            elapsed = time.time() - t0
            done = min(idx * args.batch_size, len(texts_for_embedding))
            rate = done / elapsed if elapsed > 0 else 0.0
            print(f"  embedded_batches={idx}/{len(batches)} texts={done}/{len(texts)} rate={rate:.2f} text/s")
    vecs = np.vstack(vec_parts).astype("float32", copy=False)
    embed_seconds = time.time() - t0

    index = faiss.IndexFlatIP(vecs.shape[1])
    index.add(vecs)
    faiss.write_index(index, str(index_path))
    with meta_path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    print("[4/4] wrote index")
    print(f"      faiss={index_path} bytes={index_path.stat().st_size} vectors={index.ntotal} dim={vecs.shape[1]}")
    print(f"      meta={meta_path} bytes={meta_path.stat().st_size}")
    print(f"[stat] files={len(files)} chunks={len(records)} embed_seconds={embed_seconds:.1f} rate={len(texts_for_embedding) / embed_seconds:.3f}text/s max_input_chars={args.max_input_chars}")


if __name__ == "__main__":
    main()
