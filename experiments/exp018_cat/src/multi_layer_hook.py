"""
multi_layer_hook.py — Candidate C (D22) multi-layer 4 axis instrument

D-3 反映论 instantiate: cross-layer dialectical interconnection 之 multi-channel
binary evidence accumulation. OPT-125m 12 layer × {A2 anisotropy, A3 attention 头
熵, A6 EMA divergence}, A1 PPL 之 global per-gen (paper v8 baseline reuse).

binding (Agent 4 catch + EXP_LAUNCH_PLAN_PATH_AC_D22 §1.3):
- A1 PPL 漂移: global per-gen, paper v8 reuse, +0% wall-clock
- A2 嵌入各向异性: per layer hidden_state cosine sim isotropy (Mu-Viswanath 2018 +
  Ethayarajh 2019 form), 12 layer, +5%
- A3 attention 头熵: per (layer, head) attention pattern Shannon 熵 (Voita 2019),
  12 × 12 = 144, +8%, 需 attn_implementation="eager"
- A6 每层 EMA 散度: per layer 之 EMA state vs current weight 之 L2 distance,
  12 layer, +3%

D-1 + D-3 严守:
- 仅 raw 数字 output, 不 declare Pearson r strong / weak / paradigm shift
- 不 reify "证明 dialectical totality framing correct", evidence accumulation
- 占位符禁令: 任何 fail 之 axis = None (jsonl), 不 best-case inflate
"""
from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger(__name__)


# ============================================================
# A2 嵌入各向异性 (per layer)
# ============================================================

@torch.no_grad()
def compute_a2_isotropy(hidden_states_per_layer: tuple[torch.Tensor, ...]) -> list[float]:
    """
    per layer hidden_states 之 cosine sim ISOTROPY score.

    ⚠️ ERRATA (D606 2026-06-06): 旧名 compute_a2_anisotropy + 旧 key
    a2_anisotropy_per_layer = MISLABEL. 实算一直是 isotropy (1−|mean_cos|,
    higher=less collapse, 见下). D25 SMOKE_E0 md 据旧名把"值↑"读成"anisotropy↑=
    collapse"方向反 (已 errata). 改名 isotropy; 旧 key 留 deprecated alias 兼容旧 trace.
    复跑实证: canonical/wip/maofield_e0_isotropy_rerun_20260606/.

    Ref: Mu & Viswanath 2018 (All-but-the-Top), Ethayarajh 2019 (How Contextual
    are Contextualized Word Representations). isotropy = 1 - mean(|cos sim|) of
    pairs of token vectors in batch. high isotropy = 各 token 之间 less correlated
    (random direction-ish), low isotropy = collapse 之 anisotropic signature.

    实际 implement: per layer per batch sample 之 mean pairwise cos sim 之 |.|
    再 1 - 之 (=isotropy score). higher=less collapse, lower=more collapse.

    Args:
        hidden_states_per_layer: HF output_hidden_states=True 之 tuple, len=L+1
          (含 embedding layer 0 + 12 transformer layers, 共 13). 取后 12 layer
          (skip layer 0 = embedding pre-transformer).

    Returns:
        list[float] 之 len=12 (OPT-125m 之 12 transformer layer 之 isotropy score).
    """
    isotropies: list[float] = []
    # 取 transformer layers, skip embedding (idx 0)
    transformer_layers = hidden_states_per_layer[1:]  # len = 12 for OPT-125m
    for layer_h in transformer_layers:
        # layer_h shape: [B, T, H]
        B, T, H = layer_h.shape
        # flatten 到 [B*T, H], 之 token 之 representation
        flat = layer_h.reshape(B * T, H)
        # normalize (L2)
        norms = flat.norm(dim=-1, keepdim=True).clamp_min(1e-12)
        flat_n = flat / norms
        # 之 sample-level mean pairwise cos sim (避 [B*T, B*T] matrix OOM):
        # 等价 ‖mean(flat_n)‖² 之公式: mean_pairwise_cos = (1/N²) sum_{i,j} <v_i, v_j>
        # = ‖(1/N) Σ v_i‖². 之 unbiased estimator.
        mean_vec = flat_n.mean(dim=0)  # [H]
        mean_pairwise_cos = float((mean_vec @ mean_vec).item())  # scalar
        # isotropy score (higher = less anisotropic = less collapse)
        isotropy = 1.0 - abs(mean_pairwise_cos)
        if not math.isfinite(isotropy):
            isotropy = float("nan")
        isotropies.append(isotropy)
    return isotropies


# ============================================================
# A3 attention 头熵 (per layer × per head)
# ============================================================

@torch.no_grad()
def compute_a3_attention_entropy(
    attentions_per_layer: tuple[torch.Tensor, ...],
    attention_mask: Optional[torch.Tensor] = None,
) -> list[list[float]]:
    """
    per (layer, head) attention pattern 之 Shannon 熵.

    Ref: Voita 2019 (Analyzing Multi-Head Self-Attention). attention 之 query
    position 之 over key positions distribution 之 entropy. high entropy = uniform
    diffuse attention. low entropy = concentrated 在少 token (collapse 之 信号).

    Args:
        attentions_per_layer: HF output_attentions=True 之 tuple, len=L (12 layer
          for OPT-125m). 每 layer 之 tensor shape: [B, H_heads, T, T].
        attention_mask: optional [B, T], 1=valid, 0=pad. 之 used 之 average 之
          query positions 之 valid mask.

    Returns:
        list[list[float]] shape (12 layer, 12 head) 之 mean attention entropy
        (across batch + query positions).
    """
    out: list[list[float]] = []
    for layer_attn in attentions_per_layer:
        # layer_attn shape: [B, H_heads, T_q, T_k]
        B, H, Tq, Tk = layer_attn.shape
        # entropy over key dim: H(p) = -Σ p log p
        # p = layer_attn (已 softmax-ed by transformer)
        log_p = torch.log(layer_attn.clamp_min(1e-12))
        entropy_per_q = -(layer_attn * log_p).sum(dim=-1)  # [B, H, T_q]
        # mask 之 query positions
        if attention_mask is not None:
            mask_q = attention_mask.float()  # [B, T_q]
            mask_q = mask_q.unsqueeze(1)  # [B, 1, T_q] broadcast over H
            entropy_per_q = entropy_per_q * mask_q
            denom = mask_q.sum(dim=(0, 2)).clamp_min(1.0)  # [1] → broadcast to [H]
            mean_per_head = entropy_per_q.sum(dim=(0, 2)) / denom  # [H]
        else:
            mean_per_head = entropy_per_q.mean(dim=(0, 2))  # [H]
        head_entropies: list[float] = []
        for h_idx in range(H):
            val = float(mean_per_head[h_idx].item())
            if not math.isfinite(val):
                val = float("nan")
            head_entropies.append(val)
        out.append(head_entropies)
    return out


# ============================================================
# A6 每层 EMA 散度 (per layer L2)
# ============================================================

@torch.no_grad()
def compute_a6_ema_divergence(
    model: nn.Module,
    ema_model: nn.Module,
) -> list[float]:
    """
    per layer 之 EMA state vs current weight 之 L2 distance.

    Ref: paper v8 §3.5 之 D^code (global EMA divergence) expand to per-layer.
    OPT-125m 之 12 transformer layer 之 param 累计 L2 norm.

    Args:
        model: current 之 main model
        ema_model: EMA model (KLContradictionTracker.ema_model)

    Returns:
        list[float] 之 len=12 (12 transformer layer 之 per-layer L2 distance).
    """
    if ema_model is None:
        return [float("nan")] * 12
    # OPT model 之 transformer layers 在 model.model.decoder.layers
    # (HF OPT structure: OPTForCausalLM → OPTModel (model) → OPTDecoder (decoder) →
    #  layers (ModuleList of OPTDecoderLayer, len=12 for OPT-125m))
    try:
        cur_layers = model.model.decoder.layers
        ema_layers = ema_model.model.decoder.layers
    except AttributeError:
        # fallback: 之 OPT 不同 version, 之 找
        cur_layers = None
        ema_layers = None
        for name, mod in model.named_modules():
            if name.endswith(".layers") and isinstance(mod, nn.ModuleList):
                cur_layers = mod
                break
        for name, mod in ema_model.named_modules():
            if name.endswith(".layers") and isinstance(mod, nn.ModuleList):
                ema_layers = mod
                break
    if cur_layers is None or ema_layers is None:
        logger.warning("a6_ema_divergence: 之 找 transformer layers fail, return NaN list")
        return [float("nan")] * 12
    if len(cur_layers) != len(ema_layers):
        logger.warning(
            "a6_ema_divergence: layer count mismatch cur=%d ema=%d",
            len(cur_layers), len(ema_layers)
        )
        return [float("nan")] * 12
    L2_per_layer: list[float] = []
    for layer_idx in range(len(cur_layers)):
        cur_layer = cur_layers[layer_idx]
        ema_layer = ema_layers[layer_idx]
        sq_sum = 0.0
        cur_params = dict(cur_layer.named_parameters())
        ema_params = dict(ema_layer.named_parameters())
        for pname in cur_params:
            if pname not in ema_params:
                continue
            cur_p = cur_params[pname].data
            ema_p = ema_params[pname].data
            if cur_p.shape != ema_p.shape:
                continue
            diff = cur_p - ema_p
            sq_sum += float((diff ** 2).sum().item())
        L2 = math.sqrt(sq_sum) if sq_sum >= 0 else float("nan")
        if not math.isfinite(L2):
            L2 = float("nan")
        L2_per_layer.append(L2)
    return L2_per_layer


# ============================================================
# MultiLayerHook 类 — 整合 4 axis 之 forward capture
# ============================================================

@dataclass
class MultiLayerHookConfig:
    """multi-layer hook 配置."""
    val_subset_size: int = 256
    val_max_length: int = 64
    batch_size: int = 8
    device: str = "cuda"


class MultiLayerHook:
    """
    Candidate C multi-layer 4 axis instrument.

    per chain training run 之 per generation 末尾调 capture_per_gen,
    forward val subset 256 句 之 model + ema_model, 提取:
    - A2 anisotropy: 12 layer 之 isotropy score
    - A3 attention 头熵: 12 layer × 12 head = 144 之 entropy
    - A6 EMA L2 散度: 12 layer 之 L2 distance

    A1 PPL 漂移 之 global per-gen 由 caller (candidate_c_runner.py 之 compute
    test_ppl_dict) 处理, 之 hook 不 capture A1 (避 redundant).
    """

    def __init__(self, config: MultiLayerHookConfig | None = None):
        self.cfg = config if config is not None else MultiLayerHookConfig()
        logger.info(
            "MultiLayerHook init: val_subset_size=%d val_max_length=%d batch_size=%d device=%s",
            self.cfg.val_subset_size, self.cfg.val_max_length,
            self.cfg.batch_size, self.cfg.device
        )

    @torch.no_grad()
    def capture_per_gen(
        self,
        model: nn.Module,
        ema_model: nn.Module | None,
        val_input_ids: torch.Tensor,
        val_attention_mask: torch.Tensor,
    ) -> dict:
        """
        per generation 末尾 capture 4 axis 之 raw 数字 (A2 / A3 / A6).

        Args:
            model: current 之 fine-tuned model (this generation done)
            ema_model: EMA model (可能 None, gen 0 没 EMA → A6 之 fallback to NaN)
            val_input_ids: [B, T] val subset 之 token ids
            val_attention_mask: [B, T] val subset 之 mask

        Returns:
            dict with keys:
              - "a2_isotropy_per_layer": list[float] len=12 (实为 isotropy, higher=less collapse)
              - "a2_anisotropy_per_layer": list[float] len=12 (DEPRECATED alias=isotropy, 勿据名读方向)
              - "a3_attn_entropy_per_layer_head": list[list[float]] shape (12, 12)
              - "a6_ema_l2_per_layer": list[float] len=12
        """
        model.eval()
        # forward 之 output_hidden_states + output_attentions
        out = model(
            input_ids=val_input_ids.to(self.cfg.device),
            attention_mask=val_attention_mask.to(self.cfg.device),
            output_hidden_states=True,
            output_attentions=True,
            return_dict=True,
        )

        # A2 isotropy (旧名 anisotropy = mislabel, 见 compute_a2_isotropy ERRATA)
        a2 = compute_a2_isotropy(out.hidden_states)

        # A3 attention 头熵
        a3 = compute_a3_attention_entropy(
            out.attentions,
            attention_mask=val_attention_mask.to(self.cfg.device),
        )

        # A6 EMA L2
        a6 = compute_a6_ema_divergence(model, ema_model)

        result = {
            "a2_isotropy_per_layer": a2,  # ERRATA(D606): 实为 isotropy(higher=less collapse)
            "a2_anisotropy_per_layer": a2,  # DEPRECATED alias(=isotropy, 勿据名读方向; 兼容旧 trace)
            "a3_attn_entropy_per_layer_head": a3,
            "a6_ema_l2_per_layer": a6,
        }
        return result
