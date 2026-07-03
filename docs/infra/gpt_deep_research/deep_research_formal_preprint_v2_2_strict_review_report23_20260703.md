# 严格数学审稿报告

## 执行摘要

仅依据所附 ZIP/package 内证据，我对 `from_repo/docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_2_UNDER_LOCK_20260703.tex` 作了逐条数学复核、精确 `2\times2` 见证算术复算、包内参考文献元数据核对、边界措辞核对、禁用主张扫描与包内重复风险评估。我的唯一裁决是 **`REQUEST_BOUNDARY_WORDING_PATCH_BEFORE_PI_REVIEW`**。原因不是数学硬伤：正文中唯一的引理与主定理在其当前“有限、正权、二向表”设定下是成立的，正文展示的 `2\times2` 精确有理数见证也复算无误，canonical harness-boundary sentence 已逐字出现，`MEDIUM duplicate risk` 也已明确写入；真正的阻断点是：该 TeX 草稿没有把包内一贯维持的 **Mode B MaoField empirical status = `insufficient_artifact`** 明文写进草稿边界段，而包内短提示、严格审稿提示、draft-gate taskbook、package readme 与 adoption note 都要求该状态保持且不得被弱化或省略。因此，在进入 PI 本地最终审查前，应先做一次精确的边界措辞补丁。fileciteturn0file0（`package/PROMPT_SHORT_FINAL_REVIEW_20260703.md`:17-21；`package/from_repo/docs/infra/gpt_deep_research/GPT55_PRO_MAOFIELD_FORMAL_PREPRINT_V2_2_STRICT_REVIEW_PROMPT_20260703.md`:47-53,102-106；`package/from_repo/docs/infra/recovery/ORDER_DEFECT_D703_FORMAL_PREPRINT_DRAFT_GATE_TASKBOOK_20260703.md`:78-95；`package/PACKAGE_README_FINAL_REVIEW_20260703.md`:15-27；`package/from_repo/docs/infra/gpt_deep_research/ORDER_DEFECT_ENGLISH_PREPRINT_CANDIDATE_V1_REPORT20_ADOPTION_NOTE_20260703.md`:60-81；`package/from_repo/docs/infra/debranded_residual_transport/PREPRINT_DRAFT_PROGRAMMATIC_V2_2_UNDER_LOCK_20260703.tex`:40-45,301-314）

## 详细审稿报告

### 定理与证明逐条审查

**1）引理 `Elementary intersections` 的正确性：通过。**
该引理声称 `C\perp A`、`C\perp B_0` 且 `A\cap B_0=\{0\}`。正文证明对前两项直接用零加权边际均值给出：若 `a\in A`，则 `\langle 1,a\rangle_w=\sum_q w_Q(q)a(q)=0`；`B_0` 同理。对交集部分，若函数既只依赖 `q` 又只依赖 `b`，则在 `Q\times B` 上必为常数；再由零边际均值推出该常数为零。这个论证在有限非空集合上完全充分，没有遗漏假设，也不需要额外正则性条件。（`...PREPRINT...tex`:105-111）

**2）主定理中 `(i)\Rightarrow(ii)`：通过。**
若 `w(q,b)=w_Q(q)w_B(b)`，则对任意 `a\in A`、`c\in B_0`，有
\[
\langle a,c\rangle_w
=\sum_{q,b}w_Q(q)w_B(b)a(q)c(b)
=\Bigl(\sum_q w_Q(q)a(q)\Bigr)\Bigl(\sum_b w_B(b)c(b)\Bigr)=0.
\]
这一步是标准分离变量计算，没有逻辑跳跃。（`...PREPRINT...tex`:134-141）

**3）主定理中 `(ii)\Rightarrow(i)`：通过。**
正文构造了中心化指标
\[
a_{q_0}(q)=\mathbf 1_{q=q_0}-w_Q(q_0),\qquad
c_{b_0}(b)=\mathbf 1_{b=b_0}-w_B(b_0),
\]
并指出二者分别属于 `A` 与 `B_0`。这点正确，因为
\[
\sum_q w_Q(q)a_{q_0}(q)=w_Q(q_0)-w_Q(q_0)\sum_q w_Q(q)=0
\]
且 `\sum_q w_Q(q)=1`；列侧完全同理。随后
\[
\langle a_{q_0},c_{b_0}\rangle_w
=w(q_0,b_0)-w_Q(q_0)w_B(b_0),
\]
从正交性立刻推出逐格 product identity。该证明是完备的；包内 proof-repair candidate 对同一步也给出一致论证，没有发现缺失假设或逻辑漏洞。（`...PREPRINT...tex`:143-153；`package/from_repo/docs/infra/debranded_residual_transport/FORMAL_NOTE_V1_3_ORDER_DEFECT_PROOF_REPAIR_CANDIDATE_20260630.md`:82-109）

**4）主定理中 `(ii)\Leftrightarrow(iii)\Leftrightarrow(iv)`：通过。**
正文先用 `P_A\mathbf 1=P_{B_0}\mathbf 1=0` 把
\[
D_w=(I-P_{B_0})(I-P_A)(I-P_C)-(I-P_A)(I-P_{B_0})(I-P_C)
\]
化简为
\[
D_w=P_{B_0}P_A-P_AP_{B_0}.
\]
这一步是正确的，因为涉及 `P_C` 的所有交叉项都因 `C\perp A` 与 `C\perp B_0` 而消失。若 `A\perp B_0`，则两个复合投影都为零，所以 `D_w=0`。反向则取任意 `b\in B_0`，从
\[
0=D_w b=P_{B_0}P_A b-P_A b
\]
推出 `P_A b=P_{B_0}P_A b\in A\cap B_0`，再由引理知 `P_A b=0`。由于 `P_A` 是到 `A` 的正交投影，这等价于 `b\perp A`；于是 `A\perp B_0`。`(iii)\Leftrightarrow(iv)` 只是 `D_w` 的定义重述。证明严密、闭合。（`...PREPRINT...tex`:155-166）

**5）主定理末尾关于 `I-P_{N_{\rm add}}` 的结论：通过。**
在 `A\perp B_0` 时，`C,A,B_0` 互相正交，因而 `P_{N_{\rm add}}=P_C+P_A+P_{B_0}`；于是两种 ordered stripping 都退化为 `I-P_{N_{\rm add}}`。这一步依赖的是有限维 Hilbert 空间中的标准正交直和投影公式，正文设定足够支撑这一点。（`...PREPRINT...tex`:168-169）

**6）非 product 权重下纯主效应见证存在性的证明：通过。**
正文从“非 product 权重 \(\Rightarrow A\not\perp B_0\)”出发，取某个 `K\in B_0` 满足 `P_AK\neq0`。然后，因为 `K\in B_0`，有 `P_CK=0` 且 `P_{B_0}K=K`，于是
\[
R_{B\to Q}K=(I-P_A)(I-P_{B_0})(I-P_C)K=0.
\]
另一方面，
\[
R_{Q\to B}K=(I-P_{B_0})(I-P_A)K=-(I-P_{B_0})P_AK.
\]
若此向量为零，则 `P_AK=P_{B_0}P_AK\in A\cap B_0`，从而 `P_AK=0`，与选取矛盾。最后 `K\in B_0\subset N_{\rm add}`，故 `(I-P_{N_{\rm add}})K=0`。这正好证明：非零的是“顺序性伪影”，不是真正的 additive residual。逻辑完整且没有把存在性误写成“对所有输入都如此”的全称命题。（`...PREPRINT...tex`:170-179；另与包内 proof-repair candidate 一致：`...PROOF_REPAIR_CANDIDATE...md`:164-178）

**7）反例、缺失假设、逻辑缝隙结论。**
在当前明确写出的设定——`Q,B` 有限非空，`w(q,b)>0` 且总和为 `1`——下，我没有找到正文引理或主定理的反例，也没有发现会导致结论失效的遗漏假设。若要吹毛求疵，只能说“严格正性”在证明 `(i)\Leftrightarrow(ii)` 时比必要条件略强；但这不是错误，只是保守假设。正文没有数学硬阻断。（`...PREPRINT...tex`:63-103,115-179）

### 精确 `2×2` 见证算术复算

**1）正文主见证的所有算术主张：全部核对通过。**
正文在 `2\times2` 证书节给出权矩阵、边际、非-product 判定、见证向量、两个 ordered stripping 的输出以及平方加权范数。我按正文定义直接重算，结论与文中完全一致。（`...PREPRINT...tex`:181-220；`package/from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`:30-52；`package/from_repo/docs/infra/debranded_residual_transport/exact_witness_v1_4_20260629.json`:51-77）

| 步骤 | 精确计算 | 结果 |
|---|---|---|
| 权矩阵 | \(\displaystyle w=\frac1{11}\begin{pmatrix}1&2\\3&5\end{pmatrix}\) | 正文一致 |
| 行边际 | \(\displaystyle w_Q=\left(\frac{1+2}{11},\frac{3+5}{11}\right)=\left(\frac3{11},\frac8{11}\right)\) | 正文一致 |
| 列边际 | \(\displaystyle w_B=\left(\frac{1+3}{11},\frac{2+5}{11}\right)=\left(\frac4{11},\frac7{11}\right)\) | 正文一致 |
| 非 product 检查 | \(\displaystyle w(q_1,b_1)=\frac1{11},\quad w_Q(q_1)w_B(b_1)=\frac3{11}\frac4{11}=\frac{12}{121}\neq\frac1{11}\) | 正文一致 |

**2）`K\in B_0` 与真 additive residual 为零：通过。**
正文见证
\[
K=\left(\frac7{11},-\frac4{11},\frac7{11},-\frac4{11}\right)
\]
对应列函数 \(c(b_1)=7/11,\ c(b_2)=-4/11\)。检验 `B_0` 条件：
\[
\sum_b w_B(b)c(b)
=\frac4{11}\frac7{11}+\frac7{11}\Bigl(-\frac4{11}\Bigr)=0.
\]
因此 `K\in B_0\subset N_{\rm add}`，故
\[
(I-P_{N_{\rm add}})K=0.
\]
这一步无误。（`...PREPRINT...tex`:194-205）

**3）`R_{B\to Q}K=0`：通过。**
因为 `K` 本身就是纯列主效应，先减去列主效应时被一次性消掉，所以
\[
R_{B\to Q}K=(I-P_A)(I-P_{B_0})(I-P_C)K=0.
\]
这是正文 202–205 行的结论，且由上一步 `K\in B_0` 直接得到。（`...PREPRINT...tex`:198-205）

**4）`R_{Q\to B}K` 的精确向量：通过。**
先算行投影 `P_AK`。`K` 的全局均值为
\[
\mu_K=\sum_{q,b}w(q,b)K(q,b)=0,
\]
所以
\[
P_AK(q,\cdot)=E_w[K\mid q].
\]
逐行计算：
\[
E_w[K\mid q_1]
=\frac{\frac1{11}\frac7{11}+\frac2{11}\left(-\frac4{11}\right)}{\frac3{11}}
=\frac{-1/121}{3/11}
=-\frac1{33},
\]
\[
E_w[K\mid q_2]
=\frac{\frac3{11}\frac7{11}+\frac5{11}\left(-\frac4{11}\right)}{\frac8{11}}
=\frac{1/121}{8/11}
=\frac1{88}.
\]
因此
\[
P_AK=\left(-\frac1{33},-\frac1{33},\frac1{88},\frac1{88}\right),
\]
从而
\[
(I-P_A)K
=\left(\frac7{11}+\frac1{33},-\frac4{11}+\frac1{33},\frac7{11}-\frac1{88},-\frac4{11}-\frac1{88}\right)
=\left(\frac23,-\frac13,\frac58,-\frac38\right).
\]
接着计算其列主效应：
\[
E_w[(I-P_A)K\mid b_1]
=\frac{\frac1{11}\frac23+\frac3{11}\frac58}{\frac4{11}}
=\frac{61}{96},
\]
\[
E_w[(I-P_A)K\mid b_2]
=\frac{\frac2{11}\left(-\frac13\right)+\frac5{11}\left(-\frac38\right)}{\frac7{11}}
=-\frac{61}{168}.
\]
故
\[
P_{B_0}(I-P_A)K=
\left(\frac{61}{96},-\frac{61}{168},\frac{61}{96},-\frac{61}{168}\right),
\]
于是
\[
R_{Q\to B}K
=(I-P_{B_0})(I-P_A)K
=\left(\frac1{32},\frac5{168},-\frac1{96},-\frac1{84}\right).
\]
与正文完全一致。（`...PREPRINT...tex`:206-210；`...EXACT_WITNESS...md`:44-52）

| 单元 | \((I-P_A)K\) | 列主效应 | 差值 |
|---|---:|---:|---:|
| \((q_1,b_1)\) | \(2/3\) | \(61/96\) | \(1/32\) |
| \((q_1,b_2)\) | \(-1/3\) | \(-61/168\) | \(5/168\) |
| \((q_2,b_1)\) | \(5/8\) | \(61/96\) | \(-1/96\) |
| \((q_2,b_2)\) | \(-3/8\) | \(-61/168\) | \(-1/84\) |

**5）平方加权范数 `61/177408`：通过。**
逐格计算
\[
\|R_{Q\to B}K\|_w^2
=\frac1{11}\left(\frac1{32}\right)^2
+\frac2{11}\left(\frac5{168}\right)^2
+\frac3{11}\left(\frac1{96}\right)^2
+\frac5{11}\left(\frac1{84}\right)^2.
\]
四项分别为
\[
\frac1{11264},\qquad
\frac{25}{155232},\qquad
\frac1{33792},\qquad
\frac5{77616},
\]
通分求和得到
\[
\frac{61}{177408}.
\]
与正文完全一致。（`...PREPRINT...tex`:211-219；`...EXACT_WITNESS...md`:46-52）

**6）包内 exact witness 证书中的对称 `A`-见证：也通过。**
虽然该对称见证未写进 TeX 正文，但它确实是包内 `2\times2` 见证主张的一部分，故我一并复核。证书给出
\[
K'=\left(\frac8{11},\frac8{11},-\frac3{11},-\frac3{11}\right)\in A,
\]
以及
\[
R_{Q\to B}K'=0,\qquad
R_{B\to Q}K'=\left(\frac1{42},-\frac1{84},\frac5{224},-\frac3{224}\right).
\]
精确复算如下：先按列去主效应，
\[
E_w[K'\mid b_1]=-\frac1{44},\qquad E_w[K'\mid b_2]=\frac1{77},
\]
于是
\[
(I-P_{B_0})K'=\left(\frac34,\frac57,-\frac14,-\frac27\right).
\]
再按行取条件均值：
\[
E_w[(I-P_{B_0})K'\mid q_1]=\frac{61}{84},\qquad
E_w[(I-P_{B_0})K'\mid q_2]=-\frac{61}{224}.
\]
所以
\[
R_{B\to Q}K'
=\left(\frac34-\frac{61}{84},\frac57-\frac{61}{84},-\frac14+\frac{61}{224},-\frac27+\frac{61}{224}\right)
=\left(\frac1{42},-\frac1{84},\frac5{224},-\frac3{224}\right).
\]
与证书一致；包内早前提到的 “11× 算术 slip” 在 v1.4 证书中已被纠正，当前 package 版本无此错误残留。（`package/from_repo/docs/infra/debranded_residual_transport/EXACT_WITNESS_V1_4_20260629.md`:54-60；`package/from_repo/docs/infra/debranded_residual_transport/SYNTHETIC_HARNESS_V1_3_20260628.md`:87-94）

### 参考文献元数据审查

**1）文献组织状态。**
独立 `.bib` 文件在 package 内 **未指定/缺失**；审查对象是 TeX 正文内嵌的 `thebibliography`。因此，我只能做“包内一致性”和“条目完备度”审查，不能在禁止出包外查询的前提下对外部数据库做终极核真。（`...PREPRINT...tex`:319-379；`package/PROMPT_SHORT_FINAL_REVIEW_20260703.md`:17-20）

**2）总体结论。**
20 个条目中，绝大多数在“作者、题目、年份、venue/identifier”四项上达到可用水位；主要问题集中在两类：其一，`lamboni2026` 明显低于包内已有的元数据完整度；其二，`boettcherspitkovsky2010` 的作者转写与包内 positioning file 不一致。除此之外，若按严格数学短注预印本标准看，若干 arXiv 条目仍然偏“草稿式”——作者用 `et al.`、未给 URL、未给版本。但在“仅凭包内证据”的限制下，这些只能记为非致命的规范性问题，而不是 correctness hard blocker。（`...PREPRINT...tex`:320-379；`...BIBLIOGRAPHY_AND_POSITIONING...md`:33-49）

| Key | TeX 条目位置 | 包内审查结论 | 备注/问题 |
|---|---|---|---|
| `hooker2007` | `...tex`:320-321 | 通过 | 与 positioning 记录一致，含 DOI。（`...BIBLIOGRAPHY...md`:40） |
| `bigbench2022` | `...tex`:323-324 | 基本可用 | 使用集体作者 “BIG-bench authors”，作者字段较粗；仅给 arXiv 号，无 URL。包内无更细作者元数据。 |
| `helm2022` | `...tex`:326-327 | 基本可用 | `et al.` 形式，arXiv 号已给出。 |
| `truthfulqa2021` | `...tex`:329-330 | 基本可用 | 作者、标题、年份、arXiv 号齐备。 |
| `selfcheckgpt2023` | `...tex`:332-333 | 基本可用 | 作者、标题、年份、arXiv 号齐备。 |
| `geval2023` | `...tex`:335-336 | 基本可用 | `et al.`，arXiv 号已给。 |
| `mtbench2023` | `...tex`:338-339 | 基本可用 | `et al.`，arXiv 号已给。 |
| `decodingtrust2023` | `...tex`:341-342 | 基本可用 | `et al.`，arXiv 号已给。 |
| `llmevalsurvey2023` | `...tex`:344-345 | 基本可用 | `et al.`，arXiv 号已给。 |
| `contamination2024` | `...tex`:347-348 | 基本可用 | 作者、题目、年份、arXiv 号齐备。 |
| `rethinkingcontamination2023` | `...tex`:350-351 | 基本可用 | 作者、题目、年份、arXiv 号齐备。 |
| `chastaing2012` | `...tex`:353-354 | 通过 | 与 positioning 记录一致，含 DOI。（`...BIBLIOGRAPHY...md`:41） |
| `chastaing2015` | `...tex`:356-357 | 通过 | 与 positioning 记录“2014/2015”备注相容；正文给最终 2015 发表年，合理。（`...BIBLIOGRAPHY...md`:42） |
| `owenprieur2017` | `...tex`:359-360 | 通过 | 与 positioning 记录一致，含 DOI。（`...BIBLIOGRAPHY...md`:43） |
| `ioossprieur2019` | `...tex`:362-363 | 通过 | 与 positioning 记录一致，含 DOI。（`...BIBLIOGRAPHY...md`:44） |
| `ilidrissi2025` | `...tex`:365-366 | 通过 | 与 positioning 记录一致，含 DOI。（`...BIBLIOGRAPHY...md`:45） |
| `lamboni2026` | `...tex`:368-369 | **需修补** | 相比包内 positioning 记录，正文条目把 venue 写成模糊的 “Publisher online record / DOI record”，且标题较包内记录更短，信息层级下降；应至少恢复包内已有的期刊名与谨慎的 online-record 说明。（`...BIBLIOGRAPHY...md`:46） |
| `halmos1969` | `...tex`:371-372 | 通过 | 与 positioning 记录一致，含 DOI。（`...BIBLIOGRAPHY...md`:49） |
| `boettcherspitkovsky2010` | `...tex`:374-375 | **包内不一致** | TeX 用 `Boettcher`，positioning 记录用 `Bottcher`；至少要在 package 内统一转写。（`...BIBLIOGRAPHY...md`:47） |
| `corachmaestripieri2010` | `...tex`:377-378 | 基本可用 | 作为 arXiv 预印本条目可接受；包内 positioning 也只给 arXiv 号。（`...BIBLIOGRAPHY...md`:48） |

**3）文献定位与 duplicate-risk 叙述是否一致。**
正文 related-work 段把贡献压缩为“有限加权二向表中的 projection-order artifact + exact rational certificate + programme suggestion”，并明确说相邻文献已有 dependent inputs、projection products 与 evaluation validity 的大文献群，故 duplicate-risk ceiling 保持中等。这与包内 `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 的定位完全同向，没有越界拔高。（`...PREPRINT...tex`:295-299；`...BIBLIOGRAPHY...md`:51-79）

### 边界语句、Mode B 说明与禁用主张扫描

**1）canonical harness-boundary sentence：已逐字匹配。**
项目锁定的 canonical sentence 是：

> The floating-point harness is deterministic regression support only; the mathematical claims are carried by the analytic proof and exact rational certificate, not by JSON floats.

该句在 wording-lock 文件中被明确定为必须 verbatim 出现的句子；目标 TeX 在 `Limitations` 与 `Methods and reproducibility` 两处都逐字写出了同一句，因此 **这一项本身通过，无需文字更正**。（`package/from_repo/docs/infra/debranded_residual_transport/WORDING_LOCK_V1_6_20260629.md`:7-11；`...PREPRINT...tex`:309,314；`package/from_repo/docs/infra/gpt_deep_research/GPT55_PRO_MAOFIELD_FORMAL_PREPRINT_V2_2_STRICT_REVIEW_PROMPT_20260703.md`:47-53）

**2）真正的边界缺口：TeX 草稿未明写 Mode B = `insufficient_artifact`。**
包内短提示明确要求 `Mode B remains insufficient_artifact; no MaoField empirical positive claim is allowed`；严格审稿提示也再次锁定该状态；draft-gate taskbook 更明写“must not change Mode B beyond `insufficient_artifact`”；package readme 与 adoption note 也把该标签列为当前 live label。相比之下，目标 TeX 虽然在边界段里写明“不是 paper-ready / preprint-ready / submission-authorized”，并一再声明 MaoField 部分是 programme 而非 empirical result，但 **没有把 `insufficient_artifact` 这个 Mode B 状态明文写出**。在这个 package 的内部治理结构下，这不是小风格问题，而是少了一条应显式承接的边界标签。（`package/PROMPT_SHORT_FINAL_REVIEW_20260703.md`:17-21；`...STRICT_REVIEW_PROMPT...md`:102-106；`...TASKBOOK...md`:78-95；`package/PACKAGE_README_FINAL_REVIEW_20260703.md`:15-27；`...ADOPTION_NOTE...md`:60-81；`...PREPRINT...tex`:40-45,237-247,301-314）

**我建议的精确补句** 放在 40–45 行的 `Draft status and claim boundary` 段末尾，直接写成：

```latex
Mode B MaoField empirical status remains \texttt{insufficient_artifact}. Accordingly, no MaoField empirical positive claim is made or authorized anywhere in this draft.
```

这句与包内现有边界体系相容，不会扩大主张，只会把 package-global label 显式落到草稿正文里。（同上引文）

**3）禁用 release/posting 语言：未见正向违禁。**
目标 TeX 在开头边界段明确写了 “not paper-ready, preprint-ready, public-postable, submitted, accepted, or submission-authorized”，属于禁止语的**否定声明**，不是违规授权。全文没有出现正向“已可发布/已可投稿/已获授权”的表述。（`...PREPRINT...tex`:40-45）

**4）禁用 MaoField 经验性 positive claims：未发现。**
我逐节扫描后，没有发现“已观测 MaoField residual/interactions/transport/holonomy field”“full panel has run”“checkpoint inference/training/new loss authorised”之类被 package 明令禁止的正向主张。相反，摘要、边界段、programme section 与 limitations 都在反复缩限：MaoField 部分是 programme，不是 empirical result；现阶段只是 future residual-metric audits 的提案。（`...PREPRINT...tex`:36-45,235-247,281-314；`package/PROMPT_SHORT_FINAL_REVIEW_20260703.md`:17-21；`...TASKBOOK...md`:78-95）

| 检查项 | 结果 | 位置 |
|---|---|---|
| paper-ready / preprint-ready / submission-authorized 正向语言 | 未发现 | 仅见否定声明：`...PREPRINT...tex`:41-42 |
| broad new ANOVA / dependent-input / projection theory | 未发现 | 仅见否定声明：`...PREPRINT...tex`:43,299 |
| MaoField empirical positive result | 未发现 | 摘要与 limitations 均否定：`...PREPRINT...tex`:37,308 |
| observed residual / interaction / transport / holonomy field | 未发现 | 全文未作正向宣称；package 边界持续禁止：`...TASKBOOK...md`:88-91 |
| harness / JSON floats prove theorem | 未发现 | 仅见相反声明：`...PREPRINT...tex`:309,314 |

### 包内重复风险评估

包内允许我做的只是一种**受限的内部重复风险评估**，而不是对外部文献作完整查重。基于 package 自带的 positioning file、strict review prompt 与正文 related-work 段，我的判断是：把 duplicate risk 保持在 **MEDIUM** 是合理的，而且正文确实没有把它下调。其风险来源不是“包内已发现 exact duplicate”，而是如果作者在表述上滑向“大一统 dependent-input decomposition theory / projection theory / empirical MaoField evidence”，就会与已占据的相邻文献带发生高重叠。当前 TeX 在主定理、related work 与 limitations 中总体保持了窄口径；因此这项是“边界需要继续守住”，不是“数学或重复性已实锤失败”。由于用户明确禁止外部比较，这个评估必须注明：**仅限 package 内容，不构成外部文献世界的最终重复性判断**。（`...PREPRINT...tex`:44,295-310；`package/from_repo/docs/infra/debranded_residual_transport/BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md`:17-31,65-79）

## 精确补丁指令

**1）边界补丁：必须做。**
在 `\paragraph{Draft status and claim boundary.}` 段落末尾，即当前第 44 行之后插入以下两句中的第一句；若希望把禁用经验性正向主张也一并落字，则两句都插入。

```latex
Mode B MaoField empirical status remains \texttt{insufficient_artifact}.
No MaoField empirical positive claim is made or authorized anywhere in this draft.
```

若希望一次性把 duplicate risk 与 Mode B 放在同一束边界中，也可改成下面这个合并版本：

```latex
The duplicate-risk status is MEDIUM duplicate risk.
Mode B MaoField empirical status remains \texttt{insufficient_artifact}; accordingly, no MaoField empirical positive claim is made or authorized anywhere in this draft.
```

该补丁是本次裁决的核心要求。（`...PREPRINT...tex`:40-45；`package/PROMPT_SHORT_FINAL_REVIEW_20260703.md`:17-21；`...TASKBOOK...md`:94-95）

**2）参考文献补丁：建议同步做，但不是本次唯一阻断原因。**
把 `lamboni2026` 条目改成至少不低于 package positioning file 的信息层级。基于包内已有记录，可写成：

```latex
\bibitem{lamboni2026}
Lamboni, M. On ANOVA-type decompositions of functions with non-independent variables: sensitivity analysis. SIAM/ASA Journal on Uncertainty Quantification, publisher online record / DOI record (2026). doi:10.1137/24M1712680.
```

这样既恢复了包内已有期刊名，也保留了“仅 DOI / publisher online record、不要过度声称 print status”的谨慎边界。（`...PREPRINT...tex`:368-369；`...BIBLIOGRAPHY...md`:46）

**3）作者转写统一：建议 package 内统一，但包内证据不足以唯一裁定哪一拼法为最终标准。**
`boettcherspitkovsky2010` 在 TeX 与 positioning file 间存在 `Boettcher/Bottcher` 不一致。由于用户禁止我出包外核真，我只能要求“package 内统一”，不能负责任地指定唯一正确拼写。若作者本地已有权威来源，应以同一拼写统一所有文件；若暂时没有，则至少统一 TeX 与 `BIBLIOGRAPHY_AND_POSITIONING_V1_5_20260629.md` 两处。（`...PREPRINT...tex`:374-375；`...BIBLIOGRAPHY...md`:47）

## 结论

在“只用 package 证据”的约束下，我的结论是：**数学核心可过，精确 `2\times2` 见证可过，禁用经验性主张扫描可过，duplicate risk 的内部定位可过；但边界文字尚未把 package-global 的 `Mode B = insufficient_artifact` 显式落进 TeX 草稿，因此当前仍应先做一次边界措辞补丁。** 这就是我给出的唯一裁决：**`REQUEST_BOUNDARY_WORDING_PATCH_BEFORE_PI_REVIEW`**。（`package/PROMPT_SHORT_FINAL_REVIEW_20260703.md`:17-21；`...PREPRINT...tex`:40-45,115-220,295-314）