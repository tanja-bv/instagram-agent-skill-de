#!/usr/bin/env python3
"""
tests/run.py - prüft, dass der deutsche Fork in sich stimmig ist.

  python3 tests/run.py

Keine Abhängigkeiten. Läuft jedes Skript auf den deutschen Beispielen in
tests/beispiele/ und prüft die Dinge, die beim Umbau am leichtesten kaputtgehen:
identische Kopien von sprache.py, Formel-Beispiele, die ihre eigene Formel
treffen, die Verbzweitstellung im Humanizer, die du/Sie-Prüfung, gültiges
JSON, die Punktesumme der Profil-Rubrik und die Frontmatter jeder SKILL.md.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, "skills")
BSP = os.path.join(ROOT, "tests", "beispiele")
fehler = []


def check(ok, name):
    print(("  ok    " if ok else "  FEHLER") + "  " + name)
    if not ok:
        fehler.append(name)


def lauf(*args, stdin=None):
    p = subprocess.run([sys.executable, *args], input=stdin, capture_output=True,
                       text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def skript(ordner, name):
    return os.path.join(SK, ordner, name)


print("\nDATEIEN")
hashes = {o: hashlib.sha256(open(skript(o, "sprache.py"), "rb").read()).hexdigest()
          for o in ("ig-reel", "ig-caption", "ig-human")}
check(len(set(hashes.values())) == 1, "sprache.py ist in ig-reel, ig-caption, ig-human identisch")

for pfad in ["skills/ig-reel/hooks.json", "skills/ig-human/slop.json",
             "skills/ig-profile/rubric.json", ".claude-plugin/plugin.json",
             ".claude-plugin/marketplace.json"]:
    try:
        json.load(open(os.path.join(ROOT, pfad), encoding="utf-8"))
        check(True, f"{pfad} ist gültiges JSON")
    except Exception as e:
        check(False, f"{pfad} ist gültiges JSON ({e})")

rubric = json.load(open(skript("ig-profile", "rubric.json"), encoding="utf-8"))
check(sum(i["points"] for i in rubric["items"]) == 100, "Profil-Rubrik ergibt 100 Punkte")
check(any(i["id"] == "impressum" for i in rubric["items"]), "Profil-Rubrik prüft das Impressum")

print("\nSKILL.md")
for ordner in sorted(os.listdir(SK)):
    pfad = os.path.join(SK, ordner, "SKILL.md")
    if not os.path.exists(pfad):
        continue
    t = open(pfad, encoding="utf-8").read()
    m = re.match(r"---\nname: (\S+)\ndescription: >-\n((?:  .+\n)+)---\n", t)
    check(bool(m) and m.group(1) == ordner, f"{ordner}: Frontmatter mit name: {ordner}")
    check("—" not in t, f"{ordner}: keine Geviertstriche")
    check(not re.search(r"\bJob [AB]\b|\{\{your number\}\}", t), f"{ordner}: keine englischen Reste")

print("\nHOOK-FORMELN")
d = json.load(open(skript("ig-reel", "hooks.json"), encoding="utf-8"))
by = {h["id"]: h for h in d["hooks"]}
formeln = [(i, re.compile(by[i]["match"], re.I)) for i in d["classify_order"]]
check(len(d["hooks"]) == 26 and sorted(d["classify_order"]) == list(range(1, 27)),
      "26 Formeln, alle in classify_order")
falsch = [(h["id"], k) for h in d["hooks"] for k in ("example", "example_sie") if k in h
          and next((i for i, p in formeln if p.search(h[k])), None) != h["id"]]
check(not falsch, f"jedes Beispiel trifft seine eigene Formel {falsch or ''}")

print("\nHOOKSCORE")
rc, out = lauf(skript("ig-reel", "hookscore.py"), os.path.join(BSP, "hooks.txt"), "--json")
rows = {r["hook"]: r for r in json.loads(out)}
gruss = rows["Hallo zusammen, heute möchte ich über Zeiterfassung sprechen"]
check(gruss["verdict"] == "SCHWACH" and any("Begrüßung" in f for f in gruss["flags"]),
      "Begrüßung ist SCHWACH mit K.-O.")
check(rows["Wir freuen uns, Ihnen unsere neue Lösung vorzustellen"]["flags"] != [],
      "Firmen-Einstieg wird als K.-O. markiert")
check(rows["18.000 € hat uns eine fehlende Klausel im Rahmenvertrag gekostet."]["verdict"] == "STARK",
      "Kostenbeichte mit Betrag ist STARK")
mix = rows["Wenn Sie Ihre Stunden noch auf Zetteln sammeln, hast du ein Problem."]
check(any("du und Sie" in f for f in mix["flags"]), "du/Sie-Mix im Hook ist ein K.-O.")

print("\nBEATS")
rc, out = lauf(skript("ig-reel", "beats.py"), os.path.join(BSP, "skript.txt"), "--target", "30", "--json")
a = json.loads(out)
check(a["beats"][0]["label"] == "HOOK" and a["beats"][-1]["label"] == "CTA", "HOOK vorne, CTA hinten")
check(any("Loop" in n for n in a["notes"]), "Loop über Wortstämme erkannt")
check(20 < a["total_seconds"] < 30, f"Länge plausibel ({a['total_seconds']}s)")

print("\nCAPTION")
rc, out = lauf(skript("ig-caption", "caption.py"), os.path.join(BSP, "caption_gut.txt"), "--json")
gut = json.loads(out)
st = {c["check"]: c["status"] for c in gut["checks"]}
check(st["EIN CTA"] == "OK", "Keyword + Auslieferung per DM zählt als ein CTA")
check(st["ANREDE"] == "OK", "durchgehendes Sie ist OK")
rc, out = lauf(skript("ig-caption", "caption.py"), os.path.join(BSP, "caption_schlecht.txt"), "--json")
schlecht = json.loads(out)
st = {c["check"]: c["status"] for c in schlecht["checks"]}
check(st["ANREDE"] == "FEHLER", "du/Sie-Mix in der Caption ist FEHLER")
check(st["ERSTE ZEILE"] == "FEHLER", "Begrüßung in Zeile 1 ist FEHLER")
check(st["HASHTAGS"] == "FEHLER", "mehr als fünf Hashtags ist FEHLER")
check(schlecht["verdict"] == "ÜBERARBEITEN", "Urteil ÜBERARBEITEN")

print("\nHUMANIZER")
lex_rc, out = lauf(skript("ig-human", "humanize.py"), "-", "--json",
                   stdin="Zweifellos ist das wichtig. Darüber hinaus spart es Zeit. "
                         "Wir bieten maßgeschneiderte Lösungen.\n")
text = json.loads(out)["text"]
check("Sicher ist das wichtig." in text, "Verbzweitstellung bleibt: 'Sicher ist das wichtig.'")
check("Außerdem spart es Zeit." in text, "'Darüber hinaus' -> 'Außerdem'")
check("passende Lösungen" in text, "Adjektivendung übernommen: 'passende Lösungen'")
rc, out = lauf(skript("ig-human", "humanize.py"), os.path.join(BSP, "entwurf_schlecht.txt"), "--json")
rep = json.loads(out)["report"]
check(any("Gamechanger" == f["find"] for f in rep["flagged"]), "'Gamechanger' wird gemeldet, nicht ersetzt")
check(any("Nicht nur" in s["name"] for s in rep["structures"]), "'nicht nur ... sondern auch' wird gemeldet")
rc, out = lauf(skript("ig-human", "humanize.py"), "-", "--json", "--anfuehrung", "deutsch",
               stdin="Er sagte “passt schon” und ging.\n")
check("„passt schon“" in json.loads(out)["text"], "--anfuehrung deutsch macht aus “…” „…“")

print("\nDETECT")
rc, out = lauf(skript("ig-human", "detect.py"), os.path.join(BSP, "entwurf_schlecht.txt"), "--json")
s1 = json.loads(out)
rc, out = lauf(skript("ig-human", "detect.py"), os.path.join(BSP, "entwurf_mensch.txt"), "--json")
s2 = json.loads(out)
check(s1["verdict"] == "AUFFÄLLIG", f"schlechter Entwurf ist AUFFÄLLIG ({s1['human_score']})")
check(s2["human_score"] > s1["human_score"] + 25,
      f"menschlicher Text liegt deutlich darüber ({s2['human_score']} vs {s1['human_score']})")

print("\nSWIPE")
rc, out = lauf(skript("ig-viral", "swipe.py"), os.path.join(BSP, "erfasst.tsv"), "--json")
sw = json.loads(out)
by_acc = {r["account"]: r for r in sw["reels"]}
check(by_acc["@sicher_b"]["views"] == 3100 and by_acc["@steuer_d"]["followers"] == 1200000,
      "Zahlenformate 3,1K und 1,2 Mio. gelesen")
check(by_acc["@agency_us"]["formula_id"] == 3 and by_acc["@agency_us"]["hook_score"] is None,
      "englischer Hook über match_en zugeordnet, ohne deutschen Hook-Score")
check(sw["reels"][0]["outlier"] >= sw["reels"][-1]["outlier"], "nach Outlier-Vielfachem sortiert")

print("\n" + ("ALLES OK" if not fehler else f"{len(fehler)} FEHLER") + "\n")
sys.exit(1 if fehler else 0)
