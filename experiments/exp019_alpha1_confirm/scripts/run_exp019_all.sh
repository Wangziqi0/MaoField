#!/bin/bash
# exp019 orchestrator — runs on 22, sequential, 12 chains, balanced interleaved arm order.
# PRE-LOCK CHECKLIST must be green + PI signature before launching this.
# Arm order table v2 (balanced 3+3, random.seed(20260610) shuffle, committed pre-LOCK):
#   seed 101: alpha1 first | 102: alpha1 first | 103: alpha0 first
#   seed 104: alpha0 first | 105: alpha0 first | 106: alpha1 first
set -euo pipefail
cd ~/HEZIMENG/MaoField/experiments/exp018_cat
export HIP_VISIBLE_DEVICES=0 HF_HUB_OFFLINE=1 HF_DATASETS_OFFLINE=1
MAN=/tmp/exp019_run/manifests; LOG=/tmp/exp019_run/logs; mkdir -p "$MAN" "$LOG"
WRAP=../exp019_alpha1_confirm/scripts/exp019_launch_chain.py   # synced from 36 repo
RSYNC_DST="192.168.31.36:/media/amd/raid1/canonical/wip/exp019_alpha1_confirm_run/raw"

declare -A FIRST=( [101]=1.0 [102]=1.0 [103]=0.0 [104]=0.0 [105]=0.0 [106]=1.0 )
ORDER_IDX=0
for SEED in 101 102 103 104 105 106; do
  A_FIRST=${FIRST[$SEED]}
  if [ "$A_FIRST" = "1.0" ]; then A_SECOND=0.0; else A_SECOND=1.0; fi
  for ALPHA in "$A_FIRST" "$A_SECOND"; do
    ORDER_IDX=$((ORDER_IDX+1))
    # gen0 construction guarantee: second arm copies first arm gen0 (runner resume skips it)
    FIRST_G0="data/checkpoints_armb/alpha${A_FIRST}/no_preserve_seed${SEED}/generation_0"
    THIS_G0="data/checkpoints_armb/alpha${ALPHA}/no_preserve_seed${SEED}/generation_0"
    if [ "$ALPHA" = "$A_SECOND" ] && [ -d "$FIRST_G0" ] && [ ! -d "$THIS_G0" ]; then
      mkdir -p "$(dirname "$THIS_G0")" && cp -r "$FIRST_G0" "$THIS_G0"
      echo "[orch] seed $SEED: gen0 copied ${A_FIRST}->${ALPHA}" | tee -a "$LOG/orch.log"
    fi
    echo "[orch] chain $ORDER_IDX/12: alpha=$ALPHA seed=$SEED start $(date -Is)" | tee -a "$LOG/orch.log"
    .venv/bin/python "$WRAP" --alpha "$ALPHA" --seed "$SEED" --order-index "$ORDER_IDX" \
        --manifest-dir "$MAN" > "$LOG/chain_a${ALPHA}_s${SEED}.log" 2>&1
    # per-chain rescue rsync (D34): jsonl + manifests + ckpt
    rsync -a logs/armb_alpha${ALPHA}_seed${SEED}_*.jsonl "$MAN"/ "$RSYNC_DST/" 2>>"$LOG/orch.log" || true
    rsync -a "data/checkpoints_armb/alpha${ALPHA}/no_preserve_seed${SEED}" \
        "$RSYNC_DST/ckpt_alpha${ALPHA}/" 2>>"$LOG/orch.log" || true
    echo "[orch] chain $ORDER_IDX/12 done $(date -Is)" | tee -a "$LOG/orch.log"
  done
done
echo "[orch] ALL 12 CHAINS DONE $(date -Is)" | tee -a "$LOG/orch.log"
