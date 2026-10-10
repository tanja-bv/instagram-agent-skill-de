#!/usr/bin/env python3
"""
sprache.py - die deutschen Textregeln, die alle Skripte im Paket teilen.

Deutsch bricht drei Annahmen, auf denen das englische Original gebaut war:

  1. Großbuchstaben markieren keine Namen. Jedes Substantiv ist groß, also
     taugt "großes Wort mitten im Satz" nicht als Zeichen für etwas Konkretes.
     Konkret ist hier: Zahlen (auch ausgesprochene), Geldwörter, Abkürzungen
     wie DSGVO oder KV, Marken in Binnenmajuskel (WhatsApp), @Handles,
     Monate, Wochentage und Orte im DACH-Raum.
  2. Wörter sind lang. "Arbeitszeiterfassung" ist ein Wort und sechs Silben.
     Sprechzeit wird deshalb über Silben geschätzt, nicht über Wörter.
  3. Abkürzungen mit Punkt (z. B., ca., Nr.) und Ordnungszahlen (1. Januar)
     sind keine Satzenden.

Diese Datei liegt identisch in ig-reel, ig-caption und ig-human, damit jeder
Skill-Ordner allein kopiert werden kann. Wer sie ändert, ändert alle drei
(tests/run.py prüft, dass die Kopien gleich sind).
"""

import re

# --------------------------------------------------------------------------
# Wörter und Zahlen
# --------------------------------------------------------------------------

LETTERS = "A-Za-zÄÖÜäöüßẞ"
WORD_RE = re.compile(rf"[{LETTERS}0-9€$%'’]+(?:[-.,][{LETTERS}0-9€%]+)*")
TOKEN_RE = WORD_RE

EINER = ["null", "eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben",
         "acht", "neun", "zehn", "elf", "zwölf", "dreizehn", "vierzehn",
         "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn"]
ZEHNER = ["", "", "zwanzig", "dreißig", "vierzig", "fünfzig", "sechzig",
          "siebzig", "achtzig", "neunzig"]


def _bis999(n, final=True):
    h, r = divmod(n, 100)
    out = ""
    if h:
        out += ("ein" if h == 1 else EINER[h]) + "hundert"
    if r:
        if r == 1:
            out += "eins" if final else "ein"
        elif r < 20:
            out += EINER[r]
        else:
            u, t = r % 10, r // 10
            if u:
                out += ("ein" if u == 1 else EINER[u]) + "und"
            out += ZEHNER[t]
    return out


def zahl_wort(n):
    """18000 -> 'achtzehntausend'. Reicht für Silben, nicht für Schecks."""
    if n == 0:
        return "null"
    if n < 0:
        return "minus " + zahl_wort(-n)
    if 1100 <= n <= 1999:                       # Jahreszahl: neunzehnhundert...
        h, r = divmod(n, 100)
        return _bis999(h, False) + "hundert" + (_bis999(r) if r else "")
    teile = []
    mrd, rest = divmod(n, 10 ** 9)
    mio, rest = divmod(rest, 10 ** 6)
    tsd, rest = divmod(rest, 1000)
    if mrd:
        teile.append("eine Milliarde" if mrd == 1 else _bis999(mrd, False) + " Milliarden")
    if mio:
        teile.append("eine Million" if mio == 1 else _bis999(mio, False) + " Millionen")
    wort = ""
    if tsd:
        wort += ("ein" if tsd == 1 else _bis999(tsd, False)) + "tausend"
    if rest:
        wort += _bis999(rest)
    if wort:
        teile.append(wort)
    return " ".join(teile)


ZAHL_RE = re.compile(r"\d{1,3}(?:[.’']\d{3})+(?:,\d+)?|\d+(?:[.,]\d+)?")


def parse_zahl(token):
    """'18.000' -> 18000.0, '3,5' -> 3.5, '1.2' -> 1.2, '12’000' -> 12000."""
    t = token.strip()
    if re.fullmatch(r"\d{1,3}(?:[.’']\d{3})+(?:,\d+)?", t):
        t = re.sub(r"[.’']", "", t).replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(?:,\d{3})+", t):          # englisch: 18,000
        t = t.replace(",", "")
    else:
        t = t.replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def sprech_zahl(token):
    """Wie eine Zahl ausgesprochen wird: '3,5' -> 'drei Komma fünf'."""
    v = parse_zahl(token)
    if v is None:
        return token
    if v != int(v):
        ganz, _, nach = token.replace(".", ",").partition(",")
        ganz_v = parse_zahl(ganz) or 0
        return zahl_wort(int(ganz_v)) + " Komma " + " ".join(EINER[int(c)] for c in nach if c.isdigit())
    return zahl_wort(int(v))


EINHEIT_SPRECH = {
    "€": "Euro", "eur": "Euro", "$": "Dollar", "%": "Prozent", "k": "tausend",
    "h": "Stunden", "std": "Stunden", "min": "Minuten", "sek": "Sekunden",
    "s": "Sekunden", "x": "mal", "mio": "Millionen", "mrd": "Milliarden",
    "tsd": "tausend", "&": "und", "+": "plus", "ca": "circa", "z.b": "zum Beispiel",
    "bzw": "beziehungsweise", "usw": "und so weiter", "inkl": "inklusive",
}

VOKAL_RE = re.compile(r"[aeiouyäöü]+", re.IGNORECASE)


def _silben_wort(wort):
    letters = re.sub(rf"[^{LETTERS}]", "", wort)
    if not letters:
        return 0
    # Abkürzungen werden buchstabiert: KV = Ka-Vau, DSGVO = fünf Silben.
    if letters.isupper() and 2 <= len(letters) <= 5 and len(VOKAL_RE.findall(letters)) <= 1:
        return len(letters)
    return max(1, len(VOKAL_RE.findall(letters)))


def sprechtext(text):
    """Schreibt Zahlen und Zeichen so aus, wie sie gesprochen werden."""
    t = text
    t = re.sub(r"(\d)\s*(€|%|\$)", r"\1 \2", t)
    t = re.sub(r"(€|\$)\s*(\d)", r"\2 \1", t)                 # € 18.000 -> 18.000 €
    t = re.sub(r"(?i)\b(\d+(?:[.,]\d+)?)\s*(k|h|std|min|sek|x|mio|mrd|tsd)\b\.?",
               lambda m: m.group(1) + " " + EINHEIT_SPRECH[m.group(2).lower()], t)
    t = re.sub(r"(?i)\b(z\.\s?b|bzw|usw|inkl|ca)\.",
               lambda m: EINHEIT_SPRECH[m.group(1).lower().replace(" ", "")], t)
    t = ZAHL_RE.sub(lambda m: " " + sprech_zahl(m.group(0)) + " ", t)
    for zeichen in ("€", "%", "$", "&", "+"):
        t = t.replace(zeichen, " " + EINHEIT_SPRECH[zeichen] + " ")
    return re.sub(r"\s+", " ", t).strip()


def silben(text):
    """Geschätzte gesprochene Silben eines Textes."""
    return sum(_silben_wort(w) for w in re.findall(rf"[{LETTERS}]+", sprechtext(text)))


def woerter(text):
    """Wörter, wie sie gezählt werden. '18.000 €' ist ein Wort plus Einheit."""
    return WORD_RE.findall(text)


# --------------------------------------------------------------------------
# Sätze
# --------------------------------------------------------------------------

ABKUERZUNGEN = [
    "z. B.", "z.B.", "d. h.", "d.h.", "u. a.", "u.a.", "o. Ä.", "o.Ä.", "u. U.", "u.U.",
    "bzw.", "ca.", "etc.", "usw.", "Nr.", "Dr.", "Mag.", "Ing.", "Dipl.", "Prof.", "St.",
    "Mio.", "Mrd.", "Tsd.", "inkl.", "zzgl.", "ggf.", "evtl.", "vgl.", "Std.", "Min.",
    "Sek.", "Jan.", "Feb.", "Apr.", "Aug.", "Sept.", "Sep.", "Okt.", "Nov.", "Dez.",
    "Mo.", "Di.", "Mi.", "Do.", "Fr.", "Sa.", "So.", "allg.", "bspw.", "sog.", "Hr.",
    "Fr.", "GmbH.", "max.", "min.", "rd.", "Tel.", "Str.",
]
_ABK_RE = re.compile("|".join(re.escape(a) for a in sorted(ABKUERZUNGEN, key=len, reverse=True)))
SATZ_ENDE = re.compile(r"(?<=[.!?…])[\"“”'»«)]*\s+|\n+")


def saetze(text):
    """Sätze, mit Abkürzungen und Ordnungszahlen (am 1. Januar) geschützt."""
    t = _ABK_RE.sub(lambda m: m.group(0).replace(".", "\x01"), text)
    t = re.sub(r"(\d)\.(?=\s+(?:[a-zäöüß]|\d|Jänner|Januar|Februar|Feber|März|April|Mai|"
               r"Juni|Juli|August|September|Oktober|November|Dezember|Quartal|Platz|Stock))",
               "\\1\x01", t)
    t = re.sub(r"(\d)\.(\d)", "\\1\x01\\2", t)
    out = []
    for teil in SATZ_ENDE.split(t):
        teil = teil.replace("\x01", ".").strip()
        if teil:
            out.append(teil)
    return out


# --------------------------------------------------------------------------
# Konkretes
# --------------------------------------------------------------------------

ZAHLWOERTER = {
    "null", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun",
    "zehn", "elf", "zwölf", "fünfzehn", "zwanzig", "dreißig", "vierzig", "fünfzig",
    "sechzig", "siebzig", "achtzig", "neunzig", "hundert", "tausend", "million",
    "millionen", "milliarde", "milliarden", "dutzend", "hälfte", "halb", "doppelt",
    "doppelte", "dreifach", "dreifache", "zehnfach", "viertel", "drittel",
    "zweimal", "dreimal", "zehnmal", "hundertmal",
}
# "eins" und "ersten" fehlen absichtlich: das sind öfter Füllwörter als Mengen.

GELDWOERTER = {
    "euro", "cent", "franken", "prozent", "umsatz", "gewinn", "marge", "gehalt",
    "lohn", "löhne", "stundensatz", "stundenlohn", "tagessatz", "miete", "budget",
    "rechnung", "rechnungen", "angebot", "angebote", "auftrag", "aufträge",
    "nachzahlung", "strafe", "bußgeld", "lohnnebenkosten", "deckungsbeitrag",
}

MONATE = {"januar", "jänner", "februar", "feber", "märz", "april", "mai", "juni", "juli",
          "august", "september", "oktober", "november", "dezember"}
WOCHENTAGE = {"montag", "dienstag", "mittwoch", "donnerstag", "freitag", "samstag",
              "sonntag", "montags", "dienstags", "mittwochs", "donnerstags", "freitags",
              "samstags", "sonntags"}
ORTE = {
    "wien", "graz", "linz", "salzburg", "innsbruck", "klagenfurt", "villach", "wels",
    "st. pölten", "dornbirn", "bregenz", "eisenstadt", "mödling", "wiener neustadt",
    "berlin", "hamburg", "münchen", "köln", "frankfurt", "stuttgart", "düsseldorf",
    "leipzig", "dortmund", "essen", "bremen", "dresden", "hannover", "nürnberg",
    "duisburg", "bochum", "wuppertal", "bielefeld", "bonn", "münster", "mannheim",
    "karlsruhe", "augsburg", "wiesbaden", "freiburg", "regensburg", "rosenheim",
    "zürich", "basel", "bern", "genf", "luzern", "winterthur", "st. gallen", "lugano",
    "österreich", "deutschland", "schweiz", "dach", "bayern", "tirol", "vorarlberg",
    "kärnten", "steiermark", "niederösterreich", "oberösterreich", "burgenland",
    "nrw", "sachsen", "hessen", "baden-württemberg", "südtirol", "europa", "eu",
}
# Großgeschriebene Wörter, die keine Abkürzung sind, sondern Geschrei.
KEINE_ABK = {"ICH", "WIR", "DU", "SIE", "ER", "ES", "UND", "ODER", "NICHT", "KEIN",
             "DAS", "DER", "DIE", "IST", "OK", "JA", "NEIN", "NUR", "NIE", "WAS", "WIE",
             "MIT", "VON", "FÜR", "AUF", "DEN", "DEM", "EIN", "EINE", "TOP", "NEU", "JETZT"}

ABK_RE = re.compile(r"\b[A-ZÄÖÜ]{2,6}[0-9]?\b")
BINNEN_RE = re.compile(r"\b[a-zäöü]*[A-Za-zäöü][a-zäöü]+[A-Z][A-Za-zäöü]+\b")   # WhatsApp, LinkedIn
HANDLE_RE = re.compile(r"(?<![\w.])@[A-Za-z0-9_.]{2,}")
QUARTAL_RE = re.compile(r"\bQ[1-4]\b")
GELD_RE = re.compile(r"(?:€|\$|EUR|CHF)\s?\d|\d[\d.,’']*\s?(?:€|\$|EUR\b|CHF\b|Euro\b|Franken\b)")
ZIFFER_RE = re.compile(r"\d[\d.,’']*\s?%?")


def konkrete_marker(text):
    """Liste der Dinge im Text, die man nachprüfen könnte."""
    funde = []
    funde += [m.group(0).strip() for m in ZIFFER_RE.finditer(text)]
    low = [w.lower().strip("'’.,") for w in re.findall(rf"[{LETTERS}][{LETTERS}\-]*", text)]
    funde += [w for w in low if w in ZAHLWOERTER or w in GELDWOERTER]
    funde += [w for w in low if w in MONATE or w in WOCHENTAGE]
    lowtext = text.lower()
    funde += [o for o in ORTE if re.search(r"(?<![\wäöüß])" + re.escape(o) + r"(?![\wäöüß])", lowtext)]
    funde += [a for a in ABK_RE.findall(text) if a not in KEINE_ABK]
    funde += BINNEN_RE.findall(text)
    funde += HANDLE_RE.findall(text)
    funde += QUARTAL_RE.findall(text)
    return [f for f in funde if f]


# --------------------------------------------------------------------------
# Anrede
# --------------------------------------------------------------------------

DU_RE = re.compile(r"\b(?:du|dich|dir|dein|deine|deinen|deinem|deiner|deines|"
                   r"euch|euer|eure|euren|eurem|eurer|eures)\b", re.IGNORECASE)
# Sie und Ihnen/Ihr... sind nur dann sicher die Höflichkeitsform, wenn sie groß
# mitten im Satz stehen. Am Satzanfang kann "Sie" auch "sie" (Plural) sein.
SIE_RE = re.compile(r"(?<![.!?:\n„\"“]\s)(?<![.!?:\n])(?<=\s)(?:Sie|Ihnen|Ihr|Ihre|Ihren|Ihrem|Ihrer|Ihres)\b")



def anrede(text):
    """Zählt du-Formen und Sie-Formen. Gibt {'du': n, 'sie': n} zurück."""
    du = len(DU_RE.findall(text))
    sie = len(SIE_RE.findall(text))
    return {"du": du, "sie": sie}


# --------------------------------------------------------------------------
# Stimme
# --------------------------------------------------------------------------

# Abtönungspartikeln und Kurzformen: so klingt gesprochenes Deutsch, und genau
# das lassen Sprachmodelle weg.
PARTIKEL = {"halt", "eben", "mal", "ja", "doch", "eh", "schon", "wohl", "ruhig",
            "bloß", "echt", "ziemlich", "irgendwie", "quasi", "na", "ne", "nee", "naja",
            "jedenfalls", "übrigens", "sowieso", "eigentlich"}
KURZFORM_RE = re.compile(r"\b\w+['’]s\b|\b(?:hab|nen|nich|is|isses|haste|kannste|biste|"
                         r"willste|weißte|rein|raus|rüber|drauf|drin|runter|grad)\b",
                         re.IGNORECASE)
PERSON_RE = re.compile(r"\b(?:ich|mich|mir|mein\w*|wir|uns|unser\w*|du|dich|dir|dein\w*|"
                       r"euch|euer|eure\w*)\b", re.IGNORECASE)


def stimme(text):
    w = re.findall(rf"[{LETTERS}']+", text)
    low = [x.lower() for x in w]
    partikel = sum(1 for x in low if x in PARTIKEL)
    kurz = len(KURZFORM_RE.findall(text))
    person = len(PERSON_RE.findall(text)) + anrede(text)["sie"]
    return {"woerter": len(w), "partikel": partikel, "kurzformen": kurz, "person": person}


# --------------------------------------------------------------------------
# Grobe Stammform (für "kommt das Wort aus dem Hook am Ende wieder?")
# --------------------------------------------------------------------------

STOPP = {
    "der", "die", "das", "den", "dem", "des", "ein", "eine", "einen", "einem", "einer",
    "und", "oder", "aber", "wenn", "dass", "weil", "von", "zu", "zum", "zur", "im", "in",
    "an", "am", "auf", "für", "mit", "ohne", "bei", "aus", "nach", "vor", "über", "unter",
    "ist", "sind", "war", "waren", "hat", "haben", "hatte", "wird", "werden", "kann",
    "ich", "du", "er", "sie", "es", "wir", "ihr", "mich", "dich", "mir", "dir", "uns",
    "euch", "ihnen", "mein", "dein", "unser", "so", "nur", "noch", "schon", "nicht",
    "kein", "keine", "auch", "dann", "da", "hier", "jetzt", "mal", "ja", "nein", "wie",
    "was", "wer", "eins", "alle", "man", "sich", "als", "bis", "um", "es", "sein",
}


def stamm(wort):
    w = wort.lower().strip("'’.,!?:;\"")
    for endung in ("ern", "en", "er", "es", "em", "e", "n", "s"):
        if len(w) > 5 and w.endswith(endung):
            return w[: -len(endung)]
    return w
