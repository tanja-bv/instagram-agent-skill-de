---
name: ig-caption
description: >-
  Schreibt die Instagram-Caption: die Zeile, die den "... mehr"-Schnitt
  überlebt, den Text, die eine Bitte, die Suchbegriffe und bis zu fünf
  Hashtags, und prüft sie, bevor sie rausgeht, inklusive du/Sie-Mix. Nutzen
  bei "schreib die Caption", "Caption für", "Bildunterschrift", "Beitragstext",
  "was schreib ich in die Beschreibung", wenn ein Reel oder Karussell fertig ist
  und der Text fehlt, oder bei Fragen zu Hashtags.
---

# ig-caption

Ein Werkzeug liegt in diesem Ordner, und es läuft:

```bash
python3 caption.py caption.txt
python3 caption.py caption.txt --keywords "gebäudereinigung wien,dienstplan app"
```

Es druckt die Caption so, wie der Feed sie druckt: die ersten 125 Zeichen in
einem Kasten, alles andere hinter dem Tippen. Lies diesen Kasten, bevor du
irgendetwas anderes liest, das du geschrieben hast.

## Zuerst: Welchen Fall hat diese Caption?

Das ist die Entscheidung, an der Captions kaputtgehen, wenn sie übersprungen wird.

**Fall A (Video trägt den Hook).** Ein Reel hat seinen eigenen Hook in den
ersten zwei Sekunden, gesprochen und im Bild. Die Caption ist kein zweiter
Hook, und mit dem Video zu konkurrieren ist der Weg, beides zu verlieren. Ihre
Aufgabe: die Bitte, der Zusammenhang, der die Bitte sinnvoll macht, und die
Wörter, nach denen Leute suchen.

**Fall B (Hook in der Caption).** Ein Foto, ein Einzelbild, ein
Karussell-Cover, das eine Frage aufmacht. Hier ist Zeile eins der Hook, und sie
funktioniert genau wie ein Reel-Hook: konkret, kurz, und abgeschnitten an
einer Kante statt mitten im Nebensatz.

Frag, welchen Fall du schreibst. Hat der Nutzer ein Reel mit starkem Hook,
schreib Fall A und sag warum.

## Die Form

```
Zeile 1   125 Zeichen sichtbarer Platz. Fall A: die Bitte, schlicht.
          Fall B: der Hook.
          Nie eine Begrüßung, nie "Wir freuen uns", nie ein Hashtag, nie ein
          Emoji als erstes Zeichen.
Text      kurze Absätze, je eine Leerzeile dazwischen. Zwei bis sechs Stück.
          Hier stehen die Suchbegriffe.
Bitte     eine. Keyword kommentieren, speichern oder DM. Eine.
Hashtags  bis zu fünf, in einer eigenen Zeile ganz unten, oder keine.
```

Deutsche Sätze sind länger als englische. Plan das Ende des ersten Gedankens
bei 100 bis 110 Zeichen, nicht bei 125. Die Grenze liegt bei 2.200 Zeichen,
und fast nichts braucht 2.200. Eine Caption, die das Tippen verdient und dann
600 Zeichen liefert, schlägt eine mit 1.800.

## Anrede

Eine Anrede, durchgehend, aus `~/.claude/instagram/voice.md`. Fehlt sie:
einmal fragen, ohne Antwort Sie. `caption.py` zählt du-Formen und Sie-Formen
und gibt FEHLER, sobald beide vorkommen. Das ist der häufigste Fehler in
deutschen B2B-Captions, und er passiert fast immer an derselben Stelle: Der
Text siezt, und der CTA am Ende duzt ("Folge uns für mehr").

## Hashtags, ehrlich

Hashtags sind kein Reichweitenhebel mehr, und die Plattform hat das inzwischen
mit einer Produktänderung gesagt. **Instagram hat Hashtags am 18. Dezember 2025
auf fünf pro Post begrenzt**, vorher dreißig, mit dem Hinweis, dass wenige
gezielte Hashtags besser laufen als viele allgemeine. Adam Mosseri hatte schon
im Februar 2025 gesagt, dass Hashtags keine Reichweite bringen, sondern ein
Etikett sind.

Also: bis zu fünf, spezifisch, als Themenetikett. Umlaute funktionieren
(#gebäudereinigung). Hat der Nutzer einen Block mit zwanzig Tags in seinen
Notizen, ist der jetzt Ballast, und der Linter lässt ihn durchfallen.

`#viral`, `#fyp`, `#explorepage`, `#erfolg`, `#business` beschreiben nichts.
Streichen.

## Suchbegriffe zählen mehr als Hashtags

Die Instagram-Suche liest den Caption-Text. Der Begriff, unter dem der Nutzer
gefunden werden will, gehört also als Wortfolge in die Caption, so wie ein
Mensch sie tippt, in einem Satz, der normal klingt. Im B2B heißt das fast
immer Leistung plus Region: "Gebäudereinigung in Wien" als Worte in Zeile
drei, nicht "#gebäudereinigungwien" in einem Block unten.

Frag nach zwei oder drei solcher Begriffe und gib sie dem Linter:

```bash
python3 caption.py entwurf.txt --keywords "gebäudereinigung wien,unterhaltsreinigung"
```

## Regeln

- **Kein Link in der Caption.** Captions sind nicht klickbar. Eine URL im Text
  ist toter Text, der sagt "ich nutze diese Plattform nicht". Bio oder DM.
- **Eine Bitte.** Zwei Bitten sind so gut wie keine. `caption.py` zählt sie.
  "Kommentieren Sie VERTRAG, dann schicken wir Ihnen die Vorlage per DM" ist
  eine Bitte: Die DM ist die Auslieferung.
- **Das Keyword muss sich tippen lassen.** Ein Wort, keine Leerzeichen, kein
  Emoji, und im Video auch laut sagen. `Kommentiere VORLAGE` funktioniert.
  `Kommentiere "die Angebotsvorlage für Reinigungsfirmen"` nicht. Umlaute im
  Keyword vermeiden, manche tippen "ae".
- **Den ersten Kommentar getrennt schreiben**, wenn es einen Link gibt. Im
  Beleg erwähnen.
- **Emoji als Satzzeichen, nicht als Deko.** Der Linter meldet alles über 4
  pro 100 Zeichen.
- **Alt-Text ist 20 Sekunden wert.** Für Karussells und Fotos schreiben. Er
  wird von Screenreadern gelesen und von Instagram.
- **Bezahlte Kooperation kennzeichnen.** Gibt es Geld oder eine Gegenleistung,
  gehört "Werbung" bzw. "Anzeige" in die erste Zeile und das Branded-Content-Tool
  von Instagram dazu. Keine Rechtsberatung, aber das ist der übliche Mindeststandard.
- **Kundennamen und @-Erwähnungen von Kunden nur mit Freigabe.**

## Der Ablauf

1. Fall A oder Fall B entscheiden und sagen, welcher.
2. Entwerfen.
3. `/ig-human` darüber laufen lassen. Captions sind kurz, darum fallen
   Floskeln hier lauter auf als irgendwo sonst im Paket.
4. `caption.py` mit den Suchbegriffen des Nutzers laufen lassen. Jedes FEHLER
   beheben. Über jedes WARN laut entscheiden, nicht stillschweigend.
5. Den kopierfertigen Block ausgeben, dann den Beleg:

```
CAPTION FERTIG
Fall:        A - das Reel trägt den Hook
sichtbar:    108 von 125 Zeichen vor dem Schnitt genutzt
Bitte:       eine, VERTRAG kommentieren
Anrede:      Sie, durchgehend
Hashtags:    3
Suche:       "rahmenvertrag" in Zeile 1, "gebäudereinigung wien" in Zeile 4
Linter:      FERTIG
```

So sieht eine echte Prüfung aus (gekürzt):

```
  WAS DER FEED ZEIGT
  +------------------------------------------------------+
  | 18.000 € hat uns eine fehlende Klausel gekostet.     |
  | Seitdem steht in jedem Rahmenvertrag derselbe Satz,  |
  | und Sie sollten ihn kenn                             |
  +-------------------------------------------- ... mehr +

  OK     LÄNGE         348 / 2200 Zeichen
  WARN   ERSTE ZEILE   128 Zeichen, wird bei 125 mitten im Gedanken geschnitten. ...
  OK     HOOK KONKRET  1 Zahl(en) oder Name(n) im sichtbaren Fenster
  OK     EIN CTA       eine Handlungsaufforderung: Keyword kommentieren
  OK     ANREDE        durchgehend Sie
  WARN   SUCHBEGRIFFE  1/2 vorhanden, 1 im sichtbaren Fenster. Fehlt: gebäudereinigung wien
```

Die erste Zeile endet hier drei Zeichen zu spät. Kürzen, bis "kennen" vor dem
Schnitt steht, oder den Satz so bauen, dass der Schnitt eine Kante ist.

Nichts wird gepostet. Der Nutzer fügt es ein.
