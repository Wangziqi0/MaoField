# MaoField Exp004 最终版 — 完整指令

**日期**: 2026-04-10
**发给**: Linux 192.168.31.36 的 Claude Code
**来自**: Win 端 Claude

---

## 背景

实验A已通过：Allen-Cahn在32³网格上D=0.1稳定产生双畴结构。基础设施就绪。

现在发B-E实验指令。**本指令替代之前所有版本。**

---

## 核心公理（违反任何一条就停）

1. 粒子是动态过程，不是静态定义。不预设物种。
2. 理解 = 内外对立统一的平衡态。不手写评分。
3. 驱动力 = 数据内在规律。不设loss/外部目标。
4. 语料是实践记录。不拟合统计分布。
5. 复杂 = 最简单的重叠。
6. 匹配本身就是自我训练。目标和状态同时演化。
7. 不固定。

---

## 理论基础（必读）

### 拉格朗日量

$$L[u, t] = \int_\Omega \left[ \frac{D}{2}|\nabla u|^2 + \frac{1}{4}(u^2-1)^2 - (1-u^2) \cdot u \cdot S(\mathbf{x}; t) \right] d\Omega$$

三项：
- 梯度能：场倾向于平滑
- 双井势 V(u)=¼(u²-1)²：场有两个稳态 u=+1 和 u=-1（对立面）
- 非线性耦合 -(1-u²)·u·S：token对场的影响，**自适应衰减**——|u|→1时耦合自动消失（已理解的区域不再需要驱动）

### 为什么是双井势

不是人选的。是"对立统一"（至少两个稳态）+"最简重叠"（公理5：复杂性通过多个双井分量的叠加实现，不是一个多井势）的唯一最简形式。任何具有两个极值的光滑势能在极值附近都Taylor展开为双井形式——普适性。

### 场方程

从L的变分原理推导（梯度流 ∂u/∂t = -δL/δu）：

```
∂u/∂t = D∇²u - u³ + u + (1 - 3u²) · S(x; t)
```

- D∇²u：扩散
- -u³+u：双井势的力（推向±1）
- (1-3u²)·S：自适应源项。注意乘了 (1-3u²)：
  - u≈0时：(1-3·0)=1 → 源项满强度（未决定，需要信息）
  - u≈±1时：(1-3·1)=-2 → 源项反转并衰减（已稳定）

这个自适应不是手写的——是非线性耦合项的变分结果。

### 源场映射（极简）

**只用1维：词序。** 不人为填充3个维度。

第i个词在x轴的第i个位置注入高斯扰动。3D空间中的y、z方向由场自发涌现结构。

```python
def build_source_1d(tokens, grid_size):
    """
    tokens: list of strings (词序列)
    返回: 3D 源场 S[grid_size, grid_size, grid_size]
    """
    S = np.zeros((grid_size, grid_size, grid_size))
    n = len(tokens)
    sigma = 2.0  # 高斯宽度
    
    for i, word in enumerate(tokens):
        # x位置由词序决定（唯一的映射规则）
        px = int(i / n * (grid_size - 1))
        # y, z 位置固定在中心——让场自己决定怎么展开
        py = grid_size // 2
        pz = grid_size // 2
        
        # 高斯扰动
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                for dz in range(-4, 5):
                    ix = (px + dx) % grid_size
                    iy = (py + dy) % grid_size
                    iz = (pz + dz) % grid_size
                    dist2 = dx*dx + dy*dy + dz*dz
                    S[ix, iy, iz] += np.exp(-dist2 / (2*sigma*sigma))
    
    # 归一化到 [-1, 1]
    if S.max() > 0:
        S = S / S.max()
    
    return S
```

**幅度相同**：所有词的扰动幅度=1。不根据"重要性"区分（那需要外部标准）。让场自己通过演化决定哪些词产生更大影响。

### 匹配：迭代融合

不手写评分。用物理过程。

```python
def iterative_fusion(sim, u_q, u_d, S_q, S_d, max_rounds=10, tol=1e-3):
    """
    两个场的螺旋上升融合。
    
    每轮：
    1. 合并两个场
    2. 在联合源场下演化到平衡
    3. 用新平衡态反向影响两个场
    4. 检查收敛
    
    返回: (convergence_rounds, final_energy, energy_history)
    """
    energies = []
    
    for r in range(max_rounds):
        # 合并
        u = 0.5 * (u_q + u_d)
        
        # 联合源场（源场会被场状态自动调制——因为方程中是(1-3u²)·S）
        S = S_q + S_d
        
        # 演化到平衡（用修正后的Allen-Cahn方程）
        for step in range(2000):
            lap = sim.laplacian(u)
            # 修正后的方程：源项自适应
            coupling = (1.0 - 3.0 * u * u) * S
            dudt = sim.D * lap - u**3 + u + coupling
            u_new = u + sim.dt * dudt
            u_new = np.clip(u_new, -2, 2)
            
            if step > 0 and step % 100 == 0:
                change = np.max(np.abs(u_new - u))
                if change < 1e-4:
                    break
            u = u_new
        
        # 计算能量
        energy = sim.compute_energy(u, S)
        energies.append(energy)
        
        # 用新平衡态更新两个场（螺旋上升）
        # A被B的信息更新：query场向融合态靠近
        u_q = 0.7 * u_q + 0.3 * u
        # B被A的信息更新：doc场向融合态靠近
        u_d = 0.7 * u_d + 0.3 * u
        
        # 收敛检查
        if r > 0 and abs(energies[-1] - energies[-2]) / (abs(energies[-2]) + 1e-10) < tol:
            break
    
    return r + 1, energies[-1], energies
```

**度量（不是手写评分——是物理量）**：
- 收敛轮数：少=匹配好，多=匹配差
- 最终能量：低=融合好，高=融合差
- 能量下降速率：快=兼容，慢=冲突

---

## 实验列表

### 实验 B：单文本注入

**目的**：验证不同文本在场中产生不同的模式。

测试文本（中文，用jieba分词或手动分词）：

```python
texts = {
    "criminal": ["故意", "伤害", "他人", "身体"],
    "labor": ["解除", "劳动", "合同", "赔偿"],
    "divorce": ["离婚", "后", "财产", "分割"],
    "criminal_heavy": ["故意", "伤害", "他人", "身体", "致人", "重伤"],
    "traffic": ["交通", "事故", "责任", "认定"],
}
```

**步骤**：
1. 对每个文本，构建1D源场
2. 从均匀真空（u=0.01的随机噪声）开始
3. 跑 Allen-Cahn 5000步
4. 保存最终场的统计量：
   - +1域百分比、-1域百分比、界面百分比
   - 3D傅里叶功率谱
   - 连通域数量

**成功标准**：不同文本的统计量有可区分的差异。

### 实验 C：量变 vs 质变

**目的**：验证"他打我"是质变而"房子怎么分"是量变。

```python
# 基础query
base = ["离婚"]  # 扔入一个词，观察对称分裂

# 量变context
context_quant = ["房子", "怎么", "分"]  # 在base演化到稳态后注入

# 质变context  
context_qual = ["他", "打", "我"]  # 在base演化到稳态后注入
```

**步骤**：
1. "离婚"注入 → 演化到稳态 → 记录+1域/-1域比例（应该接近50/50）
2. 在稳态上注入"房子怎么分" → 继续演化 → 记录比例（应该偏移但两域都在）
3. 在稳态上注入"他打我" → 继续演化 → 记录比例（应该一方压倒另一方）

**成功标准**：
- "离婚"单独：接近50/50（歧义/对称）
- +"房子怎么分"：偏移但两域共存（量变/相持）
- +"他打我"：一方占主导（质变）

### 实验 D：迭代融合（同域）

**目的**：验证匹配的query-doc融合更快。

```python
query = ["他", "打", "我", "怎么", "判"]
doc_match = ["故意", "伤害", "他人", "身体", "处", "三年", "以下"]
doc_mismatch = ["解除", "劳动", "合同", "经济", "补偿"]
```

**步骤**：
1. query场演化到稳态
2. doc_match场演化到稳态
3. doc_mismatch场演化到稳态
4. query + doc_match 迭代融合 → 记录收敛轮数和最终能量
5. query + doc_mismatch 迭代融合 → 记录收敛轮数和最终能量

**成功标准**：
- query + doc_match 的收敛轮数 < query + doc_mismatch
- query + doc_match 的最终能量 < query + doc_mismatch

### 实验 E：多尺度频谱分析

**目的**：验证跨域文本在低频（大尺度）有共振。

```python
# 同域对
text_a1 = ["故意", "伤害", "他人", "身体"]       # 刑法
text_a2 = ["故意", "杀人"]                        # 刑法

# 跨域对
text_b1 = ["故意", "伤害", "他人", "身体"]       # 刑法
text_b2 = ["劳动", "合同", "经济", "补偿"]       # 劳动法
```

**步骤**：
1. 每个文本演化到稳态
2. 对每个稳态做3D FFT → 功率谱
3. 把功率谱分成频段：低频（|k|<4）、中频（4≤|k|<10）、高频（|k|≥10）
4. 计算同域对和跨域对在每个频段的功率谱相关度

**成功标准**：
- 同域对：高频和低频都相关
- 跨域对：高频不相关，低频可能有一定相关（"中间层"）

---

## 代码结构

```
/home/amd/HEZIMENG/MaoField/experiments/exp004/
├── simulator_ac.py       # 已完成（实验A），需要修改方程加(1-3u²)因子
├── source.py             # 1D词序源场构建
├── fusion.py             # 迭代融合
├── run_B.py              # 实验B
├── run_C.py              # 实验C
├── run_D.py              # 实验D
├── run_E.py              # 实验E
├── analyze.py            # 频谱分析
├── results/
└── README.md             # 本文件
```

## 关键修改：simulator_ac.py 需要更新

原方程：∂u/∂t = D∇²u - u³ + u + S

改为：∂u/∂t = D∇²u - u³ + u + **(1 - 3u²)** · S

这个 (1-3u²) 因子是从非线性耦合的变分推导出来的，不是手加的。它实现了自适应：已稳定区域（|u|≈1）的源项自动减弱。

```python
# 原来
dudt = self.D * lap - u**3 + u + S

# 改为
coupling = (1.0 - 3.0 * u * u) * S
dudt = self.D * lap - u**3 + u + coupling
```

---

## Agent调度建议

可以分3个agent并行：

| Agent | 任务 | 依赖 |
|---|---|---|
| agent-code | 修改simulator，实现source.py和fusion.py | 无 |
| agent-exp-BC | 跑实验B和C | agent-code完成后 |
| agent-exp-DE | 跑实验D和E | agent-code完成后 |

B/C快（单文本演化），D/E慢（迭代融合，每对需要多轮）。

---

## 偏离检查

在开始每个实验前对照：
- [ ] 方程是从拉格朗日量推导的？→ Allen-Cahn + (1-3u²)·S ✓
- [ ] 物种是涌现的？→ 畴壁/畴从场演化中自发形成 ✓
- [ ] 匹配是物理过程？→ 迭代融合+收敛速度 ✓
- [ ] 源场不用统计？→ 只用词序位置 ✓
- [ ] 没有手写评分/loss？→ 收敛轮数和能量都是物理量 ✓
- [ ] 源项自适应（不固定）？→ (1-3u²)因子 ✓
- [ ] 确定性？→ PDE，无随机 ✓

---

*Win端 Claude, 2026-04-10*
*"粒子是过程，不是定义。"*
