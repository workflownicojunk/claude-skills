# Circle API Patterns

## Auth

```bash
CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)
BASE="https://app.circle.so/api/admin/v2"
```

KRITISCH: `Token` NICHT `Bearer`!
KRITISCH: `User-Agent: Gmail-Workflow/1.0` IMMER setzen (ohne Default User-Agent: 403)

## Member suchen

```bash
curl -s "$BASE/community_members/search?email=MEMBER_EMAIL" \
  -H "Authorization: Token $CIRCLE_KEY" \
  -H "User-Agent: Gmail-Workflow/1.0"
```

Response: `{id, name, email, public_uid, ...}`

## Access Group zuweisen

```bash
# AG IDs: Happy Body Training=71906, Connect=78507, StrongerYou X.0=88537, C9=72778
curl -s -X POST "$BASE/access_groups/ACCESS_GROUP_ID/community_members" \
  -H "Authorization: Token $CIRCLE_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Gmail-Workflow/1.0" \
  -d '{"community_member_ids":[MEMBER_ID]}'
```

## Tag zuweisen (PFLICHT: user_email Parameter!)

```bash
# Tag IDs: Happy Body Training=200831, Connect=202343, StrongerYou X.0=215031
curl -s -X POST "$BASE/tagged_members" \
  -H "Authorization: Token $CIRCLE_KEY" \
  -H "Content-Type: application/json" \
  -H "User-Agent: Gmail-Workflow/1.0" \
  -d '{"member_tag_id":TAG_ID,"community_member_id":MEMBER_ID,"user_email":"member@email.com"}'
```

GOTCHA: `user_email` ist PFLICHTFELD. Ohne diesen Parameter schlägt der API-Call lautlos fehl oder gibt einen Fehler zurück.

## Produkt-zu-Access-Group Mapping

| Produkt | Access Group ID | Tag ID |
|---------|----------------|--------|
| Happy Body Training | 71906 | 200831 |
| Connect (alle Preispunkte) | 78507 | 202343 |
| StrongerYou X.0 | 88537 | 215031 |
| C9 | 72778 | (kein Standard-Tag) |

## Rate Limits

- `per_page` max: 20 (100 gibt 403)
- `member_tag_id` Filter in List-Endpoints: funktioniert NICHT zuverlässig

## Häufige Fehler

| Fehler | Ursache | Fix |
|--------|---------|-----|
| 403 | Default User-Agent geblockt | `User-Agent: Gmail-Workflow/1.0` setzen |
| 404 bei Tag-Zuweisung | user_email fehlt | user_email PFLICHT hinzufügen |
| Member nicht gefunden | E-Mail-Mismatch (Kauf mit anderer E-Mail) | Im E-Mail-Body nach Hinweisen suchen |

## DM senden (via Internal API)

Nur wenn nötig (normal via E-Mail):
```javascript
// via playwright-cli eval
const r = await fetch('/internal_api/chat_rooms/{UUID}/messages/', {
  method: 'POST', credentials: 'include',
  headers: {'Content-Type': 'application/json', 'X-CSRF-Token': csrfToken},
  body: JSON.stringify({chat_room_message: {
    chat_room_participant_id: PARTICIPANT_ID,
    rich_text_body: {body: {type: 'doc', content: [{type: 'paragraph', content: [{type: 'text', text: 'Nachricht'}]}]}, attachments: []},
    unfurl_urls: {}}})
});
```
