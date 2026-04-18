"""MaoField Exp004: Configuration"""

import os

# Grid
GRID_SIZE = 32
DX = 1.0

# Gray-Scott defaults
D_U = 0.16
D_V = 0.08
F_BASE = 0.04
K_BASE = 0.06

# Time stepping
DT = 0.5
MAX_STEPS = 10000
SNAPSHOT_INTERVAL = 100

# Token injection
INJECT_AMPLITUDE = 0.1
INJECT_SIGMA = 1.5  # Gaussian width
INJECT_RADIUS = 3   # neighborhood radius

# F,k perturbation from token injection
DELTA_F = 0.005
DELTA_K = 0.003

# Paths
EXP_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(EXP_DIR, "results")
SNAPSHOTS_DIR = os.path.join(RESULTS_DIR, "snapshots")
ENERGY_DIR = os.path.join(RESULTS_DIR, "energy")
ANALYSIS_DIR = os.path.join(RESULTS_DIR, "analysis")
