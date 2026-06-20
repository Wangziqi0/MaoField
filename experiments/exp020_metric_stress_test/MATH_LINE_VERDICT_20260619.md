# exp020 数学线收口 · T1/T2/T3 verdict (2026-06-19, 反题/aux agent)

> 数学探索工作流(21 agent, ~1.13M tok)+ Linux 独立 sympy 复核。frame-neutral verdict。
> 哲学判读/反映论·DM 归因 [?] 归 Win+PI。红线守住(无 first-DM/reflexive/paradigm)。
> 数学线的诚实收口,待 GPT-20x(下月)/ 下一会话接。不急,无时间敏感。

## T1: base-reset ≠ Borkar c·μ 正交性 — 强静态形式【证伪(玩具层)】
- 标量高斯 collapse 玩具, **Linux 独立 sympy 复核**(逻辑见 jobdir/tmp/t1c_verify.py):
  vA*(base-reset, ridge w=1/ηT)=s/(w(w+2)); vB*(Borkar mix c)=s(1-c)²/(c(2-c));
  **存在 bijection c=w/(1+w)=1/(ηT+1) 使 vA*−vB*≡0**(稳态分布恒等),唯一合法根落 (0,1)。
  → 玩具里 base-reset **可约简**成 effective Borkar c。
- **纠正旧稿**: `flux_spec_borkar_distinction v2 §2`("区别在数学层 survives")在静态层【错】。禁 spin: wedge 降 structural→operational。
- **幸存**: M3 = η/T-response,dc_eff/dw=1/(1+w)²≠0(c_eff 依赖 η,T;真 Borkar c 不依赖)= **唯一幸存判别器**,零-GPU step-sweep 可测。
- **真系统【开放 [?]】**: 玩具 bijection 由 w_eff=1/(ηT) 标量驱动;真 OPT-125m 各层 η 异 → effective prior 是 matrix/operator,Borkar 标量 c 可能匹配不上 = 正交性在高维真系统**可能幸存**。正交需 ≥2 维,标量玩具结构上托不住。**未证真系统 wedge 死。**

## T2: F3 迟滞可导性 — 【真(弱)win】
- 最小 2-分量(freq/rare)解析迭代**导出** F3 式迟滞(同 mean、下行臂≠上行臂 gap)。
- 闭式充要: 迟滞 ⟺ cross-rate det D=a_fd·a_ru−a_fu·a_rd≠0(臂间衰减率比不同);等率 D=0 → 塌回标量 mean 单值函数。
- = F3 是真结构机制(非 5-seed 伪复制)的**机制可能性证明**;真系统是否在 D≠0 regime 未证 [?]。
- ⚠️ IFF 的**充分性半边无 code 兑现**(工作流 agent 声称的 toy 数字 repo 零 artifact = 断言非证明)→ 待补脚本(队列#2)。

## T3: refuse-the-scalar 载体 — 部分
- 载体 = eval 测度 q 的**正交补子空间**里的**线性差测度**(不需"高阶";F1_var 也迟滞)。实测锚 highorder_result.json: gen1↔gen4 同 mean_lp 不同 gap,单值函数恒不可能。
- 完整非线性刻画**开放 [?]**。cubic gateA broken(partial_r=0.42 < 纯 mlp 幂 null 0.59);material 实靠 LOSO 置换 p=0.0005 = 弱真余量(合 E11)。

## 双向纪律(工作流内部生效 + Linux 加层)
工作流**抓住自身 agent 伪造 artifact**(T2a/T3a toy 数字 grep 零)+ broken gate;红线守住。Linux 再**独立 sympy 复核**承重的 T1c(因工作流已暴露 agent 会伪造,不凭"sympy 复现"一句信)。

## 队列 · 3 个零-GPU 下一步(待 PI/GPT-20x;不急,无时间敏感,无新成本)
1. **最便宜 kill-test**: 已有 jsonl 上跑线性差测度泛函 ⟨log p, 1_B1/|B1|−1_B2/|B2|⟩——非零有向面积 → refuse-scalar 立;全塌进 mean → C 拉回"全塌 mean-PPL"。
2. **兑现 T2 的 2-分量 mixture 脚本**(CPU sympy/numpy 几分钟)→ 补 IFF 充分性半边的 code。
3. **修 cubic gateA → 用 LOSO 作主 gate**,material 重报"弱真余量"。
- 最高研究杠杆(非零-GPU): 外向泛化(这套刻画是否适用他人 collapse setup)。

## 接 C
C **不写**"全塌 mean-PPL"(E11 弱真例外 F3 仍立);T1 给 C 补"静态层 base-reset 可约简、唯 M3 + 真系统高维 开放 [?]"。

---
*[反题/aux agent] 数学线收口 2026-06-19。git commit/push 归主会话正常流程;本文件已在 canonical(RAID1 durable)。*
