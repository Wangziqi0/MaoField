#!/usr/bin/env bash
# phase5_launch_script_20260517.sh
# =============================================================================
# Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 一键 launch script
#
# 用途: RunPod A100 80GB community spot 容器内, 一凡 SSH 进 pod 后运行此脚本
#       自动完成: env verify → HF login → model+数据下载 → code 配置 → smoke →
#       α=0 chain (Day 2) → α=10 chain (Day 3) → 必要时 fallback
#
# 派遣 / 协作:
#   Linux 姐姐 D-2 实验线 first wave sub-agent (D17 = 2026-05-17)
#   Design doc: experiments/exp018_cat/literature/PHASE5_LLAMA8B_DESIGN_20260516.md
#   v1.0 code base: experiments/exp018_cat/archive/v1.0_release_20260516/
#
# D-1 binding:
#   - N=1 single-seed indicative only, 不 establish framework effect
#   - $50 floor / $51-80 真实区间 / 任何 spot kick + OOM debug 可能破 $50
#   - 不 launch GPU until 一凡 manually verify §8.1 全 checklist done
#   - 任一 unverifiable / 估计 → 标 [?]
#
# 一凡侧 pre-launch checklist 必读: PHASE5_LAUNCH_CHECKLIST_20260517.md
#
# 使用 examples:
#   阶段 0 (env verify only, no GPU spend):
#       bash phase5_launch_script_20260517.sh --stage env_verify
#   阶段 1 (setup + smoke, ~2.5h GPU ≈ $4.73):
#       bash phase5_launch_script_20260517.sh --stage setup
#   阶段 2 (α=0 baseline chain, ~10h GPU ≈ $18.90):
#       bash phase5_launch_script_20260517.sh --stage chain --alpha 0.0 --seed 42
#   阶段 3 (α=10 framework chain, ~11-12h GPU ≈ $20.79-22.68):
#       bash phase5_launch_script_20260517.sh --stage chain --alpha 10.0 --seed 42
#   阶段 4 (post-run sliding-window eval + S3 backup):
#       bash phase5_launch_script_20260517.sh --stage postrun
# =============================================================================

set -uo pipefail   # 不用 -e: 单 job fail 不 kill 整个流程, 由 retry logic 处理

# ----------------------------- 默认参数 ---------------------------------------

STAGE="${1:-}"   # 一凡可不传, 默认进入 interactive prompt
ALPHA=""
SEED=42
NUM_GENS=10
MAX_RETRY=3
WORKSPACE="${WORKSPACE:-/workspace}"
REPO_DIR="${REPO_DIR:-${WORKSPACE}/exp018_cat}"
HF_CACHE="${HF_CACHE:-${WORKSPACE}/data/checkpoints/hf_cache_llama}"
DATASET_CACHE="${DATASET_CACHE:-${WORKSPACE}/data/datasets}"
LOG_DIR="${LOG_DIR:-${WORKSPACE}/logs/phase5_llama8b}"
S3_BUCKET="${S3_BUCKET:-}"   # 一凡 .env 注入, 例: s3://maofield-phase5/
TS=$(date -u +"%Y%m%d_%H%M%SZ")

# parse CLI 参数
while [[ $# -gt 0 ]]; do
    case "$1" in
        --stage) STAGE="$2"; shift 2 ;;
        --alpha) ALPHA="$2"; shift 2 ;;
        --seed) SEED="$2"; shift 2 ;;
        --num-gens) NUM_GENS="$2"; shift 2 ;;
        --max-retry) MAX_RETRY="$2"; shift 2 ;;
        --workspace) WORKSPACE="$2"; shift 2 ;;
        *) shift ;;
    esac
done

mkdir -p "$LOG_DIR"

MASTER_LOG="${LOG_DIR}/phase5_launch_${TS}.master.log"
AUDIT_JSONL="${LOG_DIR}/phase5_launch_${TS}.audit.jsonl"

# ----------------------------- 日志 helpers -----------------------------------

log_event() {
    # log_event "event_name" "key=val key=val ..."
    local evt="$1"; shift
    local kv="$@"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"ts\":\"$now\",\"event\":\"$evt\",$kv}" >> "$AUDIT_JSONL"
    echo "[$(date '+%F %T')] $evt $kv" | tee -a "$MASTER_LOG"
}

log_info() { echo "[INFO  $(date '+%F %T')] $*" | tee -a "$MASTER_LOG"; }
log_warn() { echo "[WARN  $(date '+%F %T')] $*" | tee -a "$MASTER_LOG"; }
log_err()  { echo "[ERROR $(date '+%F %T')] $*" | tee -a "$MASTER_LOG"; }

# ----------------------------- 0. env verify ----------------------------------
# 不消耗 GPU, 仅 verify pod 已就绪 (一凡 SSH 进 pod 后第一步)

env_verify() {
    log_info "===== env_verify 开始 (no GPU spend) ====="

    # 0.1 verify CUDA + GPU device
    if ! command -v nvidia-smi &>/dev/null; then
        log_err "nvidia-smi 不可用; A100 driver 未装. abort"
        return 1
    fi
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader)
    log_info "GPU: ${GPU_INFO}"
    # binary check: 是否 A100 80GB (substring "A100" + ">=80000 MiB")
    if [[ "${GPU_INFO}" != *"A100"* ]]; then
        log_warn "GPU 不是 A100 ([?] design 强 recommend A100 80GB, 当前=${GPU_INFO})"
        log_warn "  → A100 40GB EMA model OOM 高 (R3 ~40% prob); 4090 24GB 必须走 LoRA fallback"
    fi
    MEM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    if [ "$MEM_MB" -lt 75000 ]; then
        log_warn "GPU memory ${MEM_MB} MiB < 75 GiB; design 要 A100 80GB primary"
        log_warn "  → 若坚持 40GB, 须切 LoRA path (chain consistency 弱化, paper §7.5 必须 disclose)"
    fi

    # 0.2 verify Python + key libs
    if ! command -v python3 &>/dev/null; then
        log_err "python3 不可用; abort"
        return 1
    fi
    PY_VER=$(python3 --version 2>&1)
    log_info "Python: ${PY_VER}"

    # 0.3 verify disk 足够 (Llama 8B fp16 ≈ 16 GB + 10 gen checkpoints × 2 α ≈ 320 GB worst)
    DISK_AVAIL_GB=$(df -BG "$WORKSPACE" | tail -1 | awk '{print $4}' | sed 's/G//')
    log_info "Workspace disk avail: ${DISK_AVAIL_GB} GB"
    if [ "${DISK_AVAIL_GB}" -lt 200 ]; then
        log_warn "Disk ${DISK_AVAIL_GB} GB < 200 GB; 10 gen × 2 α full checkpoint 可能不够"
        log_warn "  → 建议仅 keep gen 0 + gen 9 checkpoint (set save_strategy=no, post-run 手动 keep)"
    fi

    # 0.4 verify env vars 必备
    local missing=0
    for v in HF_TOKEN AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY; do
        if [ -z "${!v:-}" ]; then
            log_warn "env var $v 未 set"
            missing=1
        fi
    done
    if [ $missing -eq 1 ]; then
        log_warn "缺 env var, 见 PHASE5_LAUNCH_CHECKLIST_20260517.md §pre-launch"
        log_warn "  最小可启动: HF_TOKEN 必 set; AWS 仅 S3 backup 时用"
    fi

    # 0.5 verify network 到 huggingface
    if ! curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/api/models 2>/dev/null | grep -q "200\|301\|302"; then
        log_warn "无法访问 huggingface.co; 若在国内 mirror 走 hf-mirror.com (export HF_ENDPOINT=https://hf-mirror.com)"
    fi

    log_event "env_verify_done" "gpu=\"$GPU_INFO\" mem_mb=$MEM_MB disk_gb=$DISK_AVAIL_GB py=\"$PY_VER\""
    log_info "===== env_verify 完成. 下一步: --stage setup ====="
    return 0
}

# ----------------------------- 1. setup ---------------------------------------
# Day 1 (D23): HF login + model download + code repo + smoke test
# 预计 GPU ~2.5h ≈ $4.73 @ $1.89/h

setup() {
    log_info "===== setup 开始 (Day 1, GPU ~2.5h estimate) ====="
    log_event "setup_start" "ts=\"$TS\""

    # 1.1 HF login
    if [ -z "${HF_TOKEN:-}" ]; then
        log_err "HF_TOKEN 未 set; 一凡须 export HF_TOKEN=hf_xxx (一次性 token from huggingface.co/settings/tokens)"
        return 1
    fi
    log_info "huggingface-cli login (using HF_TOKEN env var)"
    huggingface-cli login --token "${HF_TOKEN}" --add-to-git-credential 2>&1 | tee -a "$MASTER_LOG"

    # 1.2 verify Llama-3.1 license accepted (HF 会 return 403 if not accepted)
    log_info "verify Llama-3.1-8B license accepted on HF"
    LICENSE_TEST=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: Bearer ${HF_TOKEN}" \
        "https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/config.json")
    if [ "$LICENSE_TEST" != "200" ]; then
        log_err "License check failed (HTTP $LICENSE_TEST). 一凡须先在 https://huggingface.co/meta-llama/Meta-Llama-3.1-8B 同意 license"
        log_err "  License auto-approve 通常 1h-2 天; abort. fallback 用 meta-llama/Llama-3.2-3B (更小 license 同 community 通常更快)"
        return 1
    fi
    log_info "License OK (HTTP $LICENSE_TEST)"

    # 1.3 download Llama-3.1-8B weights (~16 GB)
    log_info "download Llama-3.1-8B base model (~16 GB, 估 5-15 min on RunPod 1Gbps)"
    mkdir -p "$HF_CACHE"
    huggingface-cli download meta-llama/Meta-Llama-3.1-8B \
        --local-dir "${HF_CACHE}/Meta-Llama-3.1-8B" \
        --local-dir-use-symlinks False \
        2>&1 | tee -a "$MASTER_LOG"
    if [ ! -f "${HF_CACHE}/Meta-Llama-3.1-8B/config.json" ]; then
        log_err "Llama-3.1-8B download failed (config.json 缺); abort"
        return 1
    fi
    log_info "Llama-3.1-8B cached at ${HF_CACHE}/Meta-Llama-3.1-8B"

    # 1.4 download wikitext-2 dataset (~5 MB)
    log_info "download wikitext-2-raw-v1 dataset"
    mkdir -p "$DATASET_CACHE"
    python3 -c "
from datasets import load_dataset
ds = load_dataset('wikitext', 'wikitext-2-raw-v1', cache_dir='${DATASET_CACHE}')
print(f'train sequences: {len(ds[\"train\"])}')
print(f'val sequences:   {len(ds[\"validation\"])}')
print(f'test sequences:  {len(ds[\"test\"])}')
" 2>&1 | tee -a "$MASTER_LOG"

    # 1.5 verify exp018_cat repo (假设一凡已 git clone 或 rsync 进 RunPod)
    if [ ! -d "$REPO_DIR" ]; then
        log_err "exp018_cat 仓库未找到 at $REPO_DIR"
        log_err "  一凡须先 (本地 rsync 或 git clone):"
        log_err "    rsync -avz /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/ root@<pod_ip>:${REPO_DIR}/"
        log_err "  或从 v1.0 archive 解压:"
        log_err "    cp -r /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/archive/v1.0_release_20260516/ ${REPO_DIR}/"
        return 1
    fi
    log_info "repo found at ${REPO_DIR}"

    # 1.6 install Python deps
    log_info "install Python deps (transformers, accelerate, peft, datasets, jsonlines, scipy, matplotlib)"
    cd "$REPO_DIR" || return 1
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt 2>&1 | tee -a "$MASTER_LOG" | tail -30
    else
        log_warn "requirements.txt 缺; 用 minimal fallback"
        pip install transformers==4.46.0 accelerate datasets jsonlines numpy scipy matplotlib pyyaml 2>&1 | tee -a "$MASTER_LOG" | tail -10
    fi

    # 1.7 apply Phase 5 patches (D_n_code logging + Llama fp16 model loading)
    log_info "apply Phase 5 patches (D_n_code logging + Llama fp16 model loading)"
    apply_phase5_patches

    # 1.8 write phase5_llama8b_alpha_scan.yaml
    log_info "write configs/phase5_llama8b_alpha_scan.yaml"
    write_phase5_yaml

    # 1.9 smoke test (1 gen × 1 epoch × 32 train blocks, α=0)
    log_info "smoke test: 1 gen × 1 epoch × 32 train blocks, α=0"
    cd "$REPO_DIR" || return 1
    SMOKE_LOG="${LOG_DIR}/smoke_test_${TS}.log"
    HF_ENDPOINT="${HF_ENDPOINT:-https://huggingface.co}" \
    python3 src/run_arm_b_alpha_scan.py \
        --config configs/phase5_llama8b_alpha_scan.yaml \
        --alpha 0.0 \
        --seed 42 \
        --num-generations 1 \
        --smoke-test \
        > "$SMOKE_LOG" 2>&1
    SMOKE_RC=$?
    if [ $SMOKE_RC -eq 0 ]; then
        log_event "smoke_test_pass" "rc=$SMOKE_RC log=\"$SMOKE_LOG\""
        # binary verify D_n_code key 出现在 smoke jsonl
        SMOKE_JSONL=$(ls -t logs/armb_alpha0.0_seed42_*.jsonl 2>/dev/null | head -1)
        if [ -n "$SMOKE_JSONL" ] && grep -q "D_n_code" "$SMOKE_JSONL"; then
            log_info "smoke verify PASS: D_n_code key 出现在 jsonl"
        else
            log_warn "smoke verify WARN: D_n_code key NOT 出现在 jsonl; D_n logging patch 未生效, 见 apply_phase5_patches"
        fi
    else
        log_err "smoke test FAIL (rc=$SMOKE_RC); 详见 $SMOKE_LOG. abort setup"
        return 1
    fi

    log_event "setup_done" "ts=\"$TS\""
    log_info "===== setup 完成. 下一步: --stage chain --alpha 0.0 --seed 42 ====="
    return 0
}

# ----------------------------- 1.x Phase 5 patches ----------------------------
# 必须 patch 现有 v1.0 code 以适配 Llama-8B + D_n_code logging
#
# Patch 1: train_one_generation.py line ~102-105
#   原: torch_dtype=torch.float32  (8B model fp32 = 32 GB, A100 80GB OOM)
#   改: torch_dtype=torch.float16  (8B fp16 = 16 GB OK; fp16 mixed precision 仍由
#       Trainer fp16=True 自动管理; HF transformers 已支持 fp16 weights + fp16 mixed
#       Trainer 同存; 若报 "Attempting to unscale FP16 gradients" 错误, fallback 到 bf16
#       (caveat: bf16 偏离 chain consistency, paper §7.5 须 disclose))
#
# Patch 2: train_one_generation.py 结尾 + run_arm_b_alpha_scan.py log_record
#   原: TrainResult 无 D_n_code, jsonl log_record 无 D_n_code
#   改: TrainResult 加 final_D_n_code field; fine_tune_one_generation return 时
#       从 tracker.D_history[-1] 提 scalar (若 enabled);
#       run_arm_b_alpha_scan.py log_record() 加 D_n_code 字段
#
# 本 launch script 用 sed/patch 应用; PI 可 inspect 实际 diff (logged 在 master.log)

apply_phase5_patches() {
    local TRAIN_PY="${REPO_DIR}/src/train_one_generation.py"
    local CHAIN_PY="${REPO_DIR}/src/run_arm_b_alpha_scan.py"

    log_info "Patch 1: train_one_generation.py 改 model dtype torch.float32 → torch.float16 (8B fp32 OOM)"
    if grep -q "torch_dtype=torch.float32" "$TRAIN_PY"; then
        # backup 原文件
        cp "$TRAIN_PY" "${TRAIN_PY}.phase5_backup_${TS}"
        sed -i 's|torch_dtype=torch.float32,|torch_dtype=torch.float16,  # PHASE5 PATCH: Llama 8B fp32 OOM|g' "$TRAIN_PY"
        if grep -q "torch_dtype=torch.float16,  # PHASE5 PATCH" "$TRAIN_PY"; then
            log_info "  Patch 1 OK"
        else
            log_err "  Patch 1 FAIL; manual edit required"
            return 1
        fi
    else
        log_warn "  Patch 1 skipped (torch.float32 已不在 train_one_generation.py; 可能已 patch 过)"
    fi

    log_info "Patch 2: D_n_code logging — 加 TrainResult.final_D_n_code 字段 + log_record"
    # Patch 2a: TrainResult dataclass 加 final_D_n_code 字段
    if ! grep -q "final_D_n_code" "$TRAIN_PY"; then
        # 用 python 改写更安全 (sed 多行 dataclass dangerous)
        python3 <<EOF
import re
path = "$TRAIN_PY"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1) TrainResult dataclass 加 final_D_n_code field
old_pattern = '''@dataclass
class TrainResult:
    output_dir: str
    final_train_loss: float
    val_perplexity: float
    val_loss: float
    epoch_done: int'''

new_pattern = '''@dataclass
class TrainResult:
    output_dir: str
    final_train_loss: float
    val_perplexity: float
    val_loss: float
    epoch_done: int
    final_D_n_code: float = float("nan")  # PHASE5 PATCH: D_n^code scalar at gen end (NaN if CAT disabled)'''

if old_pattern in content:
    content = content.replace(old_pattern, new_pattern)
    print("Patch 2a OK: TrainResult.final_D_n_code added")
else:
    print("Patch 2a SKIP: TrainResult pattern not matched (可能已 patch 或 dataclass 形式变了)")

# 2) fine_tune_one_generation 末尾 return TrainResult 前, 提 tracker.D_history[-1]
# 找 "    # 释放 GPU 内存" pattern (Patch insert point before "del model, trainer")
patch_2b_old = '''    # 保存 final model (供下代使用)
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    logger.info(
        "fine-tune 完成: train_loss=%.4f val_loss=%.4f val_ppl=%.2f",
        final_train_loss, val_loss, val_ppl,
    )

    # 释放 GPU 内存
    del model, trainer'''

patch_2b_new = '''    # 保存 final model (供下代使用)
    trainer.save_model(str(output_dir))
    tokenizer.save_pretrained(str(output_dir))

    logger.info(
        "fine-tune 完成: train_loss=%.4f val_loss=%.4f val_ppl=%.2f",
        final_train_loss, val_loss, val_ppl,
    )

    # PHASE5 PATCH: 在 del model 之前从 tracker 提 final D_n scalar
    final_D_n_code = float("nan")
    if cat_config is not None and cat_config.enabled:
        try:
            # CATTrainer 实例上挂的 contradiction_tracker (cat_trainer.py)
            tracker_obj = getattr(trainer, "contradiction_tracker", None)
            if tracker_obj is not None and len(tracker_obj.D_history) > 0:
                final_D_n_code = float(tracker_obj.D_history[-1].item())
                logger.info("PHASE5 D_n_code (gen end) = %.6f", final_D_n_code)
            else:
                logger.warning("PHASE5 tracker.D_history empty; D_n_code = NaN")
        except Exception as e:
            logger.warning("PHASE5 D_n_code extract failed: %s", e)

    # 释放 GPU 内存
    del model, trainer'''

if patch_2b_old in content:
    content = content.replace(patch_2b_old, patch_2b_new)
    print("Patch 2b OK: D_n_code extraction added")
else:
    print("Patch 2b SKIP: insert point pattern not matched")

# 3) return TrainResult(..) 末加 final_D_n_code field
patch_2c_old = '''    return TrainResult(
        output_dir=str(output_dir),
        final_train_loss=final_train_loss,
        val_perplexity=val_ppl,
        val_loss=val_loss,
        epoch_done=epochs,
    )'''

patch_2c_new = '''    return TrainResult(
        output_dir=str(output_dir),
        final_train_loss=final_train_loss,
        val_perplexity=val_ppl,
        val_loss=val_loss,
        epoch_done=epochs,
        final_D_n_code=final_D_n_code,  # PHASE5 PATCH
    )'''

if patch_2c_old in content:
    content = content.replace(patch_2c_old, patch_2c_new)
    print("Patch 2c OK: TrainResult final_D_n_code populated")
else:
    print("Patch 2c SKIP: return pattern not matched")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
EOF
    else
        log_warn "  Patch 2a skipped (final_D_n_code 已在 train_one_generation.py; 可能已 patch 过)"
    fi

    # Patch 3: run_arm_b_alpha_scan.py log_record 加 D_n_code field
    log_info "Patch 3: run_arm_b_alpha_scan.py log_record 加 D_n_code"
    if ! grep -q "PHASE5.*D_n_code" "$CHAIN_PY"; then
        python3 <<EOF
path = "$CHAIN_PY"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 在 gen 0 + gen g log_record 双处加 D_n_code (从 gen0_result.final_D_n_code 和 gen_result.final_D_n_code)
# 找 "cat_enabled": False 上一行 + "cat_alpha": args.alpha 上一行 各插入 D_n_code
old1 = '''        "model_path": str(gen0_dir),
        "cat_enabled": False,  # gen 0 无 CAT
    })'''
new1 = '''        "model_path": str(gen0_dir),
        "cat_enabled": False,  # gen 0 无 CAT
        "D_n_code": gen0_result.final_D_n_code,  # PHASE5 PATCH: gen 0 无 CAT → NaN
    })'''
if old1 in content:
    content = content.replace(old1, new1)
    print("Patch 3a OK: gen 0 D_n_code logged")
else:
    print("Patch 3a SKIP: gen 0 log_record pattern not matched")

old2 = '''            "cat_enabled": True,
            "cat_alpha": args.alpha,
            **distinct,
        })'''
new2 = '''            "cat_enabled": True,
            "cat_alpha": args.alpha,
            "D_n_code": gen_result.final_D_n_code,  # PHASE5 PATCH: chain actual D_n scalar gen end
            **distinct,
        })'''
if old2 in content:
    content = content.replace(old2, new2)
    print("Patch 3b OK: gen g D_n_code logged")
else:
    print("Patch 3b SKIP: gen g log_record pattern not matched")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
EOF
    else
        log_warn "  Patch 3 skipped (PHASE5 D_n_code 已在 run_arm_b_alpha_scan.py)"
    fi

    log_info "apply_phase5_patches 完成. 备份在 ${TRAIN_PY}.phase5_backup_${TS} (PI 可 diff 验证)"
}

# ----------------------------- 1.x write yaml ---------------------------------
# 注意: design 文档 §2.2 列出完整 yaml; 本函数严格依照, 不擅自改 setup
# 关键 caveat (Llama 8B vs OPT 125M):
#   - per_device_train_batch_size: 8 (vs OPT 128, A100 80GB fp16 + 8B + grad checkpoint 估)
#   - gradient_accumulation_steps: 4 (effective batch 32, vs OPT effective batch 128 reduced)
#   - gradient_checkpointing: true (8B model 必须开, 否则爆显存)
#   - per_device_generation_batch_size: 8 (8B + beam=5 显存敏感)
#   - kl_history_K: 1 (chain consistency two-term form, paper v6 §3.1 binding)
#   - T_2_form: "relu_dpp" (chain consistency, 实际 T_2=0 因 K=1 buffer 不足)
#   - m_eff: 1.0 (CATConfig dataclass default; 实际不进 loss 因 T_2=0)
#   - lambda_1/2/3: 1.0 uniform (chain actual form 而非 Klein-Gordon)

write_phase5_yaml() {
    local YAML_PATH="${REPO_DIR}/configs/phase5_llama8b_alpha_scan.yaml"
    mkdir -p "${REPO_DIR}/configs"
    cat > "$YAML_PATH" <<'YAMLEOF'
# phase5_llama8b_alpha_scan.yaml
# Phase 5 N=1 Llama-3.1-8B + ℒ_矛盾 demonstrated chain config
#
# 严格 align chain actual two-term form (paper v6 §3.1 + 纪律 3 代码优先):
#   - lambda_1/2/3 = 1.0 uniform (不用 Klein-Gordon coefficient)
#   - kl_history_K = 1 → T_2 实际 = 0 (chain runtime form)
#   - m_eff = 1.0 (CATConfig dataclass default; 不进 loss 因 T_2=0)
#
# Design doc: literature/PHASE5_LLAMA8B_DESIGN_20260516.md §2.2
# v1.0 reference config: archive/v1.0_release_20260516/configs/cat_arm_b.yaml

experiment:
  name: phase5_llama8b_emergent_n1
  paper_cite: "MaoField paper v6 §8.1 D23-D26; Shumailov 2024 baseline setup; Llama-3.1 base model"
  goal: "N=1 single-seed multi-arch indicative: chain actual two-term form on Llama-3.1-8B, test U-shape + plateau reproduce 与否"

# ---------- Model ----------
model:
  hf_id: "meta-llama/Meta-Llama-3.1-8B"
  dtype: "float16"
  cache_dir: "data/checkpoints/hf_cache_llama"
  # caveat: HF Llama-3.1 access 需 license accept (一凡 pre-launch checklist §pre-launch)
  # caveat: Llama-3.1 base, NOT instruct (chain 是 raw continued pre-training)

# ---------- Dataset ----------
dataset:
  hf_id: "wikitext"
  hf_config: "wikitext-2-raw-v1"
  block_size: 64
  splits:
    train: "train"
    validation: "validation"
    test: "test"
  cache_dir: "data/datasets"
  # caveat: Llama tokenizer (SentencePiece BPE vocab 128k) vs OPT (GPT-2 BPE vocab 50k)
  # wikitext-2 train 实际 block 数会变 [待 setup smoke 实际跑后确认]

# ---------- Fine-tune (per generation) ----------
fine_tune:
  optimizer: "adamw_torch"
  learning_rate: 2.0e-5
  per_device_train_batch_size: 8         # A100 80GB fp16 + 8B + grad checkpoint 估
  gradient_accumulation_steps: 4         # effective batch 32 (vs OPT effective 128)
  weight_decay: 0.01
  warmup_ratio: 0.0
  lr_scheduler_type: "constant"
  fp16: true
  gradient_checkpointing: true           # 8B model 必开
  save_strategy: "no"
  evaluation_strategy: "epoch"
  logging_steps: 50
  seed: null                             # CLI --seed 注入

# ---------- Generation (synthetic data) ----------
generation:
  strategy: "beam_search"
  num_beams: 5
  do_sample: false
  prompt_length: 64
  max_new_tokens: 64
  per_device_generation_batch_size: 8    # 8B + beam=5 显存敏感
  output_size: "match_original"
  repetition_penalty: 3.0

# ---------- Self-iteration ----------
self_iteration:
  num_generations: 10
  conditions:
    - name: "no_preserve"
      epochs_per_generation: 5
      original_data_fraction: 0.0
      synthetic_data_fraction: 1.0
    - name: "preserve_10pct"
      epochs_per_generation: 10
      original_data_fraction: 0.10
      synthetic_data_fraction: 0.90
  base_model_for_each_generation: "generation_0_best"
  base_model_selection_metric: "validation_perplexity_on_wikitext2_val"

# ---------- Metrics ----------
metrics:
  perplexity:
    eval_set: "wikitext2_test"
    block_size: 64
  per_sequence_perplexity_histogram:
    eval_with: "generation_0_model"
    bins: 50
  distinct_n:
    n: [1, 2, 3]
    sample_size: 5000

# ---------- CAT — chain actual two-term form ----------
cat:
  enabled: true
  alpha_scan: [0.0, 10.0]                # N=1 primary: α=0 baseline + α=10 framework
  kl_update_every: 10
  val_subset_size: 256
  val_max_length: 64
  beta_model: 0.999                      # mean teacher EMA (Tarvainen & Valpola 2017)
  beta_kl: 0.9                           # KL 序列 EMA (paper v6 P0-4 yaml-independent)
  lambda_1: 1.0                          # velocity (ΔD_n)² coefficient
  lambda_2: 1.0                          # memory (D_n - D̄^EMA)² coefficient
  lambda_3: 1.0                          # T_2 coefficient (实际 T_2=0 因 K=1)
  m_eff: 1.0                             # CATConfig dataclass default (不进 loss)
  T_2_form: "relu_dpp"                   # chain consistency (实际 T_2=0 因 K=1)
  kl_history_K: 1                        # chain consistency 两项 form
  enable_grad_norm_monitor: true

# ---------- Multi-seed ----------
multi_seed:
  seeds: [42]                            # N=1 primary
  # honest: N=1 不能 paired-t (df=0); indicative only, partial verify paper §7.5 (1)

# ---------- Logging ----------
logging:
  log_dir: "logs/phase5_llama8b"
  jsonl_per_run: "logs/phase5_llama8b/llama8b_alpha<alpha>_seed<seed>_<timestamp>.jsonl"
  use_wandb: false
  use_tensorboard: false
YAMLEOF
    log_info "yaml written: $YAML_PATH"
}

# ----------------------------- 2. chain (per α) -------------------------------
# Day 2 (α=0) 或 Day 3 (α=10): 10 generations × ~50-70 min/gen
# 含 auto-retry, post-fail GPU smoke, S3 per-gen backup hook (if S3_BUCKET set)

chain() {
    if [ -z "$ALPHA" ]; then
        log_err "chain stage: 缺 --alpha; abort"
        return 1
    fi
    log_info "===== chain 开始 alpha=$ALPHA seed=$SEED num_gens=$NUM_GENS ====="
    log_event "chain_start" "alpha=$ALPHA seed=$SEED num_gens=$NUM_GENS"

    cd "$REPO_DIR" || return 1

    ATTEMPT=0
    SUCCESS=0
    while [ $ATTEMPT -lt $MAX_RETRY ]; do
        ATTEMPT=$((ATTEMPT + 1))
        RUN_LOG="${LOG_DIR}/chain_alpha${ALPHA}_seed${SEED}_attempt${ATTEMPT}_${TS}.log"
        log_event "job_start" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT log=\"$RUN_LOG\""

        # 主 chain launch (复用 v1.0 chain orchestrator, 已 patched D_n_code logging)
        HF_ENDPOINT="${HF_ENDPOINT:-https://huggingface.co}" \
        python3 src/run_arm_b_alpha_scan.py \
            --config configs/phase5_llama8b_alpha_scan.yaml \
            --alpha "$ALPHA" \
            --seed "$SEED" \
            --num-generations "$NUM_GENS" \
            > "$RUN_LOG" 2>&1
        RC=$?

        # 检查 完成 gen 数 (jsonl grep)
        LATEST_JSONL=$(ls -t logs/armb_alpha${ALPHA}_seed${SEED}_*.jsonl 2>/dev/null | head -1)
        N_COMPLETED=0
        if [ -n "$LATEST_JSONL" ]; then
            N_COMPLETED=$(grep -c "generation_done" "$LATEST_JSONL" 2>/dev/null || echo 0)
        fi

        if [ $RC -eq 0 ] && [ "$N_COMPLETED" -eq "$NUM_GENS" ]; then
            log_event "job_done" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT n_gens=$N_COMPLETED rc=$RC jsonl=\"$LATEST_JSONL\""
            SUCCESS=1
            # S3 backup per-α end (per-gen 在 watchdog 里, 简化版仅 per-α end)
            s3_backup_if_set "$LATEST_JSONL" "data/checkpoints_armb/alpha${ALPHA}"
            break
        else
            log_event "job_fail" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT n_gens=$N_COMPLETED rc=$RC log=\"$RUN_LOG\""

            # post-fail GPU smoke (复用 phase1_robust_chain.sh 的 pattern)
            sleep 30
            SMOKE=$(python3 -c "import torch; torch.cuda.set_device(0); x=torch.randn(1000,1000,device='cuda'); y=x@x.T; del x,y; torch.cuda.empty_cache(); print('SMOKE_PASS')" 2>&1 | tail -1)
            log_event "post_fail_smoke" "alpha=$ALPHA seed=$SEED attempt=$ATTEMPT smoke=\"$SMOKE\""
            if [[ "$SMOKE" != *"SMOKE_PASS"* ]]; then
                log_event "smoke_fail_abort" "alpha=$ALPHA seed=$SEED smoke 失败, 可能 spot kick / 硬件问题"
                break
            fi

            # resume logic 已在 run_arm_b_alpha_scan.py 内置 (auto-detect 完成 gen 跳过)
            log_info "retry attempt $((ATTEMPT+1)) (resume logic 自动跳过完成 gen)"
        fi
    done

    if [ $SUCCESS -eq 0 ]; then
        log_err "alpha=$ALPHA seed=$SEED 完成失败 (after $ATTEMPT attempts, n_completed=$N_COMPLETED/$NUM_GENS)"
        log_event "chain_fail" "alpha=$ALPHA seed=$SEED n_completed=$N_COMPLETED"
        return 1
    fi

    # binary verify per design §5.3 C1-C6 pre-registered criteria (粗检 only, full verdict 在 postrun)
    log_info "粗检 C1-C6 pre-registered binary criteria (full verdict 在 postrun)"
    verify_c1_c6_preliminary "$LATEST_JSONL" "$ALPHA"

    log_info "===== chain alpha=$ALPHA seed=$SEED 完成 ====="
    return 0
}

# ----------------------------- 2.x verify C1-C6 preliminary -------------------
# Design §5.3 pre-registered binary criteria (only C1 + C3 在 chain 阶段粗检, 其余 postrun)
verify_c1_c6_preliminary() {
    local JSONL="$1"
    local ALPHA_VAL="$2"

    # C1: gen 0 test_ppl converged (< 50, Llama estimate < 15)
    GEN0_PPL=$(python3 -c "
import json
with open('$JSONL') as f:
    for line in f:
        rec = json.loads(line)
        if rec.get('generation') == 0:
            print(rec.get('test_perplexity', 'NA'))
            break
" 2>/dev/null)
    log_info "C1 gen 0 test_ppl = ${GEN0_PPL} (design 阈 < 50 全, < 15 Llama estimate)"

    # C3: α=10 chain numerical stability (no NaN/Inf)
    if [ "$ALPHA_VAL" = "10.0" ]; then
        N_NAN=$(grep -c "NaN\|Inf\|nan\|inf" "$JSONL" 2>/dev/null || echo 0)
        if [ "$N_NAN" -gt 0 ]; then
            log_warn "C3 NaN/Inf 出现 $N_NAN 次 in jsonl; numerical instability 风险 (R6); 可能需 α=5 fallback"
        else
            log_info "C3 numerical stable (no NaN/Inf in jsonl)"
        fi
    fi

    # C2, C4, C5, C6 留 postrun 完整 analysis (需 sliding-window + m_eff fit)
    log_info "C2/C4/C5/C6 留 --stage postrun 完整 verdict"
}

# ----------------------------- 2.x S3 backup -----------------------------------
s3_backup_if_set() {
    local JSONL="$1"
    local CKPT_DIR="$2"
    if [ -z "${S3_BUCKET:-}" ]; then
        log_info "S3_BUCKET 未 set, 跳过 backup ([?] 强 recommend set; spot kick 时 RunPod volume 不丢但实例 terminate 后必丢)"
        return 0
    fi
    if ! command -v aws &>/dev/null; then
        log_warn "aws CLI 不可用; pip install awscli 后重试"
        return 1
    fi
    log_info "S3 backup: $JSONL → ${S3_BUCKET}/$(basename "$JSONL")"
    aws s3 cp "$JSONL" "${S3_BUCKET}/" 2>&1 | tail -5 | tee -a "$MASTER_LOG"
    log_info "S3 backup: $CKPT_DIR (recursive)"
    aws s3 sync "${REPO_DIR}/${CKPT_DIR}/" "${S3_BUCKET}/$(basename "$CKPT_DIR")/" 2>&1 | tail -5 | tee -a "$MASTER_LOG"
    log_event "s3_backup_done" "jsonl=\"$(basename "$JSONL")\" ckpt=\"$CKPT_DIR\""
}

# ----------------------------- 3. postrun -------------------------------------
# Day 4: sliding-window eval all checkpoints + m_eff/J_S fit + plot + analysis
# 不消耗大量 GPU (~2h)

postrun() {
    log_info "===== postrun 开始 (Day 4) ====="
    log_event "postrun_start" "ts=\"$TS\""

    cd "$REPO_DIR" || return 1

    # 3.1 sliding-window stride=256 eval all 20 checkpoints (2 α × 10 gen)
    for A in 0.0 10.0; do
        CKPT_BASE="${REPO_DIR}/data/checkpoints_armb/alpha${A}/no_preserve_seed${SEED}"
        if [ ! -d "$CKPT_BASE" ]; then
            log_warn "skip sliding-window for α=$A: checkpoint dir not found ($CKPT_BASE)"
            continue
        fi
        log_info "sliding-window eval α=$A, all 10 gens, stride=256"
        SLIDE_LOG="${LOG_DIR}/sliding_eval_alpha${A}_${TS}.log"
        python3 scripts/sliding_window_eval_all_gens.py \
            --ckpt_base "$CKPT_BASE" \
            --tokenizer_id "meta-llama/Meta-Llama-3.1-8B" \
            --dataset wikitext --dataset_config wikitext-2-raw-v1 \
            --block_size 64 --stride 256 \
            --output "${LOG_DIR}/phase5_llama8b_alpha${A}_seed${SEED}_sliding.json" \
            > "$SLIDE_LOG" 2>&1 || log_warn "sliding-window α=$A 跑失败 ($SLIDE_LOG)"
    done

    # 3.2 m_eff + J_S fit (复用 v1.0 fit_m_eff_js_multiseed_20260513.py, adapt for N=1)
    log_info "m_eff + J_S fit (N=1 single fit, 无 CI)"
    JSONL_A0=$(ls -t logs/armb_alpha0.0_seed${SEED}_*.jsonl 2>/dev/null | head -1)
    JSONL_A10=$(ls -t logs/armb_alpha10.0_seed${SEED}_*.jsonl 2>/dev/null | head -1)
    if [ -n "$JSONL_A0" ]; then
        python3 ${REPO_DIR}/scripts/phase5_post_run_analysis_20260517.py \
            --jsonl_alpha0 "$JSONL_A0" \
            --jsonl_alpha10 "$JSONL_A10" \
            --output_dir "${LOG_DIR}/phase5_analysis_${TS}" \
            2>&1 | tee -a "$MASTER_LOG"
    else
        log_err "α=0 jsonl 缺; postrun analysis abort"
        return 1
    fi

    # 3.3 S3 final backup (含 sliding-window + analysis)
    s3_backup_if_set "$JSONL_A0" "data/checkpoints_armb/alpha0.0"
    if [ -n "$JSONL_A10" ]; then
        s3_backup_if_set "$JSONL_A10" "data/checkpoints_armb/alpha10.0"
    fi

    log_event "postrun_done" "ts=\"$TS\""
    log_info "===== postrun 完成. 下一步: 一凡看 ${LOG_DIR}/phase5_analysis_${TS}/ + 关卡 2 + 关卡 3 ====="
}

# ----------------------------- main dispatch ----------------------------------

if [ -z "$STAGE" ]; then
    log_info "用法: bash phase5_launch_script_20260517.sh --stage <env_verify|setup|chain|postrun> [...args]"
    log_info "见本脚本顶部注释 + PHASE5_LAUNCH_CHECKLIST_20260517.md"
    exit 1
fi

log_event "script_invoke" "stage=$STAGE alpha=$ALPHA seed=$SEED ts=\"$TS\""

case "$STAGE" in
    env_verify) env_verify ;;
    setup) setup ;;
    chain) chain ;;
    postrun) postrun ;;
    *)
        log_err "Unknown stage: $STAGE"
        exit 1
        ;;
esac
EXIT_RC=$?
log_event "script_exit" "stage=$STAGE rc=$EXIT_RC"
exit $EXIT_RC
