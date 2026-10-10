---
name: ig-viral
description: >-
  Findet die Reels, die in der Nische des Nutzers gerade wirklich
  funktionieren, sortiert sie danach, wie weit jedes über dem Median des
  eigenen Kontos lag, benennt die Hook-Formel und macht daraus ein Swipe-File,
  aus dem er drehen kann. Für B2B im DACH-Raum: Ton und Themen von
  DACH-Konten, Formate auch von größeren englischsprachigen B2B-Konten.
  Verwenden, wenn der Nutzer sagt "viral", "was funktioniert gerade", "finde
  virale Videos", "was posten andere in meiner Branche", "analysier dieses
  Konto", "bau mir ein Swipe-File", "warum läuft dieses Reel so gut", oder
  fragt, was er als Nächstes machen soll, und keine Belege für eine Antwort
  hat.
---

# ig-viral

Der Recherche-Skill. Alles andere in diesem Paket schreibt, dieser schaut
nach. Einmal im Monat laufen lassen, nicht täglich. Formeln halten eine
Saison.

Ein Werkzeug liegt in diesem Ordner, und es läuft:

```bash
python3 swipe.py erfasst.tsv --out ~/.claude/instagram/swipe.md
```

## Die eine Idee, für die sich das lohnt

**Aufrufzahlen allein sind kein Beleg.** Ein Konto mit 200.000 Followern und
40.000 Aufrufen hatte einen ruhigen Dienstag. Ein Konto mit 3.000 Followern
und 40.000 Aufrufen hat etwas gefunden, und das lässt sich kopieren.

Darum sortiert hier alles nach dem **Outlier-Multiplikator**: Aufrufe geteilt
durch den aktuellen Median des jeweiligen Kontos. Alles über 3x ist ein
Signal. Alles unter 1,5x ist ein normaler Tag für dieses Konto und lehrt
nichts, egal wie groß die Zahl aussieht.

Sammle Konten **innerhalb von etwa Faktor 10 zur eigenen Größe**. Eine Formel,
die bei 2 Mio. Followern funktioniert, funktioniert oft, weil das Konto 2 Mio.
Follower hat.

Im DACH-B2B wird das schnell eng. Eine Nische wie Gebäudereinigung in
Österreich hat vielleicht fünf Konten, die regelmäßig Reels posten. Darum
haben die Quellen zwei getrennte Aufgaben:

- **DACH-Konten liefern Ton und Themen.** Was die Zielgruppe hier beschäftigt,
  welche Wörter sie benutzt, worüber in der Branche gerade geredet wird
  (KV-Abschluss, Ausschreibungen, Personalmangel).
- **Größere englischsprachige B2B-Konten liefern Formate.** Hook-Form, Aufbau,
  Länge, Schnittmuster. Übernimm die Formel, nie das Skript. Eine übersetzte
  US-Pointe klingt im DACH-Raum nach Übersetzung und meistens nach
  Übertreibung.

## Schritt 1: Konten auswählen

Frag den Nutzer nach 6 bis 12 Konten, oder schlag welche vor und lass sie
bestätigen:

- **4 direkt**: gleiche Branche, gleiches Angebot, ein Stück weiter. Gern aus
  dem Nachbarland. Ein Wiener Reinigungsbetrieb kann von einem Münchner
  lernen.
- **4 angrenzend**: andere Branche, gleiches Publikum. Wer an Hausverwaltungen
  verkauft, schaut bei Facility-Management, Haustechnik und Software für
  Hausverwaltungen. Hier werden Formate übernommen, bevor die eigene Branche
  sie hat.
- **2 bis 4 übergroß**: deutlich größere Konten, meist englischsprachige
  B2B-Konten (SaaS, Agenturen, Dienstleister). Nur für das Format, nie für
  Taktung oder Ton.

Lass den Nutzer außerdem seine eigene **Gespeichert-Sammlung** öffnen. Sie ist
der schnellste und passendste Bestand, den es gibt, und schon nach seinem
Geschmack gefiltert.

## Schritt 2: nachschauen

Nutze das Browser-Werkzeug, das diese Sitzung tatsächlich hat: einen
integrierten Browser, eine Erweiterung im Chrome des Nutzers oder ein
Computer-Use-Werkzeug. Eine API gibt es dafür nicht, und es braucht auch
keine, weil die Menge klein genug zum Lesen ist.

**Regeln, die nicht verhandelbar sind:**

- **Nie im Namen des Nutzers bei Instagram einloggen und nie nach einem
  Passwort fragen.** Braucht eine Seite einen Login, ist der Nutzer derjenige,
  der schon eingeloggt ist. Steuere seinen Browser, während er dabei ist, oder
  lass ihn die Daten einfügen.
- **Das ist Lesen, kein Scraping.** Zehn Konten, je ein Dutzend Reels, in
  menschlichem Tempo. Automatisiertes Sammeln in großer Menge verstößt gegen
  die Nutzungsbedingungen von Instagram und bringt Konten Aktionssperren ein.
  Bau keinen Crawler, nutz keinen Scraping-Dienst und lass das nicht im
  Hintergrund in einer Schleife laufen.
- **Kopiere die Formel, nie das Video.** Hook-Form, Aufbau, Länge,
  Schnittmuster. Nicht deren Skript, nicht deren Stimme, nicht deren Schnitt.
  Ordne jede Zeile im Swipe-File dem Konto zu, von dem sie stammt.

**Was pro Reel erfasst wird**, in den Worten des Kontos selbst:

| feld | hinweis |
| --- | --- |
| konto | Handle |
| follower | aus dem Profil |
| median | die letzten 12 Reels durchgehen und den mittleren Aufrufwert nehmen |
| aufrufe | dieses Reel |
| hook | die erste Zeile, gesprochen oder eingeblendet, wörtlich, auch mit Grammatikfehlern |
| texttafel | die erste Texteinblendung, falls sie abweicht |
| länge | Sekunden |
| cta | worum am Ende gebeten wird |

Der Median ist der wichtige Wert. Ohne ihn sortierst du wieder nach
Followerzahl, und genau das soll dieser Skill abstellen.

Hooks englischsprachiger Konten im Original erfassen, nicht übersetzt. Erkennt
der Klassifikator sie nicht, ordne die Formel in Schritt 4 von Hand zu.

**Wenn Instagram nicht genug zeigt:** Dieselbe Hook-Grammatik läuft auf
YouTube Shorts, wo Aufrufzahlen und Transkripte öffentlich sind und kein Login
nötig ist. Das ist ein legitimer zweiter Bestand, und an den gesprochenen Hook
kommt man dort leichter:

```bash
# Aufrufzahlen der Shorts eines Kanals
python3 -m yt_dlp --flat-playlist --playlist-end 40 -J \
  "https://www.youtube.com/@HANDLE/shorts" > kanal.json

# die gesprochene erste Zeile eines Shorts, aus den automatischen Untertiteln
# (für deutschsprachige Kanäle "de.*" statt "en.*")
python3 -m yt_dlp --skip-download --write-auto-subs --sub-langs "en.*" \
  --sub-format json3 -o hook "https://www.youtube.com/watch?v=VIDEO_ID"
```

Nimm jedes Untertitelwort mit einem Zeitstempel unter 3,0 Sekunden. Das ist
der Hook, wie er gesagt wurde, nicht wie er geschrieben steht.

## Schritt 3: sortieren

Füll eine tabulatorgetrennte Datei mit Kopfzeile und lass das Skript laufen:

```
konto	follower	median	aufrufe	hook
@beispiel_reinigung	3400	900	31000	Das sagt Ihnen keiner: Die ersten 20 Ausschreibungen verlieren Sie
```

Englische Spaltennamen (`account`, `followers`, `median`, `views`, `hook`)
funktionieren auch.

```bash
python3 swipe.py erfasst.tsv --out ~/.claude/instagram/swipe.md
```

Es berechnet den Outlier-Multiplikator, benennt die Hook-Formel anhand
derselben 26 Formeln, mit denen `/ig-reel` schreibt, bewertet jeden Hook mit
`hookscore.py` und zeigt, was das obere Drittel vom unteren unterscheidet.

## Schritt 4: sagen, was es bedeutet, und zwar vorsichtig

Berichte drei Dinge, nicht mehr:

1. **Welche Formeln im oberen Drittel überrepräsentiert sind**, mit Anzahl.
   Zwei Formeln, die je viermal über sechs Konten vorkommen, sind ein Befund.
   Eine, die zweimal vorkommt, ist keiner.
2. **Was das obere Drittel strukturell gemeinsam hat** und das untere nicht:
   Hook-Länge, ob die Auflösung visuell ist, ob sich das erste Bild bewegt, wo
   die Bitte steht.
3. **Die nicht zugeordneten Zeilen.** Jeder Hook, den der Klassifikator nicht
   benennen konnte, ist entweder Rauschen oder eine Formel, die noch nicht in
   `hooks.json` steht. Lies sie von Hand. Das ist die wertvollste Spalte der
   Ausgabe, und deshalb gibt das Skript die Anzahl aus.

Nenn dann Stichprobengröße und Sicherheit in klaren Worten. Vierzig Reels
über sechs Konten tragen eine Aussage. Zwölf nicht, und das zu sagen ist der
Unterschied zwischen Recherche und Horoskop.

Sag auch, was diese Daten nicht zeigen: Ein Outlier belegt, dass eine Formel
Aufmerksamkeit holt. Ob sie im B2B Anfragen bringt, zeigen erst die eigenen
Zahlen in `/ig-audit`.

## Schritt 5: daraus etwas zum Drehen machen

Schreib für die drei stärksten Formeln **die Version des Nutzers**: seine
eigene Geschichte, seine eigene Zahl, in der Form, die gerade funktioniert.
Bei Formeln von englischsprachigen Konten heißt das neu schreiben, nicht
übersetzen: in der Fachsprache seiner Zielgruppe und in der Anrede aus
`voice.md`. Gib jede an `/ig-reel` weiter, mit bereits gewählter Formel-ID.

Gib nie "mach ein Reel wie dieses" zurück. Gib eine Hook-Zeile zurück, die er
morgen sagen könnte.

## Ausgabe

```
SWIPE-FILE  ·  38 Reels  ·  7 Konten  ·  Basis: Konto-Median

OUTLIER (über 3x)
  38,4x  hook 86  #3  Sagt dir keiner     @konto_a     41.100  (Median 1.070)
  11,2x  hook 79  #9  Zum Mitnehmen       @konto_c    180.000  (Median 16.100)
  ...

WAS ÜBERREPRÄSENTIERT IST
  #3 Sagt dir keiner    5x im oberen Drittel, 0x im unteren
  #2 Klare Ansage       4x
  Hook-Länge (Median)   8 Wörter oben, 19 unten

NICHT ZUGEORDNET (6)
  Zwei davon haben dieselbe Form, und die steht nicht in hooks.json: ein Hook,
  der mit dem vorgelesenen Kommentar eines anderen beginnt. Aufnehmen lohnt sich.

EIGENE VERSION
  #3  "Das sagt Ihnen keiner: Die ersten 20 Ausschreibungen verlieren Sie."
  ...
```

Schreib das Swipe-File nach `~/.claude/instagram/swipe.md`. `/ig-reel` und
`/ig-plan` lesen es beide, und darum geht es: Nach einem Durchlauf arbeitet
der Rest des Pakets mit den eigenen Belegen des Nutzers statt mit
Standardwerten.

Dieser Skill postet nichts, folgt niemandem, vergibt keine Likes und schreibt
keine Nachrichten. Er liest.
