# Deterministic mathematical reproduction

`python exact_checks.py --out result.json` computes symbolic identities with SymPy. It does not read expected results or invoke a model, network or Lean. The all-quantifier minimax assertion and smooth-domain claims are proved in SI Notes 2–3; the code checks algebra and boundary constants, not all analysis.

Notation: z=1+u; p=z²+r; g is applied increment; E=(z+g)²−p. For separation 0<r≤1/4,0<v≤1/8 and the same deterministic g is used at z±=1±v, with different targets p±. The safe outer rectangle is r∈[-1/2,1/2],u∈[-1/4,1/4]; inner cutoff |r|≤1/4,|u|≤1/8. No random sample is generated.

| Claim | Proof | Code | Figure |
|---|---|---|---|
| Full residual / state cross term | SI2.1 and Note9 | complete_residual_decomposition | 2 |
| Same-r separation / minimax | SI 2.3 (piecewise proof; setup in SI 2.2) | difference, resultant, minimax candidate, reflection | 2 |
| State-aware repair / domain | SI 2.5 | rationalization, radicand margin, cutoff expansion | 2 |
| Non-monotone full residual | SI 2.6 | successor_counterexample | SI |
| Sufficient compact representation | SI3 induction | not falsely reduced to finite tests | 1 |
| Actual successor formula series and state inheritance | SI9; original programmes | successor/audit_successor.py | 4 |
| hclose estimate | SI4, original template | experiment/math_checks.py | 3 |
