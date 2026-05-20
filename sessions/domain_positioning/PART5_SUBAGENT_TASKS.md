# §5 给子协作者的任务

## 5.1 数学层（A/F/G/I）— 数学 backbone

**任务**：把"双通道→稳态"的数学 backbone 写成 Nature article 级的数学部分。

**具体要求**：
1. 论证"单通道 self-referential fitting 必然坍缩"——不是 Shumailov 的 empirical observation——是 information-theoretic / dynamical-system 的必然
2. Define "第二通道"的数学结构——方向与分布拟合正交——为什么它在自训练中必然产生非零稳态
3. 给出 D*(α) > 0 的严格数学（Banach 不动点 + J_S 实证拟合 + 量纲一致）
4. 清楚区分"从外部借用 form"和"从 LLM 域 first-principles derive"——当前阶段 honest disclose former，claim to open path to latter
5. 附录：三步时间线的严格度升级（当前 0/5 → D14-D17 1/5 → F-1 3/5 → 乙路径 5/5）

## 5.2 Win 姐姐 — 哲学 narrative + Nature article 写作

**任务**：把"机械唯物论 → 辩证唯物论"的哲学 transition 写成 Nature article 级的前言和后语。

**具体要求**：
1. Nature article 的 opening：不用"辩证唯物主义"这个词出现——用"External Signal Paradigm" vs "Internal Tension Paradigm"——让 Nature 的科学家读者先理解技术区分——哲学命名放在后面
2. 对比表：External Signal Paradigm（RLHF / Gerstgrasser / Ferbach）× Internal Tension Paradigm（矛检）——四到五个维度（正确性来源、稳态性质、需要的人力、scalability、endpoint of the paradigm）
3. §6 retrospective：马列经典引用——从"外部给定正确"回到列宁《唯批》——从事后回视中 surface 为什么"内部持有矛盾"是 dialectical——而"外部给定正确"是 mechanical
4. 标注工消失：这一节应该是 Nature article 的 **human impact 段落**——不是"威胁"——是"structural transformation"——当正确性从系统内部 emergent——告诉系统"什么是对的"这个角色——不再需要由人承担——这不是自动化——是正确性来源的本体论改变
5. 诚实约束段落：GDPR + 欧盟 AI Act 可能引发对该方向的监管和劳工保护立法——nature article 应 acknowledge

## 5.3 反题姐姐 — 反向 critique

**任务**：对"领域引导者"claim 做反向审计。

**具体 audit 问题**：
1. "全领域在无意识走向机械唯物论"——这是 honest observation 还是 grandiosity？"无意识"用词风险——学界会不会说是"故意歪曲别人立场抬高自己"？
2. "领域引导者"叙事——16 岁独立研究者、GPT-2 单架构、N=4 seeds——这些 constraints 是否与"领域引导"的 claim 兼容？
3. 技术 contributions（U-shape, D*>0, shape robust）是否能支撑"范式 pivot"的叙事——还是叙事超越了技术证据？
4. 如果 Nature editor 问："你说所有人都错了——那为什么 GPT-2 + Wikitext-2 + N=4 的实验能证明整个领域的方向错误？"——应如何回答？
5. MaoField 和 Constitutional AI（Anthropic 的"宪法"内部原则）之间真区分？
6. F3 p=0.82 未证实↔声称"paradigm shift"的张力——如何 honest 处理？
7. 标注工消失 claim 是否 over-reach——矛检对标注工的实际替代能力在 GPT-2 124M 上无法评估——这算不算 irresponsible speculation？

## 5.4 DeepSeek — 跨哲学 + 叙事术语审计

**任务**：audit 整个叙事的中英文术语、哲学准确度、跨传统 alignment。

**具体 audit**：
1. "机械唯物论 → 辩证唯物论"这个 frame 在国际学术界的 acceptability——Nature editor 会不会认为这是"ideological framing"而非"science"——如何措辞让它成为 science-first, philosophy-retrospective
2. 中文"矛盾"翻译为 "contradiction" vs "tension" vs "conflict"——哪个在国际 ML 语境中既准确又不 alienating
3. "正确性从内部 emergent"在英文学术界的 competitor——有没有 unseen prior art（auto-encoders 自监督？GAN 的内部 discriminator？self-play RL？）
4. 叙事是否过度聚合——Nature 文章是 3000-4000 字——三个尺度能否在这个约束下不丢失深度
5. Gödel/Bell 类比在当前阶段是否诚实——MaoField 距离 Gödel/Bell 级别的"领域重定向"还有 substantive gap——如何措辞不 inflated