---
name: 4l-email-edit
description: >
  Bearbeitet E-Mail-Templates im 4leads Unlayer Editor via playwright-cli. Öffnet den Editor,
  exportiert das aktuelle Design als JSON, ermöglicht Änderungen (Text, Links, Bilder, Platzhalter),
  und lädt das modifizierte Design zurück. Nutze diesen Command wenn der User eine bestehende E-Mail
  bearbeiten, einen Platzhalter korrigieren, einen Link ändern, oder Text in einer E-Mail-Vorlage
  anpassen möchte.
user_invocable: true
invocation: /4l-email-edit
arguments:
  - name: input
    description: >
      E-Mail-Hash (z.B. "5OLR") oder Beschreibung der E-Mail (z.B. "Connect Willkommens-E-Mail").
      Ohne Argument: zeigt die E-Mail-Liste. Für Hash-Lookup: lies
      ~/.claude/skills/4leads/references/email-hashes.md
    required: false
---

# E-Mail bearbeiten (Unlayer Editor)

## Schritt 1: E-Mail finden

Falls nur ein Name bekannt ist, Hash nachschlagen:
```bash
# E-Mail-Hash-Liste laden
cat ~/.claude/skills/4leads/references/email-hashes.md
# Oder in der UI suchen:
playwright-cli open --browser=chrome --persistent --headed "https://app.4leads.net/email-funnel/email"
```

## Schritt 2: Editor öffnen und Design exportieren

```bash
playwright-cli goto "https://app.4leads.net/email-funnel/email/edit/e/{HASH}"
sleep 4
# Unlayer-Check
playwright-cli eval "() => (typeof window.unlayer === 'undefined') ? 'not yet' : 'unlayer ready'"
# Design als JSON exportieren
playwright-cli eval "() => new Promise(resolve => window.unlayer.saveDesign(design => resolve(JSON.stringify(design))))" | sed '1d' | head -1 | python3 -c "
import sys, json
line = sys.stdin.read().strip()
design = json.loads(json.loads(line))
json.dump(design, open('/tmp/email-design.json', 'w'))
print(f'Saved: {len(json.dumps(design))} bytes, {len(design[\"body\"][\"rows\"])} rows')
"
```

## Schritt 3: Design ändern

Für Text-Änderungen: Python find/replace auf der JSON-Datei.
```python
import json
d = json.load(open('/tmp/email-design.json'))
s = json.dumps(d)
s = s.replace('ALTER_TEXT', 'NEUER_TEXT')
d = json.loads(s)
json.dump(d, open('/tmp/email-design-fixed.json', 'w'))
```

Für strukturelle Änderungen: lies `~/.claude/skills/4leads/references/unlayer-design.md`

## Schritt 4: Design zurückladen (localStorage-Transfer)

```bash
python3 -c "import json, base64; d=json.load(open('/tmp/email-design-fixed.json')); b64=base64.b64encode(json.dumps(d).encode()).decode(); open('/tmp/email-design.b64','w').write(b64)"
playwright-cli eval "() => { localStorage.setItem('_designTransfer', '$(cat /tmp/email-design.b64)'); return 'stored'; }"
playwright-cli eval "() => { const b64 = localStorage.getItem('_designTransfer'); const json = atob(b64); const design = JSON.parse(json); return new Promise(resolve => { window.unlayer.loadDesign(design); resolve('loaded'); }); }"
```

## Schritt 5: Speichern

```bash
# Unlayer-Content speichern
playwright-cli eval "() => { document.querySelector('.fl-e-save')?.click(); return 'save clicked'; }"
# localStorage aufräumen
playwright-cli eval "() => { localStorage.removeItem('_designTransfer'); return 'cleaned'; }"
```

## Platzhalter-Regeln

Custom Fields nutzen die numerische ID, NICHT den Namen:

| Feld | Placeholder |
|------|------------|
| connect_promo_monatlich | `{{field_15301}}` |
| connect_fenster_ablauf | `{{field_15302}}` |
| connect_promo_jaehrlich | `{{field_15303}}` |
| connect_fenster_ablauf_text | `{{field_15305}}` |
| connect_bodyguide_gutscheincode | `{{field_15306}}` |

Standard-Platzhalter: `{{firstname}}`, `{{lastname}}`, `{{email}}`, `{{contactCenter}}`, `{{unsubscribe}}`

Für unbekannte Feld-IDs: `~/.claude/skills/4leads/references/contact-schema.json`

## Gotchas

- **Cross-origin iframe:** `window.unlayer` auf der Parent-Seite, NICHT im iframe
- **Zwei Save-Buttons:** Settings-Save (Seite) vs. Unlayer-Save (`.fl-e-save`)
- **beforeunload:** Dialog akzeptieren beim Navigieren: `playwright-cli dialog-accept`
- **eval Output:** Doppelt serialisiert. Pipeline: `sed '1d' | head -1 | json.loads(json.loads(...))`
