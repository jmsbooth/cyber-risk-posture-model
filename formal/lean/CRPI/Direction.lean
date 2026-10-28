import CRPI.Aggregation

/-!
# CRPI Proposition 5: instantaneous directional sensitivity

All results hold with the other model variables fixed. They are monotonic
order statements, not empirical parameter-calibration or differentiability claims.
-/

namespace CRPI

/-- Raising domain consequence cannot lower effective consequence when all
other consequence variables are fixed. -/
theorem effectiveConsequence_mono_domain {ι : Type*}
    (s : Finset ι) (v d₁ d₂ rho r : ι → ℝ)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, Bounded (r j))
    (hd : ∀ j ∈ s, d₁ j ≤ d₂ j) :
    effectiveConsequence s v d₁ rho r ≤
      effectiveConsequence s v d₂ rho r := by
  unfold effectiveConsequence weightedSum
  apply Finset.sum_le_sum
  intro j hj
  have hfactor : 0 ≤ 1 - rho j * r j :=
    (bounded_complement (bounded_mul (hrho j hj) (hr j hj))).1
  have hcomponent :
      d₁ j * (1 - rho j * r j) ≤ d₂ j * (1 - rho j * r j) :=
    mul_le_mul_of_nonneg_right (hd j hj) hfactor
  exact mul_le_mul_of_nonneg_left hcomponent (hv j hj)

/-- Greater applicable resilience cannot increase effective consequence. -/
theorem effectiveConsequence_antitone_resilience {ι : Type*}
    (s : Finset ι) (v d rho r₁ r₂ : ι → ℝ)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hd : ∀ j ∈ s, Bounded (d j))
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, r₁ j ≤ r₂ j) :
    effectiveConsequence s v d rho r₂ ≤
      effectiveConsequence s v d rho r₁ := by
  unfold effectiveConsequence weightedSum
  apply Finset.sum_le_sum
  intro j hj
  have hproj : rho j * r₁ j ≤ rho j * r₂ j :=
    mul_le_mul_of_nonneg_left (hr j hj) (hrho j hj).1
  have hfactor : 1 - rho j * r₂ j ≤ 1 - rho j * r₁ j := by
    linarith
  have hcomponent :
      d j * (1 - rho j * r₂ j) ≤ d j * (1 - rho j * r₁ j) :=
    mul_le_mul_of_nonneg_left hfactor (hd j hj).1
  exact mul_le_mul_of_nonneg_left hcomponent (hv j hj)

/-- Hazard is increasing in threat exposure when effective consequence is nonnegative. -/
theorem hazard_mono_threat {te₁ te₂ dEff : ℝ}
    (hte : te₁ ≤ te₂) (hdEff : 0 ≤ dEff) :
    hazard te₁ dEff ≤ hazard te₂ dEff := by
  unfold hazard
  exact mul_le_mul_of_nonneg_right hte hdEff

/-- Hazard is increasing in effective consequence when TE is nonnegative. -/
theorem hazard_mono_consequence {te d₁ d₂ : ℝ}
    (hd : d₁ ≤ d₂) (hte : 0 ≤ te) :
    hazard te d₁ ≤ hazard te d₂ := by
  unfold hazard
  exact mul_le_mul_of_nonneg_left hd hte

theorem mitigation_mono_soe {u₁ u₂ cm m0 : ℝ}
    (hu : u₁ ≤ u₂) (hcm : Bounded cm) (hm0 : Bounded m0) :
    mitigation u₁ cm m0 ≤ mitigation u₂ cm m0 := by
  have hb : 0 ≤ m0 + (1 - m0) * cm := by
    have hcoef : 0 ≤ 1 - m0 := by linarith [hm0.2]
    have hterm := mul_nonneg hcoef hcm.1
    linarith [hm0.1]
  unfold mitigation
  exact mul_le_mul_of_nonneg_right hu hb

theorem mitigation_mono_cm {soe cm₁ cm₂ m0 : ℝ}
    (hcm : cm₁ ≤ cm₂) (hsoe : 0 ≤ soe)
    (hm0 : Bounded m0) :
    mitigation soe cm₁ m0 ≤ mitigation soe cm₂ m0 := by
  have hcoef : 0 ≤ 1 - m0 := by linarith [hm0.2]
  have hblend : m0 + (1 - m0) * cm₁ ≤
      m0 + (1 - m0) * cm₂ :=
    add_le_add_left (mul_le_mul_of_nonneg_left hcm hcoef) m0
  unfold mitigation
  exact mul_le_mul_of_nonneg_left hblend hsoe

theorem instantaneousResidual_mono_hazard {h₁ h₂ m : ℝ}
    (hh : h₁ ≤ h₂) (hm : Bounded m) :
    instantaneousResidual h₁ m ≤ instantaneousResidual h₂ m := by
  unfold instantaneousResidual
  exact mul_le_mul_of_nonneg_right hh (by linarith [hm.2])

theorem instantaneousResidual_antitone_mitigation {h m₁ m₂ : ℝ}
    (hm : m₁ ≤ m₂) (hh : 0 ≤ h) :
    instantaneousResidual h m₂ ≤ instantaneousResidual h m₁ := by
  unfold instantaneousResidual
  apply mul_le_mul_of_nonneg_left _ hh
  linarith

/-- Fully composed instantaneous residual, not the scalar RRAS report. -/
def currentResidual {ι : Type*} (s : Finset ι)
    (v d rho r : ι → ℝ) (te soe cm m0 : ℝ) : ℝ :=
  instantaneousResidual
    (hazard te (effectiveConsequence s v d rho r))
    (mitigation soe cm m0)

/-- Proposition 5: increasing TE cannot lower instantaneous residual. -/
theorem currentResidual_mono_threat {ι : Type*} (s : Finset ι)
    (v d rho r : ι → ℝ) (te₁ te₂ soe cm m0 : ℝ)
    (hte : te₁ ≤ te₂)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hsum : (∑ j ∈ s, v j) = 1)
    (hd : ∀ j ∈ s, Bounded (d j))
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, Bounded (r j))
    (hu : Bounded soe) (hcm : Bounded cm) (hm0 : Bounded m0) :
    currentResidual s v d rho r te₁ soe cm m0 ≤
      currentResidual s v d rho r te₂ soe cm m0 := by
  unfold currentResidual
  apply instantaneousResidual_mono_hazard _ (mitigation_bounded hu hcm hm0)
  exact hazard_mono_threat hte
    (effectiveConsequence_bounded s v d rho r hv hsum hd hrho hr).1

/-- Proposition 5: increasing any consequence domain cannot lower residual. -/
theorem currentResidual_mono_domain {ι : Type*} (s : Finset ι)
    (v d₁ d₂ rho r : ι → ℝ) (te soe cm m0 : ℝ)
    (hte : Bounded te)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, Bounded (r j))
    (hd : ∀ j ∈ s, d₁ j ≤ d₂ j)
    (hu : Bounded soe) (hcm : Bounded cm) (hm0 : Bounded m0) :
    currentResidual s v d₁ rho r te soe cm m0 ≤
      currentResidual s v d₂ rho r te soe cm m0 := by
  unfold currentResidual
  apply instantaneousResidual_mono_hazard _ (mitigation_bounded hu hcm hm0)
  exact hazard_mono_consequence
    (effectiveConsequence_mono_domain s v d₁ d₂ rho r hv hrho hr hd) hte.1

/-- Proposition 5: increasing domain-applicable resilience cannot raise residual. -/
theorem currentResidual_antitone_resilience {ι : Type*} (s : Finset ι)
    (v d rho r₁ r₂ : ι → ℝ) (te soe cm m0 : ℝ)
    (hte : Bounded te)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hd : ∀ j ∈ s, Bounded (d j))
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, r₁ j ≤ r₂ j)
    (hu : Bounded soe) (hcm : Bounded cm) (hm0 : Bounded m0) :
    currentResidual s v d rho r₂ te soe cm m0 ≤
      currentResidual s v d rho r₁ te soe cm m0 := by
  unfold currentResidual
  apply instantaneousResidual_mono_hazard _ (mitigation_bounded hu hcm hm0)
  exact hazard_mono_consequence
    (effectiveConsequence_antitone_resilience s v d rho r₁ r₂ hv hd hrho hr)
    hte.1

/-- Proposition 5: operational execution cannot increase residual. -/
theorem currentResidual_antitone_soe {ι : Type*} (s : Finset ι)
    (v d rho r : ι → ℝ) (te u₁ u₂ cm m0 : ℝ)
    (hu : u₁ ≤ u₂)
    (hte : Bounded te)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hsum : (∑ j ∈ s, v j) = 1)
    (hd : ∀ j ∈ s, Bounded (d j))
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, Bounded (r j))
    (hcm : Bounded cm) (hm0 : Bounded m0) :
    currentResidual s v d rho r te u₂ cm m0 ≤
      currentResidual s v d rho r te u₁ cm m0 := by
  unfold currentResidual
  apply instantaneousResidual_antitone_mitigation
    (mitigation_mono_soe hu hcm hm0)
  exact (hazard_bounded hte
    (effectiveConsequence_bounded s v d rho r hv hsum hd hrho hr)).1

/-- Proposition 5: monitoring cannot increase residual with operations fixed. -/
theorem currentResidual_antitone_cm {ι : Type*} (s : Finset ι)
    (v d rho r : ι → ℝ) (te soe cm₁ cm₂ m0 : ℝ)
    (hcm : cm₁ ≤ cm₂)
    (hte : Bounded te)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hsum : (∑ j ∈ s, v j) = 1)
    (hd : ∀ j ∈ s, Bounded (d j))
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, Bounded (r j))
    (hu : Bounded soe) (hm0 : Bounded m0) :
    currentResidual s v d rho r te soe cm₂ m0 ≤
      currentResidual s v d rho r te soe cm₁ m0 := by
  unfold currentResidual
  apply instantaneousResidual_antitone_mitigation
    (mitigation_mono_cm hcm hu.1 hm0)
  exact (hazard_bounded hte
    (effectiveConsequence_bounded s v d rho r hv hsum hd hrho hr)).1

end CRPI
