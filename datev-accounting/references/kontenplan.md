# SKR03 Kontenplan — Lightness Fitness Stripe Accounts

## Account Mapping Table

| EXTF/SKR03 | DATEV Internal | Name | Type | VAT Rate | BU-Schluessel | Automatik |
|------------|---------------|------|------|----------|---------------|-----------|
| 1360 | 1360 | Stripe Verrechnungskonto | Asset | — | empty | No |
| 1800 | 1800 | Bank (Sparkasse) | Asset | — | empty | No |
| 8400 | 4400 | Erloese 19% USt | Revenue | 19% | empty | Yes |
| 8338 | — | Erloese 7% USt | Revenue | 7% | empty | Yes |
| 4970 | 6855 | Nebenkosten Geldverkehr | Expense | 19% | empty | Yes |
| 70156 | 70156 | Rueckerstattungen | Revenue | — | empty | No |
| 11000 | 11000 | Sammelkonto Debitor | Asset | — | A | No |
| 4839 | 4839 | Sonstige Aufwendungen 13b | Expense | — | 3 | No |

## BU-Schluessel Rules

| Key | Meaning | When to use |
|-----|---------|-------------|
| (empty) | Standard | Automatikkonten (8400, 4970, 8338) — DATEV calculates VAT automatically |
| A | Automatik | Used by StB for debitor aggregate bookings |
| 3 | Section 13b | Reverse charge (EU cross-border services, e.g., InnoNature) |
| 9 | WRONG | NEVER use for these booking types |

## Account Number Mapping Warning

DATEV shows different numbers in its web UI than what EXTF files require:
- **DATEV UI shows 4400** → EXTF CSV must use **8400**
- **DATEV UI shows 6855** → EXTF CSV must use **4970**
- Accounts 1360, 1800, 70156, 11000 are identical in both systems

Always use the EXTF/SKR03 column numbers when generating CSV files.

## Automatikkonten

Accounts marked as "Automatik" (8400, 4970, 8338) automatically calculate VAT in DATEV. The BU-Schluessel must be left EMPTY for these accounts — adding a BU key would override the automatic tax calculation and produce incorrect results.

## Stripe Transaction Flow

```
Customer Payment (97 EUR)
  └→ Stripe Charge: 1360 (Soll) / 8400 (Haben) = 97,00 EUR
  └→ Stripe Fee:    4970 (Soll) / 1360 (Haben) = 2,81 EUR
  └→ Net to Stripe Balance: 94,19 EUR

Stripe Payout (aggregated, e.g., 5,432.10 EUR)
  └→ ALREADY IN DATEV via bank feed: 1800 (Soll) / 1360 (Haben)
  └→ DO NOT INCLUDE IN EXTF CSV

Refund (97 EUR)
  └→ 1360 (Haben) / 8400 (Soll) = reversal
  └→ In EXTF: amount;H;EUR;;;;1360;8400;;...
```
