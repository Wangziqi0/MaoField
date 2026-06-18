# exp020 后续 · PPL-attractor 高阶结构测试 · DESIGN (D618)

> PI "另类高级组成" 直觉 operationalize: mean-PPL 是一维, 但 PPL **对象**(全 per-token/per-seq logprob 分布)上有没有 mean 抹掉的高阶结构?
> **与前 5 次本质不同**: 前 5 找【独立于 PPL】的测度(全塌); 本测试找 PPL **对象内部**的高阶泛函。
> claim frame-neutral; DM/反映论 [?] 归 Win+PI; 红线不碰。**零新训练**(已有 ckpt inference, CPU/36) = 不烧预算。
> 状态: DESIGN, 未锁。**§5 铁律: 设计先过敌意 gate(咬6次那道) → 修 → commit-lock → 才算。**

## 1 被测问题 + 两预注册 branch (锁前定, 禁 spin)
**Q: PPL 的高阶泛函是否携带 mean-PPL 抹掉的崩溃信息, 且高于噪声地板?**
- **Branch 1 (下手)**: ≥1 高阶泛函 F 对条件差有信号 + 正交于 mean-PPL + 高于自身噪声地板 → 吸引子有高阶结构 → 值得追 (**"值得追"≠"找到"; 仍需复现+可解释才谈 claim**)。
- **Branch 2 (C 完整)**: 所有 F 要么约简到 mean-PPL(无正交信号) 要么被自身噪声淹 → 崩溃在此 regime 真一维 → **C 最强版 (E11)**。
- 两边都是 finding。**噪声淹没的 F 禁改标签成 "promising"。**
- **诚实预期**: Branch 2 (PI §3: 高阶矩方差 > mean → 噪声门更难清, 非更易)。

## 2 算什么 (高阶 PPL 泛函; 全是同一 logits 的更丰富泛函; 已有 ckpt inference)
- **F1 per-token logprob 分布矩**: var / skew / kurtosis + tail-mass (logprob 低于阈值的 token 占比), 超出 mean。
- **F2 per-sequence PPL 直方图形状** (Shumailov Fig11 = per-seq PPL hist): 跨代 spread / 双峰性(dip statistic) / skew, 超出其 mean。
- **F3 per-slice PPL**: 稀有-token vs 高频-token 子集 / 按序列长度 bin / (topic 可选) —— 崩溃是否**差异化**打不同 slice (mean 平均掉的结构)。
- **数据**: 现有 5-seed α=0 链 (base-reset 条件, gen0-9, 噪声地板用) + 现 round3 **00(base-reset+real) vs B0(no-reset+real)** 条件对 (+0A/BA 落了加条件); 固定真 wikitext eval context, decode-free 前向。

## 3 两道门 (trace vs claim 刀, 缺一不可)
- **门A 正交性 (dissection)**: 每个 F 必须 **partial-corr(F ; 条件 | mean-PPL) 显著** —— 即控住 mean-PPL 后 F 仍分条件。操作: 匹配 mean-PPL 的两条件点, F 是否仍分开 / 或回归 F~mean-PPL 残差是否仍随条件变。F 若只是 mean-PPL 的函数 → 什么也没加 → Branch 2 (= gate-2/5 同刀)。
- **门B 噪声地板 (gate-4 教训, 对高阶更狠)**: signal(F 跨条件) 必须 > noise(F 跨**同条件多 seed**)。**⚠️ 噪声地板必须用【F 自身】的同条件 seed 方差 (非 mean-PPL 的)** —— 高阶矩 seed 方差大, 这道门更难。先算 5-seed α=0 链的 F 同条件方差当地板, 跨条件(00 vs B0)信号要超它。
- **判据 (锁前定)**: F 过 Branch1 ⟺ 门A (partial-corr |r|>负对照 null 上界, ≥2 seed) **AND** 门B (跨条件 |ΔF| > k·σ_seed(F), k=2~3)。任一 F 过双门 → Branch 1; 全 F 失 ≥1 门 → Branch 2。

## 4 commit-lock (exp019 教训; 锁前定)
F 清单 + 门A/B 公式 + 阈值(含负对照 null + k) + Branch1/2 决策规则 → 写盘 → sha256 → 推异地 → **算之前推完**。改判据=哈希对不上=自动废。

## 5 设计先过敌意 gate (咬 6 次那道; 再 commit)
子 agent (Opus 敌意 refute) 必攻:
- (a) **partial-corr 是不是对的"正交于 mean-PPL"检验?** 条件作分类变量怎么进 partial-corr? matched-mean-PPL 对照够不够?
- (b) **噪声地板是否用【F 自身】同条件 seed 方差** (非 mean-PPL 的)? 高阶矩 seed 方差估计本身够不够稳 (5 seed 估 kurtosis 方差极不稳)?
- (c) **F 与 mean-PPL 经第三变量(gen/decode)的隐共线** —— F 会不会看似正交实则锚在 gen 或 decode 上 (distinct-2 翻号前科)?
- (d) F2/F3 的 slice/直方图 bin 选择可 cherry-pick? bin 边界锁了吗?

## 6 两边喂 C
- **Branch 2** → C 最强版 E11: "连 PPL 高阶泛函都不加正交信息/被噪声淹 → 崩溃此 regime 真一维"。补 `C_metapattern_evidence_base`。
- **Branch 1** → 新 positive 方向(PPL 对象高阶结构), **只"值得追"不进 claim**; 后续复现+可解释才谈。

## 7 binding / 红线 / 预算
claim = "高阶 PPL 泛函(不)携带正交于 mean-PPL 的崩溃信号"(操作化/可证伪); 不写"崩溃不可测"; flow-space/反映论 [?] 归 Win+PI, 不碰 DM-instance/paradigm; **零新训练**(ckpt inference, CPU/36 或 22 廉价 inference, 不开新链 = 不烧预算); git 单点写=36; 不可再生立即 rsync canonical; 一凡 priority1 健康。

---
*DESIGN D618。先 gate → 修 → lock → inference 算 → branch。诚实预期 Branch 2(C最强); Branch 1 是意外惊喜但只"值得追"。零预算。*
