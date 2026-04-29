#!/usr/bin/env python3
"""Build a JSON manifest for source files in a catalog deal workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(source_dir: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file():
            continue
        entries.append(
            {
                "path": str(path.relative_to(source_dir.parent)),
                "filename": path.name,
                "suffix": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deal_workspace", help="Path to deals/{deal-id}")
    parser.add_argument(
        "--output",
        default=None,
        help="Output JSON path. Defaults to workpapers/file-manifest.json.",
    )
    args = parser.parse_args()

    workspace = Path(args.deal_workspace)
    source_dir = workspace / "source"
    if not source_dir.is_dir():
        raise SystemExit(f"Missing source directory: {source_dir}")

    output = Path(args.output) if args.output else workspace / "workpapers" / "file-manifest.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {"deal_workspace": str(workspace), "files": build_manifest(source_dir)}
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(output), "files": len(payload["files"])}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
