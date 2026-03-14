---
name: circle-community
description: "Use when working with the StrongerYou Circle.so community. Covers: replying to community comments and notifications as Nico (Headless API), member support, onboarding FAQ, Circle Admin API V2 operations (comments, replies, tags, member management), space navigation, access groups, and content access. Trigger on: Circle, community, Kommentare beantworten, Notifications, comment replies, member FAQ, onboarding, course access, tags, community sync, space visibility, access groups, member mentions, or any task involving strongeryou.circle.so."
---

# Circle Community: Operations, API, Support & Onboarding

Complete reference for the StrongerYou Circle.so community (~960 members, women 35-65, DACH).

## Community Overview

- **URL:** https://strongeryou.circle.so
- **Members:** ~960 (Stand: Feb 2026)
- **Login:** Magic Link (OTP per E-Mail, kein Passwort)
- **App:** "Circle Community" (iOS + Android), dann "StrongerYou" wählen
- **Support:** info@nicolstanzel.de | DM an Nicol Stanzel oder lippi (Moderatorin)

## Primary Workflow: Notifications beantworten

Der häufigste Use-Case ist: Nicos Circle-Notifications durchgehen und auf technische/Support-Fragen antworten.

### PFLICHT vor jedem DM-Reply: Thread-History laden

Vor dem Verfassen JEDER DM-Antwort:
1. **Vollständigen Thread laden:** `GET /messages/{uuid}/chat_room_messages?per_page=20`
2. **Prüfen:** Ist die letzte Nachricht der Person eine Bestätigung ("Danke", "hat geklappt", "super", "ok")? -> NICHT antworten.
3. **Prüfen:** Hat Nico in den letzten 24h bereits geschrieben? -> NICHT erneut schreiben (außer neue Info).
4. **Prüfen:** Ist die Frage der Person schon beantwortet (durch eine spätere Nachricht im Thread)? -> NICHT antworten.
5. **Erst dann:** Antwort verfassen unter strikter Einhaltung von `topic-nico-voice.md`.

### Vor dem Start: Launch-Kontext laden

Vor jedem Durchlauf zwei Quellen laden:

1. **Dynamisch (Stripe):** `python3 ~/.claude/skills/circle-community/scripts/fetch_launch_context.py` ausführen. Gibt aktive Promo-Codes, Coupons, Connect-Preise und deren Ablaufdaten zurück. So erkennst du automatisch, welche Aktionen gerade laufen, ohne dass Nico dir den Kontext jedes Mal mitteilen muss.

2. **Statisch (Tonalität + FAQ):** `references/ref-current-launch.md` lesen. Enthält die häufigen Fragen, Antwort-Tonalität und FAQ für die aktuelle Launch-Phase. Wird manuell aktualisiert wenn ein neuer Launch startet.

3. **Fallback (4leads E-Mails):** Falls der Launch-Kontext unklar ist oder `ref-current-launch.md` veraltet wirkt, die letzten 4leads E-Mails und Follow-Up-Funnels prüfen. Die E-Mail-Betreffzeilen und Inhalte zeigen, was aktuell beworben wird (Preise, Deadlines, Aktionen). Dafür:
   ```bash
   # Letzte E-Mails abrufen (erfordert eingeloggte playwright-cli Session)
   playwright-cli goto "https://app.4leads.net/email-funnel/email?pageNum=0&pageSize=10"
   ```
   Die E-Mail-Betreffzeilen verraten sofort den aktuellen Fokus (z.B. "Connect Frühbucher", "BodyGuide-Bonus", "Letzte Chance").

Zusammen ergeben diese Quellen den vollständigen Kontext für korrekte Antworten auf Preis-, Promotion- und Support-Fragen.

### Quick Start (State-basiert)

```bash
# Neue Notifications mit Kontext abrufen (filtert automatisch bereits beantwortete)
python3 ~/.claude/skills/circle-community/scripts/fetch_new_notifications.py
```

Das Script gibt JSON mit allen neuen Notifications aus, inkl. Kommentar-Text, Parent-Kontext, Actor-Name/Email und Post-Titel. State wird in `~/Desktop/Area/Community/circle-notification-state.json` gespeichert.

**Nach dem Beantworten:** State aktualisieren:
```python
# In Python nach erfolgreichem Reply:
import json
state = json.load(open(os.path.expanduser("~/Desktop/Area/Community/circle-notification-state.json")))
state["last_notification_id"] = newest_notification_id  # ID der neuesten Notification
state["answered_comment_ids"].append(comment_id)  # Beantwortete Comment-ID
# Nur die letzten 200 behalten
state["answered_comment_ids"] = state["answered_comment_ids"][-200:]
json.dump(state, open(os.path.expanduser("~/Desktop/Area/Community/circle-notification-state.json"), "w"))
```

### Manueller Schritt-für-Schritt (falls Script nicht verwendet wird)

1. **JWT holen** (Headless API, gültig 1h):
   ```bash
   NICO_KEY=$(grep '^CIRCLE_HEADLESS_MEMBER_API_KEY_NICO=' ~/Desktop/.env | cut -d= -f2)
   JWT=$(curl -s -X POST "https://app.circle.so/api/v1/headless/auth_token" \
     -H "Authorization: Bearer $NICO_KEY" \
     -H "Content-Type: application/json" \
     -d '{"email":"info@nicojunk.com"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['access_token'])")
   ```

2. **Notifications abrufen:**
   ```bash
   curl -s "https://app.circle.so/api/headless/v1/notifications?per_page=50" \
     -H "Authorization: Bearer $JWT"
   ```
   Filtern nach `action: "reply"` und `action: "mention"`. Likes und allgemeine Comments ignorieren.

   **Response-Format:** `{records: [{id, action, notifiable_id, notifiable: {post_id, parent_comment_id}, actor_name, notifiable_title, space_title, action_web_url}]}`

3. **Kontext laden** (Admin API, anderer Auth-Header!):
   ```bash
   CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)
   curl -s "https://app.circle.so/api/admin/v2/comments?post_id={POST_ID}&per_page=100" \
     -H "Authorization: Token $CIRCLE_KEY"
   ```
   Für jeden relevanten Notification-Kommentar:
   - `notifiable.post_id` und `notifiable.parent_comment_id` aus der Notification extrahieren
   - Nicos vorherige Antwort im Thread finden (user.email == info@nicojunk.com)

4. **Entscheiden: Antworten oder nicht?**
   - **Antworten:** Technische Fragen, Support (Zugang, BodyGuide, Preise, Messaging, Aufzeichnungen)
   - **NICHT antworten:** Inhaltliche Fitness-Themen (Training, Ernährung, Motivation, Erfolge)
   - **Kurze Bestätigung:** Wenn jemand "Danke" oder "hat geklappt" schreibt: maximal 1 Satz, keine Mention nötig, keine Erklärung. Beispiele: "Super, freut mich!", "Sehr schön!", "Perfekt, dann passt alles."

5. **UIDs verifizieren** (für Mentions im Reply):
   - Primär: Email aus dem Comment-User-Objekt nehmen, dann `GET /community_members/search?email={email}` (gibt `public_uid` zurück)
   - Alternativ: `GET /advanced_search?query={Vorname+Nachname}`
   - **NIEMALS UIDs aus dem Gedächtnis verwenden!**

6. **Reply posten** (direkt auf den Kommentar der Person):
   ```bash
   curl -s -X POST "https://app.circle.so/api/headless/v1/comments/{DEREN_COMMENT_ID}/replies" \
     -H "Authorization: Bearer $JWT" \
     -H "Content-Type: application/json" \
     -d '{"comment":{"body":"<div><p><a class=\"mention\" href=\"https://strongeryou.circle.so/u/{public_uid}\" target=\"_blank\" rel=\"noopener noreferrer\">Vorname Nachname</a> Antworttext hier.</p></div>"}}'
   ```

7. **State aktualisieren** (nach jedem Durchlauf)

### Reply-Regeln (KRITISCH)

- **Reply-Ziel:** Immer `POST /comments/{DEREN_COMMENT_ID}/replies` verwenden, wobei `DEREN_COMMENT_ID` die ID des Kommentars ist, auf den geantwortet wird. NICHT auf den eigenen Top-Level-Kommentar replyen, sonst landen alle Replies auf gleicher Ebene im UI.
- **Reply auf Reply funktioniert:** `/comments/{id}/replies` funktioniert auch wenn der Ziel-Kommentar selbst ein Reply ist. Das `parent_comment_id` wird korrekt gesetzt.
- **`parent_comment_id` in POST /posts/{id}/comments wird IGNORIERT!** Nur der `/comments/{id}/replies` Endpoint erzeugt korrektes Nesting.
- **Admin API vermeiden für Kommentare:** Admin API `POST /comments` postet als API-Key-Inhaber und nestet nicht korrekt. Immer Headless API nutzen.
- **Chronologische Reihenfolge:** Bei mehreren Replies im gleichen Thread die älteste Nachricht zuerst beantworten.

### Kommunikationsregeln

- **Niemals Probleme zugeben:** Kein "ich prüfe das", kein "da scheint es ein Problem zu geben", kein "sollte eigentlich funktionieren". Stattdessen: Anleitungen geben, positiv formulieren.
- **Reframing statt Entschuldigung:** Statt "Sorry, das funktioniert noch nicht" lieber "Geh mal auf Mitglieder, klick auf den Namen, dann oben rechts auf das Nachrichten-Symbol."
- **Inhaltliche Fitness-Themen:** NICHT beantworten. Das macht Nicol oder die Moderatorinnen.

### Schreibstil: Nico Junk Tone of Voice (MANDATORY)

**VOR dem Schreiben JEDER Nachricht:** Lade `~/.claude/projects/-Users-nicojunk-Desktop/memory/topic-nico-voice.md`. Dieses File enthält die vollständige, aus 112 echten Nico-DMs extrahierte Tonalitätsreferenz. Jede Nachricht muss diesem File entsprechen.

**Kurzfassung der wichtigsten Regeln:**
- Schreib wie ein hilfsbereiter Kumpel, nicht wie ein Support-Agent
- Kurze Sätze (8-15 Wörter Durchschnitt), keine Textblöcke
- KEIN Schema "Begrüßung + Problem bestätigen + Lösung + CTA"
- KEINE Batch-Versendung (nie mehrere DMs zur gleichen Minute)
- KEINE Template-Closer: "Meld dich gerne, falls nochmal was ist"
- Wenn die letzte Nachricht "Danke"/"hat geklappt" war: NICHT antworten
- Bei Bestätigungen reichen 3-5 Wörter: "Ist behoben 😊"

### Rate Limits

- Headless API: ~10-15 Requests/Minute bevor 429 kommt
- Bei 429: 30 Sekunden warten, dann weiter
- Zwischen Replies: 2 Sekunden Pause

## Other Workflows

1. **Member-Frage beantworten:** Read `ref_quick_answers.md` (Top 20 Fragen mit sofortigen Antworten)
2. **Community-Struktur prüfen:** Read `ref_community_structure.md` (Spaces, Courses, Events)
3. **API-Operationen ausführen:** Read `references/ref-api-operations.md` (Admin V2, Headless, interne API)
4. **Tags/Sync verwalten:** Read `references/ref-tag-sync.md` (Tag Management, Stripe Sync, Eskalation)
5. **Spaces/Navigation prüfen:** Read `references/ref-spaces-navigation.md` (Space IDs, Access Groups, UI-Audit)

## API Kurzreferenz

**Admin API V2 Base URL:** `https://app.circle.so/api/admin/v2`
**Auth:** `Authorization: Token $CIRCLE_ADMIN_API_KEY` (NICHT Bearer!)
**Headless API Base URL:** `https://app.circle.so/api/headless/v1`
**Auth:** `Authorization: Bearer $JWT` (JWT via auth_token Endpoint)
**Rate Limit:** Admin 60 req/min, Headless ~15 req/min. **Community ID:** 346419

```bash
# .env laden
CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)
```

## Mentions in Kommentaren

```html
<a class="mention" href="https://strongeryou.circle.so/u/{public_uid}" target="_blank" rel="noopener noreferrer">Vorname Nachname</a>
```
Kein `@`-Zeichen nötig. Die `mention`-CSS-Klasse macht den Namen automatisch blau.
Body in `<div><p>...</p></div>` wrappen.

**UID ermitteln (Priorität):**
1. Email aus Comment-User-Objekt, dann `GET /community_members/search?email={email}` (zuverlässigste Methode)
2. `GET /advanced_search?query={Vorname+Nachname}` (gibt public_uid + sgid)
3. ACHTUNG: `GET /community_members?query=` ist BROKEN (ignoriert Suchbegriff)

## Headless API Keys

| Key | Email | Name | Member ID |
|-----|-------|------|-----------|
| `CIRCLE_HEADLESS_MEMBER_API_KEY_NICO` | info@nicojunk.com | Nico Junk | 38688280 |
| `CIRCLE_HEADLESS_MEMBER_API_KEY_NICOL` | nicol@lightnessfitness.de | Nicol Stanzel | 38375437 |

## Funnel & Customer Journey

Die Mitglieder in Circle kommen über verschiedene Wege rein. Diesen Kontext brauchst du, um Fragen richtig einzuordnen und korrekt zu beantworten.

### Produkte & Funnel

```
Instagram/Ads → nicolstanzel.com (7-Tage-Plan Freebie)
    → 4leads Follow-Up-Sequenz
    → Angebot: BodyGuide (97 EUR, einmalig) oder StrongerYou X.0 (497 EUR, 6 Wochen)

StrongerYou X.0 (6-Wochen-Coaching):
    → Circle: X.0 Spaces (Kurs, Chat, Live-Coaching Di 18:30)
    → Nach 6 Wochen: Upsell zu Connect (dauerhafte Mitgliedschaft)
    → X.0-Absolventinnen bekommen BodyGuide-Gutschein bei Connect-Buchung

Connect (Abo-Modell, dauerhaft):
    → Circle: Community, Live-Trainings Mo+Do, Video Library, Challenges
    → Kann auch direkt gebucht werden (ohne vorher X.0)
    → Regulär: 69 EUR/mo, 468 EUR/yr
    → Aktionspreise variieren (z.B. 59 EUR/mo, 390 EUR/yr bei Promo-Wochen)

BodyGuide (einmalig 97 EUR):
    → Personalisierter Ernährungsplan per E-Mail (PDF)
    → Kein Circle-Zugang, kein Community-Zugang
    → Wird auch als Bonus bei Connect-Aktionen verschenkt
```

### Aktueller Kontext (Stand: März 2026)

- **X.0 Chat wird geschlossen:** Die aktuelle X.0-Runde endet bald. Danach wird der X.0-Chat-Space deaktiviert.
- **Connect-Promo läuft:** X.0-Absolventinnen werden aktiv zu Connect eingeladen (Aktionspreis + BodyGuide-Gutschein).
- **Häufige Fragen daher:** "Was kostet Connect?", "Bekomme ich einen Gutschein?", "Was passiert nach den 6 Wochen?", "Kann ich auch später buchen?"

### Typische Frage-Kontexte

| Frage | Kontext | Antwort-Richtung |
|-------|---------|-----------------|
| "Was kostet Connect?" | X.0-Teilnehmerin überlegt zu wechseln | Reguläre + Aktionspreise nennen, auf Deadline hinweisen |
| "Wo ist mein Gutschein?" | Hat Connect gebucht, BodyGuide-Code nicht erhalten | Code kommt per E-Mail, Spam prüfen, sonst info@nicolstanzel.de |
| "Was passiert nach dem Jahr?" | Überlegt Connect-Jahresabo | Verlängert sich automatisch zum gleichen Preis |
| "Kann ich auch später buchen?" | Will erst X.0 fertig machen | Ja, jederzeit. Aber Aktionspreis nur bis Deadline. |
| "Wo finde ich die Aufzeichnung?" | Hat Live-Event verpasst | Events > Past, oder Video Library |
| "Messaging geht nicht" | Will andere Mitglieder kontaktieren | DMs sind freigeschaltet (seit 07.03.2026). Anleitung: Mitglieder > Name > Nachrichten-Symbol. Falls "Connection required"-Fehler: wurde deaktiviert, App/Browser neu starten. |

## Product Access Matrix

| Bereich | BodyGuide (97 EUR) | Connect (ab 29,97/mo) | X.0 Coaching (497 EUR) |
|---------|:---:|:---:|:---:|
| Community-Feed, Rezepte, Erfolge | -- | Ja | Ja |
| Live-Trainings (Mo+Do 18:00) | -- | Ja | Aufzeichnungen |
| Video Library, Ressourcen | -- | Ja | Ja |
| Challenges & Mini-Challenges | -- | Ja | Ja |
| X.0 Kurs (6 Wochen, 52 Lektionen) | -- | -- | Ja |
| X.0 Chat + Live-Coaching (Di 18:30) | -- | -- | Ja |
| Personalisierter Ernährungsplan | Ja (per E-Mail) | -- | Ja (per E-Mail) |

## Access Group IDs

| ID | Produkt | Spaces |
|----|---------|--------|
| 88537 | StrongerYou X.0 | 6 |
| 78507 | Connect | 21 |
| 72778 | C9 Reset | 2 |
| 71906 | Happy Body Training | 2 |

## Top 5 Support-Fragen (Sofort-Antworten)

**"Ich komme nicht rein"** -> Magic Link: strongeryou.circle.so, Code per E-Mail (Spam prüfen!), Absender: circle.so

**"Alles ist gesperrt / Schlösser"** -> Normal! Lektionen der Reihe nach abarbeiten, "Lesson complete" Button ganz unten drücken. Neue Wochen: Sonntag ~11 Uhr.

**"Wo ist mein BodyGuide?"** -> Zwei Szenarien unterscheiden:
  - *BodyGuide direkt gekauft (97 EUR):* Nach Fragebogen-Ausfüllung auf nicolstanzel.com/bodyguide kommt der Plan in 2-5 Werktagen per E-Mail. Absender: info@nicolstanzel.de, Spam prüfen.
  - *BodyGuide als Connect-Bonus (Gutscheincode):* Code kommt automatisch per E-Mail nach Connect-Buchung. Spam prüfen. Falls nicht da: an info@nicolstanzel.de schreiben. Kontext-Hinweis: Wer im X.0-Chat fragt, ist wahrscheinlich dieser Fall.

**"Ich sehe nicht alle Bereiche"** -> Jede Mitgliedschaft zeigt nur eigene Spaces. Connect != X.0 != BodyGuide. Siehe Access Matrix oben.

**"Was passiert nach 6 Wochen?"** -> Alle Inhalte bleiben dauerhaft erhalten. Eigenes Tempo ist okay.

## Connect Promo & BodyGuide-Gutscheine

- Coupon `bEsGn8vr` (SY3-BodyGuide-Bonus, 100% off BodyGuide)
- Code-Format: `VORNAME-BG-2026`, max_redemptions=1, metadata.customer_email
- Connect Aktionspreis (bis 9.3.2026): 59 EUR/mo, 390 EUR/yr + BodyGuide-Gutschein
- Connect Regulär: 69 EUR/mo, 468 EUR/yr
- Abo verlängert sich automatisch zum gleichen Preis (Aktionspreis bleibt bestehen)
- Bei Kündigung: Zugang endet zum Ende der Laufzeit, kein Zugriff danach
- 4leads Custom Field 15306 (`connect_bodyguide_gutscheincode`): Löst Automation "jdkm" aus -> Auto-E-Mail #51895

## Live-Events

| Event | Wann | Für |
|-------|------|------|
| Power Up Monday | Mo 18:00 | Connect |
| LIVE-Begleitung X.0 | Di 18:30 | X.0 Coaching |
| PowerUp Thursday | Do 18:00 | Connect |
| Specials (BBP, HIIT, Pilates) | Variiert | Alle |

Aufzeichnungen: Events > Past ODER Video Library. Im Browser: "Video", in der App: "Watch recording".

## Email Support: Entscheidungsbaum

| Kategorie (Anteil) | API Check | Aktion |
|---------------------|-----------|--------|
| Zugangs-Probleme (40%) | GET /community_members/search?email=... -> Tags + Spaces prüfen | Fix + Anleitung |
| FAQ (35%) | Knowledge Base / Headless Search | Antwort senden |
| Technische Probleme (15%) | Member-Status prüfen | Troubleshooting oder Eskalation an Nico |
| Kündigung/Refund (5%) | Tags prüfen (Coaching?) | SOFORT an Nicol eskalieren |
| Unklare Anfragen (5%) | Kontext holen | An Nicol mit Kontext eskalieren |

**Eskalation SOFORT bei:** ALL-CAPS, "Anwalt"/"Betrug", Coaching-Abos (179/97/189 EUR), Datenschutz, Mehrfach-Beschwerden.

## Content Visibility Regeln

- ALLE Spaces: `is_hidden_from_non_members: true`
- Zugang nur über Access Groups (kein manuelles Space-Hinzufügen)
- Historische direkte Mitgliedschaften bereinigen (Freigabe von Nicol nötig)
- Space-zu-AccessGroup Config nur im Admin UI, nicht per API

## Reference Files

| Datei | Inhalt | Wann laden |
|-------|--------|------------|
| `ref_quick_answers.md` | Top 20 Fragen mit Copy-Paste Antworten | Bei Member-Support |
| `ref_community_structure.md` | Spaces, Courses, Events Struktur | Bei Plattform-Fragen |
| `references/ref-api-operations.md` | Admin V2 + Headless + interne API Endpoints | Bei API-Calls |
| `references/ref-tag-sync.md` | Tag Management, Stripe Sync, Eskalation | Bei Tag/Sync-Aufgaben |
| `references/ref-spaces-navigation.md` | Space IDs, Access Groups, UI-Audit | Bei Space/Navigation-Fragen |
| `references/ref-circle-pages-api.md` | Circle Pages Site Builder API | Bei Pages-Aufgaben |
| `references/ref-current-launch.md` | Aktuelle Preise, Promotions, FAQ für laufenden Launch | Bei Notifications beantworten, Member-Support |

## Bekannte Probleme

1. **Circle-E-Mails im Spam:** GMX, Web.de, AOL klassifizieren circle.so als Spam
2. **App vs. Browser:** Aufzeichnungs-Button heisst "Video" (Browser) vs. "Watch recording" (App)
3. **Einladungslinks:** Laufen ab, werden von E-Mail-Clients umgeschrieben
4. **Body Circles schwer findbar:** Pfad: Ressourcen > Hilfreiche Ressourcen > Training > Body Circle Guide
5. **Drip-Content Verwirrung:** Neue Woche nur wenn ALLE Lektionen completed UND Sonntag
6. **Historische Space-Mitgliedschaften:** Alt-Member sehen zu viele Spaces (Bereinigung offen)

## Supabase Sync

Täglicher Sync via n8n Workflow `QjU5fCfYNyl4DJa3` (08:00 UTC).
9 Tabellen: members, posts, comments, events, spaces, space_members, tags, courses, lessons.
