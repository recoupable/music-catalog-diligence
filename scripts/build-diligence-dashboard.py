#!/usr/bin/env python3
"""Build a markdown diligence dashboard for a catalog deal workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SEVERE_FINDINGS = {"P0", "P1"}


def load_json(path: Path, default: object) -> object:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def finding_severity(finding: dict[str, object]) -> str:
    return str(finding.get("severity", "")).upper()


def finding_status(finding: dict[str, object]) -> str:
    return str(finding.get("status", "")).lower()


def summarize_findings(workspace: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    data = load_json(workspace / "findings" / "findings.json", {"findings": []})
    findings = data.get("findings", []) if isinstance(data, dict) else []
    typed_findings = [finding for finding in findings if isinstance(finding, dict)]
    blockers = [
        finding
        for finding in typed_findings
        if finding_status(finding) == "open" and finding_severity(finding) in SEVERE_FINDINGS
    ]
    return typed_findings, blockers


def determine_status(blockers: list[dict[str, object]]) -> str:
    if any(finding_severity(finding) == "P0" for finding in blockers):
        return "blocked"
    if blockers:
        return "review_needed"
    return "ready"


def render_dashboard(workspace: Path) -> str:
    findings, blockers = summarize_findings(workspace)
    status = determine_status(blockers)
    lines = [
        "# Diligence Dashboard",
        "",
        f"- Workspace: `{workspace}`",
        f"- Overall status: `{status}`",
        f"- Findings: `{len(findings)}`",
        f"- Open P0/P1 blockers: `{len(blockers)}`",
        "",
        "## Open blockers",
        "",
    ]
    if blockers:
        for finding in blockers:
            finding_id = finding.get("finding_id", "unknown")
            severity = finding.get("severity", "unknown")
            title = finding.get("title", "Untitled finding")
            lines.append(f"- `{severity}` `{finding_id}`: {title}")
    else:
        lines.append("- None.")
    lines.extend(
        [
            "",
            "## Next actions",
            "",
        ]
    )
    if status == "blocked":
        lines.append("- Resolve P0 blockers before sharing the package.")
    elif status == "review_needed":
        lines.append("- Review open P1 findings and disclose or resolve them before sharing.")
    else:
        lines.append("- Run final memo citation review before sharing externally.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deal_workspace", help="Path to deals/{deal-id}")
    parser.add_argument("--output", help="Output markdown path")
    args = parser.parse_args()

    workspace = Path(args.deal_workspace)
    output = Path(args.output) if args.output else workspace / "diligence-dashboard.md"
    output.write_text(render_dashboard(workspace), encoding="utf-8")
    print(json.dumps({"status": "ok", "output": str(output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
