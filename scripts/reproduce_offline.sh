#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python "$ROOT/scripts/verify_release.py"
python "$ROOT/src/analysis/offline_reproduce.py"
echo "Offline reproduction complete: $ROOT/outputs"
