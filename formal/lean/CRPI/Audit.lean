import CRPI

/-!
Run with: lake env lean CRPI/Audit.lean

Printing assumptions is part of the protocol's trust audit. The resulting
tool output must be attached to an exact source revision before any theorem
can be marked machine-checked.
-/

#print axioms CRPI.bounded_complement
#print axioms CRPI.bounded_mul
#print axioms CRPI.weightedSum_bounded
#print axioms CRPI.consequenceSeverity_bounded
#print axioms CRPI.effectiveConsequence_bounded
#print axioms CRPI.hazard_bounded
#print axioms CRPI.mitigation_bounded
#print axioms CRPI.instantaneousResidual_bounded
#print axioms CRPI.envelope_bounded
#print axioms CRPI.envelope_mono_residual
#print axioms CRPI.envelope_mono_stock
