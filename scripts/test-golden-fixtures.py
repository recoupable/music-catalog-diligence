#!/usr/bin/env python3
"""Run golden fixture tests for royalty statement normalization."""

from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PLUGIN_ROOT / "scripts" / "normalize-royalty-statement.py"
FIXTURE_ROOT = PLUGIN_ROOT / "fixtures" / "golden"


CASES = [
    ("ascap-performance", "ascap"),
    ("bmi-performance", "bmi"),
    ("mlc-mechanical", "mlc"),
    ("distributor-master", "distributor"),
    ("youtube-content-id", "youtube-content-id"),
    ("curve-income", "curve"),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class GoldenFixtureTest(unittest.TestCase):
    def test_all_golden_fixtures_match_expected_ledgers(self) -> None:
        for case_name, provider in CASES:
            with self.subTest(case=case_name):
                case_dir = FIXTURE_ROOT / case_name
                input_path = case_dir / "input.csv"
                expected_path = case_dir / "expected-royalty-ledger.csv"
                self.assertTrue(input_path.exists(), f"Missing input fixture: {input_path}")
                self.assertTrue(expected_path.exists(), f"Missing expected fixture: {expected_path}")

                with tempfile.TemporaryDirectory() as directory:
                    actual_path = Path(directory) / "actual.csv"
                    subprocess.run(
                        [
                            sys.executable,
                            str(SCRIPT),
                            "--provider",
                            provider,
                            "--input",
                            str(input_path.relative_to(PLUGIN_ROOT)),
                            "--output",
                            str(actual_path),
                        ],
                        cwd=PLUGIN_ROOT,
                        text=True,
                        capture_output=True,
                        check=True,
                    )
                    self.assertEqual(read_csv(actual_path), read_csv(expected_path))


if __name__ == "__main__":
    unittest.main()
