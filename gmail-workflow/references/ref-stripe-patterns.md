# Stripe API Patterns (via Supabase)

## Auth

```bash
STRIPE_KEY=$(grep '^STRIPE_API_KEY=' ~/Desktop/.env | cut -d= -f2)
SUPABASE_URL=$(grep '^SUPABASE_URL=' ~/Desktop/.env | cut -d= -f2)
SUPABASE_KEY=$(grep '^SUPABASE_SERVICE_ROLE_KEY=' ~/Desktop/.env | cut -d= -f2)
```

WICHTIG: `STRIPE_API_KEY` (nicht STRIPE_SECRET_KEY). Immer `grep '^STRIPE_API_KEY='` verwenden.

## Bulk-Validierung (BEVORZUGT: ein Query für alle E-Mails)

```bash
# Supabase PostgREST mit stripe-Schema
# Für mehrere Kunden auf einmal
curl -s -X POST "$SUPABASE_URL/rest/v1/rpc/query" \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -H "Content-Profile: stripe" \
  -d '{"query":"SELECT ... WHERE LOWER(c.email) IN (''email1@de'',''email2@de'')"}'
```

Wenn RPC nicht funktioniert: Direktes SQL über execute_sql oder einzelne Customer-Queries.

## Einzelner Kunde (wenn Bulk nicht möglich)

```sql
-- Kunde suchen
SELECT c.id, c.email, c.name FROM stripe.customers c WHERE LOWER(c.email) = LOWER('email@de') LIMIT 1;

-- Aktive Subscriptions (ACHTUNG: s.customer, NICHT s.customer_id)
SELECT s.id, s.status, s.plan::json->>'product' as product_id,
       (s.plan::json->>'amount')::int/100.0 as price_eur,
       s.plan::json->>'interval' as interval,
       s.metadata->>'is_installment' as is_installment,
       s.metadata->>'total_installments' as total_installments
FROM stripe.subscriptions s
JOIN stripe.customers c ON c.id = s.customer
WHERE LOWER(c.email) = LOWER('email@de') AND s.status IN ('active','past_due','trialing')
ORDER BY s.created DESC;

-- Letzte Zahlungen
SELECT ch.amount/100.0 as amount_eur, ch.status, to_timestamp(ch.created) as datum
FROM stripe.charges ch
JOIN stripe.customers c ON c.id = ch.customer
WHERE LOWER(c.email) = LOWER('email@de') AND ch.status = 'succeeded'
AND ch.created > extract(epoch from NOW() - INTERVAL '90 days')
ORDER BY ch.created DESC LIMIT 5;
```

## Produkt-Typ-Erkennung

| Preis | Interval | Metadata | Typ |
|-------|----------|----------|-----|
| 27/97/497 EUR | einmalig | - | TYPE_A |
| 97/179/189/349 EUR | monatlich | is_installment=true | TYPE_B |
| 39/59/69 EUR | monatlich | - | TYPE_C_MONTHLY |
| 299/390/468 EUR | jährlich | - | TYPE_C_YEARLY |

## Refund ausführen

```bash
# Doppelabbuchung oder berechtigte Erstattung
curl -s -X POST "https://api.stripe.com/v1/refunds" \
  -u "$STRIPE_KEY:" \
  -d "charge=CHARGE_ID"
```

## Subscription kündigen (TYPE_C_MONTHLY)

```bash
# Zum Laufzeitende (nicht sofort)
curl -s -X POST "https://api.stripe.com/v1/subscriptions/SUB_ID" \
  -u "$STRIPE_KEY:" \
  -d "cancel_at_period_end=true"
```

## Promo Code Lookup

```bash
# Alle Codes für einen Coupon
curl -s "https://api.stripe.com/v1/promotion_codes?coupon=bEsGn8vr&limit=100" \
  -u "$STRIPE_KEY:" | python3 -c "import json,sys; [print(p['code'], p.get('metadata',{}).get('customer_email','')) for p in json.load(sys.stdin)['data']]"
```

Bekannte Coupons:
- `bEsGn8vr`: SY3-BodyGuide-Bonus (100% off BodyGuide)

## Supabase Schema

Projekt: `dajxbqfiugzigrnsoqau`, Schema: `stripe.*`
Tables: `customers`, `subscriptions`, `charges`, `refunds`, `invoices`
