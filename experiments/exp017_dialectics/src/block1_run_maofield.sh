#!/bin/bash
# Run MaoField baseline (exp015) + variant E (exp016 variant_A = FUSION=0) on
# fiqa, arguana, trec-covid. Sequential per binary to avoid contention; each binary
# already uses full CPU threads.
set -e
EXP17=/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics
BASE_BIN=/home/amd/HEZIMENG/MaoField/experiments/exp015/rust_solver/target/release/exp015_solver
E_BIN=/home/amd/HEZIMENG/MaoField/experiments/exp016_diagnostic/rust_variants/variant_A/target/release/variant_a_solver

LOG=$EXP17/logs/block1
OUT=$EXP17/results/block1
mkdir -p $LOG $OUT

for DS in fiqa arguana trec-covid; do
  IN_100=$EXP17/inputs_block1/${DS}_stage1_input.json
  IN_20=$EXP17/inputs_block1_top20/${DS}_top20_input.json

  OUT_BASE=$OUT/${DS}_maofield_baseline_out.json
  OUT_E=$OUT/${DS}_maofield_E_out.json

  if [ ! -f "$OUT_BASE" ]; then
    echo "=== [$(date +%H:%M:%S)] MaoField baseline on $DS ==="
    $BASE_BIN "$IN_100" "$OUT_BASE" > $LOG/${DS}_maofield_baseline.log 2>&1
    echo "  done $DS baseline"
  else
    echo "skip $DS baseline (exists)"
  fi

  if [ ! -f "$OUT_E" ]; then
    echo "=== [$(date +%H:%M:%S)] MaoField-E on $DS ==="
    $E_BIN "$IN_20" "$OUT_E" > $LOG/${DS}_maofield_E.log 2>&1
    echo "  done $DS E"
  else
    echo "skip $DS E (exists)"
  fi
done

echo "=== All MaoField runs complete $(date +%H:%M:%S) ==="
