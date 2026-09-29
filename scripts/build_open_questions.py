#!/usr/bin/env python3
"""Build viewer/open-questions.html, the shareable rulings docket.

Joins the open questions in metadata/abilities.json with the proposed readings in
sim/data/rulings.json (id = "<slug>#<n>", n = 1-based index into that record's
open_questions). The page is viewer/open-questions-template.html with the data inlined."""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "metadata", "abilities.json")
RULINGS = os.path.join(ROOT, "sim", "data", "rulings.json")
TPL = os.path.join(ROOT, "viewer", "open-questions-template.html")
OUT = os.path.join(ROOT, "viewer", "open-questions.html")

IMPACTS = {"high", "medium", "low"}
HINTS = {None, "settled", "no-effect", "errata"}
CONFIDENCE = {"high", "medium", "low"}


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def where(rec):
    parts = []
    for a in rec.get("availability", []):
        lv = ", ".join(ordinal(x) for x in a.get("levels", []))
        freq = (a.get("frequency") or {}).get("raw", "")
        parts.append(f"{a['cls']} {lv}".strip() + (f" ({freq})" if freq else ""))
    return " · ".join(parts) or rec.get("kind", "").replace("-", " ").capitalize()


def main():
    D = json.load(open(SRC))
    ab = D["abilities"]
    ab = ab if isinstance(ab, dict) else {r["slug"]: r for r in ab}
    rulings = {r["id"]: r for r in json.load(open(RULINGS))}

    out, missing = [], []
    for rec in sorted(ab.values(), key=lambda r: r["title"].lower()):
        for n, note in enumerate(rec["open_questions"], 1):
            qid = f"{rec['slug']}#{n}"
            r = rulings.get(qid)
            if not r:
                missing.append(qid)
                continue
            assert r["sim_impact"] in IMPACTS and r["confidence"] in CONFIDENCE and r.get("hint") in HINTS, qid
            out.append(dict(
                id=qid, no=len(out) + 1, title=rec["title"], where=where(rec),
                classes=sorted({a["cls"] for a in rec.get("availability", [])}),
                sentences=[[s["id"], s["field"], s["text"]] for s in rec["sentences"]],
                question=r["question"], options=r.get("options") or [], proposed=r["ruling"],
                why=r.get("why", ""), confidence=r["confidence"], sim_impact=r["sim_impact"], topic=r["topic"],
                hint=r.get("hint"), related=r.get("related", []),
            ))
    if missing:
        sys.exit(f"no ruling for {len(missing)} open questions: {', '.join(missing[:8])}")
    known = {q["id"] for q in out}
    for q in out:
        assert set(q["related"]) <= known, q["id"]
    extra = set(rulings) - {q["id"] for q in out}
    if extra:
        sys.exit(f"rulings.json has ids with no open question: {', '.join(sorted(extra)[:8])}")

    data = dict(edition=D["edition"], questions=out)
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=True).replace("</", "<\\/")
    tpl = open(TPL, encoding="utf-8").read()
    assert tpl.count("__DATA__") == 1
    html = tpl.replace("__DATA__", blob).replace("__EDITION__", D["edition"])
    open(OUT, "w", encoding="utf-8").write(html)
    print(f"wrote {OUT}: {len(out)} questions, {len(html) // 1024} KB")


if __name__ == "__main__":
    main()
