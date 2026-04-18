# exp004 源场修正V3：比特级物质映射

**替代笔画+Unicode码点方案。直接用文本的二进制表示。**

---

## 核心思想

文本在硬件中的存在形式就是0和1。这是物质的最底层。

```
"故意伤害" UTF-8:
故: 11100110 10010101 10000101
意: 11100110 10000100 10001111
伤: 11100100 10111100 10100100
害: 11100101 10101110 10110011

= 96个比特，每个比特是确定的物质状态
```

0和1直接对应Allen-Cahn的双井势：
- 比特=1 → 正扰动（u=+1方向）
- 比特=0 → 负扰动（u=-1方向）

## 新的 source.py

```python
import numpy as np

def text_to_bits(text):
    """文本 → 比特序列（UTF-8编码）"""
    raw = text.encode('utf-8')
    bits = []
    for byte in raw:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def build_source_binary(text, grid_size=32):
    """
    比特级源场。
    
    每个比特映射到3D网格的一个位置：
      - 比特序列是1D的，展开到3D网格中
      - 1 → 正扰动 (+1)
      - 0 → 负扰动 (-1)
    
    映射方式：比特按顺序填入3D网格
      bit_index → (x, y, z)
      x = bit_index % grid_size
      y = (bit_index // grid_size) % grid_size  
      z = (bit_index // grid_size // grid_size) % grid_size
    
    多个比特落在同一个格点上时累加。
    """
    bits = text_to_bits(text)
    n_bits = len(bits)
    S = np.zeros((grid_size, grid_size, grid_size))
    
    total_cells = grid_size ** 3  # 32768
    
    for i, bit in enumerate(bits):
        # 1D → 3D 坐标
        idx = i % total_cells
        x = idx % grid_size
        y = (idx // grid_size) % grid_size
        z = (idx // (grid_size * grid_size)) % grid_size
        
        # 1 → +1, 0 → -1
        S[x, y, z] += (2 * bit - 1)  # 映射 {0,1} → {-1,+1}
    
    # 加高斯平滑（让扰动不是单个格点，有空间范围）
    from scipy.ndimage import gaussian_filter
    S = gaussian_filter(S, sigma=1.0)
    
    # 归一化到 [-1, 1]
    mx = max(abs(S.max()), abs(S.min()))
    if mx > 0:
        S = S / mx
    
    return S
```

## 验证：不同文本的源场一定不同

```python
texts = {
    "criminal": "故意伤害",
    "labor": "解除劳动合同",
    "divorce": "离婚后财产分割",
    "criminal_heavy": "故意伤害致人重伤",
    "traffic": "交通事故责任认定",
}

# 先验证比特序列不同
for name, text in texts.items():
    bits = text_to_bits(text)
    print(f"{name}: {len(bits)} bits, first 24: {''.join(map(str, bits[:24]))}")

# 源场相关度
for name_a, text_a in texts.items():
    S_a = build_source_binary(text_a)
    for name_b, text_b in texts.items():
        if name_a >= name_b:
            continue
        S_b = build_source_binary(text_b)
        corr = np.corrcoef(S_a.flatten(), S_b.flatten())[0, 1]
        print(f"{name_a} vs {name_b}: corr={corr:.4f}")
```

**预期**：
- 所有对的corr远小于1.0（每个文本的比特序列唯一）
- "故意伤害" vs "故意伤害致人重伤" 的corr应该最高（共享前缀"故意伤害"的比特）
- 不同领域的corr应该较低

## 为什么比特比笔画好

| 属性 | 笔画+Unicode | 比特 |
|---|---|---|
| 唯一性 | 不保证（同笔画数的字位置相同） | **绝对唯一** |
| 物质层级 | 中间层（人对字形的抽象） | **最底层（硬件状态）** |
| 通用性 | 只对中文有效 | **任何语言、任何文件** |
| 映射规则 | 需要笔画表（外部知识） | **零外部知识（直接读字节）** |
| 和双井势对应 | 无直接对应 | **0=-1, 1=+1（完美对应）** |

## 重跑实验

用比特源场替换笔画源场，重跑：

### 任务1：源场区分度验证
对5个文本，计算两两corr。确认corr < 1.0。

### 任务2：实验D扩大版
用昨晚的10对query-doc（exp004_overnight.md中的test_pairs），改用比特源场：
1. 每个文本 → 比特序列 → 3D源场
2. Allen-Cahn演化���稳态
3. 迭代融合
4. 记录match能量 vs mismatch能量

### 任务3：实验C（量变/质变）
用昨晚的完整句子，改用比特源场。

### 任务4：比特级信息量分析
额外分析：
```python
# 不同文本的比特0/1比例
for name, text in texts.items():
    bits = text_to_bits(text)
    ratio = sum(bits) / len(bits)
    print(f"{name}: {len(bits)} bits, 1-ratio={ratio:.3f}")
```

看不同文本的比特统计是否有区别。

---

## 关键：不改方程

Allen-Cahn方程不变：
```
∂u/∂t = D∇²u - u³ + u + (1-3u²)·S
```

只改S的构建方式：从笔��+码点 → 比特序列。

D=0.1（已验证），dt=0.1，网格32³。

---

## 公理检查

- [ ] 比特是物质属性？→ 是，硬件上的电压高低 ✓
- [ ] 不用统计/embedding？→ 不用，直接读字节 ✓
- [ ] 不用外部知识？→ 不用，连笔画表都不需要了 ✓
- [ ] 确定性？→ UTF-8编码是确定性的 ✓
- [ ] 通用？→ 任何语言任何文件 ✓
- [ ] 和双井势对应？→ 0=-1, 1=+1 完美对应 ✓

---

*Win端 Claude, 2026-04-10*
*"物质的最底层存在。"*
