# D3 早 (5/10) Launch Checklist — Phase 1 paper-convention 5 seeds chain

**生成**: 2026-05-09 凌晨 (Linux 姐姐 m_eff fit + PI verdict 后)
**5/10 凌晨更新**: Option E sub-agent 异步 + sliding-window finding + Phase 1 launched
**target**: PI 一凡 醒后顺序执行,不需 think,只需 ack/no

---

## §0 5/10 凌晨 PI 醒后 status snapshot (TL;DR)

**Phase 1 chain 已启动** (5/9 20:36 PI ack Option A + "极度严谨" 后):
- PHASE1_CHAIN_PID=2640719
- seeds [0, 1, 2, 3, 4] paper convention sequential
- 当前: seed=0 gen 2 generate (估 PI 醒时 seed=0/1 done, seed=2 跑中)
- 总 ETA ~21:30 五月十日晚 (24h 后)

**关键 finding (反题姐姐 P0-B2 DOWNGRADE)**:
- gen 0 chunked block=64 给 44.60 PPL (我们一直用)
- **gen 0 sliding-window stride=256 (HF 标准) 给 22.34 PPL** (paper 报 ~20)
- **gen 0 +80% offset 是 eval method artifact, NOT setup bug**
- 接受率 update: 24天 NMI 1-7% → **5-12%**, D31 cumulative → **60-70%**
- verdict: `literature/sliding_window_eval_verdict_20260510.md`

**5/10 凌晨主 agent 异步 work done**:
- 3 sub-agent verdict 综合 → `literature/THREE_SUBAGENT_SYNTHESIS_20260510.md`
- λ_3 ROLLBACK 1.1792 → 0.212 (数学教授 §1.3 catch)
- src 代码升级 + smoke test PASS
- sensitivity yamls (fp32 + rep_penalty=2.0) prep done
- paper §3.4-§3.7 substantive revision draft → `literature/paper_section3_4_5_6_REVISION_20260510.md`
- 全 sync 22 主机 ✓

**3 件 PI 醒后 ack 队列** (主 agent 推荐):
1. ack sliding-window finding → paper §6 disclose 用 sliding-window stride=256 重 eval all gens
2. ack paper §3.4-§3.7 revision draft (V_4/V_D 拆 + 假设 A3'/A5 + chain rule honest)
3. ack D5 sequencing: Phase 1 完成后 m_eff multi-seed refit + paper §3 final lock

---

---

## §1 PI 醒后第一件事 — 健康 check

- [ ] 醒来时间合理 (≥6 小时 sleep)?
- [ ] 没新 ideation surface?
- [ ] 早饭 + 药 ✓?
- 任何一项 no → 推迟 launch,直接联系热线 010-82951332,主 agent standby

---

## §2 m_eff = 0.212 lock status

| 已 done (5/9 凌晨) | 文件 |
|---|---|
| ✓ m_eff direct fit script | `scripts/m_eff_direct_fit.py` (CPU only, ~10 sec run) |
| ✓ verdict markdown | `literature/m_eff_direct_fit_verdict_20260510.md` |
| ✓ 新 framework yaml | `configs/cat_arm_b_v2_dialectical.yaml` (m_eff=0.212 derive 值) |
| ✓ src defaults update | `src/contradiction_loss.py` (β_model=0.999849, β_kl=0.8090, λ=[2.36, 0.11, 0.21]) |
| ✓ 同步 22 主机 | rsync done |

**Per-run statistics**: m_eff mean=0.185 median=**0.212** std=0.066 range=[0.110, 0.233]
**接近 Linux eyeball 0.20 ± 0.07** ✓

**caveat (写在 yaml + src comment)**: 3 runs 全 seed=42, variance 来自 fp16 + library drift,D5 multi-seed verdict 后 refit。

---

## §3 GPU smoke test (launch Phase 1 前必做, ~3 min)

22 主机 5/9 16:08 在 fp16 训练 step 207 hipErrorIllegalAddress crash 过。先 verify GPU 稳定:

```bash
ssh amd@192.168.31.22 'cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
  env HF_ENDPOINT=https://hf-mirror.com HIP_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 \
  .venv/bin/python -c "
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os; os.environ[\"HF_ENDPOINT\"] = \"https://hf-mirror.com\"
print(\"loading OPT-125m fp16...\")
m = AutoModelForCausalLM.from_pretrained(\"facebook/opt-125m\", torch_dtype=torch.float16).cuda()
t = AutoTokenizer.from_pretrained(\"facebook/opt-125m\")
print(\"forward + backward smoke...\")
m.train()
ids = torch.randint(0, 50000, (8, 64), device=\"cuda\")
loss = m(ids, labels=ids).loss
loss.backward()
print(f\"loss={loss.item():.4f}, grad ok\")
torch.cuda.empty_cache()
print(\"smoke pass\")
"'
```

**Pass criterion**: 全程不 crash + 输出 "smoke pass"。
**Fail handling**: hipErrorIllegalAddress 重现 → reset GPU (sudo amdgpu-reset 或 sudo modprobe -r amdgpu && sudo modprobe amdgpu) → 再 smoke。

---

## §3.5 反题姐姐 sequencing 修订 (5/10 凌晨 sub-agent verdict)

**3 sub-agent verdict synthesis** (`THREE_SUBAGENT_SYNTHESIS_20260510.md` §3): D3 早 sequencing 应**加 2 个 sensitivity baseline run** (反题姐姐 推荐, ~15h GPU 额外)。理由: gen 0 baseline 36 vs paper 20 (+80% offset) 单独是 paper reject reason,必须 close。

| Sensitivity | 文件 | 改动 | cost | close 哪个 P0 |
|---|---|---|---|---|
| **fp32 baseline** | `configs/sensitivity_fp32_baseline.yaml` | dtype=float32, fp16=false, α=[0] | ~10h GPU | P0-B4 fp16 numerics 是否是 spike artifact |
| **rep_penalty=2.0** | `configs/sensitivity_rep_penalty_2.yaml` | repetition_penalty=2.0 (vs 3.0), α=[0] | ~5h GPU (fp16 同) | P0-B3 audit "paper §5.2 typo" 判断对错 |

**D3 早启动 (PI ack 后, parallel with Phase 1 chain on 22 主机, sequential 因 GPU 单卡)**:

```bash
# fp32 sensitivity (慢, 2-3× wallclock)
ssh amd@192.168.31.22 'cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
  nohup env HF_ENDPOINT=https://hf-mirror.com HIP_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 \
  .venv/bin/python src/run_arm_b_alpha_scan.py \
    --config configs/sensitivity_fp32_baseline.yaml \
    --alpha 0.0 --seed 42 --num-generations 10 \
  > logs/sensitivity_fp32_seed42_20260510.log 2>&1 & echo "FP32_PID=$!"'

# rep_penalty=2.0 sensitivity (快, fp16 同)
ssh amd@192.168.31.22 'cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
  nohup env HF_ENDPOINT=https://hf-mirror.com HIP_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 \
  .venv/bin/python src/run_arm_b_alpha_scan.py \
    --config configs/sensitivity_rep_penalty_2.yaml \
    --alpha 0.0 --seed 42 --num-generations 10 \
  > logs/sensitivity_rep2_seed42_20260510.log 2>&1 & echo "REP2_PID=$!"'
```

**注**: 单卡 GPU sequential, 不能 parallel — Phase 1 chain 完后再跑 sensitivity, OR 反过来 sensitivity 先 + Phase 1 后。反题姐姐推荐 sensitivity 先 (D3-D4 verdict 决定 Phase 1 是否值得跑)。

---

## §4 Phase 1 launch 序列 (Linux dispatch §1 #2 旧 framework)

**注意**: Phase 1 跑 `cat_arm_b.yaml` (旧 framework: λ=1, β_kl=0.9, β_model=0.999, T_2=ReLU)。
**不**跑 `cat_arm_b_v2_dialectical.yaml`。

```bash
# Phase 1.1: α=0 seed 1337 (~5h GPU)
ssh amd@192.168.31.22 'cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
  nohup env HF_ENDPOINT=https://hf-mirror.com HIP_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 \
  .venv/bin/python src/run_arm_b_alpha_scan.py --alpha 0.0 --seed 1337 --num-generations 10 \
  > logs/armb_alpha0_seed1337_phase1_20260510.log 2>&1 & \
  echo "PHASE1_A0_S1337_PID=$!"'
```

**Chain 监控**: 完成后 (~5h) 立即 chain α=10 同 seed → α=0 seed 2024 → α=10 seed 2024 (sequential, 总 ~20h)。

**Chain script** (主 agent 写, 一凡 ack 后跑):

```bash
ssh amd@192.168.31.22 'cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && \
  nohup bash -c "
  for SEED in 1337 2024; do
    for ALPHA in 0.0 10.0; do
      env HF_ENDPOINT=https://hf-mirror.com HIP_VISIBLE_DEVICES=0 CUDA_VISIBLE_DEVICES=0 \
        .venv/bin/python src/run_arm_b_alpha_scan.py \
        --alpha \$ALPHA --seed \$SEED --num-generations 10 \
        > logs/armb_alpha\${ALPHA}_seed\${SEED}_phase1_20260510.log 2>&1
      echo \"=== \$(date) finished alpha=\$ALPHA seed=\$SEED ===\"
    done
  done
  " > logs/phase1_chain_master.log 2>&1 & echo "PHASE1_CHAIN_PID=$!"'
```

---

## §5 Parallel CPU task (m_eff fit refit on multi-seed)

Phase 1 跑期间 (~20h),CPU idle。 D5 multi-seed jsonl 出来后立即 refit:

```bash
# 等 Phase 1 全跑完 (D4-D5) 再跑
cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat
python3 scripts/m_eff_direct_fit.py 2>&1 | tee literature/m_eff_refit_multiseed_$(date +%Y%m%d).log
```

新 verdict 自动 cover 6 runs (3 seed=42 + 3 multi-seed)。如果 multi-seed 也 U-shape → finding robust。

---

## §6 D5 binary verdict (paper §3.5+§4 framing decision)

**问题**: strict-mirror baseline U-shape recovery 是 robust finding 还是 implementation bug?

**判定 criterion**:

| seed=1337 + 2024 也 U-shape? | verdict | paper §3.5+§4 framing |
|---|---|---|
| YES (3/3 seed 都 U-shape) | **robust finding** | 重写为 "U-shape recovery + collapse-recovery dynamics" 不是 monotone collapse mitigation |
| NO (只 seed=42 U-shape) | **fp16 artifact** | 重新跑 fp32 验证 |
| 部分 (1-2 seed U-shape) | **borderline** | sensitivity analysis + caveat 写法 |

---

## §7 Phase 1 完成后 next step (D6+)

完成后立即 ack 主 agent,触发:

1. **m_eff refit** (multi-seed) — 数字 lock (CPU, 5 min)
2. **paper §3.2 数字 update** — 真值 + bootstrap CI (Linux dispatch §2 改md #1)
3. **U-shape framing 决策** — 根据 §6 binary
4. **D5-6 代码升级** — T_2 = D²/2 替 ReLU + Volterra K=9 history (Linux dispatch §4 #1-2)
5. **D7-9 Phase 2 新 framework launch** — 用 cat_arm_b_v2_dialectical.yaml

---

## §8 主 agent standby protocol

PI 醒后:
- ack 此 checklist + verdict md → 主 agent push 跑 §3 smoke
- smoke pass → 主 agent push 跑 §4 chain
- smoke fail → 主 agent escalate (sudo reset 需 PI 授权)
- D5 verdict 出来 → 主 agent dispatch §6 决策给 PI ack

主 agent 不 unilateral 跑 GPU launch (一凡 PI authority);CPU fit / md 写 / yaml 改可 unilateral。

---

**Linux 姐姐 sign-off**: m_eff fit done,新 framework yaml + src ready,Phase 1 launch ack pending PI D3 早 verdict。
