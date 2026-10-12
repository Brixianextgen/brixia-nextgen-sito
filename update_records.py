#!/usr/bin/env python3
"""Aggiorna record-italiani.json dalla pagina Wikipedia
"Migliori prestazioni italiane allievi di atletica leggera" (sezione Outdoor).
Uso: python3 update_records.py [file_wikitext]  (senza argomenti scarica da Wikipedia)"""
import json, re, sys, datetime, urllib.request, urllib.parse

PAGE = "Migliori_prestazioni_italiane_allievi_di_atletica_leggera"
API = ("https://it.wikipedia.org/w/api.php?action=parse&prop=wikitext&format=json"
       "&formatversion=2&page=" + urllib.parse.quote(PAGE))
BR = "⁣"  # separatore interno per gli a capo nelle celle


def fetch():
    req = urllib.request.Request(API, headers={"User-Agent": "BrixiaNextGenSite/1.0 (info@brixia-nextgen.org)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["parse"]["wikitext"]


def split_params(body):
    out, depth, cur = [], 0, ""
    i = 0
    while i < len(body):
        c = body[i]
        if body.startswith("[[", i) or body.startswith("{{", i):
            depth += 1; cur += body[i:i+2]; i += 2; continue
        if body.startswith("]]", i) or body.startswith("}}", i):
            depth -= 1; cur += body[i:i+2]; i += 2; continue
        if c == "|" and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += c
        i += 1
    out.append(cur)
    return out


def tpl(m):
    parts = split_params(m.group(1))
    name = parts[0].strip()
    pos = [p.strip() for p in parts[1:] if "=" not in p.split("[[")[0]]
    named = {}
    for p in parts[1:]:
        if "=" in p.split("[[")[0]:
            k, v = p.split("=", 1); named[k.strip()] = v.strip()
    low = name.lower()
    if low == "risultato":
        v = pos[0] if pos else ""
        w = named.get("vento", "")
        return v + (" (" + w + ")" if w and w != "?" else "")
    if low == "società atletica":
        if len(pos) >= 2 and pos[1] and pos[1] != "nome":
            return pos[1]
        return pos[0] if pos else ""
    if low == "naz":
        return "Italia"
    if low.startswith(("bandiera", "cita", "legenda", "risultati", "nota", "chiarire", "senza fonte")):
        return ""
    return name


def clean(s):
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<br\s*/?>", BR, s)
    s = re.sub(r"<[^>]+>", "", s)
    for _ in range(6):
        n = re.sub(r"\{\{([^{}]*)\}\}", tpl, s)
        if n == s:
            break
        s = n
    s = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", s)
    s = s.replace("'''", "").replace("''", "").replace("&nbsp;", " ")
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


ATTR = re.compile(r"^\s*((?:(?:rowspan|colspan|align|style|class)\s*=\s*\"?[^|\[{\"]*\"?\s*)+)\|(.*)$", re.S)


def parse_table(txt):
    rows, cur, cell = [], None, None
    for line in txt.split("\n"):
        if line.startswith("{|") or line.startswith("!"):
            continue
        if line.startswith("|}"):
            break
        if line.startswith("|-"):
            cur = {"cells": [], "rat": "cef6f5" in line.lower()}
            rows.append(cur); cell = None
            continue
        if cur is None:
            continue
        if line.startswith("|"):
            for part in re.split(r"\|\|", line[1:]):
                cell = part; cur["cells"].append(cell)
        elif cur["cells"]:
            cur["cells"][-1] += BR + line
    grid, spans = [], {}
    for r in rows:
        if not r["cells"]:
            continue
        out, col, src, skip = [], 0, list(r["cells"]), False
        while src or any(spans.get(c, (0,))[0] > 0 for c in range(col, 6)):
            if spans.get(col, (0, ""))[0] > 0:
                n, v = spans[col]; spans[col] = (n - 1, v); out.append(v); col += 1; continue
            if not src:
                break
            raw = src.pop(0)
            m = ATTR.match(raw)
            attrs, val = (m.group(1), m.group(2)) if m else ("", raw)
            rs = re.search(r"rowspan\s*=\s*\"?(\d+)", attrs)
            cs = re.search(r"colspan\s*=\s*\"?(\d+)", attrs)
            if cs and int(cs.group(1)) >= 3:
                skip = True
            if rs and int(rs.group(1)) > 1:
                spans[col] = (int(rs.group(1)) - 1, val)
            out.append(val); col += 1
            if cs:
                for _ in range(int(cs.group(1)) - 1):
                    out.append(""); col += 1
        if skip or len(out) < 6:
            continue
        ev, res, ath, club, place, date = [clean(x) for x in out[:6]]
        ev = re.sub(BR + "+", " ", ev).strip()
        res = re.sub(BR + "+", " ", res).strip()
        ath = " / ".join(p.strip() for p in ath.split(BR) if p.strip())
        club = " ".join(p.strip() for p in club.split(BR) if p.strip())
        place = " ".join(p.strip() for p in place.split(BR) if p.strip())
        date = " ".join(p.strip() for p in date.split(BR) if p.strip())
        if not ev or not res:
            continue
        grid.append([ev, res, ath, club, place, date, 1 if r["rat"] else 0])
    return grid


def section(wt, start_pat, end_pat):
    a = re.search(start_pat, wt)
    if not a:
        return ""
    rest = wt[a.end():]
    b = re.search(end_pat, rest)
    return rest[: b.start()] if b else rest


def build(wt):
    wt = wt.replace("\r", "")
    outdoor = section(wt, r"==\s*''Outdoor''\s*==", r"\n==\s*''Indoor''\s*==")
    data = {"source": "https://it.wikipedia.org/wiki/" + PAGE,
            "fetched": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")}
    for key, title in (("m", "Maschili"), ("f", "Femminili")):
        sec = section(outdoor, r"===\s*" + title + r"\s*===", r"\n===")
        upd = re.search(r"aggiornate? all?['’]?\s*([^.'\n]+)", sec)
        data["upd_" + key] = upd.group(1).strip() if upd else ""
        t = sec[sec.find("{|"):] if "{|" in sec else ""
        data[key] = parse_table(t)
    return data


if __name__ == "__main__":
    wt = open(sys.argv[1], encoding="utf8").read() if len(sys.argv) > 1 else fetch()
    d = build(wt)
    if len(d["m"]) < 20 or len(d["f"]) < 20:
        sys.exit("Tabelle non riconosciute: file non aggiornato")
    out = "record-italiani.json"
    try:
        old = json.load(open(out, encoding="utf8"))
        if {k: v for k, v in old.items() if k != "fetched"} == {k: v for k, v in d.items() if k != "fetched"}:
            print("Nessuna modifica"); sys.exit(0)
    except Exception:
        pass
    json.dump(d, open(out, "w", encoding="utf8"), ensure_ascii=False, indent=1)
    print("Aggiornato:", len(d["m"]), "uomini,", len(d["f"]), "donne")
