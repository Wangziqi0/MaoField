# exp020 · 崩溃指标 construct-validity / 证据有效维度 应力测试 · 预注册 DRAFT v0

> **状态: DRAFT v0 · 未锁定 · 未启动 · 待 PI+Win 批准 + 核 novelty 被占。**
> 起草: Linux 姐姐 (D617 晚)。设计骨架, 阈值标 `[TBD 待 PI lock]`。
> **这是方法论/实证实验 (指标构念效度), 不是哲学宣言。** 哲学判读 (本质/现象、反映论) 留 Win+PI, Linux 不判读。

## 0 动机 (一句话)
exp019 暴露: 崩溃指标 distinct-2 换 decode (rep_penalty) **方向翻号**, 恢复相几何 ≈ PPL 投影 (非独立)。
→ 浮现一个**可证伪**问题: 模型崩溃这门科学声称的"多个独立信号", **有效维度到底 >1, 还是塌成 1 个真轴 (分布层崩溃) + 一堆 decode 伪影/PPL 冗余**?
本实验**不预设答案**, 双向可证伪。结果 bears on STATE §4.8 哲学线 standing question (留 Win+PI 判读)。

## 1 研究问题 + 双向可证伪假说
- **H_essence (待证伪)**: 去掉 decode 翻号的指标后, 剩余"稳定崩溃证据"的**有效秩 eff_rank → 1**, 且每个稳定指标都高度相关于**分布层熵收缩轴** (decode-free)。⇒ 领域"多信号"实为单轴 + 现象层装饰。
- **falsify (反面赢)**: 存在 ≥1 指标**既 decode-稳定、又与分布熵轴低相关** (独立第二轴) ⇒ H_essence 证伪, 真有独立崩溃信号 ⇒ **潜在新发现**。
- **两分支都有产出**: 支持 H_essence = 唯物地钉死"现象遮蔽本质"结构 (可复现实证); 证伪 = 新大陆候选。

## 2 数据 (零新训练, 复用既有)
- α=0 旧链 5 seed{1,2,3,4,42} × g0–g9 全 ckpt (全在 36 `experiments/exp018_cat/data/checkpoints_armb/alpha0.0/`)。
- 固定 prompt 集 (train 前 N, N=`[TBD 128/256]`), 跨所有 decode/config 同一组 (配对合法)。

## 3 指标动物园 M (崩溃证据候选)
| # | 指标 | 类型 | 备注 |
|---|---|---|---|
| M1 | test-PPL (真 wikitext test) | loss 轴 | 驼峰参照 |
| M2 | distinct-2/3/4 (corpus, 生成文本) | 表面词汇 | 已知 decode 翻号 |
| M3 | rep-n = 1−distinct-n | 重复 | |
| M4 | self-BLEU (样本间) | 表面多样性 | |
| M5 | unigram-JSD(gen‖train) | 分布漂移(unigram) | |
| M6 | 表示几何 PR_cen / isotropy / eff_rank (末层 hidden) | 几何 | 已知 ≈PPL 投影 |
| **M7** | **输出分布熵 H(p_θ(·|ctx)) + 有效支撑/top-p 质量** | **分布层 DIRECT, decode-free** | **construct-valid 锚, 不被 decode 绑架** |

## 4 装置轴 A (应力扫描)
- **decode**: beam(5) / sampling(T=1.0) / nucleus(top-p=0.9)
- **rep_penalty**: {1.0, 3.0}
- **precision**: fp32 (CPU/36)。**限制**: gfx1201 fp16 非确定性不在本扫描 (留 22 Phase-2, 已知 LN race binding)。
- **seed**: 5 (既有)

## 5 分析
1. **方向稳定性**: 每个表面指标 M2-M6, 跨所有 (decode×rep_penalty×seed) 算 sign(m(g9)−m(g0)); 一致 = 稳定, 翻号 = 装置伪影 (distinct-2 预期翻)。
2. **有效秩 eff_rank**: 把**稳定**指标的 per-gen z-score 轨迹堆成矩阵 (指标×代, 跨 seed), SVD → eff_rank = 奇异值 participation ratio (Σσ)²/Σσ²。
3. **分布锚相关**: 每个稳定指标轨迹 vs M7 分布熵轴的 |corr|。
4. (诊断) 翻号指标单列, 量化其方向对哪个装置轴最敏感。

## 6 预注册判据 `[TBD 待 PI lock]`
- **H_essence 支持**: eff_rank(稳定指标) ≤ `[1.5?]` **且** 每个稳定指标 |corr(M7)| ≥ `[0.85?]`。
- **H_essence 证伪**: ∃ 指标 decode-稳定 **且** |corr(M7)| < `[0.5?]` ⇒ 独立第二轴存在。
- 锁定时序: 阈值 + N + decode 集 + eff_rank 估计器 → T0 commit 先于第一次跑 (守 exp019 教训: commit-lock 先于开奖)。

## 7 红线 + novelty `[?]`
- **红线 (硬)**: 本实验**不复活** paradigm-shift / first dialectical materialism instantiation / reflexive-AI (12 NOT-claim)。结果是"指标构念效度的实证", **不是**任何范式/哲学宣言。
- **novelty `[?]` (待核被占)**: metric-robustness / construct-validity 批判 NLP 评测已大量在先 (BLEU/PPL≠quality)。**可能没被占满的缝**: 具体钉在"模型崩溃证据的 eff_rank"上 + 自家可复现实证。**核被占前不声明 novel** (开实验前先派文献子 agent 核 model-collapse metric-robustness 现状)。
- **哲学判读**: 结果对 STATE §4.8「本质/现象」standing question 的支撑/证伪, 由 **Win+PI** 判读; Linux 只交付 eff_rank 数字 + 可证伪结论。

## 8 成本 + 下一步
- 成本: 零训练, CPU forward+generate; 粗估 50 ckpt × {3 decode × 2 rep_penalty} ⇒ 数百 ckpt-gen, 数 h CPU (可承受, 远低于 exp019 链)。
- **下一步 (明天 PI+Win+Linux 一起)**: ① 核 novelty 被占 (文献子 agent) ② PI+Win 判"本质/现象"框架是否值得这个实验 (ROI) ③ 锁 §6 阈值 + N + decode 集 ④ 批准后才 T0 commit-lock → 跑。

---
*骨架 v0, 未锁未跑。守: 预注册先于开奖 (exp019 教训) · 分布层直接测不被 decode 绑架 · 双向可证伪 · 红线写死。*
