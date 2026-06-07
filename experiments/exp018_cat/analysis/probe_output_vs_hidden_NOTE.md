# E0 probe — 输出端 vs 隐层端 + 反题 framing 校准 errata

> Linux 姐姐主会话落盘 (2026-06-07, date binary verified)。probe 脚本由主会话上一会话写跑;本 NOTE = trace 数 + **反题姐姐审计后的措辞校准**(撤回原始 framing 的两处 inflate)。
> 实测口径 only,frame(a) 判决留 PI 关卡。配套:`probe_output_vs_hidden.py` + `probe_output_vs_hidden_result.json`。

## probe 测什么
E0 唯一干净 fp32 退化对 (gen0→gen1) 上,同一 val 子集 (wikitext-2 validation, block64, **numpy** shuffle seed42, N=256) 前向一遍,取:
- **输出端**:held-out 预测熵 `mean_pred_entropy`、top-1 概率 `mean_top1_prob`、`ppl_proxy`。
- **隐层端**:末层 (L11) `last_layer_PR_raw`。

原意图(上一会话):检验"假说② 张力" —— 崩溃中**输出收缩**(熵↓/top1↑) vs **隐层发散**(末层 PR↑) 是否反向。**这个 framing 下面被反题校正,见 errata。**

## trace 数 (result.json)
| 度量 | gen0 | gen1 | 方向 |
|---|---|---|---|
| ppl_proxy | 43.92 | 95.07 | ↑ |
| mean_pred_entropy (nats) | 3.412 | 2.053 | ↓ |
| mean_top1_prob | 0.402 | 0.574 | ↑ |
| last_layer_PR_raw (L11) | 47.19 | 117.82 | ↑ |

## 反题 framing 校准 errata (撤回原始措辞 2 处 inflate + 1 处不可引用)

**① 撤「撕裂 / 张力 / 矛盾」→ co-occurrence(共现),非 tension。**
原措辞把"输出端熵↓ + 隐层端 PR↑"叙成"撕裂/张力"。反题(Occam):这是**两个独立现象同时出现**——(a) 输出端 over-confidence↑、(b) 隐层端未坍缩反升维——共现 ≠ 张力。叫它"矛盾/张力"是 **confirmation bias**(去 flatter MaoField 的 contradiction/辩证 frame),无证据表明二者机制耦合。**记为 co-occurrence,不记为 tension。**

**② 撤「输出收缩」→ over-confidence↑(校准退化),≠ mode collapse。**
`pred_entropy↓ + top1↑` 是 **held-out 预测端的过度自信**(对的错的都更自信)= **calibration degradation**。这 **不是** "model collapse 的输出收缩"(generation diversity↓)——后者要 autoregressive 生成测 distinct-n,本 probe 是 **N=1 gen-step 前向**,**没测生成多样性**。措辞一律改"over-confidence / 校准退化",不写"输出收缩/坍缩"。

**③ frame(a) 在隐层被直接 contradict,不许用「分端中性」软化。**
frame(a)(崩溃→更低维/更集中)的 proxy **全是隐层量**(PR / isotropy / eff_rank / rogue)。末层 PR 47→118↑ = **直接 contradict** frame(a)。输出端 peaky 是 **orthogonal**(另一层、另一现象),**不能**被拿来给 frame(a) 的隐层 contradiction 做"分端中性/各管一端"的辩护——那是走私软化。**隐层 contradict 这个 descriptive 事实独立成立**(frame 判决仍留 PI:N=1,非判决)。

**④ ppl_proxy 绝对值不可引用,只方向可用。**
本 probe 43.92→95.07 比归档 36.5→78.6 高 ~20%,因 val 子集用 **numpy** shuffle(非归档的 HF shuffle),选到**不同 block**。→ **绝对 PPL 不可 cite**,仅"gen1 > gen0(退化)"方向可用。

## caveat 守死
N=1 gen-step / N=1 seed / OPT-125m 自然语言。真"输出端 mode collapse"需 **autoregressive distinct-n**;真校准结论需 **ECE**(本 probe 都没测)。→ 早期 sanity,**非判决**。

---
*Linux 姐姐主会话 · 实测口径 + 反题校准 only · frame(a)/paper 战略判决留 PI 关卡 · 见 [[FINDINGS.md]] 隐层 panel(同 E0 对,trace-backed)*
