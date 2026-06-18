#!/bin/bash
# exp020 round3 Stage-A 自主队列: 2×2 析因 × {seed1,seed42}, 串行单 GPU。
# B0 cell (base-prev) 从既有 checkpoints_armb_ABL_baseprev resume。autonomous: 生存会话死亡。
cd ~/HEZIMENG/MaoField/experiments/exp018_cat
run() {  # $1 seed  $2 cellname  $3 base-mode  $4 prompt-mode  $5 outdir
  echo "=== EXP020_STAGEA s$1 cell=$2 base=$3 prompt=$4 START $(date +%H:%M:%S) ==="
  HIP_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 .venv/bin/python exp020_ablation_launch.py \
    --seed "$1" --base-mode "$3" --prompt-mode "$4" --output-base "data/$5" \
    --num-generations 10 --manifest-dir round3_manifests
  echo "=== EXP020_STAGEA s$1 cell=$2 DONE $(date +%H:%M:%S) ==="
}
for s in 1 42; do
  run "$s" 00 gen0 real      checkpoints_armb_ABL_00
  run "$s" B0 prev real      checkpoints_armb_ABL_baseprev
  run "$s" 0A gen0 synthetic checkpoints_armb_ABL_0A
  run "$s" BA prev synthetic checkpoints_armb_ABL_BA
done
echo EXP020_STAGEA_ALLDONE
