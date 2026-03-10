# 4leads Automation Triggers — Vollständige Dokumentation

**Generated:** 2026-02-22T03:30:00+01:00
**Source:** https://app.4leads.net/processes/cockpit/edit (Automation Builder)
**Total:** 32 Trigger-Typen in 5 Kategorien

## Kategorie: Intern

### Tag hinzugefügt (type: 11000)
- **Beschreibung:** Startet sobald einem Kontakt eines der ausgewählten Tags zugewiesen wird. Verfügt der Kontakt bereits über das Tag, wird die Aktion nicht ausgeführt.
- **Config:** Multi-Tag-Selector (`tagIds[]`)
- **Hinweis:** Bei mehreren Trigger-Tags startet die Automation separat für jedes Tag.

### Tag entfernt (type: 11500)
- **Beschreibung:** Startet sobald einem Kontakt eines der ausgewählten Tags entzogen wird.
- **Config:** Multi-Tag-Selector (`tagIds[]`)

### Anmeldung Formular (type: 14000)
- **Beschreibung:** Startet durch die Eintragung in ein Formular. Befindet sich der Kontakt bereits im Prozess, startet die Automation nicht.
- **Config:** Formular-Selector

### Neuer Kontakt (type: 140000)
- **Beschreibung:** Startet durch das Erstellen eines neuen Kontakts. Kann genau einmal pro Kontakt ausgelöst werden.
- **Config:** Keine — automatisch

### Änderung Kontakt (type: 145000)
- **Beschreibung:** Startet durch Ändern der Kontakt-Stammdaten. Nur Stammsatzfelder, nicht globale Zusatzfelder.
- **Config:** Keine — automatisch
- **Hinweis:** Erstellung löst ebenfalls aus. Mehrere Änderungen können zusammengefasst werden.

### Automationen-Ziel erreicht (type: 146000)
- **Beschreibung:** Startet wenn ein Kontakt das Ziel einer anderen Automation erreicht.
- **Config:** Automation-Selector

### Beitritt Smartliste (type: 100000)
- **Beschreibung:** Startet sobald ein Kontakt einer Smartliste beitritt.
- **Config:** Smartliste-Selector

### Austritt Smartliste (type: 110000)
- **Beschreibung:** Startet sobald ein Kontakt aus einer Smartliste entfernt wird.
- **Config:** Smartliste-Selector

### Coupon Änderung (type: 120000)
- **Beschreibung:** Startet wenn der Status eines Gutscheins sich ändert oder im Bonussystem eine Aktion ausgeführt wird.
- **Config:** Coupon-Selector

### Workflow Button (type: 210000)
- **Beschreibung:** Startet sobald bei einem Kontakt der Workflow Button betätigt wird.
- **Config:** Button Name, Untertitel, Farbe, Icon, Exklusiv-Modus, Bestätigung, Deep Link
- **Hinweis:** Exklusive Buttons werden prominent in Kontakt-Details angezeigt.

### Smarttap-Kontakt (type: 180000)
- **Beschreibung:** Startet durch externen Aufruf der Webhook-URL (Smarttap).
- **Config:** Webhook-URL (auto-generated)

## Kategorie: Kontakte / Felder

### Textfeld (type: 16050)
- **Beschreibung:** Startet sobald ein benutzerdefiniertes Textfeld gesetzt wird und der Wert den Einstellungen entspricht.
- **Config:** Feld-Selector, Wert-Match (`*` als Wildcard, Regex möglich)

### Datumsfeld (type: 16100)
- **Beschreibung:** Überwacht ein Datumsfeld. Bei Änderung wird der Start berechnet.
- **Config:** Feld-Selector, Verzögerung (Minuten/Stunden/Tage), vor/nach dem Feldwert
- **Option:** "Nicht ausführen falls in Vergangenheit"

### Datums-Intervall (type: 16300)
- **Beschreibung:** Startet täglich für Kontakte deren Datumsfeld den Einstellungen entspricht.
- **Config:** Feld-Selector, Intervall (Jahre/Monate/Wochen/Tage), Start-Uhrzeit, Relative Verzögerung
- **Verhalten:** Automatische/Volle/Minimale Startabstände bei Feldwertänderungen

### Auswahlfeld (type: 16110)
- **Beschreibung:** Startet sobald ein Auswahlfeld gesetzt wird und der Wert stimmt.
- **Config:** Feld-Selector

### Nummernfeld (type: 16120)
- **Beschreibung:** Startet sobald ein numerisches Feld gesetzt wird und der Wert stimmt.
- **Config:** Feld-Selector, Wertgrenzen (ist/ist nicht/größer/kleiner)

### Geburtstag (type: 16200)
- **Beschreibung:** Wird täglich geprüft. Startet am Geburtstag des Kontakts.
- **Config:** Relative Verzögerung (Tage vor/nach), Start-Uhrzeit

### Smartlink geklickt (type: 160000)
- **Beschreibung:** Startet sobald ein Kontakt auf ein Smartlink klickt.
- **Config:** Smartlink-Selector
- **Hinweis:** Nur wenn Zuordnung zu Kontakt möglich ist (z.B. in E-Mails).

## Kategorie: Shops

### Digistore24 (type: 13000)
- **Config:** Integration, Produkt(e), E-Mail-Status

### Digistore24 Affiliate (type: 13100)
- **Config:** Integration

### Shopify (type: 13600)
- **Config:** Shopify Integration

### CopeCart (type: 13750)
- **Config:** CopeCart Integration

### elopage (type: 13200)
- **Config:** elopage Integration

## Kategorie: Extern

### Webhook (type: 17000)
- **Beschreibung:** Startet durch externen Aufruf der Webhook-URL. Beliebige Drittsysteme anbindbar.
- **Config:** Webhook-URL (auto-generated, POST/GET), Datenstruktur einlesen
- **Hinweis:** URL enthält Zugriffsschlüssel. System benötigt einmalig einen Aufruf zur Strukturerkennung.

### make / Integromat (type: 17100)
- **Beschreibung:** Verbindung mit Make/Integromat.
- **Config:** Keine — nach Speichern als Action in Make verfügbar

### Zapier Trigger (type: 130000)
- **Beschreibung:** Wartet auf Aktion von Zapier.
- **Config:** Zapier Integration

### Onepage (type: 17010)
- **Beschreibung:** Neuer Lead aus Onepage via Webhook.
- **Config:** Webhook-URL (POST/GET), Datenstruktur einlesen

### Wordpress-Event (type: 150000)
- **Beschreibung:** Event in verbundenem WordPress-System.
- **Config:** WordPress-System, Event-Typ (Login/Inaktivität/Seitenbesuch/Video gesehen/Passwort angefordert), Verhalten bei unbekannten Kontakten

### Webinare (type: 170000)
- **Config:** Webinar-Integration

### Calendly (type: 190000)
- **Beschreibung:** Calendly-Events (z.B. Termin gebucht).
- **Config:** Integration, Auslöser, Verhalten bei unbekannten Kontakten, E-Mail-Status

### LearningSuite (type: 200000)
- **Sub-Auslöser:** Zugriffsanfrage erstellt, Einreichung erstellt, Kursfortschritt geändert, Lektion abgeschlossen
- **Config:** LearningSuite Integration

### Multichannel Trigger (type: 160100)
- **Config:** Extern/Multichannel Integration

## API-Endpoints

- **Automations-Liste:** `POST /processes/ajax` mit `action=search&pageNum=0`
- **Automation-Detail:** `GET /processes/cockpit/edit/{hash}?xhr=1`
- **Trigger-Konfiguration:** Click-basiert im UI (kein direkter API-Endpoint)
- **Ajax-URL:** `/processes/ajax` (für alle Automation-CRUD Operationen)
