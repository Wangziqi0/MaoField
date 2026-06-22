#!/usr/bin/env bash
set -euo pipefail

# Rebuild the canonical knowledge RAG from node36's stable RAG environment.
# This script intentionally reuses /media/amd/raid1/rag/scope_select.py and
# build_index.py instead of modifying shared RAG code.

PROJECT_ROOT="${PROJECT_ROOT:-/media/amd/raid1/canonical/projects/MaoField}"
RAG_ROOT="${RAG_ROOT:-/media/amd/raid1/rag}"
PY="${PY:-/home/amd/venv/bin/python}"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="${OUT_DIR:-$PROJECT_ROOT/docs/infra/rag_rebuild_20260622}"
FILE_LIST="$OUT_DIR/canonical_scope_active_${STAMP}.txt"
LOG="$OUT_DIR/rag_rebuild_36_${STAMP}.log"

mkdir -p "$OUT_DIR"

{
  echo "[info] start $(date '+%F %T %Z')"
  echo "[info] project=$PROJECT_ROOT"
  echo "[info] rag=$RAG_ROOT"
  echo "[info] python=$PY"

  echo "[1/5] scan MaoField and refresh data digest"
  "$PY" "$PROJECT_ROOT/scripts/rag_scan_maofield.py" \
    --project-root "$PROJECT_ROOT" \
    --out-dir "$OUT_DIR"

  echo "[2/5] generate canonical active scope"
  HF_HUB_OFFLINE=1 "$PY" "$RAG_ROOT/scope_select.py" \
    --only-active \
    --out "$FILE_LIST"
  wc -l "$FILE_LIST"

  echo "[3/5] backup existing index"
  if [[ -f "$RAG_ROOT/index/kb.faiss" ]]; then
    cp -a "$RAG_ROOT/index/kb.faiss" "$RAG_ROOT/index/kb.faiss.bak_pre_rebuild_${STAMP}"
  fi
  if [[ -f "$RAG_ROOT/index/kb_meta.jsonl" ]]; then
    cp -a "$RAG_ROOT/index/kb_meta.jsonl" "$RAG_ROOT/index/kb_meta.jsonl.bak_pre_rebuild_${STAMP}"
  fi

  echo "[4/5] build index"
  HF_HUB_OFFLINE=1 "$PY" "$RAG_ROOT/build_index.py" \
    --file-list "$FILE_LIST" \
    --batch-size "${BATCH_SIZE:-8}"

  echo "[5/5] smoke queries"
  HF_HUB_OFFLINE=1 "$PY" "$RAG_ROOT/kb_search.py" \
    "MaoField chain actual EMA KL F3 LOSO C meta-pattern" \
    --top-k 6 \
    --project MaoField
  HF_HUB_OFFLINE=1 "$PY" "$RAG_ROOT/kb_search.py" \
    "deep research current code math glass box report" \
    --top-k 6 \
    --project MaoField

  echo "[info] done $(date '+%F %T %Z')"
  echo "[info] log=$LOG"
} 2>&1 | tee "$LOG"
