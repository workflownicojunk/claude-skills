# Tag Management und Member Sync

## Tag-Typen

### Subscription Tags (automatisch via Stripe/n8n)

| Tag Name | Trigger | Preis |
|----------|---------|-------|
| 39EUR Monatlich | Stripe subscription.created | 39 EUR/mo |
| Jahresabo | Stripe subscription.created | 390 EUR/yr |
| Coaching | Stripe subscription.created | 179 EUR oder 97 EUR |

**NIEMALS manuell ändern.** Werden automatisch vom n8n Workflow gesetzt/entfernt.

### Behavior Tags (manuell)

| Tag Name | Wann setzen |
|----------|-------------|
| Active Member | >5 Posts/Monat oder täglicher Login |
| Completed X.0 | Alle X.0 Lektionen abgeschlossen |
| Workshop Attendee | Nach Workshop-Teilnahme |
| Beta Tester | Freiwillig für Tests |

---

## Tag-zu-Access-Group Mapping

| Tag | Access Group (ID) | Spaces |
|-----|-------------------|--------|
| 39EUR Monatlich | Connect (78507) | 21 Spaces (Connect, Events, Challenges, etc.) |
| Jahresabo | Connect (78507) | Gleich wie 39EUR |
| Coaching | StrongerYou X.0 (88537) | 6 Spaces (SY X.0, Chat, Live, Start, Say HELLO, What's new?) |

### Access Group IDs

| ID | Produkt | Spaces |
|----|---------|--------|
| 88537 | StrongerYou X.0 | 6 |
| 78507 | Connect | 21 |
| 72778 | C9 Reset | 2 |
| 71906 | Happy Body Training | 2 |
| 65589 | StrongerYou 3.0 | 3 (Legacy) |
| 24767 | StrongerYou 1.0 | archiviert |
| 23952 | StrongerYou 2.0 | archiviert |

---

## Stripe-zu-Circle Sync (n8n Workflow)

### Trigger: Stripe Webhooks

- `subscription.created` -> Find/Create Member, Tag setzen, Access Group zuweisen
- `subscription.updated` -> Tags aktualisieren
- `subscription.canceled` -> Tags entfernen (mit Ratenzahlungs-Check!)

### Sync-Schritte

1. **Member finden:** `GET /community_members/search?email={email}`
2. **Falls nicht gefunden:** `POST /community_members` (neues Mitglied erstellen)
3. **Tag bestimmen:** Stripe Price Amount -> Tag Name (siehe Mapping oben)
4. **Tag setzen:** `POST /tagged_members` mit `{member_tag_id, community_member_id}`
5. **Access Group:** `POST /access_groups/{id}/community_members`
6. **Log:** Supabase `workflow_logs` Tabelle

### Ratenzahlung (KRITISCH)

Bei Coaching-Abos (179 EUR, 97 EUR) gilt:
- `subscription.canceled` bedeutet NICHT automatisch Zugang entfernen
- Prüfen: `is_installment === "true"` in Stripe Metadata
- Prüfen: Anzahl erhaltener Zahlungen
- 97 EUR: 6 Raten nötig. Unter 6 Raten: Zugang behalten!
- 179 EUR: 3 Raten nötig. Unter 3 Raten: Zugang behalten!
- Im Zweifel: An Nicol eskalieren

---

## API-Operationen für Tags

### Tag einem Member zuweisen

```bash
CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)

# Tag zuweisen
curl -X POST "https://app.circle.so/api/admin/v2/tagged_members" \
  -H "Authorization: Token $CIRCLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"member_tag_id":TAG_ID,"community_member_id":MEMBER_ID}'
```

### Tag entfernen

```bash
curl -X DELETE "https://app.circle.so/api/admin/v2/tagged_members" \
  -H "Authorization: Token $CIRCLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"member_tag_id":TAG_ID,"community_member_id":MEMBER_ID}'
```

### Alle Tags eines Members abrufen

```bash
curl -s "https://app.circle.so/api/admin/v2/community_members/$MEMBER_ID" \
  -H "Authorization: Token $CIRCLE_KEY" | python3 -c "
import json,sys; d=json.load(sys.stdin); print(d.get('member_tag_ids',[])); print(d.get('name',''))"
```

### Alternative: Tags via PUT (MERGE!)

```bash
# ACHTUNG: member_tag_ids bei PUT MERGED mit bestehenden Tags
# Erst bestehende IDs holen, dann neue ID anhängen
curl -X PUT "https://app.circle.so/api/admin/v2/community_members/$MEMBER_ID" \
  -H "Authorization: Token $CIRCLE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"community_id":346419,"member_tag_ids":[EXISTING_ID1,EXISTING_ID2,NEW_ID]}'
```

---

## Validierungsregeln

**Vor Tag-Zuweisung:**
1. Member existiert (GET prüfen)
2. Tag nicht bereits vorhanden (422 = idempotent, skip)
3. Korrekte tag_id (nicht verwechseln!)

**Vor Tag-Entfernung:**
1. Ist es ein Subscription Tag? Dann NICHT manuell entfernen
2. Bei Coaching: Ratenzahlung prüfen
3. Member sollte tatsächlich Zugang verlieren

---

## Supabase Daily Sync

n8n Workflow `QjU5fCfYNyl4DJa3` (08:00 UTC). 9 Tabellen:

| Circle Endpoint | Supabase Tabelle |
|-----------------|------------------|
| /community_members | circle_members |
| /posts | circle_posts |
| /comments | circle_comments |
| /events | circle_events |
| /member_tags | circle_tags |
| /spaces | circle_spaces |
| /space_members | circle_space_members |
| /course_lessons | circle_lessons |
| (course completions) | circle_course_progress |

---

## Email Support: Tag-basierte Entscheidungen

| Situation | API Check | Aktion |
|-----------|-----------|--------|
| "Kein Zugang" | GET member -> tags prüfen | Hat Tag + Space? -> Login-Anleitung. Kein Tag? -> Tag + Space setzen |
| "Alles gesperrt" | GET member -> tags prüfen | Drip-Content erklären (Lektionen abschließen!) |
| "Kündigung" | GET member -> tags prüfen | Coaching? SOFORT an Nicol. Standard? Check reason, eskalieren |

### Eskalations-Kriterien (SOFORT)

- ALL-CAPS, "Anwalt", "Betrug", "Abzocke"
- Coaching-Abos (179 EUR, 97 EUR, 189 EUR)
- Jahresabo (390 EUR)
- Datenschutz-Anfragen
- Mehrfach-Beschwerden
