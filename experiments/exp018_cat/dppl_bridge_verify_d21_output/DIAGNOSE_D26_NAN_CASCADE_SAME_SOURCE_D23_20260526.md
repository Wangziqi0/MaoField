# D26 NaN Cascade = D23 Phase 2 Same-Source Binary Verdict

**D26 11:35 sub-agent zero-context diagnose (7 分钟, 28 tool uses)**

## Binary Verdict

D26 NaN cascade (PID 491900) 与 D23 Phase 2 NaN 爆炸 = 同一根源。不是新机制。

- root cause: fp16 GradScaler silent skip → optimizer.step 被跳过 → 权重不更新 → 每个 gen 出 NaN
- 158/180 chain_gen_done (87.8%), 127 null (80.4%) + 31 valid (19.6%)
- 34 分钟/gen 是 fp16 chain training 的正常节奏（Volterra K=9 metric capture 占大头），不是重试循环（修正我 L1 的误判）

## 五种同源证据

1. nohup 日志逐字匹配 (loss=0.0, grad_norm=nan, eval_loss=nan)
2. MATH_VERIFY mechanism 持续实例化（4 单元比特级相同作为二进制证据）
3. NaN 传播到 α=0 在 D23 已出现
4. 种子特定数据排序数学推导保持一致性（seed=271 = 论文 N=6 最后一个种子）
5. CAT/Volterra K=9 假说已被 MATH_VERIFY §3.2/§3.5 排除

## 对我 L1 表面信息的校正

我之前 surface 的 PID 491900 NaN cascade stuck in retry loop / α continue 没意义是误判。
34 分钟/gen 是 fp16 链训练的正常节奏，不是饥饿重试。

## 对 α/β/γ 选择的影响

| 选项 | 成本 | 时间线 | 增量价值 |
|---|---|---|---|
| α continue | ~10h | D26 ~21:00 完成 | 完整 jsonl 目录 + 未来 D60+ ROCm caveat 分析的 180 链完整数据 |
| β fp32 重跑 | 7.5-10 天 | 远超 D29 | 低（论文 v8 归档不受影响，且 22 端 D25 已验证 fp32+gc 也 NaN） |
| γ 撤回 | 0 | 即时 | 丢失 D-PPL 桥数据 |

子代理倾向：α > β > γ。留关卡 3 反题三方决。

## 跨通道一致性

- 子代理裁判 + 22 端自身检查 + 我的校正：全部指向同一根源
- 5060 fp32 SMOKE_E0（36.536/78.572 双代健康）= 干净路径独立确认
- NaN 是 9070XT ROCm 栈特异的——不是通用算法性问题

---

**写入人**: 7B13 Linux 姐姐  
**提交人**: 7B13 Linux 姐姐 D26 ~13:30  
**审查人**: 待关卡 3 反题三方决
