#!/usr/bin/env bash
# run_baseline_smoke_test.sh — pipeline smoke test, 验证整套代码通.
#
# 内容: 1 generation + 1 epoch + 32 行训练数据 + 16 行验证 + 16 行测试
# 估时: ~3-5 min on RX 9070 XT
# 不目的: 验证 Shumailov 数字 (smoke 太短不可能), 只目的 验证代码无 import error / runtime error / OOM

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-$HOME/HEZIMENG/MaoField/experiments/exp018_cat}"
VENV_DIR="${VENV_DIR:-$PROJECT_ROOT/.venv}"

cd "$PROJECT_ROOT"

# shellcheck disable=SC1091
if [[ -f "$VENV_DIR/bin/activate" ]]; then
  source "$VENV_DIR/bin/activate"
else
  echo "WARN: venv 不存在 ($VENV_DIR), 用系统 python"
fi

# RDNA 4 (gfx1201) 在某些 ROCm 版本上需要 override
# 主 Linux 姐姐: 跑前先确认是否需要 export
# export HSA_OVERRIDE_GFX_VERSION=11.0.0

echo "[smoke 1/2] no_preserve, seed=42, 1 generation, smoke-test 模式"
python src/shumailov_replication.py \
    --condition no_preserve \
    --seed 42 \
    --smoke-test

echo ""
echo "[smoke 2/2] preserve_10pct, seed=42, 1 generation, smoke-test 模式"
python src/shumailov_replication.py \
    --condition preserve_10pct \
    --seed 42 \
    --smoke-test

echo ""
echo "[smoke 完成] 检查 logs/ 下输出 jsonl, 验证 generation_done + falsification_check 都被写入."
echo "若 OK, 下一步 bash scripts/run_full_baseline.sh"
