"""Complexity cost per ability: how much rule text and rules knowledge an ability costs the game.

    .venv/bin/python -m sim.analyze.complexity                 # top of the table
    .venv/bin/python -m sim.analyze.complexity --csv sim/out/complexity.csv

Everything is counted from metadata/abilities.json (nothing is simulated):

| component       | counted as                                                                   |
| --------------- | ---------------------------------------------------------------------------- |
| sentences       | rule sentences (Effect, Limitations and Note fields)                          |
| words           | words in those sentences                                                      |
| incantation     | incantation words x repetitions (what a player has to say each cast)          |
| requirements    | structured requirements (e.g. target must be wounded)                         |
| restrictions    | structured restrictions (e.g. may not be used while engaged)                  |
| endings         | ending conditions (the metadata's `termination` list)                         |
| properties      | properties (e.g. bypass-armor, engulfing, kill-trigger)                       |
| references      | references to other rules: states, mechanics, other abilities                 |
| clarifications  | clarifications the metadata had to record                                     |
| open_questions  | open questions the text leaves unanswered                                     |
| classes         | distinct classes that carry it                                                |
| class_levels    | class-level entries that carry it (a class listing it at 1st and 3rd counts 2)|

**Score** = sum over components of WEIGHTS[component] x count. A point is meant to be roughly
"one more rule sentence to learn": each structured condition is a thing to remember (1 point),
long text and long incantations cost a little per word, each open question is a likely argument
on the field (1 point), and an ability carried by more classes and levels is one more players
must know. The weights are a judgment call; change them here and every analysis follows.
`--csv` and `table()` report each component's count *and* its points, so the total is never the
only thing shown.
"""
from __future__ import annotations

import argparse
import csv
import json

from sim.paths import ABILITIES_JSON

# points per unit of each component; edit here
WEIGHTS: dict[str, float] = {
    "sentences": 1.0,        # per rule sentence
    "words": 0.05,           # per word of rule text (20 words = 1 point)
    "incantation": 0.1,      # per incantation word spoken (words x repetitions)
    "requirements": 1.0,     # per requirement
    "restrictions": 1.0,     # per restriction
    "endings": 1.0,          # per ending condition
    "properties": 1.0,       # per property
    "references": 0.25,      # per reference to another rule
    "clarifications": 0.5,   # per clarification
    "open_questions": 1.0,   # per open question
    "classes": 0.5,          # per class carrying it
    "class_levels": 0.25,    # per class-level entry
}
COMPONENTS = tuple(WEIGHTS)

# components that exist because classes carry the ability (not its own text); a merge keeps these
CARRY_COMPONENTS = ("classes", "class_levels")


def load_records(path=ABILITIES_JSON) -> list[dict]:
    recs = json.loads(open(path).read())["abilities"]
    return list(recs.values()) if isinstance(recs, dict) else recs


def counts(rec: dict) -> dict[str, int]:
    """Raw component counts for one ability record."""
    inc = rec.get("incantation") or {}
    words = int(inc.get("words") or 0)
    reps = int(inc.get("repetitions") or 1) if words else 0
    avail = rec.get("availability") or []
    return {
        "sentences": len(rec.get("sentences") or ()),
        "words": sum(len(s["text"].split()) for s in rec.get("sentences") or ()),
        "incantation": words * reps,
        "requirements": len(rec.get("requirements") or ()),
        "restrictions": len(rec.get("restrictions") or ()),
        "endings": len(rec.get("termination") or ()),
        "properties": len(rec.get("properties") or ()),
        "references": len(rec.get("references") or ()),
        "clarifications": len(rec.get("clarifications") or ()),
        "open_questions": len(rec.get("open_questions") or ()),
        "classes": len({a["cls"] for a in avail}),
        "class_levels": sum(len(a.get("levels") or ()) or 1 for a in avail),
    }


def score_counts(c: dict[str, int], weights: dict[str, float] | None = None) -> dict:
    """{'score', 'counts', 'points'} from raw component counts."""
    w = WEIGHTS if weights is None else weights
    pts = {k: w.get(k, 0.0) * c.get(k, 0) for k in COMPONENTS}
    return {"score": round(sum(pts.values()), 4), "counts": dict(c),
            "points": {k: round(v, 4) for k, v in pts.items()}}


def score(rec: dict, weights: dict[str, float] | None = None) -> dict:
    """{'slug', 'title', 'score', 'counts': {...}, 'points': {...}} for one ability record."""
    return {"slug": rec.get("slug", ""), "title": rec.get("title", ""), **score_counts(counts(rec), weights)}


def table(records: list[dict] | None = None, weights: dict[str, float] | None = None) -> dict[str, dict]:
    """slug -> score dict, for every ability in the metadata."""
    return {r["slug"]: score(r, weights) for r in (records or load_records())}


def own_text_score(entry: dict) -> float:
    """Score without the class-carry components: what a merge (B's holders get A) saves."""
    return round(entry["score"] - sum(entry["points"][k] for k in CARRY_COMPONENTS), 4)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Complexity cost per ability")
    ap.add_argument("--csv", default="")
    ap.add_argument("--top", type=int, default=25)
    args = ap.parse_args(argv)
    tab = sorted(table().values(), key=lambda e: -e["score"])
    total = sum(e["score"] for e in tab)
    print(f"{len(tab)} abilities, total complexity {total:.1f} points; weights: "
          + ", ".join(f"{k}={v:g}" for k, v in WEIGHTS.items()))
    head = "".join(f"{k[:6]:>7s}" for k in COMPONENTS)
    print(f"{'ability':28s}{'score':>7s}{head}")
    for e in tab[: args.top]:
        print(f"{e['slug']:28s}{e['score']:7.2f}" + "".join(f"{e['points'][k]:7.2f}" for k in COMPONENTS))
    if args.csv:
        with open(args.csv, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["slug", "score", *[f"n_{k}" for k in COMPONENTS], *[f"pts_{k}" for k in COMPONENTS]])
            for e in tab:
                wr.writerow([e["slug"], e["score"], *[e["counts"][k] for k in COMPONENTS],
                             *[e["points"][k] for k in COMPONENTS]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
