#!/usr/bin/env python3
"""Generate the ability/spell <-> class interoperability reference in interoperability/.

  interoperability/README.md            model, assumptions, how to answer "what if we move X" questions
  interoperability/MATRIX.md            every targeting ability x the 12 classes (works / blocked)
  interoperability/abilities/<slug>.md  one file per ability (where listed, effect on each class, links, level notes)
  interoperability/classes/<class>.md   one file per class (level list, what it shrugs off, what it hits)

Everything is derived from rules/ (see scripts/interop_data.py for the model); nothing is typed by hand.
Run:  python3 scripts/gen_interop.py
"""
import os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import interop_data as I
import rop_version as V
try:
    import meta_build as MB
    META = __import__("json").load(open(os.path.join(I.ROOT, "metadata", "abilities.json")))["abilities"]
except Exception:            # the metadata layer is optional: run scripts/meta_build.py first to include it
    MB, META = None, {}

ROOT = I.ROOT
OUT = os.path.join(ROOT, "interoperability")
ORDN = {0: "-", 1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}
REL = {"grants": "grants or gives", "removes": "removes", "replaces": "replaces", "modifies": "changes its numbers",
       "borrows": "borrows its effect", "mentions": "mentions"}
LEVEL_TEXT = re.compile(r"\b(?:\d(?:st|nd|rd|th) level|level \d)\b", re.I)


def lv(levels):
    return ", ".join(ORDN.get(x, str(x)) for x in levels) if levels else "-"


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def fm(title, extra=()):
    lines = ["---", f'title: "{title}"', "section: Interoperability", f"rulebook_version: {V.NAME}",
             f"rulebook_date: {V.DATE}", "source: Derived from rules/classes and rules/magic-and-abilities (scripts/gen_interop.py)"]
    return lines + list(extra) + ["---", ""]


def status(v):
    """'works' | 'blocked' | 'partial' for one verdict."""
    if v[0]:
        return "works"
    return "partial" if len(v) > 2 else "blocked"


def main():
    D = I.load()
    for n in D["notes"]:
        print("NOTE", n)
    ab, classes, nodes, refs = D["ab"], D["classes"], D["nodes"], D["refs"]
    cname = {c["name"]: c for c in classes}
    corder = {c["name"]: i for i, c in enumerate(classes)}
    by_slug, by_class = {}, {c["name"]: [] for c in classes}
    for n in nodes:
        by_slug.setdefault(n["slug"], []).append(n)
        by_class[n["cls"]].append(n)
    referenced_by = {}
    for sl, lst in refs.items():
        for other, rel in lst:
            referenced_by.setdefault(other, []).append((sl, rel))

    # Experienced-style level gates, read from the rule text: "Verbal must be 4th level or lower."
    gate = re.search(r"Verbal must be (\d)(?:st|nd|rd|th) level or lower", ab["experienced"].get("Limitations", ""))
    exp_max = int(gate.group(1)) if gate else None

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "abilities"))
    os.makedirs(os.path.join(OUT, "classes"))

    def ab_link(sl):
        return f"[{ab[sl]['title']}]({sl}.md)"

    def class_link(name):
        return f"[{name}](../classes/{cname[name]['key']}.md)"

    def where(sl):
        if sl not in by_slug:
            return [x.rsplit(" ", 1)[0] for x in ab[sl].get("avail", [])]
        return sorted({n["cls"] for n in by_slug[sl]}, key=lambda x: corder[x])

    # ------------------------------------------------------------ per-ability files
    for sl, a in sorted(ab.items()):
        ns = by_slug.get(sl, [])
        title = a["title"]
        targeting = any(n["target"] for n in ns)
        o = fm(f"{title} \u2014 Interoperability", [
            f"ability: {title}", f"type: {a.get('Type', '')}", f"school: {a.get('School', '')}",
            f"targets_other_players: {'true' if targeting else 'false'}",
            "classes: [" + ", ".join(f'"{n["cls"]} {lv(n["levels"])}"' for n in ns) + "]"])
        o += [f"# {title} \u2014 Interoperability", "",
              f"[Rule text](../../rules/magic-and-abilities/{sl}.md) \u00b7 **{a.get('Type', '')}**" + (f" \u00b7 {a['School']} School" if a.get("School") else "")
              + (f" \u00b7 Range {a['Range']}" if a.get("Range") else ""), ""]

        # ---- summary
        o += ["## Summary", ""]
        if not ns:
            av = ", ".join(ab[sl].get("avail", [])) or "none"
            if a.get("Type") == "Archetype":
                o.append(f"- **Archetype.** Chosen at 6th level ({av}). Archetypes are outside this model, so it has no works/blocked results here.")
            elif title.startswith("Equipment:"):
                o.append(f"- **Equipment trait.** Magic Users buy it from their spell tables ({av}); Equipment rows are left out of this model.")
            else:
                gr = [x for x, rel in referenced_by.get(sl, []) if rel == "grants" and ab[x].get("Type") == "Archetype"]
                o.append("- **Not on any class list.** It is only available through other abilities"
                         + (f" ({', '.join(ab[x]['title'] for x in gr)})" if gr else "") + f"; frontmatter availability: {av}.")
        else:
            if targeting:
                res = {}
                for c in classes:
                    vs = [n["v"][c["name"]] for n in ns if c["name"] in n["v"]]
                    sts = {status(v) for v in vs}
                    res[c["name"]] = sts.pop() if len(sts) == 1 else "mixed"
                nw = sum(1 for x in res.values() if x == "works")
                o.append("- **Can affect another player:** yes.")
                o.append(f"- **Works on:** {nw} of 12 classes.")
                bl = [c for c, x in res.items() if x == "blocked"]
                pt = [c for c, x in res.items() if x == "partial"]
                mx = [c for c, x in res.items() if x == "mixed"]
                if bl:
                    o.append("- **Blocked on:** " + ", ".join(bl) + ".")
                if pt:
                    o.append("- **Partly blocked on:** " + ", ".join(
                        f"{c} ({next(v[2] for n in ns for v in [n['v'][c]] if len(v) > 2)})" for c in pt) + ".")
                if mx:
                    o.append("- **Depends on which class's version:** " + ", ".join(mx) + " (see the table below).")
                if not (bl or pt or mx):
                    o.append("- **Blocked on:** no class.")
            else:
                why = "it is a Trait" if any(n["trait"] for n in ns) else "its range is Self or it has no target"
                o.append(f"- **Can affect another player:** no ({why}), so it has no works/blocked results. It can still be shared between classes.")
                gr = [x for x, rel in refs.get(sl, []) if rel == "grants" and any(m["target"] for m in by_slug.get(x, []))]
                if gr:
                    o.append("- **Indirect effects:** it grants " + ", ".join(ab_link(x) for x in gr)
                             + ", which can affect other players; see those files for who they work on. This model does not compute the indirect effect itself.")
            lst = where(sl)
            o.append(f"- **On {len(lst)} class list{'s' if len(lst) != 1 else ''}:** " +
                     ", ".join(f"{c} ({lv(next(n for n in ns if n['cls'] == c)['levels'])})" for c in lst) + ".")
        o.append("")

        # ---- what it does (from metadata/)
        mt = META.get(sl)
        if mt:
            o += ["## What it does", "", mt["summary"], "", "| Effect | On | Details |", "| --- | --- | --- |"]
            for e in mt["effects"]:
                o.append(f"| {e['label']} | {e['subject']} ({e['polarity']}) | {esc(MB.effect_detail(e))} |")
            o += ["", "**Capabilities:** " + (", ".join(mt["derived"]["capabilities"]) or "-") + " \u00b7 **Roles:** " + ", ".join(mt["roles"]), "",
                  f"Full profile (requirements, how it ends, properties, what stops it, similar abilities, every rule sentence): "
                  f"[`metadata/profiles/{sl}.md`](../../metadata/profiles/{sl}.md).", ""]

        # ---- where listed
        if ns:
            o += ["## Where it is listed", "",
                  "| Class | Level | Cost | Max | Frequency | Range here | Magical | Listed in | Notes |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
            for n in ns:
                notes = []
                if n["option"]:
                    notes.append(n["option"])
                if n["tag"]:
                    notes.append(n["tag"])
                if len(n["levels"]) > 1:
                    notes.append("listed again at each of these levels")
                if n["ltp"]:
                    notes.append("also the class's Look The Part, so the class has it from 1st level whatever level the table gives")
                mag = "n/a (Trait)" if n["trait"] else "yes" if n["magical"] else "no (ex)"
                o.append(f"| {class_link(n['cls'])} | {lv(n['levels'])} | {n['cost'] or '-'} | {n['max'] or '-'} | {esc(n['freq']) or '-'} | "
                         f"{n['range'] or '-'} | {mag} | {n['source']} | {esc('; '.join(notes)) or '-'} |")
            o.append("")

        # ---- effect on each class
        o += ["## Effect on each class", ""]
        if targeting:
            o += ["Assumes every class is 6th level. Results do not depend on level.", "",
                  "| Target class | Result | Why |", "| --- | --- | --- |"]
            for c in classes:
                vs = [n["v"][c["name"]] for n in ns if c["name"] in n["v"]]
                sts = [status(v) for v in vs]
                first = vs[0]
                if all(x == "works" for x in sts):
                    o.append(f"| {class_link(c['name'])} | Works | {esc(next((v[1] for v in vs if v[1]), ''))} |")
                elif all(x == "blocked" for x in sts):
                    o.append(f"| {class_link(c['name'])} | **Blocked** | {esc(first[1])} |")
                elif all(x == "partial" for x in sts):
                    o.append(f"| {class_link(c['name'])} | **Partly blocked:** {esc(first[2])} | {esc(first[1])} |")
                else:
                    detail = "; ".join(f"{n['cls']}'s version: {status(n['v'][c['name']])}" + (f" ({esc(n['v'][c['name']][1])})" if n['v'][c['name']][1] and not n['v'][c['name']][0] else "")
                                       for n in ns if c["name"] in n["v"])
                    o.append(f"| {class_link(c['name'])} | **Depends on the listing** | {detail} |")
            o.append("")
            if any(n["type"] in ("Magic Ball", "Specialty Arrow") for n in ns):
                o += ["Monks can block Magic Balls and arrows with Missile Block, but that needs an active block, so it is shown as working.", ""]
            if any(n["range"] in ("Touch", "Other") for n in ns):
                o += ["Touch and Other range also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move. That applies to every class alike and is not modelled.", ""]
        elif not ns:
            o += ["Not modelled: it is not on a class list, so the works/blocked results are not computed here. "
                  + (f"Its range is {a['Range']}; see the abilities that grant it under Connected abilities." if a.get("Range") else ""), ""]
        else:
            o += ["Not applicable: this ability does not target another player.", ""]

        # ---- connected abilities
        o += ["## Connected abilities", ""]
        mine, rb = refs.get(sl, []), referenced_by.get(sl, [])
        lst = where(sl)
        if not mine and not rb and len(lst) < 2:
            o += ["No other ability's text names it, and it names no other ability.", ""]
        if mine:
            o += [f"**{title} names these abilities in its own text** (auto-detected):", "",
                  "| Ability | How | On classes |", "| --- | --- | --- |"]
            for other, rel in mine:
                o.append(f"| {ab_link(other)} | {REL[rel]} | {', '.join(where(other)) or '-'} |")
            o.append("")
        if rb:
            o += [f"**These abilities name {title} in their text** (auto-detected). If {title} is renamed, moved or removed, check them:", "",
                  "| Ability | How | On classes |", "| --- | --- | --- |"]
            for other, rel in sorted(rb):
                o.append(f"| {ab_link(other)} | {REL[rel]} | {', '.join(where(other)) or '-'} |")
            o.append("")
        if len(lst) > 1:
            o += [f"**Shared with:** {', '.join(class_link(c) for c in lst)}. Changing this ability changes it for every one of these classes unless the classes get separate versions.", ""]
        grants = []
        for g in re.findall(r"(?<!who )(?:is|are|becomes) Immune to (one of the following Schools: [^.]*|(?:the )?[A-Z]\w+)", a.get("Effect", "")):
            g = re.sub(r"^the ", "", g)
            grants.append(g.replace("one of the following Schools: ", "one of: "))
        if grants:
            o += [f"**Grants immunity:** the effect text says the bearer is Immune to {'; '.join(dict.fromkeys(grants))}. That immunity would stop any targeting ability of that School.", ""]

        # ---- level notes
        o += ["## If you change its level", ""]
        lvl_sents = []
        for k in ("Effect", "Limitations", "Note"):
            for sent in re.split(r"(?<=[.!?])\s+", a.get(k, "")):
                if LEVEL_TEXT.search(sent):
                    lvl_sents.append(sent.strip())
        if lvl_sents:
            o += ["**Its own text mentions a level:**"] + [f"- \u201c{esc(x)}\u201d" for x in lvl_sents] + [""]
        if ns:
            o += ["- Who it works on does not change with level: class Immunities are 1st-level Traits, and Enlightened Soul is a 1st-level Monk Trait.",
                  "- What can change: which classes can use it at a given level, what it competes with at that level, and any archetype or ability that depends on it (see above).", ""]
            for n in ns:
                c = cname[n["cls"]]
                line = f"- **{n['cls']}** lists it at {lv(n['levels'])}"
                if c["kind"] == "magic":
                    L = n["levels"][0]
                    rows = [r for r in c["table_rows"] if r["level"] == L]
                    pts = sum(int(r["cost"]) for r in rows if r["cost"].isdigit())
                    ne = sum(1 for r in rows if r["name"].startswith("Equipment:"))
                    na = sum(1 for r in rows if r["type"] == "Archetype")
                    line += (f" for {n['cost']} point{'s' if n['cost'] != '1' else ''}. That level's table has {len(rows)} entries "
                             f"({pts} points if each were bought once, including {ne} Equipment trait{'s' if ne != 1 else ''} and {na} Archetype{'s' if na != 1 else ''}). "
                             f"A Magic User has five points per level, and unused points roll down to lower levels, not up (see the README).")
                    if exp_max and n["type"] == "Verbal" and n["slug"] != "experienced" and any(m["slug"] == "experienced" for m in by_class[n["cls"]]):
                        per = re.match(r"\d+/(Life|Refresh)", n["freq"] or "")
                        line += (f" **Experienced** (also on this list) only works on a single per-life or per-refresh Verbal of {ORDN[exp_max]} level or lower. "
                                 + ("This one is Unlimited, so it is not eligible at any level." if not per
                                    else f"This Verbal is eligible now but would not be if moved above {ORDN[exp_max]}." if L <= exp_max
                                    else "This Verbal is already too high for it."))
                else:
                    same = [m["name"] for m in by_class[n["cls"]] if m is not n and set(m["levels"]) & set(n["levels"])]
                    if 1 in n["levels"]:
                        same += [f"Immune to {x} (Trait)" for x in c["immune"]]
                    line += ("; " + (f"{len(same)} other entr{'y shares' if len(same) == 1 else 'ies share'} that level: " + ", ".join(same) if same
                                     else "nothing else is listed at that level") + ".")
                    if n["option"]:
                        line += f" It is one of a group ({n['option']})."
                if n["ltp"]:
                    line += " It is also this class's Look The Part, so the class has it at 1st level regardless."
                arch = [x for x in c["archetypes"] if sl in dict(refs.get(I.slug(x), []))]
                if arch:
                    line += f" Archetype{'s' if len(arch) > 1 else ''} that name{'' if len(arch) > 1 else 's'} it: {', '.join(arch)} (archetypes are outside this model)."
                o.append(line)
            o.append("")
        elif not lvl_sents:
            o += ["Not on a class list, so its level is set by whatever grants it (see above).", ""]
        o += ["---", f"*Derived from the {V.NAME} rules by `scripts/gen_interop.py`. Cross-references are detected from ability text and should be read as pointers, not rulings.*", ""]
        open(os.path.join(OUT, "abilities", sl + ".md"), "w").write("\n".join(o))

    # ------------------------------------------------------------ per-class files
    for c in classes:
        mine = by_class[c["name"]]
        o = fm(f"{c['name']} \u2014 Interoperability", [f"kind: {c['kind']}", "immunities: [" + ", ".join(f'"{s}"' for s in c["immune"]) + "]"])
        o += [f"# {c['name']} \u2014 Interoperability", "",
              f"[Class rules](../../rules/classes/{c['key']}.md) \u00b7 {'Magic User' if c['kind'] == 'magic' else 'Martial'} \u00b7 {len(mine)} abilities on its list, "
              f"{sum(1 for n in mine if n['target'])} of which can affect another player.", ""]
        o += ["## Defenses", ""]
        if c["immune"]:
            o += [f"- Immune to {', '.join(c['immune'])}. Any targeting ability from those Schools does not work on the player. Immunities do not extend to carried equipment or worn armor, "
                  "and Enchantments still apply (Enchantments rule 3)."]
        if c["name"] == "Monk":
            o += ["- Enlightened Soul: unaffected by Verbal Magical abilities used at a Range greater than Touch. It does not affect (ex) abilities, abilities used at Touch, or carried equipment and worn armor.",
                  "- Missile Block can nullify arrows, projectile weapons and Magic Balls with hands or wielded weapons; it needs an active block, so this model still shows them as working."]
        if not c["immune"] and c["name"] != "Monk":
            o += ["- No permanent Immunities. Every targeting ability works on this class."]
        o += ["", f"Archetypes (ignored in this model): {', '.join(c['archetypes']) or 'none'}.", ""]
        if c["kind"] == "martial" and c["ltp"]:
            o += ["Look The Part (available from 1st level): " + ", ".join(f"[{ab[x]['title']}](../abilities/{x}.md)" for x in c["ltp"]) + ".", ""]
        elif c["kind"] == "magic":
            o += ["Look The Part: one extra magic point at the class's highest level (six points at 6th level).", ""]
        # by level
        o += ["## Abilities by level", "",
              "| Level | Ability | Cost | Max | Frequency | Type | School | Range | Affects others | Blocked on |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        rows = []
        for n in mine:
            for L in (n["levels"] or [0]):
                rows.append((L, n["name"], n))
        for x in c["immune"]:
            rows.append((1, f"Immune to {x}", None))
        for L, nm, n in sorted(rows, key=lambda r: (r[0], r[1])):
            if n is None:
                o.append(f"| {ORDN[L]} | {nm} (Trait) | - | - | always on | Trait | {nm.split()[-1]} | - | no | - |")
                continue
            blocked = [f"{t}{' (partly)' if len(v) > 2 else ''}" for t, v in n["v"].items() if not v[0]]
            o.append(f"| {ORDN[L]} | [{n['name']}](../abilities/{n['slug']}.md){' (' + n['option'] + ')' if n['option'] else ''}{' \u2014 Look The Part' if n['ltp'] else ''} | "
                     f"{n['cost'] or '-'} | {n['max'] or '-'} | {esc(n['freq']) or '-'} | {n['type_display']} | {n['school']} | {n['range'] or '-'} | "
                     f"{'yes' if n['target'] else 'no'} | {', '.join(blocked) or '-'} |")
        o.append("")
        if c["kind"] == "magic":
            o += ["### Points per level", "", "A Magic User has five points per level (six at the highest level). This is the size of each level's table, counting every entry once.", "",
                  "| Level | Entries | Points if each bought once | Equipment traits | Archetypes |", "| --- | --- | --- | --- | --- |"]
            for L in range(1, 7):
                rs = [r for r in c["table_rows"] if r["level"] == L]
                o.append(f"| {ORDN[L]} | {len(rs)} | {sum(int(r['cost']) for r in rs if r['cost'].isdigit())} | "
                         f"{sum(1 for r in rs if r['name'].startswith('Equipment:'))} | {sum(1 for r in rs if r['type'] == 'Archetype')} |")
            o.append("")
        # what blocks
        shrug = [(m, m["v"][c["name"]]) for m in nodes if m["target"] and c["name"] in m["v"] and not m["v"][c["name"]][0]]
        o += [f"## What blocks on {c['name']}", ""]
        if shrug:
            o += [f"{len(shrug)} class-list entries across all classes cannot fully affect {'an' if c['name'][0] in 'AEIOU' else 'a'} {c['name']}:", "",
                  "| Ability | From class | Result | Why |", "| --- | --- | --- | --- |"]
            for m, v in sorted(shrug, key=lambda x: (x[1][1], x[0]["name"], x[0]["cls"])):
                o.append(f"| [{m['name']}](../abilities/{m['slug']}.md) | {m['cls']} | {'Partly blocked: ' + v[2] if len(v) > 2 else 'Blocked'} | {esc(v[1])} |")
        else:
            o.append("Nothing. Every targeting ability on every class list works on this class.")
        o.append("")
        # what it hits
        o += [f"## What {c['name']} abilities do to each class", "", "| Target class | Works | Blocked | Blocked abilities |", "| --- | --- | --- | --- |"]
        tg = [n for n in mine if n["target"]]
        for t in classes:
            g = [n for n in tg if n["v"][t["name"]][0]]
            r = [n for n in tg if not n["v"][t["name"]][0]]
            o.append(f"| [{t['name']}]({t['key']}.md) | {len(g)} | {len(r)} | {', '.join(n['name'] + (' (partly)' if len(n['v'][t['name']]) > 2 else '') for n in r) or '-'} |")
        o.append("")
        o += ["## Abilities shared with other classes", "", "| Class | Shared | Abilities |", "| --- | --- | --- |"]
        for t in classes:
            if t is c:
                continue
            sh = [n for n in mine if any(m["cls"] == t["name"] for m in by_slug[n["slug"]])]
            if sh:
                o.append(f"| [{t['name']}]({t['key']}.md) | {len(sh)} | {', '.join(f'[{n['name']}](../abilities/{n['slug']}.md)' for n in sh)} |")
        o += ["", "---", f"*Derived from the {V.NAME} rules by `scripts/gen_interop.py`.*", ""]
        open(os.path.join(OUT, "classes", c["key"] + ".md"), "w").write("\n".join(o))

    # ------------------------------------------------------------ matrix
    o = fm("Ability \u00d7 class matrix") + ["# Ability \u00d7 class matrix", "",
        "Every ability that can affect another player, against the twelve classes. Columns are the *target* class; the second column lists which classes own the ability.", "",
        "`\u2713` works \u00b7 `\u2715` blocked \u00b7 `\u25d0` blocked on the player but part of it still lands (see the ability file) \u00b7 `\u2713/\u2715` depends on which class's version is used.", "",
        "| Ability | On classes | School | " + " | ".join(c["code"] for c in classes) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in classes) + " |"]
    for sl in sorted(ab, key=lambda k: ab[k]["title"]):
        ns = [n for n in by_slug.get(sl, []) if n["target"]]
        if not ns:
            continue
        cells = []
        for c in classes:
            sts = {status(n["v"][c["name"]]) for n in ns}
            cells.append("\u2713" if sts == {"works"} else "\u2715" if sts == {"blocked"} else "\u25d0" if sts == {"partial"} else "\u2713/\u2715")
        owners = ", ".join(next(c["code"] for c in classes if c["name"] == n["cls"]) for n in by_slug[sl])
        o.append(f"| [{ab[sl]['title']}](abilities/{sl}.md) | {owners} | {ab[sl].get('School', '')} | " + " | ".join(cells) + " |")
    o += ["", "Column key: " + ", ".join(f"{c['code']} = {c['name']}" for c in classes) + ".", ""]
    open(os.path.join(OUT, "MATRIX.md"), "w").write("\n".join(o))

    # ------------------------------------------------------------ README
    wiz = open(os.path.join(I.CL, "wizard.md")).read()
    mu = re.search(r"## Magic User\n\n(.*?)\n\n", wiz, re.S).group(1)
    ov = open(os.path.join(I.CL, "_overview.md")).read()
    tot_t = sum(1 for n in nodes if n["target"])
    o = fm("Ability and class interoperability") + [
        "# Ability and class interoperability", "",
        f"How every ability and spell in the {V.NAME} rulebook relates to the classes: who has it, at what level, who it works on, "
        "what stops it, and which other abilities name it. Built to answer questions such as *what happens if this ability moves from 4th to 6th level*.", "",
        "## Files", "",
        f"- [`abilities/`](abilities/): one file per ability ({len(ab)} files). Start here for a specific spell.",
        "- [`classes/`](classes/): one file per class (12): level list, what the class is immune to, what its abilities do to every other class.",
        "- [`MATRIX.md`](MATRIX.md): every targeting ability against all 12 classes on one page.",
        "- The interactive version is `viewer/ability-chords.html` (chord diagram).", "",
        "## The model", "",
        "- **Nodes:** one per (class, ability) pair on a class list. The four Magic User classes come from their spell tables, the eight martial classes from their level tables. "
        f"That gives {len(nodes)} pairs covering {len(by_slug)} distinct abilities.",
        "- **Assumptions:** every class is 6th level and has every ability on its list, including every option of a \"Pick one\" group. "
        "Archetypes, spell points, purchase limits and the Equipment traits are ignored.",
        "- **Look The Part:** each martial class also gets one ability from 1st level (Anti-Paladin Terror, Archer one arrow, Assassin Poison or Poison Arrow, Barbarian Rage, Monk Heal, Paladin Awe, Scout Heal, Warrior Insult), "
        "and a Magic User gets one extra magic point at their highest level (six at 6th level). The level in the class table is when the class earns the ability normally; Look The Part can give it earlier.",
        f"- **Can affect another player:** a Verbal or Enchantment whose range (for that class) is Other, Touch, 20', 50' or Unlimited, or any Magic Ball or Specialty Arrow. "
        f"Traits and Self-only abilities cannot. {tot_t} class-list entries qualify. Self-range abilities that grant another ability (for example Snaring Vines granting Hold Person) are not counted as targeting, "
        "but their file says what they grant.",
        "- **Blocked** means the target class cannot be affected, for one of two reasons:",
        "  - the ability's School is one the target class is Immune to: Anti-Paladin (Command, Flame), Barbarian (Command, Subdual), Paladin (Command, Death);",
        "  - the target is a Monk and the ability is a Verbal Magical ability used beyond Touch (Enlightened Soul). The Monk is still affected if the ability is cast at Touch, and (ex) abilities are never stopped. "
        "Martial abilities are Magical only when their class table marks them (m); all Magic User abilities are Magical. "
        "Dispel Magic and Sever Spirit say they work \"regardless of the player's Traits\". This model reads that as overriding Enlightened Soul for the Enchantment removal (Dispel Magic works on a Monk; Sever Spirit is partly blocked because the Curse is not covered). That is a reading of the rule text, not an official clarification, so their files say so.",
        "- **Enchantments ignore Immunities.** The rulebook says Immunities, Traits and other Enchantments do not prevent new Enchantments (Enchantments rule 3), and effects imparted directly by the enchantment still work. "
        "So Enchantments of an immune School (Poison, Flame Blade, Toxic Blades and the like) are shown as working. Abilities the enchantment grants are still subject to Immunity (rule 3b), which is why Undead Minion is only partly blocked on a Paladin.",
        "- **Equipment is not protected.** Immunities and Enlightened Soul protect the player, not carried equipment or worn armor (Immune rules 2 and 4, and the Notes on Pyrotechnics, Destroy Armor, Heat Weapon and Shatter Weapon). "
        "So Pyrotechnics, Destroy Armor and Shatter Weapon are shown as working on immune classes; Heat Weapon works on a Monk but not on an Anti-Paladin (a Flame-Immune player may keep wielding the weapon).",
        "- **Partly blocked (\u25d0):** the player is unaffected but something still lands. Fireball and Lightning Bolt still hit an Anti-Paladin's equipment, and a Poison Arrow still counts as a normal arrow hit on a Paladin (Specialty Arrows rule 5).",
        "- **Works** is everything else. Monk Missile Block (an active block of arrows and Magic Balls) is not counted as a block. "
        "Touch and Other range abilities (Other means Touch range) also need the target to be willing, dead, stunned, frozen or Insubstantial and unable to move; and Enchantments may only be cast on willing players. "
        "Those apply to every class equally and are not modelled.",
        "- **Temporary defenses are out of scope**, for example Barbarian Rage (unaffected by Verbal abilities while it lasts), the Invulnerable and Insubstantial States, Circle of Protection and Sanctuary. "
        "So is Enlightened Soul or Song of Interference given to a non-Monk. Only permanent class Traits count.",
        "- **Shared** means the same ability appears on more than one class list.",
        "- **Connected** abilities come from automatic text matching: an ability that names another in its Effect, Limitations or Note. "
        "The relation is guessed from the wording (grants after \"Gain\" or \"may cast\", removes after \"Lose\", replaces, changes its numbers after \"becomes\", borrows after \"as per\", otherwise mentions). Treat these as pointers to read, not rulings.", "",
        "## Answering \"what if we move this ability to another level?\"", "",
        "1. Open `abilities/<name>.md`. **Where it is listed** shows every class that has it and its level, cost, max and frequency there, and flags Look The Part.",
        "2. **Effect on each class** will not change: immunities are 1st-level Traits, so moving an ability between levels never changes who it works on. "
        "It only matters if the change also changes the ability's School, type or range.",
        "3. **Its own text mentions a level** (when present) quotes rule text that depends on a level, for example Experienced only working on a Verbal of 4th level or lower, or Hunter's \"only if that ability was chosen at level 4\".",
        "4. **Connected abilities** lists archetypes and other abilities that name it. Each may assume the current level or class list.",
        "5. For a Magic User, check the level budget. The rulebook says:", "",
        f"   > {mu}", "",
        "   So a spell moved to 6th level competes for that level's five points (six with Look The Part), and points from a higher level can be used on lower levels but not the reverse. "
        "The **If you change its level** section counts the entries and points in that level's table, including the Equipment traits and Archetypes that draw on the same points.",
        "6. For a martial class, look at the class file: the level table shows what else sits at the target level (including the class's Immune traits at 1st), and some levels are pick-one groups.",
        "7. If the ability is shared, decide whether every class moves it or only one. The **Shared with** line names them.", "",
        "## Class rule text used here", "",
        "> " + re.search(r"> \*\*Classes Made Easy\*\*\n>\n> (Classes have levels\..*?)\n", ov).group(1), "",
        "---", f"*Generated by `scripts/gen_interop.py` from `rules/` ({V.NAME}). Regenerate after any rulebook update.*", ""]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(o))
    print(f"wrote {len(ab)} ability files, {len(classes)} class files, MATRIX.md, README.md to {OUT}")


if __name__ == "__main__":
    main()
