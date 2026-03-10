# Circle Pages Internal API Reference

Reverse-engineered endpoints for Circle Pages (Site Builder). All requests require an active browser session (use `playwright-cli` with persistent profile).

## Endpoints

### List all pages
```
GET /internal_api/settings/site/pages?
Headers: Accept: application/json
Response: { page, per_page, has_next_page, count, records: [...] }
```

### Get single page
```
GET /internal_api/settings/site/pages/{id}?
Headers: Accept: application/json
Response: { id, name, status, url, blocks: { content: {root}, inline_attachments: [] }, setting, theme, ... }
```

### Create new page
```
POST /internal_api/settings/site/pages?
Headers: Content-Type: application/json, Accept: application/json
Body: {}
Response: { id: number } (status 201)
```

### Update page content (PUT blocks)
```
PUT /internal_api/settings/site/pages/{id}?
Headers: Content-Type: application/json, Accept: application/json
Body: { "blocks": { "id": "uuid", "type": "root", "props": { "children": { "prop": "children", "type": "children", "value": [block1, block2, ...] } } } }
Response: full page object (status 200)
```
**WICHTIG:** Funktioniert auch auf leere Seiten (ohne existierenden Block). Die Root-ID kann frei gewählt werden.

### Update page settings (name, slug)
```
PATCH /internal_api/settings/site/pages/{id}/settings?
Headers: Content-Type: application/json, Accept: application/json
Body: { "name": "...", "slug": "..." }
Response: status 200
```

### Publish page
```
POST /internal_api/settings/site/pages/{id}/publish?
Headers: Content-Type: application/json, Accept: application/json
Response: status 200
```

## Page Editor URL
```
https://strongeryou.circle.so/settings/pages/edit/{id}
```
Muss über SPA-Navigation erreicht werden. Direkte goto-Aufrufe verursachen beforeunload-Dialoge.

## Block Types

### HomepageBlock1 (Text/Hero)
Props: `styles`, `leftContent` (children), `buttons` (children), `image`, `imagePosition`

Best for: Rechtliche Seiten (AGB, Datenschutz, Impressum), Text-lastige Seiten (Willkommen)

### SalesBlock11 (FAQ Accordion)
Props: `header` (children: h2 + p), `content` (children: faqItem[]), `footer` (children: p + primaryButton), `styles`

Jedes `faqItem` hat:
- `header`: children mit h5 (Frage)
- `content`: children mit p (Antwort)

Best for: FAQ-Seiten. Nutzt CSS-Variablen (`var(--theme-...)`) statt fester Farben.

## Verfügbare Block-Kategorien im Editor

| Kategorie | Templates |
|-----------|-----------|
| Hero | HomepageBlock1, Hero Header Sales 1, Homepage Block 1 |
| Features | Homepage Block 2-6, Sales Block 2-6, About Us Block 1/2/4 |
| CTA | Homepage Block 4/8/9, Sales Block 10/12 |
| Pricing | Sales Block 9, Pricing Block 1, Homepage Block 8 |
| Testimonials | Testimonials Block 1-3, Homepage Block 7, Sales Block 7/8 |
| Team | Homepage Block 2, About Us Block 3 |
| Stats | Homepage Block 5 |
| Blog | BlogListing Block 1, Blog Block 1 |
| Contact | Contact Block |
| FAQs | Sales Block 11 |

## Brand Styling (StrongerYou)

### Für HomepageBlock1 (feste Werte)
- Background: `#FAEDE1` (Cream)
- H1: Playfair Display, 700, italic, 2.5rem, color `#241404`
- H2: Lato, 700, normal, 1.5rem, color `#7A94CC`
- H3: Lato, 700, normal, 1.25rem, color `#7A94CC`
- p: Lato, 400, normal, 1rem, lineHeight 1.7, color `#241404`

### Für SalesBlock11 (CSS-Variablen)
Nutzt `var(--theme-website-...)` Variablen. Übernimmt automatisch das Site-Theme.

## Optimaler Workflow (5 Schritte pro Seite)

```bash
# 1. Seite erstellen
playwright-cli eval "async () => { ... POST ... }"

# 2. JSON generieren (Python mit Template-Cloning)
python3 generate-page.py

# 3. Content uploaden
playwright-cli eval "async () => { ... PUT ... }"

# 4. Settings setzen
playwright-cli eval "async () => { ... PATCH settings ... }"

# 5. Veröffentlichen
playwright-cli eval "async () => { ... POST publish ... }"
```

## Bekannte Einschränkungen
- `beforeunload` Dialog bei SPA-Navigation im Editor: `playwright-cli dialog-accept` nutzen
- Playwright MCP-Server nutzt NICHT das persistente Profil: Immer `playwright-cli` (CLI) verwenden
- Editor-URL `/settings/pages/edit/{id}` geht nur über SPA-Navigation, nicht per Direktlink von extern

## Existierende Seiten (Stand 2026-03-07)

| ID | Name | Slug | Status |
|----|------|------|--------|
| 39639 | Datenschutzerklärung | datenschutz | published |
| 39642 | Allgemeine Geschäftsbedingungen | agb | published |
| 39644 | Impressum | impressum | published |
| 39645 | Willkommen | willkommen | published |
| 39646 | FAQ | faq | published |
