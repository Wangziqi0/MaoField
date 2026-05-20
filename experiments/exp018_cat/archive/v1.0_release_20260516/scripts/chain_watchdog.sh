#!/usr/bin/env bash
# chain_watchdog.sh — kill hung run_arm_b_alpha_scan.py (deadlock detect)
#
# 5/10 seed=4 attempt 1 deadlock 10h waste teach lesson:
# robust chain 仅检 exit code, 不检 hang. 加 watchdog 监 log mtime.
#
# Logic:
#   - Find latest run_arm_b_alpha_scan process
#   - Find its log file (most recent phase1_robust_alpha*_attempt*_*.log)
#   - If log mtime stale > STALE_SEC (5 min), kill -9 the python
#   - Chain detects rc != 0, auto-retry attempt N+1
#
# Usage: nohup bash scripts/chain_watchdog.sh > logs/watchdog_$(date +%Y%m%d_%H%M%S).log 2>&1 &

set -uo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/home/amd/HEZIMENG/MaoField/experiments/exp018_cat}"
cd "$PROJECT_ROOT"

STALE_SEC=300   # 5 min — train at 6 it/s, generate at 1.3 s/it, normal max pause ~30s between gens
CHECK_INTERVAL=60   # check every 1 min
WATCHDOG_LOG="logs/watchdog_state.jsonl"

log_event() {
    local evt="$1"; shift
    local kv="$@"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"ts\":\"$now\",\"event\":\"$evt\",$kv}" >> "$WATCHDOG_LOG"
    echo "[$(date '+%F %T')] $evt $kv"
}

log_event "watchdog_start" "stale_sec=$STALE_SEC interval=$CHECK_INTERVAL"

while true; do
    PIDS=$(pgrep -f "run_arm_b_alpha_scan" 2>/dev/null)
    if [ -z "$PIDS" ]; then
        sleep $CHECK_INTERVAL
        continue
    fi

    for PID in $PIDS; do
        # Find latest phase1_robust log file (matched by mtime, most recent)
        LATEST_LOG=$(ls -t logs/phase1_robust_alpha*_seed*_attempt*_*.log 2>/dev/null | head -1)
        if [ -z "$LATEST_LOG" ] || [ ! -f "$LATEST_LOG" ]; then
            continue
        fi

        LOG_MTIME=$(stat -c %Y "$LATEST_LOG")
        NOW=$(date +%s)
        AGE=$((NOW - LOG_MTIME))

        if [ $AGE -gt $STALE_SEC ]; then
            # Verify process still running before kill
            if ! kill -0 $PID 2>/dev/null; then
                continue   # process already gone
            fi
            log_event "watchdog_kill" "pid=$PID log=\"$LATEST_LOG\" age_sec=$AGE stale_threshold=$STALE_SEC"
            kill -9 $PID
            sleep 10
            log_event "watchdog_killed_confirm" "pid=$PID"
        fi
    done

    sleep $CHECK_INTERVAL
done
