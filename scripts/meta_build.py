#!/usr/bin/env python3
"""Build the Ability Metadata Platform from the reviewed records.

Input : metadata/source/records/<slug>.json  (agent-written, reviewed)  +  scripts/meta_source.py (deterministic facets)
        metadata/glossary/glossary.json       (rules semantics)
Output: metadata/abilities.json               one merged entry per ability with derived facets
        metadata/profiles/<slug>.md           a complete human-readable profile per ability
        metadata/index/*.md                   every facet value -> the abilities that have it
        metadata/glossary/*.md                States, Special Effects, mechanics
        metadata/SIMILARITY.md, metadata/dedupe/<class>.md    duplicates, near-duplicates and containment
        metadata/STATS.md                     coverage and counts
Run: python3 scripts/meta_build.py
"""
import difflib, glob, json, os, re, shutil, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_source as MS
import meta_vocab as V
import rop_version as RV

ROOT = MS.ROOT
MD = os.path.join(ROOT, "metadata")
REC = os.path.join(MD, "source", "records")
GLOSS = json.load(open(os.path.join(MD, "glossary", "glossary.json")))
ORD = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}
OTHERS = {"target", "struck-player", "dead-target", "group", "hit-location", "target-equipment"}
SELFISH = {"caster", "bearer", "bearer-equipment", "caster-of-enchantment"}
SE_LABEL = {k: v["label"] for k, v in GLOSS["special_effects"].items() if not k.startswith("_")}
STATE_CONS = {k: v["consequences"] for k, v in GLOSS["states"].items()}


# ------------------------------------------------------------------------------------------------ labels
def effect_label(e):
    k, p = e["kind"], e.get("params") or {}
    if k == "state.apply":
        return V.STATE_VERB.get(p.get("state"), "Applies a State")
    if k == "state.remove" and p.get("what") == "specific-state" and p.get("state"):
        return f"Ends {p['state'].title()}"
    if k == "state.prevent" and p.get("states"):
        return "Prevents " + ", ".join(s.title() for s in p["states"])
    if k == "special-effect.grant" and p.get("effect"):
        return f"{SE_LABEL.get(p['effect'], p['effect'])} ({p.get('on', '').replace('-', ' ')})".replace(" ()", "")
    if k == "defense.immunity":
        return f"Immune to {p.get('school', '?')}" if p.get("school") != "choice" else "Immune to a chosen School"
    if k == "ability.grant" and p.get("ability"):
        return ("Works as " if p.get("how") == "as-per" else "Grants ") + p["ability"]
    if k == "ability.cast-via-strips" and p.get("ability"):
        return f"Casts {p['ability']} from strips"
    if k == "action.restrict" and p.get("what"):
        return "May not " + p["what"].replace("-", " ")
    if k == "ability.remove" and p.get("ability"):
        return f"Removes {p['ability']}"
    if k == "ability.modify" and (p.get("ability") or p.get("group")):
        return f"Changes {p.get('ability') or p.get('group')}"
    return V.EFFECTS[k]["label"]


def effect_detail(e):
    p = e.get("params") or {}
    bits = []
    for k, v in p.items():
        if k in ("state", "effect", "school", "ability") and effect_label(e) != V.EFFECTS[e["kind"]]["label"]:
            continue
        bits.append(f"{k.replace('_', ' ')} {', '.join(v) if isinstance(v, list) else v}")
    d = e["duration"]
    bits.append(f"{d['seconds']} s" if d["type"] == "timed" else d["type"].replace("-", " "))
    if e["timing"] != "on-cast":
        bits.append(V.TIMING[e["timing"]] + (f" ({e['delay_seconds']} s)" if e.get("delay_seconds") else ""))
    if e.get("conditions"):
        bits.append("only if " + "; ".join(V.CONDITIONS[c] for c in e["conditions"]))
    if e.get("choice"):
        bits.append(f"choice {e['choice']['group']} option {e['choice']['option']}")
    return "; ".join(bits)


# ------------------------------------------------------------------------------------------------ load + derive
def load():
    ents = MS.load()
    db = {}
    missing = []
    for slug, e in sorted(ents.items()):
        p = os.path.join(REC, slug + ".json")
        if not os.path.exists(p):
            missing.append(slug)
            continue
        r = json.load(open(p))
        x = dict(e)
        for k in ("summary", "effects", "requirements", "restrictions", "termination", "properties", "references", "clarifications",
                  "roles", "beneficiary", "open_questions"):
            x[k] = r[k]
        for ef in x["effects"]:
            ef.setdefault("params", {})
            ef.setdefault("conditions", [])
            ef["label"] = effect_label(ef)
        db[slug] = x
    return db, missing


def magical_any(x):
    if x["delivery"] in ("trait", "archetype"):
        return False
    if not x["availability"]:
        return x["delivery"] not in ("trait", "archetype")
    return any(a["magical"] for a in x["availability"])


def ranges_of(x):
    rs = {a["range"] for a in x["availability"] if a["range"]}
    if not rs and x["range"]:
        rs = set(re.findall(r"Self|Other|Touch|Unlimited|20'|50'", x["range"]))
    return sorted(rs)


GRANT_KINDS = ("ability.grant", "ability.cast-via-strips", "class.look-the-part")
DRAWBACK_RESTRICTIONS = {"no-other-protection-enchantments", "excludes-other-sources", "not-with-abilities", "stay-away-from-combat",
                         "may-not-impede-play", "caster-may-not-use-alternate-bases", "bearer-not-alternate-base", "not-exit-at-alternate-base"}
# facets that --include-granted (and the explorer's toggle) extend with what granted abilities can do
GRANTED_FACETS = ("Capability", "Effect", "Applies State", "Removes State", "Prevents State", "Property", "Special Effect", "Drawback")


def grants_of(x, by_title):
    """(ability, how) for every other entry this one grants, lets the user cast, works 'as per', or turns Look The Part into."""
    out = []
    for e in x["effects"]:
        a = e["params"].get("ability")
        if e["kind"] in GRANT_KINDS and a in by_title and by_title[a] is not x:
            how = e["params"].get("how") or ("casts-via-strips" if e["kind"] == "ability.cast-via-strips" else "gains")
            if how == "extra-use-of":          # one more use of an ability the class already has: nothing new
                continue
            out.append((by_title[a], how, e))
    return out


def moving_ok(x):
    """True when the entry itself may be cast or used while moving."""
    return (any(p["kind"] == "castable-while-moving" for p in x["properties"])
            or any("Ambulant" in (a.get("tag") or "") or "Ambulant" in (a["frequency"].get("raw") or "") for a in x["availability"])
            or any(e["kind"] == "meta.modify-next" and e["params"].get("mode") == "cast-while-moving" for e in x["effects"])
            or x["delivery"] == "specialty-arrow")


def own_caps(x, effs):
    caps = set()
    applies, removes, prevents = set(), set(), set()
    for e in effs:
        k, p, sub = e["kind"], e["params"], e["subject"]
        st = p.get("state")
        if k == "state.apply" and st:
            applies.add(st)
            c = STATE_CONS.get(st, {})
            if st == "insubstantial":
                caps.add("makes-insubstantial")
            if sub in OTHERS:
                if c.get("prevents_moving") in (True, "voluntarily"):
                    caps.add("holds-in-place")
                if st in ("frozen", "stunned", "insubstantial", "invulnerable"):
                    caps.add("neutralizes")
                if c.get("prevents_casting") is True:
                    caps.add("silences")
                if st in ("frozen", "insubstantial", "invulnerable"):
                    caps.add("removes-from-play")
                if st == "fragile":
                    caps.add("can-be-lethal")
                if st == "cursed":
                    caps.add("curses")
            else:
                if st in ("insubstantial", "invulnerable"):
                    caps.add("self-protection-state")
        if k == "state.remove":
            caps.add("cleanses")
            if st:
                removes.add(st)
            elif p.get("what") in ("one-state-or-effect", "all-states-and-effects", "chosen-states-and-effects", "same-source-states-and-effects"):
                removes.add("any")
        if k == "state.prevent":
            prevents.update(p.get("states") or [])
        if k == "state.transfer":
            caps.add("cleanses")
        if k == "death.cause":
            caps.update({"causes-death", "can-be-lethal"})
        if k == "special-effect.grant" and p.get("effect") in ("wounds-kill", "siege"):
            caps.add("can-be-lethal")
        if (k == "special-effect.grant" and p.get("effect") in ("armor-breaking", "armor-destroying")) or k == "armor.destroy" \
                or (k == "weapon.ignore-protections" and p.get("against") in ("magic-armor", "armor")):
            caps.add("defeats-armor")
        if k in ("equipment.destroy", "equipment.disable") or (k == "special-effect.grant" and p.get("effect") in (
                "weapon-destroying", "shield-destroying", "shield-crushing")):
            caps.add("attacks-equipment")
        if k == "wound.inflict":
            caps.add("wounds")
        if k == "wound.heal":
            caps.add("heals")
        if k == "life.revive":
            caps.add("revives")
        if k == "death.prevent":
            caps.add("survives-death")
        if k in ("equipment.repair", "armor.repair"):
            caps.add("repairs")
        if k == "enchantment.remove" and sub in OTHERS:
            caps.add("dispels")
        if k in ("defense.immunity", "defense.resistance", "defense.unaffected", "defense.negate-hit", "defense.negate-engulfing",
                 "defense.block-projectiles", "armor.magic", "armor.protect", "equipment.protect", "enchantment.protect", "state.prevent"):
            caps.add("protects")
        if k == "defense.resistance":
            caps.add("resists")
        if k.startswith("move.") and sub in OTHERS:
            caps.add("moves-others")
            if e["polarity"] == "benefit":
                caps.add("moves-ally")
        if k.startswith("move.") and sub in SELFISH:
            caps.add("moves-self")
        if k == "action.restrict" and sub in OTHERS:
            caps.add("restricts-others")
            if p.get("what") == "move-from-start":
                caps.add("holds-in-place")
        if k in ("ability.charge", "ability.restore-uses", "ability.charge-faster", "economy.frequency", "enchantment.extra-slot"):
            caps.add("more-uses")
        if k in ("ability.charge-faster", "economy.frequency"):
            caps.add("changes-frequency")
        if k == "enchantment.extra-slot":
            caps.add("extra-enchantments")
        if k in ("team.respawn-point", "team.alternate-base"):
            caps.add("team-base")
        if k in GRANT_KINDS:
            caps.add("grants-abilities")
    return caps, applies, removes, prevents


def derive(db):
    by_title = {x["title"]: x for x in db.values()}
    # 'as per' grants are part of the entry itself: expand them first (transitively) so their effects count as its own
    def expanded(x, seen=()):
        out = []
        for e in x["effects"]:
            a = e["params"].get("ability")
            if e["kind"] == "ability.grant" and e["params"].get("how") == "as-per" and a in by_title and a not in seen and by_title[a] is not x:
                out += [dict(y, via=a) for y in expanded(by_title[a], seen + (x["title"],))]
            out.append(e)
        return out
    for x in db.values():
        x["_effs"] = expanded(x)
    for x in db.values():
        effs = x["_effs"]
        caps, applies, removes, prevents = own_caps(x, effs)
        if any(p["kind"] in ("bypass-armor", "bypass-magic-armor") for p in x["properties"]):
            caps.add("defeats-armor")
        if any(p["kind"] == "exempt-from-enchantment-limit" for p in x["properties"]):
            caps.add("extra-enchantments")
        if moving_ok(x):
            caps.add("castable-while-moving")
        own_side = x["beneficiary"] in ("self", "ally", "team", "any")
        drawbacks = [e["id"] for e in x["effects"] if e["polarity"] == "harm" and own_side and (
            e["subject"] in SELFISH or (e["subject"] == "group" and x["beneficiary"] in ("self", "ally", "team")))]
        drawbacks += [e["id"] for e in x["effects"] if e["polarity"] == "harm" and e["subject"] in OTHERS and e["subject"] != "group"
                      and x["beneficiary"] == "ally"]
        limits = sorted({r["kind"] for r in x["restrictions"] if r["kind"] in DRAWBACK_RESTRICTIONS})
        # drawbacks inherited through an 'as per' grant (Song of Interference works as Enlightened Soul)
        inherited = sorted({f"{e['label']} (as per {e['via']})" for e in effs if e.get("via") and e["polarity"] == "harm"
                            and (e["subject"] in SELFISH or x["beneficiary"] == "ally")})
        if drawbacks or limits or inherited:
            caps.add("has-drawback")
        requires_states = {r["kind"].replace("target-", "") for r in x["requirements"] if r["kind"] in (
            "target-stopped", "target-frozen", "target-insubstantial", "target-dead", "target-wounded", "target-dead-at-start")}
        x["derived"] = dict(capabilities=sorted(caps), drawbacks=sorted(set(drawbacks)), drawback_limits=limits, drawbacks_as_per=inherited,
                            magical=magical_any(x), ranges=ranges_of(x),
                            states=dict(applies=sorted(applies), removes=sorted(removes), prevents=sorted(prevents), requires=sorted(requires_states)),
                            labels=sorted({e["label"] for e in effs}), classes=sorted({a["cls"] for a in x["availability"]}),
                            affects_others=any(e["subject"] in OTHERS for e in effs),
                            harms_others=any(e["subject"] in OTHERS and e["polarity"] == "harm" for e in effs))
    # everything reachable by granting, casting from strips or Look The Part, followed through every level
    for x in db.values():
        chain, todo, seen = [], [(y, how, [x["title"]]) for y, how, _ in grants_of(x, by_title)], {x["slug"]}
        while todo:
            y, how, path = todo.pop(0)
            if y["slug"] in seen:
                continue
            seen.add(y["slug"])
            chain.append(dict(slug=y["slug"], title=y["title"], how=how, path=path + [y["title"]]))
            todo += [(z, h, path + [y["title"]]) for z, h, _ in grants_of(y, by_title)]
        x["derived"]["grants"] = chain
        # a granted ability taken with Ambulant may be used while moving
        if any(e["kind"] == "ability.grant" and "Ambulant" in (e["params"].get("meta") or "") for e in x["effects"]):
            x["derived"]["grant_moving"] = True
    for x in db.values():
        via = set()
        for g in x["derived"]["grants"]:
            via.update(db[g["slug"]]["derived"]["capabilities"])
        if x["derived"].get("grant_moving"):
            via.add("castable-while-moving")
        x["derived"]["via_grant"] = sorted(via - set(x["derived"]["capabilities"]))
    counters(db)


def counters(db):
    """Who can stop or blunt what, derived from the records themselves (plus the Monk's Enlightened Soul rule)."""
    protectors = []
    for x in db.values():
        for e in x["effects"]:
            if e["subject"] not in ("bearer", "caster", "group", "friendly-players", "target"):
                continue
            if x["beneficiary"] == "enemy":
                continue
            k, p = e["kind"], e["params"]
            if k == "defense.immunity":
                schools = p.get("options") if p.get("school") == "choice" else [p.get("school")]
                protectors.append(("school", set(schools or []), x, "Immune" + (" (chosen School)" if p.get("school") == "choice" else "")))
            elif k == "defense.resistance":
                if p.get("to") == "chosen-school":
                    protectors.append(("school", set(p.get("options") or []), x, "Resistant (chosen School, next ability)"))
                elif p.get("to") == "next-source":
                    protectors.append(("any-harm", None, x, "Resistant to the next source"))
                elif p.get("to") == "wounds":
                    protectors.append(("wounds", None, x, "Resistant to the next wound"))
            elif k == "defense.unaffected":
                protectors.append(("unaffected:" + p.get("by", ""), set(p.get("schools") or []), x, "Unaffected by " + p.get("by", "").replace("-", " ")))
            elif k == "defense.block-projectiles":
                protectors.append(("projectiles", None, x, "Can block it by hand"))
            elif k == "state.prevent":
                protectors.append(("states", set(p.get("states") or []), x, "Cannot receive " + ", ".join(p.get("states") or [])))
            elif k == "enchantment.protect":
                protectors.append(("dispel", None, x, "Enchantments cannot be removed"))
    for x in db.values():
        out = []
        harmful = [e for e in x["effects"] if e["subject"] in OTHERS and e["polarity"] in ("harm", "depends")]
        if not harmful:
            x["derived"]["countered_by"] = []
            continue
        mag = x["derived"]["magical"]
        rng = x["derived"]["ranges"]
        beyond_touch = any(r in ("20'", "50'", "Unlimited") for r in rng)
        for kind, sset, y, why in protectors:
            if y is x:
                continue
            hit = False
            if kind == "school" and x["school"] in (sset or set()):
                hit = True
            elif kind == "any-harm":
                hit = True
            elif kind == "wounds" and any(e["kind"] == "wound.inflict" or (e["kind"] == "special-effect.grant" and e["params"].get("effect") == "wounds-kill") for e in harmful):
                hit = True
            elif kind == "unaffected:magical-abilities" and mag:
                hit = True
            elif kind == "unaffected:verbal-magical-beyond-touch" and x["delivery"] == "verbal" and mag and beyond_touch:
                hit = True
            elif kind == "unaffected:verbal-abilities" and x["delivery"] == "verbal":
                hit = True
            elif kind == "unaffected:projectiles-except-magic-balls" and x["delivery"] == "specialty-arrow":
                hit = True
            elif kind == "unaffected:schools" and x["school"] in (sset or set()) and mag:
                hit = True
            elif kind == "unaffected:hostile-actions-within-20ft":
                hit = True
            elif kind == "unaffected:combat-and-abilities":
                hit = True
            elif kind == "projectiles" and x["delivery"] in ("magic-ball", "specialty-arrow"):
                hit = True
            elif kind == "states" and set(x["derived"]["states"]["applies"]) & (sset or set()):
                hit = True
            elif kind == "dispel" and any(e["kind"] == "enchantment.remove" for e in harmful):
                hit = True
            if hit:
                out.append(dict(by=y["title"], slug=y["slug"], why=why, classes=y["derived"]["classes"]))
        x["derived"]["countered_by"] = sorted(out, key=lambda o: (o["why"], o["by"]))


# ------------------------------------------------------------------------------------------------ facets
def facets(x):
    d = x["derived"]
    f = defaultdict(set)
    f["Capability"].update(d["capabilities"])
    f["Can do through a granted ability"].update(d["via_grant"])
    for e in x["_effs"]:
        if e.get("via"):
            f["Effect"].add(e["label"])
            continue
        f["Effect"].add(e["label"])
        f["Effect family"].add(V.EFFECTS[e["kind"]]["family"])
        f["Who it affects"].add(e["subject"])
        f["Duration"].add(e["duration"]["type"] if e["duration"]["type"] != "timed" else f"{e['duration']['seconds']} seconds")
        f["When it happens"].add(e["timing"])
        for c in e.get("conditions") or []:
            f["Only if"].add(c)
        if e["kind"] == "special-effect.grant":
            f["Special Effect"].add(e["params"].get("effect"))
    for s in d["states"]["applies"]:
        f["Applies State"].add(s)
    for s in d["states"]["removes"]:
        f["Removes State"].add(s)
    for s in d["states"]["prevents"]:
        f["Prevents State"].add(s)
    for r in x["requirements"]:
        f["Requirement"].add(r["kind"])
    for r in x["restrictions"]:
        f["Restriction"].add(r["kind"])
    for r in x["termination"]:
        f["Ends when"].add(r["kind"])
        if r["kind"] == "either-dies":
            f["Ends when"].add("caster-dies")
    for r in x["properties"]:
        f["Property"].add(r["kind"])
    if "castable-while-moving" in d["capabilities"]:
        f["Property"].add("castable-while-moving")
    if any(p["kind"] in ("bypass-armor", "bypass-magic-armor") for p in x["properties"]):
        f["Special Effect"].add("ignores armor")
    for r in x["references"]:
        f["Names " + {"ability": "ability", "state": "State", "special-effect": "Special Effect", "mechanic": "mechanic"}[r["target"]]].add(r["name"])
    f["Role"].update(x["roles"])
    f["For"].add(x["beneficiary"])
    f["Delivery"].add(x["delivery"])
    if x["school"]:
        f["School"].add(x["school"])
    f["Range"].update(d["ranges"] or ["-"])
    f["Magical"].add("Magical (m)" if d["magical"] else "Extraordinary / not cast")
    for a in x["availability"]:
        f["Class"].add(a["cls"])
        for L in a["levels"]:
            f["Level"].add(ORD.get(L, str(L)))
        if a["frequency"]["per"]:
            f["Frequency"].add({"life": "per life", "refresh": "per refresh", "unlimited": "unlimited", "game": "per game"}[a["frequency"]["per"]])
        if a["frequency"]["charge"]:
            f["Frequency"].add("chargeable")
    if not x["availability"]:
        f["Class"].add("(archetype or granted)")
    for c in d["countered_by"]:
        f["Countered by"].add(c["by"])
    if d["drawbacks"]:
        f["Drawback"].update(e["label"] for e in x["effects"] if e["id"] in d["drawbacks"])
    f["Drawback"].update(V.RESTRICTIONS[r] for r in d["drawback_limits"])
    f["Drawback"].update(d["drawbacks_as_per"])
    for s in d["states"]["applies"]:
        if any(e["kind"] == "state.apply" and e["params"].get("state") == s and e["subject"] in SELFISH and e["polarity"] == "harm" for e in x["_effs"]):
            f["Applies State to own side"].add(s)
    if d["grants"]:
        f["Grants"].update(g["title"] for g in d["grants"])
    for e in x["_effs"]:
        if e["kind"] == "ability.cast-via-strips":
            f["Casts from strips"].add(e["params"]["ability"])
        if e["kind"] == "ability.modify" and e["params"].get("requirement"):
            f["Limit on use"].add(e["params"]["requirement"])
    f["Limit on use"].update(r["kind"] for r in x["requirements"])
    if x["open_questions"]:
        f["Has open question"].add("yes")
    return {k: sorted(v) for k, v in f.items() if v}


# ------------------------------------------------------------------------------------------------ similarity
def sig_effects(x, strict, effs=None):
    out = set()
    for e in effs if effs is not None else x["_effs"]:
        out.add(sig_one(e, strict))
    return out


def sig_one(e, strict):
    p = dict(e["params"])
    sub = "others" if e["subject"] in OTHERS else "self" if e["subject"] in SELFISH else e["subject"]
    key = [e["kind"], sub, e["polarity"]]
    for k in sorted(p):
        if not strict and k in ("feet", "points", "count", "frequency", "amount", "factor", "change", "note", "meta"):
            continue
        key.append(f"{k}={p[k]}")
    if strict:
        key.append("dur=" + (str(e["duration"].get("seconds")) if e["duration"]["type"] == "timed" else e["duration"]["type"]))
        key.append("cond=" + ",".join(sorted(e.get("conditions") or [])))
    else:
        key.append("dur=" + ("timed" if e["duration"]["type"] == "timed" else e["duration"]["type"]))
    return "|".join(key)


def comparable(x):
    return x["delivery"] != "archetype" and not x["title"].startswith("Equipment:")


def rel_sets(x):
    return ({r["kind"] for r in x["requirements"]}, {r["kind"] for r in x["restrictions"]},
            {r["kind"] for r in x["termination"]}, {p["kind"] for p in x["properties"]})


def is_cost(e, x):
    """An effect that is bad for the user's own side (a drawback or a cost), as opposed to something more the ability does."""
    if e["polarity"] == "neutral":
        return True
    if e["polarity"] != "harm":
        return False
    return e["subject"] in SELFISH or e["subject"] == "group" or (x["beneficiary"] == "ally" and e["subject"] in OTHERS)


RELOCATE = {"move.to-base", "move.to-location", "move.to-caster"}


def main_key(e):
    """What an effect is about, ignoring who it lands on and its numbers: used to find overlapping abilities."""
    p = e["params"]
    if e["kind"] in RELOCATE:
        return "move.relocate"
    if e["kind"] in ("equipment.repair", "armor.repair", "wound.heal") or (e["kind"] == "state.remove" and p.get("what") != "specific-state"):
        return e["kind"]
    for k in ("state", "ability", "school", "effect", "what", "against", "by", "to", "mode", "scope"):
        if p.get(k):
            v = p[k]
            return f"{e['kind']}|{','.join(v) if isinstance(v, list) else v}"
    return e["kind"]


def compare(a, b):
    """Relation of a to b, or None. 'subset' means a does less than b; 'plus-drawback' means a is b plus a cost to its own side."""
    if not comparable(a) or not comparable(b) or not a["_effs"] or not b["_effs"]:
        return None
    sa, sb = sig_effects(a, True), sig_effects(b, True)
    la, lb = sig_effects(a, False), sig_effects(b, False)
    ra, rb = rel_sets(a), rel_sets(b)
    if sa == sb:
        return "identical" if ra == rb else "same-effects"
    if la == lb:
        return "same-effects-different-numbers"
    # split each side into what it does for its user and what it costs them
    ben = lambda x: {sig_one(e, False) for e in x["_effs"] if not is_cost(e, x)}
    cost = lambda x: {sig_one(e, False) for e in x["_effs"] if is_cost(e, x)}
    ba, bb, ca, cb = ben(a), ben(b), cost(a), cost(b)
    if ba == bb and ba:
        if ca > cb:
            return "plus-drawback"
        if cb > ca:
            return "minus-drawback"
    for X, Y, fwd in ((a, b, True), (b, a, False)):
        bx, by = (ba, bb) if fwd else (bb, ba)
        as_per = any(e.get("via") == X["title"] for e in Y["_effs"])   # Troll Blood works as per Regeneration
        if bx and bx < by and not (rel_sets(Y)[0] - rel_sets(X)[0]) and (as_per or len(bx) / len(by) >= 1 / 4):
            return "subset" if fwd else "superset"
    ka, kb = {main_key(e) for e in a["_effs"]}, {main_key(e) for e in b["_effs"]}
    j = len(ka & kb) / len(ka | kb)
    if j >= 0.5:
        return ("overlap", round(j, 2))
    return None


def _loose_key(e):
    p = {k: v for k, v in e["params"].items() if k not in ("feet", "points", "count", "frequency", "amount", "factor", "change", "note")}
    sub = "others" if e["subject"] in OTHERS else "self" if e["subject"] in SELFISH else e["subject"]
    return (e["kind"], sub, e["polarity"], json.dumps(p, sort_keys=True))


def _num(e):
    p = e["params"]
    bits = [f"{k} {p[k]}" for k in ("feet", "points", "count", "amount") if k in p]
    d = e["duration"]
    bits.append(f"{d['seconds']} s" if d["type"] == "timed" else d["type"].replace("-", " "))
    if e.get("conditions"):
        bits.append("if " + ", ".join(e["conditions"]))
    return ", ".join(bits)


def differences(a, b):
    """Plain-language differences between two entries."""
    out = []
    ka, kb = defaultdict(list), defaultdict(list)
    for e in a["effects"]:
        ka[_loose_key(e)].append(e)
    for e in b["effects"]:
        kb[_loose_key(e)].append(e)
    for k in ka:
        if k in kb:
            x, y = ka[k][0], kb[k][0]
            if _num(x) != _num(y):
                out.append(f"{x['label']}: {_num(x)} vs {_num(y)}")
    for k in ka:
        if k not in kb:
            for e in ka[k]:
                out.append(f"only {a['title']}: {e['label']} ({e['subject']}, {_num(e)})")
    for k in kb:
        if k not in ka:
            for e in kb[k]:
                out.append(f"only {b['title']}: {e['label']} ({e['subject']}, {_num(e)})")
    names = ("requirement", "restriction", "ends when", "property")
    for n, x, y in zip(names, rel_sets(a), rel_sets(b)):
        if x - y:
            out.append(f"{n} only in {a['title']}: {', '.join(sorted(x - y))}")
        if y - x:
            out.append(f"{n} only in {b['title']}: {', '.join(sorted(y - x))}")
    for f in ("delivery", "school"):
        if a[f] != b[f]:
            out.append(f"{f}: {a[f] or '-'} vs {b[f] or '-'}")
    if a["derived"]["ranges"] != b["derived"]["ranges"]:
        out.append(f"range: {', '.join(a['derived']['ranges']) or '-'} vs {', '.join(b['derived']['ranges']) or '-'}")
    return out


def text_diff(a, b, limit=6):
    def toks(x):
        return re.findall(r"[A-Za-z0-9'/()-]+|[.,;:]", re.sub(r"\b" + re.escape(x["title"]) + r"\b", "THIS", " ".join(s["text"] for s in x["sentences"])))
    X, Y = toks(a), toks(b)
    sm = difflib.SequenceMatcher(None, X, Y, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            l, r = " ".join(X[i1:i2]), " ".join(Y[j1:j2])
            out.append((f"\u201c{l}\u201d" if l else "nothing") + " vs " + (f"\u201c{r}\u201d" if r else "nothing"))
    return out[:limit] + ([f"and {len(out) - limit} more"] if len(out) > limit else [])


def all_pairs(db):
    """(a, b, relation, score). Relations: identical, same-effects, same-effects-different-numbers, subset (a does less than b),
    plus-drawback (a is b plus a cost to its own side), overlap, provides (a gives its user b)."""
    xs = [x for x in db.values() if comparable(x)]
    pairs = []
    for i, a in enumerate(xs):
        for b in xs[i + 1:]:
            r = compare(a, b)
            if isinstance(r, tuple):
                pairs.append((a["slug"], b["slug"], r[0], r[1]))
            elif r == "superset":
                pairs.append((b["slug"], a["slug"], "subset", 1))
            elif r == "minus-drawback":
                pairs.append((b["slug"], a["slug"], "plus-drawback", 1))
            elif r:
                pairs.append((a["slug"], b["slug"], r, 1))
    for x in db.values():
        for g in x["derived"]["grants"]:
            if g["path"] == [x["title"], g["title"]] and g["how"] != "as-per":
                pairs.append((x["slug"], g["slug"], "provides", 1))
    return pairs


# ------------------------------------------------------------------------------------------------ writers
def fm(title):
    return ["---", f'title: "{title}"', "section: Ability Metadata", f"rulebook_version: {RV.NAME}", "generated_by: scripts/meta_build.py", "---", ""]


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def plink(x, base="../profiles/"):
    return f"[{x['title']}]({base}{x['slug']}.md)"


def cls_line(x):
    if not x["availability"]:
        return "archetype or granted" if x["kind"] == "ability" else "class trait"
    return ", ".join(f"{a['cls']} {','.join(ORD.get(l, str(l)) for l in a['levels'])}" for a in x["availability"])


def write_profile(x, db, pairs_by):
    o = fm(x["title"]) + [f"# {x['title']}", "", f"> {x['summary']}", ""]
    d = x["derived"]
    o += ["| | |", "| --- | --- |",
          f"| Type | {x['type'] or '-'} ({x['delivery']}) |", f"| School | {x['school'] or '-'} |", f"| Range | {esc(x['range']) or '-'} |",
          f"| Incantation | {esc(x['incantation']['raw']) or 'none'} |", f"| Materials | {esc(x['materials']['raw']) or 'none'} |",
          f"| Magical | {'yes, (m) for at least one class' if d['magical'] else 'no'} |",
          f"| Roles | {', '.join(x['roles'])} \u00b7 for: {x['beneficiary']} |",
          f"| Capabilities | {', '.join(d['capabilities']) or '-'}{' \u00b7 through granted abilities: ' + ', '.join(d['via_grant']) if d['via_grant'] else ''} |",
          *([f"| Gives its user | {', '.join(plink(db[g['slug']], '') + (' (' + ' \u2192 '.join(g['path'][1:-1]) + ')' if len(g['path']) > 2 else '') + ('' if g['how'] == 'gains' else ' [' + g['how'] + ']') for g in d['grants'])} |"] if d["grants"] else []),
          *([f"| Drawbacks from limits | {', '.join(V.RESTRICTIONS[r] for r in d['drawback_limits'])} |"] if d["drawback_limits"] else []),
          f"| Rule text | [{x['source_file']}](../../{x['source_file'].split('#')[0]}) \u00b7 [interoperability](../../interoperability/abilities/{x['slug']}.md) |" if x["kind"] == "ability" else f"| Rule text | {x['source_file']} |",
          ""]
    if x["availability"]:
        o += ["## Who has it", "", "| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |",
              "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for a in x["availability"]:
            fq = a["frequency"]
            notes = "; ".join(filter(None, [a["option"], a["tag"], "Look The Part" if a["look_the_part"] else ""]))
            o.append(f"| {a['cls']} | {', '.join(ORD.get(l, str(l)) for l in a['levels'])} | {a['cost'] or '-'} | {a['max'] or '-'} | {esc(fq['raw']) or '-'} | "
                     f"{(str(fq['uses']) + (' ' + fq['unit'] if fq['unit'] else '')) if fq['uses'] else '-'} | {fq['per'] or '-'} | {('x' + str(fq['charge'])) if fq['charge'] else '-'} | "
                     f"{'(m)' if a['magical'] else '(ex)' if a['magical'] is False else '-'} | {a['range'] or '-'} | {esc(notes) or '-'} |")
        o.append("")
    o += ["## What it does", "", "| # | Effect | On | For them | Details | From |", "| --- | --- | --- | --- | --- | --- |"]
    for e in x["effects"]:
        o.append(f"| {e['id']} | **{e['label']}** | {e['subject']} | {e['polarity']} | {esc(effect_detail(e))}{' \u2014 ' + esc(e['note']) if e.get('note') else ''} | {', '.join(e['evidence'])} |")
    o.append("")
    if d["drawbacks"]:
        o += ["**Drawbacks:** " + "; ".join(f"{e['label']} ({e['subject']})" for e in x["effects"] if e["id"] in d["drawbacks"]), ""]
    for key, title, vocab in (("requirements", "Requirements", V.REQUIREMENTS), ("restrictions", "Restrictions", V.RESTRICTIONS),
                              ("termination", "How it ends early", V.TERMINATION), ("properties", "Properties", V.PROPERTIES)):
        if x[key]:
            o += [f"## {title}", ""]
            for it in x[key]:
                o.append(f"- **{it['kind']}**: {vocab[it['kind']]}{' (' + str(it['n']) + ')' if it.get('n') is not None else ''}"
                         f"{' \u2014 ' + it['note'] if it.get('note') else ''} *({', '.join(it['evidence'])})*")
            o.append("")
    if x["clarifications"]:
        o += ["## Clarifications in the text", ""] + [f"- {c['text']} *({', '.join(c['evidence'])})*" for c in x["clarifications"]] + [""]
    if x["references"]:
        o += ["## Names in the text", ""]
        for r in x["references"]:
            name = r["name"]
            if r["target"] == "ability":
                y = next((z for z in db.values() if z["title"] == name), None)
                name = plink(y, "") if y else name
            o.append(f"- {r['target']} **{name}**: {r['relation']} *({', '.join(r['evidence'])})*")
        o.append("")
    if d["countered_by"]:
        o += ["## What can stop or blunt it", "", "Derived from the other records: abilities and traits that make their bearer immune, resistant or "
              "unaffected in a way that covers this ability.", "", "| Protection | How | Who has it |", "| --- | --- | --- |"]
        for c in d["countered_by"]:
            y = db[c["slug"]]
            o.append(f"| {plink(y, '')} | {c['why']} | {', '.join(c['classes']) or cls_line(y)} |")
        o.append("")
    rel = pairs_by.get(x["slug"], [])
    if rel:
        o += ["## Similar abilities", "", "| Relation | Ability | Differences |", "| --- | --- | --- |"]
        for other, r in rel:
            y = db[other]
            o.append(f"| {r} | {plink(y, '')} | {esc('; '.join(differences(x, y)[:8]))} |")
        o.append("")
    if x["open_questions"]:
        o += ["## Open questions", ""] + [f"- {q}" for q in x["open_questions"]] + [""]
    o += ["## Rule text, sentence by sentence", "", "Every sentence and the items that cite it.", "", "| Id | Sentence | Captured as |", "| --- | --- | --- |"]
    cov = defaultdict(list)
    for e in x["effects"]:
        for s in e["evidence"]:
            cov[s].append(f"effect {e['id']} ({e['label']})")
    for key in ("requirements", "restrictions", "termination", "properties"):
        for it in x[key]:
            for s in it["evidence"]:
                cov[s].append(f"{ {'requirements': 'requirement', 'restrictions': 'restriction', 'termination': 'ends when', 'properties': 'property'}[key]} {it['kind']}")
    for r in x["references"]:
        for s in r["evidence"]:
            cov[s].append(f"names {r['name']}")
    for c in x["clarifications"]:
        for s in c["evidence"]:
            cov[s].append("clarification")
    for s in x["sentences"]:
        o.append(f"| {s['id']} | {esc(s['text'])} | {esc('; '.join(cov.get(s['id'], ['(not cited)'])))} |")
    o += ["", "---", f"*Generated by `scripts/meta_build.py` from `metadata/source/records/{x['slug']}.json` and the {RV.NAME} rules.*", ""]
    open(os.path.join(MD, "profiles", x["slug"] + ".md"), "w").write("\n".join(o))


def write_indexes(db):
    by = defaultdict(lambda: defaultdict(list))
    for x in db.values():
        for fac, vals in x["facets"].items():
            for v in vals:
                by[fac][v].append(x)
    groups = [("capabilities", ["Capability", "Can do through a granted ability"]), ("effects", ["Effect", "Effect family", "Special Effect", "Drawback"]),
              ("states", ["Applies State", "Removes State", "Prevents State"]), ("targets-and-timing", ["Who it affects", "Duration", "When it happens", "Only if"]),
              ("requirements-and-limits", ["Requirement", "Restriction", "Ends when"]), ("properties", ["Property", "Magical"]),
              ("delivery", ["Delivery", "School", "Range", "Role", "For"]), ("classes", ["Class", "Level", "Frequency"]),
              ("names", ["Names ability", "Names State", "Names Special Effect", "Names mechanic"]), ("counters", ["Countered by"])]
    os.makedirs(os.path.join(MD, "index"), exist_ok=True)
    for name, facs in groups:
        o = fm(f"Index: {name}") + [f"# Index: {name.replace('-', ' ')}", ""]
        for fac in facs:
            if fac not in by:
                continue
            o += [f"## {fac}", ""]
            for v in sorted(by[fac], key=lambda s: (-len(by[fac][s]), s)):
                xs = sorted(by[fac][v], key=lambda z: z["title"])
                o.append(f"- **{v}** ({len(xs)}): " + ", ".join(plink(z) for z in xs))
            o.append("")
        open(os.path.join(MD, "index", name + ".md"), "w").write("\n".join(o))


def write_similarity(db, pairs):
    order = ["identical", "same-effects", "same-effects-different-numbers", "plus-drawback", "subset", "provides", "overlap"]
    label = {"identical": "Identical", "same-effects": "Same effects, different requirements or limits",
             "same-effects-different-numbers": "Same effects, different numbers", "plus-drawback": "Same effects plus a drawback or cost (first has it)",
             "subset": "Does less than (first does less)", "provides": "Gives its user the other (grants it, casts it from strips, or Look The Part)",
             "overlap": "Overlapping"}
    o = fm("Similar abilities") + ["# Similar abilities", "",
         "Pairs compared on their effect records (kind, who, polarity, parameters, duration, conditions), then on requirements, restrictions, "
         "ending conditions and properties. Delivery, School and range are listed as differences because they decide who the ability can hit. "
         "Each pair also shows the word-level difference in the rule text. An ability that works 'as per' another is compared with that "
         "ability's effects included. \"Does less than\" needs the bigger ability to add no requirement (Resurrect needs a dead target, so it "
         "does not simply do more than Heal); extra effects that only cost the user are a drawback, not \"more\". Archetypes and Equipment "
         "traits are compared only through what they give their user.", ""]
    for r in order:
        ps = [p for p in pairs if p[2] == r]
        if r == "overlap":
            o += [f"## {label[r]} ({len(ps)} pairs)", "", "Listed in each profile and class report rather than here.", ""]
            continue
        o += [f"## {label[r]} ({len(ps)} pairs)", "", "| First | Second | Differences | Wording |", "| --- | --- | --- | --- |"]
        for a, b, _, _ in sorted(ps, key=lambda p: (db[p[0]]["title"], db[p[1]]["title"])):
            A, B = db[a], db[b]
            o.append(f"| {plink(A, 'profiles/')} ({cls_line(A)}) | {plink(B, 'profiles/')} ({cls_line(B)}) | {esc('; '.join(differences(A, B)) or '-')} | {esc('; '.join(text_diff(A, B, 4)) or 'same')} |")
        o.append("")
    open(os.path.join(MD, "SIMILARITY.md"), "w").write("\n".join(o))
    os.makedirs(os.path.join(MD, "dedupe"), exist_ok=True)
    pairs_by = defaultdict(list)
    fwd = {"subset": "does less than", "plus-drawback": "same plus a drawback or cost", "provides": "gives its user"}
    back = {"subset": "does more than", "plus-drawback": "same without the drawback or cost", "provides": "is given by"}
    for a, b, r, sc in sorted(pairs, key=lambda p: -p[3]):
        pairs_by[a].append((b, fwd.get(r, r)))
        pairs_by[b].append((a, back.get(r, r)))
    classes = sorted({a["cls"] for x in db.values() for a in x["availability"]})
    for c in classes:
        mine = sorted([x for x in db.values() if any(a["cls"] == c for a in x["availability"]) and comparable(x)], key=lambda z: z["title"])
        o = fm(f"{c}: duplicate check") + [f"# {c}: duplicate check", "",
             f"Every comparable entry on the {c} list against every other ability, spell and trait in the rulebook.", ""]
        for x in mine:
            rel = [(o_, r) for o_, r in pairs_by.get(x["slug"], []) if r != "overlap"]
            ov = [(o_, r) for o_, r in pairs_by.get(x["slug"], []) if r == "overlap"]
            if not rel and not ov:
                continue
            o += [f"## {plink(x)}", "", x["summary"], "", "| Relation | Ability | On | Differences | Wording |", "| --- | --- | --- | --- | --- |"]
            for other, r in rel + ov[:6]:
                y = db[other]
                o.append(f"| {r} | {plink(y)} | {cls_line(y)} | {esc('; '.join(differences(x, y)) or '-')} | {esc('; '.join(text_diff(x, y, 3)) or 'same')} |")
            if len(ov) > 6:
                o.append(f"| overlapping | *and {len(ov) - 6} more* | | see the profile | |")
            o.append("")
        open(os.path.join(MD, "dedupe", c.lower().replace(" ", "-") + ".md"), "w").write("\n".join(o))
    return pairs_by


def write_glossary_pages():
    g = GLOSS
    o = fm("States, Special Effects and mechanics") + ["# States, Special Effects and mechanics", "",
         "The rules semantics the platform uses to derive answers. Source: `rules/magic-states-effects/`.", "", "## States", "",
         "| State | Summary | Moves? | Speaks? | Casts? | Attacks? | Unaffected by most? |", "| --- | --- | --- | --- | --- | --- | --- |"]
    yn = lambda v: "no" if v is True else "yes" if v is False else str(v)
    for k, s in g["states"].items():
        c = s["consequences"]
        o.append(f"| {s['label']} | {s['summary']} | {yn(c.get('prevents_moving'))} | {yn(c.get('prevents_speaking'))} | {yn(c.get('prevents_casting'))} | "
                 f"{yn(c.get('prevents_attacking'))} | {'yes' if c.get('unaffected_by_most') else 'no'} |")
    o += ["", "General rules: " + " ".join(g["state_general"]["rules"]), "", "## Derived capabilities", ""]
    for k, (label, rule) in V.CAPABILITIES.items():
        o.append(f"- **{k}** \u2014 {label}: {rule}")
    o += ["", "## Special Effects", ""] + [f"- **{v['label']}**: {v['summary']}" for k, v in g["special_effects"].items() if not k.startswith("_")]
    o += ["", "## Mechanics", ""] + [f"- **{k}**: {v}" for k, v in g["mechanics"].items() if not k.startswith("_")]
    open(os.path.join(MD, "glossary", "README.md"), "w").write("\n".join(o) + "\n")


def write_stats(db, missing, pairs):
    n_sent = sum(len(x["sentences"]) for x in db.values())
    fam = Counter(V.EFFECTS[e["kind"]]["family"] for x in db.values() for e in x["effects"])
    o = fm("Platform statistics") + ["# Platform statistics", "", f"- Entries with records: {len(db)} (missing: {', '.join(missing) or 'none'})",
         f"- Rule sentences: {n_sent}, all cited (enforced by `scripts/meta_check.py`)",
         f"- Effects: {sum(len(x['effects']) for x in db.values())}; requirements {sum(len(x['requirements']) for x in db.values())}; "
         f"restrictions {sum(len(x['restrictions']) for x in db.values())}; ending conditions {sum(len(x['termination']) for x in db.values())}; "
         f"properties {sum(len(x['properties']) for x in db.values())}; references {sum(len(x['references']) for x in db.values())}; "
         f"clarifications {sum(len(x['clarifications']) for x in db.values())}; open questions {sum(len(x['open_questions']) for x in db.values())}",
         f"- Similar pairs: " + ", ".join(f"{k} {v}" for k, v in Counter(p[2] for p in pairs).items()), "", "## Effects by family", ""]
    o += [f"- {k}: {v}" for k, v in fam.most_common()]
    open(os.path.join(MD, "STATS.md"), "w").write("\n".join(o) + "\n")


def main():
    db, missing = load()
    derive(db)
    for x in db.values():
        x["facets"] = facets(x)
    for x in db.values():
        g = defaultdict(set)
        for gr in x["derived"]["grants"]:
            for fac in GRANTED_FACETS:
                g[fac].update(db[gr["slug"]]["facets"].get(fac, []))
        if x["derived"].get("grant_moving"):
            g["Property"].add("castable-while-moving")
            g["Capability"].add("castable-while-moving")
        x["granted_facets"] = {k: sorted(v - set(x["facets"].get(k, []))) for k, v in g.items() if v - set(x["facets"].get(k, []))}
    for d in ("profiles", "index", "dedupe"):
        p = os.path.join(MD, d)
        if os.path.isdir(p):
            shutil.rmtree(p)
        os.makedirs(p)
    pairs = all_pairs(db)
    for x in db.values():
        x.pop("_effs", None)
    pairs_by = write_similarity(db, pairs)
    for x in db.values():
        write_profile(x, db, pairs_by)
    write_indexes(db)
    write_glossary_pages()
    write_stats(db, missing, pairs)
    json.dump(dict(edition=RV.NAME, date=RV.DATE, vocabulary=dict(effects=V.EFFECTS, subjects=V.SUBJECTS, requirements=V.REQUIREMENTS,
                   restrictions=V.RESTRICTIONS, termination=V.TERMINATION, properties=V.PROPERTIES, roles=V.ROLES), glossary=GLOSS,
                   abilities=db, pairs=[dict(a=a, b=b, relation=r, score=sc) for a, b, r, sc in pairs]),
              open(os.path.join(MD, "abilities.json"), "w"), indent=1, ensure_ascii=False)
    print(f"built {len(db)} entries (missing {len(missing)}), {len(pairs)} similar pairs: {dict(Counter(p[2] for p in pairs))}")


if __name__ == "__main__":
    main()
