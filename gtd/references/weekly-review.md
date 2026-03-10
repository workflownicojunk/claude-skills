# GTD — Weekly Review (jeden Freitag, 30 Min.)

## Review-Ablauf

```
1. LEEREN (10 Min.)
   → Gmail Inbox auf 0 (oder zumindest getriaged)
   → Circle DMs gecheckt
   → Alle losen Notizen in ClickUp oder backlog.md

2. REVIEWEN (10 Min.)
   → Alle offenen ClickUp Tasks durchgehen
   → Erledigte Tasks als Done markieren
   → Veraltete Tasks löschen
   → Nächste Wochen-Prioritäten setzen

3. PLANEN (10 Min.)
   → KPIs checken (MRR, neue Subs, Churn) → finanz-reporting Skill
   → Content-Plan für nächste Woche → content-strategie Skill
   → 3 Haupt-Fokus-Tasks für die Woche festlegen
```

## Weekly KPI Review (Schnell-Check)

```sql
-- Neue Subs diese Woche:
SELECT COUNT(*) FROM stripe.subscriptions
WHERE status = 'active' AND created > NOW() - INTERVAL '7 days';

-- Churn diese Woche:
SELECT COUNT(*) FROM stripe.subscriptions
WHERE status = 'canceled' AND canceled_at > NOW() - INTERVAL '7 days';

-- Offene Disputes:
SELECT COUNT(*), SUM(amount)/100.0 as eur
FROM stripe.disputes WHERE status NOT IN ('won','lost');
```

## Wöchentliche Gesundheits-Checks

| Bereich | Check | Frequenz |
|---------|-------|----------|
| Gmail Inbox | Alle ungelesen getriaged | Täglich |
| Circle DMs | Alle beantwortet | Täglich |
| Stripe Disputes | Keine älter als 3 Tage ohne Aktion | Täglich |
| ClickUp Backlog | < 20 offene Tasks | Wöchentlich |
| MRR Trend | Wachstum oder Rückgang? | Wöchentlich |
| n8n Workflows | Alle aktiven laufen? | Wöchentlich |

## Freitags-Ritual

```
Freitag 16:00 Uhr:
1. Backlog-Triage (20 Min.)
2. Next-Week-Planung (10 Min.)
3. Gmail auf 0 (oder alle gelabelt)
4. ClickUp: 3 Tasks für nächste Woche mit High Priority markieren
5. Content-Batch für nächste Woche geplant?
```
