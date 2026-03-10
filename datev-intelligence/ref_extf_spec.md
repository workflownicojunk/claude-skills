# DATEV EXTF v700 Specification
**Format:** EXTF (Exchange Text Format) v700 | **Type:** Buchungsstapel (21)

## File Format Rules

1. **Encoding:** Windows-1252 (cp1252) — NOT UTF-8!
2. **Line separator:** CRLF (`\r\n`)
3. **Field separator:** Semicolon (`;`)
4. **Decimal separator:** Comma (`,`) — `97,00` not `97.00`
5. **String quoting:** Double quotes for text fields

## Structure

```
Line 1: Header metadata (27 fields)
Line 2: Column names
Lines 3+: Transaction data
```

## Header Line 1

```
"EXTF";700;21;"Buchungsstapel";12;{YYYYMMDD};"";"";"";"671912";"20048";{YYYYMMDD_fiscal_start};{acct_len};"";"";"";"";"";1;"";;;;;"";;;"{label}"
```

Fields:
- Position 1: "EXTF" (format identifier)
- Position 2: 700 (format version)
- Position 3: 21 (data type = Buchungsstapel)
- Position 4: "Buchungsstapel"
- Position 5: 12 (Buchungsstapel data format version)
- Position 6: YYYYMMDD (creation date)
- Position 10: "671912" (Berater)
- Position 11: "20048" (Mandant)
- Position 12: YYYYMMDD (fiscal year start = 20250101)
- Position 13: 4 (Sachkontennummernlänge = 4 digits for 4-digit accounts)
- Position 19: 1 (Festschreibung = 1 means entries can be modified)

## Column Names (Line 2)

```
Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;WKZ Umsatz;Kurs;Basisumsatz;WKZ Basisumsatz;Konto;Gegenkonto (ohne BU-Schluessel);BU-Schluessel;Belegdatum;Belegfeld 1;Belegfeld 2;Skonto;Buchungstext;Postensperre;[101 empty columns]
```

## Transaction Row Format

```csv
{amount};{SH};EUR;;;;{konto};{gegenkonto};{bu};{DDMM};{belegfeld1};;;"{text}";0;[101 empty]
```

## Standard Transaction Types

### Revenue (Charge)
```csv
97,00;S;EUR;;;;1360;8400;;0104;ch_3abc123;;;;"Checkout 97 EUR";0;...
```
- `S` = Soll (Debit to clearing account)
- Konto: 1360 (Stripe clearing)
- Gegenkonto: 8400 (Revenue 19% VAT) or 8338 (7% VAT)
- BU-Schlüssel: empty (Automatikkonto handles VAT automatically)

### Stripe Fee
```csv
2,81;S;EUR;;;;4970;1360;;0104;ch_3abc123;;;;"Stripe Fee";0;...
```
- `S` = Soll (Debit to expense account)
- Konto: 4970 (Stripe fees / Nebenkosten Geldverkehr)
- Gegenkonto: 1360 (Stripe clearing)
- BU-Schlüssel: empty

### Refund
```csv
97,00;H;EUR;;;;1360;8400;;0104;re_3abc123;;;;"Refund 97 EUR";0;...
```
- `H` = Haben (Credit = reverse the original charge)
- Same accounts as charge, reversed direction

### NEVER INCLUDE: Payouts
Payouts (type='payout' in Stripe) are already booked via bank feed.
Including them causes double-booking: 1360→1800 appears twice.

## BU-Schlüssel Reference

| Code | Meaning | Use Case |
|---|---|---|
| (empty) | Automatikkonto | Standard for 8400, 4970, 8338 — DATEV auto-calculates VAT |
| A | Automatik | StB uses for debitor collective bookings |
| 3 | §13b UStG | Reverse charge (Stripe Ireland, InnoNature) |
| 9 | **FORBIDDEN** | Wrong for these booking types — never use! |

## Date Format

- `Belegdatum`: DDMM format (2-digit day + 2-digit month)
- January 4th: `0104`
- December 31st: `3112`
- Fiscal year is determined by the header, not the date field

## Belegfeld 1 Limits

- Maximum 20 characters
- Use Stripe charge ID (`ch_3...`) or refund ID (`re_3...`)
- Truncate if longer: `charge_id[:20]`

## Python Code Pattern

```python
import csv, io
from datetime import datetime

def write_extf(rows, year, output_path):
    label = f"Stripe {year}"
    now = datetime.now().strftime("%Y%m%d")
    header1 = f'"EXTF";700;21;"Buchungsstapel";12;{now};"";"";"";"671912";"20048";{year}0101;4;"";"";"";"";"";1;"";;;;;"";;;"{label}"'
    header2 = "Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;WKZ Umsatz;Kurs;Basisumsatz;WKZ Basisumsatz;Konto;Gegenkonto (ohne BU-Schluessel);BU-Schluessel;Belegdatum;Belegfeld 1;Belegfeld 2;Skonto;Buchungstext;Postensperre" + ";" * 101

    with open(output_path, 'w', encoding='cp1252', newline='\r\n') as f:
        f.write(header1 + '\n')
        f.write(header2 + '\n')
        for row in rows:
            f.write(row + '\n')
```

See `nicol-automation-hub/datev/scripts/generate_extf.py` for full implementation.
