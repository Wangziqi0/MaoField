"""
contradiction_loss.py — Σ_2 → ℒ_contradiction implementation

候选 path 整合:
- **Candidate (b) KL 二阶差分 + EMA** [PRIMARY training loss, backward-able]
  数学 motivation: Σ_2 三项分解映到 KL space (velocity + memory + ReLU(D'')_replace_T2)
  isomorphism 25-40% partial (5 维度: 2 full + 2 partial + 1 weak),
  cost ↑ 25-30%, 在 frozen base LM 上避开 cosine anisotropic collapse

- **Candidate (d) gradient norm** [SUPPLEMENTARY monitoring, post-hoc]
  数学 motivation: g''_n 二阶差分对应 Σ_2 sharpness signal
  isomorphism 78.75% (理论评估 sub-agent §2 backup),
  ML literature native instability indicator (Hochreiter 1997 / Pascanu 2013 / Ghorbani 2019)
  cost ≤ 1% as monitoring (不进 training loss 因为 second-order grad cost ↑ 30-100%)

binding (CLAUDE.md 项目级规则 + 数学教授双 sub-agent verdict):
- candidate (e) cosine = -<u,v> 已 SNLI sanity check FAIL (双 model anisotropic collapse) — 删除
- candidate (b) sanity check pending (Protocol A + B), 双 fail 概率 20-30%
- candidate (d) 作 monitoring metric, paper §4 写法 supplementary evidence
- T₂ pointwise neg → ReLU(D''_n) 是工程妥协不是同构, paper §6 必须 honest disclose

paper §6 wording binding:
- "Σ_2-motivated loss with 25-40% structural correspondence" (candidate b)
- "Σ_2-isomorphic monitoring signal with 78.75% theoretical correspondence" (candidate d)
- 不允许 "Σ_2-isomorphic loss"
"""
from __future__ import annotations

import copy
import logging
import math
from dataclasses import dataclass, field
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

logger = logging.getLogger(__name__)


# ============================================================
# Candidate (b) KL 二阶差分 + EMA — PRIMARY training loss
# ============================================================

@dataclass
class KLContradictionConfig:
    """Candidate (b) KL 二阶差分 + EMA 超参."""
    # KL 度量
    kl_direction: str = "q_to_p"        # mode-covering, 对 collapse 敏感
    val_subset_size: int = 256          # held-out val 句数
    val_max_length: int = 64

    # 5/9 凌晨 default UPDATE — m_eff = 0.212 direct fit lock (per-run median, 3 strict-mirror runs)
    # per Linux dispatch §3 #1 + §4 #1.
    # CAVEAT: 3 runs 全 seed=42 (variance from fp16 numerics + library drift); D5 Phase 1
    # multi-seed (1337, 2024) verdict 后 refit, default 数值可能 update。
    # cat_arm_b.yaml (旧 framework default λ=1, β=0.9/0.999) 仍跑 Phase 1 multi-seed baseline。
    # cat_arm_b_v2_dialectical.yaml (新 framework, 此处 default 数值) 跑 Phase 2/3。
    beta_model: float = 0.999849        # exp(-0.212/1406), N_step=1406 (strict-mirror batch=128)

    # KL 序列 EMA
    beta_kl: float = 0.8090             # exp(-0.212) from m_eff direct fit, multi-seed pending

    # ℒ_contradiction 三项权重 — Klein-Gordon Lagrangian density form-borrowing
    # (Tauber 2014 §4.2), pending iter-M1 substantive redo per 7 P0 verdict
    lambda_1: float = 2.3585            # 1/(2 m_eff), kinetic / velocity v0 placeholder
    lambda_2: float = 0.1060            # m_eff/2, mass / memory v0 placeholder
    # 5/10 凌晨 ROLLBACK to 0.212: 数学教授 sub-agent §1.3 catch: 1/(4 m_eff) = 1.1792 是
    # cumulative kernel weight, 不是 λ_3 outer coefficient. binary option:
    #   option-α: keep χ Green form, λ_3 = 4 m_eff³ = 0.0381 (但 χ(1)=1.91>1 unphysical)
    #   option-β (审稿人 push): keep λ_3 = m_eff = 0.212, χ(k) = exp(-m_eff·k)
    # 当前选 option-β 默认值 — D5-7 数学层 verdict 确认前不动.
    lambda_3: float = 0.2120            # m_eff, option-β χ(k)=exp(-m_eff·k) consistent

    # update 频次
    kl_update_every: int = 10           # 每 N train step 算一次 KL

    # 5/10 凌晨 dialectical upgrade — Linux dispatch §3 + §4 (feasibility verdict pass)
    # T_2_form:
    #   "relu_dpp" — 旧 mechanical: ReLU(D''_n) punitive 只罚增, 0 罚减 (二元机械)
    #   "quadratic" — 新 dialectical: D²/2 symmetric, 不 punitive (反映总幅度而非方向)
    # 5/10 #1 feasibility verdict: gradient ✓ + 数值 quad/relu 0.54×, gradnorm 0.26×, 量级 comparable
    T_2_form: str = "quadratic"

    # kl_history_K: Volterra kernel range
    #   1 = Markov 旧 (无历史)
    #   9 = full path-dependent (5/10 #2 feasibility verdict: cost 9× per step, χ(K=9) cover 85.2%)
    # 注意: Volterra accumulator 当前在 metric 中 logged, 进入 loss form 待 D4 数学层 verdict
    # (K-th order chain rule + T_H Markov kernel construction)
    kl_history_K: int = 9
    m_eff: float = 0.212                # 用于 χ(k) = exp(-m_eff·k)/(2 m_eff) 计算


class KLContradictionTracker:
    """
    维护 KL 时间序列 D_n + 一阶差分 ΔD_n + 二阶差分 D''_n + EMA.

    binding:
    - D_n 关于当前 θ 可微, gradient 流回 model
    - D_{n-1}, D_{n-2}, EMA 都 detach 不传梯度
    - EMA model 在每个 train step 之后 update (training_step hook)
    - KL 计算每 N step 一次 (kl_update_every) 控 cost
    """

    def __init__(self, config: KLContradictionConfig | None = None):
        self.cfg = config if config is not None else KLContradictionConfig()
        self.D_history: list[torch.Tensor] = []  # 保留 [D_{n-2}, D_{n-1}, D_n]
        self.D_ema: torch.Tensor | None = None
        self.ema_model: nn.Module | None = None
        logger.info(
            "KLContradictionTracker init: beta_model=%.6f beta_kl=%.4f "
            "lambda_1=%.4f lambda_2=%.4f lambda_3=%.4f m_eff=%.4f "
            "T_2_form=%s kl_history_K=%d kl_update_every=%d",
            self.cfg.beta_model, self.cfg.beta_kl,
            self.cfg.lambda_1, self.cfg.lambda_2, self.cfg.lambda_3, self.cfg.m_eff,
            self.cfg.T_2_form, self.cfg.kl_history_K, self.cfg.kl_update_every,
        )

    @torch.no_grad()
    def init_ema_model(self, model: nn.Module) -> None:
        """从主 model 拷贝出 EMA model snapshot. 在 fine-tune 开始时调用."""
        self.ema_model = copy.deepcopy(model)
        self.ema_model.eval()
        for p in self.ema_model.parameters():
            p.requires_grad = False
        logger.info("EMA model init done (frozen, eval mode)")

    @torch.no_grad()
    def update_ema_model(self, model: nn.Module) -> None:
        """β·θ̄ + (1-β)·θ. 每 train step 之后调用."""
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
        """
        算 KL on val batch.

        kl_direction:
          - "q_to_p": KL(q || p) where p=current, q=EMA. mode-covering. 推荐.
          - "p_to_q": KL(p || q). mode-seeking.
        """
        assert self.ema_model is not None, "init_ema_model first"

        # current model forward (with grad)
        logits_p = model(val_input_ids, attention_mask=val_attention_mask).logits
        # EMA model forward (no grad)
        with torch.no_grad():
            logits_q = self.ema_model(val_input_ids, attention_mask=val_attention_mask).logits

        log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
        log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)

        if self.cfg.kl_direction == "q_to_p":
            # KL(q || p) = E_q[log q - log p], 用 -log_p cross-entropy 形式让梯度 flow 通过 log_p
            q = log_q.exp().detach()
            kl_per_pos = (q * (log_q.detach() - log_p)).sum(dim=-1)  # [B, T-1]
        elif self.cfg.kl_direction == "p_to_q":
            p = log_p.exp()
            kl_per_pos = (p * (log_p - log_q.detach())).sum(dim=-1)
        else:
            raise ValueError(f"Unknown kl_direction {self.cfg.kl_direction}")

        # mask padding
        mask = val_attention_mask[:, 1:].float()
        kl_scalar = (kl_per_pos * mask).sum() / mask.sum().clamp_min(1)
        return kl_scalar

    def compute_loss(
        self,
        model: nn.Module,
        val_input_ids: torch.Tensor,
        val_attention_mask: torch.Tensor,
    ) -> tuple[torch.Tensor, dict]:
        """
        计算 ℒ_contradiction = λ_1 (ΔD_n)² + λ_2 (D_n - D̄^EMA)² + λ_3 T_2_term.

        T_2_term 形式 (config T_2_form 控):
          - "relu_dpp" (旧 mechanical): ReLU(D''_n) punitive 单边
          - "quadratic" (新 dialectical, 5/10 凌晨 #1 feasibility PASS): D_n² / 2 symmetric

        Volterra K=9 history (config kl_history_K 控):
          - K=1 (旧 Markov): 不累加
          - K=9 (新 path-dependent, 5/10 凌晨 #2 feasibility PASS):
            metric 中 logged Σ_k=1..K χ(k) D_{n-k}, χ(k) = exp(-m_eff·k)
            (option-β per 数学教授 §1.3, 不是 option-α exp(-m_eff·k)/(2 m_eff))
            注意: Volterra 累加当前仅 metric, 进入 loss form 待 D5-7 数学层 verdict
            (K-th order chain rule + T_H Markov kernel substantive derive 后)

        Returns:
            loss: scalar tensor with grad on model params
            metrics: dict 含 D_n / ΔD_n / D''_n / D̄^EMA / volterra_sum / T_2 scalars
        """
        D_n = self.compute_kl(model, val_input_ids, val_attention_mask)  # 有梯度

        # 三项分解
        if len(self.D_history) >= 2:
            D_nm1 = self.D_history[-1]  # detached
            D_nm2 = self.D_history[-2]  # detached
            delta_D = D_n - D_nm1
            D_doubleprime = D_n - 2 * D_nm1 + D_nm2
        elif len(self.D_history) == 1:
            D_nm1 = self.D_history[-1]
            delta_D = D_n - D_nm1
            D_doubleprime = torch.zeros_like(D_n)
        else:
            delta_D = torch.zeros_like(D_n)
            D_doubleprime = torch.zeros_like(D_n)

        # memory 项: D_n - D̄^EMA
        if self.D_ema is None:
            self.D_ema = D_n.detach().clone()
        D_ema_cur = self.D_ema.detach()
        memory_term = (D_n - D_ema_cur) ** 2

        # 三项加权
        T1_velocity = delta_D ** 2

        # T_2 form 二选 (5/10 dialectical upgrade)
        if self.cfg.T_2_form == "quadratic":
            # 新 dialectical: D²/2 symmetric, 不 punitive (#1 feasibility PASS)
            T2_replace = (D_n ** 2) / 2
        elif self.cfg.T_2_form == "relu_dpp":
            # 旧 mechanical: ReLU(D''_n) punitive 单边
            T2_replace = F.relu(D_doubleprime)
        else:
            raise ValueError(f"Unknown T_2_form: {self.cfg.T_2_form}")

        T3_memory = memory_term

        loss = (
            self.cfg.lambda_1 * T1_velocity
            + self.cfg.lambda_2 * T3_memory
            + self.cfg.lambda_3 * T2_replace
        )

        # Volterra K=9 history accumulator (5/10 dialectical, metric only - 不进 loss)
        # 待 D5-7 数学层 verdict (K-th order chain rule substantive form) 决定 enter loss
        # 当前 logged 用于 D4-D5 数据 inform 数学层 derive
        volterra_sum_val = 0.0
        if self.cfg.kl_history_K > 1 and len(self.D_history) >= 1:
            K_use = min(self.cfg.kl_history_K, len(self.D_history))
            chi_weights = [math.exp(-self.cfg.m_eff * k) for k in range(1, K_use + 1)]
            with torch.no_grad():
                volterra_acc = sum(
                    chi_weights[k - 1] * self.D_history[-k] for k in range(1, K_use + 1)
                )
                volterra_sum_val = float(volterra_acc.item())

        # update EMA of KL series (no grad)
        with torch.no_grad():
            self.D_ema = self.cfg.beta_kl * D_ema_cur + (1 - self.cfg.beta_kl) * D_n.detach()

        # update D_history (detach) - 5/10 凌晨 cap 改 K (vs 旧 cap 3)
        self.D_history.append(D_n.detach())
        if len(self.D_history) > self.cfg.kl_history_K:
            self.D_history.pop(0)

        metrics = {
            "D_n": float(D_n.item()),
            "delta_D": float(delta_D.item()) if delta_D.numel() else 0.0,
            "D_doubleprime": float(D_doubleprime.item()) if D_doubleprime.numel() else 0.0,
            "D_ema": float(self.D_ema.item()),
            "volterra_sum_K": volterra_sum_val,
            "T1_velocity": float(T1_velocity.item()) if T1_velocity.numel() else 0.0,
            "T2_replace": float(T2_replace.item()) if T2_replace.numel() else 0.0,
            "T3_memory": float(T3_memory.item()) if T3_memory.numel() else 0.0,
        }
        return loss, metrics

    def reset_state(self) -> None:
        """Generation 边界 reset (新一代 fine-tune 开始)."""
        self.D_history.clear()
        self.D_ema = None
        # EMA model 不 reset (保留 generation 间 history)
        logger.info("KLContradictionTracker D-state reset")


# ============================================================
# Candidate (d) gradient norm — SUPPLEMENTARY monitoring
# ============================================================

@dataclass
class GradNormMonitorConfig:
    """Candidate (d) gradient norm 监控超参."""
    beta_g_ema: float = 0.9             # gradient norm 序列 EMA
    record_every: int = 1               # 每 step 记录


class GradNormMonitor:
    """
    Track gradient norm trajectory g_n + 一阶/二阶差分 + EMA.

    NOT a training loss (作 monitoring metric only).
    Reason: g_n = ‖∇θ ℒ_LM‖, 把它进 ℒ_total 需要 second-order gradient (cost ↑ 30-100%).

    用途:
    - paper §4 supplementary evidence (Σ_2 78.75% theoretical isomorphism)
    - collapse detector (g''_n > threshold → instability spike)
    - dynamic α scaling (optional, 不在初版用)
    """

    def __init__(self, config: GradNormMonitorConfig | None = None):
        self.cfg = config if config is not None else GradNormMonitorConfig()
        self.g_history: list[float] = []  # 全 history (post-hoc 分析)
        self.g_ema: float | None = None
        logger.info(
            "GradNormMonitor init: beta_g_ema=%.3f record_every=%d",
            self.cfg.beta_g_ema, self.cfg.record_every
        )

    @torch.no_grad()
    def record_step(self, model: nn.Module) -> dict:
        """
        在 backward 之后 optimizer.step 之前调用.
        算 ‖∇θ ℒ_LM‖₂ + 维护 g_history + 三项 metric.

        Returns: dict of g_n / Δg_n / g''_n / g̅^EMA / ReLU(g''_n)
        """
        # cat 所有 grad
        grads = []
        for p in model.parameters():
            if p.grad is not None:
                grads.append(p.grad.detach().flatten())
        if not grads:
            g_n = 0.0
        else:
            g_n = float(torch.norm(torch.cat(grads), p=2).item())

        # EMA
        if self.g_ema is None:
            self.g_ema = g_n
        else:
            self.g_ema = self.cfg.beta_g_ema * self.g_ema + (1 - self.cfg.beta_g_ema) * g_n

        # 三项 metric (post-hoc Σ_2 78.75% indicator)
        delta_g = g_n - self.g_history[-1] if self.g_history else 0.0
        if len(self.g_history) >= 2:
            g_doubleprime = g_n - 2 * self.g_history[-1] + self.g_history[-2]
        else:
            g_doubleprime = 0.0
        memory_g = (g_n - self.g_ema) ** 2

        self.g_history.append(g_n)

        return {
            "g_n": g_n,
            "delta_g": delta_g,
            "g_doubleprime": g_doubleprime,
            "g_ema": self.g_ema,
            "memory_g": memory_g,
            "relu_g_doubleprime": max(0.0, g_doubleprime),
        }

    def reset(self) -> None:
        """Generation 边界 reset (可选, 视分析需求)."""
        self.g_history.clear()
        self.g_ema = None
