---
name: ig-profile
description: >-
  Ein Instagram-Firmenprofil mit einer 13-teiligen Rubrik auf 100 Punkte
  bewerten und die Teile umschreiben, die Punkte kosten: Impressum,
  Namensfeld, Bio, Link, Highlights, die drei angepinnten Beiträge, Grid.
  Nutzen, wenn der Nutzer sagt "Profil checken", "Profil optimieren", "bewerte
  mein Profil", "Bio verbessern", "Bio umschreiben", "was soll in die Bio",
  "Namensfeld", "Highlights benennen", "Impressum auf Instagram", "warum folgt
  mir keiner", "warum fragt keiner an", oder sein Profil einfügt und fragt, wie
  es wirkt.
---

# ig-profile

Fast alle optimieren hier das Falsche. Das Profil ist kein Schaufenster, durch
das jemand bummelt. Es ist ein **Entscheidungsbildschirm**. Jemand kommt über
ein einziges Reel und gibt dem Profil etwa drei Sekunden für eine Frage: Gibt
es hier mehr davon, und ist das für mich?

Im B2B heißt "für mich": für meinen Betrieb, meine Branche, meine Region. Ein
Geschäftsführer, der das in drei Sekunden nicht sieht, fragt nicht an.

## Eingabe

Bitte den Nutzer, einzufügen oder als Screenshot zu schicken: Namensfeld,
Handle, Bio, wohin der Link führt, die Namen der Highlights, was angepinnt ist,
und die ersten neun Cover im Grid. Frag dazu, wo das Impressum steht, und ob
das Unternehmen seinen Sitz in Deutschland, Österreich oder der Schweiz hat,
falls `~/.claude/instagram/voice.md` das nicht verrät. Ein Screenshot vom
oberen Profilteil plus die ersten zwei Grid-Reihen reicht für den ersten
Durchgang.

Logg dich nicht für den Nutzer bei Instagram ein. Auch nicht, wenn er darum
bittet.

## Bewerten

Lies `rubric.json` in diesem Ordner. Dreizehn Kriterien, 100 Punkte, zu jedem
steht, wie volle Punkte aussehen und woran es meistens scheitert. Bewerte jedes
Kriterium, zeig die Tabelle, nenn die Summe. Sei ehrlich. Die meisten
Firmenprofile landen beim ersten Durchgang in den 30ern und 40ern, und ein
großzügiger Score ist wertlos.

`impressum` ist als Pflichtpunkt markiert (`"required": true`). Kennzeichne es
in der Tabelle mit PFLICHT, sobald es nicht volle Punkte hat.

```
PROFIL-SCORE  38/100

  Impressum         0/6    PFLICHT. Bio-Link führt auf einen Linkbaum, kein Impressum
  Namensfeld        2/12   nur "Novak Facility GmbH", kein Wort, das jemand sucht
  Bio Zeile 1       3/12   "Ihr Partner für Sauberkeit" und ein Glitzer-Emoji
  Angepinnt         0/10   nichts angepinnt
  Highlights        2/8    "Allgemein", "Weihnachtsfeier", "2023"
  Grid              4/7    sechs von neun Covern ohne Text
  ...
```

## Dann umschreiben, in dieser Reihenfolge

Rechtliche Pflicht zuerst: Fehlt das Impressum oder ist es nicht erreichbar,
steht es auf Platz 1, auch wenn anderswo mehr Punkte verloren gehen. Danach
absteigend nach verlorenen Punkten. Schreib nicht alles auf einmal um, der
Nutzer muss jedes Feld selbst ändern.

Alle Texte in der Anrede aus `voice.md`. Fehlt sie, frag einmal; ohne Antwort
Sie. Die Bio ist die Stelle, an der du und Sie am häufigsten gemischt werden.

Erfinde keinen Proof. Steht in `voice.md` keine Zahl, schreib `{{Ihre Zahl}}`
bzw. `{{deine Zahl}}`. Kundennamen und Logos nur mit schriftlicher Freigabe,
sonst Branche, Größe, Ergebnis.

**1. Impressum (Pflicht).** Erreichbar mit höchstens zwei Klicks: Der Bio-Link
führt auf eine Seite mit "Impressum" im Footer, oder ein eigener Link heißt
genau so. Rechtsgrundlage nach Sitz: DE § 5 DDG, AT § 5 ECG und § 25 MedienG
(Offenlegung), CH weniger streng, Anbieterangaben trotzdem empfohlen. Schreib
keinen Impressumstext. Sag, wo es hingehört und welche Grundlage gilt, und dass
das keine Rechtsberatung ist; den Inhalt klärt der Nutzer mit Kammer, Verband
oder Anwalt.

**2. Das Namensfeld (30 Zeichen).** Die fette Zeile unter dem Foto, nicht der
Handle. Dieses Feld wertet die Instagram-Suche aus, und die meisten Firmenkonten
tragen dort nur den Firmennamen ein, gern mit Rechtsform. Format, das
funktioniert: `{Firma oder Person} | {Leistung, ggf. Region, in Suchbegriffen}`,
etwa "Novak | Gebäudereinigung Wien". Gib drei Optionen und zähl die Zeichen.

**3. Bio Zeile 1.** Für wen, und welches Ergebnis die bekommen. Keine
Berufsbezeichnung, keine Adjektive, keine Strich-Liste. "Dienstpläne für
Sicherheitsfirmen, die nicht mehr per WhatsApp laufen." Der Rest der 150
Zeichen trägt einen Proof (Kunden, Jahre, Branchen) oder ein konkretes Angebot
("Objekt-Check vor Ort, 30 Minuten").

**4. Die drei angepinnten.** Drei Plätze, drei Aufgaben: der stärkste Proof
(ein Projekt, ein Kundenergebnis), die klarste Erklärung des Angebots (was, für
wen, wie läuft es ab), die beste Vorstellung der Menschen dahinter. Das ist der
wirksamste Fix im ganzen Profil, und er dauert vier Tipps. Ein Grid ohne
Angepinntes zeigt, was zuletzt gepostet wurde, und das ist Glückssache.
Stellenanzeigen gehören ins Highlight "Jobs", nicht hierher, außer Recruiting
ist gerade das Hauptziel.

**5. Highlights.** Vier bis sechs, benannt nach den Fragen, die Käufer stellen:
Leistungen, Referenzen, Ablauf, Preise/FAQ, Team, Jobs. Nicht "Allgemein". Der
Rest wird gelöscht.

**6. Der Link.** Eine Zielseite, die hält, was die Bio verspricht: Demo buchen,
Termin vereinbaren, Anfrage stellen. Fünf Links sind erlaubt; zwei sind schon
ein Menü, und ein Menü konvertiert schlechter als eine Tür. Die Startseite der
Website ist keine Zielseite. Ein zweiter Link, der nur "Impressum" heißt, ist
in Ordnung.

**7. Grid-Cover.** Die ersten neun in Thumbnail-Größe. Reel-Cover werden
ausgewählt, nicht als erstes Frame belassen. Vier Wörter Text auf einem Cover
machen ein Grid auf einen Blick lesbar.

## Ausgabe

Die Score-Tabelle, dann die Umschreibungen als kopierfertige Blöcke in
Fix-Reihenfolge, jeder durch `/ig-human`. Am Ende neu bewerten und den
Unterschied ehrlich zeigen. Landet die Überarbeitung bei 84 und nicht bei 98,
sag 84, und sag, was der Rest braucht: meist ein Grid, eine Story-Routine und
einen angepinnten Beitrag, den es noch nicht gibt, oft ein freigegebenes
Referenzprojekt. Nichts davon ist eine Umschreibung.

Dieser Skill speichert nichts auf Instagram. Der Nutzer ändert jedes Feld
selbst.
