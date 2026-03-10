#!/usr/bin/env node
/**
 * Prozessfaktor Provisionsabrechnung - DOCX Generator v4
 * Exakt nach Original-DOCX-Vorlage (extrahierte XML-Werte)
 *
 * Farben aus Vorlage:
 *   Tabellen-Borders: #96827D (braun), Tabellen-Header: #7A94CC
 *   Zeilen alternierend: #FFFFFF / #FAEDE1
 *   Highlight-Box: #FAEDE1 fill, borderless
 *   Formel-Box: #FFFFFF fill, #7A94CC border 2pt
 *   Provisionsbetrag: Playfair 48hp #241404 (dunkelbraun!)
 */
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, Footer, Header, AlignmentType, BorderStyle, WidthType,
        ShadingType, VerticalAlign } = require('docx');
const fs = require('fs');
const path = require('path');

function parseArgs() {
  const args = {};
  const argv = process.argv.slice(2);
  for (let i = 0; i < argv.length; i += 2)
    args[argv[i].replace(/^--/, '').replace(/-/g, '_')] = argv[i + 1];
  return args;
}

const a = parseArgs();
const monat = a.monat || 'MONAT';
const zeitraum = a.zeitraum || '';
const brutto = parseFloat(a.brutto || 0);
const stripeFees = parseFloat(a.stripe_fees || 0);
const refunds = parseFloat(a.refunds || 0);
const anzahlCharges = a.anzahl_charges || '?';
const anzahlRefunds = a.anzahl_refunds || '?';
const tripwireBrutto = parseFloat(a.tripwire_brutto || 0);
const tripwireFees = parseFloat(a.tripwire_fees || 0);
const tripwireNetto = parseFloat(a.tripwire_netto || 0);
const anzahlTripwire = a.anzahl_tripwire || '?';
const outputPath = a.output || `/tmp/Abrechnung-Prozessfaktor-${monat.replace(/ /g, '-')}.docx`;

const nettoNachFees = brutto - stripeFees;
const nettoNachRefunds = nettoNachFees - refunds;
const basisProvision = nettoNachRefunds - tripwireNetto;
const provision = Math.round(basisProvision * 0.15 * 100) / 100;

let detailRows = [];
if (a.detail_json && fs.existsSync(a.detail_json))
  detailRows = JSON.parse(fs.readFileSync(a.detail_json, 'utf8'));

function eur(n) { return n.toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' \u20AC'; }
function eurNeg(n) { return '\u2212' + Math.abs(n).toLocaleString('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' \u20AC'; }

// Brand (exact from template DOCX XML)
const B = {
  FH: "Playfair Display", FB: "Noto Sans",
  DK: "241404", BL: "7A94CC", BR: "96827D", WH: "FFFFFF", CR: "FAEDE1"
};
const NB = { style: BorderStyle.NONE, size: 0 };
const NO_BORDERS = { top: NB, bottom: NB, left: NB, right: NB };
const TBL_BORDER = { style: BorderStyle.SINGLE, size: 1, color: B.BR };
const TBL_BORDERS = { top: TBL_BORDER, bottom: TBL_BORDER, left: TBL_BORDER, right: TBL_BORDER };
const FORMULA_BORDER = { style: BorderStyle.SINGLE, size: 2, color: B.BL };
const FORMULA_BORDERS = { top: FORMULA_BORDER, bottom: FORMULA_BORDER, left: FORMULA_BORDER, right: FORMULA_BORDER };

const syLogoPath = path.join(process.env.HOME, 'Desktop/Area/Marketing/brand-design/assets/logos/strongeryou-logo-dark.png');
const syLogoData = fs.existsSync(syLogoPath) ? fs.readFileSync(syLogoPath) : null;

function spacer(pts) { return new Paragraph({ spacing: { before: pts || 200 } }); }

// Exact sizes from template
function h1Center(t) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 100, after: 60 },
    children: [new TextRun({ text: t, font: B.FH, size: 56, bold: true, italics: true, color: B.DK })] });
}
function h2Center(t) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 20, after: 200 },
    children: [new TextRun({ text: t, font: B.FH, size: 40, bold: true, italics: true, color: B.BL })] });
}
function sectionHead(t) {
  return new Paragraph({ spacing: { before: 300, after: 100 },
    children: [new TextRun({ text: t, font: B.FH, size: 36, bold: true, italics: true, color: B.DK })] });
}
function subHead(t) {
  return new Paragraph({ spacing: { before: 200, after: 80 },
    children: [new TextRun({ text: t, font: B.FH, size: 22, bold: true, italics: true, color: B.BL })] });
}
function bodyText(t) {
  return new Paragraph({ spacing: { after: 80, line: 276 },
    children: [new TextRun({ text: t, font: B.FB, size: 22, color: B.DK })] });
}
function bodyMulti(runs) {
  return new Paragraph({ spacing: { after: 80, line: 276 },
    children: runs.map(r => new TextRun({ font: B.FB, size: 22, color: B.DK, ...r })) });
}
function captionText(t) {
  return new Paragraph({ spacing: { after: 40 },
    children: [new TextRun({ text: t, font: B.FB, size: 20, color: B.BR })] });
}

// Table: exact from template - brown borders, alternating white/cream, blue header+gesamt
function dataTable(headers, rows, colWidths, opts = {}) {
  const { blueLastRow = false } = opts;
  const headerRow = new TableRow({ children: headers.map((t, i) => new TableCell({
    width: { size: colWidths[i], type: WidthType.DXA }, borders: TBL_BORDERS,
    shading: { fill: B.BL, type: ShadingType.CLEAR },
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({
      alignment: i > 0 ? AlignmentType.RIGHT : AlignmentType.LEFT,
      children: [new TextRun({ text: t, font: B.FB, size: 20, bold: true, color: B.WH })]
    })]
  })) });

  const dataRows = rows.map((r, ri) => {
    const isLast = ri === rows.length - 1;
    const isBlue = blueLastRow && isLast;
    const bg = isBlue ? B.BL : (ri % 2 === 0 ? B.WH : B.CR);
    const tc = isBlue ? B.WH : B.DK;
    return new TableRow({ children: r.map((t, i) => new TableCell({
      width: { size: colWidths[i], type: WidthType.DXA }, borders: TBL_BORDERS,
      shading: { fill: bg, type: ShadingType.CLEAR },
      margins: { top: 60, bottom: 60, left: 120, right: 120 },
      verticalAlign: VerticalAlign.CENTER,
      children: [new Paragraph({
        alignment: i > 0 ? AlignmentType.RIGHT : AlignmentType.LEFT,
        children: [new TextRun({ text: t, font: B.FB, size: 20, bold: true, color: tc })]
      })]
    })) });
  });

  return new Table({
    width: { size: colWidths.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: colWidths, rows: [headerRow, ...dataRows]
  });
}

// Highlight box: cream fill, NO borders (from template Table 2 + Table 11)
function highlightBox(children) {
  return new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [9026],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: 9026, type: WidthType.DXA }, borders: NO_BORDERS,
      shading: { fill: B.CR, type: ShadingType.CLEAR },
      margins: { top: 200, bottom: 200, left: 300, right: 300 },
      children
    })] })] });
}

// Formula box: white fill, blue border 2pt (from template Table 5 + Table 9)
function formulaBox(children) {
  return new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [9026],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: 9026, type: WidthType.DXA }, borders: FORMULA_BORDERS,
      margins: { top: 160, bottom: 160, left: 300, right: 300 },
      children
    })] })] });
}

const today = new Date().toLocaleDateString('de-DE', { day: '2-digit', month: 'long', year: 'numeric' });
const headerText = `Provisionsabrechnung \u2013 ${monat}`;

// ===== TITLE PAGE =====
const titleChildren = [];

if (syLogoData) {
  titleChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 600, after: 400 },
    children: [new ImageRun({ data: syLogoData, transformation: { width: 200, height: 57 }, type: 'png' })] }));
}

titleChildren.push(h1Center("Provisionsabrechnung"));
titleChildren.push(h2Center(`Alle Stripe-Ums\u00e4tze (exkl. Tripwire)`));

titleChildren.push(new Table({ width: { size: 3400, type: WidthType.DXA }, columnWidths: [3400],
  alignment: AlignmentType.CENTER,
  rows: [new TableRow({ children: [new TableCell({
    width: { size: 3400, type: WidthType.DXA },
    borders: { top: NB, bottom: { style: BorderStyle.SINGLE, size: 3, color: B.BL }, left: NB, right: NB },
    children: [new Paragraph({ spacing: { after: 0 }, children: [] })]
  })] })] }));

titleChildren.push(spacer(300));
titleChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: "Abrechnungszeitraum", font: B.FB, size: 22, color: B.BR })] }));
titleChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 },
  children: [new TextRun({ text: monat, font: B.FB, size: 28, bold: true, color: B.DK })] }));

titleChildren.push(new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [4513, 4513],
  rows: [new TableRow({ children: [
    new TableCell({ width: { size: 4513, type: WidthType.DXA }, borders: NO_BORDERS,
      children: [
        new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Auftraggeber", font: B.FB, size: 18, color: B.BR })] }),
        new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: "Lightness Fitness", font: B.FB, size: 22, bold: true, color: B.DK })] }),
        new Paragraph({ children: [new TextRun({ text: "Nicol Stanzel", font: B.FB, size: 20, color: B.DK })] })
      ] }),
    new TableCell({ width: { size: 4513, type: WidthType.DXA }, borders: NO_BORDERS,
      children: [
        new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Auftragnehmer", font: B.FB, size: 18, color: B.BR })] }),
        new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: "Prozessfaktor", font: B.FB, size: 22, bold: true, color: B.DK })] }),
        new Paragraph({ children: [new TextRun({ text: "Ben Oesterreich", font: B.FB, size: 20, color: B.DK })] })
      ] })
  ] })] }));

titleChildren.push(spacer(400));
titleChildren.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
  children: [new TextRun({ text: `Grundlage: Joint-Venture-Vertrag \u2013 15 % Umsatzbeteiligung`, font: B.FB, size: 20, color: B.BR })] }));
titleChildren.push(new Paragraph({ alignment: AlignmentType.CENTER,
  children: [new TextRun({ text: `Erstellt am ${today}`, font: B.FB, size: 20, color: B.BR })] }));

// ===== CONTENT =====
const content = [];

content.push(sectionHead("Zusammenfassung"));

// Highlight box: cream fill, no borders, dark brown amount
content.push(highlightBox([
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: `Gesamtprovision (15 % der Nettoumsätze) \u2013 ${monat}`, font: B.FB, size: 22, color: B.BR })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: eur(provision), font: B.FH, size: 48, bold: true, italics: true, color: B.DK })] }),
]));
content.push(spacer(200));

content.push(bodyMulti([
  { text: `Gem\u00e4\u00df Joint-Venture-Vertrag erh\u00e4lt Prozessfaktor (Ben Oesterreich) eine Umsatzbeteiligung von ` },
  { text: `15 %`, bold: true },
  { text: ` auf die Nettoumsätze (nach Abzug der Stripe-Zahlungsgeb\u00fchren) aller Produkte, exkl. Happy Body Training (Tripwire).` }
]));
content.push(spacer(200));

// Main summary table: blue last row for "15% Provision"
content.push(dataTable(
  ["Position", "Betrag"],
  [
    [`Stripe-Umsatz brutto (${anzahlCharges} Transaktionen)`, eur(brutto)],
    ["Stripe-Zahlungsgeb\u00fchren", eurNeg(stripeFees)],
    ["Netto nach Geb\u00fchren", eur(nettoNachFees)],
    [`Refunds (${anzahlRefunds} Stk.)`, eurNeg(refunds)],
    ["Netto nach Refunds", eur(nettoNachRefunds)],
    [`Abzug: Tripwire Netto (${anzahlTripwire} Stk.)`, eurNeg(tripwireNetto)],
    ["Abrechnungsrelevanter Nettoumsatz", eur(basisProvision)],
    ["15 % Provision", eur(provision)],
  ],
  [5826, 3200],
  { blueLastRow: true }
));
content.push(spacer(200));

// Formula box: white fill, blue border
content.push(formulaBox([
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [
      new TextRun({ text: `Nettoumsatz ${monat}: `, font: B.FB, size: 22, color: B.BR }),
      new TextRun({ text: eur(basisProvision), font: B.FB, size: 22, bold: true, color: B.DK })
    ] }),
  new Paragraph({ alignment: AlignmentType.CENTER,
    children: [
      new TextRun({ text: `${eur(basisProvision)} \u00d7 15 % = `, font: B.FB, size: 22, color: B.DK }),
      new TextRun({ text: eur(provision), font: B.FH, size: 48, bold: true, italics: true, color: B.DK })
    ] }),
]));
content.push(spacer(300));

// Detail table
if (detailRows.length > 0) {
  content.push(sectionHead("Zusammensetzung Stripe-Umsatz"));
  content.push(subHead("Nach Produktkategorie (exkl. Tripwire)"));
  content.push(captionText("Brutto-Umsatz, Stripe-Geb\u00fchren und Nettobetrag pro Kategorie."));
  content.push(spacer(60));
  content.push(dataTable(
    ["Produkt", "Anz.", "Brutto", "Stripe-Geb.", "Netto"],
    detailRows.map(r => [r.kategorie, String(r.anzahl), r.brutto, r.stripe_fees, r.netto]),
    [3200, 700, 1600, 1400, 1600],
    { blueLastRow: false }
  ));
  content.push(spacer(200));
}

// Final highlight box
content.push(highlightBox([
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 },
    children: [new TextRun({ text: `Abrechnungsbetrag Prozessfaktor \u2013 ${monat}`, font: B.FB, size: 22, color: B.BR })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 40 },
    children: [new TextRun({ text: eur(provision), font: B.FH, size: 48, bold: true, italics: true, color: B.DK })] }),
]));
content.push(spacer(300));

content.push(bodyMulti([
  { text: "Berechnungsmethodik: ", bold: true },
  { text: "Von jedem Kundenumsatz (Bruttobetrag) werden zun\u00e4chst die Stripe-Zahlungsgeb\u00fchren abgezogen. Happy Body Training (Tripwire, 27 \u20AC) wird als Ad-Budget-Beitrag komplett ausgenommen. Auf den verbleibenden Nettobetrag werden 15 % Provision berechnet. Alle Geb\u00fchren stammen direkt aus den Stripe-Balance-Transaktionen." }
]));
content.push(spacer(100));
content.push(captionText(`Datenquelle: Stripe Dashboard, Konto acct_1Qgvx6GKl7aVHCCr. Zeitraum ${zeitraum}.`));
content.push(captionText(`Erstellt am ${today}.`));
content.push(spacer(100));
content.push(new Paragraph({ spacing: { after: 40 },
  children: [new TextRun({ text: "Bei Fragen zu dieser Abrechnung wende dich bitte an nicol@lightnessfitness.de.", font: B.FB, size: 20, color: B.BR, italics: true })] }));

// ===== DOCUMENT =====
const footer = [new Paragraph({
  children: [new TextRun({ text: "\u00A9 Lightness Fitness", font: B.FB, size: 15, color: B.BR })]
})];

const doc = new Document({
  styles: { default: { document: { run: { font: B.FB, size: 22, color: B.DK } } } },
  sections: [
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1200, left: 1440 } },
        titlePage: true
      },
      headers: {
        default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: headerText, font: B.FB, size: 14, color: B.BR })] })] }),
        first: new Header({ children: [] })
      },
      footers: { default: new Footer({ children: footer }), first: new Footer({ children: [] }) },
      children: titleChildren
    },
    {
      properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1200, left: 1440 } }
      },
      headers: {
        default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: headerText, font: B.FB, size: 14, color: B.BR })] })] })
      },
      footers: { default: new Footer({ children: footer }) },
      children: content
    }
  ]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(outputPath, buf);
  console.log(`OK: ${outputPath}`);
}).catch(err => {
  console.error('FEHLER:', err.message);
  process.exit(1);
});
