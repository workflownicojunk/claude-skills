# BodyGuide Platzhalter-Map (Google Docs Template)

**Template:** BodyGuide 2.0 [Template]
**Google Docs ID:** 14ZH_XVuYZUJuKsJzuQQKQCEHgbrJnaKQ1ipyRGr3K_Y
**Dateigroe?e:** 12.5 MB (zu gro? fuer Google Export als DOCX/HTML wegen eingebetteter Bilder)
**Plain Text Export:** 26.896 Zeichen, 1.158 Zeilen
**Platzhalter gesamt:** 198 Vorkommen, 196 unique

## Dokumentstruktur (Sektionen)

| Sektion | Zeilen (txt) | Inhalt |
|---------|-------------|--------|
| Titelseite | 1-4 | `{{firstName}}'s Personal Body Guide` |
| Intro-Brief | 9-62 | Personalisierte Ansprache, Baukastensystem erklaert |
| Sweet-Spot-Prinzip | 52-99 | 3 Saeulen: Timing, Ernaehrung, Training |
| Tipps-Tabelle | 105-150 | Pre/Post-Workout Ernaehrung |
| Fitness Journey | 152-171 | Kundendaten-Tabelle (Name, Alter, Gewicht etc.) |
| Weekly Meal Planner | 174-226 | 5x3 Uebersichtstabelle |
| Bausteine A-E | 231-573 | Je 3 Rezepte mit Kalorien, Zutaten, Zubereitung, CravingControl |
| Cheat-Days | 576-604 | Erklaerung der 2 freien Tage |
| Getraenke-Guide | 617-714 | Hydration, Alkohol, Trink-Protokoll |
| Snack-Erklaerung | 716-786 | Warum/wann/wie snacken |
| Snack-Karten | 789-1011 | 4 Tabellen (vegan, veggie, omnivor, midnight) |
| Workout-Guide | 1014-1095 | 4 Home-Workouts, Anleitung |
| Partner-Links | 1097-1135 | Harvest Republic, Les Mills, InnoNature |
| Abschluss | 1148-1159 | Nicols Schlusswort |

## Platzhalter nach Kategorie

### 1. Kundendaten (10 unique, 12 Vorkommen)

| Platzhalter | Vorkommen | Kontext |
|-------------|-----------|---------|
| `{{firstName}}` | 1x | Titelseite |
| `{{firstname}}` | 1x | Intro-Brief (ACHTUNG: anderes Casing!) |
| `{{Name}}` | 3x | Fitness Journey Tabelle + Meal Planner |
| `{{Alter}}` | 1x | Fitness Journey |
| `{{Groe?e}}` | 1x | Fitness Journey |
| `{{Aktuelles Gewicht}}` | 1x | Fitness Journey |
| `{{Zielgewicht}}` | 1x | Fitness Journey |
| `{{Gesamtenergieumsatz}}` | 1x | Fitness Journey |
| `{{Tagesanpassung/Tag}}` | 1x | Fitness Journey |
| `{{Angepasster Energieumsatz}}` | 1x | Fitness Journey |
| `{{Ernaehrungsform}}` | 1x | Fitness Journey |

**ACHTUNG:** `{{firstName}}` vs `{{firstname}}` - inkonsistentes Casing im Original!

### 2. Meal Plan Uebersicht (15)

Pattern: `{{Option.[A-E].Meal.[1-3]}}`

Tabelle im Weekly Meal Planner:
```
Option | Energiestart | Energie-Power | Ausklang
A      | Option.A.Meal.1 | Option.A.Meal.2 | Option.A.Meal.3
B      | Option.B.Meal.1 | Option.B.Meal.2 | Option.B.Meal.3
C      | Option.C.Meal.1 | Option.C.Meal.2 | Option.C.Meal.3
D      | Option.D.Meal.1 | Option.D.Meal.2 | Option.D.Meal.3
E      | Option.E.Meal.1 | Option.E.Meal.2 | Option.E.Meal.3
```

### 3. Rezepte pro Baustein (60 Felder = 5 Bausteine x 3 Mahlzeiten x 4 Felder)

Pattern: `{{Typ.[A-E].[1-3]}}`

| Feld | Anzahl | Pattern |
|------|--------|---------|
| Rezeptname | 15 | `{{Rezeptname.[A-E].[1-3]}}` |
| Kalorien | 15 | `{{Kalorien.[A-E].[1-3]}}` |
| Zutaten | 15 | `{{Zutaten.[A-E].[1-3]}}` |
| Zubereitung | 15 | `{{Zubereitung.[A-E].[1-3]}}` |

**ACHTUNG: Inkonsistentes Casing im Original!**
- Baustein A: durchgehend Grossbuchstaben (`A.1`, `A.2`, `A.3`)
- Baustein B: gemischt (`B.1`, `b.2`, `B.3`, `b.3`)
- Baustein C: gemischt (`c.1`, `C.2`, `c.3`)
- Baustein D: gemischt (`d.1`, `D.2`, `D.3`)
- Baustein E: gemischt (`E.1`, `E.2`/`e.2`, `E.3`)

Der Generator muss case-insensitive replacen!

### 4. CravingControl (45 = 5 Bausteine x 3 Mahlzeiten x 3 Felder)

Pattern: `{{cravingcontrol[typ].[a-e].[1-3]}}`

| Feld | Pattern | Beispiel |
|------|---------|----------|
| Was | `{{cravingcontrolwas.[a-e].[1-3]}}` | Was loest den Craving aus |
| Warum | `{{cravingcontrol-warum.[a-e].[1-3]}}` | Wissenschaftliche Erklaerung |
| Loesung | `{{cravingcontrolloesung.[a-e].[1-3]}}` | Praktische Loesung |

**ACHTUNG:** Inkonsistente Namenskonvention:
- `cravingcontrolwas` (zusammen, kein Bindestrich)
- `cravingcontrol-warum` (MIT Bindestrich!)
- `cravingcontrolloesung` (zusammen, kein Bindestrich, oe statt ?)

Casing: meist Kleinbuchstaben, Ausnahme `{{cravingcontrolwas.D.3}}`

### 5. Snack-Karten (62 Felder = 4 Kategorien x ~5-6 Snacks x 3 Felder)

#### Vegan (18 = 6 Snacks x 3 Felder)
```
{{vegan.name.[1-6]}}
{{vegan.ingredients.[1-6]}}
{{vegan.preparation.[1-6]}}
```

#### Vegetarisch (18 = 6 Snacks x 3 Felder)
```
{{vegetarian.name.[1-6]}}
{{vegetarian.ingredients.[1-6]}}
{{vegetarian.preparation.[1-6]}}
```

#### Flexitarisch/Omnivor (15 = 5 Snacks x 3 Felder)
```
{{flexitarian.name.[1-5]}}
{{flexitarian.ingredients.[1-5]}}
{{flexitarian.preparation.[1-5]}}
```

#### Midnight/Nacht-Regeneration (15 = 5 Snacks x 3 Felder)
```
{{midnight.name.[1-5]}}
{{midnight.ingredients.[1-5]}}
{{midnight.preparation.[1-5]}}
```

### 6. Bilder (18 Vorkommen, 4 unique)

| Dateiname | Vorkommen | Kontext |
|-----------|-----------|---------|
| `offset_355676.jpg` | 15x | Rezept-Bilder (Baustein A-E, je 3) |
| `a27687adfefecdea542ba6ba5819d223.jpg` | 1x | Timing-Illustration |
| `1f622a34ab4747a879a230bd8a239352.jpg` | 1x | Tipps-Bild |
| `2447b165db33f54538e2e5bc332991ec.jpg` | 1x | Workout-Guide Bild |

`offset_355676.jpg` ist ein Platzhalter-Bild, das durch generierte Food-Fotos ersetzt wird.

## Zusammenfassung Platzhalter-Counts

| Kategorie | Unique | Vorkommen |
|-----------|--------|-----------|
| Kundendaten | 10 | 12 |
| Meal Plan Uebersicht | 15 | 15 |
| Rezeptname | 15 | 15 |
| Kalorien | 15 | 15 |
| Zutaten | 15 | 15 |
| Zubereitung | 15 | 15 |
| CravingControl | 45 | 45 |
| Snacks Vegan | 18 | 18 |
| Snacks Vegetarisch | 18 | 18 |
| Snacks Flexitarisch | 15 | 15 |
| Snacks Midnight | 15 | 15 |
| **TOTAL** | **196** | **198** |

## JSON-Input-Schema (fuer generate-bodyguide.py)

```json
{
  "customer": {
    "firstName": "Sarah",
    "name": "Sarah M.",
    "alter": "42",
    "groesse": "168",
    "aktuellesGewicht": "78",
    "zielgewicht": "68",
    "gesamtenergieumsatz": "1.850 kcal",
    "tagesanpassung": "-350 kcal",
    "angepassterEnergieumsatz": "1.500 kcal",
    "ernaehrungsform": "Flexitarisch"
  },
  "mealPlan": {
    "A": { "meal1": "...", "meal2": "...", "meal3": "..." },
    "B": { "meal1": "...", "meal2": "...", "meal3": "..." },
    "C": { "meal1": "...", "meal2": "...", "meal3": "..." },
    "D": { "meal1": "...", "meal2": "...", "meal3": "..." },
    "E": { "meal1": "...", "meal2": "...", "meal3": "..." }
  },
  "recipes": {
    "A": [
      {
        "name": "Avocado-Ei Bowl",
        "kalorien": "420",
        "zutaten": "1 Avocado, 2 Eier, ...",
        "zubereitung": "Avocado halbieren, ...",
        "imageUrl": "https://...",
        "cravingControl": {
          "was": "Suesses nach dem Fruehstueck",
          "warum": "Blutzucker-Abfall nach ...",
          "loesung": "Zimt ins Fruehstueck ..."
        }
      }
    ]
  },
  "snacks": {
    "vegan": [
      { "name": "...", "ingredients": "...", "preparation": "..." }
    ],
    "vegetarian": [ ... ],
    "flexitarian": [ ... ],
    "midnight": [ ... ]
  },
  "images": {
    "recipeImages": { "A.1": "url_or_path", ... },
    "heroImages": { "timing": "url_or_path", "tips": "url_or_path", "workout": "url_or_path" }
  }
}
```
