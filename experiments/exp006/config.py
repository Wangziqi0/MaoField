"""MaoField Exp006: Multi-Component Field Configuration"""

import os

# Grid
GRID_SIZE = 32

# Allen-Cahn parameters
D = 0.1       # diffusion coefficient (same for all components)
DT = 0.1      # time step
DX = 1.0      # spatial step

# Evolution steps
INIT_STEPS = 1000
INTERACT_STEPS = 300
RELAX_STEPS = 100
FUSION_STEPS = 2000

# Adjoint iteration
MAX_ROUNDS = 5
CONVERGENCE_TOL = 0.01
TOP_K = 10

# Corpus
CORPUS_SIZE = 200
BLIND_SIZE = 50

# Paths
EXP_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(EXP_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Database
DB_PATH = "/home/amd/HEZIMENG/legal-assistant/knowledge_base/legal_data.db"
