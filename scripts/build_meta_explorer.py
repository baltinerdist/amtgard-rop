#!/usr/bin/env python3
"""Build viewer/ability-explorer.html from metadata/abilities.json (run scripts/meta_build.py first).
The page is viewer/ability-explorer-template.html with the data inlined."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_vocab as V

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "metadata", "abilities.json")
TPL = os.path.join(ROOT, "viewer", "ability-explorer-template.html")
OUT = os.path.join(ROOT, "viewer", "ability-explorer.html")

CAP_LABEL = {k: v[0] for k, v in V.CAPABILITIES.items()}


def main():
    D = json.load(open(SRC))
    ab = D["abilities"]
    slim = []
    for x in sorted(ab.values(), key=lambda z: z["title"].lower()):
        slim.append({k: x[k] for k in ("slug", "title", "kind", "type", "school", "range", "delivery", "incantation", "materials", "availability",
                                        "sentences", "summary", "effects", "requirements", "restrictions", "termination", "properties",
                                        "references", "clarifications", "roles", "beneficiary", "open_questions", "derived", "facets", "granted_facets", "source_file")})
    vocab = dict(requirements=V.REQUIREMENTS, restrictions=V.RESTRICTIONS, termination=V.TERMINATION, properties=V.PROPERTIES,
                 conditions=V.CONDITIONS, timing=V.TIMING, duration=V.DURATION, subjects=V.SUBJECTS, roles=V.ROLES, beneficiary=V.BENEFICIARY,
                 effects={k: dict(label=v["label"], family=v["family"], definition=v["definition"], synonyms=v["synonyms"]) for k, v in V.EFFECTS.items()},
                 caps=CAP_LABEL, cap_rules={k: v[1] for k, v in V.CAPABILITIES.items()}, state_verb=V.STATE_VERB)
    data = dict(edition=D["edition"], abilities=slim, pairs=D["pairs"], vocab=vocab, glossary=D["glossary"])
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=True).replace("</", "<\\/")
    tpl = open(TPL, encoding="utf-8").read()
    assert tpl.count("__DATA__") == 1
    html = tpl.replace("__DATA__", blob).replace("__EDITION__", D["edition"])
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"wrote {OUT}: {len(slim)} entries, {len(D['pairs'])} pairs, {len(html) // 1024} KB")


if __name__ == "__main__":
    main()
