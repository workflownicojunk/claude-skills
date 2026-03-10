# Spaces, Navigation und Content Access

## Space Groups (4 aktive + 1 Link-Gruppe)

### Willkommen (space_group_id: 847643)
| ID | Name | URL-Slug | Zugang |
|----|------|----------|--------|
| 2190086 | CONNECT - Start | /c/willkommen/ | Connect |
| 2191875 | StrongerYou X.0 - Start | /c/willkommens-checkliste/ | X.0 |
| 2193389 | Say HELLO - StrongerYou X.0 | /c/stelle-dich-vor/ | X.0 |

### Community (space_group_id: 763884)
| ID | Name | URL-Slug | Zugang |
|----|------|----------|--------|
| 2205902 | What's new? | /c/what-s-new/ | Alle |
| 2143723 | Connect | /c/workout-tipps/ | Connect |
| 2024410 | Events | /c/live-calls-1eb9fe/ | Connect |
| 2017697 | Erfolge | /c/erfolge/ | Connect |
| 2248293 | Rezepte Community | /c/rezepte-community/ | Connect |
| 2256299 | Challenges | /c/challenges-7a4eab/ | Connect |
| 2315789 | Special Challenge X-Mas 25 | - | Connect |
| 2283120 | Mini Challenge Beckenboden | - | Connect |
| 2277373 | Challenge Cellulite | - | Connect |
| 2277123 | Mini Challenge Atmung | - | Connect |
| 2275284 | Mini Challenge Abs | - | Connect |
| 2271289 | Mini Challenge Stretching | - | Connect |
| 2270213 | Mini Challenge Achtsames Essen | - | Connect |
| 2269637 | Challenge Faszienrolle | - | Connect |
| 2259884 | Mini Challenge Body Circle2 | - | Connect |
| 2259874 | Mini Challenge Body Circle1 | - | Connect |
| 2258932 | Challenge Krafttraining | - | Connect |
| 2256305 | Mini Challenge Isometrisch | - | Connect |
| 2271146 | Test Events | - | Intern (zu löschen!) |

### Coaching (space_group_id: 766869)
| ID | Name | URL-Slug | Zugang |
|----|------|----------|--------|
| 2353992 | StrongerYou X.0 | /c/strongeryou-x-0/ | X.0 |
| 2434613 | StrongerYou X.0 Chat | /c/strongeryou-x-0-chat/ | X.0 |
| 2286749 | StrongerYou X.0 Live | /c/sport-live-themencalls/ | X.0 |
| 2332535 | Happy Body Circle | /c/7-tage-happy-body-plan/ | HBT |
| 2337915 | C9 Reset | /c/c9-reset/ | C9 |
| 2286737 | StrongerYou 3.0 | /c/strongeryou-3-0/ | Legacy |
| 2056665 | StrongerYou 2.0 | /c/aufzeichnungen-2-0/ | Legacy |
| 2024383 | StrongerYou 1.0 | /c/materialien-db505c/ | Legacy |

### Ressourcen (space_group_id: 850034)
| ID | Name | URL-Slug | Zugang |
|----|------|----------|--------|
| 2195115 | Video library | /c/video-library/ | Connect |
| 2195110 | Hilfreiche Ressourcen | /c/ressourcen/ | Connect |

### Links (Sidebar, extern)
Trustpilot, BodyGuide (Stripe), Harvest Republic (20%), InnoNature (10%), Les Mills (10%), Plattform-Anleitung (YouTube), iOS App, Android App, Instagram, YouTube, Facebook

---

## Content Access: Visibility-Regeln

### Zwei Ebenen
1. `is_private: true` - Nicht-Member können nicht beitreten
2. `is_hidden_from_non_members: true` - Space unsichtbar in Sidebar

**Regel: ALLE Spaces müssen `is_hidden_from_non_members: true` haben.**

### Access Groups steuern Sichtbarkeit

Neue Member sehen nur Spaces ihrer Access Group. Access Groups werden im Circle Admin UI konfiguriert (/settings/access_groups). Die API hat KEINEN Endpoint zum Lesen/Schreiben der Space-zu-AccessGroup-Zuordnung.

### Visibility-Check (API)

```bash
CIRCLE_KEY=$(grep '^CIRCLE_ADMIN_API_KEY=' ~/Desktop/.env | cut -d= -f2)

curl -s "https://app.circle.so/api/admin/v2/spaces" \
  -H "Authorization: Token $CIRCLE_KEY" | python3 -c "
import json,sys; d=json.load(sys.stdin)
problems=[s for s in d['records'] if not s.get('is_hidden_from_non_members')]
print(f'Problematische Spaces: {len(problems)}')
for s in problems: print(f'  [{s[\"id\"]}] {s[\"name\"]}')"
```

### Bekanntes Problem: Historische Space-Mitgliedschaft

`is_hidden_from_non_members: true` verhindert nur, dass NEUE Nicht-Mitglieder Spaces sehen. Bestehende Space-Mitglieder (vor Access Group Konfiguration eingetragen) behalten vollen Zugang.

**Beispiel:** Ninett Krause sieht 31 statt 7 Spaces wegen historischer direkter Space-Mitgliedschaft.

**Fix:** Space-Mitgliedschaften manuell bereinigen (explizite Freigabe von Nicol nötig).

---

## Navigation (Header)

| Element | URL | Typ |
|---------|-----|-----|
| Home (Feed) | /feed | Link |
| Courses | /courses | Link |
| Events | /events | Link |
| Members | /members | Link |
| Leaderboard | /leaderboard | Link |

## Kurs-Kennzahlen (Stand Mär 2026)

- **StrongerYou X.0:** 258 Studenten, 57% Abschlussrate, 52 Lektionen in 7 Sektionen
- **Mini Challenges:** 8 separate Kurse (je 5-10 Lektionen)
- **Full Challenges:** 3 Kurse (9-29 Lektionen)

## Circle Enterprise Features (aktiv)

| Feature | Status |
|---------|--------|
| AI Feed Summary ("Summarize" Button) | Aktiv |
| Post-Tags (Space-Filter) | Aktiv |
| Pinned Posts | Aktiv (veraltet in Connect!) |
| Space-Header-Links (Affiliate) | Aktiv |
| Course Dashboard + Progress Tracking | Aktiv |
| Leaderboard + Gamification | Aktiv |
| Direct Messages + Chat Threads | Aktiv |
| Go Live (Live Streaming) | Sichtbar |

---

## UI-Audit Zusammenfassung (Mär 2026)

**Komplexitätsgrad: 7/10 (hoch)**

| Problem | Schweregrad | Status |
|---------|-------------|--------|
| Test Events Space in Produktion | KRITISCH | Offen |
| 8 Coaching-Spaces ohne Trennung aktiv/archiv | HOCH | Offen |
| 14 Kurse unsortiert auf Courses-Seite | HOCH | Offen |
| 11 Links in Sidebar (zu viel) | MITTEL | Offen |
| 3 Willkommen-Spaces für verschiedene Produkte | MITTEL | Offen |
| Pinned Posts in Connect veraltet (Dez 2025) | MITTEL | Offen |
| Feed ohne Produkt-Filter | NIEDRIG | Offen |

## Aktivste Community-Mitglieder

| Name | Rolle/Aktivität |
|------|-----------------|
| Claudia Bauer | Leaderboard #1 (41.842 Punkte 2025) |
| Birgit Gouw | Häufigste Posterin, hohe Qualität |
| lippi (Lucia Lippitsch) | Moderatorin, 9.011 Kommentare |
| Nicol Stanzel | Admin, uid: 7fb4894b |
