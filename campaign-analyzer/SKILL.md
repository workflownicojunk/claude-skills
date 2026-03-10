---
name: campaign-analyzer
description: Use when analyzing email campaign performance, comparing newsletter metrics, identifying top/low performers, optimizing send strategy, or making data-driven recommendations for Nicol Stanzel's 4leads email marketing. Also use when user asks about open rates, click rates, optout rates, campaign benchmarks, or funnel performance for the StrongerYou / Lightness Fitness email list.
---

# Campaign Analyzer — Email Performance Intelligence

Analysiert die Performance von Nicol Stanzels E-Mail-Kampagnen (47 Newsletter, Oct 2025 - Feb 2026).
Liefert datengetriebene Empfehlungen basierend auf Open/Click/Optout Metriken.

## Benchmarks (Stand Feb 2026)

| Metrik | Durchschnitt | Gut | Sehr gut |
|--------|-------------|-----|----------|
| Open Rate (grosse Sendung >1K) | 30% | >35% | >45% |
| Click Rate | 3.5% | >5% | >10% |
| Optout Rate | 2% | <1.5% | <0.5% |
| Open Rate (kleine Sendung <100) | 65% | >70% | >75% |

## Workflow

1. **Ueberblick:** Read `ref_newsletter_stats_summary.md` — Tabelle aller 47 Kampagnen
2. **Muster erkennen:** Read `ref_performance_intelligence.md` — Top/Low Performer Analyse
3. **Rohdaten:** Read `ref_newsletter_stats.json` — Vollstaendige Metriken pro Kampagne
4. **Kontext:** Read `ref_customer_journey.md` — Wo im Funnel sitzt jede Kampagne?
5. **Business Context:** Read `ref_master_context.md` — Produkte, Preise, Zielgruppe

## Analyse-Framework

### Schritt 1: Segmentierung der Kampagne

Jede Kampagne einordnen:

| Segment | Empfaenger | Erwartete Open Rate |
|---------|-----------|-------------------|
| Micro (Bestandskunden) | <100 | 60-75% |
| Warm (Webinar-Teilnehmer) | 500-3.000 | 35-50% |
| Medium (Registrierte) | 3.000-8.000 | 25-35% |
| Breitband (gesamte Liste) | 8.000-15.000 | 20-30% |

**Wichtig:** Kampagnen NUR innerhalb ihres Segments vergleichen. Eine 30% Open Rate bei 13.000 Empfaengern ist besser als 45% bei 200 Empfaengern.

### Schritt 2: Position in Sequenz

Performance faellt ueber eine Sequenz:
- Mail 1: Baseline (100%)
- Mail 3: ~80% der Baseline
- Mail 5: ~70% der Baseline
- Mail 7+: ~60% der Baseline + steigende Optouts

### Schritt 3: Betreff-Analyse

Top-Performing Betreff-Muster:
1. **Persoenlich-direkt:** "Darf ich dir kurz ehrlich etwas sagen?" (45.1% Open)
2. **Story-Teaser:** "Dieser Moment abends im Bad..." (37.8% Open)
3. **Urgency-klar:** "Noch 1 Stunde!" (High Open in warm segments)
4. **Re-Engagement:** "Ich hab mich gefragt wo du bist"

Low-Performing Betreff-Muster:
1. **Generisch:** "Wichtige Ankuendigung" (abfallende Performance)
2. **Wiederholungs-Einladungen:** "Morgen 10 Uhr gehts los" (sinkt stark)

### Schritt 4: Handlungsempfehlungen

Immer ableiten:
- **Was beibehalten?** (funktioniert nachweislich)
- **Was aendern?** (unterdurchschnittlich mit konkretem Fix)
- **Was stoppen?** (schadet der Liste / hohe Optouts)
- **Was testen?** (hypothesengetrieben mit A/B)

## Bekannte Erkenntnisse

1. **Segmentierung ist der staerkste Hebel** — Kleine, gezielte Sendungen outperformen Breitband um 50-200%
2. **5 Follow-Ups sind das Maximum** — Ab Mail 6+ steigen Optouts auf 3-7%
3. **8 Webinar-Einladungen sind zu viele** — 4-5 reichen, Mail 1 und letzte als "staerkste"
4. **"v2" Warm-Sequenzen performen 50-80% besser** als Breitband
5. **Content-Mails mit persoenlichem Touch** haben die besten Click Rates (4.8%)
6. **Wiederholungswebinare an die Gesamtliste** haben kaum Engagement (0.6% Click)

## Output-Format

Analyse-Reports immer in diesem Format:

```markdown
## Kampagnen-Analyse: [Name]

**Segment:** [Micro/Warm/Medium/Breitband]
**Position:** Mail [X] von [Y] in Sequenz
**Vergleichsgruppe:** [aehnliche Kampagnen nennen]

### Metriken
| Metrik | Wert | vs. Benchmark | Bewertung |
|--------|------|---------------|-----------|
| Open Rate | X% | +/-Y% | gut/schlecht |
| Click Rate | X% | +/-Y% | gut/schlecht |
| Optout Rate | X% | +/-Y% | gut/schlecht |

### Empfehlungen
1. [Konkrete Aktion mit Begruendung]
2. [Konkrete Aktion mit Begruendung]
```

## Reference Files

| Datei | Inhalt | Wann laden |
|-------|--------|------------|
| `ref_newsletter_stats_summary.md` | Tabelle aller 47 Kampagnen mit Metriken | Immer zuerst |
| `ref_performance_intelligence.md` | Top/Low Performer, Funnel-Durchschnitte, Empfehlungen | Bei Analyse |
| `ref_newsletter_stats.json` | Rohdaten: 47 Kampagnen mit allen Feldern | Bei Detailanalyse |
| `ref_customer_journey.md` | 3 Entry Points, Funnels, fehlende Journey Steps | Fuer Funnel-Kontext |
| `ref_master_context.md` | Produkte, Preise, Kampagnentypen, Zielgruppe | Fuer Business-Kontext |

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
