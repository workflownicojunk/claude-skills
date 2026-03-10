# 4leads Automationen & Follow-Ups Dokumentation
Stand: 2026-03-08 (vollständig dokumentiert)

**Vollständige Detaildoku:** `~/Desktop/Project/marketing-funnel/`

---

## Automationen (16 Gesamt)

| ID | Name | Status | Trigger |
|----|------|--------|---------|
| jdkm | Connect Kauf \| BodyGuide Gutscheincode Auto-Versand | Aktiv | Tag: connect-annual / connect-monthly |
| g5lE | Evergreen Funnel \| Webinar Automation | Bearbeitung | Formular Single-Opt-in |
| ejMX | Evergreen Funnel \| Freebie Start | Bearbeitung | Tag: Lead: 7-Tage-Challenge |
| 1o4o | LÖSCHEN - Evergreen Funnel \| Freebie Start | Bearbeitung | (leer, zur Löschung) |
| 5ZeG | Evergreen Funnel \| FU Start nach X.0 Abschluss (2-2) | Bearbeitung | Tag: connect-annual / connect-monthly |
| rL52 | Evergreen Funnel \| FU Start nach X.0 Abschluss (1-2) | Bearbeitung | Tag: X.0 Abgeschlossen |
| 8VlR | Freebie x TW (2-2) | Aktiv | Tag: TW_Happy Body Training_gekauft |
| mBJ5 | Freebie x TW (1-2) | Aktiv | Formular: Lead: 7-Tage-Challenge |
| Zxog | SY3.0 Webinarkampagne Everwebinar | Bearbeitung | Formular: SY3.0 Launch Workshop 2 Everwebinar |
| A3Xe | Evergreen Funnel \| SYX.0 Willkommensmail + Connect FU | Bearbeitung | Tag: SYX.0 gekauft |
| qlJ7 | SY3.0 Direktregistrierungen Webinarjam | Aktiv | Webhook |
| 1oBA | SY 3.0 Webinar Teilnahme | Aktiv | Webhook |
| lxnQ | Webinarregistrierung Manuell Step 2 | Aktiv | Webhook |
| 5ZlK | Webinarragistrierung Manuell Step 1 | Aktiv | Tag: Webinarregistrierung manuell |
| NPMa | SY3.0 Webinarkampagne Webinarjam | Aktiv | Formular: SY3.0 Launch Workshop Webinarjam |
| 4G3g | SY3.0 Webinarkampagne (Legacy) | Aktiv | Formular: StrongerYou Launch Workshop |

---

## Automation jdkm – Vollständige Struktur (CRM-Sync kritisch)

```
TRIGGER: Tag connect-annual ODER connect-monthly hinzugefügt

STEP 1: Themenbereiche freischalten
BEDINGUNG: "BodyGuide Gutscheincode vorhanden" (CF 15306)
  ├── JA:  Ende (kein Versand, bereits erhalten)
  └── NEIN:
        STEP 2: E-Mail senden (ID: 5OLR)
                "Connect Kauf | Auto | BodyGuide Gutscheincode Willkommen"
        STEP 3: Tag hinzufügen: "BodyGuide Gutscheincode versendet"
```

**Wichtig:** CF 15306 (`connect_bodyguide_gutscheincode`) muss VORHER gesetzt sein, damit Bestandskunden keinen Doppelversand erhalten. Neukunden (CF leer) erhalten automatisch den Code.

---

## Follow-Ups (11 Gesamt)

| ID | Name | Status | Typ | Steps |
|----|------|--------|-----|-------|
| ex8M | Evergreen Funnel \| Connect Upsell FU | pausiert | Linear | 0 (leer) |
| 16vv | Evergreen Funnel \| BodyGuide FU | pausiert | Linear | 0 (leer) |
| lJag | Evergreen Funnel \| Webinareinladung | pausiert | Linear | 0 (leer) |
| 5XVn | Evergreen Funnel \| Content FU 2 | pausiert | Linear | 0 (leer) |
| R161 | Evergreen Funnel \| Content FU 1 | pausiert | Linear | 0 (leer) |
| BAMb | Connect Upsell nach X.0 Abschluss | pausiert | Linear | 3 |
| 8lXZ | SY Workshop FU Typeform Registrierungen | aktiv | Terminserie fix | 6 |
| W6EN | StrongerYou Launch Follow Up | aktiv | Webinar-Terminserie | 6 |
| xNNV | Freebie x Tripwire Funnel | aktiv | Linear | 3 (536 aktive) |
| mJJq | SY3.0 Everwebinar Follow Up | pausiert | Webinar-Terminserie | 4 |
| AMMQ | SY3.0 Webinar Follow Up | aktiv | Webinar-Terminserie | 6 |

---

## Wichtige Erkenntnisse für CRM-Sync

### Automatische Folge-Aktionen nach Tag-Setzen
Wenn CRM-Sync `connect-monthly` oder `connect-annual` via n8n setzt:
- Automation jdkm startet und prüft CF 15306
- Automation 5ZeG stoppt FU BAMb (X.0 Upsell)

### CF 15306 Reihenfolge
CF 15306 MUSS vor den Tags gesetzt werden. Sonst sendet jdkm den BodyGuide-Code an alle, auch an Bestandskunden, die ihn schon haben.

### Legacy-Tags
`connect-monthly-legacy` und `connect-annual-legacy` triggern jdkm NICHT. Legacy-Kunden erhalten keinen automatischen BodyGuide-Code-Versand.

### 4leads Tag-IDs (Connect)

| Tag | ID |
|-----|----|
| connect-monthly | 43466 |
| connect-annual | 43467 |
| connect-monthly-legacy | 43468 |
| connect-annual-legacy | 43469 |
