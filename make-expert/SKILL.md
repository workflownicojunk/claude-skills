---
name: make-expert
description: Use when working with StrongerYou Make.com scenarios — debugging errors, understanding existing automations, creating new scenarios, or analyzing performance. Also use when someone mentions Make.com, BodyGuide errors, Stripe Checkout workflow, Instagram comments automation, or Make.com scenarios by ID.
---

# Make.com Expert — StrongerYou Automation Hub

Complete reference for the StrongerYou Make.com instance.
**Updated:** 2026-02-22 (Session 06 — full browser scrape + blueprint analysis)
**Org:** 3637606 | **Team:** 1710694 | **Plan:** Core (40,000 ops/month) | **Zone:** eu2.make.com

---

## Active Scenarios (16 active)

### Folder: 01_BODY-GUIDE (471694)

| ID | Name | Trigger | Executions | Error Rate | Modules |
|----|------|---------|------------|------------|---------|
| **7530283** | ##PRODUCTION## StrongerYou BODY GUIDE | Webhook (Typeform, instant) | 470 | **38%** (177) | 38 |
| **8147687** | [Prompt Caching] - BODY GUIDE | Schedule (polling) | 408 | **27%** (112) | ~38 |
| **8607954** | 2nd [Prompt Caching] - BODY GUIDE | Schedule (polling) | 143 | **25%** (36) | ~38 |
| 7608934 | Watch sent Messages → Update Order Status | Schedule (hourly) | 737 | 1.5% | ~5 |

### Folder: 02_COMMUNITY (471695)

| ID | Name | Trigger | Executions | Error Rate |
|----|------|---------|------------|------------|
| 6444542 | Watch Member accept Invitation | Schedule (daily 08:00) | 54 | 0% |
| 8106980 | New Member joined Community | Webhook | 181 | 1% |

### Folder: 03_INSTAGRAM (471696)

| ID | Name | Trigger | Executions | Error Rate |
|----|------|---------|------------|------------|
| **5226771** | (1/2)-IG-Comments-Automation | Webhook (instant) | 4,591 | <1% |
| 6748587 | instagram_user_insights | Schedule (daily 07:00) | 30 | 0% |
| 6473016 | Scrape Instagram Profile Daily | Schedule (daily 07:00) | 30 | 0% |

### Folder: 04_STRIPE-SALES (471697)

| ID | Name | Trigger | Executions | Error Rate | Modules |
|----|------|---------|------------|------------|---------|
| **5905616** | Stripe Checkout → Ship to Customer | Webhook (Stripe) | 351 | 6% | 37 |
| 6118129 | Subscription Event → Update Airtable | Webhook (Stripe) | 592 | 1% | ~9 |
| **8577869** | New Refunds | Webhook (Stripe) | 33 | **27%** | 4 |

### Folder: 05_CUSTOMER-SUCCESS (471698)

| ID | Name | Trigger |
|----|------|---------|
| 6995613 | New 1:1 Meeting Prep Response | Webhook (Typeform) |
| 6959860 | New Booking → Send Typeform Response | Webhook (Cal.com) |

### Folder: 06_CRM-MARKETING (471699)

| ID | Name | Trigger |
|----|------|---------|
| 8074923 | New C9 Purchase → Notify → Send Circle Invitation | Schedule (hourly) |
| 7399289 | Sync ActiveCampaign analytics to Google Sheets | On-demand |

---

## BodyGuide Production — Full Architecture (7530283)

**The core business process.** Typeform survey → AI meal plan → PDF → Gmail.
See `make/docs/bodyguide_production_deep_dive.md` for complete documentation.

### 38-Module Flow Summary

```
Phase 1 (Validation):   Typeform Webhook → Sleep → Airtable/Stripe charge check
Phase 2 (Data Prep):    Build customer JSON → Airtable upsert → Gmail history search
Phase 3 (AI — CORE):    Claude Extended Thinking API → [⚠️ JSON Parse Bug] → Airtable save
Phase 4 (nano-banana):  Claude prompt → nano-banana API → recipe predictions → Airtable
Phase 5 (Document):     Snack cards (Claude) → Google Docs template → CloudConvert PDF
Phase 6 (Delivery):     Google Drive upload → Claude email copy → Gmail Draft → Airtable update
```

### Critical Bug — 38% Warning Rate

**Root cause confirmed** (2026-02-22, module [111]):
- Module [334] calls Anthropic API directly with Extended Thinking enabled
- Claude sometimes returns non-clean JSON (markdown wrapping, thinking blocks, preamble)
- Module [111] `json:ParseJSON` receives invalid JSON → triggers "Source is not valid JSON" warning
- **Fix:** Add regex extraction step between [334] and [111] to isolate the JSON block

### Airtable Tables Used

| Table | Purpose |
|-------|---------|
| Responses | Typeform form submissions |
| Charges | Stripe charge records (payment validation) |
| Ernährungspläne | Generated meal plan records |
| Rezepte | Recipe / nano-banana prediction data |

---

## Instagram Comments (1/2) — Full Architecture (5226771)

**The Instagram engagement pipeline.** Captures all comments, catalogs media, analyzes with AI.
See `make/docs/ig_comments_automation_deep_dive.md` for complete documentation.

### 24-Module Flow Summary

```
New Comment webhook → Airtable: Search Media
    │
    ├─ [NEW media] → Instagram: Get + Download → Airtable: Create Media record
    │       ├─ VIDEO  → OpenAI Whisper (transcribe) → Airtable update → Log event
    │       ├─ ALBUM  → Get all slides → Claude analyze images → Airtable update → Log event
    │       └─ IMAGE  → Claude analyze → Airtable update → Log event
    │
    └─ [KNOWN media] → Airtable: Log event only
```

### Key Facts

- **4,591 executions**, <1% errors — well-built, stable
- Most runs: <1 second, 1 op (media already known, fast pass-through)
- AI calls only happen for NEW media → cost-efficient
- **(2/2) response scenario is INACTIVE** — comments are catalogued but NOT auto-replied

### Airtable Tables Used

| Table | Purpose |
|-------|---------|
| Media | IG post/reel catalogue with AI descriptions and transcripts |
| Events | Comment event log — feeds the (2/2) response scenario |

---

## Stripe Checkout — Architecture (5905616)

37-module multi-product fulfillment workflow. Fires on every `checkout.session.completed`.

```
Stripe Webhook → Sleep (payment settle) → Airtable lookup → 4Leads contact create
→ BasicRouter (by product type, 4 branches):
    Branch 1: Circle invite + tag + 4Leads tag + Airtable update
    Branch 2: Circle invite + tag + 4Leads tag + Airtable update
    Branch 3: Circle invite + tag + 4Leads tag + Airtable update
    Branch 4: Circle invite + tags + 4Leads global field + ActiveCampaign update
              + Gmail welcome email + 4Leads tag + Sheets log
→ SevDesk: Search / Create contact + communication ways
```

**Products handled:** 4 product types (Circle memberships and coaching products).

---

## New Refunds — Bug Analysis (8577869)

4-module workflow: `Charge.refunded` → Search Charge → Search Refund → Upsert Refund

**Confirmed Bug:**
- Module 11 searches for a Refund record using `{{10.object.id}}` = **Charge ID** (ch_xxx)
- A Refund ID has format `re_xxx` and is found at `{{10.object.refunds.data[0].id}}`
- **Fix:** Change module 11 search formula to use `{{10.object.refunds.data[0].id}}`

---

## Integration Map

```
Typeform  → 7530283 → Airtable, Claude API, Google Docs, CloudConvert, Drive, Gmail  [BodyGuide]
Instagram → 5226771 → Airtable, Claude, OpenAI Whisper                               [Comments]
Stripe    → 5905616 → Airtable, Circle, 4Leads, SevDesk, Gmail, Sheets              [Checkout]
Stripe    → 6118129 → Airtable                                                        [Subscriptions]
Stripe    → 8577869 → Airtable                                                        [Refunds ⚠️]
Circle    → 6444542 → Airtable                                                        [Member Join]
Gmail     → 8074923 → Circle, Airtable, OpenAI, Sheets                               [C9 Purchase]
```

---

## Inactive Scenarios (16 inactive)

| ID | Name | Last Modified | Action |
|----|------|--------------|--------|
| 5227378 | (2/2)-Instagram Automation | 2026-01-14 | Evaluate: which (2/2) version to reactivate |
| 7917249 | (2/2)-Instagram Automation (PRODUCTION) | 2025-11-04 | Candidate for reactivation |
| 8425709 | 4 Leads Import | 2026-02-17 | May need periodic reactivation |
| 6492206 | AI Email Assistant #1 | 2026-02-16 | Superseded by n8n Gmail AutoResponder |
| 8656692 | Email Assistant | 2026-02-15 | Superseded by n8n Gmail AutoResponder |
| 7204159 | New Zoom Recording → Clean up Transcript | 2026-02-15 | Check if still needed |
| 6507790 | AI Content Generator | 2025-07-29 | Old, evaluate |
| 7382944 | New Lead → Generate Product Rec | 2025-10-21 | Old |
| 7591600 | Add SY Workshop Registrants to 4leads | 2025-10-21 | Old |
| 6395707 | Social Media Content Calendar | 2025-08-19 | Old |
| 7326668 | Update Airtable Community Posts Database | 2025-11-13 | Old |
| 4868148 | StrongerYou - Abnehm-Guide | 2025-06-07 | Very old → delete candidate |
| 7042511 | TRAINING Guide | 2025-09-02 | Old |
| 8459559 | IF_BodyGuide x Harvest Republic | 2026-01-19 | Evaluate |
| 6654736 | Highly Relevant Content Ideas | 2025-08-25 | Old |
| 6581718 | Using regex in Make.com (masterclass) | 2025-08-05 | Test → delete |

---

## Priority Action Items

1. **Fix BodyGuide JSON parse bug** (7530283, module [111]) — 38% error rate costs money and loses customers
2. **Fix New Refunds bug** (8577869, module 11) — use `refunds.data[0].id` not `object.id`
3. **Consolidate 3 BodyGuide variants** — clarify when 8147687 vs 8607954 vs 7530283 is used
4. **Reactivate (2/2) Instagram response** — 4,591 comment events captured, zero auto-replies sent
5. **Archive AI Email Assistants** (6492206, 8656692) — replaced by n8n `y5Lw3SMN781DTtwa`

---

## Reference Files

- `make/docs/bodyguide_production_deep_dive.md` — Full 38-module BodyGuide architecture
- `make/docs/ig_comments_automation_deep_dive.md` — Full 24-module IG Comments architecture
- `make/docs/make_scenarios_audit.md` — Original API-based audit with error statistics
- `make/screenshots/` — Visual canvas screenshots of all 16 active scenarios

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
