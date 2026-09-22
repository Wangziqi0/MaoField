import NavierStokes.PrimaryTargetBounds
set_option linter.unusedVariables false
noncomputable section
open Set Filter Function MeasureTheory
open scoped Topology ContDiff BigOperators
universe u_1


namespace NavierStokes.PrimaryCovarianceBounds
def checkpoint_bridge_goal : Prop :=
  ∀ {X : Type u_1} [TopologicalSpace X] {K : Set X}
    (hK : IsCompact K) (H0 : X → Mat2) (T0 : X → Vec2)
    (hH0 : ∀ i j, ContinuousOn (fun p => H0 p i j) K)
    (hT0 : ∀ i, ContinuousOn (fun p => T0 p i) K)
    (hcone : ∀ p ∈ K, SmoothCovariance.StrictCone (H0 p) (T0 p))
    (vr vt : TorusInverse.Plane) (hdet : vr.1 * vt.2 - vr.2 * vt.1 ≠ 0)
    {r0 h a A b B E D : ℝ} (hr0 : 0 < r0) (hh : 0 ≤ h)
    (ha : 0 < a) (hA : 0 < A) (hb : 0 < b) (hE : 0 ≤ E) (hD : 0 ≤ D),
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
          (FlatCovariance.scaledTarget zeta (T0 p))
end NavierStokes.PrimaryCovarianceBounds


namespace NavierStokes.PrimaryTargetBounds
open BasePhaseGeometry PrimaryCovarianceBounds
def checkpoint_family_goal : Prop :=
  ∀ {h r0 u M : ℝ} (vr vt : TorusInverse.Plane)
    (hdet : vr.1 * vt.2 - vr.2 * vt.1 ≠ 0)
    (hh : 0 ≤ h) (hr : 0 < r0) (hM : 1 ≤ M) (hu : 0 < u) (huM : u ≤ M)
    (hL : 1 / (2*r0) ≤ M) (hslot : 4*r0*ChartScales.Tg ≤ M)
    {eta : ℝ} (heta : 0 < eta),
    ∃ N : ℕ, 4 ≤ N ∧ ∃ detGap entryBound inverseLower : ℝ,
      0 < detGap ∧ 1 ≤ entryBound ∧ 0 < inverseLower ∧
      ∀ (ι : Type u_1) (D : PhaseJetBounds.Domain ι Slow)
        (a : Fin 2 → FamilyData D h r0 u M), CompatiblePair a →
        (∀ j i, LargeBand h M u ((a j).band i)) →
      ∀ i : ι, N ≤ (a 0).band i → ∀ p ∈ D.carrier i, ∀ T : Plane,
        ((a 0).c0 i, (a 0).K i, T) ∈ modelSet M u eta →
      ∀ zeta : ℝ, 0 ≤ zeta →
        ZeroOrderBounds (Real.sqrt (ChartScales.S ((a 0).band i)))
          detGap entryBound inverseLower zeta (familyCovariance vr vt a i p)
          (FlatCovariance.scaledTarget zeta (fun k => T k))
end NavierStokes.PrimaryTargetBounds
