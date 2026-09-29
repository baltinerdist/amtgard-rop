#!/usr/bin/env python3
"""Build viewer/ability-chords.html: a chord diagram of how each class's abilities and spells
interact with every other class.

Model (all classes at 6th level, every ability/spell on their lists, archetypes and spell points
ignored):
  * one NODE per (class, ability) - martial classes from their level tables, the four Magic User
    classes from their spell tables;
  * BLUE link  - the same ability sits on two classes' lists;
  * GREEN/RED  - from an ability that can target another player to each of the 12 classes: red when
    the target class's Immunities (or Enlightened Soul) stop it, green otherwise.

Source data is rules/classes/*.md and rules/magic-and-abilities/*.md, so it follows the rulebook
edition in scripts/rop_version.py. Run:  python3 scripts/build_chord.py
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rop_version as V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MA = os.path.join(ROOT, "rules/magic-and-abilities")
CL = os.path.join(ROOT, "rules/classes")
TEMPLATE = os.path.join(ROOT, "viewer/chord-template.html")
OUT = os.path.join(ROOT, "viewer/ability-chords.html")

import interop_data as I

def main():
    D = I.load()
    for n in D["notes"]:
        print("NOTE", n)
    nodes = D["nodes"]
    for n in nodes:
        n["lv"] = ", ".join({1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}[x] for x in n["levels"])
    keep = ("cls", "slug", "name", "type", "school", "range", "freq", "magical", "trait", "inc", "eff", "target", "v", "lv", "cost", "max")
    monk_note = ("Enlightened Soul stops Verbal Magical abilities used beyond Touch. "
                 "Missile Block can also nullify arrows and Magic Balls aimed at a Monk, but it needs an active "
                 "block, so those stay green.")
    data = dict(edition=V.NAME, classes=[dict(name=c["name"], code=c["code"], kind=c["kind"], immune=c["immune"]) for c in D["classes"]],
                nodes=[{k: n[k] for k in keep} for n in nodes], monkNote=monk_note)
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=True).replace("</", "<\\/")
    tpl = open(TEMPLATE, encoding="utf-8").read()
    assert tpl.count("__DATA__") == 1
    html = tpl.replace("__DATA__", blob).replace("__EDITION__", V.NAME)
    open(OUT, "w", encoding="utf-8").write(html)
    per = {}
    for n in nodes: per[n["cls"]] = per.get(n["cls"], 0) + 1
    ver = [n["v"] for n in nodes]
    red = sum(1 for v in ver for x in v.values() if not x[0]); grn = sum(1 for v in ver for x in v.values() if x[0])
    shared = {}
    for n in nodes: shared.setdefault(n["slug"], []).append(n["cls"])
    blue = sum(len(c) * (len(c) - 1) // 2 for c in shared.values())
    print(f"wrote {OUT}: {len(nodes)} nodes {per}\n  targeting nodes {sum(1 for n in nodes if n['target'])}; green {grn}, red {red}, blue {blue}")

if __name__ == "__main__":
    main()
