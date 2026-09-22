# Targeted proof-issue resolution

## Resolution verdict

**PASS for the authorised PA-01 through PA-04 corrections, within the targeted scope below.**

- PA-01: **RESOLVED** in both the formal supplementary proposition/proof and the counterpart main-text sentence.
- PA-02: **RESOLVED** by an explicit `tau -> 0`, fixed-data, non-uniformity declaration.
- PA-03: **RESOLVED at the claimed algebraic representation level**; it remains conditional on the displayed positive rescaling and the source's compatibility bounds, and `d_i/y_i` is considered only where that quotient is defined.
- PA-04: **RESOLVED** by asserting the positive-`c` symbolic case; the modified deterministic harness passes.

This resolution is `same-family` and `provisional`. It does not rewrite or replace the original proof audit, whose three artifacts and verdict remain unchanged. It also does not review or adopt the separate offline Lean replay performed by the root task; compiler-replay statements in the change receipt are outside this targeted resolution.

## Invocation metadata

- Requested reviewer model: `gpt-5.6-sol`
- Requested reasoning effort: `ultra`
- Reviewer family: `openai`
- Review independence: `same-family`
- Acceptance status: `provisional`
- Additional reviewer/model/API calls: none

The original `PROOF_AUDIT.json` is immutable by instruction. Its model fields should therefore be read together with this resolution's metadata correction: the requested invocation route was `gpt-5.6-sol` at `ultra`, not an inferred runtime model label. This metadata correction does not alter the original input hashes, findings, or `WARN` verdict.

## Targeted inputs and actual hashes

| Input | SHA-256 |
|---|---|
| `/home/amd/下载/MAOFIELD_FINAL_AUDIT_V8_R3_20260923/SUBMISSION/manuscript.md` | `83652d21008a186b979c1349835b934c3278a2d6feb319edd13c5a47375d69f5` |
| `/home/amd/下载/MAOFIELD_FINAL_AUDIT_V8_R3_20260923/SUBMISSION/supplementary_information.md` | `d6f770f154699b6679c483ad0bc2d884ae3a0ed7a7d17bae74cd2878d578d30a` |
| `/home/amd/下载/MAOFIELD_FINAL_AUDIT_V8_R3_20260923/QA/TEXT_CHANGE_RECEIPT.json` | `1ebb827128dc34feb70b397bf5fd30d35a6c73fa340c74794b827908f9783eff` |
| `/data/MaoField/.scratch/final_submission_audit_20260923/repository_work/REPRODUCIBILITY/experiment/math_checks.py` | `ac72c3a18c0a1cac87badb5e1da461bb6ae86ae13ae7b7cfd0bdfa6f732889ab` |

The receipt contains three manuscript replacements and seven supplementary replacements. Applying them in memory, once each and in receipt order, to the previously audited inputs reproduces both current documents byte-for-byte. This check verifies the declared text delta; it does not semantically verify the receipt's unrelated compiler-replay claims.

The preserved original audit artifacts remained byte-identical during this resolution:

| Preserved artifact | SHA-256 |
|---|---|
| `PROOF_AUDIT.md` | `e097ba9decd6e2810813f309c786a30d2ab9f9a81c212533c7bce48cacef7aec` |
| `PROOF_AUDIT.json` | `61dcf125436fd36cc92be950fd571cd39c16aca6b4361c5a5558eacf85186f0a` |
| `PROOF_SKELETON.md` | `ffcc6934789870fb1a6fd90c2303f76f38f80fdf7b0206cfa87485422c4f56c9` |

## PA-01 — finite-horizon sufficient-state composition

### Revised proposition

The revised statement fixes common standard Borel spaces and one finite horizon, then specifies:

1. a common measurable exogenous-input kernel and policy kernel conditional on compact state and policy-visible history;
2. a common measurable joint kernel for next observation, cost, and compact state conditional on compact state, visible history, input, and action;
3. no remaining dependence of that joint kernel on hidden state `x`;
4. equal initial compact states and equal initial policy-visible histories;
5. an alternative for unequal initial histories only when **every** kernel above factors through the compact state, leaving no residual history dependence.

Evidence: `/home/amd/下载/MAOFIELD_FINAL_AUDIT_V8_R3_20260923/SUBMISSION/supplementary_information.md:L133-L137`.

These hypotheses close both counterexamples from the original audit:

- Systems with different future-input laws violate the common/matched exogenous-input-kernel hypothesis.
- Systems with different initial visible histories and a last-history-bit policy violate the equal-history branch; they also fail the alternative branch because the policy kernel does not factor through the compact state.

For the first branch, equality of the initial `(compact state, visible history)` pair and equality of the input, policy, and joint successor kernels give the same first-step joint law. Conditioning on each resulting finite history gives the same next-step extension, so ordinary finite induction establishes equality through the fixed horizon. Standard Borel spaces make the stated measurable-kernel composition well-defined.

For the alternative branch, potentially different old histories are irrelevant because all three kernel stages have no residual dependence on them. Equal compact states therefore give the same first extension; the same compact-state-only induction applies thereafter.

### Main-text counterpart

The current main sentence now states:

> Under common joint kernels, matched exogenous-input laws and the initial-history conditions of Supplementary Note 3, factorisation through `c` and a common compact-state update reproduce the relevant finite continuation law.

Evidence: `/home/amd/下载/MAOFIELD_FINAL_AUDIT_V8_R3_20260923/SUBMISSION/manuscript.md:L79-L81`.

The explicit cross-reference imports the two exact initial-history alternatives from the proposition. The earlier ambiguity in which only the policy was said to factor through `c` is absent.

### Claim limits after repair

- The result is for a fixed finite horizon, not an infinite-horizon limit.
- It assumes common kernels; it does not prove that a proposed record is sufficient in a new regime.
- Unequal initial histories are allowed only when every relevant kernel has no residual history dependence beyond the compact state.
- Equality concerns the declared future inputs, actions, observations, costs, and compact successor states. It does not imply equality of hidden causal states, understanding, question quality, or unencoded costs.
- Cost equivalence still depends on construction, retrieval, compaction, and restoration costs being included in the declared cost variable, as retained at `supplementary_information.md:L139`.

**Resolution status: CLOSED.**

## PA-02 — asymptotic scope and uniformity

The new sentence at `supplementary_information.md:L81` declares that throughout Notes 2 and 9:

- the limit is `tau -> 0`;
- `a,b`, the displayed coefficient functions, and the cutoffs are fixed;
- implied constants may depend on those fixed data;
- no uniformity over `a,b` or a class of programs is claimed.

This declaration covers the expansions at `L81-L83`, `L107-L109`, and `L631-L639`. It matches the actual derivations: they are pointwise fixed-program expansions, and vanishing leading coefficients may raise the observed order. No uniform family theorem is introduced.

**Resolution status: CLOSED.**

## PA-03 — basis/amplitude rescaling

The revised paragraph now defines the missing action map:

`b_i' = lambda_i b_i`, `a_i' = a_i/lambda_i`, with `lambda_i>0`.

Therefore

`a_i'b_i' = (a_i/lambda_i)(lambda_i b_i) = a_i b_i`.

With `y_i=a_i²`, `y_i'=y_i/lambda_i²`, `H'=H diag(lambda²)`, and `d_i'=d_i/lambda_i²`, direct componentwise algebra gives

`H'y'=Hy`, and `(d_i'/y_i')=d_i/y_i` wherever the relative-source quotient is defined.

Fresh symbolic remainders for the action identity, ratio identity, and two-component matrix identity were all exactly zero. Evidence: `supplementary_information.md:L119-L123`.

Claim limits retained by the text:

- `lambda_i` is positive, hence non-zero.
- The quotient claim applies where `y_i` is non-zero; the represented-action and matrix identities themselves remain valid at `a_i=0`.
- “Compatible positive slow rescaling” continues to assume the source multiplier and inverse-derivative bounds. The algebra does not certify arbitrary fast or unbounded rescaling or full PDE admissibility.

**Resolution status: CLOSED at the stated algebraic scope.**

## PA-04 — deterministic positive-case assertion

The modified harness now contains

```python
positive_case = ...
assert sp.simplify(positive_case) == 0
```

at `/data/MaoField/.scratch/final_submission_audit_20260923/repository_work/REPRODUCIBILITY/experiment/math_checks.py:L9-L15`.

Executing this exact hashed file with SymPy 1.14.0 completed successfully and reported:

`36 rational cases and 3 symbolic matrix identities: PASS`.

The harness remains an algebra check only; its own header correctly says it is neither a Lean kernel run nor a reconstruction of the full Navier–Stokes proof (`L1-L3`).

**Resolution status: CLOSED.**

## Residual scope boundary

This targeted resolution does not update the original audit verdict for new facts outside PA-01 through PA-04. In particular, it does not inspect the root task's prepared Lean environment, candidates, compiler outputs, or replay receipt. Statements about one accepted and four rejected candidates in the revised manuscript are therefore outside this resolution's semantic evidence and cannot be inferred from the checks reported here.

No manuscript, source, receipt, or original audit artifact was edited by this reviewer.

