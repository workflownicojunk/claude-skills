---
name: airtable-schema
description: Use when working with StrongerYou Airtable bases — querying records, building automations that write to Airtable, understanding data structure, or cross-referencing with Stripe/Circle/n8n data. Also use when someone mentions Airtable base IDs, CRM data, Member Intelligence, Typeform responses, BodyGuide, Instagram analytics, or any Airtable-related automation.
---

# Airtable Schema — StrongerYou Automation Hub

**Complete audit: 2026-02-22 | 31 Bases | API via Airtable MCP**

---

## Critical Findings (Read First)

**Data duplication is severe.** Customer/member records exist in 13 parallel tables across 11 different bases. Every base built to solve one problem created another customer table "just in case."

**Key insight for consolidation:**
- `app612Oaw6DXQAZwo` (Subscription Management) is the CLEANEST base — single purpose, contains the critical Stripe Price ID → Circle Tag ID mapping
- `app3aMl8dwLZ3HNcl` (StrongerYou 1.0 Community) is the LEGACY MASTER — the original full-stack CRM, still contains the most complete recipe database
- `appUJJlkdGtEL4hiP` (StrongerYou X.0) is the MOST COMPLETE current operational base — 10 tables covering full purchase-to-delivery workflow
- `appKtaVT4K4s1sksM` (nicolstanzel_Instagram) is the MOST SOPHISTICATED analytics base — has v1 AND v2 of all tables (migration in progress)

---

## Base Inventory by Category

### Category 1: Core Business — Active Production

#### `appUJJlkdGtEL4hiP` — StrongerYou X.0
**Purpose:** Complete X.0 product operational base (purchase → delivery → community access)
**Tables (10):**
- `Contacts` — 17 fields, links to Stripe + Circle
- `Checkout Sessions` — 28 fields, views: 497€ | Missing BodyGuide | Missing Typeform
- `Products` — 17 fields (product catalog with Stripe price IDs)
- `Subscriptions` — 20 fields
- `Subscription_Schedules` — 17 fields (installment tracking)
- `Charges` — 24 fields (full payment history)
- `Payment Intents` — 20 fields
- `Circle_Members` — 16 fields (community access tracking)
- `Typeform Responses` — 12 fields (intake form data)
- `BodyGuides Sent` — 8 fields (delivery tracking)
**Notes:** 12th instance of customer data. Most complete operational base for X.0 launch. "Missing BodyGuide" and "Missing Typeform" views are actionable gap reports.

#### `app612Oaw6DXQAZwo` — Subscription Management
**Purpose:** The canonical Stripe-to-Circle access control mapping
**Tables (9):**
- `Members` — 16 fields (Name, Circle Email, Stripe Email, 4Leads ID, AC ID, Circle Tags, Payments)
- `Prices` — 10 fields: **Stripe Price ID → Circle Tag Name + Circle Tag ID + Access Group** — THIS IS THE KEY MAPPING TABLE
- `Subscriptions` — 9 fields, views: 39€/Mo | 29.97€/Mo | 390€/Year | 299€/Year
- `Circle Tags` — 5 fields (Tag Name, Tag ID, Is Internal, Is Abo Tag)
- `Access Groups` — 3 fields (groups Prices into logical access tiers)
- `Payments` — 11 fields (Invoice-level payment history)
- `Circle Spaces` — 9 fields (Space ID, Type, Is Private, Post/Member Count)
- `Circle Posts` — 12 fields
- `All Contacts` — 14 fields (master contact list with 4Leads, Circle, Stripe IDs linked)
**Notes:** RECOMMENDED as canonical Stripe→Circle mapping reference. The Prices table is critical for automation: maps which Stripe price_id grants which Circle tag_id.

#### `appD4Qy8NS8OqNlPq` — Typeform Responses
**Purpose:** BodyGuide purchase + intake form tracking
**Tables (5):** Customers, Form Responses, BodyGuides Sent, Products, Subscriptions
**Notes:** Primary intake for BodyGuide workflow. Analyzed in session 06 context #5854.

#### `appYL2l06R03rAgSa` — BodyGuide v2
**Purpose:** BodyGuide product delivery workflow
**Tables:** Customers, Orders, BodyGuides Sent, Typeform Responses
**Notes:** Streamlined version of SY 1.0. Analyzed in session 06 context #5855.

#### `appxziChHxAjYvVJj` — StrongerYou CRM
**Purpose:** Haupt-CRM, 3,253 records, Stripe + Circle + 4Leads + AC cross-system identity
**Tables (5):** Members, Subscriptions, Payments, Circle Tags, Access Groups, All Contacts
**Notes:** Analyzed in session 06 context #5856. Most recently built/maintained CRM.

#### `appKtaVT4K4s1sksM` — nicolstanzel_Instagram
**Purpose:** Instagram analytics, content management, viral content analysis, AI comment responses
**Tables (14):**
- `Events` — 26 fields: Instagram comment events with AI response generation, token tracking (input/output/cache), model used
- `Media` — 33 fields: Likes, Reach, Views, Saves, Shares, Comments Count, Transcript, linked to Content Plan
- `Content Ideas` — 12 fields: Hook, Outline, Reel Script, Google Doc link
- `Content Plan` — 11 fields: Calendar view (Datum, Typ, Status, Caption, Media linked)
- `Insights` — 13 fields: Story metrics (Taps Forward/Back, Exits, Replies)
- `Viral Content Analysis` — 16 fields: Script, Virality Score, Transcript, Sentiment
- `Content Categories v2`, `Hashtags v2`, `Performance Insights v2`, `Posting Schedule v2` — v2 structure tables
- `Media v2` — 15 fields (cleaner version of Media)
- `Content Ideas v2`, `Content Plan v2`, `Events v2`, `Viral Content Analysis v2` — v2 versions
**Notes:** v1 and v2 tables coexist — migration in progress. Events/Events v2 tables show AI comment response automation is active (token cost tracking visible). This is where Instagram comment AI replies are logged.

#### `app96hu1fGEdeA4wN` — Member Intelligence
**Purpose:** Analytics layer — Circle engagement + Stripe revenue + course completion
**Tables:** Members (behavioral analytics), Spaces, Sections, Lessons, Events (Zoom recordings), Tasks
**Notes:** ETL-style base consuming from operational systems. Analyzed in session 06 context #5861.

### Category 2: Product-Specific Operational Bases

#### `appIOyMcecpPBmov7` — SY 3.0 Hub
**Purpose:** SY 3.0 launch operational base (product: 997€ one-time + 189€x6 + 349€x3 installments)
**Tables (7):**
- `Kontakte` — 14 fields, views: All | Webinar-Teilnehmer | Käufer | Plan offen | Neue Kontakte
- `Pläne` — 21 fields: JSON-Response (meal plan), PDF-Anhang, Versendet?, Entwurf-geprüft?, Mail-Body-Entwurf, Subject
- `Gmail` — 20 fields: full email thread tracking with Draft ID, label, linked to Pläne
- `Checkout Sessions` — 18 fields, views: 997€ | 189€x6Monate | 349€x63Monate
- `Subscription Schedules` — 8 fields
- `Circle Members` — 37 fields (comprehensive engagement: Posts, Comments, Likes, Gamification Level, all social links)
- `Circle Posts` — 12 fields
**Notes:** The Pläne table reveals SY 3.0 had its own BodyGuide-like fulfillment workflow — meal plans generated as JSON, reviewed as draft, then sent. The "Plan offen" view is the actionable queue. Checkout session views show exactly the SY 3.0 pricing structure.

#### `app3aMl8dwLZ3HNcl` — StrongerYou 1.0 Community (LEGACY MASTER)
**Purpose:** Original complete CRM + BodyGuide delivery + recipe database + Zoom recordings
**Tables (10):**
- `Clients` — 27 fields: BodyGuide PDF attachment, Rezepte (linked), Perplexity Deep Research, Client Context Research, Zoom recording data, all form data embedded
- `Invoices` — 23 fields (full Stripe invoice data with tax, coupons, discount)
- `Customers` — 14 fields (Stripe customers with metadata: typeform_response_id, location)
- `Emails` — 17 fields: "Response needed?", Labels, full email body
- `Form Response` — 30 fields: COMPLETE Typeform intake including Hindernisse, Fokus, Aktivitätslevel, Ernährungsform, Unverträglichkeiten, Heißhunger timing, Abneigungen, Vorlieben, personal Warum — most complete intake form schema
- `Rezepte` — 17 fields (client-specific recipe assignments with MidJourney image generation)
- `Rezeptdatenbank` — 29 fields: the MOST COMPLETE recipe database: Mahlzeitentyp, Ernährungsform, Zutaten, Anleitung, Kalorien, Protein/KH/Fett, Vorbereitungszeit, Craving Control (Was/Warum/Lösung), Saisonalität, Stoffwechselphase, Heißhungerbekämpfung, Budget-Kategorie, Training Timing, Sweet Spot Optimierung
- `Zoom Recordings` — 18 fields: file URLs, transcripts, recording types (CHAT/Shared Screen/TRANSCRIPT views)
- `Transactions` — 29 fields (full Stripe charge data)
- `Tasks` — 6 fields (ETL task queue with Partitioned JSON)
- `community-posts` — 70+ fields (raw Circle API response dump, all attachment fields)
**Notes:** THE LEGACY MASTER. Contains the most sophisticated recipe database (29 fields with metabolic phases, seasonal filters, craving control). The community-posts table with 70+ fields is a raw Circle API dump showing how Circle data was first integrated. This base should be preserved as reference architecture.

### Category 3: Stripe/Financial Bases

#### `appSTh7uBEUBclZSm` — StripeV2
**Purpose:** Monolithic business operations platform (overly ambitious)
**Tables:** Customers, Charges, Form Responses, Members, Invoices, Subscriptions, Subscription Schedules, DATEV integration
**Notes:** The "everything in one base" attempt. Analyzed in session 06 context #5857. Superseded by Stripe V3 + specialized bases.

#### `appcMEvKjpKyLmQid` — Stripe V3
**Purpose:** Simplified subscription management (course correction from V2)
**Tables:** Customers, Members, Subscriptions (views: Coaching | Connect Monthly | Connect Annual)
**Notes:** Simplified V2. Analyzed in session 06 context #5860.

#### `appcE1BMan0WWhgT1` — Fitness Coaching CRM
**Purpose:** Cleaner CRM attempt with business analytics focus
**Tables (5):**
- `Customers` — 6 fields (minimal: Name, Email, Membership)
- `Client History` — 6 fields: Physique Image, AI Advice, Body Fat % — suggests AI-powered body analysis
- `Kunden 360` — 17 fields: Segment, Aktives Produkt, Produkttyp, MRR (EUR), Total Spent (EUR), Aktive Abos, Einzelkäufe, Circle Tags, Stripe Customer ID, Circle Member ID, **Supabase ID** — newest CRM attempt
- `Abonnements` — 11 fields with Supabase ID (links to Supabase StrongerYou project)
- `Käufe` — 7 fields (one-time purchases)
**Notes:** The Supabase ID field in Kunden 360 and Abonnements signals this is the NEWEST design — actively linked to Supabase. "Kunden 360" with MRR/Total Spent fields is a proper customer analytics view. Client History with Physique Image suggests visual coaching assessment workflow.

### Category 4: Community/Circle Mirrors

#### `app5VKbbxKbUmUgei` — Community
**Purpose:** Complete Circle.so platform mirror (members, posts, events, courses)
**Tables:** Members, Posts, Events, Spaces, Subscriptions, Recordings, Courses
**Notes:** Full analysis in session 06 context #5858. Contains webhook-triggered community access removal fields.

#### `appg9ytOVoNy49qot` — Supabase CRM
**Purpose:** Identity resolution hub — cross-system customer matching
**Tables:** Contacts (with Confidence scores + Match Method), Subscriptions, BODY Check Responses, MRR analytics
**Notes:** Analyzed in session 06 context #5859. Unique value: confidence-scored cross-system matching.

#### `appnzkecPnh1Zgb0E` — Efficient Processing
**Purpose:** Circle data processing pipeline (ETL)
**Tables (11):** Posts, Tasks, Members, Spaces, Events, Event Attendees, Tags, Comments, Recordings, Stripe Customers, Subscriptions
**Notes:** Another Circle mirror with processing task queue. The "Tasks" table drives batch sync operations.

### Category 5: Content & Analytics Tools

#### `appMClBnADAYCMJRR` — Rezeptdatenbank (standalone)
**Purpose:** Simple standalone recipe database
**Tables (1):** Rezepte — 15 fields, views: Energiestart | Ausklang | Energie-Power | Low Carb | Vegetarisch | Pescetarisch | Vegan | 300 Kalorien
**Notes:** Simpler version of the recipe DB. May be the public/client-facing version while StrongerYou 1.0 Community's Rezeptdatenbank is the master.

#### `appMCK5LJmNIIBG5m` — n8n Workflows
**Purpose:** n8n workflow documentation/tracking
**Tables (1):** n8n Workflows — 9 fields: Name, Workflow ID, Status, Kategorie, Ziel, Nodes, Letzte Änderung, Zombie-Analyse, n8n Link
**Notes:** Documentation base, not operational.

#### `appbLqSsrgtZgn3du` — Base Schema
**Purpose:** Meta-base tracking all Airtable bases and Google Drive files
**Tables (2):** Bases, Google Drive
**Notes:** Self-referential architecture documentation.

### Category 6: External / Third-Party / Template Bases

These bases are not part of Nicol's core StrongerYou business operations. They are tools, templates, or projects for other clients/purposes:

| Base ID | Name | Category | Notes |
|---------|------|----------|-------|
| `appLFn29BpDqhGvp9` | Speak to Social | Tool | Speak/Social/Speakers tables |
| `appA10OrTtWUw7FyM` | MidJourney&LumaLabs | Tool | Scenes + Movies tables |
| `appAr0CPqrHFL3tfP` | AI Prompt Database | Tool | Prompt testing + optimization (Anthropic test cases) |
| `app8OEUjjrZSJCoZ8` | Prompt Battle Testing | Tool | Prompt Testing + Simulated Conversations |
| `appTbcvkvJxWLHAC7` | Kontent Story Magic | Tool | Stories, Scenes, Video API, Story Types |
| `appjpYhobkJ4gzchQ` | Slack AI Knowledge Base | Unused | Only 3 tables, barely populated |
| `apptO2eM3d8pIc4PS` | Project 10X | Tool | Content repurposing: Content + Transformation Actions + History + GDrive Tracker |
| `app54mxrNWx6CBBFO` | [Template] AI Email Assistant | Template | Read-only, Email Management only |
| `appH9897QnRxMfRGW` | Idea Rain v1.4 | Tool | Tweet/YouTube/TikTok idea tracking |
| `appUHNYIbiX9ZJmuP` | CC-Social Media | Tool | Videos, Scripts, IG Comments, Media, Tone of Voice, Webflow CMS, YouTube/Tweet/TikTok Ideas — possibly for another client |
| `appZ73pzIhwQ1fhbY` | [YT Demo] Kontent Clip Magic | Demo | Read-only demo |
| `appy4234p17tAMkzV` | TK - Social Media Content Planer | External | Social Media Posts, Content Rules, Avatare — likely external client (TK initials) |
| `appau7qm1Pvu3fM84` | Uplifted CRM | External | Sales pipeline CRM: Opportunities (41 fields), Interactions (35 fields), Contacts — sophisticated B2B sales CRM, not StrongerYou |

---

## Data Duplication Map

### Customer/Member Records (13 parallel tables)
```
Table name                          | Base
------------------------------------|----------------------------------
Customers (Form Responses)          | Typeform Responses
Customers                           | BodyGuide v2
Members                             | StrongerYou CRM
Customers + Members                 | StripeV2
members                             | Community
Contacts (+ Confidence Match)       | Supabase CRM
Members                             | Stripe V3
Members (behavioral analytics)      | Member Intelligence
Contacts                            | StrongerYou X.0
Kontakte                            | SY 3.0 Hub
Members + All Contacts              | Subscription Management
Clients                             | StrongerYou 1.0 Community
Kunden 360                          | Fitness Coaching CRM
```

### BodyGuide/Recipe Data (7 overlapping instances)
```
BodyGuides Sent                     | StrongerYou X.0
BodyGuides Sent                     | Typeform Responses
BodyGuides Sent                     | BodyGuide v2
Pläne (meal plan JSON + PDF)        | SY 3.0 Hub
Rezeptdatenbank (29 fields, MASTER) | StrongerYou 1.0 Community
Rezepte (client-specific)           | StrongerYou 1.0 Community
Rezepte                             | standalone Rezeptdatenbank
```

### Circle Community Data (6 mirrors)
```
Circle_Members                      | StrongerYou X.0
Circle Members                      | SY 3.0 Hub
Circle Members (37 fields)          | Subscription Management
members                             | Community
members                             | Efficient Processing
community-posts (70+ fields)        | StrongerYou 1.0 Community
```

---

## Critical Automation Mappings

### Stripe Price ID → Circle Tag ID (from Subscription Management)
This is the canonical access control mapping. Located in:
- Base: `app612Oaw6DXQAZwo`
- Table: `Prices` (tbl95IcePjAZahXMM)
- Key fields: `Stripe Price ID`, `Circle Tag Name`, `Circle Tag ID`, `Is Ratenzahlung`, `Berechtigt Connect`, `Access Group`

### n8n → Airtable Write Patterns
| n8n Workflow | Target Base | Target Table |
|---|---|---|
| `PGHxA72aSQ0562o7` Stripe Subscription Events | Stripe V3 / StrongerYou CRM | Members, Subscriptions |
| `QjU5fCfYNyl4DJa3` Circle Daily Sync | Member Intelligence | Members |
| `ZZMxEFeHKBa4G8By` BodyGuide Generator | Typeform Responses / X.0 | BodyGuides Sent |
| `Jaxx7UCIoFzmo2sZ` Checkout Sessions (INACTIVE!) | StrongerYou X.0 | Checkout Sessions |

### Make.com → Airtable Write Patterns
| Make Scenario | Target Base | Target Table |
|---|---|---|
| `7530283` BodyGuide PRODUCTION | Typeform Responses | Typeform Responses, BodyGuides Sent |
| `6444542` Circle Member Accept | Member Intelligence | Members (2x) |
| `5226771` IG Comments | nicolstanzel_Instagram | Events |

---

## Typeform Forms (form structure — Chrome DevTools scrape pending)
From Airtable data, the intake form fields visible in StrongerYou 1.0 Community's Form Response table (30 fields):
- Basic: Vollständiger Name, Email, Alter, Geschlecht
- Body metrics: Größe (cm), Aktuelles Gewicht (kg), Zielgewicht (kg), Zeitrahmen
- Goals: Worauf liegt dein Fokus?, Dein Aktivitätslevel, Deine Bewegungsgewohnheiten
- Nutrition: Deine Ernährungsform, Unverträglichkeiten, Deine Abneigungen, Deine Vorlieben
- Behavioral: Hindernisse, Heißhunger-Attacken Zeitpunkt, Persönliches Warum
- Health: Gesundheitliche Aspekte
- Open field: "Teile mir hier bitte ALLES mit..." (free-text max input field)

**Note:** Full visual form structure + branching logic requires Chrome DevTools MCP scrape of Typeform dashboard. See "Next Steps" below.

---

## Consolidation Recommendations (for Opus planning)

### Keep (High Value, Production)
1. `app612Oaw6DXQAZwo` **Subscription Management** — the cleanest base, Stripe→Circle mapping
2. `appKtaVT4K4s1sksM` **nicolstanzel_Instagram** — sophisticated analytics, migrate to v2 tables
3. `appUJJlkdGtEL4hiP` **StrongerYou X.0** — best operational base for current product
4. `appxziChHxAjYvVJj` **StrongerYou CRM** — most recently maintained master CRM
5. `appD4Qy8NS8OqNlPq` **Typeform Responses** — active BodyGuide intake pipeline
6. `app96hu1fGEdeA4wN` **Member Intelligence** — analytics layer, keep as BI tool
7. `app3aMl8dwLZ3HNcl` **StrongerYou 1.0 Community** — preserve as reference, has best recipe DB

### Migrate → Archive
8. `appSTh7uBEUBclZSm` StripeV2 → superseded by Stripe V3 + Supabase
9. `appcMEvKjpKyLmQid` Stripe V3 → merge into StrongerYou CRM or use Supabase
10. `app5VKbbxKbUmUgei` Community → superseded by Efficient Processing / Member Intelligence
11. `appg9ytOVoNy49qot` Supabase CRM → identity resolution logic should move to actual Supabase
12. `appnzkecPnh1Zgb0E` Efficient Processing → consolidate into single Circle mirror
13. `appIOyMcecpPBmov7` SY 3.0 Hub → archive (SY 3.0 launch complete)
14. `appYL2l06R03rAgSa` BodyGuide v2 → merge into StrongerYou X.0
15. `appcE1BMan0WWhgT1` Fitness Coaching CRM → newest clean CRM, but duplicates StrongerYou CRM

### Delete / External
16-31: All Category 6 bases (external/template/tool)

### Target Architecture (8 bases)
```
1. StrongerYou CRM        — master identity + subscription state
2. Subscription Management — Stripe→Circle access control (canonical)
3. StrongerYou X.0         — X.0 product operational
4. Typeform Responses      — BodyGuide intake + delivery
5. nicolstanzel_Instagram  — content analytics (v2 tables only)
6. Member Intelligence     — engagement analytics BI layer
7. Rezeptdatenbank         — consolidated recipe master (migrate 1.0 Community's 29-field version)
8. n8n Workflows           — documentation only
```

---

## Next Steps for Opus Planning

1. **Typeform Form Scrape** — Chrome DevTools MCP needed to capture:
   - Visual form design (question layout, design theme, colors)
   - Branching/conditional logic
   - Current form IDs and question IDs (for API integration)
   - Which forms are active vs. archived

2. **Records Count Audit** — Run `mcp__airtable__list_records` with `maxRecords: 1` on each core base to understand data volume before migration

3. **n8n Write Pattern Audit** — Verify which n8n workflows are actually writing to which Airtable tables (some may be inactive)

4. **Supabase ↔ Airtable Sync Direction** — Clarify: is Supabase the golden record or Airtable? Currently both are being written to independently.

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
