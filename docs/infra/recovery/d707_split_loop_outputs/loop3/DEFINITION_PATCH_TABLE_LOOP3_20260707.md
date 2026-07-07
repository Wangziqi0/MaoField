# Definition Patch Table - Loop 3 - 2026-07-07

Status: `LOOP3_DEFINITION_PATCH_TABLE`

This table records the minimal typed-definition patch requested by Loop 3. It is a local definition-hygiene artifact, not a proof-authority artifact.

| Patch item | Before Loop 3 risk | Loop 3 patched definition | Type / endpoint check | Claim category | Review status |
|---|---|---|---|---|---|
| Ambient chart system | "Chart" could be read as informal evaluation setting. | A finite directed graph `G=(C,E)` of chart labels and declared material-relation edges. Multiple edges are allowed when labels differ. | Each edge has a source chart and target chart. | Definition patch. | Pro A / Main Pro should verify sufficiency. |
| Chart domain | Domain norms could be missing. | For each chart `c`, `H_c` is a finite-dimensional real Hilbert space or finite-dimensional real normed vector space. | `H_c` carries declared norm `||.||_{H_c}`. | Definition patch. | Patched. |
| Chart codomain | Output/object norms could be missing. | For each chart `c`, `O_c` is a finite-dimensional real Hilbert space or finite-dimensional real normed vector space. | `O_c` carries declared norm `||.||_{O_c}`. | Definition patch. | Patched. |
| Chart operator | `Phi_c` could be untyped. | `Phi_c:H_c->O_c` is linear. | `Phi_c in Lin(H_c,O_c)`. | Definition patch. | Patched. |
| Raw edge transport | Raw transport could be unnamed or untyped. | For each edge `e:c->c'`, `U_e=U_{c->c'}:H_c->H_{c'}` is linear. | Domain `H_c`, codomain `H_{c'}`. | Definition patch. | Patched. |
| Object edge transport | Object transport could be unnamed or untyped. | For each edge `e:c->c'`, `T_e=T_{c->c'}:O_c->O_{c'}` is linear. | Domain `O_c`, codomain `O_{c'}`. | Definition patch. | Patched. |
| Edge identity condition | Same-name identity could be mistaken for closure. | Edge closure is the declared intertwining equation `T_{c->c'} Phi_c = Phi_{c'} U_{c->c'}`. | Both sides map `H_c -> O_{c'}`. | Definition patch; programme framing stays separate. | Patched. |
| Edge defect | Defect could be endpoint-ambiguous. | `Delta_{c->c'}=T_{c->c'} Phi_c - Phi_{c'} U_{c->c'} : H_c -> O_{c'}`. | Both summands have type `H_c -> O_{c'}`. | Definition patch. | Patched. |
| General path transport | Cycle could be defined before path composition. | For `alpha:c_0->...->c_k`, `U_alpha=U_{c_{k-1}->c_k}...U_{c_0->c_1}:H_{c_0}->H_{c_k}`. | Right-to-left composition. | Definition patch. | Patched. |
| General object transport | Object path transport could be omitted. | `T_alpha=T_{c_{k-1}->c_k}...T_{c_0->c_1}:O_{c_0}->O_{c_k}`. | Right-to-left composition. | Definition patch. | Patched. |
| Empty path | Identity element could be missing. | `U_{id_c}=I_{H_c}` and `T_{id_c}=I_{O_c}`. | Both are typed identities at chart `c`. | Definition patch. | Patched. |
| Path defect | Defect could be defined only for cycles. | `Delta_alpha=T_alpha Phi_{c_0}-Phi_{c_k}U_alpha:H_{c_0}->O_{c_k}`. | Both summands map `H_{c_0}->O_{c_k}`. | Definition patch. | Patched. |
| Empty-path defect | Empty path could behave inconsistently. | `Delta_{id_c}=0:H_c->O_c`. | Follows from typed identities. | Derived finite linear algebra. | Patched; Pro A check requested. |
| Path composition | Composition orientation could be ambiguous. | For `alpha:c_0->c_1`, `beta:c_1->c_2`, `beta circ alpha` means first `alpha`, then `beta`. | `U_{beta circ alpha}=U_beta U_alpha`, `T_{beta circ alpha}=T_beta T_alpha`. | Definition patch. | Patched. |
| Composition lemma | Defect propagation could be asserted without type check. | `Delta_{beta circ alpha}=T_beta Delta_alpha + Delta_beta U_alpha`. | Every term maps `H_{c_0}->O_{c_2}`. | Finite linear-algebra lemma. | Pro A review requested. |
| Restriction to `S` | Norm on restricted defect could be ambiguous. | For `S subset H_{c_0}`, `Delta_alpha|_S:S->O_{c_k}` uses norms from `H_{c_0}` and `O_{c_k}`. | Restricted sup-ratio; usual operator norm if `S` is a subspace. | Definition patch. | Patched; terminology for arbitrary subsets flagged for review. |
| Invariance of `S` | Later bounds could silently assume invariance. | No assumption that `S` is `U_gamma`-invariant unless explicitly stated. | Bounds involving iterates must track `U_gamma^j(S)` or add hypotheses. | Claim hygiene. | Patched. |
| Programme sentence | Programme framing could be promoted into theorem. | `Identity is not naming; identity is path closure under declared material relations` is `PROGRAMME_FRAMING` only. | Not used as proof. | Claim hygiene. | Patched. |
| v1.6 boundary | v1.6 could be inflated. | v1.6 remains finite two-way-table two-projection commutator geometry only. | No broad projection theory. | Claim hygiene. | Patched. |
| Black-box audit boundary | Method schema could be mistaken for mechanism. | Black-box evaluation audit remains method schema / empirical hypothesis. | No mechanism solution. | Claim hygiene. | Patched. |

## Remaining Review Hooks

- Pro A should check whether arbitrary `S subset H_c` should be allowed as a restricted sup-ratio or whether later theorem statements should require `S` to be a linear subspace.
- Loop 4 should state every additional norm-growth hypothesis explicitly, especially any control over `U_gamma^j(S)`.
- Main Pro / Sub Pro E should re-check that no programme framing, JSON support, or empirical hypothesis has been upgraded into theorem status.
