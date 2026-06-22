#!/usr/bin/env python3
"""Scan MaoField files and prepare RAG-safe manifests.

This is a project-side helper. It does not change the shared RAG code under
``/media/amd/raid1/rag``.  The intent is:

1. Recursively inventory MaoField markdown and data/artifact files.
2. Keep raw data out of the semantic index.
3. Emit a compact markdown digest that *can* be indexed by the existing
   markdown-only RAG pipeline.

RAG remains a locator. Claims still need canonical files, logs, JSON/JSONL, or
scripts as evidence.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path("/media/amd/raid1/canonical/projects/MaoField")
RAG_LAYER_MAP = Path("/media/amd/raid1/rag/layer_map.tsv")
DEFAULT_OUT_DIR = PROJECT_ROOT / "docs/infra/rag_rebuild_20260622"

TEXT_DATA_EXTS = {
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".csv",
    ".tsv",
    ".txt",
    ".log",
}
MODEL_ARTIFACT_EXTS = {
    ".safetensors",
    ".bin",
    ".arrow",
    ".npz",
    ".npy",
    ".pt",
    ".pth",
    ".so",
    ".rlib",
    ".rmeta",
    ".a",
    ".o",
}
CODE_EXTS = {".py", ".sh", ".js", ".rs", ".toml", ".lock", ".tex", ".bib"}

EXCLUDE_DIR_PARTS = {".git", ".codex", "__pycache__", ".pytest_cache"}
DEFAULT_MD_EXCLUDE_PARTS = {"archive", "wip", "sessions"}
GENERATED_REBUILD_FILENAMES = {
    "maofield_file_inventory.tsv",
    "maofield_scan_summary.json",
    "maofield_data_digest_20260622.md",
    "scope_include_maofield_active_md.txt",
    "scope_include_maofield_all_nonarchive_md.txt",
}
S_FALLBACK_STEMS = (
    "paper_v1",
    "paper_v2",
    "paper_v3",
    "paper_v4",
    "paper_v5",
    "paper_v6",
    "paper_v7",
    "progress_snapshot",
    "GLOBAL_FILE_INDEX_D26",
    "MD_INDEX_LATEST_D26",
    "INDEX_MD_D22",
    "MATH_RIGOROUS_PROOF_D26",
    "MATH_MULTI_CHANNEL",
    "SESSION_CROSS_LAYER_D25",
    "PROGRESS_D24_STAGE0",
    "SURFACE_D24_LAUNCH_FAIL",
    "CROSS_CHANNEL_VERIFY_D24",
    "PAPER_V9_DRAFT_D25",
    "VENUE_EVAL_NEURIPS_NMI_D22",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def load_layer_map(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                out[os.path.abspath(parts[0])] = parts[1]
    return out


def should_skip_dir(path: Path) -> bool:
    return any(part in EXCLUDE_DIR_PARTS for part in path.parts)


def is_generated_rebuild_artifact(path: Path, root: Path) -> bool:
    try:
        rpath = path.relative_to(root)
    except ValueError:
        return False
    parts = rpath.parts
    if len(parts) < 4 or parts[:3] != ("docs", "infra", "rag_rebuild_20260622"):
        return False
    name = path.name
    return (
        name in GENERATED_REBUILD_FILENAMES
        or name.startswith("canonical_scope_active_")
        or name.startswith("rag_build_node22_candidate_")
        or name.startswith("rag_build_node22_final_")
        or name.startswith("rag_rebuild_36_")
    )


def classify(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".md":
        return "markdown"
    if ext in TEXT_DATA_EXTS:
        return "structured_or_text_data"
    if ext in MODEL_ARTIFACT_EXTS:
        return "model_or_binary_artifact"
    if ext in CODE_EXTS:
        return "code_or_config"
    if not ext:
        return "no_extension_or_generated"
    return "other"


def md_layer(path: Path, layer_map: dict[str, str]) -> str:
    exact = layer_map.get(os.path.abspath(path))
    if exact in {"A", "S"}:
        return exact
    p = path.as_posix()
    if any(stem in p for stem in S_FALLBACK_STEMS):
        return "S"
    return "A"


def md_default_excluded(path: Path, root: Path) -> bool:
    parts = set(path.relative_to(root).parts)
    if parts & DEFAULT_MD_EXCLUDE_PARTS:
        return True
    name = path.name
    return name.endswith(".bak") or name.startswith("progress_snapshot_")


def sha256_small(path: Path, limit: int) -> str:
    try:
        if path.stat().st_size > limit:
            return "not_hashed_large"
        h = hashlib.sha256()
        with path.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "hash_unavailable"


def policy(path: Path, root: Path, layer: str, category: str) -> str:
    if category == "markdown":
        if md_default_excluded(path, root):
            return "exclude_markdown_archive_or_wip"
        if layer == "S":
            return "exclude_markdown_superseded"
        return "index_markdown_active"
    if category == "structured_or_text_data":
        return "digest_only_data"
    if category == "model_or_binary_artifact":
        return "inventory_only_binary_artifact"
    return "inventory_only"


def scan(root: Path, layer_map: dict[str, str], hash_limit: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dpath = Path(dirpath)
        dirnames[:] = [
            d for d in dirnames
            if d not in EXCLUDE_DIR_PARTS and not should_skip_dir(dpath / d)
        ]
        for name in filenames:
            path = dpath / name
            if should_skip_dir(path) or is_generated_rebuild_artifact(path, root):
                continue
            try:
                st = path.stat()
            except OSError:
                continue
            category = classify(path)
            layer = md_layer(path, layer_map) if category == "markdown" else ""
            rows.append({
                "rel_path": rel(path, root),
                "abs_path": str(path.resolve()),
                "size_bytes": st.st_size,
                "mtime_utc": datetime.fromtimestamp(st.st_mtime, tz=timezone.utc).isoformat(timespec="seconds"),
                "ext": path.suffix.lower() or "[no_ext]",
                "category": category,
                "md_layer": layer,
                "index_policy": policy(path, root, layer, category),
                "sha256_if_small": sha256_small(path, hash_limit),
            })
    rows.sort(key=lambda r: str(r["rel_path"]))
    return rows


def write_inventory(rows: list[dict[str, object]], path: Path) -> None:
    fields = [
        "rel_path",
        "size_bytes",
        "mtime_utc",
        "ext",
        "category",
        "md_layer",
        "index_policy",
        "sha256_if_small",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def write_file_lists(rows: list[dict[str, object]], root: Path, out_dir: Path) -> None:
    active = [
        str(root / str(row["rel_path"]))
        for row in rows
        if row["index_policy"] == "index_markdown_active"
    ]
    all_md = [
        str(root / str(row["rel_path"]))
        for row in rows
        if row["category"] == "markdown" and not md_default_excluded(root / str(row["rel_path"]), root)
    ]
    (out_dir / "scope_include_maofield_active_md.txt").write_text(
        "\n".join(active) + ("\n" if active else ""),
        encoding="utf-8",
    )
    (out_dir / "scope_include_maofield_all_nonarchive_md.txt").write_text(
        "\n".join(all_md) + ("\n" if all_md else ""),
        encoding="utf-8",
    )


def mib(n: int) -> float:
    return n / 1024 / 1024


def markdown_table(rows: list[list[object]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |"]
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |")
    return "\n".join(out)


def write_digest(rows: list[dict[str, object]], root: Path, out_path: Path) -> None:
    by_ext: Counter[str] = Counter()
    by_ext_size: defaultdict[str, int] = defaultdict(int)
    by_policy: Counter[str] = Counter()
    by_cat: Counter[str] = Counter()
    for row in rows:
        ext = str(row["ext"])
        by_ext[ext] += 1
        by_ext_size[ext] += int(row["size_bytes"])
        by_policy[str(row["index_policy"])] += 1
        by_cat[str(row["category"])] += 1

    ext_rows = [
        [ext, by_ext[ext], f"{mib(by_ext_size[ext]):.2f}"]
        for ext, _ in sorted(by_ext.items(), key=lambda kv: by_ext_size[kv[0]], reverse=True)[:40]
    ]
    policy_rows = [[k, v] for k, v in sorted(by_policy.items())]
    cat_rows = [[k, v] for k, v in sorted(by_cat.items())]

    data_rows = [
        row for row in rows
        if row["category"] == "structured_or_text_data"
    ]
    data_top = sorted(data_rows, key=lambda r: int(r["size_bytes"]), reverse=True)[:60]
    data_top_rows = [
        [row["rel_path"], f"{mib(int(row['size_bytes'])):.2f}", row["ext"], row["index_policy"]]
        for row in data_top
    ]
    key_patterns = (
        "verdict",
        "result",
        "locked",
        "highorder",
        "decouple",
        "metapattern",
        "manifest",
        "aggregate",
        "panel",
        "q4",
        "schema",
        "smoke",
        "jsonl",
    )
    key_data = [
        row for row in data_rows
        if any(pat in str(row["rel_path"]).lower() for pat in key_patterns)
    ][:120]
    key_rows = [
        [row["rel_path"], f"{mib(int(row['size_bytes'])):.3f}", row["ext"]]
        for row in key_data
    ]
    q4_patterns = (
        "panel_primary_20260622",
        "panel_schema_freq_q4",
        "negative_smoke_20260622",
        "multi_checkpoint_smoke_20260622",
        "one_checkpoint_smoke_seed",
    )
    q4_data = [
        row for row in data_rows
        if any(pat in str(row["rel_path"]).lower() for pat in q4_patterns)
    ]
    q4_rows = [
        [
            row["rel_path"],
            f"{mib(int(row['size_bytes'])):.3f}",
            row["ext"],
            row["sha256_if_small"],
        ]
        for row in q4_data
    ]

    text = f"""# MaoField RAG Data Digest — 2026-06-22

Generated by `scripts/rag_scan_maofield.py`.

## Scope

- Project root: `{root}`
- Generated UTC: `{utc_now()}`
- Git HEAD at scan: `{git_head(root)}`
- Generated rebuild inventory/digest/scope/log files are excluded from this
  scan to avoid self-referential file-count growth.
- Total scanned files: `{len(rows)}`
- Markdown files: `{sum(1 for r in rows if r['category'] == 'markdown')}`
- Structured/text data files: `{len(data_rows)}`

## Index Policy

Raw data is **not** embedded directly into the knowledge RAG. The RAG index should
embed active markdown plus this digest. Original JSON/JSONL/log files remain the
primary evidence and must be opened or processed directly before promoting claims.

{markdown_table(policy_rows, ['policy', 'count'])}

## Category Counts

{markdown_table(cat_rows, ['category', 'count'])}

## Largest Extensions

{markdown_table(ext_rows, ['extension', 'files', 'MiB'])}

## Largest Structured/Text Data Files

These files are inventory targets, not direct embedding targets.

{markdown_table(data_top_rows, ['path', 'MiB', 'ext', 'policy'])}

## Key Data / Verdict / Result Files

This is a path index for follow-up verification. It is deliberately not a
substitute for reading the files or running their companion scripts.

{markdown_table(key_rows, ['path', 'MiB', 'ext'])}

## Current Q4 Panel / Smoke Data Files

These D622 files are high-priority verification targets for the q4
implementation-review gate. They remain digest-only: do not treat this table as
primary evidence.

{markdown_table(q4_rows, ['path', 'MiB', 'ext', 'sha256_if_small'])}

## Guardrails

- Do not index model checkpoints, tokenizer blobs, embedding dumps, or large
  regenerated experiment outputs as raw text.
- Do not use this digest as proof. It is a locator over canonical data.
- Superseded markdown remains visible in the inventory but is excluded from the
  default active markdown file list.
"""
    out_path.write_text(text, encoding="utf-8")


def write_summary_json(rows: list[dict[str, object]], path: Path, root: Path) -> None:
    summary = {
        "generated_utc": utc_now(),
        "project_root": str(root),
        "git_head": git_head(root),
        "total_files": len(rows),
        "by_category": dict(Counter(str(row["category"]) for row in rows)),
        "by_policy": dict(Counter(str(row["index_policy"]) for row in rows)),
        "by_ext": dict(Counter(str(row["ext"]) for row in rows)),
    }
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan MaoField for RAG-safe inventory and digest files.")
    parser.add_argument("--project-root", default=str(PROJECT_ROOT))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    parser.add_argument("--layer-map", default=str(RAG_LAYER_MAP))
    parser.add_argument("--hash-limit", type=int, default=1024 * 1024)
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    layer_map = load_layer_map(Path(args.layer_map))

    rows = scan(root, layer_map, args.hash_limit)
    write_inventory(rows, out_dir / "maofield_file_inventory.tsv")
    write_digest(rows, root, out_dir / "maofield_data_digest_20260622.md")
    write_file_lists(rows, root, out_dir)
    write_summary_json(rows, out_dir / "maofield_scan_summary.json", root)

    print(f"scanned_files={len(rows)}")
    print(f"out_dir={out_dir}")
    print(f"inventory={out_dir / 'maofield_file_inventory.tsv'}")
    print(f"digest={out_dir / 'maofield_data_digest_20260622.md'}")


if __name__ == "__main__":
    main()
