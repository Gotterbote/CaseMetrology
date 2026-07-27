#!/usr/bin/env bash
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON="${PROJECT_ROOT}/.venv/bin/python"
LOG_DIR="${PROJECT_ROOT}/logs/research_preflight"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${LOG_DIR}/research_preflight_${TIMESTAMP}.txt"
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
    echo "CaseMetrology Research Session Preflight"
    echo "Timestamp: $(date --iso-8601=seconds)"
    echo "Hostname: $(hostname)"
    echo "Project root: ${PROJECT_ROOT}"
    echo

    echo "=== BASE SYSTEM PREFLIGHT ==="
    if "${PROJECT_ROOT}/scripts/run_system_preflight.sh"; then
        check_pass "Base system preflight completed successfully"
    else
        check_fail "Base system preflight failed"
    fi
    echo

    echo "=== LOCKED CAMERA CONTROLS ==="
    if "${PYTHON}" \
        "${PROJECT_ROOT}/src/acquisition/apply_locked_controls.py"; then
        check_pass "Locked camera controls applied and verified"
    else
        check_fail "Locked camera controls could not be verified"
    fi
    echo

    echo "=== RESEARCH SOFTWARE ==="
    REQUIRED_FILES=(
        "src/acquisition/capture_research.py"
        "src/acquisition/apply_locked_controls.py"
        "src/calibration/analyze_gauge_block.py"
        "src/calibration/analyze_subpixel_gauge_block.py"
        "src/calibration/analyze_subpixel_batch.py"
        "src/calibration/compare_illumination.py"
    )

    for relative_path in "${REQUIRED_FILES[@]}"; do
        if [[ -f "${PROJECT_ROOT}/${relative_path}" ]]; then
            check_pass "${relative_path}"
        else
            check_fail "Missing ${relative_path}"
        fi
    done
    echo

    echo "=== REPOSITORY STATE ==="
    GIT_COMMIT="$(git -C "${PROJECT_ROOT}" rev-parse HEAD)"
    GIT_STATUS="$(git -C "${PROJECT_ROOT}" status --porcelain)"

    echo "Git commit: ${GIT_COMMIT}"

    if [[ -z "${GIT_STATUS}" ]]; then
        check_pass "Git working tree is clean"
    else
        check_fail "Git working tree contains uncommitted changes"
        printf '%s\n' "${GIT_STATUS}"
    fi
    echo

    if [[ "${FAILURES}" -eq 0 ]]; then
        echo "RESEARCH SESSION PREFLIGHT RESULT: PASS"
    else
        echo "RESEARCH SESSION PREFLIGHT RESULT: FAIL (${FAILURES} issue(s))"
    fi
} | tee "${LOG_FILE}"

echo
echo "Research preflight log saved to: ${LOG_FILE}"

exit "${FAILURES}"
