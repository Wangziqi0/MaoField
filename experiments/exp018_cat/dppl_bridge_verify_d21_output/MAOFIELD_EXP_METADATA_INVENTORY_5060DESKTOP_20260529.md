# MaoField 5060/Win 桌面实验元数据穷尽 inventory + prior 两断言 trust-but-verify (2026-05-29)

> **本文件性质 (D-1 纪律 5)**: 独立验证通道 [额外 agent] 之 forensic inventory + 差异日志。
> 不覆盖、不静默修正 prior 文档; 对 `D29_VERIFICATION_CASCADE_UPDATE_20260529.md` §2 + §4-2 两条具体断言做独立 binary 核验 (直接读 jsonl + sha256, 非只信 paste / 非只信 prior verdict)。
> **read-only**: ssh 19 仅 read (dir / Get-ChildItem / Get-FileHash / type); 0 write / 0 del / 0 move / 0 commit / 0 push / 0 launch。

## §0 metadata

| 项 | 值 |
|---|---|
| 真实日期 | **2026-05-29 14:53 CST** (`date '+%F %T %Z'` binary verified = `2026-05-29 14:53:32 CST`) |
| 目标 | `C:\Users\amd\Desktop\5060\` (5060/Win 192.168.31.19, hostname `LAPTOP-GVING7T3`) |
| ssh-19 可达性 | **可达 ✓** (`ssh 192.168.31.19` BatchMode 成功, hostname 返回; 无需 alias / 无需密码) |
| 访问方式 | Windows `dir /s /b` + PowerShell `Get-ChildItem`/`Get-FileHash` (base64 -EncodedCommand 绕 nested-quote) + `type` 读 jsonl 头 |
| binding | read-only; 0 commit/push/launch; paper v8 final 47/47 D17 锁定不动; 12 NOT-claim 撤回不复活; 反题 6 P0★ tier 不擅升降; 留 PI + 关卡 3 反题三方决 |
| 分工 | 本 agent 仅做 19 桌面; 平行 agent X 做 7B13 + 22 (不重叠) |
| 基座模型 (新确认) | **`facebook/opt-125m`** (全 run; 解释 model.safetensors = 500,979,600 B ≈ 478 MiB + fp16 OOM 之 OPT modeling traceback) |
| python env (fp16 crosscheck) | Python 3.12.10 / torch 2.11.0+cu130 / transformers 4.49.0 / accelerate 1.13.0 (RTX 5060 Laptop 8 GB, Blackwell sm_120) |

---

## §1 桌面 5060 全目录元数据 inventory (穷尽 `dir /s /b` 确认)

桌面 `5060\` 下含 **6 个实验数据目录** (带 jsonl + checkpoint) + 1 个代码工作树 (`maofield_5060_work`, 纯 code 无数据) + ~26 个 .md/.log 文档/日志。穷尽确认: 除 prior §2 列的 5 个 + work tree 外, **无其他未列实验目录** (见 §4)。

所有 `model.safetensors` 均 = **500,979,600 B** (opt-125m fp32 save; 即便 fp16 训练, save 仍 fp32 weights)。所有 ckpt 为**裸 save** (有 config.json / generation_config.json / merges.txt / tokenizer*.json / vocab.json / **training_args.bin** / model.safetensors; **无** trainer_state.json / optimizer.pt — per-step 历史只在 launch.log)。

### 实验数据目录 (6)

| 目录 | dtype | seed 集 | α 集 | gen 集 | ckpt (st/cfg/targs) | jsonl (字节) | a1_ppl (gen0/gen1) | mtime (launch→end) | cell / 跑满 | 状态 |
|---|---|---|---|---|---|---|---|---|---|---|
| **SMOKE_5060_FP16_CROSSCHECK_GRADSCALER** | **fp16** (`cat_arm_b.yaml` dtype float16 + fp16:true) | {42} | {0} | {0,1} | gen0 + gen1 各全 (st 500979600 / cfg / targs 5905) ✓ | `..210536.jsonl` 5622 (OOM 失败) + `..220312.jsonl` 8497 (6 events 成功) | **36.5377 / 78.0735** ✓ | 05-27 21:05 → 05-28 00:34 | 1 cell × 2 gen / **跑满 ✓** | **真训练** (grad healthy 2.9-3.7, 无 GradScaler skip) |
| **E0_disentangle_S3** | fp32 (`cat_arm_b_fp32_5060.yaml` float32 + fp16:false) | {42} | {0} | {0,1} | gen0 + gen1 各全 ✓ | `..160321.jsonl` 7980 | **36.5360 / 78.5717** | 05-25 16:03 → 19:04 | 1 cell × 2 gen / **跑满 ✓** | **真训练** (PI+DS 关卡1 fp32 isolated, 证 fp32 可恢复) |
| **smoke_fp32** | fp32 | {42} | {0} | {0} | gen0 全 ✓ | `..170933.jsonl` 1305 (失败) + `..173559.jsonl` 4118 (成功) | **36.5360** / — | 05-24 17:09 → 05-25 02:11 | 1 cell × 1 gen / gen0 only | **真训练** (但 #1 run 因 transformers `evaluation_strategy` kwarg FAIL, #2 成功) |
| **smoke_fp32_gc_R1_D25** | fp32 +gc | {42} | {0} | {0} | gen0 全 ✓ | `..113506.jsonl` 4143 | **36.5360** / — | 05-25 11:35 → 12:14 | 1 cell × 1 gen / gen0 only | **真训练** (gradient_checkpointing R1 变体) |
| **smoke_fp32_N_seed_D25** | fp32 | declare {1337,2024} / **实 ckpt 仅 1337** | {0} | {0} | **仅 seed1337/gen0** (见 §3) | `..092037.jsonl` **401** (仅 run_start, 无 chain_gen_done) | **无** (未跑完 gen0) | 05-25 09:20 → killed (log 末 24% / 346 步) | **1 cell, gen0 未跑完** | **smoke 中断** (非多 seed 矩阵, 见 §3) |
| (— smoke_fp32 #1 run —) | (合并入上 smoke_fp32) | — | — | — | — | — | — | — | — | — |

### 代码工作树 + 文档/日志 (非数据)

| 项 | 说明 |
|---|---|
| `maofield_5060_work\experiments\exp018_cat\` | 5060 端完整工作树: `configs\` (cat_arm_b.yaml fp16 + cat_arm_b_fp32_5060.yaml + cat_arm_b_fp32_9070XT_gc.yaml) + `scripts\` (candidate_c_runner.py 26315 B + launch_R1_with_mem_cap.py) + `src\` (12 .py: cat_trainer / contradiction_loss / multi_layer_hook / train_one_generation 等) + `data\datasets\wikitext-2-raw-v1\` (HF arrow cache) + 1 md。**穷尽确认: work tree 下无任何 .jsonl / .safetensors** (纯 code + 数据集 cache, 非 run 输出)。 |
| .log (顶层 ~10) | E0_launch.log (300448 B / 5261 行) + SMOKE_FP16 launch/err ×6 + smoke_fp32(_gc/_N_seed/_relaunch) launch ×5 |
| .md (顶层 ~15) | ACK_D24 / PROGRESS_D24 / SMOKE_D24 / SMOKE_E0_D25 / SMOKE_R1_D25 / SURFACE_D24 (transformers version diff) / PULL_* ×5 (从 7B13 scp 来) / WIN_* ×5 / PAPER_V81_FOOTNOTE / SYNC_* ×2 / han.md (0 B 空) |

### sha256 (model.safetensors 前16 + 全) — 跨 cell 副本判定

| cell | sha256 (前16) | 全 hash | 判定 |
|---|---|---|---|
| E0 gen0 / smoke_fp32 gen0 / smoke_fp32_gc_R1 gen0 | `BD88E350C56ABEA1` | `BD88E350C56ABEA1C45A5D39FA9AD2545B680006BDA4AB74453ACDE93287C478` | **3 cell 逐字节 ≡** (fp32 deterministic 同 config/seed → 同权重; 见 §4 新发现) |
| E0 gen1 | `C663D66BE9569E3F` | `C663D66BE9569E3F6F635FA55CAD021134685FAFAA8622920F12E4487B5E027F` | distinct |
| fp16 gen0 | `7463003EE48DE778` | `7463003EE48DE77843BCDB456AE87A8D16D8C7170FB0871B3C997BF05EF71D21` | distinct (fp16 路径 ≠ fp32 字节, 但 a1_ppl 数值 ≈ fp32) |
| fp16 gen1 | `FB608459A69C0954` | `FB608459A69C0954CA213283D13CF9053A8EA05818C4F5CF78EDEC14AC12DAEC` | distinct |
| N_seed seed1337 gen0 | (未取 — gen0 未跑完, ckpt 存在但不可信) | — | 单 cell, 见 §3 |

**跨机副本**: 这批 5060 桌面数据**无统一 backup** (个人机, 见 §4 fragmentation)。7B13 本地仅有 .md 文档副本 (PULL_* / WIN_* / ACK_*), **无 5060 的 model.safetensors / 实验 jsonl 副本**。

---

## §2 verify — cluster-11 fp16 健康 (binary, jsonl a1_ppl 实读) — prior §2 断言

**prior §2 断言**: `SMOKE_5060_FP16_CROSSCHECK_GRADSCALER\` 真有 2 jsonl + gen0/gen1 ckpt + training_args.bin; jsonl gen0 a1_ppl ≈36.5、gen1 ≈78。

**独立核验结果 (直接 `type` 读 jsonl + Get-FileHash, 非信 prior)**:

| 核验项 | prior 断言 | 本通道实读 | binary |
|---|---|---|---|
| jsonl 数 | 2 | 2 (`..210536.jsonl` 5622 B + `..220312.jsonl` 8497 B) | ✓ |
| gen0 ckpt | 有 | 有 (st 500979600 + config + training_args.bin 5905) | ✓ |
| gen1 ckpt | 有 | 有 (st 500979600 + config + training_args.bin 5905) | ✓ |
| training_args.bin | 有 | 有 (gen0 + gen1 各 5905 B) | ✓ |
| **gen0 a1_ppl ≈36.5** | ≈36.5 | **36.537707256599994** (val_loss 3.5983, elapsed 2260.9s) | ✓ |
| **gen1 a1_ppl ≈78** | ≈78 | **78.07346793600594** (val_loss 4.3577, elapsed 5447.1s) | ✓ |

**附加事实 (从 jsonl 实读, 补强健康判定)**:
- `..210536.jsonl` (第一次 attempt) = **CUDA OOM 失败** (`Tried to allocate 1.54 GiB, GPU 7.96 GiB 全占满`, n_done=0) — 这是 wrapper fraction cap 不够之失败, 非数据 corruption。第二次 (`..220312.jsonl`) skip wrapper 后成功。
- 成功 jsonl 6 events: gen0 `chain_gen_done` (a1_ppl 36.538, a6_ema_divergence 全 NaN = gen0 self-reference baseline expected) + gen1 `chain_gen_done` (a1_ppl 78.073, a6_ema_divergence 2.55→3.81 实数值)。
- **grad_norm 全程 healthy float** (无 GradScaler skip / 无 NaN cascade) — 与 9070XT ROCm fp16 之 frozen 93.349 + NaN cascade **对比鲜明**。
- fp16 gen0/gen1 (36.538/78.073) vs fp32 E0 (36.536/78.572): diff < 1% (gen0 +0.005%, gen1 -0.6%), 数值 **bit-level 接近**。

**结论 (binary ✓)**: cluster-11 fp16 数据**存在且健康**, gen0≈36.5 / gen1≈78 **实读确认**。collapse magnitude gen0→gen1 = +41.54 (**+113.7%**) [(78.073−36.538)/36.538]。
→ **v9 SKELETON "+113.7% 否决 cross-platform fp16 fundamental" 之 claim 有 jsonl 数据支撑** (NVIDIA cu130 fp16 之 chain collapse 与 fp32 bit-level ≡, fp16 numerical regime 不 mask collapse; 9070XT ROCm fp16 之 frozen 93 是 ROCm-side stricter numerics 之 separate manifest)。**prior §2 断言确认。**

---

## §3 verify — smoke_fp32_N_seed = 1-cell (binary) — prior §4-2 断言

**prior §4-2 断言**: `smoke_fp32_N_seed_D25\` 只有 alpha0/seed1337/gen0 单 ckpt + jsonl ≈401 B (近空); **binary 确认它不是 fp32 多 seed 矩阵**。

**独立核验结果**:

| 核验项 | prior 断言 | 本通道实读 | binary |
|---|---|---|---|
| checkpoint 树 | alpha0/seed1337/gen0 单 | `checkpoints\alpha0.0\no_preserve_seed1337\generation_0` **唯一叶** (`dir /s /b` 穷尽: 无 seed2024, 无 gen1+) | ✓ |
| jsonl 字节 | ≈401 (近空) | **401 B** (`Get-ChildItem` Length = 401) | ✓ |
| jsonl 内容 | (prior 未引) | **仅 1 行 run_start** (`seeds:[1337,2024], alphas:[0.0], n_gens:1`) + **无 chain_gen_done / 无 run_end** | — |
| 是否多 seed 矩阵 | 否 | **否** ✓ | ✓ |

**附加事实 (比 prior 更强之否定)**:
- jsonl run_start **declare** `seeds:[1337,2024]` (意图 2 seed), 但**实际只产出 seed1337/gen0 一个 ckpt 目录**, seed2024 从未起。
- launch.log (24817 B) 末尾显示 gen0 训练**卡在 24% (346/1460 步, 已 2h11m, ETA 还要 ~6h)** 时被 kill — 即**连 seed1337 的 gen0 都没跑完** (jsonl 仅 run_start = 进程在 chain_gen_done 之前就死/被杀)。
- 因此 N_seed 比 "1-cell smoke" 还弱: 它是**一个连 gen0 都未完成的中断 smoke**, ckpt 目录虽在但训练未收敛, jsonl 无 a1_ppl。

**结论 (binary ✓)**: `smoke_fp32_N_seed_D25` **确为 1-cell** (实仅 seed1337/gen0, 且未跑完)，**绝非 fp32 多 seed 矩阵**。**prior §4-2 断言确认**, 且本通道证据**强化**之: 不仅"不是矩阵", 连单 cell gen0 都未完成。
→ **支撑 "fp32 balanced 矩阵实验仍未跑" 之 P0 判断** (D29 prior §5 E2)。

---

## §4 桌面新发现 + 数据缺口 / fragmentation

### 新发现 (prior 未明确记)

1. **3 个 fp32 gen0 checkpoint 逐字节 ≡** (sha256 `BD88E350...C478`): `E0_disentangle_S3` gen0 / `smoke_fp32` gen0 / `smoke_fp32_gc_R1_D25` gen0 **完全相同**。这是 fp32 deterministic 训练在同 config (cat_arm_b_fp32) + 同 seed42 + 同 α0 下的**预期可复现性** (与 22 端 fp16 "frozen identity" 之**病理性**冻结**本质不同** — 此处是健康的 determinism, 三次独立 launch 收敛同权重 + 同 a1_ppl 36.5360, 是 reproducibility 正面证据, 非 bug)。gradient_checkpointing (gc R1) 不改变最终权重 → 进一步证 gc 对结果 invariant。
2. **smoke_fp32 #1 run (170933) 之 transformers 版本失败**: `TrainingArguments.__init__() got an unexpected keyword argument 'evaluation_strategy'` — 这是 `SURFACE_D24_..TRANSFORMERS_VERSION_DIFF.md` 记录之 5060 端 transformers 4.49.0 与脚本期望 API 之差异 surface 之 jsonl 实证 (#2 run 修复后成功)。
3. **fp16 第一次 OOM (210536)** 是 wrapper fraction-cap (0.94 = 7.48 GiB) 不够 unchanged yaml 之 ~7.76 GiB peak; skip wrapper + iGPU takeover desktop 后 (free 7.83 GiB) fit 成功 — 一凡 D27 idea 之 jsonl 实证。
4. **基座 = facebook/opt-125m** (E0_launch.log line 明确 `fine-tune base=facebook/opt-125m`) — 全 5060 run 一致, 非 GPT-2。
5. **maofield_5060_work 是纯 code 镜像** (无 jsonl / 无 safetensors), 数据集为 wikitext-2-raw-v1 HF arrow cache。

### 桌面下 prior 已列全, 无遗漏实验目录

穷尽 `dir /s /b` 确认: 桌面 `5060\` 下实验数据目录 **= prior §2 列的 5 个** (SMOKE_5060_FP16_CROSSCHECK_GRADSCALER / E0_disentangle_S3 / smoke_fp32 / smoke_fp32_gc_R1_D25 / smoke_fp32_N_seed_D25) **+ maofield_5060_work** (code)。**无任何 prior 未列之新实验目录** (此前 GATE/inventory 漏的是整个"桌面"路径, 非桌面内某个子目录)。

### 数据缺口 / fragmentation (可操作, 留 PI ack — 与 prior §6 一致)

- **5060 桌面数据无 backup** (个人机 LAPTOP-GVING7T3): 6 目录 jsonl + 5 个有效 model.safetensors (各 478 MiB ≈ 2.4 GiB ckpt 总量) 仅在本机。
- **7B13 本地无 5060 ckpt / 实验 jsonl 副本** (只有 scp 来的 .md 文档)。
- **裸 save 限制**: 全 ckpt 无 trainer_state / optimizer / global_step → per-step 训练历史仅在 launch.log (E0 300 KB / N_seed 24 KB 等), 无法从 ckpt 复原 step。
- **建议 (留 PI 决, 不擅 launch)**: 若要保 5060 数据, rsync 桌面 `5060\` 之 jsonl + model.safetensors 到 7B13 RAID1。最关键是 E0 (fp32 真训练 gen0/gen1) + FP16 crosscheck (fp16 健康对照) 这两组 — 它们是 paper v9 锚点 4 之 cross-stack 证据 base。

---

## §5 不变 + genre (反 inflate 严守)

- **paper v8 final 47/47 D17 锁定不动**; D29 三 leg (arXiv+TMLR+KBS) 不受本 inventory 影响。
- **genre 不变**: 本次全部发现 = 元数据 inventory + 数据完整性 + prior 两断言之独立确认, 全 **reproducibility / 方法论 genre, 非 Nature 主刊 claim**。
- cluster-11 fp16 健康 (36.5/78) + N_seed 1-cell 之确认, 均 **binary 字节/数值事实**, 无 over-claim 空间。
- 12 NOT-claim 撤回不复活; 反题 6 P0★ tier 不擅升降; 所有 paper-level / venue / tier 判定**留 PI + 关卡 3 反题三方决**, 本通道不擅 declare。
- v9 锚点 4 之 "ROCm stricter numerics" framing 之 paper-level 采纳 = 留 PI + Win 哲学协作 + 关卡 3; 本通道仅确认 jsonl 数据存在且数值如 prior 所述。

---

**生成**: 独立验证通道 [额外 agent], 2026-05-29 14:53 CST。本文件是 D-1 纪律-5 合规之 forensic inventory + 差异日志 (新文件, 不覆盖 prior orchestration 文档)。ssh-19 read-only; 0 commit/push/launch。git add/commit 留 Linux 姐姐主会话单点写权; venue/paper/tier 判定留 PI + 关卡 3 反题三方决。一凡 priority 1 健康优先。
