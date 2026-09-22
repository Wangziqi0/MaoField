import NavierStokes.R3.ProblemStatement
import NavierStokes.PeriodicPaperStatement

/- Trusted target statements only. This file contains no witness or proof.
   In the researcher reference environment, these definitions are compared
   with the original full roots. In the actor environment, all imported
   target definitions must be preserved without the completed proof bodies. -/

namespace GoalSpec

def main_goal : Prop := NavierStokesR3.ProblemStatement.breakdownStatement

def periodic_goal : Prop := NavierStokes.PeriodicPaper.breakdownStatement

end GoalSpec
