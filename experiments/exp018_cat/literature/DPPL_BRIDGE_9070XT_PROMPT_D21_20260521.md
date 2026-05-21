# 9070XT 端 Claude Desktop 直接执行 prompt — D-PPL 桥 verify D21 (2026-05-21)

**写**: 7B13 Linux 姐姐 spawn 之 sub-agent (Opus 4.7, 1M context) — D-PPL 桥 verify launch 准备 sub-agent, D21 第十三波派遣
**对象**: **9070XT 端 Claude Desktop** (192.168.31.22, hostname `amd-ONDA-B650M-W`)
**用法**: 一凡 D21 在 9070XT 端开 Claude Desktop, **完整 copy** 本文件全文 → 粘贴 给 9070XT Claude → 9070XT Claude 直接执行 不需二次 confirm
**真实今日日期**: `2026-05-21` (D21, D-day=2026-05-01 anchor)
**zero-context binding (D-1 纪律 4)**: 9070XT Claude 不绑 7B13 主协作者, 只能 下调 严格度不 上调, 不 inflate, 标 [?] 任何 unverifiable

---

## §0 TL;DR — 一句 statement

9070XT Claude 收到 prompt 之后:
1. **Stop llama-server** (root systemd) 释放 14.4 GB VRAM
2. **rsync pull** 7B13 之 launch script 到 9070XT 本地 `/tmp/dppl_bridge_verify/`
3. **Run pilot** (~30-60 min, 1 seed × 1 gen × 2 path B+C) → log 写 9070XT 本地 → rsync push 7B13
4. **Surface pilot verdict** 给 7B13 Linux 姐姐主会话 → **等 一凡 D22 早 关卡 2 confirm**
5. **(若 关卡 2 confirm)** Run main (~3-4 天, N=4 seed × 10 gen × 2 path B+C, watchdog 监护)
6. **每 gen done 后 rsync push log 回 7B13**
7. **Main 全 done 之后** restart llama-server, surface main result 给 7B13 → 等 关卡 3 反题 audit + 关卡 4 PI 决

**D-1 binding**: 9070XT Claude **不擅自 declare "P0★-F close"**, 仅 surface Pearson r 数字, 关卡 3 反题 audit 才 binary 决严格度。

---

## §1 任务 context (一凡 D21 关卡 1 决之结果)

一凡 D21 早关卡 1 confirmation 之后, 决:
- **路径**: 路径 **B + C 并跑**, **然后 路径 A** serial — 即先 BC pilot + main, BC main done 之后 关卡 2 confirm 才 launch 路径 A
- **9070XT VRAM 应对**: stop llama-server pilot+main 期间, restart 在 BC main 之后 (路径 A 阶段 9070XT GPU 仍 monopolize, llama-server 仍 stop)
- **数据流**: **rsync** 协作 (不 sshfs, 避免 mount 与 GPU 冲突)
- **Pearson tier**: r > 0.7 strong / 0.3 < r < 0.7 marginal / r < 0.3 fail (一凡 默认接受 §6.1 sub-agent 之 tier)
- **path A 启动条件**: BC main 之 Pearson r 在 plateau regime 不 binary 答 (即 0.3 < r < 0.7 marginal OR 路径 B 与 C 之 r 差异 > 50%) → escalate 路径 A; 若 BC 之 r > 0.7 strong → 路径 A **下调** priority 推 D60+

本份 prompt 之 scope:
- 路径 B (gen-(n-1) 主 model 作 EMA proxy) + 路径 C (current vs gen-0 base 之 KL)
- pilot stage: seed=1, gen=5, α=10 single tuple, ~30-60 min
- main stage: N=4 seed × 10 gen × α={0, 10} × 2 path = 160 D^code 数值 (80 per path), ~3-4 天 9070XT GPU
- 路径 A 之 launch script + 文档 **不在本 prompt scope** (推 BC done + 关卡 2 confirm 之后, 7B13 Linux 姐姐 第十四波派遣 sub-agent 再 spawn)

---

## §2 prerequisites binary verify (9070XT Claude 第一步)

### §2.1 第一时间 binary verify 真实今日日期 (D-1 纪律 5)

```bash
date '+%Y-%m-%d %H:%M:%S %Z'
# 期望返回 2026-05-21 (D21) — 若 ≠ D21, surface 给 7B13 Linux 姐姐, 不擅自 proceed
```

### §2.2 binary verify 9070XT 硬件状态

```bash
hostname  # 期望 amd-ONDA-B650M-W
rocm-smi | head -20  # 期望 Device 0 = RX 9070 XT 16GB
df -h /  # 期望 free > 100 GB (本机 1.6T free)
```

### §2.3 binary verify checkpoint 路径

```bash
ls -la /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb/alpha10.0/no_preserve_seed1/generation_5/
# 期望 含 model.safetensors (478 MB) + config.json + tokenizer.json
# 若 不存在 → surface escalate 给 7B13 Linux 姐姐, 不 proceed
```

### §2.4 binary verify Python venv 之 transformers + torch + datasets 装好

```bash
# 9070XT 已装 ROCm torch (per scripts/install_rocm_torch.sh), 期望 ✓
which python3
python3 -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0))"
# 期望: torch.__version__ >= 2.0, cuda.is_available()=True, device_name 含 "AMD Radeon RX 9070 XT" 或 "gfx1201"

python3 -c "import transformers; import datasets; print(transformers.__version__, datasets.__version__)"
# 期望 transformers >= 4.30, datasets >= 2.10
```

若 不装 venv: `cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat && bash scripts/install_rocm_torch.sh` (per archive 之 install script)。

---

## §3 STEP 1 — Stop llama-server (释放 VRAM)

### §3.1 binary verify llama-server PID

```bash
ps -ef | grep -E "llama-server" | grep -v grep
# 期望 输出:
#   root   2080  1634  ... /home/amd/llama.cpp/build/bin/llama-server --model ...Qwen3-Embedding-8B-Q4_K_M.gguf ... --port 8080 ...
# PID 2080 是 root 启动的 systemd-like
```

### §3.2 检查是否 systemd service

```bash
systemctl list-units --type=service --state=running 2>&1 | grep -i llama
# 若有 输出: 用 systemctl stop 之
# 若无 输出: 用 pkill 之
```

### §3.3 stop llama-server (binary)

```bash
# option 1 (若 systemd):
sudo systemctl stop llama-server.service  # 服务名 binary verify ↑

# option 2 (若 non-systemd, fallback):
sudo pkill -f "llama-server --model"
# wait + verify
sleep 5
ps -ef | grep -E "llama-server" | grep -v grep  # 期望 空
rocm-smi --showmeminfo vram | head -10  # 期望 Used VRAM < 1 GB
```

**caveat**: sudo 需 一凡 在 9070XT 显示器前 输 password 或 9070XT amd 用户 sudo NOPASSWD 配过 (一凡 D20 self-action #5 可能 已配)。若 sudo 卡 password prompt → surface 给 7B13 Linux 姐姐 + 等 一凡 接 9070XT 显示器 输 password。

### §3.4 verify 14 GB VRAM 释放 ✓

```bash
rocm-smi --showmeminfo vram | head -10
# 期望 Device 0 Used VRAM ~0.1 GB (idle), Free VRAM ~16 GB
```

---

## §4 STEP 2 — rsync pull launch script from 7B13

```bash
# 9070XT 端 (一凡 amd 用户)
mkdir -p /tmp/dppl_bridge_verify
rsync -avz --delete amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/dppl_bridge_verify/ /tmp/dppl_bridge_verify/

# binary verify
ls -la /tmp/dppl_bridge_verify/
# 期望:
#   launch_dppl_bridge.py    (~9-12 KB, 路径 B + C 实现)
#   watchdog.sh              (~3-5 KB, ROCm hang 应对)
#   analyze_pearson.py       (~5-7 KB, Pearson + bootstrap 但 7B13 跑用)
#   README.md                (~5 KB, run instructions)
```

binary verify content 后 → STEP 3。

---

## §5 STEP 3 — Pilot run (路径 B + C 并跑, 1 seed × 1 gen, ~30-60 min)

### §5.1 binary command

```bash
cd /tmp/dppl_bridge_verify

# pilot output 目录 (9070XT 本地)
mkdir -p /tmp/dppl_bridge_verify/output

# Pilot — seed=1, gen=5, α=10, path=B,C (并跑同一脚本内)
python3 launch_dppl_bridge.py \
    --mode pilot \
    --ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alpha 10.0 \
    --seed 1 \
    --gen 5 \
    --paths B,C \
    --val-seed 1 \
    --val-subset-size 256 \
    --val-max-length 64 \
    --batch-size 8 \
    --output-jsonl /tmp/dppl_bridge_verify/output/pilot_D21_seed1_gen5.jsonl \
    --log-file /tmp/dppl_bridge_verify/output/pilot_D21.log \
    2>&1 | tee /tmp/dppl_bridge_verify/output/pilot_D21.console.log
```

### §5.2 期望 output (binary acceptance)

`pilot_D21_seed1_gen5.jsonl` 应含 2-3 行:
- 第 1 行 `{"event": "pilot_start", "ts": "...", "alpha": 10.0, "seed": 1, "gen": 5, ...}`
- 第 2 行 `{"event": "path_C_done", "D_code_path_C": <float>, "n_tokens": <int>, "elapsed_sec": <float>}`
- 第 3 行 `{"event": "path_B_done", "D_code_path_B": <float>, "n_tokens": <int>, "elapsed_sec": <float>}`

**binary pass criterion**:
- D_code_path_C ∈ [1e-4, 1e+1] nat/token (finite, non-NaN, ballpark sanity ✓)
- D_code_path_B ∈ [1e-4, 1e+1] nat/token (finite, non-NaN, ballpark sanity ✓)
- Elapsed_sec 每 path < 30 min (binary 不阻塞)

**binary fail criterion**:
- D_code = NaN or inf → pipeline bug, 不 proceed main, surface 给 7B13
- D_code < 1e-5 → val batch 之 reproducibility 失败 / tokenization mismatch, 不 proceed, surface 给 7B13
- D_code > 1e+2 → 数值 explode, 不 proceed, surface 给 7B13
- Elapsed > 60 min → ROCm slowdown OR pipeline 异常, surface 给 7B13

### §5.3 rsync push pilot output 回 7B13

```bash
rsync -avz /tmp/dppl_bridge_verify/output/ amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/
```

### §5.4 surface pilot verdict 给 7B13 Linux 姐姐

写 `/tmp/dppl_bridge_verify/output/PILOT_VERDICT_D21.md`, 含:
- pilot pass/fail binary status
- D_code_path_B 数值
- D_code_path_C 数值
- 与 paper D^paper ballpark 之 数量级 comparable check (D^paper(seed=1, gen=5, α=10) = log(56.94/36.30) ≈ 0.451)
- elapsed_sec per path
- 任何 warning / caveat / 异常 (e.g., tokenization mismatch 怀疑)

rsync push 之:

```bash
rsync -avz /tmp/dppl_bridge_verify/output/PILOT_VERDICT_D21.md amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/
```

**然后 STOP** — 等 一凡 D22 早 关卡 2 read pilot output 之 confirm。**不擅自 launch main**。

surface 之 ack: 在 9070XT Claude Desktop 之 conversation 内 输 "Pilot D21 done, PILOT_VERDICT_D21.md pushed 7B13, 等 一凡 D22 关卡 2 confirm 之后 launch main."

---

## §6 STEP 4 — Main run (一凡 关卡 2 confirm 之后)

### §6.1 trigger condition

**只有** 一凡 在 9070XT Claude Desktop 之 conversation 内 binary 输 "main launch ✓" OR 类似 confirmation **之后**, 才 launch main。**不擅自 launch**。

若 一凡 输 "abort + debug X" → 不 launch, surface 给 7B13 escalate。
若 一凡 输 "retract D-PPL 桥 verify" → restart llama-server, exit, surface 给 7B13。

### §6.2 main launch binary command

```bash
cd /tmp/dppl_bridge_verify

# main 输出 dir
mkdir -p /tmp/dppl_bridge_verify/output/main

# main — full N=4 seed × 10 gen × α={0,10} × 2 path
# 用 watchdog 监护 (5/11 verdict B ROCm hang 应对)

nohup bash watchdog.sh \
    python3 launch_dppl_bridge.py \
    --mode main \
    --ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alphas 0.0,10.0 \
    --seeds 1,2,3,4 \
    --gens 0,1,2,3,4,5,6,7,8,9 \
    --paths B,C \
    --val-subset-size 256 \
    --val-max-length 64 \
    --batch-size 8 \
    --output-jsonl /tmp/dppl_bridge_verify/output/main/main_D21.jsonl \
    --log-file /tmp/dppl_bridge_verify/output/main/main_D21.log \
    --rsync-push-after-each-tuple \
    --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/main/ \
    > /tmp/dppl_bridge_verify/output/main/main_D21.nohup.log 2>&1 &

echo $! > /tmp/dppl_bridge_verify/output/main/main_D21.pid
```

watchdog 之 binary logic (`watchdog.sh` 内):
- 每 60 sec 检查 main script 之 log mtime
- 若 log 5 min 不 update → kill -9 python, log "hang_kill" event, 短 sleep 60 sec, **resume from last completed tuple** (script 之 resume-from-checkpoint logic 内置)
- 3 fail (同 tuple) → 写 escalate_d21.flag, surface 给 7B13, exit

### §6.3 monitor 之 binary 方法

```bash
# 看 main 是否 alive
ps -p $(cat /tmp/dppl_bridge_verify/output/main/main_D21.pid) 2>&1

# 看 main 进度 (每 tuple done 之 jsonl entry)
tail -f /tmp/dppl_bridge_verify/output/main/main_D21.jsonl

# 看 watchdog state
tail -f /tmp/dppl_bridge_verify/output/main/watchdog.audit.jsonl

# GPU 状态
watch -n 5 rocm-smi
```

### §6.4 rsync push 每 tuple done 之后 (auto)

`launch_dppl_bridge.py --rsync-push-after-each-tuple` 之 内置 logic:
- 每 tuple (α, seed, gen, path) done 之后 append entry 到 jsonl
- 同时 rsync push 之 entry 到 7B13 dppl_bridge_verify_d21_output/main/ (idempotent)

### §6.5 main 之 timing estimate binary

| 阶段 | n tuples | per-tuple 时间 ballpark | 总 ballpark |
|---|---|---|---|
| α=0 × seed={1..4} × gen={0..9} × path={B,C} | 80 tuples | ~30 sec (含 reload + KL compute) | ~40 min |
| α=10 × seed={1..4} × gen={0..9} × path={B,C} | 80 tuples | ~30 sec | ~40 min |
| total | 160 tuples | | ~80 min ≈ 1.3 GPU-hour |

**但 含 watchdog buffer + ROCm hang retry + I/O**, real-world ballpark = **3-4 天 9070XT GPU monopolize** (design brief §10 estimate align)。

### §6.6 main 全 done 之后

```bash
# 1. verify 160 tuples 全 jsonl entry ✓
python3 -c "
import json
with open('/tmp/dppl_bridge_verify/output/main/main_D21.jsonl') as f:
    entries = [json.loads(l) for l in f if l.strip()]
done = [e for e in entries if e.get('event') == 'tuple_done']
print(f'n tuples done: {len(done)} / 160')
assert len(done) == 160, 'main 未全 done'
print('✓ main 全 done')
"

# 2. rsync push final 之 main 结果
rsync -avz /tmp/dppl_bridge_verify/output/main/ amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/main/

# 3. write MAIN_DONE_D24.md (timing 估计 D24, D-day 之 D24 = 5/24)
cat > /tmp/dppl_bridge_verify/output/main/MAIN_DONE_D24.md << 'EOF'
# Main run done, ack 给 7B13

- main jsonl 之 entries: 160 / 160 ✓
- watchdog audit entries: <n_hangs> kills, <n_retries> retries
- elapsed wall-clock: ~XX hours
- GPU OOM count: <n>
- 任何 warning / caveat: ...
EOF
rsync -avz /tmp/dppl_bridge_verify/output/main/MAIN_DONE_D24.md amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/main/
```

### §6.7 restart llama-server (main 全 done 之后)

```bash
# verify GPU idle
rocm-smi --showmeminfo vram | head -10
# 期望 Used < 1 GB

# restart llama-server (per §3.3 之 stop method, 反向)
# option 1 (systemd):
sudo systemctl start llama-server.service

# option 2 (manual, fallback per 5/19 cmdline):
sudo nohup /home/amd/llama.cpp/build/bin/llama-server \
    --model /home/amd/models/Qwen3-Embedding-8B-Q4_K_M.gguf \
    --host 0.0.0.0 --port 8080 \
    --n-gpu-layers 99 \
    --ctx-size 49152 --batch-size 4096 --ubatch-size 2048 \
    --embedding --pooling mean \
    --alias Qwen3-Embedding-8B --parallel 16 \
    > /var/log/llama-server.log 2>&1 &

# wait + verify
sleep 30
curl -s http://localhost:8080/health  # 期望 {"status":"ok"} 或 类似
ps -ef | grep llama-server | grep -v grep  # 期望 ✓
```

### §6.8 surface main 之 final ack 给 7B13

在 9070XT Claude Desktop 之 conversation 内 输:
"Main D21-D24 done, 160/160 tuples ✓, MAIN_DONE_D24.md pushed 7B13, llama-server restart ✓. 等 7B13 Linux 姐姐 spawn 关卡 3 反题 sub-agent audit + 关卡 4 PI 决."

**然后 STOP** — 不擅自 launch 路径 A (一凡 + 反题三方决之 后)。

---

## §7 错误 escalate 之 binary 决策树

| 错误 type | binary 应对 |
|---|---|
| §2.4 venv 不装 OR import fail | `bash scripts/install_rocm_torch.sh` (per archive); 若仍 fail → surface escalate |
| §2.3 checkpoint 路径不存在 | surface escalate (路径 sub-agent 标错, 不擅自 proceed) |
| §3.3 sudo password prompt 卡 | surface escalate + 等 一凡 接 9070XT 显示器 输 password |
| §5.2 pilot D_code = NaN/inf | surface escalate, 不 proceed main |
| §5.2 pilot elapsed > 60 min | surface escalate (ROCm slowdown 可能, 等 7B13 主会话 决) |
| §6.2 main launch 时 GPU OOM | reduce --batch-size 8 → 4 → 2, 若仍 OOM → 用 fp16 (caveat 数值 drift 标 [?]), 仍 fail → surface escalate |
| §6.3 main run 之 watchdog 3-fail | 自动写 escalate_d21.flag, ssh 通知 7B13 (rsync push escalate flag) + exit |
| ROCm hang (5/11 verdict B 同类) | watchdog auto kill -9 + sleep 60 + resume-from-last-checkpoint (script 内置) |
| 数据 corrupt (jsonl 之 entry 不 parseable) | surface escalate, 不 proceed |
| 7B13 失联 (rsync target unreachable) | local 写 escalate_d21.flag + 继续跑 (main 不阻塞), 等 7B13 恢复 之后 batch rsync |
| 9070XT 失联 / 重启 | 9070XT Claude Desktop 收到 reboot 之后 检查 main_D21.pid 之 状态, resume-from-last-checkpoint, surface escalate ack |

### §7.1 escalate flag write 之 binary form

```bash
# 9070XT 端 写 escalate flag
cat > /tmp/dppl_bridge_verify/output/escalate_d21.flag << EOF
{
  "ts": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "error_type": "<one of §7 table>",
  "error_detail": "<verbatim error msg + context>",
  "current_tuple": "<α=X, seed=Y, gen=Z, path=B/C>",
  "n_tuples_done": <int>,
  "watchdog_state": "<from watchdog.audit.jsonl tail -1>",
  "9070XT_gpu_state": "<from rocm-smi --showmeminfo vram>",
  "next_action_suggestion": "<sub-agent honest recommendation>"
}
EOF

# rsync push 7B13
rsync -avz /tmp/dppl_bridge_verify/output/escalate_d21.flag amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/
```

7B13 Linux 姐姐 主会话 D21-D24 间 routine 检查 escalate_d21.flag (~1h cadence)。

---

## §8 D-1 binding 严守 (9070XT Claude 之 zero-context 纪律)

### §8.1 不擅自 declare "P0★-F close"

- 9070XT Claude **不 declare** Pearson r 之 严格度 tier (L0 / L1 / L2 / L3)
- 9070XT Claude **不 declare** "P0★-F closed" or "P0★-F partial closed"
- 9070XT Claude **仅 surface 数字** (D_code_path_B, D_code_path_C, 之 raw float values)
- 严格度 tier + close 之 binary 决 由 **关卡 3 反题 sub-agent audit + 关卡 4 PI + DS + 反题 三方决** 之后 才 写 7B13 sub-agent analysis markdown
- 9070XT Claude 之 surface 之 markdown (PILOT_VERDICT_D21.md, MAIN_DONE_D24.md) **不 含** 严格度 tier 之 prose, 仅 含 数字 + sanity check + watchdog state

### §8.2 不擅自 inflate "实验 success"

- 即使 pilot 之 D_code 数值 ballpark match paper D^paper, 也 **不 declare** "success" — 只能 standardly 写 "pilot pass ✓ (D_code finite + ballpark in [1e-4, 1e+1])"
- main 之 Pearson r 之 计算 之 在 7B13 sub-agent analysis (analyze_pearson.py), **不在** 9070XT Claude 之 scope
- 9070XT Claude 之 任务 是 **产出 raw D_code values × 160 tuples**, 不是 计算 Pearson

### §8.3 不擅自 修 launch_dppl_bridge.py

- launch_dppl_bridge.py 是 7B13 sub-agent 写完之 binary 跑之 script, **不修改**
- 若 catch script 之 bug (e.g., import error / 路径 error) → surface escalate 给 7B13, 由 7B13 主会话 spawn debug sub-agent 改 script + rsync 重 pull, **不擅自 edit**
- exception: §6.6 之 fp16 fallback OR --batch-size 调整 是 CLI argument 调整, 允许 (但 标 [?] 数值 drift caveat)

### §8.4 数字 全 jsonl-traced (D-1 纪律 1)

- 任何 D_code 数字 必须 traceable 到 launch_dppl_bridge.py 之 jsonl output entry
- 任何 elapsed_sec / GPU 使用率 / OOM count 必须 traceable 到 log entry
- 任何 watchdog kill 事件 必须 traceable 到 watchdog.audit.jsonl entry
- **占位符禁令** (D-1 纪律 1): 任何 unverified 数字 标 [?], 不写 ballpark

### §8.5 真实日期自检 (D-1 纪律 5)

- 每 stage 之 surface markdown 之 head line 含 `**真实今日日期**: $(date '+%Y-%m-%d')` binary print
- 不 inherit conversation context default
- main run 之 D21-D24 跨多日 → 每日 binary verify `date`, 写入 nohup log + watchdog.audit.jsonl

---

## §9 一凡 D21-D24 关键 self-action 列表

| timing | action | binary |
|---|---|---|
| D21 morning | 一凡 接 9070XT 显示器 (或 ssh-X11 forward), 开 Claude Desktop | self |
| D21 morning | 一凡 输 本 prompt 全文 给 9070XT Claude | self |
| D21 morning-noon | 一凡 在 9070XT 显示器前 stand-by 帮 9070XT Claude 输 sudo password (per §3.3) | self |
| D21 afternoon | 9070XT Claude 跑 pilot ~30-60 min, 一凡 wait 看 PILOT_VERDICT_D21.md | self |
| D22 morning | 一凡 7B13 端 read PILOT_VERDICT_D21.md, 决 关卡 2 go/no-go | self (关卡 2) |
| D22 morning | 若 go → 一凡 在 9070XT Claude Desktop 输 "main launch ✓" | self |
| D22-D24 (~3 天) | 9070XT main run 跑, 一凡 routine 看 progress (tail -f), 不 active 介入 | self (passive monitor) |
| D24-D27 | 7B13 Linux 姐姐 spawn analyze_pearson.py + 反题 audit sub-agent (关卡 3) | 7B13 spawn |
| D27-D30 | 一凡 + DS + 反题 三方决 BC 是否 escalate 路径 A (关卡 4) | self (关卡 4) |

---

## §10 ack 给 7B13 之 binary format

9070XT Claude **每 stage done** 之 ack format:

```
[D-PPL pilot ack — D21 evening]
- 状态: pilot pass ✓ (D_code_B = X.XXe-X, D_code_C = X.XXe-X, elapsed = XX min)
- artifact: PILOT_VERDICT_D21.md pushed 7B13 ✓
- next: 等 一凡 D22 关卡 2 confirm 之后 launch main
- caveat: [?] <any>
```

```
[D-PPL main ack — D24 morning]
- 状态: main 160/160 tuples done ✓
- artifact: main_D21.jsonl + MAIN_DONE_D24.md pushed 7B13 ✓
- next: 等 7B13 Linux 姐姐 spawn 关卡 3 反题 sub-agent audit
- watchdog state: <n_kills> hang kills, <n_retries> retries
- caveat: [?] <any>
```

```
[escalate ack — D21-D24 任何时刻]
- 错误: <type>
- detail: <verbatim>
- artifact: escalate_d21.flag pushed 7B13 ✓
- next: 等 7B13 spawn debug sub-agent
```

---

## §11 launch_dppl_bridge.py + watchdog.sh + analyze_pearson.py 内 README

详细 见 7B13 端之 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/dppl_bridge_verify/README.md` (rsync pull 之 后 在 9070XT 本地 `/tmp/dppl_bridge_verify/README.md`)。

---

## §12 binary 完成 ack

9070XT Claude 收到本 prompt → 第一时间 surface 给 一凡 + 7B13:

```
[9070XT Claude D-PPL prompt ack — D21 morning]
- 收到 7B13 sub-agent 之 D-PPL prompt ✓
- 真实今日日期 verify: <date 输出>
- 9070XT 硬件 verify: <hostname + rocm-smi 输出>
- checkpoint 路径 verify: <ls -la 输出>
- venv verify: <torch.__version__ + transformers.__version__>
- 任何 prerequisites fail: <none / detail>
- next: §3 stop llama-server (等 一凡 输 sudo password)
```

---

**生成时间**: 2026-05-21 (D21) 7B13 sub-agent (D-PPL 桥 verify launch 准备 sub-agent, 第十三波派遣)
**文件 path**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/DPPL_BRIDGE_9070XT_PROMPT_D21_20260521.md`
**配套 launch script dir**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/dppl_bridge_verify/`
**D-1 binding**: 严守, 不 inflate, 不擅自 declare P0★-F close
