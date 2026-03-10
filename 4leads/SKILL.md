---
name: 4leads
description: >
  Complete 4leads CRM system expertise: email editing (Unlayer editor), automation design, contact management,
  tags, forms, custom fields, follow-up funnels, newsletter campaigns, and API integration. Use this skill
  whenever working with 4leads in any capacity: editing or creating email templates, fixing placeholder
  variables, building or debugging automations, looking up tags or custom field IDs, managing contacts,
  configuring webhooks, integrating 4leads with n8n/Stripe/Circle, creating or sending newsletter campaigns,
  setting up tag-based audience segmentation, or auditing existing workflows. Triggers on: 4leads, email
  editor, unlayer, email template, email bearbeiten, email erstellen, placeholder, custom field, field_,
  automation, follow-up funnel, tag management, CRM tag, formular, process, e-mail-marketing, newsletter
  erstellen, newsletter kampagne, newsletter versenden, segmentierung, tag-filter, empfänger auswählen,
  newsletter konfigurieren, broadcast, mailing.
---

# 4leads CRM — Unified System Reference

Complete reference for the 4leads CRM system of Lightness Fitness / StrongerYou.
Covers emails, automations, contacts, tags, forms, custom fields, and integrations.

## System Overview

- **4leads** = E-Mail-CRM mit Automations, Tags, Formularen, Follow-Up Funnels, Unlayer Email-Editor
- **~28.000 Kontakte**, 55+ Tags, 16 Automations, 5 Follow-Up Funnels, 84+ E-Mail Templates
- **REST API:** `https://api.4leads.net/v1` with Bearer Token (`FOURLEADS_API_KEY`, format `4l.xxx`)
- **Internal Web API:** Cookie-based at `app.4leads.net` (session expires every 20min, keepalive: `GET /heartbeat?xhr=1`)
- **Rate Limit:** 1 call / 1.5s on REST API; 429 → sleep(3) + retry
- **Browser Access:** ALWAYS use `playwright-cli` (persistent profile, logged in), NEVER Playwright MCP server

## The #1 Mistake: Placeholder Syntax

4leads custom fields use `{{field_XXXXX}}` with the **numeric field ID**, not the human-readable name.
Getting this wrong means customers see raw text like `{{connect_bodyguide_gutscheincode}}` instead of their actual promo code.

| Human-readable name | Field ID | Correct placeholder |
|---------------------|----------|-------------------|
| connect_promo_monatlich | 15301 | `{{field_15301}}` |
| connect_fenster_ablauf | 15302 | `{{field_15302}}` |
| connect_promo_jaehrlich | 15303 | `{{field_15303}}` |
| connect_fenster_ablauf_text | 15305 | `{{field_15305}}` |
| connect_bodyguide_gutscheincode | 15306 | `{{field_15306}}` |

Standard placeholders that work by name: `{{firstname}}`, `{{lastname}}`, `{{email}}`, `{{contactCenter}}`, `{{unsubscribe}}`, `{{disclaimer}}`

To look up unknown field IDs: navigate to `https://app.4leads.net/contacts/fields` via playwright-cli, or read `references/contact-schema.json`.

## Email Editing (Unlayer Editor)

4leads uses Unlayer (editor.unlayer.com) as a cross-origin iframe email editor.
The `window.unlayer` global on the **parent page** provides the API. Direct iframe DOM access fails (cross-origin).

### Quick Workflow: Edit an Email

```bash
# 1. Navigate to editor
playwright-cli goto "https://app.4leads.net/email-funnel/email/edit/e/{hash}"
# Wait 3-5s for Unlayer to load

# 2. Export current design as JSON
playwright-cli eval "() => new Promise(resolve => window.unlayer.saveDesign(design => resolve(JSON.stringify(design))))"

# 3. Modify in Python (find/replace on serialized JSON)
# python3 -c "import json; d=open('/tmp/design.json').read(); d=d.replace('OLD','NEW'); open('/tmp/fixed.json','w').write(d)"

# 4. Load modified design (for large JSON, use run-code with fs.readFileSync)
playwright-cli eval "() => { const d = PASTE_JSON; window.unlayer.loadDesign(d); return 'loaded'; }"

# 5. Save
playwright-cli click e203  # "Speichern" in Unlayer toolbar

# 6. Handle beforeunload when navigating away
playwright-cli dialog-accept
```

### Email Settings (outside the iframe)

| Setting | Ref | Notes |
|---------|-----|-------|
| Subject line | e140 | textbox |
| Internal name | e147 | textbox |
| Tags on open | e160 | textbox |
| Tags on click | e168 | textbox |
| Save settings | e173 | button "speichern" (separate from Unlayer save!) |

### eval Syntax Rules

- Arrow function required: `() => expression`, not bare `document.title`
- Promises for callbacks: `() => new Promise(resolve => window.unlayer.saveDesign(d => resolve(...)))`
- Large JSON: use `run-code` with `fs.readFileSync` instead of inline eval

### Common Pitfalls

1. **Stale refs** after navigation: always take fresh snapshot
2. **Cross-origin iframe**: `contentDocument` returns null; use `window.unlayer` only
3. **beforeunload**: 4leads shows "Website verlassen?" dialog; run `dialog-accept` immediately
4. **Two save buttons**: e173 = settings, e203 = email content (Unlayer)

## Automations

### Architecture

Automations are tag/event-driven workflows: Trigger → Actions → Conditions → Actions.
Created in the Automation Builder at `/processes/cockpit/edit/{hash}`.

### Key Trigger Types

| Trigger | Code | Use case |
|---------|------|----------|
| Tag added | 11000 | Purchase events, segmentation |
| Form submission | 14000 | Freebie, webinar registration |
| Webhook | 17000 | External (n8n, Webinarjam) |
| Tag removed | 11500 | Status changes |
| Date field | 16100 | Time-based flows |
| Smartlink clicked | 160000 | Engagement tracking |
| Birthday | 16200 | Annual triggers |

### Key Action Types

| Action | Use case |
|--------|----------|
| Send email (24000) | Core of every automation |
| Add/remove tags (26000/26500) | Segmentation, status |
| Set field value (190000) | UTM, URLs, custom fields |
| Start/stop follow-up (27000/27500) | Sequence management |
| Condition/if-else (200) | Branch by tag/field/activity |
| Wait (99) | Time delays (min/hrs/days) |
| Webhook (50000) | n8n/Make integration |
| Distribute (300) | A/B split testing |

### Current Automations (16)

| Hash | Name | Trigger | Status |
|------|------|---------|--------|
| jdkm | Connect Kauf - BodyGuide Gutscheincode Auto-Versand | Tag: connect-annual/connect-monthly | Aktiv |
| mBJ5 | Freebie x TW (1-2) | Form: 7-Tage-Challenge | Aktiv |
| 8VlR | Freebie x TW (2-2) | Tag: TW gekauft | Aktiv |
| NPMa | Webinarkampagne Webinarjam | Form: Workshop Webinarjam | Aktiv |
| Zxog | Webinarkampagne Everwebinar | Form: Workshop Everwebinar | Aktiv |
| 4G3g | Webinarkampagne Legacy | Form: Launch Workshop | Aktiv |
| qlJ7 | Direktreg. Webinarjam | Webhook | Aktiv |
| 1oBA | Webinar Teilnahme | Webhook | Aktiv |
| lxnQ | Manuell Step 2 | Webhook | Aktiv |
| 5ZlK | Manuell Step 1 | Tag: Webinarreg. manuell | Aktiv |
| A3Xe | SYX.0 Willkommens-E-Mail | Tag: SYX.0 gekauft | Aktiv |
| g5lE | Evergreen Funnel - Webinar Automation | — | Bearbeitung |
| ejMX | Evergreen Funnel - Freebie Start | — | Bearbeitung |
| 1o4o | LOESCHEN - Evergreen Funnel - Freebie Start | — | Bearbeitung |
| 5ZeG | Evergreen Funnel - Follow-Up (2-2) | — | Bearbeitung |
| rL52 | Evergreen Funnel - Follow-Up (1-2) | — | Bearbeitung |

### Connect BodyGuide Automation (jdkm) — Deep Dive

This automation was the source of the placeholder bug fixed on 2026-03-07:

```
Trigger: Tag connect-annual OR connect-monthly added
  │
  ▼
Condition: "BodyGuide Gutscheincode vorhanden" (field_15306 set?)
  ├── YES → Send email #51895 (5OLR) "Connect Kauf | Auto | BodyGuide Gutscheincode Willkommen"
  │         Uses {{field_15306}} for promo code + Stripe checkout link
  └── NO  → (end, wait for n8n to set the field, then re-trigger)
```

The n8n workflow `SBQlqibf7jzkFInX` creates the Stripe promo code and sets field_15306.

## Contacts & Tags

### REST API Endpoints

```bash
BASE=https://api.4leads.net/v1
AUTH="Authorization: Bearer $FOURLEADS_API_KEY"

# Upsert contact (creates or updates by email)
POST $BASE/contacts  {"email":"x@y.de", "fname":"Name", "fields":{"15306":"CODE"}}

# Search by email
POST $BASE/contacts/search  {"email":"x@y.de"}  # returns HTTP 201 (not 200!)

# Set custom field
PUT $BASE/contacts/{id}/global-field-values/{field_id}  {"value":"..."}

# Tag operations — REST API Tag assignment does NOT persist!
# Use n8n fleads Node instead (Credential: PzZd7uq7Kum2G6zQ)
# DELETE $BASE/contacts/{id}/tags/{tag_id}  ← this works for removal

# Tag CRUD
POST $BASE/tags  {"name":"tag-name"}
DELETE $BASE/tags/{id}
```

### Tag Categories (55+ tags)

| Category | Count | Top tag (contacts) |
|----------|-------|--------------------|
| Newsletter | 1 | Newsletter (7.735) |
| Lead Capture | 1 | Lead: 7-Tage-Challenge (7.487) |
| Webinar Registration | 9 | zum Webinar registriert (5.274) |
| Webinar Attendance | 5 | am Workshop teilgenommen (2.355) |
| Purchase | 8 | BODY GUIDE Kaeufer (633) |
| Subscription | 14 | Abo_39,00EUR_monatlich (74) |
| Connect | 5 | connect-annual (48) |
| Internal | 3 | INT SY26 FU NORM (2.975) |
| Import | 3 | Import_Typeform (1.232) |

### Forms (4 active, all single opt-in)

| Hash | Name | Registrations | Triggers |
|------|------|---------------|----------|
| R2Wv | Lead: 7-Tage-Challenge | 6.175 | Freebie x TW (mBJ5) |
| M20A | Workshop Webinarjam | 6.730 | Webinarkampagne WJ (NPMa) |
| xYde | Workshop Everwebinar | 980 | Webinarkampagne EW (Zxog) |
| ogXk | Launch Workshop (legacy) | 34 | Legacy (4G3g) |

## Integration Patterns

### n8n fleads Node (Credential: PzZd7uq7Kum2G6zQ)

This is the ONLY reliable way to assign tags (REST API tag assignment silently fails).

```js
// Tag assignment via n8n
{ resource: "contact", operation: "addATag",
  contactId: {__rl: true, value: "={{$('Node').item.json.data.id}}", mode: "id"},
  bListOfTags: true, contactTagIdList: "={{ [TAG_ID] }}" }

// Custom field via n8n
{ resource: "contact", operation: "setValue",
  globalFieldContactId: {__rl: true, value: "={{id}}", mode: "id"},
  bSetMultiFields: true,
  fieldsToSet: {field: [{globalFieldId: {__rl: true, value: FIELD_ID, mode: "id"}, value: "..."}]} }
```

### 4leads → n8n → External System

```
4leads Automation:
  Trigger: Tag added
  Action: Webhook to n8n URL
  Body: { contact_email, tag_name, timestamp }
n8n: Process + write to Airtable/Stripe/Circle
```

### Internal Web API (cookie-auth via playwright-cli)

| Action | Method | URL |
|--------|--------|-----|
| List emails | GET | `/email-funnel/email?pageNum=0&pageSize=25` |
| Email detail | GET | `/email-funnel/email/detail/e/{hash}?xhr=1` |
| Email preview | GET | `/editor/email/preview/e/{hash}` |
| Load editor | POST | `/editor/email/load` body `{id:"HASH"}` |
| Automation list | POST | `/processes/ajax` body `action=search&pageNum=0` |
| Automation detail | GET | `/processes/cockpit/edit/{hash}?xhr=1` |
| Select tags | GET | `/select/tags` |
| Select fields | GET | `/select/global-fields` |
| Contact detail | GET | `/contacts/details/c/{hash}?xhr=1` |
| Heartbeat | GET | `/heartbeat?xhr=1` (call every <20min) |

Append `?xhr=1` to any page URL to get JSON instead of HTML.

## Known Issues

1. **REST API tag assignment silently fails**: PUT returns 200 but tag is not persisted. Use n8n fleads node.
2. **No `/global-fields` list endpoint**: Custom fields only visible in UI or via `GET /select/global-fields`
3. **Tag duplicate**: "Abo_299,00EUR_jaehrlich" exists twice (#43276 with 7, #43282 with 0 contacts)
4. **Naming inconsistency**: Some tags use underscore (SY2.0_gekauft), others use spaces (SY3.0 gekauft)
5. **Legacy form ogXk**: Only 34 registrations, can be archived
6. **Missing forms**: No dedicated form for BodyGuide purchases or SY Connect

## Newsletter Campaigns (playwright-cli)

Newsletter-Kampagnen werden über die 4leads-UI erstellt. Es gibt keinen API-Endpoint dafür.
Der Workflow besteht aus 5 Phasen. Für die vollständige SOP mit allen Code-Snippets: `references/newsletter-sop.md`.

### Kurzablauf

1. **Design exportieren:** Referenz-E-Mail im Editor öffnen, `window.unlayer.saveDesign()` → JSON-Datei
2. **Segment-E-Mails generieren:** Python-Script ändert den Text-Body im NL03-Template (4 Rows)
3. **Designs hochladen:** localStorage-Transfer (base64) → `loadDesign()` → `.fl-e-save` klicken
4. **Newsletter konfigurieren:** 4-Schritt-Wizard (Einstellungen → Empfänger → E-Mail → Prüfen)
5. **Verifizieren:** Design per eval prüfen, Newsletter-Übersicht kontrollieren

### Kritische Gotchas

**selectize.js (Tag-Auswahl in Empfänger-Schritt):**
- Nach JEDER Tag-Auswahl werden alle Element-Refs ungültig. IMMER frischen Snapshot nehmen.
- Kurze Suchbegriffe verwenden ("connect" statt "connect-annual"), sonst findet das Dropdown nichts.
- Vorheriges Dropdown kann nächstes Feld überlagern: erst `playwright-cli press Escape`, dann weiter.

**Design-Upload für große JSON (>5KB):**
- Inline eval scheitert an Shell-Escaping. IMMER den localStorage-Transfer-Pfad nutzen:
  Python → base64 → Datei → `cat` in eval → localStorage → zweiter eval → `atob` → `loadDesign()`

**beforeunload Dialog:**
- 4leads zeigt "Website verlassen?" beim Navigieren weg vom Editor.
- Lösung: `playwright-cli run-code "async page => { page.on('dialog', d => d.accept()); await page.goto('...'); }"`

**Zwei Save-Buttons:** Settings-Save (button "speichern" auf der Seite) vs. Unlayer-Save (`.fl-e-save` im Editor-iframe)

### Segmentierungs-Logik

| Filter-Sektion | Logik | Beispiel |
|---------------|-------|---------|
| "mindestens einen dieser Tags" | OR | connect-annual ODER connect-monthly |
| "alle dieser Tags" | AND | SYX.0 gekauft UND Newsletter |
| "mindestens einen nicht" (Nicht markiert) | Exclude | Hat SYX.0 gekauft NICHT |

### Standard-Template: NL03 (Hash G3o6)

4-Row-Struktur: Banner-Image, Text-Body (Open Sans 16px, line-height 140%), Social Icons, Footer.
CTA-Links sind inline im Text, kein separater Button. Link-Farbe: `#7A94CC`.

## Marketing Funnel Übersicht (Kontext immer verfügbar)

```
Instagram/Ads → Freebie (7-Tage-Plan) → Tag "Lead: 7-Tage-Challenge"
  → Automation mBJ5: Welcome-E-Mail + Bedingung TW gekauft?
      NEIN → FU xNNV (Freebie x Tripwire, 3 Tage)
      JA   → Automation 8VlR: TW-Welcome, FU stoppen

Webinar-Registrierung → Automation NPMa/4G3g/Zxog
  → Bestätigung + FU AMMQ/W6EN/mJJq (6 Steps: 3T vor bis 1T nach)

X.0 Kauf (497 EUR) → Automation A3Xe
  → Welcome-E-Mail + nach 42 Tagen: Connect Upsell FU ex8M

X.0 Abschluss → Automation rL52
  → Wenn nicht Connect: FU BAMb starten (3 Steps, Connect Upsell)

Connect-Kauf → Automation 5ZeG (FU BAMb stoppen)
            → Automation jdkm (BodyGuide-Code wenn CF 15306 leer)
```

**Vollständige Funnel-Doku:** `~/Desktop/Project/marketing-funnel/`
- `README.md` — Architektur-Übersicht
- `automationen/alle-automationen.md` — Alle 16 Automationen mit Steps
- `follow-ups/alle-follow-ups.md` — Alle 11 Follow-Ups mit E-Mail-Sequenzen

## Reference Files

| File | Content | When to load |
|------|---------|--------------|
| `references/triggers.md` | All 32 trigger types in 5 categories | When designing automations |
| `references/actions.md` | All 34 action types + conditions + flow diagrams | When designing automations |
| `references/automations-map.md` | All automations with complete step details | When auditing/debugging flows |
| `references/missing-automations.md` | 9 recommended new automations with priorities | When planning new automations |
| `references/campaigns-api.md` | 15 internal API endpoints, all email/newsletter hashes | When doing API work or looking up emails |
| `references/email-hashes.md` | Quick lookup table for email templates by category | When finding a specific email to edit |
| `references/unlayer-design.md` | Unlayer JSON structure and modification patterns | When making targeted edits to email design JSON |
| `references/contact-schema.json` | 17 standard + 27 custom fields with IDs | When working with contact data |
| `references/tags-summary.md` | All 55+ tags by category with IDs and counts | When working with tags |
| `references/tags-list.json` | All tags as JSON for programmatic access | When building automations |
| `references/forms-map.md` | 4 forms with details, hashes, triggers | When working with forms |
| `references/airtable-integration.md` | 5 recommended tables, webhook patterns, n8n workflows | When planning Airtable integration |
| `references/newsletter-sop.md` | Step-by-step SOP for creating segmented newsletter campaigns | When creating newsletters with playwright-cli |
