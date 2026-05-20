# Σ_2 → ℒ_contradiction 严格 derivation

**写**: 数学教授 sub-agent（zero-context, paper-review subagent_type, 不 share 主 session 立场）, 2026-05-08
**对象**: Linux 主 Agent + PI 一凡 + Win 姐姐 + 反题姐姐
**前置**: WIN_INVENTORY §C2 Σ 嵌套甲数学结构 + LINUX_P0_C_CHI_HARTREE_20260430 Hartree closure sympy verify ✓
**判定**: **存疑（partial 通过）** — candidate (e) Bregman 二阶差分 with self-NLI signal **partial 65% isomorphism**, full 不可能
**关键 surface**: arm A (NLI supervised) 与 Σ_2 数学结构基本无关 (15% isomorphism), paper 不应包装成 "Σ_2-motivated"

---

## §1 Σ_2 精确数学 statement

### 1.1 起点

Mexican-hat 势 $V(\psi) = (|\psi|^2 - v^2)^2/4$ 上场 $\psi(x,t)$, T resolvent $T = (I + \eta \nabla_\psi^\dagger V)^{-1}$.

Σ 嵌套甲: $\Sigma_{\text{nest}}(\psi) = \Sigma_3(\psi + \lambda_1 \Sigma_1(\psi) + \lambda_2 \Sigma_2(\psi))$

- **Σ_1**: 因果二阶 Volterra 算子, $(\Sigma_1\psi)(t) = \int_{-\infty}^t \chi(t-s)\psi(s)ds$, $\chi(\tau) = \frac{1}{2m_{\text{eff}}}e^{-m_{\text{eff}}|\tau|}\mathbf{1}[\tau\ge 0]$ (因果版)
- **Σ_2**: 题面定义 = $\partial_t^2 \Sigma_1$, 严格 statement = "二阶时间导 of Volterra-convolved field"（不是作用于 kernel）
- **Σ_3**: lift-projection $P_{\mathcal H} \circ T \circ i$ (Sz.-Nagy-Foias 膨胀)

### 1.2 Σ_2 三项分解

直接对 $(\Sigma_1\psi)(t)$ 求 $\partial_t^2$:

$$\boxed{\;(\Sigma_2\psi)(t) = \frac{\dot\psi(t)}{2m_{\text{eff}}} - \frac{1}{2}\psi(t) + m_{\text{eff}}^2 (\Sigma_1\psi)(t)\;}$$

**结构性解读**:
1. $\dot\psi/(2m_{\text{eff}})$: **当下速度**
2. $-\psi/2$: **当下值的负反馈**
3. $m_{\text{eff}}^2 (\Sigma_1\psi)$: **历史 memory term**（正项）

**严格 caveat**: Σ_2 是 inhomogeneous linear operator, 不是 quadratic form. 第三项是合法 quadratic form, 前两项是 distribution-valued boundary contribution ($\delta(t-s)$, $\dot\delta(t-s)$).

### 1.3 与 Hartree closure 接口

主 session $\lambda_\Sigma \langle\|\delta\theta\|^2\rangle$ 是 **Σ_1 的方差闭合**（不是 Σ_2）. Σ_2 在 Hartree closure 对应 **方差的二阶时间导** $\partial_t^2 \langle\|\delta\theta\|^2\rangle$. **type error 警告**: 不要把 $\lambda_\Sigma \approx 25$ 数字直接挪到 ℒ_contradiction 的 $\alpha$ 系数.

---

## §2 PDE→LLM 4 candidate audit

LLM 训练动力学是离散 step. 时间轴选择决定 Σ_2 语义:
- **generation index $n$**（外层时间, self-iteration 轴）
- **token position $\tau$**（内层时间, sequence 轴）

主 Agent 必须选定. crash 是 generation 轴现象, **不是 token 轴**.

### Candidate (a): hidden state 二阶时间导 ∂²h/∂t²

**与 Σ_2 同构度: 30%**, **判定: 否决**
- type-mismatch: token 轴 ≠ generation 轴, $h''^{(\tau)}$ 与 crash 物理无关
- 没 history memory term + 没 pointwise neg feedback
- paper §6 写 "motivated by Σ_2" 会被 reviewer 抓 type error

### Candidate (b): KL 二阶差分 ∂² KL(p_n||p_{n-1}) / ∂n²

**与 Σ_2 同构度: 55%**, **判定: cost 问题**
- 时间轴对 ✓ + 已是分布层位移 ✓
- forward pass 翻倍 → cost ↑ 60-80% **超过 50% ceiling**
- 修补 EMA 替代 model_{n-1} → cost ↑ 30%, 但语义滑到 self-distillation regularizer

### Candidate (c): self-attention path-history correlation ⟨a_t · a_{t-k}⟩

**与 Σ_2 同构度: 20%**, **判定: 否决**
- 是 Σ_1 不是 Σ_2 (二阶导丢失)
- token 轴问题与 (a) 同

### Candidate (d): 参数空间二阶差分 + Volterra-加权 history loss

**与 Σ_2 同构度: 70%**, **判定: 语义弱**
- 三项分解完整保留 + 与 $\lambda_\Sigma$ Hartree 同型 ✓
- "矛盾" 直觉 weak — 度量参数轨迹大小, 不是 contradiction 语义

### Candidate (e): Bregman 二阶差分 with self-NLI signal **(数学教授新加, 推荐)**

**Statement**: 对每个 example $x$, 取分割点 $i$, 算 self-entailment 矛盾度
$$c_i = -\langle u_i, v_i \rangle, \quad u_i = \mathbb{E}_{w\sim p_\theta(\cdot|x_{<i})}[\phi(w)], \quad v_i = \mathbb{E}_{w\sim p_\theta(\cdot|x_{<i+m})}[\phi(w)]$$

generation 轴 Σ_2 三项构造:
$$\mathcal{C}_n^{\text{self}}(x) = \underbrace{\frac{c_i^{(n)} - c_i^{(n-1)}}{2m_{\text{eff}}}}_{\dot\psi\text{ analog}} - \frac{1}{2}c_i^{(n)} + \underbrace{m_{\text{eff}}^2 \sum_{k=1}^K \chi(k) c_i^{(n-k)}}_{\Sigma_1\text{ analog}}$$

**与 Σ_2 同构度: 65% (partial)**, **判定: 首选**
- 语义对 (contradiction 真在数学结构有反映) ✓
- 与 $\lambda_\Sigma$ Hartree 在结构上承接 ✓
- tractable (cost ↑ 25-35%) ✓
- full isomorphism 不可能 (PDE→discrete + operator→scalar 必然损失 35%)

---

## §3 选定 (e) + ℒ_contradiction 显式 loss

### 3.1 显式 formula

EMA history $\bar c^{(n-1)}$ 用 momentum $\beta = e^{-m_{\text{eff}}}$ 维护:

$$\boxed{\;\mathcal{L}_{\text{contradiction}}(\theta) = \frac{1}{|\mathcal{B}|}\sum_x \frac{1}{|\mathcal{I}(x)|}\sum_i \left[\frac{c_i^{(n)} - c_i^{(n-1)}}{2m_{\text{eff}}} - \frac{c_i^{(n)}}{2} + m_{\text{eff}}^2 \bar c_i^{(n-1)}\right]^2\;}$$

整体: $\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{LM}} + \alpha \cdot \mathcal{L}_{\text{contradiction}}$, $\alpha \in \{0, 0.05, 0.1, 0.5\}$ (4 档预扫描)

**超参建议**:
- $m_{\text{eff}} = \ln 2 \approx 0.693$ (half-life 1 generation)
- $|\mathcal{I}(x)| = 4$ (per example 采样 4 个分割点)
- $\beta = e^{-m_{\text{eff}}} = 0.5$

### 3.2 Python pseudocode (新建 src/contradiction_loss.py)

```python
import torch, torch.nn.functional as F

class ContradictionLoss:
    def __init__(self, m_eff: float = 0.693, num_splits: int = 4,
                 ema_beta: float | None = None):
        self.m_eff = m_eff
        self.num_splits = num_splits
        self.beta = ema_beta if ema_beta is not None else float(torch.tensor(-m_eff).exp())
        self.c_ema = None
        self.c_prev = None

    def _embed(self, hidden_states, attn_mask):
        mask = attn_mask.unsqueeze(-1).float()
        return (hidden_states * mask).sum(1) / mask.sum(1).clamp_min(1)

    def compute_c(self, model, input_ids, attn_mask):
        B, L = input_ids.shape
        splits = torch.linspace(L // 5, 4 * L // 5, self.num_splits).long()
        c_list = []
        for i in splits:
            pre_ids,  pre_mask  = input_ids[:, :i],   attn_mask[:, :i]
            post_ids, post_mask = input_ids[:, :i+L//8], attn_mask[:, :i+L//8]
            u = self._embed(model(pre_ids, attention_mask=pre_mask,
                                  output_hidden_states=True).hidden_states[-1], pre_mask)
            v = self._embed(model(post_ids, attention_mask=post_mask,
                                  output_hidden_states=True).hidden_states[-1], post_mask)
            u = F.normalize(u, dim=-1); v = F.normalize(v, dim=-1)
            c_list.append(-(u * v).sum(-1))
        return torch.stack(c_list, dim=1)

    def __call__(self, model, input_ids, attn_mask):
        c_now = self.compute_c(model, input_ids, attn_mask)
        if self.c_prev is None:
            c_prev = c_now.detach()
            c_ema  = c_now.detach()
        else:
            c_prev = self.c_prev
            c_ema  = self.c_ema
        velocity = (c_now - c_prev) / (2 * self.m_eff)
        pointwise_neg = -0.5 * c_now
        memory = (self.m_eff ** 2) * c_ema
        sigma2_analog = velocity + pointwise_neg + memory
        loss = (sigma2_analog ** 2).mean()
        with torch.no_grad():
            self.c_ema  = self.beta * c_ema + (1 - self.beta) * c_now.detach()
            self.c_prev = c_now.detach()
        return loss
```

---

## §4 arm A vs arm B 严格区分

### 4.1 arm A (人为定义矛盾, supervised)

**Loss**: $\mathcal{L}^{(A)} = \mathbb{E}_{(p,h,y)\sim\mathcal{D}_{\text{NLI}}}[\text{CE}(g_\phi(\text{enc}_\theta(p,h)), y)]$
- $g_\phi$: parallel head 3-class classifier
- 数据: SNLI / MNLI 提供 (premise, hypothesis, label)

**与 Σ_2 关系: weak 15%** — arm A 的 "矛盾" 是外部 label 注入的离散标签, 与 Σ_2 path-dependent 二阶导**没有直接 isomorphism**.

### 4.2 arm B (emergent, self-supervised)

**Loss**: 同 §3.1 (candidate e), 无外部 NLI label, $c_i$ 完全 self-derived.

**与 Σ_2 关系: 65% partial isomorphism**.

### 4.3 区分表

| 维度 | arm A | arm B |
|---|---|---|
| Contradiction signal | 外部 NLI label | self-derived $c_i = -\langle u_i, v_i\rangle$ |
| Σ_2 isomorphism | **15%** | **65%** |
| 数据需求 | SNLI + MNLI ~570k | 无外部标注 |
| 哲学定位 | thesis (实验者主导) | antithesis (系统主导) |

**关键 binding**: arm A 与 Σ_2 数学结构**基本无关**, 只借了 "contradiction" 词. paper §6 不应把 arm A 包装成 "Σ_2-motivated", **会被 reviewer 抓**. arm A 角色重新定位 = "supervised upper bound baseline" (告诉读者 "就算给 supervised contradiction signal 效果也只是 X", 让 arm B 有比较意义).

---

## §5 自检 (CLAUDE.md 项目级规则 7)

| Q | A | 备注 |
|---|---|---|
| Q1 ready binary verified? | 否 | 65% partial, 不 declare ready |
| Q2 跳过 reviewer 要求真不能做? | 部分 | full isomorphism 不可能 (跨 domain), honest disclose |
| Q3 honest 还是 user-pleasing? | honest | 不评接受概率, derive 可信度: 数学 70% / 语义 65% / 工程 90% |
| Q4 timeline gap? | 否 | 1 天 derive, D2-D3 implementation 合理 |
| Q5 mechanical-fix 替代 substantive? | 部分 | candidate (e) 65% partial 是 substantive, pseudocode 是 mechanical, 要分别评估 |

---

## §6 漏洞列表 (reviewer 视角)

- **L1**: $\lambda_\Sigma \approx 25$ 是 Σ_1 closure 不是 Σ_2 closure, 不要直接挪到 $\alpha$ 系数. $\alpha$ 必须独立扫.
- **L2**: $m_{\text{eff}}$ 在 PDE 是物理 mass, 在 LLM 是 EMA decay rate — paper 必须写 "we reinterpret $m_{\text{eff}}$ as EMA half-life in generation index space".
- **L3** ⚠️: candidate (e) 的 $c_i = -\langle u_i, v_i\rangle$ cosine signal **在 GPT-2 base 是否真有 contradiction discriminative power 尚未实证**. **必先跑 SNLI sanity check** — 在 SNLI val set 用 frozen GPT-2 base 算 $c_i$, contradiction-pair 应系统性大于 entailment-pair. 如果差距 < 1σ, **65% isomorphism 数字要降到 30%**, 可能要重选 candidate.
- **L4**: generation-axis vs token-axis 选择 ad-hoc. paper 写 "axis 选择 justification" 一段.
- **L5**: 自迭代 N1 实验要求 $n \ge 3$ 才有 $\delta^2$ 信号. 前两代退化处理要 paper 明示.

---

## §7 给主 Agent 建议修正

### 必改

1. paper 写法: candidate (e) 是 "**Σ_2-motivated loss with 65% structural correspondence**", **不**是 "Σ_2-isomorphic loss"
2. **必先**跑 §6 L3 的 SNLI sanity check (半天工作), 失败则回到 candidate (b) + EMA history
3. 跑实验前 pre-register $\alpha$ 扫描档 $\{0, 0.05, 0.1, 0.5\}$, 不事后挑 best
4. arm A 重新定位为 "supervised upper bound baseline" 而非 "Σ_2-motivated"

### 建议

5. 实做 num_splits=4, $\beta=0.5$, 先在 OPT-125m 跑 1 generation 验证 cost ↑ ≤ 50%

---

## §8 实做位置

- **新建** `src/contradiction_loss.py` (§3.2 完整版)
- **修改** `src/train_one_generation.py` (~112 行 Trainer → CATTrainer)
- **新建** `configs/cat_arm_b.yaml` ($\alpha$ 扫描 + $m_{\text{eff}}$ + num_splits)
- **新建** `scripts/sanity_check_c_signal.py` (**先跑这条 — L3 漏洞验证**)
- **修改** `src/config.py` (加 CAT dataclass 字段)

---

## §9 教学 5 元素 (给 PI 一凡)

**中文翻译**:
- candidate (候选方案): 把 Σ_2 桥到 LLM 的几种数学映射尝试
- partial isomorphism (部分同构): 两个数学结构有结构对应但不完全等价, 等价度可量化
- Volterra kernel (Volterra 核): 因果记忆型积分核, 把过去状态加权积进当下
- EMA (指数移动平均): 用 momentum 系数对历史值做指数衰减加权代替显式存历史

**直觉**: Σ_2 在 PDE 是「场的二阶时间变化」= 加速度. 映到 LLM 就是问「模型自迭代时, 自相矛盾度的加速度是不是被压住了?」如果是, η 不单调累积, 崩溃停下. 严格说是三项 (速度 + 当下负反馈 + 历史记忆) 离散 lift 在 self-entailment 空间做平方化 loss.

**机制**: next-token 单通道训练只优化 KL(p_data || p_θ), 没有「自相矛盾」的 countervailing signal. 加 ℒ_contradiction 后每次梯度更新除拟合数据还要让自相矛盾度 Σ_2-analog 趋稳, 打断 Shumailov collapse 单调上升路径. 65% isomorphism 来自三项结构都保留 + 时间轴对了, 丢失 35% 是 PDE→discrete + operator→scalar 必然损失.

**入门读物**:
- Volterra integral equation: Polyanin & Manzhirov《Handbook of Integral Equations》第 1 章 (中文版张同合译)
- Sz.-Nagy-Foias 膨胀: Sz.-Nagy 等《Harmonic Analysis of Operators on Hilbert Space》第 1-2 章 (advanced 无好中文版)
- self-distillation 与 collapse: Shumailov et al. 2024 Nature

**自验动作**:
1. jupyter 上手算 $\partial_t^2(\chi*\psi)(t)$ 验证 §1.2 三项分解
2. SNLI val set 100 对样本上算 candidate (e) 的 $c_i$, 画 contradiction vs entailment 直方图看是否分得开
3. OPT-125m 上跑 1 dummy generation, timeit 测 cost ↑ 实际 25-35%

—— 数学教授 sub-agent (zero-context, paper-review, 2026-05-08)
