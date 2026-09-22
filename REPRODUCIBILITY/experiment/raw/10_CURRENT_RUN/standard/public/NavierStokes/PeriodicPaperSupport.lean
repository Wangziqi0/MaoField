import NavierStokes.R3.ProblemStatement

noncomputable section
namespace NavierStokes.PeriodicPaper
open ProblemStatement Set
open scoped Topology ContDiff

/-- The interior of the centered fundamental unit cube. -/
def fundamentalInterior : Set Space := {x | ∀ i : Fin 3, |x i| < 1 / 2}

/-- The closed centered fundamental unit cube. -/
def fundamentalCube : Set Space := {x | ∀ i : Fin 3, |x i| ≤ 1 / 2}


end NavierStokes.PeriodicPaper
