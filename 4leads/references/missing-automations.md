# Empfohlene neue Automations für 4leads

**Stand:** 2026-02-22
**Basis:** Analyse der 11 bestehenden Automations, 47 Kampagnen-Stats, Customer Journey Gaps

## Priorität 1 — Sofortiger ROI

### Automation: BodyGuide Post-Kauf Onboarding
- **Trigger:** Tag "BG_97EUR_gekauft" hinzugefügt (data-type: 11000)
- **Ziel:** Onboarding + Upsell auf StrongerYou Coaching
- **Steps:**
  1. E-Mail: "Dein BodyGuide ist unterwegs" (sofort)
  2. Warte 2 Tage
  3. E-Mail: "So holst du das Maximum aus deinem BodyGuide" (Tipps)
  4. Warte 5 Tage
  5. E-Mail: "Wie läuft's? Hier sind 3 Turbo-Tipps" (Check-in)
  6. Warte 7 Tage
  7. Bedingung: Hat SYX.0 bereits?
  8. Falls nein: E-Mail "Bereit für den nächsten Schritt? StrongerYou X.0" (Upsell)
- **Warum jetzt:** 276 BodyGuide-Käufer bekommen NULL Onboarding. Größter Quick-Win.
- **Erwarteter Impact:** 5-10% Upsell auf SY = ~14-28 neue Coaching-Kunden

### Automation: Re-Engagement Sequenz
- **Trigger:** Datums-Intervall (data-type: 16300) — 60 Tage keine E-Mail geöffnet
- **Ziel:** Inaktive Kontakte reaktivieren oder Liste bereinigen
- **Steps:**
  1. E-Mail: "Bist du noch dabei?" (persönlich, direkt von Nicol)
  2. Warte 3 Tage
  3. Bedingung: Hat geöffnet?
  4. Falls ja: Tag "reaktiviert" setzen, zurück in reguläre Liste
  5. Falls nein: E-Mail "Letzte Chance — exklusives Angebot" (mit kleinem Incentive)
  6. Warte 5 Tage
  7. Bedingung: Hat geöffnet?
  8. Falls nein: Tag "inaktiv" setzen, aus Newsletter-Sendungen entfernen
- **Warum jetzt:** Listenqualität direkt verbessert Open Rates. Bei ~14.000 Empfängern sind geschätzt 4.000-6.000 inaktiv (basierend auf 28% Ø Open Rate).
- **Erwarteter Impact:** 5-10% Reaktivierung + 10-20% bessere Open Rates durch saubere Liste

### Automation: Webinar No-Show Recovery
- **Trigger:** Datums-Intervall oder Bedingung nach Webinar
- **Ziel:** 57% der Registrierten die nicht kommen, zurückholen
- **Steps:**
  1. Warte 2 Stunden nach Webinar-Ende
  2. Bedingung: Hat Tag "Webinar teilgenommen"?
  3. Falls nein: E-Mail "Du hast es verpasst — hier ist die Aufzeichnung"
  4. Warte 1 Tag
  5. E-Mail: "Die 3 wichtigsten Erkenntnisse aus dem Workshop"
  6. Warte 2 Tage
  7. Bedingung: Hat Aufzeichnung geklickt?
  8. Falls ja: In normale Post-Webinar-Sequenz einfügen
- **Warum jetzt:** 3.021 von 5.274 Registrierten kommen nicht zum Webinar. Aufzeichnungs-Mails zeigen 48-65% Open Rates — sehr hohe Engagement-Bereitschaft.
- **Erwarteter Impact:** 20-30% der No-Shows sehen Aufzeichnung, davon 5-10% kaufen

## Priorität 2 — Mittelfristiger ROI

### Automation: Upsell Tripwire -> BodyGuide
- **Trigger:** Tag "TW_Happy Body Training_gekauft" + 14 Tage warten
- **Ziel:** Happy Body Training Käufer auf BodyGuide upgraden
- **Steps:**
  1. Warte 14 Tage (Training abgeschlossen)
  2. Bedingung: Hat BG bereits?
  3. Falls nein: E-Mail "Du hast das Training gerockt — bereit für deinen persönlichen Plan?"
  4. Warte 3 Tage
  5. E-Mail: "Dein Angebot: BodyGuide mit 10 EUR Rabatt" (Coupon)
- **Warum jetzt:** 445 TW-Käufer sind warme Leads. Upsell-Pfad fehlt komplett.
- **Erwarteter Impact:** 10-15% Conversion = ~45-67 BodyGuide-Verkäufe

### Automation: SYX.0 Onboarding-Sequenz (erweitert)
- **Trigger:** Tag "SYX.0 gekauft" (bestehende Automation erweitern)
- **Ziel:** Strukturiertes 6-Wochen Onboarding statt nur 1 Willkommens-Mail
- **Steps:**
  1. Willkommens-E-Mail (existiert bereits)
  2. Tag 1: "So startest du — Dein Onboarding-Call"
  3. Woche 1: "Deine erste Woche — Einfindungsphase"
  4. Woche 2: "Themencall 1 — Schlaf, Stress, Energiekiller"
  5. Woche 3: "Themencall 2 — Essen ohne Verbote"
  6. Woche 4: "Halbzeit! Wie läuft's?"
  7. Woche 5: "Themencall 3 — Training"
  8. Woche 6: "Geschafft! Nächste Schritte"
- **Warum jetzt:** 272 SYX.0 Käufer bekommen nur 1 Mail. Retention-Risiko.
- **Erwarteter Impact:** Bessere Kundenbindung, weniger Support-Anfragen, mehr Testimonials

### Automation: Geburtstags-Gruss
- **Trigger:** Geburtstag (data-type: 16200)
- **Ziel:** Persönliche Bindung stärken, optional mit Angebot
- **Steps:**
  1. E-Mail: "Alles Gute zum Geburtstag, [Name]!" (sehr persönlich)
  2. Optional: Kleiner Rabatt-Coupon als Geschenk
- **Warum jetzt:** Trigger existiert in 4leads, wird nicht genutzt. Minimal-Aufwand.
- **Erwarteter Impact:** Hohe Open Rates (>50%), Marken-Loyalität

## Priorität 3 — Nice-to-have

### Automation: Testimonial-Request
- **Trigger:** 30 Tage nach Kauf (SYX.0 oder BodyGuide)
- **Ziel:** Automatisch Testimonials sammeln
- **Steps:**
  1. E-Mail: "Wie geht's dir nach 4 Wochen?"
  2. Link zu Typeform oder einfache Antwort-Möglichkeit
  3. Bei positiver Antwort: "Darf ich deine Erfolgsgeschichte teilen?"

### Automation: Win-Back für Kündigungen
- **Trigger:** Tag "gekündigt" oder Smartliste "ehemalige Mitglieder"
- **Ziel:** Ehemalige Mitglieder nach 30-60 Tagen reaktivieren
- **Steps:**
  1. Warte 30 Tage
  2. E-Mail: "Wir vermissen dich" (persönlich, nicht sales-y)
  3. Warte 14 Tage
  4. E-Mail: "Komm zurück — mit Sonderkonditionen"

### Automation: Content-Engagement Tracking
- **Trigger:** Smartlink geklickt (data-type: 160000) in Content-Mails
- **Ziel:** Engagierte Leser identifizieren und gezielt ansprechen
- **Steps:**
  1. Tag "content-engagiert" setzen
  2. In spezielle Smartliste aufnehmen
  3. Bei nächster Sales-Kampagne: diese Gruppe zuerst + separat ansprechen

## Implementierungs-Reihenfolge

| Prio | Automation | Aufwand | Impact | Zeitrahmen |
|------|-----------|---------|--------|------------|
| 1 | BodyGuide Onboarding | 3h | Hoch | Sofort |
| 2 | Re-Engagement | 2h | Hoch | Sofort |
| 3 | No-Show Recovery | 2h | Mittel-Hoch | Vor nächstem Webinar |
| 4 | Upsell TW->BG | 1h | Mittel | Diese Woche |
| 5 | SYX.0 Onboarding (erweitert) | 4h | Mittel | Nächste Woche |
| 6 | Geburtstag | 30min | Niedrig | Jederzeit |
| 7 | Testimonial-Request | 1h | Niedrig | Nächster Monat |
| 8 | Win-Back | 2h | Niedrig | Nächster Monat |
| 9 | Content-Engagement | 1h | Niedrig | Nice-to-have |
