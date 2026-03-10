# DATEV REST API (Hidden/Undocumented)

These are internal APIs on webapps.datev.de discovered via browser traffic interception. They require an active SmartLogin session (QR code scan) — no API keys exist.

## Authentication

1. Navigate to webapps.datev.de
2. Scan QR code with DATEV SmartLogin app
3. Session cookies are set automatically
4. All requests must include `credentials: include`
5. Sessions expire (exact timeout unknown, likely 30-60 minutes)

## Base URL
```
https://webapps.datev.de/awre-fibu-gateway
```

## Endpoints

### Kontoblatt (Account Ledger) — v2
```
POST /api/v2/kontoblatt/clients/671912-20048/fiscal-years/{YYYY-MM-DD}/accounts/{account_number}
```
Query params: `fiscal-year-month-start=1&fiscal-year-month-end=12&ausziffern=ALL&sort=`
Headers: `X-Requested-With: kontoblatt`, `Accept: application/json, text/plain, */*`
Body: `null` (literally null, NOT `'{}'`)

Response: Array of transaction objects.

### Transaction Object Schema (compressed keys)
```json
{
  "d": "2025-01-23",     // Datum (date)
  "bu": "",              // BU-Schluessel (posting key)
  "gk": "1800",          // Gegenkonto (contra account)
  "gkn": "Bank",         // Gegenkontoname (contra account name)
  "txt": "Stripe",       // Buchungstext (posting text)
  "bf": "",              // Belegfeld (document reference)
  "s": null,             // Soll (debit amount, null if credit)
  "h": 1.46,             // Haben (credit amount, null if debit)
  "ld": null,            // Leistungsdatum (service date)
  "bl": null,            // Beleglink (document link)
  "eb": false,           // EB-Wert (opening balance)
  "st": false            // Storno (reversal)
}
```

### SuSa (Trial Balance) — v3
```
GET /api/v3/susa/clients/671912-20048/fiscal-years/{YYYY-MM-DD}/months/{month_1_to_12}
```
Headers: `X-Requested-With: kontoblatt`

Response structure:
```json
{
  "archiveTimestampsId": "...",
  "baseCurrency": "EUR",
  "balances": [
    {
      "groupId": "1",        // Account class
      "rowType": "TOTAL",
      "balances": [...]       // Nested: SUB_TOTAL -> DATA rows
    }
  ]
}
```

Hierarchy: TOTAL (class) → SUB_TOTAL (subgroup) → DATA (individual account)

Each DATA row:
```json
{
  "accountType": "SKR03",
  "number": "1360",
  "name": "Geldtransit",
  "rowType": "DATA",
  "total": { "debit": 1234.56, "credit": 5678.90 },
  "balances": [
    { "month": 1, "debit": 100, "credit": 200 },
    ...
  ]
}
```

### Archive Info
```
GET /api/v2/kontoblatt/clients/671912-20048/fiscal-years/{YYYY-MM-DD}/archive-info
```

### Known NON-functional Endpoints (return 404):
upload-online, belege-online, bank, kassenbuch, bwa, uva, stammdaten, kontenplan, v3 kontoblatt, v2 susa

## Local Data Files

| File | Size | Content |
|------|------|---------|
| `.tmp/datev_kontoblatt_ALL.json` | 561 KB | 86 accounts, 2,652 transactions |
| `.tmp/datev_susa_dec2025.json` | 61 KB | Year-end trial balance |
| `.tmp/datev_susa_monthly.json` | 149 KB | All 12 monthly trial balances |
| `.tmp/datev_kontoblatt_1360_full.json` | 112 KB | Stripe clearing account (179 txns) |

Missing accounts in kontoblatt dump: 4000, 4400, 4839, 4840, 5906, 9000, 9008, 9009, 10001-11000
