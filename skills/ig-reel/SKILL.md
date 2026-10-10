---
name: ig-reel
description: >-
  Schreibt ein Instagram-Reel aus einer rohen Idee: Hook-Optionen aus 26
  Formeln, das gesprochene Skript, den Bildschirmtext und ein Beat-Sheet mit
  Zeitmarken, in der Stimme und Anrede des Nutzers und bewertet, bevor gedreht
  wird. Nutzen, wenn der Nutzer ein Reel will, ein Kurzvideo-Skript, einen
  Hook oder ein Voiceover, bei "schreib mir ein Reel", "mach ein Reel über X",
  "Hook für", "was sag ich in dem Video", "Skript für ein Video", oder wenn er
  gleich aufnimmt und den ersten Satz noch nicht hat.
---

# ig-reel

Macht aus einer rohen Idee ein Reel, das jemand bis zum Ende schaut.

Zwei Werkzeuge liegen in diesem Ordner, und beide laufen wirklich. Nutz sie.
Schätz den Hook nicht nach Gefühl und rate nicht bei der Länge.

```bash
python3 hookscore.py hooks.txt              # Hook-Optionen ranken
python3 hookscore.py --hook "eine Zeile"    # eine einzelne bewerten
python3 beats.py skript.txt --target 30     # Beat-Sheet mit Zeiten, vor dem Dreh
```

Beide teilen sich `sprache.py`: Silben statt Wörter (deutsche Wörter sind
lang), Zahlen so gezählt, wie man sie sagt ("18.000 €" sind sechs Silben), und
"konkret" heißt Zahl, Abkürzung, Marke, Monat oder Ort, nicht großgeschrieben.
Im Deutschen ist jedes Substantiv groß.

## Bevor du schreibst

1. Lies `~/.claude/instagram/voice.md`, falls es die Datei gibt. Das ist das
   Stimmprofil des Nutzers: wie er vor der Kamera spricht, was er nie sagt, mit
   wem er redet, **ob er duzt oder siezt** und sein Sprechtempo in Silben pro
   Sekunde. Gibt es die Datei nicht, frag nach **drei eigenen Reels**, lies
   oder transkribier sie, leite die Stimme ab und schreib die Datei. Ein Skript
   in der falschen Stimme ist unbrauchbar, weil er es laut sagen muss. Fehlt
   die Anrede: einmal fragen, ohne Antwort Sie. Nie mischen.
2. Lies `hooks.json` in diesem Ordner. 26 Formeln, jede mit Vorlage,
   ausgefülltem Beispiel (bei Formeln mit Ansprache auch `example_sie`),
   Bildschirmversion, wofür sie gut ist und wie sie kaputtgeht.
3. Ist die Idee dünn, polster sie nicht. Stell eine gebündelte Frage: Was ist
   passiert, bei wem, und was hat es gekostet oder gebracht. Ein Reel braucht
   eine konkrete, wahre Sache. Hol sie, bevor du schreibst.
4. Gibt es `~/.claude/instagram/swipe.md`, lies es. `/ig-viral` schreibt diese
   Datei, und sie ist der eigene Beleg des Nutzers, welche Formeln in seiner
   Branche gerade laufen. Sie schlägt die Standardwerte hier.

## Die Form

Ein Reel entscheidet sich in den ersten zwei Sekunden und hält in den nächsten fünf.

```
0:00 - 0:02   HOOK         die Behauptung. Gesprochene Zeile und Bildschirmzeile
                           getrennt geschrieben. Bewegung im ersten Bild, kein starrer Kopf.
0:02 - 0:07   FALLHÖHE     warum das den Zuschauer betrifft. Eine Zeile.
0:07 - ...    HAUPTTEIL    eine Idee pro Beat, und das Bild wechselt mit jedem Beat.
LETZTE 3s     AUFLÖSUNG    liefern, was der Hook versprochen hat, dann die eine Bitte.
LETZTE ZEILE  LOOP         ein Wort aus dem Hook wiederholen, damit der Replay sauber landet.
```

Länge: 15 bis 45 Sekunden ist der Arbeitsbereich. Reels laufen bis zu drei
Minuten, und fast keiner sollte das nutzen. Unter 7 Sekunden steigen die
Loop-Zahlen, sonst nichts. Im B2B gilt: Ein Geschäftsführer schaut 30 Sekunden
zu Ende, wenn in Sekunde zwei sein Problem steht. Er schaut keine 60 Sekunden
Imagefilm.

## Der Ablauf

**1. Drei Hooks, nicht einen.** Lauf mit der Idee durch `hooks.json`, wähl drei
Formeln, die wirklich passen, und schreib für jede die gesprochene Zeile plus
die Bildschirmzeile. Drei verschiedene Formeln, nicht drei Umformulierungen
einer. Nimm `example` oder `example_sie` als Muster, je nach Anrede.

**2. Bewerten.** Die drei gesprochenen Zeilen in eine Datei, eine pro Zeile,
und `hookscore.py` laufen lassen. Zeig dem Nutzer das Ranking. Liegt der beste
unter 50, gibt es den Hook noch nicht, und kein Feilen ändert das. Ein K.-O.
(Begrüßung, "In diesem Video", "Wir freuen uns", du/Sie gemischt) wird nicht
diskutiert, sondern neu geschrieben.

**3. Das Skript schreiben**, auf dem Sieger-Hook. Gesprochene Sprache, so wie
der Nutzer wirklich redet. Kurze Zeilen. Kein Satz, den er üben müsste.
Fachwörter seiner Kunden ("Objekt", "Dienstplan", "Abnahme") statt
Marketingdeutsch.

**4. Takten.** `beats.py skript.txt --target {Länge} --sps {Tempo aus voice.md}`.
Jede Markierung beheben: Hook über 3 Sekunden, ein Beat über 4 Sekunden, eine
Reihe Beats ohne Konkretes, kein Loop, du/Sie gemischt. Neu laufen lassen, bis
es sauber ist.

**5. Humanisieren.** Das Skript durch `/ig-human` schicken, bevor du es zeigst.
Eine geschrieben klingende Zeile hört man in dem Moment, in dem sie jemand laut
sagt.

**6. Den Block ausgeben.** Das Skript in einem Code-Block, den Bildschirmtext
als eigene Liste mit Zeiten, und dann:

```
REEL FERTIG
Hook:        #5 Zeitraffer, 77,9 STARK
Länge:       24,2s über 9 Beats bei 4,5 Silben/s
Bildschirm:  6 Tafeln, Untertitel durchgehend
Humanizer:   3 Artefakte entfernt, Mensch-Score 74 BESTANDEN
Anrede:      du, durchgehend
Caption:     als Nächstes /ig-caption

Antworte "ja", dann logge ich es, oder sag, was sich ändern soll.
```

**7. Nie veröffentlichen.** Dieser Skill liefert ein Skript. Der Nutzer dreht
und postet. Bei "ja" an `~/.claude/instagram/log.md` anhängen: Datum, genutzte
Hook-Formel und erste Zeile, damit `/ig-audit` später eine Historie hat.

## Bildschirmtext ist ein eigenes Skript

Schreib ihn getrennt, jedes Mal. Er wird gelesen, bevor er gehört wird.

- **Höchstens sechs Wörter pro Tafel, etwa 20 Zeichen pro Zeile.** Gelesen auf
  Armlänge von jemandem, der noch nicht zuhört. Lange Komposita von Hand
  trennen: "Arbeitszeit-/erfassung" statt einer Zeile, die aus dem Bild läuft.
- **Die Hook-Tafel steht ab Bild 1**, nicht nach einem Beat Stille.
- **Im sicheren Bereich bleiben.** Auf einem 1080x1920-Bild nichts über y=230
  oder unter y=1440, und die rechten 230 Pixel frei lassen. Außerhalb dieses
  Rahmens liegt die Oberfläche über allem: Caption, Aktionsleiste, Audiozeile.
- **Den Hook nie dorthin, wo die Caption sitzt.** Das ist der untere Bildrand,
  und der ist verdeckt.
- **Untertitel für den ganzen Hauptteil einbrennen.** Pflicht, nicht Kür: Viele
  schauen zuerst ohne Ton, und im B2B schauen viele im Büro.
- **Umlaute und ß prüfen.** Manche Schriften in Schnitt-Apps haben kein ß oder
  setzen es in Großbuchstaben falsch. Vor dem Export anschauen.

## Regeln, die den Unterschied machen

- **Eine Idee pro Reel.** Hat das Skript zwei, sind es zwei Reels. Sag das.
- **Zahlen statt Adjektive.** "4.200 €" schlägt "viel Geld". Hat der Nutzer
  keine Zahl genannt, frag danach, statt um das Loch herumzuschreiben.
- **Das Intro streichen.** Keine Begrüßung, kein "In diesem Video", kein Name,
  kein Logo-Jingle, kein "Wir freuen uns". Das Video beginnt bei dem Satz, den
  man sonst in Sekunde sechs erreicht.
- **Mit jedem Beat das Bild wechseln.** Eine starre Einstellung über 8 Sekunden
  ist die Stelle, an der Leute gehen, und `beats.py` markiert sie.
- **Eine Bitte am Ende.** Keyword kommentieren, speichern oder folgen. Eine.
  Im B2B meistens das Keyword, weil es zu einem Gespräch führt.
- **Nie erfinden.** Keine erfundenen Kennzahlen, Kunden, Umsätze oder
  Ergebnisse unter dem Namen des Nutzers, auch nicht als Platzhalter. Fehlt
  eine Zahl, bleibt `{{deine Zahl}}` bzw. `{{Ihre Zahl}}` im Skript stehen, mit
  Markierung.
- **Kunden, Mitarbeiter und Kundenobjekte nur mit Einwilligung.** Kundennamen,
  Logos und Kundenzahlen nur mit schriftlicher Freigabe. Ein Dreh beim Kunden
  vor Ort braucht dessen Okay, und nichts Sicherheitsrelevantes ins Bild
  (Schließpläne, Alarmanlagen, Zugangscodes).
- **Kein Skript um einen Trend-Sound, den der Nutzer nicht nutzen kann.**
  Unternehmenskonten haben meist nur die lizenzfreie Musikbibliothek. Braucht
  die Idee die eigene Stimme des Nutzers, sag das.
- **Rechtliche oder steuerliche Aussagen nur mit Quelle.** Ein B2B-Publikum
  prüft nach, und ein falscher Satz über Arbeitsrecht kostet mehr Vertrauen,
  als das Reel je bringt.

## Beispiel

```
/ig-reel wir haben die Angebotszeit mit einer Vorlage von 5 Stunden auf 20 Minuten gedrückt
```

```
HOOK-RANKING
->  77,9 STARK   #5  Zeitraffer      "Für Angebote haben wir früher fünf Stunden gebraucht. Heute zwanzig Minuten."
                                     Bildschirm: 5 STD → 20 MIN
    52,6 OK      -   (frei)          "Vier Stunden pro Woche haben wir für Formatierung verrechnet. Zwei Jahre lang."
                                     Bildschirm: 2 JAHRE FORMATIERT
    37,8 SCHWACH #9  Zum Mitnehmen   "Klau dir die Angebotsvorlage, die das geschafft hat."
                                     Bildschirm: ZUM MITNEHMEN
```

Gedreht wird #5: Das Verhältnis ist glaubwürdig, es liest sich auf einen Blick
im Bild, und die Zahl gehört dem Nutzer. `beats.py` meldet danach, dass der
Hook mit 4,9 Sekunden zu lang ist. Darum wird er geteilt: "Angebote: früher
fünf Stunden." als Beat 1, "Heute zwanzig Minuten." als Beat 2. Die
Bildschirmtafel bleibt gleich.
