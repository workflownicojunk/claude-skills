---
name: datev-accounting
description: >
  German DATEV accounting toolkit for generating EXTF CSV imports, calculating quarterly
  Umsatzsteuer (VAT), and reconciling Stripe payment data with DATEV bookkeeping.
  Use when: (1) generating DATEV EXTF v700 CSV files from Stripe transactions,
  (2) calculating quarterly USt liability (7%/19% VAT rates),
  (3) reconciling Stripe payouts against DATEV bank feed entries,
  (4) mapping SKR03 chart of accounts between DATEV internal and EXTF numbering,
  (5) preparing tax-related correspondence with the Steuerberater,
  (6) analyzing DATEV Kontoblatt or SuSa (trial balance) JSON data,
  (7) any task involving BU-Schluessel, Automatikkonten, or Section 13b reverse charge.
  Outputs in German where required. Internal reasoning in English.
---

# DATEV Accounting Toolkit

Generate DATEV-compliant EXTF CSV exports from Stripe data, calculate German VAT obligations, and reconcile financial records for Lightness Fitness / Nicol Stanzel.

## Quick Reference

| Item | Value |
|------|-------|
| DATEV Mandant | 671912-20048 |
| Chart of Accounts | SKR03 |
| Fiscal Year | Calendar year (Jan-Dec) |
| Stripe Clearing Account | 1360 |
| Revenue 19% | 8400 (DATEV internal: 4400) |
| Revenue 7% | 8338 |
| Fees | 4970 (DATEV internal: 6855) |
| Bank | 1800 |
| EXTF Encoding | Windows-1252 |
| Decimal Separator | Comma (97,00) |
| Field Separator | Semicolon |
| Belegdatum Format | DDMM (4 digits) |

## Task Decision Tree

1. **Generate DATEV import CSV** → Run `scripts/generate_extf.py` or follow EXTF rules below
2. **Calculate quarterly VAT** → Read [references/tax-rules.md](references/tax-rules.md), query Supabase
3. **Reconcile payouts** → Compare Stripe payouts vs DATEV Kontoblatt 1360
4. **Analyze DATEV data** → Read [references/datev-api.md](references/datev-api.md) for data structures
5. **Email Steuerberater** → Professional German, du-Form, sign as Nico

## EXTF CSV Generation

### Using the Script
```bash
python scripts/generate_extf.py --year 2025 --output EXTF_Stripe_2025.csv
```

### Manual Row Patterns

Revenue (charge hits clearing account, credits revenue):
```
97,00;S;EUR;;;;1360;8400;;0104;ch_3abc123;;;"Checkout 97 EUR";0;
```

Fee (expense debited, clearing credited):
```
2,81;S;EUR;;;;4970;1360;;0104;ch_3abc123;;;"Stripe Fee";0;
```

Refund (reversal of charge):
```
97,00;H;EUR;;;;1360;8400;;0104;re_abc123;;;"Refund 97 EUR";0;
```

### Critical Rules
- NEVER include payout rows (type=payout). Already in DATEV via bank feed.
- BU-Schluessel: Leave EMPTY for Automatikkonten. Never use "9".
- Belegdatum: DDMM format (0104 = Jan 4th), not DDMMYYYY.
- Encoding: Windows-1252, not UTF-8.
- DATEV internal 4400 = EXTF 8400. DATEV 6855 = EXTF 4970.

For full EXTF format specification: [references/extf-format.md](references/extf-format.md)

## USt Calculation Workflow

1. Query revenue per VAT rate from Supabase (stripe.charges + stripe.balance_transactions)
2. Output tax: `19% revenue * 19/119` + `7% revenue * 7/107`
3. Input tax (Vorsteuer): Sum from DATEV expense accounts
4. Section 13b (Stripe Ireland fees): Tax-neutral (USt = Vorsteuer, cancels out)
5. Net liability = Output tax - Input tax

For detailed rules and quarterly breakdown: [references/tax-rules.md](references/tax-rules.md)

## Reference Files

| File | Read when... |
|------|-------------|
| [references/extf-format.md](references/extf-format.md) | Generating or validating EXTF CSV files |
| [references/kontenplan.md](references/kontenplan.md) | Looking up account numbers, mappings, or BU-Schluessel |
| [references/tax-rules.md](references/tax-rules.md) | Calculating VAT, preparing UStVA, or tax questions |
| [references/datev-api.md](references/datev-api.md) | Querying DATEV REST API or parsing JSON responses |
| [references/stripe-queries.md](references/stripe-queries.md) | Writing Supabase SQL for Stripe data |
| `~/.claude/skills/datev-intelligence/SKILL.md` | Account balances, 2025 annual summary, DATEV portal context |

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
