#!/usr/bin/env python3
"""
hookscore.py - bewertet die erste Zeile eines Reels nach den fünf Dingen, die
starke Hooks gemeinsam haben, und rankt mehrere gegeneinander.

Was das ist:  fünf lokale Heuristiken, auf deinem Rechner aus dem Text allein
berechnet. Sie messen Eigenschaften, die Hooks mit Haltekraft meistens haben:
eine Länge, die man in unter drei Sekunden sagen kann, etwas Konkretes, etwas,
das auf dem Spiel steht, das Wichtige vorne statt hinten, und einen Zuschauer,
auf den die Zeile zielt.

Was das NICHT ist:  eine Reichweitenprognose. Das englische Original wurde an
74 echten Short-Form-Hooks gemessen: Echte Hooks von absichtlich schlechten
trennt es gut (AUC 0,83), die Treffer eines guten Creators von seinen Flops
kaum (AUC 0,56, Münzwurf ist 0,50). Diese deutsche Fassung ist neu gebaut
(Silben statt Wörter, deutsche Einstiege, Zahlwörter, du/Sie) und noch nicht
an einem deutschen Korpus gemessen. Nimm sie für das, was das Original gut
konnte: Begrüßungen, Vorläufe, Hooks ohne Konkretes und Hooks, die fünf
Sekunden dauern, aussortieren. Welcher von zwei ordentlichen Hooks läuft,
entscheiden Gesicht, Schnitt, Ton und wem Instagram es zeigt. Trau der
Retention-Kurve mehr als diesem Skript.

Jede Prüfung liefert 0 bis 100. Höher ist besser.

Aufruf
  python3 hookscore.py hooks.txt              # ein Hook pro Zeile, gerankt
  python3 hookscore.py --hook "18.000 € hat uns eine fehlende Klausel gekostet."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sprache  # noqa: E402

SPRECHTEMPO = 4.5        # Silben pro Sekunde, gesprochen, Reel-Tempo
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Wörter, die etwas aufs Spiel setzen. Kurze Wörter exakt, lange als Stamm,
# weil Deutsch beugt: "verlier" trifft verlieren, verliert, verlierst.
FALLHOEHE_WORT = {
    "nie", "niemals", "kein", "keine", "keinen", "keiner", "keinem", "nicht", "niemand",
    "aber", "nur", "ohne", "gegen", "vs", "versus", "noch", "schon", "erst", "zuerst",
    "statt", "stattdessen", "außer", "bevor", "sollte", "solltest", "solltet", "sollten",
    "eigentlich", "frist", "hör", "hört", "hören", "stopp", "schluss", "gratis", "haft",
    "spät", "teuer", "teurer", "früher", "bisher", "plötzlich", "endlich",
}
FALLHOEHE_STAMM = [
    "verlier", "verlor", "kost", "gekostet", "fehler", "falsch", "aufhör", "kündig",
    "gekündigt", "gefeuert", "entlass", "lösch", "gelöscht", "ersetz", "gespart", "spart",
    "sparen", "verdien", "bezahlt", "strafe", "bußgeld", "abmahn", "klage", "verklagt",
    "illegal", "verbot", "schlimmst", "schlechtest", "teuerst", "hass", "verschwend",
    "verbrannt", "lüge", "gelogen", "wahrheit", "geheim", "versteckt", "geklaut",
    "gestohlen", "problem", "risiko", "gefahr", "warnung", "bereu", "wünschte", "haftung",
    "prüfung", "nachzahl", "ausfall", "fluktuation", "überstunde", "pleite", "insolvenz",
    "verpasst", "absage", "abgesagt", "reklamation", "beschwerde", "storniert",
]
FALLHOEHE_RE = re.compile(r"^(?:" + "|".join(re.escape(s) for s in FALLHOEHE_STAMM) + r")",
                          re.IGNORECASE)


def ist_fallhoehe(token):
    t = token.lower().strip("'’.,!?:")
    return t in FALLHOEHE_WORT or bool(FALLHOEHE_RE.match(t))


# Einstiege, die die erste Sekunde mit nichts füllen.
SCHWACHE_EINSTIEGE = [
    "also", "ok", "okay", "hey", "hi", "hallo", "servus", "moin", "grüß", "guten",
    "liebe", "leute", "willkommen", "herzlich", "heute", "im heutigen", "in diesem",
    "in dem", "kurz", "kurze", "ich wollte", "ich möchte", "ich will", "ich dachte",
    "lass uns", "lasst uns", "lassen sie uns", "habt ihr", "hast du", "haben sie",
    "kennst du", "kennen sie", "kennt ihr", "wusstest du", "wussten sie", "es gibt",
    "das ist", "es ist", "na", "so", "ja", "ähm", "äh", "einfach", "ehrlich gesagt",
    "mal ehrlich", "wenn es um", "ihr kennt", "du kennst", "wir alle", "jeder kennt",
    "wir freuen", "wir sind", "unser unternehmen", "als führender",
]

# Imperative, die die erste Position verdienen.
IMPERATIVE = {
    "hör", "hört", "klau", "kopier", "lösch", "probier", "schau", "lies", "speicher",
    "nutz", "bau", "mach", "schreib", "schick", "nimm", "starte", "kündige",
    "vergiss", "prüf", "rechne", "stell", "frag", "lass", "streich", "spar", "teste",
    "vergleich", "zähl", "check",
}
SIE_IMPERATIV_RE = re.compile(r"^\s*[A-ZÄÖÜ][a-zäöüß]+en Sie\b")

DEALBREAKER = [
    (re.compile(r"(?i)^\s*(?:hör auf zu scrollen|nicht (?:weiter)?scrollen|stopp[!,.]?\s|"
                r"scroll nicht weiter|warte,? nicht scrollen)"),
     "Startet mit \"hör auf zu scrollen\". Wer um Aufmerksamkeit bittet, beweist, dass er sie nicht verdient hat."),
    (re.compile(r"(?i)\b(?:in diesem (?:video|reel|beitrag|post)|im heutigen (?:video|reel|beitrag)|"
                r"heute zeige? ich (?:euch|dir|ihnen)|ich zeige? (?:euch|dir|ihnen) (?:heute|jetzt)|"
                r"heute geht es um|in diesem clip)\b"),
     "Video-Vorlauf. Streich ihn und fang beim Ergebnis an."),
    (re.compile(r"(?i)^\s*(?:hallo|hi|hey|servus|moin|grüß gott|guten (?:morgen|tag|abend)|"
                r"liebe community|herzlich willkommen|willkommen)\b"),
     "Begrüßung. Keiner ist in den Feed gekommen, um begrüßt zu werden."),
    (re.compile(r"(?i)^\s*(?:wir freuen uns|wir sind (?:stolz|froh)|als (?:führender|erfahrener) "
                r"(?:anbieter|partner|dienstleister)|unser unternehmen)\b"),
     "Firmen-Einstieg. Keiner scrollt, um zu hören, dass Sie sich freuen. Fang beim Problem des Kunden an."),
    (HASHTAG_RE,
     "Hashtag im Hook. Hashtags gehören ans Ende der Caption, wenn überhaupt."),
    (EMOJI_RE,
     "Emoji im Hook. Text in Hook-Größe hat Platz für Worte oder für ein Emoji, nicht für beides."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def komma(x, stellen=1, breite=0):
    """81.4 -> '81,4'. Deutsche Dezimalzahl, auf Wunsch rechtsbündig."""
    return f"{x:{breite}.{stellen}f}".replace(".", ",")


def woerter(text):
    return sprache.woerter(text)


def check_laenge(text):
    """Ein Hook muss landen, bevor der Daumen weiterzieht. Etwa zwei Sekunden."""
    n = sprache.silben(text)
    secs = n / SPRECHTEMPO
    chars = len(text.strip())
    if 7 <= n <= 20:
        score = 100.0
    elif n < 7:
        score = clamp(100 - (7 - n) * 14)
    else:
        score = clamp(100 - (n - 20) * 6)
    if chars > 70:                       # zwei Zeilen großer Bildschirmtext
        score -= 12
    return clamp(score), (f"{n} Silben, {len(woerter(text))} Wörter, {chars} Zeichen, "
                          f"~{komma(secs)}s gesprochen (Ziel 7-20 Silben)")


def check_konkret(text):
    """Eine konkrete Sache schlägt drei abstrakte."""
    funde = sprache.konkrete_marker(text)
    n = len(funde)
    score = 15.0 if n == 0 else clamp(45 + n * 30)
    zeige = ", ".join(dict.fromkeys(funde))[:60]
    return score, (f"{n} konkrete Marker" + (f": {zeige}" if funde else
                   " - keine Zahl, kein Name, nichts Prüfbares"))


def check_fallhoehe(text):
    """Spannung, Kosten, Verneinung. Etwas, das der Zuschauer verlieren könnte."""
    w = [x.lower().strip("'’") for x in woerter(text)]
    treffer = sorted({x for x in w if ist_fallhoehe(x)})
    if re.search(r"\d\s?(?:€|euro\b)|€\s?\d", text, re.IGNORECASE):
        treffer.append("ein Betrag")
    n = len(treffer)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} Spannungsmarker" + (f": {', '.join(treffer[:4])}" if treffer else
                                       " - in dieser Zeile steht nichts auf dem Spiel")
    return clamp(score), detail


def check_einstieg(text):
    """Das interessante Wort darf nicht an Position neun stehen."""
    w = woerter(text)
    if not w:
        return 0.0, "leer"
    low = [x.lower().strip("'’") for x in w]
    anfang = " ".join(low[:3])
    abzug, schwach = 0, None
    for s in SCHWACHE_EINSTIEGE:
        if anfang == s or anfang.startswith(s + " ") or low[0] == s:
            abzug, schwach = 30, s
            break
    payload = None
    konkret = {m.lower() for m in sprache.konkrete_marker(text)}
    for i, token in enumerate(low):
        if (ist_fallhoehe(token) or token in konkret or re.match(r"\d", token)
                or token in sprache.ZAHLWOERTER or token in sprache.GELDWOERTER):
            payload = i
            break
    if payload is None:
        base, wo = 30.0, "kein tragendes Wort in der ganzen Zeile"
    elif payload <= 3:
        base, wo = 100.0, f"tragendes Wort an Position {payload + 1}"
    elif payload <= 6:
        base, wo = 70.0, f"tragendes Wort an Position {payload + 1}, könnte nach vorne"
    else:
        base, wo = 40.0, f"tragendes Wort an Position {payload + 1}, zu spät"
    return clamp(base - abzug), wo + (f"; schwacher Einstieg \"{schwach}\"" if schwach else "")


ZIELGRUPPE_RE = re.compile(r"^\s*[A-ZÄÖÜ][\wäöüß\-]{3,}(?:\s+[\wäöüß\-]+){0,6}\s*:")


def check_ansprache(text):
    """Auf einen Zuschauer gezielt, oder ins Leere gesprochen."""
    a = sprache.anrede(text)
    w = [x.lower() for x in woerter(text)]
    if a["du"] and a["sie"]:
        return 40.0, "du und Sie gemischt. Eins von beiden"
    if a["du"]:
        return 100.0, "spricht den Zuschauer an (du)"
    if a["sie"]:
        return 100.0, "spricht den Zuschauer an (Sie)"
    if SIE_IMPERATIV_RE.match(text):
        return 95.0, "Imperativ in der Sie-Form"
    if w and w[0] in IMPERATIVE:
        return 90.0, f"Imperativ am Anfang (\"{w[0]}\")"
    if ZIELGRUPPE_RE.match(text):
        return 90.0, "ruft eine Zielgruppe auf"
    if re.search(r"\b(?:ich|mein\w*|mir|mich|wir|unser\w*|uns)\b", text, re.IGNORECASE):
        return 70.0, "erste Person, kein Zuschauer genannt"
    return 35.0, "dritte Person, keiner im Raum"


CHECKS = ["LÄNGE", "KONKRET", "FALLHÖHE", "EINSTIEG", "ANSPRACHE"]


def run(text):
    results = {
        "LÄNGE": check_laenge(text),
        "KONKRET": check_konkret(text),
        "FALLHÖHE": check_fallhoehe(text),
        "EINSTIEG": check_einstieg(text),
        "ANSPRACHE": check_ansprache(text),
    }
    flags = [msg for pattern, msg in DEALBREAKER if pattern.search(text)]
    a = sprache.anrede(text)
    if a["du"] and a["sie"]:
        flags.append("du und Sie in einer Zeile. Im B2B der Fehler, der sofort nach Vorlage aussieht.")
    scores = [results[c][0] for c in CHECKS]
    # Die schwächste Eigenschaft deckelt den Hook, wie in detect.py: eine
    # schlechte Eigenschaft reicht, damit der Daumen weiterzieht.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "STARK" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "SCHWACH")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    print("\nHOOK-SCORE", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {name:<13} {bar(score)} {komma(score, 1, 5)}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'HOOK-SCORE':<13} {bar(overall)} {komma(overall, 1, 5)}   {verdict}", file=out)
    for f in flags:
        print(f"\n  K.-O.  {f}", file=out)
    if verdict != "STARK":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Schwächste Eigenschaft: {weakest}. Die zuerst reparieren, dann neu laufen lassen.",
              file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    print("\nHOOK-RANKING\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 60 else r["hook"][:57] + "..."
        print(f"{mark} {komma(r['score'], 1, 5)} {r['verdict']:<7} {hook}", file=out)
        print(f"        schwächste: {r['weakest']} ({r['checks'][r['weakest']]['score']:.0f})",
              file=out)
        for f in r["flags"]:
            print(f"        K.-O.: {f}", file=out)
    print("\nDreh den obersten. Liegt der oberste unter 50, ist keiner davon der Hook.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Bewertet einen Reel-Hook nach fünf Eigenschaften.")
    ap.add_argument("input", nargs="?", default="-", help="Datei mit einem Hook pro Zeile, oder -")
    ap.add_argument("--hook", help="einen einzelnen Hook direkt bewerten")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("nichts zu bewerten", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
