# Bestehende 4leads Automations

**Stand:** 2026-02-22
**Gesamt:** 11 Automations (10 Aktiv, 1 Bearbeitung/Draft)

## Übersicht nach Funktion

### Freebie / Tripwire Funnel (2 Automations)

#### Freebie x TW (1-2) [mBJ5] — Aktiv
- **Trigger:** Eintragung in Formular "Lead: 7-Tage-Challenge"
- **Ziel:** Freebie ausliefern, nach 1 Stunde Tripwire-Funnel starten
- **Steps:**
  1. UTM Parameter setzen (FSE + LSE Feldwerte)
  2. Warte 1 Minute
  3. E-Mail "Freebie Welcome + Download" senden
  4. Warte 1 Stunde
  5. Bedingung: "Hat TW gekauft?"
  6. Falls nein: Follow-Up "Freebie x Tripwire Funnel" starten
- **Tags:** -
- **Verknüpft mit:** Follow-Up xNNV, E-Mail AjRd

#### Freebie x TW (2-2) [8VlR] — Aktiv
- **Trigger:** Tag "TW_Happy Body Training_gekauft" hinzugefügt
- **Ziel:** Tripwire-Funnel stoppen wenn Kauf erfolgt, Welcome senden
- **Steps:**
  1. Follow-Up "Freebie x Tripwire Funnel" stoppen
  2. Themenbereiche freischalten
  3. E-Mail "TW WELCOME ZUM TRIPWIRE (Happy Body Training)" senden
- **Tags:** TW_Happy Body Training_gekauft
- **Verknüpft mit:** Follow-Up xNNV, E-Mail R0Nl

### Webinar-Registrierung (5 Automations)

#### SY3.0 Webinarkampagne Webinarjam [NPMa] — Aktiv
- **Trigger:** Eintragung in Formular "StrongerYou 3.0 Launch Workshop Webinarjam"
- **Ziel:** Registrierung bestätigen, Tags setzen, Follow-Up starten
- **Steps:**
  1. Tags hinzufügen: "StrongerYou zum Webinar registriert WT"
  2. Feldwerte setzen (2x)
  3. E-Mail "SY3.0 Registrierungsbestätigung" senden
  4. Follow-Up "SY3.0 Webinar Follow Up" starten
- **Tags:** StrongerYou zum Webinar registriert WT
- **Verknüpft mit:** Follow-Up AMMQ, E-Mail xLnm

#### SY3.0 Webinarkampagne Everwebinar [Zxog] — Aktiv
- **Trigger:** Eintragung in Formular "StrongerYou 3.0 Launch Workshop 2 Everwebinar"
- **Ziel:** Registrierung bestätigen, Tags setzen, Follow-Up starten
- **Steps:**
  1. Tags hinzufügen: "SY3.0 zum Workshop registriert", "SY3.0 Registrierung Everwebinar"
  2. Feldwerte setzen (2x)
  3. E-Mail "SY3.0 Everwebinar Registrierungsbestätigung" senden
  4. Follow-Up "SY3.0 Everwebinar Follow Up" starten
- **Tags:** SY3.0 zum Workshop registriert, SY3.0 Registrierung Everwebinar
- **Verknüpft mit:** Follow-Up mJJq, E-Mail OAOl

#### SY3.0 Webinarkampagne (Legacy) [4G3g] — Aktiv
- **Trigger:** Eintragung in Formular "StrongerYou Launch Workshop"
- **Ziel:** Älterer Registrierungs-Flow
- **Steps:**
  1. Tags hinzufügen: "StrongerYou zum Webinar registriert", "StrongerYou Manuelle Registrierung"
  2. E-Mail "StrongerYou Launch Registrierungsbestätigung" senden
  3. Follow-Up "StrongerYou Launch Follow Up" starten
- **Verknüpft mit:** Follow-Up W6EN, E-Mail eAqk

#### SY3.0 Direktregistrierungen Webinarjam [qlJ7] — Aktiv
- **Trigger:** Webhook (von Webinarjam)
- **Ziel:** Direktregistrierungen taggen
- **Steps:**
  1. Tags hinzufügen: "StrongerYou zum Webinar registriert"
- **Tags:** StrongerYou zum Webinar registriert

#### Webinarragistrierung Manuell Step 1 [5ZlK] — Aktiv
- **Trigger:** Tag "Webinarregistrierung manuell" hinzugefügt
- **Ziel:** Manueller Start für Webinar-Registrierung
- **Steps:** 1 Action (Details hidden)

### Webinar-Teilnahme (1 Automation)

#### SY 3.0 Webinar Teilnahme [1oBA] — Aktiv
- **Trigger:** Webhook (von Webinarjam)
- **Ziel:** Teilnahme tracken
- **Steps:**
  1. Tags hinzufügen: "StrongerYou Webinar teilgenommen WT"
- **Tags:** StrongerYou Webinar teilgenommen WT

### Webinar-Nachbereitung (1 Automation)

#### Webinarregistrierung Manuell Step 2 [lxnQ] — Aktiv
- **Trigger:** Webhook
- **Ziel:** Webinarraum-URL setzen und Follow-Up starten
- **Steps:**
  1. Feldwert setzen: "SY3.0 Webinarraum URL Vorregistrierungen"
  2. Follow-Up "StrongerYou Launch Follow Up" starten
- **Verknüpft mit:** Follow-Up W6EN

### Post-Kauf (1 Automation)

#### StrongerYou X.0 - Willkommens-E-Mail bei Kauf [A3Xe] — Aktiv
- **Trigger:** Tag "SYX.0 gekauft" hinzugefügt
- **Ziel:** Willkommens-E-Mail nach Kauf senden
- **Steps:**
  1. E-Mail "SYX.0 Willkommensmail nach Kauf" senden
- **Tags:** SYX.0 gekauft
- **Verknüpft mit:** E-Mail YK4q

### Draft (1 Automation)

#### Test [rL52] — Bearbeitung
- Leere Test-Automation ohne Trigger

## Verknüpfte Follow-Up Funnels
| Hash | Name | Verwendet von |
|------|------|---------------|
| xNNV | Freebie x Tripwire Funnel | Freebie (1-2), Freebie (2-2) |
| mJJq | SY3.0 Everwebinar Follow Up | Everwebinar Kampagne |
| AMMQ | SY3.0 Webinar Follow Up | Webinarjam Kampagne |
| W6EN | StrongerYou Launch Follow Up | Legacy Kampagne, Manuell Step 2 |

## Tags in Automations verwendet
| Tag | Typ | Verwendet in |
|-----|-----|-------------|
| TW_Happy Body Training_gekauft | Trigger + Segmentierung | Freebie (2-2) |
| SYX.0 gekauft | Trigger | Willkommens-E-Mail |
| Webinarregistrierung manuell | Trigger | Manuell Step 1 |
| StrongerYou zum Webinar registriert | Segmentierung | Direktreg., Legacy |
| StrongerYou zum Webinar registriert WT | Segmentierung | Webinarjam |
| SY3.0 zum Workshop registriert | Segmentierung | Everwebinar |
| SY3.0 Registrierung Everwebinar | Segmentierung | Everwebinar |
| StrongerYou Webinar teilgenommen WT | Tracking | Teilnahme |
| StrongerYou Manuelle Registrierung | Segmentierung | Legacy |

## Lücken und Empfehlungen

### Fehlende Automations (kritisch)
1. **Kein Re-Engagement Flow** — Inaktive Kontakte werden nicht reaktiviert
2. **Kein Post-Kauf Onboarding für BodyGuide** — 97-E-Mail nur für SYX.0, nicht für BodyGuide
3. **Keine Churn-Prevention** — Wenn Kontakte abspringen, passiert nichts
4. **Keine Geburtstags-Automation** — Obwohl Trigger verfügbar
5. **Kein Post-Webinar Sales Funnel als Automation** — Nur als Follow-Up, nicht als intelligente Automation mit Conditions

### Fehlende Automations (nice-to-have)
6. **Keine Upsell-Automation** — BodyGuide-Käufer werden nicht automatisch auf SY gelenkt
7. **Kein Feedback-Request** — Nach Kauf/Programm kein automatischer Feedback-Request
8. **Keine Win-Back Sequenz** — Ehemalige Mitglieder werden nicht angesprochen
9. **Kein Webhook zu n8n/Make** — Keine der Automations nutzt externe Webhooks für CRM-Sync
