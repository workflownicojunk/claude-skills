# Provisionsabrechnung Design-Spezifikation

Exakt extrahiert aus der Original-DOCX-Vorlage:
`~/Downloads/Provisionsabrechnung_StrongerYou_X0_30_Dez2025_Jan2026.docx`

## Farben

| Token | HEX | Verwendung |
|-------|-----|------------|
| dark | #241404 | Headlines, Body-Text, Provisionsbetrag |
| blue | #7A94CC | Sub-Headlines, Tabellen-Header-Fill, Gesamt-Zeile-Fill, Formel-Box-Rahmen |
| brown | #96827D | Labels, Captions, Footer, Header, Tabellen-Rahmen |
| white | #FFFFFF | Seiten-BG, Tabellen-Datenzeilen (ungerade) |
| cream | #FAEDE1 | Tabellen-Datenzeilen (gerade), Highlight-Box-Fill |

## Typografie (exakt aus DOCX XML)

| Element | Font | Size (half-pt) | Color | Style |
|---------|------|----------------|-------|-------|
| H1 "Provisionsabrechnung" | Playfair Display | 56 | #241404 | Bold Italic |
| H2 Untertitel | Playfair Display | 40 | #7A94CC | Bold Italic |
| Sektions-Headline | Playfair Display | 36 | #241404 | Bold Italic |
| Sub-Headline | Playfair Display | 22-28 | #7A94CC | Bold Italic |
| Provisionsbetrag (gross) | Playfair Display | 48 | #241404 | Bold Italic |
| "Abrechnungszeitraum" Label | Noto Sans | 22 | #96827D | Regular |
| Zeitraum-Wert | Noto Sans | 28 | #241404 | Bold |
| Auftraggeber Label | Noto Sans | 18 | #96827D | Regular |
| Firmenname | Noto Sans | 22 | #241404 | Bold |
| Personenname | Noto Sans | 20 | #241404 | Regular |
| Body-Text | Noto Sans | 22 | #241404 | Regular |
| Grundlage/Caption | Noto Sans | 20 | #96827D | Regular |
| Tabellen-Header | Noto Sans | 20 | #FFFFFF | Bold |
| Tabellen-Daten | Noto Sans | 20 | #241404 | Bold |
| Tabellen-Gesamt | Noto Sans | 20 | #FFFFFF | Bold |
| Highlight-Box Label | Noto Sans | 22 | #96827D | Regular |
| Formel-Box Text | Noto Sans | 22 | #96827D/#241404 | Regular/Bold |

## Tabellen

### Header-Zeile
- Fill: #7A94CC (blau)
- Schrift: Noto Sans Bold 20hp, #FFFFFF
- Borders: #96827D (braun), 1pt, alle Seiten

### Datenzeilen
- Fill alternierend: ungerade = #FFFFFF, gerade = #FAEDE1
- Schrift: Noto Sans Bold 20hp, #241404
- Borders: #96827D (braun), 1pt, alle Seiten
- Zahlen: rechtsbuendig, Text: linksbuendig

### Gesamt-Zeile (in Zusammenfassungstabellen)
- Fill: #7A94CC (blau, identisch mit Header)
- Schrift: Noto Sans Bold 20hp, #FFFFFF
- Borders: #96827D (braun), 1pt

### Gesamt-Zeile (in Detail-Tabellen)
- Fill: #FAEDE1 (cream, wie gerade Zeile)
- Schrift: Noto Sans Bold 20hp, #241404
- Borders: #96827D (braun), 1pt

## Highlight-Box (Provisions-Zusammenfassung)

- Fill: #FAEDE1 (cream)
- Borders: KEINE (borderless)
- Label: Noto Sans 22hp, #96827D, zentriert
- Betrag: Playfair Display Bold Italic 48hp, #241404 (DUNKELBRAUN, nicht blau!)

## Formel-Box (Provisionsberechnung)

- Fill: #FFFFFF (weiss)
- Borders: #7A94CC (blau), 2pt, alle Seiten
- Text: Noto Sans 22hp, #96827D (Label) / #241404 (Wert)
- Ergebnis: Playfair Display Bold Italic 48hp, #241404

## Titelseite

Kein Header, kein Footer.

1. Logo: StrongerYou Wordmark, zentriert, 200x57pt
2. "Provisionsabrechnung": Playfair 56hp #241404 BI, zentriert
3. Untertitel: Playfair 40hp #7A94CC BI, zentriert
4. Blaue Linie: 3400 DXA, bottom-border #7A94CC 3pt
5. "Abrechnungszeitraum": Noto Sans 22hp #96827D, zentriert
6. Zeitraum: Noto Sans 28hp #241404 Bold, zentriert
7. Auftraggeber/Auftragnehmer: 2-Spalten-Table, borderless
8. "Grundlage: ...": Noto Sans 20hp #96827D, zentriert
9. "Erstellt am ...": Noto Sans 20hp #96827D, zentriert

## Inhaltsseiten

- Header rechts: Dokumenttitel, Noto Sans 14hp #96827D
- Footer links: "(C) Lightness FitnessSeite X", Noto Sans 15hp #96827D

## Logo-Pfad

`~/Desktop/Area/Marketing/brand-design/assets/logos/strongeryou-logo-dark.png`
Seitenverhaeltnis: 3.51:1 (2560x729px)

## Vorlage-Datei

Die Original-DOCX liegt unter: `~/Downloads/Provisionsabrechnung_StrongerYou_X0_30_Dez2025_Jan2026.docx`
