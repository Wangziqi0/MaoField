"""
exploration_d17_power_law_loss.py — D-2 代码线 third wave (D17 = 2026-05-17)

throwaway exploration prototype 不是 production code。
N=1 gen 1 seed sanity check, 不 statistical conclude / 不 declare framework α-effect。

scope (binary)
--------------
- 复用 v1.0 release `archive/v1.0_release_20260516/src/contradiction_loss.py` 之 EMA-deviation 实际 form 作为 baseline reference
- 新 alternative form: **power-law decay** $\\bar{D}_n^{\\rm power-law} = \\sum_{k=1}^{K} k^{-\\alpha} D_{n-k} / Z$
  其中 $Z = \\sum_{k=1}^{K} k^{-\\alpha}$ (normalize), $\\alpha = 1.0$ (Zipf-like exponent), $K = 5$ (truncation)
  注: power-law $\\sum k^{-\\alpha}$ 在 $\\alpha \\le 1$ 时 diverge, 必须 truncate K
- T3_memory_powerlaw = $(D_n - \\bar{D}_n^{\\rm power-law})^2$
  其余 (T1_velocity / T2_replace) 与 EMA-deviation form 完全一致 (binary: 只改 T3 memory 项, 隔离 alternative form 之 single-axis 影响)
- chain 实际只跑 1 gen, $K=5$ history buffer 在 gen 0 是 vacuous (no prior gens)
  这是 sanity check scope 之 known limit, 标 [?]

数学线 outline ref [?]
---------------------
- 数学线 D17 third wave outline (file `MATH_LINE_D17_THIRD_WAVE_THREE_QUESTIONS_OUTLINE_20260517.md`) 在本 script
  落地时尚未 surface 到 literature/, 实现根据 prompt outline alternative form candidate (power-law decay)
  之 minimal sketch
- paper v8 §3.6 mean-field NESS analysis 之 long-tail memory kernel discussion 对应 power-law decay
  $k^{-\\alpha}$ form (相对 EMA $\\beta^k$ 之 exponential decay)
- 数学线 outline release 后 cross-check 此 sketch 是否 form-consistent — 不强制 backport, 保留 throwaway

binding
-------
- 不 modify v1.0 release archive 任何文件 (manifest 47/47 ✓)
- 不写 unit test / 不写 documentation / 不写 production checklist — throwaway exploration only
- 1 gen 1 seed = N=1 sanity check, **不**是 verification

文献参考 (paper v8 §3 / §3.6 / §3.2 P0-1 honest disclose)
------
- paper v8 §3.2 P0-1 EMA-deviation form 与 paper §3.5 Volterra 借用 form 不一致 (D-1 纪律 3 binding)
- power-law $k^{-\\alpha}$ 与 Volterra $\\chi(k) = \\exp(-m_{\\rm eff} k)$ EMA kernel 是
  two distinct memory kernel families, alternative form sketch 是 third wave 之 sanity check sketch
- 反题 v8 P0★-A linearization gap (EMA-deviation 之 Taylor 展开 leading order 与 paper §3.2
  Klein-Gordon mass term 之 form-borrowing claim 之 partial gap) — power-law alternative form
  之 leading-order linearization 在 prototype scope 外, 留 D60+ substantive paired comparison
"""
from __future__ import annotations

import copy
import logging
import math
from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger(__name__)


# ============================================================
# Power-law alternative form configuration
# ============================================================

@dataclass
class PowerLawContradictionConfig:
    """
    Power-law alternative form 超参 (exploration prototype, throwaway).

    与 v1.0 release `KLContradictionConfig` 之 EMA-deviation form 之差异 (binary):
    - memory_form: "ema" (v1.0 release default) / "power_law" (本 script 新加 alternative)
    - power_law_alpha: $\\alpha$ Zipf exponent (1.0 = harmonic, 2.0 = quadratic decay)
    - power_law_K: truncation horizon (history buffer size)

    保留 v1.0 release 全部其他 hyperparam (lambda_i / beta_model / kl_update_every / T_2_form),
    binary 锁定 only T3_memory 项之 form 改变, 隔离 alternative form 之 single-axis 影响。
    """
    # KL 度量 (v1.0 release inherit)
    kl_direction: str = "q_to_p"
    val_subset_size: int = 256
    val_max_length: int = 64

    # EMA model (v1.0 release inherit — 即使 memory_form="power_law", D̄^EMA reservoir
    # 仍维护用作 logging baseline + tracker.D_ema 之 placeholder)
    beta_model: float = 0.999

    # ℒ_contradiction 三项权重 (v1.0 release inherit, λ=1.0 旧 framework)
    lambda_1: float = 1.0    # velocity (ΔD_n)²
    lambda_2: float = 1.0    # memory (D_n - bar_D)² — bar_D form 由 memory_form 控
    lambda_3: float = 1.0    # T₂ replace

    # update 频次
    kl_update_every: int = 10

    # T₂ form (v1.0 release inherit)
    T_2_form: str = "relu_dpp"      # 与 v1.0 release cat_arm_b.yaml chain 实跑 form 一致

    # ============================================================
    # power-law alternative form 新加参数
    # ============================================================
    memory_form: str = "power_law"   # "ema" (v1.0 release) / "power_law" (alternative)
    power_law_alpha: float = 1.0     # Zipf exponent
    power_law_K: int = 5             # truncation horizon (history buffer size)

    # EMA kernel reference (memory_form="ema" 时用, "power_law" 时 ignore)
    beta_kl: float = 0.9             # v1.0 release旧 framework default


class PowerLawContradictionTracker:
    """
    Power-law alternative form tracker。

    与 v1.0 release `KLContradictionTracker` 之差异 (binary):
    - 新增 `_compute_powerlaw_bar_D()` 方法 returning $\\bar{D}_n^{\\rm power-law}$
    - compute_loss 时根据 cfg.memory_form 选 EMA / power-law bar_D
    - D_history buffer cap 改为 max(K, 3) 以确保 power-law history 之 K=5 容量

    binding (D-1 纪律 3):
    - D_n 关于当前 θ 可微 (gradient flow 通过 KL forward)
    - D_{n-k} (k≥1) detach (history is fixed signal)
    - D̄^{\\rm power-law} 计算 with no_grad (history weighted sum, no backprop)
    """

    def __init__(self, config: Optional[PowerLawContradictionConfig] = None):
        self.cfg = config if config is not None else PowerLawContradictionConfig()
        self.D_history: list[torch.Tensor] = []
        self.D_ema: Optional[torch.Tensor] = None   # 仍维护 EMA reservoir 作 logging baseline
        self.ema_model: Optional[nn.Module] = None

        # 预算 power-law normalization Z (constant, 只算一次)
        self._compute_powerlaw_weights()

        logger.info(
            "PowerLawContradictionTracker init: memory_form=%s "
            "power_law_alpha=%.3f power_law_K=%d beta_model=%.6f beta_kl=%.4f "
            "lambda_1=%.4f lambda_2=%.4f lambda_3=%.4f T_2_form=%s "
            "kl_update_every=%d",
            self.cfg.memory_form, self.cfg.power_law_alpha, self.cfg.power_law_K,
            self.cfg.beta_model, self.cfg.beta_kl,
            self.cfg.lambda_1, self.cfg.lambda_2, self.cfg.lambda_3,
            self.cfg.T_2_form, self.cfg.kl_update_every,
        )

    def _compute_powerlaw_weights(self) -> None:
        """
        预算 power-law weights $w_k = k^{-\\alpha}/Z$, $Z = \\sum_{k=1}^{K} k^{-\\alpha}$.

        binary: K=5 + α=1.0 → weights = [1, 0.5, 0.333, 0.25, 0.2] / Z=2.283,
        normalized = [0.4380, 0.2190, 0.1460, 0.1095, 0.0876] (sums to 1).
        """
        K = self.cfg.power_law_K
        alpha = self.cfg.power_law_alpha
        raw = [k ** (-alpha) for k in range(1, K + 1)]
        Z = sum(raw)
        self.powerlaw_weights = [w / Z for w in raw]
        logger.info(
            "power-law weights (K=%d alpha=%.3f Z=%.4f): %s",
            K, alpha, Z, [f"{w:.4f}" for w in self.powerlaw_weights],
        )

    @torch.no_grad()
    def init_ema_model(self, model: nn.Module) -> None:
        """从主 model 拷贝出 EMA model snapshot (与 v1.0 release 一致)."""
        self.ema_model = copy.deepcopy(model)
        self.ema_model.eval()
        for p in self.ema_model.parameters():
            p.requires_grad = False
        logger.info("EMA model init done (frozen, eval mode)")

    @torch.no_grad()
    def update_ema_model(self, model: nn.Module) -> None:
        """β·θ̄ + (1-β)·θ 每 train step 之后调用 (与 v1.0 release 一致)."""
        if self.ema_model is None:
            self.init_ema_model(model)
            return
        for p_ema, p in zip(self.ema_model.parameters(), model.parameters()):
            p_ema.data.mul_(self.cfg.beta_model).add_(p.data, alpha=1 - self.cfg.beta_model)

    def compute_kl(
        self,
        model: nn.Module,
        val_input_ids: torch.Tensor,
        val_attention_mask: torch.Tensor,
    ) -> torch.Tensor:
        """KL on val batch (与 v1.0 release contradiction_loss.compute_kl 一致)."""
        assert self.ema_model is not None, "init_ema_model first"

        logits_p = model(val_input_ids, attention_mask=val_attention_mask).logits
        with torch.no_grad():
            logits_q = self.ema_model(val_input_ids, attention_mask=val_attention_mask).logits

        log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
        log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)

        if self.cfg.kl_direction == "q_to_p":
            q = log_q.exp().detach()
            kl_per_pos = (q * (log_q.detach() - log_p)).sum(dim=-1)
        elif self.cfg.kl_direction == "p_to_q":
            p = log_p.exp()
            kl_per_pos = (p * (log_p - log_q.detach())).sum(dim=-1)
        else:
            raise ValueError(f"Unknown kl_direction {self.cfg.kl_direction}")

        mask = val_attention_mask[:, 1:].float()
        kl_scalar = (kl_per_pos * mask).sum() / mask.sum().clamp_min(1)
        return kl_scalar

    def _compute_powerlaw_bar_D(self, D_n: torch.Tensor) -> torch.Tensor:
        """
        $\\bar{D}_n^{\\rm power-law} = \\sum_{k=1}^{K} w_k \\cdot D_{n-k}$
        where $w_k = k^{-\\alpha}/Z$.

        binary fallback (history vacuous):
        - 如果 len(D_history) == 0 (gen 0 first step): bar_D = D_n.detach() (与 EMA cold start 一致)
        - 如果 len(D_history) < K: use available weights, renormalize to sum=1
        """
        K_use = min(self.cfg.power_law_K, len(self.D_history))
        if K_use == 0:
            # cold start, same convention as v1.0 release EMA cold start
            return D_n.detach().clone()

        # use first K_use weights, renormalize
        weights = self.powerlaw_weights[:K_use]
        Z_use = sum(weights)
        weights_norm = [w / Z_use for w in weights]

        # weighted sum (all D_history entries are detached)
        with torch.no_grad():
            bar_D = sum(
                weights_norm[k - 1] * self.D_history[-k]
                for k in range(1, K_use + 1)
            )
        return bar_D

    def compute_loss(
        self,
        model: nn.Module,
        val_input_ids: torch.Tensor,
        val_attention_mask: torch.Tensor,
    ) -> tuple[torch.Tensor, dict]:
        """
        ℒ_contradiction = λ_1 (ΔD_n)² + λ_2 (D_n - bar_D)² + λ_3 T_2_term

        bar_D form (binary):
        - cfg.memory_form == "ema": $\\bar{D}_n = \\beta_{kl} \\bar{D}_{n-1} + (1-\\beta_{kl}) D_n$
          (与 v1.0 release contradiction_loss.compute_loss 完全一致)
        - cfg.memory_form == "power_law": $\\bar{D}_n = \\sum_{k=1}^{K} w_k D_{n-k}$
          (新 alternative form, $w_k = k^{-\\alpha}/Z$)

        T1_velocity / T2_replace 与 v1.0 release 一致, 隔离 alternative form 之 single-axis 影响。
        """
        D_n = self.compute_kl(model, val_input_ids, val_attention_mask)

        # T1 velocity (与 v1.0 release 一致)
        if len(self.D_history) >= 2:
            D_nm1 = self.D_history[-1]
            D_nm2 = self.D_history[-2]
            delta_D = D_n - D_nm1
            D_doubleprime = D_n - 2 * D_nm1 + D_nm2
        elif len(self.D_history) == 1:
            D_nm1 = self.D_history[-1]
            delta_D = D_n - D_nm1
            D_doubleprime = torch.zeros_like(D_n)
        else:
            delta_D = torch.zeros_like(D_n)
            D_doubleprime = torch.zeros_like(D_n)

        # T3 memory — bar_D form 二选 (binary, exploration alternative form 之 single-axis 改变)
        if self.cfg.memory_form == "ema":
            if self.D_ema is None:
                self.D_ema = D_n.detach().clone()
            bar_D = self.D_ema.detach()
        elif self.cfg.memory_form == "power_law":
            bar_D = self._compute_powerlaw_bar_D(D_n)
            # 仍维护 EMA reservoir 作 logging baseline cross-check
            if self.D_ema is None:
                self.D_ema = D_n.detach().clone()
        else:
            raise ValueError(f"Unknown memory_form: {self.cfg.memory_form}")

        T3_memory = (D_n - bar_D) ** 2

        # T1
        T1_velocity = delta_D ** 2

        # T2 (与 v1.0 release 一致)
        if self.cfg.T_2_form == "quadratic":
            T2_replace = (D_n ** 2) / 2
        elif self.cfg.T_2_form == "relu_dpp":
            T2_replace = F.relu(D_doubleprime)
        else:
            raise ValueError(f"Unknown T_2_form: {self.cfg.T_2_form}")

        loss = (
            self.cfg.lambda_1 * T1_velocity
            + self.cfg.lambda_2 * T3_memory
            + self.cfg.lambda_3 * T2_replace
        )

        # update EMA reservoir (无论 memory_form 都 maintain, log cross-check 用)
        with torch.no_grad():
            self.D_ema = self.cfg.beta_kl * self.D_ema.detach() + (1 - self.cfg.beta_kl) * D_n.detach()

        # update D_history (detach) — cap 改 max(K, 3) 以确保 power-law K=5 容量
        self.D_history.append(D_n.detach())
        max_cap = max(self.cfg.power_law_K, 3)
        if len(self.D_history) > max_cap:
            self.D_history.pop(0)

        metrics = {
            "D_n": float(D_n.item()),
            "delta_D": float(delta_D.item()) if delta_D.numel() else 0.0,
            "D_doubleprime": float(D_doubleprime.item()) if D_doubleprime.numel() else 0.0,
            "D_ema": float(self.D_ema.item()),
            "bar_D_used": float(bar_D.item()),     # power-law 时显示 powerlaw bar_D
            "memory_form": self.cfg.memory_form,
            "T1_velocity": float(T1_velocity.item()) if T1_velocity.numel() else 0.0,
            "T2_replace": float(T2_replace.item()) if T2_replace.numel() else 0.0,
            "T3_memory": float(T3_memory.item()) if T3_memory.numel() else 0.0,
            "history_len": len(self.D_history),
        }
        return loss, metrics

    def reset_state(self) -> None:
        """Generation 边界 reset (与 v1.0 release 一致)."""
        self.D_history.clear()
        self.D_ema = None
        logger.info("PowerLawContradictionTracker D-state reset")
