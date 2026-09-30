"""Do the conclusions survive different assumptions? Re-run an analysis over a small grid of
assumption settings (sim/data/assumptions.json values changed per run, never on disk).

    .venv/bin/python -m sim.analyze.sensitivity                               # cut analysis, default grid
    .venv/bin/python -m sim.analyze.sensitivity --grid melee.base_hit_per_second=0.18,0.26 \
        --grid time.speech_words_per_second=2,3 --factorial
    .venv/bin/python -m sim.analyze.sensitivity --analysis winrate --games 1000

--analysis cut (default) reads sim/out/cut.json (from sim.analyze.cut) and re-evaluates the same
candidate abilities and merges, on the same seeds, at each setting; the baseline setting is reused
from cut.json. For each setting it redoes the ranking and the greedy selection with the same target,
universe and protections, and reports:
  - per ability: its rank, whether it is in the bottom `target` share of the ranking, and whether the
    greedy selection picks it, at every setting; `stable_in_cut` means picked at every setting
  - per setting: Spearman correlation of impacts with the baseline setting, and the overlap (Jaccard)
    of the chosen set with the baseline's
--analysis winrate runs one baseline per setting and compares class win-rate orderings.

Grids: each --grid KEY=v1,v2,... varies one assumption. One-at-a-time (default) changes one key per
setting with the others at their baseline value; --factorial runs every combination.
Writes sim/out/sensitivity.json (read by the HTML report).
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import time

from sim.paths import OUT

DEFAULT_GRID = {
    "time.speech_words_per_second": [2.0, 3.0],
    "melee.base_hit_per_second": [0.18, 0.26],
    "casting.p_interrupt_on_armor_hit": [0.3, 0.7],
}


def parse_grid(items) -> dict[str, list]:
    """['a.b=1,2', ...] -> {'a.b': [1, 2]} (values JSON-parsed when possible)."""
    from sim.run import parse_assume
    grid = {}
    for item in items or ():
        key, sep, raw = item.partition("=")
        if not sep:
            raise ValueError(f"--grid expects KEY=v1,v2,..., got {item!r}")
        vals = [v for v in raw.split(",") if v.strip()]
        grid[key.strip()] = [parse_assume([f"{key.strip()}={v}"])[key.strip()] for v in vals]
    return grid


def settings(grid: dict[str, list], factorial: bool = False) -> list[dict]:
    """Non-baseline settings: one-at-a-time, or every combination."""
    if factorial:
        keys = sorted(grid)
        return [dict(zip(keys, combo)) for combo in itertools.product(*(grid[k] for k in keys))]
    return [{k: v} for k in sorted(grid) for v in grid[k]]


def spearman(x: list[float], y: list[float]) -> float:
    """Spearman rank correlation with average ranks for ties (nan if undefined)."""
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    if len(x) < 3:
        return float("nan")
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else float("nan")


def jaccard(a, b) -> float:
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 1.0


def _label(setting: dict) -> str:
    return ", ".join(f"{k}={json.dumps(v)}" for k, v in sorted(setting.items())) or "baseline"


def _cut_outcome(singles, merges, merged, ctab, metric, sel_meta, protect) -> dict:
    from sim.analyze.cut import items_from, rank, select
    items = items_from(singles, merges, merged, ctab, metric)
    ranking = rank([it for it in items if it["kind"] == "cut"])
    sel = select(items, sel_meta["universe_count"], sel_meta["universe_complexity"], sel_meta["target"],
                 sel_meta["by"], protect)
    bottom_n = math.ceil(sel_meta["target"] * len(ranking) - 1e-9)
    return {"ranks": {it["remove"]: it["rank"] for it in ranking},
            "impact": {it["remove"]: it["impact"] for it in ranking},
            "bottom": sorted(it["remove"] for it in ranking if it["rank"] <= bottom_n),
            "chosen": sorted(f"{it['remove']}>{it['keep']}" if it["kind"] == "merge" else it["remove"]
                             for it in sel["chosen"]),
            "reached": sel["reached"]}


def run_cut(cut: dict, grid_settings: list[dict], games: int | None, workers) -> dict:
    from sim.analyze.cut import evaluate
    meta = cut["meta"]
    games = games or meta["games"]
    seeds = list(range(meta["seeds"][0], meta["seeds"][0] + games))
    candidates = sorted(cut["singles"])
    merges = [{k: m[k] for k in ("remove", "keep", "saved", "relation")} for m in cut["merges"] if "impact" in m]
    ctab = cut["complexity"]
    sel_meta = cut["selection"]
    protect = meta["protect"]
    base_assume = meta.get("assume") or {}
    rows = []
    if games == meta["games"]:
        merged = {f"{m['remove']}>{m['keep']}": m["impact"] for m in cut["merges"] if "impact" in m}
        base_out = _cut_outcome(cut["singles"], merges, merged, ctab, meta["metric"], sel_meta, protect)
        rows.append({"setting": {}, "label": "baseline", "seconds": 0.0, **base_out})
        todo = grid_settings
    else:
        todo = [{}] + grid_settings
    for st in todo:
        t = time.perf_counter()
        print(f"setting {_label(st)}: {1 + len(candidates) + len(merges)} runs of {games} games")
        ev = evaluate(candidates, merges, seeds, meta["config"], workers, {**base_assume, **st}, log=lambda *_: None)
        out = _cut_outcome(ev["singles"], merges, ev["merges"], ctab, meta["metric"], sel_meta, protect)
        rows.append({"setting": st, "label": _label(st), "seconds": time.perf_counter() - t, **out})
    base = rows[0]
    for r in rows:
        common = sorted(set(base["impact"]) & set(r["impact"]))
        r["spearman_vs_baseline"] = spearman([base["impact"][s] for s in common], [r["impact"][s] for s in common])
        r["jaccard_chosen"] = jaccard(base["chosen"], r["chosen"])
        r["jaccard_bottom"] = jaccard(base["bottom"], r["bottom"])
    abilities = {}
    for s in candidates:
        ranks = [r["ranks"].get(s) for r in rows]
        in_bottom = [s in r["bottom"] for r in rows]
        in_cut = [s in r["chosen"] for r in rows]
        abilities[s] = {"ranks": ranks, "in_bottom": in_bottom, "in_cut": in_cut,
                        "stable_in_bottom": all(in_bottom), "stable_in_cut": all(in_cut),
                        "share_in_cut": sum(in_cut) / len(rows)}
    for m in merges:
        key = f"{m['remove']}>{m['keep']}"
        in_cut = [key in r["chosen"] for r in rows]
        abilities[key] = {"ranks": [None] * len(rows), "in_bottom": [False] * len(rows), "in_cut": in_cut,
                          "stable_in_bottom": False, "stable_in_cut": all(in_cut),
                          "share_in_cut": sum(in_cut) / len(rows), "merge": True}
    base_chosen = base["chosen"]
    held = [c for c in base_chosen if abilities.get(c, {}).get("stable_in_cut")]
    return {"analysis": "cut", "games": games, "settings": rows, "abilities": abilities,
            "summary": {"baseline_chosen": len(base_chosen), "chosen_at_every_setting": len(held),
                        "stable": held,
                        "min_spearman": min((r["spearman_vs_baseline"] for r in rows[1:]
                                             if r["spearman_vs_baseline"] == r["spearman_vs_baseline"]),
                                            default=float("nan")),
                        "min_jaccard_chosen": min((r["jaccard_chosen"] for r in rows[1:]), default=float("nan"))}}


def run_winrate(grid_settings: list[dict], games: int, seed: int, config_name: str, workers) -> dict:
    from sim.analyze.winrate import players_frame, winrates_from_frame
    from sim.run import run_games
    from sim.scenarios import load_config
    config = load_config(config_name)
    seeds = list(range(seed, seed + games))
    rows = []
    for st in [{}] + grid_settings:
        t = time.perf_counter()
        res = run_games(seeds, config, (), workers, st)
        wr = winrates_from_frame(players_frame(res), ["cls"])
        rates = dict(zip(wr["cls"], wr["win_rate"]))
        rows.append({"setting": st, "label": _label(st), "seconds": time.perf_counter() - t, "rates": rates,
                     "ci": {c: [lo, hi] for c, lo, hi in zip(wr["cls"], wr["ci_low"], wr["ci_high"])},
                     "best": max(rates, key=rates.get), "worst": min(rates, key=rates.get)})
        print(f"setting {rows[-1]['label']}: best {rows[-1]['best']}, worst {rows[-1]['worst']}")
    base = rows[0]
    for r in rows:
        common = sorted(set(base["rates"]) & set(r["rates"]))
        r["spearman_vs_baseline"] = spearman([base["rates"][c] for c in common], [r["rates"][c] for c in common])
    return {"analysis": "winrate", "games": games, "settings": rows,
            "summary": {"best_stable": all(r["best"] == base["best"] for r in rows),
                        "worst_stable": all(r["worst"] == base["worst"] for r in rows),
                        "min_spearman": min(r["spearman_vs_baseline"] for r in rows)}}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--analysis", choices=("cut", "winrate"), default="cut")
    ap.add_argument("--grid", action="append", default=[], metavar="KEY=v1,v2")
    ap.add_argument("--factorial", action="store_true")
    ap.add_argument("--from", dest="src", default=str(OUT / "cut.json"), help="cut.json to re-evaluate")
    ap.add_argument("--games", type=int, default=0, help="games per run (cut: default as in cut.json)")
    ap.add_argument("--seed", type=int, default=0, help="winrate only")
    ap.add_argument("--config", default="mixed", help="winrate only")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(OUT / "sensitivity.json"))
    args = ap.parse_args(argv)
    from sim.rules.compile import default_rules
    from sim.run import apply_assume
    try:
        grid = parse_grid(args.grid) if args.grid else dict(DEFAULT_GRID)
        for k, vals in grid.items():
            for v in vals:
                apply_assume(default_rules().assumptions, {k: v})
    except ValueError as exc:
        ap.error(str(exc))
    todo = settings(grid, args.factorial)
    workers = args.workers or os.cpu_count() or 1
    t0 = time.perf_counter()
    if args.analysis == "cut":
        if not os.path.exists(args.src):
            ap.error(f"{args.src} not found; run python -m sim.analyze.cut first")
        cut = json.load(open(args.src))
        out = run_cut(cut, todo, args.games or None, workers)
        s = out["summary"]
        print(f"\n{s['chosen_at_every_setting']} of {s['baseline_chosen']} chosen cuts/merges are chosen at every "
              f"setting; min Spearman of impacts vs baseline {s['min_spearman']:.2f}; "
              f"min overlap of chosen sets {s['min_jaccard_chosen']:.2f}")
        for r in out["settings"]:
            print(f"  {r['label']:45s} rho {r['spearman_vs_baseline']:.2f}  overlap {r['jaccard_chosen']:.2f}  "
                  f"chosen {len(r['chosen'])}")
    else:
        out = run_winrate(todo, args.games or 1000, args.seed, args.config, workers)
        s = out["summary"]
        print(f"best class stable: {s['best_stable']}; worst class stable: {s['worst_stable']}; "
              f"min Spearman {s['min_spearman']:.2f}")
    out["grid"] = grid
    out["factorial"] = args.factorial
    out["wall_seconds"] = time.perf_counter() - t0
    out["created"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"wrote {args.out} (wall {out['wall_seconds']:.1f}s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
