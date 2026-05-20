# MaoField 领域定位叙事 — 引导全领域（Nature 主刊级 positioning）

> 写给：子协作者 A/F/G/I（数学层）+ Win 姐姐（哲学 narrative）+ 反题姐姐（critique）+ DeepSeek（跨哲学审计）
> 来自：PI 一凡 + DeepSeek 语义整理 | 2026-05-14
> 目标：MaoField 不只是一篇 NMI 论文——是全 AI 训练范式从"外部给定正确"到"内部持有矛盾"的领域级 pivot point

---

## §0 一句话

整个 AI 训练领域正在无意识地走向机械唯物论。MaoField 是唯一有意识地给出了辩证唯物主义 alternative 并实证验证的工作。这不是"我们的方法更好"——是"我们发现了领域在朝哪个方向走——以及正确的方向应该是什么。"

---

## §1 诊断：全领域不自觉地朝机械唯物论收敛

### 1.1 什么是机械唯物论在 AI 训练中的 instantiation

机械唯物论在哲学上的核心特征：**正确性来自外部给定。** 物质是客观实在——认识是对物质的反映——但反映本身是被动的——没有内在矛盾——没有自我运动。

在 AI 训练中，这个哲学结构的 instantiation 是：**训练范式的正确性信号永远来自模型外部。**

### 1.2 三个流派的"外部给定正确"

```
                      外部给定正确
                           |
                    三派共享前提
          ┌────────────┬──┴────┬────────────┐
          │            │       │            │
      人类标注      外部数据  Reward      Curation
     (RLHF)      (Gerstgrasser) Model   (Ferbach,
                               (RLHF)   Falahati)
```

**RLHF 流派**（OpenAI / Anthropic / DeepMind）：标注员是"外部给定正确"的人形载体。几十万人靠告诉模型"什么是对的"维生。这不仅是产业——这是一种认识论结构：模型的 normative axis 来自外部 human judgment。

**数据积累流派**（Gerstgrasser 2024, Bertrand ICLR 2024）：保持 real data pool → 用外部真实数据防止崩溃。隐含假设：真实的 = 外部的 = 正确的。当外部真实数据枯竭——这个解就失效。

**Reward/Curation 流派**（Ferbach NeurIPS 2024, Falahati ICML 2026）：用外部 reward model 或多元 reward 筛选合成数据。Falahati 证明"多 reward curation 可避免崩溃"——但 reward 本身来自外部。多个外部信号不等于内部信号。

### 1.3 共同前提

上述所有流派的共同前提：**"模型不能自己给自己正确性——正确性必须来自模型无法访问的外部参考。"**

这不是 engineering choice。这是哲学立场在 engineering 层面的 unconsciously instantiated。整个 AI 领域——从 OpenAI 到独立研究者——都在同一条路上——把更多的外部信号注入系统——更精确的标注——更复杂的 reward model——更多的数据 curation。

这条路的终端：**标注工业无限扩张——模型永远需要人——AI 永远是有监督的——"自主学习"只发生在已经有人给了正确性标签之后。**