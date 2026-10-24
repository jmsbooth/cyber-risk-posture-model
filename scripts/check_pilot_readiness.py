"""Metadata-only study readiness check; no participant/source records are accepted."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from models.pilot_readiness import assess_registration


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("registration", type=Path, help="metadata-only JSON manifest")
    ap.add_argument("--require-ready", action="store_true", help="fail when documentary gates are pending")
    args = ap.parse_args()
    manifest = json.loads(args.registration.read_text(encoding="utf-8"))
    result = assess_registration(manifest)
    print(json.dumps(result, sort_keys=True, indent=2))
    if not result["structurally_valid"]:
        return 1
    if args.require_ready and not result["documentary_gates_complete"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())