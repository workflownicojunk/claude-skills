# SOP: Newsletter-Kampagne erstellen (4leads + playwright-cli)

Schrittweise Anleitung zum Erstellen segmentierter Newsletter-Kampagnen in 4leads.
Deckt den kompletten Workflow ab: E-Mail-Vorlage exportieren, segmentspezifische E-Mails generieren, in 4leads hochladen, Newsletter konfigurieren.

## Voraussetzungen

- `playwright-cli` mit persistent Chrome-Profil (eingeloggt in 4leads)
- Referenz-Newsletter mit dem gewünschten Design (z.B. NL03, Hash G3o6)
- E-Mail-Texte pro Segment vorbereitet

## Phase 1: Referenz-Design exportieren

### 1.1 Editor öffnen und Design als JSON exportieren

```bash
# Referenz-Newsletter im Editor öffnen
playwright-cli open --browser=chrome --persistent --headed "https://app.4leads.net/email-funnel/email/edit/e/{REFERENZ_HASH}"

# 3-5 Sekunden warten bis Unlayer geladen ist
sleep 4

# Prüfen ob Unlayer bereit ist
playwright-cli eval "() => (typeof window.unlayer === 'undefined') ? 'not yet' : 'unlayer ready'"

# Design als JSON exportieren und in Datei speichern
playwright-cli eval "() => new Promise(resolve => window.unlayer.saveDesign(design => resolve(JSON.stringify(design))))" | sed '1d' | head -1 | python3 -c "
import sys, json
line = sys.stdin.read().strip()
design = json.loads(json.loads(line))
json.dump(design, open('/tmp/base-design.json', 'w'))
print(f'Saved: {len(json.dumps(design))} bytes, {len(design[\"body\"][\"rows\"])} rows')
"
```

### GOTCHA: eval Output-Format

`playwright-cli eval` gibt das Ergebnis als doppelt-serialisierten JSON-String aus.
Die Pipeline `sed '1d' | head -1 | python3 -c "json.loads(json.loads(line))"` ist nötig weil:
1. `sed '1d'` entfernt die "### Result" Headerzeile
2. `head -1` nimmt nur die Datenzeile
3. `json.loads(json.loads(...))` entpackt die doppelte Serialisierung

### GOTCHA: beforeunload Dialog

Beim Navigieren weg vom Editor zeigt 4leads einen "Website verlassen?" Dialog.
```bash
# VOR dem Navigieren: Dialog vorab akzeptieren
playwright-cli run-code "async page => { page.on('dialog', d => d.accept()); await page.goto('https://...'); }"
# ODER nach Timeout:
playwright-cli dialog-accept
```

## Phase 2: Segment-E-Mails generieren (Python)

### 2.1 Standard-Template: NL03 (Nicol Stanzel)

4-Row-Struktur:
- **Row 0:** Banner-Image (1350x450, URL: `https://srvm.4leads.net/8OxR/uploads/BAzUQDr6LSBrE6SvUkXzN4uwy.png`)
- **Row 1:** Text-Body (containerPadding: "50px 70px 120px", font: Open Sans 16px, line-height: 140%)
- **Row 2:** Divider + Social Icons (Instagram, YouTube, Email)
- **Row 3:** Divider + Footer (Impressum, Abmelden, Einstellungen)

CTA-Links sind INLINE im Text (kein separater Button-Row). Hintergrund: `#ffffff`, Column-Bg: `#ffffff`.

### 2.2 Python-Script zum Generieren

```python
import json, copy

BASE = json.load(open('/tmp/base-design.json'))

def make_html(paragraphs):
    """Wandelt Text-Absätze in HTML mit NL03-Styling um."""
    parts = []
    for p in paragraphs:
        if p == '':
            parts.append('<p style="line-height: 140%; text-align: left;">&nbsp;</p>')
        else:
            parts.append(
                f'<p style="line-height: 140%; text-align: left;">'
                f'<span style="font-size: 16px; line-height: 22.4px; '
                f"font-family: 'Open Sans', sans-serif;\">{p}</span></p>"
            )
    return '\n'.join(parts)

def make_email(body_paragraphs):
    """Erstellt ein neues Design mit geändertem Text-Body."""
    design = copy.deepcopy(BASE)
    rows = design['body']['rows']
    for col in rows[1].get('columns', []):
        for content in col.get('contents', []):
            if content.get('type') == 'text':
                content['values']['text'] = make_html(body_paragraphs)
    return design
```

### 2.3 HTML-Formatierung im Text

| Element | HTML |
|---------|------|
| Normaler Text | `<span style="font-size: 16px; line-height: 22.4px; font-family: 'Open Sans', sans-serif;">Text</span>` |
| Fett | `<strong>NICOL15</strong>` |
| Link | `<a href="URL" style="color: #7A94CC; text-decoration: underline;">Linktext</a>` |
| Leerzeile | `<p style="line-height: 140%; text-align: left;">&nbsp;</p>` |
| Signatur | Normaler Text, z.B. "Eure Nicol 🤍" |

### 2.4 Designs speichern

```python
for label, paragraphs in [('a', SEG_A_PARAS), ('b', SEG_B_PARAS), ('c', SEG_C_PARAS)]:
    design = make_email(paragraphs)
    json.dump(design, open(f'/tmp/newsletter-{label}.json', 'w'))
```

## Phase 3: E-Mails in 4leads erstellen

### 3.1 Leere E-Mails über API erstellen (schneller als UI)

```bash
# Session-Cookie aus Playwright holen
playwright-cli eval "() => document.cookie"

# Oder direkt in der UI: E-Mail-Marketing > E-Mails > "neue E-Mail" Button
# Dann: Name eingeben, Betreff setzen, speichern
# Hash merken (aus der URL: /email-funnel/email/edit/e/{HASH})
```

### 3.2 Design per localStorage-Transfer laden

Die zuverlässigste Methode für große JSON-Designs:

```bash
# 1. Design als base64 encoden
python3 -c "
import json, base64
d = json.load(open('/tmp/newsletter-a.json'))
b64 = base64.b64encode(json.dumps(d).encode()).decode()
open('/tmp/newsletter-a.b64', 'w').write(b64)
print(f'Base64: {len(b64)} chars')
"

# 2. In localStorage schreiben
playwright-cli eval "() => { localStorage.setItem('_designTransfer', '$(cat /tmp/newsletter-a.b64)'); return 'stored'; }"

# 3. Aus localStorage lesen und in Unlayer laden
playwright-cli eval "() => { const b64 = localStorage.getItem('_designTransfer'); const json = atob(b64); const design = JSON.parse(json); return new Promise(resolve => { window.unlayer.loadDesign(design); resolve('loaded ' + json.length + ' chars'); }); }"

# 4. Unlayer Save-Button klicken
playwright-cli eval "() => { document.querySelector('.fl-e-save')?.click(); return 'save clicked'; }"

# 5. localStorage aufräumen
playwright-cli eval "() => { localStorage.removeItem('_designTransfer'); return 'cleaned'; }"
```

### GOTCHA: Inline eval vs. localStorage

Für Designs >5KB funktioniert inline `eval` NICHT zuverlässig (Shell-Escaping-Probleme).
Immer den localStorage-Transfer-Pfad nutzen:
1. Python → base64 → Datei
2. `cat datei` in eval → localStorage
3. Zweiter eval → localStorage → atob → JSON.parse → loadDesign

### 3.3 E-Mail-Settings konfigurieren

Nach dem Design-Upload die Settings der E-Mail konfigurieren:

```
Refs (können sich ändern, immer frischen Snapshot nehmen):
- Betreff: textbox nach "Betreff" Label
- Interner Name: textbox nach "Interner Name" Label
- Tags on open: textbox nach "Tags bei Öffnung"
- Tags on click: textbox nach "Tags bei Klick"
- Speichern: button "speichern" (NICHT der Unlayer-Save!)
```

## Phase 4: Newsletter erstellen und konfigurieren

### 4.1 Neuen Newsletter anlegen

```bash
playwright-cli goto "https://app.4leads.net/email-funnel/newsletter"
# "Neuer Newsletter" klicken
```

### 4.2 Schritt 1: Einstellungen

| Feld | Aktion |
|------|--------|
| Newsletter-Name (intern) | `playwright-cli fill {ref} "Name"` |
| Versand-Zeitpunkt | `playwright-cli fill {ref} "DD.MM.YYYY HH:MM"` |
| E-Mail-Versand durch | `playwright-cli select {ref} "info@nicolstanzel.de"` |
| Speichern + Weiter | Button "weiter zu Schritt 2" klicken |

### 4.3 Schritt 2: Empfänger (Tag-basierte Segmentierung)

**Reihenfolge:**
1. "Empfänger aus Kontakten auswählen" klicken (öffnet Filteroptionen)
2. "Markiert mit Tag" Tab expandieren
3. Tags im selectize.js-Dropdown auswählen
4. Falls nötig: "Nicht markiert mit Tag" Tab für Ausschlüsse

**selectize.js Tag-Eingabe:**
```bash
# 1. Textfeld klicken
playwright-cli click {textbox_ref}
# 2. Suchbegriff eingeben (KURZ halten, z.B. "connect" statt "connect-annual")
playwright-cli fill {textbox_ref} "connect"
# 3. Snapshot nehmen, Dropdown-Option finden
playwright-cli snapshot
# 4. Option anklicken
playwright-cli click {dropdown_option_ref}
# 5. Für weiteren Tag: neues Textfeld-Ref holen (ändert sich nach Auswahl!)
playwright-cli snapshot
playwright-cli fill {NEUER_textbox_ref} "SYX"
```

### GOTCHA: Stale Refs nach Tag-Auswahl

Nach jeder Tag-Auswahl ändern sich die Element-Refs. **IMMER** einen frischen Snapshot nehmen bevor das nächste Element interagiert wird.

### GOTCHA: selectize.js Dropdown erscheint nicht

- Vollständige Tag-Namen (z.B. "connect-annual") zeigen manchmal keine Ergebnisse
- **Lösung:** Kürzeren Suchbegriff verwenden (z.B. "connect" statt "connect-annual")
- Nach dem Tippen 1-2 Sekunden warten

### GOTCHA: Element-Overlay bei "Kontakt hat alle dieser Tags"

Das Dropdown des vorherigen Feldes kann das nächste Feld überlagern.
```bash
# Erst Dropdown schließen
playwright-cli press Escape
# Dann das nächste Feld klicken
playwright-cli click {ref}
```

### Segmentierungs-Logik

| Filter-Sektion | Logik | Verwendung |
|---------------|-------|------------|
| "mindestens einen dieser Tags" (Markiert) | OR | Include: connect-annual ODER connect-monthly |
| "alle dieser Tags" (Markiert) | AND | Include: SYX.0 gekauft UND weitere |
| "mindestens einen nicht" (Nicht markiert) | Exclude IF has tag | Ausschluss: Hat SYX.0 gekauft NICHT |
| "keinen dieser Tags" (Nicht markiert) | Exclude ALL | Ausschluss: Hat KEINEN der genannten Tags |

### Segment-Konfigurationen (Beispiel: Les Mills Kampagne)

**Segment A (X.0 ohne Connect):**
- Markiert/mindestens einen: SYX.0 gekauft
- Nicht markiert/mindestens einen nicht: connect-annual, connect-monthly

**Segment B (X.0 mit Connect):**
- Markiert/mindestens einen: connect-annual, connect-monthly
- Markiert/alle: SYX.0 gekauft

**Segment C (Connect ohne X.0):**
- Markiert/mindestens einen: connect-annual, connect-monthly
- Nicht markiert/mindestens einen nicht: SYX.0 gekauft

### 4.4 Schritt 3: E-Mail zuweisen

```bash
# E-Mail-Suchfeld klicken und nach Name suchen
playwright-cli click {email_textbox_ref}
playwright-cli fill {email_textbox_ref} "Suchbegriff"
# Aus Dropdown auswählen
playwright-cli click {dropdown_option_ref}
# Speichern + Weiter
```

### 4.5 Schritt 4: Prüfen

Letzte Überprüfung vor dem Speichern:
- Empfänger-Anzahl plausibel?
- Versandzeitpunkt korrekt?
- E-Mail-Vorschau korrekt (Betreff, Absender, Inhalt)?
- Status: **Entwurf** (NICHT Aktiv setzen ohne explizite Freigabe!)

```bash
# Speichern und Fertig
playwright-cli click {speichern_ref}
playwright-cli click {fertig_ref}
```

## Phase 5: Verifikation

### Design-Verifikation per eval (ohne Snapshot)

```bash
playwright-cli eval "() => new Promise(resolve => window.unlayer.saveDesign(design => {
  const rows = design.body.rows;
  const text = rows[1]?.columns?.[0]?.contents?.[0]?.values?.text || 'EMPTY';
  resolve(JSON.stringify({
    rows: rows.length,
    hasConnect: text.includes('Connect'),
    hasStripe: text.includes('stripe.com'),
    hasNicol15: text.includes('NICOL15'),
    len: text.length
  }));
}))"
```

### Newsletter-Übersicht prüfen

```bash
playwright-cli goto "https://app.4leads.net/email-funnel/newsletter"
playwright-cli snapshot
# Prüfe: Name, Empfänger-Anzahl, Versandzeitpunkt, Status (Entwurf)
```

## Token-Effizienz-Regeln

### Was diese Session teuer gemacht hat (vermeiden!)

1. **Falsches Template verwendet:** Erst RJlb (6-Row) genommen statt NL03 (4-Row). Kosten: ~50k Tokens extra. **Lösung:** Template-Hash IMMER im Prompt spezifizieren.

2. **Stale Refs:** Nach jeder selectize.js-Auswahl werden Refs ungültig. 3-4 unnötige Retry-Zyklen. **Lösung:** IMMER Snapshot nach jeder Interaktion.

3. **Volle Snapshots statt gezielter evals:** Snapshots der 4leads-Seite sind 200-300 Zeilen. **Lösung:** `playwright-cli eval` für gezielte Abfragen, `grep` auf Snapshot-Dateien statt alles zu lesen.

4. **Manuelle Newsletter-Erstellung (4 Schritte x 3 Segmente):** 12 Schritt-Durchläufe mit je ~5 Interaktionen. **Lösung:** Unvermeidbar in der UI, aber durch Routine schneller.

### Optimaler Ablauf (Ziel: <50 Tool-Calls pro Newsletter)

```
1. Design exportieren: 3 Calls (goto, sleep+eval, python)
2. 3 Designs generieren: 1 Call (python script)
3. 3 E-Mails erstellen + Design laden: 9 Calls (3x: goto, sleep+eval, eval)
4. Pro Newsletter (3x): ~15 Calls (settings, tags, email, prüfen)
= ~57 Calls total für 3 Newsletter
```

### Grep statt Read für Snapshots

```bash
# Statt: Read snapshot (200+ Zeilen)
# Mache: Grep für spezifische Elemente
playwright-cli snapshot
grep -E "speichern|weiter|button" .playwright-cli/page-*.yml | tail -5
```

## Referenz: Bewährte E-Mail-Hashes

| Name | Hash | Verwendung |
|------|------|------------|
| NL03 Design-Vorlage | G3o6 | Standard-Newsletter-Template (4 Rows) |
| Les Mills Seg A | bEvX | X.0 ohne Connect |
| Les Mills Seg B | OGBd | X.0 mit Connect |
| Les Mills Seg C | XRPy | Connect ohne X.0 |
