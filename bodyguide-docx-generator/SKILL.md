---
name: bodyguide-docx-generator
description: >
  End-to-end BodyGuide production: Fetches Typeform responses, generates personalized
  IF meal plans via AI pipeline, creates PDF from Google Docs template.
  Triggers: bodyguide, ernährungsplan, body guide, PDF, kundenplan, typeform,
  rezepte, IF plan, bodyguide generieren, bodyguide erstellen, /bodyguide
user_invocable: true
invocation: /bodyguide
arguments:
  - name: input
    description: >
      Kundenname, E-Mail, Typeform response ID, oder JSON file path.
      Ohne Argumente: listet ausstehende Typeform-Einreichungen.
    required: false
---

# BodyGuide End-to-End Generator

Ein Aufruf ("Erstelle BodyGuide für Alexandra Arpagaus") produziert ein fertiges, personalisiertes PDF.

## Deliverable

Ein 30+ Seiten PDF mit:
- 15 maßgeschneiderte Rezepte (5 Bausteine x 3 Mahlzeiten) mit AI-generierten Food-Fotos
- 22 personalisierte Snacks (4 Kategorien)
- Wissenschaftlich berechnete Kalorien (Zutat-für-Zutat validiert)
- CravingControl-Strategien die auf die individuelle Lebenssituation eingehen
- Alles im StrongerYou Brand-Design

## Der Flow

```
TYPEFORM ──> PROFIL ──> KALORIEN ──> KONTEXT ──> REZEPTE ──> SNACKS ──> BILDER ──> GOOGLE DOCS ──> PDF
  (API)      (parse)   (Formel)    (Recherche)   (AI+Validierung)    (Gemini)    (Template)     (Export)
```

Kein Schritt wird übersprungen. Der Agent orchestriert alles selbst.

## 1. Kundendaten abrufen

Zwei Typeform-Formulare durchsuchen (nach Name oder E-Mail):

```bash
TYPEFORM_KEY=$(grep '^TYPEFORM_API_TOKEN=' ~/Desktop/.env | cut -d= -f2)
# SY X.0 BodyGuide Fragebogen
curl -s "https://api.typeform.com/forms/ff3KTDd9/responses?page_size=200&sort=submitted_at,desc" -H "Authorization: Bearer $TYPEFORM_KEY"
# Body-Check Fragebogen (alternatives Formular)
curl -s "https://api.typeform.com/forms/iMjEnQr4/responses?page_size=200&sort=submitted_at,desc" -H "Authorization: Bearer $TYPEFORM_KEY"
```

Relevante Felder: firstName, lastName, email, age, height, current_weight, goal_weight, Wechseljahre, nutrition_preference, Abneigungen, Lieblings_Proteinquellen, Heisshunger_tageszeit, training_frequency, sleep_hours, stress_level, desired_recipes, meal_prep_time, additional_info.

## 2. Kalorienberechnung (deterministisch, kein AI)

```
BMR (Mifflin-St Jeor, Frauen) = (10 × Gewicht_kg) + (6.25 × Größe_cm) - (5 × Alter) - 161

Aktivitätsfaktor:
  Sitzend (Büro, wenig Bewegung)                = 1.2
  Leicht aktiv (aktiver Job, Spaziergänge)      = 1.375
  Moderat aktiv (3-5x Sport/Woche)              = 1.55
  Sehr aktiv (6-7x Sport/Woche, körperlich)     = 1.725

TDEE = BMR × Aktivitätsfaktor
Zielkalorien = TDEE - 350 kcal (moderates Defizit)
Protein = 2g × Zielgewicht_kg, Fett = 30% der Zielkalorien, Carbs = Rest
```

## 3. Kundenkontext aggregieren

Bevor Rezepte entstehen, alle verfügbaren Infos sammeln:
- **Typeform**: Die Fragebogen-Antworten (Schritt 1)
- **Stripe** (via Supabase): Welches Produkt? Wann gekauft? Repeat Customer?
- **E-Mail-Verlauf**: Hat die Kundin spezielle Wünsche per Mail geäußert?
- **Circle**: Aktiv in der Community? Welche Fragen gestellt?

Das fließt als Kontext in die Rezeptgenerierung ein. Spezialanforderungen wie "Nachtdienst", "Reisen", "kleine Küche" oder "koche für die ganze Familie" verändern die Baustein-Stile grundlegend.

## 4. Rezepte generieren + validieren

### Kalorien-Referenztabelle (pro 100g Rohgewicht)

| Zutat | kcal | Zutat | kcal | Zutat | kcal |
|-------|------|-------|------|-------|------|
| Quinoa | 350 | Reis | 350 | Haferflocken | 370 |
| Hähnchen | 110 | Eier (1=60g) | 155 | Lachs | 208 |
| Skyr | 63 | Magerquark | 67 | Hüttenkäse | 98 |
| Feta | 264 | Avocado | 160 | Cashews | 580 |
| Olivenöl | 884 | Honig | 304 | Tomaten | 18 |
| Paprika | 27 | Gurke | 12 | Zucchini | 17 |
| Brokkoli | 34 | Beeren | 45 | Chia | 486 |
| Leinsamen | 534 | Banane | 89 | Thunfisch(Dose) | 110 |
| Tofu | 144 | Kichererbsen(Dose) | 120 | Spinat | 23 |
| Süßkartoffel | 86 | Parmesan | 400 | Mozzarella light | 180 |
| Walnüsse | 654 | Apfel | 52 | Backkakao | 228 |
| Linsen(rot,trocken) | 330 | Tortilla | 300 | Vollkornbrot | 220 |
| Hackfleisch(mager) | 170 | Erdnüsse | 567 | Proteinpulver | 380 |

1 TL Öl = 4.5g = 40 kcal. 1 EL Öl = 13.5g = 120 kcal. 1 TL Honig = 7g = 21 kcal.

### Rezept-Regeln

- 5 Bausteine (A-E) × 3 Mahlzeiten = 15 total
- Alle Gewichte = Rohgewicht
- Max 2 Fleischmahlzeiten von 15
- 80%+ der Lieblingsproteine verwenden
- Keine abgelehnten Lebensmittel oder Allergene
- Max 40% Zutaten-Überlappung zwischen Mahlzeiten
- Min 5 Küchenstile über 15 Mahlzeiten
- Rezeptname: max 30 Zeichen, verboten: Power, Kraft, Energie, Boost, Super, Mega, Ultra, Golden
- Zutaten: max 100 Zeichen. Zubereitung: max 120 Zeichen
- Zubereitungszeit gemäß Kundenwunsch

### Kalorienvalidierung (PFLICHT, jedes Rezept)

Jede Zutat einzeln: `Menge_g × kcal_pro_100g / 100 = Teilkalorien`. Summe aller Teilkalorien muss +/-5% der angegebenen Kalorien sein. Wenn nicht: Mengen anpassen, neu berechnen.

### CravingControl (pro Mahlzeit)

| Feld | Max Wörter | Inhalt |
|------|-----------|--------|
| was | 8 | Was hilft gegen den Craving |
| warum | 10 | Wissenschaftliche Begründung |
| lösung | 20 | Praktischer Tipp, bezogen auf Kundensituation |

### Baustein-Personalisierung

Die 5 Bausteine passen sich an die Lebenssituation an:
- **Nachtdienst**: kalt essbar, transportabel, geräuschlos
- **Bürojob**: Box-tauglich, Mikrowelle möglich
- **Familie**: Alle essen mit, kinderfreundlich
- **Wenig Zeit**: Max 15 Min Zubereitung
- **Sportlerin**: Pre/Post-Workout optimiert

## 5. Snacks generieren

22 Snacks (~130 kcal), 4 Kategorien:
- Vegan (6), Vegetarisch (6), Flexitarisch (5), Midnight (5)
- Keine abgelehnten Lebensmittel, Favoriten priorisieren

## 6. Rezeptbilder (Gemini nano-banana-pro-preview)

```python
GOOGLE_API_KEY = grep_env("GOOGLE_API_KEY")
PREFIX = (
    "Editorial food photography, warm cream tones, soft natural lighting from left, "
    "shallow depth of field, overhead angle 30-45 degrees, rustic ceramic plate or bowl, "
    "premium magazine aesthetic, NOT stock photo, NOT clinical, NOT generic AI aesthetic. "
    "Photo of: "
)
# Endpoint: generativelanguage.googleapis.com/v1beta/models/nano-banana-pro-preview:generateContent
# responseModalities: ["IMAGE", "TEXT"]
# Prompt: {PREFIX}{Rezeptname}. Main ingredients visible: {Zutaten}. Beautiful plating on rustic surface.
```

15 Bilder speichern: `/tmp/bodyguide-images/{A1..E3}.png`

## 7. Google Docs Template befüllen

### Template kopieren + Platzhalter ersetzen
```bash
python3 ~/.claude/skills/bodyguide-docx-generator/scripts/generate-bodyguide-gdocs.py input.json output.pdf
```

Template-ID: `14ZH_XVuYZUJuKsJzuQQKQCEHgbrJnaKQ1ipyRGr3K_Y` (197 Platzhalter, 12.5 MB)
Details: `references/placeholder-map.md`

### Bilder einfügen via GCS (replaceImage Workaround)

Google Docs `replaceImage` akzeptiert KEINE Google Drive URLs. Lösung:

```bash
# 1. Upload nach GCS
gcloud storage cp /tmp/bodyguide-images/*.png gs://strongeryou2/bodyguide-temp/
# 2. Platzhalter-Image-IDs aus Dokument extrahieren (214x287, gleiche URI = Rezept-Platzhalter)
# 3. replaceImage mit https://storage.googleapis.com/strongeryou2/bodyguide-temp/{CODE}.png
# 4. Cleanup nach Export: gcloud storage rm gs://strongeryou2/bodyguide-temp/*
```

## 8. PDF-Export

```bash
TOKEN=$(gcloud auth print-access-token)
curl -sL -H "Authorization: Bearer $TOKEN" -o output.pdf \
  "https://docs.google.com/document/d/{DOC_ID}/export?format=pdf"
```

## Repeat Customers

Vorherige Rezeptnamen abrufen (E-Mail-Historie, Airtable). Alle neuen Rezepte komplett anders: andere Küchen, Kochmethoden, Zutaten-Kombinationen.

## Qualitäts-Checkliste (vor Export)

- [ ] 15 Rezepte kalorienvalidiert (Zutat-für-Zutat, +/-5%)
- [ ] Keine abgelehnten Lebensmittel
- [ ] 80%+ Lieblingsproteine verwendet
- [ ] Max 2 Fleischmahlzeiten
- [ ] Rezeptnamen unter 30 Zeichen, keine verbotenen Wörter
- [ ] CravingControl referenziert Kundendaten
- [ ] Bausteine passen zum Lebensstil
- [ ] 15 Bilder via nano-banana-pro-preview generiert
- [ ] Bilder via GCS in Google Doc eingefügt
- [ ] PDF exportiert (>5 MB = OK)

## Dependencies

- `GOOGLE_API_KEY` in ~/Desktop/.env (Bildgenerierung)
- `TYPEFORM_API_TOKEN` in ~/Desktop/.env
- gws CLI (Drive + Docs Scopes)
- gcloud CLI (PDF-Export, GCS)
- GCS Bucket: `gs://strongeryou2/bodyguide-temp/`

## File Map

| Datei | Zweck |
|-------|-------|
| `scripts/generate-bodyguide-gdocs.py` | Template kopieren + Platzhalter ersetzen + PDF |
| `scripts/generate-bodyguide.py` | Legacy DOCX Generator (Fallback) |
| `references/placeholder-map.md` | 197 Platzhalter mit Casing-Dokumentation |
| `references/brand-rules.md` | Brand-Farben, Fonts, Layout |

## Casing-Gotchas im Template

- `{{firstName}}` vs `{{firstname}}` (Titelseite vs Intro)
- Bausteine: A immer groß, B-E gemischt
- CravingControl: meist klein, Ausnahme `{{cravingcontrolwas.D.3}}`
- `cravingcontrol-warum` (MIT Bindestrich), `cravingcontrolwas`/`cravingcontrollösung` (OHNE)

Das Script handhabt alle Varianten korrekt.

## Self-Healing: Fehler erkennen und beheben

Dieser Workflow hat mehrere Stellen die fehlschlagen können. Bei jedem Fehler: nicht abbrechen, sondern den alternativen Pfad nehmen.

### Typeform nicht gefunden
- Kundenname in BEIDEN Formularen suchen (ff3KTDd9 UND iMjEnQr4)
- Auch nach E-Mail suchen, nicht nur nach Name
- Wenn in keinem Formular: E-Mail-Verlauf durchsuchen, ob der Fragebogen-Link geschickt wurde
- Wenn kein Typeform: Daten manuell aus E-Mail-Korrespondenz extrahieren (Kundin hat oft relevante Infos per Mail geschickt)

### Kalorien-Diskrepanz
- Wenn berechnete Kalorien >5% vom Zielwert abweichen: Mengen anpassen, NICHT die angegebenen Kalorien fälschen
- Zutat mit dem größten Anteil zuerst anpassen (z.B. 150g Hähnchen -> 130g)
- Nach Anpassung neu berechnen und Validierung wiederholen

### Bildgenerierung fehlgeschlagen
- nano-banana-pro-preview Modell zuerst versuchen
- Fallback 1: gemini-2.5-flash-image
- Fallback 2: imagen-4.0-generate-001 (predict endpoint)
- Wenn alle fehlschlagen: Platzhalterbilder im Template belassen, im Log vermerken

### GCS Upload fehlgeschlagen
- Prüfe ob gcloud authentifiziert: `gcloud auth list`
- Prüfe ob Bucket existiert: `gcloud storage ls gs://strongeryou2/`
- Fallback: Bilder in Google Drive hochladen, auch wenn replaceImage damit nicht funktioniert. PDF hat dann Platzhalterbilder.

### Google Docs API Fehler
- Bei 500er: 10 Sekunden warten, einmal wiederholen
- Bei "exportSizeLimitExceeded": curl mit access token statt gws export
- Bei batchUpdate-Fehler: Batch-Größe von 50 auf 20 reduzieren

### PDF zu klein (<1 MB)
- Wahrscheinlich eine Fehlerseite statt echtem PDF
- Erste 200 Bytes lesen und prüfen ob es "%PDF" startet
- Wenn nicht: Token erneuern (`gcloud auth print-access-token`) und erneut exportieren

### .env Variablen nicht gefunden
- NICHT raten. Immer prüfen: `grep '^VARIABLENNAME' ~/Desktop/.env | head -1`
- `source ~/Desktop/.env` funktioniert NICHT zuverlässig in Subshells. Immer grep + cut verwenden.
- Bekannte Variablen: GOOGLE_API_KEY, TYPEFORM_API_TOKEN, STRIPE_API_KEY

## Duplizierten Template-Hinweis

Die Produktion-Vorlage (Original) darf NICHT verändert werden:
- **Original (NICHT ANFASSEN):** `14ZH_XVuYZUJuKsJzuQQKQCEHgbrJnaKQ1ipyRGr3K_Y`
- **Arbeitskopie für Redesign:** `1qS4mw-YqGmyC1NkYKJIvhx5G7LZTDy-iSeiMqFlziUI`

Für jeden BodyGuide wird eine frische Kopie des Templates erstellt. Die Kopie wird nach PDF-Export NICHT gelöscht (falls Nachbearbeitung nötig).

## Session-Learnings (Self-Improvement)

Diese Erkenntnisse stammen aus der Session 2026-03-08:

1. **Typeform hat 2 Formulare**: ff3KTDd9 (SY X.0) und iMjEnQr4 (Body-Check). Immer beide durchsuchen.
2. **source .env Bug**: `source ~/Desktop/.env` lädt Keys nicht in Bash-Subshells. Fix: `grep + cut`.
3. **replaceImage + Drive = kaputt**: Google Docs API replaceImage akzeptiert KEINE Drive URLs. Nur GCS (`storage.googleapis.com`) funktioniert.
4. **Platzhalter-Reihenfolge**: Die 15 Rezept-Platzhalterbilder (214x287, gleiche URI) erscheinen im Dokument in der Reihenfolge A1-E3. Reihenfolge per API extrahieren, NICHT raten.
5. **PDF-Export >10MB**: Google API Export schlägt fehl. curl mit gcloud access token nutzen.
6. **Kalorienvalidierung**: AI schätzt Kalorien ungenau. Immer selbst Zutat-für-Zutat berechnen mit der Referenztabelle.
