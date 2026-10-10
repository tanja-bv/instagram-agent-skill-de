#!/usr/bin/env python3
"""
beats.py - macht aus einem Reel-Skript ein Beat-Sheet mit Zeitmarken, bevor
du drehst.

Schätzt, wie lange jede Zeile zum Sprechen braucht, stapelt sie zu
Timecodes und markiert die vier Dinge, die ein Reel im Schnitt umbringen:
ein Hook, der über die Drei-Sekunden-Marke läuft, ein Beat, der lang genug
ist, dass der Zuschauer geht, eine Reihe von Zeilen ohne irgendetwas
Konkretes, und eine Gesamtlänge, die nicht zu dem passt, was du vorhattest.

Die Zeiten werden über Silben geschätzt, nicht über Wörter, weil deutsche
Wörter lang sind: "Arbeitszeiterfassung" ist ein Wort und dauert so lange wie
sechs kurze. Zahlen werden so gezählt, wie man sie sagt ("18.000 €" sind
sechs Silben). Das reicht, um einen Schnitt zu planen, und ersetzt keine
Aufnahme. Stell dein eigenes Tempo mit --sps ein, sobald du dich einmal
gestoppt hast: Skript laut lesen, Sekunden messen, Silbenzahl aus dem Kopf
dieser Ausgabe durch die Sekunden teilen. Die meisten landen zwischen 4 und 5,5.

Aufruf
  python3 beats.py skript.txt
  python3 beats.py skript.txt --target 30
  python3 beats.py skript.txt --sps 5 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py skript.txt --json
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sprache  # noqa: E402

HOOK_FENSTER = 3.0       # Sekunden. Danach hat der Daumen schon entschieden.
MAX_BEAT = 4.0           # Sekunden auf einer Idee, ohne dass sich im Bild etwas ändert.
ABSTRAKT_SERIE = 3       # Beats hintereinander ohne etwas Prüfbares.


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}".replace(".", ",")


def zahl(x, stellen=1):
    return f"{x:.{stellen}f}".replace(".", ",")


def split_beats(raw, sps):
    """Eine Zeile ist ein Beat, außer sie ist zu lang für einen."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if sprache.silben(line) / sps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Langer Absatz: an Satzenden brechen, damit die Zeiten etwas bedeuten.
        buf = ""
        for part in sprache.saetze(line):
            candidate = (buf + " " + part).strip()
            if buf and sprache.silben(candidate) / sps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, sps=4.5, target=None):
    beats = split_beats(raw, sps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = sprache.silben(text)
        dur = n / sps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "silben": n,
            "woerter": len(sprache.woerter(text)),
            "text": text,
            "konkret": len(sprache.konkrete_marker(text)),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_FENSTER:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MITTE"

    notes = []
    if rows[0]["dur"] > HOOK_FENSTER:
        rows[0]["flags"].append(f"Hook dauert {zahl(rows[0]['dur'])}s, über der "
                                f"{HOOK_FENSTER:.0f}-Sekunden-Marke")
        notes.append(f"Beat 1 braucht {zahl(rows[0]['dur'])}s. Kürz ihn auf höchstens "
                     f"{int(HOOK_FENSTER * sps)} Silben, sonst landet der Hook, nachdem die "
                     "Entscheidung gefallen ist.")
    if rows[0]["konkret"] == 0:
        notes.append("Beat 1 hat keine Zahl und keinen Namen. Hooks ohne etwas Prüfbares "
                     "sind die, die weggewischt werden.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{zahl(r['dur'])}s auf einem Beat")
    lange = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if lange:
        notes.append(f"Beat {', '.join(map(str, lange))} läuft über {MAX_BEAT:.0f}s. Entweder "
                     "die Zeile teilen oder innerhalb der Zeile das Bild wechseln. Ein "
                     "stehendes Bild ist die Stelle, an der Leute gehen.")

    serie, start = 0, None
    for r in rows:
        if r["konkret"] == 0:
            serie += 1
            start = start if start is not None else r["n"]
            if serie == ABSTRAKT_SERIE:
                notes.append(f"Beats {start}-{r['n']} haben nichts Konkretes. Pack eine Zahl, "
                             "einen Namen oder einen Preis in einen davon.")
        else:
            serie, start = 0, None

    # Führt die letzte Zeile zurück zur ersten?
    def staemme(text):
        return {sprache.stamm(w): w for w in sprache.woerter(text)
                if w.lower() not in sprache.STOPP and len(w) > 2}
    erste, letzte = staemme(rows[0]["text"]), staemme(rows[-1]["text"])
    loop = sorted({erste[s] for s in erste.keys() & letzte.keys()})
    if loop:
        notes.append(f"Loop: Der letzte Beat greift \"{', '.join(loop[:3])}\" aus dem Hook auf. "
                     "Zweites Anschauen ist geschenkte Reichweite.")
    else:
        notes.append("Kein Loop. Der letzte Beat teilt kein Wort mit dem Hook, das Video endet "
                     "flach. Ein Wort aus Beat 1 wiederholen ist der billigste Replay, den es gibt.")

    if sprache.anrede(raw)["du"] and sprache.anrede(raw)["sie"]:
        notes.append("Das Skript duzt und siezt. Eins von beiden, durchgehend.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"Länge passt ({zahl(total)}s bei Ziel {zahl(target, 0)}s).")
        elif delta > 0:
            notes.append(f"{zahl(delta)}s über dem Ziel. Streich etwa {int(delta * sps)} Silben.")
        else:
            notes.append(f"{zahl(-delta)}s unter dem Ziel. Entweder etwa {int(-delta * sps)} "
                         "Silben ergänzen oder kürzer drehen. Kürzer ist meistens richtig.")

    return {
        "sps": sps, "target": target,
        "total_seconds": round(total, 2),
        "total_silben": sum(r["silben"] for r in rows),
        "total_woerter": sum(r["woerter"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"BEAT-SHEET  ·  {a['total_silben']} Silben  ·  ~{zahl(a['total_seconds'])}s "
            f"bei {zahl(a['sps'])} Silben/s"
            + (f"  ·  Ziel {zahl(a['target'], 0)}s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    for r in a["beats"]:
        label = f"{r['label']:<8}" if r["label"] else " " * 8
        print(f"  {tc(r['start'])}  {zahl(r['dur']):>4}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<8}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Macht aus einem Reel-Skript ein Beat-Sheet.")
    ap.add_argument("input", nargs="?", default="-", help="Skriptdatei, oder - für stdin")
    ap.add_argument("--sps", type=float, default=4.5,
                    help="Sprechtempo in Silben pro Sekunde (Standard 4,5)")
    ap.add_argument("--target", type=float, help="Ziellänge in Sekunden")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, sps=args.sps, target=args.target)
    if not a:
        print("leeres Skript", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
