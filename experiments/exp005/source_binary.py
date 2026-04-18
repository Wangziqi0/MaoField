"""
MaoField Exp005: Binary Source Field
=====================================
Text → UTF-8 bytes → bit sequence → 3D source field.
Reused from exp004.
"""

import numpy as np
from scipy.ndimage import gaussian_filter


def text_to_bits(text):
    """Text → bit sequence (UTF-8)."""
    raw = text.encode('utf-8')
    bits = []
    for byte in raw:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def build_source_binary(text, grid_size=32, sigma=1.0):
    """Bit-level source field. Each bit → one grid point: 1→+1, 0→-1."""
    bits = text_to_bits(text)
    S = np.zeros((grid_size, grid_size, grid_size))
    total_cells = grid_size ** 3

    for i, bit in enumerate(bits):
        idx = i % total_cells
        x = idx % grid_size
        y = (idx // grid_size) % grid_size
        z = (idx // (grid_size * grid_size)) % grid_size
        S[x, y, z] += (2 * bit - 1)

    S = gaussian_filter(S, sigma=sigma)
    mx = max(abs(S.max()), abs(S.min()))
    if mx > 0:
        S = S / mx
    return S
