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
lake env lean CRPI/Audit.lean
