import CRPI.Direction

/-!
# CRPI exact stock-flow transition

Independent real-valued formalization of
  dS/dt = beta * R_inst * (1-S) - kappa * M * S
under piecewise-constant R_inst and M on a reporting interval.

This module checks properties of the manuscript's exact exponential interval
transition; it does not claim a general time-varying ODE solution theorem.
-/

namespace CRPI

/-- Accumulation term a = beta * R_inst (inverse-time rate). -/
def accumulationRate (beta residual : ℝ) : ℝ := beta * residual

/-- Dissipation term b = kappa * M (inverse-time rate). -/
def dissipationRate (kappa mitigationValue : ℝ) : ℝ :=
  kappa * mitigationValue

/-- q = a + b; unchanged across intervals in the cadence theorem. -/
def totalRate (beta kappa residual mitigationValue : ℝ) : ℝ :=
  accumulationRate beta residual + dissipationRate kappa mitigationValue

/-- Equilibrium a / q. Used by the exact transition only for q ≠ 0. -/
noncomputable def stockEquilibrium
    (beta kappa residual mitigationValue : ℝ) : ℝ :=
  accumulationRate beta residual /
    totalRate beta kappa residual mitigationValue

/-- Positive exponential factor exp(-q * dt). -/
noncomputable def decayFactor (q dt : ℝ) : ℝ :=
  Real.exp ((-q) * dt)

/-- Exact constant-input interval update S* + (S-S*)exp(-q dt). -/
noncomputable def intervalStep (equilibrium q dt stock : ℝ) : ℝ :=
  equilibrium + (stock - equilibrium) * decayFactor q dt

/-- Total stock-flow transition, including the manuscript's q=0 identity. -/
noncomputable def stockTransition
    (beta kappa residual mitigationValue dt stock : ℝ) : ℝ :=
  if totalRate beta kappa residual mitigationValue = 0 then stock
  else intervalStep (stockEquilibrium beta kappa residual mitigationValue)
    (totalRate beta kappa residual mitigationValue) dt stock

theorem totalRate_nonneg {beta kappa residual mitigationValue : ℝ}
    (hbeta : 0 ≤ beta) (hkappa : 0 ≤ kappa)
    (hr : Bounded residual) (hm : Bounded mitigationValue) :
    0 ≤ totalRate beta kappa residual mitigationValue := by
  unfold totalRate accumulationRate dissipationRate
  exact add_nonneg (mul_nonneg hbeta hr.1) (mul_nonneg hkappa hm.1)

/-- If q=0 with both physical rates nonnegative, both contributions vanish. -/
theorem zero_totalRate_zero_terms {beta kappa residual mitigationValue : ℝ}
    (hbeta : 0 ≤ beta) (hkappa : 0 ≤ kappa)
    (hr : Bounded residual) (hm : Bounded mitigationValue)
    (hz : totalRate beta kappa residual mitigationValue = 0) :
    accumulationRate beta residual = 0 ∧
      dissipationRate kappa mitigationValue = 0 := by
  have ha : 0 ≤ accumulationRate beta residual :=
    mul_nonneg hbeta hr.1
  have hb : 0 ≤ dissipationRate kappa mitigationValue :=
    mul_nonneg hkappa hm.1
  unfold totalRate at hz
  constructor <;> linarith

/-- With q>0, the unique equilibrium is in [0,1]. -/
theorem stockEquilibrium_bounded {beta kappa residual mitigationValue : ℝ}
    (hbeta : 0 ≤ beta) (hkappa : 0 ≤ kappa)
    (hr : Bounded residual) (hm : Bounded mitigationValue)
    (hq : 0 < totalRate beta kappa residual mitigationValue) :
    Bounded (stockEquilibrium beta kappa residual mitigationValue) := by
  have ha : 0 ≤ accumulationRate beta residual :=
    mul_nonneg hbeta hr.1
  have hb : 0 ≤ dissipationRate kappa mitigationValue :=
    mul_nonneg hkappa hm.1
  have hle : accumulationRate beta residual ≤
      totalRate beta kappa residual mitigationValue := by
    unfold totalRate
    linarith
  unfold stockEquilibrium
  constructor
  · exact div_nonneg ha (le_of_lt hq)
  · exact (div_le_iff₀ hq).2 (by simpa using hle)

/-- Exponential decay lies in (0,1] for q≥0 and duration≥0. -/
theorem decayFactor_bounded {q dt : ℝ}
    (hq : 0 ≤ q) (hdt : 0 ≤ dt) :
    Bounded (decayFactor q dt) := by
  have hneg : (-q) * dt ≤ 0 := by
    nlinarith [mul_nonneg hq hdt]
  constructor
  · exact le_of_lt (Real.exp_pos _)
  · unfold decayFactor
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.mpr hneg

/-- The interval solution is a convex combination of old stock and S*. -/
theorem intervalStep_bounded {equilibrium q dt stock : ℝ}
    (heq : Bounded equilibrium) (hq : 0 ≤ q) (hdt : 0 ≤ dt)
    (hs : Bounded stock) :
    Bounded (intervalStep equilibrium q dt stock) := by
  have hf := decayFactor_bounded hq hdt
  have hf0 : 0 ≤ decayFactor q dt := hf.1
  have hf1 : decayFactor q dt ≤ 1 := hf.2
  have hlow1 : 0 ≤ (1 - decayFactor q dt) * equilibrium :=
    mul_nonneg (by linarith) heq.1
  have hlow2 : 0 ≤ decayFactor q dt * stock :=
    mul_nonneg hf0 hs.1
  have hupper1 : 0 ≤ (1 - decayFactor q dt) * (1 - equilibrium) :=
    mul_nonneg (by linarith) (by linarith [heq.2])
  have hupper2 : 0 ≤ decayFactor q dt * (1 - stock) :=
    mul_nonneg hf0 (by linarith [hs.2])
  have hconvex : intervalStep equilibrium q dt stock =
      (1 - decayFactor q dt) * equilibrium +
        decayFactor q dt * stock := by
    unfold intervalStep
    ring
  rw [hconvex]
  constructor
  · nlinarith
  · nlinarith

theorem stockTransition_zero_rate
    (beta kappa residual mitigationValue dt stock : ℝ)
    (hz : totalRate beta kappa residual mitigationValue = 0) :
    stockTransition beta kappa residual mitigationValue dt stock = stock := by
  simp [stockTransition, hz]

/-- Invariance of the closed [0,1] stock interval under a valid update. -/
theorem stockTransition_bounded {beta kappa residual mitigationValue dt stock : ℝ}
    (hbeta : 0 ≤ beta) (hkappa : 0 ≤ kappa)
    (hr : Bounded residual) (hm : Bounded mitigationValue)
    (hdt : 0 ≤ dt) (hs : Bounded stock) :
    Bounded (stockTransition beta kappa residual mitigationValue dt stock) := by
  by_cases hz : totalRate beta kappa residual mitigationValue = 0
  · simpa [stockTransition, hz] using hs
  · have hq : 0 < totalRate beta kappa residual mitigationValue :=
      lt_of_le_of_ne (totalRate_nonneg hbeta hkappa hr hm) (Ne.symm hz)
    simpa [stockTransition, hz] using
      (intervalStep_bounded
        (stockEquilibrium_bounded hbeta hkappa hr hm hq)
        (le_of_lt hq) hdt hs)

/-- Equilibrium is a fixed point of the constant-input exact transition. -/
theorem intervalStep_equilibrium (equilibrium q dt : ℝ) :
    intervalStep equilibrium q dt equilibrium = equilibrium := by
  simp [intervalStep]

theorem stockTransition_equilibrium
    (beta kappa residual mitigationValue dt : ℝ) :
    stockTransition beta kappa residual mitigationValue dt
      (stockEquilibrium beta kappa residual mitigationValue) =
      stockEquilibrium beta kappa residual mitigationValue := by
  by_cases hz : totalRate beta kappa residual mitigationValue = 0
  · simp [stockTransition, hz]
  · simp [stockTransition, hz, intervalStep_equilibrium]

/-- Absolute displacement from equilibrium cannot grow for nonnegative rates. -/
theorem intervalStep_contraction {equilibrium q dt stock : ℝ}
    (hq : 0 ≤ q) (hdt : 0 ≤ dt) :
    |intervalStep equilibrium q dt stock - equilibrium| ≤
      |stock - equilibrium| := by
  have hf := decayFactor_bounded hq hdt
  have hdiff : intervalStep equilibrium q dt stock - equilibrium =
      (stock - equilibrium) * decayFactor q dt := by
    unfold intervalStep
    ring
  rw [hdiff, abs_mul, abs_of_nonneg hf.1]
  calc
    |stock - equilibrium| * decayFactor q dt ≤
        |stock - equilibrium| * 1 :=
      mul_le_mul_of_nonneg_left hf.2 (abs_nonneg _)
    _ = |stock - equilibrium| := mul_one _

/-- When stock is above equilibrium, longer time cannot increase stock. -/
theorem intervalStep_decreases_above {equilibrium q t₁ t₂ stock : ℝ}
    (hq : 0 ≤ q) (ht : t₁ ≤ t₂) (hs : equilibrium ≤ stock) :
    intervalStep equilibrium q t₂ stock ≤
      intervalStep equilibrium q t₁ stock := by
  have hexp : decayFactor q t₂ ≤ decayFactor q t₁ := by
    unfold decayFactor
    apply Real.exp_le_exp.mpr
    nlinarith [mul_nonneg hq (sub_nonneg.mpr ht)]
  have hm : (stock - equilibrium) * decayFactor q t₂ ≤
      (stock - equilibrium) * decayFactor q t₁ :=
    mul_le_mul_of_nonneg_left hexp (sub_nonneg.mpr hs)
  unfold intervalStep
  exact add_le_add_left hm equilibrium

/-- When stock is below equilibrium, longer time cannot decrease stock. -/
theorem intervalStep_increases_below {equilibrium q t₁ t₂ stock : ℝ}
    (hq : 0 ≤ q) (ht : t₁ ≤ t₂) (hs : stock ≤ equilibrium) :
    intervalStep equilibrium q t₁ stock ≤
      intervalStep equilibrium q t₂ stock := by
  have hexp : decayFactor q t₂ ≤ decayFactor q t₁ := by
    unfold decayFactor
    apply Real.exp_le_exp.mpr
    nlinarith [mul_nonneg hq (sub_nonneg.mpr ht)]
  have hm : (stock - equilibrium) * decayFactor q t₁ ≤
      (stock - equilibrium) * decayFactor q t₂ :=
    mul_le_mul_of_nonpos_left hexp (sub_nonpos.mpr hs)
  unfold intervalStep
  exact add_le_add_left hm equilibrium

/-- Under q>0 the exact interval update converges toward its equilibrium. -/
theorem intervalStep_tendsto_equilibrium {equilibrium q stock : ℝ}
    (hq : 0 < q) :
    Filter.Tendsto (fun t : ℝ => intervalStep equilibrium q t stock)
      Filter.atTop (nhds equilibrium) := by
  have hbot : Filter.Tendsto (fun t : ℝ => (-q) * t)
      Filter.atTop Filter.atBot :=
    Filter.tendsto_id.const_mul_atTop_of_neg (by linarith : -q < 0)
  have hdec : Filter.Tendsto (fun t : ℝ => decayFactor q t)
      Filter.atTop (nhds (0 : ℝ)) := by
    simpa [decayFactor] using Real.tendsto_exp_atBot.comp hbot
  have hscale : Filter.Tendsto
      (fun t : ℝ => (stock - equilibrium) * decayFactor q t)
      Filter.atTop (nhds (0 : ℝ)) := by
    have hmul : Filter.Tendsto
        (fun t : ℝ => (stock - equilibrium) * decayFactor q t)
        Filter.atTop (nhds ((stock - equilibrium) * (0 : ℝ))) :=
      Filter.tendsto_const_nhds.mul hdec
    simpa using hmul
  have hadd : Filter.Tendsto
      (fun t : ℝ => equilibrium + (stock - equilibrium) * decayFactor q t)
      Filter.atTop (nhds (equilibrium + 0)) :=
    Filter.tendsto_const_nhds.add hscale
  simpa [intervalStep] using hadd

theorem stockTransition_tendsto_equilibrium
    {beta kappa residual mitigationValue stock : ℝ}
    (hq : 0 < totalRate beta kappa residual mitigationValue) :
    Filter.Tendsto
      (fun t : ℝ => stockTransition beta kappa residual mitigationValue t stock)
      Filter.atTop (nhds (stockEquilibrium beta kappa residual mitigationValue)) := by
  have hz : totalRate beta kappa residual mitigationValue ≠ 0 := ne_of_gt hq
  simpa [stockTransition, hz] using
    (intervalStep_tendsto_equilibrium
      (equilibrium := stockEquilibrium beta kappa residual mitigationValue)
      (q := totalRate beta kappa residual mitigationValue)
      (stock := stock) hq)

/-- Composition for fixed q and S*: exact cadence-invariance equality. -/
theorem intervalStep_semigroup (equilibrium q dt₁ dt₂ stock : ℝ) :
    intervalStep equilibrium q dt₂ (intervalStep equilibrium q dt₁ stock) =
      intervalStep equilibrium q (dt₁ + dt₂) stock := by
  have hexp : decayFactor q dt₁ * decayFactor q dt₂ =
      decayFactor q (dt₁ + dt₂) := by
    unfold decayFactor
    rw [← Real.exp_add]
    congr 1
    ring
  unfold intervalStep
  calc
    equilibrium +
        (equilibrium + (stock - equilibrium) * decayFactor q dt₁ -
          equilibrium) * decayFactor q dt₂ =
        equilibrium + (stock - equilibrium) *
          (decayFactor q dt₁ * decayFactor q dt₂) := by ring
    _ = equilibrium + (stock - equilibrium) *
        decayFactor q (dt₁ + dt₂) := by rw [hexp]

/-- Exact semigroup for identical interval inputs (not for time-varying inputs). -/
theorem stockTransition_semigroup
    (beta kappa residual mitigationValue dt₁ dt₂ stock : ℝ) :
    stockTransition beta kappa residual mitigationValue dt₂
      (stockTransition beta kappa residual mitigationValue dt₁ stock) =
      stockTransition beta kappa residual mitigationValue (dt₁ + dt₂) stock := by
  by_cases hz : totalRate beta kappa residual mitigationValue = 0
  · simp [stockTransition, hz]
  · simpa [stockTransition, hz] using
      (intervalStep_semigroup
        (stockEquilibrium beta kappa residual mitigationValue)
        (totalRate beta kappa residual mitigationValue) dt₁ dt₂ stock)

/-- P6 is end-to-end bounded once Phase C establishes stock preservation. -/
theorem envelope_after_transition_bounded
    {residual stock beta kappa mitigationValue dt : ℝ}
    (hbeta : 0 ≤ beta) (hkappa : 0 ≤ kappa)
    (hr : Bounded residual) (hm : Bounded mitigationValue)
    (hdt : 0 ≤ dt) (hs : Bounded stock) :
    Bounded
      (envelope residual
        (stockTransition beta kappa residual mitigationValue dt stock)) := by
  exact envelope_bounded hr
    (stockTransition_bounded hbeta hkappa hr hm hdt hs)

end CRPI
