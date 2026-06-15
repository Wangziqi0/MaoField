# 恢复相表示几何 — fresh-eyes 盲点的 trace 答案 (exp019 12链 gen0-9)

> Linux 姐姐主会话,2026-06-15 (date 二值验证)。触发 = `fresh-eyes-0bias` 子 agent 零偏见审视指出的盲点。复用 `rerun_e0_metric_panel.py` 口径(同 val/同 layer_metrics),12 链 × gen0-9 全测末层(L12)。脚本 `recovery_geometry_panel.py` + 结果 `recovery_geometry_panel_result.json` 同目录。

## TL;DR
唯一被测过的崩溃几何信号(E0「崩溃→升维」)是 **gen0→gen1 单步**——而 12 链数据显示那一步正落在 **PPL 驼峰的上升边/峰**。补测全 10 代(N=6/arm)后:
- **所有 4 个几何量(PR_raw / PR_centered / isotropy / eff_rank)都是非单调驼峰,峰在 gen1-2,恢复相(gen2→gen9)回落,与 PPL 驼峰同步。**
- **E0 的「升维」是驼峰瞬态:** E0 单步 gen0→gen1 (PR_cen +78% / PR_raw +148%) ≈ **峰幅度**,而稳态 gen9 只 **+35% / +64%** → **E0 单步夸大稳态 ~2.2x**。净方向仍升(gen9 > gen0),但温和得多。
- **几何站 PPL 那边(同驼峰),不站多样性那边(单调崩)** → 证伪 fresh-eyes 自己提的「几何 vs PPL 第二解耦」假设。真正解耦 = (PPL + 几何) 一组驼峰 vs (多样性/复制) 一组单调崩。
- **α0 ≈ α1 全程全量**(gen9 PR_cen 153.8 vs 153.9,差 +0.1)→ 强化 exp019 C1 撤回:α=1 对几何**全轨迹**无效,不只 gen1。

## 口径 + 自检 (防 multi_layer_hook 口径漂移)
复用 `rerun_e0_metric_panel`:wikitext-2 val → block64 → numpy-shuffle(42) → 前256,末层 L12,fp32。
**自检通过**:α0 s101 gen1 PR_centered = **200.6** ≈ pairs.json E1["101"][0] = **200.638**。与 exp019 E1 同尺,不可能口径漂移。

## 均值轨迹 (N=6/arm,末层 L12)
```
gen:            0      1      2      3      4      5      6      7      8      9
α0  PR_raw :  46.9  116.2  111.0   94.0   81.4   76.4   74.8   73.7   75.0   76.8
    PR_cen : 113.8  202.2  203.1  188.6  170.7  160.7  155.4  151.3  152.0  153.8
    isotrpy: .894   .944   .940   .932   .925   .923   .923   .923   .924   .925
    effRank: 320.1  414.6  413.7  401.6  387.0  379.3  374.9  371.0  371.9  374.3
    PPL    :  36.3   77.7  104.9   92.6   74.7   63.8   57.9   54.3   52.9   53.3
α1  (全量与 α0 几乎重叠;PR_cen gen9=153.9, PPL gen9=54.4)
```
峰代:几何 PR_cen 峰 gen2(203),PPL 峰 gen2(105);几何上升比 PPL 快一步(gen1 已≈峰)。

## 四个判定 (descriptive,trace-backed)
1. **fresh-eyes 盲点真实**:恢复相几何此前确无任何测量(E0=gen0→gen1,exp019 E1=gen1)。已填。
2. **E0「崩溃→升维」精确化(非杀死)**:非单调驼峰;单步测量在峰附近夸大稳态 ~2.2x;净升维方向仍在但温和。
3. **几何 = PPL 的同过程两面**:几何与 PPL 同驼峰、同步回落 → 「几何升维」很可能是 PPL 退化在表示空间的投影,**不是独立现象**(降低其作为独立 finding 的分量)。
4. **C1 强化**:α0≈α1 全 10 代 × 全 4 量 → α=1 几何无效是全程的。

## caveat (守死)
- N=6/arm 强,但**单实验 / OPT-125m / 末层 L12 / fp16-trained ckpt**;不外推强模型(命题 A 鸿沟)。
- 「升维」是表示空间统计(PR/isotropy/eff_rank),**非「能力/可解释性」**;"更可解释"未测。
- 全 12 层、PR_raw/isotropy/eff_rank 全轨迹在 result json;本 md 聚焦末层 PR_centered + 关键标量。
- 这是**对 E0 的精确化(descriptive)**,不下 paper/战略结论(留 PI)。E0 那条线整体仍受 SIGMA + Ma2018 双削(组装型窄缝,见 `../../../wip/blackbox_dimreduction_recon_d35/COLLAPSE_GEOMETRY_RECON_VERDICT_20260607.md`)。

---
*Linux 主会话 · fresh-eyes 指方向 + 主会话 trace 实测 · 对称:E0 被削 + fresh-eyes 解耦假设被证伪 + C1 被强化,无偏袒 · 战略留 PI*
