# Circle Workflows Dokumentation
Stand: 2026-03-08 (aktualisiert: CRM-Sync Phase 2 Erkenntnisse)

## Legacy-Tag Workaround (Stand 2026-03-08)

Die 4 Legacy-Workflows (connect-monthly-legacy, connect-annual-legacy added/removed → Access Group Connect) sind **noch nicht implementiert**. Als Workaround wird der Umbrella-Tag `202343` verwendet:
- Legacy-Kunden (connect-monthly-legacy=230680, connect-annual-legacy=230679) erhalten zusätzlich den Umbrella-Tag `202343` (Connect-Zugang über bestehende Workflows)
- Die 4 geplanten Legacy-Workflows sind als "ausstehend" markiert und können über Circle UI erstellt werden: Trigger "Mitglied-Tag hinzugefügt" → Aktion "Zugangsgruppe hinzufügen (Connect 78507)"

## Workflow-Typen

Circle unterstützt drei Typen:
- **Automation** – Event-Trigger, läuft automatisch bei Ereignis
- **Bulk action** – Manuelle Auswahl einer Zielgruppe, sofortige Ausführung
- **Scheduled** – Wie Bulk action, aber zeitgesteuert (einmalig oder wiederkehrend)

---

## Verfügbare Trigger (Automation)

### Members
- Joined community
- Profile field updated
- Changed email
- Member leveled up
- Member leveled down

### Events
- RSVP'd to event
- RSVP'd to recurring event
- Event ended for member
- Event starts in an hour
- Published an event
- Attended live event

### Access Groups
- Added to access group
- Removed from access group

### Spaces
- Joined space
- Removed from space

### Space Groups
- Joined space group
- Removed from space group

### Paywalls
- Charged for a paywall
- Subscribed to paywall
- Subscription scheduled to cancel
- Trial scheduled to cancel
- Subscription canceled
- Subscription resumed
- Trial resumed
- Installment completed
- Trial ended and not converted
- Trial converted
- Trial started
- Coupon used at checkout
- Coupon added
- Coupon removed
- Coupon ended
- Failed recurring payment
- Subscription changed

### Tags
- **Tag added** ← für CRM-Sync relevant
- **Tag removed** ← für CRM-Sync relevant

### Posts & Comments
- Published a post
- Posted a comment
- Liked a post

### Moderation
- Post was flagged / approved / rejected
- Comment was flagged / approved / rejected

### Courses
- Completed course / lesson / section
- Passed quiz / Failed quiz / Submits quiz

### Forms
- Form submitted

### Messaging
- Admin received a direct message

---

## Verfügbare Actions

### AI Actions (5.000 Credits kontingent)
- Agent comments on post
- AI reports post / comment
- AI edits topics
- AI renames post title
- Agent sends direct message

### Communication
- Send an email
- Send a direct message
- Send mobile push notification
- Unsubscribe from email marketing

### Tags
- Add tag
- Remove tag

### Members
- Remove member(s) from community
- Enable / Disable direct messaging

### Space / Space Groups
- Add / Remove member(s) to/from space
- Add / Remove member(s) to/from space group

### Access Groups
- Add member(s) to access group
- Remove member(s) from access group

### Webhook
- **Send to webhook** ← für n8n/Make.com Integration

### Paywalls
- Cancel subscription at period end / immediately
- Subscribe to paywall trial
- Add / Remove coupon from subscription
- Change subscription

### Posts
- Edit post settings

### Events
- RSVP or invite member(s) to event

### Flow
- Time delay

### Gamification
- Reward points

---

## Aktive Workflows (Stand 2026-03-08)

### Connect-relevante Workflows (CRM-Sync kritisch)

| Name | UUID | Trigger | Actions | Runs |
|------|------|---------|---------|------|
| Connect Tag->Add to Access + Space Groups | c9a4460b-445a-42e4-a8fa-b111b0a1710f | Tag added: "Connect" | Add to Access Group "Connect" + 2x Add to Space Group | 34 |
| connect-monthly->Access+Space Groups | 5292bfc8-3b93-4432-ba9a-fb37529f1b07 | Tag added: "connect-monthly" | Add to Access Group + 2x Space Group | 3 |
| connect-annual->Access+Space Groups | (UUID nicht bekannt) | Tag added: "connect-annual" | Add to Access Group + Space Groups | 34 |
| Connect Tag removed->Remove member from Access Group Connect | (UUID nicht bekannt) | Tag removed: "Connect" | Remove from Access Group "Connect" | 50 |
| New Connect TAG->Add member to Access Group Connect | (UUID nicht bekannt) | Tag added: (Connect-Tags) | Add to Access Group "Connect" | 156 |
| Goldstatus->Connect Access Group | (UUID nicht bekannt) | Tag added: "Goldstatus" | Add to Access Group "Connect" | 2 |

### Webhook-Workflows (externe Integration)

| Name | Trigger | Zweck | Runs |
|------|---------|-------|------|
| Joined Community->Send to Webhook | Joined community | Meldet neue Mitglieder an externen Webhook (n8n/Make) | 908 |
| Tag X.0 abgeschlossen->Webhook | Tag added: "X.0 Abgeschlossen" | Webhook bei X.0-Abschluss | 41 |
| SY X.0 Kurs abgeschlossen->Tag-Webhook | Kurs abgeschlossen + Webhook | X.0-Kurs Completion | 58 |

### Kurs-Workflows

| Name | Trigger | Zweck | Runs |
|------|---------|-------|------|
| Tag SY X.0->Access Groups+Spaces | Tag added: "StrongerYou X.0" | X.0-Kursteilnehmer Zugang | 267 |
| Tag StrongerYou 3.0 added->Apply respective Access Group | Tag added: "StrongerYou 3.0" | 3.0-Kursteilnehmer Zugang | 88 |
| Tag Connect->Add to Access Group | Tag added: "Connect" | (ältere Version) | 247 |
| C9 Tag->Assign C9 Access Group+Space | Tag added: "C9 Reset" | C9 Zugang | 40 |
| New C9 Member->Assign C9 Tag | Joined community + Bedingung | C9-Tag setzen | 41 |

### Mini Challenge Loops (lippi)

7 Workflows für Mini-Challenges (Isometrische Übungen, Mini Workout, Abs, Faszienrolle, Stretching, Beckenboden, Xmas Special) – alle aktiv, erstellt von "lippi".

---

## Circle Tags (Stand 2026-03-08)

| Tag | ID | Mitglieder | Zweck |
|-----|-----|-----------|-------|
| connect-monthly | 230678 | 12 | Aktive Monats-Abonnenten |
| connect-annual | 228771 | 99 | Aktive Jahres-Abonnenten |
| connect-monthly-legacy | 230680 | 75 | Legacy-Monats-Abonnenten |
| connect-annual-legacy | 230679 | 48 | Legacy-Jahres-Abonnenten |
| Connect (umbrella) | 202343 | 291 | Alle Connect-Mitglieder (Summe) |
| X.0 Abgeschlossen | 228773 | 43 | X.0-Absolventinnen |
| StrongerYou X.0 | 215031 | 262 | X.0-Kursteilnehmer |
| Goldstatus | 212967 | 2 | Goldstatus-Mitglieder |
| StrongerYou 3.0 | 192239 | 82 | 3.0-Kursteilnehmer |
| StrongerYou 2.0 | 155487 | 176 | 2.0-Kursteilnehmer |
| StrongerYou 1.0 | 155485 | 122 | 1.0-Kursteilnehmer |
| Happy Body Training | 200831 | 867 | HBT-Mitglieder |
| C9 Reset | 199967 | 39 | C9-Teilnehmer |
| customerEmail!=memberEmail | 205363 | 14 | Bekannte Email-Mismatches |
| !!NEEDS_ATTENTION!! | 211109 | 3 | Manuelle Prüfung erforderlich |

---

## Wichtige Erkenntnisse für CRM-Sync

### Bestehende Automation-Logik
Wenn per API ein Connect-Tag gesetzt wird, triggern automatisch die Circle-Workflows:
1. `connect-monthly` Tag -> Workflow fügt Access Group + Space Groups hinzu
2. `connect-annual` Tag -> Workflow fügt Access Group + Space Groups hinzu
3. `Connect` (umbrella) Tag -> weiterer Workflow fügt Access Group hinzu

Das bedeutet: Beim CRM-Sync müssen nur die Tags gesetzt werden. Die Access Groups und Spaces werden von Circle selbst via Workflow verwaltet.

### Lücken / Handlungsbedarf
- `connect-monthly-legacy` und `connect-annual-legacy` haben KEINE eigenen Workflows für Access Groups/Spaces
- Nur der umbrella-Workflow "Connect Tag->Add to Access + Space Groups" würde greifen wenn auch der "Connect" Tag gesetzt wird
- **Empfehlung:** Legacy-Tags ebenfalls in Circle-Workflows berücksichtigen oder sicherstellen, dass Connect-Umbrella-Tag für Legacy gesetzt wird
