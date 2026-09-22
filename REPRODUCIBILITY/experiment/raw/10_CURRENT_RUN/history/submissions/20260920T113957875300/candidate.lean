import Checkpoint.NodeGoal

noncomputable section
open Set
open NavierStokes NavierStokes.PrimaryCovarianceBounds

namespace Branch.Direct

theorem completed {X : Type*} [TopologicalSpace X] {K : Set X}
    (hK : IsCompact K) (H0 : X → Mat2) (T0 : X → Vec2)
    (hH0 : ∀ i j, ContinuousOn (fun p => H0 p i j) K)
    (hT0 : ∀ i, ContinuousOn (fun p => T0 p i) K)
    (hcone : ∀ p ∈ K, SmoothCovariance.StrictCone (H0 p) (T0 p))
    (vr vt : TorusInverse.Plane) (hdet : vr.1 * vt.2 - vr.2 * vt.1 ≠ 0)
    {r0 h a A b B E D : ℝ} (hr0 : 0 < r0) (hh : 0 ≤ h)
    (ha : 0 < a) (hA : 0 < A) (hb : 0 < b) (hE : 0 ≤ E) (hD : 0 ≤ D) :
    ∃ N : ℕ, 4 ≤ N ∧ ∃ detGap entryBound inverseLower : ℝ,
      0 < detGap ∧ 1 ≤ entryBound ∧ 0 < inverseLower ∧
      ∀ n : ℕ, N ≤ n → ∀ p ∈ K, ∀ P : Fin 2 → PartitionedCovariance.Pulse,
        (∀ j, PulseCovariance.PulseBounds (slotRadius r0 h n) a A b B (P j).ψ (P j).x) →
        (∀ j i v, v ∈ Icc 0 (ChartScales.slotLength r0 h n) →
          |(P j).t v i / (P j).x v - H0 p i j| ≤ E / ChartScales.slotLength r0 h n +
            D * |v - ChartScales.slotLength r0 h n / 2| / ChartScales.slotLength r0 h n) →
        ∀ zeta : ℝ, 0 ≤ zeta →
        ZeroOrderBounds (Real.sqrt (ChartScales.S n)) detGap entryBound inverseLower zeta
          (PartitionedCovariance.pairMatrix vr vt r0 (fun _ => ChartScales.timeCoefficient h n) P)
          (FlatCovariance.scaledTarget zeta (T0 p)) := by
  obtain ⟨rho, delta, M, hrho, hdelta, hM, hmargin⟩ := compact_model_margins hK H0 T0 hH0 hT0 hcone
  let kappa := PartitionedCovariance.nativePrefactor vr vt r0
  have hkappa : 0 < kappa := PartitionedCovariance.nativePrefactor_pos hdet hr0
  let lo := scalarLower kappa r0 a B
  let hi := scalarUpper kappa r0 A b
  have hlo : 0 < lo := scalarLower_pos hkappa hr0 ha
  have hhi : 0 < hi := scalarUpper_pos hkappa hr0 hA hb
  let Q := E + D * |PulseCovariance.concentrationConstant a A b B|
  have hQ : 0 ≤ Q := by dsimp [Q]; positivity
  obtain ⟨N, hN4, hN⟩ := eventually_slotRadius_large hr0 hh (max 1 (Q / rho))
  refine ⟨N, hN4, lo ^ 2 * delta, max 1 (hi * M), delta / hi,
    by positivity, le_max_left _ _, div_pos hdelta hhi, ?_⟩
  intro n hn p hp P hP hratio zeta hzeta
  have hn4 : 4 ≤ n := hN4.trans hn
  have hr : 0 < slotRadius r0 h n := slotRadius_pos hr0 h n
  have hrlarge : Q / rho ≤ slotRadius r0 h n := (le_max_right _ _).trans (hN n hn)
  have hsmall : Q / slotRadius r0 h n ≤ rho := by
    apply (div_le_iff₀ hr).mpr
    have ht := (div_le_iff₀ hrho).mp hrlarge
    nlinarith
  have hclose (i j : Fin 2) : |normalizedPair P i j - H0 p i j| ≤ rho := by
    
    
    have hsl_eq : slotRadius r0 h n ^ 2 = ChartScales.slotLength r0 h n := slotRadius_sq hr0 h n
      have hnorm := normalizedPair_entry_error P hP (H0 p) hE hD (by
        intro j i v hv
        have hv' : v ∈ Icc 0 (ChartScales.slotLength r0 h n) := by
          rw [hsl_eq]
          exact hv
        simpa [hsl_eq] using hratio j i v hv'
      ) i j
      calc
        |normalizedPair P i j - H0 p i j| ≤ (E + D * PulseCovariance.concentrationConstant a A b B) / slotRadius r0 h n := hnorm
        _ ≤ (E + D * |PulseCovariance.concentrationConstant a A b B|) / slotRadius r0 h n := by
          apply (div_le_iff hr).mpr
          have := mul_le_mul_of_nonneg_left (le_abs_self (PulseCovariance.concentrationConstant a A b B)) hD
          linarith
        _ = Q / slotRadius r0 h n := by dsimp [Q]
        _ ≤ rho := hsmall
  obtain ⟨hd, hw, he⟩ := hmargin p hp (normalizedPair P) hclose
  have hscale (j : Fin 2) : lo ≤ Real.sqrt (ChartScales.S n) *
      pairScales kappa (fun _ => ChartScales.timeCoefficient h n) P j ∧
      Real.sqrt (ChartScales.S n) * pairScales kappa (fun _ => ChartScales.timeCoefficient h n) P j ≤ hi :=
    chart_column_mass_bounds hr0 hh hkappa hn4 (hP j)
  have hR : 0 < Real.sqrt (ChartScales.S n) := Real.sqrt_pos.mpr (ChartScales.S_pos (by omega))
  have hbounds := column_scale_bounds (normalizedPair P) (T0 p)
    (pairScales kappa (fun _ => ChartScales.timeCoefficient h n) P)
    hR hlo hhi hdelta hzeta hscale hd hw he
  rw [pairMatrix_factorization P hP vr vt r0]
  exact ⟨hbounds.1, fun i j => (hbounds.2.1 i j).trans (le_max_right _ _), hbounds.2.2⟩

end Branch.Direct

#check (Branch.Direct.completed : NavierStokes.PrimaryCovarianceBounds.checkpoint_bridge_goal)
#print axioms Branch.Direct.completed
