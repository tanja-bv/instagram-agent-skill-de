#!/usr/bin/env python3
"""
humanize.py - entfernt den Maschinen-Fingerabdruck aus einem deutschen Entwurf.

Drei Durchgänge, in dieser Reihenfolge:

  1. UNSICHTBAR  löscht oder normalisiert Zeichen, die eine Tastatur nie
                 erzeugt: Nullbreiten-Verbinder, Wortverbinder, weiche
                 Trennzeichen, BOMs, Unicode-Tag-Zeichen, geschützte und
                 schmale Leerzeichen. Sie überleben Copy-Paste und sind das
                 mechanischste Erkennungszeichen in generiertem Text.
  2. TYPOGRAFIE  Geviertstrich -> Komma, Halbgeviertstrich -> Bindestrich,
                 Auslassungspunkte -> drei Punkte, Aufzählungspunkt -> Strich.
                 Anführungszeichen: Standard "gerade" (so tippt ein Handy
                 meistens), mit --anfuehrung deutsch werden englische “…”
                 zu deutschen „…“. Deutsche „…“ sind kein Fingerabdruck,
                 englische “…” in deutschem Text schon.
  3. FLOSKELN    ersetzt Floskeln aus slop.json, aber nur dort, wo der Ersatz
                 dieselbe Satzposition füllt. Deutsch stellt das Verb an
                 Position zwei: Wer "Zweifellos ist das wichtig" das erste
                 Wort wegnimmt, bekommt "Ist das wichtig", eine Frage. Darum
                 wird "zweifellos" zu "sicher", nicht zu nichts, und alles,
                 was Artikel oder Kasus mitziehen würde, wird nur gemeldet.

Struktur-Muster ("nicht nur X, sondern auch Y", "Hier kommt X ins Spiel",
Dreierreihen, du/Sie-Mix) werden GEMELDET, nie automatisch umgeschrieben. Den
Bau eines Satzes zu ändern braucht Urteilsvermögen, also ist das die Aufgabe
des Modells, nicht die eines Regex.

Aufruf
  python3 humanize.py entwurf.txt
  python3 humanize.py entwurf.txt --report
  pbpaste | python3 humanize.py - --report
  python3 humanize.py entwurf.txt --json
  python3 humanize.py entwurf.txt -o sauber.txt
  python3 humanize.py entwurf.txt --anfuehrung deutsch
"""

import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sprache  # noqa: E402

LEX = os.path.join(HERE, "slop.json")

URL_RE = re.compile(r"https?://\S+|www\.\S+|\S+@\S+\.\S+")
ADJ_ENDUNG = r"(?P<endung>e|en|er|es|em)?"


def load_lexicon(path=LEX):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _cp(spec):
    """'U+200B' -> 0x200B;  'U+E0000-U+E007F' -> (start, end)."""
    if "-" in spec:
        a, b = spec.split("-")
        return (int(a[2:], 16), int(b[2:], 16))
    return int(spec[2:], 16)


def protect_urls(text):
    """URLs durch Platzhalter ersetzen, damit kein Durchgang in einem Link schreibt."""
    found = []

    def stash(m):
        found.append(m.group(0))
        return f"\x00URL{len(found) - 1}\x00"

    return URL_RE.sub(stash, text), found


def restore_urls(text, found):
    for i, url in enumerate(found):
        text = text.replace(f"\x00URL{i}\x00", url)
    return text


def pass_invisible(text, lex):
    """Unsichtbare Zeichen löschen oder zu Leerzeichen machen."""
    hits = []
    for entry in lex["invisible"]:
        cp = _cp(entry["cp"])
        if isinstance(cp, tuple):
            pattern = "[" + re.escape(chr(cp[0])) + "-" + re.escape(chr(cp[1])) + "]"
        else:
            pattern = re.escape(chr(cp))
        n = len(re.findall(pattern, text))
        if n:
            aktion = "gelöscht" if entry["action"] == "delete" else "Leerzeichen"
            hits.append({"name": entry["cp"] + " " + entry["name"], "count": n, "action": aktion})
            text = re.sub(pattern, "" if entry["action"] == "delete" else " ", text)
    stray = [c for c in text if unicodedata.category(c) == "Cf"]
    if stray:
        hits.append({"name": "weitere unsichtbare Formatzeichen", "count": len(stray),
                     "action": "gelöscht"})
        text = "".join(c for c in text if unicodedata.category(c) != "Cf")
    return text, hits


def pass_typographic(text, lex, anfuehrung="gerade"):
    hits = []
    if anfuehrung == "deutsch":
        # Englische Paare “…” und ”…” zu „…“; deutsche Zeichen bleiben stehen.
        n = len(re.findall(r"[“”][^“”„\n]{1,200}”", text))
        if n:
            hits.append({"name": "“…” englische Anführung", "count": n, "to": "„…“"})
            text = re.sub(r"[“”]([^“”„\n]{1,200})”", "„\\1“", text)
        skip = {"„", "“", "‚", "‘", "”"}
    else:
        skip = set()
    for entry in lex["typographic"]:
        ch = entry["from"]
        if ch in skip:
            continue
        n = text.count(ch)
        if not n:
            continue
        hits.append({"name": f"{ch} {entry['name']}", "count": n,
                     "to": entry["to"].strip() or "(Leerzeichen)"})
        if ch in "—―":
            text = re.sub(r"\s*[—―]\s*", ", ", text)
        elif ch in "–‒":
            text = re.sub(r"(\d)\s*[–‒]\s*(?=\d)", r"\1-", text)   # 5–10 -> 5-10
            text = re.sub(r"\s+[–‒]\s+", " - ", text)             # Gedankenstrich -> wie getippt
            text = text.replace(ch, "-")
        else:
            text = text.replace(ch, entry["to"])
    # Ein eingefügtes Komma vor vorhandenen Satzzeichen liest sich falsch.
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*\n", "\n", text)
    return text, hits


def _match_case(src, repl):
    if not repl:
        return repl
    if src.isupper() and len(src) > 1:
        return repl.upper()
    if src[0].isupper():
        return repl[0].upper() + repl[1:]
    return repl


def entry_pattern(entry):
    """Regex für einen Lexikoneintrag. Gibt (pattern, flex) zurück."""
    if entry.get("match"):
        return re.compile(entry["match"], re.IGNORECASE), False
    find = re.escape(entry["find"]).replace(r"\ ", r"\s+")
    flex = entry.get("flex") == "adj"
    end = ADJ_ENDUNG if flex else ""
    tail = r"\b" if re.match(r"\w", entry["find"][-1]) else ""
    return re.compile(r"\b" + find + end + tail, re.IGNORECASE), flex


def pass_lexical(text, lex):
    """Ersetzt Floskeln mit sicherem Ersatz, meldet den Rest. Längste zuerst."""
    hits, flagged = [], []
    entries = sorted(lex["phrases"] + lex["words"], key=lambda e: len(e["find"]), reverse=True)
    for entry in entries:
        pattern, flex = entry_pattern(entry)
        found = [m.group(0) for m in pattern.finditer(text)]
        if not found:
            continue
        if entry.get("replace") is None:
            flagged.append({"find": entry["find"], "count": len(found), "family": entry["family"],
                            "hint": entry.get("hint", "")})
            continue
        hits.append({"find": entry["find"], "replace": entry["replace"] or "(gelöscht)",
                     "count": len(found), "family": entry["family"]})

        def ersetze(m, entry=entry, flex=flex):
            repl = _match_case(m.group(0), entry["replace"])
            if flex:
                repl += m.group("endung") or ""
            return repl
        text = pattern.sub(ersetze, text)
    # Aufräumen nach Löschungen: verwaiste Satzzeichen, doppelte Leerzeichen.
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"(?m)^[ \t]*(?:[,.;:]+[ \t]*)+", "", text)
    text = re.sub(r"(?m)^[ \t](?=\S)", "", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r",\s*([,.;:!?])", r"\1", text)
    text = text.replace("...", "\x00ELL\x00")
    text = re.sub(r"\.\s*\.+", ".", text)
    text = re.sub(r"([!?])\s*\.", r"\1", text)
    text = text.replace("\x00ELL\x00", "...")
    text = re.sub(r"(?m)^[ \t]+$", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, hits, flagged


def scan_structures(text, lex):
    flags = []
    for s in lex["structures"]:
        try:
            pattern = re.compile(s["regex"], re.MULTILINE)
        except re.error:
            continue
        found = pattern.findall(text)
        if found:
            flags.append({"name": s["name"], "count": len(found), "fix": s["fix"]})
    a = sprache.anrede(text)
    if a["du"] and a["sie"]:
        flags.append({"name": f"du und Sie gemischt ({a['du']}x du, {a['sie']}x Sie)",
                      "count": a["du"] + a["sie"],
                      "fix": "Eine Anrede, durchgehend. Welche, steht in voice.md."})
    lens = [len(s.split()) for s in sprache.saetze(text) if len(s.split()) > 2]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        var = sum((n - mean) ** 2 for n in lens) / len(lens)
        cv = (var ** 0.5) / mean if mean else 0
        if cv < 0.35:
            flags.append({
                "name": f"Gleich lange Sätze (Variation {cv:.2f})".replace(".", ","),
                "count": len(lens),
                "fix": "Einen Satz halbieren. Einen anderen lang laufen lassen. Maschinen schreiben gleichmäßig.",
            })
    return flags


GROSS = "A-ZÄÖÜ"
KLEIN = "a-zäöüß"


def restore_capitals(original, text):
    """Eine gelöschte Floskel am Satzanfang lässt das nächste Wort klein.

    Nur für Schreiber, die Satzanfänge großschreiben: Eine bewusst kleine
    Schreibweise ist Stil, kein Artefakt.
    """
    starts = re.findall(rf"(?:^|[.!?]\s+|\n)\s*([{GROSS}{KLEIN}])", original)
    if not starts or sum(1 for c in starts if c.isupper()) * 2 < len(starts):
        return text
    return re.sub(rf"(?:^|(?<=[.!?] )|(?<=[.!?]\n)|(?<=\n))\s*([{KLEIN}])",
                  lambda m: m.group(0)[:-1] + m.group(1).upper(), text)


def humanize(text, lex, anfuehrung="gerade"):
    raw_for_case = text
    text, urls = protect_urls(text)
    text, inv = pass_invisible(text, lex)
    text, typo = pass_typographic(text, lex, anfuehrung)
    text, lexi, flagged = pass_lexical(text, lex)
    text = restore_capitals(raw_for_case, text)
    text = restore_urls(text, urls)
    return text.strip() + "\n", {
        "invisible": inv,
        "typographic": typo,
        "lexical": lexi,
        "flagged": flagged,
        "structures": scan_structures(text, lex),
    }


def render_report(report, out=sys.stderr):
    def head(title):
        print(f"\n{title}\n" + "-" * len(title), file=out)

    total = sum(h["count"] for h in report["invisible"]) \
        + sum(h["count"] for h in report["typographic"]) \
        + sum(h["count"] for h in report["lexical"])

    head("HUMANIZE-BERICHT")
    print(f"{total} Maschinen-Artefakte entfernt, "
          f"{sum(h['count'] for h in report['flagged'])} Floskeln zu prüfen, "
          f"{len(report['structures'])} Struktur-Muster zum Umschreiben", file=out)

    if report["invisible"]:
        head("1. UNSICHTBARE ZEICHEN")
        for h in report["invisible"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['action']}", file=out)
    if report["typographic"]:
        head("2. TYPOGRAFIE")
        for h in report["typographic"]:
            print(f"  {h['count']:>3}x  {h['name']}  -> {h['to']}", file=out)
    if report["lexical"]:
        head("3. FLOSKELN ERSETZT")
        for h in report["lexical"]:
            print(f"  {h['count']:>3}x  {h['find']}  -> {h['replace']}   [{h['family']}]", file=out)
    if report["flagged"]:
        head("4. FLOSKELN ZU PRÜFEN  (nicht ersetzt - Satz umbauen)")
        for h in report["flagged"]:
            print(f"  {h['count']:>3}x  {h['find']}   [{h['family']}]", file=out)
            if h["hint"]:
                print(f"        {h['hint']}", file=out)
    if report["structures"]:
        head("5. STRUKTUR-MUSTER  (nicht automatisch korrigiert - selbst umschreiben)")
        for h in report["structures"]:
            print(f"  {h['count']:>3}x  {h['name']}\n        {h['fix']}", file=out)
    if not any(report.values()):
        head("SAUBER")
        print("  Nichts zu entfernen.", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Entfernt den Maschinen-Fingerabdruck aus einem Entwurf.")
    ap.add_argument("input", nargs="?", default="-", help="Datei, oder - für stdin")
    ap.add_argument("-o", "--out", help="bereinigten Text hierhin schreiben statt auf stdout")
    ap.add_argument("--report", action="store_true", help="Änderungen auf stderr ausgeben")
    ap.add_argument("--json", action="store_true", help="{text, report} als JSON ausgeben")
    ap.add_argument("--lexicon", default=LEX, help="Pfad zu slop.json")
    ap.add_argument("--anfuehrung", choices=["gerade", "deutsch"], default="gerade",
                    help="Anführungszeichen: gerade (Standard) oder deutsch „…“")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    lex = load_lexicon(args.lexicon)
    clean, report = humanize(raw, lex, args.anfuehrung)

    if args.json:
        print(json.dumps({"text": clean, "report": report}, indent=2, ensure_ascii=False))
        return
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(clean)
        print(f"geschrieben: {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(clean)
    if args.report:
        render_report(report)


if __name__ == "__main__":
    main()
