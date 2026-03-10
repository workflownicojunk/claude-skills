# Email-Kategorien: Antwort-Templates & Wissen

## Kategorie 1: Body Guide FAQ (35%)

**Was ist der Body Guide:** Personalisierter Ernährungsplan (KEIN Training!). Baustein-System (A-E). Basiert auf Typeform-Fragebogen. Lieferung als PDF, 24-72h nach Fragebogen.

**Kern-Wissen:**
- Plan ist fix für 6-12 Monate, keine laufenden Anpassungen
- Einkaufsliste gilt für EINEN Baustein, nicht alle
- Zutaten austauschbar (Protein gegen Protein, KH gegen KH)
- Würzen erlaubt (Kräuter, Gewürze, Zitrone, Salz in Maßen)
- BODY Guide = NUR Ernährung, Training ist separat (Circle/BodyCircle)

**Template: Body Guide fehlt (<72h)**
```
Hallo [NAME],

dein Fragebogen ist angekommen. Dein BODY Guide wird gerade individuell erstellt, das dauert in der Regel 24-72h.

Du bekommst eine E-Mail, sobald er fertig ist. Bitte schau auch im Spam-Ordner nach.

Herzliche Grüße
Nicol
```

**Template: Body Guide fehlt (>72h)**
```
Hallo [NAME],

dein Guide sollte bereits da sein. Bitte check deinen Spam-Ordner nach "StrongerYou" oder "Body Guide".

Falls nicht gefunden, melde dich nochmal.

Herzliche Grüße
Nicol
```

**Template: Zutatenaustausch**
```
Hallo [NAME],

du kannst Zutaten austauschen: Protein gegen Protein (Hähnchen, Fisch, Tofu, Eier), Kohlenhydrate gegen Kohlenhydrate (Reis, Kartoffeln, Quinoa), Gemüse gegen Gemüse. So bleibt das Makro-Verhältnis gleich.

Herzliche Grüße
Nicol
```

**Eskalation nötig bei:** Gesundheitliche Einschränkungen (Diabetes, Schwangerschaft), Guide >72h nicht erhalten, "Plan funktioniert nicht", >20 Unverträglichkeiten.

---

## Kategorie 2: Zugang/Login (25%)

**Hauptursache (80%):** E-Mail-Mismatch. Kunde zahlt mit E-Mail A (Stripe), versucht Login mit E-Mail B.

**Circle-Basics:**
- Web: login.circle.so/strongeryou
- App: "Circle Community" (iOS/Android)
- Tags steuern Zugang (automatisch via n8n/Stripe)
- Freischaltung dauert 5-30 Min nach Zahlung

**Template: E-Mail-Mismatch**
```
Hallo [NAME],

das häufigste Problem: Du nutzt eine andere E-Mail als die, mit der du bezahlt hast.

Quick Fix:
1. Schau in deine Stripe-Rechnung (letzte Bestätigungs-E-Mail)
2. Nutze DIESE E-Mail für den Circle-Login
3. Gehe zu: login.circle.so/strongeryou

Falls du die Rechnung nicht findest, schreib mir. Ich prüfe das in Stripe.

Herzliche Grüße
Nicol
```

**Template: App-Probleme**
```
Hallo [NAME],

App-Probleme löst du so:
1. App komplett schließen
2. App deinstallieren, Handy neu starten, App neu installieren

Alternative: Nutze die Browser-Version unter login.circle.so/strongeryou. Funktioniert immer.

Herzliche Grüße
Nicol
```

**Template: Einladung nicht erhalten**
```
Hallo [NAME],

die Einladung landet oft im Spam-Ordner. Suche nach "Circle" oder "StrongerYou".

Falls nicht gefunden: Gehe zu login.circle.so/strongeryou und klicke "Passwort vergessen". Nutze die E-Mail aus deiner Stripe-Rechnung.

Ich schicke dir jetzt auch eine frische Einladung.

Herzliche Grüße
Nicol
```

**Auto-Checks (Backend):** 1. Stripe: subscription.status=active? 2. Circle: Tags gesetzt? 3. Wenn Tags fehlen: n8n Workflow triggern.

---

## Kategorie 3: Kündigungen (15%)

Siehe `ref-refund-sop.md` für komplette SOP.

**Kurzfassung:**
- Connect monatlich: Reframing AUTO-SENDEN, bei Insistieren zum Laufzeitende kündigen
- Connect jährlich: Reframing AUTO-SENDEN, keine Erstattung, Laufzeitende
- Coaching-Raten (97/179/189/349): NIEMALS kündigen. Reframing AUTO-SENDEN. "Vereinbarte Ratenzahlung, keine Mitgliedschaft."
- Retention: Wert betonen, Nutzung aufzeigen, kreativ halten

---

## Kategorie 4: Widerrufe/Refunds (12%)

Siehe `ref-refund-sop.md` für komplette SOP.

**Kurzfassung:** Refund-Anfragen: Reframing AUTO-SENDEN. Doppelabbuchungen sofort erstatten. Kein Refund ohne Stripe-Verifizierung.

---

## Kategorie 5: Zahlungsprobleme (8%)

**Template: Einmalig vs. Abo Erklärung**
```
Hallo [NAME],

dein Produkt [PRODUKT] ist [EINMAL/RATEN/ABO]:

Einmalzahlung: Happy Body (27 EUR), Body Guide (97 EUR), X.0 (497 EUR)
Ratenzahlung: X.0 in 3/6 Raten, 3.0 in 6 Raten. Läuft automatisch aus.
Abo: Connect monatlich (39/59 EUR), jederzeit kündbar.

Herzliche Grüße
Nicol
```

**Doppelabbuchung:** Sofort-Refund via Stripe (keine Eskalation nötig).
**Zahlungsstatus:** Stripe API prüfen (SUCCEEDED/PENDING/FAILED).

---

## Kategorie 6: Fehlende Inhalte (7%)

**Template: Fragebogen fehlt**
```
Hallo [NAME],

hier ist dein Fragebogen-Link: [TYPEFORM-LINK]

So geht's: Ausfüllen (ca. 10 Min), dann bekommst du deinen BODY Guide in 24-48h per E-Mail.

Falls der Link nicht geht, check deinen Spam-Ordner nach "Typeform" oder "StrongerYou".

Herzliche Grüße
Nicol
```

**Body Guide nicht erhalten:** Prüfen ob Fragebogen ausgefüllt. Wenn ja und >48h: erneut senden + Spam-Hinweis. Wenn nein: Typeform-Link schicken.

---

## Kategorie 7: Gesundheit (6%)

**AUTO-SENDEN. Keine medizinische Beratung. Kein "meldet sich".**

**Template:**
```
Hallo [NAME],

bei Fragen zu Medikamenten oder speziellen gesundheitlichen Themen kann ich dir keine Empfehlung geben. Besprich das bitte mit deinem Arzt, der kennt deine Situation am besten.

Herzliche Grüße
Nicol
```

**VERBOTEN in Gesundheits-Antworten:**
- "meldet sich innerhalb von 24h" (leeres Versprechen, Rule 7)
- "verbinde dich mit Nicol" (Agent kann das nicht, Rule 11)
- "persönlich bei dir melden" (Agent kann das nicht, Rule 11)
- Konkrete Empfehlungen zu Medikamenten, Dosierungen, Fasten bei Krankheit

**ERLAUBT:**
- Allgemeine Tipps zu Ernährung (Zutaten austauschen, Portionsgrößen)
- Verweis auf Arzt bei Medikamenten-/Krankheitsfragen
- Verweis auf Live-Q&A (Di 18:00) für allgemeine Coaching-Fragen

Themen: Diabetes, Schilddrüse, Medikamente, Schwangerschaft, Stillzeit, Verdauungsbeschwerden, Schmerzen.

---

## Kategorie 8: Coaching-spezifisch (5%)

**Auto-Antwort OK:** Aufzeichnungen finden (Circle > Archiv), Material/Workbook Standort.
**Umleitung:** Individuelle Coaching-Fragen -> Live-Q&A (Di 18:00, Circle Space "StrongerYou X.0 Chat - Q&A").
**Eskalation:** Inhaltliche Coaching-Methodik, Übungsmodifikationen (gesundheitlich), Unzufriedenheit.

---

## Kategorie 9: Technische Probleme (4%)

**Standard-Troubleshooting:**
1. Browser wechseln (Chrome/Firefox/Safari)
2. Inkognito-Modus testen
3. App: Deinstallieren, Handy neu starten, neu installieren
4. Alternative: Browser-Version login.circle.so/strongeryou

**Eskalation:** Wiederholte Probleme nach Troubleshooting, kaputte Videos/Links.

---

## Kategorie 10: Positives Feedback (3%)

**AUTO-SENDEN. Warme kurze Antwort (2-3 Sätze).**

**Template:**
```
Hallo [NAME],

das freut mich riesig zu hören! Genau dafür mache ich das. Weiter so, du machst das großartig.

Herzliche Grüße
Nicol
```

**Wichtig bei gemischtem Content (Feedback + Frage):**
- Die Frage hat IMMER Vorrang. Frage beantworten + kurze warme Reaktion auf Feedback.
- NIEMALS nur das Feedback beantworten und die Frage ignorieren.
- Beispiel: "Toll, danke! Wo finde ich die Aufzeichnung?" → Aufzeichnungs-Info geben + kurzer Dank.
