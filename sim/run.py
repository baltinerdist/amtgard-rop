"""Run many games in parallel and store the results in DuckDB.

    .venv/bin/python -m sim.run --games 1000                      # mixed scenarios, all cores
    .venv/bin/python -m sim.run --games 500 --config small --seed 100 --ablate call-lightning,heal
    .venv/bin/python -m sim.run --games 500 --assume melee.base_hit_per_second=0.3 \
        --assume "range.p_in_range.20'=0.4"                      # change assumptions for this run only
    .venv/bin/python -m sim.run --games 500 --substitute icy-blast:iceball   # merge: holders of Icy Blast get Iceball

Each game is fully determined by its seed (scenario, loadouts and play all derive their own
random streams from it), so a seed replays exactly and paired runs share scenarios.

Variants (both change the rules object the workers build, never the files on disk):
  --assume  KEY=VALUE   KEY is group.name[.sub...] in sim/data/assumptions.json; the value is JSON
                        (numbers, true/false, lists, objects) or else a plain string. Sub-keys reach into
                        a dict-valued assumption, e.g. melee.shield_logit.large=-0.8. Repeatable.
  --substitute B:A,...  merge B into A: every class-table entry for B (and Look The Part options) now
                        names A, keeping B's levels, frequency, cost and options. A Magic User class that
                        already lists A folds B's entry into A's: A's copy cap becomes the sum of the two
                        and A is buyable from the earlier of the two levels.

Tables (appended to; one row set per run_id):
  runs      run_id, started, games, seed, config, ablate, assume, substitute, wall_seconds, workers
  games     run_id, seed, game_type, balance, n_players, skill_sd, winner, duration
  players   run_id, seed, pid, team, cls, level, skill, role, kills, deaths, time_dead, won
  abilities run_id, seed, slug, metric, detail, n     (metric: cast / applied / noop / fail / kill)
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import os
import time
import uuid
from multiprocessing import Pool

from sim.paths import OUT

_RULES: dict = {}
NO_VARIANT: tuple = ((), ())


# ---------------------------------------------------------------- variants: --assume and --substitute

def parse_assume(items) -> dict:
    """['melee.base_hit_per_second=0.3', ...] -> {'melee.base_hit_per_second': 0.3, ...}.
    Values are parsed as JSON when possible (0.3, true, [1,2], {"a":1}), otherwise kept as strings."""
    out = {}
    for item in items or ():
        key, sep, raw = item.partition("=")
        key = key.strip()
        if not sep or not key or len(key.split(".")) < 2:
            raise ValueError(f"--assume expects group.name[.sub]=value, got {item!r}")
        raw = raw.strip()
        try:
            val = json.loads(raw)
        except json.JSONDecodeError:
            val = raw
        out[key] = val
    return out


def apply_assume(assumptions: dict, overrides: dict) -> dict:
    """A deep copy of `assumptions` with each dotted override applied to the entry's "value".
    Unknown keys and type changes (a number replaced by a string, say) raise ValueError."""
    out = copy.deepcopy(assumptions)
    for key, val in overrides.items():
        group, name, *sub = key.split(".")
        if sub and sub[0] == "value":
            sub = sub[1:]
        grp = out.get(group)
        entry = grp.get(name) if isinstance(grp, dict) else None
        if not isinstance(entry, dict) or "value" not in entry:
            known = sorted(grp) if isinstance(grp, dict) else sorted(g for g in out if not g.startswith("_"))
            raise ValueError(f"unknown assumption {group}.{name}; known here: {', '.join(known)}")
        holder, last = entry, "value"
        for part in sub:
            cur = holder[last]
            if not isinstance(cur, dict) or part not in cur:
                opts = ", ".join(map(str, cur)) if isinstance(cur, dict) else "(not a dict)"
                raise ValueError(f"unknown sub-key {part!r} in {key}; options: {opts}")
            holder, last = cur, part
        old = holder[last]
        num = (int, float)
        if isinstance(old, bool) != isinstance(val, bool) or (
                isinstance(old, num) and not isinstance(val, num)) or (
                isinstance(old, (dict, list, str)) and type(old) is not type(val)):
            raise ValueError(f"{key}: {val!r} does not match the type of the current value {old!r}")
        holder[last] = val
    return out


def substitute_classes(classes: dict, subs: dict) -> dict:
    """Class sheets with ability B replaced by A for every B -> A in `subs` (see module doc)."""
    out = {}
    for name, sheet in classes.items():
        have = {ca.slug for ca in sheet.abilities}
        absorbed: dict[str, list] = {}   # A -> B entries folded into A's spell-list entry
        rows = []
        for ca in sheet.abilities:
            target = subs.get(ca.slug)
            if target is None:
                rows.append(ca)
            elif sheet.magic_user and target in have:
                absorbed.setdefault(target, []).append(ca)
            else:
                rows.append(dataclasses.replace(ca, slug=target))
        for i, ca in enumerate(rows):
            extra = absorbed.pop(ca.slug, None) if ca.kind in ("spell", "archetype") else None
            if extra:
                mx = None if ca.max is None or any(b.max is None for b in extra) else ca.max + sum(b.max for b in extra)
                lv = tuple(sorted(set(ca.levels).union(*(b.levels for b in extra))))
                rows[i] = dataclasses.replace(ca, max=mx, levels=lv)
        ltp = sheet.look_the_part
        if ltp and ltp.get("options"):
            ltp = {**ltp, "options": [{**o, "slug": subs.get(o["slug"], o["slug"])} for o in ltp["options"]]}
        out[name] = dataclasses.replace(sheet, abilities=tuple(rows), look_the_part=ltp)
    return out


def make_variant(assume: dict | None = None, substitute: dict | None = None) -> tuple:
    """Hashable, picklable description of a rules variant: ((key, json value)...), ((B, A)...)."""
    a = tuple(sorted((k, json.dumps(v, sort_keys=True)) for k, v in (assume or {}).items()))
    s = tuple(sorted((substitute or {}).items()))
    return (a, s)


def variant_rules(variant: tuple = NO_VARIANT):
    """Rules for a variant; the default rules when the variant is empty."""
    from sim.rules.compile import default_rules
    rules = default_rules()
    assume, subs = variant
    if assume:
        rules = dataclasses.replace(rules, assumptions=apply_assume(
            rules.assumptions, {k: json.loads(v) for k, v in assume}))
    if subs:
        rules = dataclasses.replace(rules, classes=substitute_classes(rules.classes, dict(subs)))
    return rules


def _rules(variant: tuple = NO_VARIANT):
    if variant not in _RULES:
        _RULES[variant] = variant_rules(variant)
    return _RULES[variant]


# ---------------------------------------------------------------- running

def play_seed(args: tuple) -> dict:
    """Worker entry point: (seed, config, ablate[, variant]) -> result dict with the scenario summary."""
    from sim.engine.game import play
    from sim.scenarios import generate
    seed, config, ablate, *rest = args
    rules = _rules(rest[0] if rest else NO_VARIANT)
    sc = generate(seed, config, rules)
    res = play(rules, sc, seed, frozenset(ablate))
    res["scenario"] = {k: v for k, v in sc.items() if k != "teams"}
    return res


def run_games(seeds: list[int], config: dict, ablate: tuple = (), workers: int | None = None,
              assume: dict | None = None, substitute: dict | None = None) -> list[dict]:
    variant = make_variant(assume, substitute)
    jobs = [(s, config, tuple(ablate), variant) for s in seeds]
    workers = workers or os.cpu_count() or 1
    if workers == 1:
        results = [play_seed(j) for j in jobs]
    else:
        with Pool(workers) as pool:
            results = list(pool.imap_unordered(play_seed, jobs, chunksize=max(1, len(jobs) // (workers * 8))))
    results.sort(key=lambda r: r["seed"])
    return results


def frames(results: list[dict], run_id: str):
    import pandas as pd
    games, players, abil = [], [], []
    for r in results:
        sc = r["scenario"]
        games.append({"run_id": run_id, "seed": r["seed"], "game_type": sc["game_type"], "balance": sc["balance"],
                      "n_players": sc["n_players"], "skill_sd": sc["skill_sd"], "winner": r["winner"],
                      "duration": r["duration"]})
        for p in r["players"]:
            players.append({"run_id": run_id, "seed": r["seed"], **p})
        for slug, n in r["casts"].items():
            abil.append((run_id, r["seed"], slug, "cast", "", n))
        for metric in ("applied", "noops", "fails"):
            for key, n in r[metric].items():
                slug, detail = key.split("|", 1)
                abil.append((run_id, r["seed"], slug, metric.rstrip("s"), detail, n))
        for slug, n in r["kill_sources"].items():
            abil.append((run_id, r["seed"], slug, "kill", "", n))
    return (pd.DataFrame(games), pd.DataFrame(players),
            pd.DataFrame(abil, columns=["run_id", "seed", "slug", "metric", "detail", "n"]))


def store(results: list[dict], run_meta: dict, db_path) -> None:
    import duckdb
    import pandas as pd
    g, p, a = frames(results, run_meta["run_id"])
    runs = pd.DataFrame([run_meta])
    con = duckdb.connect(str(db_path))
    for name, df in (("runs", runs), ("games", g), ("players", p), ("abilities", a)):
        con.register("df", df)
        exists = con.execute("select count(*) from information_schema.tables where table_name = ?", [name]).fetchone()[0]
        if exists:
            cols = {r[0] for r in con.execute(
                "select column_name from information_schema.columns where table_name = ?", [name]).fetchall()}
            for col in df.columns:
                if col not in cols:  # e.g. runs.assume / runs.substitute in databases made before they existed
                    con.execute(f'alter table {name} add column "{col}" varchar')
            con.execute(f"insert into {name} by name select * from df")
        else:
            con.execute(f"create table {name} as select * from df")
        con.unregister("df")
    con.close()


def parse_substitute(text: str) -> dict:
    """'b1:a1,b2:a2' -> {'b1': 'a1', 'b2': 'a2'} (B is removed, its holders get A)."""
    out = {}
    for part in (s.strip() for s in text.split(",")):
        if not part:
            continue
        b, sep, a = part.partition(":")
        if not sep or not a or not b or a == b:
            raise ValueError(f"--substitute expects removed:kept pairs, got {part!r}")
        out[b.strip()] = a.strip()
    return out


def main(argv=None) -> int:
    from sim.scenarios import load_config
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0, help="first seed; games use seed..seed+games-1")
    ap.add_argument("--config", default="mixed", help="preset name (mixed/small/large) or JSON file")
    ap.add_argument("--ablate", default="", help="comma-separated ability slugs to remove from every loadout")
    ap.add_argument("--substitute", default="", help="comma-separated B:A merges (B's holders get A instead)")
    ap.add_argument("--assume", action="append", default=[], metavar="KEY=VALUE",
                    help="override an assumptions.json value for this run (repeatable)")
    ap.add_argument("--workers", type=int, default=0, help="processes (default: all cores)")
    ap.add_argument("--db", default=str(OUT / "runs.duckdb"))
    args = ap.parse_args(argv)

    config = load_config(args.config)
    ablate = tuple(s for s in args.ablate.split(",") if s)
    from sim.rules.compile import default_rules
    rules = default_rules()
    try:
        assume = parse_assume(args.assume)
        apply_assume(rules.assumptions, assume)
        subs = parse_substitute(args.substitute)
    except ValueError as exc:
        ap.error(str(exc))
    unknown = [s for s in (*ablate, *subs, *subs.values()) if s not in rules.abilities]
    if unknown:
        ap.error(f"unknown ability slug(s): {', '.join(unknown)}")
    OUT.mkdir(parents=True, exist_ok=True)
    workers = args.workers or os.cpu_count() or 1
    seeds = list(range(args.seed, args.seed + args.games))
    t0 = time.perf_counter()
    results = run_games(seeds, config, ablate, workers, assume, subs)
    wall = time.perf_counter() - t0
    run_id = uuid.uuid4().hex[:12]
    meta = {"run_id": run_id, "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "games": len(results),
            "seed": args.seed, "config": json.dumps(config, sort_keys=True), "ablate": ",".join(ablate),
            "assume": json.dumps(assume, sort_keys=True) if assume else "",
            "substitute": ",".join(f"{b}:{a}" for b, a in sorted(subs.items())),
            "wall_seconds": round(wall, 3), "workers": workers}
    store(results, meta, args.db)
    draws = sum(1 for r in results if r["winner"] == -1)
    print(f"run {run_id}: {len(results)} games in {wall:.1f}s on {workers} workers "
          f"({len(results) / wall:.1f} games/s); draws {draws}; stored in {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
