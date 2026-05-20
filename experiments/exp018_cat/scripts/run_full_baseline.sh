#!/usr/bin/env bash
# run_full_baseline.sh — Shumailov baseline 完整运行: 2 condition × 3 seed × 10 generation.
#
# 估时 (RX 9070 XT 16GB FP16, 与 llama-server 共享):
#   no_preserve: 5 epoch × 10 generation × ~3min train + ~2min generate = ~50min/seed
#   preserve_10pct: 10 epoch × 10 generation × ~6min train + ~2min generate = ~80min/seed
#   总计: 3 seed × (50 + 80) = ~6.5 GPU-hour
#
# 注: 如果 22 主机 GPU 真只剩 5.6GB (4 个 llama-server 占 10.4GB), 实际可能 OOM.
#     先跑 smoke-test 通了再考虑全跑.

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/HEZIMENG/MaoField/experiments/exp018_cat}"
VENV_DIR="${VENV_DIR:-$PROJECT_ROOT/.venv}"

cd "$PROJECT_ROOT"

# shellcheck disable=SC1091
if [[ -f "$VENV_DIR/bin/activate" ]]; then
  source "$VENV_DIR/bin/activate"
fi

SEEDS=(42 1337 2024)
CONDITIONS=(no_preserve preserve_10pct)

mkdir -p logs

for seed in "${SEEDS[@]}"; do
  for cond in "${CONDITIONS[@]}"; do
    echo ""
    echo "============================================================"
    echo "[FULL] condition=$cond seed=$seed"
    echo "============================================================"
    python src/shumailov_replication.py \
        --condition "$cond" \
        --seed "$seed" \
        2>&1 | tee -a "logs/full_run_${cond}_seed${seed}.txt"
  done
done

echo ""
echo "[FULL 完成] 全部 6 run 结束. 下一步: 跑分析脚本聚合 jsonl."
echo "  python src/analyze_collapse.py --logs-dir logs/"
echo "(注: analyze_collapse.py 是 exp018_cat 主目录的, 不属于本 baseline 复现)"
