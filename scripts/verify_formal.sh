#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT/formal/lean"

if ! command -v lake >/dev/null 2>&1; then
  echo "BLOCKED: lake is not installed; no Lean verification was performed." >&2
  exit 127
fi

echo "Lean executable: $(command -v lean || echo unavailable)"
echo "Lake executable: $(command -v lake)"
echo "Toolchain: $(cat lean-toolchain)"

# Formalization source checks provide a secondary safeguard; compiler and
# kernel checks below remain mandatory for acceptance.
if grep -R -n -E '(^|[^[:alnum:]_])(sorry|admit|axiom|unsafe|native_decide)([^[:alnum:]_]|$)' \
    CRPI CRPI.lean; then
  echo "BLOCKED: forbidden construct in theorem-bearing sources." >&2
  exit 1
fi

lake build
AUDIT_DIR="$ROOT/artifacts/formal-axiom-audits"
mkdir -p "$AUDIT_DIR"
for audit in Audit AuditB AuditC; do
    echo "Auditing CRPI/$audit.lean"
    lake env lean "CRPI/$audit.lean" | tee "$AUDIT_DIR/$audit.log"
    if grep -n -E 'sorryAx|unsupported axiom|^error:' "$AUDIT_DIR/$audit.log"; then
        echo "BLOCKED: unexpected axiom or error in $audit audit." >&2
        exit 1
    fi
done
echo "A/B/C axiom audit logs captured at $AUDIT_DIR"
