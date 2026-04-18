# 审查报告 P5 — Z_1 措辞回退 + Lawvere 降级

**审查员**：独立 paper-review subagent, 2026-04-14
**范围**：FINAL_REPORT §3.1 / §4.2 + lawvere_monad_draft §2.3.2 / 脚注 ⁵
**判定**：**存疑（3 阻塞 + 3 小修）** → Linux 已修订

---

## 审查员发现

| # | 项 | 判定 | 处理 |
|---|---|---|---|
| 1 | "phase sector" 术语 | ⚠️ 非标准 | 改为 "arg(ψ) distribution" / "U(1) phase variable"（line 153, 236, 238）✓ |
| 2 | V=¼(|ψ|²−1)² `|ψ|=0 unstable fixed point` | ✅ 保留（ψ∈ℂ 空间下 ∇V|₀=0, Hessian 负定）| 补说明"ψ∈ℂ 空间 critical point" ✓ |
| 3 | **endofunctor 严格性** | ❌ G∘F 跨三 category 非 endofunctor | lawvere 主文 + 脚注 ⁵ 显式声明 ambient `C = Meas` + Giry monad lift 路径 ✓ |
| 4 | SSB 三条缺 order parameter + 热力学极限 | ⚠️ | [^zn-loose] 脚注扩到 5 条，明确 N=32³ 违反 (5) ✓ |
| 5 | arXiv v1 readiness 细节 | ⚠️ | line 236 "distributionally concentrated"、antipodal parenthetical 已补 ✓ |
| 6 | **FINAL_REPORT [^zn-loose] 未落地** | ❌ | 已补脚注定义在 line 240 ✓ |
| 7 | 审查员反驳"|ψ|=0 不是 critical point"的用户质疑 | ✅ | 保留 "unstable fixed point"（ψ∈ℂ 空间正确）✓ |

## 关键修订

### FINAL_REPORT
- "effective Z_1 phase collapse" → "arg(ψ) 分布强集中；U(1) in empirical distribution broken 但未 antipodally split (kmeans-2 26.2° ≠ 180°)；Z_2 ⊂ U(1) not realized"
- "Z_2 amplitude bistability" → "bimodal amplitude distribution at |ψ|∈{0,1}"，加说明 V(0)=¼≠V(1)=0 不存在 Z_2 group action
- 新增 [^zn-loose] 脚注（line 240）：5 条严格 SSB 条件 + 明确 N=32³ 违反 (5)

### lawvere
- 主文 §2.3.2：显式声明 `C = Meas`，F, G 扩展为 identity on complement，G∘F 成 bona fide endofunctor
- 脚注 ⁵：明示 Giry monad (P) lift，`P∘T_•` 继承 (η, μ)；位置 paper-level rigor，monad lift 留 future work
- 引用 Giry 1982; Jacobs 2010

## Bottom Line

position-paper-level rigor 达标（与草稿自我定位一致）。主要概念（Kleisli 可达性、Δ_OP2 categorical gap、source-density coupling）保持；"Z_n" 标签退化为 empirical distributional pattern label + 脚注说明；endofunctor on Meas + Giry monad lift 给出清晰的 follow-up 路径。

arXiv v1 §2.3 和 §3.1 可基于此措辞起草，不冒充 "full formalization"。
