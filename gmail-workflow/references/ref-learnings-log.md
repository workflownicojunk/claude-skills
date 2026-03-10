# Email Support Learnings Log

This file captures mistakes, edge cases, and optimizations discovered during live email support sessions. Read this file at the START of every email support workflow. Update it at the END.

## Critical Mistakes (never repeat)

### 1. Empty promises (severity: HIGH)
**What happened:** Agent promised "we'll manually unlock within 24h" but never executed.
**Affected:** Marion, Christine, Andrea, Melanie (March 2026)
**Root cause:** Agent wrote promise in email before executing the action.
**Fix:** Execute the action FIRST (Circle API), THEN write the confirmation email. Never promise future actions.

### 2. Sent cancellation without Nicol's approval (severity: CRITICAL)
**What happened:** Sarah Schrank's cancellation was auto-confirmed via send_email instead of draft.
**Root cause:** Agent classified TYPE_B coaching cancellation as TYPE_C monthly.
**Fix:** IMMER den Stripe-Preis prüfen um TYPE_B vs TYPE_C zu unterscheiden. 97/179/189/349 EUR/Mo = TYPE_B (Coaching-Raten) = NIEMALS kündigen, Reframing AUTO-SENDEN. Die Kundin sagt vielleicht "Mitgliedschaft" oder "Abo", aber der Preis entscheidet. TYPE_B: Reframing senden, NICHT kündigen. TYPE_C: Reframing senden, bei Insistenz zum Laufzeitende kündigen.

### 3. Duplicate emails (severity: HIGH)
**What happened:** Isabelle and Marion each received 2 identical emails same day.
**Root cause:** Session restart or parallel agent didn't check sent folder.
**Fix:** Triager-Agent prüft sent_24h PFLICHT. Duplikat-Erkennung ist in Phase 1 eingebaut.

### 4. Wrong customer context (severity: HIGH)
**What happened:** Nathalie received an answer meant for another customer.
**Root cause:** Agent mixed up thread contexts when processing multiple emails.
**Fix:** Read the FULL thread before composing. Extract customer name + email from the thread, not from memory.

### 5. Internal system names leaked (severity: MEDIUM)
**What happened:** Melanie was told "im Stripe-System".
**Forbidden terms in customer emails:** Stripe, Supabase, n8n, Circle API, Webhook, 4leads, Pipeline, Backend, Database, SQL, API, MCP.
**Replacement:** "in unserem System", "in deinem Konto", "bei uns".

### 6. Broken umlauts (severity: MEDIUM)
**What happened:** 4 emails sent with "oe/ae/ue" instead of "ö/ä/ü".
**Affected:** Nicole Senftleben, Christine Kramer, Irmtraut, Sabine Hümpfer
**Root cause:** Encoding issue in htmlBody generation.
**Fix:** Always verify umlauts in final email text. Use UTF-8 encoding explicitly.

### 7. Forbidden phrases used (severity: MEDIUM)
**What happened:** "Tut mir leid" and "Ich verstehe" appeared in emails.
**Blacklist:** "Tut mir leid", "Entschuldigung", "Ich verstehe dich", "Ich verstehe deine Frustration", "Kein Problem", "Gerne geschehen", any em-dash.
**Replace with:** Direct, warm, confident tone. Acknowledge the situation, don't apologize for it.

### 8. Unverified payment claims (severity: HIGH)
**What happened:** "Deine Zahlung ist eingegangen" sent without Stripe check.
**Fix:** Supabase SQL query is MANDATORY before any payment claim. No shortcuts.

### 9. Phone calls promised (severity: MEDIUM)
**What happened:** "Ich rufe dich an" written in email.
**Fix:** Agent cannot make phone calls. Never promise calls, meetings, or video chats.

### 10. Emails too long (severity: LOW)
**What happened:** 15 of 21 emails exceeded 5-sentence limit.
**Fix:** 3-5 sentences MAX. One clear action item. No redundant politeness.

### 11. Circle tag without user_email parameter (severity: HIGH)
**What happened:** Tag-Zuweisung schlägt fehl ohne user_email.
**Fix:** `user_email` ist PFLICHTFELD in `POST /api/admin/v2/tagged_members`.

## Edge Cases Discovered

### Coaching rate vs. monthly subscription
Customers sometimes confuse their coaching installment (TYPE_B, 97-349 EUR, contractually bound) with a monthly subscription (TYPE_C, 39-69 EUR, cancellable). Always check Stripe price to determine type before responding.

### Email mismatch detection
80% of "I can't log in" emails are caused by email mismatch (paid with email A, trying to log in with email B). Check Stripe customer email vs. the email they're writing from. If different, that's the answer.

### Draft label removal quirk
Gmail API: `removeLabelIds: ["DRAFT"]` throws an error. Use gws batchDelete statt removeLabelIds für Drafts.

### inReplyTo "Entity not found"
Gmail API: `inReplyTo` parameter expects the RFC 822 Message-ID header (format: `<CAxxxxxx@mail.gmail.com>`), NOT the Gmail message ID. Workaround: Send without `inReplyTo`/`threadId`, use a fresh subject line.

### Connect pricing confusion
Multiple Connect price points exist (39/59/69 EUR monthly, 299/390/468 EUR yearly). Always verify the customer's actual price in Stripe before quoting any number.

### Template variable bug recovery
When automated systems (4leads, n8n) send emails with unrendered template variables like `{{variable_name}}`, send a follow-up with the correct value. Never acknowledge the error. Act as if it's a normal message: "Hier ist dein Gutscheincode: XXXX".

### Stripe promo code email mismatch
Customers sometimes write from a different email than their Stripe purchase email. Promo codes are mapped via `metadata.customer_email` in Stripe. When looking up a code, check both the writing email AND common variations.

### .env variable naming
`STRIPE_API_KEY` (not STRIPE_SECRET_KEY). `SUPABASE_SERVICE_ROLE_KEY` (NOT SUPABASE_KEY). Always verify with `grep '^STRIPE\|^SUPABASE' ~/Desktop/.env` if unsure about exact variable names. Never guess.

### gws base64 encoding
RFC 2822 Messages für gws gmail send: `base64 | tr -d '\n'` (kein line-wrap). Sonst werden E-Mails nicht korrekt geparst.

### gws batchModify requires userId parameter
`gws gmail users messages batchModify` braucht `--params '{"userId":"me"}'`. Ohne diesen Parameter: 400 "Required path parameter userId is missing".

### Supabase RPC execute_sql unreliable
Supabase RPC `execute_sql` hat zeitweise Schema-Cache-Probleme (PGRST002). Direkte Stripe API als Primary verwenden, Supabase als Fallback.

### Typografische Anführungszeichen brechen JSON
Sonnet-Responder verwendet manchmal „..." (typografische Anführungszeichen) in HTML-Bodies. Diese brechen JSON-Parsing. Responder-Agent muss nur ASCII-Anführungszeichen oder HTML-Entities verwenden.

### gws +triage zeigt unread, nicht inbox
`gws gmail +triage` zeigt `is:unread` E-Mails (inkl. archivierte). Für Inbox-Prüfung: `gws gmail users messages list --params '{"q":"in:inbox"}'`.

## Session Log (append after each session)

| Date | Emails processed | Sent | Errors | Tool Calls | Notes |
|------|-----------------|------|--------|------------|-------|
| 2026-03-04 | 21 | 14 | 5 | ~142 | Baseline. Duplicates, empty promises, umlauts |
| 2026-03-05 | 15 | 10 | 2 | ~120 | Improved. Still too long emails |
| 2026-03-06 | 14 | 11 | 0 | ~95 | Circle API fixes applied. Clean run. |
| 2026-03-07 | 4 | 4 | 0 | ~40 | Supabase down, used Stripe API direct. |
| 2026-03-07b | 18 | 14 | 0 | ~130 | Connect promo codes via Stripe API. Template variable bug recovery. inReplyTo bug. |
| 2026-03-07c | 20 | 2 | 0 | ~60 | Mostly follow-ups on already-answered emails. |
| 2026-03-08 | 30 | 14 | 0 | ~142 | 18 Kunden + 12 System. 7 Duplikat-Sperren. Julia Langner Connect freigeschaltet. |
| 2026-03-08b | 16 | 11 | 0 | ~100 | Sarah Salmen Circle freigeschaltet. 48 Entwürfe geleert. |
| 2026-03-09 | 29 | 18 | 0 | ~142 | Roberta + Claudia Circle freigeschaltet. 25 Drafts geleert. |
| 2026-03-10 | 50 | 17 | 0 | ~48 | ERSTER multi-agent Workflow-Test. 4 Agents (Haiku/Sonnet). 33 archiviert, 18 Drafts gelöscht. Fixes: SUPABASE_KEY→SUPABASE_SERVICE_ROLE_KEY, batchModify braucht userId:me, Duplikat-Erkennung verschärft, Stripe API direkt statt Supabase RPC. |
| 2026-03-10b | 50 | 9 | 0 | ~45 | 9 Antworten (6 FAQ, 3 Access), 39 archiviert, 1 Draft gelöscht. Orchestrator korrigierte Umlaute (Responder liefert ae/oe/ue statt ä/ö/ü) + entfernte unverified payment claim bei Nadine. Executor hat beantwortete Mails nicht archiviert → Orchestrator fix via modify --json body. |
