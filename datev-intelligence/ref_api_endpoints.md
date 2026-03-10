# DATEV API Endpoints Reference
**Discovered:** 2026-02-22 | **Auth:** Session cookies from SmartLogin QR scan

## Base URLs

- **Kontoblatt / SuSa:** `https://webapps.datev.de/awre-fibu-gateway/`
- **BWA Dashboard:** `https://bwadashboardfrontend.apps.datev.de/api/amr/bwadashboardbackend/api/v1/`
- **DATEV Portal:** `https://webapps.datev.de/duo-start/671912-20048`

## Working Endpoints

### Kontoblatt — Account Ledger (v2)
```
POST /awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048/fiscal-years/{YYYY-MM-DD}/accounts/{SKR03 × 10000}
  ?fiscal-year-month-start=1&fiscal-year-month-end=12&ausziffern=ALL&sort=
Headers:
  X-Requested-With: kontoblatt
  Accept: application/json, text/plain, */*
  Content-Length: 0
Body: null (CRITICAL — NOT '{}', literally null)
Auth: credentials: include (session cookies)
```

**Account Number Format (CRITICAL):**
- Multiply SKR03 account by 10000
- 4-digit SKR03 → 8-digit: `1360 → 13600000`, `4400 → 44000000`
- 5-digit SKR03 → 9-digit: `11000 → 110000000`, `70156 → 701560000`
- HTTP 400 = wrong format!

**Response schema:**
```json
{
  "archiveTimestampsId": 1272724074,
  "months": [{"fiscalYearMonth": 1, "calenderMonth": 1, "state": "DATA_EXISTS"}],
  "transactions": [{
    "kontonummer": 44000000,
    "kontonummerDisplay": "4400",
    "belegdatum": "2025-03-14",
    "buschluessel": "",
    "gegenkonto": 110000000,
    "gegenkontobeschriftung": "Sammelkonto Debitor",
    "gegenkontonummerDisplay": "11000",
    "text": "Lightness Fitness",
    "ust": 19,
    "belegfeld": "BB5CF980-0001",
    "umsatzSoll": null,
    "umsatzHaben": 81.51,
    "eingegumsatz": 97.00,
    "beleglink": "UUID",
    "ebkennzeichen": false,
    "stornokennz": false
  }]
}
```

### SuSa — Trial Balance (v3)
```
GET /awre-fibu-gateway/api/v3/susa/clients/671912-20048/fiscal-years/{YYYY-MM-DD}/months/{1-12}
Headers: X-Requested-With: kontoblatt
Auth: credentials: include
```
Note: SuSa 2026 returns 400 (fiscal year not yet created in DATEV).

### Archive Info
```
GET /awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048/fiscal-years/{YYYY-MM-DD}/archive-info
Headers: X-Requested-With: kontoblatt
Response: {"archiveTimestampsId": 1272724074}
```

### Kontoblatt Settings
```
GET /awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048/settings
GET /awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048
GET /awre-fibu-gateway/api/v2/kontoblatt/clients/671912-20048/fiscal-years/2025-01-01
```

### BWA Dashboard (Read-Only via DOM)
```
Base: https://bwadashboardfrontend.apps.datev.de/api/amr/bwadashboardbackend/api/v1/consultants/671912/clients/20048
/fiscal-years/{YYYYMMDD}/enddate/{YYYYMMDD}/overviewValues?language=de
/fiscal-years/{YYYYMMDD}/enddate/{YYYYMMDD}/comparedate/{YYYYMMDD}/cumulativeValues/false/detailValuesWithAccounts?language=de
```
**Auth:** Requires in-memory Angular OAuth Bearer token — NOT accessible via fetch() from evaluate_script.
**Workaround:** Extract rendered DOM content instead.

## Non-Working Endpoints (HTTP 400/403/404)

| Endpoint | Status | Reason |
|---|---|---|
| `fiscal-years` list | 403 | Forbidden |
| `upload-online` | 404 | Not in Kontoblatt context |
| `belege-online` | 404 | |
| `bank` | 404 | |
| `kassenbuch` | 404 | |
| `bwa` (via FIBU gateway) | 404 | |
| `v3/kontoblatt` | 404 | Version doesn't exist |
| `v2/susa` | 404 | Version mismatch |

## Navigation URLs

```
Dashboard:    https://webapps.datev.de/duo-start/671912-20048
Kontoblatt:   https://webapps.datev.de/awre-fibu/671912-20048/kontoblatt?wj=2025-01-01
SuSa:         https://webapps.datev.de/awre-fibu/671912-20048/susa?wj=2025-01-01
BWA:          https://bwadashboardfrontend.apps.datev.de/rw-dashboard/671912-20048/dashboard-details
```
