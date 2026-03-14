# 4leads REST API — Vollständige Referenz

**Base URL:** `https://api.4leads.net/v1`
**Auth:** `Authorization: Bearer $FOURLEADS_API_KEY` (Format: `4l.xxx`)
**Content-Type:** `application/json`
**Rate Limit:** 1 Call/1.5s, bei 429 → sleep(3) + retry

**Response-Wrapper (immer):**
```json
{"data": {...}, "errors": [], "success": true}
```
Bei Fehler: `{"errors": {"input-error": "Meldung"}, "success": false}` oder `{"errors": [], "success": false, "message": "record not found"}`

**Pagination-Response:**
```json
{"data": {"totalResults": 28876, "pageSize": 25, "pageNum": 0, "totalPages": 1155, "results": [...]}}
```

---

## 1. Contacts

### GET /contacts — Liste alle Kontakte

```
GET /contacts?pageSize=25&pageNum=0&searchString=&mode=&status=
```

| Parameter | Typ | Beschreibung |
|-----------|-----|-------------|
| pageSize | int | Max Ergebnisse pro Seite (default: 25) |
| pageNum | int | Seitennummer, 0-basiert |
| searchString | string | Freitext-Suche (email, fname, lname) |
| mode | int | `1` = nur IDs zurückgeben (schneller) |
| status | string | Filter: `active` o.ä. (hat keinen Effekt in Tests) |

**Response (mode=0, default):** Array mit vollständigen Contact-Objekten
**Response (mode=1):** Array mit nur IDs `[3524595, 3524592, ...]`

**Contact-Objekt:**
```json
{
  "id": 3524595,
  "status_email": 2,        // 0=unbekannt, 1=optout, 2=optin, 3=bounce, 4=spam
  "email_verify": 100,      // Verifikations-Score 0-100
  "status_sms": null,
  "email": "katja@example.de",
  "salutation": "f",        // "f"=weiblich, "m"=männlich, null=unbekannt
  "fname": "Katja",
  "lname": null,
  "company": null,
  "fax": null,
  "street": null,
  "streetNumber": null,
  "zip": null,
  "city": null,
  "country": null,
  "website": null,
  "skype": null,
  "companyPosition": null,
  "optinDate": "2026-03-10 23:19:52",
  "optoutDate": null,
  "bounceDate": null,
  "spamReportDate": null,
  "updatedAt": "2026-03-10 23:19:52",
  "privatePhone": null,
  "mobilePhone": null,
  "birthday": null,
  "createdAt": "2026-03-10 23:19:52"
}
```

---

### GET /contacts/{id} — Einzelner Kontakt

```
GET /contacts/3524595
```

**Response:** `{"data": {Contact-Objekt}, "errors": [], "success": true}`

---

### POST /contacts — Kontakt erstellen / upsert

```
POST /contacts
Body: {"email": "x@y.de", "fname": "Name", "salutation": "f"}
```

Wenn E-Mail bereits existiert: **Update** (kein Fehler, kein 409). Gibt immer den Kontakt zurück.

**Alle Felder (optional außer email):**
`email`, `salutation`, `fname`, `lname`, `company`, `fax`, `street`, `streetNumber`, `zip`, `city`, `country`, `website`, `skype`, `companyPosition`, `optinDate`, `optoutDate`, `bounceDate`, `bounceState`, `privatePhone`, `mobilePhone`, `birthday`

**Response:** `{"data": {Contact-Objekt}, "errors": [], "success": true}` (HTTP 201 bei Neu, 200 bei Update)

---

### PUT /contacts/{id} — Kontakt aktualisieren

```
PUT /contacts/3524595
Body: {"fname": "Neuname", "city": "Berlin"}
```

**Response:** `{"data": {Contact-Objekt}, "errors": [], "success": true}`

---

### DELETE /contacts/{id} — Kontakt löschen

```
DELETE /contacts/3524595
```

**Response:** `{"data": {}, "errors": [], "success": true}` (HTTP 200)

---

### POST /contacts/search — Kontakt per E-Mail suchen

```
POST /contacts/search
Body: {"email": "katja@example.de"}
```

**Response:** `{"data": {Contact-Objekt}, "errors": [], "success": true}` (HTTP 201!)
Wenn nicht gefunden: `{"errors": {...}, "success": false}`

> WICHTIG: Search gibt HTTP 201 zurück, nicht 200. Prüfe immer `success`, nicht den HTTP-Status.

---

### POST /contacts/{id}/opt-out — Kontakt abmelden

```
POST /contacts/3524595/opt-out
Body: {} (leer)
```

**Response:** `{"data": {}, "errors": [], "success": true}`
Wenn nicht gefunden: HTTP 404, `success: false, message: "record not found"`

---

## 2. Contact Tags

### GET /contacts/{id}/getTagList — Tags eines Kontakts

```
GET /contacts/3524595/getTagList
```

**Response:**
```json
{
  "data": [
    {
      "id": 42997,
      "name": "Lead: 7-Tage-Challenge",
      "description": "",
      "color": "green",
      "updatedAt": "2025-11-28 23:36:01",
      "createdAt": "2025-11-12 16:18:58",
      "connectedAt": "2026-03-10 23:19:52"  // Wann dem Kontakt zugewiesen
    }
  ],
  "errors": [], "success": true
}
```

---

### GET /contacts/{id}/getFieldList — Custom Fields eines Kontakts

```
GET /contacts/3524595/getFieldList
```

**Response:**
```json
{
  "data": [
    {
      "id": 15306,
      "status": 1,
      "name": "connect_bodyguide_gutscheincode",
      "fieldTypeId": "text",
      "priority": null,
      "createdAt": "...",
      "updatedAt": "...",
      "_value": "CODE123"   // Aktueller Wert für diesen Kontakt
    }
  ],
  "errors": [], "success": true
}
```

Wenn keine Custom Fields gesetzt: `{"data": [], ...}` (leeres Array)

---

### POST /contacts/{id}/addTag — Einzelnen Tag hinzufügen

```
POST /contacts/3524595/addTag
Body: {"tagId": 42997}
```

**Response:** `{"errors": [], "success": true}`
Wenn tagId invalid: `{"errors": {"input-error": "no valid tagId Paramter"}, "success": false}`

> BEKANNTES PROBLEM: REST API addTag gibt `success: true` zurück, aber der Tag wird in der UI manchmal nicht gespeichert. Für produktive Nutzung n8n fleads Node verwenden (Credential: PzZd7uq7Kum2G6zQ).

---

### POST /contacts/{id}/addTagList — Mehrere Tags hinzufügen

```
POST /contacts/3524595/addTagList
Body: {"tagIds": [42997, 42824]}
```

Max. 20 Tags pro Call.
**Response:** `{"errors": [], "success": true}`

---

### POST /contacts/{id}/removeTag — Einzelnen Tag entfernen

```
POST /contacts/3524595/removeTag
Body: {"tagId": 42997}
```

**Response:** `{"errors": [], "success": true}`

---

### POST /contacts/{id}/removeTagList — Mehrere Tags entfernen

```
POST /contacts/3524595/removeTagList
Body: {"tagIds": [42997, 42824]}
```

**Response:** `{"errors": [], "success": true}`

---

## 3. Tags

### GET /tags — Alle Tags

```
GET /tags?pageSize=25&pageNum=0&searchString=newsletter
```

**Tag-Objekt:**
```json
{
  "id": 42997,
  "name": "Lead: 7-Tage-Challenge",
  "description": "",
  "color": "green",     // null oder Farbstring
  "updatedAt": "2025-11-28 23:36:01",
  "createdAt": "2025-11-12 16:18:58"
}
```

---

### GET /tags/{id} — Einzelner Tag

```
GET /tags/42997
```

---

### POST /tags — Tag erstellen

```
POST /tags
Body: {"name": "neuer-tag-name"}
```

**Response:** `{"data": {Tag-Objekt}, "errors": [], "success": true}` (HTTP 201)

---

### PUT /tags/{id} — Tag umbenennen

```
PUT /tags/42997
Body: {"name": "neuer-name"}
```

---

### DELETE /tags/{id} — Tag löschen

```
DELETE /tags/42997
```

---

## 4. GlobalFields (Custom Contact Fields)

### GET /globalFields — Alle Custom Fields

```
GET /globalFields?pageSize=25&pageNum=0&searchString=connect
```

**GlobalField-Objekt:**
```json
{
  "id": 15306,
  "status": 1,
  "name": "connect_bodyguide_gutscheincode",
  "placeholder": "",
  "config": {},          // Kann Items für Select-Felder enthalten
  "fieldTypeId": "text", // "text", "number", "date", "select", "checkbox" etc.
  "priority": null,      // Anzeigereihenfolge
  "lockedValue": 0,      // 1 = Wert kann nicht überschrieben werden
  "personalData": 0,     // 1 = DSGVO-relevant
  "createdAt": "2026-03-05 04:08:58",
  "updatedAt": "2026-03-05 04:08:58"
}
```

**Alle 26 bekannten Custom Fields** → `references/contact-schema.json`

---

### POST /globalFields — Custom Field erstellen

```
POST /globalFields
Body: {
  "name": "feldname",
  "priority": 10,
  "fieldTypeId": "text",
  "config": {}          // Optional: {"items": [...], "preselect": ..., "rowNum": ...}
}
```

---

### PUT /globalFields/{id} — Custom Field aktualisieren

```
PUT /globalFields/15306
Body: {"name": "neuer-name", "priority": 5}
```

---

### DELETE /globalFields/{id}

```
DELETE /globalFields/15306
```

---

### GET /globalFields/{id}/getValue — Wert eines Felds für Kontakt lesen

```
GET /globalFields/15306/getValue?contactId=3524595
```

**Response:** `{"data": {"value": "CODE123"}, "errors": [], "success": true}`
Wenn kein Wert gesetzt: `{"data": {"value": ""}, ...}`

---

### POST /globalFields/{id}/setValue — Wert setzen

```
POST /globalFields/15306/setValue
Body: {
  "contactId": 3524595,
  "value": "NEUER-CODE",
  "doTriggers": true,   // Optional, default true — löst Automations aus
  "overwrite": true     // Optional, default true — überschreibt bestehenden Wert
}
```

**Response:** `{"errors": [], "success": true}`
Wenn contactId nicht gefunden: `{"errors": [], "success": false, "message": "record not found"}`

---

### POST /globalFields/setFieldList — Mehrere Felder auf einmal setzen

```
POST /globalFields/setFieldList
Body: {
  "contactId": 3524595,
  "fields": [
    {
      "globalFieldId": 15306,
      "value": "CODE123",
      "doTriggers": true,
      "overwrite": true
    },
    {
      "globalFieldId": 15301,
      "value": "PROMO-CODE",
      "doTriggers": false,
      "overwrite": true
    }
  ]
}
```

Max. 20 Felder pro Call.
**Response:** `{"errors": [], "success": true}`

---

## 5. Campaigns (Follow-Up Funnels / Automationen)

> HINWEIS: "Campaigns" in der API = Follow-Up Funnels in der 4leads-UI, NICHT die Newsletter-Kampagnen.

### GET /campaigns — Alle Campaigns

```
GET /campaigns?pageSize=25&pageNum=0&searchString=&mode=
```

**Campaign-Objekt:**
```json
{
  "id": 46382,
  "publicKey": "cvx2wbsIFKd3lz60OjKFVyw9uOb349zn78sY6QN1",
  "status": 1,
  "updatedAt": "2026-02-04 02:43:08",
  "visible": 0,
  "optinEmailId": null,
  "emailFunnelId": null,
  "singleOptin": 1,         // 1 = Single Opt-in
  "optinCaseBlock": null,
  "adminWatch": null,
  "hasWebinarRegister": 1,
  "processId": null,
  "optinUrl": null,
  "thxUrl": "https://nicolstanzel.com/dankesseite",
  "name": "StrongerYou Launch Workshop",
  "createdAt": "2025-10-10 11:42:56",
  "autoresponderId": 16
}
```

**Bekannte Campaign-IDs (Lightness Fitness):**
| ID | Name |
|----|------|
| 46382 | StrongerYou Launch Workshop |
| 46383 | StrongerYou 3.0 Launch Workshop Webinarjam |
| 46403 | StrongerYou 3.0 Launch Workshop 2 Everwebinar |

---

### GET /campaigns/{id} — Einzelne Campaign

```
GET /campaigns/46382
```

---

### DELETE /campaigns/{id}

```
DELETE /campaigns/46382
```

---

### POST /campaigns/{id}/start — Kontakt in Campaign einschreiben

```
POST /campaigns/46382/start
Body: {"contactId": 3524595}
```

**Response:** `{"errors": [], "success": true}`
Wenn contactId-Parameter fehlt/invalid: `{"errors": {"input-error": "no valid contactId Paramter"}, "success": false}`

---

### POST /campaigns/{id}/stop — Kontakt aus Campaign austragen

```
POST /campaigns/46382/stop
Body: {"contactId": 3524595}
```

**Response:** `{"errors": [], "success": true}`

---

## 6. Opt-In Cases

### GET /opt-in-cases — Alle Opt-In-Kategorien

```
GET /opt-in-cases?pageSize=25&pageNum=0
```

**Opt-In-Case-Objekt:**
```json
{
  "id": 39171,
  "name": "Nachrichten von Nicol Stanzel (Standard)",
  "publicName": "Nachrichten von Nicol Stanzel",
  "publicDescription": "Nachrichten zu diesem Thema können...",
  "isDefault": 1,        // 1 = Standard-Opt-In-Kategorie
  "canPause": null,
  "pauseDuration": null,
  "pauseType": null,
  "createdAt": "2025-10-06 15:48:38",
  "updatedAt": "2025-10-06 15:48:38"
}
```

**Bekannte Opt-In-Case-IDs:**
| ID | Name |
|----|------|
| 39171 | Nachrichten von Nicol Stanzel (Standard) |

---

### POST /opt-in-cases/{id}/grant — Opt-In gewähren

```
POST /opt-in-cases/39171/grant
Body: {"contactId": 3524595, "ip": "1.2.3.4"}  // ip optional
```

**Response:** `{"errors": [], "success": true}`
Wenn contactId fehlt: `{"errors": {"input-error": "mandatory field missing"}, "success": false}`

---

### POST /opt-in-cases/{id}/revoke — Opt-In widerrufen

```
POST /opt-in-cases/39171/revoke
Body: {"contactId": 3524595, "ip": "1.2.3.4"}  // ip optional
```

**Response:** `{"errors": [], "success": true}`

---

## 7. Opt-Ins (Double Opt-In E-Mails)

### GET /opt-ins — Alle DOI-E-Mails

```
GET /opt-ins?pageSize=25&pageNum=0&mode=&searchString=
```

**Kein Daten im Account vorhanden** (singleOptin-Konfiguration, kein DOI genutzt).

---

### DELETE /opt-ins/{id}

### POST /opt-ins/{id}/send — DOI-E-Mail senden

```
POST /opt-ins/123/send
Body: {"contactId": 3524595, "redo": 0}  // redo optional, 1=nochmal senden
```

---

## 8. Storage / Storage Values

> HINWEIS: Storage-Endpunkte sind leer / nicht genutzt im Lightness-Fitness-Account. Wahrscheinlich ein älteres Feature, ersetzt durch GlobalFields.

### GET /storage — Alle Storage Fields
### POST /storage — Storage Field erstellen
### PUT /storage/{id} — Aktualisieren
### DELETE /storage/{id} — Löschen
### GET /storage-values — Alle Werte
### POST /storage-values — Werte setzen

```
POST /storage-values
Body: {
  "fields": [{"key": "feldname", "value": "wert"}],
  "options": {"overwrite": true}
}
```

---

## Wichtige Learnings & Gotchas

### Tag-Assignment-Bug
`POST /contacts/{id}/addTag` und `addTagList` geben `success: true` zurück, persistieren den Tag aber manchmal NICHT. Für produktive Nutzung immer **n8n fleads Node** verwenden (Credential: `PzZd7uq7Kum2G6zQ`).

### HTTP-Status-Anomalie bei /contacts/search
`POST /contacts/search` gibt HTTP 201 zurück (nicht 200). Prüfe `success`-Flag, nicht den HTTP-Status.

### Error-Response-Formate (zwei Varianten)
```json
// Variante 1: Validierungsfehler
{"errors": {"input-error": "no valid tagId Paramter"}, "success": false}

// Variante 2: Nicht gefunden
{"errors": [], "success": false, "message": "record not found"}
```

### Campaigns vs. Newsletter
- `GET /campaigns` = Follow-Up Funnels (Autoresponder-Sequenzen), NICHT Newsletter-Broadcasts
- Newsletter-Kampagnen haben keinen REST-API-Endpoint, nur über Internal Web API zugänglich

### doTriggers-Flag
Bei `setValue` und `setFieldList`: `"doTriggers": false` verhindert, dass Automations ausgelöst werden. Immer explizit setzen für kontrolliertes Verhalten.

### Pflicht-Felder
- `POST /contacts`: nur `email` ist Pflicht
- `POST /contacts/{id}/addTag`: `tagId` als int im Body
- `POST /campaigns/{id}/start`: `contactId` als int im Body
- `POST /opt-in-cases/{id}/grant`: `contactId` als int im Body

---

## Python-Schnellstart

```python
import requests
import os

API_KEY = os.environ["FOURLEADS_API_KEY"]
BASE = "https://api.4leads.net/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def api(method, path, **kwargs):
    r = requests.request(method, f"{BASE}{path}", headers=HEADERS, **kwargs)
    return r.json()

# Kontakt per E-Mail suchen
contact = api("POST", "/contacts/search", json={"email": "test@example.de"})

# Kontakt anlegen / updaten
contact = api("POST", "/contacts", json={"email": "neu@example.de", "fname": "Neu", "salutation": "f"})
contact_id = contact["data"]["id"]

# Tag zuweisen (via REST, nur für unkritische Fälle)
api("POST", f"/contacts/{contact_id}/addTag", json={"tagId": 42997})

# Custom Field setzen
api("POST", f"/globalFields/15306/setValue", json={
    "contactId": contact_id, "value": "PROMO-CODE", "doTriggers": True, "overwrite": True
})

# Tags eines Kontakts lesen
tags = api("GET", f"/contacts/{contact_id}/getTagList")["data"]

# GlobalField-Wert lesen
value = api("GET", f"/globalFields/15306/getValue", params={"contactId": contact_id})["data"]["value"]
```

---

## Endpoint-Übersicht

| Methode | Pfad | Beschreibung |
|---------|------|-------------|
| GET | `/contacts` | Alle Kontakte (paginiert) |
| GET | `/contacts/{id}` | Einzelner Kontakt |
| POST | `/contacts` | Erstellen / Upsert |
| PUT | `/contacts/{id}` | Aktualisieren |
| DELETE | `/contacts/{id}` | Löschen |
| POST | `/contacts/search` | Per E-Mail suchen |
| POST | `/contacts/{id}/opt-out` | Abmelden |
| GET | `/contacts/{id}/getTagList` | Tags lesen |
| GET | `/contacts/{id}/getFieldList` | Custom Fields lesen |
| POST | `/contacts/{id}/addTag` | Tag hinzufügen |
| POST | `/contacts/{id}/addTagList` | Mehrere Tags (max 20) |
| POST | `/contacts/{id}/removeTag` | Tag entfernen |
| POST | `/contacts/{id}/removeTagList` | Mehrere Tags entfernen |
| GET | `/tags` | Alle Tags |
| GET | `/tags/{id}` | Einzelner Tag |
| POST | `/tags` | Tag erstellen |
| PUT | `/tags/{id}` | Tag umbenennen |
| DELETE | `/tags/{id}` | Tag löschen |
| GET | `/globalFields` | Alle Custom Fields |
| GET | `/globalFields/{id}` | Einzelnes Field |
| POST | `/globalFields` | Field erstellen |
| PUT | `/globalFields/{id}` | Field aktualisieren |
| DELETE | `/globalFields/{id}` | Field löschen |
| GET | `/globalFields/{id}/getValue` | Wert für Kontakt lesen |
| POST | `/globalFields/{id}/setValue` | Wert setzen |
| POST | `/globalFields/setFieldList` | Mehrere Werte (max 20) |
| GET | `/campaigns` | Alle Campaigns (Follow-Up Funnels) |
| GET | `/campaigns/{id}` | Einzelne Campaign |
| DELETE | `/campaigns/{id}` | Löschen |
| POST | `/campaigns/{id}/start` | Kontakt einschreiben |
| POST | `/campaigns/{id}/stop` | Kontakt austragen |
| GET | `/opt-in-cases` | Alle Opt-In-Kategorien |
| POST | `/opt-in-cases/{id}/grant` | Opt-In gewähren |
| POST | `/opt-in-cases/{id}/revoke` | Opt-In widerrufen |
| GET | `/opt-ins` | DOI-E-Mails (ungenutzt) |
| DELETE | `/opt-ins/{id}` | DOI-E-Mail löschen |
| POST | `/opt-ins/{id}/send` | DOI-E-Mail senden |
