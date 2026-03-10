---
name: prozessfaktor-abrechnung
description: Monatliche Provisionsabrechnung für Prozessfaktor GmbH (Ben). Berechnet 15% JV-Provision auf alle Stripe-Umsätze (exkl. Tripwire) und erstellt ein gebrandetes DOCX-Dokument. Trigger auf "Abrechnung Ben", "Prozessfaktor", "Provision Ben", "monatliche Abrechnung", "Ben bezahlen", "wie viel bekommt Ben", oder wenn der Abrechnungszeitraum für Prozessfaktor ansteht.
---

# Prozessfaktor Provisionsabrechnung

Erstellt die monatliche JV-Provisionsabrechnung für **Prozessfaktor GmbH / Ben** basierend auf Stripe-Umsatzdaten.

## Vertragsgrundlage

| Punkt | Regelung |
|-------|----------|
| Modell | Joint Venture, 15% Umsatzbeteiligung |
| Basis | Netto nach Stripe-Zahlungsgebühren (NICHT Brutto) |
| Ausnahme | Happy Body Training (Tripwire, 27 EUR) wird komplett ausgenommen |
| Tripwire-Regelung | Tripwire-Einnahmen fließen in einen Ad-Budget-Topf, nicht in die Provision |
| Produkte inkl. | SY X.0 Coaching, SY 3.0 Coaching, Connect (alle Varianten), BodyGuide, LIVEstyle |
| Zeitraum | Kalendermonat |

Die Vereinbarung basiert auf einem Zoom-Call (Transkript in `Inbox/Prozessfaktor Vertrag.txt`). Es gibt keinen formellen Vertrag, nur die mündliche Absprache.

## Berechnungsmethodik (KRITISCH)

Die Provision wird auf **Nettoumsätze nach Abzug der Stripe-Zahlungsgebühren** berechnet, nicht auf Bruttoumsätze. Dies wurde in der ersten Abrechnung (Dez 2025/Jan 2026) so etabliert und muss konsistent beibehalten werden.

```
brutto           = Summe aller succeeded Charges (amount)
stripe_fees      = Summe aller Balance-Transaction-Fees (fee)
netto_nach_fees  = brutto - stripe_fees
refunds          = Summe aller amount_refunded
netto_nach_ref   = netto_nach_fees - refunds
tripwire_netto   = Tripwire-Brutto - Tripwire-Stripe-Fees
basis            = netto_nach_ref - tripwire_netto
provision_15pct  = basis * 0.15
```

## Bens Kommunikationsprofil

Ben will **schnell und unkompliziert** seine Abrechnung. Wichtige Punkte:

- **Keine Mikrorechnung.** Er reagiert allergisch darauf, wenn jeder Euro dreimal umgedreht wird.
- **Professionell, transparent, fair.** Er denkt in Gesamtpaketen. "15% einfach von dem Gesamten" war sein eigener Vorschlag.
- **Schnelle Auszahlung.** Letztes Mal hat es "ewig gedauert". Das darf nicht wieder passieren.
- **Kein Verhandlungston.** Das Dokument ist eine sachliche Aufstellung, keine Rechtfertigung.
- **Slack-Kanal:** DM mit Ben = Channel `D09K28070GM`

## Workflow

### 1. Zeitraum bestimmen

Frage den User nach dem Abrechnungsmonat. Default: der Vormonat.

### 2. Stripe-Daten abrufen

Datenquelle: **Supabase** (Projekt `dajxbqfiugzigrnsoqau`, Schema `stripe`).

**Unix-Timestamps berechnen:**
```sql
SELECT
  extract(epoch from '<YYYY-MM-01>'::timestamp) as month_start,
  extract(epoch from '<YYYY-MM-01>'::timestamp + interval '1 month') as month_end;
```

**Gesamtsummen mit Stripe-Gebühren (über Balance Transactions):**

WICHTIG: Join über `bt.id = c.balance_transaction` (NICHT `bt.source = c.id`, das matcht nur ~20%).

```sql
SELECT
  COUNT(*) as anzahl_charges,
  SUM(c.amount/100.0) as brutto_eur,
  SUM(bt.fee/100.0) as stripe_fees,
  SUM(bt.net/100.0) as netto_eur,
  SUM(c.amount_refunded/100.0) as refunds_eur
FROM stripe.charges c
JOIN stripe.balance_transactions bt ON bt.id = c.balance_transaction
WHERE c.created >= :month_start AND c.created < :month_end
  AND c.status = 'succeeded';
```

**Aufschlüsselung nach Produkt (mit Gebühren):**
```sql
SELECT
  CASE
    WHEN c.amount = 2700 THEN 'Happy Body Training (Tripwire)'
    WHEN c.amount = 9700 AND c.invoice IS NOT NULL AND c.invoice != '' THEN 'SY X.0 Coaching Rate (6x97)'
    WHEN c.amount = 9700 AND (c.invoice IS NULL OR c.invoice = '') THEN 'BODY GUIDE (Einmalkauf)'
    WHEN c.amount = 3900 THEN 'Connect Monatlich (39 EUR)'
    WHEN c.amount = 5900 THEN 'Connect Monatlich (59 EUR)'
    WHEN c.amount = 1990 THEN 'Connect Monatlich (19,90 EUR)'
    WHEN c.amount = 39000 THEN 'Connect Jahresabo (390 EUR)'
    WHEN c.amount = 29900 THEN 'Connect Jahresabo (299 EUR)'
    WHEN c.amount = 18900 THEN 'SY 3.0 Rate (189 EUR)'
    WHEN c.amount = 17900 THEN 'SY X.0 Rate (179 EUR)'
    WHEN c.amount = 2997 THEN 'LIVEstyle Weekly (29,97 EUR)'
    ELSE 'Sonstiges (' || (c.amount/100.0)::text || ' EUR)'
  END as kategorie,
  COUNT(*) as anzahl,
  SUM(c.amount/100.0) as brutto_eur,
  SUM(bt.fee/100.0) as stripe_fees,
  SUM(bt.net/100.0) as netto_eur,
  SUM(c.amount_refunded/100.0) as refunds_eur
FROM stripe.charges c
JOIN stripe.balance_transactions bt ON bt.id = c.balance_transaction
WHERE c.created >= :month_start AND c.created < :month_end
  AND c.status = 'succeeded'
GROUP BY kategorie
ORDER BY netto_eur DESC;
```

**Tripwire separat (Netto nach Stripe-Gebühren):**
```sql
SELECT
  COUNT(*) as count,
  SUM(c.amount/100.0) as brutto,
  SUM(bt.fee/100.0) as fees,
  SUM(bt.net/100.0) as netto
FROM stripe.charges c
JOIN stripe.balance_transactions bt ON bt.id = c.balance_transaction
WHERE c.created >= :month_start AND c.created < :month_end
  AND c.status = 'succeeded' AND c.amount = 2700;
```

### 3. DOCX generieren

Nutze das Script `scripts/generate-abrechnung.js` (v2). CLI-Argumente:

```bash
cd <skill-dir>/scripts && node generate-abrechnung.js \
  --monat "Februar 2026" \
  --zeitraum "01.02.2026 bis 28.02.2026" \
  --brutto 31845.54 \
  --stripe-fees 1163.58 \
  --refunds 116.90 \
  --anzahl-charges 634 \
  --anzahl-refunds 2 \
  --tripwire-brutto 10719.00 \
  --tripwire-fees 468.25 \
  --tripwire-netto 10250.75 \
  --anzahl-tripwire 397 \
  --detail-json '/tmp/detail.json' \
  --output '/tmp/Abrechnung-Prozessfaktor-<Monat>-<Jahr>.docx'
```

Die `detail.json` enthält die Produktaufschlüsselung mit Stripe-Gebühren:
```json
[
  {"kategorie": "BODY GUIDE (Einmalkauf)", "anzahl": 124, "brutto": "12.028,00 EUR", "stripe_fees": "-372,29 EUR", "netto": "11.655,71 EUR"},
  {"kategorie": "Gesamt (exkl. Tripwire)", "anzahl": 237, "brutto": "21.126,54 EUR", "stripe_fees": "-695,33 EUR", "netto": "20.431,21 EUR"}
]
```

### 4. User-Freigabe und Zustellung

Zeige dem User die Kernzahlen und frage nach Freigabe, bevor das Dokument versendet wird.

Zustellung: Per Slack DM an Ben (Channel `D09K28070GM`) oder als E-Mail-Anhang. Der User entscheidet.

## Stripe-Schema Hinweise

| Gotcha | Detail |
|--------|--------|
| Timestamps | `created` ist Unix-Timestamp (integer), NICHT ISO-Datum |
| Balance Transaction Join | `bt.id = c.balance_transaction` (NICHT `bt.source = c.id`) |
| Stripe-Gebühren | Aus `balance_transactions.fee`, NICHT aus charges direkt |
| 97-EUR-Differenzierung | `amount=9700` + `invoice IS NOT NULL` = X.0 Rate. Ohne Invoice = BodyGuide |
| Charges | Single Source of Truth. Hat `amount`, `amount_refunded`, `invoice`, `status`, `balance_transaction` |

## Neue Produkte erkennen

Falls neue Preispunkte auftauchen (nicht im CASE-Statement), erscheinen sie als "Sonstiges (X EUR)". In dem Fall:

1. Über `stripe.charges.invoice` die Invoice finden
2. `invoices.lines->'data'->0->>'description'` lesen
3. Oder Payment Link via Stripe API identifizieren
4. CASE-Statement in diesem Skill-Dokument aktualisieren

## Design (konsistent mit Dez2025/Jan2026-Abrechnung)

Das DOCX-Design basiert auf der ersten Abrechnung (Referenz: `~/Downloads/Provisionsabrechnung_StrongerYou_X0_30_Dez2025_Jan2026.pdf`):

- **Seitenhintergrund:** Weiß (NICHT Cream)
- **Logo:** StrongerYou Wordmark (`~/Desktop/Area/Marketing/brand-design/assets/logos/strongeryou-logo-dark.png`)
- **Titelseite:** Logo, "Provisionsabrechnung", Untertitel in Blau, Auftraggeber/Auftragnehmer nebeneinander
- **Headlines:** Playfair Display Bold Italic, Farbe `#241404`
- **Sub-Headlines:** Playfair Display Bold Italic, Farbe `#7A94CC`
- **Body:** Noto Sans Regular/Bold
- **Tabellen-Header:** `#7A94CC` (blau), weiße Schrift
- **Tabellen-Zeilen:** Alternierend `#FFFEF2` / `#F5EDE4`
- **Highlight-Box** (Provision): `#D6DEF0` (hellblau) mit `#C4CEE8` Rahmen
- **Provisionszeile** in Haupttabelle: Blau hervorgehoben (`#7A94CC` BG, weiße Schrift)
- **Header rechts oben** (Folgeseiten): "Provisionsabrechnung - [Monat]" in Braun
- **Footer:** "(C) Lightness Fitness"
- **Caption/Datenquelle:** `#96827D` (braun)

## Abrechnungshistorie

| Zeitraum | Provision | Dokument |
|----------|-----------|----------|
| Dez 2025 + Jan 2026 | 17.995,91 EUR | Provisionsabrechnung_StrongerYou_X0_30_Dez2025_Jan2026.pdf |
| Feb 2026 | 3.047,15 EUR | 260308-abrechnung-prozessfaktor-feb-2026.docx |
