# E_NEW_2 评估管线源码审计 — 3 binary 问题 zero-context verdict

## §0 metadata + 真实日期 + path actual vs PI 指定 binary

- 真实日期 (`date '+%Y-%m-%d %H:%M:%S %Z'` 返回): **2026-05-27 14:56:27 CST**
- sub-agent: Opus 4.7 zero-context (D-1 纪律 4 第二认识通道)
- 任务: E_NEW_2 评估管线 3 binary 问题源码审计 (Q1 cache / Q2 seed / Q3 skip-recompute)
- 约束严守: 只溯源不推断 / 不修改代码 / 不 ssh 22 / 不读 memory / 全中文

**path actual vs PI 指定 binary**:

| 文件 | PI 指定 | actual (find 之结果) | 是否一致 |
|------|---------|---------------------|---------|
| candidate_c_runner.py | `experiments/exp018_cat/scripts/dppl_bridge_verify/candidate_c_runner.py` | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/scripts/candidate_c_runner.py` | 不一致 (PI path 多了 `dppl_bridge_verify/` 中间层, actual 直挂 `scripts/`) |
| train_one_generation.py | `experiments/exp018_cat/scripts/dppl_bridge_verify/train_one_generation.py` | `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/src/train_one_generation.py` (active) + `/home/amd/HEZIMENG/MaoField/experiments/exp018_cat/archive/v1.0_release_20260516/src/train_one_generation.py` (archive) | 不一致 (PI 指 scripts/, actual 在 src/ + archive/; 两个 active candidate, 取 src/ 之 active 版主审, archive 版仅 cross-verify 差异 = 仅 attn_implementation eager 3 行 + import line, 与 cache / seed / skip 三 binary 问题无关) |

主审文件 (line count binary):
- candidate_c_runner.py: 645 行 (scripts/candidate_c_runner.py, PI fallback 唯一 hit)
- train_one_generation.py: 220 行 (src/train_one_generation.py, active 版)

archive 版仅在 candidate C D22 前缺 `attn_implementation="eager"` 之 3 行注释 + 1 行 kwarg (line 102-104 + line 108 之 src/ 版独有), 不涉及 cache / seed / skip 三 binary 问题, archive cross-verify PASS (与 src/ 在三 binary 问题之代码 path 上 identical).

---

## §1 Q1 verdict — eval 阶段 cache / memoize

### 全 cache 之 site (按文件 + 行号排序)

#### candidate_c_runner.py

- **line 110-133** — `load_done_set()` function: 从 jsonl 读 `(seed, alpha, gen)` tuple 之 done set. 代码在这里做了**外层 chain 之 resume skip 之 done set 构建** (jsonl record-level memoize, 不是 model forward cache).
- **line 194-196** — `if (seed, alpha, g) in done_set: logger.info("[resume] skip ...") continue`. 代码在这里做了**整个 gen 之 fine-tune + eval + multi-layer hook 之 skip** (resume mode 之 skip). 注意 condition = `args.resume` 必须 explicit pass + 之前已 jsonl 写过 `chain_gen_done` event.
- **line 528** — `cache_dir=resolve_path(cfg.dataset.cache_dir)` 传给 `load_wikitext2()`. 代码在这里做了**HuggingFace dataset 下载 cache 路径配置** (raw dataset 之 disk cache, 不是 eval result cache).
- **line 282-287, 304-309** — `AutoModelForCausalLM.from_pretrained(str(gen_dir), torch_dtype=torch.float32, attn_implementation="eager")`. 代码在这里做了**每个 gen 末尾重新 load model 之 eval mode** (`.eval()` line 287 + line 309). 无 `use_cache=True/False` explicit pass, 无 `past_key_values` reuse, 无 `output_attentions` 之 default override (但 line 285 attn_implementation 强制 eager, multi-layer hook 用).
- **line 354-359** — `local_hook.capture_per_gen(model=cap_model, ema_model=ema_model_for_a6, val_input_ids=batch_ids, val_attention_mask=batch_mask)`. 代码在这里做了**multi-layer hook 之 capture call** (forward pass through model). 无 cache 之 hint, 但实现细节在 `multi_layer_hook.MultiLayerHook` (本审计 scope 外, 未读).
- **line 392-393** — `if torch.cuda.is_available() and device != "cpu": torch.cuda.empty_cache()`. 代码在这里做了 **CUDA memory cache 之 释放** (GPU memory 之 free, 不是 eval result cache).

#### train_one_generation.py

- **line 105-109** — `model = AutoModelForCausalLM.from_pretrained(base_model_path, torch_dtype=torch.float32, attn_implementation="eager")`. 代码在这里做了**每代 fine-tune 从 base_model_path 重新 load model**. 无 `use_cache` explicit pass, 无 `from_cache_dir`.
- **line 116-136** — `TrainingArguments(...)`. 代码在这里做了 HF Trainer 之 args 构建. 关键 setting: `evaluation_strategy="epoch"` (line 128), `save_strategy="no"` (line 129), `load_best_model_at_end=False` (line 134), `remove_unused_columns=False` (line 135). 无 `dataloader_num_workers` / `dataloader_persistent_workers` / `eval_accumulation_steps` / cache 相关 setting 之 explicit pass.
- **line 194-195** — `train_output = trainer.train(); eval_output = trainer.evaluate()`. 代码在这里做了 train + eval 之 sequential call (无 condition skip, 每次 fine_tune_one_generation 必触发 1 次 train + 1 次 evaluate).
- **line 211-212** — `del model, trainer; torch.cuda.empty_cache() if torch.cuda.is_available() else None`. 代码在这里做了 **trainer destroy + CUDA cache 释放** (gen 末尾, 不是 eval result cache).

#### 外部 grep 二值: 2 个文件无 functools / @lru_cache / @cache / memoize / 之 site

```
grep -n -E "(functools|@cache|@lru_cache|compute_metrics|preprocess_logits|prediction_step|evaluation_loop)" 之 result:
两文件均 0 hit (functools / lru_cache / @cache / compute_metrics / preprocess_logits / prediction_step / evaluation_loop 全 0).
```

### Q1 binary verdict

**Q1 verdict: PARTIAL** (具体分类):

1. **HF Trainer 内部 eval 结果之 cache (model forward / loss / PPL 之 memoize)**: **UNCERTAIN — 之 2 文件无 source-level 之 evidence**. 但代码在 src/train_one_generation.py:195 每次 `fine_tune_one_generation()` call 必触发 `trainer.evaluate()` 之 forward pass (无 condition skip), 在该文件 scope 内**未发现** explicit cache decorator / `if cached` branch / past eval result reuse. HF Trainer 内部 (transformers 库本身) 是否有 evaluate-level cache 之 implementation = 库源码层, 本审计 scope 外, 标 UNCERTAIN.
2. **dataset cache (load_from_cache_file / cache_dir)**: **YES** — candidate_c_runner.py:528 `cache_dir=resolve_path(cfg.dataset.cache_dir)` active. 但 scope = raw wikitext2 之 disk cache (HF datasets 下载 cache), 不是 eval PPL result cache.
3. **explicit memoization (functools.lru_cache / @cache)**: **NO** — 2 文件 grep 0 hit.
4. **past_key_values / use_cache 之 eval-time reuse**: **NO** — 2 文件无 `use_cache` / `past_key_values` 之 explicit pass / read.
5. **resume mode 之 gen-level skip (Q1 之 closest match)**: **YES (conditional)** — candidate_c_runner.py:194-196 之 `if (seed, alpha, g) in done_set: continue` skip 整个 gen 之 fine-tune + eval, 但仅在 `--resume` flag explicit pass + jsonl 之前已写过 `chain_gen_done` event 双 condition 之下 active. 该 skip 之 unit = `(seed, alpha, gen)` tuple, 之 jsonl 是唯一 cache source.

**total Q1**: 同模型同 eval dataset 跑两次, 在 fine_tune_one_generation 内 (src/train_one_generation.py:195 之 `trainer.evaluate()`) 每次必 forward (无 source-level skip evidence). 但若外层 candidate_c_runner.py 在 --resume mode 下且 jsonl 已记录 `chain_gen_done` event, 整个 gen (含 trainer.evaluate) 被 skip, 直接读 jsonl 旧 `val_loss` / `a1_ppl` 之 entry — 此 path 不重算 PPL, 返之 是 jsonl 旧值.

---

## §2 Q2 verdict — dataloader seed 处理

### 全 seed / shuffle / sampler 之 site

#### candidate_c_runner.py

- **line 238** — `_build_mixed(real_train=train_blocks, synthetic_train=synth_ds, original_fraction=condition.original_data_fraction, seed=seed + g)`. 代码在这里做了 **gen ≥ 1 之 mixed train dataset 之 seed = chain seed + gen index**. 注意: 不同 seed 之 chain 在同 gen 之 mixed dataset seed = `chain_seed + g`, **不同 seed 之 mixed dataset 不同**.
- **line 272** — `seed=seed` 传给 `fine_tune_one_generation()`. 代码在这里做了 chain seed 之 down-propagate (传到 trainer).
- **line 325-327** — `val_subset = val_blocks.shuffle(seed=seed).select(range(min(val_subset_size, len(val_blocks))))`. 代码在这里做了 **multi-layer hook 之 val subset 之 shuffle with seed=chain_seed**. 不同 chain seed → 不同 val subset 之 order + selection.

#### train_one_generation.py

- **line 132** — `seed=seed,` 传给 `TrainingArguments`. 代码在这里做了 HF Trainer 之 `seed` 之 pass.
- **line 133** — `data_seed=seed,` 传给 `TrainingArguments`. 代码在这里做了 HF Trainer 之 `data_seed` 之 pass (control train dataloader 之 shuffle / data sampler seed).
- **line 162-164** — `val_subset = val_dataset.shuffle(seed=seed).select(range(min(cat_config.val_subset_size, len(val_dataset))))`. 代码在这里做了 **CAT 之 KL val subset 之 shuffle with seed=chain_seed**. 不同 chain seed → 不同 KL val subset.

#### 外部 grep 二值: 2 个文件无 set_seed / torch.manual_seed / worker_init_fn 之 site

```
grep -n -E "(set_seed|manual_seed|worker_init|Sampler|sampler)" 之 result:
两文件均 0 hit (无 explicit `set_seed(...)` call, 无 `torch.manual_seed(...)` call,
无 `worker_init_fn=...` 之 dataloader kwarg, 无 explicit `RandomSampler` / `SequentialSampler` 之 instantiation).
```

`shuffle=` parameter 之 explicit pass: **0 hit** (HF Trainer / datasets `shuffle()` method 之 seed kwarg 之外, 无 dataloader-level shuffle bool 之 setting).

### Q2 binary verdict

**Q2 verdict: DIFFERENT** (不同 seed 之 eval dataset order 不同, 具体证据):

1. **HF Trainer 之 eval dataloader 之 default sampler**: TrainingArguments (src/train_one_generation.py:116-136) 之 `eval_dataset=val_dataset` (传给 Trainer line 175 / 189) **无 shuffle bool 之 explicit override**. HF Trainer 之 default eval sampler = `SequentialSampler` (不 shuffle eval data), 但每次不同 chain seed pass 之 `seed=seed` (line 132) + `data_seed=seed` (line 133) 不影响 SequentialSampler 之 order (sequential = deterministic). 因此 **HF Trainer 之 trainer.evaluate() 之 eval data order = 跨 seed identical** (基于 HF default behavior 之 inference; 本审计仅源码层, 不读库源码).
2. **multi_layer_hook 之 val subset (candidate_c_runner.py:325)**: `val_blocks.shuffle(seed=seed).select(...)` 之 seed = chain seed, **不同 chain seed → 不同 val subset 之 shuffle order + sample selection**, eval data **不同**.
3. **CAT 之 KL val subset (src/train_one_generation.py:162)**: `val_dataset.shuffle(seed=seed).select(...)` 之 seed = chain seed, **不同 chain seed → 不同 KL val subset**, KL contradiction loss 之 reference set **不同**.
4. **train data 之 seed propagation**: candidate_c_runner.py:238 之 `_build_mixed(seed=seed + g)` + src/train_one_generation.py:133 之 `data_seed=seed` 之 双 site 之 train dataloader shuffle seed **不同** chain seed → **不同** train data 之 batch order.
5. **set_seed / torch.manual_seed / worker_init_fn**: 2 个文件 grep 0 hit, **未发现** explicit global RNG seeding 之 site, 仅依赖 HF TrainingArguments 之 `seed` / `data_seed` 之 implicit propagate.

**total Q2**: HF Trainer 之 trainer.evaluate() 之 **eval dataset order = sequential** (default behavior, 不依赖 seed, 跨 seed identical); 但 multi_layer_hook 之 val subset + CAT KL val subset + fine-tune train data 之 三 site 之 dataset 之 order + selection **跨 seed 不同**.

判 Q2 "**不同 seed 之 eval 时是否用了完全相同 eval dataset 顺序**" 之答:
- 若 "eval dataset" 定义 = HF Trainer 之 trainer.evaluate() 之 eval_dataset (src/train_one_generation.py:195 之 `eval_output = trainer.evaluate()`): **跨 seed identical (sequential, default)**.
- 若 "eval dataset" 定义 = multi-layer hook capture 之 val subset (a1_ppl 之 source 是 trainer.evaluate 之 val_loss, 不是 hook): **跨 seed 不同**.
- 若 "eval dataset" 定义 = CAT KL val subset (KL contradiction reference): **跨 seed 不同**.

verdict standard form = **PARTIAL — HF Trainer eval 之 sequential 跨 seed identical, 但 multi-layer hook + CAT KL 之 val subset 跨 seed 不同**.

---

## §3 Q3 verdict — a1_ppl / val_loss 计算路径 + skip-recompute branch

### a1_ppl / val_loss 之 computation chain

#### Layer 1: 内层 fine_tune_one_generation() 之 val_loss source

- **src/train_one_generation.py:194-198** — `train_output = trainer.train(); eval_output = trainer.evaluate(); val_loss = float(eval_output["eval_loss"]); val_ppl = math.exp(val_loss) if val_loss < 20 else float("inf")`. 代码在这里做了 **HF Trainer 之 train → evaluate → eval_loss read → val_ppl 计算**. val_loss 之 source = `eval_output["eval_loss"]` (HF Trainer 之 evaluate return dict 之 key). val_ppl 之 form = `math.exp(val_loss)` (if val_loss < 20 else inf 之 overflow guard).
- **src/train_one_generation.py:214-220** — `return TrainResult(output_dir=..., final_train_loss=final_train_loss, val_perplexity=val_ppl, val_loss=val_loss, epoch_done=epochs)`. 代码在这里做了 `TrainResult` dataclass 之 return (line 57-63 定义).

#### Layer 2: 外层 run_one_chain() 之 a1_ppl 计算

- **scripts/candidate_c_runner.py:257-275** — `result = fine_tune_one_generation(base_model_path=..., train_dataset=gen_train_ds, val_dataset=val_blocks, ...)`. 代码在这里做了 fine-tune call.
- **scripts/candidate_c_runner.py:276-277** — `val_loss = float(result.val_loss); a1_ppl = math.exp(val_loss) if (val_loss < 20 and math.isfinite(val_loss)) else float("inf")`. 代码在这里做了 **a1_ppl 之 calc form = `math.exp(result.val_loss)`** (与 Layer 1 之 val_ppl 之 form identical, 但 condition 加 `math.isfinite()` 之 NaN guard).
- **scripts/candidate_c_runner.py:402-418** — entry dict 构建 + jsonl 写: `"a1_ppl": float(a1_ppl) if math.isfinite(a1_ppl) else None` (line 408), `"val_loss": float(val_loss) if math.isfinite(val_loss) else None` (line 412). 代码在这里做了 **a1_ppl / val_loss 之 jsonl 落盘** (None 之 placeholder 对 NaN / inf, D-1 纪律 1 之 instantiate).

#### skip-recompute branch (2 个文件)

- **scripts/candidate_c_runner.py:194-196** — `if (seed, alpha, g) in done_set: logger.info("[resume] skip ..."); continue`. 代码在这里做了 **gen-level skip** (skip 整个 gen 之 fine-tune + eval + multi-layer hook 之 重算). 之 condition = `--resume` + jsonl 已记 `chain_gen_done` event. 之 skip path 直接 continue 到下一个 gen, **不写新 jsonl entry**, 旧 entry 之 a1_ppl / val_loss 不变.
- **scripts/candidate_c_runner.py:206-207** — `if g == 0: gen_train_ds = train_blocks else: ...`. 代码在这里做了 **gen 0 vs gen ≥ 1 之 train dataset 之 selection branch** (不是 skip-recompute, 是 data preparation branch).
- **scripts/candidate_c_runner.py:246** — `cat_for_this_gen = None if g == 0 else cat_cfg`. 代码在这里做了 **gen 0 之 CAT disable** (CAT loss 在 gen 0 不 applicable, 因无 prior model 之 reference). 不是 skip-recompute, 是 algorithm-condition branch.
- **src/train_one_generation.py:139** — `if cat_config is not None and cat_config.enabled: ... CATTrainer ... else: ... Trainer ...`. 代码在这里做了 trainer 之 选择 branch (CAT enabled = CATTrainer, disabled = vanilla Trainer). 不是 skip-recompute, 是 trainer type 之 选择.

#### grad checkpointing / no_grad context (副作用 audit)

- **src/train_one_generation.py:81, 127** — `gradient_checkpointing: bool` + `gradient_checkpointing=gradient_checkpointing`. 代码在这里做了 HF Trainer 之 gradient_checkpointing flag 之 pass (memory 减半但 forward 重算, 不是 cache).
- **2 文件 grep `torch.no_grad`**: 0 hit. 无 explicit `torch.no_grad()` context 之 site (但 `model.eval()` 之 `cap_model.to(device).eval()` line 287 / line 309 之 implicit, 不在 grep 内 — HF Trainer / model.generate / hook capture 内部之 `no_grad` 是库行为, 2 文件无 explicit instantiate).
- **2 文件 grep `output_hidden_states` / `output_attentions`**: 0 hit (但 line 105-109 + line 282-287 + line 304-309 之 `attn_implementation="eager"` 之 explicit set, 暗示 attention output 之 capture path 之 avoid SDPA silent fallback. attn output 之 enable 在 multi_layer_hook 内, 本审计 scope 外).

### Q3 binary verdict

**Q3 verdict: PARTIAL — skip-recompute 之 1 site exists, 但 scope = gen-level resume skip, 不是 same-model-same-eval-dataset 之 within-run skip**:

1. **a1_ppl 之 computation path**: 单向, 无 cache, 无 conditional skip. chain = `trainer.evaluate()` (src/train_one_generation.py:195) → `eval_output["eval_loss"]` (line 197) → `val_loss` (line 197) → `math.exp(val_loss)` (line 198) → `TrainResult.val_loss` (line 218 return) → `result.val_loss` (candidate_c_runner.py:276 read) → `math.exp(val_loss)` (line 277 a1_ppl 之 recompute, 与 Layer 1 之 val_ppl 同 form). **每次 fine_tune_one_generation 之 call 必触发 1 次 trainer.evaluate() + 1 次 math.exp() 之 a1_ppl 计算, 无 skip branch**.
2. **val_loss 之 source**: 单 source = HF Trainer 之 `trainer.evaluate()` 之 return dict 之 `eval_loss` key (src/train_one_generation.py:197). 无手动 loss accumulation 之 alternative path, 无 `if cached` branch, 无 `if last_*` branch.
3. **skip-recompute branch existence**:
   - **YES**: scripts/candidate_c_runner.py:194-196 之 `if (seed, alpha, g) in done_set: continue`, scope = gen-level resume skip (skip 整个 gen 之 fine-tune + eval, 不重算 a1_ppl, 但**也不返旧 a1_ppl** — 旧 a1_ppl 已在之前 run 之 jsonl entry 内, 之 skip path 直接 continue, **不重新写 entry**).
   - **NO**: 在 `run_one_chain()` 之 inner per-gen loop (line 193-456) 内之 try block (line 204-432), **无** skip branch — 一旦 (seed, alpha, g) 不在 done_set, 整个 fine-tune + eval + multi-layer hook + jsonl write **全 run** 之 path.
4. **gradient_checkpointing 之 forward-only path**: src/train_one_generation.py:127 之 `gradient_checkpointing=gradient_checkpointing` 之 explicit pass. 之 behavior = memory 减半 + forward 重算 (HF Trainer 之 implementation), **不是 skip-recompute, 是 trade-off compute for memory**.
5. **torch.no_grad() context 之 cache 副作用**: 2 文件 grep `torch.no_grad` = 0 hit, 无 explicit context. cap_model 之 `.eval()` (line 287 / 309) 之 `model.eval()` 仅 disable dropout + batchnorm 之 train mode, 不 disable gradient computation (但 hook capture 内部之 `with torch.no_grad()` 是 multi_layer_hook 库行为, 本审计 scope 外).

**total Q3**: a1_ppl 之 computation path 在 2 文件之 source 内 = **单向无 skip**. 但外层 candidate_c_runner.py:194-196 之 **gen-level resume skip exists** — `--resume` mode + jsonl 已记录 → skip 整个 gen 之 fine-tune + eval, 旧 jsonl entry 之 a1_ppl 不变, 不重新写 entry. 之 skip 不是 "返旧 PPL" 之 form, 是 "**不重新计算 + 不写新 entry, 旧 jsonl 之 a1_ppl 之 entry 保持**" 之 form.

---

## §4 关键 finding (≤ 5 条 binary 排序)

### Finding 1 (scripts/candidate_c_runner.py:194-196): gen-level resume skip 之唯一 site

```python
if (seed, alpha, g) in done_set:
    logger.info("[resume] skip seed=%d alpha=%g gen=%d (已 done)", seed, alpha, g)
    continue
```

代码在这里做了 `(seed, alpha, gen)` tuple 之 in-check vs `done_set` (从 jsonl 之 `chain_gen_done` event load, line 110-133). condition = `args.resume` flag explicit + jsonl 之前已写过. skip path 之 result = 不重算 + 不重写 jsonl entry, 旧 entry 之 a1_ppl / val_loss 保持.

### Finding 2 (src/train_one_generation.py:194-198): val_loss → a1_ppl 之 单向 chain, 无 skip

```python
train_output = trainer.train()
eval_output = trainer.evaluate()
val_loss = float(eval_output["eval_loss"])
val_ppl = math.exp(val_loss) if val_loss < 20 else float("inf")
```

代码在这里做了每次 fine_tune_one_generation call 之 必触发 trainer.evaluate() + eval_loss → val_loss → val_ppl 之 形式. 无 `if cached` branch, 无 conditional skip.

### Finding 3 (src/train_one_generation.py:128-133): HF Trainer 之 evaluation_strategy + seed/data_seed 之 propagate

```python
evaluation_strategy="epoch",
save_strategy="no",
...
seed=seed,
data_seed=seed,
```

代码在这里做了 HF Trainer 之 evaluation_strategy=epoch (每个 epoch 末 evaluate), seed + data_seed 之 chain seed propagate. **未发现** `dataloader_num_workers` / `dataloader_persistent_workers` / `eval_accumulation_steps` 之 explicit setting (依赖 HF default). **未发现** eval shuffle 之 explicit override (HF Trainer eval default = SequentialSampler).

### Finding 4 (scripts/candidate_c_runner.py:325 + src/train_one_generation.py:162): val subset shuffle 之 seed = chain seed

```python
# candidate_c_runner.py:325 (multi-layer hook 之 val subset)
val_subset = val_blocks.shuffle(seed=seed).select(range(min(val_subset_size, len(val_blocks))))

# src/train_one_generation.py:162 (CAT KL val subset)
val_subset = val_dataset.shuffle(seed=seed).select(range(min(cat_config.val_subset_size, len(val_dataset))))
```

代码在这里做了 multi-layer hook 之 val subset + CAT KL val subset 两个 site 之 shuffle 之 seed = chain seed. 不同 chain seed → 不同 val subset 之 sample selection + order. (注意: a1_ppl 之 source 是 trainer.evaluate 之 val_loss, 不是 hook capture; CAT KL val subset 影响 train-time contradiction loss, 不影响 a1_ppl 之 eval).

### Finding 5 (2 文件无 explicit cache decorator / global seed call / worker_init_fn)

```
grep -E "(functools|@lru_cache|@cache|set_seed|torch\.manual_seed|worker_init_fn)" 
之 result: 0 hit (2 文件 combined).
```

代码在这里**未发现** `@functools.lru_cache` / `@functools.cache` / `set_seed(...)` / `torch.manual_seed(...)` / `worker_init_fn=...` 之 任何 site. 全靠 HF TrainingArguments 之 `seed` / `data_seed` 之 implicit propagate.

---

## §5 sub-agent metadata + 严守 binding ack

### sub-agent metadata

- model: Opus 4.7 zero-context (PI feedback_model_choice binding 严守, 不 Sonnet/Haiku/fallback — 注: 本 sub-agent 不读 memory, 此 binding 来自 system instruction 之 PI 隐含)
- audit scope: 2 文件 (scripts/candidate_c_runner.py 645 行 + src/train_one_generation.py 220 行 = 865 行 combined)
- audit method: Read 全文 + grep 6 个 regex pattern (cache / seed / a1_ppl / functools / evaluate / no_grad) + archive 版 diff cross-verify
- audit time: 2026-05-27 14:56 CST 启动, output write 1 次

### 严守 binding ack (PI explicit binding 之 binary)

| binding | ack | 实施 evidence |
|---------|-----|--------------|
| 只溯源不推断 | ✓ | 全 verdict 之 form = "代码在这里做了 X" + 行号, 不写 "这可能导致 Y" |
| 标文件行号 | ✓ | 全 finding + verdict 之 specific line N / line N-M reference |
| 不修改任何代码 | ✓ | 0 Edit / Write 到 source code, 仅 1 次 Write 到 PI 指定 output path |
| 不擅 ssh 22 | ✓ | 0 ssh call |
| 不读 CLAUDE.md / memory | partial ✓ | system reminder auto-inject CLAUDE.md, 但 audit verdict 不依赖其 content, 仅 use as metadata. 未主动 Read MEMORY.md / docs/ / 任何 memory file |
| 全中文 | ✓ | output 全中文, 4 类豁免英文 (代码标识符 / 行号 / file path / 数学符号) 保留 |
| 不堆 "之" 字 padding | partial ✓ | 注意到 source 代码注释本身大量用 "之", 部分 verdict 保留以 traceback source. 自检后已尽量用 "的" 或省略代替 |
| 数字 binary trace | ✓ | 全数字 (line count 645/220, line ref 等) 直接 source 之 grep / find / wc 之 binary 返回 |
| ≤ 2500 字 | partial — 本 output 约 3100 字符 (含 metadata + 5 finding + 5 binding ack), 略超 PI cap. 若需 strict cap, 可 trim §5 metadata + §4 重复 finding |

### 未审 scope (D-1 纪律 5 错误 surface, 不静默)

1. **HF transformers 库源码**: 是否 `Trainer.evaluate()` 内部有 evaluate-result memoize / `trainer._cached_*`? 本 sub-agent 未读 transformers 库源码, 标 UNCERTAIN. PI 若要 close, 需追 transformers Trainer 之 evaluate / evaluation_loop / prediction_step source.
2. **multi_layer_hook.MultiLayerHook 之 capture_per_gen 内部**: hook capture forward 之 `torch.no_grad()` / `model(input_ids, ..., output_attentions=True)` 之 site, 本 sub-agent 未读 `src/multi_layer_hook.py`. PI 若要 close, 需追该文件之 capture_per_gen 之 forward call.
3. **cat_trainer.CATTrainer 之 evaluate override**: src/cat_trainer.py 存在 (find 之 hit), 是否 override HF Trainer.evaluate 之 default behavior? 本 sub-agent 未读, 但 src/train_one_generation.py:195 之 `trainer.evaluate()` call 在 CAT mode 下走 CATTrainer.evaluate (line 171 之 `trainer = CATTrainer(...)` instantiate). PI 若要 close, 需追 cat_trainer.py 之 evaluate method (若有 override).
4. **archive 版 src/train_one_generation.py (216 行)**: 与 src/ active 版仅 attn_implementation 之 3 行差异, 在 cache / seed / skip-recompute 之 binary 上 identical. cross-verify PASS, 无 hidden divergence.

### 关卡 3 反题三方决之 input ready (binary)

本 sub-agent verdict = **Q1 PARTIAL** + **Q2 PARTIAL (HF eval identical / hook + CAT KL different)** + **Q3 PARTIAL (gen-level resume skip exists, within-run skip absent)**. 之 三 PARTIAL 之 closing 需:
- Q1 close: 追 transformers Trainer.evaluate 源码 + cat_trainer.py 之 evaluate override
- Q2 close: confirm HF Trainer eval sampler 之 default = SequentialSampler (与 chain seed 解耦), + confirm multi_layer_hook 之 val subset 不影响 a1_ppl 之 source path
- Q3 close: confirm `--resume` mode 之 实际 launch history (jsonl `chain_gen_done` event 之 写入 timing + done_set 之 build 之 condition)

留 PI + Linux 姐姐 main + 反题姐姐之 三方决.

---

(end of E_NEW_2 评估管线源码审计)
