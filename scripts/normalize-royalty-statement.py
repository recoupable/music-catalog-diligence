#!/usr/bin/env python3
"""Normalize first-pass provider CSV exports into royalty-ledger.csv."""

from __future__ import annotations

import argparse
import calendar
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


CANONICAL_COLUMNS = [
    "ledger_line_id",
    "catalog_asset_id",
    "source_file",
    "provider",
    "period_start",
    "period_end",
    "payment_date",
    "rights_type",
    "income_type",
    "territory",
    "platform_or_licensee",
    "gross_amount",
    "deductions",
    "participant_share",
    "owner_net_amount",
    "currency",
    "fx_rate",
    "pro_use_type",
    "pro_credits",
    "pro_bonus_type",
    "cue_sheet_ref",
    "match_confidence",
    "notes",
]


def clean_amount(value: str | None) -> str:
    if not value:
        return ""
    cleaned = value.strip().replace("$", "").replace(",", "")
    is_negative = cleaned.startswith("(") and cleaned.endswith(")")
    cleaned = cleaned.strip("()")
    if not cleaned:
        return ""
    amount = float(cleaned)
    if is_negative:
        amount *= -1
    return f"{amount:.2f}"


def parse_month(value: str | None) -> tuple[str, str]:
    if not value:
        return "", ""
    text = value.strip()
    match = re.fullmatch(r"(\d{4})-(\d{2})", text)
    if not match:
        return text, text
    year = int(match.group(1))
    month = int(match.group(2))
    last_day = calendar.monthrange(year, month)[1]
    return f"{year:04d}-{month:02d}-01", f"{year:04d}-{month:02d}-{last_day:02d}"


def parse_quarter(value: str | None) -> tuple[str, str]:
    if not value:
        return "", ""
    text = value.strip()
    match = re.fullmatch(r"(\d{4})Q([1-4])", text)
    if not match:
        return "", ""
    year = int(match.group(1))
    quarter = int(match.group(2))
    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2
    last_day = calendar.monthrange(year, end_month)[1]
    return f"{year:04d}-{start_month:02d}-01", f"{year:04d}-{end_month:02d}-{last_day:02d}"


def parse_yyyymmdd(value: str | None) -> str:
    if not value:
        return ""
    text = value.strip()
    match = re.fullmatch(r"(\d{4})(\d{2})(\d{2})", text)
    if not match:
        return text
    return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"


def first(row: dict[str, str], *names: str) -> str:
    lower_lookup = {key.lower(): value for key, value in row.items() if isinstance(key, str)}
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value.strip()
        value = lower_lookup.get(name.lower())
        if value not in (None, ""):
            return value.strip()
    return ""


def has_meaningful_value(row: dict[str, str]) -> bool:
    values = [value.strip() for key, value in row.items() if isinstance(key, str) and value]
    if not values:
        return False
    first_value = values[0].lower()
    if first_value.startswith("totals") or first_value.startswith("note:"):
        return False
    return True


def asset_id(prefix: str, value: str, fallback: str) -> str:
    if value:
        return f"{prefix}:{value}"
    return f"title:{fallback.strip().lower().replace(' ', '-')}" if fallback else "unknown"


def blank_row(index: int, source_file: str) -> dict[str, str]:
    row = {column: "" for column in CANONICAL_COLUMNS}
    row["ledger_line_id"] = f"RL-{index:06d}"
    row["source_file"] = source_file
    row["match_confidence"] = "medium"
    return row


@dataclass(frozen=True)
class ProviderProfile:
    provider_name: str
    rights_type: str
    income_type: str
    normalize: Callable[[dict[str, str], int, str], dict[str, str]]


def normalize_ascap(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    output = blank_row(index, source_file)
    title = first(row, "Work Title", "Title")
    gross = clean_amount(first(row, "Gross Amount", "Gross", "Royalty Amount"))
    net = clean_amount(first(row, "Publisher Share", "Net", "Royalty Amount"))
    output.update(
        {
            "provider": "ASCAP",
            "rights_type": "publishing",
            "income_type": "performance",
            "catalog_asset_id": asset_id("iswc", first(row, "ISWC"), title),
            "period_start": first(row, "Performance Start", "Period Start"),
            "period_end": first(row, "Performance End", "Period End"),
            "payment_date": first(row, "Distribution Date", "Payment Date"),
            "territory": first(row, "Territory"),
            "platform_or_licensee": first(row, "Licensee", "Station", "Network", "Series / Film Title"),
            "gross_amount": gross,
            "deductions": clean_amount(first(row, "Deductions", "Fees")),
            "participant_share": first(row, "Share %"),
            "owner_net_amount": net,
            "currency": first(row, "Currency") or "USD",
            "pro_use_type": first(row, "Use Type", "Perf. Type"),
            "pro_credits": first(row, "Credits", "Total Credits", "Premium Credits"),
            "pro_bonus_type": first(row, "Bonus Type", "Premium Type"),
            "cue_sheet_ref": first(row, "Cue Sheet", "Program"),
            "notes": f"work_id={first(row, 'Work ID')}" if first(row, "Work ID") else "",
        }
    )
    return output


def normalize_bmi(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    output = blank_row(index, source_file)
    title = first(row, "Title", "Work Title")
    quarter_start, quarter_end = parse_quarter(first(row, "Statement Qtr"))
    hit_song_bonus = clean_amount(first(row, "Hit Song Bonus"))
    bonus_type = first(row, "Bonus Category", "Bonus Type") or ("Hit Song Bonus" if hit_song_bonus not in ("", "0.00") else "")
    net = clean_amount(first(row, "Publisher Net", "Net", "Amount Paid"))
    output.update(
        {
            "provider": "BMI",
            "rights_type": "publishing",
            "income_type": "performance",
            "catalog_asset_id": asset_id("iswc", first(row, "ISWC"), title),
            "period_start": first(row, "Period Start") or quarter_start,
            "period_end": first(row, "Period End") or quarter_end,
            "payment_date": first(row, "Payment Date"),
            "territory": first(row, "Territory"),
            "platform_or_licensee": first(row, "Station", "Licensee", "Network"),
            "gross_amount": clean_amount(first(row, "Amount", "Gross Amount", "Amount Paid")),
            "deductions": clean_amount(first(row, "Admin Fee", "Deductions")),
            "owner_net_amount": net,
            "currency": first(row, "Currency") or "USD",
            "pro_use_type": first(row, "Performance Type", "Use Type"),
            "pro_bonus_type": bonus_type,
            "notes": f"bmi_work_id={first(row, 'BMI Work #')}" if first(row, "BMI Work #") else "",
        }
    )
    return output


def normalize_distributor(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    output = blank_row(index, source_file)
    title = first(row, "Track Title", "Title")
    period_start, period_end = parse_month(first(row, "Sales Month", "Period"))
    rights_type = first(row, "Rights Type").lower() or "master"
    income_type = first(row, "Income Type").lower() or "streaming"
    output.update(
        {
            "provider": "Distributor",
            "rights_type": rights_type,
            "income_type": income_type,
            "catalog_asset_id": asset_id("isrc", first(row, "ISRC"), title),
            "period_start": first(row, "Period Start") or period_start,
            "period_end": first(row, "Period End") or period_end,
            "payment_date": first(row, "Report Date", "Payment Date"),
            "territory": first(row, "Territory", "Country"),
            "platform_or_licensee": first(row, "Store", "DSP", "Platform", "Source"),
            "gross_amount": clean_amount(first(row, "Gross", "Gross Amount")),
            "deductions": clean_amount(first(row, "Fee", "Deductions")),
            "owner_net_amount": clean_amount(first(row, "Net", "Net Amount", "Net Payable")),
            "currency": first(row, "Currency") or "USD",
            "fx_rate": first(row, "FX", "FX Rate"),
            "notes": first(row, "Notes"),
        }
    )
    return output


def normalize_common_statement(
    row: dict[str, str],
    index: int,
    source_file: str,
    provider: str,
    rights_type: str,
    income_type: str,
) -> dict[str, str]:
    output = normalize_distributor(row, index, source_file)
    output.update(
        {
            "provider": provider,
            "rights_type": rights_type,
            "income_type": income_type,
        }
    )
    return output


def normalize_publisher_admin(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    return normalize_common_statement(row, index, source_file, "Publisher Admin", "publishing", "mechanical")


def normalize_soundexchange(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    return normalize_common_statement(row, index, source_file, "SoundExchange", "neighboring", "radio")


def normalize_direct_sync(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    return normalize_common_statement(row, index, source_file, "Direct Sync", "sync", "sync")


def normalize_youtube(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    output = blank_row(index, source_file)
    title = first(row, "Asset Title", "Track Title", "Title")
    report_date = parse_yyyymmdd(first(row, "date"))
    period_start, period_end = parse_month(first(row, "Reporting Month", "Month"))
    output.update(
        {
            "provider": "YouTube Content ID",
            "rights_type": "master",
            "income_type": "ugc",
            "catalog_asset_id": first(row, "custom_id") or asset_id("isrc", first(row, "ISRC", "isrc"), title),
            "period_start": period_start or report_date,
            "period_end": period_end or report_date,
            "territory": first(row, "Country", "Territory", "country_code"),
            "platform_or_licensee": "YouTube",
            "gross_amount": clean_amount(first(row, "Gross Revenue", "Gross", "youtube_revenue_split")),
            "owner_net_amount": clean_amount(first(row, "Net Revenue", "Net", "partner_revenue_usd")),
            "currency": first(row, "Currency", "currency_code") or "USD",
            "notes": f"content_type={first(row, 'Content Type')}" if first(row, "Content Type") else f"asset_id={first(row, 'asset_id')}" if first(row, "asset_id") else "",
        }
    )
    return output


def normalize_mlc(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    output = blank_row(index, source_file)
    title = first(row, "Song Title", "Work Title", "Title")
    period_start, period_end = parse_month(first(row, "Usage Period", "Period"))
    output.update(
        {
            "provider": "The MLC",
            "rights_type": "publishing",
            "income_type": "mechanical",
            "catalog_asset_id": asset_id("iswc", first(row, "ISWC"), title),
            "period_start": first(row, "Period Start") or period_start,
            "period_end": first(row, "Period End") or period_end,
            "payment_date": first(row, "Report Date", "Payment Date"),
            "territory": first(row, "Territory") or "US",
            "platform_or_licensee": first(row, "DSP", "Platform", "Source"),
            "gross_amount": clean_amount(first(row, "Mechanical Gross", "Gross")),
            "deductions": clean_amount(first(row, "Admin Fee", "Deductions")),
            "owner_net_amount": clean_amount(first(row, "Publisher Net", "Net", "Net Payable")),
            "currency": first(row, "Currency") or "USD",
            "fx_rate": first(row, "FX", "FX Rate"),
            "notes": first(row, "Notes"),
        }
    )
    return output


def normalize_curve(row: dict[str, str], index: int, source_file: str) -> dict[str, str]:
    output = blank_row(index, source_file)
    title = first(row, "Track Title", "Work Title", "Title")
    rights_type = first(row, "Rights Type").lower() or "unknown"
    output.update(
        {
            "provider": "Curve",
            "rights_type": rights_type,
            "income_type": first(row, "Income Type").lower() or "unknown",
            "catalog_asset_id": first(row, "Source Work ID") or asset_id("isrc", first(row, "ISRC"), title),
            "period_start": first(row, "Period Start"),
            "period_end": first(row, "Period End"),
            "territory": first(row, "Territory"),
            "platform_or_licensee": first(row, "Royalty Source", "Source"),
            "gross_amount": clean_amount(first(row, "Gross")),
            "deductions": clean_amount(first(row, "Deductions")),
            "owner_net_amount": clean_amount(first(row, "Net Payable", "Net")),
            "currency": first(row, "Currency") or "USD",
        }
    )
    return output


PROFILES: dict[str, ProviderProfile] = {
    "ascap": ProviderProfile("ASCAP", "publishing", "performance", normalize_ascap),
    "bmi": ProviderProfile("BMI", "publishing", "performance", normalize_bmi),
    "distributor": ProviderProfile("Distributor", "master", "streaming", normalize_distributor),
    "publisher-admin": ProviderProfile("Publisher Admin", "publishing", "mechanical", normalize_publisher_admin),
    "soundexchange": ProviderProfile("SoundExchange", "neighboring", "radio", normalize_soundexchange),
    "direct-sync": ProviderProfile("Direct Sync", "sync", "sync", normalize_direct_sync),
    "youtube-content-id": ProviderProfile("YouTube Content ID", "master", "ugc", normalize_youtube),
    "mlc": ProviderProfile("The MLC", "publishing", "mechanical", normalize_mlc),
    "curve": ProviderProfile("Curve", "unknown", "unknown", normalize_curve),
}


def normalize(provider: str, input_path: Path, output_path: Path) -> dict[str, object]:
    profile = PROFILES.get(provider)
    if profile is None:
        supported = ", ".join(sorted(PROFILES))
        raise SystemExit(f"Unsupported provider '{provider}'. Supported providers: {supported}")

    with input_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if has_meaningful_value(row)]

    normalized_rows = [
        profile.normalize(row, index + 1, str(input_path))
        for index, row in enumerate(rows)
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANONICAL_COLUMNS)
        writer.writeheader()
        writer.writerows(normalized_rows)

    return {
        "status": "ok",
        "provider": profile.provider_name,
        "input": str(input_path),
        "output": str(output_path),
        "rows": len(normalized_rows),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, help=f"One of: {', '.join(sorted(PROFILES))}")
    parser.add_argument("--input", required=True, help="Provider CSV export")
    parser.add_argument("--output", required=True, help="Output royalty-ledger.csv path")
    args = parser.parse_args()

    payload = normalize(args.provider, Path(args.input), Path(args.output))
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
