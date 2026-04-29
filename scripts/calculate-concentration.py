#!/usr/bin/env python3
"""Calculate concentration by common catalog royalty ledger dimensions."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


DEFAULT_DIMENSIONS = ["catalog_asset_id", "provider", "platform_or_licensee", "territory", "income_type"]


def parse_amount(value: str | None) -> float:
    if not value:
        return 0.0
    cleaned = value.replace("$", "").replace(",", "").replace("(", "-").replace(")", "")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger_csv", help="Path to royalty-ledger.csv")
    parser.add_argument("--amount-column", default="owner_net_amount")
    parser.add_argument("--dimensions", nargs="*", default=DEFAULT_DIMENSIONS)
    args = parser.parse_args()

    path = Path(args.ledger_csv)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))

    total = sum(parse_amount(row.get(args.amount_column)) for row in rows)
    results: dict[str, list[dict[str, object]]] = {}
    for dimension in args.dimensions:
        buckets: defaultdict[str, float] = defaultdict(float)
        for row in rows:
            key = row.get(dimension) or "unknown"
            buckets[key] += parse_amount(row.get(args.amount_column))
        ranked = sorted(buckets.items(), key=lambda item: abs(item[1]), reverse=True)
        results[dimension] = [
            {
                "value": key,
                "amount": amount,
                "percent_of_total": (amount / total * 100) if total else None,
            }
            for key, amount in ranked[:10]
        ]

    print(json.dumps({"status": "ok", "total": total, "concentration": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
