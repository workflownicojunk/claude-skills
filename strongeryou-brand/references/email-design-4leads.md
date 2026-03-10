# 4leads E-Mail Design-Patterns

Extrahiert aus den Live-E-Mails im 4leads-Account (92 E-Mails, Stand 03/2026).

## E-Mail-Typen und Namenskonvention

4leads nutzt eine klare Namenskonvention:
- `NL [Nr] [Segment] | [MM-YYYY] | [Zielgruppe] | [Betreff]` (Newsletter)
- `Connect [Typ] FU [Nr] | [Thema]` (Follow-Up Sequenzen)
- `Connect Kauf | Auto | [Thema]` (Automatisierte Transaktionsmails)

### Segmente
- **Connect** = StrongerYou Coaching-Mitglieder
- **BodyGuide** = BodyGuide-Käufer
- **STY X.o Kauf** = StrongerYou X.0 Käufer

## E-Mail-Layout (Standard)

Die E-Mails sind bewusst schlicht gehalten. Sie sollen wirken wie eine persönliche Nachricht von Nicol, nicht wie ein Marketing-Newsletter.

### Header
- Nicol Stanzel Signatur-Logo (links, kleiner als auf der Website)
- Daneben: "Nicol Stanzel" + "DEIN HAPPY BODY IMPULS" (Subline)
- Rundes Profilbild von Nicol (kreisförmig ausgeschnitten)

### Body
- **Anrede:** "Hey {{firstname}}," (persönlich, immer mit Vorname)
- **Hintergrund:** Weiß (NICHT Cream wie die Website)
- **Schrift:** Serifenlos, schlicht (vermutlich System-Font oder Lato)
- **Formatierung:** Minimal. Fettdruck für Emphasis, keine Farb-Akzente
- **Absätze:** Kurz, conversational. Jeder Satz fast ein eigener Absatz.
- **Emojis:** Sparsam, in Betreffzeilen (z.B. "🎁"), selten im Body

### Stil-Regeln
- Kein aufwändiges HTML-Layout
- Keine farbigen Boxen oder Karten
- Keine großen Header-Bilder
- Maximal 1 CTA-Link pro E-Mail (als Text-Link, kein Button)
- Persönlicher, warmer Ton. Als ob Nicol eine SMS schreibt.
- Fettdruck für: wichtige Termine, Deadlines, Handlungsaufforderungen
- Kursiv: selten, für Betonungen

### Footer
- Minimalistisch
- Abmelde-Link (rechtlich erforderlich)
- Kein StrongerYou-Logo im Footer (anders als Website)

## Betreffzeilen-Muster

Nicols Betreffzeilen folgen bestimmten Patterns:
- **Persönlich + Vorname:** "{{firstname}}, willkommen bei Connect!"
- **Dringlichkeit:** "[Wichtig] Dein nächster Schritt..."
- **Neugier:** "Ich hätte sowas nicht für möglich gehalten..."
- **Story:** "Unser letzter Call gestern... und ein sehr ehrliches Wort an dich"
- **Direkt:** "Du hast es geschafft. Und jetzt?"
- **Emoji:** Sparsam, max. 1 pro Betreff (🎁 am häufigsten)

## Automatisierte E-Mails vs. Newsletter

### Automatisiert (Transaktional)
- Noch schlichter als Newsletter
- Klare Handlungsanweisung (z.B. "Hier ist dein Gutscheincode")
- Kurz (3-5 Sätze)

### Newsletter
- Länger, storytelling-basiert
- Persönliche Anekdoten von Nicol
- Leichte Urgency am Ende
- Oft referenziert auf aktuelle Events (Calls, Community-Momente)

## Follow-Up Sequenzen

Typisches 3er Follow-Up Pattern:
1. **FU 1:** Gratulation + Ausblick ("Du hast es geschafft. Und jetzt?")
2. **FU 2:** Social Proof + Story ("Was Claudia nach dem Coaching anders macht")
3. **FU 3:** Scarcity + Deadline ("Morgen schließt sich das Fenster")

## Personalisierung

- `{{firstname}}` — Vorname (in Anrede und Betreff)
- `{{field_15306}}` — Custom Field (z.B. Gutscheincode)
- Keine komplexen Conditional Blocks sichtbar

## Design-Empfehlung für neue E-Mails

Wenn neue E-Mails für StrongerYou erstellt werden:
1. **Schlicht halten.** Kein aufwändiges Design. Text-fokussiert.
2. **Header:** Logo + Nicol-Foto (rund) + Subline
3. **Ton:** Warm, persönlich, direkt. Nicols Stimme.
4. **Max 1 CTA** pro E-Mail
5. **Absätze:** Kurz. Max 2-3 Sätze pro Absatz.
6. **Kein Marketing-Look.** Soll aussehen wie von einer Freundin.
