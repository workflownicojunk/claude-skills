# 4leads Actions & Conditions — Vollständige Dokumentation

**Generated:** 2026-02-22T03:35:00+01:00
**Source:** https://app.4leads.net/processes/cockpit/edit (Automation Builder)
**Total:** 34 Action-Typen in 6 Kategorien + Conditions/Branching

## Kategorie: Intern

### Warten (type: 99)
- **Beschreibung:** Zeitverzögerung im Automation-Flow
- **Config:** Dauer (Minuten / Stunden / Tage)
- **Verwendung in Bestand:** Freebie-Flow (1 Minute, 1 Stunde)

### Bedingung (type: 200)
- **Beschreibung:** If/Else Verzweigung basierend auf Tags, Feldern, Aktivitäten
- **Config:** Feld/Tag/Status auswählen, Operator, Wert. Zwei Pfade: Ja/Nein
- **Verwendung in Bestand:** Freebie-Flow ("Hat TW gekauft?")
- **Branching:** Genau 2 Pfade (If/Else), keine Verschachtelung im gleichen Step, aber sequentielle Conditions möglich
- **Verfügbare Prüfungen:** Tags (hat/hat nicht), Feldwerte (Text/Zahl/Datum), E-Mail-Aktivität (geöffnet/geklickt), Smartlisten-Zugehörigkeit

### Tag(s) hinzufügen (type: 26000)
- **Beschreibung:** Ein oder mehrere Tags zum Kontakt hinzufügen
- **Config:** Multi-Tag-Selector
- **Verwendung in Bestand:** Webinar-Registrierung (5 Automations), Teilnahme-Tracking
- **Häufigste Tags:** "StrongerYou zum Webinar registriert", "SYX.0 gekauft"

### Tag(s) entfernen (type: 26500)
- **Beschreibung:** Ein oder mehrere Tags vom Kontakt entfernen
- **Config:** Multi-Tag-Selector
- **Verwendung in Bestand:** Nicht direkt in bestehenden Automations gefunden

### Kontakt ändern (type: 191000)
- **Beschreibung:** Kontakt-Stammdaten ändern (Name, E-Mail-Adresse, etc.)
- **Config:** Felder auswählen + neue Werte
- **Verwendung in Bestand:** Nicht in bestehenden Automations

### E-Mail Status ändern (type: 193000)
- **Beschreibung:** E-Mail-Zustellstatus des Kontakts ändern
- **Config:** Neuer Status (aktiv/pausiert/deaktiviert)
- **Verwendung in Bestand:** Nicht in bestehenden Automations

### Feldwert setzen (type: 190000)
- **Beschreibung:** Wert für benutzerdefiniertes Feld setzen (Text, Zahl, Datum, Auswahl)
- **Config:** Feld-Selector + Wert (auch dynamische Platzhalter möglich)
- **Verwendung in Bestand:** UTM-Parameter (Freebie-Flow), Webinarraum-URL (3 Automations)

### Formulareintragung (type: 25000)
- **Beschreibung:** Kontakt in ein bestehendes Formular eintragen
- **Config:** Formular-Selector
- **Verwendung in Bestand:** Nicht in bestehenden Automations

### Follow-Up starten (type: 27000)
- **Beschreibung:** Einen Follow-Up/E-Mail-Funnel für den Kontakt starten
- **Config:** Follow-Up-Selector
- **Verwendung in Bestand:** 5 Automations (xNNV, mJJq, AMMQ, W6EN)

### Zu Follow-Up-Step springen (type: 27600)
- **Beschreibung:** Zu einem bestimmten Step innerhalb eines laufenden Follow-Ups springen
- **Config:** Follow-Up + Step-Selector
- **Verwendung in Bestand:** Nicht in bestehenden Automations

### Follow-Up stoppen (type: 27500)
- **Beschreibung:** Einen laufenden Follow-Up/E-Mail-Funnel stoppen
- **Config:** Follow-Up-Selector
- **Verwendung in Bestand:** Freebie (2-2) — Tripwire-Funnel stoppen bei Kauf

### Opt-in-Prozess (type: 180000)
- **Beschreibung:** Opt-in-/Double-Opt-in-Prozess für den Kontakt auslösen
- **Config:** Opt-in-Typ-Selector

### Smartliste hinzufügen (type: 100001)
- **Beschreibung:** Kontakt zu einer Smartliste hinzufügen
- **Config:** Smartliste-Selector

### Aus Smartliste entfernen (type: 110002)
- **Beschreibung:** Kontakt aus einer Smartliste entfernen
- **Config:** Smartliste-Selector

### Themenbereiche ändern (type: 120000)
- **Beschreibung:** Themenbereiche/Content-Kategorien für den Kontakt freischalten oder sperren
- **Config:** Themenbereich-Selector + Aktion (freischalten/sperren)
- **Verwendung in Bestand:** Freebie (2-2) — Themenbereiche bei TW-Kauf freischalten

### Benutzerzugriff ändern (type: 130000)
- **Beschreibung:** Zugriffsrechte für geschützte Bereiche ändern
- **Config:** Zugriffs-Selector

### Verteilen (type: 300)
- **Beschreibung:** Kontakte auf verschiedene Pfade verteilen (A/B-Split-Testing)
- **Config:** Anzahl Pfade + Prozentuale Verteilung
- **Branching:** Mehrere Pfade (2+), gewichtete Zufallsverteilung

### Verlauf teilen (type: 400)
- **Beschreibung:** Automationsverlauf in parallele Pfade teilen (kein Split, sondern Fork)
- **Config:** Anzahl paralleler Pfade
- **Branching:** Alle Pfade werden gleichzeitig durchlaufen

### Lookups / Speicher (type: 279999)
- **Beschreibung:** Daten aus externen Quellen nachschlagen oder im Speicher zwischenspeichern
- **Config:** Lookup-Quelle + Mapping

### Smarttap-Link festlegen (type: 240000)
- **Beschreibung:** Smarttap-URL für Kontakt festlegen (für NFC/QR-Code Interaktionen)
- **Config:** URL-Pattern

## Kategorie: Multichannel

### E-Mail senden (type: 24000)
- **Beschreibung:** E-Mail an den Kontakt senden
- **Config:** E-Mail-Template (aus E-Mail-Builder) oder Inline-Erstellung
- **Gruppen:** Intern + Multichannel
- **Verwendung in Bestand:** 6 Automations senden je 1 E-Mail (Welcome, Registrierungsbestätigung)

### SMS senden (type: 29000)
- **Beschreibung:** SMS an die Mobilnummer des Kontakts senden
- **Config:** SMS-Text (mit Platzhaltern), Absender-ID

### Telegram Benachrichtigung (type: 220000)
- **Beschreibung:** Nachricht über Telegram senden
- **Config:** Telegram-Bot + Chat-ID + Nachrichtentext

## Kategorie: Extern

### E-Mail-Benachrichtigung (type: 28000)
- **Beschreibung:** E-Mail-Benachrichtigung an einen Admin/Mitarbeiter senden (nicht an den Kontakt!)
- **Config:** Empfänger-E-Mail + Betreff + Text

### Webhook (type: 50000)
- **Beschreibung:** HTTP-Request an eine externe URL senden
- **Config:** URL, Methode (POST/GET), Headers, Body-Template (JSON mit Platzhaltern)
- **Verwendung in Bestand:** Nicht in bestehenden Automations (!)
- **Hinweis:** Wichtigste Action für n8n/Make-Integration

### Webinar (type: 249999)
- **Beschreibung:** Webinar-Integration (z.B. Webinarjam-Registrierung)
- **Config:** Webinar-Integration + Event

### Membado (type: 150000)
- **Beschreibung:** Membado-Mitgliedschaft verwalten (aktivieren/deaktivieren)
- **Config:** Membado-Integration

### Kajabi (type: 51000)
- **Beschreibung:** Kajabi-Kurs/Produkt freischalten
- **Config:** Kajabi-Integration

### WP-Benutzer erstellen (type: 200000)
- **Beschreibung:** WordPress-Benutzer für den Kontakt erstellen
- **Config:** WordPress-System + Rolle

### WP Tag-/Feldsync (type: 201000)
- **Beschreibung:** Tags und Felder mit WordPress synchronisieren
- **Config:** WordPress-System + Mapping

### Zapier Trigger (type: 160000)
- **Beschreibung:** Zapier-Aktion auslösen (sendet Daten an Zapier)
- **Config:** Zapier-Integration
- **Gruppen:** Extern + Multichannel

### make (Integromat) (type: 165000)
- **Beschreibung:** Make/Integromat-Aktion auslösen
- **Config:** Make-Integration
- **Gruppen:** Extern + Multichannel

### LearningSuite (type: 260000)
- **Beschreibung:** LearningSuite-Integration (Kurs-Zugriff, Lektionen)
- **Config:** LearningSuite-Integration

### Multichannel Trigger (type: 270000)
- **Beschreibung:** Generischer Multichannel Trigger für externe Integrationen
- **Config:** Integration-Selector
- **Gruppen:** Extern + Multichannel

## Conditions & Branching System

### Bedingung (If/Else — type: 200)
- **Pfade:** Genau 2 (Ja-Pfad / Nein-Pfad)
- **Zusammenführung:** Pfade laufen nach dem Branch-Block weiter in den gemeinsamen Flow
- **Verschachtelung:** Sequentiell (Condition nach Condition), nicht innerhalb eines Pfads verschachtelt
- **Verfügbare Bedingungstypen:**
  - Hat Tag / Hat Tag nicht
  - Feldwert gleich / ungleich / größer / kleiner
  - E-Mail geöffnet / nicht geöffnet
  - E-Mail geklickt / nicht geklickt
  - Ist in Smartliste / nicht in Smartliste
  - E-Mail-Status (aktiv/inaktiv)

### Verteilen (A/B-Split — type: 300)
- **Pfade:** 2 oder mehr (konfigurierbar)
- **Verteilung:** Prozentuale Gewichtung (z.B. 50/50 oder 70/30)
- **Verwendung:** Ideal für E-Mail-Betreffzeilen-Tests oder Angebotsvariantenm

### Verlauf teilen (Fork — type: 400)
- **Pfade:** 2 oder mehr parallele Pfade
- **Verhalten:** Alle Pfade werden gleichzeitig durchlaufen
- **Verwendung:** Wenn mehrere Aktionen parallel passieren sollen

### Goal-basierter Exit
- **Automation-Ziel:** Jede Automation kann ein Ziel definieren
- **Verhalten:** Wenn das Ziel erreicht wird (z.B. Tag gesetzt), verlässt der Kontakt die Automation sofort
- **Trigger für andere:** "Automationen-Ziel erreicht" (type: 146000) kann andere Automations starten

## Bestehende Automations — Flow-Diagramme

### Freebie-Funnel (2 Automations)

```
FREEBIE x TW (1-2) [mBJ5]
═══════════════════════════════════════
[Formular: Lead 7-Tage-Challenge]
    │
    ├── UTM Parameter setzen (FSE)
    ├── UTM Parameter setzen (LSE)
    │
    ▼ Warte 1 Minute
    │
    ├── E-Mail: "Freebie Welcome + Download"
    │
    ▼ Warte 1 Stunde
    │
    ◆ Bedingung: Hat TW gekauft?
    ├── JA → (Ende)
    └── NEIN → Follow-Up "Freebie x Tripwire Funnel" starten


FREEBIE x TW (2-2) [8VlR]
═══════════════════════════════════════
[Tag: TW_Happy Body Training_gekauft]
    │
    ├── Follow-Up "Freebie x Tripwire Funnel" STOPPEN
    ├── Themenbereiche freischalten
    ├── E-Mail: "TW WELCOME ZUM TRIPWIRE"
    │
    └── (Ende)
```

### Webinar-Registrierung (3 parallele Flows)

```
WEBINARKAMPAGNE WEBINARJAM [NPMa]
═══════════════════════════════════════
[Formular: SY3.0 Launch Workshop Webinarjam]
    │
    ├── Tags: "StrongerYou zum Webinar registriert WT"
    ├── Feldwerte setzen (2x)
    ├── E-Mail: "SY3.0 Registrierungsbestätigung"
    ├── Follow-Up: "SY3.0 Webinar Follow Up" starten
    └── (Ende)


WEBINARKAMPAGNE EVERWEBINAR [Zxog]
═══════════════════════════════════════
[Formular: SY3.0 Launch Workshop 2 Everwebinar]
    │
    ├── Tags: "SY3.0 zum Workshop registriert" + "Registrierung Everwebinar"
    ├── Feldwerte setzen (2x)
    ├── E-Mail: "SY3.0 Everwebinar Registrierungsbestätigung"
    ├── Follow-Up: "SY3.0 Everwebinar Follow Up" starten
    └── (Ende)


WEBINARKAMPAGNE LEGACY [4G3g]
═══════════════════════════════════════
[Formular: StrongerYou Launch Workshop]
    │
    ├── Tags: "zum Webinar registriert" + "Manuelle Registrierung"
    ├── E-Mail: "Launch Registrierungsbestätigung"
    ├── Follow-Up: "StrongerYou Launch Follow Up" starten
    └── (Ende)
```

### Webinar-Hilfsfunktionen

```
DIREKTREGISTRIERUNGEN WEBINARJAM [qlJ7]
═══════════════════════════════════════
[Webhook von Webinarjam]
    │
    ├── Tags: "StrongerYou zum Webinar registriert"
    └── (Ende)


WEBINAR TEILNAHME [1oBA]
═══════════════════════════════════════
[Webhook von Webinarjam]
    │
    ├── Tags: "StrongerYou Webinar teilgenommen WT"
    └── (Ende)


MANUELL STEP 1 [5ZlK]
═══════════════════════════════════════
[Tag: Webinarregistrierung manuell]
    │
    ├── (1 hidden action)
    └── (Ende)


MANUELL STEP 2 [lxnQ]
═══════════════════════════════════════
[Webhook]
    │
    ├── Feldwert: "SY3.0 Webinarraum URL Vorregistrierungen"
    ├── Follow-Up: "StrongerYou Launch Follow Up" starten
    └── (Ende)
```

### Post-Kauf

```
SYX.0 WILLKOMMENS-E-MAIL [A3Xe]
═══════════════════════════════════════
[Tag: SYX.0 gekauft]
    │
    ├── E-Mail: "SYX.0 Willkommensmail nach Kauf"
    └── (Ende)
```

## Verknüpfte Follow-Up Funnels

| Hash | Name | Referenziert von | URL |
|------|------|-----------------|-----|
| xNNV | Freebie x Tripwire Funnel | mBJ5 (starten), 8VlR (stoppen) | /funnel/detail/f/xNNV |
| mJJq | SY3.0 Everwebinar Follow Up | Zxog (starten) | /funnel/detail/f/mJJq |
| AMMQ | SY3.0 Webinar Follow Up | NPMa (starten) | /funnel/detail/f/AMMQ |
| W6EN | StrongerYou Launch Follow Up | 4G3g (starten), lxnQ (starten) | /funnel/detail/f/W6EN |

## Verknüpfte E-Mails

| Hash | Name | Verwendet in | URL |
|------|------|-------------|-----|
| R0Nl | TW WELCOME ZUM TRIPWIRE (Happy Body Training) | 8VlR | /email-funnel/email/detail/e/R0Nl |
| AjRd | Freebie Welcome + Download | mBJ5 | /email-funnel/email/detail/e/AjRd |
| OAOl | SY3.0 Everwebinar Registrierungsbestätigung | Zxog | /email-funnel/email/detail/e/OAOl |
| YK4q | SYX.0 Willkommensmail nach Kauf | A3Xe | /email-funnel/email/detail/e/YK4q |
| xLnm | SY3.0 Registrierungsbestätigung | NPMa | /email-funnel/email/detail/e/xLnm |
| eAqk | StrongerYou Launch Registrierungsbestätigung | 4G3g | /email-funnel/email/detail/e/eAqk |

## API-Endpoints

| Aktion | Methode | URL | Body |
|--------|---------|-----|------|
| Automations-Liste | POST | /processes/ajax | `action=search&pageNum=0` |
| Automation-Detail | GET | /processes/cockpit/edit/{hash}?xhr=1 | — |
| Trigger-Auswahl | POST | /processes/ajax | `action=get_start_automation_edit` |
| Action hinzufügen | Drag & Drop im UI | — | Kein direkter API-Endpoint |
| Follow-Up-Detail | GET | /funnel/detail/f/{hash}?xhr=1 | — |
| E-Mail-Detail | GET | /email-funnel/email/detail/e/{hash}?xhr=1 | — |
