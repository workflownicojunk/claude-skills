---
name: 4l-contact
description: "4leads Kontakte suchen, erstellen und Custom Fields setzen via REST API."
user-invocable: false
invocation: /4l-contact
arguments:
  - name: input
    description: >
      E-Mail-Adresse, Name, oder Kontakt-Hash. Ohne Argument: erklärt die verfügbaren
      Operationen (suchen, erstellen, Feld setzen).
    required: false
---

# Kontakt-Management (4leads REST API)

```bash
source ~/Desktop/.env
BASE=https://api.4leads.net/v1
AUTH="Authorization: Bearer $FOURLEADS_API_KEY"
```

## Kontakt suchen (per E-Mail)

```bash
curl -s -X POST "$BASE/contacts/search" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"email":"kunde@example.de"}'
# ACHTUNG: Returns HTTP 201, nicht 200!
```

## Kontakt erstellen/aktualisieren (Upsert)

```bash
curl -s -X POST "$BASE/contacts" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"email":"kunde@example.de", "fname":"Vorname", "lname":"Nachname"}'
```

## Custom Field setzen

```bash
curl -s -X PUT "$BASE/contacts/{CONTACT_ID}/global-field-values/{FIELD_ID}" \
  -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"value":"WERT"}'
```

Feld-IDs: lies `~/.claude/skills/4leads/references/contact-schema.json`

Wichtige Custom Fields:
| Feld | ID |
|------|-----|
| connect_promo_monatlich | 15301 |
| connect_fenster_ablauf | 15302 |
| connect_promo_jaehrlich | 15303 |
| connect_fenster_ablauf_text | 15305 |
| connect_bodyguide_gutscheincode | 15306 |

## Kontakt in der UI anzeigen

```bash
playwright-cli open --browser=chrome --persistent --headed "https://app.4leads.net/contacts"
# Suchfeld nutzen, oder direkt per Hash:
playwright-cli goto "https://app.4leads.net/contacts/details/c/{CONTACT_HASH}"
```

## Rate Limiting

- 1 Call pro 1,5 Sekunden
- Bei HTTP 429: `sleep 3` und retry
