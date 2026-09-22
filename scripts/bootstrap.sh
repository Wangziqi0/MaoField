#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
ASSETS="${MAOFIELD_ASSETS:-$ROOT/../RELEASE_ASSETS}"
MODE="${1:---full}"
case "$MODE" in --full|--analysis-only) ;; *) echo "Usage: ./reproduce.sh [--full|--analysis-only]"; exit 2;; esac
[ "$(uname -s)" = Linux ] && [ "$(uname -m)" = x86_64 ] || { echo 'Packaged runtime requires Linux x86_64.'; exit 2; }
for cmd in tar sha256sum git; do command -v "$cmd" >/dev/null || { echo "Missing host prerequisite: $cmd"; exit 2; }; done
if [ "$MODE" = --full ]; then
  for cmd in bwrap zstd; do command -v "$cmd" >/dev/null || { echo "Missing host prerequisite: $cmd (install bubblewrap and zstd)."; exit 2; }; done
fi
cd "$ROOT"
mkdir -p WORK/environment
check_asset() {
  local name="$1" expected actual
  expected="$(awk -v n="$name" '$2==n {print $1}' environment/SHA256SUMS)"
  [ -n "$expected" ] || { echo "No pinned checksum: $name"; exit 2; }
  [ -f "$ASSETS/$name" ] || { echo "Place the release asset $name in $ASSETS, or set MAOFIELD_ASSETS."; exit 2; }
  actual="$(sha256sum "$ASSETS/$name")"; actual="${actual%% *}"
  [ "$actual" = "$expected" ] || { echo "Checksum mismatch: $name"; exit 2; }
}
check_asset python-linux-x86_64.tar.gz
if [ ! -f WORK/environment/.python-ready ]; then
  tar -xzf "$ASSETS/python-linux-x86_64.tar.gz" -C WORK/environment
  touch WORK/environment/.python-ready
fi
if [ "$MODE" = --full ]; then
  if [ ! -f "$ASSETS/lean-offline-linux-x86_64.tar.zst" ]; then
    (cd "$ASSETS" && sha256sum -c "$ROOT/environment/LEAN_PARTS.sha256")
    cat "$ASSETS/lean-offline-linux-x86_64.tar.zst.part00" "$ASSETS/lean-offline-linux-x86_64.tar.zst.part01" > WORK/environment/lean-offline-linux-x86_64.tar.zst
    LEAN_ASSET="$ROOT/WORK/environment/lean-offline-linux-x86_64.tar.zst"
    expected="$(awk '$2=="lean-offline-linux-x86_64.tar.zst" {print $1}' environment/SHA256SUMS)"
    actual="$(sha256sum "$LEAN_ASSET")"; actual="${actual%% *}"
    [ "$actual" = "$expected" ] || { echo 'Joined Lean asset checksum mismatch'; exit 2; }
  else
    check_asset lean-offline-linux-x86_64.tar.zst
    LEAN_ASSET="$ASSETS/lean-offline-linux-x86_64.tar.zst"
  fi
  if [ ! -f WORK/environment/.lean-ready ]; then
    tar --zstd -xf "$LEAN_ASSET" -C WORK/environment
    touch WORK/environment/.lean-ready
  fi
fi
exec "$ROOT/WORK/environment/python/bin/python3" "$ROOT/scripts/run_all.py" "$MODE"
