# exp020 §D flux 判别器 spec · base-reset vs Borkar c·μ · DRAFT **v2** (D618)

> 反题 dispatch §B/§D 定的**真生死线**: flux 必须证 base-reset 注入的锚定**不能**被 Borkar 2506.09401 的 c·μ (经 sample 的 persistent excitation) 解释。
> **v2 = 敌意子 agent (§H-a, default-to-refute) verdict 采纳后重写。** 主会话已亲核全部载重代码事实 (见 §1)。
> 状态: DRAFT v2, 未进 prereg。**§E commit-lock 现 blocked on PI 关卡 (M3 需新 step-sweep 实验, 见 §3/§7)**。Linux 只递测量/数学事实, framing 归 Win+PI。

## 0 crux 问题 (一句话)
base-reset (`base-mode gen0`: 每代权重从 θ₀ 重初始化再 fine-tune 合成数据) 是一条**经权重的真实信息锚**, 还是只是 Borkar c·μ (经 sample 注入 fraction c 真数据 μ₀) 的换皮?

## 1 装置事实 (主会话亲核 D618; 子 agent 独立 trace 一致)
- **c=0 实锤**: `run_arm_b_ablation.py` gen≥1 训练数据 = `build_mixed_generation_dataset(..., original_fraction=condition.original_data_fraction)`, no_preserve→`cat_arm_b/shumailov_baseline.yaml: original_data_fraction: 0.0`。4 cell 真数据占比 **c=0**。✓
- **base-mode**: `base_model_path = gen0_dir if base-mode==gen0 else prev_gen_dir`; `train_one_generation.py:105` 每代 `from_pretrained(base_model_path, torch_dtype=float32)` 全新 reload。base-reset = 每代权重真从 gen0 ckpt 重载。✓
- **⚠️ 勘误 (v1→v2, 攻击点1地基)**: reset 目标 = **`gen0_dir` = HF base (`cfg.model.hf_id`=opt-125m) 在真 wikitext-2 上 fine-tune 过的 gen0 模型** (`run_arm_b_ablation.py` gen0 分支 `base_model_path=cfg.model.hf_id` + train_blocks 真数据), **不是 raw HF 预训练初值**。θ₀ **已编码 μ₀**, 是见过真数据的训练产物, 非中性初值。
- **精度**: 训练 model dtype=fp32, 但 `fp16:true` 控 mixed-precision autocast + **GradScaler** (skip-on-inf 活跃)。`save_strategy:"no"` → val 只测量不选模型。
- **Borkar 2506.09401 实模型** (子 agent fetch PDF; **paper-verbatim 前主会话须人工再核 §2-3 update eq + Assumptions**): 作用于**概率测度 μₙ**, recursion `μₙ₊₁=(1−α)μₙ+αμ₀`, α=数据混入 fraction(=c)。**de novo 训于 μₙ, 无权重通道、无 θ₀ 重置**。

## 2 杀手论证 (v2 收紧; 子 agent 攻后唯一不可换皮的刀)
**v1 旧版"c=0 是 Borkar 盲区"强度不足** (没堵 effective-prior 重写)。**v2 收紧到正交自由度**:
- early-stop 从固定 θ₀ 出发 ≅ L2-to-init 正则 (标准结果): θ_n ≈ argmin[L_synth(θ;D_n) + (1/2η_eff)‖θ−θ₀‖²], **effective-prior 权重 w_eff ∝ 1/η_eff = 1/(η·T)** (η=lr, T=步数)。
- **base-reset 锚 = param-space prior, ∝ 1/η_eff (优化几何)**; **Borkar α=c = measure 凸组合系数 (数据管线属性), 与 η/T 无关**。两者是**正交的两个旋钮**: 可 c=0 且 w_eff>0 (本装置), 可 c>0 且 w_eff=0 (训到收敛+数据混入)。
- ⇒ **无 base-reset→effective-c 的满射映射** (c 是 measure-mixture 系数, w_eff 是 param-prior 系数, 维度/单位不同)。能构造 effective-**prior** ⇏ 塌回 Borkar; 它需外挂权重几何 (H₀,η_eff,θ₀), **恰是本文 distinction 本身**。
- **distinction 在数学层 SURVIVES** (子 agent 攻击点1+3): wedge 不塌回 Borkar 已占。

## 3 判别测量 (v2 重排; decode-free, CPU@36 offline)
**M3 = 主判别器 (v1 误标"可选"; 子 agent 攻击点2 后升级)** — 唯一正面分"经初值"vs"经数据"的签名:
- 预注册: **base-reset 锚强度对 (fine-tune 步数 T / lr η) 单调依赖** (∝1/η_eff)。base-reset: T↑/η↑ → θ₀ 被覆写 → 锚↓; Borkar c·μ: 锚 ∝c, **独立于 T/η**。
- **⚠️ 需新 step-sweep 实验** (同 cell 扫 2-3 个 epochs/lr, gen1-3 即可, 相对廉价): 当前 Stage-A 固定 epochs/lr **测不出 M3** → **PI 关卡 (§7)**。

**M1 = 降级为 sanity-check (v1 当主判别器 = 错; 子 agent REFUTED)**:
- ‖θ_n−θ₀‖ 有界 在 base-mode 是**代码强加的同义反复** (每代 from_pretrained(gen0_dir) 定义层 true), 零 emergent 信息; 且 c·μ-on-prev-weight 在 persistent excitation (c>α*) 下收敛到 θ₀ 附近吸引子 → **也有界** = 非权重通道指纹。
- 保留作用: 确认重置生效 + 链非冻结 (配合冻结 gate)。**不作机制判别。**

**M2 = per-gen KL(μ‖model_n) (分布层通量, 必要非充分; 复用 armA measure() decode-free)**:
- 预测 {00,0A}(reset) 显著低于 {B0,BA}(无reset); BA 最高。但 **M2 单独不区分 c·μ** (Borkar 恢复 regime 也压低 KL) → 必须配 M3。
- **强制前置控制 (子 agent 攻击点4)**: ①冻结 gate **全覆盖**通过 (每 ckpt sha256 互异+skip/NaN/GradScaler=0) 才作数, 否则 [?]; ②**BA"发散"须用 skip-count=0 证明不是 GradScaler 冻结** (发散与冻结在 KL 曲线同形 = D612 同构风险); ③4 cell 用**同一固定 eval context** (非各 cell 自己 prompt 分布); ④≥2 seed 同向才作 directional, 满 5 seed 前不下 confirmatory。

## 4 锁定判据 (双向可证伪; 待 PI 决 M3 后定稿+commit-lock)
- **PASS (wedge 成立)** ⟺ M3 显 base-reset 锚 ∝1/η_eff (步数依赖, ≥2 seed 同向) **AND** M2 {00,0A}<{B0,BA}(全过 gate) **AND** Borkar PDF 人工核无权重通道脚注。
- **FAIL (塌回 Borkar / 死)** ⟺ base-reset 锚**独立于步数** (与 c·μ 同形) **OR** M2 无可分离差 (Schaeffer/vanilla 不可分) **OR** {00,0A} ‖θ−θ₀‖ 也累积 **OR** 任一进入分析的 ckpt 未过冻结 gate。
- **只下调不上调**: 任一通道 [?] → 整体 [?]; 不得用"M1 有界"补"M3 缺失"。
- 铁律: "驼峰仍在"≡中心命题 FALSE, 禁 spin。

## 5 子 agent verdict 摘要 (§H-a, a157...; verbatim 进 paper 须主会话复证)
- 攻击点1 (c=0 杀手): [?]偏 SURVIVES, 但 v1 论证不足 → v2 §2 收紧到 1/η_eff⊥c。
- 攻击点2 (M1 判别力): **REFUTED** → M1 降 sanity-check。
- 攻击点3 (Borkar 逐字): **SURVIVES** (Borkar 测度空间/de novo/无 θ₀ 重置; 不隐含 base-reset)。caveat: PDF 经小模型转述, paper 前人工核。
- 攻击点4 (测量混杂): SURVIVES 但 conditional on 冻结 gate 全覆盖 + fp16 round-off 标定 + GradScaler-skip 排除。
- **整体: [?]中间区, 偏成立** (数学 distinction 实质成立, 不塌回 Borkar) **但当前 spec 判别器配置撑不住** (M1 tautology + M3 缺实验) → 见 §7 PI 关卡。

## 6 强制 disclose (§F)
Borkar 2506.09401 · Bertrand 2310.00429 · Schaeffer 2503.03150 (正交 axis, 打赢区分) · SIGMA 2601.03385 v3 (同装置 S1/S2=Eq4.1/4.2) · 2505.08803 + 2509.04796 (conditioning-grounding 已占) · TTA/CoTTA/FIRE (weight-reset 作 stability 已有)。

## 7 PI 关卡 (子 agent 暴露的真实成本, 不软化)
**当前 Stage-A 2×2 (M1 已死) 无法单独实证 distinction。** 唯一不可换皮签名 = M3 (步数依赖), **需新 step-sweep 实验** (GPU, 廉价但非零)。
- **关卡**: wedge 值不值这个 M3 实验? 不做 M3 → 实证主张 reviewer 可打穿 (M1 同义反复 + M2 单独不分 c·μ); 做 M3 → 才有正面刀。
- P(wedge 作 novel 量化贡献存活) 现进一步 conditional on M3 成功显步数依赖 (prereg §6 旧估 15-30%, M3 是新 gate)。
- 与 J①(fp32-5060)/J②(seed42/Stage-B GPU-天) 并列待 PI 决。
