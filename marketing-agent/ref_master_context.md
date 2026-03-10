# Marketing Agent — Vollständiger Kontext

**Stand:** 2026-02-22
**Datenquellen:** 84 E-Mails, 47 Newsletter-Stats, 11 Automations, 5 Funnels

## Wer bin ich?

Nicol Stanzel, 53, Fitness Coach und Community Builder.
- Instagram: 192.000 Follower (@nicolstanzel)
- E-Mail-Liste: ~14.600 Kontakte (größte Sendung)
- Community: Circle.so mit ~960 Mitgliedern
- Tools: 4leads (E-Mail + Automations), Circle.so (Community), Stripe (Payments)
- Zielgruppe: Frauen 35-65, DACH, Intermittent Fasting + Body Recomposition

## Meine Produkte

| Produkt | Preis | Käufer | Typ |
|---------|-------|--------|-----|
| 7-Tage Happy Body Challenge | Kostenlos (Freebie) | 7.484 | Lead Magnet |
| Happy Body Training (Tripwire) | 27 EUR | 445 | One-time |
| BodyGuide | 97 EUR | 276 | One-time (PPTX Ernährungsplan) |
| StrongerYou X.0 | 497 EUR / 97 EUR/mo | 272 | 6-Wochen Coaching |
| Connect Membership | 39 EUR/mo | ~100 | Community |
| Connect Annual | 390 EUR/yr | ~35 | Community |

## Meine Kampagnen-Typen

### Aktive Kampagnen (aus E-Mail-Daten)
1. **Webinar-Einladungen** (8 Mails, 10 Tage vor Event) — 10.000+ Empfänger
2. **Post-Webinar Follow-Up** (7+ Mails, 7 Tage nach Event) — 8.000-13.500 Empfänger
3. **Post-Webinar v2** (Warm-Segment, 7 Mails) — 2.200-2.450 Empfänger
4. **BodyGuide-Kampagnen** (3 Mails, monatlich) — 7.000-14.600 Empfänger
5. **Content-Newsletter** (unregelmäßig) — 10.000-11.100 Empfänger
6. **Connect-Mails** (kleine, gezielte Sendungen) — 35-65 Empfänger
7. **Freebie Welcome + Tripwire** (automatisch) — pro Neuanmeldung

### Versandrhythmus
- Während Launch-Phasen: Täglich (manchmal 2x)
- Zwischen Launches: 1-2x/Woche
- Content-Newsletter: Alle 2-3 Wochen

## Meine bestehenden Automations (11 total)

### Aktive Flows
- **Freebie-Flow:** Formular -> Welcome Mail -> 1h warten -> Bedingung (gekauft?) -> Tripwire Funnel
- **Tripwire-Kauf:** Tag-Trigger -> Funnel stoppen -> Welcome Mail
- **Webinar-Registrierung:** 3 parallele Flows (Webinarjam, Everwebinar, Legacy) -> Tags + Bestätigung + Follow-Up
- **Webinar-Teilnahme:** Webhook -> Tag setzen
- **SYX.0 Kauf:** Tag-Trigger -> 1 Willkommens-Mail

### Verknüpfte Follow-Up Funnels
- Freebie x Tripwire Funnel (xNNV)
- SY3.0 Everwebinar Follow Up (mJJq)
- SY3.0 Webinar Follow Up (AMMQ)
- StrongerYou Launch Follow Up (W6EN)

## Was performt gut (Zusammenfassung)

- **Kleine, gezielte Sendungen:** 60-75% Open Rates (vs. 28% bei Breitband)
- **Post-Webinar v2 an warme Leads:** 38-45% Open, 4-6% Click
- **Erste Mail einer Sequenz:** Immer 20-30% besser als spätere Mails
- **Content-Mails mit persönlichem Touch:** 30-32% Open, 3.5-4.8% Click
- **Allgemeine Durchschnitte:** 30% Open, 3.5% Click, 2% Optout

## Was fehlt noch (Zusammenfassung)

### Kritische Lücken
1. BodyGuide-Käufer: Kein Onboarding, kein Upsell
2. SYX.0-Käufer: Nur 1 Willkommens-Mail, kein Onboarding
3. Inaktive Kontakte: Kein Re-Engagement
4. Webinar No-Shows: 57% kommen nicht, keine Recovery-Sequenz
5. Upsell-Pfade: Tripwire->BodyGuide und BodyGuide->SY fehlen komplett

### Details
-> Siehe missing_automations.md für vollständige Empfehlungen mit Steps

## Meine Schreibstimme

-> Wird in Session 02b als separater Abschnitt ergänzt (Tone of Voice Analyse aus 84 E-Mail-HTMLs)

## Verfügbare 4leads Trigger (32 Typen)

Wichtigste für neue Automations:
- Tag hinzugefügt/entfernt (am häufigsten genutzt)
- Anmeldung Formular
- Webhook (für externe Integrationen wie n8n/Make)
- Datumsfeld / Datums-Intervall (für zeitbasierte Flows)
- Geburtstag (ungenutzt!)
- Smartlink geklickt (für Engagement-Tracking)

## Verfügbare 4leads Actions (34 Typen)

Wichtigste:
- E-Mail senden / SMS senden
- Tag(s) hinzufügen/entfernen
- Feldwert setzen
- Follow-Up starten/stoppen
- Bedingung (If/Else)
- Warten (Zeitverzögerung)
- Webhook (für n8n/Make Integration)
- Verteilen (A/B-Split)
