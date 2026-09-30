"""Which ~30% of abilities could be cut with the least change to how battlegames play?

    .venv/bin/python -m sim.analyze.cut --games 300                       # every measurable ability
    .venv/bin/python -m sim.analyze.cut --games 200 --sample 15 --merges 4 # quick look
    .venv/bin/python -m sim.analyze.cut --target 0.3 --by complexity --protect heal,mend
    .venv/bin/python -m sim.reports.build_report                           # -> sim/out/report.html

Pipeline (writes sim/out/cut.json, which the report and sim.analyze.sensitivity read):

1. **Complexity** of every ability (sim/analyze/complexity.py).
2. **Baseline** run over seeds seed..seed+games-1.
3. **Single ablations**: each candidate removed on its own, same seeds, compared with the baseline
   (sim/analyze/impact.py: holder-team win change and the gameplay change distance D).
   Candidates are abilities some baseline player held whose effects the engine executes at least
   partly. Abilities the engine cannot execute ("unmodeled") would show zero impact whatever they
   really do, so they are listed separately and left out unless --include-unmodeled.
4. **Merges**: pairs from metadata `pairs` (also listed in metadata/SIMILARITY.md) whose relation is
   identical / same effects / same effects with different numbers / plus a drawback. The ability
   carried by more class-levels is kept (A); the other (B) is replaced by A for its holders, simulated
   with sim.run's substitution. A merge saves B's own text (its complexity minus the class-carry part).
5. **Ranking** by impact per unit of complexity (impact = bias-corrected distance, `distance_adj`).
6. **Greedy selection** of cuts and merges until the target share is reached:
   --by count       remove >= target x N abilities, taking the smallest impact first (ties: larger saving)
   --by complexity  save >= target x total complexity, taking the smallest impact per point saved first
   An ability is removed at most once, a merge's kept ability is never removed, --protect is never removed.
   N and the total are over all abilities in the metadata, or over the evaluated ones when --sample or
   --abilities limits the evaluation (so a quick run still picks a proportionate set).
7. **Combined check**: the chosen set is removed together and re-simulated, because single-ablation
   impacts do not add up (abilities substitute for and counter each other).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import re
import subprocess
import time

from sim.analyze import complexity as cx
from sim.analyze.ablation import ablate_one
from sim.analyze.impact import compare, run_summary
from sim.analyze.winrate import players_frame, winrates_from_frame
from sim.paths import OUT, REPO

MERGE_RELATIONS = ("identical", "same-effects", "same-effects-different-numbers", "plus-drawback")
MEASURED = ("full", "partial")          # coverage statuses whose ablation can show an effect
SIMILARITY_MD = REPO / "metadata" / "SIMILARITY.md"


# ---------------------------------------------------------------- merges

def similarity_notes(path=SIMILARITY_MD) -> dict[tuple[str, str], dict]:
    """(slug1, slug2) -> {'section', 'differences'} from the tables in metadata/SIMILARITY.md."""
    notes, section = {}, ""
    if not os.path.exists(path):
        return notes
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "):
            section = re.sub(r"\s*\(\d+ pairs?\)\s*$", "", line[3:].strip())
        elif line.startswith("| ["):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            slugs = re.findall(r"profiles/([a-z0-9-]+)\.md", line)
            if len(slugs) >= 2 and len(cells) >= 3:
                notes[(slugs[0], slugs[1])] = {"section": section, "differences": cells[2]}
    return notes


def merge_candidates(pairs: list[dict], ctab: dict, coverage: dict, known: set[str],
                     protect=(), notes: dict | None = None) -> list[dict]:
    """Merge proposals B -> A from metadata pairs (see module doc for the relation filter and direction)."""
    notes = notes or {}
    out, seen = [], set()
    order = {r: i for i, r in enumerate(MERGE_RELATIONS)}
    for p in sorted(pairs, key=lambda p: (order.get(p["relation"], 99), -p.get("score", 0), p["a"], p["b"])):
        if p["relation"] not in MERGE_RELATIONS:
            continue
        x, y = p["a"], p["b"]
        if x not in known or y not in known or x not in ctab or y not in ctab:
            continue
        if any(coverage.get(s, {}).get("status") not in MEASURED for s in (x, y)):
            continue
        cx_, cy = ctab[x], ctab[y]
        # keep the more widely carried ability; on a tie keep the simpler one (remove the more complex)
        kx = (cx_["counts"]["class_levels"], -cx_["score"])
        ky = (cy["counts"]["class_levels"], -cy["score"])
        keep, remove = (x, y) if kx >= ky else (y, x)
        if remove in protect or (remove, keep) in seen:
            continue
        seen.add((remove, keep))
        note = notes.get((x, y)) or notes.get((y, x)) or {}
        out.append({"remove": remove, "keep": keep, "relation": p["relation"],
                    "differences": note.get("differences", ""), "saved": cx.own_text_score(ctab[remove])})
    return out


# ---------------------------------------------------------------- ranking and greedy selection

def rank(items: list[dict]) -> list[dict]:
    """Items sorted by impact per point of complexity (ascending), with 'ratio' and 'rank' added."""
    out = []
    for it in items:
        ratio = it["impact"] / it["saved"] if it["saved"] > 0 else math.inf
        out.append({**it, "ratio": ratio})
    out.sort(key=lambda it: (it["ratio"], -it["saved"], it["remove"]))
    for i, it in enumerate(out, 1):
        it["rank"] = i
    return out


def select(items: list[dict], universe_count: int, universe_complexity: float, target: float = 0.3,
           by: str = "count", protect=()) -> dict:
    """Greedy cut set. Each item: {'kind': 'cut'|'merge', 'remove', 'keep' (merge only), 'impact', 'saved'}.
    Stops as soon as the target is met; `reached` says whether it was."""
    if by not in ("count", "complexity"):
        raise ValueError("by must be 'count' or 'complexity'")
    need_n = math.ceil(target * universe_count - 1e-9)
    need_c = target * universe_complexity
    if by == "count":
        key = lambda it: (it["impact"], -it["saved"], it["remove"])
    else:
        key = lambda it: (it["impact"] / it["saved"] if it["saved"] > 0 else math.inf, -it["saved"], it["remove"])
    protect = set(protect)
    removed, kept, chosen, saved, impact = set(), set(), [], 0.0, 0.0

    def done():
        return len(removed) >= need_n if by == "count" else saved >= need_c - 1e-9

    for it in sorted(items, key=key):
        if done():
            break
        r, k = it["remove"], it.get("keep")
        if r in removed or r in kept or r in protect or (k is not None and k in removed):
            continue
        chosen.append(it)
        removed.add(r)
        if k is not None:
            kept.add(k)
        saved += it["saved"]
        impact += it["impact"]
    return {"chosen": chosen, "reached": done(), "removed_count": len(removed), "need_count": need_n,
            "saved": round(saved, 4), "need_complexity": round(need_c, 4),
            "universe_count": universe_count, "universe_complexity": round(universe_complexity, 4),
            "impact_sum": impact, "impact_rss": math.sqrt(sum(it["impact"] ** 2 for it in chosen)),
            "target": target, "by": by}


# ---------------------------------------------------------------- evaluation

def _git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True,
                              text=True, timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001 - metadata only
        return ""


def _impact_row(row: dict) -> dict:
    keep = ("games_present", "games_with_holder", "casts_per_game_present", "holder_win_delta", "holder_ci_low",
            "holder_ci_high", "distance", "distance_lo", "distance_hi", "noise", "distance_adj", "measures")
    return {k: row[k] for k in keep}


def evaluate(candidates: list[str], merges: list[dict], seeds: list[int], config: dict, workers,
             assume: dict | None = None, log=print, base: list[dict] | None = None,
             base_seconds: float = 0.0, space: str = "off") -> dict:
    """Baseline (unless given) + one run per candidate and per merge.
    Returns {'base', 'singles', 'merges', 'timing'}."""
    from sim.run import run_games
    t0 = time.perf_counter()
    if base is None:
        base = run_games(seeds, config, (), workers, assume, space=space)
    t_base = time.perf_counter() - t0 + base_seconds
    singles = {}
    t1 = time.perf_counter()
    for i, slug in enumerate(candidates, 1):
        row = ablate_one(base, seeds, config, workers, (slug,), assume=assume, space=space)
        singles[slug] = _impact_row(row)
        log(f"  [{i}/{len(candidates)}] {slug:30s} D_adj {row['distance_adj']:.3f}  "
            f"holder {row['holder_win_delta']:+.3f}  present {row['games_present']}")
    t_singles = time.perf_counter() - t1
    merged = {}
    t2 = time.perf_counter()
    for i, m in enumerate(merges, 1):
        row = ablate_one(base, seeds, config, workers, (), {m["remove"]: m["keep"]}, assume, space)
        merged[f"{m['remove']}>{m['keep']}"] = _impact_row(row)
        log(f"  [merge {i}/{len(merges)}] {m['remove']} -> {m['keep']}: D_adj {row['distance_adj']:.3f}")
    t_merges = time.perf_counter() - t2
    runs = 1 + len(candidates) + len(merges)
    total = time.perf_counter() - t0 + base_seconds
    return {"base": base, "singles": singles, "merges": merged,
            "timing": {"baseline_s": t_base, "singles_s": t_singles, "merges_s": t_merges, "total_s": total,
                       "runs": runs, "seconds_per_run": total / runs, "games_per_run": len(seeds)}}


def items_from(singles: dict, merges: list[dict], merged: dict, ctab: dict, metric: str) -> list[dict]:
    items = []
    for slug, imp in singles.items():
        items.append({"kind": "cut", "remove": slug, "keep": None, "impact": imp[metric],
                      "saved": ctab[slug]["score"]})
    for m in merges:
        key = f"{m['remove']}>{m['keep']}"
        if key in merged:
            items.append({"kind": "merge", "remove": m["remove"], "keep": m["keep"],
                          "impact": merged[key][metric], "saved": m["saved"]})
    return items


def main(argv=None) -> int:
    from sim.rules.compile import default_rules
    from sim.rules.coverage import compute as coverage_compute
    from sim.run import add_space_arg, apply_assume, parse_assume, run_games, warn_space
    from sim.scenarios import load_config
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--games", type=int, default=300, help="games per run (baseline, each ablation, combined)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--config", default="mixed")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--target", type=float, default=0.3, help="share to cut (default 0.3)")
    ap.add_argument("--by", choices=("count", "complexity"), default="count")
    ap.add_argument("--protect", default="", help="comma-separated slugs that must stay")
    ap.add_argument("--abilities", default="", help="evaluate only these slugs (comma-separated)")
    ap.add_argument("--sample", type=int, default=0, help="evaluate a random sample of N candidates")
    ap.add_argument("--merges", type=int, default=-1, help="how many merge proposals to simulate (-1 all, 0 none)")
    ap.add_argument("--include-unmodeled", action="store_true",
                    help="also rank abilities the engine cannot execute (their impact reads as ~0)")
    ap.add_argument("--metric", choices=("distance_adj", "distance"), default="distance_adj")
    ap.add_argument("--assume", action="append", default=[], metavar="KEY=VALUE")
    ap.add_argument("--no-combined", action="store_true", help="skip the combined re-simulation")
    ap.add_argument("--out", default=str(OUT / "cut.json"))
    add_space_arg(ap)
    args = ap.parse_args(argv)
    warn_space(args.space)
    if not 0 < args.target < 1:
        ap.error("--target must be between 0 and 1")

    rules = default_rules()
    try:
        assume = parse_assume(args.assume)
        apply_assume(rules.assumptions, assume)
    except ValueError as exc:
        ap.error(str(exc))
    protect = [s for s in args.protect.split(",") if s]
    bad = [s for s in protect if s not in rules.abilities]
    if bad:
        ap.error(f"unknown slug(s) in --protect: {', '.join(bad)}")
    config = load_config(args.config)
    workers = args.workers or os.cpu_count() or 1
    seeds = list(range(args.seed, args.seed + args.games))
    records = cx.load_records()
    ctab = cx.table(records)
    cov = coverage_compute(rules)["abilities"]

    # the baseline decides the candidates: an ability nobody held has no measurable impact
    t_start = time.perf_counter()
    print(f"baseline: {args.games} games ...")
    base = run_games(seeds, config, (), workers, assume, space=args.space)
    t_base = time.perf_counter() - t_start
    held = {s for r in base for s, h in r["holdings"].items() if sum(h)}
    status = {}
    for slug in ctab:
        if slug in protect:
            status[slug] = "protected"
        elif cov.get(slug, {}).get("status") not in MEASURED:
            status[slug] = "unmodeled"
        elif slug not in held:
            status[slug] = "not-held"
        else:
            status[slug] = "candidate"
    if args.include_unmodeled:
        status.update({s: "candidate" for s, st in status.items() if st == "unmodeled" and s in held})
    pool = sorted(s for s, st in status.items() if st == "candidate")
    if args.abilities:
        pool = [s for s in args.abilities.split(",") if s]
        bad = [s for s in pool if s not in ctab]
        if bad:
            ap.error(f"unknown slug(s) in --abilities: {', '.join(bad)}")
    elif args.sample:
        pool = sorted(random.Random(args.seed).sample(pool, min(args.sample, len(pool))))
    limited = bool(args.abilities or args.sample)

    pairs = json.loads(open(cx.ABILITIES_JSON).read()).get("pairs", [])
    all_merges = [m for m in merge_candidates(pairs, ctab, cov, set(rules.abilities), protect, similarity_notes())
                  if m["remove"] in held]  # B needs holders for the substitution to show anything
    merges = all_merges
    if args.merges >= 0:
        merges = merges[: args.merges]

    print(f"evaluating {len(pool)} single ablations and {len(merges)} merges at {args.games} games each "
          f"on {workers} workers")
    ev = evaluate(pool, merges, seeds, config, workers, assume, base=base, base_seconds=t_base, space=args.space)
    items = items_from(ev["singles"], merges, ev["merges"], ctab, args.metric)
    ranking = rank([it for it in items if it["kind"] == "cut"])
    if limited:
        uni = set(pool) | {m["remove"] for m in merges}
        u_count, u_cx = len(uni), sum(ctab[s]["score"] for s in uni)
    else:
        u_count, u_cx = len(ctab), sum(e["score"] for e in ctab.values())
    sel = select(items, u_count, u_cx, args.target, args.by, protect)

    combined = None
    if sel["chosen"] and not args.no_combined:
        cuts = tuple(sorted(it["remove"] for it in sel["chosen"] if it["kind"] == "cut"))
        subs = {it["remove"]: it["keep"] for it in sel["chosen"] if it["kind"] == "merge"}
        t = time.perf_counter()
        var = run_games(seeds, config, cuts, workers, assume, subs or None, args.space)
        row = compare(base, var, list(cuts) + list(subs))
        combined = {**_impact_row(row), "ablate": list(cuts), "substitute": subs,
                    "seconds": time.perf_counter() - t, "summary": run_summary(var),
                    "additive_sum": sel["impact_sum"], "additive_rss": sel["impact_rss"]}
    wall = time.perf_counter() - t_start

    n_full = sum(1 for st in status.values() if st == "candidate")
    m_full = len(all_merges)
    per_game = ev["timing"]["total_s"] / (ev["timing"]["runs"] * args.games)
    est = {"runs": n_full + m_full + 2, "games_per_run": args.games,
           "seconds_at_this_scale": (n_full + m_full + 2) * args.games * per_game,
           "seconds_at_1000_games": (n_full + m_full + 2) * 1000 * per_game,
           "seconds_per_game_wall": per_game, "candidates": n_full, "merges": m_full}

    wr = winrates_from_frame(players_frame(base), ["cls"])
    out = {
        "meta": {"created": time.strftime("%Y-%m-%dT%H:%M:%S"), "commit": _git_commit(), "games": args.games,
                 "seeds": [seeds[0], seeds[-1]], "config": config, "config_name": args.config, "workers": workers,
                 "assume": assume, "space": args.space, "target": args.target, "by": args.by, "protect": protect, "metric": args.metric,
                 "sample": args.sample, "abilities_arg": args.abilities, "limited": limited,
                 "include_unmodeled": args.include_unmodeled, "wall_seconds": wall, "timing": ev["timing"],
                 "full_run_estimate": est,
                 "complexity_weights": cx.WEIGHTS},
        "coverage": {"statuses": {k: sum(1 for v in cov.values() if v["status"] == k)
                                  for k in ("full", "partial", "none", "no effects")},
                     "ability_status": status},
        "baseline": {**run_summary(base), "class_winrates": wr.to_dict(orient="records")},
        "complexity": ctab,
        "singles": ev["singles"],
        "merges": [{**m, **({"impact": ev["merges"][f"{m['remove']}>{m['keep']}"]}
                             if f"{m['remove']}>{m['keep']}" in ev["merges"] else {})} for m in merges],
        "ranking": ranking,
        "selection": sel,
        "combined": combined,
    }
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    _print(out)
    print(f"wrote {args.out}  (wall {wall:.1f}s)")
    return 0


def _print(out: dict) -> None:
    sel, comb = out["selection"], out["combined"]
    print(f"\nranking by impact per complexity point ({out['meta']['metric']}):")
    print(f"{'rank':>4s} {'ability':28s} {'impact':>7s} {'cmplx':>6s} {'ratio':>7s} {'holder':>7s}")
    for it in out["ranking"]:
        s = out["singles"][it["remove"]]
        print(f"{it['rank']:4d} {it['remove']:28s} {it['impact']:7.3f} {it['saved']:6.2f} {it['ratio']:7.4f} "
              f"{s['holder_win_delta']:+7.3f}")
    print(f"\nselection (--by {sel['by']}, target {sel['target']:.0%}): removed {sel['removed_count']} of "
          f"{sel['universe_count']}, saved {sel['saved']:.1f} of {sel['universe_complexity']:.1f} points; "
          f"target {'reached' if sel['reached'] else 'NOT reached'}")
    for it in sel["chosen"]:
        what = it["remove"] if it["kind"] == "cut" else f"{it['remove']} -> {it['keep']} (merge)"
        print(f"  {what:44s} impact {it['impact']:.3f}  saves {it['saved']:.2f}")
    if comb:
        print(f"combined re-simulation: D {comb['distance']:.3f} [{comb['distance_lo']:.3f}, {comb['distance_hi']:.3f}]"
              f" adj {comb['distance_adj']:.3f}; singles sum {comb['additive_sum']:.3f}, rss {comb['additive_rss']:.3f}")
    est = out["meta"]["full_run_estimate"]
    print(f"full run: {est['runs']} runs ({est['candidates']} abilities + {est['merges']} merges + 2) "
          f"~{est['seconds_at_this_scale'] / 60:.1f} min at {est['games_per_run']} games/run, "
          f"~{est['seconds_at_1000_games'] / 60:.1f} min at 1000")


if __name__ == "__main__":
    raise SystemExit(main())
