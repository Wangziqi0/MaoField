# Linux Frechet 谱 spot-check (数学教授致一凡第 5 条 Linux 代办)

**写**: Linux 姐姐, 2026-04-26 ~16:45 CST (Auto mode active)
**对象**: 一凡 (代办自验) + 数学教授 + Win + 反题姐姐 (cross-check)
**前置**: `MATH_PROFESSOR_NONLINEAR_T_DRAFT_20260425.md` §8.5 致一凡第 5 条 + Win `WIN_P0_A_D1_DELIVERY_20260425.md` §3.2 主形式 + Linux V3 stamp §2.5 Linux 04-26 早代办承诺

---

## Brake B commit 复述 (slip count 2/2, 试行至 04-30)

- **当前 commit**: 2026-04-26 早 sympy Frechet 谱 spot-check (resolvent 主形式 accretivity + contraction verify, 对照 alt 形式 P0 数字失败) — Linux 04-26 早自承诺 deliverable 之一
- **距 commit**: ~immediate
- **上次 slip**: Entry #2 2026-04-24 10:37 Win D-1 交付 → 11:40 Linux 发现 (~1h30min, P2)
- **预期下次 deliverable**: 2026-04-26 晚 integrate memo (依赖 Win 端 04-26 work sync 过来)

---

## §0 verdict 先行

**主形式 Win v0.2.1 $T = (I + \eta \nabla_\psi^\dagger V)^{-1}$ 在 Phase B Exp 1 NESS regime (⟨ρ⟩=1.19, v=1) 数值上 verify 通过**: Hessian 两 eigenvalue (λ_Higgs = 2.57, λ_Goldstone = 0.19) 都严格 > 0, **strict accretive ✓**, resolvent 对任何 η > 0 严格 contraction ‖T‖ ≤ 1。**对照** projection clip alt 形式数学教授 §4.2.2 P0 数字失败 (要 ε < 0 不存在), **alt retire 确认**。

但 Linux 同时 flag: **toy scalar Mexican-hat 不是完整 GL Hartree 二阶 χ 物理模型**, 这个 spot-check 只 verify "resolvent 数学形式 well-posed", **不**直接解决 P0-C χ 1500× violation。完整 P0-C verdict 在 04-30 工作 (含 Volterra 因果核 + Σ 二阶展开 + Hartree resummation, 不是单点标量 Hessian)。

---

## §1 数学 setup

U(1)-symmetric Mexican-hat 势能 (Win D-1 v0.2.1 §2 标准约定):
$$V(\psi) = \frac{(|\psi|^2 - v^2)^2}{4}, \quad \psi = \psi_R + i\psi_I, \quad v = 1$$

Hessian (symbolic):
$$\nabla_\psi^\dagger \nabla_\psi V = \begin{pmatrix} \psi_I^2 + 3\psi_R^2 - v^2 & 2\psi_R \psi_I \\ 2\psi_R \psi_I & 3\psi_I^2 + \psi_R^2 - v^2 \end{pmatrix}$$

Phase B Exp 1 NESS regime evaluation point: $\psi_{NESS} = (\sqrt{1.19}, 0)$ (true vacuum overshoot, U(1) 任选固定相):

$$\nabla_\psi^\dagger \nabla_\psi V|_{\psi_{NESS}} = \begin{pmatrix} 257/100 & 0 \\ 0 & 19/100 \end{pmatrix}$$

eigenvalues (symbolic exact): $\{257/100, 19/100\} = \{2.57, 0.19\}$

---

## §2 Accretivity verify

定义: $A$ accretive $\iff \text{Re}\langle Au, u \rangle \ge 0 \quad \forall u \in \mathcal{H}$ $\iff$ numerical range $W(A) \subset \{z \in \mathbb{C}: \text{Re}(z) \ge 0\}$

Hessian Hermitian (real symmetric), accretivity $\iff$ all eigenvalues $\ge 0$:

| eigenvalue | 物理含义 | 值 |
|---|---|---|
| λ_Higgs (径向 mode) | massive Higgs-like radial fluctuation | 2.57 |
| λ_Goldstone (角向 mode) | quasi-Goldstone-like angular fluctuation | 0.19 |

$\text{min}(\lambda) = 0.19 > 0$ → **strict accretive ✓**

Linux V3 stamp §3.1 P2 flag "Phase B regime ($\langle|\psi|^2\rangle \approx 1.19 > v^2 = 1$, true vacuum side) 应 accretive 但未量化 verify" — **本 spot-check 量化 verify 完成**: 严格成立。

---

## §3 Resolvent contraction verify

$T = (I + \eta H)^{-1}$, $H$ Hermitian → $\|T\|_{op} = \max_i |1/(1 + \eta \lambda_i)|$

由 strict accretive ($\lambda > 0$): $\|T\|_{op} = 1/(1 + \eta \cdot \min(\lambda)) = 1/(1 + 0.19\eta) < 1$ for any $\eta > 0$.

| η | ‖T‖_op | contraction? |
|---|---|---|
| 0.01 | 0.998 | ✓ |
| 0.10 | 0.981 | ✓ |
| 0.30 | 0.946 | ✓ |
| 0.50 | 0.913 | ✓ |
| 1.00 | 0.840 | ✓ |
| 2.00 | 0.725 | ✓ |
| 5.00 | 0.513 | ✓ |
| 10.00 | 0.345 | ✓ |

**$\eta_{\max}$ analysis**:
- 数学上: 任何 $\eta > 0$ 都满足 $\|T\| \le 1$ (strict accretive case)
- 实用建议: $\eta = 1/\lambda_{\min} = 1/0.19 \approx 5.26$ 给 $\|T\| = 1/2$ (50% 压缩, 数值稳定佳)
- 推荐工作 $\eta$: $\eta \in [0.1, 0.5]$ 给 $\|T\| \in [0.91, 0.98]$ (弱到中度压缩, 物理上 conservative)

---

## §4 对照 projection clip alt 数学教授 §4.2.2 P0 数字失败

Linux 04-22 ~ 04-24 期间原推 alt 形式: $T_{\text{alt}} = \text{Proj}_{\|\cdot\|\le 1}(-\epsilon \nabla V)$

不动点方程 (数学教授 §4.2.1, Case 1 投影恒等):
$$|\psi_*|^2 = v^2 - 1/\epsilon \quad (\text{require } \epsilon > 1/v^2)$$

Phase B 数据代入 $|\psi|^2 = 1.42$ (数学教授 §4.2.2 cite, **注**: Phase B 平均 ⟨ρ⟩=1.19, $|\psi|^2 \approx 1.42$ 是 mode 上的某 sample 值, 数学教授原文如此用), $v^2 = 1$:
$$1/\epsilon = 1 - 1.42 = -0.42 \Rightarrow \epsilon = -2.38 < 0 \quad ✗$$

**结论**: alt 形式 NESS regime 不动点不存在, 与数学教授 §4.2.2 verdict 一致, **alt retire 确认**, Win v0.2.1 §3.2 footnote 应 update 标 alt P0 数字失败 (defer 到 master merge pass 时一起做, 见 `LINUX_ACK_WIN_SITREP_20260426.md` §1)。

---

## §5 与 P0-C χ 1500× violation 的初步交叉 (preview, 不替 04-30 final)

Toy scaffold 给的 λ_Goldstone = 0.19 是 mean-field scalar approximation 下的 angular mode mass²。Phase B Exp 1 实测 $\chi_{\text{exp}} \approx 0.04$, 经典 $\chi = 1/m_\theta^2$ 关系给:

$$m_{\theta, \text{exp}}^2 = 1/\chi_{\text{exp}} = 1/0.04 = 25$$

vs toy scalar Hessian $\lambda_{Goldstone} = 0.19$ 给 $\chi_{\text{toy}} = 1/0.19 \approx 5.26$

**关系**:
- 反题姐姐 P0-C 1500× gap 是 $\chi_{\text{exp}} = 0.04$ vs $\chi_{\text{theory}} = 59$ (GL Hartree 二阶预测)
- **toy** scalar mean-field Hessian $\chi \approx 5.26$ **介于实测和理论之间**, 不是简单中间点 — 是不同 model
- 实测 $m_\theta^2 \approx 25$ 与 toy $m_\theta^2 = 0.19$ 差 **132×**, 与 GL 二阶 $\chi = 59$ 差 **312×** (这两个差比 1500× 小, 说明 1500× gap 来自 GL 二阶展开的 IR 增强, 不是 mean-field scaffold)

**Linux preview 解读** (非 04-30 final, 仅 sketch):
- Hartree 自洽条件 $m_\theta^{\text{eff}, 2} = m_\theta^2 + \lambda_\Sigma \cdot \langle|\delta\theta|^2\rangle$ (Linux 04-24 P0-C draft §2.2)
- 若 toy $m_\theta^2 = 0.19$ 是 bare mass², Hartree 修正给 $m_{\theta, \text{eff}}^2 = 0.19 + \lambda_\Sigma \cdot \langle|\delta\theta|^2\rangle = 25$ ⇒ $\lambda_\Sigma \cdot \langle|\delta\theta|^2\rangle \approx 24.81 \approx 25$ ✓ **与 04-24 P0-C draft 桥接条件吻合**
- 这是 weak 一致性, 不是 hard verdict — 04-30 P0-C 工作时还要 verify (a) bare mass² 取 0.19 是否合法 (Mexican-hat at $|\psi|^2 = 1.19$ vs vacuum $|\psi|^2 = 1$ 的差异) (b) $\lambda_\Sigma$ 具体表达式 from Σ 二阶展开 (c) $\langle|\delta\theta|^2\rangle$ Phase B 实测值

**Linux flag 给反题姐姐**: λ_Goldstone = 0.19 较小 (与 Higgs ratio 13.5×) 是**预期的 Goldstone-like behavior** (虽未严格 massless, 因 ψ overshoot to $|\psi|^2 > v^2$), **不是** anomaly。但若 04-30 P0-C 工作发现完整 GL Hartree 不能桥 1500×, 这个 toy spot-check 的 λ = 0.19 不 serve as 救援 — 需独立 alternative。

---

## §6 Linux V3 stamp § 3.1 P2 flag 升级 status

V3 stamp 原 P2 flag verbatim:
> "$T = (I + \eta A)^{-1}$ 的 $\|T\| \le 1$ 数学要求 $A$ accretive ... Phase B Exp 1 regime 应 accretive, **但未量化 verify**"

**本 spot-check 量化 verify 完成**: P2 flag close ✓ (at toy scalar Mexican-hat scaffold)

**未 close**: P2 在**完整 GL field theory 含 Volterra 因果核 + Σ 二阶展开**下的 accretivity, 此 spot-check 无法 cover (model gap)。**04-30 P0-C 工作必须重做** at full GL Hartree 上的 accretivity verify, 不能 cite 本 spot-check 作 substitute。

---

## §7 致一凡: 自验动作 (30 秒 sanity check)

打开你 desktop sympy 跑这 5 行:
```python
import sympy as sp
v, x = sp.symbols('v x', real=True)
H_radial = 3*x - v**2  # Hessian 径向 (substituting psi_R²=x, psi_I=0)
H_angular = x - v**2    # Hessian 角向
print(H_radial.subs({x: sp.Rational(119, 100), v: 1}))  # 期望 257/100 = 2.57
print(H_angular.subs({x: sp.Rational(119, 100), v: 1})) # 期望 19/100 = 0.19
```

若两个数 match, 你 verify 了 Linux 这个 spot-check 的核心数字。30 秒事。

---

## §8 教学 5 元素

**中文翻译**: Frechet 导数 (Fréchet derivative, 无穷维空间映射的线性近似导数, 推广有限维 Jacobian 到 Banach 空间) / accretive (增殖性, 算子谱在右半复平面 numerical range 条件) / numerical range $W(A)$ (算子的数值范围, 集合 $\{\langle Au, u\rangle : \|u\| = 1\}$) / contraction (压缩, $\|T\| \le 1$ 意味着不放大输入) / Goldstone mode (歌德斯通模, 自发对称破缺产生的零质量或近零质量模)

**直觉**: Mexican-hat 是物理学**最简单的 SSB (自发对称破缺) toy 模型** — 像一个墨西哥草帽, 中心高 (false vacuum) 周围低圈 (true vacuum)。Phase B 实测 ⟨|ψ|²⟩ = 1.19 比 vacuum |ψ|²=1 略高, 说明系统 overshoot 到草帽圈外侧, **不在 vacuum 上**, 这让本来该 massless 的 Goldstone 也获得**小但 nonzero mass²** (= 0.19, 比 Higgs 2.57 小 13.5×)。Win 选 resolvent 形式 $T = (I + \eta H)^{-1}$ 在这种情况下数学 well-defined, 数值 verify 通过。

**机制**: resolvent 形式比 projection clip 鲁棒, 因为它**不需要不动点存在**; 只需 $H$ accretive 就保证 $T$ 压缩。Mexican-hat Hessian 在 Phase B regime overshoot side ($|\psi|^2 > v^2$) 严格 positive definite (两 eigenvalue 都 > 0), 满足 strict accretive。projection clip alt 失败是因为它要求**不动点**满足 $|\psi*|^2 = v^2 - 1/\epsilon$, Phase B regime 数据代入要 ε<0 不可行。

**入门读物**: Reed & Simon《Methods of Modern Mathematical Physics》Vol. I §VIII.1-VIII.3 (英文, 入门-中级, ~30 页讲 Hilbert space self-adjoint operators + numerical range + spectral theorem) 或 Kreyszig《Introductory Functional Analysis with Applications》Ch. 7 §7.1-7.3 (中文版三联出版, 入门, accretive/dissipative 算子的几何直觉)。

**自验**: 见 §7。如果你想更深, 把 Mexican-hat 换成 quartic + linear bias $V = (|\psi|^2 - v^2)^2/4 + h \psi_R$ 加 explicit U(1) 破缺 (Win D-1 §2.1 source $S_0$ 的数学化), 再算 Hessian 看 λ_Goldstone 是否变, 这是 P0-C 04-30 工作的预热。

---

## §9 Linux 立场 (1 句话)

**Win v0.2.1 主形式 $T = (I + \eta \nabla_\psi^\dagger V)^{-1}$ 在 Phase B Exp 1 NESS regime toy scalar Mexican-hat scaffold 上数值 verify 通过 (Hessian 两 eigenvalue 严格 > 0, accretivity 严格成立, contraction 对任何 η > 0 严格成立)**, 对照 projection clip alt 数学教授 §4.2.2 P0 数字失败 alt retire 确认; Linux V3 stamp §3.1 P2 flag (accretivity 未量化 verify) **at toy scalar scaffold close**, **at full GL field theory + Volterra + Σ 二阶展开仍 standing pending 04-30 P0-C**; toy λ_Goldstone = 0.19 与 Hartree 桥 1500× gap 弱一致 (preview only, 非 04-30 final), 反题姐姐 04-30 P0-C 完稿时若 full model accretivity 不严格成立则 P2 升 P1 future-tense forward。

— Linux 姐姐, 2026-04-26 ~16:45 CST
