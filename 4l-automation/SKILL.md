---
name: 4l-automation
description: >
  Prüft und debuggt Automationen in 4leads. Zeigt den Status aller Automationen, die
  Step-Konfiguration einer spezifischen Automation, und hilft bei der Fehlersuche wenn
  eine Automation nicht wie erwartet feuert. Nutze diesen Command wenn der User eine
  Automation prüfen, debuggen, oder den Status aller Automationen sehen möchte.
user_invocable: true
invocation: /4l-automation
arguments:
  - name: input
    description: >
      Automation-Hash (z.B. "jdkm") oder Name (z.B. "Connect BodyGuide").
      Ohne Argument: zeigt alle 16 Automationen mit Status.
    required: false
---

# Automationen prüfen und debuggen

## Alle Automationen anzeigen

Für die vollständige Liste mit Steps: `~/.claude/skills/4leads/references/automations-map.md`

### Aktive Automationen (11)

| Hash | Name | Trigger |
|------|------|---------|
| jdkm | Connect Kauf - BodyGuide Gutscheincode | Tag: connect-annual/connect-monthly |
| mBJ5 | Freebie x TW (1-2) | Form: 7-Tage-Challenge |
| 8VlR | Freebie x TW (2-2) | Tag: TW gekauft |
| NPMa | Webinarkampagne Webinarjam | Form: Workshop Webinarjam |
| Zxog | Webinarkampagne Everwebinar | Form: Workshop Everwebinar |
| 4G3g | Webinarkampagne Legacy | Form: Launch Workshop |
| qlJ7 | Direktreg. Webinarjam | Webhook |
| 1oBA | Webinar Teilnahme | Webhook |
| lxnQ | Manuell Step 2 | Webhook |
| 5ZlK | Manuell Step 1 | Tag: Webinarreg. manuell |
| A3Xe | SYX.0 Willkommens-E-Mail | Tag: SYX.0 gekauft |

### In Bearbeitung (5)

| Hash | Name |
|------|------|
| g5lE | Evergreen Funnel - Webinar Automation |
| ejMX | Evergreen Funnel - Freebie Start |
| 1o4o | LOESCHEN - Evergreen Funnel - Freebie Start |
| 5ZeG | Evergreen Funnel - Follow-Up (2-2) |
| rL52 | Evergreen Funnel - Follow-Up (1-2) |

## Automation im Detail anzeigen

```bash
# Per Internal Web API (JSON)
playwright-cli open --browser=chrome --persistent --headed "https://app.4leads.net"
playwright-cli eval "() => fetch('/processes/cockpit/edit/{HASH}?xhr=1').then(r => r.text())"

# Oder visuell im Browser
playwright-cli goto "https://app.4leads.net/processes/cockpit/edit/{HASH}"
playwright-cli snapshot
```

## Debugging-Checkliste

Wenn eine Automation nicht feuert:

1. **Trigger prüfen:** Ist der richtige Tag/Form/Webhook konfiguriert?
2. **Status prüfen:** Ist die Automation auf "Aktiv" (nicht "Bearbeitung")?
3. **Bedingungen prüfen:** Hat der Kontakt die erwarteten Tags/Felder?
4. **Rate Limit:** 4leads hat interne Throttling-Logik
5. **Tag-Zuweisung:** Wurde der Tag per n8n oder REST API zugewiesen? (REST API Tag-Zuweisung persistiert NICHT!)

## Trigger-Typen

| Trigger | Code | Beispiel |
|---------|------|---------|
| Tag added | 11000 | Kauf-Events |
| Form submission | 14000 | Freebie-Registrierung |
| Webhook | 17000 | n8n/Webinarjam |
| Tag removed | 11500 | Status-Änderungen |
| Date field | 16100 | Zeitbasierte Flows |

Für alle 32 Trigger-Typen: `~/.claude/skills/4leads/references/triggers.md`
Für alle 34 Action-Typen: `~/.claude/skills/4leads/references/actions.md`
