#!/usr/bin/env bash
# phase1_paper_seeds_chain.sh — Phase 1 paper-convention 5-seed Shumailov mirror
#
# 5/10 凌晨 PI ack Option A (binding "不能错" + "极度严谨"):
#   - 弃用 historical seed=42 runs (deterministic re-runs 不 add information)
#   - 跑 paper convention 5 seeds [0, 1, 2, 3, 4]
#   - 严格 audit-fixed setup (batch=128, lr_const, weight_decay=0.01, fp16, rep_penalty=3.0)
#   - alpha=0 baseline only (CAT disabled)
#   - cat_arm_b.yaml (already audit-fixed) + run_arm_b_alpha_scan.py --alpha 0.0 --seed N
#
# 估时: 5 seeds × 10 generations × ~30 min/gen = ~25 GPU hours sequential
# (RX 9070 XT 22 主机, fp16, batch=128 effective)
#
# paper §6 disclose: "5 seeds (paper convention 0-4), 严格按 official Shumailov 2024 Zenodo
#   (DOI 10.5281/zenodo.10866595): batch=128, AdamW lr=2e-5, weight_decay=0.01, constant
#   schedule, 5 epochs/generation, block_size=64, 5-beam search rep_penalty=3.0,
#   max_new_tokens=64, fp16."

set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/home/amd/HEZIMENG/MaoField/experiments/exp018_cat}"

cd "$PROJECT_ROOT"

PAPER_SEEDS=(0 1 2 3 4)
TS=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="logs/phase1_paper_seeds_chain_${TS}.master.log"

mkdir -p logs

echo "=== Phase 1 paper-convention seeds chain start ===" | tee -a "$MASTER_LOG"
echo "TS=$TS  seeds=${PAPER_SEEDS[*]}" | tee -a "$MASTER_LOG"
echo "estimated: 25h GPU sequential" | tee -a "$MASTER_LOG"

for SEED in "${PAPER_SEEDS[@]}"; do
  RUN_LOG="logs/phase1_paper_seed${SEED}_${TS}.log"
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
    echo "[$(date)] !!! SEED=$SEED FAILED with rc=$RC, abort chain !!!" | tee -a "$MASTER_LOG"
    exit $RC
  fi
  echo "[$(date)] SEED=$SEED done" | tee -a "$MASTER_LOG"
done

echo "" | tee -a "$MASTER_LOG"
echo "=== Phase 1 chain done. 5 seeds × 10 gen complete. ===" | tee -a "$MASTER_LOG"
echo "[$(date)] all 5 paper-convention seeds done" | tee -a "$MASTER_LOG"
echo "next: refit m_eff with 5-seed data, multi-seed verdict" | tee -a "$MASTER_LOG"
