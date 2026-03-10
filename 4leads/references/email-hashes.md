# 4leads Email Hashes

Full list of known email templates. Use hash to navigate to edit page:
`/email-funnel/email/edit/e/{hash}`

For the complete list with dates, see `4leads-expert` skill: `ref_campaigns_api.md`

## Connect / BodyGuide Emails (most relevant)

| Hash | Name | Notes |
|------|------|-------|
| R0Lk | Connect Kauf - BodyGuide Gutscheincode Zustellung | Uses {{field_15306}} for promo code |
| 5OLR | Connect Kauf - Auto - BodyGuide Gutscheincode Willkommen | Automation email, uses {{field_15306}} |
| j3pm | Connect Kauf - BodyGuide Promo - Gutscheincode | Uses {{field_15306}} |
| YK4q | SYX.0 Willkommensmail nach Kauf | Welcome email after SY purchase |
| 2rQ4 | BG_gekauft_Onboarding | BodyGuide purchase onboarding |

## Freebie / Tripwire Emails

| Hash | Name |
|------|------|
| AjRd | Freebie Welcome + Download - 7-Tage Happy Body Plan |
| YKBE | TW FOLLOW-UP #1 Tag 1 |
| ZKjG | TW FOLLOW-UP #2 Tag 2 |
| JqY7 | TW FOLLOW-UP #3 Tag 3 |
| vG8L | TW WELCOME Tripwire - Zugang bereit |
| R0Nl | TW WELCOME ZUM TRIPWIRE (Happy Body Training) |

## Webinar Emails

| Hash | Name |
|------|------|
| xLnm | SY3.0 Registrierungsbestätigung |
| BRpP | SY3.0 Erinnerung 3 Tage vorher |
| jQkG | SY3.0 Erinnerung 1 Tag vorher |
| RJZj | SY3.0 Erinnerung 1 Stunde vorher |
| 5reY | SY3.0 Erinnerung 15 Minuten vorher |
| l2Nn | SY3.0 Erinnerung 2 Stunden nachher |
| 1r3R | SY3.0 Erinnerung 1 Tag nachher |

## Connect Follow-Up Emails

| Hash | Name |
|------|------|
| RJlb | NL 01 Connect Follow-Up - Der Moment in dem alles kippt |
| gK71 | NL 02 Connect Follow-Up v1 |
| eKGG | NL 02 Connect Follow-Up v2 |
| l2XO | NL 02 Connect Follow-Up v3 |
| aKvB | NL 03 Connect Follow-Up - Letzte Chance |

## Lookup by Email ID

If you have an internal email ID (numeric, e.g., 51894) but not the hash, use:
```bash
playwright-cli eval "() => fetch('/email-funnel/email?pageNum=0&pageSize=100&xhr=1').then(r=>r.json()).then(d=>d.htmlReplaces)"
```
Then search the HTML for the email ID to find its hash.
