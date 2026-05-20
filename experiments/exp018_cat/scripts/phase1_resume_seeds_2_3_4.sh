#!/usr/bin/env bash
# phase1_resume_seeds_2_3_4.sh — resume Phase 1 chain after seed=2 launch crash
#
# Background:
#   - 5/9 20:36 phase1_paper_seeds_chain.sh launched seeds [0, 1, 2, 3, 4]
#   - seed=0 done 5/10 01:10 (4h34m)
#   - seed=1 done 5/10 05:44 (4h33m)
#   - seed=2 launch 5/10 05:44 → 立刻 hipErrorIllegalAddress 核心转储 (GPU 切换瞬间 stuck state)
#   - chain `set -euo pipefail` 退出 at seed=2
#   - GPU smoke test passed (5/10 verify), GPU 状态可用
#
# 5/10 凌晨 PI ack "极度严谨" — 不留 broken chain
# 此 script 重 launch seeds [2, 3, 4] sequential, 1 seed crash 不阻塞下一个 (改 || true)
# 总: 3 seeds × ~4h35m = ~14h GPU
# 完成 ETA: 5/10 早 launch + 14h = 5/10 晚 ~20:00 (与原 chain ETA 21:30 接近)

set -uo pipefail   # 改: 不用 -e (不让 1 seed crash kill 整 chain), 但保 -uo

PROJECT_ROOT="${PROJECT_ROOT:-/home/amd/HEZIMENG/MaoField/experiments/exp018_cat}"
cd "$PROJECT_ROOT"

RESUME_SEEDS=(2 3 4)
TS=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="logs/phase1_resume_${TS}.master.log"

mkdir -p logs

echo "=== Phase 1 RESUME chain start ===" | tee -a "$MASTER_LOG"
echo "TS=$TS  resume seeds=${RESUME_SEEDS[*]}" | tee -a "$MASTER_LOG"

for SEED in "${RESUME_SEEDS[@]}"; do
  RUN_LOG="logs/phase1_paper_seed${SEED}_resume_${TS}.log"
  echo "" | tee -a "$MASTER_LOG"
  echo "[$(date)] starting SEED=$SEED → $RUN_LOG" | tee -a "$MASTER_LOG"

  env HF_ENDPOINT=https://hf-mirror.com \
      HIP_VISIBLE_DEVICES=0 \
      CUDA_VISIBLE_DEVICES=0 \
      .venv/bin/python src/run_arm_b_alpha_scan.py \
        --config configs/cat_arm_b.yaml \
        --alpha 0.0 \
        --seed "$SEED" \
        --num-generations 10 \
        > "$RUN_LOG" 2>&1

  RC=$?
  if [ $RC -ne 0 ]; then
    echo "[$(date)] !!! SEED=$SEED FAILED with rc=$RC, log: $RUN_LOG !!!" | tee -a "$MASTER_LOG"
    echo "[$(date)] continuing to next seed (single failure 不 kill chain)" | tee -a "$MASTER_LOG"
    # GPU smoke recovery before next seed
    sleep 10
  else
    echo "[$(date)] SEED=$SEED done" | tee -a "$MASTER_LOG"
  fi
done

echo "" | tee -a "$MASTER_LOG"
echo "=== Phase 1 RESUME chain done. Status check: ===" | tee -a "$MASTER_LOG"
for SEED in "${RESUME_SEEDS[@]}"; do
  N_DONE=$(grep -c "generation_done" "logs/armb_alpha0.0_seed${SEED}_*.jsonl" 2>/dev/null || echo "0")
  echo "  seed=$SEED: $N_DONE/10 generations done" | tee -a "$MASTER_LOG"
done

echo "[$(date)] Phase 1 RESUME chain complete." | tee -a "$MASTER_LOG"
