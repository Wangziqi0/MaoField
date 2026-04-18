#!/bin/bash
# Wait for all Block I background jobs to finish, then run final aggregate
# and write block1_final_report.md for mainline Claude to read.
EXP17=/home/amd/HEZIMENG/MaoField/experiments/exp017_dialectics
cd $EXP17
source /home/amd/HEZIMENG/legal-assistant/.venv/bin/activate

LOG=$EXP17/logs/block1/finalize.log
exec > $LOG 2>&1

echo "=== finalize started $(date) ==="

# Wait for stage1_scorers (python) and MaoField binaries (rust) to finish.
# We poll PIDs of known processes; also catch any new variant_a_solver spawns.
while pgrep -f 'block1_stage1_scorers' > /dev/null \
   || pgrep -x exp015_solver > /dev/null \
   || pgrep -x variant_a_solver > /dev/null \
   || pgrep -f 'block1_run_maofield.sh' > /dev/null; do
  sleep 180
  echo "  [$(date +%H:%M:%S)] still waiting..."
  echo "    stage1: $(pgrep -f block1_stage1_scorers | head -1)"
  echo "    exp015_solver: $(pgrep -x exp015_solver | head -1)"
  echo "    variant_a_solver: $(pgrep -x variant_a_solver | head -1)"
  echo "    runner: $(pgrep -f block1_run_maofield.sh | head -1)"
done

echo "=== all jobs finished $(date) ==="

# Final aggregate
python3 $EXP17/src/block1_aggregate.py

# Write final completion marker with summary + BGE timing
REPORT=$EXP17/results/block1_final_report.md
{
  echo "# Block I complete ($(date))"
  echo ""
  echo "## Files produced"
  echo "- block1_baselines.csv (final, 5x6 = 30 rows)"
  echo "- block1_summary.md (final)"
  echo "- block1_partial_baselines.csv / block1_partial_summary.md (early snapshot, 15 rows)"
  echo ""
  echo "## BGE HTTP stats"
  grep -hE 'bge.*done.*fails' $EXP17/logs/block1/stage1_*.log || true
  echo ""
  echo "## MaoField runtimes"
  ls -la $EXP17/results/block1/*maofield*_out.json
  echo ""
  echo "## block1_baselines.csv"
  cat $EXP17/results/block1_baselines.csv
  echo ""
  echo "## block1_summary.md"
  cat $EXP17/results/block1_summary.md
} > $REPORT 2>&1

echo "=== wrote $REPORT ==="
echo "DONE $(date)"
