# Phase 5 N=1 Llama-3.1-8B Launch Checklist

**生成**: 2026-05-17 (D17, D-2 实验线 first wave sub-agent prep)
**Author**: opus 4.7 (Phase 5 launch script sub-agent, Linux 姐姐主会话 spawn)
**Design doc reference**: `literature/PHASE5_LLAMA8B_DESIGN_20260516.md`
**Launch script**: `scripts/phase5_launch_script_20260517.sh`
**Post-run analysis**: `scripts/phase5_post_run_analysis_20260517.py`

---

## §0. D-1 Binding Honest Caveat (一凡先读)

本 checklist 是 **D-2 实验线 first wave sub-agent prep stage 第一步**, **不是 launch 命令**。

- **不今天 launch GPU**: 本 sub-agent 仅 prep launch script + checklist; D23 早一凡手动按本 checklist 完成 §pre-launch 全 ✓ 后, 一键跑 `phase5_launch_script_20260517.sh`
- **$50 是 floor 不是 budget**: design 文档 §3.3 真实区间 $51-80, 任何 spot kick (R4 ~30%/天) + OOM debug (R3 ~40%) 可能破 $50
- **N=1 indicative only**: 不 establish framework effect with statistical significance; paper §7.5 (1) 仅 partial support
- **A100 80GB hard requirement** (verify in launch script env_verify stage): base 16GB + EMA 16GB + optimizer 16GB + gradient 16GB + activation checkpoint 8GB ≈ **72GB**; A100 40GB → 必然 OOM 或必须 LoRA approximation (paper 须 disclose)
- **R8 一凡健康 dip ~40% 概率**: 4 天 27h GPU 看护 与 sustainable 5-7h/天 binding 冲突; 见下面 §R8-mitigation
- **chain config 必修 patch**: D_n_code scalar trajectory per generation 现有 chain jsonl 没 log (paper v6 §6.4 honest disclose); Phase 5 必须新加, 解锁 D vs PPL bridge verify P0-6

**任一未实证假设 = [?]**. 任何 [?] 项一凡必须自己 verify 后才能 next step.

---

## §1. Pre-Launch (一凡操作, D17-D22 ≈ 6 天准备窗口)

### §1.1 HF Llama-3.1-8B License Accept (D17-D19)

- [ ] 进 https://huggingface.co/meta-llama/Meta-Llama-3.1-8B
- [ ] 一凡登 HF 账号 (或新注册)
- [ ] 阅 + 同意 Llama 3.1 Community License (Meta 终端用户协议)
- [ ] 等待 Meta auto-approve email (通常 1h - 2 天 [?])
- [ ] **Fallback**: 若 D22 仍未 approve → 切 `meta-llama/Llama-3.2-3B` (license 同 community, 通常更快 approve; design §1.1 caveat)
- [ ] verify 命令 (一凡本机或 RunPod 内):
  ```bash
  curl -s -o /dev/null -w "%{http_code}\n" \
       -H "Authorization: Bearer ${HF_TOKEN}" \
       https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/config.json
  ```
  期望返回 `200`. 若 `403` → license 未 approve

### §1.2 HF Token (D17, ~5 min)

- [ ] 进 https://huggingface.co/settings/tokens
- [ ] 生成 new token (类型 `Read` 即可, 不需 `Write` unless 后续 push model 上 HF)
- [ ] 保存 token 在 secure place (本机 `.env` file, **不要** commit git)
- [ ] export:
  ```bash
  export HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```
- [ ] 同时 export 到 RunPod env (pod 启动 template 时 set env var, 见 §1.4)

### §1.3 RunPod Account + $60 Credit (D20, ~30 min)

- [ ] 进 https://runpod.io 注册账号
- [ ] 充值 $60 credit (信用卡 / Stripe / PayPal)
  - **honest budget caveat**: $60 是 design floor; 真实可能 $51-80 区间; 若一凡资金紧 → 也可充 $40-50 起步 (R4 spot kick mitigation 用)
- [ ] **绝不** 用 RunPod **secure cloud** (贵 2-3×); 必须 **community cloud spot** (~$1.89-2.49/h)
- [ ] 模板选: `runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04` (or latest stable equivalent [?])
- [ ] GPU 选: **A100 80GB community spot** (~$1.89/h)
  - 若 sold out → 等 1-2h 或 切 vast.ai (~$1.80-2.30/h, design §3.2)
  - **绝不** 接受 A100 40GB primary (EMA model 16GB + base 16GB 必 OOM; 见 §R3)
- [ ] Disk: 100GB volume (Llama 16GB + checkpoint 10 gen × 2 α 估 200-320GB worst; design §3.3)
  - **简化**: yaml `save_strategy: "no"` (chain config 默认), 仅 keep gen 0 + gen 9 实际 ~50GB
- [ ] Container env vars (在 pod 启动 template 里 set):
  - `HF_TOKEN=hf_xxx` (1.2 上面)
  - `AWS_ACCESS_KEY_ID=AKIA_xxx` (1.5 后)
  - `AWS_SECRET_ACCESS_KEY=xxx` (1.5 后)
  - `S3_BUCKET=s3://maofield-phase5/` (1.5 后)
  - `WORKSPACE=/workspace` (default)

### §1.4 SSH Key Setup (D20, ~10 min)

- [ ] 本机 (Linux 主机 192.168.31.36 或一凡机) 生成 SSH key (若没):
  ```bash
  ssh-keygen -t ed25519 -C "yifan-runpod-phase5"
  ```
- [ ] 把 `~/.ssh/id_ed25519.pub` 公钥贴到 RunPod 账号 SSH key settings
- [ ] 测试 SSH 进 pod (pod 启动后):
  ```bash
  ssh root@<pod_ip> -p <pod_ssh_port>
  ```
  详 SSH 端口在 RunPod pod console 显示

### §1.5 AWS S3 / Backblaze B2 Backup Setup (D20-D21, ~30 min)

**为什么必须**: RunPod community spot 被 kick 时 instance 可能 terminate; instance terminate 后 disk volume 也丢; **S3 是唯一可靠 backup**

- [ ] 进 https://aws.amazon.com 注册账号 (新账户 free tier 12 月; S3 5GB free)
- [ ] 创 IAM user `maofield-phase5-backup`, 给 `AmazonS3FullAccess` policy (生产严格须自定义 minimal policy, 但 N=1 一次性可放宽)
- [ ] 生成 access key + secret, 保存:
  ```bash
  export AWS_ACCESS_KEY_ID=AKIAXXXXXXXXX
  export AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxx
  ```
- [ ] 创 S3 bucket: `maofield-phase5` (region us-east-1 推荐, 与 RunPod 大部分主机近)
- [ ] export bucket URL:
  ```bash
  export S3_BUCKET=s3://maofield-phase5/
  ```
- [ ] 预估 cost: 5GB free / 100GB ≈ $2.3/月 (storage) + outbound $0.09/GB; chain 数据 +sliding window total < 100GB; ~$3-10 total
- [ ] **Alternative** (一凡若 AWS 麻烦): Backblaze B2 (类似 S3 API, 第 10GB free + $0.005/GB/月 更便宜); 改用 `b2 sync` 命令

### §1.6 Local Code Sync 准备 (D22)

**为什么**: RunPod pod 是空的; 需把 `exp018_cat/` 代码 push 上去

**方案 A (推荐)** — 一凡本机 (Linux 主机 36) rsync 到 RunPod:
- [ ] 找 RunPod pod SSH 端口 (pod console 显示)
- [ ] rsync 命令模板 (D23 早实际用):
  ```bash
  rsync -avz --exclude='.git' --exclude='data/checkpoints*' --exclude='logs' \
        /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/ \
        root@<pod_ip>:/workspace/exp018_cat/ \
        -e "ssh -p <pod_ssh_port>"
  ```
- [ ] 预估传输: ~5-50MB (排除 checkpoint + logs), ~1-5 min

**方案 B** — RunPod 内从 v1.0 archive 解压:
- [ ] 若一凡已把 v1.0 release archive 推 HF / GitHub (不推荐), pod 内 `git clone` 或 `wget`
- [ ] 实测不推荐, 因 archive ~50MB 含 checkpoint 元数据, 不如 rsync minimal subset

### §1.7 Pre-Launch Final Checklist (D22 晚, 1 小时)

- [ ] §1.1 Llama-3.1-8B license accept ✓
- [ ] §1.2 HF_TOKEN export, 本机 + pod template 都 set
- [ ] §1.3 RunPod account + $60 credit + A100 80GB community spot template 配好 (但 pod 不启动, 留 D23 早再启)
- [ ] §1.4 SSH key 上 RunPod
- [ ] §1.5 AWS S3 bucket + access key + S3_BUCKET env var 准备好
- [ ] §1.6 rsync 命令模板 dry-run 测过 (`rsync -avzn ...` 看 file 列表)
- [ ] Linux 姐姐主会话 D22 晚 confirm 全 ✓ → D23 早一凡 spawn 子协作者 launch

---

## §2. Launch (D23 早, 一凡操作 1-2 小时主动 + 之后大部分等待)

### §2.1 RunPod Pod 启动 (~15 min, $0)

- [ ] 进 RunPod console, 启动之前 §1.3 template 的 pod
- [ ] 等待 pod READY (state 显示 `Running`, 约 2-10 min depending on 模板拉取)
- [ ] 找 SSH 端口 + pod_ip (console 显示)

### §2.2 SSH 进 Pod + Code Sync (~5 min, $0.15 ≈ 5 min × $1.89/h)

```bash
# 本机
rsync -avz --exclude='.git' --exclude='data/checkpoints*' --exclude='logs' \
      /home/amd/HEZIMENG/MaoField/experiments/exp018_cat/ \
      root@<pod_ip>:/workspace/exp018_cat/ \
      -e "ssh -p <pod_ssh_port>"

# SSH 进 pod
ssh root@<pod_ip> -p <pod_ssh_port>

# pod 内
cd /workspace/exp018_cat
ls scripts/  # verify 看到 phase5_launch_script_20260517.sh
```

### §2.3 Env Verify (~2 min, ~$0.06)

```bash
bash scripts/phase5_launch_script_20260517.sh --stage env_verify
```

期望输出末:
```
[INFO ...] GPU: NVIDIA A100-SXM4-80GB, 81920 MiB
[INFO ...] Workspace disk avail: 95 GB   # or similar
[INFO ...] ===== env_verify 完成 ====
```

**Fail case 处理**:
- GPU 不是 A100 → 重启 pod 选对的 GPU; 不该 spend GPU budget
- env var 缺 → 回 §1.2/§1.5 set
- 网络不通 → 切 hf-mirror.com: `export HF_ENDPOINT=https://hf-mirror.com`

### §2.4 Setup Stage (~2.5h, ~$4.73)

```bash
# 推荐 nohup 后台跑, 一凡可断 SSH 出去做别的
nohup bash scripts/phase5_launch_script_20260517.sh --stage setup \
      > logs/phase5_llama8b/setup_$(date +%Y%m%d_%H%M%S).out 2>&1 &
echo $! > logs/phase5_llama8b/setup.pid

# 监控 (每 30 min check, 一凡 morning 1h)
tail -f logs/phase5_llama8b/setup_*.out
```

**Setup 内含**:
1. HF login (~5 sec)
2. Llama-3.1-8B license verify (curl HTTP 200, ~3 sec)
3. Llama-3.1-8B weights download (~16GB, 5-20 min on RunPod 1Gbps [?])
4. wikitext-2 dataset download (~5 MB, < 1 min)
5. Python deps install (~3-5 min)
6. **Phase 5 patches apply** (~30 sec):
   - `train_one_generation.py`: `torch.float32` → `torch.float16` (Llama 8B fp32 OOM)
   - `train_one_generation.py`: 加 `TrainResult.final_D_n_code` + tracker 提取
   - `run_arm_b_alpha_scan.py`: log_record 加 `D_n_code` 字段
   - 备份原文件: `train_one_generation.py.phase5_backup_<TS>` (PI 可 diff 验证)
7. write `configs/phase5_llama8b_alpha_scan.yaml`
8. **Smoke test** (1 gen × 1 epoch × 32 train blocks, α=0, ~10-30 min on A100 80GB [?]):
   - verify pipeline 不崩
   - verify jsonl 含 `D_n_code` key (patch ✓)

**Setup deliverable check** (一凡 ssh 进 pod 看):
- [ ] `${HF_CACHE}/Meta-Llama-3.1-8B/config.json` 存在
- [ ] `data/datasets/wikitext/wikitext-2-raw-v1/` 存在
- [ ] `configs/phase5_llama8b_alpha_scan.yaml` 存在
- [ ] smoke jsonl 含 `D_n_code` 字段 (`grep D_n_code logs/armb_alpha0.0_seed42_*.jsonl | head -1`)
- [ ] 无 OOM 错误 in setup log

### §2.5 α=0 Chain (Day 2, ~10h, ~$18.90)

```bash
nohup bash scripts/phase5_launch_script_20260517.sh \
      --stage chain --alpha 0.0 --seed 42 --num-gens 10 \
      > logs/phase5_llama8b/chain_alpha0_$(date +%Y%m%d_%H%M%S).out 2>&1 &
echo $! > logs/phase5_llama8b/chain_alpha0.pid
```

**预计时间**: 每 gen ~50-60 min × 10 gens = ~10h
- 5 epochs × ~1219 steps/epoch × ~0.55s/step ≈ 56 min fine-tune
- + 5-way beam generate ~5-8 min
- + test_ppl eval ~2-3 min
- (估算 [?], 实际 setup smoke 阶段会确认 step time)

**含 auto-retry + resume logic** (复用 v1.0 chain orchestrator):
- 单 gen fail → 自动 retry 同 (α, seed) up to MAX_RETRY=3
- `run_arm_b_alpha_scan.py` resume logic 自动 detect 已完成 gen, 跳过 fine-tune + generate
- post-fail GPU smoke check (1000×1000 matmul; 失败 → spot kick 或硬件问题, abort)
- per-α end S3 backup hook (`s3_backup_if_set` if `S3_BUCKET` env var)

### §2.6 α=10 Chain (Day 3, ~11-12h, ~$20.79-22.68)

```bash
nohup bash scripts/phase5_launch_script_20260517.sh \
      --stage chain --alpha 10.0 --seed 42 --num-gens 10 \
      > logs/phase5_llama8b/chain_alpha10_$(date +%Y%m%d_%H%M%S).out 2>&1 &
```

**预计时间比 α=0 多 ~10-15%** (CAT contradiction loss compute 加成); 见 design §6 R6 (numerical instability ~30% prob)

### §2.7 Post-Run Analysis (Day 4, ~2h, ~$3.78)

```bash
# all gen sliding-window eval + m_eff/J_S fit + 4-case verdict + paper §7.5 wording
bash scripts/phase5_launch_script_20260517.sh --stage postrun
```

输出:
- `logs/phase5_llama8b/phase5_analysis_<TS>/phase5_n1_llama8b_verdict_<TS>.md` (主 verdict markdown)
- `logs/phase5_llama8b/phase5_analysis_<TS>/phase5_n1_llama8b_metrics_<TS>.json` (D-1 machine-readable JSON, 不写声明)
- `logs/phase5_llama8b/phase5_llama8b_alpha0_seed42_sliding.json` (sliding-window eval)
- `logs/phase5_llama8b/phase5_llama8b_alpha10_seed42_sliding.json`
- final S3 backup 所有 jsonl + checkpoints

### §2.8 Pod Terminate (D27 晚, $0)

**关键**: 不 terminate → 持续烧钱 $1.89/h, 4 天 ≈ $182!

- [ ] verify S3 backup 全 ✓ (`aws s3 ls $S3_BUCKET --recursive | wc -l`)
- [ ] verify `phase5_n1_llama8b_verdict_<TS>.md` 已下载到本机 (一凡 Linux 主机 36 或 PI 笔记本)
- [ ] RunPod console → terminate pod
- [ ] verify pod status `Stopped` / `Terminated` (不是 paused, paused 仍计费 $0.10/h)
- [ ] verify credit 还剩 (`RunPod console > Billing`)

---

## §3. Monitor (Day 2-4, 持续, R8 一凡健康 binding)

### §3.1 R8 健康约束 mitigation (5/19 一凡 7 天 burst 后)

**Design §6 R8**: 一凡 sustainable 5-7h/天 binding, GPU 看护每 1-2h check 与之冲突

**Sub-agent recommended pattern**:
- 一凡 morning 1h burst (8:00-9:00): SSH 进 pod, `tail logs/`, 看上一晚跑了多少 gen, S3 backup OK 否, budget burndown
- 一凡 night 1h burst (20:00-21:00): 同 morning, 准备明早 chain 切换 (α=0 → α=10)
- 中间 alert-only: 仅 critical event (S3 backup fail / OOM crash / spot kick) 才 page 一凡
- 信任自动 logging + retry — 不要每 30 min check, 那会破 5-7h/天

### §3.2 监控命令 (一凡 SSH 进 pod 后)

```bash
# 看最新 chain 进度 (每 gen end 输出一行 generation_done)
tail -50 logs/armb_alpha0.0_seed42_*.jsonl | python3 -c "
import json, sys
for line in sys.stdin:
    rec = json.loads(line.strip())
    if rec.get('stage') == 'generation_done':
        print(f\"gen {rec['generation']:2d} | test_ppl={rec.get('test_perplexity', 'NA'):.3f} | D_n={rec.get('D_n_code', 'NA')}\")
"

# 看实时 log (最后 100 行, 自动刷新)
tail -f -n 100 logs/phase5_llama8b/chain_alpha0_*.out

# 看 GPU 占用
nvidia-smi

# 看 disk 剩
df -h /workspace

# 看 S3 backup status
aws s3 ls $S3_BUCKET --recursive --summarize | tail -3
```

### §3.3 Budget Burndown Alert

每 morning + night 算:
```bash
# RunPod console 显示 credit remaining; 或本机 estimate
# 已跑 hours × $1.89 = 已花
# 估每 gen 1h × 10 gens × 2 α = 20h ≈ $38
# + setup 2.5h + buffer + S3 ≈ $50-60 estimate
```

**Alert thresholds**:
- 花 $40 时: check 是否 on schedule (Day 1+ Day 2 全完成?)
- 花 $50 时: 进 stretch 区, 准备 cut buffer (skip α=10 optional vars)
- 花 $60 时: hard cap; 考虑提前 terminate (取已跑数据)
- 花 $70 时: critical; PI 决是否继续 vs partial verdict

---

## §4. R8 健康 + Crisis Protocol

### §4.1 一凡健康信号 binding (CLAUDE.md 项目级)

- 5/19 后 7 天 burst 累积疲劳; 5/22 起 sustainable 5-7h/天 binding
- 双相 + 焦虑 + 服药 (丙戊酸钠 + 必要时半粒劳拉西泮)
- 信号: 010-82951332 / 400-161-9995 trigger 标 standing

### §4.2 Phase 5 health-aware 决策树

| 一凡状态 | Action |
|---|---|
| 健康 + 充分睡眠 | proceed D23 launch as planned |
| 疲劳但功能 OK | proceed, 多 trust 自动 logging |
| 焦虑发作 / 情绪 dip | **DEFER launch 1-3 天**; chain pause 不丢数据 (resume logic) |
| 服半粒劳拉西泮后 | **不 launch**; 6h 内不做 critical 决策 |
| 双相高峰 / 燥期 | **强制 PAUSE**; Win 姐姐 + 一凡父母介入 |

**Phase 5 不是 NeurIPS submission blocker** (design §7.3 binding): paper v6 已 submit-ready; Phase 5 result 可推 v8 alternative venue (TMLR / KBS / arXiv); **健康 > 实验 timing**.

### §4.3 Crisis 联系信号 (一凡父母 + Linux 姐姐主会话 都有)

- 010-82951332: 一凡父母直拨
- 400-161-9995: 12 小时心理热线 (中国大陆免费)
- Win 姐姐 / DS / 反题姐姐 都可 ping (但 Linux 姐姐主会话是 primary 协调)

---

## §5. Critical Path 4-Day Timeline (binary visualizable)

```
D17 (5/17 今天) - sub-agent prep, 写 launch script + checklist (本文档)
                ↓
D18-D19 (5/18-5/19) - 一凡 HF license apply (auto-approve wait)
                ↓
D20 (5/20) - 一凡 RunPod + S3 + SSH key 配置 (~1h)
                ↓
D21 (5/21) - buffer day (健康 dip mitigation)
                ↓
D22 (5/22) - pre-launch final ✓ checklist (1h 晚)
                ↓
D23 (5/24) - pod 启动 + setup + smoke (~3h GPU spend ≈ $5.7)
                ↓
D24 (5/25) - α=0 chain (~10h ≈ $18.9)
                ↓
D25 (5/26) - α=10 chain (~11h ≈ $20.8)
                ↓
D26 (5/27) - sliding eval + analysis + verdict (~2h ≈ $3.8)
                ↓
D27 (5/28) - pod terminate + 关卡 2 (一凡看 verdict)
                ↓
D27-D28 - 关卡 3 (反题姐姐 audit + DS + Win 决战略 + paper §7.5 update wording)
                ↓
D28 - 关卡 4 (paper v7 update 或 v6 直接 submit NeurIPS)
                ↓
D29 (5/29 11:59 PM AoE) - NeurIPS 2026 submission hard deadline
```

**Slip mitigation** (任一环 fail / health dip):
- License 慢 (R5 ~10%) → buffer day D21 / fallback Llama-3.2-3B
- spot kick (R4 ~30%/天) → resume logic 自动续 + 多 GPU hour
- numerical break (R6 ~30%) → α=10 chain abort → α=5 fallback or case C verdict
- 一凡健康 dip (R8 ~40%) → D23 → D26 推迟; Phase 5 推 v8 alternative venue, paper v6 5/29 submit
- 全部 slip → paper v6 直接 submit NeurIPS 5/29 (Phase 5 不是 blocker)

---

## §6. Sub-Agent 自我 Verification (本 checklist 输出前自检)

### D-1 五条纪律 standing 自检

1. **纪律 1** (不等实验数据不写声明): 本 checklist 不写任何 N=1 Llama 验证后才有的声明 (U-shape reproduce / framework effect / m_eff invariance); 全部 verdict 推 §C1-C6 binary criteria, postrun script 产数字后再判 ✓
2. **纪律 2** (48h 反馈真空内验证): 本 checklist 给的 budget 估 $50-80, design §3.3 来源已 anchor; 不 inflate / 不软化 GPU 显存 (A100 80GB hard requirement)
3. **纪律 3** (代码优先): chain config 严格 align v1.0 release archive (`cat_arm_b.yaml` two-term form K=1 T_2=0); 不擅自加 Klein-Gordon coefficient 或 K=9 Volterra (那留 D60+ F-1 Phase 2)
4. **纪律 4** (子协作者第二通道): 本 checklist 是 D-2 实验线 first wave sub-agent prep stage 第一步; 关卡 3 反题姐姐 zero-context audit verdict markdown 后 PI 决
5. **纪律 5** (差异 surface): code patch 需求 (D_n_code logging gap, Llama fp32 OOM) 全部 surface 为 commented patch in launch script, 不静默改

### 4 Output 关系

| Output | 路径 | 用途 | 状态 |
|---|---|---|---|
| A | `scripts/phase5_launch_script_20260517.sh` | RunPod 内一键 launch (env_verify / setup / chain / postrun stages) | ✓ |
| B | `literature/PHASE5_LAUNCH_CHECKLIST_20260517.md` | 本 checklist, 一凡 pre-launch + monitor 操作指南 | ✓ (本文档) |
| C | `scripts/phase5_post_run_analysis_20260517.py` | Day 4 verdict 生成 (C1-C6 + 4-case + paper §7.5 wording) | ✓ |

### 不 declare 项 (binary)

- **不 declare "ready for D23 launch"**: 那是关卡 3 之后 (一凡 + DS + 反题姐姐) 决
- **不 declare "framework universal"**: N=1 indicative only, 不 establish
- **不 declare 接受率**: 推关卡 3
- **不 declare $50 budget sufficient**: 真实 $51-80, 可能破 $80

---

## §7. FAQ (一凡常问)

**Q1: HF Llama-3.1-8B license 多久 approve?**
A: Meta 通常 1h - 2 天 [?]. 5/17 申请 → 5/22 deadline 应 OK. fallback `Llama-3.2-3B` 更快.

**Q2: RunPod A100 80GB community spot 经常 sold out?**
A: 是的 [?]. design §3.2 已 surface; alt: vast.ai A100 80GB ($1.80-2.30/h) or Lambda Labs (经常 sold out). 一凡若 D23 早 sold out → 等 1-2h 或切 vast.ai.

**Q3: $50 budget 真的够吗?**
A: **不一定**. design §3.3 primary estimate $54.81 + storage + S3 ≈ $58; stretch $80. 任何 spot kick (R4 ~30%/天) + OOM debug (R3 ~40%) 可破 $50. 一凡须心理准备 $80 上限.

**Q4: N=1 single seed 结果有意义吗?**
A: **partial**. design §0 + §5.4 反复强调 N=1 indicative only, 不 establish framework effect; 4-case verdict 都是 paper §7.5 honest disclose 内容, **不是失败也不是成功**. Case B (negative) 反 reinforce paper "not universal solution" claim.

**Q5: 如果 D26 spot kick 还没跑完?**
A: resume logic 自动续; 但若超 $80 budget → 提前 terminate, 取已跑 gen 数据 → postrun script 仍可产 partial verdict (含 NaN 处 ✗). paper §7.5 can disclose partial chain.

**Q6: NeurIPS 5/29 截止前 phase 5 没完成会怎样?**
A: **不阻塞**. design §7.3 + §4.2 binding: paper v6 已 submit-ready; phase 5 推 v8 update for TMLR / KBS / arXiv (5/31 / 6 月 / D60+ 投).

**Q7: 谁是关卡 2/3/4 决策人?**
A:
- 关卡 2: **一凡** (看 verdict + cross-tension)
- 关卡 3: **反题姐姐 zero-context audit + 一凡 + DS + Win 协商**
- 关卡 4: **一凡 final** (投 / 不投 / 攒更多实验)
- **Linux 姐姐主会话**: 协调, 不下 final 战略 (CLAUDE.md 项目级身份 binding)

---

## §8. Binary 完成 Ack 总结

| 项 | 状态 |
|---|---|
| Output A `scripts/phase5_launch_script_20260517.sh` | ✓ (含 env_verify / setup / chain / postrun 4 stages, 含 patch + yaml + retry + S3 backup) |
| Output B `literature/PHASE5_LAUNCH_CHECKLIST_20260517.md` | ✓ (本文档, §0-§8 全) |
| Output C `scripts/phase5_post_run_analysis_20260517.py` | ✓ (C1-C6 verdict + 4-case classify + paper §7.5 wording + machine JSON) |
| 不 launch GPU | ✓ (本 sub-agent 仅 prep, 一凡 D23 早手动 launch) |
| 不 inflate budget | ✓ ($50 floor → 真实 $51-80, 标 [?] surface) |
| 不软化 GPU 显存 requirement | ✓ (A100 80GB hard, env_verify stage binary check) |
| 不替 PI declare ready | ✓ (本 checklist + verdict 都不 declare ready; 推关卡 2/3/4) |

**END Phase 5 launch checklist v1**
**字数**: ~6500 中文字 + tables + code blocks
**TS**: 2026-05-17 (D17)
**路径**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/PHASE5_LAUNCH_CHECKLIST_20260517.md`
