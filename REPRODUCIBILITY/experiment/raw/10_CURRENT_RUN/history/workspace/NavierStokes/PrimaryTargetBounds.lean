import NavierStokes.BasePhaseGeometry
import NavierStokes.AlignedProfileSpectralCone
import NavierStokes.PrimaryGeometryAssembly









noncomputable section

open Set Filter Function Matrix
open scoped Topology ContDiff InnerProductSpace BigOperators

namespace NavierStokes.PrimaryTargetBounds

abbrev Plane := MovingFrameODE.Plane
abbrev Slow := PhaseCalculus.Slow
abbrev Mat2 := SmoothCovariance.Mat2
abbrev Vec2 := SmoothCovariance.Vec2


noncomputable def phaseSign (j : Fin 2) : ℝ := if j = 0 then 1 else -1

theorem phaseSign_abs (j : Fin 2) : |phaseSign j| = 1 := by
  fin_cases j <;> norm_num [phaseSign]


noncomputable def basisMatrix (K : Plane) : Mat2 :=
  fun i j => if j = 0 then MovingFrameODE.quarterTurn K i else K i

noncomputable def modelMatrix (c u : ℝ) (K : Plane) : Mat2 :=
  basisMatrix K * PulseCovariance.signedModel c u

noncomputable def modelNormal (K T : Plane) : ℝ := -⟪T, MovingFrameODE.quarterTurn K⟫_ℝ
noncomputable def modelTransverse (K T : Plane) : ℝ := ⟪T, K⟫_ℝ

theorem basisMatrix_det (K : Plane) (hK : ‖K‖ = 1) : (basisMatrix K).det = -1 := by
  have hs := ViscousPropagator.plane_norm_sq K
  rw [hK, one_pow] at hs
  simp only [basisMatrix, Matrix.det_fin_two, ite_true, show (1 : Fin 2) ≠ 0 by decide,
    ite_false]
  change -K 1 * K 1 - K 0 * K 0 = -1
  nlinarith

theorem modelMatrix_column (c u : ℝ) (K : Plane) (i j : Fin 2) :
    modelMatrix c u K i j =
      c * Real.sqrt (1 + u ^ 2) * MovingFrameODE.quarterTurn K i - phaseSign j * u * K i := by
  fin_cases j <;>
    simp [modelMatrix, basisMatrix, Matrix.mul_apply, Fin.sum_univ_two,
      PulseCovariance.signedModel, PulseCovariance.modelDirection, PulseCovariance.signedSlopes,
      PulseCovariance.radiusProfile, phaseSign] <;> ring

theorem basisMatrix_target (K T : Plane) (hK : ‖K‖ = 1) :
    (basisMatrix K).mulVec (Covariance.target (modelNormal K T) (modelTransverse K T)) =
      (fun i => T i) := by
  have hs := ViscousPropagator.plane_norm_sq K
  rw [hK, one_pow] at hs
  ext i
  fin_cases i <;>
    simp [basisMatrix, Covariance.target, modelNormal, modelTransverse, Matrix.mulVec,
      dotProduct, Fin.sum_univ_two, PiLp.inner_apply, MovingFrameODE.quarterTurn] <;>
    nlinarith [congrArg (fun x : ℝ => x * T 0) hs, congrArg (fun x : ℝ => x * T 1) hs]

theorem weights_unique {H : Mat2} {T z : Vec2} (hd : H.det ≠ 0) (he : H.mulVec z = T) :
    SmoothCovariance.weights H T = z := by
  rw [← SmoothCovariance.inverse_formula H T hd, ← he, Matrix.mulVec_mulVec,
    Matrix.nonsing_inv_mul H (isUnit_iff_ne_zero.mpr hd), Matrix.one_mulVec]

theorem strictCone_mul_left {B H : Mat2} {T : Vec2} (hB : B.det ≠ 0)
    (hH : SmoothCovariance.StrictCone H T) :
    SmoothCovariance.StrictCone (B * H) (B.mulVec T) := by
  have he : SmoothCovariance.weights (B * H) (B.mulVec T) = SmoothCovariance.weights H T :=
    weights_unique (by rw [Matrix.det_mul]; exact mul_ne_zero hB hH.det_ne_zero)
      (by rw [← Matrix.mulVec_mulVec, SmoothCovariance.reconstruct H T hH.det_ne_zero])
  apply (SmoothCovariance.weights_pos_iff _ _).mp
  intro j
  rw [he]
  exact hH.weights_pos j

theorem modelMatrix_strictCone {c u eta : ℝ} {K T : Plane}
    (hc : c < 0) (hu : 0 < u) (heta : 0 < eta) (hK : ‖K‖ = 1)
    (hm : eta ≤ modelNormal K T)
    (hr : |c * modelTransverse K T| ≤
      (PrimaryRepresentatives.slopeRatio u - eta) * modelNormal K T) :
    SmoothCovariance.StrictCone (modelMatrix c u K) (fun i => T i) := by
  have hmp : 0 < modelNormal K T := heta.trans_le hm
  have hratio : |c * modelTransverse K T / modelNormal K T| <
      u / Real.sqrt (1 + u ^ 2) := by
    rw [abs_div, abs_of_pos hmp]
    apply (div_lt_iff₀ hmp).mpr
    have hh := mul_pos heta hmp
    change |c * modelTransverse K T| < PrimaryRepresentatives.slopeRatio u * modelNormal K T
    nlinarith
  have hbase := PulseCovariance.signedModel_strictCone hc hu (Covariance.cone_of_ratio hmp hratio)
  have hh := strictCone_mul_left (B := basisMatrix K) (by rw [basisMatrix_det K hK]; norm_num) hbase
  rwa [basisMatrix_target K T hK] at hh

abbrev ModelPoint := ℝ × (Plane × Plane)

noncomputable def modelSet (M u eta : ℝ) : Set ModelPoint :=
  {p | p.1 ∈ Icc (-M) (-(1 / M)) ∧ ‖p.2.1‖ = 1 ∧ ‖p.2.2‖ = 1 ∧
    eta ≤ modelNormal p.2.1 p.2.2 ∧
    |p.1 * modelTransverse p.2.1 p.2.2| ≤
      (PrimaryRepresentatives.slopeRatio u - eta) * modelNormal p.2.1 p.2.2}

theorem modelNormal_continuous : Continuous (fun p : ModelPoint => modelNormal p.2.1 p.2.2) :=
  ((continuous_snd.snd.inner (MovingFrameODE.quarterTurn.continuous.comp continuous_snd.fst))).neg

theorem modelTransverse_continuous : Continuous (fun p : ModelPoint => modelTransverse p.2.1 p.2.2) :=
  continuous_snd.snd.inner continuous_snd.fst

theorem modelSet_compact (M u eta : ℝ) : IsCompact (modelSet M u eta) := by
  have hcomp : IsCompact ((Icc (-M) (-(1 / M))) ×ˢ
      (Metric.sphere (0 : Plane) 1 ×ˢ Metric.sphere (0 : Plane) 1)) :=
    isCompact_Icc.prod ((isCompact_sphere 0 1).prod (isCompact_sphere 0 1))
  have hclosed : IsClosed {p : ModelPoint | eta ≤ modelNormal p.2.1 p.2.2 ∧
      |p.1 * modelTransverse p.2.1 p.2.2| ≤
        (PrimaryRepresentatives.slopeRatio u - eta) * modelNormal p.2.1 p.2.2} :=
    (isClosed_le continuous_const modelNormal_continuous).inter
      (isClosed_le (continuous_fst.mul modelTransverse_continuous).abs
        (continuous_const.mul modelNormal_continuous))
  convert! hcomp.inter_right hclosed using 1
  ext p
  simp only [modelSet, Set.mem_ofPred_eq, mem_inter_iff, mem_prod, Metric.mem_sphere,
    dist_zero_right]
  tauto

theorem modelMatrix_continuous (u : ℝ) (i j : Fin 2) :
    Continuous (fun p : ModelPoint => modelMatrix p.1 u p.2.1 i j) := by
  simp_rw [modelMatrix_column]
  fun_prop

theorem compact_model_data {M u eta : ℝ} (hM : 1 ≤ M) (hu : 0 < u) (heta : 0 < eta) :
    (∀ i j, ContinuousOn (fun p : ModelPoint => modelMatrix p.1 u p.2.1 i j) (modelSet M u eta)) ∧
    (∀ i, ContinuousOn (fun p : ModelPoint => p.2.2 i) (modelSet M u eta)) ∧
    ∀ p ∈ modelSet M u eta,
      SmoothCovariance.StrictCone (modelMatrix p.1 u p.2.1) (fun i => p.2.2 i) := by
  refine ⟨fun i j => (modelMatrix_continuous u i j).continuousOn,
    fun i => (show Continuous (fun p : ModelPoint => p.2.2 i) by fun_prop).continuousOn, ?_⟩
  intro p hp
  have hc : p.1 < 0 := hp.1.2.trans_lt (neg_neg_of_pos (one_div_pos.mpr (zero_lt_one.trans_le hM)))
  exact modelMatrix_strictCone hc hu heta hp.2.1 hp.2.2.2.1 hp.2.2.2.2

noncomputable def modelVector (c s : ℝ) (K : Plane) : Plane :=
  (-s) • K + (c * Real.sqrt (1 + s ^ 2)) • MovingFrameODE.quarterTurn K

theorem modelVector_column (c u : ℝ) (K : Plane) (j i : Fin 2) :
    modelVector c (phaseSign j * u) K i = modelMatrix c u K i j := by
  have hs : (phaseSign j * u) ^ 2 = u ^ 2 := by
    fin_cases j <;> simp [phaseSign]
  rw [modelMatrix_column]
  simp only [modelVector, PiLp.add_apply, PiLp.smul_apply, smul_eq_mul, hs]
  ring

theorem modelVector_lipschitz (c s t : ℝ) (K : Plane) (hK : ‖K‖ = 1) :
    ‖modelVector c s K - modelVector c t K‖ ≤ (|c| + 1) * |s - t| := by
  have he : modelVector c s K - modelVector c t K =
      (t-s) • K + (c * (PulseCovariance.radiusProfile s - PulseCovariance.radiusProfile t)) •
        MovingFrameODE.quarterTurn K := by
    unfold modelVector PulseCovariance.radiusProfile
    module
  rw [he]
  calc
    _ ≤ ‖(t-s) • K‖ + ‖(c * (PulseCovariance.radiusProfile s - PulseCovariance.radiusProfile t)) •
        MovingFrameODE.quarterTurn K‖ := norm_add_le _ _
    _ = |s-t| + |c| * |PulseCovariance.radiusProfile s - PulseCovariance.radiusProfile t| := by
      simp only [norm_smul, Real.norm_eq_abs, hK, PhaseEstimates.quarterTurn_norm, mul_one, abs_mul,
        abs_sub_comm t s]
    _ ≤ |s-t| + |c| * |s-t| := add_le_add_right
      (mul_le_mul_of_nonneg_left (PulseCovariance.radiusProfile_lipschitz s t) (abs_nonneg c)) _
    _ = _ := by ring

theorem frame_combination_error (k K : Plane) (hk : ‖k‖ = 1) (a b a0 b0 : ℝ) :
    ‖a • k + b • MovingFrameODE.quarterTurn k -
      (a0 • K + b0 • MovingFrameODE.quarterTurn K)‖ ≤
      |a-a0| + |b-b0| + (|a0| + |b0|) * ‖k-K‖ := by
  have he : a • k + b • MovingFrameODE.quarterTurn k -
      (a0 • K + b0 • MovingFrameODE.quarterTurn K) =
      ((a-a0) • k + (b-b0) • MovingFrameODE.quarterTurn k) +
        (a0 • (k-K) + b0 • MovingFrameODE.quarterTurn (k-K)) := by
    rw [map_sub]
    module
  rw [he]
  calc
    _ ≤ ‖(a-a0) • k + (b-b0) • MovingFrameODE.quarterTurn k‖ +
        ‖a0 • (k-K) + b0 • MovingFrameODE.quarterTurn (k-K)‖ := norm_add_le _ _
    _ ≤ (‖(a-a0) • k‖ + ‖(b-b0) • MovingFrameODE.quarterTurn k‖) +
        (‖a0 • (k-K)‖ + ‖b0 • MovingFrameODE.quarterTurn (k-K)‖) :=
      add_le_add (norm_add_le _ _) (norm_add_le _ _)
    _ = _ := by
      simp only [norm_smul, Real.norm_eq_abs, PhaseEstimates.quarterTurn_norm, hk, mul_one]
      ring

theorem tangent_ratio_error {n : MovingFrameODE.Space} {K : Plane} {B s delta r h : ℝ}
    (hB : 0 < B) (hK : ‖K‖ = 1) (hd : delta ≤ B / 2)
    (hn : ‖n - MovingFrameODE.pack (B*s) (B • K)‖ ≤ delta) :
    ‖(-MovingFrameODE.radialSlope n) • MovingFrameODE.normalDirection n +
        r • MovingFrameODE.quarterTurn (MovingFrameODE.normalDirection n) -
      ((-s) • K + h • MovingFrameODE.quarterTurn K)‖ ≤
        (2 * (1 + |s|) + 4 * (|s| + |h|)) * delta / B + |r-h| := by
  have hne := (PhaseEstimates.normal_lower_bounds hB hK hd hn).2.2.1
  have he := frame_combination_error (MovingFrameODE.normalDirection n) K
    (MovingFrameODE.normalDirection_unit hne) (-MovingFrameODE.radialSlope n) r (-s) h
  have hs := PhaseEstimates.radialSlope_close hB hK hd hn
  have hk := PhaseEstimates.normalDirection_close hB hK hd hn
  have hss : |-MovingFrameODE.radialSlope n - -s| = |MovingFrameODE.radialSlope n - s| := by
    rw [← abs_neg]
    congr 1
    ring
  rw [hss, abs_neg] at he
  calc
    _ ≤ |MovingFrameODE.radialSlope n - s| + |r-h| +
        (|s| + |h|) * ‖MovingFrameODE.normalDirection n-K‖ := he
    _ ≤ 2 * (1 + |s|) * delta / B + |r-h| + (|s| + |h|) * (4*delta/B) :=
      add_le_add (add_le_add_left hs _) (mul_le_mul_of_nonneg_left hk (by positivity))
    _ = _ := by ring

noncomputable def pulseRatio (d : PrimaryODE.FrameData Slow) (lam u L : ℝ) (p : Slow) (v : ℝ) : Plane :=
  !₂[PrimaryPulseBounds.normalizedPulse d lam u L (p, v/L) 1 /
      PrimaryPulseBounds.normalizedPulse d lam u L (p, v/L) 0,
    PrimaryPulseBounds.normalizedPulse d lam u L (p, v/L) 2 /
      PrimaryPulseBounds.normalizedPulse d lam u L (p, v/L) 0]

theorem pulseRatio_eq (d : PrimaryODE.FrameData Slow) (lam u : ℝ) {L : ℝ} (hL : 0 < L)
    {U : Set Slow} (hA : ContinuousOn (d.coefficient 1) (U ×ˢ Icc 0 L))
    {p : Slow} (hp : p ∈ U) {v : ℝ} (hv : v ∈ Icc 0 L)
    (hx : PrimaryODE.radialPrimary hL.le d
      (fun z => PrimaryPulseBounds.referenceP lam u L z.2) p v ≠ 0) :
    pulseRatio d lam u L p v =
      (-d.rho (p,v)) • d.frame (p,v) 0 +
        (PrimaryODE.transversePrimary hL.le d (fun z => PrimaryPulseBounds.referenceP lam u L z.2) p v /
          PrimaryODE.radialPrimary hL.le d (fun z => PrimaryPulseBounds.referenceP lam u L z.2) p v) •
            d.frame (p,v) 1 := by
  have hLv : L * (v / L) = v := by field_simp
  unfold pulseRatio PrimaryPulseBounds.normalizedPulse
  rw [hLv, PrimaryPulseBounds.fundamental_eq_primary hL U hA hp hv]
  ext i
  fin_cases i <;>
    simp [PrimaryODE.FrameData.ambient, MovingFrameODE.tangent, MovingFrameODE.pack,
      PiLp.add_apply, PiLp.smul_apply, smul_eq_mul, PrimaryODE.radialPrimary,
      PrimaryODE.transversePrimary] at * <;>
    field_simp

noncomputable def geometricRatioConstant (M u : ℝ) : ℝ :=
  (2 * (1 + 3*M) + 4 * (3*M + BasePhaseGeometry.eigenBound M)) *
    BasePhaseGeometry.phaseConstant M / BasePhaseGeometry.normalLower M u

noncomputable def ratioConstant (M u gap : ℝ) : ℝ :=
  geometricRatioConstant M u + 4 * BasePhaseGeometry.eigenBound M *
    GrowingMode.coneConstant gap (BasePhaseGeometry.modalConstant M u)

theorem geometricRatioConstant_nonneg {M u : ℝ} (hM : 1 ≤ M) : 0 ≤ geometricRatioConstant M u := by
  have hnormal := (BasePhaseGeometry.normalLower_pos (u := u) hM).le
  have hp := (BasePhaseGeometry.phaseConstant_pos hM).le
  have hM0 : 0 ≤ M := zero_le_one.trans hM
  unfold geometricRatioConstant BasePhaseGeometry.eigenBound
  positivity

theorem ratioConstant_nonneg {M u gap : ℝ} (hM : 1 ≤ M) (hgap : 0 < gap) :
    0 ≤ ratioConstant M u gap := by
  have hg := geometricRatioConstant_nonneg (u := u) hM
  have hC := (BasePhaseGeometry.error_constants_nonneg (u := u) hM).2.1
  have hM0 : 0 ≤ M := zero_le_one.trans hM
  unfold ratioConstant GrowingMode.coneConstant BasePhaseGeometry.eigenBound
  positivity

theorem signedSlot_center {u L : ℝ} (hu : 0 ≤ u) (hL : 0 < L)
    (j : Fin 2) (v : ℝ) :
    |PhaseEstimates.signedSlot (phaseSign j) u L v - phaseSign j * u| =
      u * |v - L / 2| / L := by
  have he : PhaseEstimates.signedSlot (phaseSign j) u L v - phaseSign j * u =
      phaseSign j * u * (v-L/2) / L := by
    unfold PhaseEstimates.signedSlot
    field_simp ; ring
  rw [he, abs_div, abs_mul, abs_mul, phaseSign_abs, one_mul, abs_of_nonneg hu,
    abs_of_pos hL]

section FamilyRatio

open BasePhaseGeometry

variable {ι : Type*} {D : PhaseJetBounds.Domain ι Slow} {h r0 u M : ℝ}
    (a : FamilyData D h r0 u M)
    (hh : 0 ≤ h) (hr : 0 < r0) (hM : 1 ≤ M) (hu : 0 < u) (huM : u ≤ M)
    (hL : 1 / (2 * r0) ≤ M) (hslot : 4 * r0 * ChartScales.Tg ≤ M)
    (hlarge : ∀ i, LargeBand h M u (a.band i))

include hh hr hM hu huM hL hslot hlarge

theorem coefficient_continuous (i : ι) :
    ContinuousOn ((a.frame i).coefficient 1) (D.carrier i ×ˢ Icc 0 (a.length i)) :=
  ((a.coefficient_jets hh hr hM hu huM hL hslot hlarge 1).smooth i).continuousOn.mono
    (fun _ hz => ⟨hz.1, a.interval_subset_slot hr i hz.2⟩)

theorem primary_ratio_error (i : ι) {p : Slow} (hp : p ∈ D.carrier i)
    {gap : ℝ} (hgap : 0 < gap)
    (hg : ∀ v ∈ Icc 0 (a.length i),
      gap ≤ ViscousPropagator.referenceEigenvalue (a.lam i) u (a.length i) v)
    (hcone : 2 * GrowingMode.coneConstant gap (modalConstant M u) ≤ D.scale i)
    {v : ℝ} (hv : v ∈ Icc 0 (a.length i)) :
    ‖pulseRatio (a.frame i) (a.lam i) u (a.length i) p v -
      modelVector (a.c0 i) (a.slope i (p,v)) (a.K i)‖ ≤ ratioConstant M u gap / D.scale i := by
  have hlength := a.length_pos hr i
  have hS : 0 < D.scale i := zero_lt_one.trans_le (D.one_le_scale i)
  have hc := a.coefficientControl hh hr hM hu huM hL hslot i (hlarge i) hp
  have hA := coefficient_continuous a hh hr hM hu huM hL hslot hlarge i
  have hslotL : a.length i ≤ (2*r0*ChartScales.Tg) * D.scale i := by
    simpa only [FamilyData.length, a.scale_eq i, mul_assoc] using
      (ChartScales.slotLength_bounds r0 h hr.le hh (hlarge i).four_le).2
  have hP (t : ℝ) (_ht : t ∈ Icc 0 (a.length i)) :=
    PrimaryPulseBounds.referenceP_pos (a.lam i) u (a.length i) t
  have hPeq (t : ℝ) (ht : t ∈ Icc 0 (a.length i)) :
      HasDerivAt (PrimaryPulseBounds.referenceP (a.lam i) u (a.length i))
        (((a.frame i).eigenvalue (p,t) - ViscousPropagator.referenceViscosity (a.lam i) u (a.length i) t) *
          PrimaryPulseBounds.referenceP (a.lam i) u (a.length i) t) t := by
    rw [hc.eigenvalue t ht]
    exact PrimaryPulseBounds.referenceP_hasDerivAt _ _ _ _
  have herrors := error_constants_nonneg (u := u) hM
  have hprimary := PrimaryODE.primary_bounds hlength.le (a.frame i)
    (fun z => PrimaryPulseBounds.referenceP (a.lam i) u (a.length i) z.2)
    hA hp hgap herrors.2.1 herrors.2.2 hS hcone (by simpa using hslotL)
    (ViscousPropagator.referenceViscosity (a.lam i) u (a.length i))
    (fun t ht => by rw [hc.eigenvalue t ht]; exact hg t ht)
    hc.errors hc.viscosity hP hPeq v hv
  have hv' := a.interval_subset_slot hr i hv
  have hnormal := (a.phase_estimates hh hr hM (by simpa only [abs_of_pos hu] using huM)
    hL hslot i (hlarge i) hp hv').1
  have hsmall := a.phase_error_small hh hM i (hlarge i)
  have hB := a.B_pos hh hM i
  have hne := (PhaseEstimates.normal_lower_bounds hB (a.unit i) hsmall hnormal).2.2.1
  have hs := a.slope_bound hr hu.le huM (q := p) hv'
  have hprof := reference_profile_bounds (one_div_pos.mpr (zero_lt_one.trans_le hM))
    (a.ratio_bound i).1 (a.ratio_bound i).2 (a.magnitude_bound hr hu.le huM hv')
  have hH : |PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v| ≤ eigenBound M :=
    hprof.1.trans (by unfold eigenBound; nlinarith [show 0 ≤ M by linarith])
  have hgeom := tangent_ratio_error hB (a.unit i) hsmall hnormal
    (r := PrimaryODE.transversePrimary hlength.le (a.frame i)
      (fun z => PrimaryPulseBounds.referenceP (a.lam i) u (a.length i) z.2) p v /
      PrimaryODE.radialPrimary hlength.le (a.frame i)
        (fun z => PrimaryPulseBounds.referenceP (a.lam i) u (a.length i) z.2) p v)
    (h := PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v)
  have hsq : (a.slope i (p,v))^2 = PulseGrowth.slotMagnitude u (a.length i) v ^ 2 :=
    signedSlot_sq (a.sign i) u (a.length i) v
  have hprofile : PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v =
      a.c0 i * Real.sqrt (1 + (a.slope i (p,v))^2) := by
    rw [hsq]
    rfl
  have he : pulseRatio (a.frame i) (a.lam i) u (a.length i) p v -
      modelVector (a.c0 i) (a.slope i (p,v)) (a.K i) =
      (-MovingFrameODE.radialSlope (a.phase.normal i (p,v))) •
          MovingFrameODE.normalDirection (a.phase.normal i (p,v)) +
        (PrimaryODE.transversePrimary hlength.le (a.frame i)
          (fun z => PrimaryPulseBounds.referenceP (a.lam i) u (a.length i) z.2) p v /
          PrimaryODE.radialPrimary hlength.le (a.frame i)
            (fun z => PrimaryPulseBounds.referenceP (a.lam i) u (a.length i) z.2) p v) •
          MovingFrameODE.quarterTurn (MovingFrameODE.normalDirection (a.phase.normal i (p,v))) -
        ((-a.slope i (p,v)) • a.K i +
          PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v • MovingFrameODE.quarterTurn (a.K i)) := by
    rw [pulseRatio_eq (a.frame i) (a.lam i) u hlength hA hp hv hprimary.1.ne']
    simp only [FamilyData.frame, PhaseJetBounds.PhaseFamily.frameData, PrimaryODE.FrameData.ofNormalLocal,
      PrimaryODE.localFrame_eq hne, MovingFrameODE.normalFrame_zero, MovingFrameODE.normalFrame_one]
    rw [hprofile]
    rfl
  rw [he]
  apply hgeom.trans
  have hBmin := (a.B_bounds hh hM i).1
  have hcoef : 0 ≤ 2*(1+3*M)+4*(3*M+eigenBound M) := by unfold eigenBound; positivity
  have hph : 0 ≤ phaseConstant M / D.scale i := div_nonneg (phaseConstant_pos hM).le hS.le
  have hgeometric :
      (2*(1+|a.slope i (p,v)|)+4*(|a.slope i (p,v)|+
        |PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v|)) *
          (phaseConstant M / D.scale i) / a.B i ≤ geometricRatioConstant M u / D.scale i := by
    calc
      _ ≤ (2*(1+3*M)+4*(3*M+eigenBound M)) * (phaseConstant M / D.scale i) / a.B i :=
        div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_right (by linarith) hph) hB.le
      _ ≤ (2*(1+3*M)+4*(3*M+eigenBound M)) * (phaseConstant M / D.scale i) / normalLower M u :=
        div_le_div_of_nonneg_left (mul_nonneg hcoef hph) (normalLower_pos hM) hBmin
      _ = _ := by unfold geometricRatioConstant; ring
  have hconeNonneg : 0 ≤ GrowingMode.coneConstant gap (modalConstant M u) := by
    unfold GrowingMode.coneConstant
    exact div_nonneg (mul_nonneg (by norm_num) (by linarith [herrors.2.1])) hgap.le
  have hratiobound := hprimary.2.2.2
  change |PrimaryODE.transversePrimary _ _ _ _ _ / PrimaryODE.radialPrimary _ _ _ _ _ -
    PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v| ≤ _ at hratiobound
  have hratiobound' := hratiobound.trans (mul_le_mul_of_nonneg_right
    (show 4 * |PrimaryODE.referenceProfile (a.c0 i) u (a.length i) v| ≤ 4 * eigenBound M by linarith)
    (div_nonneg hconeNonneg hS.le))
  exact (add_le_add hgeometric hratiobound').trans_eq (by unfold ratioConstant; ring)




theorem primary_center_error (i : ι) (j : Fin 2) (hsign : a.sigma i = phaseSign j)
    {p : Slow} (hp : p ∈ D.carrier i) {gap : ℝ} (hgap : 0 < gap)
    (hg : ∀ v ∈ Icc 0 (a.length i),
      gap ≤ ViscousPropagator.referenceEigenvalue (a.lam i) u (a.length i) v)
    (hcone : 2 * GrowingMode.coneConstant gap (modalConstant M u) ≤ D.scale i)
    {v : ℝ} (hv : v ∈ Icc 0 (a.length i)) (k : Fin 2) :
    |PrimaryPulseBounds.normalizedPulse (a.frame i) (a.lam i) u (a.length i)
          (p,v / a.length i) k.succ /
        PrimaryPulseBounds.normalizedPulse (a.frame i) (a.lam i) u (a.length i)
          (p,v / a.length i) 0 - modelMatrix (a.c0 i) u (a.K i) k j| ≤
      ((2*r0*ChartScales.Tg) * ratioConstant M u gap) / a.length i +
        ((M+1)*u) * |v-a.length i/2| / a.length i := by
  have hlength := a.length_pos hr i
  have hS : 0 < D.scale i := zero_lt_one.trans_le (D.one_le_scale i)
  have hslotL : a.length i ≤ (2*r0*ChartScales.Tg) * D.scale i := by
    simpa only [FamilyData.length, a.scale_eq i, mul_assoc] using
      (ChartScales.slotLength_bounds r0 h hr.le hh (hlarge i).four_le).2
  have hratio := primary_ratio_error a hh hr hM hu huM hL hslot hlarge i hp hgap hg hcone hv
  have hslope : |a.slope i (p,v) - phaseSign j*u| = u*|v-a.length i/2|/a.length i := by
    simpa only [FamilyData.slope, hsign] using signedSlot_center hu.le hlength j v
  have hmodel := modelVector_lipschitz (a.c0 i) (a.slope i (p,v)) (phaseSign j*u) (a.K i) (a.unit i)
  rw [hslope] at hmodel
  have hbound : ‖pulseRatio (a.frame i) (a.lam i) u (a.length i) p v -
      modelVector (a.c0 i) (phaseSign j*u) (a.K i)‖ ≤
      ratioConstant M u gap / D.scale i + ((M+1)*u)*|v-a.length i/2|/a.length i := by
    apply (norm_sub_le_norm_sub_add_norm_sub _ _ _).trans
    apply add_le_add hratio
    apply hmodel.trans
    calc
      _ ≤ (M+1) * (u*|v-a.length i/2|/a.length i) :=
        mul_le_mul_of_nonneg_right (by linarith [(a.ratio_bound i).2]) (by positivity)
      _ = _ := by ring
  have hratioL : ratioConstant M u gap / D.scale i ≤
      ((2*r0*ChartScales.Tg) * ratioConstant M u gap) / a.length i := by
    apply (div_le_div_iff₀ hS hlength).mpr
    nlinarith [mul_le_mul_of_nonneg_left hslotL (ratioConstant_nonneg (u := u) hM hgap)]
  have hcomponent := (PiLp.norm_apply_le
    (pulseRatio (a.frame i) (a.lam i) u (a.length i) p v -
      modelVector (a.c0 i) (phaseSign j*u) (a.K i)) k)
  have he : (pulseRatio (a.frame i) (a.lam i) u (a.length i) p v -
      modelVector (a.c0 i) (phaseSign j*u) (a.K i)) k =
      PrimaryPulseBounds.normalizedPulse (a.frame i) (a.lam i) u (a.length i)
          (p,v / a.length i) k.succ /
        PrimaryPulseBounds.normalizedPulse (a.frame i) (a.lam i) u (a.length i)
          (p,v / a.length i) 0 - modelMatrix (a.c0 i) u (a.K i) k j := by
    rw [PiLp.sub_apply, modelVector_column]
    fin_cases k <;> rfl
  rw [he, Real.norm_eq_abs] at hcomponent
  exact hcomponent.trans (hbound.trans (add_le_add_left hratioL _))

end FamilyRatio

section FamilyPair

open BasePhaseGeometry PrimaryCovarianceBounds

variable {ι : Type*} {D : PhaseJetBounds.Domain ι Slow} {h r0 u M : ℝ}


structure CompatiblePair (a : Fin 2 → FamilyData D h r0 u M) : Prop where
  band : ∀ j i, (a j).band i = (a 0).band i
  ratio : ∀ j i, (a j).c0 i = (a 0).c0 i
  transverse : ∀ j i, (a j).K i = (a 0).K i
  sign : ∀ j i, (a j).sigma i = phaseSign j


noncomputable def familyCovariance (vr vt : TorusInverse.Plane)
    (a : Fin 2 → FamilyData D h r0 u M) (i : ι) (p : Slow) : Mat2 :=
  PrimaryPulseBounds.primaryCovariance
    (fun j i => PartitionedCovariance.nativePrefactor vr vt r0 *
      ChartScales.timeCoefficient h ((a j).band i) * (a j).length i)
    (fun j => (a j).frame) (fun j => (a j).lam) (fun _ _ => u)
    (fun j => (a j).length) i p

theorem familyCovariance_eq_native (vr vt : TorusInverse.Plane)
    (a : Fin 2 → FamilyData D h r0 u M) (hc : CompatiblePair a) (i : ι) (p : Slow) :
    familyCovariance vr vt a i p = nativePrimaryCovariance vr vt r0 h
      (fun j _ => (a j).frame i) (fun j _ => (a j).lam i) (fun _ _ => u)
      ((a 0).band i) p := by
  unfold familyCovariance nativePrimaryCovariance PrimaryPulseBounds.primaryCovariance
  ext r c
  change _ * _ = _ * _
  simp only [FamilyData.length, hc.band]


end FamilyPair
end NavierStokes.PrimaryTargetBounds
