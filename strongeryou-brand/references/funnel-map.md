# StrongerYou Funnel-Map

Vollständige Dokumentation des Funnels: OnePage-Seiten, 4leads-Automationen, Follow-Up-Sequenzen. Stand 03/2026.

## Funnel-Übersicht

```
TRAFFIC (Meta Ads, Instagram, Organic)
    |
    v
[nicolstanzel.com/] 7-Tage Happy Body Plan (Freebie, 0 EUR)
    |  CTA -> Stripe Checkout (buy.stripe.com/...2400b)
    v
[4leads] Automation "Freebie x TW (1-2)": Welcome-E-Mail + Download
    |  Nach 1 Stunde: Tripwire gekauft?
    |
    +-- NEIN --> Follow-Up "Freebie x Tripwire Funnel" (3 E-Mails, 3 Tage)
    |               Tag 1: "Du machst den gleichen Fehler wie alle anderen"
    |               Tag 2: "{{firstname}} - du bist gerade an der Grenze"
    |               Tag 3: "{{firstname}} - letzte Chance"
    |
    +-- JA (Tag: TW_Happy Body Training_gekauft)
    |       --> Automation "Freebie x TW (2-2)": Follow-Up stoppen + TW Welcome
    |
    v
[Webinar-Registrierung] (3 Wege)
    |  1. 4leads-Formular "StrongerYou 3.0 Launch Workshop Webinarjam"
    |  2. 4leads-Formular "StrongerYou Launch Workshop" (Legacy)
    |  3. Direkt via WebinarJam (Webhook)
    |  4. Manuell (Tag "Webinarregistrierung manuell" -> Zapier -> WebinarJam)
    |
    v
[4leads] Tags: "StrongerYou zum Webinar registriert" (+ WT-Variante)
    |  Registrierungsbestätigungs-E-Mail
    |  Follow-Up startet (6 E-Mails):
    |    3T vor: "Nur noch 3 Tage: Warum die Waage dich belügt"
    |    1T vor: "Morgen X Uhr - 800 Frauen haben es geschafft"
    |    1Std vor: "In 60 Minuten: Die Wahrheit über deinen Stoffwechsel"
    |    15Min vor: "JETZT: In 15 Minuten geht's los!"
    |    2Std nach: "Ich muss was korrigieren (wichtig!)"
    |    1T nach: "WOW"
    |
    v
[WEBINAR LIVE] -> Pitch auf StrongerYou Coaching
    |  Teilnahme-Tracking: Tag "StrongerYou Webinar teilgenommen WT"
    |
    v
[nicolstanzel.com/zahlungsart] Zahlungsauswahl
    |  497 EUR einmal -> Stripe ...2400J
    |  3x 179 EUR     -> Stripe ...2400M
    |  6x 97 EUR      -> Stripe ...2400N
    |
    v
[nicolstanzel.com/danke-nach-kauf] Onboarding
    |  1. E-Mail checken (Zugangsdaten Connect)
    |  2. Body Check ausfüllen (30 Fragen -> personalisierter Ernährungsplan)
    |  3. Community erkunden (Circle/Connect)
    |
    v
[Circle: StrongerYou Connect] Coaching-Community
    |
    |  (nach X.0 Abschluss, PAUSIERT)
    v
[4leads] Follow-Up "Connect Upsell nach X.0 Abschluss" (3 E-Mails)
    Tag 0: "Du hast es geschafft. Und jetzt?"
    Tag 3: "Was Claudia nach dem Coaching anders macht"
    Tag 6: "Morgen schließt sich das Fenster"


NEBENARM: BodyGuide
[nicolstanzel.com/bodyguide] Sales Page (97 EUR, statt 297 EUR)
    |  ACHTUNG: CTA-Link ist DEFEKT (zeigt auf Freebie-Stripe-Link)
```

## OnePage-Seiten (nicolstanzel.com)

### Live-Seiten

| URL | Typ | Headline | Status |
|-----|-----|----------|--------|
| `/` | Lead Magnet (Freebie) | "Du machst alles richtig. Und nimmst trotzdem nicht ab." | OK |
| `/bodyguide` | Produkt-Sales (97 EUR) | "Warum funktioniert keine Diät bei dir?" | CTA DEFEKT |
| `/online-workshop-jan` | Workshop-Anmeldung | "Verwandle Fett in straffe Muskulatur" | CTAs DEFEKT, Datum veraltet |
| `/dankesseite` | Thank You (Workshop) | "Deine Anmeldung war erfolgreich!" | OK |
| `/danke-nach-kauf` | Thank You (Coaching) | "Willkommen in der Stronger You Familie!" | OK |
| `/zahlungsart` | Checkout-Zwischenseite | "Glückwunsch! Du hast dir deinen Platz gesichert." | OK |
| `/impressum` | Rechtlich | Impressum | "Zurück"-Link defekt (/St) |

### Offline/Defekt

| URL | Problem |
|-----|---------|
| `/sty-workshop` | 404 |
| `/datenschutz` | Leitet zu 4leads Login weiter (DSGVO-Problem!) |

### Seitenstruktur-Muster

Alle Sales-Seiten (/, /bodyguide, /online-workshop-jan) teilen:
- Nicol Stanzel Logo oben zentriert
- VSL-Video mit Play-Button
- Identische 3 Testimonials (Lippi, Biggi G., Jenny K.)
- Über-Nicol Bio-Sektion
- Cream-Hintergrund durchgängig

Homepage-Sektionen: Hero -> Problem -> Versprechen -> Plan-Inhalt (5 Bestandteile) -> Über Nicol -> 3 Testimonials -> Finaler CTA -> Footer

## 4leads Automationen

### Aktiv (10)

| Name | Trigger | Kernfunktion |
|------|---------|--------------|
| Connect Kauf \| BodyGuide Gutscheincode Auto-Versand | Tag `connect-annual` oder `connect-monthly` | Prüft Gutscheincode, sendet E-Mail |
| Freebie x TW (1-2) -- Freebie-Einstieg | Formular "Lead: 7-Tage-Challenge" bestätigt | Welcome-E-Mail, nach 1h Follow-Up wenn kein TW-Kauf |
| Freebie x TW (2-2) -- Tripwire-Kauf | Tag `TW_Happy Body Training_gekauft` | Stoppt Follow-Up, sendet TW Welcome |
| SY3.0 Direktregistrierungen Webinarjam | Webhook (WebinarJam) | Tag "zum Webinar registriert" |
| SY 3.0 Webinar Teilnahme | Webhook (WebinarJam) | Tag "Webinar teilgenommen WT" |
| Webinarregistrierung Manuell Step 1 | Tag "Webinarregistrierung manuell" | POST an Zapier-Webhook |
| Webinarregistrierung Manuell Step 2 | Webhook (Zapier-Rückmeldung) | Setzt Webinarraum-URL, startet Launch FU |
| SY3.0 Webinarkampagne Webinarjam | Formular "SY 3.0 Launch Workshop Webinarjam" | Bestätigungs-E-Mail + Webinar FU |
| SY3.0 Webinarkampagne (Legacy) | Formular "StrongerYou Launch Workshop" | Bestätigungs-E-Mail + Launch FU |

### In Bearbeitung (7, alle Evergreen-Funnel)

Alle am 03.03.26 oder früher angelegt. Evergreen-Varianten die den Launch-basierten Flow ablösen sollen:
- Evergreen Funnel \| Webinar Automation
- Evergreen Funnel \| Freebie Start
- LOSCHEN - Evergreen Funnel \| Freebie Start (zum Löschen markiert)
- Evergreen Funnel \| Follow-Up Start nach X.0 Abschluss (1-2 und 2-2)
- SY3.0 Webinarkampagne Everwebinar
- Evergreen Funnel \| StrongerYou X.0 Willkommens-E-Mail bei Kauf + Connect FU

### Verwendete Tags

| Tag | Bedeutung |
|-----|-----------|
| `connect-annual` | Connect Jahresabo gekauft |
| `connect-monthly` | Connect Monatsabo gekauft |
| `TW_Happy Body Training_gekauft` | Tripwire gekauft |
| `StrongerYou zum Webinar registriert` | Webinar-Registrierung (4leads) |
| `StrongerYou zum Webinar registriert WT` | Webinar-Registrierung (WebinarJam) |
| `StrongerYou Manuelle Registrierung` | Manuell registriert |
| `StrongerYou Webinar teilgenommen WT` | Tatsächlich teilgenommen |
| `Webinarregistrierung manuell` | Trigger für manuelle Registrierung |

## Follow-Up-Sequenzen

### Aktiv

| Name | Typ | E-Mails | Pattern |
|------|-----|---------|---------|
| Freebie x Tripwire Funnel | Linear | 3 (über 3 Tage) | Problem -> Urgency -> Letzte Chance |
| StrongerYou Workshop FU Typeform Reg. | Terminserie (fix: 18.01.26) | 6 | Erinnerungen vor/nach Workshop |
| StrongerYou Launch Follow Up | Webinar-Terminserie | 6 | Erinnerungen vor/nach Webinar |
| SY3.0 Webinar Follow Up | Webinar-Terminserie | 6 | Erinnerungen vor/nach Webinar |

### Pausiert

| Name | E-Mails | Zweck |
|------|---------|-------|
| Connect Upsell nach X.0 Abschluss | 3 | Gratulation -> Social Proof -> Deadline |
| SY3.0 Everwebinar Follow Up | 4 | Evergreen-Webinar-Erinnerungen |
| 5x Evergreen Funnel Platzhalter | je 0 | Noch nicht befüllt |

### Webinar-Erinnerungs-Pattern (Standard)

Alle Webinar-FUs folgen dem gleichen Schema:
1. 3 Tage vorher: Teaser-Content ("Warum die Waage dich belügt")
2. 1 Tag vorher: Social Proof ("800 Frauen haben es geschafft")
3. 1 Stunde vorher: Sachlich ("Die Wahrheit über deinen Stoffwechsel")
4. 15 Min vorher: Dringend ("JETZT: In 15 Minuten geht's los!")
5. 2 Stunden nachher: Neugier-Hook ("Ich muss was korrigieren")
6. 1 Tag nachher: Emotionaler Nachklang ("WOW")

## Bekannte Probleme

### Kritisch
1. **`/datenschutz` defekt** - Leitet zu 4leads Login. DSGVO-Verstoß.
2. **`/bodyguide` CTA falsch verlinkt** - Zeigt auf Freebie-Stripe-Link statt BodyGuide-Checkout.
3. **`/online-workshop-jan` CTAs tot** - Alle Links zeigen auf `https://onepage.io/` (Platzhalter).

### Medium
4. **Veraltete Daten** - Workshop "22. Januar" und BodyGuide-Footer "23. Oktober" in der Vergangenheit.
5. **`/impressum` Startseite-Link** zeigt auf `/St` statt `/`.

### Beobachtungen
6. Alle 3 Sales-Seiten verwenden identische Testimonials.
7. Evergreen-Funnel ist in Vorbereitung (7 Platzhalter-Automationen/-Follow-Ups).
8. Connect Upsell FU ist pausiert, kein aktiver Post-Purchase-Upsell.
