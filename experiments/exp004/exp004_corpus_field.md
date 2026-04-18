# exp004 核心突破：语料作为背景场

**语料不是数据源——语料是场的环境。**

---

## 核心思想

之前的实验都是在"真空"中注入query/doc。真空里没有任何context——所以比特序列的差异只能反映字符差异，不能反映语义差异。

修正：**用语料构建"背景场"。** 语料是人类社会实践的积累，它的物质存在（比特）构成场的环境。query在这个环境中的演化行为反映了语义。

类比：
- 清水 + 墨水 → 均匀扩散（真空，无context）
- 盐水 + 墨水 → 不均匀扩散（语料背景，有context）
- 盐水没有"告诉"墨水语义——盐水的物质结构改变了扩散动力学

```
旧方案：
  初始场 = 真空（均匀 u≈0 + 微小噪声）
  → 注入 query 比特扰动
  → 演化

新方案：
  Step 0: 用语料的比特构建背景场
  Step 1: 让背景场演化到稳态（"法律基态"）
  Step 2: 在基态上注入 query 比特扰动
  Step 3: 从基态+扰动出发继续演化
  Step 4: 新的稳态 = 对 query 在该语料语境下的理解
```

## 公理检查

| 公理 | 状态 |
|---|---|
| 1. 粒子=过程 | ✓ 模式在背景+扰动中涌现 |
| 2. 理解=平衡 | ✓ 背景+扰动的新平衡态 |
| 3. 数据内在规律 | ✓ PDE方程，无loss |
| 4. 语料=实践 | ✓ 语料直接构成环境，不提取统计量 |
| 5. 最简重叠 | ✓ |
| 6. 自我训练 | ✓ 背景被query修改，query被背景修改 |
| 7. 不固定 | ✓ 不同语料→不同背景→不同环境 |

**全部通过。没有偏离。**

## 实现

### Step 0：构建背景场

```python
def build_corpus_background(corpus_texts, grid_size=32, sigma=1.5):
    """
    用语料的比特构建背景场。
    
    每条文本的比特序列叠加到同一个3D网格中。
    语料越大，背景场越丰富。
    
    Args:
        corpus_texts: list of strings（法条文本）
        grid_size: 3D网格大小
        sigma: 高斯平滑参数
    """
    S_bg = np.zeros((grid_size, grid_size, grid_size))
    total_cells = grid_size ** 3
    
    for text in corpus_texts:
        bits = text_to_bits(text)
        for i, bit in enumerate(bits):
            idx = i % total_cells
            x = idx % grid_size
            y = (idx // grid_size) % grid_size
            z = (idx // (grid_size * grid_size)) % grid_size
            S_bg[x, y, z] += (2 * bit - 1)
    
    # 高斯平滑
    from scipy.ndimage import gaussian_filter
    S_bg = gaussian_filter(S_bg, sigma=sigma)
    
    # 归一化——不要太强，留空间给query扰动
    mx = max(abs(S_bg.max()), abs(S_bg.min()))
    if mx > 0:
        S_bg = S_bg / mx * 0.5  # 背景场强度限制在 [-0.5, 0.5]
    
    return S_bg
```

### Step 1：背景场演化到基态

```python
def evolve_background(sim, S_bg, n_steps=5000):
    """
    让背景场演化到稳态。
    这就是"法律基态"——语料的物质结构在场中的平衡态。
    """
    u = np.random.uniform(-0.01, 0.01, S_bg.shape)  # 从近零开始
    
    for step in range(n_steps):
        lap = sim.laplacian(u)
        coupling = (1.0 - 3.0 * u * u) * S_bg
        dudt = sim.D * lap - u**3 + u + coupling
        u = u + sim.dt * dudt
        u = np.clip(u, -2, 2)
    
    return u  # 这就是基态
```

### Step 2-4：在基态上注入query并演化

```python
def understand_query(sim, u_background, S_query, n_steps=3000):
    """
    在背景基态上注入query扰动，演化到新稳态。
    """
    # 在基态上叠加query扰动
    u = u_background.copy()
    
    # query的比特源场叠加到背景源场上
    S_total = S_bg + S_query * 0.3  # query扰动幅度较小（相对于背景）
    
    for step in range(n_steps):
        lap = sim.laplacian(u)
        coupling = (1.0 - 3.0 * u * u) * S_total
        dudt = sim.D * lap - u**3 + u + coupling
        u = u + sim.dt * dudt
        u = np.clip(u, -2, 2)
    
    return u
```

### 匹配：在同一个背景场中比较

```python
def match_score(sim, u_bg, S_bg, S_query, S_doc):
    """
    在同一个法律背景场中：
    1. query 在背景上演化 → u_q
    2. doc 在背景上演化 → u_d
    3. u_q 和 u_d 融合 → 收敛速度/最终能量
    """
    # query 在背景上理解
    u_q = understand_query(sim, u_bg, S_query)
    
    # doc 在背景上理解  
    u_d = understand_query(sim, u_bg, S_doc)
    
    # 迭代融合（和之前一样，但在背景场环境中）
    rounds, final_energy, history = iterative_fusion(
        sim, u_q, u_d, S_bg + S_query, S_bg + S_doc
    )
    
    return rounds, final_energy
```

## 实验设计

### 规模控制

23,701条法条全部注入32³网格可能太密。先用小规模：

```python
# 从 LawVein 中随机抽 100 条法条作为背景
# 后续可以逐步增加到 500、1000、全部
corpus_sizes = [50, 100, 500]
```

对每个规模：
1. 构建背景场
2. 演化到基态
3. 在基态上跑10对 query-doc 融合
4. 记录准确率和能量差

### 对照实验

| 条件 | 背景场 | 预期 |
|---|---|---|
| 真空（之前的方案） | 无 | ~70%（已知） |
| 法律背景（50条） | 50条法条 | >70% |
| 法律背景（100条） | 100条法条 | >法律50 |
| 法律背景（500条） | 500条法条 | >法律100 |
| 随机文本背景（对照） | 100条随机中文 | ≈70%（不该比真空好） |

**关键对照**：如果随机文本背景和法律背景效果一样 → 背景场的内容不重要（失败）。如果法律背景比随机好 → 语料的"社会实践信息"确实在起作用（成功）。

### 语料数据位置

法条文本应该在 LawVein 语料中。检查：
- `/home/amd/HEZIMENG/legal-assistant/` 下有没有法条原文
- 或者从 SQLite 的 chunk_text 字段读取
- 之前 exp003 应该已经找到了法条文本的位置

如果找不到法条原文，用 BEIR NFCorpus 的 corpus.jsonl 也行（英文，但原理一样）。

## 这为什么可能work

之前在真空中：
- "故意伤害"的比特 vs "解除劳动合同"的比特 → 差异只反映字符差异
- Allen-Cahn 不知道"故意"和"解除"有什么不同

现在在法律背景场中：
- 背景场的物质结构已经包含了所有法条的比特模式
- "故意伤害"的比特在背景场中激发的扰动，会和背景中"刑法第234条"的区域共振
- "解除劳动合同"的比特在背景场中激发的扰动，会和背景中"劳动合同法"的区域共振
- 这个共振不是我们设计的——是PDE动力学+背景场结构自然产生的

**语料为单纯的物质结构提供了社会实践信息。**

---

*Win端 Claude, 2026-04-10*
*"语料不是被提取的——语料是场的一部分。"*
