# Circle API Operations (Kompaktreferenz)

## Was die Admin API V2 KANN (Cheat Sheet)

| Aufgabe | Endpoint | Methode |
|---------|----------|---------|
| Member einladen | `POST /community_members` | `{"email":"...","skip_invitation":false}` |
| Member suchen | `GET /community_members?query=email` | Nur `?query=`, kein `/search` Endpoint |
| Access Group zuweisen | `POST /access_groups/{AG_ID}/community_members` | `{"email":"...","community_member_ids":[MEMBER_ID]}` (email Pflicht!) |
| Access Group zuweisen (ALT) | `PUT /community_members/{id}` mit `access_group_ids` | Funktioniert NICHT zuverlässig, Feld wird oft ignoriert |
| Tag zuweisen (Methode A) | `POST /tagged_members` | `{"member_tag_id":X,"community_member_id":Y,"user_email":"..."}` (user_email Pflicht!) |
| Tag zuweisen (Methode B) | `PUT /community_members/{id}` | `{"member_tag_ids":[id1,id2,...]}` (MERGE!) |
| Tag erstellen | `POST /member_tags` | `{"name":"...","display_format":"label"}` (display_format Pflicht!) |
| Profile Fields setzen | `PUT /community_members/{id}` | `{"custom_profile_field_values":{"key":"val"}}` |
| Space Member hinzufügen | `POST /space_members` | `{"space_id":X,"community_member_id":Y}` |

Für Tag-Sync und Custom Fields siehe auch den `crm-sync` Skill (verifizierte Endpoints).

## Admin API V2

**Base URL:** `https://app.circle.so/api/admin/v2`
**Auth:** `Authorization: Token $CIRCLE_ADMIN_API_KEY` (NICHT Bearer!)
**Rate Limit:** 60 req/min, 1s Pause zwischen Calls
**Community ID:** 346419
**Swagger:** https://api-headless.circle.so/?urls.primaryName=Admin%20API%20V2

### .env laden (WICHTIG)
```bash
CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)
```

### Members

```bash
# Suchen (nach Email)
GET /community_members/search?email={email}

# Auflisten (paginiert)
GET /community_members?per_page=100&page=1
# Response: {records: [{id, name, email, public_uid, avatar_url, ...}], has_next_page}

# Einzeln abrufen
GET /community_members/{id}

# Erstellen/Einladen
POST /community_members
{"email":"...","name":"...","skip_invitation":false}

# Aktualisieren (Name, Bio, Custom Fields)
PUT /community_members/{id}
{"name":"...","custom_profile_field_values":{"key":"value"}}

# Deaktivieren (soft delete)
DELETE /community_members/{id}

# Löschen (hard delete)
PUT /community_members/{id}/delete_member

# Bannen
PUT /community_members/{id}/ban_member
```

**public_uid:** Wird für Mentions gebraucht. Ist der User-Slug, NICHT die Member-ID.

**ACHTUNG:** `?query=` Parameter bei `GET /community_members` ist BROKEN. Ignoriert den Suchbegriff und gibt immer die gleichen 10 Member zurück. Stattdessen:
- Email-Suche: `GET /community_members/search?email={email}` (funktioniert)
- Name-Suche: `GET /advanced_search?query={name}` (gibt public_uid + sgid zurück)

### Mentions in Kommentaren

```html
<a class="mention" href="https://strongeryou.circle.so/u/{public_uid}"
   target="_blank" rel="noopener noreferrer">Vorname Nachname</a>
```
Kein `@`-Zeichen nötig. Der Name wird durch das `mention`-CSS-Klasse automatisch blau hinterlegt.
Body immer in `<div><p>...</p></div>` wrappen.

### Comments

```bash
# Auflisten (nach Post)
GET /comments?post_id={id}

# Erstellen (Top-Level)
POST /comments
{"community_id":346419,"post_id":POST_ID,"body":"<p>Text</p>"}

# Reply auf Kommentar
POST /comments
{"community_id":346419,"post_id":POST_ID,"body":"<p>Text</p>","parent_comment_id":COMMENT_ID}

# Löschen
DELETE /comments/{id}
```

### Posts

```bash
# Auflisten (nach Space, paginiert)
GET /posts?space_id={id}&per_page=100&page=1&status=published

# Erstellen
POST /posts
{"community_id":346419,"space_id":SPACE_ID,"name":"Titel","body":"<p>HTML</p>","published":true}

# Aktualisieren
PUT /posts/{id}

# Löschen
DELETE /posts/{id}

# AI Summary
GET /posts/{post_id}/summary
```

### Spaces

```bash
# Alle auflisten
GET /spaces
# Response: {records: [{id, name, slug, is_private, is_hidden_from_non_members, ...}]}

# Erstellen
POST /spaces

# Aktualisieren (z.B. hidden setzen)
PUT /spaces/{id}
{"is_hidden_from_non_members":true}

# AI Summary eines Space
GET /spaces/{space_id}/ai_summaries

# Löschen
DELETE /spaces/{id}
```

### Space Groups

```bash
GET /space_groups           # Alle auflisten
POST /space_groups          # Erstellen
PUT /space_groups/{id}      # Aktualisieren
DELETE /space_groups/{id}   # Löschen
```

### Space Members

```bash
# Auflisten
GET /space_members?space_id={id}

# Hinzufügen
POST /space_members
{"community_id":346419,"space_id":SPACE_ID,"community_member_id":MEMBER_ID}

# Entfernen
DELETE /space_members
```

### Member Tags

```bash
# Alle Tags auflisten
GET /member_tags

# Tag erstellen
POST /member_tags
{"community_id":346419,"name":"Tag-Name","display_format":"label"}

# Tag Details
GET /member_tags/{id}

# Tag löschen
DELETE /member_tags/{id}
```

### Tagged Members (Tag-Zuweisung)

```bash
# Tag zuweisen (user_email ist Pflicht!)
POST /tagged_members
{"member_tag_id":TAG_ID,"community_member_id":MEMBER_ID,"user_email":"member@email.com"}

# Tag entfernen
DELETE /tagged_members
# Body: {"member_tag_id":TAG_ID,"community_member_id":MEMBER_ID,"user_email":"member@email.com"}

# Alle Members mit Tag auflisten
GET /tagged_members?member_tag_id={id}
```

**ACHTUNG (MEMORY):** `PUT /community_members/{id}` mit `member_tag_ids` funktioniert auch als MERGE. Erst GET, dann bestehende IDs + neue ID senden.

### Access Groups

```bash
# Auflisten
GET /access_groups

# Member zu Access Group hinzufügen
POST /access_groups/{access_group_id}/community_members
{"community_member_ids":[MEMBER_ID]}

# Member entfernen
DELETE /access_groups/{access_group_id}/community_members

# Member's Access Groups prüfen
GET /community_members/{community_member_id}/access_groups
```

### Events

```bash
# Auflisten
GET /events?space_id={id}

# Erstellen
POST /events
{"community_id":346419,"space_id":SPACE_ID,"name":"...","starts_at":"ISO8601","ends_at":"ISO8601"}

# Event-Teilnehmer
GET /event_attendees?event_id={id}
POST /event_attendees {"event_id":ID,"community_member_id":MEMBER_ID}
```

### Courses

```bash
# Sections auflisten
GET /course_sections?space_id={id}

# Lessons auflisten
GET /course_lessons?space_id={id}

# Lesson Progress aktualisieren
PUT /course_lesson_progress
```

### Advanced Search

```bash
GET /advanced_search?query={text}
# Durchsucht Posts, Comments, Lessons, Spaces, Members
```

### Invitation Links

```bash
GET /invitation_links         # Auflisten
DELETE /invitation_links/{id} # Löschen
PATCH /invitation_links/{id}/revoke  # Widerrufen
```

---

## Headless Member API V1

**Base URL:** `https://app.circle.so/api/headless/v1`
**Auth:** JWT Token (per Auth API generiert, 1h gültig)
**Zweck:** Member-Perspektive, Custom Frontend, Content-Suche, **Kommentare als bestimmter User posten**

### Auth Token holen

```bash
# WICHTIG: Dedizierte Headless Keys verwenden, NICHT den Admin API Key!
NICO_KEY=$(grep '^CIRCLE_HEADLESS_MEMBER_API_KEY_NICO=' ~/Desktop/.env | cut -d= -f2)
curl -s -X POST "https://app.circle.so/api/v1/headless/auth_token" \
  -H "Authorization: Bearer $NICO_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"info@nicojunk.com"}'
# Response: {access_token, refresh_token, community_member_id}
# Token gültig für 1h
```

Verfügbare Headless Keys in .env:
- `CIRCLE_HEADLESS_MEMBER_API_KEY_NICO` → info@nicojunk.com (Nico Junk, member_id: 38688280)
- `CIRCLE_HEADLESS_MEMBER_API_KEY_NICOL` → nicol@lightnessfitness.de (Nicol Stanzel, member_id: 38375437)

### Kommentare als bestimmter User posten

```bash
# Top-Level-Kommentar (WICHTIG: Body muss in "comment" Objekt gewrapped werden!)
curl -s -X POST "https://app.circle.so/api/headless/v1/posts/{POST_ID}/comments" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":{"body":"<div><p>Text</p></div>"}}'

# Reply auf einen Kommentar (EINGENESTETER Reply):
# WICHTIG: parent_comment_id im POST /posts/{id}/comments wird IGNORIERT!
# Stattdessen den /comments/{id}/replies Endpoint nutzen:
curl -s -X POST "https://app.circle.so/api/headless/v1/comments/{COMMENT_ID}/replies" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"comment":{"body":"<div><p>Reply-Text</p></div>"}}'
# Dieser Endpoint setzt parent_comment_id automatisch korrekt.
```

**KRITISCH: Reply-Nesting funktioniert NUR über `/comments/{id}/replies`!**
- `POST /posts/{id}/comments` mit `parent_comment_id` → wird IGNORIERT, postet als Top-Level
- `POST /comments/{id}/replies` → setzt `parent_comment_id` korrekt, Reply wird eingenested
- **Reply auf Reply funktioniert!** Auch wenn der Ziel-Kommentar selbst ein Reply ist, kann man darauf mit `/comments/{id}/replies` antworten. Das `parent_comment_id` wird korrekt auf den Ziel-Kommentar gesetzt.
- **Reply-Ziel:** Immer direkt auf den Kommentar der Person antworten (deren Comment-ID), NICHT auf den eigenen Top-Level-Kommentar. Sonst erscheinen alle Replies im UI auf gleicher Ebene.

**Admin API vs Headless API für Kommentare:**
- Admin API `POST /comments`: Postet als Nico Junk (API-Key-Inhaber), NICHT als Community-Owner
- Admin API unterstützt `parent_comment_id`, aber die Replies werden nicht korrekt eingenested im UI
- Headless API `POST /posts/{id}/comments`: Postet als der User des JWT Tokens (Top-Level)
- Headless API `POST /comments/{id}/replies`: Postet als JWT-User mit korrektem Nesting
- **Für Kommentare als Nico: IMMER Headless API nutzen, für Replies IMMER /comments/{id}/replies!**

### Mention-UID Verification (PFLICHT)

Vor jeder Mention die UID verifizieren. NIEMALS UIDs aus dem Gedächtnis verwenden!

**Methode 1 (bevorzugt):** Email aus dem Comment-User-Objekt nehmen:
```bash
GET /community_members/search?email={email}
# Response enthält public_uid. Zuverlässigste Methode.
```

**Methode 2 (Fallback):** Name-Suche:
```bash
GET /advanced_search?query={Vorname+Nachname}
# Gibt public_uid + sgid zurück.
```

### Notifications

```bash
# Notifications abrufen (Replies und Mentions auf eigene Posts/Comments)
GET /notifications?per_page=50
# Response: {records: [{id, action, notifiable_id, notifiable: {post_id, parent_comment_id}, actor_name, notifiable_title, space_title, action_web_url}]}
# action: "reply" | "mention" | "like" | "comment"
# Filtern: nur "reply" und "mention" sind relevant für Kommentar-Antworten
```

### Wichtige Endpoints

```bash
# Content-Suche (für RAG, Knowledge Base)
GET /advanced_search?query={text}
GET /search?query={text}

# Posts in Space
GET /spaces/{space_id}/posts?per_page=100&page=1

# Kommentare zu Post
GET /posts/{post_id}/comments

# Home Feed
GET /home?page=1&per_page=20&sort=popular

# Spaces (Member-Perspektive, nur sichtbare)
GET /spaces

# Events
GET /community_events

# Chat Rooms + Messages
GET /messages
GET /messages/{chat_room_uuid}/chat_room_messages

# Kurs-Sections und Lessons
GET /courses/{course_id}/sections
GET /courses/{course_id}/lessons/{lesson_id}
```

---

## Interne API (Cookie-basiert, nur Browser-Session)

Nur aus Chrome DevTools nutzbar, kein Token-Header.

```bash
# Einladungslink erstellen
POST /internal_api/admin/invitation_links
{"invitation_link":{"name":"...","space_ids":[],"space_group_ids":[],"member_tag_ids":[],"access_groups_enabled":true},"access_groups":[ACCESS_GROUP_ID]}
# URL: https://strongeryou.circle.so/join?invitation_token={token}

# Bestehende Links
GET /internal_api/admin/invitation_links?page=1&per_page=20

# Member-sichtbare Spaces (für Validierung)
GET /internal_api/spaces?include_sidebar=true

# Email Templates
GET /internal_api/communities/custom_invitation_email
```

### Direct Messages (DMs)

**API-Hierarchie für DMs (verifiziert 2026-03-13):**
- **Lesen:** Headless API (`GET /messages`, `GET /messages/{uuid}/chat_room_messages`)
- **Senden:** Headless API funktioniert direkt mit JWT. Kein Playwright/Browser nötig!
- **Löschen:** Headless API (`DELETE /messages/{uuid}/chat_room_messages/{id}`)
- **Chat-Room erstellen:** Headless API
- **Internal API:** Nur noch als Fallback, erfordert Browser-Session (Playwright)

```bash
# JWT holen (Nico-Key für Support-Antworten)
NICO_KEY=$(grep '^CIRCLE_HEADLESS_MEMBER_API_KEY_NICO=' ~/Desktop/.env | cut -d= -f2)
JWT=$(curl -s -X POST "https://app.circle.so/api/v1/headless/auth_token" \
  -H "Authorization: Bearer $NICO_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"info@nicojunk.com"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")

# Chat-Rooms auflisten
GET /api/headless/v1/messages
# Response: {records: [{uuid, chat_room_name, unread_messages_count, chat_room_kind,
#   other_participants_preview: [{id (participant_id), community_member_id, name, email}],
#   current_participant: {id (eigene participant_id), ...}}]}

# Nachrichten lesen
GET /api/headless/v1/messages/{UUID}/chat_room_messages?per_page=25
# Response: {records: [{id, body, rich_text_body, chat_room_participant_id, sent_at, ...}]}

# Nachricht senden (VERIFIZIERT - kein Wrapper, kein participant_id nötig!)
POST /api/headless/v1/messages/{UUID}/chat_room_messages
{"rich_text_body": {"body": {"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Nachricht"}]}]}, "attachments": []}}
# Erfolg: HTTP 202 {"creation_uuid":"...","sent_at":"ISO8601"}

# Nachricht löschen
DELETE /api/headless/v1/messages/{UUID}/chat_room_messages/{MESSAGE_ID}
# Erfolg: HTTP 200 {}

# Chat-Room erstellen
POST /api/headless/v1/messages
{"chat_room":{"community_member_ids":[MEMBER_ID],"kind":"direct"}}

# Room-Details (gibt current_participant.id = eigene participant_id)
GET /api/headless/v1/messages/{UUID}
# Nützlich um zu prüfen wer die letzte Nachricht gesendet hat (chat_room_participant_id vergleichen)
```

**Bekannte Chat-UUIDs:**
| Chat | UUID |
|------|------|
| Nicol Stanzel (Nicols Account) | `85eccd9a-d0d0-4d0d-872b-7775f1ae58b3` |

**Python-Pattern für DM senden:**
```python
import urllib.request, json

jwt = "..."  # Aus auth_token Endpoint
headers = {'Authorization': f'Bearer {jwt}', 'Content-Type': 'application/json', 'User-Agent': 'CRM-Sync/1.0'}

payload = json.dumps({"rich_text_body": {"body": {"type":"doc","content":[{"type":"paragraph","content":[{"type":"text","text":"Nachricht"}]}]},"attachments":[]}}).encode()
req = urllib.request.Request(f'https://app.circle.so/api/headless/v1/messages/{uuid}/chat_room_messages', data=payload, headers=headers, method='POST')
with urllib.request.urlopen(req) as resp:
    result = json.load(resp)  # {"creation_uuid":"...","sent_at":"..."}
```

**Internal API (Fallback, nur wenn Headless nicht klappt):**
```bash
# Senden via Playwright eval (Cookie Auth)
POST /internal_api/chat_rooms/{UUID}/messages/
{"chat_room_message":{"chat_room_participant_id":PARTICIPANT_ID,"rich_text_body":{...},"unfurl_urls":{}}}
# CSRF-Token aus <meta name="csrf-token"> nötig
```

### Connect & Messaging Settings (Admin)

```bash
# Settings abrufen
GET /internal_api/admin/connect/settings
# Response: {connect: {enabled, recommendations, ...}, member_directory: {...}, messaging: {enabled, member_to_member_messaging_enabled, group_messaging_enabled, voice_messages_enabled, require_connection_before_messaging}}

# Settings aktualisieren (über Browser-UI: Settings > Connect)
# UI-Pfad: https://strongeryou.circle.so/settings/connect

# Community Settings (Feature Flags, read-only)
GET /internal_api/community_settings
```

---

## HTTP Status Codes

| Code | Bedeutung | Aktion |
|------|-----------|--------|
| 200/201 | OK/Created | Weiter |
| 401 | Unauthorized | Token prüfen |
| 404 | Not Found | ID prüfen |
| 422 | Validation Error | Payload prüfen (z.B. "already has tag") |
| 429 | Rate Limit | 60s warten, dann retry (max 3x) |

## Best Practices

- Webhooks bevorzugen statt Polling (Circle Workflows > Admin > Automations)
- Responses cachen wenn möglich
- Pagination: immer `has_next_page` prüfen
- Zapier: Admin V1 Usage ist kostenlos (kein Quota)
- `display_format: "label"` ist Pflicht bei `POST /member_tags`
