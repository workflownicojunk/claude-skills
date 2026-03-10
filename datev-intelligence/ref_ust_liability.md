# USt Liability 2025 — Lightness Fitness
**Calculated:** 2026-02-22 | **Based on:** Stripe Supabase data (dajxbqfiugzigrnsoqau)

## Outstanding Tax Position

| Quarter | Stripe Revenue | Output USt | Filed | Outstanding |
|---|---|---|---|---|
| Q1 (Jan–Mar) | ~81,875 EUR | ~6,475 EUR | 1,160 EUR | **~5,315 EUR** |
| Q2 (Apr–Jun) | ~148,311 EUR | ~11,740 EUR | 712 EUR | **~11,028 EUR** |
| Q3 (Jul–Sep) | ~44,406 EUR | ~3,520 EUR | 0 EUR | **~3,520 EUR** |
| Q4 (Oct–Dec) | ~189,370 EUR | ~15,003 EUR | 0 EUR | **~15,003 EUR** |
| **Total 2025** | **~313,252 EUR** | **~36,738 EUR** | **1,872 EUR** | **~34,866 EUR** |

Input Vorsteuer ~13,277 EUR already deducted in above.
Section 13b (Stripe Ireland fees) ~4,555 EUR — tax-neutral (Steuer = Vorsteuer cancels out).

## USt Calculation Method

For each Stripe charge (gross amount):
```python
# 19% VAT (most products from May 2025 onwards)
ust_19 = gross_amount * 19 / 119

# 7% VAT (some products Jan–Apr 2025)
ust_7 = gross_amount * 7 / 107
```

Revenue split:
- Account 8338 (7%): 176,434 EUR → Jan–Apr 2025 (SevDesk legacy bookings)
- Account 8400 (19%): 147,901 EUR → mixed periods

## Vorsteuer Sources (2025)

| Source | Amount |
|---|---|
| Stripe Ireland fees (4970/§13b) | 4,555 EUR |
| General business expenses | ~8,722 EUR |
| **Total Vorsteuer** | **~13,277 EUR** |

## Filed UStVA Status

| Quarter | Amount | Date Filed | Notes |
|---|---|---|---|
| Q1 | 1,160 EUR | ~Apr 2025 | Corrected/Nachzahlung |
| Q2 | 712 EUR | ~Jul 2025 | |
| Q3 | 0 EUR | NOT FILED | StB in progress (Dec 2025) |
| Q4 | 0 EUR | NOT FILED | Awaiting EXTF import |

**Action Required:** StB must file Q3 + Q4 + correct Q1/Q2 after EXTF import processing.

## Revenue by Product (Estimated 2025)

| Product | Price | Volume | Revenue |
|---|---|---|---|
| Circle Membership (39 EUR/mo) | 39 EUR | ~960 active | ~45K EUR |
| StrongerYou X.0 Full (497 EUR) | 497 EUR | ~100 units | ~50K EUR |
| StrongerYou X.0 Installment (97 EUR) | 97 EUR | ~400 charges | ~39K EUR |
| SY 3.0 Coaching (179/349 EUR) | 179–349 EUR | ~100 charges | ~25K EUR |
| BodyGuide (97 EUR) | 97 EUR | ~600 units | ~58K EUR |
| Annual Memberships | 239–390 EUR | ~50 | ~15K EUR |

Note: These are estimates. Actual Stripe data in Supabase is authoritative.
