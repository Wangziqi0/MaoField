"""MaoField Exp005: Configuration"""

import os

# Grid
GRID_SIZE = 32

# Allen-Cahn parameters
D = 0.1       # diffusion coefficient (verified in exp004)
DT = 0.1      # time step
DX = 1.0      # spatial step

# Evolution steps
INIT_STEPS = 1000       # initial evolution to form basic structure
INTERACT_STEPS = 300    # interaction with each corpus text
RELAX_STEPS = 100       # relaxation after removing corpus source
FUSION_STEPS = 2000     # fusion evolution for matching

# Adjoint iteration
MAX_ROUNDS = 5          # max adjoint iteration rounds
CONVERGENCE_TOL = 0.01  # convergence threshold (relative change in residual norm)
TOP_K = 10              # default number of demand-driven practice targets

# Corpus
CORPUS_SIZE = 200       # practice pool size
BLIND_SIZE = 50         # for condition B (blind practice)

# Paths
EXP_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(EXP_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Database
DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
