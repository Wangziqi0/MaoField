"""
MaoField Exp004: Token → 3D Space Injection
=============================================

Maps text tokens to 3D spatial perturbations.
Uses ONLY physical text structure (word order, char count, sentence boundary).
NO embeddings. NO statistics.

Position mapping:
  x = token position in sentence (sequence order)
  y = sentence index
  z = character count of token (complexity)

Each token injects:
  - Gaussian perturbation to u and v fields
  - Local modification of F and k parameters
"""

import numpy as np
import re
from config import *


def tokenize_simple(text):
    """
    Simple Chinese tokenization based on physical structure.
    Split by punctuation and spaces. Each segment = one token.
    No NLP library needed — just physical text boundaries.
    """
    # Split by Chinese/English punctuation and spaces
    segments = re.split(r'[，。；：！？、\s,.:;!?\n]+', text)
    tokens = [s.strip() for s in segments if s.strip()]
    return tokens


def text_to_sentences(text):
    """Split text into sentences based on physical punctuation"""
    sentences = re.split(r'[。！？\n]+', text)
    return [s.strip() for s in sentences if s.strip()]


def compute_token_positions(text, grid_size=GRID_SIZE):
    """
    Map tokens to 3D grid positions based on physical text structure.
    Returns: list of (token_text, x, y, z) tuples
    """
    sentences = text_to_sentences(text)
    if not sentences:
        sentences = [text]

    positions = []
    for sent_idx, sentence in enumerate(sentences):
        tokens = tokenize_simple(sentence)
        n_tokens = len(tokens)

        for tok_idx, token in enumerate(tokens):
            # x = position in sentence (0 to grid_size-1)
            x = int(tok_idx / max(n_tokens - 1, 1) * (grid_size - 1))

            # y = sentence index (0 to grid_size-1)
            y = int(sent_idx / max(len(sentences) - 1, 1) * (grid_size - 1))
            if len(sentences) == 1:
                y = grid_size // 2  # center if single sentence

            # z = character count (complexity), normalized
            char_count = len(token)
            max_chars = 10  # normalize: 10+ chars → max z
            z = int(min(char_count / max_chars, 1.0) * (grid_size - 1))

            # Clamp to grid bounds
            x = min(max(x, 0), grid_size - 1)
            y = min(max(y, 0), grid_size - 1)
            z = min(max(z, 0), grid_size - 1)

            positions.append((token, x, y, z))

    return positions


def inject_tokens(sim, text, amplitude=INJECT_AMPLITUDE, sigma=INJECT_SIGMA,
                  radius=INJECT_RADIUS, delta_f=DELTA_F, delta_k=DELTA_K):
    """
    Inject token perturbations into the 3D reaction-diffusion simulator.

    Each token:
    1. Creates a Gaussian perturbation at its mapped position
    2. u gets positive perturbation (activate)
    3. v gets negative perturbation (destabilize → trigger pattern formation)
    4. F and k locally modified (change reaction environment)
    """
    positions = compute_token_positions(text, sim.N)

    for token, px, py, pz in positions:
        # Create Gaussian perturbation in neighborhood
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    # Periodic boundary
                    ix = (px + dx) % sim.N
                    iy = (py + dy) % sim.N
                    iz = (pz + dz) % sim.N

                    dist_sq = dx*dx + dy*dy + dz*dz
                    gauss = amplitude * np.exp(-dist_sq / (2 * sigma * sigma))

                    # Inject: u positive, v also positive (seed pattern)
                    sim.u[ix, iy, iz] = min(sim.u[ix, iy, iz] - gauss * 0.5, 1.0)
                    sim.v[ix, iy, iz] = min(sim.v[ix, iy, iz] + gauss, 1.0)

                    # Locally modify F and k
                    sim.F[ix, iy, iz] += delta_f * gauss
                    sim.k[ix, iy, iz] += delta_k * gauss

    return positions


if __name__ == "__main__":
    print("Testing token injection...")

    test_texts = [
        "故意伤害他人身体",
        "解除劳动合同赔偿",
        "离婚后财产分割",
        "故意伤害他人身体致人重伤",
        "交通事故责任认定",
    ]

    for text in test_texts:
        positions = compute_token_positions(text)
        print(f"\n'{text}':")
        for token, x, y, z in positions:
            print(f"  '{token}' → ({x}, {y}, {z})")
