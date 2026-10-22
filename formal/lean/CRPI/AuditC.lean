import CRPI

/-!
Run from formal/lean:
  lake env lean CRPI/AuditC.lean

All proof status remains OPEN until source compiles and this dependency report
is captured with the pinned project toolchain on an exact commit.
-/

#print axioms CRPI.totalRate_nonneg
#print axioms CRPI.zero_totalRate_zero_terms
#print axioms CRPI.stockEquilibrium_bounded
#print axioms CRPI.decayFactor_bounded
#print axioms CRPI.intervalStep_bounded
#print axioms CRPI.stockTransition_zero_rate
#print axioms CRPI.stockTransition_bounded
#print axioms CRPI.intervalStep_equilibrium
#print axioms CRPI.stockTransition_equilibrium
#print axioms CRPI.intervalStep_contraction
#print axioms CRPI.intervalStep_decreases_above
#print axioms CRPI.intervalStep_increases_below
#print axioms CRPI.intervalStep_tendsto_equilibrium
#print axioms CRPI.stockTransition_tendsto_equilibrium
#print axioms CRPI.intervalStep_semigroup
#print axioms CRPI.stockTransition_semigroup
#print axioms CRPI.envelope_after_transition_bounded
