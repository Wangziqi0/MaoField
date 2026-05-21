#!/usr/bin/env bash
# watchdog.sh — D-PPL bridge main run 之 ROCm hang 监护 wrapper
#
# 5/11 verdict B (alpha10 hang case 之 ROCm bug 不是 framework boundary) 之 应对。
# 借鉴 archive/v1.0_release_20260516/scripts/chain_watchdog.sh 之 pattern。
#
# Logic:
#   - Launch wrapped python command in background, PID 写 .pid
#   - Loop: 每 CHECK_INTERVAL 检查 log file 之 mtime
#   - 若 log mtime stale > STALE_SEC → kill -9 python, log "hang_kill" event
#   - 短 sleep + relaunch (python 之 main script 内置 resume-from-last-checkpoint logic)
#   - 3 fail in a row (same tuple, per python 之 jsonl entry detection) → 写 escalate flag, exit
#
# Usage:
#   bash watchdog.sh python3 launch_dppl_bridge.py --mode main ...

set -uo pipefail

# -----------------------------------------------------------------------------
# Config (env override 之 不修)
# -----------------------------------------------------------------------------
STALE_SEC="${STALE_SEC:-300}"          # 5 min — per gen-per-path 之 ~30 sec 之 normal, 5 min stale = hang
CHECK_INTERVAL="${CHECK_INTERVAL:-60}"  # 1 min cadence
MAX_RETRIES="${MAX_RETRIES:-10}"        # 总 retry 上限
MAX_SAME_TUPLE_RETRIES="${MAX_SAME_TUPLE_RETRIES:-3}"  # same tuple 之 3 fail → escalate
RESUME_SLEEP_SEC="${RESUME_SLEEP_SEC:-60}"  # kill 之 后 等待 GPU 恢复

WATCHDOG_DIR="${WATCHDOG_DIR:-/tmp/dppl_bridge_verify/output/main}"
mkdir -p "$WATCHDOG_DIR"
WATCHDOG_LOG="$WATCHDOG_DIR/watchdog.audit.jsonl"
WATCHDOG_PID_FILE="$WATCHDOG_DIR/main_D21.pid"
ESCALATE_FLAG="$WATCHDOG_DIR/../escalate_d21.flag"

# -----------------------------------------------------------------------------
# 内部 helpers
# -----------------------------------------------------------------------------
log_event() {
    local evt="$1"; shift
    local kv="$*"
    local now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "{\"ts\":\"$now\",\"event\":\"$evt\",$kv}" >> "$WATCHDOG_LOG"
    echo "[$(date '+%F %T')] watchdog: $evt $kv" >&2
}

write_escalate_flag() {
    local reason="$1"
    local current_tuple="$2"
    cat > "$ESCALATE_FLAG" << EOF
{
  "ts": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "error_type": "watchdog_escalate",
  "error_detail": "$reason",
  "current_tuple": "$current_tuple",
  "n_total_kills": $TOTAL_KILLS,
  "n_total_retries": $TOTAL_RETRIES,
  "next_action_suggestion": "7B13 sub-agent 检查 watchdog.audit.jsonl + main_D21.jsonl + main_D21.log, 决定 是否 escalate 路径 A OR retract D-PPL 桥 verify"
}
EOF
    log_event "escalate_flag_written" "reason=\"$reason\" file=\"$ESCALATE_FLAG\""
}

get_last_tuple() {
    # Read last tuple_done OR tuple_error entry from main_D21.jsonl
    # Return e.g., "alpha=10.0 seed=2 gen=3 path=B" or "none"
    local jsonl="$WATCHDOG_DIR/main_D21.jsonl"
    if [ ! -f "$jsonl" ]; then
        echo "none"
        return
    fi
    local last_entry=$(grep -E '"event":"tuple_(done|error|skipped)"' "$jsonl" | tail -1)
    if [ -z "$last_entry" ]; then
        echo "none"
        return
    fi
    # quick parse (jq 不一定装, sed fallback)
    if command -v jq > /dev/null 2>&1; then
        echo "$last_entry" | jq -r '"alpha=\(.alpha) seed=\(.seed) gen=\(.gen) path=\(.path)"' 2>/dev/null || echo "parse_fail"
    else
        echo "$last_entry" | sed -E 's/.*"alpha":([0-9.]+).*"seed":([0-9]+).*"gen":([0-9]+).*"path":"([BC])".*/alpha=\1 seed=\2 gen=\3 path=\4/' || echo "parse_fail"
    fi
}

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
if [ $# -lt 1 ]; then
    echo "Usage: bash watchdog.sh <python_command_and_args>"
    echo "e.g., bash watchdog.sh python3 launch_dppl_bridge.py --mode main ..."
    exit 2
fi

PYTHON_CMD=("$@")
LOG_FILE="$WATCHDOG_DIR/main_D21.log"

log_event "watchdog_start" "stale_sec=$STALE_SEC interval=$CHECK_INTERVAL max_retries=$MAX_RETRIES cmd=\"$(echo "${PYTHON_CMD[*]}" | head -c 200)\""

TOTAL_KILLS=0
TOTAL_RETRIES=0
LAST_FAIL_TUPLE=""
SAME_TUPLE_FAIL_COUNT=0

while [ $TOTAL_RETRIES -lt $MAX_RETRIES ]; do
    # Launch python in background
    log_event "launch_python" "retry=$TOTAL_RETRIES"

    "${PYTHON_CMD[@]}" >> "$LOG_FILE" 2>&1 &
    PYTHON_PID=$!
    echo $PYTHON_PID > "$WATCHDOG_PID_FILE"
    log_event "python_launched" "pid=$PYTHON_PID"

    # Monitor loop
    LAST_LOG_MTIME=$(stat -c %Y "$LOG_FILE" 2>/dev/null || echo 0)
    while kill -0 $PYTHON_PID 2>/dev/null; do
        sleep $CHECK_INTERVAL

        # Check log mtime
        CUR_MTIME=$(stat -c %Y "$LOG_FILE" 2>/dev/null || echo 0)
        NOW=$(date +%s)
        AGE=$((NOW - CUR_MTIME))

        if [ $AGE -gt $STALE_SEC ]; then
            # Hang detected — kill -9
            CURRENT_TUPLE=$(get_last_tuple)
            log_event "hang_detected" "pid=$PYTHON_PID log_age=$AGE stale_sec=$STALE_SEC current_tuple=\"$CURRENT_TUPLE\""

            kill -9 $PYTHON_PID 2>/dev/null
            wait $PYTHON_PID 2>/dev/null
            TOTAL_KILLS=$((TOTAL_KILLS + 1))

            log_event "python_killed" "pid=$PYTHON_PID total_kills=$TOTAL_KILLS current_tuple=\"$CURRENT_TUPLE\""

            # same tuple 之 3 fail check
            if [ "$CURRENT_TUPLE" = "$LAST_FAIL_TUPLE" ] && [ "$CURRENT_TUPLE" != "none" ]; then
                SAME_TUPLE_FAIL_COUNT=$((SAME_TUPLE_FAIL_COUNT + 1))
            else
                LAST_FAIL_TUPLE="$CURRENT_TUPLE"
                SAME_TUPLE_FAIL_COUNT=1
            fi

            if [ $SAME_TUPLE_FAIL_COUNT -ge $MAX_SAME_TUPLE_RETRIES ]; then
                log_event "escalate_same_tuple_3_fail" "current_tuple=\"$CURRENT_TUPLE\" count=$SAME_TUPLE_FAIL_COUNT"
                write_escalate_flag "same tuple 3 hang fails: $CURRENT_TUPLE" "$CURRENT_TUPLE"
                # 试图 rsync push escalate flag 7B13 (若 rsync target 在 env 内)
                if [ -n "${RSYNC_TARGET:-}" ]; then
                    rsync -avz "$ESCALATE_FLAG" "$RSYNC_TARGET" 2>/dev/null || true
                fi
                exit 3
            fi

            # GPU 恢复 sleep
            log_event "gpu_recovery_sleep" "sec=$RESUME_SLEEP_SEC"
            sleep $RESUME_SLEEP_SEC

            # break inner loop → relaunch
            break
        fi

        LAST_LOG_MTIME=$CUR_MTIME
    done

    # Python exited (natural OR killed)
    if [ -e /proc/$PYTHON_PID ]; then
        wait $PYTHON_PID 2>/dev/null
    fi
    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        log_event "python_done_clean" "exit_code=$EXIT_CODE"
        log_event "watchdog_end" "total_kills=$TOTAL_KILLS total_retries=$TOTAL_RETRIES status=clean"
        exit 0
    elif [ $EXIT_CODE -ne 137 ] && [ $EXIT_CODE -ne 9 ]; then
        # Non-kill, non-clean exit — Python error
        log_event "python_exit_nonzero" "exit_code=$EXIT_CODE"
        # 不重启 (Python script bug, not GPU hang)
        log_event "watchdog_end" "total_kills=$TOTAL_KILLS total_retries=$TOTAL_RETRIES status=python_error"
        write_escalate_flag "python script error exit $EXIT_CODE (non-hang)" "$(get_last_tuple)"
        exit 4
    fi

    TOTAL_RETRIES=$((TOTAL_RETRIES + 1))
    log_event "retry_will_relaunch" "total_retries=$TOTAL_RETRIES max=$MAX_RETRIES"
done

# Hit MAX_RETRIES
log_event "escalate_max_retries" "total_retries=$TOTAL_RETRIES max=$MAX_RETRIES"
write_escalate_flag "max watchdog retries reached ($MAX_RETRIES)" "$(get_last_tuple)"
exit 5
