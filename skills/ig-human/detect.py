#!/usr/bin/env python3
"""
detect.py - fünf Prüfungen, die bewerten, wie maschinell ein deutscher Entwurf
wirkt.

Was das ist:  fünf lokale Heuristiken nach den Signalen, auf die öffentliche
KI-Detektoren schauen: Variation der Satzlänge, Konkretheit, Floskelvokabular,
typografischer Fingerabdruck und Stimme. Für Deutsch umgebaut: Konkretheit
zählt Zahlen, Abkürzungen, Marken und Orte statt großgeschriebener Wörter
(im Deutschen ist jedes Substantiv groß), Stimme zählt Abtönungspartikeln und
Kurzformen ("halt", "mal", "gibt's") statt englischer Kontraktionen, und
deutsche „…“ gelten nicht als Fingerabdruck, englische “…” schon. Alles läuft
auf deinem Rechner, nichts wird hochgeladen.

Was das NICHT ist:  GPTZero, Originality, Copyleaks, Winston oder Turnitin.
Es ruft deren APIs nicht auf und kann ihr Urteil nicht versprechen. Es fängt
die Dinge, auf die sie alle schauen, darum bewegt das Reparieren meistens auch
deren Zahlen. Mehr behauptet es nicht.

Jede Prüfung liefert einen MENSCH-Score von 0 bis 100. Höher ist besser.

Aufruf
  python3 detect.py entwurf.txt
  pbpaste | python3 detect.py -
  python3 detect.py entwurf.txt --json
  python3 detect.py vorher.txt nachher.txt      # zwei Entwürfe vergleichen
"""

import argparse
import json
import os
import re
import statistics
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sprache  # noqa: E402
from humanize import entry_pattern  # noqa: E402

LEX = os.path.join(HERE, "slop.json")


def clamp(n):
    return max(0.0, min(100.0, n))


def scale(value, human, machine):
    """Bildet value auf 0-100 ab: human -> 100, machine -> 0."""
    if human == machine:
        return 50.0
    return clamp((value - machine) / (human - machine) * 100)


def komma(x, stellen=1, breite=0):
    return f"{x:{breite}.{stellen}f}".replace(".", ",")


def saetze(text):
    return [s for s in sprache.saetze(text) if len(s.split()) > 2]


def woerter(text):
    return re.findall(rf"[{sprache.LETTERS}']+", text)


def check_rhythmus(text):
    """Menschen variieren die Satzlänge stark. Modelle schreiben gleichmäßig."""
    lens = [len(s.split()) for s in saetze(text)]
    if len(lens) < 4:
        return 50.0, "zu kurz zum Beurteilen"
    mean = statistics.mean(lens)
    cv = statistics.pstdev(lens) / mean if mean else 0
    score = scale(cv, human=0.70, machine=0.22)
    return score, f"Variation {komma(cv, 2)} über {len(lens)} Sätze (Ziel 0,55+)"


def check_konkret(text):
    """Zahlen, Namen, Orte, Abkürzungen. Floskeln sind abstrakt."""
    w = woerter(text)
    if len(w) < 25:
        return 50.0, "zu kurz zum Beurteilen"
    hits = len(sprache.konkrete_marker(text))
    density = hits * 100 / len(w)
    score = scale(density, human=4.0, machine=0.4)
    return score, f"{hits} konkrete Marker, {komma(density)} pro 100 Wörter (Ziel 3+)"


def check_floskeln(text, lex):
    """Dichte des Floskelvokabulars gegen das Lexikon."""
    w = woerter(text)
    if not w:
        return 50.0, "leer"
    hits, found = 0, []
    for entry in lex["words"] + lex["phrases"]:
        pattern, _ = entry_pattern(entry)
        n = len(pattern.findall(text))
        if n:
            hits += n
            found.append(entry["find"])
    density = hits * 100 / len(w)
    score = scale(density, human=0.0, machine=4.0)
    detail = f"{hits} Floskeln, {komma(density)} pro 100 Wörter"
    if found:
        detail += " (" + ", ".join(sorted(found)[:4]) + (", ..." if len(found) > 4 else "") + ")"
    return score, detail


def check_fingerabdruck(text):
    """Zeichen, die eine Handytastatur nicht erzeugt."""
    invisible = sum(1 for c in text if unicodedata.category(c) == "Cf")
    em = text.count("—") + text.count("―")
    # Englische Anführung in deutschem Text: ” gibt es im Deutschen nicht, und
    # “ als öffnendes Zeichen (vor einem Buchstaben) auch nicht.
    englisch = text.count("”") + len(re.findall(r"(?:^|\s)“\w", text))
    ellip = text.count("…")
    nbsp = sum(text.count(c) for c in "    ")
    gedanken = len(re.findall(r"\s–\s", text))
    zuviel_gedanken = max(0, gedanken - 1)
    total = invisible * 4 + em * 2 + englisch + ellip * 0.5 + nbsp + zuviel_gedanken
    per1k = total * 1000 / max(len(text), 1)
    score = scale(per1k, human=0.0, machine=12.0)
    detail = (f"{invisible} unsichtbar, {em} Geviertstrich, {gedanken} Gedankenstrich, "
              f"{englisch} engl. Anführung, {ellip} Auslassung, {nbsp} geschützte Leerzeichen")
    return score, detail


def check_stimme(text, lex):
    """Partikeln, Person, und die Formen, auf die Modelle zurückfallen."""
    st = sprache.stimme(text)
    if st["woerter"] < 25:
        return 50.0, "zu kurz zum Beurteilen"
    per100 = 100 / st["woerter"]
    locker = (st["partikel"] + st["kurzformen"]) * per100
    person = st["person"] * per100
    tells, names = 0, []
    for s in lex["structures"]:
        try:
            n = len(re.compile(s["regex"], re.MULTILINE).findall(text))
        except re.error:
            continue
        if n:
            tells += n
            names.append(s["id"])
    a = sprache.anrede(text)
    if a["du"] and a["sie"]:
        tells += 1
        names.append("du-sie-mix")
    bullets = [len(b.split()) for b in re.findall(r"(?m)^\s*[-*•]\s+(.+)$", text)]
    uniform = (len(bullets) >= 3 and statistics.pstdev(bullets) < 1.6)
    score = (scale(locker, human=2.5, machine=0.0) * 0.35
             + scale(person, human=7.0, machine=1.0) * 0.35
             + clamp(100 - tells * 22) * 0.30)
    if uniform:
        score -= 12
        names.append("gleiche-aufzählung")
    detail = (f"{komma(locker)} Partikeln/Kurzformen, {komma(person)} Personalpronomen "
              f"pro 100 Wörter, {tells} Struktur-Muster")
    if names:
        detail += " [" + ", ".join(names[:4]) + "]"
    return clamp(score), detail


CHECKS = ["SATZRHYTHMUS", "KONKRETHEIT", "FLOSKELDICHTE", "FINGERABDRUCK", "STIMME"]


def run(text, lex):
    results = {
        "SATZRHYTHMUS": check_rhythmus(text),
        "KONKRETHEIT": check_konkret(text),
        "FLOSKELDICHTE": check_floskeln(text, lex),
        "FINGERABDRUCK": check_fingerabdruck(text),
        "STIMME": check_stimme(text, lex),
    }
    scores = [results[c][0] for c in CHECKS]
    # Die schwächste Prüfung zieht das Urteil: Einem Detektor reicht ein Signal.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4
    verdict = "BESTANDEN" if overall >= 70 and min(scores) >= 55 else (
        "PRÜFEN" if overall >= 50 else "AUFFÄLLIG")
    return results, overall, verdict


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render(results, overall, verdict, label=None, out=sys.stdout):
    title = "KI-ERKENNUNG" + (f"  -  {label}" if label else "")
    print("\n" + title, file=out)
    print("=" * max(len(title), 62), file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<14} {bar(score)} {komma(score, 1, 5)}", file=out)
        print(f"  {'':<14} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'MENSCH-SCORE':<14} {bar(overall)} {komma(overall, 1, 5)}   {verdict}", file=out)
    if verdict != "BESTANDEN":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Schwächstes Signal: {weakest}. Das zuerst reparieren.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Bewertet, wie maschinell ein Entwurf wirkt.")
    ap.add_argument("input", nargs="?", default="-", help="Datei, oder - für stdin")
    ap.add_argument("compare", nargs="?", help="zweite Datei, für vorher/nachher")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--lexicon", default=LEX)
    args = ap.parse_args()

    lex = json.load(open(args.lexicon, encoding="utf-8"))
    read = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()

    targets = [(args.input, read(args.input))]
    if args.compare:
        targets.append((args.compare, read(args.compare)))

    payload = []
    for name, text in targets:
        results, overall, verdict = run(text, lex)
        payload.append({
            "source": name,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "human_score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if args.compare else payload[0], indent=2, ensure_ascii=False))
        return

    for (name, text), p in zip(targets, payload):
        results, overall, verdict = run(text, lex)
        render(results, overall, verdict, label=os.path.basename(name) if args.compare else None)
    if args.compare:
        a, b = payload
        delta = b["human_score"] - a["human_score"]
        print(f"  {komma(a['human_score'])} {a['verdict']}  ->  "
              f"{komma(b['human_score'])} {b['verdict']}   ({'+' if delta >= 0 else ''}{komma(delta)})\n")

    sys.exit(0 if payload[-1]["verdict"] == "BESTANDEN" else 1)


if __name__ == "__main__":
    main()
