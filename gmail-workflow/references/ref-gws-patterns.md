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

## E-Mail senden (HTML-Body, RFC 2822, THREAD-ANTWORT)

`gws gmail +send` unterstützt nur Plain-Text. Für HTML IMMER dieses Python-Pattern verwenden.

**NIEMALS** Shell `printf ... | base64` verwenden: Das führt zu `\n`-Literalen im Body und falschem Encoding bei Umlauten im Subject (Ã¶ statt ö).

**PFLICHT: Thread-Antwort.** Jede Antwort MUSS im bestehenden Thread landen. Dafür sind DREI Elemente nötig:
1. `In-Reply-To` Header: RFC 822 Message-ID der Original-E-Mail
2. `References` Header: Dieselbe Message-ID (bei Ketten: alle vorherigen)
3. `threadId` im JSON-Payload: Gmail threadId der Original-E-Mail

**Message-ID extrahieren** (aus eingehender E-Mail):
```python
# Im Triager/Validator: Für jede E-Mail Message-ID + threadId mitspeichern
msg = gws_get_message(msg_id, format='full')
headers = {h['name']: h['value'] for h in msg['payload']['headers']}
original_message_id = headers.get('Message-ID', '')
thread_id = msg.get('threadId', '')
```

**Sende-Pattern:**
```python
import json, base64, subprocess

FROM = "info@nicolstanzel.de"
to = "kunde@example.de"
subject_raw = "Re: Betreff mit Ümlauten"
html_body = "<p>Hey Name,</p><p>...</p>"
original_message_id = "<CAxxxxxx@mail.gmail.com>"  # RFC 822 Message-ID aus Original
thread_id = "19ce670731580d11"  # Gmail threadId aus Original

# Subject als RFC 2047 UTF-8 Base64 kodieren (Pflicht für Umlaute)
subject_b64 = base64.b64encode(subject_raw.encode('utf-8')).decode('ascii')
subject_encoded = f"=?UTF-8?B?{subject_b64}?="

# RFC 2822 Nachricht mit Thread-Headern
message = (
    f"From: {FROM}\r\n"
    f"To: {to}\r\n"
    f"Subject: {subject_encoded}\r\n"
    f"In-Reply-To: {original_message_id}\r\n"
    f"References: {original_message_id}\r\n"
    f"MIME-Version: 1.0\r\n"
    f"Content-Type: text/html; charset=UTF-8\r\n"
    f"\r\n"
    f"{html_body}"
)

# base64url kodieren (Gmail API erwartet urlsafe, kein padding)
raw = base64.urlsafe_b64encode(message.encode('utf-8')).decode('ascii').rstrip('=')

# WICHTIG: threadId im JSON-Payload mitgeben!
subprocess.run(['gws', 'gmail', 'users', 'messages', 'send',
                '--json', json.dumps({"raw": raw, "threadId": thread_id})], check=True)
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
| `inReplyTo` "Entity not found" | Falsches ID-Format (Gmail ID statt RFC 822 Message-ID) | RFC 822 Message-ID verwenden (Format: `<...@mail.gmail.com>`). NICHT weglassen! Siehe Thread-Antwort-Pattern oben. |
| `\n` erscheint als Literaltext in gesendeten E-Mails | Shell-Variable übergibt JSON-escapes unverarbeitet an printf | NIEMALS Shell-printf; IMMER Python zum Bauen der RFC-2822-Nachricht verwenden |
| Umlaute kommen als `Ã¶` an (z.B. "Öffnen" → "Ã–ffnen") | Subject roh in RFC-2822-Header eingefügt; Mailclient dekodiert Bytes als Latin-1 | Subject als RFC 2047 enkodieren: `=?UTF-8?B?BASE64?=` (via Python `base64.b64encode`) |
| HTML-Body kommt als Plain-Text an | Content-Type Header fehlt | `Content-Type: text/html; charset=UTF-8` + `MIME-Version: 1.0` |
| base64 mit Zeilenumbrüchen (Shell) | `base64` fügt nach 76 Zeichen Umbrüche ein | Irrelevant wenn Python `base64.urlsafe_b64encode` verwendet wird |
