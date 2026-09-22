# Common mathematical inputs

Both arms receive these identical existing declarations from NavierStokes.PrimaryCovarianceBounds. Their actual proofs are already available in the retained imported source. The fixed surrounding proof supplies the other parameters and assumptions.

```lean
theorem slotRadius_sq {r0 : ℝ} (hr0 : 0 < r0) (h : ℝ) (n : ℕ) :
    slotRadius r0 h n ^ 2 = ChartScales.slotLength r0 h n
```

```lean
noncomputable def normalizedPair (P : Fin 2 → PartitionedCovariance.Pulse) : Mat2 :=
  fun i j => PulseCovariance.normalizedColumn (P j).ψ (P j).x (P j).t i
```

```lean
theorem normalizedPair_entry_error {r a A b B E D : ℝ}
    (P : Fin 2 → PartitionedCovariance.Pulse)
    (hP : ∀ j, PulseCovariance.PulseBounds r a A b B (P j).ψ (P j).x)
    (H0 : Mat2) (hE : 0 ≤ E) (hD : 0 ≤ D)
    (hratio : ∀ j i v, v ∈ Icc 0 (r ^ 2) →
      |(P j).t v i / (P j).x v - H0 i j| ≤
        E / r ^ 2 + D * |v - r ^ 2 / 2| / r ^ 2) (i j : Fin 2) :
    |normalizedPair P i j - H0 i j| ≤
      (E + D * PulseCovariance.concentrationConstant a A b B) / r
```
