# gws CLI Patterns für Gmail

## Auth prüfen

```bash
gws auth status
```

## Inbox fetchen

```bash
# Triage-Übersicht (bevorzugt)
gws gmail +triage --max 50 --format json

# Alternativ: Liste (userId PFLICHTFELD!)
gws gmail users messages list --params '{"userId":"me","q":"in:inbox","maxResults":50}' --format json
```

## E-Mail aus Inbox archivieren (INBOX-Label entfernen)

```bash
# RICHTIG: removeLabelIds im --json body, NICHT in --params
gws gmail users messages modify \
  --params '{"userId":"me","id":"MESSAGE_ID"}' \
  --json '{"removeLabelIds":["INBOX"]}'

# FALSCH (gibt "Invalid label" Fehler):
# --params '{"userId":"me","id":"...","removeLabelIds":["INBOX"]}'

# batchModify funktioniert NICHT mit ids-Array (gibt "Invalid ids value")
# Stattdessen: for-Schleife mit einzelnen modify-Calls
```

## E-Mail vollständig lesen

```bash
gws gmail users messages get --params '{"id":"MSG_ID","format":"full"}' --format json
```

## Sent/Draft fetchen

```bash
# Sent der letzten 24h (für Duplikat-Erkennung)
gws gmail users messages list --params '{"q":"in:sent newer_than:1d","maxResults":100}' --format json

# Aktuelle Drafts
gws gmail users messages list --params '{"q":"in:draft","maxResults":30}' --format json
```

## E-Mail senden (HTML-Body, RFC 2822)

`gws gmail +send` unterstützt nur Plain-Text. Für HTML IMMER dieses Pattern:

```bash
TO="kunde@example.de"
SUBJECT="Re: Betreff"
HTML_BODY="<p>Hey Name,</p><p>...</p>"

# WICHTIG: base64 ohne Zeilenumbrüche (tr -d '\n')
RAW=$(printf 'From: info@nicolstanzel.de\r\nTo: %s\r\nSubject: %s\r\nContent-Type: text/html; charset=UTF-8\r\nMIME-Version: 1.0\r\n\r\n%s' \
  "$TO" "$SUBJECT" "$HTML_BODY" | base64 | tr -d '\n')

gws gmail users messages send --json "{\"raw\":\"$RAW\"}"
```

Sonderzeichen im Subject (Umlaute) als encoded header wenn nötig:
```bash
SUBJECT_ENC=$(printf '=?UTF-8?B?%s?=' "$(echo -n "$SUBJECT" | base64 | tr -d '\n')")
```

## Batch-Archivieren (Inbox-Label entfernen)

```bash
# EINE Call für alle IDs auf einmal
# WICHTIG: --params '{"userId":"me"}' ist PFLICHT, sonst 400 Error
gws gmail users messages batchModify \
  --params '{"userId":"me"}' \
  --json '{"ids":["id1","id2","id3"],"removeLabelIds":["INBOX"]}'
```

## Batch-Löschen (Drafts entsorgen)

```bash
# EINE Call für alle Draft-IDs
gws gmail users messages batchDelete \
  --json '{"ids":["draft_id1","draft_id2"]}'
```

WICHTIG: Für Drafts NICHT `removeLabelIds: ["DRAFT"]` verwenden (wirft Error). Stattdessen batchDelete.

## Labels setzen

```bash
# Labels: Support = Label_3955183308810104764, Kündigung = Label_7235028904381884705
gws gmail users messages modify --id MSG_ID \
  --json '{"addLabelIds":["Label_3955183308810104764"]}'
```

## Suche

```bash
# Duplikat-Check
gws gmail users messages list \
  --params '{"q":"in:sent to:EMAIL newer_than:1d","maxResults":5}' --format json

# Gesendete BodyGuides
gws gmail users messages list \
  --params '{"q":"in:sent to:EMAIL subject:dein Plan ist da newer_than:7d","maxResults":3}' --format json
```

## Bekannte Bugs & Workarounds

| Problem | Ursache | Lösung |
|---------|---------|--------|
| `removeLabelIds: ["DRAFT"]` Error | Gmail erlaubt kein manuelles Entfernen des DRAFT-Labels | `batchDelete` für Drafts |
| `inReplyTo` "Entity not found" | Erwartet RFC 822 Message-ID, nicht Gmail message ID | Ohne `inReplyTo` senden |
| base64 mit Zeilenumbrüchen | E-Mail wird falsch geparst | `base64 \| tr -d '\n'` |
| HTML-Body kommt als Plain-Text an | Content-Type Header fehlt | `Content-Type: text/html; charset=UTF-8` + `MIME-Version: 1.0` |
