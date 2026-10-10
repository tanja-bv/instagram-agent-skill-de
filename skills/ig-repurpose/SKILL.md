---
name: ig-repurpose
description: >-
  Macht aus einem langen Inhalt eine Woche Reels und Karussells: Webinar,
  Fachartikel, Newsletter, Podcast, Messevortrag, Kundenprojekt (mit
  Freigabe), LinkedIn-Post, YouTube-Video oder Gesprächsnotiz. Verwenden, wenn
  der Nutzer sagt "Video umwandeln", "mach daraus Reels", "recyceln", "ich
  habe ein Webinar/einen Podcast/ein Transkript", "zerleg das", "aus dem
  Vortrag Content machen", oder etwas Langes einfügt und es auf Instagram
  haben will.
---

# ig-repurpose

Ein guter langer Inhalt steckt voller Posts, meist vier bis sechs. Die meisten
holen einen heraus und werfen den Rest weg.

## Eingabe

Ein Transkript, ein Fachartikel, ein Newsletter, ein Skript, eine
Gesprächsnotiz, die Aufzeichnung eines Webinars oder Messevortrags, ein
LinkedIn-Post, der dort gut lief. Gibt der Nutzer eine URL und hat diese
Sitzung ein Transkript-Werkzeug, nutz es; sonst lass ihn den Text einfügen.
Lies alles, bevor du irgendetwas herausziehst.

Ist die Quelle ein Video des Nutzers, frag auch nach der Datei. Ein Reel aus
seinem eigenen Material schlägt eines, in dem er seine eigenen Worte noch
einmal vorliest.

Zwei Prüfungen vor dem Start:

- **Kundenprojekt oder Kundenzitat:** Kundenname, Logo, Objekt und Zahlen nur
  mit schriftlicher Freigabe. Ohne Freigabe anonymisieren: Branche, Größe,
  Ergebnis ("Hausverwaltung, 40 Objekte in Graz, Reklamationen halbiert").
  Frag nach, bevor du schreibst, nicht danach.
- **Webinar oder Messevortrag mit Publikum:** Wer im Bild oder zu hören ist,
  braucht eine Einwilligung. Fragen aus dem Publikum lieber nachsprechen als
  den Ausschnitt zeigen.

## Herausziehen, nicht zusammenfassen

Eine Zusammenfassung eines Webinars ist kein Reel. Niemand will die
Zusammenfassung. Geh den Inhalt durch und zieh heraus, was für sich allein
steht:

| Fundstück | was es ist |
| --- | --- |
| **Thesen** | jeder Satz, über den jemand widersprechen würde |
| **Zahlen** | jede Zahl, jeder Betrag, jede Dauer, jeder Prozentwert |
| **Geschichten** | jeder Moment mit einer Person, einer Szene und einem Preis |
| **Mechanismen** | jedes "so funktioniert das wirklich" |
| **Fehler** | jedes Eingeständnis, dass etwas schiefging |
| **Sätze** | jeder Satz, der so wie er ist zitierfähig ist |

Ein B2B-Webinar ist meist voller Mechanismen und arm an Geschichten. Die
besten Stellen stecken oft in der Fragerunde am Ende, weil dort die echten
Einwände kommen. Lies sie nicht zuletzt.

Liste auf, was du gefunden hast, mit Anzahl, bevor du irgendetwas schreibst.
Ergibt der Inhalt weniger als vier Fundstücke, ist er dünn, und vier Posts
daraus werden auch dünn. Sag das.

## Dann das Format pro Fundstück wählen

Nicht alles ist ein Reel.

- **These, Fehler, Geschichte** werden ein Reel. Sie brauchen eine Stimme und
  ein Gesicht.
- **Mechanismus, nummerierte Liste** werden ein Karussell. Die will man noch
  einmal lesen, und im B2B werden sie gespeichert und an Kollegen
  weitergeleitet.
- **Ein zitierfähiger Satz** wird ein Story-Frame, kein Post.

Untertitel und Texteinblendungen sind bei jedem Reel Pflicht. Webinar-Material
hat oft schlechten Ton, und viele schauen im Büro ohnehin ohne.

## Dann die Woche bauen

Jedes Fundstück wird ein Post, und jeder Post steht komplett für sich. Der
Zuschauer hat die Quelle nicht gesehen und wird sie nie sehen. Schreib nie
"wie ich im letzten Webinar gesagt habe". Der Post ist das Produkt.

Ordne jedem Post eine Hook-Formel aus `ig-reel/hooks.json` zu und wechsle
sie. Fünf Posts aus einer Quelle mit derselben Hook-Form wirken wie aus der
Content-Fabrik, weil sie das sind.

Ist die Quelle ein Video des Nutzers, **nimm das echte Material**. Der
Ausschnitt, in dem er den Satz gesagt hat, mit der echten Reaktion darin,
schlägt jede Neuaufnahme. Schneide am Satz, nicht am Atem.

Ist die Quelle ein LinkedIn-Post, übernimm nicht den Text. Ein LinkedIn-Post
ist zum Lesen gebaut, ein Reel zum Sagen. Nimm die These und schreib sie neu.

Ordne die Woche so: die stärkste These zuerst, die Geschichte zur Wochenmitte,
der Mechanismus zuletzt, wenn die Leute, denen die ersten Posts gefallen
haben, darauf warten.

## Ausgabe

```
QUELLE: "Warum wir IT-Support nicht mehr nach Stunden abrechnen" (45-Min.-Webinar, 7.800 Wörter)

GEFUNDEN  5 Thesen, 9 Zahlen, 3 Geschichten, 4 Mechanismen, 2 Fehler, 7 zitierfähige Sätze

WOCHE
DI  REEL       #2  Klare Ansage       Kaufen Sie IT-Support nicht nach Stunden ein
                                      Ausschnitt bei 14:20 nehmen, er lacht am Ende
MI  KARUSSELL  Hook in der Caption    Die 4 Fragen, die das Erstgespräch ersetzt haben
FR  REEL       #21 Mitten im Satz     "...und neun Tage nach der Abnahme wollte er Geld zurück"
SO  REEL       #5  Zeitraffer         6 Stunden pro Woche zurück, ein Formular weniger

FREIGABE   Die Geschichte am FR nennt einen Kunden. Freigabe liegt nicht vor:
           anonymisiert als "Steuerkanzlei, 25 Arbeitsplätze".

Sag "schreib Dienstag", dann entwerfe ich ihn.
```

Entwirf dann auf Wunsch, einen nach dem anderen, jeweils über `/ig-reel` und
`/ig-human`. Kipp nicht vier fertige Skripte auf einmal aus. Sie klingen dann
alle gleich, und der Nutzer dreht keines davon.
