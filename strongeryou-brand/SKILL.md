---
name: strongeryou-brand
description: "Use when creating any visual output (.docx, .pptx, .html, email, .pdf, Circle Pages) for Lightness Fitness or StrongerYou. Triggers: StrongerYou branding, brand colors, brand fonts, Nicol Stanzel documents, professional formatting for Lightness Fitness, brand compliance review, landing page design, Circle community pages. Also triggers on any file generation (.docx, .pptx, .html) where the target audience is StrongerYou customers or the document represents the Lightness Fitness brand. Use this whenever visual assets, logos, or photos of Nicol are needed. Never generate placeholder images when real brand assets are available."
---

# StrongerYou Brand System

## Brand Palette

| Token | HEX | Use |
|-------|-----|-----|
| `dark` | `#241404` | Headlines, body text (NEVER use `#000000`) |
| `blue` | `#7A94CC` | Accent ONLY: section titles, table headers, CTAs, thin lines, pill buttons |
| `brown` | `#96827D` | Secondary: footer, captions, dividers |
| `cream` | `#FAEDE1` | PPTX/HTML/Landing Page background (NOT DOCX - DOCX uses white) |
| `card` | `#FFFEF2` | Content boxes, table data rows |
| `white` | `#FFFFFF` | DOCX page background, table header text |
| `warm-brown` | `#8B6F47` | Pricing pages: headlines, card borders, CTAs |
| `gold` | `#C4943A` | Badges, "Gratis" labels, promotional accents |

**FORBIDDEN colors:** `#8B7355`, `#141413`, `#d97757`, `#6a9bcc`, `#000000`

## Typography

| Role | Font (Docs/PPTX) | Font (Web/Landing) | Weight | Style |
|------|------------------|-------------------|--------|-------|
| H1/H2 | Playfair Display | Playfair Display | Bold 700 | **Italic** (BOTH required) |
| H3 | Noto Sans | Lato | Bold 700 | Normal, color: `#7A94CC` |
| Body | Noto Sans | Lato | Regular 400 | Normal |
| Caption | Noto Sans | Lato | Regular 400 | color: `#96827D` |
| Buttons | Noto Sans | Lato | Bold 700 | White on blue, pill-shape |

Playfair Display Bold Italic is non-negotiable for all headlines across all formats. The body font differs by context: Noto Sans for documents (DOCX, PPTX), Lato for web (HTML, landing pages, Circle Pages). This reflects what's live on nicolstanzel.com. Both are clean sans-serif fonts with similar proportions, so the brand feel stays consistent.

**CRITICAL:**
- Headlines = `"Playfair Display"` Bold + Italic. NEVER `"Georgia"` as primary font.
- Body docs = `"Noto Sans"`. Body web = `"Lato"`. NEVER `"Arial"` as primary font.
- Georgia/Arial are CSS fallbacks ONLY (second in `font-family` stack).

## Asset Library

Real brand assets exist locally and via URL. Never generate placeholder images when these are available. Choose the asset that fits the context.

### Logos

| Asset | Local Path | URL | When to Use |
|-------|-----------|-----|-------------|
| Nicol Stanzel (black, signature circle) | `~/Desktop/Area/Marketing/brand-design/assets/logos/logo-nicol-stanzel.png` | `https://onecdn.io/media/2a83dc76-dc55-4d6b-a859-9b101375edbc/md2x` | Documents, emails, page headers |
| StrongerYou (beige script wordmark) | `~/Desktop/Area/Marketing/brand-design/assets/logos/strongeryou-logo-dark.png` | `https://onecdn.io/media/950f89c5-0fb6-420a-8d18-6669569e1649/md2x` | Formal documents (Abrechnungen), footers, community pages |

### Photos of Nicol

| Asset | Local Path | URL | Context |
|-------|-----------|-----|---------|
| Portrait (colorful, smiling) | `nicol-portrait-bunt.jpg` | `https://onecdn.io/media/ad1c7eef-e89d-408a-b052-59c1bf3ffc37/lg2x` | About sections, bios |
| Fitness mirror (athletic) | `nicol-spiegel-fitness.jpg` | `https://onecdn.io/media/af6f494c-9111-4a9e-a3fb-149bbaba092d/lg2x` | Results, transformation |
| Couch portrait (relaxed) | `nicol-couch-portrait.jpg` | `https://onecdn.io/media/982063b1-ea82-41a9-8b1a-ec98627fec66/lg2x` | Welcome pages, personal touch |
| Happy Body mockup (iPad) | `freebie-happy-body-mockup.jpg` | `https://onecdn.io/media/6c1b80d9-15a4-4bc4-878c-713b2f367b16/lg2x` | Freebie offers, lead magnets |

All photo files in: `~/Desktop/Area/Marketing/brand-design/assets/images/`

### Mood / Stock Images

| Asset | File | URL | Context |
|-------|------|-----|---------|
| Woman sad (pain point) | `stock-frau-traurig.jpg` | `https://onecdn.io/media/a52e688e-36a5-41f0-b1c6-20ac806e2479/lg2x` | Problem awareness |
| Woman dancing (transformation) | `stock-frau-tanzend.jpg` | `https://onecdn.io/media/1ba3cc57-15b9-49b9-b0c7-06ac4d4e0981/lg2x` | Desired outcome |
| Gym faded cream | `bg-gym-faded-cream.jpg` | `https://onecdn.io/media/38862139-ecee-4947-9393-edd39efda9a9/lg2x` | Background texture |
| Golden key | `golden-key-symbol.jpg` | `https://onecdn.io/media/59104aa6-f02b-4837-a631-b767ee3cd800/lg2x` | Unlock/access metaphor |

### Testimonials (Vorher/Nachher)

Three authentic before/after photos from real clients. Use for social proof sections.
- `testimonial-vorher-nachher-1.jpg` — `https://onecdn.io/media/df95e445-298b-4843-bba0-12d27076538d/lg2x`
- `testimonial-vorher-nachher-2.jpg` — `https://onecdn.io/media/12536064-f70c-451c-bf5c-6696222c53ec/lg2x`
- `testimonial-vorher-nachher-3.jpg` — `https://onecdn.io/media/3f1bd44f-82f1-42f3-a631-d778dafd94b1/lg2x`

### Full-Page Screenshots (Design Reference)

When building new pages, refer to these for layout inspiration:
`~/Desktop/Area/Marketing/brand-design/assets/onepage-screenshots/`
- `homepage-full.png` — 7-Tage Happy Body Plan (main funnel)
- `online-workshop-jan.png` — Workshop sales page
- `bodyguide-full.png` — BodyGuide sales page
- `dankesseite.png` — Thank-you page (post signup)
- `danke-nach-kauf.png` — Thank-you page (post purchase, onboarding)
- `zahlungsart.png` — Payment/pricing page

## Format-Specific Workflow

Determine output format, then read the corresponding reference BEFORE writing any code:

| Output | Background | Body Font | Reference (MUST read first) |
|--------|------------|-----------|----------------------------|
| **DOCX** | WHITE `#FFFFFF` | Noto Sans | [references/docx-template.md](references/docx-template.md) |
| **PPTX** | Cream `#FAEDE1` | Noto Sans | [references/pptx-template.md](references/pptx-template.md) |
| **HTML/Email** | Cream `#FAEDE1` | Noto Sans | [references/html-template.md](references/html-template.md) |
| **Landing Page / Circle** | Cream `#FAEDE1` | Lato | [references/onepage-visual-brand.md](references/onepage-visual-brand.md) |

For landing pages and Circle Pages, the OnePage reference contains proven design patterns (hero sections, testimonial layouts, pricing cards, onboarding flows) extracted from live nicolstanzel.com pages.

For funnel context (customer journey, automations, follow-up sequences, page connections), read [references/funnel-map.md](references/funnel-map.md).

## Button Style (Web/Landing/Circle)

Buttons on web properties use a specific style that differs from document CTAs:
- **Shape:** Pill (border-radius: 100px), NOT rectangular
- **Primary:** `#7A94CC` background, white text, Lato Bold
- **Secondary (pricing):** `#8B6F47` background, white text
- **Padding:** 16px 40px (generous)

## PPTX Design Rules (Critical)

- **NEVER** use `#7A94CC` (blue) as full slide background. Blue is accent-only.
- **Proven formula:** Cream background + white content cards (rounded, shadow) + blue as text/line accents
- White boxes MUST have: rounded corners (`border-radius: 16pt`) + shadow (`0 3pt 8pt rgba(0,0,0,0.06)`) + no border

## Pre-Output Checklist (MANDATORY)

Run through EVERY item before delivering ANY branded output:

- [ ] Headlines: `"Playfair Display"` Bold Italic (not Georgia, not missing Italic)
- [ ] Body: `"Noto Sans"` (docs) or `"Lato"` (web) — not Arial
- [ ] H3 titles: Bold `#7A94CC`
- [ ] Table headers: `#7A94CC` bg + white text
- [ ] Table rows: `#FFFEF2` bg
- [ ] No borders on tables or content boxes
- [ ] Background correct for format (DOCX=white, PPTX/HTML/Landing=cream)
- [ ] PPTX: NO full-slide blue backgrounds
- [ ] No forbidden colors (`#8B7355`, `#000000`, `#141413`, `#d97757`, `#6a9bcc`)
- [ ] Footer: `#96827D` warm brown
- [ ] Real logo/photo used (not placeholder) when context calls for it
- [ ] Web buttons: pill-shape (100px radius), not rectangular

## Self-Improvement Protocol

See `~/.claude/rules/self-improvement.md` (global rule, applies to all skills).
