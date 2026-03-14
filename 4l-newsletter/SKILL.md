---
name: 4l-newsletter
description: "4leads Newsletter-Kampagnen erstellen mit Tag-basierter Empfänger-Segmentierung."
user-invocable: false
invocation: /4l-newsletter
arguments:
  - name: input
    description: >
      Beschreibung der Kampagne: Thema, Anzahl Segmente, welche Tags pro Segment,
      Betreffzeile, und Versandzeitpunkt. Ohne Argumente: zeigt die aktuelle
      Newsletter-Übersicht in 4leads.
    required: false
---

# Newsletter-Kampagne erstellen

Dieser Command führt durch den kompletten Newsletter-Workflow in 4leads.
Lies zuerst die vollständige SOP: `~/.claude/skills/4leads/references/newsletter-sop.md`

## Voraussetzungen prüfen

1. playwright-cli mit persistent Chrome-Profil (eingeloggt in 4leads)
2. E-Mail-Texte pro Segment vorbereitet (oder vom User erfragen)
3. Referenz-Template-Hash bekannt (Standard: NL03 = G3o6)

## Workflow-Übersicht

### Phase 1: Design exportieren
```bash
playwright-cli open --browser=chrome --persistent --headed "https://app.4leads.net/email-funnel/email/edit/e/{HASH}"
sleep 4
playwright-cli eval "() => (typeof window.unlayer === 'undefined') ? 'not yet' : 'unlayer ready'"
playwright-cli eval "() => new Promise(resolve => window.unlayer.saveDesign(design => resolve(JSON.stringify(design))))" | sed '1d' | head -1 | python3 -c "
import sys, json
line = sys.stdin.read().strip()
design = json.loads(json.loads(line))
json.dump(design, open('/tmp/base-design.json', 'w'))
print(f'Saved: {len(json.dumps(design))} bytes, {len(design[\"body\"][\"rows\"])} rows')
"
```

### Phase 2: Segment-E-Mails generieren (Python)
Lies `references/newsletter-sop.md` Phase 2 für das `make_html()` / `make_email()` Pattern.
NL03-Template: 4 Rows (Banner, Text-Body, Social Icons, Footer). Text ist in Row 1.

### Phase 3: Designs hochladen (localStorage-Transfer)
```bash
# Pro E-Mail: base64 encode → localStorage → loadDesign
python3 -c "import json, base64; d=json.load(open('/tmp/newsletter-a.json')); b64=base64.b64encode(json.dumps(d).encode()).decode(); open('/tmp/newsletter-a.b64','w').write(b64)"
playwright-cli eval "() => { localStorage.setItem('_designTransfer', '$(cat /tmp/newsletter-a.b64)'); return 'stored'; }"
playwright-cli eval "() => { const b64 = localStorage.getItem('_designTransfer'); const json = atob(b64); const design = JSON.parse(json); return new Promise(resolve => { window.unlayer.loadDesign(design); resolve('loaded ' + json.length + ' chars'); }); }"
playwright-cli eval "() => { document.querySelector('.fl-e-save')?.click(); return 'save clicked'; }"
playwright-cli eval "() => { localStorage.removeItem('_designTransfer'); return 'cleaned'; }"
```

### Phase 4: Newsletter konfigurieren (4-Schritt-Wizard)
1. **Einstellungen:** Name, Versandzeitpunkt, Absender (info@nicolstanzel.de)
2. **Empfänger:** Tag-basierte Segmentierung (selectize.js Dropdowns)
3. **E-Mail:** Zuweisen per Suchfeld
4. **Prüfen:** Empfänger-Anzahl, Vorschau, Status auf ENTWURF lassen

### Phase 5: Verifizieren
```bash
playwright-cli eval "() => new Promise(resolve => window.unlayer.saveDesign(design => {
  const text = design.body.rows[1]?.columns?.[0]?.contents?.[0]?.values?.text || 'EMPTY';
  resolve(JSON.stringify({ rows: design.body.rows.length, len: text.length }));
}))"
```

## Kritische Regeln

- **selectize.js:** Nach JEDER Tag-Auswahl frischen Snapshot nehmen. Refs werden ungültig.
- **Kurze Suchbegriffe:** "connect" statt "connect-annual" bei Tag-Suche.
- **Escape vor nächstem Feld:** `playwright-cli press Escape` um Dropdown-Overlay zu schließen.
- **localStorage-Transfer:** IMMER für Designs >5KB. Inline eval scheitert an Shell-Escaping.
- **beforeunload:** `run-code "async page => { page.on('dialog', d => d.accept()); ... }"` beim Navigieren.
- **Status ENTWURF:** Newsletter NIE auf Aktiv setzen ohne explizite User-Freigabe.

## Segmentierungs-Logik

| Filter | Logik | Verwendung |
|--------|-------|-----------|
| "mindestens einen dieser Tags" | OR | Include-Tags |
| "alle dieser Tags" | AND | Alle müssen vorhanden sein |
| "mindestens einen nicht" (Nicht markiert) | Exclude | Ausschluss-Tags |
