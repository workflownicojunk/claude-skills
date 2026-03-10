# Customer Journey Map

**Stand:** 2026-02-22
**Basierend auf:** 84 E-Mails, 47 Newsletter-Stats, 11 Automations, 5 Funnels

## Einstiegspunkte

### 1. Freebie: 7-Tage Happy Body Challenge
- **Formular:** "Lead: 7-Tage-Challenge" (7.484 Kontakte mit Tag)
- **Welcome-Sequenz:**
  1. UTM-Parameter werden gespeichert (Tracking)
  2. 1 Minute warten
  3. "Freebie Welcome + Download" E-Mail
  4. 1 Stunde warten
  5. Bedingung: Hat Tripwire gekauft?
  6. Falls nein: Tripwire Funnel startet
- **Tripwire:** Happy Body Training (TW) — Conversion von Freebie zu Bezahlprodukt
- **Stats:** 445 Kontakte haben TW gekauft (6% Conversion vom Freebie)

### 2. Webinar-Registrierung
- **Kanäle:** Webinarjam (live) + Everwebinar (automated)
- **Registrierungs-Flow:**
  1. Formular-Eintragung oder Webhook von Webinarjam
  2. Tags setzen (registriert, Kanal-spezifisch)
  3. Feldwerte setzen (URL, etc.)
  4. Registrierungsbestätigung per E-Mail
  5. Follow-Up Funnel starten (Erinnerungs-Sequenz)
- **Stats:** 5.274 registriert, 2.253 teilgenommen (43% Show-Up Rate)
- **Wiederholungswebinar (WT):** 2.581 registriert, 1.233 teilgenommen (48% Show-Up Rate)

### 3. Direktkauf (ohne Webinar)
- **Trigger:** Tag "SYX.0 gekauft" wird gesetzt
- **Einziger Step:** Willkommens-E-Mail nach Kauf
- **Stats:** 272 SYX.0-Käufer total

## Webinar-Funnel (Detail)

### Einladungs-Sequenz (vor Webinar)
- **8 E-Mails** über 10 Tage (09.01-18.01.26)
- **Rhythmus:** Täglich, manchmal 2x/Tag
- **Open Rates:** 23-33% (sinken über die Sequenz)
- **Beste Mail:** Mail 1 (33.0% Open, 4.1% Click)
- **Schlechteste:** Mail 8 (23.0% Open, 0.9% Click)
- **Empfänger:** ~10.000-11.000 pro Mail

### Nach dem Webinar
- **7+ Follow-Up Mails** über 7 Tage
- **Rhythmus:** Täglich nach dem Webinar
- **Open Rates:** 24-31% (relativ stabil)
- **Click Rates:** 1.1-4.6%
- **Besonderheit:** Wiederholungswebinar wird separat beworben
- **Conversion-Push:** "nach Webinar v2" Mails an kleinere Gruppe (2.252-2.447) mit 34-45% Open Rate

### Direkte Sales-Mails (Top-Performer)
- Mail 5 "nach Webinar v2": **45.1% Open, 6.3% Click** (stärkste Conversion-Mail)
- Mail 6 "nach Webinar v2": **37.8% Open, 4.1% Click**
- Mail 7 "nach Webinar v2": **33.8% Open, 3.4% Click**

## Produkte und ihre Funnel

### StrongerYou X.0 (Coaching)
- **Einstieg:** Webinar-Funnel (8 Einladungs-Mails + 7 Follow-Up-Mails)
- **Onboarding:** 1 Willkommens-E-Mail nach Kauf (sehr minimal!)
- **Retention:** Keine E-Mail-Automation vorhanden
- **Upsell:** Keine

### BodyGuide (97 EUR)
- **Einstieg:** Newsletter-Kampagnen (3 Mails pro Kampagne, ca. monatlich)
- **Onboarding:** Keine Automation nach Kauf!
- **Retention:** Keine
- **Upsell auf SY:** Keine automatische Sequenz
- **Stats:** 276 Käufer (Tag BG_97EUR_gekauft)
- **Kampagnen-Rhythmus:**
  - Nov 25: 3 Mails (7.000-7.700 Empfänger)
  - Feb 26: 3 Mails (13.200-14.600 Empfänger)

### Happy Body Training (Tripwire, 27 EUR)
- **Einstieg:** Automatisch nach Freebie (wenn nicht gekauft nach 1h)
- **Onboarding:** Willkommens-E-Mail nach Kauf + Themenbereiche freischalten
- **Follow-Up Funnel:** "Freebie x Tripwire Funnel" (Verkaufssequenz)

### Connect Membership (39 EUR/mo)
- **Einstieg:** 3 spezielle Follow-Up Mails für Connect (kleine Gruppe, 35-46 Empfänger)
- **Performance:** Extrem hohe Open Rates (60-70%) — sehr engagierte Gruppe
- **Jahresmitgliedschaft:** 2 separate Kampagnen (SY2.0 + Connect39)
  - 75% Open Rate, 23-30% Click Rate (Top-Performer)

## Fehlende Journey-Schritte

### Kritisch fehlend
1. **BodyGuide Post-Kauf Onboarding** — 276 Käufer bekommen keine automatische Onboarding-Sequenz
2. **SYX.0 Onboarding-Sequenz** — Nur 1 Willkommensmail, kein strukturiertes Onboarding
3. **Re-Engagement** — Inaktive Kontakte (~60 Tage keine Öffnung) werden nicht angesprochen
4. **Upsell BodyGuide -> SY** — Kein automatischer Pfad von 97 EUR auf 497 EUR
5. **Upsell Tripwire -> BodyGuide** — Kein Pfad von 27 EUR auf 97 EUR

### Nice-to-have
6. **Geburtstags-Mail** — Trigger existiert in 4leads, wird nicht genutzt
7. **Webinar No-Show Sequenz** — 57% registrieren sich aber kommen nicht (2.581 von 5.274)
8. **Testimonial-Request** — Automatisch nach erfolgreichem Programmabschluss
9. **Win-Back für Kündigungen** — Ehemalige Mitglieder reaktivieren
10. **Content-Newsletter Automation** — Aktuell manueller Versand, könnte automatisiert werden
