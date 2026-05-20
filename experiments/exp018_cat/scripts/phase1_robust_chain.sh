#!/usr/bin/env bash
# phase1_robust_chain.sh — Phase 1 with auto-restart resume logic
#
# 5/10 PI ack Option β + 4 caveats (binding):
#   (1) auto-restart logic 严格 (resume not restart), jsonl crash log audit trail
#   (2) 5/9 chain α=0 seed 0/1 数据 yaml_setup_hash explicit verify same setup 才能 stack
#   (3) D4 早 Phase 1 verdict 二元 binary, 数据驱动 framing 决策
#   (4) D3-D4 framework 冻结, fp32/batch 等 D5-6 sequencing 内做
#
# Linux dispatch §1 #2: 旧 framework α=0+10 multi-seed (PI 5/9 ack Option A 改 paper convention seeds)
#   - alphas: [0, 10] (caveat 1 binding 补 Linux 漏的 α=10 multi-seed)
#   - seeds:  [0, 1, 2, 3, 4] paper convention (PI 5/9 ack Option A)
#   - setup:  fp16 batch=128 (rolled back per caveat 4 framework freeze)
#
# Total: 10 jobs × ~5h = ~50h GPU sequential
# (但 5/9 chain 已有 α=0 seed=0/1 数据可 stack-skip via resume logic = 实际 ~45h)
#
# Crash policy (caveat 1):
#   - rc != 0 → log to AUDIT_JSONL, sleep 30s, GPU smoke verify, retry same (seed, alpha)
#   - Max 3 retry per (seed, alpha) — avoid infinite loop
#   - resume logic in run_arm_b_alpha_scan.py auto-skips completed gens
#   - Single seed 3-time-fail → log + skip to next seed (don't kill chain)

set -uo pipefail   # not -e (single-job fail 不 kill chain)

PROJECT_ROOT="${PROJECT_ROOT:-/home/amd/HEZIMENG/MaoField/experiments/exp018_cat}"
cd "$PROJECT_ROOT"

ALPHAS=(0.0 10.0)
SEEDS=(0 1 2 3 4)
MAX_RETRY=3
TS=$(date +%Y%m%d_%H%M%S)
MASTER_LOG="logs/phase1_robust_${TS}.master.log"
AUDIT_JSONL="logs/phase1_robust_${TS}.audit.jsonl"

mkdir -p logs

log_event() {
    # log_event "event_name" "key=val key=val ..."
    local evt="$1"; shift
    local kv="$@"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"ts\":\"$now\",\"event\":\"$evt\",$kv}" >> "$AUDIT_JSONL"
    echo "[$(date '+%F %T')] $evt $kv" | tee -a "$MASTER_LOG"
}

gpu_smoke() {
    env HF_ENDPOINT=https://hf-mirror.com HIP_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 \
        .venv/bin/python -c "
import torch
torch.cuda.set_device(0)
x = torch.randn(1000, 1000, device='cuda')
y = x @ x.T
del x, y; torch.cuda.empty_cache()
print('SMOKE_PASS')
" 2>&1 | tail -1
}

log_event "chain_start" "ts=\"$TS\" alphas=\"${ALPHAS[*]}\" seeds=\"${SEEDS[*]}\" max_retry=$MAX_RETRY"

for ALPHA in "${ALPHAS[@]}"; do
    for SEED in "${SEEDS[@]}"; do
        ATTEMPT=0
        SUCCESS=0
        while [ $ATTEMPT -lt $MAX_RETRY ]; do
            ATTEMPT=$((ATTEMPT + 1))
            RUN_LOG="logs/phase1_robust_alpha${ALPHA}_seed${SEED}_attempt${ATTEMPT}_${TS}.log"
            log_event "job_start" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT log=\"$RUN_LOG\""

            env HF_ENDPOINT=https://hf-mirror.com \
                HIP_VISIBLE_DEVICES=0 \
                CUDA_VISIBLE_DEVICES=0 \
                .venv/bin/python src/run_arm_b_alpha_scan.py \
                  --config configs/cat_arm_b.yaml \
                  --alpha "$ALPHA" \
                  --seed "$SEED" \
                  --num-generations 10 \
                  > "$RUN_LOG" 2>&1
            RC=$?

            # Count completed gens from latest jsonl
            LATEST_JSONL=$(ls -t logs/armb_alpha${ALPHA}_seed${SEED}_*.jsonl 2>/dev/null | head -1)
            N_COMPLETED=0
            if [ -n "$LATEST_JSONL" ]; then
                N_COMPLETED=$(grep -c "generation_done" "$LATEST_JSONL" 2>/dev/null || echo 0)
            fi

            if [ $RC -eq 0 ] && [ $N_COMPLETED -eq 10 ]; then
                log_event "job_done" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT n_gens=$N_COMPLETED rc=$RC"
                SUCCESS=1
                break
            else
                log_event "job_fail" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT n_gens=$N_COMPLETED rc=$RC log=\"$RUN_LOG\""
                # GPU smoke before retry
                sleep 30
                SMOKE=$(gpu_smoke)
                log_event "post_fail_smoke" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT smoke=\"$SMOKE\""
                if [[ "$SMOKE" != *"SMOKE_PASS"* ]]; then
                    log_event "smoke_fail_abort_seed" "alpha=$ALPHA seed=$SEED"
                    break
                fi
            fi
        done

        if [ $SUCCESS -eq 0 ]; then
            log_event "seed_skipped" "alpha=$ALPHA seed=$SEED final_attempt=$ATTEMPT n_completed=$N_COMPLETED"
        fi
    done
done

log_event "chain_done" "audit=\"$AUDIT_JSONL\""

# 终极 status summary
echo "" >> "$MASTER_LOG"
echo "=== FINAL STATUS ===" >> "$MASTER_LOG"
for ALPHA in "${ALPHAS[@]}"; do
    for SEED in "${SEEDS[@]}"; do
        LATEST_JSONL=$(ls -t logs/armb_alpha${ALPHA}_seed${SEED}_*.jsonl 2>/dev/null | head -1)
        N=0
        if [ -n "$LATEST_JSONL" ]; then
            N=$(grep -c "generation_done" "$LATEST_JSONL" 2>/dev/null || echo 0)
        fi
        echo "  alpha=$ALPHA seed=$SEED: $N/10 generations done" >> "$MASTER_LOG"
    done
done
