# exp020 臂A · 自迭代崩溃 = 多通道均衡 (D618 findings)

> 2026-06-18 (date 二值)。Linux 姐姐主会话 + PI 实时哲学线。预注册 prereg_exp020_draft_v1 §A。
> **3 跑 (round1/round2/testB) + runner code 核实。** 分布层直接测 (decode-free)。
> 红线: 不复活 paradigm-shift / first-DM-instantiation / reflexive-AI。哲学判读归 Win+PI。

## 0 一句话
α=0「no_preserve」自迭代**不是纯内循环**: runner code 实锤每代**(a) 用真实 wikitext prompt 生成 + (b) 权重重置回 gen0 真实 base**, 训练数据虽 100% 合成。所以**「崩溃」是内通道(合成退化) vs 两条常驻外通道(真 prompt + gen0 重置)的均衡**, 非纯自吞单向湮灭。分布层熵呈**驼峰**(谷@g2, 自愈~60%, 残余~16% 永久), 谷与残余**内部不可逆**但**外部锚拉得回大部分**。PI 早提的"内/外是通道、通量是本质、内/外标签是表面" **被 code 字面证实**。

## 1 分布层熵轨迹 (round2, 5 seed, decode-free 逐 token 条件熵)
```
gen:  0    1    2(谷) 3    4    5    6    7    8    9
H̄:  3.40 2.00 1.93  2.13 2.48 2.68 2.83 2.90 2.85 2.86   (5/5 seed 谷@g2)
```
- **驼峰非单调**: 谷@g2 (H=1.93, eff_supp~7), 自愈 g2→g7 (~60% of g0−谷 gap), g9 plateau (~2.86, **g8→g9 |Δ|<0.03 = 已渐近**)。
- **残余 ~16% of g0 永久** (g9 回不到 g0=3.40, 且已 flatten 非继续闭合)。

## 2 不可逆性 (round1+round2 干预, decode-free)
| 干预 g9 残余 | 恢复 | | 干预 g2 深谷 | 恢复 |
|---|---|---|---|---|
| noise | +9~10% | | noise | +6.8% |
| soup(两塌缩) | ~0/−14% | | soup(两深谷) | −2% |
| soup(+健康 g0) | +36% | | soup(+健康 g0) | +40% |
→ **谷与残余都"内部不可逆"** (噪声/塌缩互 soup 不恢复); **只有注健康权重 (外部信息) 部分恢复**。seed42 复制 seed1 ✓。

## 3 testB: 自愈**不是** decode 伪影 (证伪主会话假说)
g2 生成语料多样性 rep=1.0 vs 3.0 (seed1/42): ΔunigramH +0.04~0.06, Δdistinct2 +0.01 (微) → **rep_penalty 几乎不注多样性**。
- 主会话原假说「自愈=rep_penalty 伪通量」**证伪** (差异日志 §6)。
- 但暴露关键: g2 模型条件熵仅 1.94 (峰尖), 其**生成语料 unigram_H=5.69 ≈ 健康 g0 的 5.71** —— 训练数据远比模型自身杂, **多样性来自 prompt 不是模型/decode**。

## 4 runner code 实锤: 多通道结构 (本 findings 核心, 全是 code 事实)
| 通道 | code | 性质 |
|---|---|---|
| 内: 合成数据链 | `build_mixed(original_fraction=0.0)` (config L128 no_preserve) | 训练数据 100% 合成, 逐代退化 |
| **外1: 真 prompt** | `run_arm_b_alpha_scan.py:288 real_train_blocks=train_blocks` | 每代生成都拿真 wikitext 前 64 token 作 prompt |
| **外2: gen0 base 重置** | `:307 base_model_path=gen0_dir` (注释 "每代 base 是 gen0, 不在前一代 continue") | 每代权重拉回真实起点, 不累积漂移 |
→ **连最纯 no_preserve 都有两条常驻真实锚。** 「崩溃」= 三通道均衡; 谷=退化瞬态占上风; 自愈=外锚拉回; 残余=外锚拉不回的部分。

## 5 净裁定 (诚实, 不拔高)
- **铁 (code/数据)**: setup 是多通道, 非纯内; 熵驼峰 5/5; 谷+残余内部不可逆; rep_penalty 非自愈源。
- **假说 (待 round3 消融证)**: 自愈由外通道(prompt/gen0)驱动 → **消融测**: 生成 prompt 改用合成数据 / 每代从前代 continue 不重置 gen0 → 看崩溃是否变单调更深。GPU, 留 PI budget/22 + manual-LN patch。
- **撞回风险**: 剥掉外锚若回单调崩溃 = 撞 Shumailov/DPI; **可能没被占 = "自吞 setup 暗含常驻外部通道、collapse 实为多通道均衡"这个对实验范式的解剖**。novelty `[?]` 待核 (novelty agent 未核此角度)。

## 6 差异日志 (D-1 纪律 5)
- **主会话 testB 预测错** (预测 rep=3.0≫rep=1.0 注伪通量; 实测 ≈, 证伪)。修正: 自愈非 decode 伪影, 真源是 prompt 外通道 (code 实锤)。**again: 先测后改口, 不凭预测翻烧饼。**
- round1 把 g9 当"塌缩态"测逆转, 被轨迹数据打洞 (真谷在 g2); round2 已修正从 g2 测。
- 哲学: "不可逆的东西"被材料改写为"多通道均衡的残余", 比单向算子更拧巴 (D-3 物质顶理性认识)。

---
*landed: round1 `armA_firstlook_20260618/` · round2 `armA_round2_20260618/` · testB `armA_testB_20260618/` · 脚本 `scripts/armA_*.py`。下一步 round3 消融外通道 (GPU) 留 PI。*
