# Additional organization: the result directly applicable to this gap

The source result is PrimaryCovarianceBounds.normalizedPair_entry_error. It transfers the actual pulses' pointwise ratio-error premise to an error bound for their normalized integral matrix. Its exact declaration is already present in the common mathematical inputs.

To apply it at the current gap, match its pulse family to P, its model matrix to H0 p, and its nonnegative error coefficients to the existing E, D, hE, hD. The supplied hP has exactly the required PulseBounds type.

There is one representation mismatch in the pointwise premise: that result uses (slotRadius r0 h n)^2, whereas the existing hratio uses ChartScales.slotLength r0 h n. The established equality slotRadius_sq hr0 rewrites these to the same interval, denominator and center; no new analytical estimate is needed for this step.

The result then bounds the local error by

    (E + D * concentrationConstant a A b B) / slotRadius r0 h n.

The surrounding proof has already defined Q = E + D * |concentrationConstant a A b B| and established hsmall : Q / slotRadius r0 h n ≤ rho. Use concentrationConstant ≤ |concentrationConstant|, D ≥ 0 and the positive radius hr to pass from the result's numerator to Q. Transitivity then reaches the required rho bound.

Remaining work: express this short application, rewrite and scalar comparison in Lean at the existing local goal. This note supplies no tactic script or completed proof body.
