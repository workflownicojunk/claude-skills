---
name: crm-sync
description: >
  Unified CRM synchronization across Stripe, Circle, and 4leads for Lightness Fitness / StrongerYou.
  Stripe is the single source of truth for subscriptions. Circle and 4leads must mirror Stripe.
  Use when syncing subscription data across systems, assigning/removing tags based on Stripe status,
  setting custom fields (Stripe Customer ID, Circle Member ID), cleaning up stale tags,
  resolving email mismatches between systems, or auditing cross-system consistency.
  Triggers: CRM sync, tag sync, subscription sync, Stripe mirror, Circle tags, 4leads tags,
  cross-system audit, entity matching, customer 360, unified CRM, tag cleanup, custom field sync,
  "synchronisieren", "abgleichen", "Tags aufräumen", "Stripe spiegeln".
  Replaces: 4leads-expert (API section), 4leads-contacts (tag/field ops), circle-community (tag/member ops).
---

# CRM Sync: Stripe -> Circle + 4leads

Stripe is the single source of truth. Circle and 4leads must mirror active subscriptions exactly.

## Architecture

```
Stripe (Truth)
  |
  ├── Circle (Community Platform)
  |   ├── Member Tags: connect-monthly, connect-annual, connect-monthly-legacy, connect-annual-legacy
  |   └── Profile Fields: stripe_customer_id, stripe_subscription_id, stripe_email, subscription_price, subscription_interval
  |
  └── 4leads (Email CRM)
      ├── Contact Tags: connect-monthly (#43466), connect-annual (#43467), connect-monthly-legacy (#43468), connect-annual-legacy (#43469)
      └── Custom Fields: Stripe Customer ID (#15219), Circle Member ID (TBD)
```

## Workflow

1. **Build Stripe truth:** Read `references/price-tag-mapping.json`, then fetch all active subscriptions via Stripe SDK
2. **Match entities:** Email-based matching first. For mismatches, read `references/email-mismatches.json` (11 known cases). Then fuzzy name match (SequenceMatcher > 0.7). Finally Gmail search for remaining.
3. **Sync Circle:** Read `references/circle-api.md`. Tags via PUT member_tag_ids (merge!). Profile fields via custom_profile_field_values.
4. **Sync 4leads:** Tags ONLY via n8n Webhook `4leads-tag-single` (Workflow sogXm8e5FB8qjKp1). Custom fields via REST PUT global-field-values.
5. **Validate:** Compare tag counts across all 3 systems
6. **Report:** List unmatched subscribers and discrepancies

## n8n Workflows

| Workflow | ID | Zweck | Status |
|----------|-----|-------|--------|
| 4leads Single Contact Tag + Field | sogXm8e5FB8qjKp1 | Tag + Stripe CID (CF 15219) + BodyGuide Code (CF 15306) via fleads Node | Aktiv |
| Connect Purchase -> BodyGuide Bonus | SBQlqibf7jzkFInX | Stripe Checkout -> Promo Code erstellen -> 4leads CF 15306 setzen | Aktiv |
| Connect Upgrade: Monats->Jahr | 1h0chLogGxQi6uG1 | Webhook: cancel_at_period_end auf True setzen (Downgrade-Schutz) | Aktiv |
| Webhook URL | `https://n8n.srv805917.hstgr.cloud/webhook/4leads-tag-single` | POST {email, tag_id, customer_id, promo_code} |

Der n8n fleads Node-Typ ist `n8n-nodes-4leads.fleads` (Community-Node, NICHT n8n-nodes-base).
Credential: `PzZd7uq7Kum2G6zQ` ("4leads")

**Bulk CF-Set Pattern** (für Retro-Batches):
```python
# Rufe Webhook für jeden Kontakt auf, setze tag_id=43467 (dummy) + promo_code
payload = {"email": "x@y.de", "tag_id": 43467, "customer_id": "", "promo_code": "CODE-BG-2026"}
requests.post("https://n8n.srv805917.hstgr.cloud/webhook/4leads-tag-single", json=payload)
```

## Quick Reference: API Endpoints

### Stripe (Python SDK)
```python
import stripe
stripe.api_key = STRIPE_API_KEY
# Fetch all active subs with customer email in one call
result = stripe.Subscription.list(status='active', limit=100, expand=['data.customer'])
```

### Circle Admin API V2
```bash
BASE="https://app.circle.so/api/admin/v2"
AUTH="Authorization: Token $CIRCLE_ADMIN_API_KEY"
CID=346419

# Get members (paginated)
GET $BASE/community_members?community_id=$CID&per_page=100&page=N

# Assign tags (MERGE! Get existing first, then send all)
PUT $BASE/community_members/{id}  {"community_id":346419,"member_tag_ids":[id1,id2,...]}

# Set profile fields
PUT $BASE/community_members/{id}  {"community_id":346419,"custom_profile_field_values":{"stripe_customer_id":"cus_xxx"}}

# Create tag (display_format required!)
POST $BASE/member_tags  {"community_id":346419,"name":"tag-name","display_format":"label"}

# Delete tag
DELETE $BASE/member_tags/{id}?community_id=346419
```

### 4leads REST API
```bash
BASE="https://api.4leads.net/v1"
AUTH="Authorization: Bearer $FOURLEADS_API_KEY"

# Search contact (returns HTTP 201, not 200!)
POST $BASE/contacts/search  {"email":"x@y.de"}  -> {data:{id:...}}

# Set custom field (ONLY PUT, path includes field_id!)
PUT $BASE/contacts/{id}/global-field-values/{field_id}  {"value":"..."}
```

**TAG-ZUWEISUNG: NUR via n8n fleads Node!**
Die REST API (`PUT /contacts/{id}/tags/{tag_id}`) gibt 200 zurück, persistiert den Tag aber NICHT.
Verifiziert am 2026-03-06: Mehrfach getestet, Tag erscheint nie im Kontakt.
Nutze stattdessen den n8n fleads Node (Credential: PzZd7uq7Kum2G6zQ):
```js
{ resource: "contact", operation: "addATag",
  contactId: {__rl: true, value: "={{id}}", mode: "id"},
  bListOfTags: true, contactTagIdList: "={{ [TAG_ID] }}" }
```

## Supabase Schema (Projekt dajxbqfiugzigrnsoqau, Schema: crm)

| Tabelle | Inhalt |
|---------|--------|
| contacts | 246 Kontakte: email_normalized, stripe_customer_id, circle_member_id, fourleads_contact_id |
| sync_state | Erwartete Tags + aktive Sub-IDs pro Kontakt |
| sync_log | Audit-Trail aller Sync-Operationen |
| sync_runs | Status der Sync-Runs (run_id, status, counts) |
| product_mapping | 33 Stripe-Preise -> Circle/4leads Tag-IDs |
| email_mismatches | 11 bekannte Email-Abweichungen zwischen Systemen |
| unmatched | 5 Kontakte ohne Match (Viktor Neumann, Michael Engelbrecht, etc.) |
| lifecycle_events | Subscription-Änderungen (Upgrade/Downgrade) |

Views: `v_active_subscriptions`, `v_discrepancies`, `v_funnel_overview`

Supabase PostgREST: `Content-Profile: crm` Header für Schema-Zugriff erforderlich.

## Critical Gotchas

These are hard-won lessons. A simpler model MUST know these to avoid wasting hours:

1. **Circle `member_tag_ids` vs `tag_ids`:** Only `member_tag_ids` works for tag assignment. `tag_ids` and `add_tag_ids` are silently ignored. Always GET existing tags first, merge, then PUT.

2. **Circle tag creation requires `display_format`:** Without `{"display_format":"label"}` the API returns 422.

3. **Circle V1 API is dead:** `api.circle.so/api/v1/` returns HTML. Only V2 works: `app.circle.so/api/admin/v2/`

4. **4leads search returns 201:** `POST /contacts/search` returns HTTP 201 with `{data:{...}}`. This is normal, not an error.

5. **4leads tag assignment via REST API does NOT work:** `PUT /contacts/{id}/tags/{tag_id}` returns 200 but does NOT persist. The tag never appears on the contact. Use the n8n fleads Node instead.

6. **4leads custom fields via REST API:** `PUT /contacts/{id}/custom-fields` mit `{"15306": "WERT"}` gibt `success: true` zurück aber Custom Field-Werte sind NICHT über REST GET abrufbar. Setzen funktioniert nur sicher via n8n fleads Node.

7. **.env loading:** `source ~/Desktop/.env` does not reliably load all keys. Always use:
   ```bash
   KEY=$(grep '^VARIABLE=' ~/Desktop/.env | cut -d= -f2)
   ```

8. **Rate limits:** 4leads = 1 call/1.5s (sleep 3 on 429). Circle = 60 req/min (sleep 1.1 between calls).

9. **Circle Auth:** Use `Token` prefix, NOT `Bearer`. Header: `Authorization: Token $CIRCLE_ADMIN_API_KEY`

10. **Circle per_page:** Max `per_page=20` (100 gibt 403 Forbidden). `member_tag_id` Filter in GET /community_members funktioniert NICHT.

11. **Python urllib User-Agent:** Circle API blockt Default Python User-Agent mit 403. Immer `User-Agent: CRM-Sync/1.0` setzen.

12. **n8n Webhook Aktivierung:** `POST /api/v1/workflows/{id}/activate` (nicht PATCH/PUT). Webhook-Endpunkt: `/webhook/{path}` (Production), `/webhook-test/{path}` (Test, nur mit offenem Canvas).

## Reference Files

| File | Content | When to load |
|------|---------|--------------|
| `references/price-tag-mapping.json` | 14 Stripe prices -> 4 tag categories | At sync start |
| `references/circle-api.md` | Full Circle V2 API reference with examples | When working with Circle |
| `references/fourleads-api.md` | Full 4leads REST API reference with examples | When working with 4leads |
| `references/tag-ids.json` | All tag IDs across Circle and 4leads | When assigning/removing tags |
| `references/field-ids.json` | Custom field IDs for both systems | When setting fields |
| `references/email-mismatches.json` | 11 known Stripe!=Circle email pairs + 4 truly unmatched | When matching fails |
| `references/circle-workflows.md` | Alle 22 Circle Workflows, Trigger-Optionen, Actions, Tags mit Counts | Vor Sync-Design-Entscheidungen |
| `references/fourleads-automations.md` | 16 4leads Automationen, 11 Follow-Ups, Connect-Automation jdkm Struktur | Vor Sync-Design-Entscheidungen |

## Validation Checklist

After any sync operation, verify:

- [ ] Sum of connect-* tag counts in Circle = number of matched Stripe subscribers
- [ ] Sum of connect-* tag counts in 4leads = number of matched Stripe subscribers
- [ ] No Circle member has connect-* tag without active Stripe subscription
- [ ] Every 4leads contact with connect-* tag has Stripe Customer ID field set
- [ ] Unmatched subscribers (different email in Stripe vs Circle) are documented

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
