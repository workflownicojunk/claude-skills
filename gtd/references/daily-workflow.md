# GTD — Daily Workflow

## Morgen-Triage (max. 10 Minuten)

```
1. ClickUp öffnen → alle Tasks mit Due Date = heute oder überfällig
2. Neue Tasks aus backlog.md prüfen → in ClickUp einpflegen wenn relevant
3. EINEN Haupt-Task für die Session wählen
4. Alle anderen: priorisieren (High/Med/Low), nicht bearbeiten
```

**Faustregel:** Wenn du dich nicht entscheiden kannst, nimm den Task der am meisten blockt oder das größte Revenue-Risiko hat.

## Session-Start Protokoll

```
VOR jeder Session:
→ Welchen EINEN Task mache ich heute fertig?
→ Alle anderen Tasks: parken in .claude/plans/backlog.md
→ Session-Intake (session-intake Skill) ausführen
```

## Inbox-Quellen täglich checken

| Quelle | Tool | Frequenz |
|--------|------|----------|
| Gmail info@nicolstanzel.de | gmail-autoresponder Skill | Täglich |
| Circle DMs unanswered | circle-dm-responder Skill | Täglich |
| Stripe Disputes | stripe-dispute-monitor Skill | Bei Bedarf |
| ClickUp Notifications | ClickUp MCP | Morgens |
| Backlog .claude/plans/backlog.md | Read Tool | Session-Start |

## ClickUp Task-Status Workflow

```
To Do → In Progress (nur EINER gleichzeitig) → Done

NIEMALS: Mehrere Tasks gleichzeitig auf "In Progress"
```

## Ende-der-Session Checkliste

```
[ ] Task als Done markiert (oder explizit auf "blocked" mit Kommentar)
[ ] Neue Erkenntnisse/Tasks in backlog.md notiert
[ ] Nächste Priorität oben in backlog.md gesetzt
[ ] Kein offener Draft oder halbfertiger Code gelassen
```

## Prioritäts-Matrix

```
         DRINGEND            NICHT DRINGEND
WICHTIG  → SOFORT            → PLANEN (Due Date setzen)
         (Disputes, Legal,    (Strategie, Content, Automation)
          Kundenanfragen)

NICHT    → DELEGIEREN/         → LÖSCHEN / Someday-Maybe
WICHTIG   BATCHEN              (backlog.md ohne Due Date)
         (Admin, Routine)
```

## Backlog.md Format

```markdown
## [DATUM] Offene Tasks

### High Priority (diese Woche)
- [ ] [Task] — [Kontext] — Due: [DATUM]

### Normal Priority (nächste 2 Wochen)
- [ ] [Task] — [Kontext]

### Someday / Maybe
- [ ] [Idee] — [Warum interessant]

### Abgeschlossen
- [x] [Task] — Fertig: [DATUM]
```
