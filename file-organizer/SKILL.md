---
name: file-organizer
description: Workspace guardian for the PARA directory structure (Project, Area, Resource, Archive, Inbox). Audits naming conventions, finds misplaced files, enforces structure rules, handles path migrations, and runs health checks. Customized for ~/Desktop/ iCloud-synced layout.
---

# File Organizer

Workspace-specific organization skill for the ~/Desktop/ PARA structure. Not a generic tool. Knows the exact directory layout, naming rules, and config files that reference paths.

## When to Use

- Organize files dropped in wrong locations
- Audit directories for naming violations or structure drift
- Migrate/rename directories and update all path references
- Health check after a work session or via /loop
- Classify and file new documents (invoices, contracts, screenshots, etc.)

## Directory Structure (FIXED, do NOT create new top-level dirs)

```
~/Desktop/
├── Inbox/         # Unsortierte Dateien, sofort verschieben
├── Project/       # Aktive Projekte mit Enddatum
├── Area/          # Laufende Verantwortungsbereiche
│   ├── Finanzen/      (Datev/, Stripe/, Bank/, Steuern/)
│   ├── Marketing/     (brand-design/, email-automation/, launches/)
│   ├── Kunden/        (Support/, Anfragen/)
│   ├── Community/     (Circle/)
│   ├── Produkte/      (body-guide/, connect/, strongeryou-x0/)
│   └── Persönlich/    (Behörden/, TK-Krankenkasse/, ING-DiBa/)
├── Resource/      # Referenzmaterial, Templates, Wissen
├── Archive/       # Abgeschlossene Projekte und Dokumente
├── .env           # API-Keys (NIEMALS verschieben)
├── STATE.json     # Aktive Workstreams
└── CLAUDE.md      # Root-Instruktionen
```

### Erlaubte Dateien auf Desktop Root

NUR diese Dateien dürfen direkt unter `~/Desktop/` liegen:
- `.env`, `CLAUDE.md`, `STATE.json`, `communication-style.md`
- Die 5 PARA-Ordner: `Inbox/`, `Project/`, `Area/`, `Resource/`, `Archive/`
- Versteckte Ordner: `.claude/`, `.planning/`

Alles andere ist eine Violation und gehört in `Inbox/`.

## Naming Rules

| Rule | Convention | Example |
|------|-----------|---------|
| Folders | `kebab-case`, echte Umlaute erlaubt, kein CamelCase | `rechnungen-eingang` |
| Dated files | `YYMMDD-beschreibung.ext` | `260302-quartalsreport.pdf` |
| Invoices in | `YYMMDD-anbieter-beschreibung.pdf` | `250428-activecampaign-invoice.pdf` |
| Extensions | Immer lowercase | `.pdf` nicht `.PDF` |
| Forbidden | Spaces in neuen Dateien, CamelCase, Underscores in neuen Dirs | |

## Instructions

### Mode 1: Audit (default when user says "organize", "aufräumen", "check", "audit")

Scan for violations and report. Do NOT fix without approval.

```bash
# 1. Fehlplatzierte Dateien auf Desktop Root
find ~/Desktop -maxdepth 1 -type f ! -name '.DS_Store' ! -name '.env' ! -name 'CLAUDE.md' ! -name 'STATE.json' ! -name 'communication-style.md' 2>/dev/null

# 2. Fehlplatzierte Ordner auf Desktop Root (keine PARA-Ordner)
find ~/Desktop -maxdepth 1 -type d ! -name 'Desktop' ! -name 'Inbox' ! -name 'Project' ! -name 'Area' ! -name 'Resource' ! -name 'Archive' ! -name '.claude' ! -name '.planning' ! -name '.git' ! -name '.*' 2>/dev/null

# 3. Downloads sollte leer sein
ls ~/Downloads/ 2>/dev/null | head -20

# 4. Naming violations in PARA-Ordnern
find ~/Desktop/Inbox ~/Desktop/Project ~/Desktop/Area ~/Desktop/Resource -maxdepth 2 -name "*.PDF" -o -name "*.JPG" -o -name "*.PNG" -o -name "*.DOCX" 2>/dev/null

# 5. Duplikate (Dateien mit (1), (2) etc.)
find ~/Desktop ~/Downloads -name "* (*)*" 2>/dev/null | grep -v .DS_Store

# 6. Leere Dateien
find ~/Desktop ~/Downloads -maxdepth 3 -type f -empty 2>/dev/null | grep -v .DS_Store | grep -v .git

# 7. Inbox-Alter (Dateien älter als 7 Tage)
find ~/Desktop/Inbox -maxdepth 1 -type f -mtime +7 2>/dev/null | grep -v .DS_Store

# 8. /tmp/ Hygiene (User-eigene Dateien)
ls /tmp/*.pdf /tmp/*.json /tmp/*.py /tmp/*.docx /tmp/*.pptx /tmp/*.html 2>/dev/null | head -20
```

Report format:
```
## Audit Report

### Violations Found
- [X] Dateien auf Desktop Root (gehören in Inbox/)
- [X] Downloads nicht leer
- [X] Duplikate gefunden
- [X] Naming violations
- [X] Inbox-Altlasten (>7 Tage)
- [X] /tmp/ Hygiene

### Proposed Fixes
1. Move: `circle-screenshot.png` -> `Inbox/circle-screenshot.png`
2. Delete: `3169886 (1)` (Duplikat)
3. Rename: `Invoice.PDF` -> `260302-vendor-invoice.pdf`

Approve fixes? (y/n)
```

### Mode 2: Classify & File (when user drops files or says "sort this", "file these")

For each file:
1. Read/identify the file (PDF content, filename patterns)
2. Determine PARA category (Project, Area, Resource, Archive)
3. Determine the specific subdirectory within Area/
4. Rename to match conventions
5. Move with approval

Classification rules:
- Eingangsrechnungen -> `Area/Finanzen/rechnungen-eingang/YYMMDD-anbieter-beschreibung.pdf`
- Ausgangsrechnungen -> `Area/Finanzen/rechnungen-ausgang/`
- Provisionsabrechnungen -> `Area/Finanzen/`
- Bankbelege (Sparkasse, ING-DiBa) -> `Area/Persönlich/ING-DiBa/`
- Steuerdokumente -> `Area/Persönlich/Behörden/`
- Krankenkasse -> `Area/Persönlich/TK-Krankenkasse/`
- Verträge -> `Area/Finanzen/` oder `Resource/`
- DATEV-Exporte -> `Area/Finanzen/Datev/`
- Stripe-Daten -> `Area/Finanzen/Stripe/`
- Präsentationen -> `Area/Marketing/`
- Screenshots -> `Inbox/` (zur manuellen Klassifizierung)
- Community-Inhalte -> `Area/Community/`
- Brand-Assets -> `Area/Marketing/brand-design/`
- OAuth/Credentials -> WARNUNG ausgeben, nicht verschieben

### Mode 3: Path Migration (when directories are moved/renamed)

When a directory moves, ALL references must be updated:

1. **Find all references** to the old path:
   ```bash
   grep -r "old/path" ~/.claude.json ~/Desktop/CLAUDE.md ~/.claude/projects/*/memory/MEMORY.md ~/Library/LaunchAgents/*.plist ~/.claude/rules/*.md ~/.claude/agents/*.md ~/.claude/skills/*/SKILL.md 2>/dev/null
   ```

2. **Update each reference** (in order):
   - `~/.claude.json` (MCP server configs)
   - `~/Desktop/CLAUDE.md` (root documentation)
   - `~/.claude/projects/-Users-nicojunk-Desktop/memory/MEMORY.md`
   - `~/Library/LaunchAgents/*.plist` (LaunchAgent configs)
   - `~/.claude/rules/*.md` and `~/.claude/agents/*.md`
   - `~/.claude/skills/*/SKILL.md` (alle Skills)

3. **Reload affected services** if LaunchAgent plist was changed.

4. **Verify** no stale references remain.

### Mode 4: Health Check (quick end-of-session check)

Fast scan, report only:
```bash
# Desktop Root sauber?
STRAY=$(find ~/Desktop -maxdepth 1 -type f ! -name '.DS_Store' ! -name '.env' ! -name 'CLAUDE.md' ! -name 'STATE.json' ! -name 'communication-style.md' 2>/dev/null | wc -l | tr -d ' ')

# Downloads leer?
DL=$(ls ~/Downloads/ 2>/dev/null | grep -cv '^$')

# Inbox-Alter
OLD=$(find ~/Desktop/Inbox -maxdepth 1 -type f -mtime +7 2>/dev/null | grep -cv .DS_Store)

# Duplikate
DUPES=$(find ~/Desktop ~/Downloads -name "* (*)*" 2>/dev/null | grep -cv .DS_Store)

# /tmp/ Dateien
TMP=$(ls /tmp/*.pdf /tmp/*.json /tmp/*.py /tmp/*.docx 2>/dev/null | wc -l | tr -d ' ')

echo "Desktop Root: ${STRAY} fehlplatziert | Downloads: ${DL} Dateien | Inbox alt: ${OLD} | Duplikate: ${DUPES} | /tmp: ${TMP}"
```

### Mode 5: Loop Health Check (for /loop automated runs)

Automatischer Check, der als /loop alle 30 Minuten läuft. Gibt nur bei Problemen Output.

Prüft:
1. Desktop Root: Nur erlaubte Dateien?
2. Downloads: Leer?
3. Inbox: Dateien älter als 7 Tage?
4. Duplikate: Dateien mit `(1)`, `(2)` im Namen?
5. /tmp/ Hygiene: Mehr als 10 Temp-Dateien?
6. Sicherheit: `client_secret_*.json` oder `.env`-Dateien außerhalb Desktop Root?

Bei Problemen: Kurzen Report ausgeben mit vorgeschlagenen Aktionen.
Bei keinen Problemen: "Workspace sauber." und fertig.

## Important Constraints

- NEVER create new top-level directories under ~/Desktop/ (nur die 5 PARA-Ordner)
- NEVER place files directly in Area/ root (immer in Unterordner)
- NEVER use YYYY-MM-DD format (use YYMMDD without dashes)
- NEVER use underscores in new directory names (kebab-case only)
- NEVER move .env, CLAUDE.md, STATE.json vom Desktop Root
- NEVER delete files ohne explizite User-Freigabe (außer 0-Byte-Dateien und offensichtliche Duplikate)
- OAuth/Credential-Dateien: Nur Warnung, niemals automatisch verschieben
- All data lives under ~/Desktop/ (iCloud sync). ~/Downloads/ stays empty.

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
