# HTML / Email Template for StrongerYou Brand

## Brand Constants (self-contained)

```
COLORS:  BG=#FAEDE1  CARD=#FFFEF2  DARK=#241404  BLUE=#7A94CC  BROWN=#96827D  WHITE=#FFFFFF
FONTS:   Headlines = "Playfair Display" Bold Italic  |  Body = "Noto Sans" Regular/Bold
SIZES:   H1=36px  H2=26px  H3=20px  Body=17px  Caption=14px
LOGO:    https://onecdn.io/media/2a83dc76-dc55-4d6b-a859-9b101375edbc/md2x
```

## Design Rules

**HTML/Email uses CREAM `#FAEDE1` background** (not white like DOCX).

**NEVER DO:**
- White page/body background in HTML (use `#FAEDE1`)
- Black (`#000000`) anywhere, use `#241404` instead
- Georgia or Arial as primary font name (CSS fallbacks only)
- Borders on tables or content boxes
- Skip Google Fonts import for web HTML

**ALWAYS DO:**
- Body background: `#FAEDE1`
- Content boxes: gradient `#FFFEF2` to `#FFFFFF` + `border-radius: 16px` + `box-shadow`
- Table headers: `#7A94CC` background + white text, Noto Sans Bold
- Table data rows: `#FFFEF2` background, no borders
- CTA buttons: `#7A94CC` background, white text, `border-radius: 8px`
- Footer: Noto Sans 14px in `#96827D`, centered
- Container max-width: 720px (web) or 600px (email)

## Web HTML Template

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StrongerYou</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,700&family=Noto+Sans:wght@400;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #FAEDE1; color: #241404; font-family: 'Noto Sans', Arial, sans-serif; font-size: 17px; line-height: 1.6; }
    .container { max-width: 720px; margin: 0 auto; padding: 40px 24px; }
    h1, h2 { font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-style: italic; color: #241404; }
    h1 { font-size: 36px; margin-bottom: 16px; }
    h2 { font-size: 26px; margin-bottom: 12px; }
    h3 { font-family: 'Noto Sans', Arial, sans-serif; font-weight: 700; color: #7A94CC; font-size: 20px; margin-bottom: 8px; }
    p { margin-bottom: 12px; }
    .caption { font-size: 14px; color: #96827D; }
    .content-box { background: linear-gradient(135deg, #FFFEF2, #FFFFFF); border-radius: 16px; padding: 24px 28px; margin: 20px 0; box-shadow: 0 3px 8px rgba(0,0,0,0.08); }
    .brand-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
    .brand-table th { background: #7A94CC; color: #FFFFFF; font-weight: 700; padding: 8px 12px; text-align: left; }
    .brand-table td { background: #FFFEF2; color: #241404; padding: 8px 12px; }
    .cta-button { display: inline-block; background: #7A94CC; color: #FFFFFF; font-weight: 700; padding: 14px 32px; border-radius: 8px; text-decoration: none; }
    .cta-button:hover { opacity: 0.9; }
    .divider { border: none; border-top: 1px solid #96827D; margin: 24px 0; }
    .footer { text-align: center; font-size: 14px; color: #96827D; padding: 24px 0; }
    .logo { display: block; width: 180px; height: auto; }
    .logo-center { margin: 0 auto 24px; }
    .logo-right { margin-left: auto; margin-bottom: 16px; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Content here -->
  </div>
</body>
</html>
```

## Component Examples

### Logo

```html
<!-- Centered (cover pages) -->
<img src="https://onecdn.io/media/2a83dc76-dc55-4d6b-a859-9b101375edbc/md2x"
     alt="Nicol Stanzel" class="logo logo-center">

<!-- Right-aligned (content pages) -->
<img src="https://onecdn.io/media/2a83dc76-dc55-4d6b-a859-9b101375edbc/md2x"
     alt="Nicol Stanzel" class="logo logo-right">
```

### Content Box

```html
<div class="content-box">
  <h3>Wichtig zu wissen</h3>
  <p>Content here.</p>
</div>
```

### Table

```html
<table class="brand-table">
  <thead><tr><th>Column 1</th><th>Column 2</th></tr></thead>
  <tbody>
    <tr><td>Data</td><td>Data</td></tr>
  </tbody>
</table>
```

### CTA Button + Footer

```html
<a href="#" class="cta-button">Jetzt starten</a>

<hr class="divider">
<div class="footer">StrongerYou X.0 | Nicol Stanzel | Lightness Fitness</div>
```

## Email-Specific Rules

When generating HTML emails, these additional constraints apply:

- **Inline all CSS** (no `<style>` blocks, email clients strip them)
- **Tables for layout** (not flexbox/grid)
- **Max width: 600px**
- **Font fallbacks mandatory:** Always `Arial, sans-serif` or `Georgia, serif`
- **No CSS custom properties** (email clients don't support them)
- **Background on `<td>`** not `<div>` (Outlook compatibility)
- **Logo min 180px width** for retina displays

### Email Skeleton

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>StrongerYou</title>
</head>
<body style="margin:0; padding:0; background-color:#FAEDE1; font-family:'Noto Sans',Arial,sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#FAEDE1;">
    <tr>
      <td align="center" style="padding:40px 16px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background-color:#FFFFFF; border-radius:16px; box-shadow:0 3px 8px rgba(0,0,0,0.08);">
          <!-- Header -->
          <tr>
            <td align="center" style="padding:32px 40px 16px;">
              <img src="https://onecdn.io/media/2a83dc76-dc55-4d6b-a859-9b101375edbc/md2x"
                   alt="Nicol Stanzel" width="180" style="display:block;">
            </td>
          </tr>
          <!-- Content -->
          <tr>
            <td style="padding:16px 40px 32px; color:#241404; font-family:'Noto Sans',Arial,sans-serif; font-size:17px; line-height:1.6;">
              <h1 style="font-family:'Playfair Display',Georgia,serif; font-weight:700; font-style:italic; color:#241404; font-size:32px; margin:0 0 16px;">
                Headline hier
              </h1>
              <p style="margin:0 0 12px;">Body text hier.</p>
              <!-- CTA -->
              <table role="presentation" cellpadding="0" cellspacing="0" style="margin:24px 0;">
                <tr>
                  <td style="background:#7A94CC; border-radius:8px; padding:14px 32px;">
                    <a href="#" style="color:#FFFFFF; font-family:'Noto Sans',Arial,sans-serif; font-weight:700; font-size:17px; text-decoration:none;">
                      Jetzt starten
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <!-- Footer -->
          <tr>
            <td style="padding:16px 40px 24px; border-top:1px solid #96827D;">
              <p style="font-family:'Noto Sans',Arial,sans-serif; font-size:14px; color:#96827D; text-align:center; margin:0;">
                Nicol Stanzel | Lightness Fitness
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
```
