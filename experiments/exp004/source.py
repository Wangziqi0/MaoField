"""
MaoField Exp004: Character-Level Physical Property Source Field
================================================================

Each CHARACTER (not word) gets a unique 3D position from:
  x = position in sequence (word order)
  y = stroke count (physical structure of the glyph)
  z = Unicode code point mod grid_size (character identity)

No embeddings. No statistics. Pure physical properties of text.
"""

import numpy as np
from config import GRID_SIZE

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
    '赔': 12, '法': 8, '条': 7, '款': 12,
    '盗': 11, '窃': 9, '抢': 7, '劫': 7, '诈': 7, '骗': 12,
    '醉': 15, '驾': 15, '驶': 8, '机': 6, '酒': 10,
    '未': 5, '成': 6,
    '工': 3, '资': 10, '加': 5, '班': 10, '费': 9,
    '押': 8, '金': 8, '退': 9, '租': 10,
    '遗': 12, '继': 10, '承': 8,
    '约': 6, '违': 7,
    '诉': 7, '讼': 6, '申': 5,
    '复': 9, '议': 5,
    '拘': 8, '留': 10, '行': 6, '政': 9,
}


def get_stroke(char):
    if char in STROKE_COUNT:
        return STROKE_COUNT[char]
    return (ord(char) * 7 + 3) % 25 + 1


def build_source_physical(text, grid_size=GRID_SIZE, sigma=1.5):
    """
    Character-level physical property source field.

    Each CJK character → 3D position:
      x = position in sequence
      y = stroke count % grid_size
      z = ord(char) % grid_size
    """
    S = np.zeros((grid_size, grid_size, grid_size))

    chars = [c for c in text if '\u4e00' <= c <= '\u9fff']
    n = len(chars)
    if n == 0:
        return S

    radius = int(sigma * 2.5)

    for i, char in enumerate(chars):
        px = int(i / max(n - 1, 1) * (grid_size - 1))
        py = get_stroke(char) % grid_size
        pz = ord(char) % grid_size

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    ix = (px + dx) % grid_size
                    iy = (py + dy) % grid_size
                    iz = (pz + dz) % grid_size
                    dist2 = dx * dx + dy * dy + dz * dz
                    S[ix, iy, iz] += np.exp(-dist2 / (2 * sigma * sigma))

    mx = S.max()
    if mx > 0:
        S = S / mx

    return S


# Convenience: text dict for experiments (now plain strings, char-level)
TEXTS = {
    "criminal": "故意伤害他人身体",
    "labor": "解除劳动合同赔偿",
    "divorce": "离婚后财产分割",
    "criminal_heavy": "故意伤害他人身体致人重伤",
    "traffic": "交通事故责任认定",
}

QUERY_TEXTS = {
    "query_hit": "他打我怎么判",
    "doc_match": "故意伤害他人身体处三年以下",
    "doc_mismatch": "解除劳动合同经济补偿",
}

EXP_C = {
    "base": "离婚",
    "quant": "离婚后房子怎么分",
    "qual": "离婚他打我",
}

EXP_E = {
    "criminal_1": "故意伤害他人身体",
    "criminal_2": "故意杀人",
    "labor_1": "劳动合同经济补偿",
}
