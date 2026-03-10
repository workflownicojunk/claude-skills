# PPTX Template for StrongerYou Brand

## Brand Constants (self-contained)

```
COLORS:  BG=#FAEDE1  BOX=#FFFEF2  DARK=#241404  BLUE=#7A94CC  BROWN=#96827D  WHITE=#FFFFFF
FONTS:   Headlines = "Playfair Display" Bold Italic  |  Body = "Noto Sans" Regular/Bold
SIZES:   H1=52-80pt  H2=24-32pt  H3=18-24pt  Body=13-18pt  Caption=9-12pt
SLIDE:   16:9 (13.333" x 7.5")  |  720pt x 405pt (html2pptx)
```

## Design Rules

**PROVEN FORMULA:** Cream `#FAEDE1` background + white `#FFFEF2` content cards + blue `#7A94CC` as text/line accents only.

**NEVER DO:**
- Blue (`#7A94CC`) as full slide background
- Large blue areas (sidebars, panels, full-width bars)
- Black (`#000000`) anywhere - use `#241404` instead
- Georgia or Arial as primary font name

**ALWAYS DO:**
- White content boxes: ROUNDED corners + shadow + NO border
- Shadow on ALL white boxes: `box-shadow: 0 3pt 8pt rgba(0,0,0,0.06)` (CSS) or `blur=6pt dist=3pt opacity=15%` (python-pptx)
- Playfair Display: Bold AND Italic together
- Blue accent: thin lines, text color, small bars, borders only

## Slide Template Types (html2pptx)

When using the html2pptx workflow, use these proven templates:

### CSS Base (copy into every script)

```javascript
const BG='#FAEDE1', BOX='#FFFEF2', DK='#241404', BL='#7A94CC', BR='#96827D', WH='#FFFFFF';
const FH="'Playfair Display',Georgia,serif", FB="'Noto Sans',Arial,sans-serif";

const CSS = `
html{background:${BG}}
body{width:720pt;height:405pt;margin:0;padding:0;background:${BG};font-family:${FB};
     display:flex;flex-direction:column;overflow:hidden}
h1{font-family:${FH};font-weight:700;font-style:italic;color:${DK};margin:0}
h2{font-family:${FH};font-weight:700;font-style:italic;color:${DK};margin:0}
h3{font-family:${FB};font-weight:700;color:${BL};margin:0;font-size:9pt;
   letter-spacing:2pt;text-transform:uppercase}
p{color:${DK};font-size:14pt;line-height:1.5;margin:0 0 6pt}
`;
```

### White Content Card (most common element)

```html
<div style="background:#FFFEF2;border-radius:16pt;box-shadow:0 3pt 8pt rgba(0,0,0,0.06);
            padding:22pt 28pt;display:flex;flex-direction:column;justify-content:center">
  <p>Content here - MUST be in p/h1-h6 tags, never bare text in div</p>
</div>
```

### Blue Accent Bar (for emphasis slides)

```html
<div style="display:flex;flex:1">
  <div style="width:4pt;background:#7A94CC;border-radius:2pt"></div>
  <div style="flex:1;background:#FFFEF2;border-radius:0 16pt 16pt 0;
              box-shadow:0 3pt 8pt rgba(0,0,0,0.06);padding:22pt 28pt">
    <p>Content with blue accent bar</p>
  </div>
</div>
```

### Two-Column Comparison

```html
<div style="display:flex;gap:16pt;flex:1">
  <div style="flex:1;background:#FFFEF2;border-radius:16pt;
              box-shadow:0 3pt 8pt rgba(0,0,0,0.06);padding:18pt 22pt">
    <h3>LEFT TITLE</h3>
    <p>Left content</p>
  </div>
  <div style="flex:1;background:#FFFEF2;border-radius:16pt;
              box-shadow:0 3pt 8pt rgba(0,0,0,0.06);padding:18pt 22pt">
    <h3>RIGHT TITLE</h3>
    <p>Right content</p>
  </div>
</div>
```

### Breathing Slide (dramatic centered text, no card)

```html
<div style="flex:1;display:flex;flex-direction:column;align-items:center;
            justify-content:center;padding:44pt 72pt">
  <h1 style="font-size:34pt;text-align:center;line-height:1.3">Big statement here</h1>
  <div style="width:44pt;height:2pt;background:#7A94CC;margin:20pt 0"></div>
  <p style="font-size:11pt;color:#96827D;text-align:center">Supporting text</p>
</div>
```

### Quote Slide

```html
<div style="background:#FFFEF2;border-radius:16pt;box-shadow:0 3pt 8pt rgba(0,0,0,0.06);
            padding:28pt 36pt;display:flex;flex-direction:column;align-items:center">
  <p style="font-family:'Playfair Display',Georgia,serif;font-size:52pt;color:#7A94CC;
            margin:0;line-height:0.7;opacity:0.5">&bdquo;</p>
  <p style="font-family:'Playfair Display',Georgia,serif;font-style:italic;font-size:16pt;
            text-align:center;line-height:1.5;margin:6pt 8pt 16pt">Quote text here</p>
  <div style="width:32pt;height:2pt;background:#7A94CC"></div>
  <p style="font-size:11pt;color:#96827D;text-align:center;margin-top:10pt"><b>Author</b></p>
</div>
```

### CTA Button

```html
<div style="background:#7A94CC;border-radius:8pt;padding:10pt 44pt;margin-top:18pt">
  <p style="color:#FFFFFF;font-size:13pt;font-weight:700;text-align:center;margin:0">Button text</p>
</div>
```

## Spacing Guidelines

- Slide padding: 34-52pt sides, 34-44pt top/bottom
- Card padding: 18-28pt
- Between headline and card: 12-16pt
- Between cards (dual layout): 16pt gap
- Minimum distance from bottom edge: 0.5" (36pt)
- Body font in cards: 13-15pt (NOT 18-24pt - cards need denser text)

## python-pptx Alternative

For direct python-pptx generation (without html2pptx):

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

# Colors
DARK = RGBColor(0x24, 0x14, 0x04)
BLUE = RGBColor(0x7A, 0x94, 0xCC)
BROWN = RGBColor(0x96, 0x82, 0x7D)
CREAM = RGBColor(0xFA, 0xED, 0xE1)
CARD = RGBColor(0xFF, 0xFE, 0xF2)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

def add_shadow(shape):
    spPr = shape._element.spPr
    el = etree.SubElement(spPr, qn('a:effectLst'))
    sh = etree.SubElement(el, qn('a:outerShdw'))
    sh.set('blurRad', '76200'); sh.set('dist', '38100')
    sh.set('dir', '5400000'); sh.set('algn', 'tl'); sh.set('rotWithShape', '0')
    c = etree.SubElement(sh, qn('a:srgbClr')); c.set('val', '000000')
    a = etree.SubElement(c, qn('a:alpha')); a.set('val', '15000')

def branded_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = CREAM
    return slide

def content_box(slide, left, top, w, h):
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    box.fill.solid(); box.fill.fore_color.rgb = CARD
    box.line.fill.background()
    add_shadow(box)
    return box
```
