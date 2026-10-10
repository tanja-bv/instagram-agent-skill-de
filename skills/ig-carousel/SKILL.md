---
name: ig-carousel
description: >-
  Ein Instagram-Karussell bauen: das Cover, das den Swipe holt, den Text Slide
  für Slide und die 1080x1350-Dateien zum Hochladen. Für B2B: Checklisten,
  Prozess-Schritte, Vorher/Nachher-Abläufe, Kalkulationen. Nutzen, wenn der
  Nutzer sagt "Karussell", "Carousel", "Slides", "Swipe-Post", "mach daraus
  ein Karussell", "Checkliste als Post", "Ablauf in Slides", oder eine Idee hat,
  die nach Liste oder Schritten aussieht und als Einzelbild untergehen würde.
---

# ig-carousel

Karussells halten Leute am längsten im Grid, weil ein Swipe eine Interaktion
ist und ein Scroll nicht. Sie bekommen außerdem eine zweite Chance: Instagram
kann ein Karussell jemandem, der beim ersten Mal nicht reagiert hat, noch
einmal ab einer späteren Slide zeigen. Slide zwei muss also auch allein stehen
können.

Das Format belohnt eine Idee, in Schritte zerlegt. Es bestraft eine Caption,
die in Stücke geschnitten wurde.

## Wann statt eines Reels

Nimm ein Karussell, wenn die Idee **eine Reihenfolge hat und nochmal gelesen
werden muss**: Schritte, ein Modell mit Teilen, ein Vorher/Nachher, eine Liste,
die man sich als Screenshot speichert. Nimm ein Reel, wenn die Idee Bewegung
hat, ein Gesicht braucht oder eine Pointe, die man passieren sehen muss.

Ist die Idee nur eine Behauptung, ist sie keins von beidem. Gib sie an
`/ig-reel` und sag das.

Im B2B ist das Karussell das Format, das am häufigsten gespeichert und intern
weitergeschickt wird, vom Objektleiter an die Geschäftsführung, vom Einkauf an
die Kollegin. Vier Formen tragen fast immer:

| Form | Beispiel | warum es funktioniert |
| --- | --- | --- |
| **Checkliste** | "9 Punkte, die in jede Reinigungsausschreibung gehören" | wird gespeichert und beim nächsten Mal wirklich benutzt |
| **Prozess-Schritte** | "So läuft der erste Monat mit uns: Begehung, Angebot, Einarbeitung, Abnahme" | nimmt die Angst vor dem Wechsel, beantwortet das Erstgespräch vorab |
| **Vorher/Nachher-Ablauf** | "Dienstplan vorher: 3 Excel-Listen, 40 WhatsApp-Nachrichten. Nachher: eine App." | zeigt den Unterschied am Ablauf, nicht am Hochglanzfoto |
| **Kalkulation** | "Was eine Stunde Sicherheitsdienst wirklich kostet, Position für Position" | erklärt den eigenen Preis, bevor der Einkauf nachfragt |

Bei Kalkulationen: nur Zahlen, die der Nutzer belegen kann, sonst
`{{Ihre Zahl}}` bzw. `{{deine Zahl}}`. Lohnangaben nach KV oder Tarif mit
Stand und Quelle; B2B-Publikum rechnet nach. Kundennamen, Logos und Zahlen von
Kunden nur mit schriftlicher Freigabe, sonst Branche, Größe, Ergebnis.

## Aufbau

6 bis 10 Slides. Erlaubt sind 20, und 20 sind fast immer ein Buch, das keiner
zu Ende liest. Unter 5 kommt der Swipe gar nicht erst in Gang.

```
1         COVER     der Hook. Höchstens 6 Wörter, so groß, dass er im Grid als
                    Thumbnail lesbar ist. Eine Zeile Versprechen darunter.
2         EINSATZ   warum das wichtig ist, in einem Satz. Diese Slide ist auch
                    ein zweites Cover, also keine Vorrede.
3 bis N   EINE IDEE PRO SLIDE. Eine Überschrift mit 3 bis 7 Wörtern, darunter
                    höchstens 25 Wörter. Braucht eine Slide einen Absatz, sind
                    es zwei Slides.
N+1       RECAP     alles als Liste. Das ist die Screenshot-Slide.
LETZTE    CTA       eine Handlung. Speichern, ein Keyword kommentieren oder
                    folgen. Eine.
```

## Regeln für den Slide-Text

- **Das Cover macht 80 % des Ergebnisses.** Sechs Wörter. Groß. Der Rest des
  Karussells rettet kein Cover, bei dem keiner swipet.
- **Deutsche Wörter sind lang.** Im Cover höchstens ca. 20 Zeichen pro Zeile,
  höchstens drei Zeilen. "Unterhaltsreinigungsvertrag" hat 27 Zeichen und
  passt in keiner lesbaren Größe auf eine Zeile. Entweder umformulieren
  ("Vertrag für die Unterhaltsreinigung") oder selbst an einer Wortfuge
  trennen: "Unterhalts-" in Zeile eins, "reinigungsvertrag" in Zeile zwei.
  Nie den Browser mitten im Wort umbrechen lassen. Gib im Cover die
  Zeilenumbrüche vor und zähl die Zeichen.
- **Für den Grid-Ausschnitt bauen.** Das Profil-Grid schneidet auf ein
  Hochformat zu, und das genaue Seitenverhältnis hat sich schon mehrmals
  geändert. Bau in 1080x1350 und halt den Cover-Text deutlich in der Mitte, mit
  mindestens 120 Pixeln Abstand zu jedem Rand. Dann ist der Ausschnitt egal.
- **Slides nummerieren** (3/8). Leute swipen eher zu Ende, wenn sie das Ende
  sehen.
- **Keine Slide ist ein Absatz.** Geht es nicht in 25 Wörtern, teilen.
- **Die Recap-Slide wird gespeichert und weitergeschickt.** Weiterleitungen
  sind das stärkste Signal, das ein Post bekommen kann, und im B2B ist das
  genau der Weg in die Geschäftsführung. Mach sie eigenständig und ohne Kontext
  lesbar.
- **Der Handle auf jede Slide**, klein, Ecke unten. Screenshots reisen ohne
  Absender.
- **Anrede einheitlich**, aus `~/.claude/instagram/voice.md`. Fehlt sie, frag
  einmal; ohne Antwort Sie. Cover, Slides, CTA und Caption in derselben
  Anrede.
- **Alternativtext mindestens für das Cover.** Den lesen Screenreader und
  Instagram.

## Die Dateien bauen

Instagram will 1080x1350 (4:5), JPEG oder PNG, bis zu 20 Elemente. Bau es als
HTML und druck jede Slide einzeln:

```bash
# ein <section> pro Slide, 1080x1350, page-break-after: always
# dann Chrome headless --print-to-pdf, oder jedes HTML-zu-Bild, das du schon nutzt
```

Schreib das HTML mit `width:1080px; height:1350px`, einer einzigen
Akzentfarbe und keiner Schrift unter 32px, weil das auf einem Handy in einem
Drittel der echten Größe gelesen wird. Hat das Projekt einen Brand-Skill oder
ein Design-System, nimm das und erfinde keine Palette.

Für deutschen Text zusätzlich:

- **Umlaute und ß müssen in der Schrift sitzen.** Prüf vor dem Bauen mit einer
  Testzeile: `ÄÖÜ äöü ß ẞ € 18.000 € 3,5 %`. Fehlt ein Zeichen, springt der
  Browser für genau diesen Buchstaben auf eine andere Schrift, und "Gebäude"
  sieht aus wie geflickt. Webfonts mit dem Zeichensatz latin-ext laden, sonst
  fehlt oft das große ẞ. Das €-Zeichen extra prüfen, jede Kalkulation hängt
  daran.
- **Großbuchstaben-Cover:** `text-transform: uppercase` macht aus ß ein SS
  ("STRASSE"). Das ist korrekt. Wer ẞ will, schreibt es direkt in den Text und
  prüft, dass die Schrift es hat.
- **Silbentrennung:** `<html lang="de">` setzen. Für Fließtext auf den Slides
  `hyphens: auto` erlauben, im Cover nicht: Dort trennst du von Hand, mit
  `&shy;` an der Wortfuge oder einem festen Umbruch. Automatische Trennung
  kennt Silben, nicht Wortfugen, und setzt womöglich "Abnahmepro-tokoll".
  Lesbar ist "Abnahme-protokoll". Headless-Chrome hat nicht immer
  Trennwörterbücher geladen, also im fertigen Bild prüfen, ob überhaupt
  getrennt wurde.
- **Schriftgröße am längsten Wort festmachen**, nicht am kürzesten. Erst das
  längste Wort jeder Slide in der geplanten Größe setzen, dann den Rest.

## Ausgabe

Zuerst der Text Slide für Slide, als nummerierte Liste, die der Nutzer in zehn
Sekunden liest und ändern kann, bevor irgendetwas gerendert wird. Im Cover mit
den Zeilenumbrüchen, wie sie gesetzt werden. Dann die **Caption**, die bei
einem Karussell Fall B (Hook in der Caption) in `/ig-caption` ist, also der Fall, in dem die Caption
selbst Inhalt ist: Das Cover hat seine sechs Wörter schon verbraucht.

Beides durch `/ig-human`. Die Dateien erst bauen, wenn der Nutzer den Text
freigegeben hat.

```
KARUSSELL  ·  8 Slides  ·  Anrede: Sie

1  COVER   WAS EINE STUNDE
           REINIGUNG KOSTET
           Unsere Kalkulation, Position für Position.
2  EINSATZ Wer unter {{Ihre Zahl}} € pro Stunde anbietet, zahlt bei jedem Auftrag drauf.
3          DER LOHN NACH KV
           {{Ihre Zahl}} € brutto pro Stunde. Das ist die Basis, nicht der Preis.
4          LOHNNEBENKOSTEN
           Sozialversicherung, Urlaub, Feiertage, Ausfallzeiten.
...
7  RECAP   Alle Positionen untereinander, mit Summe.
8  CTA     Kommentieren Sie KALKULATION, dann schicken wir Ihnen die Vorlage.

Caption: Fall B (Hook in der Caption), Hook in Zeile 1, eine Bitte, 3 Hashtags.
```

Nichts wird hochgeladen. Der Nutzer postet selbst.
