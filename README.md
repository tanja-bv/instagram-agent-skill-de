# Instagram-Agent-Skill, deutsch und B2B

Dreizehn Claude-Skills, die einen Instagram-Account für ein B2B-Unternehmen im
DACH-Raum betreiben. Deutsche Fassung von
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill)
von Jake Schincariol. Kostenlos, MIT, kein Konto, kein API-Key, nichts zu verbinden.

Das ist keine Übersetzung, sondern ein Umbau. Die Skripte des Originals waren auf
Englisch gebaut und lieferten bei deutschem Text falsche Werte: Ein guter
deutscher Hook bekam kaum mehr Punkte als "Hallo zusammen", und der Humanizer
fand in "nicht nur ein Tool, sondern ein echter Gamechanger" null Floskeln.
Jetzt messen sie Deutsch:

- **Silben statt Wörter.** "Arbeitszeiterfassung" ist ein Wort und sechs Silben.
  Sprechzeit, Hook-Länge und Beat-Sheet rechnen mit Silben, Zahlen werden
  gezählt, wie man sie sagt.
- **Konkret heißt nicht großgeschrieben.** Im Deutschen ist jedes Substantiv
  groß. Konkret sind Zahlen, Zahlwörter, Euro-Beträge, Abkürzungen (DSGVO, KV),
  Marken (WhatsApp), Monate und Orte im DACH-Raum.
- **du oder Sie, nie beides.** Jedes Skript erkennt den Mix, den häufigsten
  Fehler deutscher B2B-Texte.
- **KI-Deutsch und Werbedeutsch.** "Hier kommt X ins Spiel", "Genau hier setzt
  X an", "Ihr zuverlässiger Partner", "Qualität steht bei uns an erster Stelle".
- **Verbzweitstellung.** Der Humanizer ersetzt nur, wo die Wortstellung richtig
  bleibt ("Zweifellos ist das wichtig" wird "Sicher ist das wichtig", nicht
  "Ist das wichtig"), und meldet den Rest.

Dazu B2B: Ziel sind Gespräche, nicht Reichweite. Kundennamen und Zahlen nur mit
Freigabe. Impressum im Profil. Keine werbenden Kalt-DMs (UWG/TKG). Untertitel
Pflicht, weil im Büro ohne Ton geschaut wird.

**Nichts wird gepostet, bevor du Ja sagst.** Diese Skills schreiben. Du postest.

## Installieren

In Claude Code:

```bash
git clone <URL dieses Repos> instagram-agent-skill-de
cp -r instagram-agent-skill-de/skills/ig-* ~/.claude/skills/
```

Oder als Plugin, aus dem lokalen Ordner:

```
/plugin marketplace add ./instagram-agent-skill-de
/plugin install instagram-agent-de
```

Nur für ein Projekt: dieselben Ordner nach `.claude/skills/` im Repo kopieren.
Kein Claude Code? Eine einzelne `SKILL.md` oben in einen Chat einfügen, dann
läuft sie als Modus. Die fünf Python-Werkzeuge fehlen dann, und die sind bei
`/ig-reel` und `/ig-human` der halbe Wert.

Das englische Original und dieser Fork benutzen dieselben Befehlsnamen
(`/ig-reel` usw.). Installier nur eins von beiden.

Dann zehn Minuten in `templates/voice.md` stecken. Nach
`~/.claude/instagram/voice.md` kopieren und ausfüllen, oder Claude drei eigene
Reels schicken und sagen "schreib meine voice.md daraus". Jeder Skill liest die
Datei, auch die Anrede.

## Die dreizehn

| Befehl | was er macht |
| --- | --- |
| `/ig-reel` | Eine Idee wird ein Reel. Drei Hooks aus [26 Formeln](skills/ig-reel/hooks.json), bewertet, dann Skript, Bildschirmtext und Beat-Sheet nach Silben. |
| `/ig-viral` | Findet, was in der Branche läuft, rankt nach Vielfachem über dem Median des Kontos, benennt die Formel, schreibt das Swipe-File. Auch für englische Vorbild-Konten. |
| `/ig-caption` | Die Caption, geprüft. Zeigt die 125 Zeichen vor dem "... mehr", prüft du/Sie, CTA, Hashtags, Suchbegriffe. |
| `/ig-carousel` | Karussells: Cover, Folientext, 1080x1350-Dateien, mit Umlaut- und Komposita-Check. |
| `/ig-story` | Die tägliche Story-Sequenz, welcher Sticker welchen Job hat, und der DM-Funnel, bei dem der andere zuerst schreibt. |
| `/ig-profile` | Bewertet das Profil nach einer [Rubrik mit 13 Punkten](skills/ig-profile/rubric.json) auf 100, inklusive Impressum, und schreibt es in Fix-Reihenfolge neu. |
| `/ig-plan` | Die Woche: was, welches Format, wann, und welche Kunden, Partner und Verbände du kommentierst. |
| `/ig-human` | Der Humanizer für KI-Deutsch. Zwei Skripte, die wirklich laufen. |
| `/ig-comment` | Kommentare unter fremden Posts. Neun Typen, ohne Pitch, Anrede passend zum Konto. |
| `/ig-reply` | Antworten unter eigenen Posts, sortiert in KEYWORD / LEAD / INHALT / FRAGE / SUPPORT / RAUSCHEN. Support von Bestandskunden nie öffentlich. |
| `/ig-dm` | Keyword-Auslieferung, Erstkontakt per Sie, Kooperations-Pitch und zwei Follow-ups. Mit der rechtlichen Grenze bei Kalt-Nachrichten. |
| `/ig-repurpose` | Webinar, Fachartikel, Messevortrag oder Kundenprojekt wird eine Woche Reels und Karussells. |
| `/ig-audit` | Auswertung des Geposteten: Outlier-Vielfaches, Sends pro Reichweite, und die B2B-Zahlen, die zählen (Profilaufrufe, Link-Klicks, Anfragen). |

## Die Werkzeuge, die wirklich laufen

Keine Abhängigkeiten, kein Netzwerk, nichts wird hochgeladen. Sie laufen auf
deinem Rechner, auf deinem Text.

```bash
python3 skills/ig-reel/hookscore.py hooks.txt           # Hooks ranken
python3 skills/ig-reel/beats.py skript.txt --target 30  # Skript takten
python3 skills/ig-caption/caption.py caption.txt --keywords "gebäudereinigung wien"
python3 skills/ig-human/humanize.py entwurf.txt --report
python3 skills/ig-human/detect.py vorher.txt nachher.txt
python3 skills/ig-viral/swipe.py erfasst.tsv --out ~/.claude/instagram/swipe.md
python3 tests/run.py                                    # alles gegen deutsche Beispiele prüfen
```

So sieht der Hook-Scorer auf deutschen B2B-Hooks aus:

```
HOOK-RANKING
==============================================================================
->  81,4 STARK   Hören Sie auf, Dienstpläne per WhatsApp zu verschicken.
        schwächste: FALLHÖHE (70)
    79,2 STARK   18.000 € hat uns eine fehlende Klausel im Rahmenvertrag g...
        schwächste: ANSPRACHE (70)
    30,0 SCHWACH Wenn Sie Ihre Stunden noch auf Zetteln sammeln, hast du e...
        schwächste: KONKRET (15)
        K.-O.: du und Sie in einer Zeile. Im B2B der Fehler, der sofort nach Vorlage aussieht.
    13,2 SCHWACH Wir freuen uns, Ihnen unsere neue Lösung vorzustellen
        schwächste: EINSTIEG (0)
        K.-O.: Firmen-Einstieg. Keiner scrollt, um zu hören, dass Sie sich freuen. ...
     9,6 SCHWACH Hallo zusammen, heute möchte ich über Zeiterfassung sprechen
        schwächste: EINSTIEG (0)
        K.-O.: Begrüßung. Keiner ist in den Feed gekommen, um begrüßt zu werden.
```

Und der Humanizer auf einem absichtlich schlechten Entwurf. Er ersetzt, was
sich sicher ersetzen lässt, und meldet den Rest, weil der am Satzbau hängt:

```
3. FLOSKELN ERSETZT
    1x  In der heutigen schnelllebigen Welt  -> heute   [einstiege]
    1x  zweifellos  -> sicher   [konnektoren]
    1x  maßgeschneidert  -> passend   [adjektive]
4. FLOSKELN ZU PRÜFEN  (nicht ersetzt - Satz umbauen)
    1x  Gamechanger   [substantive]
        Sag, was sich ändert, mit Zahl.
5. STRUKTUR-MUSTER  (nicht automatisch korrigiert - selbst umschreiben)
    1x  "Nicht nur X, sondern auch Y"
    1x  "Genau hier setzt X an"
```

## Was gemessen ist und was nicht

Das Original hat seinen Hook-Scorer an 74 echten Short-Form-Hooks getestet:
Schlechte Hooks erkennt er gut (AUC 0,83), zwischen den Treffern und Flops
eines guten Creators unterscheidet er kaum (AUC 0,56, Münzwurf ist 0,50). Das
ist ehrlich und gilt für das englische Original.

**Diese deutsche Fassung ist nicht an einem deutschen Korpus gemessen.** Sie ist
nach denselben Prinzipien neu gebaut und gegen die Beispiele in `tests/`
geprüft, mehr nicht. Nimm sie für das, was das Original nachweislich gut
konnte: Begrüßungen, Vorläufe, Hooks ohne Konkretes und zu lange Hooks
aussortieren. Welcher von zwei ordentlichen Hooks läuft, entscheiden Gesicht,
Schnitt, Ton und wem Instagram ihn zeigt. Die Formel-Regexe sind an deutscher
Sprechweise geschrieben; rechne damit, dass ein guter Teil echter Hooks "nicht
zugeordnet" bleibt. Wer das an echten deutschen Reels misst, sollte die
Ergebnisse hier eintragen.

## Das Kleingedruckte

**Diese Skills posten nicht auf Instagram.** Es gibt eine Content Publishing API
für Professional-Konten, die braucht eine Meta-Entwickler-App, eine verknüpfte
Seite, ein langlebiges Token und App-Review. Alles andere, womit Leute Posten,
Kommentieren, Folgen oder DMs automatisieren, ist Browser-Automatisierung oder
ein Dritt-Tool, und beides verstößt gegen die
[Nutzungsbedingungen von Instagram](https://help.instagram.com/581066165581870)
und führt zu Sperren. Darum endet jeder Skill gleich: mit einem kopierfertigen
Block, und du postest.

Die Ausnahme sind automatische Keyword-Antworten in DMs über Instagrams eigene
Werkzeuge oder zugelassene Partner, und nur, nachdem jemand zuerst kommentiert
oder geschrieben hat. `/ig-dm` sagt, wo die Grenze liegt.

**`/ig-viral` liest, es scrapt nicht.** Zehn Konten, ein Dutzend Reels je
Konto, in menschlichem Tempo, mit dir am Steuer deines eigenen Browsers. Es
fragt nie nach deinem Passwort und loggt sich nie als du ein.

**Die fünf Erkennungs-Prüfungen sind lokale Heuristiken, keine Detektor-APIs.**
Sie sind nicht GPTZero, Originality, Copyleaks, Winston oder Turnitin und
versprechen deren Urteil nicht. Wer "nicht erkennbar" verkauft, verkauft dir
etwas.

**Nichts wird erfunden.** Keine erfundenen Kennzahlen, Kunden oder Ergebnisse
unter deinem Namen. Fehlt eine Zahl, steht `{{deine Zahl}}` bzw. `{{Ihre Zahl}}`
im Entwurf, mit Markierung.

**Rechtliche Hinweise sind keine Rechtsberatung.** Impressum (DE § 5 DDG, AT
§ 5 ECG und § 25 MedienG), Werbekennzeichnung, Kalt-Nachrichten (UWG/TKG),
Recht am eigenen Bild: Die Skills weisen darauf hin, ersetzen aber keinen
Anwalt.

**Plattformzahlen veralten.** Die Hashtag-Grenze ist im Dezember 2025 von 30
auf 5 gefallen. Widerspricht hier etwas dem, was Instagram gerade macht, hat
Instagram recht.

## Dateien

```
skills/ig-reel/hooks.json          26 Hook-Formeln: Vorlage, Beispiel (du und Sie), Bildschirmzeile,
                                   wofür, wie sie kaputtgeht, deutsches und englisches Erkennungsmuster
skills/ig-reel/hookscore.py        die fünf Hook-Prüfungen
skills/ig-reel/beats.py            Skript zu Beat-Sheet, nach Silben
skills/ig-reel/sprache.py          deutsche Textregeln (identisch in ig-caption und ig-human)
skills/ig-caption/caption.py       Feed-Vorschau und Caption-Prüfung
skills/ig-human/slop.json          das Lexikon: Floskeln, unsichtbare Zeichen, Struktur-Muster
skills/ig-human/humanize.py        die drei Bereinigungs-Durchgänge
skills/ig-human/detect.py          die fünf Erkennungs-Prüfungen
skills/ig-viral/swipe.py           Outlier-Ranking und Formel-Zuordnung
skills/ig-profile/rubric.json      der 100-Punkte-Profil-Score mit Impressum
templates/voice.md                 dein Stimmprofil. Zuerst ausfüllen.
tests/run.py                       Prüfungen gegen die deutschen Beispiele in tests/beispiele/
```

## Herkunft

Original von Jake Schincariol, [opusjake.ai](https://opusjake.ai):
[instagram-agent-skill](https://github.com/Jakeschincariol/instagram-agent-skill).
Deutsche B2B-Fassung von Mladen Vukovic.

## Lizenz

MIT, wie das Original. Nimm es, änder es, nutz es.
