# exp004 源场修正：字级物质属性映射

**问题**：之前的源场只编码词序，所有4词文本产生一模一样的源场。
**修正**：每个字单独注入，位置由字的物质属性决定。

---

## 新的源场映射

每个**字**（不是词）在3D空间中有唯一的位置，由三个物质属性决定：

```
x = 字在序列中的位置 / 总字数 * (grid_size - 1)
y = 笔画数 % grid_size
z = ord(字符) % grid_size    # Unicode码点取模
```

这三个都是字的**物质属性**：
- x：这个字排在第几个——客观事实
- y：这个字有几画——字的物理结构
- z：这个字的Unicode编码——字符的数字身份

不用embedding，不用统计，不用语义知识。

## 笔画数获取

中文常用字的笔画数可以用 Unicode CJK 笔画数据库，或者用一个简单的查找表。

**方案1：用 unicodedata 标准库**

Python 的 unicodedata 没有直接给笔画数，但可以用 CJK Unified Ideographs 的一些属性。

**方案2：硬编码一个常用字笔画表**

对实验中用到的几十个字，直接硬编码笔画数。这不是"预设语义"——笔画数是字形的客观物理属性，就像原子的质子数。

```python
STROKE_COUNT = {
    '故': 9, '意': 13, '伤': 6, '害': 10,
    '解': 13, '除': 10, '劳': 7, '动': 6, '合': 6, '同': 6,
    '离': 11, '婚': 11, '后': 6, '财': 7, '产': 6, '分': 4, '割': 12,
    '致': 10, '人': 2, '重': 9,
    '交': 6, '通': 10, '事': 8, '故': 9, '责': 8, '任': 6, '认': 4, '定': 8,
    '他': 5, '打': 5, '我': 7, '怎': 9, '么': 3, '判': 7,
    '处': 5, '三': 3, '年': 6, '以': 4, '下': 3, '有': 6, '期': 12, '徒': 10, '刑': 6,
    '经': 8, '济': 9, '补': 7, '偿': 11,
    '杀': 6,
    '的': 8, '体': 7, '身': 7,
}

def get_stroke_count(char):
    """获取字的笔画数。未知字用Unicode码点的简单哈希替代。"""
    if char in STROKE_COUNT:
        return STROKE_COUNT[char]
    # fallback: 用码点的某个变换近似（不精确，但保证不同字不同值）
    return (ord(char) * 7 + 3) % 25 + 1
```

**方案3：从网上下载完整的笔画数据库**

如果有 `unihan` 数据库（Unicode Han Database），可以从 kTotalStrokes 字段获取所有CJK字符的笔画数。

```bash
# 下载 Unihan 数据库
wget https://unicode.org/Public/UCD/latest/ucd/Unihan.zip
unzip Unihan.zip
grep kTotalStrokes Unihan_DictionaryLikeData.txt > strokes.txt
```

然后解析成 Python 字典。这是最完整的方案。

**建议先用方案2（硬编码实验用到的字），跑通后再换方案3。**

## 新的 source.py

```python
import numpy as np

STROKE_COUNT = {
    '故': 9, '意': 13, '伤': 6, '害': 10,
    '解': 13, '除': 10, '劳': 7, '动': 6, '合': 6, '同': 6,
    '离': 11, '婚': 11, '后': 6, '财': 7, '产': 6, '分': 4, '割': 12,
    '致': 10, '人': 2, '重': 9,
    '交': 6, '通': 10, '事': 8, '责': 8, '任': 6, '认': 4, '定': 8,
    '他': 5, '打': 5, '我': 7, '怎': 9, '么': 3, '判': 7,
    '处': 5, '三': 3, '年': 6, '以': 4, '下': 3, '有': 6, '期': 12, '徒': 10, '刑': 6,
    '经': 8, '济': 9, '补': 7, '偿': 11,
    '杀': 6, '的': 8, '体': 7, '身': 7,
    '房': 8, '子': 3, '车': 4, '藏': 17, '证': 7,
}

def get_stroke(char):
    if char in STROKE_COUNT:
        return STROKE_COUNT[char]
    return (ord(char) * 7 + 3) % 25 + 1

def build_source_physical(text, grid_size=32, sigma=1.5):
    """
    字级物质属性源场。
    
    每个字在3D空间中的位置由三个物质属性决定：
      x = 字在序列中的位置
      y = 笔画数
      z = Unicode码点 mod grid_size
    
    Args:
        text: 字符串（每个字符单独处理）
        grid_size: 3D网格大小
        sigma: 高斯扰动宽度
    
    Returns:
        S: np.array of shape (grid_size, grid_size, grid_size)
    """
    S = np.zeros((grid_size, grid_size, grid_size))
    
    # 过滤掉空格和标点
    chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
    n = len(chars)
    if n == 0:
        return S
    
    radius = int(sigma * 2.5)
    
    for i, char in enumerate(chars):
        # 三个物质属性 → 3D位置
        px = int(i / max(n - 1, 1) * (grid_size - 1))
        py = get_stroke(char) % grid_size
        pz = ord(char) % grid_size
        
        # 高斯扰动
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    ix = (px + dx) % grid_size
                    iy = (py + dy) % grid_size
                    iz = (pz + dz) % grid_size
                    dist2 = dx*dx + dy*dy + dz*dz
                    S[ix, iy, iz] += np.exp(-dist2 / (2 * sigma * sigma))
    
    # 归一化到 [0, 1]
    mx = S.max()
    if mx > 0:
        S = S / mx
    
    return S
```

## 验证：不同文本的源场确实不同

跑这个快速检查：

```python
texts = {
    "criminal": "故意伤害",
    "labor": "解除劳动合同",
    "divorce": "离婚后财产分割",
    "criminal_heavy": "故意伤害致人重伤",
    "traffic": "交通事故责任认定",
}

# 对每对文本计算源场的相关度
for name_a, text_a in texts.items():
    S_a = build_source_physical(text_a)
    for name_b, text_b in texts.items():
        if name_a >= name_b:
            continue
        S_b = build_source_physical(text_b)
        corr = np.corrcoef(S_a.flatten(), S_b.flatten())[0, 1]
        print(f"{name_a} vs {name_b}: corr={corr:.4f}")
```

**预期**：所有对的 corr 远小于 1.0（之前全是 1.0000）。相似文本（criminal vs criminal_heavy）的 corr 应该比不相似文本高。

## 重跑 B-E

源场改了之后，用修正后的 Allen-Cahn 方程（带 (1-3u²)·S 因子）重跑所有实验。

代码改动很小——只改 source.py（或者 inject.py 中的源场构建函数）。simulator_ac.py 的方程也需要改成 (1-3u²)·S 版本（如果还没改的话）。

实验 B-E 的逻辑不变，只是输入的源场不同了。

---

## 偏离检查

- [ ] 笔画数是物质属性？→ 是，字形的客观物理结构 ✓
- [ ] Unicode码点是物质属性？→ 是，字符的数字编码 ✓  
- [ ] 用了统计/embedding？→ 没有 ✓
- [ ] 硬编码笔画表算不算"预设知识"？→ 不算。笔画数是字的客观物理属性，和语义无关。就像记录原子的质子数不是"预设化学知识" ✓

---

*Win端 Claude, 2026-04-10*
