#!/usr/bin/env python3
"""Validate the expected structure for a music catalog deal workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_DIRS = ["source", "normalized", "workpapers", "findings", "memos"]
REQUIRED_FILES = ["assumptions.yaml", "evidence-ledger.json"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deal_workspace", help="Path to deals/{deal-id}")
    args = parser.parse_args()

    workspace = Path(args.deal_workspace)
    missing_dirs = [name for name in REQUIRED_DIRS if not (workspace / name).is_dir()]
    missing_files = [name for name in REQUIRED_FILES if not (workspace / name).is_file()]
    status = "ok" if not missing_dirs and not missing_files else "missing_requirements"
    payload = {
        "status": status,
        "workspace": str(workspace),
        "missing_dirs": missing_dirs,
        "missing_files": missing_files,
    }
    print(json.dumps(payload, indent=2))
    return 0 if status == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
