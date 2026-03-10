# Stripe Supabase Query Patterns

All Stripe data is mirrored in Supabase project `dajxbqfiugzigrnsoqau`, schema `stripe.*`.

## Available Tables (34 total, key ones listed)

| Table | Key Columns | Notes |
|-------|-------------|-------|
| stripe.charges | id, amount, currency, created, customer, status, payment_intent | Amounts in cents |
| stripe.balance_transactions | id, amount, fee, net, created, source, type | fee field for Stripe fees |
| stripe.refunds | id, amount, created, charge, reason | amount in cents |
| stripe.payouts | id, amount, created, status, arrival_date | DO NOT use for EXTF |
| stripe.customers | id, email, name, created | Customer lookup |
| stripe.subscriptions | id, customer, status, items, current_period_start | Active subs |
| stripe.products | id, name, active | Product catalog |
| stripe.prices | id, product, unit_amount, currency, recurring | Price lookup |
| stripe.invoices | id, customer, amount_due, status, created | Invoice data |
| stripe.checkout_sessions | id, customer, payment_intent, amount_total | Checkout tracking |
| stripe.disputes | id, charge, amount, status, reason | Dispute tracking |

## Common Queries

### Revenue for a Fiscal Year (charges)
```sql
SELECT
  id,
  amount::numeric / 100 as amount_eur,
  to_timestamp(created) as charge_date,
  description,
  customer
FROM stripe.charges
WHERE created >= EXTRACT(EPOCH FROM '2025-01-01'::date)
  AND created < EXTRACT(EPOCH FROM '2026-01-01'::date)
  AND status = 'succeeded'
ORDER BY created;
```

### Fees from Balance Transactions
```sql
SELECT
  source,
  fee::numeric / 100 as fee_eur,
  amount::numeric / 100 as gross_eur,
  net::numeric / 100 as net_eur,
  to_timestamp(created) as txn_date,
  type
FROM stripe.balance_transactions
WHERE created >= EXTRACT(EPOCH FROM '2025-01-01'::date)
  AND created < EXTRACT(EPOCH FROM '2026-01-01'::date)
  AND type = 'charge'
ORDER BY created;
```

### Refunds
```sql
SELECT
  id,
  amount::numeric / 100 as amount_eur,
  to_timestamp(created) as refund_date,
  charge,
  reason
FROM stripe.refunds
WHERE created >= EXTRACT(EPOCH FROM '2025-01-01'::date)
  AND created < EXTRACT(EPOCH FROM '2026-01-01'::date)
ORDER BY created;
```

### Monthly Revenue Summary
```sql
SELECT
  date_trunc('month', to_timestamp(created)) as month,
  COUNT(*) as charge_count,
  SUM(amount::numeric / 100) as gross_revenue
FROM stripe.charges
WHERE status = 'succeeded'
  AND created >= EXTRACT(EPOCH FROM '2025-01-01'::date)
GROUP BY 1
ORDER BY 1;
```

### Customer Lookup by Email
```sql
SELECT c.id, c.email, c.name,
  (SELECT COUNT(*) FROM stripe.charges ch WHERE ch.customer = c.id AND ch.status = 'succeeded') as charge_count,
  (SELECT SUM(ch.amount::numeric / 100) FROM stripe.charges ch WHERE ch.customer = c.id AND ch.status = 'succeeded') as total_revenue
FROM stripe.customers c
WHERE c.email ILIKE '%example@email.com%';
```

### Payouts (for reconciliation only, NOT for EXTF)
```sql
SELECT
  id,
  amount::numeric / 100 as amount_eur,
  to_timestamp(created) as payout_date,
  to_timestamp(arrival_date) as arrival_date,
  status
FROM stripe.payouts
WHERE created >= EXTRACT(EPOCH FROM '2025-01-01'::date)
ORDER BY created;
```

### Payout Reconciliation (by arrival_date)
```sql
-- CRITICAL: Use arrival_date for bank reconciliation, NOT created
SELECT
  date_trunc('month', to_timestamp(arrival_date::bigint))::date as arrival_month,
  SUM(CASE WHEN amount::bigint > 0 THEN amount::numeric / 100 ELSE 0 END) as pos_total,
  SUM(CASE WHEN amount::bigint < 0 THEN amount::numeric / 100 ELSE 0 END) as neg_total,
  SUM(amount::numeric / 100) as net_total
FROM stripe.payouts
WHERE arrival_date::bigint >= EXTRACT(EPOCH FROM '2025-01-01'::date)::bigint
  AND arrival_date::bigint < EXTRACT(EPOCH FROM '2026-01-01'::date)::bigint
  AND status = 'paid'
GROUP BY 1
ORDER BY 1;
```

## Important Notes

1. All amounts in Stripe tables are in **cents** — divide by 100 for EUR.
2. All timestamps are **Unix epoch seconds** — use `to_timestamp()` to convert.
3. The `created` column is stored as BIGINT (epoch), not TIMESTAMPTZ.
4. Always use Supabase SQL instead of direct Stripe API (faster, no rate limits).
5. NEVER create payment links, refunds, or modify subscriptions via these queries.
6. **Payout reconciliation**: DATEV records by bank arrival date. Always use `arrival_date` (not `created`) when comparing to Kontoblatt 1360. Payouts can have negative amounts (Stripe clawbacks).
7. **2025 reconciliation result**: 8/12 months match perfectly by arrival_date. Net discrepancy: +1,429.55 EUR (0.49%), immaterial for EXTF import. Key items: Jun 16 extra 1,130.98 in DATEV, Feb missing -79 debit, Aug/Sep minor timing.
