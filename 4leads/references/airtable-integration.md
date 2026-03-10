# 4leads <> Airtable Integration — Empfehlungen

**Generated:** 2026-02-22T03:40:00+01:00
**Basis:** 32 Trigger-Typen, 34 Action-Typen, 11 bestehende Automations, 4 Follow-Up Funnels

## Zusammenfassung

4leads hat kein offenes REST-API. Alle Interaktionen laufen über Session-basierte Requests mit Cookie-Auth. Für eine Airtable-Integration müssen wir deshalb den **Webhook-Weg** nutzen: 4leads sendet Daten per Webhook an n8n, n8n schreibt in Airtable (und umgekehrt).

## Empfohlene Airtable-Tabellen

### Tabelle 1: Automations

Spiegel aller 4leads-Automations für Monitoring und Reporting.

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| automation_id | Text (PK) | 4leads Process-Hash (z.B. "8VlR") |
| name | Text | Name der Automation |
| status | Single Select | Aktiv / Bearbeitung / Inaktiv |
| trigger_type | Text | Trigger-Typ-Code (z.B. "11000") |
| trigger_description | Long Text | Menschenlesbare Trigger-Beschreibung |
| step_count | Number | Anzahl Steps |
| linked_followups | Link to Record | Verknüpfung zu Follow-Ups Tabelle |
| linked_emails | Link to Record | Verknüpfung zu Emails Tabelle |
| tags_used | Multiple Select | Verwendete Tags |
| last_synced | Date | Letzter Sync-Zeitpunkt |

**Sync-Strategie:** Manuell oder wöchentlich (Automations ändern sich selten).

### Tabelle 2: Follow-Up Funnels

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| funnel_id | Text (PK) | 4leads Funnel-Hash (z.B. "xNNV") |
| name | Text | Funnel-Name |
| step_count | Number | Anzahl Steps/E-Mails |
| used_by | Link to Record | Verknüpfung zu Automations |
| emails | Link to Record | E-Mails in diesem Funnel |
| last_synced | Date | Letzter Sync |

### Tabelle 3: Automation Emails

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| email_id | Text (PK) | 4leads Email-Hash (z.B. "R0Nl") |
| subject | Text | Betreffzeile |
| used_in_automation | Link to Record | Verknüpfung zu Automations |
| used_in_funnel | Link to Record | Verknüpfung zu Follow-Ups |
| html_backup | URL | Link zum gesicherten HTML (output/emails/) |

### Tabelle 4: Automation Events (Live-Feed)

Wichtigste Tabelle: Echtzeit-Events aus 4leads per Webhook.

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| event_id | Auto Number | Unique ID |
| timestamp | Date | Zeitpunkt des Events |
| contact_email | Email | Kontakt-E-Mail |
| contact_id | Text | 4leads Kontakt-ID |
| event_type | Single Select | tag_added / tag_removed / email_sent / form_submitted / automation_entered / automation_completed |
| automation_hash | Link to Record | Welche Automation |
| tag_name | Text | Bei Tag-Events: welcher Tag |
| metadata | Long Text | Zusätzliche JSON-Daten |

**Sync-Strategie:** Echtzeit per Webhook (4leads -> n8n -> Airtable).

### Tabelle 5: Tags

| Feld | Typ | Beschreibung |
|------|-----|-------------|
| tag_name | Text (PK) | Tag-Name |
| usage | Single Select | trigger / action / segmentation / tracking |
| used_in | Link to Record | Verknüpfung zu Automations |
| contact_count | Number | Anzahl Kontakte mit diesem Tag |
| category | Single Select | Kauf / Registrierung / Tracking / Segmentierung |

## Sync-Strategien

### Push: 4leads -> n8n -> Airtable

**Pattern:** 4leads Webhook-Trigger (type: 17000) oder Smarttap (type: 180000) sendet an n8n-Webhook-URL.

```
4leads Automation:
  Trigger: Tag hinzugefügt (z.B. "SYX.0 gekauft")
  Action 1: [bestehende Aktionen]
  Action 2: Webhook an https://n8n.example.com/webhook/4leads-event
            Body: { contact_email, tag_name, timestamp }

n8n Workflow:
  1. Webhook empfangen
  2. Airtable: Record in "Automation Events" erstellen
  3. Airtable: Kontakt in CRM-Tabelle aktualisieren
  4. Optional: Slack-Benachrichtigung
```

**Vorteil:** Echtzeit, zuverlässig
**Nachteil:** Jede Automation muss um einen Webhook-Step erweitert werden

### Pull: n8n pollt 4leads (NICHT EMPFOHLEN)

4leads hat kein offenes API. Session-basierte Requests sind fragil und brechen bei Cookie-Expiry.
Polling erfordert Browser-Automation oder Session-Management — zu aufwändig.

**Empfehlung:** Nur Push-Pattern verwenden.

### Hybrid: Airtable -> n8n -> 4leads API

Für Aktionen VON Airtable NACH 4leads:

```
Airtable Button/Automation:
  -> Webhook an n8n

n8n Workflow:
  1. Webhook empfangen (E-Mail-Adresse + Aktion)
  2. 4leads API: Tag setzen
     POST https://api.4leads.net/v1/contacts/{id}/tags
     Headers: Authorization: Bearer 4L.{token}
  3. 4leads Automation reagiert auf neuen Tag
```

**Wichtig:** 4leads API URL ist `https://api.4leads.net/v1` (NICHT app.4leads.eu), Bearer Token mit `4L.` Prefix.

## n8n Workflow-Entwürfe

### Workflow A: 4leads Tag Event -> Airtable CRM Update

```
[Webhook] -> [Set Variables] -> [Airtable: Search Contact] ->
  -> IF exists: [Airtable: Update Record] + [Airtable: Create Event]
  -> IF new:    [Airtable: Create Contact] + [Airtable: Create Event]
```

**Trigger:** 4leads sendet Webhook bei Tag-Änderung
**Relevante Tags:** SYX.0 gekauft, TW_Happy Body Training_gekauft, BG_97EUR_gekauft

### Workflow B: Airtable Button -> 4leads Tag setzen

```
[Webhook from Airtable] -> [4leads API: Search Contact by Email] ->
  -> IF found: [4leads API: Add Tag] -> [Airtable: Update Status]
  -> IF not found: [Airtable: Mark "Contact not in 4leads"]
```

**Use Cases:**
- Manuelles Tagging aus Airtable CRM
- Re-Engagement starten (Tag "re-engagement" setzen)
- VIP-Status vergeben

### Workflow C: Täglicher Automation-Status Sync

```
[Cron: 06:00 UTC] -> [HTTP Request: 4leads /processes/ajax] ->
  [Parse HTML] -> [Loop: Each Automation] ->
  [Airtable: Upsert Record in Automations Table]
```

**Hinweis:** Erfordert aktive 4leads-Session (Cookie). Session-Refresh muss eingebaut werden. Empfehlung: Nur wöchentlich ausführen, da Automations sich selten ändern.

### Workflow D: Neuer Kauf -> Multi-System Update

```
[4leads Webhook: Tag "SYX.0 gekauft"] ->
  [Parallel]:
    Branch 1: [Airtable: Update CRM Contact + Create Event]
    Branch 2: [Stripe API: Verify Payment]
    Branch 3: [Circle API: Check Member Status]
    Branch 4: [Slack: Notify Team]
```

## Implementierungs-Reihenfolge

| Prio | Schritt | Aufwand | Beschreibung |
|------|---------|---------|-------------|
| 1 | Airtable Tabellen erstellen | 1h | 5 Tabellen mit Feldern und Relations |
| 2 | Bestehende Daten importieren | 30min | 11 Automations + 4 Funnels + 6 Emails + 9 Tags |
| 3 | n8n Workflow A bauen | 2h | Webhook-Empfänger + Airtable-Schreiber |
| 4 | 4leads Automations erweitern | 1h | Webhook-Steps zu 3 wichtigsten Automations hinzufügen |
| 5 | n8n Workflow B bauen | 2h | Airtable -> 4leads Tag-Setter |
| 6 | n8n Workflow D bauen | 3h | Multi-System Kauf-Handler |
| 7 | n8n Workflow C bauen | 2h | Automation-Status-Sync (optional) |

## Wichtige Entscheidungen

### Welche Automations zuerst mit Webhooks erweitern?

1. **StrongerYou X.0 Willkommens-E-Mail [A3Xe]** — Jeder Kauf sollte in Airtable landen
2. **Freebie x TW (2-2) [8VlR]** — Jeder Tripwire-Kauf sollte getrackt werden
3. **Freebie x TW (1-2) [mBJ5]** — Jede neue Freebie-Anmeldung ist ein neuer Lead

### Webhook-Body Format (Empfehlung)

```json
{
  "event": "tag_added",
  "tag": "SYX.0 gekauft",
  "contact": {
    "email": "{{contact.email}}",
    "first_name": "{{contact.first_name}}",
    "last_name": "{{contact.last_name}}"
  },
  "automation": {
    "hash": "A3Xe",
    "name": "StrongerYou X.0 Willkommens-E-Mail"
  },
  "timestamp": "{{now}}"
}
```

### Airtable Base-Struktur

Empfehlung: Eigener Airtable Base "4leads Automation Hub", getrennt vom CRM-Base.
Verknüpfung zum CRM über E-Mail-Adresse als gemeinsames Feld.

## Risiken & Hinweise

1. **4leads hat kein offenes API** — Session-basierte Requests sind fragil
2. **Webhook-URLs** in 4leads enthalten Zugriffsschlüssel — sicher aufbewahren
3. **Rate Limits** der 4leads API sind unbekannt — konservativ starten
4. **Cookie-Expiry** der Browser-Session (~20 Minuten) — kein Langzeit-Polling möglich
5. **Automations NICHT deaktivieren** beim Erweitern — immer "Bearbeitung" Modus nutzen
6. **4leads API korrekte URL:** `https://api.4leads.net/v1` — Bearer Token mit `4L.` Prefix
