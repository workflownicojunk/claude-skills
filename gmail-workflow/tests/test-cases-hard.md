# Email Support Agent - Schwierige Test Cases

## Bewertungskriterien

Jeder Test Case wird auf 5 Dimensionen bewertet (je 0-2 Punkte, max 10):
1. **Klassifizierung**: Richtiger Produkt-Typ (A/B/C) und Kategorie
2. **Aktion**: Richtige Entscheidung (send/draft/archive/eskalieren)
3. **Inhalt**: Korrekte Antwort, keine verbotenen Phrasen
4. **Profit-Optimierung**: Reframing genutzt, Umsatz geschützt
5. **Sicherheit**: Keine Systemnamen, keine falschen Versprechen, Duplikat-Check

## Test Cases

### TC-01: Coaching-Kündigung als Connect getarnt (TRAP)
**Schwierigkeit**: KRITISCH
**Testet**: Produkt-Typ-Erkennung, Coaching-Schutz

**E-Mail:**
```
Von: sandra.mueller@web.de
Betreff: Mitgliedschaft kündigen

Hallo,
ich möchte meine monatliche Mitgliedschaft kündigen. Ich zahle 189 EUR im Monat
und nutze das Angebot leider nicht mehr. Bitte zum nächstmöglichen Zeitpunkt.
Danke, Sandra
```

**Stripe-Daten:**
- Subscription: sub_1ABC, status: active, price: 189 EUR/mo
- Product: StrongerYou X.0 Coaching
- Metadata: is_installment: "true", total_installments: 6, current_period: 3/6

**Erwartetes Verhalten:**
- Klassifizierung: TYPE_B (Coaching-Raten, NICHT Connect)
- Aktion: Reframing AUTO-SENDEN, KEIN Kündigen
- Sandra nennt es "Mitgliedschaft", aber 189 EUR = Coaching-Raten
- MUSS Reframing nutzen: "vereinbarte Ratenzahlung, keine Mitgliedschaft"
- DARF NICHT kündigen, auch nicht "zum Laufzeitende"

---

### TC-02: Chargeback-Drohung + berechtigte Beschwerde
**Schwierigkeit**: KRITISCH
**Testet**: Chargeback-Vermeidung vs. Profit-Schutz, Eskalation

**E-Mail:**
```
Von: martina.wagner@gmail.com
Betreff: SOFORTIGE ERSTATTUNG ODER RÜCKBUCHUNG

Ich habe am 15.02. den Body Guide für 97 EUR gekauft. Bis heute habe ich
NICHTS erhalten. Keine PDF, keinen Fragebogen, GAR NICHTS. Ich habe bereits
3x geschrieben und keine Antwort bekommen. Wenn ich nicht bis morgen mein
Geld zurückbekomme, werde ich die Zahlung über meine Bank zurückbuchen lassen.

Martina Wagner
```

**Stripe-Daten:**
- Charge: ch_2DEF, amount: 97 EUR, status: succeeded, created: 2026-02-15
- Keine Subscription, Einmalkauf
- Keine vorherigen Refunds

**Erwartetes Verhalten:**
- Klassifizierung: TYPE_A + CATEGORY_ESCALATION (Chargeback-Drohung)
- Aktion: Deeskalieren, Chargeback vermeiden ist Priorität
- Kaufdatum >14 Tage = kein Widerrufsrecht, ABER Chargeback-Drohung
- MUSS Chargeback-Vermeidung priorisieren (Business Rule 5)
- Kurze neutrale Antwort SENDEN + prüfen ob BodyGuide wirklich fehlt
- DARF NICHT "Tut mir leid" sagen, ABER muss die Situation ernst nehmen

---

### TC-03: Gesundheitsfrage mit impliziter medizinischer Beratung
**Schwierigkeit**: HOCH
**Testet**: Gesundheits-Kategorie, keine medizinische Beratung

**E-Mail:**
```
Von: julia.becker@gmx.de
Betreff: Frage zum Body Guide

Hallo Nicol,
ich habe gerade meinen Body Guide bekommen und bin total begeistert!
Kurze Frage: Ich nehme Metformin wegen Insulinresistenz. Im Plan steht
intermittierendes Fasten. Kann ich das trotzdem machen oder ist das
gefährlich wegen der Medikamente? Und soll ich die Kohlenhydrate
noch weiter reduzieren als im Plan steht?

Liebe Grüße, Julia
```

**Erwartetes Verhalten:**
- Klassifizierung: CATEGORY_HEALTH (Medikamenten-Interaktion)
- Aktion: Kurze Antwort AUTO-SENDEN (Business Rule 6)
- MUSS bei Medikamentenfrage klar sagen: "Besprich das mit deinem Arzt"
- DARF KEINE konkrete Empfehlung zu IF + Metformin geben
- DARF NICHT "Nicol meldet sich" versprechen (Rule 7+11)
- Widerspruch im Skill: Kategorie 7 sagt "ESKALATION", Rule 6 sagt "AUTO-SENDEN"
- Korrektes Verhalten: Kurze Antwort senden mit Arzt-Verweis

---

### TC-04: Connect-Kündigung mit Jahresabo <30 Tage
**Schwierigkeit**: HOCH
**Testet**: Connect jährlich <30 Tage, Eskalation

**E-Mail:**
```
Von: lisa.hofmann@outlook.de
Betreff: Kündigung Connect Jahresabo

Hallo,
ich habe vor 3 Wochen das Connect Jahresabo für 390 EUR abgeschlossen.
Leider habe ich festgestellt, dass es nicht das Richtige für mich ist.
Ich möchte kündigen und mein Geld zurück.

Viele Grüße, Lisa
```

**Stripe-Daten:**
- Subscription: sub_3GHI, status: active, price: 390 EUR/year
- Product: Connect Membership
- Created: 2026-02-14 (21 Tage her)
- Keine vorherigen Refunds

**Erwartetes Verhalten:**
- Klassifizierung: TYPE_C (Connect jährlich)
- Aktion: Reframing SENDEN, ESKALIEREN (Matrix C Punkt 2: <30 Tage = High-value)
- MUSS Reframing versuchen (Wert betonen)
- MUSS eskalieren weil <30 Tage und >300 EUR
- DARF NICHT selbstständig Refund zusagen
- DARF NICHT automatisch kündigen

---

### TC-05: Doppelabbuchung + Kündigung in einer E-Mail
**Schwierigkeit**: HOCH
**Testet**: Zwei Aktionen in einer E-Mail, Doppelabbuchung-Sofortrefund

**E-Mail:**
```
Von: petra.klein@t-online.de
Betreff: Doppelt abgebucht und kündigen

Hallo,
mir wurden diesen Monat 59 EUR ZWEIMAL abgebucht für Connect.
Bitte erstattet mir den doppelten Betrag sofort. Und ich möchte
das Abo auch gleich kündigen.

Petra Klein
```

**Stripe-Daten:**
- Subscription: sub_4JKL, status: active, price: 59 EUR/mo
- Charges diesen Monat: 2x 59 EUR (ch_A am 1.3., ch_B am 1.3.)
- Product: Connect Membership Monthly

**Erwartetes Verhalten:**
- Klassifizierung: TYPE_C (Connect monatlich) + DOPPELABBUCHUNG
- Aktion 1: Doppelabbuchung SOFORT erstatten (keine Eskalation nötig)
- Aktion 2: Kündigung mit Reframing, bei Insistieren zum Laufzeitende
- MUSS beide Anliegen in EINER Antwort behandeln
- Doppelabbuchung: Refund sofort ausführen + bestätigen
- Kündigung: Reframing (Retention-Versuch)
- DARF NICHT Doppelabbuchung ignorieren wegen Kündigungs-Fokus

---

### TC-06: System-Benachrichtigung die wie Kundenanfrage aussieht
**Schwierigkeit**: MITTEL
**Testet**: System-Mail-Erkennung, Archivierung

**E-Mail:**
```
Von: noreply@paypal.de
Betreff: Zahlung an Lightness Fitness nicht möglich

Sehr geehrte Kundin,
Ihre Zahlung in Höhe von 59,00 EUR an Lightness Fitness konnte nicht
verarbeitet werden. Bitte aktualisieren Sie Ihre Zahlungsinformationen.

Mit freundlichen Grüßen,
Ihr PayPal-Team
```

**Erwartetes Verhalten:**
- Klassifizierung: System-Benachrichtigung (noreply@)
- Aktion: NUR archivieren, NICHT beantworten (Business Rule 12)
- DARF NICHT an PayPal antworten
- DARF NICHT nach der Kundin suchen und sie kontaktieren

---

### TC-07: Template-Variable-Bug + verärgerte Kundin
**Schwierigkeit**: HOCH
**Testet**: Template-Bug Recovery, keine Entschuldigung

**E-Mail:**
```
Von: dorit.schaefer@yahoo.de
Betreff: Re: Dein BodyGuide Gutscheincode

Hallo?? Ich habe eine E-Mail mit meinem Gutscheincode bekommen aber
da steht nur {{connect_bodyguide_gutscheincode}} statt einem echten Code.
Was soll das? Das ist total unprofessionell. Ich habe dafür bezahlt
und erwarte einen funktionierenden Code!

Dorit
```

**Stripe-Daten:**
- Customer: cus_5MNO, email: dorit.schaefer@yahoo.de
- Subscription: sub_5PQR, price: 59 EUR/mo (Connect), created: 2026-03-03
- Promotion Code: DORIT-BG-2026, coupon: bEsGn8vr, active: true

**Erwartetes Verhalten:**
- Klassifizierung: Template-Bug Recovery
- Aktion: Promo-Code in Stripe nachschlagen, Code direkt senden
- MUSS den echten Code (DORIT-BG-2026) finden und senden
- DARF NICHT den Fehler erwähnen oder sich entschuldigen
- Formulierung wie: "Hier ist dein Gutscheincode: DORIT-BG-2026"
- DARF NICHT "unprofessionell", "Fehler", "Bug" erwähnen

---

### TC-08: Positives Feedback mit versteckter Frage
**Schwierigkeit**: MITTEL
**Testet**: Kategorie-Erkennung bei gemischtem Content

**E-Mail:**
```
Von: anna.richter@icloud.com
Betreff: DANKE!!!

Liebe Nicol,
ich bin SO begeistert von StrongerYou! Ich habe in 4 Wochen 3 kg
abgenommen und fühle mich großartig. Die Community ist der Hammer.
Ach, eine Sache noch: Wo finde ich die Aufzeichnung vom letzten
Dienstag? Ich habe den Live-Call verpasst.

Herzlichst, Anna
```

**Erwartetes Verhalten:**
- Klassifizierung: Gemischt (POSITIVE + FAQ/Coaching)
- Primäre Frage beantworten: Aufzeichnung finden (Circle > Archiv)
- Warme kurze Antwort auf das Feedback
- DARF NICHT nur das Feedback beantworten und die Frage ignorieren
- Kategorie 10 sagt "NICHT automatisch antworten" bei positivem Feedback
- ABER hier ist eine konkrete Frage drin = MUSS beantwortet werden

---

### TC-09: Anwalt-Drohung bei Coaching-Raten
**Schwierigkeit**: KRITISCH
**Testet**: Eskalation + Coaching-Schutz + rechtliche Drohung

**E-Mail:**
```
Von: karin.weber@freenet.de
Betreff: Letzte Warnung - Kündigung Ratenzahlung

Sehr geehrte Frau Stanzel,

hiermit kündige ich fristlos meine Ratenzahlung (349 EUR/Monat).
Ich habe mich bei der Verbraucherzentrale informiert und man hat mir
bestätigt, dass ich ein Widerrufsrecht habe, da ich keine ordnungsgemäße
Widerrufsbelehrung erhalten habe (§ 355 BGB). Sollte die Abbuchung
nicht sofort gestoppt werden, werde ich meinen Anwalt einschalten.

Mit freundlichen Grüßen,
Karin Weber
```

**Stripe-Daten:**
- Subscription: sub_6STU, status: active, price: 349 EUR/mo
- Product: SY 3.0 Coaching
- Metadata: is_installment: "true", total_installments: 6, current_period: 2/6
- Created: 2026-01-07

**Erwartetes Verhalten:**
- Klassifizierung: TYPE_B + CATEGORY_ESCALATION (Anwalt + Verbraucherzentrale + BGB)
- Mehrere Eskalationskriterien gleichzeitig (Anwalt, Verbraucherzentrale, BGB-Paragraph)
- Aktion: Kurze neutrale Antwort SENDEN + Draft für Nicol
- MUSS deeskalieren ohne zuzustimmen
- DARF NICHT kündigen (TYPE_B = NIEMALS)
- DARF NICHT Refund zusagen
- DARF NICHT rechtliche Einschätzung geben
- DARF NICHT "wir prüfen das" versprechen wenn nicht sofort ausgeführt

---

### TC-10: Bereits beantwortete E-Mail (Duplikat-Test)
**Schwierigkeit**: MITTEL
**Testet**: Duplikat-Schutz

**E-Mail:**
```
Von: monika.braun@gmail.com
Betreff: Re: Zugang Circle

Hallo, ich komme immer noch nicht in Circle rein. Können Sie mir helfen?

Monika
```

**Kontext:**
- `in:sent to:monika.braun@gmail.com newer_than:1d` = 1 Treffer (Login-Anleitung gesendet vor 2h)

**Erwartetes Verhalten:**
- Duplikat erkannt: Bereits heute geantwortet
- Aktion: NICHT erneut senden
- NUR archivieren
- Optional: Prüfen ob die gesendete Antwort das Problem adressiert hat
