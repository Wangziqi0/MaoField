# exp020 · 自迭代崩溃 双臂预注册 DRAFT v1 (臂A 不可逆性 + 臂B 证据有效维度)

> **状态: DRAFT v1 · 未锁定 · 未启动 · 待 PI+Win 批准 + novelty 被占核查。** supersede v0 (v0 = 仅臂B)。
> 起草: Linux 姐姐 (D618)。PI 决「两臂合一」。阈值标 `[TBD 待 PI lock]`。
> **这是方法论/实证实验, 不是哲学宣言。** 「本质/现象 ↔ 反映论」判读归 Win+PI (见 STATE §4.8), Linux 不判。

## 0 动机 + 双臂逻辑
exp019 全线 negative + 测量发现 (distinct-n 换 decode 翻号 / 几何≈PPL投影) → STATE §4.8 浮现一个 `[?]` 结构: 一连串失败指向**一个不可逆算子 (本质)**, 而领域用**多信号崩溃现象学 (现象)** 把它遮住。
- **臂A 测"本质"**: 那个算子真是**单向不可逆**的吗 (essence 一不一)。
- **臂B 测"现象"**: 多信号崩溃证据真塌成**单轴**吗 (phenomenon 几维)。
- **两臂都双向可证伪, 两分支都有产出** (支持 = 钉死结构; 证伪 = 新发现)。哲学对应见 §C, 留 Win+PI。

---

# 臂 A · 不可逆性 / 算子非可逆性

## A.1 命题 (精确形式)
自迭代「生成→再训练」映射 T 是**信息单向湮灭**的: 一旦尾部/多样性丢失 (塌到退化不动点附近), **丢掉的信息无法从塌缩模型自身内部恢复——只能靠外部真实数据重新注入 (= 替换, 非逆转)。**
→ "不可逆" 严格定义 = **塌缩模型在"无外部真实数据"的廉价干预下, 分布层多样性 (熵/有效支撑/尾部) 不可恢复**; 信息须从箱外来。

## A.2 数据 (复用既有, 零或极少新训练)
- 已塌缩 ckpt: α=0 seed{1,2,3,4,42} 的 **g9** (主), g5/g7 (剂量, 可选)。全在 36。
- baseline 锚: 同 seed g0 (未塌) 的分布层测度。

## A.3 干预集 I
**内部干预 (核心——不引入外部真实数据)**:
- I1 **自模型 souping**: g9 与 g9 不同 seed 加权平均 / g9 与早代 g2 权重平均 (model soup)。
- I2 **权重/采样扰动**: g9 权重加噪 / 解码端加熵正则 (温度/entropy bonus) 若干步。
- I3 **继续自训练 (control-)**: g9→g10..g13 纯自迭代, 预期**不恢复** (确认停在不动点)。
**外部干预 (control+, 确认信息须外部再注入)**:
- I4 **真实数据再注入**: g9 在 **真 wikitext** 上继续 fine-tune K 步 (K 设小, K ≪ 原训练量)。
  - 关键不是"训够久能不能恢复"(那是替换/平凡), 而是 **恢复曲线是否有 hysteresis**: 塌缩路径 vs 恢复路径不对称、恢复远难于塌缩 = 非可逆的实证签名。

## A.4 测度 (分布层 DIRECT, 不被 decode 绑架)
- M_ent: 输出分布逐 token 熵 H(p_θ(·|ctx)) 在固定 context 集均值。
- M_supp: 有效支撑 / top-p 质量集中度。
- M_tail: 尾部质量 (低频 token 覆盖) vs g0。
- (cross-ref) PPL + distinct (固定**忠实** decode rep=3.0), 仅作旁证, 不作主判。

## A.5 判据 `[TBD 待 PI lock]`
- **H_irreversible 支持**: 所有**内部干预 (I1/I2)** 后, M_ent/M_supp 恢复 < g0−g9 gap 的 `[20%?]`; 且 I3 自训练不恢复。⇒ 信息不可从内部复原 = 算子非可逆 (essence 单向坐实)。
- **falsify (可逆, 新发现)**: ∃ 某内部廉价干预使 M_ent/M_supp 恢复 ≥ `[50%?]` g0 水平 ⇒ 崩溃**可从内部逆转** ⇒ 不可逆命题证伪, **且这是比"不可逆"更可发表的 positive**。
- I4 外部再注入: 若仅 I4 (外部) 能恢复且呈 hysteresis ⇒ 佐证"信息须箱外来"= 非可逆。

---

# 臂 B · 崩溃指标 construct-validity / 证据有效维度 (承 v0)

## B.1 命题 + 双向假说
领域"多个独立崩溃信号"实为**单轴 (分布层崩溃) + decode 伪影/PPL 冗余**, eff_rank→1。
- **H_essence 支持**: 去 decode-翻号指标后, 稳定指标 eff_rank ≤ `[1.5?]` 且每个 |corr(分布熵轴 M_ent)| ≥ `[0.85?]`。
- **falsify**: ∃ decode-稳定 **且** |corr(M_ent)| < `[0.5?]` 的指标 ⇒ 独立第二轴 ⇒ 新发现。

## B.2 设计 (同 v0, 略)
指标动物园 M1-M7 (含分布层 M7=M_ent) × 装置轴 A (decode beam/sampling/nucleus × rep_penalty{1,3} × precision fp32 × seed5); 方向稳定性 → 稳定指标堆矩阵 SVD → eff_rank participation ratio + 对 M_ent 相关。**复用 α=0 链, 零新训练。** (gfx1201 fp16 不在扫描, 留 22 Phase-2, LN race binding。)

---

# §C 红线 + novelty + 哲学对应
- **红线 (硬)**: 不复活 paradigm-shift / first dialectical materialism instantiation / reflexive-AI (12 NOT-claim)。结果是"崩溃动力学不可逆性 + 指标构念效度"的实证, **不是范式/哲学宣言**。
- **novelty `[?]` (核查中)**: 文献子 agent 正核臂A(可逆性/不可逆性 vs Gerstgrasser 累积避免崩溃 / Bertrand 不动点)+臂B(metric robustness)是否被占。**核完才定 ROI; 被占则降级或不跑。**
- **哲学对应 (留 Win+PI, Linux 不判, `[?]`)**:
  | 哲学命题 (本质/现象) | 实验判据 |
  |---|---|
  | 本质 = 不可逆算子 (单向) | 臂A H_irreversible 支持 |
  | 本质非单向 (可逆) | 臂A falsify = 新发现 |
  | 现象遮蔽本质 (多信号实为单轴) | 臂B eff_rank→1 |
  | 现象有独立第二维 | 臂B falsify = 新发现 |

# §D 成本 + 下一步
- 成本: 臂B 零训练 (CPU 测量, 数 h); 臂A I1/I2 零或极少训练, I3/I4 少量 fine-tune (K 小, 36 CPU 或 22 GPU 经 manual-LN patch)。总可承受。
- **下一步 (今天 D618 PI+Win+Linux)**: ① 文献子 agent 核 novelty 被占 (跑中) ② Win-role 子 agent 哲学 framing 初判 (跑中) ③ PI+Win 判 ROI/框架 ④ 锁 §A.5/§B.1 阈值 + K + N + 干预集 ⑤ 批准才 T0 commit-lock → 跑。

---
*骨架 v1, 未锁未跑。守: 预注册先于开奖 (exp019 教训) · 分布层直接测不被 decode 绑架 · 双臂双向可证伪 · 红线写死 · 哲学判读归 Win+PI。*
