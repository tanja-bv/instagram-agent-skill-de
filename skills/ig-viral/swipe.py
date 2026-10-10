#!/usr/bin/env python3
"""
swipe.py - rankt gesammelte Reels danach, wie weit sie ihr eigenes Konto
geschlagen haben, benennt die Hook-Formel und schreibt das Swipe-File.

Der ganze Sinn dieses Skripts ist eine Korrektur: Reine Aufrufe sind kein
Beleg. Ein Konto mit 2.000.000 Followern und 400.000 Aufrufen hatte einen
ruhigen Tag. Ein Konto mit 4.000 Followern und 400.000 Aufrufen hat etwas
gefunden. Gerankt wird nach dem Vielfachen über der eigenen Basis des Kontos,
der einzigen Version von "ging viral", aus der man etwas lernen kann.

Eingabe ist eine tabulatorgetrennte Datei, die du beim Durchschauen füllst,
ein Reel pro Zeile, mit einer Kopfzeile (deutsch oder englisch):

    konto     follower   median   aufrufe   hook
    @firma    4800       1100     41200     Was Ihnen bei Ausschreibungen keiner sagt

`median` sind die typischen Aufrufe der letzten Reels dieses Kontos und die
bessere Basis. Hast du nur `follower`, lass median weg, das Skript sagt es
dann. Zahlen dürfen deutsch (41.200), englisch (41,200) oder kurz (41K,
1,2 Mio., 12 Tsd.) sein. `hook` ist die erste Zeile, gesprochen oder
eingeblendet, in ihren Worten.

Hooks englischsprachiger Konten werden mit den englischen Mustern aus
hooks.json (`match_en`) zugeordnet. Ihr Hook-Score bleibt leer, weil
hookscore.py deutsche Heuristiken nutzt und englische Zeilen falsch bewerten
würde.

Aufruf
  python3 swipe.py erfasst.tsv
  python3 swipe.py erfasst.tsv --out ~/.claude/instagram/swipe.md
  python3 swipe.py erfasst.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")

try:                                              # optional: Hooks auch bewerten
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
    import sprache                                # noqa: E402
except Exception:                                 # ig-viral allein kopiert
    score_hook = None
    sprache = None

SPALTEN = {"konto": "account", "account": "account", "follower": "followers",
           "followers": "followers", "median": "median", "aufrufe": "views",
           "views": "views", "hook": "hook"}
ENGLISCH_RE = re.compile(r"(?i)\b(?:the|you|your|this|that|what|nobody|stop|how|why|i|my|we|is|are)\b")
DEUTSCH_RE = re.compile(r"(?i)\b(?:der|die|das|und|nicht|ich|wir|sie|du|ist|sind|ein|eine|was|wie|für)\b")


def load_formulas(path):
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    out = []
    for i in order:
        if i not in by_id:
            continue
        h = by_id[i]
        de = re.compile(h["match"], re.IGNORECASE)
        en = re.compile(h["match_en"], re.IGNORECASE) if h.get("match_en") else None
        out.append((h["id"], h["name"], de, en))
    return out


def ist_englisch(hook):
    return len(ENGLISCH_RE.findall(hook)) > len(DEUTSCH_RE.findall(hook))


def classify(hook, formulas):
    if not formulas:
        return None, "nicht zugeordnet"
    englisch = ist_englisch(hook)
    for fid, name, de, en in formulas:
        pattern = en if englisch else de
        if pattern is not None and pattern.search(hook):
            return fid, name
    return None, "nicht zugeordnet"


def parse_anzahl(cell):
    """'41.200' / '41,200' / '41K' / '1,2 Mio.' / '12 Tsd.' -> int."""
    c = (cell or "").strip().lower().replace(" ", "").rstrip(".")
    if not c:
        return None
    faktor = 1
    for suffix, f in (("mio", 10 ** 6), ("m", 10 ** 6), ("tsd", 1000), ("k", 1000), ("t", 1000)):
        if c.endswith(suffix):
            faktor, c = f, c[: -len(suffix)].rstrip(".")
            break
    if faktor > 1:
        c = c.replace(",", ".")
        try:
            return int(round(float(c) * faktor))
        except ValueError:
            return None
    digits = re.sub(r"[^\d]", "", c)
    return int(digits) if digits else None


def read_rows(path):
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    head = [SPALTEN.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        r["views"] = parse_anzahl(r.get("views")) or 0
        for k in ("followers", "median"):
            r[k] = parse_anzahl(r.get(k))
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["englisch"] = ist_englisch(r["hook"])
        r["words"] = len(re.findall(r"[\wäöüß€%'’-]+", r["hook"]))
        if score_hook and not r["englisch"]:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts, counts_bottom = {}, {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    for r in bottom:
        counts_bottom[r["formula"]] = counts_bottom.get(r["formula"], 0) + 1
    return {
        "baseline": "Konto-Median" if used_median else "Followerzahl",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "bottom_formulas": counts_bottom,
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "nicht zugeordnet"),
        "englisch": sum(1 for r in ranked if r["englisch"]),
    }


def tsd(n):
    return f"{n:,}".replace(",", ".")


def komma(x, stellen=1):
    return f"{x:.{stellen}f}".replace(".", ",")


def render(a, out=sys.stdout):
    head = (f"SWIPE-FILE  ·  {a['n']} Reels  ·  {a['accounts']} Konten  ·  "
            f"Basis: {a['baseline']}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{komma(r['outlier'])}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        print(f"  {mult:>7}  hook {score:>3}  {fid} {r['formula'][:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {tsd(r['views']):>9}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("WAS ÜBERREPRÄSENTIERT IST", file=out)
    if a["top_formulas"]:
        teile = []
        for name, c in a["top_formulas"][:4]:
            unten = a["bottom_formulas"].get(name, 0)
            teile.append(f"{name} {c}x (unten {unten}x)")
        print("  oberes Drittel:        " + ", ".join(teile), file=out)
    if a["top_hook_score"] is not None and a["bottom_hook_score"] is not None:
        print(f"  Hook-Score (Median):   oben {a['top_hook_score']:.0f}  "
              f"vs unten {a['bottom_hook_score']:.0f}", file=out)
    print(f"  Hook-Länge (Median):   oben {komma(a['top_words'], 0)} Wörter  "
          f"vs unten {komma(a['bottom_words'], 0)} Wörter", file=out)
    print(f"  nicht zugeordnet:      {a['unclassified']} von {a['n']}. Lies die von Hand, "
          "dort versteckt sich eine Formel, die du noch nicht hast.", file=out)
    if a["englisch"]:
        print(f"  englisch:              {a['englisch']} Hook{'s' if a['englisch'] != 1 else ''}, ohne Hook-Score. Formel übernehmen, "
              "nie den Wortlaut.", file=out)
    print("\n  Eine von Hand gesammelte Stichprobe ist ein Hinweis, kein Beweis. Zwölf Reels "
          "zeigen\n  nichts, vierzig über sechs Konten zeigen etwas. Sammel mehr, bevor du es "
          "glaubst.\n", file=out)


def to_markdown(a):
    lines = ["# Swipe-File", "",
             f"{a['n']} Reels aus {a['accounts']} Konten. "
             f"Gerankt nach Vielfachem über {a['baseline']}.", ""]
    for r in a["reels"]:
        mult = f"{komma(r['outlier'])}x" if r["outlier"] else "?"
        fid = f"#{r['formula_id']} " if r["formula_id"] else ""
        lines += [f"## {mult}  {fid}{r['formula']}  ({r.get('account', '')})",
                  f"- Aufrufe: {tsd(r['views'])}  Basis: {tsd(r['baseline']) if r['baseline'] else '?'}",
                  f"- Hook-Score: {r['hook_score'] if r['hook_score'] is not None else '-'}  "
                  f"Wörter: {r['words']}" + ("  (englisch)" if r["englisch"] else ""),
                  f"- Hook: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Rankt gesammelte Reels nach Outlier-Vielfachem.")
    ap.add_argument("input", nargs="?", default="-", help="TSV-Datei, oder - für stdin")
    ap.add_argument("--hooks", default=HOOKS, help="Pfad zu ig-reel/hooks.json")
    ap.add_argument("--out", help="das Swipe-File zusätzlich als Markdown hierhin schreiben")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("keine brauchbaren Zeilen. Nötig ist eine tabulatorgetrennte Datei mit "
              "mindestens aufrufe und hook.", file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("Hinweis: hooks.json nicht gefunden, Formeln bleiben unbenannt. --hooks angeben.",
              file=sys.stderr)
    if score_hook is None:
        print("Hinweis: hookscore.py nicht importierbar, Hook-Scores übersprungen.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        open(path, "w", encoding="utf-8").write(to_markdown(a))
        print(f"geschrieben: {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
