import CRPI.Basic

namespace CRPI

/-- Reporting-only aggregate CS of consequence domains. -/
def consequenceSeverity {ι : Type*} (s : Finset ι)
    (v d : ι → ℝ) : ℝ :=
  weightedSum s v d

theorem consequenceSeverity_bounded {ι : Type*} (s : Finset ι)
    (v d : ι → ℝ)
    (hv : ∀ i ∈ s, 0 ≤ v i)
    (hsum : (∑ i ∈ s, v i) = 1)
    (hd : ∀ i ∈ s, Bounded (d i)) :
    Bounded (consequenceSeverity s v d) := by
  exact weightedSum_bounded s v d hv hsum hd

/-- Resilience-adjusted consequence from the manuscript, not scalar RRAS. -/
def effectiveConsequence {ι : Type*} (s : Finset ι)
    (v d rho r : ι → ℝ) : ℝ :=
  weightedSum s v (fun j => d j * (1 - rho j * r j))

theorem effectiveConsequence_bounded {ι : Type*} (s : Finset ι)
    (v d rho r : ι → ℝ)
    (hv : ∀ j ∈ s, 0 ≤ v j)
    (hsum : (∑ j ∈ s, v j) = 1)
    (hd : ∀ j ∈ s, Bounded (d j))
    (hrho : ∀ j ∈ s, Bounded (rho j))
    (hr : ∀ j ∈ s, Bounded (r j)) :
    Bounded (effectiveConsequence s v d rho r) := by
  exact weightedSum_bounded s v
    (fun j => d j * (1 - rho j * r j)) hv hsum (by
      intro j hj
      exact bounded_mul (hd j hj)
        (bounded_complement (bounded_mul (hrho j hj) (hr j hj))))

/-- Hazard H = TE * D_eff. -/
def hazard (te dEff : ℝ) : ℝ := te * dEff

theorem hazard_bounded {te dEff : ℝ}
    (hte : Bounded te) (hdEff : Bounded dEff) :
    Bounded (hazard te dEff) := by
  exact bounded_mul hte hdEff

end CRPI
