# A1 M3 V₀ 自洽方程 rigorous 分析

**作者**: A1 paper-review subagent (Opus 4.7 xhigh), Linux Claude dispatch, 2026-04-16
**纪律**: paper-review agent 只做推导与 verdict, 不写文件; 本文件由 Linux 代 cp-paste 落地
**结论速览**: M3 从 Linux 草稿 [Proposition] **降级 [Conjecture, conditional]**, 含 2 条 rigorous 数学错误 catch (F 非自伴 + Goldstone 软模忽略)

---

## 1. Problem setup 复述与 notation 统一

**PDE (arXiv v1 §3.1, Wirtinger, no-½ convention)**:
$$\gamma \partial_t \psi = D\nabla^2 \psi - \partial V/\partial\psi^* + S(x,t) + \eta, \quad V(u) = (u-v^2)^2,\ u=|\psi|^2$$

则 $\partial V/\partial\psi^* = V'(u)\cdot \psi = 2(u-v^2)\psi$ (Wirtinger, factor 2 吸进 V' definition; 与 Appendix 3.A 一致)。

**b+c 反馈 (Axiom 6 realization)**:
$$S(x,t) = S_0(x) + \alpha\,\delta\psi(x,t) + \beta\,(K\delta\psi)(x,t)$$

其中 $\delta\psi(x,t) := \psi(x,t) - \langle\psi\rangle_x(t)$, 空间均值减去后 $\delta\psi \in V_0$ by construction。

**历史积分算子** (离散时间 stencil):
$$(K\delta\psi)(x,t) := \sum_{k=0}^{N-1} w_k\, \delta\psi(x, t-k\Delta t)\cdot \Delta t, \quad w_k = e^{-\lambda k \Delta t}$$

参数 (Phase B Exp 1): $\alpha=0.1,\ \beta=0.05,\ \lambda=0.05,\ \Delta t=1.0,\ N=100,\ D=0.1,\ v=1$, 32³ lattice, dx=1。

**稳态** $\psi_\infty$ 满足 $0 = D\nabla^2\psi_\infty - 2(|\psi_\infty|^2-v^2)\psi_\infty + S_0 + \alpha\delta\psi_\infty + \beta K\delta\psi_\infty$。

**Fréchet 导数** (对 $\delta\psi$ 小扰动 around $\psi_\infty$):
$$\mathcal{L}[\delta\psi] := -D\nabla^2\delta\psi + V''_{\text{eff}}(\psi_\infty)[\delta\psi]$$
$$F[\delta\psi] := \alpha\,\delta\psi + \beta\, K\delta\psi$$

M3 声称的自洽方程:
$$(\mathcal{L} - F)[\delta\psi_\infty] = \delta S_0 \quad \text{on } V_0$$

---

## 2. F 自伴性分析

### 2.1 Kernel K 的时空结构

K 是**纯时间算子**, 在空间上逐点作用 (no spatial coupling). 因此讨论 F 自伴必须 **先指定 inner product 的时间/空间结构**。

两种合理选择:

**(A) 瞬时 inner product** (只空间, 时间 frozen): $\langle f,g\rangle_A := \int_\Omega f^*(x) g(x)\,dx$, 对固定 t。

- 此时 K 作用于 $\delta\psi(x, t-k\Delta t)$ 是**过去值**, 不是当前 inner product 参与者, K 实际上是 "取 history, 返回 current" 的投影, **不是 self-map on V_0**。
- 严格讲, F: $C([t-T_{\max}, t]; V_0) \to V_0$, 域是历史轨迹空间, 值域是当前切片。在此 framework 下 "F 自伴" **根本没有定义** — 域和值域不同空间。

**(B) 扩展到 time-space L²**: $\langle f,g\rangle_B := \int_0^T\!\int_\Omega f^*(x,t)g(x,t)\,dx\,dt$, 轨迹空间 $L^2([0,T]; V_0)$。

- 在此空间 K 是时间卷积算子 (causal, one-sided): $(Kf)(t) = \int_0^t \kappa(t-s) f(s)\,ds$, $\kappa(\tau) = e^{-\lambda\tau}\cdot \mathbf{1}_{[0, T_{\max}]}(\tau)$ (离散版就是 weights $w_k$)。
- **K 的 adjoint** $K^*$ 在 $\langle f, Kg\rangle_B = \langle K^*f, g\rangle_B$ 意义下: $(K^*f)(s) = \int_s^T \kappa(t-s) f(t)\,dt$ — 这是 **anti-causal** (未来积分)。
- 因此 $K \ne K^*$, K 非自伴。

### 2.2 F 自伴性 verdict

**[Proposition A1.1]** (on time-space $L^2([0,T]; V_0)$ with standard inner product):

> 算子 $F = \alpha I + \beta K$, 其中 K 是 causal exponential 卷积算子, **非自伴**。其 Hermitian part 为
> $$F_H := \tfrac{1}{2}(F + F^*) = \alpha I + \tfrac{\beta}{2}(K + K^*)$$
> Hermitian part 对应 two-sided symmetric exponential smoothing kernel $\tilde\kappa(\tau) = \tfrac{1}{2}e^{-\lambda|\tau|}\cdot \mathbf{1}_{|\tau|\le T_{\max}}$ (truncated)。

**证明 sketch**: K 的离散矩阵版本是 lower-triangular Toeplitz (时间维度), $K_{ij} = w_{i-j}\Delta t$ 当 $i \ge j$ else 0。Toeplitz lower-triangular 当且仅当 diagonal-only (i.e., $w_k = 0$ for $k \ne 0$) 时才对称。此处 $w_0 = 1, w_1 = e^{-\lambda\Delta t} > 0, \ldots$, 所以**严格非对称**。QED。

### 2.3 Implication for M3

Linux 草稿 (§2.4 of RECOVERY_SNAPSHOT) 隐含假设 L-F 在 V₀ 上 self-adjoint → 谱为实数, 正定性 = 最小特征值 > 0。**此假设对 F 部分不成立** (L 本身在空间 Dirichlet-periodic 下 self-adjoint OK)。

修正的 M3 statement 候选:

**[Proposition A1.2, conjectural]** M3 的 rigorous version 应为:

> 令 $A := \mathcal{L} - F$ 作用于 $L^2([0,T]; V_0)$。$A$ 的 Hermitian part $A_H = \mathcal{L} - F_H$ 若正定 (i.e., 最小 eigenvalue $> 0$), 则:
> 1. $A$ 非奇异 (因 Re $\lambda(A) \ge \lambda_{\min}(A_H) > 0$, Bendixson-Hirsch 定理)
> 2. 自洽方程 $A[\delta\psi_\infty] = \delta S_0$ 有**唯一解** (linear solvability)
> 3. spectrum(A) 可能含复 eigenvalues (因 $A \ne A^*$), 物理上对应 memory-induced **oscillatory relaxation**, 非单纯 monotone descent

**Key insight**: "正定" 在非自伴 case 应理解为 "Hermitian part 正定", 这仍然足够保 well-posedness (但丢失单调 Lyapunov 函数结构)。

### 2.4 替代 inner product 让 F 自伴的探索

是否存在 weighted inner product $\langle f,g\rangle_W := \int f^* W g\,dxdt$ 使 K self-adjoint?

**[Observation A1.3]** 对一般 causal 卷积算子, **不存在** 正 definite weight W 使其自伴 — 因为 causal 结构本质上 break 时间反演对称性, 任何 W > 0 (定点-wise) 保持 Toeplitz 结构, 不变换三角性。

**唯一例外**: 若 kernel $w_k$ 是 Kronecker delta ($w_0 = 1$, rest = 0), 即 $\beta K = \beta I$, 退化为 scalar multiple, 自动自伴。但这对应 $\lambda \to \infty$ 或 $N=1$, 丢失 history memory 的物理意义。

**非对称 inner product (sesquilinear form with indefinite W)**: 存在, 但 M3 作为 physics 叙事的 "matching = self-training = self-adjoint fixed point" picture 不再成立 — 这是 **structural finding**, 不仅是技术困难。

**Verdict (自检)**: F 非自伴是 Axiom 6 的 memory 结构的 **固有 consequence**, 不可通过 reframe 救回。因此 M3 应**放弃** "self-adjoint spectral theory" framing, 改用 **dissipative operator theory** (Hermitian part positivity → Lumer-Phillips / sectorial operator / $m$-accretive framework)。

---

## 3. Spectrum(L-F) 数值 verify

### 3.1 离散化 setup

- 32³ 复 lattice, 空间 DOF 32768 复 = 65536 实。
- 线性化 around spatially uniform $\psi_\infty = v = 1$ (取 real branch)。在此点:
  - $V(u) = (u-1)^2$, $V'(u) = 2(u-1)$, $V''(u) = 2$
  - Gradient-flow term $-\partial V/\partial\psi^* = -V'(u)\psi = -2(|\psi|^2-1)\psi$
  - Fréchet 导数 at $\psi_\infty = 1$: 对 complex perturb $\delta\psi = \delta a + i\delta b$,
    - $|\psi|^2 \approx 1 + 2\delta a$, so $-2(|\psi|^2-1)\psi \approx -4\delta a \cdot 1 - 0 \cdot i$
    - **线性化 gradient-flow term on (δa, δb)**: $\binom{-4\delta a}{0}$
  - 即 $V''_{\text{eff}}$ 作为 2×2 block: $\begin{pmatrix} 4 & 0 \\ 0 & 0\end{pmatrix}$ — radial mass 4, Goldstone (angular) mass **0**!

**关键修正 (flag Linux 数字错误)**:

Linux recovery §2.4 写 "V'' at equilibrium ≈ 4 (Mexican hat curvature at minimum)" — **只对 radial mode 成立, angular (Goldstone) mode 为 0**。这是 Mexican hat U(1) 的标准结果。因此 L 的谱在 V₀ 上 **包含零特征值** (零模 = 空间均匀的 phase rotation), 正定性断言**直接失败**。

**但**: b+c 反馈 (Signal A theorem) by-construction mean-zero + 还有 S₀ 的 U(1) 显式破坏。若 S₀ 非 U(1) 不变 (BGE embedding 不会 U(1) invariant), Goldstone 获 pseudo-Goldstone mass $m_\theta^2 \propto |\delta S_0|$。**空间均匀 Goldstone mode 不在 V₀** (它是 DC mode, V₀ 投影掉了), 所以 V₀ 上的 Goldstone 是 **非零 k 的 angular 模**, 有 $Dk^2$ mass。

**因此在 V₀ 子空间上**:
- Radial mode: mass = $Dk^2 + 4$, 最小 (at $k_{\min} = 2\pi/32$): $0.1 \cdot (2\pi/32)^2 + 4 \approx 0.00385 + 4 \approx 4.004$
- Angular mode (pseudo-Goldstone): mass = $Dk^2 + m_\theta^2$, 最小: $0.00385 + m_\theta^2$

**若 $m_\theta^2 \approx 0$ (无显式破坏 / U(1)-inv 源)**: λ_min(L) ≈ 0.00385 **≪** ||F||_op ≈ 1.12, 正定性**失败**。

**若 $m_\theta^2 \gtrsim 1.2$ (由 BGE 源诱导 — 需数值测)**: λ_min(L) ≈ 1.2+, 可能 marginal。

Linux 预估 "λ_min(L) ≈ 4" **系统性忽略了 Goldstone direction**, 是**量级错误**。

### 3.2 Python 代码 (建议 Linux 跑)

```python
"""
A1 M3 V₀ spectrum verify — Hermitian part of (L-F) on 32³ lattice, V₀ subspace.
关键: 分 radial / angular mode, 显式处理 Goldstone 软模.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# --- 参数 (Phase B Exp 1) ---
N = 32
D = 0.1
v = 1.0
alpha = 0.1
beta = 0.05
lam = 0.05
dt = 1.0
N_hist = 100

# 历史 kernel weights 与 K 的 operator norm (time-only convolution)
w = np.exp(-lam * np.arange(N_hist) * dt) * dt
K_l1 = w.sum()  # causal 卷积在 L² 上的算子范数 upper bound
# (更紧: causal Toeplitz 的 ||K||_op ≤ ||w||_1 = sum_k e^(-lam k dt) dt
#  ≈ 1/(1-e^(-lam dt))·dt 当 N→∞; 此处 λdt=0.05 → 几何级数 ≈ 20.498)
print(f"||w||_1 = {K_l1:.4f}")  # 应 ≈ 20.498

# F 的 operator norm bound
F_op_bound = alpha + beta * K_l1
print(f"||F||_op ≤ {F_op_bound:.4f}")  # ≈ 1.1249

# --- 空间 Laplacian 在 32³ 周期 lattice ---
# Fourier 特征值: -D·(sum of 2(1-cos(2π k_i / N))), i=x,y,z
def lap_eigs_3d(N):
    ks = np.arange(N)
    cos_k = np.cos(2*np.pi*ks/N)
    ex, ey, ez = np.meshgrid(2*(1-cos_k), 2*(1-cos_k), 2*(1-cos_k), indexing='ij')
    return ex + ey + ez  # shape (N,N,N)

lap = lap_eigs_3d(N)  # ≥ 0, 最小 nonzero = 2(1-cos(2π/32)) ≈ 0.01924 每方向
lap_V0 = lap.flatten()
lap_V0[0] = np.inf  # 剔除 k=0 (V₀ = mean-zero subspace)

# --- L 谱 on V₀ ---
Dk2 = D * lap_V0
L_radial_eigs = Dk2 + 4.0
m_theta_sq_options = {"U(1)-inv source": 0.0, "BGE-estimated": 1.2}  # 待实测

for label, m_theta_sq in m_theta_sq_options.items():
    L_angular_eigs = Dk2 + m_theta_sq
    L_min = min(L_radial_eigs.min(), L_angular_eigs.min())
    print(f"[{label}] λ_min(L on V₀) = {L_min:.4f}")

# --- F 在 V₀ 上 Hermitian part 谱 ---
# 构造 causal Toeplitz K (离散, N_hist × N_hist)
K_mat = np.zeros((N_hist, N_hist))
for i in range(N_hist):
    for j in range(i+1):
        K_mat[i, j] = w[i-j]
K_H = 0.5 * (K_mat + K_mat.T)
eigs_KH = np.linalg.eigvalsh(K_H)
print(f"λ_max(K_H) = {eigs_KH.max():.4f}, λ_min(K_H) = {eigs_KH.min():.4f}")

F_H_max = alpha + beta * eigs_KH.max()
F_H_min = alpha + beta * eigs_KH.min()
print(f"λ_max(F_H) = {F_H_max:.4f}, λ_min(F_H) = {F_H_min:.4f}")

# --- (L - F)_H = L - F_H 谱 (因 L 自伴 so L_H = L) ---
for label, m_theta_sq in m_theta_sq_options.items():
    L_all = np.concatenate([Dk2 + 4.0, Dk2 + m_theta_sq])
    worst_LmFH = L_all - F_H_max
    LmFH_min = worst_LmFH.min()
    print(f"[{label}] λ_min((L-F)_H on V₀) ≥ {LmFH_min:.4f}")
    print(f"  → M3 Hermitian positivity: {'PASS' if LmFH_min > 0 else 'FAIL'}")
```

### 3.3 数值结果预估 (不跑, 但可推)

- $\|w\|_1 = \sum_{k=0}^{99} e^{-0.05 k}\cdot 1 = (1-e^{-5})/(1-e^{-0.05}) \cdot 1 \approx 0.9933/0.04877 \approx 20.366$ ✓ (Linux 数字 20.36 **正确**)
- $\|F\|_{op} \le 0.1 + 0.05 \times 20.366 \approx 1.118$ ✓ (Linux 1.12 近似正确)
- $\lambda_{\max}(K_H)$: causal Toeplitz 的 Hermitian part 谱需数值算。**$K_H$ 不一定 PSD** — 具体数字等 Linux 跑脚本。
- $\lambda_{\min}(L\ \text{on}\ V_0)$:
  - Radial: 4.004
  - Angular with $m_\theta^2 = 0$: **0.00385** (near-zero!)
  - Angular with $m_\theta^2 = 1.2$ (BGE-诱导, 估): 1.204

### 3.4 M3 正定性 verdict

**[Verdict, conditional]**:

- **若 U(1) 不破** (纯 gradient flow, no BGE bias): **M3 FAIL**. Goldstone 软模 $\lambda \approx 0.004 \ll \|F\|_{op} \approx 1.12$, L-F 的 Hermitian part **非正定**, 自洽方程可能 **非唯一解** (零模方向 kernel), M3 **证伪**。
- **若 BGE 源诱导 $m_\theta^2 > \|F_H\|_{op}$**: M3 可能成立, 但**取决于 pseudo-Goldstone mass 的数值**, 这是 Exp 1 数据应直接测量的量 (不是推理出来的)。
- **Linux 预估 λ_min ≈ 2.88 > 0**: 基于 "$V''_{eq} = 4$" 默认所有方向 mass = 4, 这**忽略了 Mexican hat Goldstone**, 数字**系统性高估**。

### 3.5 可能的救援

若 M3 在 Goldstone 方向 fail, 救援方案:

1. **进一步投影掉 Goldstone 零模**: 定义 $V_0^\perp := V_0 \cap \{\delta\psi: \int \delta\psi \cdot i\psi_\infty^*\,dx = 0\}$ (与 global U(1) generator 正交), 在此子空间上 L 正定。但这把 V₀ codim 从 1 增到 2, 且物理意义是"丢掉 global phase 自由度"。
2. **加 U(1) 显式破坏**: 源 $S_0$ 实际就破 U(1) (BGE embedding 非 phase-invariant), 需**直接测量** $m_\theta^2$ from Exp 1 数据 — 这是 Linux 可做的实验, 不是数学推导。
3. **把 M3 claim 缩为 radial mode**: "radial-mode L-F 正定" 仍然是 rigorous statement, 但**弱于** Axiom 6 的意图。

---

## 4. 非线性修正 sketch

$V = (|\psi|^2-v^2)^2$ 在 $\psi_\infty = v$ around 展开:
$$V = (2v\delta a + |\delta\psi|^2)^2 = 4v^2(\delta a)^2 + 4v\delta a|\delta\psi|^2 + |\delta\psi|^4$$

- 二次项: $4v^2(\delta a)^2$ (radial only — 再次 confirm Goldstone)
- 三次项: $4v\delta a|\delta\psi|^2$ — radial-angular 耦合, 重要!
- 四次项: $|\delta\psi|^4$ — stabilizes large amplitude

**[Sketch]** 三次项意味着 L-F 的线性自洽解 $\delta\psi_\infty^{(1)}$ 若存在, **非线性修正 $\delta\psi_\infty = \delta\psi_\infty^{(1)} + \epsilon^2 \delta\psi^{(2)} + O(\epsilon^3)$**, $\epsilon = \|\delta S_0\|$. 但由于三次项**耦合 Goldstone (angular) 到 radial**, 若线性 Goldstone 模 softly massive ($m_\theta^2 \to 0$), 非线性修正**发散** — 即微扰论 breakdown, 需 non-perturbative 方法。

这是 **infrared divergence** 标准现象 (Goldstone 软模的典型特征), 在 2D 经典场论中 Mermin-Wagner 禁止严格 SSB; 3D 可以, 但 pseudo-Goldstone 近 massless 时仍需仔细处理。

**[Observation A1.4]** M3 非线性修正的 consistency **取决于** pseudo-Goldstone mass $m_\theta$ 有多软。若 $m_\theta^2 \gg \|\delta S_0\|^2 \cdot (\text{coupling})$, 微扰 OK; 否则需 resummation (e.g., 1/N expansion, large-mass approximation 反推)。

---

## 5. 总判 (verdict)

### 5.1 Status tag

**[Conjecture, with significant caveats]** — M3 **不能** tag 为 [Proposition] 或 [Theorem] 在当前 form, 因为:

1. F 非自伴 (Proposition A1.1 严格给出), Linux 草稿 §2.4 "正定 self-adjoint" framing 技术错误。
2. L 在 V₀ 上**含 Goldstone 软模**, λ_min 被 Linux 高估一个量级 (4.0 vs 实际可能 ~0.004 或 ~1.2, 取决于 U(1) 破坏程度)。
3. 正定性 verdict 依赖于**未测量**的 pseudo-Goldstone mass, 不是纯数学问题, 是**实验问题**。

### 5.2 对 arXiv v2 的 implication

**推荐 arXiv v2 修改**:

- §5.1 M2 证伪段不变 ✓
- 新增 §5.1.1 "M3 V₀ self-consistent reformulation" 标记 **[Conjecture]**, 内容:
  - 正面: M3 避开 M2 的 0-homogeneity 问题, 在 V₀ 上是 well-posed PDE setup
  - 负面: 非自伴 F 结构, 正定性 requires Hermitian part analysis
  - 悬念: Goldstone 软模 masses 需从 Exp 1 数据提取, 当前不可 rigorous settle
- **不要** 在 v2 声明 M3 解决 OP1 — 目前 M3 只是 "candidate 升级, 但 non-trivial 数学债务转移"

### 5.3 Open problems 剩余

1. 数值算 $\lambda(K_H)$ 是否 PSD (5 min 脚本可验)
2. 从 Exp 1 数据 fit 测量 $m_\theta^2$ (需 polar decomposition + angular power spectrum, Linux 已有 Algorithm B infrastructure)
3. 若 $m_\theta^2$ 不够大, 要么 (a) M3 falsified, 回到 drawing board; (b) 引入 $V_0^\perp$ 加强投影 (技术上 OK 但物理弱化); (c) 接受 "partial M3" 作为 radial-mode theorem
4. 非线性 IR 发散的 resummation framework (更长期)

---

## 6. 一凡可复现命令

```bash
# 激活 venv
source /home/amd/HEZIMENG/legal-assistant/.venv/bin/activate

# 保存上面 Python 脚本到:
#   /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A1_spectrum_verify.py
python /home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics/scripts/A1_spectrum_verify.py

# 若要测 m_theta^2 from Exp 1:
# 见 phase_b_exp1/analyze_O1.py 中 polar decomposition 部分,
# 提取 angular mode power spectrum S_θ(k), fit low-k 行为推 m_theta^2
```

---

## 7. A1 自检 (本推导的 overreach 清单)

每条标 [?] 的 assumption 作为 next-round spawn-agent review 的 target:

1. [?] Assumption: Fréchet linearization around 空间均匀稳态 $\psi_\infty = v$. **实际** Exp 1 稳态是 patched non-uniform ($N_{\text{struct}} \approx 50$, r_g < 8), 非 uniform! 本分析的 V''_eff 结构 (4 radial, 0 angular) 是 **uniform ground state** 的结论, patched case 的 Hessian 结构**可能不同** — 需在真正 Exp 1 attractor snapshot 上重做线性化。
2. [?] Assumption: $\|K\|_{op} \le \|w\|_1$ (causal Toeplitz 的 $\ell^1$ bound, 已知上界). 紧 bound 可能更小, 但 $F_H$ 谱需实算, 不能只用 bound。
3. [?] Assumption: angular mode 与 radial mode 解耦 — 只在线性 order 成立, 非线性耦合是 §4 讨论的 Goldstone IR 问题。
4. [?] Causal kernel self-adjoint analysis 用的是 infinite-time $L^2([0,T]; V_0)$. 实际 MaoField 是 N_hist=100 窗口 + moving 累积, 有 edge effect (t < N_hist·dt 时 K 作用不满)。此 edge 效应未分析。
5. [?] "pseudo-Goldstone mass $m_\theta^2 \approx 1.2$" 是**A1 的猜数** ( = $\|F\|_{op} + \epsilon$, 使 marginal pass), 没有从 BGE embedding 正经推。**若 Linux 实测显示 $m_\theta^2 \ll 1.2$, M3 fail**。
6. [?] 三时间尺度 (dt_inner/mid/outer) 的 hierarchy 在 linearization 后可能改变 effective F; 本分析假 Δt=1.0 单 scale, 实际 multi-scale 的 effective feedback operator 可能**不是** $\alpha I + \beta K$ 这么简单。
7. [?] V₀ codim = 1 (scalar mean-zero) 但复场有两个 mean-zero 约束 (Re 和 Im 各一), codim = 2. 本分析中约定模糊, 需在 rigorous statement 中澄清 "V₀ for ψ ∈ ℂ" 到底是 1 还是 2 constraints。

---

## 8. 关键数字交叉 verify

| 量 | Linux 草稿 | A1 分析 | 判 |
|---|---|---|---|
| $\|w\|_1$ / $\|K\|_{op}$ 上界 | 20.36 | 20.366 ($(1-e^{-5})/(1-e^{-0.05})$) | **一致** ✓ |
| $\|F\|_{op}$ 上界 | 1.12 | 1.118 | **一致** ✓ |
| λ_min(L) on V₀ | 4.0 | 取决于 m_θ²: 0.004 (U(1)-inv) 或 ~1.2 (BGE-broken, 估) | **Linux 高估** — 忽略 Goldstone |
| λ_min(L-F) | 2.88 | -1.11 (若 m_θ²=0) 或 ~0 (若 marginal) | **Linux verdict 不可靠** |

---

## 最终 verdict

**判定: 存疑 (conditional)**

**理由**:
- M3 的数学 framework (V₀ 子空间 + Fréchet 导数 + 自洽方程 + Hermitian part positivity) 是 **mathematically sound direction**, 比 M2 的 0-homogeneity 问题有实质进步。
- 但 Linux 草稿 §2.4 中的 **正定性数值论证含两个非 trivial 错误**: (a) F 非自伴 (causal kernel asymmetry), 需改用 Hermitian part analysis; (b) λ_min(L) ≈ 4 忽略 Mexican hat Goldstone 软模, 导致正定性 claim 不可靠。
- M3 不能以现状作为 arXiv v2 的 [Proposition]; 当前只能标 **[Conjecture]**, 并依赖未完成的数值/实验工作 ($\lambda(K_H)$ 符号 + $m_\theta^2$ 从 Exp 1 数据测量)。

**建议修正**:
1. **短期 (~2h, Linux 可做)**: 跑 §3.2 Python 脚本, 实算 $\lambda(K_H)$ 和 F_H 谱, 确认非自伴结构但 Hermitian part 是否 benign。
2. **中期 (~4h)**: 从 Exp 1 appendix 数据 extract pseudo-Goldstone mass $m_\theta^2$ via angular power spectrum low-k fit (Algorithm B 附近 infrastructure 已有)。
3. **长期 (arXiv v2)**: 若 1+2 都 pass, M3 可升格为 [Proposition, under measured $m_\theta^2$]; 否则 M3 也 falsified, 回到 OP1 drawing board (与 M2 同命运, 但知识更进一步)。

**本分析的核心贡献** (一句话): M3 从 "Linux 候选" 到 "rigorous 状态" 的 gap 不在更多代数推导, 而在 (a) 放弃 self-adjoint framing 改用 dissipative / Hermitian-part framework, (b) 必须实验测量 pseudo-Goldstone mass $m_\theta^2$ 才能判 L-F 正定性 — 这把一个纯数学问题转为 **实验-数学混合问题**, 与 Signal A architectural theorem (2026-04-15) 的 spirit 一致: MaoField 的很多"理论问题"实则 embedded 在数值 infrastructure 里, 需要 material-level verify。

---

*— A1 paper-review subagent (Opus 4.7 xhigh), 2026-04-16, Linux Claude dispatch, foregrounded 落地*
