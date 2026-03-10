#!/usr/bin/env python3
"""
DATEV EXTF CSV Generator — Stripe to DATEV Export

Generates a DATEV EXTF v700 compliant CSV from Stripe transaction data
stored in Supabase. Connects to project dajxbqfiugzigrnsoqau, schema stripe.*.

Usage:
    python generate_extf.py --year 2025 --output EXTF_Stripe_2025.csv
    python generate_extf.py --year 2025 --quarter 1 --output EXTF_Q1_2025.csv

Requirements:
    pip install supabase python-dotenv

Environment:
    SUPABASE_URL=https://dajxbqfiugzigrnsoqau.supabase.co
    SUPABASE_SERVICE_ROLE_KEY=...
"""

import argparse
import csv
import io
import os
import sys
from datetime import datetime, date
from pathlib import Path

try:
    from supabase import create_client
    from dotenv import load_dotenv
except ImportError:
    print("Missing dependencies. Install: pip install supabase python-dotenv")
    sys.exit(1)

# DATEV constants
BERATER = "671912"
MANDANT = "20048"
SACHKONTENNUMMERNLAENGE = 4
CURRENCY = "EUR"

# Account mapping
ACCOUNT_REVENUE_19 = "8400"
ACCOUNT_REVENUE_7 = "8338"
ACCOUNT_CLEARING = "1360"
ACCOUNT_FEES = "4970"


def get_date_range(year: int, quarter: int = None):
    """Return start/end dates for year or quarter."""
    if quarter:
        month_start = (quarter - 1) * 3 + 1
        month_end = quarter * 3
        start = date(year, month_start, 1)
        if month_end == 12:
            end = date(year + 1, 1, 1)
        else:
            end = date(year, month_end + 1, 1)
    else:
        start = date(year, 1, 1)
        end = date(year + 1, 1, 1)
    return start, end


def format_amount(cents: int) -> str:
    """Convert cents to DATEV decimal format (comma separator)."""
    eur = abs(cents) / 100
    return f"{eur:.2f}".replace(".", ",")


def format_belegdatum(unix_ts: int) -> str:
    """Convert Unix timestamp to DDMM format."""
    dt = datetime.utcfromtimestamp(unix_ts)
    return dt.strftime("%d%m")


def build_header(year: int, label: str) -> str:
    """Generate EXTF header line 1."""
    now = datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]
    fiscal_start = f"{year}0101"
    parts = [
        '"EXTF"', '700', '21', '"Buchungsstapel"', '12',
        now[:8], '""', '""', '""',
        f'"{BERATER}"', f'"{MANDANT}"',
        fiscal_start, str(SACHKONTENNUMMERNLAENGE),
        '""', '""', '""', '""', '""', '1', '""',
        '', '', '', '""', '', '', f'"{label}"'
    ]
    return ";".join(parts)


COLUMN_NAMES = (
    "Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;WKZ Umsatz;Kurs;"
    "Basisumsatz;WKZ Basisumsatz;Konto;Gegenkonto (ohne BU-Schluessel);"
    "BU-Schluessel;Belegdatum;Belegfeld 1;Belegfeld 2;Skonto;Buchungstext;"
    "Postensperre"
)
# Pad remaining ~101 columns with empty fields
COLUMN_PADDING = ";" * 101


def make_row(amount_str: str, sh: str, konto: str, gegenkonto: str,
             bu: str, belegdatum: str, belegfeld1: str, text: str) -> str:
    """Create a single EXTF data row."""
    fields = [
        amount_str, sh, CURRENCY, "", "", "",
        konto, gegenkonto, bu, belegdatum,
        belegfeld1[:20] if belegfeld1 else "",
        "", "", f'"{text}"', "0"
    ]
    return ";".join(fields) + COLUMN_PADDING


def main():
    parser = argparse.ArgumentParser(description="Generate DATEV EXTF CSV from Stripe data")
    parser.add_argument("--year", type=int, required=True, help="Fiscal year")
    parser.add_argument("--quarter", type=int, choices=[1, 2, 3, 4], help="Quarter (optional)")
    parser.add_argument("--output", type=str, required=True, help="Output CSV filename")
    parser.add_argument("--revenue-account", type=str, default=ACCOUNT_REVENUE_19,
                        help=f"Revenue account (default: {ACCOUNT_REVENUE_19})")
    args = parser.parse_args()

    # Load env
    env_paths = [
        Path(__file__).parent.parent.parent.parent.parent / ".env",  # workspace root
        Path.cwd() / ".env",
    ]
    for p in env_paths:
        if p.exists():
            load_dotenv(p)
            break

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        print("Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        sys.exit(1)

    supabase = create_client(url, key)
    start, end = get_date_range(args.year, args.quarter)
    start_epoch = int(datetime.combine(start, datetime.min.time()).timestamp())
    end_epoch = int(datetime.combine(end, datetime.min.time()).timestamp())

    print(f"Generating EXTF for {start} to {end}...")

    # Fetch charges
    charges = supabase.from_("charges").select(
        "id,amount,created,description,customer,status"
    ).gte("created", start_epoch).lt("created", end_epoch).eq(
        "status", "succeeded"
    ).execute()
    print(f"  Charges: {len(charges.data)}")

    # Fetch balance transactions (for fees)
    balance_txns = supabase.from_("balance_transactions").select(
        "id,amount,fee,net,created,source,type"
    ).gte("created", start_epoch).lt("created", end_epoch).eq(
        "type", "charge"
    ).execute()
    fee_map = {bt["source"]: bt for bt in balance_txns.data}
    print(f"  Balance transactions: {len(balance_txns.data)}")

    # Fetch refunds
    refunds = supabase.from_("refunds").select(
        "id,amount,created,charge,reason"
    ).gte("created", start_epoch).lt("created", end_epoch).execute()
    print(f"  Refunds: {len(refunds.data)}")

    # Build rows
    rows = []
    label = f"Stripe {args.year}" + (f" Q{args.quarter}" if args.quarter else "")

    for charge in charges.data:
        amt = format_amount(charge["amount"])
        belegdatum = format_belegdatum(charge["created"])
        desc_amount = charge["amount"] / 100

        # Revenue row
        rows.append(make_row(
            amt, "S", ACCOUNT_CLEARING, args.revenue_account,
            "", belegdatum, charge["id"],
            f"Checkout {desc_amount:.0f} EUR"
        ))

        # Fee row (if available)
        bt = fee_map.get(charge["id"])
        if bt and bt["fee"] > 0:
            fee_amt = format_amount(bt["fee"])
            rows.append(make_row(
                fee_amt, "S", ACCOUNT_FEES, ACCOUNT_CLEARING,
                "", belegdatum, charge["id"],
                "Stripe Fee"
            ))

    for refund in refunds.data:
        amt = format_amount(refund["amount"])
        belegdatum = format_belegdatum(refund["created"])
        desc_amount = refund["amount"] / 100

        rows.append(make_row(
            amt, "H", ACCOUNT_CLEARING, args.revenue_account,
            "", belegdatum, refund["id"],
            f"Refund {desc_amount:.0f} EUR"
        ))

    # Write EXTF CSV
    header1 = build_header(args.year, label)
    header2 = COLUMN_NAMES + COLUMN_PADDING

    output_path = Path(args.output)
    with open(output_path, "w", encoding="cp1252", newline="\r\n") as f:
        f.write(header1 + "\n")
        f.write(header2 + "\n")
        for row in rows:
            f.write(row + "\n")

    total_revenue = sum(c["amount"] / 100 for c in charges.data)
    total_fees = sum(fee_map.get(c["id"], {}).get("fee", 0) / 100 for c in charges.data)
    total_refunds = sum(r["amount"] / 100 for r in refunds.data)

    print(f"\nGenerated: {output_path}")
    print(f"  Rows: {len(rows)}")
    print(f"  Revenue: {total_revenue:,.2f} EUR ({len(charges.data)} charges)")
    print(f"  Fees: {total_fees:,.2f} EUR")
    print(f"  Refunds: {total_refunds:,.2f} EUR ({len(refunds.data)} refunds)")
    print(f"  Encoding: Windows-1252")


if __name__ == "__main__":
    main()
