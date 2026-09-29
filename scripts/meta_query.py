#!/usr/bin/env python3
"""Ask questions of the Ability Metadata Platform (metadata/abilities.json).

  meta_query.py "causes death"                    free text: matches effect labels, synonyms, capabilities, summaries and rule text
  meta_query.py --cap holds-in-place              a derived capability (see --list Capability)
  meta_query.py --effect Freezes --effect Stops   effect labels (any of them)
  meta_query.py --facet Requirement=target-willing --facet Class=Druid     (AND across flags)
  meta_query.py --facet "Applies State=frozen|stopped"                    ("|" means any of these values, "*" any value at all)
  meta_query.py --cap heals --include-granted     count what granted abilities can do too (every filter)
  meta_query.py "causes death" --or "curses"      union of two free-text questions
  meta_query.py --state frozen                    applies, removes, prevents or requires that State
  meta_query.py --class Druid --role defense
  meta_query.py --list Effect                     every value of a facet with counts
  meta_query.py --explain icy-blast               print the profile
  meta_query.py --similar hold-person             similar abilities with differences
  meta_query.py --dedupe Druid                    the Druid duplicate report
  meta_query.py --countered-by icy-blast          what can stop it
Add --json for machine-readable output, --not-facet Name=value to exclude.
"""
import argparse, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_vocab as V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "metadata")


def load():
    p = os.path.join(MD, "abilities.json")
    if not os.path.exists(p):
        sys.exit("metadata/abilities.json is missing: run python3 scripts/meta_build.py")
    return json.load(open(p))


def resolve(db, key):
    k = key.lower()
    if k in db:
        return db[k]
    hits = [x for x in db.values() if x["title"].lower() == k] or [x for x in db.values() if k in x["title"].lower()]
    if len(hits) == 1:
        return hits[0]
    sys.exit(f"no unique entry matches {key!r}: {[x['title'] for x in hits][:10] or 'none'}")


SYN = {}
for kind, spec in V.EFFECTS.items():
    for w in spec["synonyms"] + [spec["label"].lower()]:
        SYN.setdefault(w.lower(), set()).add(kind)
for st, verb in V.STATE_VERB.items():
    for w in (st, verb.lower(), st.rstrip("ed"), "freeze" if st == "frozen" else st):
        SYN.setdefault(w, set()).add("state:" + st)


def norm(t):
    return re.sub(r"[^a-z0-9']+", " ", t.lower()).strip()


PHRASE_FACETS = ("Capability", "Effect", "Applies State", "Removes State", "Prevents State", "Special Effect", "Property", "Requirement",
                 "Restriction", "Ends when", "Drawback", "Role")


def phrases(F):
    """Every facet value of an entry, and the plain labels of its capabilities and vocabulary terms, normalised for phrase matching."""
    out = set()
    for fac in PHRASE_FACETS:
        for v in F.get(fac, []):
            out.add(norm(v))
            if fac == "Capability" and v in V.CAPABILITIES:
                out.add(norm(V.CAPABILITIES[v][0]))
            for vocab in (V.PROPERTIES, V.REQUIREMENTS, V.RESTRICTIONS, V.TERMINATION):
                if v in vocab:
                    out.add(norm(vocab[v]))
    return out


def text_match(x, F, q, all_phrases):
    """Free text, most specific first: (1) the whole question is a label or facet value (\"causes death\", \"holds a player in place\");
    (2) short questions (up to 3 words) match effect synonyms (\"kill\", \"freeze\", \"banish\"); (3) every word appears, as a whole word,
    in the title, summary, rule text or labels."""
    ql = norm(q)
    if ql in all_phrases:
        return ql in phrases(F)
    if len(ql.split()) <= 3:
        kinds = {k for w, ks in SYN.items() if re.search(r"\b" + re.escape(w) + r"\b", ql) for k in ks}
        if kinds:
            return bool(kinds & F.get("Effect kind", set())) or \
                any(k.split(":")[1] in F.get("Applies State", ()) for k in kinds if k.startswith("state:"))
    hay = " " + norm(" ".join([x["title"], x["summary"], " ".join(s["text"] for s in x["sentences"]), " ".join(F.get("Effect", [])),
                              " ".join(V.CAPABILITIES[c][0] for c in F.get("Capability", []) if c in V.CAPABILITIES)])) + " "
    return all(f" {w} " in hay for w in ql.split())


KINDS = {}


def view(x, granted):
    """The entry's facets, extended with what its granted abilities can do when asked."""
    F = {k: set(v) for k, v in x["facets"].items()}
    F["Effect kind"] = {e["kind"] for e in x["effects"]}
    if granted:
        for k, v in x.get("granted_facets", {}).items():
            F.setdefault(k, set()).update(v)
        for g in x["derived"]["grants"]:
            F["Effect kind"] |= KINDS.get(g["slug"], set())
    return F


def show(xs, as_json):
    if as_json:
        print(json.dumps([dict(slug=x["slug"], title=x["title"], type=x["type"], school=x["school"], summary=x["summary"],
                               classes=[f"{a['cls']} {a['levels']}" for a in x["availability"]]) for x in xs], indent=1))
        return
    for x in sorted(xs, key=lambda z: z["title"]):
        cl = ", ".join(f"{a['cls']} {','.join(str(l) for l in a['levels'])}" for a in x["availability"]) or ("archetype/granted" if x["kind"] == "ability" else "class trait")
        print(f"{x['title']:<26} {x['type']:<16} {x['school'] or '-':<11} {cl}\n    {x['summary']}")
    print(f"-- {len(xs)} entries")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("text", nargs="*")
    ap.add_argument("--cap", action="append", default=[])
    ap.add_argument("--effect", action="append", default=[])
    ap.add_argument("--facet", action="append", default=[])
    ap.add_argument("--not-facet", action="append", default=[])
    ap.add_argument("--state")
    ap.add_argument("--class", dest="cls")
    ap.add_argument("--role")
    ap.add_argument("--include-granted", action="store_true", help="also count what granted abilities can do (every filter)")
    ap.add_argument("--or", dest="or_", action="append", default=[], help="also include entries matching this free text")
    ap.add_argument("--list"), ap.add_argument("--explain"), ap.add_argument("--similar"), ap.add_argument("--dedupe"), ap.add_argument("--countered-by")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    D = load()
    db = D["abilities"]
    if a.list:
        from collections import Counter
        c = Counter(v for x in db.values() for v in x["facets"].get(a.list, []))
        if not c:
            sys.exit(f"no facet {a.list!r}; facets: {sorted({f for x in db.values() for f in x['facets']})}")
        for v, n in c.most_common():
            print(f"{n:4}  {v}")
        return
    if a.explain:
        x = resolve(db, a.explain)
        print(open(os.path.join(MD, "profiles", x["slug"] + ".md")).read())
        return
    if a.similar or a.countered_by:
        x = resolve(db, a.similar or a.countered_by)
        if a.countered_by:
            for c in x["derived"]["countered_by"]:
                print(f"{c['by']:<28} {c['why']:<45} {', '.join(c['classes'])}")
            print(f"-- {len(x['derived']['countered_by'])} protections")
            return
        fwd = {"subset": "does less than", "plus-drawback": "same plus a drawback or cost", "provides": "gives its user"}
        back = {"subset": "does more than", "plus-drawback": "same without the drawback or cost", "provides": "is given by"}
        rows = [(p["b"], fwd.get(p["relation"], p["relation"])) for p in D["pairs"] if p["a"] == x["slug"]] + \
               [(p["a"], back.get(p["relation"], p["relation"])) for p in D["pairs"] if p["b"] == x["slug"]]
        for o, r in sorted(rows, key=lambda t: t[1]):
            print(f"{r:<32} {db[o]['title']}")
        print(f"-- {len(rows)} related")
        return
    if a.dedupe:
        p = os.path.join(MD, "dedupe", a.dedupe.lower().replace(" ", "-") + ".md")
        if not os.path.exists(p):
            sys.exit(f"no report for {a.dedupe!r}")
        print(open(p).read())
        return
    all_phrases = set()
    for x in db.values():
        all_phrases |= phrases(view(x, True))
    out = []
    anyof = lambda want, have: (want == "*" and bool(have)) or any(w in have for w in want.split("|"))
    KINDS.update({x["slug"]: {e["kind"] for e in x["effects"]} for x in db.values()})
    for x in db.values():
        F = view(x, a.include_granted)
        ok = all(anyof(c, F.get("Capability", ())) for c in a.cap)
        ok = ok and (not a.effect or any(e.lower() == l.lower() for e in a.effect for l in F.get("Effect", ())))
        for fv in a.facet:
            k, _, v = fv.partition("=")
            ok = ok and anyof(v, F.get(k, ()))
        for fv in a.not_facet:
            k, _, v = fv.partition("=")
            ok = ok and not anyof(v, F.get(k, ()))
        if a.state:
            st = set().union(*(F.get(k, ()) for k in ("Applies State", "Removes State", "Prevents State"))) | set(x["derived"]["states"]["requires"])
            ok = ok and anyof(a.state, st)
        ok = ok and (not a.cls or anyof(a.cls, F.get("Class", ())))
        ok = ok and (not a.role or anyof(a.role, x["roles"]))
        ok = ok and (not a.text or text_match(x, F, " ".join(a.text), all_phrases))
        if ok:
            out.append(x)
    if a.or_:
        seen = {x["slug"] for x in out}
        for q in a.or_:
            out += [x for x in db.values() if x["slug"] not in seen and text_match(x, view(x, a.include_granted), q, all_phrases)]
            seen = {x["slug"] for x in out}
    show(out, a.json)


if __name__ == "__main__":
    main()
