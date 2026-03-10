# DATEV EXTF v700 Format Specification

## File Structure

- **Line 1:** Header metadata (semicolon-separated, 38+ fields)
- **Line 2:** Column names (semicolon-separated)
- **Lines 3+:** Transaction data rows

## Header Line 1

```
"EXTF";700;21;"Buchungsstapel";12;{created_yyyymmdd};{created_by};"";"";"671912";"20048";{fiscal_year_start_yyyymmdd};{sachkontennummernlaenge};"";"";"";"";"";1;"";;;;"";;;"{label}"
```

### Key Positions:
| Position | Field | Value |
|----------|-------|-------|
| 1 | Format | "EXTF" |
| 2 | Version | 700 |
| 3 | Category | 21 (Buchungsstapel) |
| 4 | Label | "Buchungsstapel" |
| 5 | Format Version | 12 |
| 6 | Created Date | YYYYMMDD format |
| 10 | Berater-Nr | "671912" |
| 11 | Mandant-Nr | "20048" |
| 12 | Fiscal Year Start | YYYYMMDD (e.g., "20250101") |
| 13 | Sachkontennummernlaenge | 4 (length of account numbers) |
| 19 | WKZ | 1 (for EUR) |

## Header Line 2 (Column Names)

```
Umsatz (ohne Soll/Haben-Kz);Soll/Haben-Kennzeichen;WKZ Umsatz;Kurs;Basisumsatz;WKZ Basisumsatz;Konto;Gegenkonto (ohne BU-Schluessel);BU-Schluessel;Belegdatum;Belegfeld 1;Belegfeld 2;Skonto;Buchungstext;Postensperre;Diverse Adressnummer;Geschaeftspartnerbank;Sachverhalt;Zinssperre;Beleglink;Beleginfo - Art 1;Beleginfo - Inhalt 1;Beleginfo - Art 2;Beleginfo - Inhalt 2;Beleginfo - Art 3;Beleginfo - Inhalt 3;Beleginfo - Art 4;Beleginfo - Inhalt 4;Beleginfo - Art 5;Beleginfo - Inhalt 5;Beleginfo - Art 6;Beleginfo - Inhalt 6;Beleginfo - Art 7;Beleginfo - Inhalt 7;Beleginfo - Art 8;Beleginfo - Inhalt 8;KOST1 - Kostenstelle;KOST2 - Kostenstelle;Kost-Menge;EU-Land u. UStID;EU-Steuersatz;Abw. Versteuerungsart;Sachverhalt L+L;Funktionsergaenzung L+L;BU 49 Hauptfunktionstyp;BU 49 Hauptfunktionsnummer;BU 49 Funktionsergaenzung;Zusatzinformation - Art 1;Zusatzinformation - Inhalt 1;Zusatzinformation - Art 2;Zusatzinformation - Inhalt 2;Zusatzinformation - Art 3;Zusatzinformation - Inhalt 3;Zusatzinformation - Art 4;Zusatzinformation - Inhalt 4;Zusatzinformation - Art 5;Zusatzinformation - Inhalt 5;Zusatzinformation - Art 6;Zusatzinformation - Inhalt 6;Zusatzinformation - Art 7;Zusatzinformation - Inhalt 7;Zusatzinformation - Art 8;Zusatzinformation - Inhalt 8;Zusatzinformation - Art 9;Zusatzinformation - Inhalt 9;Zusatzinformation - Art 10;Zusatzinformation - Inhalt 10;Zusatzinformation - Art 11;Zusatzinformation - Inhalt 11;Zusatzinformation - Art 12;Zusatzinformation - Inhalt 12;Zusatzinformation - Art 13;Zusatzinformation - Inhalt 13;Zusatzinformation - Art 14;Zusatzinformation - Inhalt 14;Zusatzinformation - Art 15;Zusatzinformation - Inhalt 15;Zusatzinformation - Art 16;Zusatzinformation - Inhalt 16;Zusatzinformation - Art 17;Zusatzinformation - Inhalt 17;Zusatzinformation - Art 18;Zusatzinformation - Inhalt 18;Zusatzinformation - Art 19;Zusatzinformation - Inhalt 19;Zusatzinformation - Art 20;Zusatzinformation - Inhalt 20;Stueck;Gewicht;Zahlweise;Forderungsart;Veranlagungsjahr;Zugeordnete Faelligkeit;Skontotyp;Auftragsnummer;Buchungstyp;USt-Schluessel (Anzahlungen);EU-Land (Anzahlungen);Sachverhalt L+L (Anzahlungen);EU-Steuersatz (Anzahlungen);Erloeskonto (Anzahlungen);Herkunft-Kz;Buchungs GUID;KOST-Datum;SEPA-Mandatsreferenz;Skontosperre;Gesellschaftername;Beteiligtennummer;Identifikationsnummer;Zeichnernummer;Postensperre bis;Bezeichnung SoBil-Sachverhalt;Kennzeichen SoBil-Buchung;Festschreibung;Leistungsdatum;Datum Zuord.Steuerperiode
```

## Data Row Format

Position-by-position for the most common fields:

| # | Field | Required | Format | Example |
|---|-------|----------|--------|---------|
| 1 | Umsatz | Yes | Decimal with comma | 97,00 |
| 2 | Soll/Haben | Yes | S or H | S |
| 3 | WKZ Umsatz | Yes | ISO currency | EUR |
| 4 | Kurs | No | Exchange rate | (empty) |
| 5 | Basisumsatz | No | | (empty) |
| 6 | WKZ Basisumsatz | No | | (empty) |
| 7 | Konto | Yes | Account number | 1360 |
| 8 | Gegenkonto | Yes | Contra account | 8400 |
| 9 | BU-Schluessel | No | Posting key | (empty) |
| 10 | Belegdatum | Yes | DDMM | 0104 |
| 11 | Belegfeld 1 | No | Document reference | ch_abc123 |
| 12 | Belegfeld 2 | No | | (empty) |
| 13 | Skonto | No | | (empty) |
| 14 | Buchungstext | Yes | Description | "Checkout 97 EUR" |
| 15 | Postensperre | No | 0 or 1 | 0 |

Remaining fields (16-116): Generally empty for Stripe imports. Fill with semicolons.

## Encoding & Format Rules

1. **File encoding:** Windows-1252 (CP1252), NOT UTF-8
2. **Line endings:** CRLF (\r\n)
3. **Field separator:** Semicolon (;)
4. **Decimal separator:** Comma (97,00)
5. **Text quoting:** Double quotes for text fields containing special chars
6. **Date format (Belegdatum):** DDMM — exactly 4 digits (0104 = January 4)
7. **Empty fields:** Just semicolons (no spaces)

## Complete Row Examples

### Charge (Revenue):
```
97,00;S;EUR;;;;1360;8400;;0104;ch_3QZCmLABC123;;;"Checkout 97 EUR";0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
```

### Fee (Expense):
```
2,81;S;EUR;;;;4970;1360;;0104;ch_3QZCmLABC123;;;"Stripe Fee";0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
```

### Refund (Credit):
```
97,00;H;EUR;;;;1360;8400;;0104;re_ABC123;;;"Refund 97 EUR";0;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
```
