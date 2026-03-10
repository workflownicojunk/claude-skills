---
name: gtd
description: Use when user asks "Was steht heute an?", "Aufgaben priorisieren", "Backlog triage", "ClickUp Tasks", "GTD", "Was machen wir heute?", "Welche Aufgaben sind offen?", "Backlog leeren", or any session planning involving task management. Also use when parking new tasks during a session to prevent scope creep.
---

# GTD — Getting Things Done (StrongerYou Workspace)

Task management für das Lightness Fitness BOS. Integriert ClickUp MCP, `.claude/plans/backlog.md`, und die Session-Governance-Regel (1 Task pro Session).

**Supabase:** `dajxbqfiugzigrnsoqau` | **ClickUp Workspace:** 49 active tasks (48 To Do, 1 In Progress)

## Load This Reference When...

| Task | Reference File |
|------|---------------|
| Daily triage, Aufgaben priorisieren, Session planen | [daily-workflow.md](references/daily-workflow.md) |
| Backlog aufräumen, Aufgaben kategorisieren, archivieren | [backlog-management.md](references/backlog-management.md) |
| Wöchentliches Review, KPIs checken, Fortschritt bewerten | [weekly-review.md](references/weekly-review.md) |

## Die 3 Regeln (NICHT verhandelbar)

1. **1 Task pro Session.** Neue Ideen kommen SOFORT in `.claude/plans/backlog.md`. Kein Scope Creep.
2. **ClickUp ist Single Source of Truth.** Nichts mündlich "gemerkt" lassen. Alles rein.
3. **Tasks parken vor Ausführung.** Wenn du mittendrin etwas Neues siehst: backlog.md, dann weiter.

## Quick Capture (Scope Creep Guard)

Wenn während einer Session eine neue Aufgabe auftaucht:

```
1. Kurz notieren in .claude/plans/backlog.md (Titel + Kontext, 1 Zeile)
2. NICHT abzweigen
3. Weiter mit aktueller Aufgabe
```

Backlog-Format:
```markdown
## [DATUM] Neue Tasks
- [ ] [Task-Titel] — [Kontext/Warum entdeckt] — [Priorität: High/Med/Low]
```

## ClickUp MCP Schnellreferenz

```
# Alle offenen Tasks abrufen:
list_tasks mit: status=open, order_by=priority

# Task erstellen:
create_task mit: name, description, priority (1=urgent, 2=high, 3=normal, 4=low), due_date

# Task updaten:
update_task mit: task_id, status, priority

# Tasks suchen:
search mit: query, space_id
```

**Workspace Struktur:** ClickUp → StrongerYou Workspace → Listen nach Domain (Sales, Tech, Community, Finance, Content)

## Triage Kriterien

| Signal | Aktion |
|--------|--------|
| Blocking andere Aufgaben | Sofort erledigen |
| Stripe/Legal/Dispute | Gleiche Woche |
| Customer-facing (offene Anfragen) | 24h SLA |
| Automation/Tech | Batch am Freitag |
| Content/Marketing | Batch Montag |
| Ideen ohne klaren Nutzen | Someday/Maybe → backlog.md |

## GTD Phasen (angepasst)

```
CAPTURE → PROCESS → ORGANIZE → ENGAGE

Capture:  Alles rein in ClickUp (via MCP oder direkt)
Process:  Ist es actionable? → ja: Task. Nein: Referenz oder löschen.
Organize: Label setzen (Domain + Priorität), Due Date wenn nötig
Engage:   Session-Fokus: EINEN Task wählen und fertigmachen
```

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
