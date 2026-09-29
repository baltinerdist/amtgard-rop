#!/usr/bin/env python3
"""Shared extraction for the ability/class interoperability tools.

Reads rules/classes/*.md (level tables, spell tables, immunities) and rules/magic-and-abilities/*.md
(the ability stat blocks) and answers, for every (class, ability) pair on a class list:
  * what level(s) / cost / max / frequency the class lists it at,
  * whether it can affect another player,
  * for each of the 12 classes: does it work, or is it blocked, and why,
  * which other abilities it is connected to (shared, granted, removed, replaced, mentioned).

Model: every class is 6th level with every ability on its list, archetypes and spell points ignored
(verdicts do not depend on level, because class Immunities are 1st-level Traits).
Consumers: scripts/gen_interop.py (markdown), scripts/build_chord.py (chord diagram).
"""
import glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rop_version as V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MA = os.path.join(ROOT, "rules/magic-and-abilities")
CL = os.path.join(ROOT, "rules/classes")

CLASSES = [("anti-paladin", "Anti-Paladin", "Ap", "martial"), ("archer", "Archer", "Ar", "martial"),
           ("assassin", "Assassin", "As", "martial"), ("barbarian", "Barbarian", "Bn", "martial"),
           ("monk", "Monk", "Mk", "martial"), ("paladin", "Paladin", "Pa", "martial"),
           ("scout", "Scout", "Sc", "martial"), ("warrior", "Warrior", "Wa", "martial"),
           ("bard", "Bard", "Bd", "magic"), ("druid", "Druid", "Dr", "magic"),
           ("healer", "Healer", "He", "magic"), ("wizard", "Wizard", "Wi", "magic")]
ORD = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6}
FIELDS = ("Type", "School", "Range", "Incantation", "Materials", "Effect", "Limitations", "Note")


# Immunities and Enlightened Soul protect the *player*, not carried equipment or worn armor (Immune rule 2 and 4;
# the Notes of Pyrotechnics, Destroy Armor, Heat Weapon and Shatter Weapon say so explicitly). These are the
# targeting abilities whose result therefore differs from the plain "immune school / Enlightened Soul" test.
EQUIPMENT = {
    "pyrotechnics": dict(ignores_immunity=True, ignores_enlightened_soul=True,
                         works_note="Affects the player's equipment, which immunities and Enlightened Soul do not protect"),
    "destroy-armor": dict(ignores_immunity=True, ignores_enlightened_soul=True,
                          works_note="Affects the hit location's armor, which immunities and Enlightened Soul do not protect"),
    "shatter-weapon": dict(ignores_immunity=True, ignores_enlightened_soul=True,
                           works_note="The weapon, not the person, is the target, so Enlightened Soul does not protect it"),
    "heat-weapon": dict(ignores_enlightened_soul=True,
                        immune_negates="Its target is the weapon, but a Flame-Immune player may keep wielding it, so it has no effect on them",
                        works_note="The weapon, not the person, is the target, so Enlightened Soul does not protect it"),
}


# Blocked on the player, but part of the ability still lands (slug -> (detail, short label)). Third element of a verdict.
PARTIAL = {
    "fireball": ("Weapon, Armor and Shield Destroying still hit their equipment (Immune rule 2)", "equipment still hit"),
    "lightning-bolt": ("Weapon Destroying and Armor Breaking still hit their equipment (Immune rule 2)", "equipment still hit"),
    "poison-arrow": ("Wounds Kill is Death School so it does nothing, but a Specialty Arrow still counts as a normal arrow hit (Specialty Arrows rule 5)", "arrow still lands as a normal hit"),
    "undead-minion": ("The enchantment itself applies (Enchantments rule 3), but the Raise Dead it grants is affected normally by Immunity (rule 3b)", "enchantment applies, granted Raise Dead cannot"),
}
# Rule text that overrides Traits (and so Enlightened Soul): "Will always remove Enchantments if successfully cast on a valid target,
# regardless of the player's Traits, States, Immunities...". Dispel Magic only removes Enchantments, so it works on a Monk; Sever Spirit
# also Curses, and nothing says the Curse overrides Enlightened Soul. This is a reading of the rule text, not an official clarification.
TRAIT_OVERRIDE = {
    "dispel-magic": [1, "Its text removes Enchantments 'regardless of the player's Traits', so Enlightened Soul does not stop it (a reading of the rule text, not an official ruling)"],
    "sever-spirit": [0, "Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch. Its text removes Enchantments 'regardless of the player's Traits', so that part still lands; the Curse does not (a reading of the rule text, not an official ruling)",
                     "enchantment removal still lands, the Curse does not"],
}


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def clean(s):
    return re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s or "").strip()


def load_abilities():
    ab = {}
    for f in sorted(glob.glob(os.path.join(MA, "*.md"))):
        b = os.path.basename(f)
        if b in ("INDEX.md", "_overview.md"):
            continue
        t = open(f).read()
        d = {"slug": b[:-3], "title": re.search(r'^title: "?(.*?)"?$', t, re.M).group(1),
             "pdf_page": (re.search(r"^pdf_page: (\d+)", t, re.M) or [None, ""])[1]}
        body = t.split("\n# ", 1)[1] if "\n# " in t else t
        body = re.split(r"\n---\n\*Source", body)[0]
        cur = None
        for line in body.splitlines():
            m = re.match(r"^\*\*([A-Za-z ]+):\*\*\s?(.*)$", line)
            if m and m.group(1) != "Available to":
                cur = m.group(1)
                d[cur] = m.group(2).strip()
            elif cur and line.strip():
                d[cur] += " " + line.strip()          # bullet / numbered continuation lines belong to the field
        av = re.search(r"^class_availability: \[(.*)\]", t, re.M)
        d["avail"] = [x.strip().strip('"') for x in av.group(1).split(",")] if av and av.group(1).strip() else []
        # field text for cross-reference scanning; Materials/Incantation are labels, not rules
        d["text"] = " || ".join(clean(d.get(k, "")) for k in ("Effect", "Limitations", "Note") if d.get(k))
        ab[d["slug"]] = d
    return ab


def class_range(rng, code):
    """'Other (He, Wi) Touch (Pa)' -> this class's range; plain 'Touch' -> 'Touch'."""
    parts = re.findall(r"(Self|Other|Touch|Unlimited|20'|50')\s*\(([^)]*)\)", rng or "")
    if parts:
        for r, codes in parts:
            if code in [c.strip() for c in codes.split(",")]:
                return r
        return parts[0][0]
    return (rng or "").strip()


def can_target(typ, rng):
    if typ in ("Magic Ball", "Specialty Arrow", "Magic-Ball"):
        return True
    if typ in ("Verbal", "Enchantment"):
        return bool(re.search(r"Other|Touch|Unlimited|20'|50'", rng or ""))
    return False


def _martial_rows(text):
    """Yield (level, group, segment) from a martial class's Level Progression section.
    group is '' or the 'Pick one'-style heading the segment sits under; 'Optional' rows are archetypes."""
    sec = re.search(r"## Level Progression\n(.*?)(?=\n## |\Z)", text, re.S).group(1)
    sec = re.sub(r"<br\s*/?>|\||;", "\n", sec)
    level, group = 0, ""
    for raw in sec.split("\n"):
        s = re.sub(r"^\s*[-*]+\s*", "", raw).strip().strip("*").strip()
        s = re.sub(r"^\*\*|\*\*$", "", s).strip()
        if not s or set(s) <= set("-: ") or s.startswith((">", "#")):
            continue
        if s in ORD:
            level, group = ORD[s], ""
            continue
        m = re.match(r"(1st|2nd|3rd|4th|5th|6th)\s+(.*)", s)
        if m:
            level, group, s = ORD[m.group(1)], "", m.group(2).strip()
        if re.match(r"(Level|Ability|Abilities|At 6th)", s) or re.search(r"Abilities By Level$", s):
            continue
        if s.startswith("Optional") or re.match(r"Pick ", s):
            head, _, rest = s.partition(":")
            group = "Optional" if s.startswith("Optional") else head.strip()
            s = rest.strip()
            if not s:
                continue
        yield level, group, s


def load():
    ab = load_abilities()
    titles = sorted(ab, key=lambda k: -len(ab[k]["title"]))
    classes = [dict(key=k, name=n, code=c, kind=kind, immune=[], archetypes=[], trait_notes=[], table_rows=[], ltp=[]) for k, n, c, kind in CLASSES]
    cidx = {c["name"]: i for i, c in enumerate(classes)}
    nodes, notes, byk = [], [], {}

    def add(ci, sl, level, **kw):
        key = (ci, sl)
        if key in byk:
            n = byk[key]
            if level and level not in n["levels"]:
                n["levels"].append(level)
            return
        a = ab[sl]
        n = dict(cls=classes[ci]["name"], c=ci, slug=sl, name=a["title"], levels=[level] if level else [], **kw)
        byk[key] = n
        nodes.append(n)

    for ci, (key, name, code, kind) in enumerate(CLASSES):
        text = open(os.path.join(CL, key + ".md")).read()
        lm = re.search(r"\*\*Look The Part:\*\*(.*?)(?=\n\n|\n- \*\*|\n## )", text, re.S)
        if lm and kind == "martial":
            masked, found = lm.group(1), []
            for k in titles:                                  # longest title first, so "Poison Arrow" hides "Poison"
                pat = re.compile(r"(?<![\w-])" + re.escape(ab[k]["title"]) + r"(?![\w-])")
                if pat.search(masked) and ab[k].get("Type") != "Meta-Magic":
                    found.append(k)
                    masked = pat.sub(" ", masked)
            classes[ci]["ltp"] = found
        if kind == "martial":
            for level, group, s in _martial_rows(text):
                m = re.match(r"Immune to (\w+)", s)
                if m:
                    classes[ci]["immune"].append(m.group(1))
                    continue
                if "(A)" in s:
                    classes[ci]["archetypes"].append(re.sub(r"\s*\(A\)", "", s))
                    continue
                low = s.lower()
                sl = next((k for k in titles if low.startswith(ab[k]["title"].lower())), None)
                if not sl:
                    notes.append(f"{name}: no ability file for {s!r}")
                    continue
                a = ab[sl]
                ov = re.search(r"\((Self|Other|Touch)\)", s)
                rng = ov.group(1) if ov else class_range(a.get("Range", ""), code)
                rest = s[len(a["title"]):]
                freq = re.sub(r"\s*\((m|ex|T|Self|Other|Touch)\)", "", rest)
                freq = re.sub(r"\s*\((Ambulant|Swift)\)", "", freq).strip(" -")
                note = ", ".join(re.findall(r"\((Ambulant|Swift)\)", rest))
                trait = "(T)" in s or a.get("Type") == "Trait"
                add(ci, sl, level, source="Level table", option=group, cost="", max="", freq=freq,
                    range=rng, magical="(m)" in s, trait=trait, type=a.get("Type", ""), school=a.get("School", ""),
                    tag=note)
        else:
            sec = text[text.index("## Spell List"):]
            level = 0
            for line in sec.splitlines():
                h = re.match(r"### (\d)(?:st|nd|rd|th) Level", line)
                if h:
                    level = int(h.group(1))
                    continue
                c = [x.strip() for x in line.strip().strip("|").split("|")]
                if len(c) < 7 or c[0] in ("Name", "") or set(c[0]) <= set("-"):
                    continue
                nm = clean(c[0])
                classes[ci]["table_rows"].append(dict(level=level, name=nm, cost=c[1], type=c[4]))
                if nm.startswith("Equipment:") or c[4] == "Archetype":
                    if c[4] == "Archetype":
                        classes[ci]["archetypes"].append(nm)
                    continue
                lk = re.search(r"\(\.\./magic-and-abilities/([^)]*)\.md\)", c[0])
                sl = lk.group(1) if lk else slug(nm)
                if sl not in ab:
                    notes.append(f"{name}: no ability file for {nm!r}")
                    continue
                a = ab[sl]
                add(ci, sl, level, source="Spell table", option="", cost=c[1], max=c[2] if c[2] != "-" else "",
                    freq=c[3] if c[3] != "-" else "", range=c[6] if c[6] != "-" else "", magical=True,
                    trait=(a.get("Type") == "Trait"), type=a.get("Type", c[4]), school=a.get("School", c[5]), tag="")
    for n in nodes:
        a = ab[n["slug"]]
        n["inc"] = clean(a.get("Incantation", ""))
        n["eff"] = clean(a.get("Effect", ""))
        n["target"] = can_target(n["type"], n["range"]) and not n["trait"]
        n["levels"].sort()
        n["ltp"] = n["slug"] in classes[n["c"]]["ltp"]
        n["type_display"] = "Trait" if n["trait"] else n["type"]
        v = {}
        if n["target"]:
            rule = EQUIPMENT.get(n["slug"], {})
            part = PARTIAL.get(n["slug"])
            for t in classes:
                imm = n["school"] in t["immune"]
                es = (t["name"] == "Monk" and n["type"] == "Verbal" and n["magical"]
                      and re.search(r"20'|50'|Unlimited", n["range"]))
                if imm and part:
                    v[t["name"]] = [0, f"Immune to {n['school']}. {part[0]}", part[1]]
                elif imm and n["type"] == "Enchantment":
                    v[t["name"]] = [1, "Enchantments apply despite Immunity (Enchantments rule 3)"]
                elif imm and not rule.get("ignores_immunity"):
                    why = f"Immune to {n['school']}"
                    v[t["name"]] = [0, why + ". " + rule["immune_negates"]] if rule.get("immune_negates") else [0, why]
                elif es and n["slug"] in TRAIT_OVERRIDE:
                    v[t["name"]] = list(TRAIT_OVERRIDE[n["slug"]])
                elif es and not rule.get("ignores_enlightened_soul"):
                    v[t["name"]] = [0, "Enlightened Soul: unaffected by Verbal Magical abilities used beyond Touch (still works if cast at Touch)"]
                elif (imm or es) and rule:
                    v[t["name"]] = [1, rule["works_note"]]
                else:
                    v[t["name"]] = [1, ""]
        n["v"] = v
    return dict(ab=ab, classes=classes, cidx=cidx, nodes=nodes, notes=notes, refs=references(ab))


RANK = {"grants": 0, "removes": 1, "replaces": 2, "modifies": 3, "borrows": 4, "mentions": 5}


def references(ab):
    """Auto-detected cross-references between ability texts (Effect, Limitations, Note).
    Returns {slug: [(other_slug, relation)]}: *slug's text* names other_slug.
    relation: grants (gain / may cast / Replace-X-with-Y's Y / becomes / additional use of), removes (lose),
    replaces (Replace X with Y's X), modifies (X becomes ...), borrows (as per X), mentions (anything else).
    Names in one list ("Blink, Shadow Step and Teleport") share the first name's relation. A parenthesised
    Meta-Magic name such as '(Ambulant)' is a tag on the granted ability, not a reference."""
    order = sorted(ab, key=lambda k: -len(ab[k]["title"]))
    out = {}
    for sl, a in ab.items():
        if a["title"].startswith("Equipment:"):
            out[sl] = []
            continue
        text = a["text"]
        masked = re.sub(re.escape(a["title"]), lambda m: " " * len(m.group(0)), text)   # own name (and names inside it)
        hits = []
        for ok in order:
            if ok == sl:
                continue
            t = ab[ok]["title"]
            for m in re.finditer(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", masked):
                hits.append((m.start(), m.end(), ok))
                masked = masked[:m.start()] + " " * len(t) + masked[m.end():]
        hits.sort()
        rels = []
        for start, end, ok in hits:
            brk = max(text.rfind(".", 0, start), text.rfind("||", 0, start))
            before = text[brk + 1:start].lower()
            after = text[end:end + 16].lower()
            if ab[ok].get("Type") == "Meta-Magic" and start > 0 and text[start - 1] == "(":
                rels.append(None)                                        # tag on another ability
                continue
            if re.search(r"\bas per\s*$|\beffects? of\s*$", before):
                rel = "borrows"
            elif re.search(r"\breplace", before):
                rel = "grants" if " with " in before[before.rfind("replace"):] else "replaces"
            elif re.search(r"\blose\b", before):
                rel = "removes"
            elif re.search(r"\bgains?\b|\bmay(?: cast)?\s*$|\bbecomes?\s*$|\badditional use of\s*$", before):
                rel = "grants"
            elif re.match(r"\W*(?:\([^)]*\)\s*)*\W*(?:becomes?|now)\b", after):
                rel = "modifies"
            else:
                rel = "mentions"
            rels.append(rel)
        # names in one list ("Blink, Shadow Step, and Teleport"; "Blink and Shadow Step become ...") share the strongest relation
        i = 0
        while i < len(hits):
            j = i
            while j + 1 < len(hits) and re.fullmatch(r"\s*(?:,\s*)?(?:(?:and|or)\s+)?", text[hits[j][1]:hits[j + 1][0]]):
                j += 1
            grp = [r for r in rels[i:j + 1] if r and r != "mentions"]
            if grp:
                best = min(grp, key=RANK.get)
                for k in range(i, j + 1):
                    if rels[k]:
                        rels[k] = best
            i = j + 1
        found = {}
        for (start, end, ok), rel in zip(hits, rels):
            if rel and (ok not in found or RANK[rel] < RANK[found[ok]]):
                found[ok] = rel
        out[sl] = sorted(found.items())
    return out


if __name__ == "__main__":
    D = load()
    print(len(D["nodes"]), "nodes;", D["notes"])
    for c in D["classes"]:
        print(c["name"], c["immune"], c["archetypes"])
