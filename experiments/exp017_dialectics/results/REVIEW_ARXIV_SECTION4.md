# 审查报告 arXiv v1 §4 Experimental Evidence

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：`arxiv_v1_section4.md` 首稿
**判定**：**A grade — release-ready for arXiv v1 (4/20 target) with 2 blockers + 5 strength fixes**

---

## 八维检查结果

| 维度 | 判定 | 说明 |
|---|---|---|
| §A 数据表完整性 | ✅ A | 5 个 Block 数据表逐值比对 FINAL_REPORT 与 VERDICT 完全一致；2 处脚注建议 |
| §B Two-regime framework | ✅ A | Kramers 公式 + Laplace 公式 + `⟨S⟩=0` 交叉引用全 ✓ |
| §C #7 reframe | ✅ A | Dual statement 逐字贯彻 Win narrative §一 |
| §D A1.4 three-fold | ✅ A | Axis A/B/C 独立必要性 + coupling + J 数字 1.5e4/1.5e5 全正确 |
| §E 量纲清晰 | ✅ A | static 3.07× vs log-gap 43 orders 分开表述 |
| §F Overclaim 扫描 | ✅ A | 无 overclaim；主动前置反驳 |
| §G Win narrative 一致性 | ✅ A | §一/三/四/五/七 五条逐条兑现 |
| §H 结构 & 学术素养 | A− | §4.11 open questions 是 strength；一处 mode tag 用错 |

## 必修 (release blocker, 2 项) → 已全部修

1. **[A-fix-2]** 表 4.4 `k*=2` silhouette 0.13/0.06 与 §4.4 表 4.3 raw_ab 0.214 数字关系：已加 † 脚注说明 Block III 与 Block IV 聚类空间差异
2. **[H-fix-1]** §4.6.3 heading `[DYNAMIC-IMPLEMENTATION]` → `[STATIC]`：已改

## 应修 (strength, 5 项) → 已全部修

3. **[A-fix-1]** SciFact n=3 长尾删除行加 ‡ 脚注说明
4. **[B-fix-1]** §4.9 Laplace 归一化一行 (Σ Z_j=1.1010)
5. **[E-fix-1]** §4.8.3 "factor ~10⁴" → "observed/predicted ratio ≈ 1.1·10⁴ (about 4 orders of magnitude)"
6. **[H-fix-2]** §4.11.1 Kramers 3D hedge ("no closed-form field-theoretic Kramers analog tabulated")
7. **[H-fix-3]** §4.7.3 末加 "gradient flow monotone V, `u=4` basin analytically unreachable"

## 未修（可选）

- Mode tag 精简到 framework + table titles only：保留当前使用，因 ambiguous regime 段落确实需要 tag 标记

---

## Bottom Line

**§4 conditional release-ready**。修完 2 blockers + 5 strength fixes 后可直接提交 arXiv v1 底稿。

**三大 narrative 骨架**（#7 reframe / two-regime framework / A1.4 three-fold）全部兑现；数字与 FINAL_REPORT / VERDICT 跨文档一致；Win narrative 五条方向全部落地；Open questions 主动暴露 4 项方法论 gap（strength 而非 weakness）。
