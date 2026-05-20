#!/usr/bin/env bash
# sync_to_22.sh — 把 7B13 端 exp018_cat 代码 rsync 到 22 主机.
# 不同步 data/checkpoints (大), 不同步 logs (避免覆盖).

set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-amd@192.168.31.22}"
REMOTE_PATH="${REMOTE_PATH:-/home/amd/HEZIMENG/MaoField/experiments/exp018_cat}"
LOCAL_PATH="${LOCAL_PATH:-$HOME/HEZIMENG/MaoField/experiments/exp018_cat}"

echo "sync $LOCAL_PATH/ → $REMOTE_HOST:$REMOTE_PATH/"

# 远端建目录
ssh "$REMOTE_HOST" "mkdir -p $REMOTE_PATH/{src,configs,scripts,logs,data,results,literature,figures}"

# rsync 代码 (排除 data/checkpoints, logs, __pycache__, .venv)
rsync -av --progress \
    --exclude="data/checkpoints/" \
    --exclude="data/datasets/" \
    --exclude="logs/" \
    --exclude="__pycache__/" \
    --exclude="*.pyc" \
    --exclude=".venv/" \
    --exclude="results/raw/" \
    "$LOCAL_PATH/" "$REMOTE_HOST:$REMOTE_PATH/"

echo "[完成] sync 结束. 下一步在 22 主机:"
echo "  ssh $REMOTE_HOST"
echo "  cd $REMOTE_PATH"
echo "  bash scripts/install_rocm_torch.sh   # 首次"
echo "  bash scripts/run_baseline_smoke_test.sh"
