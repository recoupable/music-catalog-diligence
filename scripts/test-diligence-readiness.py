#!/usr/bin/env python3
"""Tests for diligence readiness helpers."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
RUN_CHECKS = SCRIPT_DIR / "run-diligence-checks.py"
BUILD_DASHBOARD = SCRIPT_DIR / "build-diligence-dashboard.py"


def create_workspace(root: Path) -> Path:
    workspace = root / "deals" / "catalog-sale"
    for directory in ["source", "normalized", "workpapers", "findings", "memos"]:
        (workspace / directory).mkdir(parents=True, exist_ok=True)
    (workspace / "assumptions.yaml").write_text("deal_id: catalog-sale\n", encoding="utf-8")
    (workspace / "evidence-ledger.json").write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "evidence_id": "EV-001",
                        "source_file": "source/royalties.csv",
                        "source_type": "royalty_statement",
                        "locator": "row 2",
                        "extracted_field": "owner_net_amount",
                        "extracted_value": "85.00",
                        "confidence": "high",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (workspace / "normalized" / "royalty-ledger.csv").write_text(
        "ledger_line_id,catalog_asset_id,source_file,provider,period_start,period_end,rights_type,income_type,gross_amount,owner_net_amount,currency\n"
        "RL-000001,isrc:USRC17607839,source/royalties.csv,Distributor,2025-01-01,2025-01-31,master,streaming,100.00,85.00,USD\n",
        encoding="utf-8",
    )
    (workspace / "findings" / "findings.json").write_text(
        json.dumps(
            {
                "findings": [
                    {
                        "finding_id": "F-001",
                        "severity": "P1",
                        "status": "open",
                        "title": "Missing split sheet for top composition",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (workspace / "workpapers" / "valuation-summary.json").write_text(
        '{"status": "preliminary"}\n',
        encoding="utf-8",
    )
    return workspace


class DiligenceReadinessTest(unittest.TestCase):
    def test_run_checks_reports_all_validator_results(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = create_workspace(Path(directory))

            result = subprocess.run(
                [sys.executable, str(RUN_CHECKS), str(workspace)],
                check=False,
                text=True,
                capture_output=True,
            )

        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(
            [check["name"] for check in payload["checks"]],
            ["workspace", "normalized_ledger", "evidence_ledger"],
        )

    def test_build_dashboard_writes_status_summary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = create_workspace(Path(directory))
            output = workspace / "diligence-dashboard.md"

            result = subprocess.run(
                [sys.executable, str(BUILD_DASHBOARD), str(workspace), "--output", str(output)],
                check=False,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0)
            text = output.read_text(encoding="utf-8")

        self.assertIn("# Diligence Dashboard", text)
        self.assertIn("Overall status: `review_needed`", text)
        self.assertIn("Missing split sheet for top composition", text)


if __name__ == "__main__":
    unittest.main()
