#!/usr/bin/env python3
"""Deterministic layer of the Ability Metadata Platform, read from the markdown in rules/.

For every entry in scope (rules/magic-and-abilities/*.md plus the four class immunity traits) this builds:
  * sentences   the rule text split into numbered sentences: E1.. (Effect), L1.. (Limitations), N1.. (Note)
  * identity    type, school, range, delivery
  * casting     incantation text and repetitions, materials and strip/cover colors
  * availability  every class listing with level, cost, max, (m)/(ex), per-class range, Look The Part, pick groups,
                  and the frequency parsed into uses / per / charge / balls or arrows
Agents never write these facets; they cite the sentence ids.
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import interop_data as I

ROOT = I.ROOT
MA = os.path.join(ROOT, "rules", "magic-and-abilities")
COLORS = ["red", "white", "yellow", "orange", "green", "blue", "black", "gray", "grey", "purple", "brown", "silver", "gold", "pink"]
DELIVERY = {"Verbal": "verbal", "Enchantment": "enchantment", "Magic Ball": "magic-ball", "Specialty Arrow": "specialty-arrow",
            "Trait": "trait", "Meta-Magic": "meta-magic", "Archetype": "archetype"}
_PROTECT = [("e.g.", "e․g․"), ("i.e.", "i․e․"), ("etc.", "etc․"), ("vs.", "vs․"), ("Mt.", "Mt․")]


def split_sentences(text):
    t = text
    for a, b in _PROTECT:
        t = t.replace(a, b)
    parts = re.split(r"(?<=[.!?”\"])\s+(?=[A-Z0-9\"“(`])", t)
    out = []
    for p in parts:
        for a, b in _PROTECT:
            p = p.replace(b, a)
        p = p.strip()
        if p:
            out.append(p)
    return out


def parse_fields(md):
    """Return {field: [units]} where each unit is a paragraph or list item, in order. A blank line ends a paragraph."""
    body = md.split("\n# ", 1)[1] if "\n# " in md else md
    body = re.split(r"\n---\n\*Source", body)[0]
    fields, cur, blank = {}, None, False
    for line in body.splitlines()[1:]:
        m = re.match(r"^\*\*([A-Za-z ]+):\*\*\s?(.*)$", line)
        if m:
            cur = m.group(1)
            fields[cur] = [m.group(2).strip()] if m.group(2).strip() else []
            blank = False
            continue
        if cur is None:
            continue
        if not line.strip():
            blank = True
            continue
        s = line.strip()
        if re.match(r"^(?:[-*]|\d+\.)\s+", s) or blank or not fields[cur]:
            fields[cur].append(s)
        else:
            fields[cur][-1] += " " + s
        blank = False
    return fields


def split_unit(unit):
    """Split a paragraph or list item into sentences, keeping a list marker with its first sentence."""
    m = re.match(r"^((?:[-*]|\d+\.)\s+)(.*)$", unit)
    marker, rest = (m.group(1), m.group(2)) if m else ("", unit)
    ss = split_sentences(rest)
    if marker and ss:
        ss[0] = marker + ss[0]
    return ss


def sentences_of(fields):
    out = []
    for field, prefix in (("Effect", "E"), ("Limitations", "L"), ("Note", "N")):
        n = 0
        for unit in fields.get(field, []):
            for s in split_unit(unit):
                n += 1
                out.append(dict(id=f"{prefix}{n}", field=field, text=s))
    return out


def parse_incantation(raw):
    if not raw:
        return dict(raw="", text="", repetitions=None, words=0, special="none")
    reps = re.search(r"\bx(\d+)\s*$", raw.strip())
    quoted = re.findall(r"[\"“](.+?)[\"”]", raw)
    text = " / ".join(q.strip() for q in quoted) if quoted else raw.strip()
    special = raw.strip()[len(quoted[-1]) + 2:].strip() if quoted else ""
    special = re.sub(r"^x\d+$", "", special).strip()
    return dict(raw=raw.strip(), text=text, repetitions=int(reps.group(1)) if reps else 1,
                words=len(re.findall(r"[A-Za-z']+", text)), special=special or "none")


def parse_materials(raw):
    cols = sorted({c.replace("grey", "gray") for c in COLORS if re.search(r"\b" + c + r"\b", (raw or "").lower())})
    kind = "none"
    if raw:
        low = raw.lower()
        kind = "strip" if "strip" in low else "magic-ball" if "magic ball" in low else "arrow-cover" if "arrow" in low else "other"
    return dict(raw=raw or "", colors=cols, kind=kind)


def parse_frequency(f):
    """'1/Refresh Charge x10' -> {uses:1, per:'refresh', charge:10}; '2 Balls / Unlimited' -> {uses:2, unit:'balls', per:'unlimited'}."""
    f = (f or "").strip()
    out = dict(raw=f, uses=None, per=None, charge=None, unit=None)
    if not f or f == "-":
        return out
    m = re.search(r"Charge x(\d+)", f)
    if m:
        out["charge"] = int(m.group(1))
    m = re.match(r"(\d+)\s*(Balls?|Arrows?)\s*/\s*(Unlimited|Life|Refresh)", f, re.I)
    if m:
        out.update(uses=int(m.group(1)), unit=m.group(2).lower().rstrip("s") + "s", per=m.group(3).lower())
        return out
    m = re.match(r"(\d+)\s*/\s*(Life|Refresh|Game)", f, re.I)
    if m:
        out.update(uses=int(m.group(1)), per=m.group(2).lower())
        return out
    if f.lower().startswith("unlimited"):
        out["per"] = "unlimited"
    return out


def class_trait_entries(D):
    """The four 'Immune to <School>' class Traits. Their rule text is the Immune mechanic (rules/magic-states-effects)."""
    mech = open(os.path.join(ROOT, "rules", "magic-states-effects", "mechanics-and-definitions.md")).read()
    sec = mech.split("### Immune", 1)[1].split("\n### ", 1)[0]
    lead = [l.strip() for l in sec.splitlines() if l.strip() and not re.match(r"^\d+\.", l.strip())][0]
    items = [re.sub(r"^\d+\.\s*", "", l.strip()) for l in sec.splitlines() if re.match(r"^\d+\.", l.strip())]
    by_school = {}
    for c in D["classes"]:
        for s in c["immune"]:
            by_school.setdefault(s, []).append(c["name"])
    out = {}
    for s, cls in sorted(by_school.items()):
        slug = "immune-to-" + s.lower()
        sents = [dict(id="E1", field="Effect", text=lead)]
        n = 0
        for it in items:
            for x in split_sentences(it):
                n += 1
                sents.append(dict(id=f"N{n}", field="Note", text=x))
        out[slug] = dict(slug=slug, title=f"Immune to {s}", kind="class-trait", type="Trait", school=s, range="", delivery="trait",
                         incantation=parse_incantation(""), materials=parse_materials(""), sentences=sents,
                         availability=[dict(cls=c, levels=[1], cost="", max="", frequency=parse_frequency(""), magical=None, range="",
                                            look_the_part=False, option="", tag="", source="Level table") for c in cls],
                         source_file="rules/magic-states-effects/mechanics-and-definitions.md#immune",
                         note=f"Class Trait granted at 1st level to {', '.join(cls)}; its rules are the Immune mechanic.")
    return out


def load():
    """{slug: entry} for every entry in scope."""
    D = I.load()
    nodes = D["nodes"]
    avail = {}
    for n in nodes:
        avail.setdefault(n["slug"], []).append(dict(
            cls=n["cls"], levels=n["levels"], cost=n["cost"], max=n["max"], frequency=parse_frequency(n["freq"]),
            magical=n["magical"], range=n["range"], look_the_part=False, option=n["option"], tag=n["tag"], source=n["source"]))
    ltp = {c["name"]: set(c.get("ltp", [])) for c in D["classes"]}
    table_cost = {}
    for c in D["classes"]:
        for r in c.get("table_rows", []):
            table_cost[(c["name"], I.clean(r["name"]), r["level"])] = r["cost"]
    out = {}
    for f in sorted(glob.glob(os.path.join(MA, "*.md"))):
        b = os.path.basename(f)
        if b in ("INDEX.md", "_overview.md"):
            continue
        md = open(f).read()
        slug = b[:-3]
        title = re.search(r'^title: "?(.*?)"?$', md, re.M).group(1)
        fl = parse_fields(md)
        one = lambda k: " ".join(fl.get(k, [])).strip()
        typ = one("Type")
        rows = list(avail.get(slug, []))
        have = {(r["cls"], L) for r in rows for L in r["levels"]}
        av = re.search(r"^class_availability: \[(.*)\]", md, re.M)
        for item in (av.group(1).split(",") if av and av.group(1).strip() else []):
            m = re.match(r'\s*"?([A-Za-z-]+(?: [A-Za-z-]+)?) (\d)"?\s*$', item)
            if m and (m.group(1), int(m.group(2))) not in have:
                is_ltp = int(m.group(2)) == 1 and slug in ltp.get(m.group(1), set())
                rows.append(dict(cls=m.group(1), levels=[int(m.group(2))], cost=table_cost.get((m.group(1), title, int(m.group(2))), ""), max="", frequency=parse_frequency(""), magical=None, range="",
                                 look_the_part=is_ltp, option="", tag="", source="Look The Part (class description)" if is_ltp else "ability header only (archetype pick, equipment row or granted)"))
        out[slug] = dict(slug=slug, title=title, kind="ability", type=typ, school=one("School"), range=one("Range"),
                         delivery=DELIVERY.get(typ, "trait" if typ == "Trait" else typ.lower()),
                         incantation=parse_incantation(one("Incantation")), materials=parse_materials(one("Materials")),
                         sentences=sentences_of(fl), availability=rows,
                         source_file=f"rules/magic-and-abilities/{b}", note="")
    out.update(class_trait_entries(D))
    return out


if __name__ == "__main__":
    ents = load()
    from collections import Counter
    print(len(ents), "entries;", sum(len(e["sentences"]) for e in ents.values()), "sentences")
    print(Counter(e["delivery"] for e in ents.values()))
    for s in ("gift-of-air", "resurrect", "true-grit", "reload", "immune-to-death", "entangle"):
        e = ents[s]
        print("\n##", e["title"], e["delivery"], e["incantation"], e["materials"])
        for x in e["sentences"]:
            print("  ", x["id"], x["text"][:110])
        for a in e["availability"][:3]:
            print("   avail", a["cls"], a["levels"], a["frequency"], a["magical"], a["range"])
