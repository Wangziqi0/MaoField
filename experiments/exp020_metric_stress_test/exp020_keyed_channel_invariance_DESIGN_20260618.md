# exp020 密钥证伪实验 · keyed channel-invariance · DESIGN (D618)

> PI dispatch (社会实践=检验真理唯一标准 operationalize): path A + 三重密钥封。坐 C 脊梁 (A 失败→Borkar-distinction→喂 C)。
> **claim 红线**: claim 停在 channel-invariance 结果 = frame-neutral 信息论陈述; 反映论/DM 归因 [?] 归 Win+PI; 绝不写 实证反映论/DM/first-reflexive/paradigm。
> 状态: **DESIGN, 未 seal**。**PI §4 铁律: 本设计先过敌意 gate (咬了3次那道) → 修 → 才 seal KEY-1。gate 管【有力】, KEY 管【诚实】, 两者都要。** supersede prereg_channel_invariance_DRAFT (GATE FAILED 版)。

## 1 被实践检验的预测 (反映论【生成】, claim frame-neutral)
**H: 崩溃稳定 = f(真实信息总通量 Φ_total), 与注入【通道】无关。**
- 支持 (invariant): 三通道 same-Φ → 同稳定轨迹 (落一条线)。
- 证伪 (channel matters): same-Φ 不同稳定 (分层) → Borkar mechanism-specific (优化几何 ⊥ 数据测度)。
- **两边都是 finding, 禁 spin。**

## 2 解洞①: Φ 外生 (构造上 ⊥PPL)
Φ = **每代经通道注入的真实信息率, 纯 knob 定义, 不含任何"模型/合成数据离 μ₀ 距离"项**:
- **Φ_data(c) = c · I_real** — c=数据混入 fraction (knob), I_real=固定真 wikitext block 信息量 (常数, 跑前测一次)。∝ c。
- **Φ_weight(η,T) = κ · 1/(η·T) · I(θ₀)** — η=lr, T=steps (knob), I(θ₀)=θ₀ 编码的 μ₀-info (常数)。∝ 1/(η·T)。
- **Φ_prompt ∈ {0, 1} · I_prompt** — 二值 (synthetic=0 / real=1), I_prompt=真 prompt block 信息量 (常数)。
- **累积**: Φ_g = Σ_{i≤g} per-gen 注入率 (data/prompt 每代恒定率 → 线性累积; weight 每代 reset 注入率 ∝1/(η·T))。
- **⊥PPL 构造保证**: Φ 是 knob 的函数, 与模型当前态无关 → 不可能是 PPL 的伪装。KEY-1 写死验证: `|corr(Φ_g, test_ppl_g | knob)| ≈ 0` (平凡满足=外生性自证) + `|partial-corr(S_g, Φ_g | test_ppl_g)| > 阈` (S 对 Φ 的依赖超出 PPL = 非循环)。

## 3 解洞②: 通约性 = 可测假设 (非 premise; early-calibrate/late-predict)
**不假设三通道可通约。** 通约性本身作可证伪假设, 用 PI 的多点匹配:
- **校准 (早代 g1-g3)**: 对每 channel-pair (如 data↔weight), 拟合**单个**兑换率 λ (把 Φ_weight 单位换算到 Φ_data 单位), 使两通道在 g1-g3 的稳定轨迹 S(g) 重合。**λ = 一个数, 非自由函数** → DOF=1/pair。
- **预测 (晚代 g5-g9)**: 用该早代拟合的 λ, **预测** matched-Φ_common 下两通道 g5-g9 的 S(g) 仍重合。**不许晚代再拟合。**
- **判读 (解"分层=不可通约 vs 非线性动力学"歧义)**:
  - g1-g9 全程一条线 (一个 λ 撑全程) → **channel-invariant** → H 支持。
  - g1-g3 match 但 g5-g9 分层 → **channel matters** (通道带 hidden state 超出稳定变量) → Borkar mechanism-specific (= 不可通约的实证签名, 喂 C)。
  - g1-g3 都 match 不上 (任何 λ) → 通约性 premise REFUTED (早于 H 判定; 避免把"轴无效"误读成 channel matters)。
- **DOF 防作弊**: 一个 λ/pair 撑不起任意重合 (若 S-vs-Φ 高度非线性, 单 λ 早代 match 不蕴含晚代 match) → falsifiable。

## 4 解洞③: outcome S = decode-free 全轨迹 (非单端点, 非 PPL)
- **S(g) = eff_supp(g) = exp(H̄(g))**, H̄ = measure() 在**固定真 wikitext eval context** (4 cell 全同) 上的 logit 熵 (前向, **decode-free, 非生成, 非 PPL 轨迹**)。
- **用全轨迹 g0-g9 匹配, 非单端点**: 非单调谷 (g0=3.39→g2≈1.92→g9≈2.79, 5/5 seed) 被全轨迹匹配自然吸收; 权重臂"θ₀ 机械抬熵"若存在 → 早代轨迹形状就不同 → 匹配自动计入。
- **decode 污染已查**: testB 实测 `rep3_injects_flux=False` (rep3≈rep1) 已否决 rep_penalty 伪通量; 但 S 是 measure() 前向熵, 本就 decode-free, 双保险。
- **阈值 ε (跑前用现有 5-seed σ 标定, 锁进 KEY-1)**: ε_match = k·σ_seed(S), k=2~3; "重合"= |ΔS(g)| < ε_match 全 g; "分层"= |ΔS(g)| > ε_strat 且单调可分, ≥2 seed。

## 5 实验臂 (= channel-invariance; CPU 测量, GPU 训练)
| 臂 | knob 扫 | 成本 |
|---|---|---|
| 数据-mixing (c) | original_fraction ∈ {0, .05, .1, .2} | 廉价 |
| 权重-reset (1/η_eff) = M3 | epochs/lr 2-3 档 (base-reset, c=0) | M3 主成本 |
| 生成 (prompt) | real / synthetic 二值 | 廉价 |
- 单变量/臂; 每链 fp16 冻结 gate (sha256 互异/skip/NaN/GradScaler=0, 全覆盖); 22 必经 manual-LN patch; 单 GPU 串行。
- **混杂控制 (洞④, 预注册锁)**: 固定 total-token / batch / accumulation / warmup / prompt_length / decode(beam=5,rep 单值) / eval-context; c 臂报 support+有效数据量; η 臂报每档 skip pattern; 现 2×2 = c=0+fixed-η 锚, 复用。
- Φ + S 全 CPU@36 offline 算, 不占 GPU。

## 6 三重密钥协议 (PI §2; 让实践不可篡改)
- **KEY-1 封预测 (commit-before-practice)**: 本设计过 gate 修订后, 完整决策规则 [§2 Φ 定义 + §3 λ-匹配协议 + §4 S 定义 + ε 数值 + outcome→判读映射] → 冻结写盘 → `sha256` → git commit (hash+file) → push 异地 + 时间戳。**任何 keyed cell 结果在此 push 完成前一律不读。**
- **KEY-2 盲分析 (blind the analyst)**: cell 身份用 seed 生成随机置换**匿名化** (cell→匿名 ID 映射单独存, 不进分析脚本)。分析脚本在**匿名 cell** 上算 verdict (哪些匿名 cell 一条线/分层) → **verdict 算完落盘后, 才 unseal 置换揭真通道**。堵 exp019"偷看 gen2 retrofit"口。
- **KEY-3 异地时间戳 = 防篡改**: prereg-hash + key-hash 先推异地, 证预测早于实践 (事后改→哈希对不上)。
- **KEY 实现**: 置换 = `seed→permutation` 确定性生成 (可复现); 匿名映射文件 sha256 单独 commit, unseal = 公布该文件。分析脚本只吃匿名 ckpt 目录 (软链 anon_<id> → 真 cell, 映射封存)。

## 7 实践即裁定 (PI §5; 已上锁)
KEY 封完 → 跑 → blinded verdict → unseal → **结果就是裁定**。主会话只能据结果**下调不上调**; post-hoc 改判据/Φ/阈值 = 哈希对不上 = 自动废。
- H 支持 → 反映论那条【预测】被实践确认 (但"是否反映论"=[?] Win+PI; 别 frame 也可能预测 invariance; **实践证预测不证形而上学**)。
- H 证伪 → 预测错记 FALSE 不 spin → Borkar mechanism-specific = finding, 喂 C。

## 8 binding/红线/disclose
claim 操作化/可证伪; 反映论/DM = 启发, discussion [?] 归 Win+PI, 不写 first-*/paradigm/DM-instance (红线); Opus 子 agent 敌意 default-refute, verbatim 进 paper 主会话亲核; disclose Borkar 2506.09401 / SIGMA v3 / Bertrand 2310.00429 / Schaeffer 2503.03150 / 2505.08803+2509.04796; git 单点写=36; 不可再生立即 rsync canonical; 一凡 priority1 健康。

---
*DESIGN D618。先 gate(有力) → 修 → seal KEY-1/2/3(诚实) → 盲跑 → unseal → 裁定。两个洞洞①(外生Φ)②(λ-可测假设)③(全轨迹S)已设计解, 待 gate 验。*
