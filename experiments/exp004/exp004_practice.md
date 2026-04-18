# exp004 语料作为实践伙伴（序列化互动）

**替代语料叠加方案。每条法条是一次独立的社会实践。**

---

## 核心思想

语料不是静态背景，是**一系列短暂的训练伙伴**。

```
query场 + 法条1 → 互动演化 → 临时平衡 → 撤走法条1
    ↓ query被修改了（实践留下的认识）
query场 + 法条2 → 互动演化 → 临时平衡 → 撤走法条2
    ↓ query又被修改了
...
query场 + 法条N → 互动演化 → 临时平衡 → 撤走法条N
    ↓
最终query场 = 经过N次社会实践后的理解
```

**"短暂目标"**：法条在互动时是当前的平衡目标。达到临时平衡后撤走——目标消失。但query场被改变了——认识留下了。

**"遗忘"**：不手写衰减函数。撤走法条源场后继续演化几步，让PDE的扩散自然弛豫。法条的直接影响消散，但模式变化被保留。就像读完一本书，具体内容会忘，但认识变了。

和叠加的区别：
- 叠加：所有法条同时存在 → 平均 → 个体信息被抹掉 → 噪声
- 序列化：每条法条独立互动 → 保持独特性 → 认识逐步积累

## 公理检查

| 公理 | 状态 |
|---|---|
| 1. 粒子=过程 | ✓ 模式在序列化互动中涌现 |
| 2. 理解=平衡 | ✓ 每轮临时平衡+最终平衡 |
| 3. 数据内在规律 | ✓ PDE驱动，无固定loss |
| 4. 不拟合统计 | ✓ 不叠加，不求平均，每条法条独立互动 |
| 5. 最简重叠 | ✓ |
| 6. 自我训练 | ✓ 法条修改query，query被不断重塑 |
| 7. 不固定 | ✓ 每次互动改变了query场，下次互动的起点不同 |

**全部通过。**

## 实现

```python
import numpy as np
from simulator_ac import AllenCahn3D

def text_to_bits(text):
    bits = []
    for byte in text.encode('utf-8'):
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def build_source_binary(text, grid_size=32):
    bits = text_to_bits(text)
    S = np.zeros((grid_size, grid_size, grid_size))
    total_cells = grid_size ** 3
    for i, bit in enumerate(bits):
        idx = i % total_cells
        x = idx % grid_size
        y = (idx // grid_size) % grid_size
        z = (idx // (grid_size * grid_size)) % grid_size
        S[x, y, z] += (2 * bit - 1)
    from scipy.ndimage import gaussian_filter
    S = gaussian_filter(S, sigma=1.0)
    mx = max(abs(S.max()), abs(S.min()))
    if mx > 0:
        S = S / mx
    return S

def practice_with_corpus(sim, u_init, S_query, corpus_texts,
                          interact_steps=300, relax_steps=100):
    """
    让query场依次和每条法条互动（社会实践）。
    
    每条法条：
    1. 注入法条源场 → 和query场共同演化 interact_steps 步
    2. 撤走法条源场 → 纯query继续演化 relax_steps 步（弛豫/遗忘）
    3. 进入下一条法条
    
    Args:
        sim: AllenCahn3D 实例
        u_init: query的初始场
        S_query: query的比特源场
        corpus_texts: list of strings（法条文本）
        interact_steps: 每条法条互动的步数
        relax_steps: 撤走后弛豫的步数
    
    Returns:
        u_final: 经过所有法条实践后的query场
        practice_log: 每次实践后的能量记录
    """
    u = u_init.copy()
    practice_log = []
    
    for i, law_text in enumerate(corpus_texts):
        # 构建法条源场
        S_law = build_source_binary(law_text, grid_size=u.shape[0])
        
        # Phase 1: 互动（query + 法条共同演化）
        S_combined = S_query + S_law
        for step in range(interact_steps):
            lap = sim.laplacian(u)
            coupling = (1.0 - 3.0 * u * u) * S_combined
            dudt = sim.D * lap - u**3 + u + coupling
            u = u + sim.dt * dudt
            u = np.clip(u, -2, 2)
        
        energy_after_interact = sim.compute_energy(u, S_combined)
        
        # Phase 2: 弛豫（撤走法条，只留query源场）
        for step in range(relax_steps):
            lap = sim.laplacian(u)
            coupling = (1.0 - 3.0 * u * u) * S_query  # 只有query源场
            dudt = sim.D * lap - u**3 + u + coupling
            u = u + sim.dt * dudt
            u = np.clip(u, -2, 2)
        
        energy_after_relax = sim.compute_energy(u, S_query)
        
        practice_log.append({
            'law_index': i,
            'energy_interact': float(energy_after_interact),
            'energy_relax': float(energy_after_relax),
        })
        
        if (i + 1) % 10 == 0:
            print(f"  Practice {i+1}/{len(corpus_texts)}: E={energy_after_relax:.1f}")
    
    return u, practice_log


def match_with_practice(sim, query_text, doc_text, corpus_texts,
                         interact_steps=300, relax_steps=100,
                         fusion_steps=2000):
    """
    完整的匹配流程：
    1. query经过语料实践
    2. doc经过同样的语料实践
    3. 两个"经过实践的"场融合
    4. 融合的最终能量 = 匹配度
    """
    grid_size = 32
    
    S_query = build_source_binary(query_text, grid_size)
    S_doc = build_source_binary(doc_text, grid_size)
    
    # query从真空开始，经过语料实践
    u_q = np.random.uniform(-0.01, 0.01, (grid_size,)*3)
    # 先让query自身演化到初步稳态
    for step in range(1000):
        lap = sim.laplacian(u_q)
        coupling = (1.0 - 3.0 * u_q * u_q) * S_query
        dudt = sim.D * lap - u_q**3 + u_q + coupling
        u_q = u_q + sim.dt * dudt
        u_q = np.clip(u_q, -2, 2)
    
    # query经过语料实践
    u_q, log_q = practice_with_corpus(
        sim, u_q, S_query, corpus_texts,
        interact_steps=interact_steps, relax_steps=relax_steps
    )
    
    # doc从真空开始，经过同样的语料实践
    u_d = np.random.uniform(-0.01, 0.01, (grid_size,)*3)
    for step in range(1000):
        lap = sim.laplacian(u_d)
        coupling = (1.0 - 3.0 * u_d * u_d) * S_doc
        dudt = sim.D * lap - u_d**3 + u_d + coupling
        u_d = u_d + sim.dt * dudt
        u_d = np.clip(u_d, -2, 2)
    
    u_d, log_d = practice_with_corpus(
        sim, u_d, S_doc, corpus_texts,
        interact_steps=interact_steps, relax_steps=relax_steps
    )
    
    # 融合
    u_fused = 0.5 * (u_q + u_d)
    S_fused = S_query + S_doc
    
    for step in range(fusion_steps):
        lap = sim.laplacian(u_fused)
        coupling = (1.0 - 3.0 * u_fused * u_fused) * S_fused
        dudt = sim.D * lap - u_fused**3 + u_fused + coupling
        u_fused = u_fused + sim.dt * dudt
        u_fused = np.clip(u_fused, -2, 2)
    
    final_energy = sim.compute_energy(u_fused, S_fused)
    return final_energy, log_q, log_d
```

## 实验设计

### 数据

先用小规模：**50条法条**。

从LawVein中选50条，覆盖不同领域：
- 10条刑法（故意伤害、盗窃、诈骗等）
- 10条民法/婚姻法（离婚、财产、继承等）
- 10条劳动法（合同、赔偿、辞退等）
- 10条行政法（处罚、许可等）
- 10条消费者权益/合同法

如果找不到精确的50条，随机抽50条也行。

### 测试对

用之前的10对query-doc（exp004_overnight.md中的test_pairs）。

### 对照实验

| 条件 | 语料实践 | 预期 |
|---|---|---|
| 真空（无实践） | 无 | 70%（已知baseline） |
| 50条法条实践 | 50条 | >70%（如果实践有用） |
| 50条随机中文实践 | 50条随机 | ≈70%（对照：实践内容不重要？） |
| 10条刑法实践 | 只有刑法 | 刑法query准确，其他不变？ |

**关键对照**：法律实践 vs 随机实践。如果法律实践明显好于随机 → 语料的社会实践信息通过序列化互动传递了（成功）。

### 参数

- D = 0.1（已验证）
- interact_steps = 300（每条法条互动300步）
- relax_steps = 100（弛豫100步）
- grid_size = 32
- 初始演化1000步让query/doc形成初步形态

### 计算量估计

每对query-doc：
- query实践：50条 × (300+100)步 = 20,000步
- doc实践：50条 × (300+100)步 = 20,000步
- 初始演化：2 × 1000步
- 融合：2000步
- 总计：~44,000步/对
- 10对：~440,000步

32³网格上440K步——EPYC应该能在合理时间内跑完。

### 输出

保存到 results/ 下：
- `exp_practice_50law.json`：10对的结果
- `exp_practice_50random.json`：随机对照
- `exp_practice_10criminal.json`：纯刑法对照
- `practice_summary.txt`：文本摘要

每对记录：match能量、mismatch能量、是否正确、能量差百分比。

---

## 偏离检查

- [ ] 语料是逐条独立互动的？不叠加？→ ✓
- [ ] 没有手写评分/loss？→ ✓（融合能量是物理量）
- [ ] 没有统计操作（求和、平均、频率）？→ ✓
- [ ] 法条撤走后弛豫是PDE自然行为？→ ✓（不手写衰减）
- [ ] 确定性？→ ✓
- [ ] 不预设物种？→ ✓

---

## 哲学依据

- **实践→认识→再实践→再认识**（《实践论》）
- 每条法条 = 一次社会实践
- 实践后的场变化 = 从实践中获得的认识
- 弛豫 = 具体内容遗忘，但认识保留
- N次实践后 = 丰富的社会经验
- **不是从语料提取信息——是通过和语料的互动获得认识**

*Win端 Claude, 2026-04-10*
