# DOCX Template for StrongerYou Brand

## Brand Constants (self-contained)

```
COLORS:  DARK=#241404  BLUE=#7A94CC  BROWN=#96827D  CARD=#FFFEF2  WHITE=#FFFFFF
FONTS:   Headlines = "Playfair Display" Bold Italic  |  Body = "Noto Sans" Regular/Bold
SIZES:   H1=28pt  H2=18pt  H3=14pt  Body=11pt  Caption=10pt  Footer=9pt
PAGE:    A4 (11906 x 16838 DXA)  |  Margins: 1440 DXA all sides
```

## Design Rules

**DOCX uses WHITE page background** (not cream like PPTX/HTML).

**NEVER DO:**
- Cream/beige page background (`#FAEDE1`) in DOCX
- Black (`#000000`) anywhere, use `#241404` instead
- Georgia or Arial as primary font name (fallbacks only)
- Borders on tables or content boxes
- Missing Italic on Playfair Display headlines

**ALWAYS DO:**
- Page background = WHITE `#FFFFFF`
- Table headers: `#7A94CC` background + white `#FFFFFF` text
- Table data rows: `#FFFEF2` background, no borders
- Content boxes: single-cell table with `#FFFEF2` shading, no borders
- H3 section titles: Noto Sans Bold in `#7A94CC`
- Footer: Noto Sans 9pt in `#96827D`, centered

## Library: docx-js (Node.js)

```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, Header, Footer, AlignmentType, LevelFormat,
        HeadingLevel, BorderStyle, WidthType, ShadingType,
        PageNumber, PageBreak } = require('docx');
const fs = require('fs');

// Brand Constants
const B = {
  FH: "Playfair Display", FB: "Noto Sans",
  DK: "241404", BL: "7A94CC", BR: "96827D", CW: "FFFEF2", WH: "FFFFFF",
  H1: 56, H2: 36, H3: 28, BD: 22, SM: 20, FT: 18  // half-points
};
```

## Document Setup

```javascript
function createDoc(sections) {
  return new Document({
    styles: {
      default: { document: { run: { font: B.FB, size: B.BD, color: B.DK } } },
      paragraphStyles: [
        { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: B.FH, size: B.H1, bold: true, italics: true, color: B.DK },
          paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
        { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: B.FH, size: B.H2, bold: true, italics: true, color: B.DK },
          paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
        { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
          run: { font: B.FB, size: B.H3, bold: true, color: B.BL },
          paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } }
      ]
    },
    numbering: { config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } }, run: { font: B.FB, size: B.BD } } }] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } }, run: { font: B.FB, size: B.BD } } }] }
    ]},
    sections
  });
}
```

## Helper Functions

```javascript
const NB = { style: BorderStyle.NONE, size: 0 };
const NO_BORDERS = { top: NB, bottom: NB, left: NB, right: NB };

// Paragraphs
function h1(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_1,
    children: [new TextRun({ text: t, font: B.FH, size: B.H1, bold: true, italics: true, color: B.DK })] });
}
function h2(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_2,
    children: [new TextRun({ text: t, font: B.FH, size: B.H2, bold: true, italics: true, color: B.DK })] });
}
function h3(t) {
  return new Paragraph({ heading: HeadingLevel.HEADING_3,
    children: [new TextRun({ text: t, font: B.FB, size: B.H3, bold: true, color: B.BL })] });
}
function body(t) {
  return new Paragraph({ spacing: { after: 120, line: 276 },
    children: [new TextRun({ text: t, font: B.FB, size: B.BD, color: B.DK })] });
}
function bodyBold(t) {
  return new Paragraph({ spacing: { after: 120, line: 276 },
    children: [new TextRun({ text: t, font: B.FB, size: B.BD, bold: true, color: B.DK })] });
}
function caption(t) {
  return new Paragraph({ spacing: { after: 80 },
    children: [new TextRun({ text: t, font: B.FB, size: B.SM, color: B.BR })] });
}
function quote(t) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 200 },
    indent: { left: 720, right: 720 },
    children: [new TextRun({ text: `\u201E${t}\u201C`, font: B.FH, size: B.BD, italics: true, color: B.BR })] });
}
function divider() {
  return new Paragraph({ spacing: { before: 120, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 1, color: B.BR } } });
}

// Branded Table
function table(headers, rows, colWidths) {
  const hRow = new TableRow({ children: headers.map((t, i) => new TableCell({
    width: { size: colWidths[i], type: WidthType.DXA }, borders: NO_BORDERS,
    shading: { fill: B.BL, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text: t, font: B.FB, size: B.BD, bold: true, color: B.WH })] })]
  })) });
  const dRows = rows.map(r => new TableRow({ children: r.map((t, i) => new TableCell({
    width: { size: colWidths[i], type: WidthType.DXA }, borders: NO_BORDERS,
    shading: { fill: B.CW, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({ children: [new TextRun({ text: t, font: B.FB, size: B.BD, color: B.DK })] })]
  })) }));
  return new Table({ width: { size: colWidths.reduce((a,b)=>a+b,0), type: WidthType.DXA }, columnWidths: colWidths, rows: [hRow, ...dRows] });
}

// Content Box (single-cell table with card shading)
function calloutBox(t) {
  return new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [9026],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: 9026, type: WidthType.DXA }, borders: NO_BORDERS,
      shading: { fill: B.CW, type: ShadingType.CLEAR },
      margins: { top: 120, bottom: 120, left: 200, right: 200 },
      children: [new Paragraph({ children: [new TextRun({ text: t, font: B.FB, size: B.BD, color: B.DK })] })]
    })] })]
  });
}

// Section with footer
function section(children, footerText) {
  const s = {
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children
  };
  if (footerText) {
    s.footers = { default: new Footer({ children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ text: footerText + "  |  Seite ", font: B.FB, size: B.FT, color: B.BR }),
        new TextRun({ children: [PageNumber.CURRENT], font: B.FB, size: B.FT, color: B.BR })
      ]
    })] }) };
  }
  return s;
}
```

## Formal Documents (Abrechnungen, Berichte)

Formelle Dokumente wie Provisionsabrechnungen verwenden abweichende Tabellen-Regeln:

**Tabellen in formellen Dokumenten:**
- Header: `#7A94CC` Hintergrund, weiße Schrift (identisch)
- Datenzeilen: Weißer Hintergrund, **dünne graue Rahmen** (`#BFBFBF`, 1pt)
- KEINE alternierenden Zeilenfarben
- Letzte Zeile (Gesamt): Noto Sans Bold
- Nettoumsatz-Spalte: fett

**Highlight-Box** (z.B. Provisionsbetrag):
- Hintergrund: `#D6DEF0` (hellblau)
- Rahmen: `#C4CEE8`, 1pt
- Betrag: Playfair Display Bold Italic, `#7A94CC`

**Formel-Box** (z.B. "X EUR x 15% = Y EUR"):
- Hintergrund: weiß
- Rahmen: `#BFBFBF`, 1pt (dünner grauer Rahmen)
- Ergebnis: Playfair Display Bold Italic, `#241404`

**Sektions-Headlines in formellen Dokumenten:**
- Playfair Display Bold Italic in `#241404` (dunkelbraun, NICHT blau)
- Sub-Headlines: Playfair Bold Italic in `#7A94CC` (blau)

**Header/Footer:**
- Header rechts: Dokumenttitel in `#96827D`, Noto Sans 7pt
- Footer links: "(C) Lightness Fitness" in `#96827D`

**Logo:** StrongerYou Wordmark (`assets/logos/strongeryou-logo-dark.png`), NICHT Nicol Stanzel Logo

Referenz-Implementierung: `~/.claude/skills/prozessfaktor-abrechnung/scripts/generate-abrechnung.js`

## Complete Example

```javascript
const doc = createDoc([
  // Cover page (no footer)
  section([
    new Paragraph({ spacing: { before: 2400 } }),
    divider(),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 400, after: 200 },
      children: [new TextRun({ text: "STRONGERYOU X.0", font: B.FH, size: 72, bold: true, italics: true, color: B.BL })] }),
    new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: "Dein Hormon-Workbook", font: B.FH, size: 48, bold: true, italics: true, color: B.DK })] }),
    divider(),
  ]),
  // Content page
  section([
    h1("Dein Hormon-Orchester"),
    body("Stell dir deine Hormone als Orchester vor."),
    table(["Hormon", "Rolle"], [
      ["Oestrogen & Progesteron", "Die Koerperformer"],
      ["Insulin", "Der Energiemacher"],
    ], [3000, 6026]),
    calloutBox("Mehr Cardio macht es SCHLIMMER: Cortisol steigt!"),
  ], "StrongerYou X.0 | Nicol Stanzel | Lightness Fitness")
]);

Packer.toBuffer(doc).then(buf => fs.writeFileSync("output.docx", buf));
```
