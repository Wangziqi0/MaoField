#!/usr/bin/env bash
set -euo pipefail

# Optional node22 runner for temporary vectorization.
#
# Current node22 status observed on 2026-06-22:
# - reachable as amd@192.168.31.22
# - has rocm-smi
# - does NOT have /media/amd/raid1/rag mounted
# - system python lacked numpy/torch/faiss/FlagEmbedding/transformers
#
# Therefore this script is conservative. It probes node22 and exits with clear
# preparation instructions unless the remote environment is already ready.
# The stable default remains scripts/rag_rebuild_maofield_36.sh.

NODE22="${NODE22:-amd@192.168.31.22}"
REMOTE_PY="${REMOTE_PY:-/home/amd/venv-rag/bin/python}"
REMOTE_ROOT="${REMOTE_ROOT:-/home/amd/tmp/maofield_rag_node22}"
PROJECT_ROOT="${PROJECT_ROOT:-/media/amd/raid1/canonical/projects/MaoField}"
RAG_ROOT="${RAG_ROOT:-/media/amd/raid1/rag}"

echo "[probe] $NODE22"
ssh -o BatchMode=yes -o ConnectTimeout=10 "$NODE22" \
  'hostname; date "+%F %T %Z"; command -v rocm-smi || true'

set +e
ssh -o BatchMode=yes "$NODE22" "$REMOTE_PY" - <<'PY'
mods = ["numpy", "torch", "faiss", "FlagEmbedding", "transformers"]
ok = True
for name in mods:
    try:
        mod = __import__(name)
        print(name, "OK", getattr(mod, "__version__", ""))
    except Exception as exc:
        ok = False
        print(name, "MISSING", type(exc).__name__, str(exc)[:160])
raise SystemExit(0 if ok else 2)
PY
status=$?
set -e

if [[ "$status" != "0" ]]; then
  cat <<EOF
[blocked] node22 is reachable but the requested RAG Python environment is not ready.

Prepare node22 first, for example:
  ssh $NODE22 'python3 -m venv /home/amd/venv-rag'
  ssh $NODE22 '/home/amd/venv-rag/bin/pip install numpy torch faiss-cpu FlagEmbedding transformers'

Then rerun:
  NODE22=$NODE22 REMOTE_PY=$REMOTE_PY $0

The script intentionally does not install packages automatically, because that is
an external environment mutation. Use node36 stable rebuild meanwhile:
  $PROJECT_ROOT/scripts/rag_rebuild_maofield_36.sh
EOF
  exit 2
fi

echo "[prepare] remote workspace $REMOTE_ROOT"
ssh "$NODE22" "mkdir -p '$REMOTE_ROOT/rag' '$REMOTE_ROOT/out'"

echo "[sync] RAG scripts/model subset to node22"
rsync -a --delete \
  "$RAG_ROOT/build_index.py" \
  "$RAG_ROOT/chunk_md.py" \
  "$RAG_ROOT/kb_search.py" \
  "$RAG_ROOT/models" \
  "$NODE22:$REMOTE_ROOT/rag/"

echo "[sync] project markdown snapshot to node22"
rsync -a --delete \
  --include='*/' \
  --include='*.md' \
  --exclude='*' \
  "$PROJECT_ROOT/" \
  "$NODE22:$REMOTE_ROOT/MaoField/"

cat <<EOF
[ready] node22 workspace prepared, but build_index.py currently hardcodes
/media/amd/raid1/rag/models/bge-m3. Either mount/symlink that path on node22 or
run the stable node36 rebuild. This runner is left as the controlled handoff
point for future node22 GPU vectorization.
EOF
