# 4leads Internal API Documentation

**Generated:** 2026-02-22T03:15:00+01:00
**Method:** Chrome DevTools MCP reverse-engineering of app.4leads.net
**Session:** 02 - Campaign Statistics API
**Auth:** Cookie-based (user_login + user), session expires every 20 minutes (Max-Age=1200)

---

## Authentication

4leads uses cookie-based auth on `app.4leads.net`. No Bearer token or API key needed for the internal API.

| Cookie | Purpose |
|--------|---------|
| `user_login` | Session identifier (long hash) |
| `user` | User session token |

**Session Keepalive:** `GET /heartbeat?xhr=1` — call every <20 minutes to prevent timeout.

**Important:** This is NOT the official 4leads REST API (`api.4leads.net/v1` with `4L.` Bearer token). This documents the internal web application endpoints.

---

## XHR Pattern

Appending `?xhr=1` to any page URL returns JSON instead of HTML:

```json
{
  "success": true,
  "htmlReplaces": {
    "#content-container": "<div>...HTML fragment...</div>",
    ".breadcrumb-box": "<div>...breadcrumb HTML...</div>"
  },
  "functionCalls": [
    { "function": "$elNewsletter.init", "values": [] }
  ],
  "scriptVars": { ... },
  "title": "4leads"
}
```

The `htmlReplaces` object contains CSS selectors as keys and HTML fragments as values — this is how 4leads does client-side rendering.

---

## Endpoints

### 1. Dashboard

```
GET /dashboard?xhr=1
```

Returns dashboard HTML with tag widgets, contact statistics, and menu structure.

**Response:** JSON with `htmlReplaces` containing dashboard widgets.

---

### 2. Contact Analytics

```
GET /analytics/ajax/contacts?stStart={DD.MM.YYYY}&stEnde={DD.MM.YYYY}&self=true&stUser={userId}
```

| Param | Type | Example |
|-------|------|---------|
| stStart | string | `01.02.2026` |
| stEnde | string | `22.02.2026` |
| self | boolean | `true` |
| stUser | integer | `15346` (Nicol's user ID) |

**Response:**
```json
{
  "success": true,
  "labels": ["02. Feb.", "04. Feb.", ...],
  "leads": [90, 59, 64, ...],
  "leadsTotal": 1241,
  "bounces": [0, 1, 0, ...],
  "optouts": [14, 16, 10, ...],
  "optins": [91, 57, 64, ...],
  "start": "01.02.2026",
  "ende": "22.02.2026",
  "updated": "55 Min., 01:52",
  "updatedAt": 1771721568
}
```

---

### 3. Newsletter List

```
GET /email-funnel/newsletter
```

Returns HTML page with all newsletters. Extract rows via DOM:
- Selector: `tr[data-href*="/newsletter/detail/n/"]`
- Hash in URL: `/newsletter/detail/n/{hash}`

**Total newsletters found:** 47

---

### 4. Newsletter Detail + Statistics

```
GET /email-funnel/newsletter/detail/n/{hash}?xhr=1
```

| Param | Type | Example |
|-------|------|---------|
| hash | string | `83EQ` |

**Response includes `scriptVars.analyticData`:**
```json
{
  "analyticData": {
    "currentRecieverCount": 13509,
    "totalBase": 13509,
    "lastUpdated": "0 Min., 02:50",
    "clicked": 618,
    "clicked_multi": 692,
    "opened": 4119,
    "opened_multi": 5033,
    "opened_avg": 1.22,
    "send": 13488,
    "bounced": 21,
    "optouts_total": 226,
    "optouts": [
      {
        "id": 39171,
        "hash": "Grn3",
        "count": 226,
        "name": "Nachrichten von Nicol Stanzel (Standard)"
      }
    ],
    "updatedAt": 1771725020
  }
}
```

**Key metrics:**
- `opened` = unique opens (bot-filtered)
- `opened_multi` = total opens (including repeats)
- `clicked` = unique clicks
- `clicked_multi` = total clicks
- `bounced` = hard bounces
- `optouts_total` = unsubscribes from this newsletter

---

### 5. Refresh Newsletter Statistics

```
POST /email-funnel/ajax/newsletter/n/{hash}
Content-Type: application/x-www-form-urlencoded

action=postDetailStats
```

Triggers a server-side recalculation of newsletter statistics. Response contains updated `analyticData`.

---

### 6. Email Content Preview

```
GET /editor/email/preview/e/{emailHash}
```

Returns **full HTML** of the email including:
- Complete template with CSS styles
- Template variables: `{{firstname}}`, `{{lastname}}`, etc.
- Tracking links through `app.4leads.net/public/email-preview/links?placeholder=...`
- Images hosted on `onecdn.io`

**Example:** `/editor/email/preview/e/Y5PZ`

---

### 7. Email List

```
GET /email-funnel/email?pageNum={0-based}&pageSize=25&groupConnector=0
```

Returns paginated list of all emails (templates). Pagination is 0-based.

| Param | Type | Default |
|-------|------|---------|
| pageNum | integer | 0 |
| pageSize | integer | 25 |
| groupConnector | integer | 0 |

**Total emails found:** 84 across 4 pages.

Row selector: `tr[data-href*="/email/detail/e/"]`
Hash format: `/email/detail/e/{hash}`

---

### 8. Email Detail

```
GET /email-funnel/email/detail/e/{hash}?xhr=1
```

Returns email metadata, settings, and the preview iframe URL.

---

### 9. Follow-Up Funnels

```
GET /email-funnel/funnel
```

Returns list of all follow-up funnels.

**5 funnels found:**

| Hash | Name | Status |
|------|------|--------|
| `8lXZ` | Workshop Typeform Follow Up Dez24 | Active |
| `W6EN` | Launch Follow Up | Active |
| `xNNV` | Freebie → Tripwire Follow Up | Active |
| `mJJq` | Everwebinar Follow Up | Paused |
| `AMMQ` | Webinar Follow Up | Active |

---

### 10. Funnel Detail

```
GET /funnel/detail/f/{hash}
```

Returns funnel steps with email assignments, delays, and conditions.

---

### 11. Funnel Step Email Display

```
GET /funnel?action=getFunnelStepDisplay&funnelStepId={stepId}
```

| Param | Type | Example |
|-------|------|---------|
| funnelStepId | integer | `4035` |

**Response:** JSON with HTML containing email preview iframe and metadata.
- Email hash is in the iframe src: `/editor/email/preview/e/{emailHash}`
- Internal email ID in `data-post` attribute: `{emailId}#{funnelStepId}`

---

### 12. Tag Management

```
POST /tag/ajax/tagList
Content-Type: application/x-www-form-urlencoded
```

Returns tag list with date-based filtering. Tags are used for segmentation in 4leads.

---

### 13. Select/Search Endpoints (Dropdowns)

These endpoints power dynamic search dropdowns throughout the 4leads UI:

| Endpoint | Returns |
|----------|---------|
| `GET /select/tags` | All tags (for segmentation) |
| `GET /select/groups` | Contact groups |
| `GET /select/groups?filter=funnel` | Funnel-specific groups |
| `GET /select/campaign?includeProcesses=1` | Campaigns with processes |
| `GET /select/email` | All emails (for selection) |
| `GET /select/email-funnel` | All funnels |
| `GET /select/optin-cases` | Opt-in categories |
| `GET /select/global-fields` | Custom contact fields |
| `GET /select/integration/typemin/240101/typemax/240999/` | Typeform integrations |
| `GET /tools/coupons/select` | Coupons |
| `GET /tools/smartlinks/select?live=1` | Smart links |

---

### 14. Contact Management

```
POST /contacts/ajax/manage
```

Used for bulk operations on contacts. Specific actions determined by POST body.

---

### 15. Session Heartbeat

```
GET /heartbeat?xhr=1
```

Keeps session alive. Must be called within 20-minute window (cookie Max-Age=1200).

---

## Data Model

### Newsletter Object
```
{
  hash: string          // Short alphanumeric (e.g., "83EQ")
  internalId: number    // Numeric ID (e.g., 21002)
  name: string          // Full name with targeting info
  subject: string       // Email subject line
  sender: string        // "Nicol Stanzel <info@nicolstanzel.de>"
  replyTo: string       // "info@nicolstanzel.de"
  emailHash: string     // Separate hash for email content (e.g., "Y5PZ")
  sentAt: string        // "19.01.26 18:00"
  analyticData: {
    currentRecieverCount: number
    totalBase: number
    send: number
    bounced: number
    opened: number         // Unique opens
    opened_multi: number   // Total opens
    opened_avg: number     // Avg opens per opener
    clicked: number        // Unique clicks
    clicked_multi: number  // Total clicks
    optouts_total: number
    optouts: [{
      id: number
      hash: string
      count: number
      name: string       // Opt-out category name
    }]
    updatedAt: number    // Unix timestamp
  }
}
```

### Email Object
```
{
  hash: string          // Short alphanumeric (e.g., "bEKj")
  internalId: number    // Numeric ID (e.g., 51476)
  name: string          // Internal name with campaign/targeting info
  subject: string       // Email subject line
  createdAt: string     // "12.02.26" (DD.MM.YY)
}
```

### Funnel Object
```
{
  hash: string          // Short alphanumeric (e.g., "8lXZ")
  name: string          // Funnel name
  status: string        // "active" | "paused"
  steps: [{
    stepId: number
    emailId: number
    emailHash: string
    delay: string       // Delay before sending
    condition: string   // Targeting condition
  }]
}
```

---

## All 47 Newsletter Hashes

| # | Hash | Name | Date |
|---|------|------|------|
| 1 | `83EQ` | NL 01 nach Webinar SY Jan 26 | 19.01.26 |
| 2 | `Y5PZ` | Email: NL 01 nach Webinar SY Jan26 | 19.01.26 |

(Full list: run the extraction script in `4leads_api_client.js`)

---

## All 84 Email Hashes

### Page 1 (Jan-Feb 2026)
| Hash | Name | Date |
|------|------|------|
| `bEKj` | NL 01 BodyGuide 02-2026 - Ich hätte sowas nicht für möglich gehalten | 12.02.26 |
| `KGkY` | NL 02 BodyGuide 02-2026 - es wäre schade, wenn du das verpasst | 12.02.26 |
| `yPM1` | NL 01 BodyGuide 02-2026 - Wichtige Information für dich | 12.02.26 |
| `77rk` | Kopie - NL 8 nach Webinar - Wichtige Information zu deiner Teilnahme | 12.02.26 |
| `kVBJ` | NL 06 nach Webinar Jan 26 v2 - Noch 4 Stunden | 23.01.26 |
| `qje3` | NL 06 nach Webinar Jan 26 v2 - Dieser Moment abends im Bad | 23.01.26 |
| `gZ0Y` | NL 05 nach Webinar Jan 26 v2 - Darf ich dir kurz ehrlich etwas sagen? | 23.01.26 |
| `KGl8` | NL 04 nach Webinar Jan 26 - Noch 1 Stunde! | 22.01.26 |
| `5OaJ` | NL 3 nach Webinar SY Jan 26 - Deine letzte Chance | 21.01.26 |
| `NNY5` | NL 02 nach Webinar SY Jan26 - Vielleicht ist das der Moment | 20.01.26 |
| `rRb6` | Wiederholungstermin Datum - Info zum Live-Workshop Donnerstag | 20.01.26 |
| `Y5PZ` | NL 01 nach Webinar SY Jan26 - das ist für dich! | 19.01.26 |
| `rRAy` | Webinar Einladung STY Jan 26 Mail 8 - Woran liegt es? | 17.01.26 |
| `4K0n` | Webinar Einladung STY Jan 26 Mail 7 - Wichtige Info wegen morgen | 17.01.26 |
| `eA4x` | Webinar Einladung STY Jan 26 Mail 6 - Re: Deine Anmeldung | 15.01.26 |
| `VBkX` | Webinar Einladung STY Jan 26 Mail 5 - Letztens im Klamottenladen | 14.01.26 |
| `oxEl` | Webinar Einladung STY Jan 26 Mail 4 - Wichtige Ankündigung | 13.01.26 |
| `17JV` | Webinar Einladung STY Jan 26 Mail 3 - Du verlierst deinen Platz | 12.01.26 |
| `QXN7` | Kopie - Webinar Einladung Mail 1 - Persönliches Anliegen | 09.01.26 |
| `OGKR` | Webinar Einladung STY Jan 26 Mail 2 - Endlos-Schleife | 09.01.26 |
| `bE8m` | Webinar Einladung STY Jan 26 Mail 1 - Persönliches Anliegen | 09.01.26 |
| `eAqk` | StrongerYou Launch Registrierungsbestätigung | 08.01.26 |
| `akZG` | Content NL 2 - Sprachnachricht hat mich tief berührt | 05.01.26 |
| `3745` | NL 02 Jahresmitgliedschaft - Pilates im Hotelzimmer | 03.01.26 |
| `dp48` | NL 02 Jahresmitgliedschaft Connect 39 - Pilates im Hotelzimmer | 01.01.26 |

### Page 2 (Nov 2025 - Jan 2026)
| Hash | Name | Date |
|------|------|------|
| `07Ej` | NL 01 Jahresmitgliedschaft - Mein Geschenk an euch | 01.01.26 |
| `dpde` | Kopie - Content NL 1 - Persönliche Nachricht von Nicol | 01.01.26 |
| `NNm3` | NL 01 Jahresmitgliedschaft Connect 39 - Mein Geschenk | 01.01.26 |
| `rR5V` | Kopie - NL 03 Connect Follow-Up - Letzte Chance | 01.01.26 |
| `4KOJ` | Kopie - NL 03 Connect Follow-Up - Letzte Chance | 01.01.26 |
| `R0Nl` | TW WELCOME ZUM TRIPWIRE (Happy Body Training) | 28.12.25 |
| `l0JQ` | Content NL 1 - Persönliche Nachricht von Nicol | 22.12.25 |
| `aKvB` | NL 03 Connect Follow-Up - Letzte Chance | 03.12.25 |
| `gK71` | NL 02 Connect Follow-Up - Mail verpasst v1 | 03.12.25 |
| `eKGG` | NL 02 Connect Follow-Up - Mail verpasst v2 | 03.12.25 |
| `l2XO` | NL 02 Connect Follow-Up - Mail verpasst v3 | 03.12.25 |
| `RJlb` | NL 01 Connect Follow-Up - Der Moment in dem alles kippt | 03.12.25 |
| `vG8L` | TW WELCOME Tripwire - Zugang bereit | 19.11.25 |
| `JqY7` | TW FOLLOW-UP #3 Tag 3 - letzte Chance | 19.11.25 |
| `ZKjG` | TW FOLLOW-UP #2 Tag 2 - an der Grenze | 19.11.25 |
| `YKBE` | TW FOLLOW-UP #1 Tag 1 - gleicher Fehler wie alle | 19.11.25 |
| `AjRd` | Freebie Welcome + Download - 7-Tage Happy Body Plan | 19.11.25 |
| `YK6Q` | NL 01 BodyGuide - Ich hätte sowas nicht für möglich gehalten | 03.11.25 |
| `6rxq` | NL 02 nach Webinar - es wäre schade wenn du das verpasst | 03.11.25 |
| `rGrg` | NL 01 BodyGuide - Wichtige Information für dich | 03.11.25 |
| `pKlB` | NL 10 nach Webinar - Ich hätte sowas nicht für möglich gehalten | 30.10.25 |
| `6r5r` | NL 9 nach Webinar - es wäre schade wenn du das verpasst | 30.10.25 |
| `5rR5` | NL 8 nach Webinar - Wichtige Information zu deiner Teilnahme | 29.10.25 |
| `BRWb` | NL 7.1 nach Webinar SY3.0 V2 - Bestellung fehlgeschlagen | 23.10.25 |
| `8reZ` | NL 6.1 nach Webinar SY3.0 - wo bist du? | 23.10.25 |

### Page 3 (Oct 2025)
| Hash | Name | Date |
|------|------|------|
| `db1Z` | Neue E-Mail vom 23.10.2025 | 23.10.25 |
| `0r8W` | NL 7 nach Webinar SY3.0 V2 - Re: Deine Teilnahme | 23.10.25 |
| `gKoY` | NL 6 nach Webinar SY3.0 - Noch 1 Stunde | 22.10.25 |
| `eK4A` | 5 nach Webinar SY3.0 - Deine letzte Chance | 22.10.25 |
| `1rLr` | NL 3 nach Webinar SY3.0 - Würdest du es riskieren | 22.10.25 |
| `0rQX` | NL 3 nach Webinar SY3.0 - das ist für dich | 21.10.25 |
| `Np08` | NL 3 nach Webinar SY3.0 - Ratenzahlungs-Optionen | 21.10.25 |
| `2rQ4` | BG_gekauft_Onboarding | 20.10.25 |
| `6rby` | NL 2 nach Webinar SY3.0 - Wichtige Info zu deiner Anmeldung | 20.10.25 |
| `oo7q` | SY3.0 Everwebinar Erinnerung 1 Tag nachher - WOW | 20.10.25 |
| `2rL4` | SY3.0 Everwebinar Erinnerung 2 Stunden nachher | 20.10.25 |
| `QZWd` | SY3.0 Everwebinar Erinnerung 15 Minuten vorher | 20.10.25 |
| `WKZJ` | SY3.0 Everwebinar Erinnerung 1 Stunde vorher | 20.10.25 |
| `XMol` | SY3.0 Everwebinar Erinnerung 1 Tag vorher | 20.10.25 |
| `OAOl` | SY3.0 Everwebinar Registrierungsbestätigung | 20.10.25 |
| `vGv3` | 2. Versuch - SY3.0 Erinnerung 2 Stunden nachher VReg | 19.10.25 |
| `YK4q` | SYX.0 Willkommensmail nach Kauf | 19.10.25 |
| `PY4X` | SY3.0 NL4 - Morgen 10 Uhr gehts los | 17.10.25 |
| `ZKmK` | SY3.0 NL3 - Nur noch 2x schlafen | 17.10.25 |
| `l2xn` | SY3.0 NL2 - Sonntag 19.10. LIVE | 16.10.25 |
| `5rjY` | SY3.0 Erinnerung 1 Tag nachher VReg - WOW | 15.10.25 |
| `RJ8j` | SY3.0 Erinnerung 2 Stunden nachher VReg | 15.10.25 |
| `jQVG` | SY3.0 Erinnerung 15 Minuten vorher VReg | 15.10.25 |
| `BRvP` | SY3.0 Erinnerung 1 Stunde vorher VReg | 15.10.25 |
| `xL4m` | SY3.0 Erinnerung 1 Tag vorher VReg | 15.10.25 |

### Page 4 (Oct 2025)
| Hash | Name | Date |
|------|------|------|
| `8r7Y` | SY3.0 Erinnerung 3 Tage vorher VReg | 15.10.25 |
| `WK5B` | SY3.0 NL1 - Sonntag 19.10. LIVE | 15.10.25 |
| `1r3R` | SY3.0 Erinnerung 1 Tag nachher - Wow | 10.10.25 |
| `l2Nn` | SY3.0 Erinnerung 2 Stunden nachher | 10.10.25 |
| `5reY` | SY3.0 Erinnerung 15 Minuten vorher | 10.10.25 |
| `RJZj` | SY3.0 Erinnerung 1 Stunde vorher | 10.10.25 |
| `jQkG` | SY3.0 Erinnerung 1 Tag vorher | 10.10.25 |
| `BRpP` | SY3.0 Erinnerung 3 Tage vorher | 10.10.25 |
| `xLnm` | SY3.0 Registrierungsbestätigung | 10.10.25 |

---

## 5 Follow-Up Funnels

| Hash | Name | Status |
|------|------|--------|
| `8lXZ` | Workshop Typeform Follow Up Dez24 | Active |
| `W6EN` | Launch Follow Up | Active |
| `xNNV` | Freebie -> Tripwire Follow Up | Active |
| `mJJq` | Everwebinar Follow Up | Paused |
| `AMMQ` | Webinar Follow Up | Active |

---

## Usage Notes

1. **Cookie session expires every 20 minutes.** Use `/heartbeat?xhr=1` for keepalive.
2. **Rate limiting:** No explicit rate limit observed, but 4leads is slow (~2-5s response times).
3. **Pagination:** 0-based page numbers, default pageSize=25.
4. **Hash system:** Two separate hash spaces — one for content entities (newsletters, funnels), another for email templates.
5. **Email content:** Always retrieved via `/editor/email/preview/e/{hash}` — returns full HTML with template variables.
6. **Statistics refresh:** Use POST to `postDetailStats` action to get fresh stats; cached data can be stale.
7. **User ID:** Nicol's account = `15346`.
