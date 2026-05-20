"""
cat_trainer.py — Contradiction-Aware Trainer

继承 transformers.Trainer, hook KLContradictionTracker into compute_loss + 维护 EMA model.

设计:
- Auxiliary val loader (256 wikitext-2 val 句, 同 sanity check), 每 N step 算一次 ℒ_contradiction
- training_step 之后 update EMA model (mean teacher 模式)
- 可选 GradNormMonitor 在 training_step 中 record gradient norm (post-hoc Σ_2 78.75% indicator)

binding (sub-agent §2.3):
- D_n 关于当前 θ 可微 (gradient flow 通过 KL forward)
- D_{n-1}, D_{n-2}, EMA 全 detach (history 是 fixed signal)
- EMA model β=0.999 horizon ~1000 step matches 单代 fine-tune step 数
- KL 计算频次 kl_update_every=10 控 cost (~25-30%)
"""
from __future__ import annotations

import logging
from typing import Any, Optional

import torch
from torch.utils.data import DataLoader
from transformers import Trainer, TrainerCallback, TrainerControl, TrainerState

from contradiction_loss import (
    KLContradictionConfig,
    KLContradictionTracker,
    GradNormMonitor,
    GradNormMonitorConfig,
)

logger = logging.getLogger(__name__)


class CATTrainer(Trainer):
    """
    Contradiction-Aware Trainer.

    extra args (相对 Trainer):
      - contradiction_tracker: KLContradictionTracker 实例
      - val_loader_for_kl: torch.utils.data.DataLoader (cycle 用于算 KL)
      - contradiction_alpha: α 系数 (ℒ_total = ℒ_LM + α * ℒ_contradiction)
      - kl_update_every: 每 N step 算一次 KL (默认 10)
      - grad_norm_monitor: 可选 GradNormMonitor (作 supplementary 78.75% Σ_2 indicator)
    """

    def __init__(
        self,
        *args,
        contradiction_tracker: KLContradictionTracker | None = None,
        val_loader_for_kl: DataLoader | None = None,
        contradiction_alpha: float = 0.1,
        kl_update_every: int = 10,
        grad_norm_monitor: GradNormMonitor | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.contradiction_tracker = contradiction_tracker
        self.val_loader_for_kl = val_loader_for_kl
        self.contradiction_alpha = contradiction_alpha
        self.kl_update_every = kl_update_every
        self.grad_norm_monitor = grad_norm_monitor
        self._val_iter = None

        # 初始化 EMA model
        if self.contradiction_tracker is not None:
            self.contradiction_tracker.init_ema_model(self.model)

        logger.info(
            "CATTrainer init: contradiction_alpha=%.4f kl_update_every=%d "
            "tracker=%s val_loader=%s grad_norm_monitor=%s",
            self.contradiction_alpha, self.kl_update_every,
            self.contradiction_tracker is not None,
            self.val_loader_for_kl is not None,
            self.grad_norm_monitor is not None,
        )

    def _get_val_batch(self) -> dict[str, torch.Tensor] | None:
        """从 val_loader cycle 取一个 batch."""
        if self.val_loader_for_kl is None:
            return None
        if self._val_iter is None:
            self._val_iter = iter(self.val_loader_for_kl)
        try:
            batch = next(self._val_iter)
        except StopIteration:
            self._val_iter = iter(self.val_loader_for_kl)
            batch = next(self._val_iter)
        return batch

    def compute_loss(
        self,
        model,
        inputs,
        return_outputs: bool = False,
        num_items_in_batch=None,
    ):
        """
        ℒ_total = ℒ_LM + α * ℒ_contradiction.

        ℒ_contradiction 每 kl_update_every step 算一次, 其他 step 只算 ℒ_LM.
        """
        outputs = model(**inputs)
        lm_loss = outputs.loss

        # 决定本 step 是否算 contradiction loss
        cur_step = self.state.global_step if self.state is not None else 0
        should_compute_contradiction = (
            self.contradiction_tracker is not None
            and self.val_loader_for_kl is not None
            and self.contradiction_alpha > 0
            and cur_step > 0
            and cur_step % self.kl_update_every == 0
        )

        if should_compute_contradiction:
            try:
                val_batch = self._get_val_batch()
                if val_batch is not None:
                    val_ids = val_batch["input_ids"].to(model.device)
                    val_mask = val_batch["attention_mask"].to(model.device)
                    contra_loss, contra_metrics = self.contradiction_tracker.compute_loss(
                        model, val_ids, val_mask
                    )
                    total_loss = lm_loss + self.contradiction_alpha * contra_loss
                    # log metrics
                    if cur_step % (self.kl_update_every * 5) == 0:
                        log_metrics = {
                            f"contradiction/{k}": v for k, v in contra_metrics.items()
                        }
                        log_metrics["contradiction/loss"] = float(contra_loss.item())
                        log_metrics["contradiction/alpha"] = self.contradiction_alpha
                        self.log(log_metrics)
                else:
                    total_loss = lm_loss
            except Exception as e:
                logger.warning("contradiction loss compute failed at step %d: %s, fallback LM only", cur_step, e)
                total_loss = lm_loss
        else:
            total_loss = lm_loss

        return (total_loss, outputs) if return_outputs else total_loss

    def training_step(self, model, inputs, num_items_in_batch=None):
        """父类 backward 之后, 调 grad_norm_monitor + update EMA model."""
        loss = super().training_step(model, inputs, num_items_in_batch)

        # 记录 gradient norm (post-hoc Σ_2 78.75% indicator)
        if self.grad_norm_monitor is not None:
            try:
                g_metrics = self.grad_norm_monitor.record_step(model)
                if self.state.global_step % 50 == 0:
                    log_metrics = {f"grad_monitor/{k}": v for k, v in g_metrics.items()}
                    self.log(log_metrics)
            except Exception as e:
                logger.warning("grad norm monitor failed at step %d: %s", self.state.global_step, e)

        # update EMA model after optimizer step
        if self.contradiction_tracker is not None:
            self.contradiction_tracker.update_ema_model(model)

        return loss


def build_val_loader_for_kl(
    val_dataset,
    tokenizer,
    batch_size: int = 8,
    max_length: int = 64,
) -> DataLoader:
    """构造 KL 计算用的 val loader (256 句子集). 与 sanity check 一致."""
    from torch.utils.data.dataloader import default_collate

    def collate_fn(batch):
        # val_dataset 已 tokenize (input_ids, attention_mask, labels)
        input_ids = torch.stack([torch.tensor(b["input_ids"]) for b in batch])
        attention_mask = torch.stack([torch.tensor(b["attention_mask"]) for b in batch])
        return {"input_ids": input_ids, "attention_mask": attention_mask}

    loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn,
        drop_last=True,
        num_workers=0,
    )
    return loader
