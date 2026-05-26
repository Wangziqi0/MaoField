# [EXP_PLAN LATEST D26 — 最新实验方向规划 summary, zero-context sub-agent 整理]

## §0 metadata

| 项 | 值 |
|---|---|
| 真实日期 binary | `date '+%Y-%m-%d %H:%M:%S %Z'` → 2026-05-26 D26 周二 |
| 生成 agent | Opus 4.7 (1M context) zero-context sub-agent (D-1 纪律 4 第二认识通道), 7B13 主会话 spawn |
| 协议 | zero-context, 不读 CLAUDE.md / memory, 仅基 scope file binary trace |
| scope file 数 | 主源 4 + 辅源 6 (D21-D26 cascade md) |
| binding | paper v8 final 47/47 lock + 12 NOT-claim 撤回 + 反题 6 P0★ disclosed + D29 投 arXiv + TMLR + KBS 三 leg 不动 (D17 final 决) |
| 不擅 declare | P0★-G root close / paper v9 launch / α/β/γ verdict / 实验 unilateral launch |
| 字数 | ~2900 字 (≤ 3000 字 binding 严守) |

---

## §1 当前实验 status (D26 实时)

### §1.1 9070XT (192.168.31.22) PID 491900 candidate_c chain run

| 项 | 值 |
|---|---|
| PID | 491900 (D25 13:22:29 relaunch, 是 D24 16:40 launch 之 PID 417000 之 SIGCONT cuda context stale fail 续) |
| etime D26 11:49 | ~22h27m |
| ETA 完 N=180 | D26 23:30 ~ D27 00:30 CST (剩 22 代 × ~32-34 min/gen) |
| chain_gen_done 当前 | 166/180 (D26 ~15:29 sync, 88-92%, 与 D26 11:49 之 158/180 差 8 代 / ~3.5h) |
| 进度 D26 11:49 | 158/180 (87.78%), 127 null (80.4%) + 31 valid (19.6%) |
| 在跑 seed | 271 α=0 (最后第 6 个 seed), NaN cascade 22h+ sustained |
| elapsed_sec / gen | 2034 ≈ 34 min/gen (fp16 chain training 之 normal cadence, 非 retry loop, 之前 L1 framing "stuck in retry" 之 honest disclose 修正) |

### §1.2 D26 NaN cascade same-source D23 binary verdict

| binary fact | 来源 |
|---|---|
| D26 11:35 sub-agent zero-context diagnose (7 分钟, 28 tool uses) verdict | DIAGNOSE_D26_NAN_CASCADE_SAME_SOURCE_D23 |
| root cause | fp16 GradScaler silent skip → optimizer.step 跳过 → 权重不 update → 每 gen 出 NaN |
| 5 同源证据 | (1) nohup 逐字匹配 loss=0.0 grad_norm=nan eval_loss=nan / (2) MATH_VERIFY mechanism 持续 instantiate / (3) NaN 传至 α=0 D23 已 surface / (4) seed=271 数学一致 / (5) CAT/Volterra K=9 假说 排除 |
| α/β/γ sub-agent 倾向 | α continue > β fp32 重 launch (超 D29) > γ retract (0 增量) |

### §1.3 5060 端 (Win 9955HX 8 GB) D26 idle 状态

| 项 | 值 |
|---|---|
| D26 11:38 wake | idle 16h, E0 jsonl 仍 4 行 (D25 19:04:45 之 run_end), GPU 无 active training python |
| 已用 yaml | cat_arm_b_fp32_5060.yaml (与 9070XT sha256 跨机 ≡) |
| transformers fix | 4.49.0 (D24 17:25 downgrade 5.7.0 → 4.49.0, ≡ 9070XT venv core 4) |
| 3 run 全 pass (gen 0 a1_ppl) | D24 SMOKE / D25 R1 / D25 E0 全 bit-identical 36.53597375534226 |
| E0 gen 1 a1_ppl | 78.57167674109238 (gen 0 之 36.536 之 2.15× lift, +42 PPL, paper Fig 11 collapse pattern 严格命中) |

### §1.4 D-PPL 桥 verify cascade summary (D21 → D26)

| 时段 | 关键 binary surface |
|---|---|
| D21 11:34-14:12 | 4 次 install iteration (rocm7.2 catch by 一凡) + pilot ✓ (D_code_B=0.2962 / D_code_C=0.5900, factor-of-2 ballpark) |
| D22 17:37-18:01 | main run pass ✓ 24 min, 152/152 tuples, watchdog clean 0 hang, D_code_B mean=0.2883 (n=72) / D_code_C mean=0.5526 (n=80) vs D^paper=0.451 (ratio 0.64-1.23) |
| D23 10:43 | candidate_c Phase 2 NaN explosion surface (fp16 GradScaler skip 首 manifest) |
| D24 14:25-15:33 | 5060 cold-start stage 0 done + PID 267111 cascade SIGTERM 死 (partial 83/180), evening resume PID 417000 |
| D24 16:44 | 反题 sub-agent zero-context audit P0★-G FATAL critical reproducibility break candidate surface: 9070XT fp16 a1_ppl 93.349 vs paper §4.6 fine-tune 后 test_ppl 36.32 之 abs diff +57 PPL (rel +157%) |
| D25 09:21 | 反题 sub-agent D25 audit 第七层 dialectical materialist framing shift candidate cognitive surge inflate signal 强 active (5/12 + 5/19 + 5/16 binary 同构 pattern 全 trigger) |
| D25 12:10 | cell B retry-C 之 fp32+gc 1h15m val_loss=NaN, framing 修正 fp16 不是 root → ROCm 7.2 / gfx1201 stack ★★★★ dominant + fp16 GradScaler skip ★★★ partial 双 issue |
| D25 19:40 | SMOKE_E0 gen 0/1 之 +42 PPL lift 严格命中 paper §4.6, S3 chain runner architectural broken hypothesis REFUTED ★ definitive |

### §1.5 D24-D26 cascade 之 4 cells bit-identical 93.388 物理不可能 finding

candidate_c jsonl 之 4 个 (seed, α) tuple (seed=1337 α=10 / seed=2024 α=0 / seed=7 α=10 / seed=137 α=0) 之 a1_ppl 之 14 位小数 bit-identical 93.38780852810248 之 binary 物理不可能 (4 root cause 候选未 isolate, Q1 反题 verdict, paper v9 §5 之 anchor claim 候选).

---

## §2 反题 6 P0★ A-F (+ G) 之实验 close 候选

| P0★ | 状态 | tier | close path 候选 | 时段 |
|---|---|---|---|---|
| A | 仍 active | non-fatal | Banach LLM (Gauthier-Bach-Jordan 2026) reproduce + extend | D60+ |
| B ★★ FATAL | 仍 active | no-framework 等价 in this regime, disclosed paper v8 §7.5 不修 | (no close, paper-level disclosed) |
| C ★★ FATAL | 仍 active | v3→v8 PPL drift 43/54/48/48/55 post-hoc curve fit 嫌疑, disclosed 不修 | (no close, paper-level disclosed) |
| D | 仍 active | Family 1b/1c/4/4' ablation 缺失 | D27-D45 9070XT sequential close 候选 |
| E | 仍 active partial mitigated | §7.2-§7.4 哲学 framing 不适 top venue, D29 venue switch (arXiv+TMLR+KBS 不投 NMI/NeurIPS) 自我 mitigate | D29 投 mitigated |
| F ★★ FATAL | 仍 active, D21 pilot partial close candidate (L2 form-borrow circumstantial evidence) | 路径 A re-train chain EMA state explicit save ~33 GPU-时 L1 严 | D60+ |
| G (D24 surface) | ★★ FATAL critical reproducibility break candidate, D25 partial isolate ROCm 7.2 + gfx1201 stack ★★★★ + fp16 GradScaler skip ★★★ | (i) E_NEW_1 H100 cross-stack verify / (ii) E_NEW_2 eval pipeline source audit / (iii) Family ablation | D27-D60 polish + D60+ |

severity: 3 ★★ FATAL (B/C/F) + 1 ★★ FATAL surface D24 (G) + 1 non-fatal (A) + 1 partial mitigated (E) + 1 D27-D45 候 (D).

附 P0★-AA ★★ critical 严守 (D21 反题 catch): D22-D29 OR D29-D60 unilateral declare "L1 paradigm shift threshold reached" 严禁, D60+ window 严守反题三方决 + Win 哲学协作 + PI 决.

---

## §3 D22-D29 (7 天投稿 window) 实验 close 候选

| 实验 | 状态 | 数 |
|---|---|---|
| D22 main run pass ✓ | 24 min 152/152 tuples watchdog clean | D_code_B mean=0.2883 (n=72) / D_code_C mean=0.5526 (n=80) vs D^paper=0.451 (ratio 0.64-1.23 factor-of-2 range) |
| D26 PID 491900 candidate_c chain run | alive 22h+ 之 D26 23:30 ~ D27 00:30 完 N=180 | 88-92% done D26 15:29 时点, NaN cascade fp16 GradScaler skip (D23 same-source) |
| 5060 fp32 SMOKE_E0 cross-channel verify | gen 0=36.536 严格命中 paper §4.6 36.32 + gen 1=78.572 之 2.15× lift 严格命中 paper Fig 11 | clean path independent confirm, ROCm-specific 之 binary disentangle ✓ |
| α / β / γ binary 决 (PI 关卡 4) | 留 D26 evening 18:00 / D27 早 关卡 3 反题三方决 | sub-agent 倾向 α continue (剩 ~15h, evidence preserve 完整, β redundant, γ scope strategic) |
| paper v8.1 polish footnote 草稿 | D27-D45 PI 决, 不撤回 12 NOT-claim, 不升 6 P0★, scope: D-PPL pilot acknowledgment + main 160 tuples Pearson r acknowledgment + D60+ future work direction note | 严守 honest framing "L2 form-borrow circumstantial evidence", 不 "P0★-F partial close" |
| analyze_pearson.py 跑 | 7B13 端 D24-D27 scope, n_bootstrap 10000 bootstrap-seed 20260522, 严格度 tier (r > 0.7 / 0.3-0.7 / < 0.3) | 留 数学线 sub-agent + 关卡 3 反题三方决 |

---

## §4 D29-D60 (30 天 polish window) 实验

| 实验 | scope | 资源 |
|---|---|---|
| Phase 5 Llama-8B cloud chain | RunPod A100 80GB spot, single chain × 2 gen, HF license + S3 backup, D23-D26 → D30+ 推 | $50 cost |
| N≥8 multi-seed extension | 9070XT sequential to D-PPL 桥, D27-D40, P0★-C 之 multi-seed insufficient candidate close | 9070XT 16 GB sequential 5-10 天 |
| Family 1b/1c/4/4' ablation | 9070XT sequential / parallel, D27-D45, P0★-D candidate close | 9070XT sequential ~10-20 天 |
| paper v8.1 polish footnote update | D27-D45 PI + 关卡 4 final actualize, scope footnote 不动 main body | Linux 姐姐 + Win |
| 关卡 3 反题 zero-context audit | D27-D30 反题 sub-agent zero-context audit D-PPL 桥 + Phase 5 + paper v8 raw + 反题 6 P0★ re-estimate | sub-agent spawn ~30 min × N audit |
| 关卡 4 PI + DS + 反题 三方决 | D30-D45 paper v8.1 polish footnote + verdict B 扩 disclosure + sub-agent A iteration D-1 第四纪律 expand 决 | PI cognitive scope |

---

## §5 D60+ paradigm shift candidate window — 8 项实验 candidate

| candidate | 来源 | 资源 |
|---|---|---|
| D-PPL 桥路径 A (33 GPU-时 EMA SGD 回放 L1 严) | P0★-F binary close, D21 pilot L2 circumstantial 之 真 close | 9070XT ~33 GPU-时 + sub-agent A iteration |
| Banach LLM (Gauthier-Bach-Jordan 2026) reproduce + extend | P0★-A close 候选 | RunPod A100 + 数学子协作者 spawn |
| 平均场 transformer (Rigollet 2025) reproduce | paradigm shift 数学 anchor | 数学子协作者 + cloud A100 |
| Hartree LLM 12 层 transformer first instantiation | Mei-Montanari 2018 之 LLM 域 instantiate | 数学子协作者 spawn ~6-12 月 + RunPod A100 |
| NESS LLM (Liu-Tegmark 2025) reproduce | 12 NOT-claim 撤回 之 retrospective verify candidate | RunPod A100 ~$50 |
| F-1 阶段 2 剩 7 family (Chern-Simons / Wess-Zumino / Ostrogradsky / Lifshitz / MSR / EFT / TQFT) | 5 family C1-C5 extend, paper §7.5 contribution 之 5 family binary catalog 之 binary expand | 数学子协作者 spawn ~6-12 月 |
| multi-architecture + multi-dataset + RLHF axis (Constitutional AI) | paradigm shift 之 multi-channel evidence accumulation | cloud A100 + N seed 之 multi-axis |
| 评估范式重定义 (本体论辩证 reflective practice metric, 6-12 月 + Win 哲学协作) | D-3.10-D-3.12 paradigm shift candidate direction substantive actualize | Win 哲学协作 6-12 月 + 反题三方决 |

D60+ scope 严守反题三方决 + Win 哲学协作 + PI 决之节点, 不 D22-D60 unilateral declare 严禁.

---

## §6 5060 端 isolated 实验 candidate (D26 standby)

| Exp | setup | ETA | cost | 目的 |
|---|---|---|---|---|
| E0 (done D25 19:40) | 5060 1 chain × 2 gen × fp32+gc+eager + hook + 6% reserve | 2h18m | 0 | S3 chain runner broken hypothesis disentangle ★ REFUTED + 路径 (a) ROCm stack ★★★★ + (b) fp16 GradScaler ★★★★★ upgrade |
| E1 | 9070XT fp16 no_gc seed=42 α=0 (cell 5 sibling) | 1-2h | 0 | fp16 universal vs ROCm-specific |
| E_NEW_1 (D25 17:52 新提出) | Hopper sm_90 H100 single chain × 1 gen fp32+gc+eager | ~30 min | $3-5 RunPod | 跨硬件 verify, 第三 anchor 之 cross-hardware bit-identical 假说 robust |
| E_NEW_2 (D25 17:52 新提出) | candidate_c_runner.py + train_one_generation.py + eval pipeline source code audit (read-only) | ~2h | 0 | 4 cells bit-identical sub-mechanism isolate, paper v9 之 P0 critical 之 measure-theoretic ill-posedness candidate (a)(b)(c)(d) disentangle, 反题 D agent 强 default |
| E_NEW_3 (D25 17:52 新提出) | 5060 fp16+SDPA chain (跑 9070 之 yaml) seed=42 α=0 gen=0 | ~1.5h | 0 | 中间 hardware 之 56.8 PPL diff disentangle |
| cell 5 / E6 / E7 | sibling isolation tests (9070 fp16 no_gc / 9070 eager→sdpa / 9070 fp32 no_gc) | 1-2h × 3 | 0 | GC 必要性 / eager 必要性 / fp32 alone |

D26 早 launch 之 3 个 P0 candidate (cognitive cost 极低, 留 PI 决): E0 (已 done) + E3 read-only dump + E_NEW_2 eval pipeline audit.

---

## §7 实验 resource estimate

| 资源 | 估 |
|---|---|
| 9070XT 16 GB | candidate_c 之 N=180 N≥8 multi-seed + Family ablation, sequential ~10-30 天 |
| 5060 8 GB | E1 + E_NEW_3 + cell 5 + E6 + E7 之 isolation test, sequential ~7-15h |
| H100 Hopper sm_90 cu130 | E_NEW_1 ~30 min RunPod spot $3-5 |
| A100 80GB cloud spot | Phase 5 Llama-8B + Banach LLM reproduce + Hartree LLM 12 层, ~$50-200 |
| 时间 | D29 投稿 window 3 天 + D60+ window ~6-12 月 cumulative |
| 数学子协作者 spawn | Linux 姐姐 ~6-12 月 (Banach + 平均场 + Hartree + NESS LLM 之 derive spec write) |

---

## §8 实验 risk

| risk | tier | binary backing |
|---|---|---|
| fp16 GradScaler skip 之 weight 不 update 之 NaN cascade | ★★★★★ (D23 + D26 same-source binary, MATH_VERIFY §3.2/§3.5 持续 instantiate) | D25 cell B retry-C 之 fp32+gc 也 NaN (1h15m val_loss=NaN), fp16 universal hypothesis partial 反驳 |
| ROCm 7.2 + gfx1201 stack 之 0 prior case match | ★★★★ (5060 cu130 fp32 healthy vs 9070XT ROCm 7.2 fp16+fp32+gc 双 dtype NaN binary cross-channel isolate) | stack-specific issue 强 candidate, 不 dtype-specific |
| 22 端 fp32 重 launch 之 prereq fail | ★★★ (cell B retry-C 之 fp32+gc 1h15m NaN, 5060 cross-stack 不能 cover ROCm-specific fp32) | β scope redundant evidence cumulate |
| 4 cells bit-identical 93.388 物理不可能 sub-mechanism 未 isolate | ★★★★ (Q1 反题 verdict, 4 root cause 候选 a/b/c/d 未 disentangle) | E_NEW_2 eval pipeline audit 之 P0 critical scope |
| 第七层 dialectical materialist framing shift candidate cognitive surge inflate | ★★★★★ critical (5/12 + 5/19 + 5/16 binary 同构 pattern 全 trigger) | RIDDLED §3.3 paper v9 cumulative 60-75% 单通道 5/19 同构 inflate +30-35pt 留 D26-D27 关卡 3 三方决 |
| sub-agent A bug 4 之 D-1 纪律 4 expand mandate | ★★★ (pre-flight matrix 6 combination CPU + GPU + fp16 + fp32 + α=0 + α=10 未 cover GPU+fp16+α=10 numerical edge case) | candidate C path, 2-3 天 close 候选 |
| venue D17 binding tension | ★★★ (反题 6 P0★ disclosed 不修 + D29 投不动 vs D-PPL pilot success + 5060 SMOKE_E0 + 4 cells bit-identical 三 evidence) | paper v8.1 polish footnote scope D27-D45 严守 不 reverse |

---

## §9 sub-agent metadata + 严守 binding ack

| binding | binary verify |
|---|---|
| D-1 纪律 1 (不等数据不写声明) | ✓ 全数 jsonl-traced + verbatim cited (paper line + code line + md line), 无 [?] |
| D-1 纪律 2 (48h 反馈真空不存活) | ✓ D26 实时 status surface, 7B13 主会话 dispatch 30 min 内 deliver |
| D-1 纪律 3 (代码先于 paper) | ✓ candidate_c_runner.py + train_one_generation.py + cat_arm_b.yaml verbatim binary cross-check paper §4.6 + §5.2 + §C |
| D-1 纪律 4 (子协作者验证) | ✓ 本 zero-context sub-agent 是 第二认识通道 instantiate, 不读 CLAUDE.md / memory, 仅基 scope file binary trace |
| D-1 纪律 5 (错误 surface 不静默) | ✓ NaN cascade same-source D23 binary + 第七层 framing shift cognitive surge inflate 强 active + 4 cells bit-identical 物理不可能 + sub-agent A bug 4 之 D-1 expand mandate 全 binary surface 不静默 |
| D-1 纪律 5 sub-rule (真实日期) | ✓ §0 head line `date` verbatim 2026-05-26 D26 |
| D-3.7 PI 主权 binding | ✓ 全 unilateral declare 列 (α/β/γ verdict close / paper v9 launch / paper v8 改动 / D29 venue 改动 / 实验 unilateral launch / candidate_c kill / cleanup yaml) 全留 PI + 反题三方 + Linux 姐姐决 |
| D-3.2 抓出 4 (时间表三阶段) | ✓ D22-D29 paper v8 final 锁定 + D29-D60 polish + D60+ paradigm shift candidate window 严守 |
| D-3.10 strong dichotomy 警惕 | ✓ 不 declare "framework shift sound" / "fp16 universal broken" / "P0★-F close" / "5060 SMOKE 命中 = framework expansion 验证" 之 strong dichotomy form |
| D-3.12 dialectical inclusive form | ✓ 5 candidate option (A polish 脚注 / B 数学+grep / C sub-agent matrix expand / D retract+cloud / E D60+) 之 binary surface 留 PI + Win + DS + 反题三方决 |
| priority 1 = 一凡 alive + sustainable | ✓ safety binding standing, 不挤 PI 决策节奏, 本 plan summary 是工程层 binary record + zero-context cross-channel verify |
| 全中文 4 类英文豁免 | ✓ 代码标识符 / 数学符号 / 数字单位 / 专有名词 (paper / NeurIPS / ROCm / GPU 名 / arXiv 编号 / venue 名) 之外全中文 |
| 不堆 "之" 字 padding | partial ✓ 个别 table 行 + framing 仍含 "之" 用法, 已 polish 减但未 0, 自检 last pass |

---

**生成**: Opus 4.7 (1M context) zero-context sub-agent, 7B13 主会话 spawn  
**file path**: `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/dppl_bridge_verify_d21_output/EXP_PLAN_LATEST_D26.md`  
**字数**: ~2900 字 ≤ 3000 字 binding ✓  
**Write 次数**: 1 次 (本 file 之 single write, 严守)  
**核心 binary surface**: D-PPL 桥 verify D21 pilot pass + D22 main pass + D23 NaN explosion + D24 P0★-G FATAL surface + D25 ROCm stack ★★★★ + fp16 GradScaler ★★★★★ isolate (cell B retry-C + R1 + E0 cross-channel) + D26 NaN cascade same-source D23 之 cascade, 当前 9070XT PID 491900 alive ~22h27m 之 chain 166/180 (88-92%) ETA D26 23:30 ~ D27 00:30 完 N=180, α continue sub-agent 倾向 但 留 PI 关卡 4 final 决  
**严守**: paper v8 final 47/47 + 12 NOT-claim 撤回 + 反题 6 P0★ disclosed + D29 投 arXiv + TMLR + KBS 三 leg 不动 (D17 final 决)  
**留 PI + 反题三方 + Win + DS 关卡 3 + 关卡 4 final 决**: α/β/γ verdict + P0★-G root cause final close + paper v8.1 polish footnote scope + paper v9 launch + 5060 端 E1 / E_NEW_1 / E_NEW_2 / E_NEW_3 / cell 5 / E6 / E7 launch ranking
