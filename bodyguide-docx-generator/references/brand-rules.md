# BodyGuide DOCX Brand Rules

## Format
- **Typ:** DOCX (Word-Dokument), NICHT PPTX-Slides
- **Seitenformat:** A4 Hochformat
- **Export:** DOCX -> PDF via LibreOffice CLI

## Farben (identisch mit PPTX Brand)

| Token | HEX | Verwendung |
|-------|-----|------------|
| Background | `#FAEDE1` | Seiten-Hintergrund (Cream) - nur fuer Abschnittstrennungen |
| Card | `#FFFEF2` | Tabellen-Hintergrund, Box-Hintergrund |
| Dark | `#241404` | Headlines, Body Text |
| Blue | `#7A94CC` | Akzent: Ueberschriften, Trennlinien, Baustein-Labels |
| Brown | `#96827D` | Footer, Captions, Seitenzahlen |

**VERBOTEN:** `#000000` (immer `#241404`), Blue als Flaechenfuellung

## Typografie

| Element | Font | Groesse | Style |
|---------|------|---------|-------|
| Dokumenttitel | Playfair Display | 28pt | Bold Italic |
| Abschnittstitel | Playfair Display | 22pt | Bold Italic |
| Rezeptname | Playfair Display | 18pt | Bold Italic |
| Body Text | Noto Sans | 11pt | Regular |
| Tabellen-Header | Noto Sans | 10pt | Bold |
| Tabellen-Body | Noto Sans | 10pt | Regular |
| Kalorienangabe | Noto Sans | 12pt | Bold, Blue |
| CravingControl Labels | Noto Sans | 9pt | Bold, Blue |

## Seitenstruktur

### Seite 1: Titelseite
- Grosser Name + "Personal Body Guide"
- Logo oben rechts
- Cream-Hintergrund

### Seiten 2-5: Einfuehrung
- Fliesstext mit Nicols Stimme
- Bullet Points mit Stern-Symbol
- Bilder inline (Timing, Sweet Spot)

### Seite 6: Fitness Journey Tabelle
- 2-spaltige Tabelle (Label | Wert)
- Card-Hintergrund (#FFFEF2)
- Blaue Trennlinie oben

### Seite 7: Weekly Meal Planner
- 4-spaltige Tabelle (Option | Energiestart | Energie-Power | Ausklang)
- 5 Zeilen (A-E)
- Header in Blue (#7A94CC)

### Seiten 8-22: Bausteine A-E (je 3 Seiten)
Pro Rezept:
- Baustein-Label (z.B. "Baustein A") in Blue
- Rezeptname als Headline
- Rezeptbild (rechteckig, abgerundete Ecken)
- Kalorienangabe
- Zutaten (Bullet-Liste)
- Zubereitung (nummerierte Liste)
- CravingControl-Box: Was/Warum/Loesung in Card-Hintergrund

### Seiten 23-25: Cheat Days + Getraenke
- Fliesstext
- Trink-Protokoll Tabelle

### Seiten 26-29: Snack-Karten (4 Tabellen)
Pro Kategorie:
- Kategorie-Header (VEGAN, VEGGIE, OMNIVOR, NACHT-REGENERATION)
- 4-spaltige Tabelle (kcal | Name | Zutaten | Zubereitung)
- 5-6 Zeilen pro Kategorie

### Seiten 30-32: Workout-Guide
- 4 Uebungen mit Beschreibung
- Timing-Regeln

### Seite 33: Partner-Links + Abschluss
- Harvest Republic, Les Mills, InnoNature
- Nicols Schlusswort

## Bilder

### Rezeptbilder (15)
- Position: ueber Zutaten/Zubereitung
- Groesse: Seitenbreite minus Raender (ca. 16cm)
- Hoehe: max 8cm
- Abgerundete Ecken: 8pt (via python-docx XML)

### Statische Bilder (3)
- Timing-Illustration
- Tipps-Bild
- Workout-Bild
- Quelle: Google Docs Template (eingebettet)

## python-docx Spezifika

### Font-Installation pruefen
```bash
# Playfair Display und Noto Sans muessen installiert sein
fc-list | grep -i "playfair"
fc-list | grep -i "noto sans"
```

### Seitenraender
```python
from docx.shared import Cm
sections = document.sections
for section in sections:
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
```

### Farb-Helper
```python
from docx.shared import RGBColor

COLORS = {
    'dark': RGBColor(0x24, 0x14, 0x04),     # #241404
    'blue': RGBColor(0x7A, 0x94, 0xCC),     # #7A94CC
    'brown': RGBColor(0x96, 0x82, 0x7D),    # #96827D
    'card': RGBColor(0xFF, 0xFE, 0xF2),     # #FFFEF2
    'cream': RGBColor(0xFA, 0xED, 0xE1),    # #FAEDE1
}
```
