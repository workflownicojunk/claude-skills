---
name: gmail-workflow
description: >
  Orchestrated multi-agent email support workflow for StrongerYou / Lightness Fitness.
  Use this skill whenever the user mentions: email, support, inbox, process inbox,
  refund, Widerruf, Erstattung, cancellation, Kündigung, body guide, BodyGuide,
  PDF validieren, PDF senden, Entwürfe, Drafts, Circle access,
  login problem, Zugang, Ratenzahlung, coaching cancellation, Doppelabbuchung,
  Stripe payment issue, Zahlungsproblem, or wants to work through customer support emails.
  Replaces email-support-agent. Runs five specialized agents in sequence:
  Triager (bulk fetch + categorize + draft inspection), Validator (Stripe/Circle lookup),
  BodyGuide-Validator (Gemini PDF QA, only when drafts contain PDFs),
  Responder (writes HTML replies in Nicol's voice), Executor (sends + PDF delivery + batch cleanup).
---

# Gmail Workflow (Orchestrator)

**Session-Start:** Immer zuerst `references/ref-learnings-log.md` lesen.

## Autonomie-Prinzip

Dieser Workflow arbeitet VOLLSTÄNDIG AUTONOM. KEINE Drafts, KEINE Eskalation. Jede E-Mail wird direkt beantwortet und gesendet.
Profit ist das EINZIGE Ziel. Jeder kreative Hebel ist erlaubt, um Umsatz zu halten oder zu steigern.
Einzige Ausnahme: Bei drohendem Chargeback/Dispute lieber nachgeben als das Risiko eingehen.

## Gmail Setup

Server: `gmail-nicolstanzel` via gws CLI (info@nicolstanzel.de). NIEMALS `gmail-lightnessfitness`.
Labels: Support = `Label_3955183308810104764`, Kündigung = `Label_7235028904381884705`.

## Harte Business Rules

1. **Max 1 E-Mail pro Kunde pro Tag**
2. **Coaching-Ratenzahlungen (97/179/189/349 EUR) NIEMALS kündigen**. Reframing senden, Wert betonen.
3. **Refund-Anfragen: Reframing AUTO-SENDEN.** Kein Refund ohne Stripe-Verifizierung.
4. **Profit = EINZIGES Ziel.** Jeder kreative Hebel erlaubt.
5. **Chargeback-Vermeidung:** Bei Dispute-Drohung: Problem lösen wenn möglich, sonst erstatten.
6. **Gesundheitsfragen: Kurze Bestätigung AUTO-SENDEN.** Kein medizinischer Rat. Bei Medikamenten: Arzt empfehlen.
7. **NUR versprechen was SOFORT ausgeführt wird.** Kein "innerhalb 24h", kein "ich rufe dich an".
8. **Circle-Zugang selbst freischalten** wenn Stripe-Zahlung bestätigt ist.
9. **Keine internen Systemnamen** in E-Mails (Stripe, Supabase, n8n, Circle API, 4leads).
10. **KEINE unbegründeten Annahmen.** Kundenbehauptungen nicht bestätigen ohne Datenprüfung.
11. **NICHTS anbieten was nicht sofort ausführbar ist.** Kein Rückruf, kein Termin.
12. **System-Benachrichtigungen (PayPal, Stripe, no-reply) nur archivieren.** NICHT beantworten.
13. **NIEMALS entschuldigen.** Kein "Tut mir leid", kein "Entschuldigung". Einfach die Lösung liefern.

## Duplikat-Schutz

Triager-Agent prüft automatisch gegen sent_24h. Wenn E-Mail-Adresse in sent_24h vorkommt: Kategorie `duplicate`, nur archivieren.

## Produkt-Typen

| Typ | Produkt | Preis | Kündbar? |
|-----|---------|-------|----------|
| A | Happy Body Training | 27 EUR | Nein (Widerruf erloschen) |
| A | Body Guide | 97 EUR | Nein (Widerruf erloschen) |
| A | StrongerYou X.0 | 497 EUR | Nein (Widerruf erloschen) |
| B | Coaching-Raten (X.0, 3.0) | 97/179/189/349 EUR/Mo | NIEMALS (Ratenzahlung) |
| C | Connect monatlich | 39/59/69 EUR/Mo | Ja, zum Laufzeitende |
| C | Connect jährlich | 299/390/468 EUR/Jahr | Reframing, Laufzeitende |

## Kommunikationsstil

**VOR dem Schreiben JEDER Antwort:** Lade `~/.claude/projects/-Users-nicojunk-Desktop/memory/topic-nicol-voice.md`. Dieses File enthält die vollständige Nicol-Tonalitätsreferenz mit Few-Shot Examples für Support-Emails.

- Du-Ansprache, Vorname. 2-5 Sätze (VARIIERT die Länge, nicht immer 3).
- HTML-Format. Kurze Absätze (1-2 Sätze), Leerzeilen dazwischen.
- Keine Bullet Points, keine Listen.
- Nicols Stimme: warm, direkt, selbstbewusst. Reagiere ZUERST auf das was die Person geschrieben hat, DANN löse das Problem.
- Jede Email muss sich anders lesen. Keine zwei Emails mit identischer Struktur im selben Batch.
- VERBOTEN: "Tut mir leid", "Entschuldigung", "Ich verstehe dich", "Kein Problem", Em-Dashes, Emojis, Systemnamen, identische Formulierungen über mehrere Emails.
- Umlaute korrekt: ä, ö, ü, ß. NIEMALS ae, oe, ue, ss.

**Signatur (IMMER):**
```html
<p>Herzliche Grüße<br>Nicol</p>
<p><em>Nicol Stanzel</em><br><em>Gesundheitscoach &amp; Ernährungsberaterin</em><br><em>Lightness Fitness</em></p>
```

## Entscheidungsbaum

```
E-Mail eingehend
  |
  +-- System-Benachrichtigung? (PayPal, Stripe, no-reply)
  |     -> NUR archivieren. NICHT beantworten.
  |
  +-- Chargeback/Dispute angekündigt? (Rückbuchung, Bank einschalten)
  |     -> 1. Problem lösbar? JA: Sofort lösen + Bestätigung AUTO-SENDEN
  |        2. NEIN: Refund via Stripe + Bestätigung AUTO-SENDEN
  |        3. Ton: deeskalierend, nie auf Drohung eingehen
  |
  +-- Rechtliche Drohungen? (Anwalt, Klage, DSGVO, Verbraucherzentrale)
  |     -> Kurze neutrale Antwort AUTO-SENDEN: "Deine Nachricht ist angekommen. Ich schaue mir das an."
  |     -> Kein "melde mich", kein Zeitversprechen.
  |
  +-- Kündigung/Refund?
  |     +-- TYPE_B (Coaching-Raten): Reframing AUTO-SENDEN. NIEMALS kündigen.
  |     +-- TYPE_C monatlich: Reframing, bei Insistieren zum Laufzeitende kündigen
  |     +-- TYPE_C jährlich: Reframing, kein Refund, Laufzeitende
  |     +-- TYPE_A (Einmalkauf): Reframing (Widerrufsrecht erloschen)
  |
  +-- Gesundheitsfrage?
  |     -> Kurze Bestätigung AUTO-SENDEN. Keine medizinische Beratung. Arzt empfehlen.
  |
  +-- Zugang/Login fehlt?
  |     -> Stripe validieren -> Circle freischalten -> Bestätigung AUTO-SENDEN
  |
  +-- BodyGuide-Draft mit PDF-Anhang? (Entwurfsordner)
  |     -> Phase 2.5: Gemini QA-Validierung
  |     -> Bestanden: Executor versendet Draft mit Anhang
  |     -> Nicht bestanden: Draft bleibt, User wird informiert
  |
  +-- BodyGuide FAQ?
  |     -> Direkte Antwort AUTO-SENDEN
  |
  +-- Positives Feedback (OHNE Frage)?
  |     -> Warme Antwort AUTO-SENDEN (2-3 Sätze)
  |
  +-- Positives Feedback MIT Frage?
  |     -> Frage ZUERST beantworten + kurze warme Reaktion
  |
  +-- Unklar?
        -> Bestmögliche Antwort AUTO-SENDEN. Im Zweifel nachfragen statt nichts tun.
```

## Orchestrierungs-Workflow

**IMMER in dieser Reihenfolge (sequentiell). KEINE Phase startet ohne bestandene Validierung der vorherigen Phase.**

---

### Phase 1: Triage
```
Agent(subagent_type="gmail-triager")
```
Fetcht Inbox, kategorisiert alle E-Mails, erstellt Plan.
Output: `/tmp/gmail-triage-result.json`

#### Validierung 1 (Orchestrator, PFLICHT vor Phase 2):

**1a. Strukturvalidierung:**
```python
python3 -c "
import json, sys
t = json.load(open('/tmp/gmail-triage-result.json'))
errors = []
# Pflichtfelder im Root
for key in ['inbox','sent_24h_recipients','plan','archive_ids']:
    if key not in t: errors.append(f'MISSING: {key}')
# Jeder plan-Eintrag braucht thread_id + message_id
for i, p in enumerate(t.get('plan',[])):
    if not p.get('thread_id'): errors.append(f'plan[{i}] ({p.get(\"to\",\"?\")}) MISSING thread_id')
    if not p.get('message_id'): errors.append(f'plan[{i}] ({p.get(\"to\",\"?\")}) MISSING message_id')
    if not p.get('email_id'): errors.append(f'plan[{i}] ({p.get(\"to\",\"?\")}) MISSING email_id')
    if not p.get('category'): errors.append(f'plan[{i}] ({p.get(\"to\",\"?\")}) MISSING category')
if errors: print('TRIAGE VALIDATION FAILED:'); [print(f'  - {e}') for e in errors]; sys.exit(1)
else: print(f'TRIAGE OK: {len(t[\"plan\"])} plan, {len(t[\"archive_ids\"])} archive, {len(t.get(\"escalations\",[]))} escalations')
# Write audit trail
import datetime
audit = {'phase': '1a', 'timestamp': datetime.datetime.now().isoformat(), 'passed': len(errors)==0, 'details': f'{len(t[\"plan\"])} plan, {len(t[\"archive_ids\"])} archive'}
open('/tmp/gmail-validation-audit.json','w').write(json.dumps(audit)+'\\n')
"
```
- FAIL -> Triager erneut starten oder manuell fixen. NICHT weiter.

**1b. Inhaltliche Pruefung (Orchestrator liest JSON):**
- Escalations vorhanden? Orchestrator entscheidet pro Fall (Chargeback, TYPE_B, rechtlich)
- Duplikat-Erkennung plausibel? (sent_24h_recipients nicht leer wenn gestern gesendet wurde)
- Kategorien plausibel? (access-Fälle brauchen Validierung, FAQ nicht)

---

### Phase 2: Validate
```
Agent(subagent_type="gmail-validator")
```
Bulk-Stripe + Circle-Validierung fuer alle `access`/`refund`/`cancellation`-E-Mails.
Output: `/tmp/gmail-validation-result.json`

#### Validierung 2 (Orchestrator, PFLICHT vor Phase 3):

**2a. Strukturvalidierung:**
```python
python3 -c "
import json, sys
v = json.load(open('/tmp/gmail-validation-result.json'))
t = json.load(open('/tmp/gmail-triage-result.json'))
errors = []
# Jeder access/refund/cancellation plan-Eintrag muss validiert sein
needs_validation = [p for p in t.get('plan',[]) if p.get('category') in ('access','refund','cancellation')]
# Handle multiple output formats: dict-of-dicts (primary), list, or dict with results key
validated_emails = set()
if isinstance(v, dict):
    vals = v.get('validations', v.get('results', {}))
    if isinstance(vals, dict):
        # dict-of-dicts keyed by email (Validator's documented output format)
        validated_emails = set(k.lower() for k in vals.keys())
    elif isinstance(vals, list):
        for entry in vals:
            email = entry.get('email') or entry.get('to') or ''
            if email: validated_emails.add(email.lower())
elif isinstance(v, list):
    for entry in v:
        email = entry.get('email') or entry.get('to') or ''
        if email: validated_emails.add(email.lower())
# TYPE_B price check: 97/179/189/349 EUR/month MUST be TYPE_B, never TYPE_C
vals_data = v.get('validations', {}) if isinstance(v, dict) else {}
for email_key, val in (vals_data.items() if isinstance(vals_data, dict) else []):
    stripe = val.get('stripe', {})
    price = stripe.get('price_eur', 0)
    interval = stripe.get('interval', '')
    ptype = stripe.get('product_type', '')
    if price in (97,179,189,349) and interval == 'month' and 'TYPE_C' in ptype:
        errors.append(f'{email_key}: price {price} EUR/month classified as {ptype} but MUST be TYPE_B')
for p in needs_validation:
    if p.get('to','').lower() not in validated_emails:
        errors.append(f'{p[\"to\"]} ({p[\"category\"]}) NOT validated')
if errors: print('VALIDATION FAILED:'); [print(f'  - {e}') for e in errors]; sys.exit(1)
else: print(f'VALIDATION OK: {len(validated_emails)} validated, {len(needs_validation)} required')
# Write audit trail
import datetime
audit = {'phase': '2a', 'timestamp': datetime.datetime.now().isoformat(), 'passed': True, 'details': f'{len(validated_emails)} validated'}
open('/tmp/gmail-validation-audit.json','a').write(json.dumps(audit)+'\\n')
"
```
- FAIL -> Validator erneut starten fuer fehlende E-Mails. NICHT weiter.

**2b. Inhaltliche Pruefung (Orchestrator):**
- E-Mail-Mismatches? Orchestrator entscheidet ob alternative E-Mail plausibel
- Kein Stripe-Eintrag? Nicht blind "Zahlung bestätigt" schreiben
- TYPE_B falsch als TYPE_C klassifiziert? Preis pruefen: 97/179/189/349 = TYPE_B

---

### Phase 2.5: BodyGuide-Validierung (nur wenn bodyguide_drafts vorhanden)

```
# Nur ausfuehren wenn triage-result bodyguide_drafts enthaelt und Array nicht leer ist
Agent(subagent_type="gmail-bodyguide-validator")
```

Output: `/tmp/gmail-bodyguide-validation.json`

#### Validierung 2.5:
- `passed=true`: Drafts gehen an Executor zum Versand
- `passed=false`: Draft bleibt. User informieren. NICHT versenden.
- Leeres Array / nicht vorhanden: Phase komplett ueberspringen

---

### Phase 2.7: BodyGuide-Delivery-Check (PFLICHT fuer JEDE Email die BodyGuide erwaehnt)

**SCOPE: Dieser Check gilt fuer ALLE plan-Eintraege wo:**
- `category` ist "bodyguide" oder "faq"
- Email-Body oder Betreff enthaelt: Fragebogen, Plan, Body Guide, BodyGuide, "angekommen", "erstellt", "wann kommt"
- `template_hint` ist "bodyguide_status" (alter Trigger, bleibt kompatibel)

**WARUM SO BREIT:** Am 2026-03-13 haben 6 von 6 Kundinnen NACH PDF-Zustellung nochmal "wird gerade erstellt" erhalten. Der alte Check griff nur bei `template_hint: "bodyguide_status"`, aber der Triager setzte diesen Hint nicht zuverlaessig. Deshalb: JEDE Email mit BodyGuide-Bezug wird gecheckt.

```bash
# Fuer JEDEN BodyGuide-relevanten plan-Eintrag: Versandverlauf pruefen
# Suche BREIT: "Plan ist da" ODER jede Email mit PDF-Anhang an diese Adresse
gws gmail users messages list --params '{"userId":"me","q":"to:KUNDE_EMAIL in:sent (subject:(Plan ist da) OR has:attachment)","maxResults":5}' --format json
```

Fuer jedes Ergebnis pruefen ob es ein BodyGuide-PDF war:
```bash
gws gmail users messages get --params '{"userId":"me","id":"MSG_ID","format":"full"}' --format json
# Pruefen: Hat die Email einen PDF-Anhang UND wurde NACH dem Kaufdatum gesendet?
```

**Ergebnis in triage-result.json zurueckschreiben:**

Fuer jeden BodyGuide-relevanten plan-Eintrag ein Feld `delivery_status` setzen:
- `"delivered"`: PDF-Anhang an diese Adresse gefunden. Datum mitspeichern. -> Responder MUSS dies beruecksichtigen!
- `"not_delivered"`: Keine PDF-Versand-Mail gefunden. Plan ist noch in Produktion.
- `"draft_pending"`: BodyGuide-Draft existiert in bodyguide_drafts fuer diese Kundin (wird in dieser Session versendet).

```python
python3 -c "
import json
t = json.load(open('/tmp/gmail-triage-result.json'))
bg_keywords = ['bodyguide', 'body guide', 'fragebogen', 'plan', 'erstellt', 'angekommen']
for p in t.get('plan',[]):
    # Breiterer Check: category bodyguide/faq ODER bodyguide-relevanter Inhalt
    is_bg = p.get('template_hint') == 'bodyguide_status'
    is_bg = is_bg or p.get('category') in ('bodyguide',)
    if not is_bg and p.get('summary',''):
        is_bg = any(kw in p.get('summary','').lower() for kw in bg_keywords)
    if is_bg:
        ds = p.get('delivery_status')
        if not ds:
            print(f'BLOCKER: {p[\"to\"]} hat BodyGuide-Bezug aber KEIN delivery_status')
            print(f'  -> Orchestrator MUSS sent-Ordner pruefen bevor Phase 3 startet')
            import sys; sys.exit(1)
        action = 'SKIP (schon geliefert)' if ds == 'delivered' else 'RESPOND (noch nicht geliefert)'
        print(f'{p[\"to\"]}: delivery_status={ds} -> {action}')
print('DELIVERY CHECK OK')
"
```

**Responder-Regel bei delivery_status=delivered:**
- NICHT "wird gerade erstellt" schreiben
- Stattdessen: "Dein Plan muesste schon bei dir sein! Ich habe ihn am [DATUM] verschickt. Schau bitte nochmal im Spam nach."
- Wenn Kundin NACH Zustellung nochmal fragt und im gleichen Thread: NUR auf die neue Frage eingehen, nicht den Status wiederholen

**Responder-Regel bei delivery_status=not_delivered:**
- "Dein Plan wird gerade erstellt" ist korrekt
- Zeitangabe dosiert: "dauert ein paar Tage" statt "24-72h" (klingt menschlicher)

---

### Phase 3: Respond
```
Agent(subagent_type="gmail-responder")
```
Formuliert alle HTML-E-Mail-Bodies in Nicols Stimme.
Output: `/tmp/gmail-responses.json`

#### Validierung 3 (Orchestrator, PFLICHT vor Phase 4):

**3a. Vollstaendigkeitspruefung:**
```python
python3 -c "
import json, sys
r = json.load(open('/tmp/gmail-responses.json'))
t = json.load(open('/tmp/gmail-triage-result.json'))
errors = []
plan_ids = {p['email_id'] for p in t.get('plan',[])}
response_ids = {resp['email_id'] for resp in r.get('responses',[])}
missing = plan_ids - response_ids
if missing: errors.append(f'MISSING responses for: {missing}')
extra = response_ids - plan_ids
if extra: errors.append(f'EXTRA responses (no plan entry): {extra}')
if errors: print('RESPONSE COMPLETENESS FAILED:'); [print(f'  - {e}') for e in errors]; sys.exit(1)
else: print(f'COMPLETENESS OK: {len(response_ids)} responses for {len(plan_ids)} plan entries')
# Write audit trail
import datetime
audit = {'phase': '3a', 'timestamp': datetime.datetime.now().isoformat(), 'passed': len(errors)==0, 'details': f'{len(response_ids)} responses'}
open('/tmp/gmail-validation-audit.json','a').write(json.dumps(audit)+'\\n')
"
```

**3b. Qualitaetspruefung (Orchestrator liest JEDE Antwort):**

Checkliste pro E-Mail (ALLE muessen bestehen):

| # | Check | Wie pruefen |
|---|-------|-------------|
| 1 | Verbotene Phrasen | Suche: "tut mir leid", "entschuldigung", "ich verstehe dich", "kein problem", "gerne geschehen" |
| 2 | Em-Dashes | Suche: Unicode U+2014 (—) |
| 3 | Umlaute korrekt | Keine "ae", "oe", "ue", "ss" wo ae/oe/ue/ss nicht das echte Wort ist |
| 4 | Laenge 3-5 Saetze | Zaehle `<p>` Tags (exkl. Signatur) |
| 5 | Signatur vorhanden | "Herzliche" + "Nicol Stanzel" + "Lightness Fitness" |
| 6 | Keine leeren Versprechen | Kein "innerhalb 24h", "ich rufe an", "melde mich", "kommt gleich" |
| 7 | Keine Systemnamen | Kein "Stripe", "Circle", "Supabase", "API", "n8n", "4leads", "Pipeline" |
| 8 | Keine unbewiesenen Behauptungen | "Zahlung eingegangen" NUR wenn Validator das bestaetigt hat |
| 9 | Thread-Daten vorhanden | `email_id` muss mit plan-Eintrag matchen (fuer thread_id/message_id Lookup) |
| 10 | Aktionen ausfuehrbar | Wenn E-Mail "ist umgestellt/freigeschaltet" sagt: Aktion muss VOR Versand passieren |

```python
python3 -c "
import json, re, sys
r = json.load(open('/tmp/gmail-responses.json'))
FORBIDDEN = ['tut mir leid','tut mir','entschuldigung','ich verstehe dich','ich verstehe deine','ich verstehe das','das verstehe ich','nachvollziehen','kein problem','keine sorge','macht nichts','gerne geschehen','du hast recht','gerne bei weiteren fragen','schreib mir gerne']
SYSTEM_NAMES = ['stripe','supabase','circle api','n8n','4leads','pipeline','webhook','backend','database','sql','api key','mcp']
EMPTY_PROMISES = ['innerhalb 24','rufe dich an','melde mich','kommt gleich','werde ich','kuemmere mich']
# Umlaut stems: ae/oe/ue substitutions that indicate broken umlauts
UMLAUT_STEMS = ['aerger','aender','oeffn','ueber','fuer','moeglich','koennen','wuerden','natuerlich','unterstuetz','zurueck','gruesse','hoer','loesen','ernaehr','muess','wuensch','pruef','naechst','spaet','regelmaess','verfueg','ausfuehr','schaetz','gebuehr','voellig','schaedl','genueg','aerztin','aerztlich']
# Sharp-s stems: ss substitutions that should be sharp-s
SHARP_S_STEMS = ['strass','grosse','gross ','auss','gemass','mass ','schliess','fuss','suess','weiss','heiss']
errors = []
for resp in r.get('responses',[]):
    body_lower = resp['html_body'].lower()
    to = resp['to']
    for phrase in FORBIDDEN:
        if phrase in body_lower: errors.append(f'{to}: FORBIDDEN \"{phrase}\"')
    for name in SYSTEM_NAMES:
        if name in body_lower: errors.append(f'{to}: SYSTEM_NAME \"{name}\"')
    for promise in EMPTY_PROMISES:
        if promise in body_lower: errors.append(f'{to}: EMPTY_PROMISE \"{promise}\"')
    if chr(8212) in resp['html_body']: errors.append(f'{to}: EM_DASH found')
    if 'herzliche' not in body_lower: errors.append(f'{to}: MISSING signature')
    for bad in UMLAUT_STEMS:
        if bad in body_lower: errors.append(f'{to}: UMLAUT \"{bad}\" should use aeoeue')
    for bad in SHARP_S_STEMS:
        if bad in body_lower: errors.append(f'{to}: SHARP_S \"{bad}\" should use sharp-s')
if errors: print(f'QUALITY CHECK FAILED ({len(errors)} issues):'); [print(f'  - {e}') for e in errors]; sys.exit(1)
else: print(f'QUALITY CHECK OK: {len(r[\"responses\"])} emails passed all checks')
# Write audit trail
import datetime
audit = {'phase': '3b', 'timestamp': datetime.datetime.now().isoformat(), 'passed': len(errors)==0, 'details': f'{len(r[\"responses\"])} checked, {len(errors)} issues'}
open('/tmp/gmail-validation-audit.json','a').write(json.dumps(audit)+'\\n')
"
```

- FAIL -> Orchestrator fixt problematische Antworten direkt in der JSON-Datei. NICHT weiter bis alle bestehen.

**3c. Aktions-Konsistenz (Orchestrator):**
- Wenn eine Antwort sagt "ist freigeschaltet/umgestellt": Aktion in `circle_action` oder `stripe_action` Feld dokumentiert?
- Wenn Antwort auf `access`-E-Mail: Validation-Result pruefen ob Zugang tatsaechlich existiert
- Wenn Antwort Preis nennt: Stimmt der Preis mit Stripe-Daten ueberein?

---

### Phase 4: Execute
```
Agent(subagent_type="gmail-executor")
```
Fuehrt Circle-Aktionen ZUERST aus, sendet dann E-Mails (mit Thread-Headern), Batch-Archivierung.
Executor Steps: 0.5 (BodyGuide PDF send), 0.6 (4leads tag 43570 via n8n webhook for sent BodyGuides), 1 (Circle/Stripe), 2 (emails), 4 (archive), 5 (delete drafts).
Output: `/tmp/gmail-execution-result.json`

#### Validierung 4 (Orchestrator, PFLICHT):

**4a. Versandpruefung:**
```python
python3 -c "
import json, sys
e = json.load(open('/tmp/gmail-execution-result.json'))
r = json.load(open('/tmp/gmail-responses.json'))
errors = []
sent = {s['to'].lower() for s in e.get('sent',[])}
expected = {resp['to'].lower() for resp in r.get('responses',[])}
not_sent = expected - sent
if not_sent: errors.append(f'NOT SENT: {not_sent}')
failed = e.get('failed',[])
if failed: errors.append(f'FAILED: {[f[\"to\"] for f in failed]}')
# Check Circle actions: any failed circle updates?
circle_failed = [c for c in e.get('circle_updates',[]) if c.get('status') != 'ok']
if circle_failed: errors.append(f'CIRCLE FAILED: {[c[\"email\"] for c in circle_failed]}')
# Check 4leads tag assignments for sent BodyGuides
tag_failed = [t for t in e.get('bodyguide_tags_set',[]) if t.get('status') != 'ok']
if tag_failed: errors.append(f'4LEADS TAG FAILED: {[t[\"to\"] for t in tag_failed]}')
if errors: print('SEND VALIDATION FAILED:'); [print(f'  - {err}') for err in errors]; sys.exit(1)
else: print(f'SEND OK: {len(sent)}/{len(expected)} sent, {e.get(\"archived_count\",0)} archived')
# Write audit trail
import datetime
audit = {'phase': '4a', 'timestamp': datetime.datetime.now().isoformat(), 'passed': len(errors)==0, 'details': f'{len(sent)} sent, {len(failed)} failed'}
open('/tmp/gmail-validation-audit.json','a').write(json.dumps(audit)+'\\n')
"
```

**4b. Thread-Validierung (Stichprobe):**
```bash
# Pruefe ob die letzte gesendete E-Mail im richtigen Thread gelandet ist
gws gmail users messages list --params '{"userId":"me","q":"in:sent newer_than:1h","maxResults":3}' --format json
# Fuer jede: threadId muss mit der Original-E-Mail uebereinstimmen
```

**4c. Circle-Aktions-Validierung:**
- Wenn circle_action ausgefuehrt: Ergebnis in execution-result pruefen
- Fehlgeschlagene Circle-Aktionen: Antwort war moeglicherweise falsch ("ist freigeschaltet" aber nicht wirklich). User informieren.

---

### Phase 5: Post-Send-Verify

```bash
# Inbox muss leer sein
gws gmail users messages list --params '{"q":"in:inbox","maxResults":10}' --format json
```

Falls Inbox NICHT leer:
- Identifiziere was uebrig ist
- Waren es E-Mails die waehrend des Workflows reinkamen? -> Naechste Session
- Waren es E-Mails die vergessen wurden? -> Manuell archivieren oder beantworten

```bash
# Stichprobe: Letzte 3 gesendete E-Mails auf Thread-Korrektheit pruefen
gws gmail users messages list --params '{"userId":"me","q":"in:sent newer_than:1h","maxResults":3}' --format json
# Fuer jede Message: threadId auslesen und mit triage-result abgleichen
```

---

### Phase 6: Log

**6a. Audit Trail pruefen (PFLICHT):**
```bash
cat /tmp/gmail-validation-audit.json
# Muss Eintraege fuer Phase 1a, 2a, 3a, 3b, 4a enthalten, alle mit passed=true
```
Falls ein Eintrag fehlt oder `passed=false`: Session als fehlerhaft markieren.

**6b. Learnings-Log updaten:** `/references/ref-learnings-log.md`
Session-Zeile appenden: Datum, Anzahl E-Mails, Gesendet, Fehler, Tool Calls, Validierungsergebnis.

---

## Validierungs-Zusammenfassung

| Phase | Validierung | Blockiert naechste Phase? |
|-------|-------------|---------------------------|
| 1 -> 2 | Struktur (thread_id, message_id) + Inhalt (Escalations, Kategorien) | JA |
| 2 -> 2.7 | Alle access/refund/cancellation validiert, keine TYPE_B/C Verwechslung | JA |
| 2.7 -> 3 | Alle bodyguide_status plan-Eintraege haben delivery_status gesetzt | JA |
| 3 -> 4 | Vollstaendigkeit + 10-Punkte-Qualitaetscheck + Aktions-Konsistenz | JA |
| 4 -> 5 | Versandpruefung + Thread-Stichprobe + Circle-Aktionen | JA |
| 5 -> 6 | Inbox leer, Threads korrekt | JA |

**Prinzip: Kein Agent startet bevor der vorherige validiert ist. Jede Validierung hat einen automatisierten UND einen inhaltlichen Teil.**

## .env Variable Names

Korrekte Variablennamen (NICHT raten!):
- `STRIPE_API_KEY` (nicht STRIPE_SECRET_KEY)
- `CIRCLE_ADMIN_API_KEY`
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` (NICHT SUPABASE_KEY)

Bei Unsicherheit: `grep '^VARIABLENNAME' ~/Desktop/.env | head -1`

## Reference Files

| Datei | Laden wenn |
|-------|------------|
| `references/ref-learnings-log.md` | **IMMER am Session-Start** |
| `references/ref-categories.md` | FAQ/Zugang/Technik-Fragen |
| `references/ref-refund-sop.md` | Jede Refund/Kündigungs-Anfrage |
| `references/ref-stripe-promo-codes.md` | Gutschein-Anfragen, Template-Bug-Recovery |
| `references/ref-gws-patterns.md` | gws CLI Syntax-Fragen |
| `references/ref-circle-patterns.md` | Circle API Zugang/Tags |
| `references/ref-stripe-patterns.md` | Stripe SQL, Bulk-Queries |
