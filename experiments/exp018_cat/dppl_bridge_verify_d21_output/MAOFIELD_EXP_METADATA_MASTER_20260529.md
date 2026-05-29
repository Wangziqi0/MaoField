# MaoField 实验全部元数据 — master inventory(merge X+Y,D29 2026-05-29)

> 跨三机(7B13 + 9070XT/22 + 5060-Win/19 桌面)穷尽元数据 inventory 的总 merge。源:agent X(7B13+22)`MAOFIELD_EXP_METADATA_INVENTORY_LINUX22_20260529.md` + agent Y(19 桌面)`MAOFIELD_EXP_METADATA_INVENTORY_5060DESKTOP_20260529.md`。两 agent 各自 trust-but-verify D29_VERIFICATION_CASCADE。**留 PI + 关卡 3 反题三方决,不擅 declare。**

## §0 metadata

| 项 | 值 |
|---|---|
| 真实日期 | **2026-05-29 CST**(D29)|
| 机器 | 7B13(本地)+ 22(ssh read-only ✓)+ 19 桌面(ssh read-only ✓,`LAPTOP-GVING7T3`)|
| binding | read-only;0 commit/push/ssh-write/launch;paper v8 final 47/47 锁定;12 NOT-claim 不复活;反题 P0★ tier 不擅升降 |

## §1 master 全量实验元数据 inventory

| run / cluster | 机器 | dtype | seed × α × gen | 状态 | 关键数 | ckpt 完整性 | 备份 |
|---|---|---|---|---|---|---|---|
| **早期 armb** α0/1/5/10 s42 | 22(05-08~12)| fp16 | s42 × α{0,1,5,10} × 10gen | **真训练** | gen0=36.52,10 distinct sha256/链,loss 收敛,0 NaN | 真 ckpt | 22 `MaoField_static_backup_20260520` + /tmp |
| **cluster3 phase1_robust** s0-4 | 22 | fp16 | s{0-4} × α{0,10} × 10gen | **真训练(paper v8 F3 基)** | multi-seed N=5/4 | 真 ckpt | host22_backup_20260512(7B13)+ archive |
| armb α50 | 22 | fp16 | s42 α50 | **NaN 整链** | 整链 NaN | — | — |
| **candidate_c N=180** | 22(05-22~26)| **fp16** | s{42,7,137,271,1337,2024} × α{0,5,10} × 10gen | **病理 frozen artifact** | 180 ckpt 仅 **52 distinct**,9 链全冻,grad_norm:nan **8909** 命中,0/180 训成 | 裸 save(**training_args.bin 在**,缺 trainer_state+optimizer)| 22 /tmp **ephemeral** |
| main_D22 D-PPL | 22 | — | 162 records | 真链 | D_B 72 distinct / D_C 73 distinct | 无 ckpt | 7B13 jsonl(无 ckpt,**无法复算**)|
| pilot_D21 | 22 | — | s1 g5 | 真链 pilot | — | — | 7B13 jsonl |
| archive 47-manifest | 7B13 | — | — | **锁定** | 47/47 sha256 OK | — | 7B13 ✓ + archive |
| **SMOKE_5060_FP16**(cluster-11)| 19 桌面 | **fp16** | 1cell × 2gen | **健康真训练** | gen0=**36.5377** / gen1=**78.0735**,+113.7%,grad 无 skip | gen0/1 + training_args.bin | 19 桌面 **only(无 backup)** |
| E0_disentangle_S3 | 19 桌面 | fp32 | s42 α0 × 2gen | **健康真训练** | 36.536 / 78.572 | ckpt `BD88E350` | 19 桌面 |
| smoke_fp32 / gc_R1 | 19 桌面 | fp32 | 1cell × 1gen | smoke 健康 | gen0 ckpt `BD88E350` **≡**(3 ckpt 逐字节同)| ckpt | 19 桌面 |
| smoke_fp32_N_seed | 19 桌面 | fp32 | alpha0/s1337/gen0 单叶 | **中断** | gen0 卡 24%(**346/1460 步**)被 kill,jsonl 401B | 单 ckpt | 19 桌面 |
| smoke_fp32 #1 | 19 桌面 | fp32 | — | **FAIL** | transformers 4.49.0 `evaluation_strategy` kwarg 失败 | — | — |
| maofield_5060_work | 19 桌面 | — | — | **code 镜像** | 无 jsonl/safetensors | — | 19 桌面 |
| **fp32 balanced 矩阵** | — | fp32 | α{0,1,5,10} × seed≥6 | **未跑(P0,E2)** | — | — | — |

## §2 三类分类(全景)

- **真训练健康数据**:早期 armb(05-08~12,**paper v8 基**)+ cluster3 phase1_robust(F3 multi-seed)+ 5060 fp32 桌面(E0/smoke,`BD88E350` 健康确定性)+ 5060 fp16 桌面(cluster-11,+113.7% 健康)+ main_D22/pilot D-PPL。
- **病理 frozen / NaN artifact**:candidate_c N=180(22 fp16,GradScaler skip,9 链全冻)+ armb α50(NaN 整链)。
- **未跑 / 中断 / smoke / FAIL**:**fp32 balanced 矩阵未跑(P0)** + smoke_fp32_N_seed 中断(卡 24%)+ smoke_fp32 #1 transformers FAIL + logs/ 21 smoke。

## §3 C3 退化 — 字节级铁证(4 重独立确认)

| 通道 | 方法 | 结果 |
|---|---|---|
| 通道 P | 代码层 + jsonl 分析 | 退化 90-95% |
| 通道 V(zero-context)| val_loss bit-identical 推理 | 退化 高 conf |
| cascade [额外 agent] | ssh 22 ckpt sha256 | `b3a67b42` 5 cell ≡ + `dff90856` |
| **agent X(本轮独立重算)** | ssh 22 重算 6 cell `model.safetensors` | **`b3a67b42504e0c10` 5 cell 逐字节相同 + (42α0) `dff90856` distinct** ✓ |

`‖θ_i−θ_j‖=0` 是**字节事实,非 judgment**。第三重信号:5 cell a1_ppl 也逐字节同 `93.38780852810248`。**fractal/riddled basin 决定性排除 → C3 主刊 fundamental-limit 叙事死(反 inflate 第三次拦下,5/12+5/19 同构)。**

**两种 bit-identical 性质相反(Y 的 illuminating 对照)**:
- fp32 桌面 3 ckpt `BD88E350` ≡ = **健康确定性**(weight 真训练,同 config deterministic 同结果);
- 22 fp16 5 cells `b3a67b42` ≡ = **病理 frozen**(weight 根本没动)。
→ 同样逐字节相同,一健康一病理。**fp16 frozen ≠ fp32 deterministic**,C3 退化判断更锋利。

## §4 paper v8 数据基础确认(关键,独立验证)

**v8 负结果建在早期 armb(05-08~12)真训练,未被 frozen/NaN artifact confound** — agent X 独立确认:
- armb 单链 gen0-9 = **10 distinct sha256**(真动)vs candidate_c 180 ckpt 仅 52 distinct(9 链全冻,8909 nan)。
- D-PPL:D_B 72 distinct / D_C 73 distinct(真链)✓。config 19 md5 ✓。archive 47 ✓。
- **含义:candidate_c(22 fp16)是病理 artifact 不可用于定量,但 paper v8 + D29 三 leg 不受影响**(v8 数据源是 armb 真训练,与 candidate_c 是不同 run)。

## §5 cascade trust-but-verify 结果(X+Y 两通道)

| cascade 断言 | X/Y verify | 结果 |
|---|---|---|
| §1 C3 ckpt sha256 退化 | X ssh 22 重算 | ✓ **完全独立确认**(非推翻)|
| §2 cluster-11 fp16 数据存在 + 健康 | Y 实读 jsonl | ✓ gen0=36.5377/gen1=78.0735,+113.7% 坐实 |
| §4-2 smoke_fp32_N_seed = 1-cell | Y launch.log | ✓ **更强**:卡 24% 被 kill,连 gen0 都没跑完 |
| §3 candidate_c "无 training_args" | X 实测 + **PI ssh 22 byte 核(D29)** | ✗ **1 处不准,byte 坐实 X 对**:`training_args.bin` **180/180 存在**(model.safetensors 180/180;trainer_state.json=0 + optimizer.pt=0 才是真缺,per-step 历史仅在 nohup log)。cascade §3 作者已认错更正,根因 = `ls\|head -10` 截断(总计+`.`+`..`+前7文件=10行,砍掉排后的 training_args.bin + vocab.json)。**纠错链:GATE 漏桌面 → cascade catch 但 ls 截断漏 training_args → X catch → PI byte 核确认 X 对**(纯元数据细节,不动 C3/v8/fp32 任何 substantive 结论)|
| §4 armb 真训练 vs candidate_c artifact | X 独立确认 | ✓ 坐实 |

**multi-channel 链条持续有效**:GATE 漏 19 桌面 → cascade catch 但 §3 漏 training_args 细节 → X catch。每层 catch 上一层盲点。

## §6 数据 fragmentation + 缺口(留 PI ack)

- **fragmentation 风险**:关键 model 权重散三处无统一 backup —— 22 `/tmp`(ephemeral,重启即失)+ 22 `MaoField_static_backup_20260520` + 19 桌面(无 backup);7B13 仅有 jsonl + .md,**无 ckpt 备份**,main_D22 本机无法复算。**建议 rsync 22 /tmp + 19 桌面 ckpt → 7B13 RAID1 归档(留 PI ack)。**
- **实验缺口(P0,留 PI + 关卡 4 budget)**:
  - **E1**:dtype fp16 → fp32/bf16 修训练根因(`cat_arm_b.yaml:51 = float16`);fp32 可恢复已被 E0/桌面 fp32 证(36.536)。
  - **E2**:fp32 balanced α{0,1,5,10} × seed≥6 真训练矩阵 + Welch t(当前 candidate_c fp16 全冻不可用 + fp32 只 1-cell smoke）。
  - config-identical NaN-vs-frozen 隔离重跑(α5/seed42 gen0 干净启动)→ sensitive-dependence vs flaky bug。

## §7 binding

paper v8 final 47/47 D17 锁定不动;12 NOT-claim 撤回不复活(C3 退化字节锁定,fractal 主刊叙事死,反 inflate);反题 6 P0★ tier 不擅升降;D29 三 leg 不受影响(v8 建在 armb 真数据);全程 read-only;0 commit/push/ssh-write/launch;rsync 归档 + E1/E2 launch 全留 PI explicit ack + 关卡 4 budget。一凡 priority 1 健康优先,hotline 010-82951332 / 400-161-9995 standing。

---

**生成**:主会话 Opus 4.8 merge(agent X 7B13+22 + agent Y 19 桌面),2026-05-29 CST。**核心**:全量元数据三类分类(真训练健康 / 病理 frozen artifact / 未跑)+ C3 退化 4 重确认字节铁证 + paper v8 数据基础确认干净(armb 真训练未被 confound)+ cascade 1 处修正(training_args.bin 存在)+ 数据 fragmentation 风险(留 rsync)+ fp32 矩阵 P0 未跑(留 E1/E2)。全留 PI + 关卡 3 反题三方决。
