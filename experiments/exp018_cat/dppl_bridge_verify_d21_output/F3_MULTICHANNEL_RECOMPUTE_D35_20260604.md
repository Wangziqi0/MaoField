# F3 多通道复核 + 数学理论延伸 — cycle 1 findings

> **辅助 agent 产出**(PI + 辅助 agent 实践多通道研究 cycle 1)。差异日志(D-1 纪律 5)。
> **status**: 中间交付,涉及 paper v8.1 footnote → 留 PI / 关卡 3 三方决。**未动 STATE.md、未 git**(单点写权 = 主会话)。
> **日期**: 2026-06-04(D35),date binary verified。
> **方法**: 主协作者复算 anchor + 通道 A(algo-verify,Opus,零上下文独立复算)+ 通道 B(paper-review,Opus,数学理论延伸)。三通道 cross。

---

## §0 一句话裁定

**F3(α=10 contradiction-loss vs α=0 baseline,plateau test-ppl)= inconclusive(p=0.70–0.818,三算法方向一致,无显著效应),且 inconclusive 是 underpowered(power≈5–6%,80% power 需 N≈245–470)的数学必然,不构成 framework 有效/无效任一方的证据。seed0 排除经查为 infrastructure OOM(rc=137),MCAR,非 α divergence → N=4 listwise ≈ unbiased,不存在 selection bias。** [综合证据等级:高]

---

## §1 F3 真相结构(source trace)

- **预注册 convention** = seeds [0,1,2,3,4](`D4_binary_pre_registration`,PI Option A,N=5)。
- **实际 chain_logs** = seeds {0,1,2,3,4,42} × {α=0,α=10}(archive `v1.0_release_20260516/chain_logs/`)。
- **paper v8 F3** 实际 = N=4 paired(convention 内排除 broken seed0),`MAOFIELD_FULL_DATA_AUDIT §10.2 line 506-509`。
- **D28 audit** = gen9 单点 + unpaired Welch(α0 N=5 vs α10 N=4),`D28_EXPERIMENTAL_DEEP_AUDIT §3.1`。
- 指标 = `test_perplexity`,plateau = gen 6–9 mean,diff = α10 − α0(负 = α10 更优)。

## §2 三算法复算(主协作者 + 通道 A 逐位一致)

per-seed plateau(gen6-9 mean)test_ppl:

| seed | α0 | α10 | diff(α10−α0) | 备注 |
|---|---|---|---|---|
| 0 | 54.889 | **broken** | — | α10 rc=137 OOM,排除 |
| 1 | 59.837 | 57.325 | −2.511 | |
| 2 | 54.031 | 58.254 | +4.223 | outlier(dominate variance) |
| 3 | 54.335 | 54.013 | −0.322 | |
| 4 | 57.351 | 54.300 | −3.051 | |
| 42 | 57.414 | 56.428 | −0.986 | convention 外,valid |

| 算法 | 指标 | 配对 | N | t | df/Welch-df | p(two) | verdict |
|---|---|---|---|---|---|---|---|
| **paper v8 F3** | plateau | paired | 4 (s1-4) | −0.251 | 3 | **0.818** | n.s. |
| +seed42 敏感性 | plateau | paired | 5 | −0.412 | 4 | **0.702** | n.s. |
| **D28 Welch** | gen9 单点 | unpaired | 4 vs 5 | ∣0.524∣ | 6.73 | **0.617** | n.s. |

mean diff: N=4 = −0.415(−0.74%),N=5 = −0.530。Cohen's d: N=4 = −0.13,N=5 = −0.18。
**三算法全部 p≫0.05,方向一致(略偏 α10 更优,量级在噪声内)。**

## §3 数学理论延伸(通道 B,主协作者审定)

1. **指标选择**:plateau mean 严格优于 gen9 单点(降噪,Var(X̄)<Var(X9) 即使强自相关)。p=0.62↔0.818 的差异**主要来自 paired/unpaired + seed0 不对称,非指标本身**。
2. **paired vs unpaired**:同 seed 配对设计 → **paired-t 正确**。Welch unpaired 把 between-seed 方差 S² 重新混入 SE,放大 2.5–10×(S∈[5,20] 时)。**D28 的 p=0.62 是功效损失伪影,不应作"更保守真值"引用**。
3. **功效**:N=4/5 power≈5–6%(≈名义假阳率)。80% power 需 N≈467(d=0.13)~245(d=0.18)。"N≈470" 估计核对通过。**non-significance 是 underpowered 预期输出,absence of evidence ≠ evidence of absence**。报 p 必须同报 power/MDE(宪法 §2 规则 6,反 inflate)。
4. **selection bias —— 通道 B 提出,主协作者 REFUTE**:见 §4。
5. **seed42 诚实表述**:两个 N 都报;seed42 方向 favor framework(−0.99),纳入使结论"更 favor framework 却仍不显著"= 对 negative result 稳健性的有利证据,应明说(deflate 防护)。

## §4 差异日志(D-1 纪律 5)

| # | 差异 | 裁决 |
|---|---|---|
| D1 | paper paired p=0.818 vs D28 Welch p=0.62 | **reconciled** = 指标(plateau vs gen9)+ 配对(paired vs unpaired)不同;两者各自自洽,方向一致(null)。paired-t 是正确主分析。 |
| D2 | 通道 B:seed0 排除 → 偏向 framework 的 selection bias | **REFUTED(主协作者 + 实测)**。seed0 α10 = `rc=137`(SIGKILL/OOM,3 次重试均 137),且 gen0 test_ppl=36.30 **健康无发散**。排除是 **infrastructure MCAR,非 α divergence**。前提(treatment-related failure)不成立 → 无 selection bias,N=4 ≈ unbiased。强行 ITT 编码 seed0 为"α failure"= 把资源故障算到 α 头上 = anti-framework distortion,同样拒绝。 |
| D3 | "α=10 更易 divergence" endpoint | **证据不足**。F3 source(cluster 3)内仅 seed0 缺失且为 OOM。cluster 9 candidate_c 的 NaN 是已知 ROCm gfx1201 fp16 artifact(STATE §3,不可定量),不能作 α endpoint。 |
| D4 | **新 artifact**:α0 seed1 两个 bit 级完全相同的 jsonl(`armb_alpha0.0_seed1_20260510_011048` / `_130149`) | 重复落盘,数值同不影响统计,但**建议 archive manifest 注明**以防误计为独立 seed。 |
| D5 | Welch Δ 符号(+0.83 vs −0.83) | 约定差(α0−α10 vs α10−α0),数值无误;paper/footnote 须写明谁减谁。 |

## §5 v8.1 footnote 诚实表述建议(措辞级,留 PI/反题/Win 定)

> **F3 multi-seed test.** 主分析为预注册 paired design(同 seed 配对 α=0/α=10,plateau = gen6–9 mean test perplexity),convention seeds {1,2,3,4}(N=4):mean diff −0.42,paired-t(3)=−0.25,p=0.818,Cohen's d≈−0.13(负=α=10 更优)。敏感性:纳入 convention 外但 cell valid 的 seed42(N=5)得 mean −0.53,t(4)=−0.41,p=0.70;纳入使点估计更偏 framework 而结论(不显著)不变,一并报告以避免选择性纳入。
> **Power.** 观测效应量 |d|≈0.13–0.18 下 N=4–5 power 仅 ~5–6%(双侧 α=0.05),80% power 需 N≈245–467;故 non-significance 是 underpowered 的预期结果,不构成无效应证据。
> **Exclusion note.** convention seed0 的 α=10 链因 `rc=137`(进程被 kill,infrastructure/OOM,3 次重试均失败)未完成,而 gen0 perplexity(36.30)健康、无数值发散;该缺失为 infrastructure-related(随机于 treatment),N=4 listwise 因此为无偏估计。 [证据等级:高]
> **D28 reconcile.** 此前 D28 audit 以 gen9 单点 + unpaired Welch(α0 N=5、α10 N=4)得 p=0.62;该检验丢弃配对、引入臂间不对称,功效低于 paired-t,差异源于检验选择而非效应本身。`[?]` 语气强度留校。

## §6 留 PI / 关卡 3 决

1. v8.1 footnote 是否纳入 §5 措辞(尤其 exclusion note 用 "infrastructure/OOM" 而非通道 B 原建议的 "α divergence" —— 后者实测不成立)。
2. 是否把 power/MDE 句正式补进 paper §6 F3(反 inflate 强化)。
3. D4 重复 jsonl 是否进 archive manifest 勘误。
4. 本 findings 是否 promote + 追加 `MD_CATALOG.md`(单点写权 = 主会话)。

---
*cycle 1 by 辅助 agent;通道 A=algo-verify(Opus,a050636d)、通道 B=paper-review(Opus,aaa4d29c);anchor 脚本 `$CLAUDE_JOB_DIR/tmp/recompute_f3.py`。*
