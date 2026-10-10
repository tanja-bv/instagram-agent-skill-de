---
name: ig-plan
description: >-
  Plant die Instagram-Woche: was gepostet wird, in welchem Format, wann, und
  mit welchen Konten (Kunden, Partner, Verbände, Fachmedien) interagiert wird.
  Für B2B im DACH-Raum, mit Posting-Zeiten für Entscheider und optionalem
  Recruiting-Slot. Verwenden, wenn der Nutzer sagt "Wochenplan", "plan meine
  Woche", "was soll ich posten", "Redaktionsplan", "Content-Kalender", "mir
  fällt nichts zum Posten ein", oder einen Posting-Plan und eine
  Engagement-Liste will.
---

# ig-plan

Die Schaltzentrale. Alles andere in diesem Paket führt aus, dieser Skill
entscheidet, was ausgeführt wird. Einmal pro Woche laufen lassen, immer am
selben Tag.

## Eingabe

Wenn `~/.claude/instagram/voice.md`, `swipe.md` und `log.md` existieren, lies
sie. Das Swipe-File ist der eigene Beleg des Nutzers aus `/ig-viral` dafür,
welche Formeln in seiner Branche gerade ankommen, und es sticht alles in
dieser Datei. Das Log verhindert, dass der Plan ein Thema aus den letzten zwei
Wochen wiederholt.

Wenn sie nicht existieren, frag nach vier Dingen und schreib sie auf:

1. Was der Nutzer verkauft, und an wen (Branche, Betriebsgröße, Funktion:
   Inhaber, Objektleitung, HR, Einkauf).
2. Die drei oder vier Themen, für die er bekannt sein will.
3. Was diese Woche tatsächlich passiert ist: ein Kundentermin, eine Zahl, ein
   Fehler, eine Abnahme, eine gewonnene oder verlorene Ausschreibung, eine
   Diskussion im Team. Daraus entstehen Posts.
4. Zehn Konten, bei denen er sichtbar sein will: Kunden, Partner, Verbände,
   Fachmedien.

Frag nebenbei, ob gerade Stellen offen sind. Das entscheidet über den
Recruiting-Slot.

## Was gepostet wird

Vier bis fünf Posts pro Woche, davon mindestens drei Reels. Reels sind das
einzige Format auf Instagram, das zuverlässig Leute erreicht, die dem Konto
nicht folgen. Karussells gehen in die Tiefe bei denen, die schon folgen, und
werden im B2B gern gespeichert und weitergeleitet. Stories laufen täglich und
werden separat geplant.

Über die Woche mischen, nie zweimal derselbe Typ hintereinander:

| Typ | Anteil | Aufgabe |
| --- | --- | --- |
| **Beleg** | 1 pro Woche | etwas, das passiert ist, mit einer Zahl. Reel. Kundenbezug nur mit Freigabe, sonst anonymisiert (Branche, Größe, Ergebnis). |
| **Wissen** | 1 bis 2 pro Woche | eine Sache, die der Zuschauer heute umsetzen kann. Reel oder Karussell. |
| **Meinung** | 1 pro Woche | eine Position, die Follower kosten könnte. Reel. |
| **Geschichte** | 1 alle zwei Wochen | eine Szene mit einem Preis. Reel. |
| **Angebot** | 1 alle zwei Wochen | was der Nutzer verkauft, klar gesagt, ohne Entschuldigung. Karussell oder Stories. |
| **Recruiting** | optional, höchstens 1 pro Woche | nur bei offener Stelle: echter Arbeitsalltag statt Stellenanzeige. Ersetzt Geschichte oder Angebot, nie einen Beleg. |

Recruiting läuft im B2B oft über denselben Kanal, darf ihn aber nicht
übernehmen. Ein Konto, das drei Wochen nur Stellen postet, sehen Kunden als
Betrieb, der seine Leute nicht hält. Mitarbeiter im Bild nur mit Einwilligung.

Gib für jeden Slot an: das Thema, den konkreten Blickwinkel aus dem, was diese
Woche passiert ist, das Format und die Nummer der Hook-Formel aus
`ig-reel/hooks.json`. Kein Thema, ein Blickwinkel. "Sicherheit" ist kein Plan.
"Der Revierfahrer, der um 03:10 die Tür offen fand, die laut Protokoll zu war"
ist ein Reel.

## Wann gepostet wird

Poste, wenn das Publikum aufs Handy schaut und nicht gerade arbeitet. Für
Entscheider in KMU gilt als **Startannahme**:

- DI–DO, 07:00–08:00 (vor dem ersten Termin), 12:00 (Mittagspause) und
  19:00–20:30 (nach Feierabend), MEZ bzw. MESZ.
- Montagvormittag und Freitagnachmittag eher schwach.
- Recruiting-Posts zielen auf Bewerber: abends und am Wochenende.
- Branchen mit Schichtbetrieb ticken anders. Eine Objektleitung in der
  Gebäudereinigung ist um 06:00 schon unterwegs, eine Bauleitung auch.

Das ist eine Annahme zum Starten, keine Regel. Sobald das Konto genug Follower
hat, stehen in den Insights bei den Follower-Daten die aktivsten Zeiten. Die
schlagen jede Tabelle, auch diese.

Und sag es deutlich: **Die Uhrzeit zählt viel weniger als die ersten zwei
Sekunden.** Instagram zeigt ein Reel tagelang weiter, wenn es gut läuft, und
begräbt ein perfekt getimtes, das nicht läuft. Optimiert der Nutzer
Posting-Zeiten, bevor seine Hooks funktionieren, poliert er das Falsche, und
das sollst du ihm sagen.

Richte die Zeiten nach der Zeitzone des Publikums, nicht nach der des
Nutzers. Im DACH-Raum ist das dieselbe; wichtig wird es erst bei Kunden
außerhalb.

## Die Engagement-Runde, und die ist Pflicht

20 Minuten am Tag, vor dem Posten, nicht danach. Stell eine Liste mit 10
Konten zusammen. Keine Influencer, sondern die Konten, bei denen die
Zielgruppe ohnehin mitliest:

- **4 Reichweite**: Verbände, Innungen, Kammern, Fachmedien, Messen. Konten,
  deren Publikum die Zielgruppe des Nutzers ist und wo ein guter Kommentar
  gesehen wird. Früh kommentieren, bevor der Thread 200 Kommentare lang ist.
- **3 Partner**: Partner, Lieferanten, Nachbarbranchen, ähnliche Größe. Das
  ist die Gruppe, die zurückkommentiert.
- **3 Kunden**: Bestandskunden und Wunschkunden, also Leute, die tatsächlich
  kaufen könnten. Wochenlang kommentieren, bevor eine DM kommt, und nie im
  Kommentar pitchen. Die erste DM enthält kein Angebot (siehe `/ig-dm`).
  Support-Themen von Bestandskunden nie öffentlich in Kommentaren klären.

Gib die Liste an `/ig-comment` weiter.

## Ausgabe

```
WOCHE AB 15.09.

MO  nur Engagement  (20 Min., Liste unten)
DI  07:30  REEL       BELEG       #5  Zeitraffer           Dienstplan für 60 Wachleute: 5 Std. auf 20 Min.
MI  19:30  REEL       MEINUNG     #2  Klare Ansage         Schreiben Sie Bewachung nicht nach Stundensatz aus
DO  12:00  KARUSSELL  WISSEN      Hook in der Caption      die 4 Punkte, die in jede Dienstanweisung gehören
FR  nur Stories + Engagement
SA  -
SO  19:30  REEL       GESCHICHTE  #21 Mitten im Satz       "...und um 02:00 stand der Kunde selbst vor dem Tor"

STORIES     jeden Tag, 3 bis 5 Frames, Fragen-Sticker am Donnerstag.
RECRUITING  Stelle Revierfahrer offen: SO wahlweise als Recruiting-Reel
            (#18 Kaltstart-Demo, eine Nachtschicht im Revier in 30 Sekunden).
ZEITEN      Startannahme, nach vier Wochen mit den Insights abgleichen.

ENGAGEMENT  (4 Reichweite / 3 Partner / 3 Kunden)
  ...

Sag "schreib Dienstag", dann entwerfe ich ihn.
```

Schreib den Plan nach `~/.claude/instagram/plan.md`, damit die anderen Skills
ihn lesen können. Nichts wird irgendwo eingeplant oder gepostet. Das ist ein
Plan, und der Nutzer setzt ihn um.
