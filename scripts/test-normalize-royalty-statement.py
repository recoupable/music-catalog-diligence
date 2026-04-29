#!/usr/bin/env python3
"""Golden-fixture tests for provider CSV royalty normalization."""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("normalize-royalty-statement.py")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class NormalizeRoyaltyStatementTest(unittest.TestCase):
    def run_normalizer(self, provider: str, rows: list[dict[str, str]]) -> list[dict[str, str]]:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.csv"
            output = Path(directory) / "royalty-ledger.csv"
            write_csv(source, rows)
            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--provider",
                    provider,
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                ],
                check=True,
                text=True,
                capture_output=True,
            )
            return read_csv(output)

    def test_normalizes_ascap_performance_rows_with_bonus_detail(self) -> None:
        rows = [
            {
                "Work Title": "Forever Hook",
                "Work ID": "ASC123",
                "ISWC": "T1234567890",
                "Performance Start": "2025-01-01",
                "Performance End": "2025-03-31",
                "Distribution Date": "2025-06-15",
                "Territory": "US",
                "Licensee": "WABC-FM",
                "Use Type": "Feature",
                "Credits": "125.5",
                "Bonus Type": "Audio Feature Premium",
                "Gross Amount": "$1,250.00",
                "Deductions": "$125.00",
                "Publisher Share": "$1,125.00",
                "Currency": "USD",
            }
        ]

        ledger = self.run_normalizer("ascap", rows)

        self.assertEqual(len(ledger), 1)
        row = ledger[0]
        self.assertEqual(row["provider"], "ASCAP")
        self.assertEqual(row["rights_type"], "publishing")
        self.assertEqual(row["income_type"], "performance")
        self.assertEqual(row["catalog_asset_id"], "iswc:T1234567890")
        self.assertEqual(row["platform_or_licensee"], "WABC-FM")
        self.assertEqual(row["gross_amount"], "1250.00")
        self.assertEqual(row["deductions"], "125.00")
        self.assertEqual(row["owner_net_amount"], "1125.00")
        self.assertEqual(row["pro_use_type"], "Feature")
        self.assertEqual(row["pro_credits"], "125.5")
        self.assertEqual(row["pro_bonus_type"], "Audio Feature Premium")

    def test_normalizes_distributor_master_rows(self) -> None:
        rows = [
            {
                "Track Title": "Night Drive",
                "ISRC": "USRC17607839",
                "Sales Month": "2025-02",
                "Store": "Spotify",
                "Territory": "GB",
                "Gross": "500.00",
                "Fee": "75.00",
                "Net": "425.00",
                "Currency": "USD",
            }
        ]

        ledger = self.run_normalizer("distributor", rows)

        self.assertEqual(len(ledger), 1)
        row = ledger[0]
        self.assertEqual(row["provider"], "Distributor")
        self.assertEqual(row["rights_type"], "master")
        self.assertEqual(row["income_type"], "streaming")
        self.assertEqual(row["catalog_asset_id"], "isrc:USRC17607839")
        self.assertEqual(row["period_start"], "2025-02-01")
        self.assertEqual(row["period_end"], "2025-02-28")
        self.assertEqual(row["platform_or_licensee"], "Spotify")
        self.assertEqual(row["owner_net_amount"], "425.00")

    def test_rejects_unknown_provider(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.csv"
            output = Path(directory) / "royalty-ledger.csv"
            write_csv(source, [{"Title": "Unknown", "Amount": "10"}])
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--provider",
                    "not-a-provider",
                    "--input",
                    str(source),
                    "--output",
                    str(output),
                ],
                text=True,
                capture_output=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unsupported provider", result.stderr)


if __name__ == "__main__":
    unittest.main()
