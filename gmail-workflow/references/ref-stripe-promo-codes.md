# Stripe Promo Code Lookup

## Wann laden
- Kunde fragt nach Gutscheincode
- Template-Variable-Bug mit Gutscheincode-Platzhalter
- Promo-Kampagne validieren (z.B. Connect Bonus-Woche)

## API Pattern

```bash
STRIPE_KEY=$(grep '^STRIPE_API_KEY=' ~/Desktop/.env | cut -d= -f2)

# Alle Promo-Codes für einen Coupon auflisten
curl -s "https://api.stripe.com/v1/promotion_codes?coupon={COUPON_ID}&limit=100" \
  -u "$STRIPE_KEY:"

# Einzelnen Promo-Code per Code suchen
curl -s "https://api.stripe.com/v1/promotion_codes?code={CODE}&limit=1" \
  -u "$STRIPE_KEY:"

# Neuen Promo-Code erstellen (für einzelnen Kunden)
curl -s -X POST "https://api.stripe.com/v1/promotion_codes" \
  -u "$STRIPE_KEY:" \
  -d "coupon={COUPON_ID}" \
  -d "code={UNIQUE_CODE}" \
  -d "max_redemptions=1" \
  -d "metadata[customer_email]={EMAIL}"
```

## Bekannte Coupons

| Coupon ID | Name | Rabatt | Verwendung |
|-----------|------|--------|------------|
| `bEsGn8vr` | SY3-BodyGuide-Bonus | 100% off | Connect-Käufer bekommen kostenlosen BodyGuide |

## Promo-Code-Zuordnung

Promo-Codes werden per Kunde erstellt. Die Zuordnung läuft über `metadata.customer_email` im Promo-Code-Objekt. Lookup-Pattern:

```python
import json, sys
data = json.load(sys.stdin)
for p in data['data']:
    email = p.get('metadata', {}).get('customer_email', 'N/A')
    print(f"{p['code']} -> {email} (active: {p['active']})")
```

## Kampagnen-Validierung

Bei zeitlich begrenzten Kampagnen (z.B. Connect Promo-Woche 2.-9. März):
1. Kaufdatum des Kunden prüfen: `charges` API mit Kunden-ID
2. Prüfen ob `charge.created` innerhalb des Kampagnen-Fensters liegt
3. Nur bei Match den Code herausgeben oder erstellen
4. Kein Code für Käufe außerhalb des Fensters

## E-Mail-Mismatch

Kunden schreiben oft von einer anderen E-Mail als ihrer Stripe-E-Mail. Bei Promo-Code-Lookup:
1. Zuerst nach Absender-E-Mail suchen
2. Dann nach häufigen Variationen (gmail/gmx/web.de)
3. `metadata.customer_email` ist die Stripe-Kauf-E-Mail, nicht die Kontakt-E-Mail

## Template-Bug Recovery

Wenn 4leads/n8n eine E-Mail mit `{{connect_bodyguide_gutscheincode}}` (oder ähnlichen Platzhaltern) verschickt hat:
1. Coupon-ID identifizieren (meist `bEsGn8vr` für BodyGuide-Bonus)
2. Promo-Codes für diesen Coupon abrufen
3. Per `metadata.customer_email` den richtigen Code finden
4. Falls kein Code existiert: neuen erstellen
5. Dem Kunden den Code direkt senden, OHNE den Fehler zu erwähnen
