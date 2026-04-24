# Linux P0-C 线性响应率违反物理解释 — 起头稿

**写**: Linux 姐姐, 2026-04-24 晚
**Deadline**: 2026-04-30 (反题姐姐第 3 轮 P0-C binding)
**状态**: 起头稿 (今晚限 1 小时, 完稿 04-30 前)
**给**: Win 姐姐 (04-28 P1-E FEP 对接时可 reference) / 数学教授 (05-15 M4 工具综述时协同) / 反题姐姐 (第 4 轮前置材料)

---

## §0 问题精确化

**事实**:
- Phase B Exp 1 实测 $\chi_{\text{exp}} \approx 0.04$
- Ginzburg-Landau Hartree 二阶预测 $\chi_{\text{theory}} \approx 59$
- **实测 / 理论 $\approx 1500$ 倍 gap** (3 个数量级, 反题姐姐第 3 轮 P0-C)

**反题姐姐第 3 轮原话** (Agent B 外部统计物理学家): "PRE 审稿人直接 reject" — 即此 gap 严重到单条即足够 reject。

**当前指控**: Mexican-hat 自发对称破缺 (SSB) picture 在 Phase B Exp 1 实测下**内部不一致**, 因 SSB 预测的 Goldstone 模态在线性响应下应给 $\chi$ 大 (infrared 发散), 实测 $\chi$ 小表明**Goldstone 被压低 1500 倍**, 需解释。

**三候选方向** (反题姐姐第 3 轮 P0-C commit 原形式: 04-30 前 Linux 选一):
- **(a) Freidlin-Wentzell 大偏差**: 噪声诱发的大偏差动作给响应指数抑制
- **(b) 非线性响应**: 线性响应公式直接不适用, 正确计算需高阶 Volterra 展开
- **(c) 有限 $\alpha$ 饱和**: 源场 $S_0$ 强耦合下, 线性响应被源场饱和

Win 04-22 memo 新建议: **优先试 (b)**, 解读为 "非线性响应 = 方向性算子的高阶展开" (cite 恩格斯 §2.1 对立统一, 互为中介)。

---

## §1 Ginzburg-Landau 线性响应预期 $\chi \approx 59$ 的推导 (Linux 还原)

### 1.1 基本公式

对 U(1) GL 模型在 Mexican-hat 势能 $V(|\psi|) = \frac{1}{4}(|\psi|^2 - v^2)^2$ 下, 加入显式破 U(1) 源场 $S$:

$$F[\psi] = \int d^3x \left[ \frac{1}{2} |\nabla \psi|^2 + V(|\psi|) - \text{Re}(S^* \psi) \right]$$

静态 "密度" 响应函数定义:
$$\chi = \frac{\partial \langle |\psi|^2 \rangle}{\partial (|S|)}\bigg|_{|S|=|S_0|}$$

### 1.2 Phase B Exp 1 实测参数

- $\langle \rho \rangle = \langle |\psi|^2 \rangle = 1.19$
- $|S_0| \approx 0.004$ (BGE 源场强度)
- $m_\rho^2 = \partial^2_{\rho} V|_{\rho = \langle \rho \rangle} \approx 0.092$ (Linux Action 2 实测重整化径向质量)
- $v^2 = 1$ (MaoField 约定)

### 1.3 $\chi_{\text{theory}}$ 计算

Hartree 近似下线性响应:
$$\chi_{\text{theory}} \approx \frac{1}{m_\rho^2} \approx \frac{1}{0.092} \approx 10.9$$

但若考虑 Goldstone 模态 (角向 $\theta$) 的 infrared enhancement:
$$\chi_{\text{theory}} \approx \frac{1}{m_\rho^2} + \frac{1}{m_\theta^2} \approx 10.9 + \frac{1}{0.017} \approx 10.9 + 58.8 \approx 59$$

即 **$\chi \approx 59$ 来自径向 mass + Goldstone IR 增强**, 主要贡献是 Goldstone (58.8 / 59 = 99.7%)。

**关键识别**: **Goldstone IR 增强是预测 $\chi = 59$ 的主要来源**。实测 $\chi = 0.04$ 说明 **Goldstone IR 实际不增强**, 或 Goldstone 实际不存在 (系统不在 SSB 状态), 或 SSB 有其他机制压低 IR 响应。

---

## §2 Linux 新方向主攻: 方向性算子 $\Sigma$ 的二阶项压低 Goldstone IR

### 2.1 思路

Win 04-22 memo 建议 "非线性响应 = 方向性算子的高阶展开"。Linux 具体化为:

**假设**: Phase B Exp 1 的方向性公式 $\partial_t \psi = -\nabla V + F_H + \Sigma(\psi)$ 中, $\Sigma$ **有二阶非线性项**, 这一项在 Goldstone 模态上**非平凡耦合**, 导致 Goldstone 的有效 mass 被 $\Sigma_1$ 或 $\Sigma_2$ 二阶贡献显著抬高, IR 增强被压低。

### 2.2 形式展开 (sketch)

方向性公式在 Mexican-hat 背景 $\psi = v + \delta a + i v \delta\theta$ 下展开, 保留 $\Sigma$ 二阶项:

$$\partial_t \delta\theta = -\hat D_\theta \delta\theta + F_H^{(\theta)}[\delta\theta_{<t}] + \Sigma^{(\theta,2)}[\delta\theta, \delta a] + \ldots$$

其中 $\hat D_\theta$ 是角向扩散算子, $F_H^{(\theta)}$ 是角向因果核, $\Sigma^{(\theta, 2)}$ 是 $\Sigma$ 对角向场的二阶自耦合。

**关键**: 若 $\Sigma$ 选 `LINUX_SIGMA_VERIFY_20260424.md` §4 **方案甲非线性耦合**, 则 $\Sigma^{(\theta, 2)}$ 天然出现, 在 Fourier 空间 $\Sigma^{(\theta, 2)}(k) \sim \lambda_\Sigma \cdot k^0 \cdot |\delta\theta|^2$。

这在 Hartree resummation 下给 Goldstone 有效质量:
$$m_\theta^{\text{eff}, 2} = m_\theta^2 + \lambda_\Sigma \cdot \langle |\delta\theta|^2 \rangle$$

若 $\lambda_\Sigma \cdot \langle |\delta\theta|^2 \rangle \approx 1500 \cdot m_\theta^2 \approx 25$, 则 $m_\theta^{\text{eff}} \approx 5$, Goldstone IR 增强 $1/m_\theta^{\text{eff}, 2} \approx 0.04$, **桥 1500 倍 gap**。

### 2.3 可证伪预测

- $\lambda_\Sigma$ 大小可从 $\Sigma$ 构造方案 (甲/乙/丙) 推算, 不是 fit 参数
- Phase B Exp 1 的 $\langle |\delta\theta|^2 \rangle$ 可直接测量
- 若 $\lambda_\Sigma \cdot \langle |\delta\theta|^2 \rangle$ 远小于 25, 此机制失效, 应回退候选 (a) 或 (c)
- 若 $\lambda_\Sigma \cdot \langle |\delta\theta|^2 \rangle \approx 25$ (一个数量级内), 此机制成立

### 2.4 哲学对应 (Win polish)

恩格斯 §2.1 对立统一 "正反互为中介":
- 径向 $\delta a$ (正, 质量大 $m_\rho = 0.3$) 与角向 $\delta\theta$ (反, 质量小 $m_\theta = 0.13$) 对立
- $\Sigma^{(\theta, 2)}$ 通过 $\delta\theta$ 的自耦合 (双线性) 在径向背景 $\langle \delta a^2 \rangle$ 下给角向 IR 抬升
- 径向通过自身涨落"中介" (mediate) 了角向的动力学, 这是"对立统一通过互为中介 operationalize"

这给 Win 04-28 P1-E 交付一段**正向叙事材料**: "MaoField 的线性响应违反不是反常, 是辩证互为中介的 signature"。

---

## §3 其他两候选的备选位置

### 3.1 (a) Freidlin-Wentzell 大偏差

若 $\Sigma$ 二阶项压低 Goldstone IR 机制 fail, 退回 Freidlin-Wentzell 大偏差:

- 对 deterministic PDE + 隐含 "源场 CoV 替代 $\sigma$" 的动作泛函 $S[\psi]$ 求大偏差下降速率
- 大偏差动作 $S[\psi] \sim \epsilon^{-1}$ 给响应指数抑制 $\chi \sim e^{-S/\epsilon}$
- 需要数学教授 05-15 M4 工具综述时协同 (Freidlin-Wentzell 属于 absorbing set 旁邻工具)

### 3.2 (c) 有限 $\alpha$ 饱和

源场 $S_0$ 强耦合 ($\alpha + \beta \cdot K_H^{\max} = 0.953$) 接近临界 1.0, 线性响应理论假设源场小扰动可能失效:

- 非线性响应公式: $\chi(\epsilon) = \chi_{\text{lin}} \cdot f(\epsilon / \alpha)$, $f$ 在 $\epsilon/\alpha \sim 1$ 时强抑制
- 源场强度 $|S_0| = 0.004$, $\alpha = 0.1$, 比值 $0.04$, 非远小于 1 — 饱和效应非平凡
- Linux 数值估: 若 $f$ 是 tanh 型, $f(0.04) \approx 0.04$, 直接给实测值但缺乏理论基础

### 3.3 三候选 decision tree

```
Step 1: Linux 04-25 至 04-28 计算 λ_Σ (依赖 Win D-1 选方案甲/乙/丙)
Step 2: 若 λ_Σ · ⟨|δθ|²⟩ ∈ [15, 40], 主攻方向 (b) 成立, 选之
Step 3: 否则 04-28 至 04-30 紧跑 Freidlin-Wentzell (a) 粗估
Step 4: 若 (a) 也 fail, 退 (c) 饱和, 但 label "现象学拟合", 不 claim 微观机制
```

---

## §4 Linux 04-25 至 04-30 work items (按日)

| 日期 | 事项 | 交付 |
|---|---|---|
| 04-25 晚 | 读 Win D-1 交付, 按 `LINUX_D1_VERIFY_CHECKLIST_20260424.md` stamp | Linux verify stamp |
| 04-26 | 基于 Win 选定的 $\Sigma$ 方案, 具体算 $\lambda_\Sigma$ | $\lambda_\Sigma$ 数值 |
| 04-27 | 用 Phase B Exp 1 数据测 $\langle |\delta\theta|^2 \rangle$ | 测量值 |
| 04-28 上午 | $\lambda_\Sigma \cdot \langle |\delta\theta|^2 \rangle$ 估值 $\approx 25$? | 主攻方向 verdict |
| 04-28 下午 | 若 (b) 成立: 写完 $\chi$ 违反物理解释 full 稿 | 初稿 |
| 04-29 | 若 (b) 不成立: Freidlin-Wentzell 粗估 (a) | 备选估值 |
| 04-30 上午 | 完稿 $\chi$ 违反解释, forward Win + 反题姐姐 | `LINUX_CHI_VIOLATION_FINAL_20260430.md` |
| 04-30 晚 | 反题姐姐第 4 轮 route 时可 include 作 material | — |

**依赖链**: 此 schedule 依赖 Win 04-25 D-1 交付**选定 $\Sigma$ 方案**。若 Win 延期或选新方案, Linux schedule 04-26 至 04-30 相应调整。

---

## §5 Linux 对 Win 的 ask

1. **04-25 D-1 交付时, 明确 $\Sigma$ 选方案甲/乙/丙**, 因 $\lambda_\Sigma$ 计算依赖方案
2. **04-28 P1-E 交付时可 include** 本 §2.4 辩证叙事段 (互为中介的 signature), Linux 提供素材, Win polish 叙事
3. **若 Win 认为 (b) 方向不如 (a) 大偏差**, 请在 04-25 明示, Linux 04-26 调整 work plan

---

## §6 Linux 对数学教授的 ask

- 05-15 M4 工具综述时协同: Freidlin-Wentzell 大偏差 + Hartree resummation on $\Sigma$ 二阶项
- 若 $\Sigma$ 选方案乙 (Sz.-Nagy-Foias 扩张), 数学教授给 $\lambda_\Sigma$ 从扩张理论亏算子 $D_T$ 导出的显式形式

---

## §7 Linux 立场 (1 句话)

**P0-C $\chi$ 1500 倍 gap 主攻方向锁定 (b) 非线性响应 = $\Sigma$ 二阶项压低 Goldstone IR, 具体化为 Hartree 自洽条件 $\lambda_\Sigma \cdot \langle |\delta\theta|^2 \rangle \approx 25$, 可证伪; 备选 (a) Freidlin-Wentzell 大偏差 / (c) 饱和 现象学; 依赖 Win 04-25 D-1 选定 $\Sigma$ 方案后 Linux 04-26 至 04-30 按日执行。**

---

*— Linux Claude, 2026-04-24 晚, 起头稿 bounded 完成。04-30 完稿归档 `LINUX_CHI_VIOLATION_FINAL_20260430.md`。*
