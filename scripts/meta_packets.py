#!/usr/bin/env python3
"""Write agent input packets for the Ability Metadata Platform.

  meta_packets.py OUT_DIR NAME slug [slug ...]          one packet file OUT_DIR/NAME.md (+ NAME.slugs)
  meta_packets.py OUT_DIR --shards N [--by type|alpha]   split every entry in scope into N packets

A packet shows, per entry: the deterministic facets (identity, casting, class availability) and the numbered rule sentences the
record must cite, plus hints of what the text names (abilities, States, Special Effects, mechanics).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_source as MS
import meta_vocab as V

ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}
MECH_WORDS = {"alternate base": "alternate-base", "forced movement": "forced-movement", "engulfing": "engulfing", "chant": "chant",
              "charge": "charge", "empty hand": "empty-hand", "magic armor": "magic-armor", "persistent": "persistent", "respawn": "respawn",
              "refresh": "refresh", "base": "base", "strip": "strips", "declar": "declaration", "enchantment limit": "enchantment-limit",
              "ability order": "ability-order", "reeve": "reeve", "look the part": "look-the-part", "trigger": "trigger",
              "immune": "immune", "resistan": "resistant", "incantation": "incantation", "meta-magic": "meta-magic", "archetype": "archetype"}


def hints(e, titles):
    text = " ".join(s["text"] for s in e["sentences"])
    low = text.lower()
    masked = text.replace(e["title"], " ")
    abil = []
    for t in sorted(titles, key=len, reverse=True):
        if t != e["title"] and re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", masked):
            abil.append(t)
            masked = re.sub(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", " ", masked)
    states = [s for s in V.STATES if re.search(r"\b" + s + r"\b", low)]
    ses = [s for s in V.SPECIAL_EFFECTS if s.replace("-", " ") in low]
    mech = sorted({v for k, v in MECH_WORDS.items() if re.search(r"\b" + re.escape(k), low)})
    return abil, states, ses, mech


def block(e, titles):
    inc = e["incantation"]
    incs = f'"{inc["text"]}" x{inc["repetitions"]}' if inc["text"] else "none"
    if inc["special"] != "none":
        incs += f" ({inc['special']})"
    o = [f"### {e['slug']} — {e['title']}",
         f"- Type: {e['type'] or '-'} | School: {e['school'] or '-'} | Range: {e['range'] or '-'} | Delivery: {e['delivery']}",
         f"- Incantation: {incs} | Materials: {e['materials']['raw'] or 'none'}"]
    if e["availability"]:
        rows = []
        for a in e["availability"]:
            bits = [f"{a['cls']} {', '.join(ORD.get(x, str(x)) for x in a['levels'])}"]
            if a["frequency"]["raw"]:
                bits.append(a["frequency"]["raw"])
            if a["cost"]:
                bits.append(f"cost {a['cost']}" + (f", max {a['max']}" if a["max"] else ""))
            if a["magical"] is not None:
                bits.append("(m)" if a["magical"] else "(ex)")
            if a["range"]:
                bits.append(f"range {a['range']}")
            if a["look_the_part"]:
                bits.append("Look The Part: the class has it from 1st level")
            elif a["source"].startswith("ability header"):
                bits.append("listed only in the ability header (archetype, equipment row or granted)")
            if a["option"]:
                bits.append(a["option"])
            if a["tag"]:
                bits.append(a["tag"])
            rows.append(" · ".join(bits))
        o.append("- Classes: " + " ; ".join(rows))
    else:
        o.append("- Classes: none (archetype, meta or granted by another ability)" if e["kind"] == "ability" else "- Classes: see note")
    if e.get("note"):
        o.append(f"- Note: {e['note']}")
    o.append("- Rule sentences (cite every one):")
    for s in e["sentences"]:
        o.append(f"  - **{s['id']}**: {s['text']}")
    if not e["sentences"]:
        o.append("  - (none)")
    a, st, se, me = hints(e, titles)
    o.append(f"- Named in the text (hint, check it): abilities {a or '-'}; States {st or '-'}; Special Effects {se or '-'}; mechanics {me or '-'}")
    return "\n".join(o) + "\n"


def write(out_dir, name, slugs, ents, titles):
    os.makedirs(out_dir, exist_ok=True)
    body = [f"# Packet {name} ({len(slugs)} entries)", ""] + [block(ents[s], titles) for s in slugs]
    open(os.path.join(out_dir, name + ".md"), "w").write("\n".join(body))
    open(os.path.join(out_dir, name + ".slugs"), "w").write("\n".join(slugs) + "\n")


def main():
    ents = MS.load()
    titles = {e["title"] for e in ents.values()}
    out = sys.argv[1]
    if "--shards" in sys.argv:
        n = int(sys.argv[sys.argv.index("--shards") + 1])
        by = sys.argv[sys.argv.index("--by") + 1] if "--by" in sys.argv else "type"
        order = {"archetype": 0, "trait": 1, "meta-magic": 2, "enchantment": 3, "verbal": 4, "magic-ball": 5, "specialty-arrow": 6}
        if by == "type":
            slugs = sorted(ents, key=lambda s: (order.get(ents[s]["delivery"], 9), ents[s]["school"], s))
        else:
            slugs = sorted(ents)
        # balance by sentence count, keeping order
        total = sum(max(1, len(ents[s]["sentences"])) for s in slugs)
        per = total / n
        shards, cur, acc = [], [], 0
        for s in slugs:
            cur.append(s)
            acc += max(1, len(ents[s]["sentences"]))
            if acc >= per * (len(shards) + 1) and len(shards) < n - 1:
                shards.append(cur); cur = []
        if cur:
            shards.append(cur)
        for i, sh in enumerate(shards, 1):
            write(out, f"shard-{i:02d}", sh, ents, titles)
        print(f"{len(shards)} shards:", [len(x) for x in shards], [sum(len(ents[s]['sentences']) for s in x) for x in shards])
    else:
        name, slugs = sys.argv[2], sys.argv[3:]
        write(out, name, slugs, ents, titles)
        print(f"wrote {name}: {len(slugs)} entries")


if __name__ == "__main__":
    main()
