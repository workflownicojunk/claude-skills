---
name: datev-intelligence
description: >
  REFERENCE ONLY — loaded by datev-accounting as context. Contains Mandant
  671912-20048 account balances, 2025 annual summary, and discovered DATEV REST
  API endpoints. Do NOT trigger this skill directly. Use datev-accounting for all
  DATEV tasks including EXTF imports, VAT calculation, reconciliation, and portal queries.
---
# DATEV Intelligence Skill
**Version:** 1.0 | **Created:** 2026-02-22 | **Context:** Lightness Fitness / Nicol Stanzel

## When to Use This Skill

- Generating DATEV EXTF CSV imports from Stripe transaction data
- Querying DATEV Kontoblatt or SuSa data via the hidden REST API
- Calculating quarterly USt (Umsatzsteuer-Voranmeldung)
- Reconciling Stripe payouts against DATEV bank feed
- Answering questions about SKR03 account structure for this business

## Quick Reference

### Business Context
- **Mandant:** 671912-20048 | **Berater:** 671912
- **StB:** Andreas Möller (Andi) — admin@steuerberater-amoeller.de — 06655/9172414
- **Fiscal Year:** Calendar year (Jan 1 – Dec 31)
- **Chart of Accounts:** SKR03
- **Stripe Account:** acct_1Qgvx6GKl7aVHCCr (project: dajxbqfiugzigrnsoqau, schema: stripe.*)

### SKR03 Account Mapping (Critical)

| SKR03 (DATEV UI) | EXTF CSV | Description | DATEV Internal (×10000) |
|---|---|---|---|
| 1360 | 1360 | Stripe Clearing | 13600000 |
| 1800 | 1800 | Bank (Sparkasse) | 18000000 |
| 4400 | 8400 | Revenue 19% VAT | 44000000 |
| 4839 | 4839 | Section 13b Reverse Charge | 48390000 |
| 6855 | 4970 | Stripe Processing Fees | 68550000 |
| 70156 | 70156 | Refunds | 701560000 |
| 11000 | 11000 | Sammelkonto Debitor | 110000000 |

**EXTF ≠ DATEV UI numbers for revenue and fees!**

### DATEV Kontoblatt API

```bash
# Correct format — account × 10000 in URL path:
POST /awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048/fiscal-years/2025-01-01/accounts/{acct_x_10000}?fiscal-year-month-start=1&fiscal-year-month-end=12&ausziffern=ALL&sort=
Headers: X-Requested-With: kontoblatt
Body: null  # literally null, NOT '{}'
Auth: Session cookies (SmartLogin QR scan required)

# Examples:
# Account 4400 → /accounts/44000000
# Account 11000 → /accounts/110000000
# Account 70156 → /accounts/701560000
```

### EXTF CSV Format (v700) — Key Rules

1. Header line: `"EXTF";700;21;"Buchungsstapel";12;...;671912;20048;20250101;4;...`
2. Encoding: **Windows-1252** (not UTF-8!)
3. Decimal separator: **comma** (97,00 — not 97.00)
4. Date format: **DDMM** (0104 = January 4th)
5. Leave BU-Schlüssel empty for Automatikkonten (8400, 4970)
6. DO NOT include payout rows (already in DATEV via bank feed)

**Transaction row examples:**
```csv
97,00;S;EUR;;;;1360;8400;;0104;ch_xxx;;;"Checkout 97 EUR";0;...
2,81;S;EUR;;;;4970;1360;;0104;ch_xxx;;;"Stripe Fee";0;...
97,00;H;EUR;;;;1360;8400;;0104;re_xxx;;;"Refund 97 EUR";0;...
```

---

## Workflow: Generate EXTF CSV

```bash
cd nicol-automation-hub/datev/scripts
python generate_extf.py --year 2025 --output EXTF_2025.csv
# Or quarterly: python generate_extf.py --year 2025 --quarter 1 --output EXTF_Q1.csv
```

Reads from Supabase `stripe.*` schema (project: dajxbqfiugzigrnsoqau).
See `ref_extf_spec.md` for full column specification.

---

## Workflow: Query DATEV via API

Prerequisites: Active DATEV session in Chrome (SmartLogin QR scan done).

```javascript
// In Chrome DevTools console or via MCP evaluate_script:
const res = await fetch(
  'https://webapps.datev.de/awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048/fiscal-years/2025-01-01/accounts/44000000?fiscal-year-month-start=1&fiscal-year-month-end=12&ausziffern=ALL&sort=',
  { method: 'POST', headers: { 'X-Requested-With': 'kontoblatt', 'Accept': 'application/json' }, credentials: 'include', body: null }
);
const data = await res.json();
// data.transactions[] contains all bookings for account 4400
```

---

## Workflow: USt Calculation

```sql
-- Q1 2025 revenue from Supabase
SELECT SUM(amount)/100 as eur, COUNT(*) as charges
FROM stripe.charges
WHERE created >= 1735689600 AND created < 1743465600  -- Jan 1 – Mar 31 2025
  AND status = 'succeeded';

-- Output USt: revenue × 19/119 (for 19% gross amounts)
-- Net liability = Output USt - Input USt (Vorsteuer from DATEV expenses)
```

See `ref_ust_liability.md` for complete 2025 quarterly breakdown.

---

## Current Status (2026-02-22)

- EXTF CSV delivered to StB (4,960 rows, 324,335 EUR gross)
- StB must process CSV and resolve SevDesk overlap
- ~34,866 EUR USt outstanding for 2025 (Q3+Q4 unfiled)
- After import: 1360 account should balance to near-zero

## Reference Files

- `ref_extf_spec.md` — Complete EXTF v700 column specification
- `ref_kontenplan.md` — Full SKR03 account list with 2025 transaction totals
- `ref_ust_liability.md` — 2025 quarterly USt breakdown
- `ref_api_endpoints.md` — All discovered DATEV API endpoints
- `ref_2025_annual_summary.json` — Machine-readable year-end data

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
