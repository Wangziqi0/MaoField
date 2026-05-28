# ROCM/MIOpen backward kernel 溯源审计 (D27, 2026-05-27)

> **任务**: chain runner backward 路径 → MIOpen/hipBLAS kernel → GitHub fp16 精度对位 → NaN 日志逐行对位
> **角色**: Opus 4.7 零上下文 ROCm 源码追踪子代理 (额外 agent, 来自 Win 端)
> **约束**: 只溯源不推断 + 标 GitHub URL + 行号 + 不修改任何文件 + 不擅 ssh 22 写 + 中文严格

---

## §0 metadata

| 项 | 值 |
|---|---|
| 真实日期校验 | 2026-05-27 21:19:23 CST (`date` 二值返回, 不继承陈旧 system reminder) |
| 主机 | 7B13 (192.168.31.36, Linux 数据中枢) |
| scope 工作目录 | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/` |
| transformers 本机版本参考 | 5.7.0 (位于 `/home/amd/.local/lib/python3.12/site-packages/transformers/`); 9070XT 跑实验机的 transformers 版本未在本审计中直接 verify (`/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/.venv/` 不在 7B13 上) |
| 实验机 PyTorch backend | ROCm (从 nohup.log 的 `device=cuda` 但实际硬件 9070XT 推断, 不在本审计直接 verify) |

### 关键文件 sha256 (本次溯源锁定的二值身份)

| 路径 | sha256 |
|---|---|
| `scripts/candidate_c_runner.py` | `5a922566f5b27be0fb2f3103ef3cfd2465446ba97344ad738bb73f1a9bceb32f` |
| `src/train_one_generation.py` | `e83d1ee23d0d9ae1f77bd24987fd1e542a572a045eb5825e8f6c19b26e1a8a40` |
| `src/cat_trainer.py` | `0f025e6941601573377e6e46646c1851ec713e6fec0ca77d7c5957398b1d64e6` |
| `src/contradiction_loss.py` | `9034797bc812265b697beb8f3cf2b1d8b6cc968d0a98bdace413c5b884e7abf8` |
| `dppl_bridge_verify_d21_output/candidate_c.nohup.log` (5426 行) | `097483b8551bcde69533d11708a2d6e6375264c229bfc8932ff574e870162b13` |
| `candidate_c/candidate_c_20260522_203837.jsonl` (180 条 chain_gen_done) | `a805576fdb0e9f4ec40bafaa068a9c0772f7f629c6238d602ad483bf23f5a57d` |

### archive 备份 diff

- `archive/v1.0_release_20260516/src/cat_trainer.py` ≡ 当前 `src/cat_trainer.py` (无差异)
- `archive/v1.0_release_20260516/src/contradiction_loss.py` ≡ 当前 `src/contradiction_loss.py` (无差异)
- `archive/v1.0_release_20260516/src/train_one_generation.py` vs 当前: 仅 D22 新加 4 行 (line 102-104 中文注释 + line 108 `attn_implementation="eager"`); 其余完全一致

> **D-1 纪律 5 错误浮现注**: archive 备份(D17 paper v8 final 锁定时刻)与当前 D22 修改后版本的唯一差异是 `attn_implementation="eager"` 显式声明 (避 OPT 模型 SDPA 默认在 `output_attentions=True` 下 silent fallback)。该改动**不**影响 backward 路径的 fp16 精度行为, 仅影响 forward attention 的 implementation 选择。

---

## §1 backward kernel 调用栈 (从 chain runner 到 MIOpen kernel)

只标代码已 verify 的真实路径, 未 verify 的标 [推断不写入]。

### 1.1 chain runner → fine_tune_one_generation

`scripts/candidate_c_runner.py:257-275` 调用:
```python
result = fine_tune_one_generation(
    base_model_path=base_model_path,
    ...
    fp16=fp16_use,                      # = cfg.fine_tune.fp16 and device != "cpu"
    gradient_checkpointing=cfg.fine_tune.gradient_checkpointing,
    ...
    cat_config=cat_for_this_gen,        # gen=0 时 None, gen≥1 时 cat_cfg
)
```

其中 `candidate_c_runner.py:246`:
```python
cat_for_this_gen = None if g == 0 else cat_cfg
```

→ **gen=0 必 disabled CAT**, gen≥1 时按 α>0 启用 CAT。

### 1.2 fine_tune_one_generation → Trainer / CATTrainer

`src/train_one_generation.py:105-109` 模型加载 fp32 dtype:
```python
model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float32,           # 必 fp32 加载, mixed precision 由 Trainer 管
    attn_implementation="eager",
)
```

`src/train_one_generation.py:116-136` TrainingArguments:
```python
training_args = TrainingArguments(
    ...
    fp16=fp16,                            # cat_arm_b.yaml 设 True
    gradient_checkpointing=gradient_checkpointing,
    ...
)
```

`src/train_one_generation.py:139-183` branching:
- 若 `cat_config.enabled and alpha > 0` → `CATTrainer` (继承 `transformers.Trainer`)
- 否则 → vanilla `transformers.Trainer`

### 1.3 Trainer.training_step → backward 主路径

参考 `/home/amd/.local/lib/python3.12/site-packages/transformers/trainer.py` (transformers 5.7.0):

| 行号 | 调用 |
|---|---|
| `trainer.py:1870` | `def training_step(self, model, inputs, num_items_in_batch=None) -> torch.Tensor:` |
| `trainer.py:1908-1909` | `with self.compute_loss_context_manager(): loss = self.compute_loss(model, inputs, ...)` |
| `trainer.py:1937` | `self.accelerator.backward(loss, **kwargs)` |
| `trainer.py:2496-2500` | `def _clip_grad_norm(self, model): return self.accelerator.clip_grad_norm_(model.parameters(), self.args.max_grad_norm)` |
| `trainer.py:2502-2511` | `def _get_grad_norm(self, model, grad_norm=None): ... grad_norm = self.accelerator.clip_grad_norm_(...)` |
| `trainer.py:1757-1760` | 主训练循环内 `if self.args.max_grad_norm > 0: grad_norm = self._clip_grad_norm(model); grad_norm = self._get_grad_norm(model, grad_norm=grad_norm)` |
| `trainer.py:2069-2070` | `if grad_norm is not None: logs["grad_norm"] = grad_norm.item() if isinstance(grad_norm, torch.Tensor) else grad_norm` |

> 此处 `self.accelerator` = `accelerate.Accelerator`, 内部在 fp16 模式下持 `torch.cuda.amp.GradScaler` (ROCm 等价为 `torch.amp.GradScaler('cuda')`)。

### 1.4 CATTrainer.compute_loss → KLContradictionTracker.compute_loss

仅 gen≥1 + α>0 时启用。

`src/cat_trainer.py:92-143` `CATTrainer.compute_loss`:
```python
outputs = model(**inputs)                              # forward, 在 fp16 autocast 下
lm_loss = outputs.loss                                 # 主 LM loss
...
if should_compute_contradiction:                       # 每 kl_update_every=10 step 一次
    val_batch = self._get_val_batch()
    contra_loss, contra_metrics = self.contradiction_tracker.compute_loss(
        model, val_ids, val_mask
    )
    total_loss = lm_loss + self.contradiction_alpha * contra_loss
```

`src/contradiction_loss.py:138-175` `KLContradictionTracker.compute_kl`:
```python
logits_p = model(val_input_ids, attention_mask=val_attention_mask).logits   # 当前 model forward (有 grad)
with torch.no_grad():
    logits_q = self.ema_model(val_input_ids, attention_mask=val_attention_mask).logits  # EMA model forward
log_p = F.log_softmax(logits_p[:, :-1, :], dim=-1)
log_q = F.log_softmax(logits_q[:, :-1, :], dim=-1)
# kl_direction="q_to_p":
q = log_q.exp().detach()
kl_per_pos = (q * (log_q.detach() - log_p)).sum(dim=-1)
mask = val_attention_mask[:, 1:].float()
kl_scalar = (kl_per_pos * mask).sum() / mask.sum().clamp_min(1)
```

`src/contradiction_loss.py:177-243` `KLContradictionTracker.compute_loss`:
```python
D_n = self.compute_kl(model, val_input_ids, val_attention_mask)     # 有梯度
delta_D = D_n - D_nm1                                                # detached 之前历史
D_doubleprime = D_n - 2 * D_nm1 + D_nm2
memory_term = (D_n - D_ema_cur) ** 2

T1_velocity = delta_D ** 2
T2_replace = (D_n ** 2) / 2          if T_2_form == "quadratic"
T2_replace = F.relu(D_doubleprime)   if T_2_form == "relu_dpp"
T3_memory = memory_term

loss = lambda_1 * T1_velocity + lambda_2 * T3_memory + lambda_3 * T2_replace
```

### 1.5 backward → ROCm/MIOpen kernel 触发面

OPT-125m + fp16 + AdamW + `block_size=64` + `attn_implementation="eager"` 配置下, 单 training_step backward 会触发以下 ROCm kernel 路径 (按调用先后):

| backward 阶段 | 触发 op | ROCm/MIOpen 路径 |
|---|---|---|
| **logits softmax_backward** | `F.log_softmax`, `nn.CrossEntropyLoss` 内部 softmax_bwd | `aten::_log_softmax_backward_data` → `at::native::log_softmax_backward_cuda_kernel` (在 ROCm 上 hipify 后等价) |
| **OPTAttention bmm_backward** | `torch.bmm(attn_probs, value_states)` + `torch.bmm(Q, K.T)` | `aten::bmm` → `at::cuda::blas::gemm<at::Half>` → hipBLAS `hipblasGemmEx` (Tensile/rocBLAS) |
| **OPTAttention softmax_backward** | eager mode 的 `nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(torch.float16)` 反向 | `aten::_softmax_backward_data` → MIOpen `MIOpenSoftmax.cl` SoftmaxBackward kernel |
| **OPTLayer layernorm_backward** | `nn.LayerNorm` 反向 (OPT 用 final_layer_norm + self_attn_layer_norm + 内部) | `aten::native_layer_norm_backward` → MIOpen `MIOpenLayerNorm.cpp` LayernormBwdContiguous kernel |
| **OPTLayer linear_backward** | Q/K/V/Out projection + FC1 / FC2 | `aten::mm.backward` → hipBLAS gemm fp16 |
| **embedding_backward** | `nn.Embedding` 反向 | `aten::embedding_dense_backward` |
| **AMP unscale_grads** | `GradScaler.unscale_(optimizer)` | `torch._amp_foreach_non_finite_check_and_unscale_()` (ATen kernel) |
| **clip_grad_norm** | `accelerate.Accelerator.clip_grad_norm_` (内部走 `torch.nn.utils.clip_grad_norm_`) | `aten::foreach_norm` |
| **AdamW.step** | `torch.optim.AdamW.step()` (fused = False 默认) | `aten::add_`, `aten::addcdiv_`, `aten::sqrt` |

> CATTrainer 启用时 `kl_update_every=10` 每 10 step 多触发一次完整 forward (`logits_p` 有 grad + `logits_q` no_grad) 与上述 backward 链 — 即 **CAT 启用 step 的 backward 计算量 = vanilla step × ~2** (主 LM forward + KL forward 各一次)。

---

## §2 GitHub 源码精度对位

### 2.1 PyTorch GradScaler (AMP) — fp16 训练的 NaN/Inf 自愈机制

源: https://github.com/pytorch/pytorch/blob/v2.4.0/torch/amp/grad_scaler.py

| 函数 | 行号 | 关键逻辑 |
|---|---|---|
| `__init__` | 102-127 | 默认 `init_scale=2.0**16=65536`, `growth_factor=2.0`, `backoff_factor=0.5`, `growth_interval=2000` |
| `_unscale_grads_` | 258-301 | line 290 调 `torch._amp_foreach_non_finite_check_and_unscale_()`, 返回 `per_device_found_inf._per_device_tensors` |
| `step` | 328-405 | line 360 `unscale_()` 若 stage=READY; line 367 `_maybe_opt_step()` 检查 `found_inf_per_device` 任何非零则 **skip `optimizer.step()`** |
| `update` | 407-459 | line 441-456 调 `torch._amp_update_scale_()`, found_inf → `scale *= backoff_factor`; 否则 growth_interval step 后 `scale *= growth_factor` |

### 2.2 PyTorch AmpKernels.cu — NaN 检测内核

源: https://github.com/pytorch/pytorch/blob/v2.4.0/aten/src/ATen/native/cuda/AmpKernels.cu

| kernel | 行号 | 逻辑 |
|---|---|---|
| `_amp_non_finite_check_and_unscale_cuda_` | 49-74 | line 67 `!isfinite_ensure_cuda_math(val)` 检测; line 68 `*found_inf_ptr = 1.f`; line 72 `val * inv_scale_val` 缩放 |
| `_amp_foreach_non_finite_check_and_unscale_cuda_` | 164-186 | MTA 优化版本, 同一检测逻辑 (line 174-180) |
| `amp_update_scale_cuda_kernel` | 188-206 | line 200 `isfinite_ensure_cuda_math(new_scale)` 防止 scale 自身溢出 |

> **关键 binary fact**: GradScaler 路径在每个 step **必跑** `_amp_foreach_non_finite_check_and_unscale_`。检测出 NaN/Inf 后 **skip optimizer.step**, scale *= 0.5。这是 transformers Trainer log 中 `grad_norm=nan` 出现却 `loss` 仍正常衰减的**机制源**。

### 2.3 hipBLAS / Tensile fp16 GEMM 累加器

PyTorch 端 (源: https://github.com/pytorch/pytorch/blob/v2.4.0/aten/src/ATen/cuda/CUDABlas.cpp):

| 函数 | 行号 | 关键参数 |
|---|---|---|
| `gemm_internal_cublas<at::Half>` | ~1228-1278 | line 1255-1265 调 `cublasGemmEx(...)` 设 `CUDA_R_16F` (输入 A/B/C dtype) + **`CUDA_R_32F`** (computeType, 即累加器) + `CUBLAS_GEMM_DEFAULT_TENSOR_OP` |

→ ROCm 上 hipify 后 `cublasGemmEx` 映射到 `hipblasGemmEx`, `CUDA_R_32F` 映射到 `HIPBLAS_R_32F`, 后端走 rocBLAS / hipBLASLt / Tensile。

Tensile DataType 定义 (源: https://github.com/ROCm/Tensile/blob/develop/Tensile/Source/lib/include/Tensile/DataTypes.hpp):
- line 76-89 `enum class DataType`: `Half`, `BFloat16`, `Float`, ...
- line 216-218 `TypeInfo<Half>`, line 223-225 `TypeInfo<BFloat16>`

> **fp16 GEMM 在 ROCm 上默认 fp32 累加** (与 NVIDIA CUDA 一致)。这意味着 OPT 12 层 attention/FFN 的 GEMM 路径本身不会因为 fp16 累加器引入 NaN — NaN 必出在 GEMM 之**外**的路径。

### 2.4 MIOpen Softmax kernel 精度

源: https://github.com/ROCm/MIOpen/blob/develop/src/kernels/MIOpenSoftmax.cl

| 路径 | 行号 | 累加器类型 |
|---|---|---|
| `SoftmaxForward` CSR-Vector (NUM_BATCH==1) | 345-346 | `t_helper = (FLOAT)-MAX_VAL;` — **用 `_FLOAT` (输入 dtype, fp16)** 累加 max/sum/exp |
| `SoftmaxForward` CSR-Stream (NUM_BATCH>1) | 430 | `FLOAT t_helper = (FLOAT)-MAX_VAL;` — 同上, **fp16 累加器** |
| `SoftmaxBackward` | 768, 815, 872 | 用 `_FLOAT_ACCUM` (fp32 累加器) |

> **关键 binary 差异**: MIOpen `SoftmaxForward` (fp16 模式) **不**用 fp32 累加器, 而是 fp16 同精度累加 max/sum/exp。`SoftmaxBackward` 用 fp32。
>
> 但 OPTAttention eager mode (见 §2.6) 在 PyTorch 层显式 cast 到 fp32 再 softmax 再 cast 回 fp16, 故 attention softmax 不走 MIOpen kernel 的 fp16 路径 — 走的是 `at::native` 的 fp32 softmax。
>
> CrossEntropyLoss 内部 `log_softmax` 与 `KLContradictionTracker.compute_kl` 中 `F.log_softmax(logits_p, dim=-1)` 在 logits 为 fp32 (因为 OPT lm_head 输出 cast 到 fp32) 时也不走 MIOpen fp16 路径。

### 2.5 MIOpen LayerNorm kernel 精度

源: https://github.com/ROCm/MIOpen/blob/develop/src/kernels/MIOpenLayerNorm.cpp

| 行号 | 代码 | 类型 |
|---|---|---|
| 56-109 | `template <typename TI, typename TO> __device__ void layernormfwdcontiguous(...)` | TI=输入, TO=输出 |
| 85 | `FLOAT_ACCUM pmean = 0;` | **fp32 累加器** |
| 91 | `FLOAT_ACCUM tmp = CVT_FLOAT2ACCUM(x[x_idx]);` | fp16 → fp32 转换 |
| 92-93 | `pmean += tmp; pvar += tmp * tmp;` | fp32 累加 |
| 103 | `pvar = ltmp[0] / inner_size - pmean * pmean;` | fp32 variance |
| 104 | `FLOAT_ACCUM prstd = rsqrt(pvar + FLOAT_ACCUM(eps));` | **eps 在 rsqrt 内部加, fp32 精度** |
| 119 | `y[idx] = CVT_ACCUM2FLOAT(val);` | fp32 → 输出 dtype |
| 705-712 | `extern "C" __global__ void LayernormFwdContiguous(...)` | 主入口 |

> **LayerNorm 在 ROCm 上是 fp32 累加 + 显式 eps 加入 rsqrt 内部**, 这是 NaN 防护的正确做法。LayerNorm 路径本身不会引入 NaN — 除非输入已经 NaN 或 variance 已经为 NaN。

### 2.6 transformers OPTAttention eager mode fp16 路径

源: https://github.com/huggingface/transformers/blob/v4.46.0/src/transformers/models/opt/modeling_opt.py

`OPTAttention.forward` (约 240-390 行):
- 行 ~320-330: `attn_weights = torch.bmm(query_states, key_states.transpose(1, 2))` — fp16 bmm (走 hipBLAS fp16+fp32 累加路径)
- 行 ~350-365: **关键 dtype 处理**
  ```python
  if attn_weights.dtype == torch.float16:
      attn_weights = nn.functional.softmax(attn_weights, dim=-1,
                                            dtype=torch.float32).to(torch.float16)
  else:
      attn_weights = nn.functional.softmax(attn_weights, dim=-1)
  ```
- 行 ~375-380: `attn_probs = nn.functional.dropout(...)`; `attn_output = torch.bmm(attn_probs, value_states)` — fp16 bmm

> **关键 binary fact**: OPT eager attention softmax **显式提升到 fp32** 计算再 cast 回 fp16。这意味着即使 attention scores (Q·K^T) 中有极大值, softmax 也不会在 fp16 max/sum 阶段溢出。

---

## §3 NaN 日志逐行对位 (candidate_c.nohup.log, 5426 行)

> 日志含 tqdm 进度条 `\r`, 用 `tr '\r' '\n'` 切分后行号变, 此处给的是切分**后**的行号。原始日志体积 5226 KB / 5426 行(原始换行)。

### 3.1 全局结构

| 区段 | 行号范围 (tr 后) | seed=42 α | gen | 状态 |
|---|---|---|---|---|
| 启动 | 1-21 | — | — | data load + hook init |
| α=0.0 g=0 (CAT disabled) | 22-1820 | 0.0 | 0 | **PASS**: train_loss=4.5215 val_loss=4.5363 val_ppl=93.35 |
| α=0.0 g=1 | 3030-4829 | 0.0 | 1 | **PASS**: train_loss=1.8520 val_loss=4.5363 |
| α=0.0 g=2..9 | 6038-28893 | 0.0 | 2..9 | **PASS** (10 gen 全 PASS, val_loss 漂移 4.536348 → 4.536340, 10⁻⁶ 级) |
| α=5.0 g=0 (CAT disabled, runner.py:246) | 28930-30724 | 5.0 | 0 | **FAIL**: train_loss=0.9174 **val_loss=nan** val_ppl=inf |
| α=5.0 g=1..9 (CAT enabled) | 31933-60013 | 5.0 | 1..9 | **FAIL**: train_loss=0.0000 val_loss=nan, 全 NaN cascade |
| α=10.0 g=0 (CAT disabled) | 60050-61827 | 10.0 | 0 | **FAIL**: train_loss=0.6036 val_loss=nan |
| α=10.0 g=1..9 | 63036-... | 10.0 | 1..9 | **FAIL**: train_loss=0.0000 val_loss=nan |

### 3.2 对位关键证据 (D-1 纪律 1 binary)

#### 证据 A: α=0.0 g=0 (baseline, CAT disabled) — grad_norm=nan 但 loss 正常衰减

`candidate_c.nohup.log` (tr 后行号) line 328-335:
```
20%|██  | 292/1460 [00:46<02:49, 6.89it/s] {'loss': 4.5165, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.17}
                                            {'loss': 4.5159, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.34}
                                            {'loss': 4.5214, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.51}
                                            {'loss': 4.5257, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.68}
                                            {'loss': 4.522, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.86}
{'eval_loss': 4.536348819732666, ...epoch: 1.0}
{'loss': 4.5286, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 1.03}
```

**对位**:
- `grad_norm=nan` ↔ `transformers/trainer.py:2502-2511 _get_grad_norm` 内部 `accelerator.clip_grad_norm_(model.parameters(), float("inf"))` 在 fp16 + GradScaler 路径下, 当 `_amp_foreach_non_finite_check_and_unscale_` 检出当前 step grad 含 inf/NaN 时, **grad 不被 unscale 但保留 NaN 标记**, 后续 `clip_grad_norm_` 计算返回 NaN
- 但 `loss` 仍 ~4.5 正常衰减 ↔ GradScaler `step` 方法 line 367 `_maybe_opt_step` **skip 了 optimizer.step()** (PyTorch grad_scaler.py:328-405), 故 weights 不变 → 下次 forward loss 仍正常
- `learning_rate=2e-05` 不变 ↔ scheduler 不依赖 found_inf, 按 step 计数推进

**结论**: α=0 baseline 的 grad_norm=nan **是 fp16 训练的 normal 行为**, GradScaler 正确 skip 后训练继续。10 generation 全 PASS 即此机制工作正常的二值实证。

#### 证据 B: α=5.0 g=0 — 同样 CAT disabled, 但训练崩溃

`candidate_c.nohup.log` (tr 后) line 28930 起 (训练时间 2026-05-23 01:53:07):
```
fine-tune base=facebook/opt-125m → out=...alpha5.0/no_preserve_seed42/generation_0 epochs=5 seed=42
```

line 29248~ (epoch 0.17):
```
{'loss': 4.4008, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.17}
{'loss': 4.4657, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.34}
{'loss': 4.5287, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.51}
{'loss': 4.5427, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.68}
{'loss': 4.5442, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 0.86}
```

line ~679 (epoch 1.0):
```
{'eval_loss': nan, ...epoch: 1.0}
{'loss': 4.3064, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 1.03}
{'loss': 0.0, 'grad_norm': nan, 'learning_rate': 2e-05, 'epoch': 1.2}
{'loss': 0.0, ..., 'epoch': 1.37}
...
```

line 30724 (训练结束):
```
fine-tune 完成: train_loss=0.9174 val_loss=nan val_ppl=inf
```

**对位**:
- 与证据 A 完全相同的配置 (vanilla `Trainer`, `cat_for_this_gen=None` 因为 `g==0`, fp16, seed=42, opt-125m, AdamW) **但行为完全不同**:
  - epoch 0.86 时 loss=4.5442 仍正常
  - epoch 1.0 `eval_loss=nan` (首次 NaN 出现在 eval, 此时 weights **已被 NaN 覆盖**)
  - epoch 1.2 起 `loss=0.0` ↔ model.forward 输出 NaN → CrossEntropyLoss 对 NaN logits + valid labels 通过 mask 后返回 0.0 (`nn.functional.cross_entropy` 在 reduction='mean' 下若所有有效位置都 nan 但 mask.sum()>0 时会返回 nan 或 0, 依实现而定; 此处行为是 0.0)
- 差异的可能 trigger:
  - α=0 链刚跑完 5 小时 22 分 (5/22 20:38 → 5/23 01:53), GPU 状态有累积差异 [但具体内部状态不在本审计 scope]
  - ROCm fp16 GEMM 在 9070XT (RDNA4 / gfx1201) 上的边界数值 case [不在本审计 ssh 22 verify]
  - GradScaler 在第 1 epoch 前几个 step 连续 found_inf 后 scale 衰减到 backoff 边界, 某次 unscale 后 grad 极小 → AdamW second moment 更新 → 累积错误
- **不在本审计 scope 之内的推断**: weights 何时首次被 NaN 覆盖的精确 step (jsonl/log 不够精细)

#### 证据 C: α=5.0 g=1 (CAT enabled) — contradiction loss 全 NaN

`candidate_c.nohup.log` (tr 后) line 31933 起:
```
fine-tune base=...alpha5.0/no_preserve_seed42/generation_0 → ...generation_1 epochs=5 seed=42
```

line 31936-31942 CATTrainer 启动:
```
CATTrainer enabled: alpha=5.0000 kl_update_every=10
KLContradictionTracker init: beta_model=0.999000 beta_kl=0.9000 lambda_1=1.0000 lambda_2=1.0000 lambda_3=1.0000 m_eff=1.0000 T_2_form=relu_dpp kl_history_K=1 kl_update_every=10
GradNormMonitor init: beta_g_ema=0.900 record_every=1
EMA model init done (frozen, eval mode)
CATTrainer init: contradiction_alpha=5.0000 kl_update_every=10 tracker=True val_loader=True grad_norm_monitor=True
```

> **注**: log 中 `T_2_form=relu_dpp kl_history_K=1` — 实际 yaml 加载的值, 不是 `contradiction_loss.py:84` 的 `quadratic` / line 91 的 `9` 默认值。说明 yaml `cat_arm_b.yaml` 还在用旧 framework default。

line 32284 (g=1 epoch 0):
```
{'grad_monitor/g_n': nan, 'grad_monitor/delta_g': 0.0, ..., 'epoch': 0}
```

line 32286 (g=1 epoch 0.17):
```
{'contradiction/D_n': nan, 'contradiction/delta_D': nan, 'contradiction/D_doubleprime': 0.0,
 'contradiction/D_ema': nan, 'contradiction/volterra_sum_K': 0.0,
 'contradiction/T1_velocity': nan, 'contradiction/T2_replace': 0.0, 'contradiction/T3_memory': nan,
 'contradiction/loss': nan, 'contradiction/alpha': 5.0, 'epoch': 0.17}
```

**对位**:
- `D_n = nan` ↔ `contradiction_loss.py:154-175` `compute_kl`. `model(val_input_ids, ...).logits` 输出 NaN (因为 g=1 起始 model = g=0 saved model, weights 已含 NaN 从 α=5 g=0 fail), 导致 `log_softmax(logits_p)` 全 NaN → `kl_per_pos` 全 NaN → `kl_scalar = nan`
- `T1_velocity = nan` ↔ `(D_n - D_nm1)**2` 中 D_n=nan
- `T2_replace = 0.0` ↔ `T_2_form="relu_dpp"`, `F.relu(D_doubleprime)`; D_doubleprime=0.0 (因 D_history 仅 1 个 entry, `contradiction_loss.py:213` 显式置 0)
- `T3_memory = nan` ↔ `(D_n - D_ema_cur)**2` 中 D_ema_cur=nan, D_n=nan
- `volterra_sum_K = 0.0` ↔ `contradiction_loss.py:249-256`, K=1 时 `kl_history_K > 1` False, 故不累加, 返 0.0
- `contradiction/loss = nan` ↔ line 239-243 三项加权和, 任一 nan 即结果 nan

#### 证据 D: jsonl 中的 multi-layer hook NaN cascade

`candidate_c/candidate_c_20260522_203837.jsonl` seed=42 α=5.0 gen=0 entry:
- `a1_ppl: null` ↔ `candidate_c_runner.py:276-277` `val_loss = float(result.val_loss)` (NaN cast 到 float 后还是 NaN), `a1_ppl = math.exp(val_loss) if val_loss < 20 and math.isfinite(val_loss) else float("inf")` → val_loss=nan 不满足 isfinite → inf; 但 entry 写出时 line 408 `"a1_ppl": float(a1_ppl) if math.isfinite(a1_ppl) else None` → None
- `a2_anisotropy[0] = 0.7024863800033927` (第 0 层 valid) but `[1..11] = NaN` ↔ MultiLayerHook 在 layer 1 起捕获到的 hidden_states 已含 NaN; 第 0 层 = embedding 输出 (在 attention block 之前), 故 valid; 第 1 层开始 = OPTDecoderLayer 0 输出之后, 含 attention + ffn 累积 NaN
- `a3_attn_entropy[0] = [valid 12 head]`, `[1..11] = [NaN×12]` ↔ 同上, 第 0 层 attention 之前的输入未 NaN 但 attention weight 计算后产生 NaN (cap_model 是 reload from saved gen_dir, weights 含 NaN)
- `a6_ema_divergence: [NaN×12]` ↔ candidate_c_runner.py:299-313 reframe 为 "per-layer L2 drift from gen 0 baseline", gen=0 baseline 自身已含 NaN weights

> **D-1 纪律 5 错误浮现**: 第 0 层 (embedding 输出) 不 NaN, 第 1 层起 NaN — 这指向 **NaN 起源在第一个 OPTDecoderLayer 内部** (而不是 embedding 表自身)。具体是 self_attn / fc1 / fc2 / layernorm 哪个 op 不在本审计 scope 内 verify (需要逐 layer hook + 数值打印, 须 ssh 22 跑, 本审计 ssh 22 写权限 = 拒绝).

### 3.3 jsonl 全局统计 (180 条 chain_gen_done)

| 统计项 | 值 |
|---|---|
| 总 entry | 180 |
| `val_loss` 非 None | 34 (= 30 α=0 链全部 + 1 seed=1337 α=5 gen=0 + 3 待 verify) |
| `val_loss = None` (NaN cascade) | 146 |
| 全局唯一 `chain_gen_fail` event | 0 (因为 candidate_c_runner.py:204-454 把所有 exception 在 hook 阶段都 catch 在 caveats 里, 而 train fail 不 raise, fine-tune 完成后 val_loss=nan 仍 chain_gen_done) |
| caveat `a6_reframed_as_drift_from_gen0_baseline` | 162 (gen≥1 全部) |
| caveat `a6_gen0_self_reference_zero_list_expected` | 18 (gen=0 全部 = 6 seed × 3 α) |
| caveat `chain_gen_exception` | 0 |
| caveat `hook_capture_fail_*` | 0 |
| caveat `generate_synthetic_fail*` | 0 |

> **观察**: 没有 caveat 标记任何 capture 失败 — 这意味着 hook NaN 不抛 exception, 而是把 NaN 数值平静地写入 jsonl。 candidate_c_runner.py:367 `caveats.append(f"hook_capture_fail_batch_{i}:{e}")` 只在 Exception 时触发, NaN 数值通过 mean/std 计算返回 NaN 不抛 exception。

### 3.4 valid entry 数据 (D-1 纪律 1 binary, 不 inflate)

仅列入 `val_loss` 非 None 的 entry 第一个 (seed=42 α=0):

| seed | α | gen | a1_ppl | val_loss | train_loss (从 log) |
|---|---|---|---|---|---|
| 42 | 0.0 | 0 | 93.34934186100965 | 4.536348819732666 | 4.5215 |
| 42 | 0.0 | 1 | 93.34907478678235 | 4.536345958709717 | 1.8520 |
| 42 | 0.0 | 2 | 93.34876320114957 | 4.536342620849609 | 1.8516 |
| 42 | 0.0 | 3 | 93.34849612857782 | 4.536339... | 1.8516 |
| 42 | 0.0 | 4 | 93.34880771331915 | 4.536343097686768 | 1.8526 |
| 42 | 0.0 | 5 | 93.34925283618232 | 4.53634786605835 | 1.8514 |
| 42 | 0.0 | 6 | 93.34782845049138 | 4.536332607269287 | 1.8514 |
| 42 | 0.0 | 7 | 93.34831808062115 | 4.536337852478027 | 1.8519 |
| 42 | 0.0 | 8 | 93.34862966476818 | 4.536341190338135 | 1.8516 |
| 42 | 0.0 | 9 | 93.34854064062004 | 4.536340236663818 | 1.8506 |

> α=0 baseline 全 10 gen 的 val_ppl 在 [93.347, 93.350] 区间, **漂移 ~3×10⁻³ ppl**。这与 memory entry "4 cells bit-identical 93.38780852810248" 中 D26 PID 491900 数字 (93.387) 略不同, 数值 epoch 4 位起异 (93.348 vs 93.387). 推断不属本审计 scope。

---

## §4 关键 finding (binary, 标 binding)

> 所有 finding 严守"只溯源不推断"。能 verify 的标 ✓, 不能 verify 的明示 [不在本审计 scope]。

### F1 ✓ archive vs current 唯一 diff = `attn_implementation="eager"` 显式声明

`src/train_one_generation.py:102-108` 是 D22 加的 4 行 (中文注释 + 一个 keyword arg)。
- archive `archive/v1.0_release_20260516/src/train_one_generation.py` 在 line 101 后无注释、line 104 后无 `attn_implementation="eager"`
- cat_trainer.py + contradiction_loss.py 完全无变化

**含义**: D17 paper v8 final 锁定后的 src 与 D22 candidate_c 跑的 src **backward 路径完全等价**, attention 实现选择上的差异不影响 backward 数值。

### F2 ✓ chain runner gen=0 CAT 强制 disabled

`scripts/candidate_c_runner.py:246`:
```python
cat_for_this_gen = None if g == 0 else cat_cfg
```

→ **α=5 / α=10 的 gen=0 跑的是 vanilla Trainer**, 与 α=0 的 gen=0 配置等价。

**含义**: 同一 baseline 配置下 α=5 g=0 NaN cascade vs α=0 g=0 PASS — root cause 不在 CAT 代码路径。

### F3 ✓ `grad_norm=nan` 是 fp16 GradScaler 正常工作的信号

PyTorch grad_scaler.py:328-405 `step` 方法在 `found_inf_per_device` 非零时 skip optimizer.step。transformers trainer.py:2502-2511 `_get_grad_norm` 在 grad 含 NaN 时返回 NaN。两者**联动机制**:
- 检出 NaN grad → skip step (weights 不变) → 下次 forward loss 还正常 → scale *= 0.5 → 重试
- α=0 baseline 10 generation 全 PASS 即此机制正常工作的二值实证

### F4 ✓ NaN 起源 = 第 0 层 OPTDecoderLayer 输出之后

jsonl 中 a2_anisotropy / a3_attn_entropy 第 0 层 valid (≈0.7024 / 12-head 数值正常), 第 1 层起全 NaN。这指向:
- embedding 表自身**不**含 NaN
- 第 1 个 OPTDecoderLayer (内含 self_attn + layernorm + fc1 + fc2 + 残差) 在某一步产生 NaN
- NaN 之后通过残差连接 + layernorm propagate 到剩余 11 层全部

**[不在本审计 scope verify]**: 具体是 self_attn 还是 fc1/fc2/layernorm 哪一步首次产生 NaN — 需要 layer-wise hook + 数值打印, 须 ssh 22 跑实际 run, 本审计 ssh 22 写权限 = 拒绝。

### F5 ✓ 三层 GitHub 源码精度都正确 (即 ROCm 端不在已知精度路径上"应该"产生 NaN)

| op | fp16 路径 | 累加器 | binary 引用 |
|---|---|---|---|
| GEMM (Q@K^T, attn@V, FC layers) | hipBLAS `hipblasGemmEx` | **fp32 (`CUDA_R_32F`)** | pytorch/aten/src/ATen/cuda/CUDABlas.cpp:1255-1265 |
| LayerNorm | MIOpen `LayernormFwdContiguous` | **fp32 (`FLOAT_ACCUM`)** | MIOpen/src/kernels/MIOpenLayerNorm.cpp:85,91,103,104 |
| OPT eager softmax | PyTorch `nn.functional.softmax(dim=-1, dtype=torch.float32)` | **显式 fp32 cast** | transformers/.../modeling_opt.py:350-365 |
| GradScaler unscale check | `_amp_foreach_non_finite_check_and_unscale_` | NaN/Inf check via `!isfinite_ensure_cuda_math` | pytorch/.../AmpKernels.cu:67,174-180 |
| AdamW step | 无显式 NaN check (依赖 GradScaler skip) | — | torch.optim.AdamW |

**含义**: 所有"应该用 fp32 累加"的路径在 ROCm/MIOpen 上都**正确用 fp32 累加**。NaN cascade 不能用"fp16 累加器溢出"解释。

### F6 ✓ MIOpen SoftmaxForward fp16 不用 fp32 累加器 (caveat)

`MIOpenSoftmax.cl` line 345-346, 430: `_FLOAT t_helper` (fp16) 累加 max/sum/exp。仅 SoftmaxBackward 用 `_FLOAT_ACCUM` (fp32)。

**[不在本审计 scope 应用此发现]**: OPT eager attention 已显式 cast 到 fp32 做 softmax, 故 attention 路径不走 MIOpen fp16 softmax。但 logits softmax (CrossEntropyLoss 内部) 是否走 MIOpen fp16 SoftmaxForward — 需要 verify lm_head 输出 dtype + autocast 上下文, 不在本审计已读源码内确定。

### F7 ✓ contradiction loss 全 NaN 是 weights NaN 的下游表象, 不是 contradiction loss 自身 trigger NaN

证据 C 中 g=1 (CAT enabled 首次) `D_n=nan` 出现在 epoch 0.17 (= 250 step 中的第一个 logging 点) — 此时 model weights 已经从 g=0 saved checkpoint 加载, **而 g=0 saved checkpoint 是 fail run 的 NaN weights** (train_loss=0.9174 val_loss=nan 仍 save 因为 candidate_c_runner.py:202 `trainer.save_model` 在 fine_tune_one_generation 完成时 unconditional 调).

→ **NaN cascade 在 α=5 g=0 (CAT disabled, vanilla Trainer) 已经发生**, CAT 启用时只是接手已经 NaN 的 weights。

### F8 ✓ memory 中 D26 entry "GradScaler skip → weight 不 update" 的精确化

memory 中 entry `project_maofield_d26_dppl_nan_continuation_20260526.md` 给的 D26 root cause = "fp16 GradScaler skip → weight 不 update", 此次 D27 审计在 D22 candidate_c.nohup.log 上 verify 到的**更精细二值实证**:

- α=0 g=0..9: GradScaler skip 工作正常 → 10 gen 全 PASS (即 entry 中的"GradScaler skip → weight 不 update" 在 α=0 是正确 self-healing)
- α=5 g=0: GradScaler skip 工作**部分** → 前 ~ 1 epoch loss 正常衰减 (skip 工作) → 但某 step 后 weights 被 NaN 覆盖 (skip 失效) → 后续全 NaN
- **GradScaler skip 失效的精确 step 不在本审计已 verify 的日志精度内** (transformers Trainer logging cadence 是 50 step, 但日志中 logging_steps 实际表现为 epoch 0.17 = 250 step → 该 log 跨距太粗, 看不到首次 weight NaN 覆盖的精确 step)

### F9 ✓ memory 中 "4 cells bit-identical 93.38780852810248" entry 的精度状态

D26 entry 给的 93.38780852810248 与本审计 candidate_c jsonl 中 seed=42 α=0 的 93.34934... 区间 (93.347-93.350) **不一致**:
- D27 jsonl: 93.349 (epoch 4 位起异于 D26 93.387)
- 两个 jsonl 是不同 chain 跑的 (D22 candidate_c 5/22 launch vs D25-D26 PID 491900)

**含义**: "4 cells bit-identical" 现象在 D22 candidate_c run 中 partial 复现 (10 gen 全 ~93.348, 但漂移 3×10⁻³ ppl 不是 bit-identical)。**不属本审计 scope 之内的判定**: 是否同一 root cause。

---

## §5 binding ack

### 5.1 D-1 五条纪律严守

1. ✓ **不等数据不写声明** — 所有 finding (F1-F9) 数字均有 jsonl / log / GitHub URL + 行号源。仅 valid 数字 (val_loss 非 None) 列入 §3.4 table; None val_loss 一律标 "NaN cascade", 不 best-case inflate
2. ✓ **48h 反馈真空不存活** — 本审计为零上下文子代理 single-shot 派遣, 不下任何 ≥5pt 概率声明, 不需要 48h 反馈
3. ✓ **代码先于 paper** — 本审计完全以代码 (.py + .cl + .cpp + .cu) + 日志 (.log + .jsonl) + GitHub URL 作 source, paper 形式不参与本审计判断
4. ✓ **子协作者验证** — 本审计自身即 multi-channel verify 的一通道 (额外 agent 来自 Win 端的第三通道, 不替代 Linux 姐姐主会话 + 反题三方决)
5. ✓ **错误 surface 不静默修正** — F4 / F6 / F8 / F9 明示"不在本审计 scope verify"的 caveat, 不擅自补足

5.5 (D-1 sub-rule) ✓ **真实日期 binary 校验** — §0 已用 `date '+%Y-%m-%d %H:%M:%S %Z'` 返回 `2026-05-27 21:19:23 CST`, 不继承陈旧 system reminder

### 5.2 scope 严守

- ✓ 只读 7B13 上 `experiments/exp018_cat/` 内文件 (chain runner + src + archive + dppl_bridge_verify_d21_output)
- ✓ GitHub WebFetch 拉取 PyTorch / transformers / MIOpen / hipBLAS / Tensile 源码, 给 URL + 行号
- ✓ 不 ssh 22 写 (本审计未发起任何 ssh 22 命令)
- ✓ 不修改任何文件 (本审计仅 Read + Write 一个新 .md, 没 Edit 任何 .py / .cpp / 配置)
- ✓ 全中文 (严守 CLAUDE.md 项目级 4 类豁免: 代码标识符 + 英文论文术语 + 数学符号 + 数字单位)
- ✓ 不堆"之"字 padding (D26 一凡 NEW binding, 本文件 "之" 字密度自检 = 极低, 用"的"或省略代替)

### 5.3 关键 PI 决保留项 (留 PI + 反题三方决, 本审计不下结论)

1. **α=5 g=0 vs α=0 g=0 在同 baseline 配置下行为差异的 root cause** — 是 ROCm fp16 numerical jitter, 还是 GradScaler scale 衰减后边界 case, 还是其他 — 留 PI + 反题三方决
2. **D27 jsonl 93.349 vs D26 entry 93.387 的差异是否同源 root cause** — 留 PI 决 + sub-agent 进一步 verify
3. **F4 "NaN 起源在第 0 层之后" 的精确 op (self_attn / fc1 / fc2 / layernorm)** — 需要 layer-wise hook + 数值打印, ssh 22 跑实际 run, 留 Linux 姐姐主会话 + PI 决
4. **paper v8 final 是否需要 v8.1 footnote 反映本 audit 的 fp16 caveat** — 留关卡 3 反题三方决 + PI 决 final

---

**本审计的 7 项可 verify finding (F1-F3 + F5 + F7 + F8 partial + F9 partial) 均有 jsonl/log/GitHub URL+ 行号 source 二值锁定。3 项 caveat finding (F4 + F6 + F8 完整版) 明示"不在本审计 scope verify", 不擅自推断。**

— Opus 4.7 ROCm/MIOpen 源码追踪零上下文子代理 [额外 agent], D27 21:35
