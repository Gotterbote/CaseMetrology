#!/usr/bin/env bash
set -u

PROJECT_ROOT="/home/timmy/Projects/CaseMetrology"
CAMERA="/dev/case-metrology-camera"
PYTHON="${PROJECT_ROOT}/.venv/bin/python"
LOG_DIR="${PROJECT_ROOT}/logs/preflight"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${LOG_DIR}/preflight_${TIMESTAMP}.txt"
FAILURES=0

mkdir -p "${LOG_DIR}"

check_pass() {
    echo "PASS: $1"
}

check_fail() {
    echo "FAIL: $1"
    FAILURES=$((FAILURES + 1))
}

{
    echo "CaseMetrology System Preflight"
    echo "Timestamp: $(date --iso-8601=seconds)"
    echo "Hostname: $(hostname)"
    echo "Git commit: $(git -C "${PROJECT_ROOT}" rev-parse --short HEAD)"
    echo

    echo "=== TIME SYNCHRONIZATION ==="
    if [[ "$(timedatectl show -p NTPSynchronized --value)" == "yes" ]]; then
        check_pass "System clock synchronized"
    else
        check_fail "System clock is not synchronized"
    fi
    timedatectl status
    echo

    echo "=== POWER MODE ==="
    nvpmodel -q 2>&1 || check_fail "Unable to read Jetson power mode"
    echo

    echo "=== STORAGE ==="
    df -hT /
    FREE_GB="$(df --output=avail -BG / | tail -1 | tr -dc '0-9')"
    if [[ "${FREE_GB:-0}" -ge 100 ]]; then
        check_pass "At least 100 GB storage available"
    else
        check_fail "Less than 100 GB storage available"
    fi
    echo

    echo "=== CAMERA ==="
    if lsusb | grep -qi '04b4:0499'; then
        check_pass "Arducam detected on USB bus"
    else
        check_fail "Arducam not detected; physically reconnect camera"
    fi

    if [[ -e "${CAMERA}" ]]; then
        check_pass "Persistent camera alias exists"
        ls -l "${CAMERA}"
    else
        check_fail "Persistent camera alias is missing"
    fi

    if [[ -e "${CAMERA}" ]] && v4l2-ctl --device="${CAMERA}" --all >/dev/null 2>&1; then
        check_pass "Camera capture interface responds"
    else
        check_fail "Camera capture interface does not respond"
    fi
    echo

    echo "=== PYTHON ENVIRONMENT ==="
    if [[ -x "${PYTHON}" ]]; then
        check_pass "Project Python interpreter exists"
        "${PYTHON}" --version
    else
        check_fail "Project Python interpreter is missing"
    fi

    if "${PYTHON}" -c 'import cv2, numpy, scipy, pandas, skimage' >/dev/null 2>&1; then
        check_pass "Required Python packages import successfully"
    else
        check_fail "One or more required Python packages failed to import"
    fi
    echo

    echo "=== REPOSITORY ==="
    git -C "${PROJECT_ROOT}" status -sb
    echo

    if [[ "${FAILURES}" -eq 0 ]]; then
        echo "PREFLIGHT RESULT: PASS"
    else
        echo "PREFLIGHT RESULT: FAIL (${FAILURES} issue(s))"
    fi
} | tee "${LOG_FILE}"

echo
echo "Preflight log saved to: ${LOG_FILE}"

exit "${FAILURES}"
