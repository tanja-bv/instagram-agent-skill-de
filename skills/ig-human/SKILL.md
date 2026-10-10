---
name: ig-human
description: >-
  Entfernt den Maschinen-Fingerabdruck aus jedem deutschen Entwurf:
  Geviertstriche, KI-Deutsch und Werbedeutsch, unsichtbare Zeichen, du/Sie-Mix,
  und bewertet ihn mit fünf Prüfungen, bevor er rausgeht. Nutzen, wann immer
  Text menschlich klingen soll, bei "klingt das nach KI", "humanisieren",
  "klingt wie ChatGPT", "mach das weniger werblich", "Floskeln raus", "Striche
  raus", und vor jeder Caption, jedem Skript, Kommentar, jeder Antwort oder DM,
  die dem Nutzer gezeigt wird.
---

# ig-human

Zwei Werkzeuge liegen in diesem Ordner, und beide laufen wirklich. Nutz sie.
Schätz das nicht nach Gefühl.

```bash
python3 humanize.py entwurf.txt --report       # bereinigen, Änderungen zeigen
python3 detect.py entwurf.txt                   # bewerten, fünf Prüfungen
python3 detect.py vorher.txt nachher.txt        # den Unterschied belegen
```

Beide lesen `slop.json`: rund 150 Floskeln in den Familien einstiege, schluss,
konnektoren, adjektive, substantive, verben, werbedeutsch und instagram, 18
Klassen unsichtbarer Zeichen, 12 typografische Ersetzungen und 23
Struktur-Muster. Die Datei ist zum Bearbeiten da. Benutzt der Nutzer ein Wort
bewusst, das das Lexikon meldet ("effizient" bei einer Software, die nun mal
schneller ist), nimm es raus.

## Warum das auf Instagram mehr zählt, als es aussieht

Captions sind kurz, und Skripte werden laut gesagt. Eine geschrieben klingende
Zeile ist in einer 600-Zeichen-Caption ein größerer Anteil als derselbe Satz in
einem Fachartikel, und ein Voiceover, das keiner natürlich sagen kann, hört man
beim ersten Take. Das Problem ist nicht ein Detektor, der den Post markiert. Das
Problem ist ein Geschäftsführer, der an etwas vorbeiscrollt, das nach Prospekt
klingt, oder ein Inhaber, der über sein eigenes Skript stolpert.

## Was automatisch korrigiert wird

**1. Unsichtbare Zeichen.** Nullbreiten-Leerzeichen und -Verbinder,
Wortverbinder, weiche Trennzeichen, Byte-Order-Marks, Unicode-Tag-Zeichen,
unsichtbare Trenner, geschützte und schmale Leerzeichen. Eine Tastatur erzeugt
sie nicht. Sie überleben Copy-Paste, sind in jedem Editor unsichtbar und das
mechanischste Merkmal in generiertem Text. `humanize.py` löscht jedes davon,
auch jedes weitere Unicode-Formatzeichen, für das es keinen Namen hat.

**2. Typografie.** Geviertstrich zu Komma, Gedankenstrich " – " zu " - " (so
tippt man ihn), Bereich "5–10" zu "5-10", Auslassungspunkte zu drei Punkten,
Aufzählungspunkt zu Bindestrich. Anführungszeichen: Standard ist gerade,
weil Handys meistens so tippen. Mit `--anfuehrung deutsch` bleiben deutsche
„…“ stehen, und nur englische “…” werden zu „…“. Deutsche Anführung ist kein
Fingerabdruck. Englische Anführung in einem deutschen Text schon.

**3. Das Floskel-Lexikon, mit Rücksicht auf die Wortstellung.** Deutsch stellt
das Verb an Position zwei. Wer in "Zweifellos ist das wichtig" das erste Wort
löscht, bekommt "Ist das wichtig", also eine Frage. Darum wird nur ersetzt, wo
der Ersatz dieselbe Satzposition füllt:

- "zweifellos" wird "sicher", "darüber hinaus" wird "außerdem",
  "letztendlich" wird "am Ende", "In der heutigen schnelllebigen Welt" wird
  "heute".
- Adjektive übernehmen die Endung: "nahtlose Integration" wird "reibungslose
  Integration", "maßgeschneiderten Lösungen" wird "passenden Lösungen".
- Ganze Füllsätze werden gelöscht, wenn sie allein stehen: "Tauchen wir ein!",
  "Hallo zusammen!", "Folgen Sie uns für mehr!", "Wir freuen uns auf Ihre
  Anfrage!". "Zögern Sie nicht, uns zu kontaktieren" wird "Melden Sie sich".

Großschreibung bleibt erhalten, URLs bleiben unberührt.

## Was NICHT automatisch korrigiert wird

**Floskeln, bei denen der Ersatz Artikel, Kasus oder Konjugation mitzieht,**
werden gemeldet, mit Vorschlag, im Abschnitt "FLOSKELN ZU PRÜFEN": Mehrwert,
Gamechanger, Synergien, "ermöglicht es Ihnen", "das volle Potenzial
ausschöpfen", "Ihr zuverlässiger Partner", "Qualität steht bei uns an erster
Stelle", professionell, kompetent, individuell. Das Werbedeutsch der B2B-Welt
steht fast vollständig hier, weil man es nicht austauschen kann. Man muss den
Satz neu bauen und einen Beleg statt des Adjektivs hinschreiben.

**Struktur-Muster** werden gemeldet, nicht umgeschrieben, weil die Form eines
Satzes zu ändern Urteilsvermögen braucht:

- "Nicht nur X, sondern auch Y" (das KI-Deutsch-Muster schlechthin)
- "Hier kommt X ins Spiel" und "Genau hier setzt X an"
- "Egal, ob X oder Y" und "Es geht nicht um X, es geht um Y"
- Dreierreihen "X, Y und Z."
- Rhetorische Ein-Zeilen-Fragen: "Das Ergebnis?"
- Video-Vorlauf: "In diesem Video zeige ich euch"
- "Wir freuen uns" und "Wir sind stolz"
- Emoji-Aufzählungen, drei Wörter in Großbuchstaben, Hashtag-Wände
- Gedankenstrich-Häufung
- Reflex-Köder: "Folge für mehr", "Markiere jemanden", "Was meint ihr?"
- **du und Sie im selben Text**

Diese Liste ist deine Aufgabe. Schreib jede gemeldete Zeile von Hand um, mit
derselben Aussage, und lass dann `detect.py` noch einmal laufen. Genau das
bewegt den Score von PRÜFEN zu BESTANDEN, und genau das kann kein Skript.

## Die fünf Prüfungen

`detect.py` bewertet fünf Signale mit 0-100, höher ist menschlicher:

| Prüfung | was sie misst | so sieht Maschine aus |
| --- | --- | --- |
| SATZRHYTHMUS | Variation der Satzlänge | jeder Satz gleich lang |
| KONKRETHEIT | Zahlen, Abkürzungen, Marken, Orte, Monate pro 100 Wörter | abstrakte Begriffe, keine Zahlen |
| FLOSKELDICHTE | Lexikon-Treffer pro 100 Wörter | Standardvokabular |
| FINGERABDRUCK | unsichtbare Zeichen, Geviertstriche, englische Anführung, gehäufte Gedankenstriche pro 1.000 Zeichen | typografisch perfekt |
| STIMME | Abtönungspartikeln und Kurzformen ("halt", "mal", "gibt's"), Personalpronomen, Struktur-Muster | keine Partikeln, inszenierte Enthüllungen |

Konkretheit zählt keine großgeschriebenen Wörter wie im englischen Original,
weil im Deutschen jedes Substantiv groß ist. Und: Ein formeller Sie-Text an
Geschäftsführer hat naturgemäß weniger Partikeln. Das ist kein Grund, ein
"halt" in eine Erstkontakt-DM zu stopfen. Die Stimme soll zur `voice.md`
passen, nicht zum Score.

Das Urteil gewichtet den Mittelwert mit 60 % und die **schwächste einzelne
Prüfung** mit 40 %, weil ein Signal reicht. BESTANDEN braucht 70+ insgesamt
und keine Prüfung unter 55.

## Sag das ehrlich

Das sind fünf lokale Heuristiken nach den Signalen, auf die öffentliche
Detektoren schauen. Sie laufen komplett auf dem Rechner des Nutzers, nichts
wird hochgeladen. Sie sind **nicht** GPTZero, Originality, Copyleaks, Winston
oder Turnitin, sie rufen deren APIs nicht auf und können deren Urteil nicht
versprechen. Wer behebt, was sie messen, bewegt meistens auch deren Zahlen,
weil sie dasselbe messen. Das ist die Behauptung. Mach keine größere im Namen
des Nutzers, und sag nie, ein Text sei "nicht erkennbar".

Die deutsche Fassung ist neu kalibriert und noch nicht an einem großen Korpus
deutscher Texte gemessen. Der Durchgang für unsichtbare Zeichen ist echt und
eng: Er entfernt Format-Zeichen, die in generiertem Text landen und Copy-Paste
überleben. Er behauptet nicht, ein kryptografisches Wasserzeichen zu brechen.

## Reihenfolge

1. `humanize.py entwurf.txt -o sauber.txt --report`
2. "FLOSKELN ZU PRÜFEN" und "STRUKTUR-MUSTER" lesen. Diese Zeilen selbst umschreiben.
3. `detect.py entwurf.txt sauber.txt`, um vorher und nachher zu zeigen.
4. Ist das Urteil nicht BESTANDEN, die schwächste Prüfung aus der Ausgabe
   beheben und noch einmal. Zwei Runden sind normal. Fünf heißen, der Entwurf
   wurde nach Schema geschrieben, und die Lösung ist ein anderer Entwurf, nicht
   mehr Durchgänge.
5. Dem Nutzer den bereinigten Text und den Score zeigen. Nie den Score allein.

So sieht ein absichtlich schlechter Entwurf vor und nach dem automatischen
Durchgang aus, bevor die gemeldeten Stellen umgeschrieben sind:

```
HUMANIZE-BERICHT
15 Maschinen-Artefakte entfernt, 5 Floskeln zu prüfen, 6 Struktur-Muster zum Umschreiben

3. FLOSKELN ERSETZT
    1x  In der heutigen schnelllebigen Welt  -> heute   [einstiege]
    1x  zweifellos  -> sicher   [konnektoren]
    1x  nahtlos  -> reibungslos   [adjektive]
    ...
4. FLOSKELN ZU PRÜFEN  (nicht ersetzt - Satz umbauen)
    1x  Gamechanger   [substantive]
        Sag, was sich ändert, mit Zahl.
    ...

  18,8 AUFFÄLLIG  ->  26,6 AUFFÄLLIG   (+7,8)
```

Der automatische Teil bringt wenig Punkte, weil der Rest am Satzbau hängt. Die
Punkte kommen beim Umschreiben.
