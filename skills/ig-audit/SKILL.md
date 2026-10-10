---
name: ig-audit
description: >-
  Auswertung dessen, was der Nutzer schon gepostet hat: welche Reels wirklich
  funktioniert haben, warum, welche Anfragen sie gebracht haben und was er
  nicht mehr machen sollte. Für B2B: neben Reichweite auch Profilaufrufe,
  Link-Klicks, DMs und qualifizierte Gespräche. Verwenden, wenn der Nutzer
  Insights oder alte Posts einfügt und fragt "Auswertung", "was funktioniert",
  "warum ist das gefloppt", "lies meine Insights", "analysier meinen
  Content", "bringt uns Instagram Anfragen", oder wissen will, wovon er mehr
  machen soll.
---

# ig-audit

Die einzige ehrliche Quelle dafür, was bei einem Konto funktioniert, ist das
Konto selbst. Jede Regel in jedem Instagram-Ratgeber, auch die in diesem
Paket, ist eine Vorannahme. Die letzten 30 Posts des Nutzers sind der Beleg.

## Eingabe

Frag nach dem, was der Nutzer hat:

- Insights pro Post: Aufrufe, Reichweite, Interaktionen, Wiedergabedauer,
  Gespeichert, Geteilt, Follows und den Anteil der Reichweite bei
  Nicht-Followern. Screenshots reichen.
- Oder die Zuschauerbindungskurve des besten und des schlechtesten Reels der
  letzten Wochen. Dieser eine Screenshot ist mehr wert als alles andere
  zusammen.
- Oder nur die Posts mit ihren Aufrufen. Für einen ersten Durchgang reicht
  das.

Für B2B zusätzlich, soweit vorhanden:

- **Profilaktivität pro Post**: Profilaufrufe und Taps auf den Link im Profil
  bzw. externe Links.
- **DMs und Anfragen pro Post**: Keyword-DMs, Anfragen mit Bezug auf ein Reel,
  Antworten auf "Wie sind Sie auf uns aufmerksam geworden?".
- **Qualifizierte Gespräche aus dem CRM**: Termine, Angebote, Ausschreibungen
  mit Quelle Instagram. Zahlen pro Post oder Monat reichen, Namen und
  Kontaktdaten braucht das Audit nicht.

Diese Werte **nie raten und nie aus Aufrufen hochrechnen**. Was der Nutzer
nicht liefert, bleibt leer und wird in der Ausgabe als fehlend markiert.

Lies außerdem `~/.claude/instagram/log.md`, falls vorhanden. Dort steht,
welche Hook-Formel jeder Post verwendet hat.

## Was wirklich gemessen wird

Aufrufe sind die am wenigsten nützliche Zahl auf der Seite, weil sie vor allem
davon abhängen, wie viele Leute dem Konto schon folgen. Berechne stattdessen
diese Werte und zeig den Rechenweg:

| Kennzahl | Berechnung | was sie zeigt |
| --- | --- | --- |
| **Outlier-Multiplikator** | Aufrufe / Median-Aufrufe des Kontos | ob das ein echter Treffer war oder ein normaler Tag |
| **Nicht-Follower-Reichweite** | % der Reichweite von Leuten, die nicht folgen | ob es überhaupt gewandert ist |
| **Halterate nach 3 s** | Zuschauer nach 3 s / Zuschauer, die gestartet haben | ob der Hook funktioniert hat. Das ist die Note für den Hook. |
| **Durchschnittliche Wiedergabedauer** | direkt aus den Insights | ob die Mitte funktioniert hat |
| **Sends pro Reichweite** | Geteilt / Reichweite | das stärkste Einzelsignal, das man sich verdienen kann. Wer teilt, setzt seinen Namen darunter. Im B2B oft: an Kollegen oder den Chef weitergeleitet. |
| **Follows pro Reichweite** | Follows / Reichweite | ob das Profil die Aufmerksamkeit umgewandelt hat |
| **Profilaufrufe pro Reichweite** | Profilaufrufe / Reichweite | ob jemand wissen wollte, wer dahintersteckt |
| **Link-Klicks** | Taps auf Links / Profilaufrufe | ob das Profil einen nächsten Schritt anbietet, den jemand nimmt |
| **Anfragen pro Post** | DMs mit echtem Anliegen, gezählt vom Nutzer | ob der Post Gespräche bringt |
| **Qualifizierte Gespräche** | aus dem CRM, nur wenn geliefert | ob daraus Geschäft werden kann |

Sortiere nach Outlier-Multiplikator und Sends pro Reichweite, nicht nach
Aufrufen. Ein Reel mit 2.000 Aufrufen und 60 Sends hat das mit 40.000
Aufrufen und 11 Sends geschlagen.

Liegen Anfragen oder CRM-Zahlen vor, sind sie das Urteil und die anderen
Kennzahlen die Erklärung. Ein Reel mit 3.000 Aufrufen und zwei Anfragen von
Geschäftsführern schlägt eines mit 80.000 und keiner. Aber: Anfragen sind
seltene Ereignisse. Zwei Anfragen auf einem Post sind ein Hinweis, kein
Muster. Zähl sie über alle Posts zusammen, gruppiert nach Formel und Thema.

## Dann das Muster finden

Leg die Top 5 und die Bottom 5 nebeneinander, such, was sie trennt, und sei
bereit, etwas zu folgern, das dem Nutzer nicht gefällt:

- **Halterate nach 3 Sekunden.** Unterscheiden sich Top und Bottom hier, liegt
  es am Hook und an nichts anderem. Alles danach ist Ablenkung.
- **Hook-Formel.** Welche IDs aus `ig-reel/hooks.json` stehen in den Top 5?
- **Format.** Reel, Karussell, Einzelbild.
- **Länge.** In Gruppen: unter 15 s, 15–30 s, 30–60 s, über 60 s.
- **Thema.**
- **Publikum.** Kam die Reichweite von möglichen Kunden oder von Kollegen aus
  der eigenen Branche? Branchenwitze holen oft Reichweite bei der Konkurrenz
  und keine einzige Anfrage. Hinweise darauf: wer kommentiert, wer folgt.
- **Ob der Nutzer in der ersten Stunde auf Kommentare geantwortet hat.**
- **Wochentag und Uhrzeit.** Das **zuletzt** prüfen und nur, wenn alles
  andere nichts zeigt. Es ist fast nie die Ursache, und genau dort wollen die
  Leute sie finden.

Formulier den Befund als Aussage mit dem Beleg daneben und sag, wie sicher er
ist. Mit 30 Posts sieht man ein Muster. Mit 6 nicht, und das zu sagen ist
besser, als eines zu erfinden.

## Die Unterscheidung, die Monate spart

**Ein Reel mit Aufrufen und ohne Follows ist kein gescheitertes Reel, sondern
ein Profilproblem.** Ein Reel ohne Aufrufe ist ein Hook-Problem. Trenn die
beiden, bevor du irgendetwas empfiehlst. Ist die Nicht-Follower-Reichweite
hoch und Follows pro Reichweite niedrig, hör auf, Hooks umzuschreiben, und geh
zu `/ig-profile`.

Im B2B gibt es eine dritte Stufe: **Profilaufrufe, aber keine Link-Klicks und
keine Anfragen** heißt, das Profil sagt nicht, was der nächste Schritt ist.
Auch das ist ein Fall für `/ig-profile`, nicht für neue Hooks.

## Ausgabe

```
AUDIT  ·  31 Posts  ·  12.06.–05.09.  ·  Median-Aufrufe 1.900

TOP 5 NACH OUTLIER-MULTIPLIKATOR
                                  Aufrufe  Nicht-F.  Halt 3s  Sends  Profil  Links  Anfr.
  18,2x  #3  Sagt dir keiner       34.600     62 %     71 %     128     210     14     1
   6,4x  #1  Kostenbeichte         12.200     48 %     64 %      71     340     31     4
   5,1x  #25 Kundenergebnis         9.700     41 %     60 %      44     290     27     3
  ...

BOTTOM 5
   0,3x  #11 Liste mit Favorit        600      9 %     31 %       2      12      0     0
  ...

WAS DIE DATEN SAGEN
1. Die Halterate nach 3 Sekunden erklärt die Reichweite. Top 5 im Schnitt 66 %,
   Bottom 5 33 %. Alles andere hängt an den ersten zwei Sekunden.
2. Anfragen kommen von anderen Posts als die Reichweite. 8 von 11 Anfragen
   stammen aus Kostenbeichte und Kundenergebnis, mit echten Zahlen aus
   Kundenprojekten. Das Reel mit der höchsten Reichweite brachte eine.
   n=31, Tendenz deutlich, aber 11 Anfragen sind wenig.
3. Tool-Listen holen Reichweite und sonst nichts. Keine Sends, keine
   Profilaufrufe. Drei der Bottom 5.
4. CRM (vom Nutzer geliefert): 2 qualifizierte Gespräche im Zeitraum, beide
   nach Kostenbeichte-Reels. Zu wenig für eine Regel, passt aber zu Punkt 2.
5. Der Wochentag zeigt nichts. Dienstag und Freitag liegen im Rauschen.
   Nicht weiter optimieren.

FEHLT: Link-Klicks für Juni, DMs vor dem 01.07. nicht gezählt.

STOPP: Tool-Listen.
MEHR DAVON: Posts mit echten Kosten und einer Zahl dazu.
```

Gib die Schlüsse dann an `/ig-plan` weiter, damit die nächste Woche auf den
eigenen Belegen des Nutzers aufbaut statt auf Standardwerten, und an
`/ig-viral`, damit das Swipe-File auf die Formeln gefiltert wird, die bei
genau diesem Konto funktionieren.
