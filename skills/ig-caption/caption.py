#!/usr/bin/env python3
"""
caption.py - prüft eine Instagram-Caption und zeigt genau das, was der Feed
vor dem "... mehr" zeigt.

Instagram gibt einer Caption im Feed etwa 125 Zeichen und versteckt den Rest
hinter einem Tippen. Fast jede Caption, die scheitert, scheitert dort: Der
Hook steht in Satz drei, die erste Zeile ist eine Begrüßung, oder alles
beginnt mit einem Hashtag. Das Skript druckt das sichtbare Fenster als Kasten,
damit du es liest wie ein Fremder beim Scrollen, und prüft dann die Dinge, die
sich zu prüfen lohnen. Für deutsche B2B-Captions kommt eine Prüfung dazu, die
das Original nicht brauchte: ob du duzt und siezt im selben Text.

Die 125 Zeichen sind eine Näherung. Die echte Zahl hängt vom Gerät, der
Schriftgröße und den Zeilenumbrüchen ab, darum willst du Abstand statt einer
Caption, die exakt bei 125 endet. Deutsche Sätze sind länger als englische:
plan das Ende des ersten Gedankens bei 100 bis 110 Zeichen. Mit --truncate
testest du ein engeres Fenster.

Aufruf
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "gebäudereinigung wien,dienstplan app"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import os
import re
import sys
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sprache  # noqa: E402

LIMIT = 2200             # Harte Grenze von Instagram für Captions.
TRUNCATE = 125           # Ungefähr dort schneidet der Feed auf "... mehr".
HASHTAG_LIMIT = 5        # Obergrenze pro Post oder Reel seit 18. Dezember 2025,
                         # vorher 30. Angekündigt vom @Creators-Konto: weniger
                         # (bis zu 5), dafür gezieltere Hashtags.

HASHTAG_RE = re.compile(r"(?:^|\s)(#\w+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app|"
                     r"at|de|ch|eu|info|biz|wien|berlin)/\S*", re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")

CTAS = [
    (re.compile(r"\b(?:[Kk]ommentier\w*|[Ss]chreib\w*|[Tt]ipp\w*)\b[^.!?\n]{0,40}?[\"„“]?\b[A-ZÄÖÜ]{3,}\b"),
     "Keyword kommentieren"),
    (re.compile(r"(?i)\b(?:schreib mir|schreibt mir|schreiben sie (?:mir|uns)|schick mir|"
                r"schicken sie (?:mir|uns)|dm an uns|melde dich|meldet euch|melden sie sich)\b"),
     "DM schreiben"),
    (re.compile(r"(?i)\b(?:per dm|in die dm|per direktnachricht|per nachricht)\b"), "DM schreiben"),
    (re.compile(r"(?i)\b(?:speicher\w*|merk dir|merken sie sich)\b[^.!?\n]{0,25}\b(?:das|den|die|diesen|"
                r"diese|beitrag|post)\b"), "speichern"),
    (re.compile(r"(?i)\b(?:teil\w*|schick\w*|leite\w*)\b[^.!?\n]{0,30}\b(?:weiter|kolleg\w*|team|chef\w*|"
                r"an jemanden|mit jemandem)\b"), "teilen"),
    (re.compile(r"(?i)\b(?:folg\w*|folgen sie)\b[^.!?\n]{0,15}\b(?:mir|uns|für mehr)\b"), "folgen"),
    (re.compile(r"(?i)\blink (?:in (?:der |meiner |unserer )?bio|im profil)\b"), "Link in Bio"),
    (re.compile(r"(?i)\b(?:wisch|swipe|tipp)\w*\b[^.!?\n]{0,10}\b(?:durch|nach links|weiter|rüber)\b"),
     "wischen"),
    (re.compile(r"(?i)\b(?:sag mir|sagt mir|sagen sie (?:mir|uns)|was meinst du|was meinen sie|"
                r"welche[rsn]? (?:nimmst|nehmt|nehmen sie|würdest|würden sie)|wie macht ihr|"
                r"wie machen sie|wie löst ihr|wie lösen sie)\b"), "Frage beantworten"),
    (re.compile(r"(?i)\b(?:termin|demo|erstgespräch|rückruf|beratungsgespräch|angebot anfordern|"
                r"kostenlos testen|testzugang|probemonat)\b"), "Termin oder Demo"),
]

FUELL_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
              "#trending", "#instagood", "#love", "#liebe", "#follow", "#like4like",
              "#reels", "#reelsinstagram", "#viralreels", "#instadaily", "#motivation",
              "#erfolg", "#mindset", "#business", "#success", "#entrepreneur",
              "#unternehmer", "#selbstständig", "#marketing", "#instagram"}


def visible_window(text, cut):
    """Was der Feed zeigt. Instagram schneidet mitten im Wort, also das hier auch."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  WAS DER FEED ZEIGT", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... mehr" if truncated else "(passt komplett)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=TRUNCATE, keywords=None):
    text = text.rstrip()
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    ohne_links = LINK_RE.sub(" ", stripped)
    asks = list(dict.fromkeys(name for pattern, name in CTAS if pattern.search(ohne_links)))
    # "Kommentiere X, dann kommt es per DM" ist ein CTA, nicht zwei: die DM ist
    # die Auslieferung. Als eigener CTA zählt die DM nur ohne Keyword.
    if "Keyword kommentieren" in asks and "DM schreiben" in asks and not CTAS[1][0].search(ohne_links):
        asks.remove("DM schreiben")
    filler = [t for t in tags if t.lower() in FUELL_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]
    anrede = sprache.anrede(stripped)
    konkret = sprache.konkrete_marker(window)

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LÄNGE", "FEHLER" if chars > LIMIT else "OK",
        f"{chars} / {LIMIT} Zeichen" + (f", {chars - LIMIT} über der Grenze"
                                        if chars > LIMIT else ""))

    if not first_line:
        add("ERSTE ZEILE", "FEHLER", "die Caption beginnt mit einer Leerzeile")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("ERSTE ZEILE", "FEHLER",
            "beginnt mit Hashtag oder Erwähnung, auf dem einen Platz, der einen Satz verdient")
    elif re.match(r"(?i)\s*(?:hallo|hi|hey|servus|moin|guten (?:morgen|tag)|liebe |wir freuen uns)",
                  first_line):
        add("ERSTE ZEILE", "FEHLER",
            "beginnt mit Begrüßung oder Firmenfreude. Die ersten Zeichen gehören dem Hook")
    elif len(first_line) > cut:
        add("ERSTE ZEILE", "WARN",
            f"{len(first_line)} Zeichen, wird bei {cut} mitten im Gedanken geschnitten. "
            "Gut, wenn der Schnitt ein Cliffhanger ist, schlecht, wenn es ein Nebensatz ist")
    else:
        add("ERSTE ZEILE", "OK", f"{len(first_line)} Zeichen, landet komplett")

    add("HOOK KONKRET", "OK" if konkret else "WARN",
        f"{len(konkret)} Zahl(en) oder Name(n) im sichtbaren Fenster"
        + ("" if konkret else " - nichts Prüfbares vor dem Tippen"))

    if len(tags) > HASHTAG_LIMIT:
        add("HASHTAGS", "FEHLER", f"{len(tags)} Tags, über Instagrams Grenze von {HASHTAG_LIMIT}. "
                                  "Tags nach dem fünften zählen nicht, und der Block wirkt alt")
    elif len(tags) == HASHTAG_LIMIT and filler:
        add("HASHTAGS", "WARN", f"{len(tags)} Tags, an der Grenze, und "
                                f"{len(filler)} davon generisch. Gib die fünf für Themen aus")
    elif filler:
        add("HASHTAGS", "WARN", f"{len(tags)} Tags, {len(filler)} davon generisch "
                                f"({', '.join(filler[:3])}). Die beschreiben nichts")
    else:
        add("HASHTAGS", "OK", f"{len(tags)} Tag(s)" + (f": {' '.join(tags)}" if tags else ""))

    if not tags:
        add("HASHTAG-ORT", "OK", "keine Tags zu platzieren")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("HASHTAG-ORT", "WARN", "ein Hashtag steht im sichtbaren Fenster und verbraucht "
                                   "Feed-Platz für ein Etikett")
    else:
        add("HASHTAG-ORT", "OK", "Tags stehen unter dem Schnitt")

    add("LINKS", "WARN" if links else "OK",
        f"{len(links)} Link(s) in der Caption, und Captions sind nicht klickbar. "
        f"Ab in die Bio oder in die DM" if links else "keine toten Links im Text")

    if len(asks) == 1:
        add("EIN CTA", "OK", f"eine Handlungsaufforderung: {asks[0]}")
    elif not asks:
        add("EIN CTA", "WARN", "keine Handlungsaufforderung. Entscheide, wofür dieser Post da ist")
    else:
        add("EIN CTA", "WARN", f"{len(asks)} Aufforderungen ({', '.join(asks)}). "
                               "Zwei Aufforderungen sind so gut wie keine")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "WARN" if density > 4 else "OK",
        f"{len(emoji)} Emoji, {sprache_zahl(density)} pro 100 Zeichen"
        + (" - wirkt wie Deko" if density > 4 else ""))

    if anrede["du"] and anrede["sie"]:
        add("ANREDE", "FEHLER", f"du und Sie gemischt ({anrede['du']}x du, {anrede['sie']}x Sie). "
                                "Eins von beiden, durchgehend")
    elif anrede["du"]:
        add("ANREDE", "OK", "durchgehend du")
    elif anrede["sie"]:
        add("ANREDE", "OK", "durchgehend Sie")
    else:
        add("ANREDE", "OK", "keine direkte Anrede")

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "OK" if not missing else ("WARN" if found else "FEHLER")
        add("SUCHBEGRIFFE", status,
            f"{len(found)}/{len(keywords)} vorhanden"
            + (f", {len(in_window)} im sichtbaren Fenster" if found else "")
            + (f". Fehlt: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FEHLER")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "ÜBERARBEITEN" if fails else ("PRÜFEN" if warns else "FERTIG")

    return {
        "characters": chars, "limit": LIMIT, "truncate_at": cut,
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks, "anrede": anrede,
        "checks": checks, "verdict": verdict,
    }


def sprache_zahl(x):
    return f"{x:.1f}".replace(".", ",")


def render(a, out=sys.stdout):
    head = (f"CAPTION-CHECK  ·  {a['characters']} / {a['limit']} Zeichen  ·  "
            f"{len(a['hashtags'])} Hashtags  ·  {len(a['asks'])} CTA")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    for c in a["checks"]:
        print(f"  {c['status']:<6} {c['check']:<13} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    print(f"  URTEIL  {a['verdict']}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Prüft eine Instagram-Caption.")
    ap.add_argument("input", nargs="?", default="-", help="Caption-Datei, oder - für stdin")
    ap.add_argument("--truncate", type=int, default=TRUNCATE,
                    help=f"Zeichen vor '... mehr' (Standard {TRUNCATE})")
    ap.add_argument("--keywords", default="", help="kommagetrennte Begriffe, unter denen du "
                                                   "gefunden werden willst")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","))
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "FERTIG" else 1)


if __name__ == "__main__":
    main()
