# D-PPL 桥 verify launch scripts — D21 (2026-05-21)

**写**: 7B13 sub-agent (D-PPL 桥 verify launch 准备 sub-agent, 第十三波派遣)
**位置**: 7B13 `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/dppl_bridge_verify/`
**9070XT 端 mirror 路径**: `/tmp/dppl_bridge_verify/` (rsync pulled)

---

## 0. 一句 statement

D21 (一凡 关卡 1 confirm 之后) launch D-PPL 桥 verify 之 路径 **B + C 并跑 然后 A serial**:
- 路径 B: gen-(n-1) 主 model 作 EMA proxy (KL(q^{θ_{n-1}} || p^{θ_n}))
- 路径 C: gen-0 base 作 anchor (KL(q^{θ_0} || p^{θ_n}))
- (路径 A: re-train EMA SGD replay, BC 之后 关卡 2 confirm 之后 launch — **不在本 dir scope**)

scope: pilot (1 seed × 1 gen, ~30-60 min) + main (N=4 seed × 10 gen × α={0,10}, ~3-4 天) on 9070XT GPU。

---

## 1. 文件 list

| 文件 | 用途 | 跑机 |
|---|---|---|
| `launch_dppl_bridge.py` | Pilot + main 之 D_code value 计算 (路径 B + C) | **9070XT** |
| `watchdog.sh` | Main run 之 ROCm hang 监护 wrapper | **9070XT** |
| `analyze_pearson.py` | D_code vs D_paper Pearson + bootstrap CI 95% | **7B13** (main done 之后) |
| `README.md` | 本文件 | both |

---

## 2. 一凡 D21 关卡 1 决定 (binary)

| 项 | 决 |
|---|---|
| 路径 | B + C 并跑 然后 A serial (BC done + 关卡 2 confirm 之后 launch A) |
| 9070XT VRAM 应对 | stop llama-server (pilot+main 期间), restart 在 main 之后 |
| 数据流 | rsync (不 sshfs) |
| Pearson tier | r > 0.7 strong / 0.3 < r < 0.7 marginal / r < 0.3 fail |
| pilot 之 seed / gen / α | seed=1 / gen=5 / α=10 |
| main 之 (seeds, gens, alphas) | seeds={1,2,3,4} × gens={0..9} × alphas={0,10} = 160 tuples |

---

## 3. Workflow timing (D-1 binding 严守)

```
D21 morning   → 一凡 关卡 1 confirm 之后, 7B13 sub-agent (本 dir) ✓ writ done
D21 morning   → 一凡 9070XT 端 read PROMPT_D21_20260521.md (在 literature/)
D21 noon      → 9070XT Claude Desktop: stop llama-server + rsync pull + pilot 跑
D21 evening   → pilot done, rsync push 7B13, 9070XT Claude ack 给 一凡 + 7B13
D22 morning   → 一凡 7B13 端 read PILOT_VERDICT_D21.md, 关卡 2 confirm OR abort
D22-D24       → main run (含 watchdog buffer ~3-4 天)
D24 evening   → main done, rsync push 7B13, 9070XT Claude restart llama-server
D24-D27       → 7B13 sub-agent 跑 analyze_pearson.py + write pearson_summary.json
D27-D30       → 关卡 3 反题 zero-context audit + 关卡 4 PI + DS + 反题 三方决
(D30+         → 决 路径 A escalate OR 路径 D D60+ OR retract)
```

---

## 4. 9070XT 端 binary 命令 sequence

完整 prompt 见: `7B13:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/literature/DPPL_BRIDGE_9070XT_PROMPT_D21_20260521.md`

简版 sequence (one-liner ladder):

```bash
# 1. 9070XT 端 stop llama-server (sudo)
sudo systemctl stop llama-server.service || sudo pkill -f "llama-server --model"
sleep 5 && rocm-smi --showmeminfo vram | head -10  # verify Used < 1 GB

# 2. rsync pull 本 dir → 9070XT 本地
mkdir -p /tmp/dppl_bridge_verify
rsync -avz --delete amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/dppl_bridge_verify/ /tmp/dppl_bridge_verify/

# 3. Pilot (1 tuple × 2 path)
cd /tmp/dppl_bridge_verify
mkdir -p output
python3 launch_dppl_bridge.py \
    --mode pilot \
    --ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alpha 10.0 --seed 1 --gen 5 --paths B,C \
    --val-subset-size 256 --val-max-length 64 --batch-size 8 --dtype fp32 \
    --output-jsonl output/pilot_D21_seed1_gen5.jsonl \
    --log-file output/pilot_D21.log

# 4. rsync push pilot result 回 7B13
rsync -avz output/ amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/

# 5. 等 一凡 D22 关卡 2 confirm 之后 launch main
nohup bash watchdog.sh \
    python3 launch_dppl_bridge.py \
    --mode main \
    --ckpt-root /home/amd/HEZIMENG/MaoField_static_backup_20260520/experiments/exp018_cat/data/checkpoints_armb \
    --alphas 0.0,10.0 --seeds 1,2,3,4 --gens 0,1,2,3,4,5,6,7,8,9 --paths B,C \
    --val-subset-size 256 --val-max-length 64 --batch-size 8 --dtype fp32 \
    --output-jsonl output/main/main_D21.jsonl \
    --log-file output/main/main_D21.log \
    --rsync-push-after-each-tuple \
    --rsync-target amd@192.168.31.36:/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/main/ \
    > output/main/main_D21.nohup.log 2>&1 &

# 6. Main done 之后 restart llama-server
sudo systemctl start llama-server.service || \
    sudo nohup /home/amd/llama.cpp/build/bin/llama-server \
        --model /home/amd/models/Qwen3-Embedding-8B-Q4_K_M.gguf \
        --host 0.0.0.0 --port 8080 --n-gpu-layers 99 \
        --ctx-size 49152 --batch-size 4096 --ubatch-size 2048 \
        --embedding --pooling mean \
        --alias Qwen3-Embedding-8B --parallel 16 > /var/log/llama-server.log 2>&1 &
```

---

## 5. 7B13 端 Pearson 分析 binary 命令 (main done 之后)

```bash
cd /home/amd/HEZIMENG/MaoField/experiments/exp018_cat
python3 scripts/dppl_bridge_verify/analyze_pearson.py \
    --main-jsonl dppl_bridge_verify_d21_output/main/main_D21.jsonl \
    --chain-logs-dir archive/v1.0_release_20260516/chain_logs \
    --alphas 0.0,10.0 --seeds 1,2,3,4 --paths B,C \
    --output-json dppl_bridge_verify_d21_output/main/pearson_D24_summary.json \
    --n-bootstrap 10000 --bootstrap-seed 20260521
```

---

## 6. 数学定义 (per design brief §2)

### 6.1 路径 B (gen-(n-1) main as EMA proxy)

```
D_n^{code, proxy-EMA} := KL(q^{θ_{n-1}} || p^{θ_n}) on val batch
                       = E_q[log q^{θ_{n-1}} - log p^{θ_n}]
```

- 实现: `compute_kl_q_to_p(model_p=θ_n, model_q=θ_{n-1}, ...)` (即 path B 之 'q' = gen-(n-1))
- L2 form-borrow tier: β_θ=0.999, EMA 之 真 time constant ≈ 1.4 gen — gen-(n-1) main 是 EMA 之 first-order approx
- gen=0 之 path B skip (无 gen=-1 reference)

### 6.2 路径 C (gen-0 base anchor)

```
D_n^{code, gen0-anchor} := KL(q^{θ_0} || p^{θ_n}) on val batch
                         = E_q[log q^{θ_0} - log p^{θ_n}]
```

- 实现: `compute_kl_q_to_p(model_p=θ_n, model_q=θ_0, ...)` (即 path C 之 'q' = gen-0)
- L2 form-borrow tier: q^{θ_0} 是 fixed base, 不是 chain training 之 EMA teacher
- D_paper relative-to-gen-0 form align: paper §6.2 之 D_n^{paper} = log(PPL_n/PPL_0) 也是 gen-0 anchored
- gen=0 之 path C trivially = 0 (sanity verify pipeline)

### 6.3 D_paper (paper §6.2)

```
D_n^{paper, relative} := log(PPL_n^{test} / PPL_0^{test}) = D_KL(q* || p^{θ_n}) - D_KL(q* || p^{θ_0})
```

- 单位 nat/token
- Source: chain log jsonl 之 `test_perplexity` 字段 (generation_done event)

### 6.4 D-1 严格度 caveat (binary 列, sub-agent 不 inflate)

- 路径 B + C 之 r 高 ≠ paper §3.6.2 main theorem (2) fixed-point identification close
- 必要 非 充分 — high r 可 by spurious co-monotonic decay (两 distinct random variables 各自 monotone decay) 而 achieve
- 真 L1 严 close 需路径 A (re-train EMA SGD replay) OR 路径 D (D60+ rerun chain with EMA save)
- within-seed gen-axis correlation 严重 → effective N < 80 → statistical power < ballpark (per design brief §6.2)

---

## 7. 9070XT 硬件 + VRAM budget

| item | spec |
|---|---|
| GPU | RX 9070 XT 16 GB ROCm Device 0 |
| OPT-125M fp32 weight | ~500 MB per model |
| 同时 load 2 模型 | ~1 GB |
| activation (batch=8, seq=64) | ~50 MB |
| 总 budget | ~1.1 GB (远 < 16 GB) |
| 当前 占用 (llama-server) | 14.39 GB (Qwen3-Embedding-8B-Q4) |
| 释放后 available | ~16 GB (well above 1.1 GB budget) |

---

## 8. ROCm hang watchdog 之 binary logic

per `watchdog.sh`:

| condition | action |
|---|---|
| log mtime stale > 5 min | kill -9 python, log "hang_kill", sleep 60 sec, relaunch |
| same tuple 3 fail in a row | 写 `escalate_d21.flag`, rsync push 7B13, exit 3 |
| python non-clean exit (non-kill) | 不重启 (script bug), 写 escalate flag, exit 4 |
| MAX_RETRIES (default 10) | 写 escalate flag, exit 5 |
| clean exit (Python 自己 done) | log "watchdog_end status=clean", exit 0 |

resume-from-last-checkpoint: launch_dppl_bridge.py 之 `load_done_tuples()` 之 logic 实现 — 启动时 read 之前 之 jsonl, skip 已 done tuples。

---

## 9. 错误 escalate path (per design brief §7.5)

| 错误 | 应对 |
|---|---|
| 9070XT venv 不装 | 跑 `archive/v1.0_release_20260516/scripts/install_rocm_torch.sh` |
| sudo password 卡 | 等 一凡 接 9070XT 显示器 输 password |
| pilot D_code = NaN/inf | 不 proceed main, surface 给 7B13 |
| pilot 数量级 异常 (< 1e-5 OR > 1e+2) | val batch reproducibility 失败 / tokenization mismatch, surface 给 7B13 |
| OOM | reduce --batch-size 8 → 4 → 2, fp16 fallback (caveat 数值 drift [?]) |
| ROCm hang | watchdog auto kill + sleep + resume |
| same tuple 3 hang fail | escalate flag + exit |
| 7B13 失联 (rsync target unreachable) | local 写 escalate flag + 继续跑 (main 不阻塞), 等 7B13 恢复 batch rsync |

---

## 10. 一凡 关卡 acceptance (D-1 binding 严守)

### 关卡 1 (D21 morning) — 一凡 confirm 本 dir + prompt
- [x] BC 然后 A serial (一凡 决)
- [x] stop llama-server pilot+main 期间 (一凡 决)
- [x] rsync (不 sshfs) (一凡 决)
- [x] tier r>0.7 / 0.3-0.7 / <0.3 (一凡 决)
- [x] pilot seed=1 gen=5 α=10 (一凡 默认接受)

### 关卡 2 (D22 morning) — 一凡 read PILOT_VERDICT_D21.md → main go/no-go
- 一凡 输 "main launch ✓" → 9070XT Claude launch main
- 一凡 输 "abort + debug X" → 不 launch, surface
- 一凡 输 "retract" → 不 launch, 9070XT Claude restart llama-server, exit

### 关卡 3 (D27-D30) — 反题 sub-agent zero-context audit
- 7B13 主会话 spawn 反题 sub-agent
- 输入: main_D21.jsonl + pearson_D24_summary.json
- 输出: 反题 audit markdown (zero-context, 不 read 主协作者 之 prior context)

### 关卡 4 (D30+) — 一凡 + DS + 反题 三方决
- 输入: 反题 audit + 数学线 sub-agent + 哲学线 sub-agent
- 输出: D-PPL 桥 result 之 落地 — enter paper v8.1 polish footnote OR D90+ paper v9 重 derive OR retract

---

## 11. D-1 binding 严守 statement (本 dir 之 sub-agent + 9070XT Claude 共)

1. 不 declare "P0★-F close" — 仅 surface raw 数字
2. 不 inflate "实验 success" — pilot pass ≠ paper success
3. 数字 全 jsonl-traced (D-1 纪律 1) — 任何 数字 必 traceable 到 jsonl entry
4. 占位符禁令 — unverified 数字 标 [?]
5. 真实日期 verify — 每 stage `date '+%Y-%m-%d'` binary print
6. proxy form 之 L2 严格度 caveat 实时 surface
7. 必要 非 充分 — high r ≠ stationary equality
8. 真 close 需 路径 A OR 路径 D D60+

---

**生成**: 2026-05-21 (D21) by 7B13 sub-agent (D-PPL 桥 verify launch 准备 sub-agent, 第十三波派遣)
**配套**: prompt → `literature/DPPL_BRIDGE_9070XT_PROMPT_D21_20260521.md`
**design brief**: `literature/DPPL_BRIDGE_VERIFY_EXPERIMENT_DESIGN_BRIEF_D21_20260521.md`
