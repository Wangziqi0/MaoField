"""
MaoField Exp006: Multi-Component Binary Source Field
=====================================================

Text -> UTF-8 bits -> split across n_components source fields.
  2 components: odd/even bits
  3 components: i%3 == 0/1/2
"""

import numpy as np
from scipy.ndimage import gaussian_filter


def text_to_bits(text):
    """Text -> bit sequence (UTF-8)."""
    raw = text.encode('utf-8')
    bits = []
    for byte in raw:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def build_source_single(bits, grid_size=32, sigma=1.0):
    """Bit list -> single 3D source field."""
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


def build_source_binary(text, grid_size=32, sigma=1.0):
    """Single-component source field (backward compat with exp005)."""
    bits = text_to_bits(text)
    return build_source_single(bits, grid_size, sigma)


def build_source_mc(text, n_components, grid_size=32, sigma=1.0):
    """Multi-component source fields by splitting bits across components.

    n_components=1: all bits -> S[0]
    n_components=2: odd bits -> S[0], even bits -> S[1]
    n_components=3: i%3==0 -> S[0], i%3==1 -> S[1], i%3==2 -> S[2]
    """
    bits = text_to_bits(text)

    if n_components == 1:
        return [build_source_single(bits, grid_size, sigma)]

    # Split bits by component
    bit_groups = [[] for _ in range(n_components)]
    for i, bit in enumerate(bits):
        bit_groups[i % n_components].append(bit)

    return [build_source_single(bg, grid_size, sigma) for bg in bit_groups]
