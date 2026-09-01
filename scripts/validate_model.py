"""Run deterministic CRPI invariant checks and print a machine-readable report."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Support direct invocation from the repository root without requiring an
# editable package install.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from models.validation import run_invariant_checks


def main() -> None:
    checks = run_invariant_checks()
    print(json.dumps({"status": "pass", "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
