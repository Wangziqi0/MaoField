# exp004 修正指令

**发给 Linux 端。替代原 exp004_dispatch.md 中的 B-E 部分。**
**实验 A（纯模拟器搭建）照做。方程和匹配逻辑改了。**

---

## 修正内容

### 1. 方程改为 Allen-Cahn + 源项

**不用 Gray-Scott。** Gray-Scott 是经验模型，和理论框架无关。

Allen-Cahn 方程从拉格朗日量 L[u,t] 的变分原理推导：

```
∂u/∂t = D∇²u - u³ + u + S(x; t)
```

- D∇²u：扩散（梯度能的变分）
- -u³ + u：双井势 V(u) = ¼(u²-1)² 的负梯度
- S(x; t)：token 源场

这不是人选的方程——是能量泛函 L = ∫[D/2|∇u|² + V(u) - u·S] dΩ 的梯度流。

**实现**：
```python
def allen_cahn_step(u, S, D, dt, dx):
    lap = laplacian_3d(u, dx)  # 7点模板 + 周期边界
    dudt = D * lap - u**3 + u + S
    return u + dt * dudt
```

参数：D=0.5, dt=0.1, dx=1.0, 网格 32³

### 2. 势能验证

先验证双井势的基本行为：
- 初始 u ≈ 0 + 小噪声 → 应该自发分裂成 u≈+1 和 u≈-1 的畴（domain）
- 畴壁（界面）应该是光滑的、宽度约 √(D) 个网格点

如果看不到分裂 → D太大（扩散压制了分裂）。减小D。
如果分裂太碎 → D太小。增大D。

### 3. 匹配改为迭代融合

**不是两个场叠加一次就算分数。是螺旋上升的迭代过程。**

```python
def iterative_fusion(u_q, u_d, S_q, S_d, max_rounds=10, tol=1e-3):
    """
    query场和doc场的螺旋上升融合。
    
    每轮：
    1. 合并场：u = (u_q + u_d) / 2
    2. 联合源场：S = S_q + S_d（但S_q和S_d会被u修改——关键！）
    3. 演化到平衡
    4. 用平衡态更新 S_q 和 S_d（互相影响）
    5. 检查收敛
    
    返回：收敛轮数、最终能量
    """
    energies = []
    
    for round in range(max_rounds):
        # 合并
        u = 0.5 * (u_q + u_d)
        
        # 联合源场（关键：源场被当前状态修改）
        S_combined = update_source(S_q, S_d, u)
        
        # 演化到平衡
        u_new, energy = evolve_to_equilibrium(u, S_combined, D, dt, dx)
        energies.append(energy)
        
        # 用新的平衡态反向更新两个场
        # A的深层认识：query场被doc的信息更新
        u_q = update_field_from_partner(u_q, u_new, S_d)
        # B的深层补全：doc场被query的信息更新
        u_d = update_field_from_partner(u_d, u_new, S_q)
        
        # 收敛检查
        if round > 0 and abs(energies[-1] - energies[-2]) < tol:
            break
    
    convergence_rounds = round + 1
    final_energy = energies[-1]
    
    return convergence_rounds, final_energy, energies


def update_source(S_q, S_d, u):
    """
    源场被当前场状态修改。
    
    关键思想：场u中已经形成的模式会反过来影响源场——
    已经理解的部分不再需要驱动，未理解的部分驱动力增强。
    
    实现：S_effective = S * (1 - |u|)
    当 |u|≈1（已经稳定在一个极值）→ 源场减弱（已理解）
    当 |u|≈0（还在界面上，未决定）→ 源场保持（需要更多信息）
    """
    suppression = 1.0 - np.abs(u)
    suppression = np.clip(suppression, 0.1, 1.0)  # 保留最低10%
    return (S_q + S_d) * suppression
```

### 4. 度量

**不手写评分。用物理过程的自然属性。**

两个度量（都不是手写的评分公式——是物理量）：

**a. 收敛速度**：融合需要几轮迭代？
- 少轮 → 两个场兼容 → 匹配好
- 多轮 → 两个场冲突 → 匹配差

**b. 多尺度频谱分析**：
```python
# 3D 傅里叶变换
F_q = np.fft.fftn(u_q_final)
F_d = np.fft.fftn(u_d_final)
F_fused = np.fft.fftn(u_fused_final)

# 功率谱
P_q = np.abs(F_q)**2
P_d = np.abs(F_d)**2

# 多尺度匹配：不同频率范围的相关度
for freq_band in [low, mid, high]:
    correlation = spectral_correlation(P_q[freq_band], P_d[freq_band])
    # 低频相关 = 抽象结构匹配（跨域也可能有）
    # 高频相关 = 具体概念匹配（同域才有）
```

### 5. 实验列表

| 实验 | 内容 | 目的 |
|---|---|---|
| A | 纯 Allen-Cahn（无源项），从噪声开始 | 验证双井势分裂 |
| B | 单词注入（"离婚"、"他打我"等） | 验证不同词产生不同模式 |
| C | 相似文本对比 | 验证量变 vs 质变 |
| D | 迭代融合（同域 query-doc） | 验证收敛速度反映匹配度 |
| E | 迭代融合（跨域 query-doc） | 验证多尺度频谱分析 |

### 6. 关键检查

每步对照公理：
- [ ] 方程是从拉格朗日量推导的（不是人选的）？ → Allen-Cahn ✓
- [ ] 物种是涌现的（不是预设的）？ → 畴壁/模式自发形成 ✓
- [ ] 匹配是物理过程（不是手写公式）？ → 迭代融合+收敛速度 ✓
- [ ] 源场被状态修改（不固定）？ → update_source 中 suppression ✓
- [ ] 确定性？ → PDE，无随机 ✓

---

*修正者: Win 端 Claude, 2026-04-10*
*基于一凡的直觉验证修正*
