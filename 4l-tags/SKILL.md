---
name: 4l-tags
description: "4leads Tags auflisten, erstellen und zuweisen (Zuweisung via n8n, nicht REST API)."
user-invocable: false
invocation: /4l-tags
arguments:
  - name: input
    description: >
      "list" zeigt alle Tags, Tag-Name zum Suchen, oder "assign {tag} to {email}"
      für Zuweisung. Ohne Argument: zeigt Tag-Übersicht nach Kategorien.
    required: false
---

# Tag-Management (4leads)

## Tags auflisten

Für die vollständige Tag-Liste: `~/.claude/skills/4leads/references/tags-summary.md`
Für programmatischen Zugriff: `~/.claude/skills/4leads/references/tags-list.json`

### Per API

```bash
source ~/Desktop/.env
# Tags per Internal Web API (schneller, vollständig)
playwright-cli open --browser=chrome --persistent --headed "https://app.4leads.net"
playwright-cli eval "() => fetch('/select/tags').then(r => r.json()).then(d => JSON.stringify(d))"
```

### Tag-Kategorien (Übersicht)

| Kategorie | Anzahl | Top-Tag |
|-----------|--------|---------|
| Newsletter | 1 | Newsletter (7.735) |
| Lead Capture | 1 | Lead: 7-Tage-Challenge (7.487) |
| Webinar Reg. | 9 | zum Webinar registriert (5.274) |
| Webinar Teilnahme | 5 | am Workshop teilgenommen (2.355) |
| Purchase | 8 | BODY GUIDE Kaeufer (633) |
| Subscription | 14 | Abo_39,00EUR_monatlich (74) |
| Connect | 5 | connect-annual (48) |

## Tag erstellen

```bash
source ~/Desktop/.env
curl -s -X POST "https://api.4leads.net/v1/tags" \
  -H "Authorization: Bearer $FOURLEADS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"neuer-tag-name"}'
```

## Tag löschen

```bash
curl -s -X DELETE "https://api.4leads.net/v1/tags/{TAG_ID}" \
  -H "Authorization: Bearer $FOURLEADS_API_KEY"
```

## Tag zuweisen (NUR per n8n!)

Die REST API Tag-Zuweisung (`PUT /contacts/{id}/tags/{tag_id}`) gibt HTTP 200 zurück,
aber der Tag wird NICHT dauerhaft gespeichert. Das ist ein bekannter Bug.

Zuverlässige Methode: n8n fleads Node (Credential: PzZd7uq7Kum2G6zQ)

```js
// n8n Node Config für Tag-Zuweisung
{
  resource: "contact",
  operation: "addATag",
  contactId: { __rl: true, value: "={{$('Node').item.json.data.id}}", mode: "id" },
  bListOfTags: true,
  contactTagIdList: "={{ [TAG_ID] }}"
}
```

## Tag entfernen (REST API funktioniert hier)

```bash
curl -s -X DELETE "https://api.4leads.net/v1/contacts/{CONTACT_ID}/tags/{TAG_ID}" \
  -H "Authorization: Bearer $FOURLEADS_API_KEY"
```
