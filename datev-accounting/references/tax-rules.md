# German Umsatzsteuer (VAT) Rules — Lightness Fitness

## VAT Rates

| Rate | Applies to | EXTF Account |
|------|-----------|-------------|
| 19% (standard) | Digital courses, coaching, one-time purchases | 8400 |
| 7% (reduced) | Books, certain educational materials, cultural events | 8338 |

## Quarterly UStVA (Umsatzsteuer-Voranmeldung)

Filing frequency: Quarterly
Deadline: 10th of the month following the quarter end (with Dauerfristverlaengerung: +1 month)
- Q1 (Jan-Mar): Due April 10 / May 10
- Q2 (Apr-Jun): Due July 10 / August 10
- Q3 (Jul-Sep): Due October 10 / November 10
- Q4 (Oct-Dec): Due January 10 / February 10

## Calculation Formula

```
Output Tax (Umsatzsteuer):
  USt_19 = Revenue_19_gross * 19 / 119
  USt_7  = Revenue_7_gross * 7 / 107

Input Tax (Vorsteuer):
  VSt = Sum of deductible input tax from expense invoices

Section 13b Reverse Charge:
  USt_13b = Stripe_fees_Ireland * 19 / 100  (output tax)
  VSt_13b = Stripe_fees_Ireland * 19 / 100  (input tax, same amount)
  Net effect = 0 (tax-neutral)

Net Liability:
  Zahllast = (USt_19 + USt_7 + USt_13b) - (VSt + VSt_13b)
  Simplified: Zahllast = (USt_19 + USt_7) - VSt
```

## 2025 Tax Position (as of 2026-02-22)

| Quarter | Gross Revenue | USt Output | Vorsteuer | Net Liability | Filed | Outstanding |
|---------|--------------|-----------|-----------|---------------|-------|-------------|
| Q1 | ~58,600 EUR | ~7,635 EUR | ~1,160 EUR | ~6,475 EUR | 1,160 EUR | ~5,315 EUR |
| Q2 | ~107,500 EUR | ~15,104 EUR | ~3,364 EUR | ~11,740 EUR | 712 EUR | ~11,028 EUR |
| Q3 | ~34,200 EUR | ~4,390 EUR | ~870 EUR | ~3,520 EUR | 0 | ~3,520 EUR |
| Q4 | ~112,950 EUR | ~22,886 EUR | ~7,883 EUR | ~15,003 EUR | 0 | ~15,003 EUR |
| **Total** | **~313,252 EUR** | **~50,015 EUR** | **~13,277 EUR** | **~36,738 EUR** | **1,872 EUR** | **~34,866 EUR** |

Section 13b (Stripe Ireland fees): 4,555 EUR — tax-neutral, not included in net liability.

## Revenue Account Classification Issue

In 2025, two revenue accounts were used:
- **8338 (7% VAT):** 854 transactions, 171,880 EUR — predominantly Jan-Apr
- **8400 (19% VAT):** 1,407 transactions, 141,372 EUR — predominantly May-Dec

Identical price points (97, 29.97, 27, 39 EUR) appear in both accounts, indicating a reclassification mid-year rather than different products. The StB needs to confirm whether to unify on 8400 (19%).

## DATEV Gap (Critical)

As of Feb 2026:
- DATEV shows only ~29,284 EUR revenue (10% of actual)
- Actual Stripe revenue: ~313,252 EUR
- Missing: ~284,000 EUR in unbooked revenue
- DATEV shows a loss of -73,623 EUR; actual profit exceeds 208,000 EUR
- DATEV shows VAT refund position (-7,446 EUR); actual liability is +36,738 EUR
