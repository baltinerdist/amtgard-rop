"""Calibrate the usefulness score's anchor weights by measurement: paired "gifts" to one team.

    .venv/bin/python -m sim.analyze.calibrate                     # full run -> sim/data/value-calibration.json
    .venv/bin/python -m sim.analyze.calibrate --scale 0.1 --out /tmp/cal.json      # a quick look
    .venv/bin/python -m sim.analyze.calibrate --dry-run           # the plan and a time estimate
    .venv/bin/python -m sim.analyze.calibrate --report sim/data/value-calibration.json   # print a file's table
    .venv/bin/python -m sim.analyze.calibrate --weights           # every weight value.py uses, and its source

`sim/policies/value.py` scores abilities with anchor weights (a kill 10, a heal 4, 2 per point of
armor, a State 3-6, ...) that were set by hand. Here each anchor is **given** to team 0 as a gift
(`sim/engine/gifts.py`) and the change in team 0's result (win 1, draw 0.5, loss 0) is measured
against the same seeds without it. The gift draws from its own random stream, so the two games of a
pair share the scenario, every loadout and the play itself until the gift first matters: the
comparison is paired by seed, like the ablation harness.

**Recipients.** A gift to one player of a 30-player team moves the result by a few thousandths,
below what any affordable number of games resolves. So each gift goes to `SHARE` (half) of the
eligible players of team 0, at least one (a State: that many applications on random enemies), and
the change is reported **per unit**: per recipient, per point of armor, per application. A pilot
in small annihilation games gave the same per-unit value for one recipient and for all eligible
ones, within the intervals: Finger of Death 0.015 ± 0.014 and 0.025 ± 0.004 per recipient; a point
of armor 0.028 ± 0.013 and 0.031 ± 0.006 (2,000 pairs each).

**Contexts.** The value of an anchor depends on the game, so every anchor is measured in six:
the small, mixed and large presets, each as Mutual Annihilation and as attrition. Each context
has its own game count (`CONTEXTS`), chosen so the full run takes about 2 h 20 min on 10 cores.

**Scale.** A win-probability change is converted to the score's scale by one reference: a use of
Finger of Death per life (a 20' Verbal whose only effect is `death.cause`) is worth
`REFERENCE_SCORE` = 10, the hand weight of `death.cause`. An anchor's score is
`10 x (its per-unit change) / (Finger of Death's per-recipient change)`, per context and pooled.
The pooled score is the ratio of the per-unit changes summed over the six contexts, so a context
where the result is more sensitive to anything (small games) counts for more. Intervals are
percentile intervals from resampling seeds within each context (every anchor of a context is
resampled with the same seeds as the baseline and the reference, so their correlation is kept).

**What an anchor calibrates** (`Anchor.calibrates`, read by `sim/policies/calibration.py`):
`kind.X` a `KIND_WEIGHT`, `state.X` a `STATE_WEIGHT` (a 30 s application), `special.X` a
`SPECIAL_WEIGHT`, `equipment.X` an `EQUIPMENT_WEIGHT`, `scalar.X` a per-unit number (a point of
armor, a second of Charge), `factor.X` a ratio to what the valuation would say compositionally
(computed when value.py loads). Where the gift is an ability with other effects too (Raise Dead's
heal and drawbacks, Force Bolt's Armor Breaking), the other effects are taken at their hand
weights and subtracted (`residual`).

**Map flags.** Phase 1 has no map, so an anchor whose value comes from position is undervalued
here. Each anchor carries a flag: `fair`, `may-overstate` (melee wins more games than it would with
room to kite, so melee anchors may read high), `may-understate` (the calibrated weight is used
only above the hand weight: a floor) or `needs-map` (the measurement is kept for the record, the
hand weight is used). See `MAP_FLAGS`.

The games are played with the hand weights (`SIM_CALIBRATION=off`), so the measurement doesn't
depend on an earlier calibration.
"""
from __future__ import annotations

import os

os.environ["SIM_CALIBRATION"] = "off"     # measure under the hand weights (see the docstring)

import argparse                            # noqa: E402
import gzip                                # noqa: E402
import json                                # noqa: E402
import math                                # noqa: E402
import time                                # noqa: E402
from collections import Counter            # noqa: E402
from dataclasses import dataclass, field   # noqa: E402
from multiprocessing import Pool           # noqa: E402

import numpy as np                         # noqa: E402

from sim.paths import DATA, OUT            # noqa: E402

CALIBRATION_JSON = DATA / "value-calibration.json"
RAW_JSON = OUT / "calibration-raw.json.gz"     # every pair's results, for --from-raw
SHARE = 0.5
REFERENCE = "kill"
REFERENCE_SCORE = 10.0
STATE_SECONDS = 30
STATE_WINDOW = 300      # a State lands at a uniform time in the first 5 minutes after pregame prep
BOOT = 2000

# name -> (preset, game type, games). Game counts balance cost against precision: small games
# run ~160/s on 10 cores, mixed 23-38/s, large 7-13/s.
CONTEXTS = {
    "small-annihilation": ("small", "annihilation", 6000),
    "small-attrition": ("small", "attrition", 4500),
    "mixed-annihilation": ("mixed", "annihilation", 2250),
    "mixed-attrition": ("mixed", "attrition", 1500),
    "large-annihilation": ("large", "annihilation", 900),
    "large-attrition": ("large", "attrition", 450),
}
GAMES_PER_SECOND = {"small-annihilation": 160, "small-attrition": 90, "mixed-annihilation": 38,
                    "mixed-attrition": 23, "large-annihilation": 13.5, "large-attrition": 6.9}

MAP_FLAGS = {
    "fair": "Nothing positional drives this anchor's value; the measurement stands.",
    "may-overstate": "Wins melee. Without a map melee decides most games (casters can't keep distance "
                     "or kite), so this may read high against ranged and control anchors. Used as measured.",
    "may-understate": "Part of the value is positional and Phase 1 has no space, so the calibrated "
                      "weight is used only above the hand weight (a floor).",
    "needs-map": "The engine gives this no effect without a map; the measurement is recorded but the "
                 "hand weight is used (uncalibrated, needs map).",
}


@dataclass(frozen=True)
class Anchor:
    name: str
    gift: dict
    unit: str                    # what one unit is
    calibrates: str | None       # "table.key" (module docstring), None for a check only
    map: str = "fair"
    why: str = ""
    per_recipient: float = 1.0   # units per gift log entry (3 for three points of armor)
    realized: str | None = None  # units counted in play instead: an `applied` key "slug|kind"
    residual_of: str | None = None   # ability whose other effects are subtracted (hand weights)


def _ab(slug, freq="1/Life", **kw):
    return {"kind": "ability", "slug": slug, "frequency": freq, **kw}


ANCHORS: tuple[Anchor, ...] = (
    Anchor("kill", _ab("finger-of-death"), "a use of Finger of Death per life", "kind.death.cause",
           why="The reference: 20' range is a probability, and a kill is a kill."),
    Anchor("armor", {"kind": "armor", "points": 1, "who": "fighter"}, "a point of armor on every location",
           "scalar.armor_point", "may-overstate", "Worn armor only matters in melee and against arrows."),
    Anchor("armor-3-bare", {"kind": "armor", "points": 3, "who": "fighter", "bare": True},
           "a point of armor, 0 to 3 for a fighter wearing none", "scalar.armor_loss_point",
           "may-overstate", "What Berserker's 'may not wear armor' takes from a Barbarian in 3 points.",
           per_recipient=3.0),
    Anchor("magic-armor", {"kind": "magic-armor", "points": 1, "who": "fighter"},
           "Magic Armor 1 on a fighter, every life", "scalar.magic_armor_point", "may-overstate",
           "Like worn armor; it goes to front-line fighters in play."),
    Anchor("shield-small", {"kind": "shield", "size": "small"}, "a small shield", "equipment.small-shield",
           "may-overstate", "Blocks blows in melee only."),
    Anchor("shield-medium", {"kind": "shield", "size": "medium"}, "a medium shield", "equipment.medium-shield",
           "may-overstate", "Blocks blows in melee only."),
    Anchor("shield-large", {"kind": "shield", "size": "large"}, "a large shield", "equipment.large-shield",
           "may-overstate", "Blocks blows in melee only."),
    Anchor("heal", _ab("heal"), "a Heal per life", "kind.wound.heal",
           why="Touch range and standing behind the line are probabilities; the policy heals out of melee."),
    Anchor("heal-fighter", _ab("heal", who="fighter"), "a Heal per life held by a fighter",
           "scalar.fighter_heal",
           why="A Heal's value to a fighter, by how fighters use it (step back and heal when not attacked)."),
    Anchor("revive", _ab("raise-dead", "1/Refresh"), "a Raise Dead per refresh (per game in annihilation)",
           "kind.life.revive", residual_of="raise-dead",
           why="Reaching the body is a probability; Raise Dead's heal and drawbacks are subtracted."),
    Anchor("death-ward", {"kind": "death-ward"}, "one death prevented per life (Phoenix Tears' way)",
           "kind.death.prevent", residual_of="gift-death-ward"),
    Anchor("wound-ball", _ab("force-bolt"), "a Force Bolt per life", "kind.wound.inflict",
           residual_of="force-bolt", why="A thrown ball hits at a flat rate; its Armor Breaking is subtracted."),
    *(Anchor(f"state-{s}", {"kind": "state", "state": s, "seconds": STATE_SECONDS, "window": STATE_WINDOW},
             f"{s} for {STATE_SECONDS} s on a random enemy", f"state.{s}", flag, why)
      for s, flag, why in (
          ("stunned", "fair", "Can't act and is easy to hit: both modeled."),
          ("frozen", "may-understate", "Phase 1 counts the time out of the fight, not a lane or ground left open."),
          ("stopped", "needs-map", "Nothing stops a Stopped player closing to melee in Phase 1: no effect at all."),
          ("suppressed", "fair", "No casting: modeled."),
          ("fragile", "fair", "Dies on the next wound: modeled."),
          ("insubstantial", "may-understate", "Out of the fight for the time; a map would add where they are."))),
    Anchor("armor-breaking", {"kind": "weapon-special", "effect": "armor-breaking", "who": "fighter"},
           "Armor Breaking on a fighter's weapon, every life", "special.armor-breaking", "may-overstate",
           "A melee special."),
    Anchor("wounds-kill", {"kind": "weapon-special", "effect": "wounds-kill", "who": "fighter"},
           "Wounds Kill on a fighter's weapon, every life", "special.wounds-kill", "may-overstate",
           "A melee special."),
    Anchor("free-charge", {"kind": "free-charge"}, "an instant Charge of a spent chargeable ability",
           "factor.refill_factor", realized="gift-free-charge|ability.charge",
           why="Per Charge actually made; compared with what value.py says a refill is worth."),
    Anchor("charge-time", {"kind": "charge-time", "seconds": 8}, "a second of Charge incantation saved",
           "scalar.charge_second", "may-understate",
           "Per second actually saved. With a map a player Charges behind the line; Phase 1 lets fighters "
           "Charge only in a lull.", realized="gift-charge-time|seconds-saved"),
    Anchor("extra-slot", {"kind": "extra-slot", "who": "fighter"}, "an extra Enchantment slot on a fighter",
           "factor.stack_share",
           why="Teammates fill it; compared with the whole value of the Enchantment that fills it."),
)
BY_NAME = {a.name: a for a in ANCHORS}


# ---------------------------------------------------------------- playing

_RULES = None


def _rules():
    global _RULES
    if _RULES is None:
        from sim.rules.compile import default_rules
        _RULES = default_rules()
    return _RULES


def context_config(ctx: str) -> dict:
    from sim.scenarios import load_config
    preset, gt, _ = CONTEXTS[ctx]
    cfg = load_config(preset)
    cfg["game_types"] = {gt: 1.0}
    return cfg


def gift_of(anchor: Anchor) -> dict:
    return {"team": 0, "share": SHARE, **anchor.gift}


def play_job(job: tuple) -> tuple:
    """(context, anchor name or '', seed) -> (context, anchor, seed, team-0 result, units, roles)."""
    from sim.engine.game import Game
    from sim.scenarios import generate
    ctx, name, seed = job
    rules = _rules()
    sc = generate(seed, context_config(ctx), rules)
    anchor = BY_NAME.get(name)
    if anchor is not None:
        sc["gifts"] = [gift_of(anchor)]
    g = Game(rules, sc, seed)
    res = g.run()
    w = res["winner"]
    result = 0.5 if w == -1 else float(w == 0)
    units, roles = 0.0, {}
    if anchor is not None:
        if anchor.realized:
            slug, kind = anchor.realized.split("|")
            units = float(g.applied.get((slug, kind), 0))
        else:
            units = len(g.gift_log) * anchor.per_recipient
        roles = dict(Counter(e["role"] for e in g.gift_log if e["role"]))
    return ctx, name, seed, result, units, roles


def plan(contexts, anchors, scale: float, seed0: int) -> list[tuple]:
    jobs = []
    for ctx in contexts:
        n = max(20, int(CONTEXTS[ctx][2] * scale))
        for name in ("", *anchors):
            jobs.extend((ctx, name, s) for s in range(seed0, seed0 + n))
    # the slowest games first, so no long game is left for the end
    order = {c: i for i, c in enumerate(sorted(CONTEXTS, key=lambda c: GAMES_PER_SECOND[c]))}
    return sorted(jobs, key=lambda j: (order[j[0]], j[1], j[2]))


def estimate_seconds(contexts, anchors, scale: float, workers: int = 10) -> float:
    per = sum(max(20, int(CONTEXTS[c][2] * scale)) * (1 + len(anchors)) / GAMES_PER_SECOND[c] for c in contexts)
    return per * 10 / max(1, workers)


def run(contexts, anchors, scale: float = 1.0, seed0: int = 1, workers: int | None = None,
        progress=print) -> dict:
    """Play every (context, baseline or anchor, seed); returns {(ctx, anchor): {seed: (result, units, roles)}}."""
    jobs = plan(contexts, anchors, scale, seed0)
    out: dict = {}
    workers = workers or os.cpu_count() or 1
    t0, done, step = time.perf_counter(), 0, max(1, len(jobs) // 20)
    if workers == 1:
        it = map(play_job, jobs)
        pool = None
    else:
        pool = Pool(workers)
        it = pool.imap_unordered(play_job, jobs, chunksize=4)
    try:
        for ctx, name, seed, result, units, roles in it:
            out.setdefault((ctx, name), {})[seed] = (result, units, roles)
            done += 1
            if progress and done % step == 0:
                progress(f"  {done}/{len(jobs)} games, {time.perf_counter() - t0:.0f} s")
    finally:
        if pool is not None:
            pool.close()
            pool.join()
    return out


def save_raw(raw: dict, path, meta: dict) -> None:
    rows = [[ctx, name, seed, *v] for (ctx, name), got in sorted(raw.items()) for seed, v in sorted(got.items())]
    with gzip.open(path, "wt") as fh:
        json.dump({"meta": meta, "rows": rows}, fh)


def load_raw(path) -> tuple[dict, dict]:
    with gzip.open(path, "rt") as fh:
        doc = json.load(fh)
    raw: dict = {}
    for ctx, name, seed, result, units, roles in doc["rows"]:
        raw.setdefault((ctx, name), {})[seed] = (result, units, roles)
    return raw, doc["meta"]


# ---------------------------------------------------------------- summarizing

def _ci(samples: np.ndarray) -> tuple[float, float]:
    s = samples[np.isfinite(samples)]
    if len(s) == 0:
        return (float("nan"), float("nan"))
    return float(np.quantile(s, 0.025)), float(np.quantile(s, 0.975))


def summarize(raw: dict, contexts, anchors, boot: int = BOOT, seed: int = 0) -> dict:
    """Per anchor: per context and pooled per-unit change with bootstrap intervals, and the score."""
    rng = np.random.default_rng(seed)
    per_ctx: dict = {}
    boots: dict = {}          # (ctx, anchor) -> per-unit change per bootstrap resample
    for ctx in contexts:
        base = raw[(ctx, "")]
        seeds = sorted(base)
        n = len(seeds)
        idx = rng.integers(0, n, size=(boot, n))
        b = np.array([base[s][0] for s in seeds])
        for name in anchors:
            got = raw[(ctx, name)]
            v = np.array([got[s][0] for s in seeds])
            u = np.array([got[s][1] for s in seeds])
            d = v - b
            mu = u.mean()
            pu = d.mean() / mu if mu > 0 else float("nan")
            dsum, usum = d[idx].mean(axis=1), u[idx].mean(axis=1)
            with np.errstate(divide="ignore", invalid="ignore"):
                pub = np.where(usum > 0, dsum / usum, np.nan)
            boots[(ctx, name)] = pub
            se = d.std(ddof=1) / math.sqrt(n) if n > 1 else float("nan")
            roles = Counter()
            for s in seeds:
                roles.update(got[s][2])
            per_ctx[(ctx, name)] = {
                "pairs": n, "flips": float(np.mean(d != 0)), "units_per_game": float(mu),
                "dwin": float(d.mean()), "dwin_lo": float(d.mean() - 1.96 * se), "dwin_hi": float(d.mean() + 1.96 * se),
                "per_unit": float(pu), **dict(zip(("per_unit_lo", "per_unit_hi"), _ci(pub))),
                "roles": dict(sorted(roles.items())),
            }
    out = {}
    for name in anchors:
        entry = {"per_context": {}}
        for ctx in contexts:
            row = dict(per_ctx[(ctx, name)])
            if REFERENCE in anchors:
                ref, refb = per_ctx[(ctx, REFERENCE)]["per_unit"], boots[(ctx, REFERENCE)]
                with np.errstate(divide="ignore", invalid="ignore"):
                    sb = REFERENCE_SCORE * boots[(ctx, name)] / refb
                row["score"] = REFERENCE_SCORE * row["per_unit"] / ref if ref else float("nan")
                row["score_lo"], row["score_hi"] = _ci(sb)
            entry["per_context"][ctx] = row
        pus = np.array([per_ctx[(c, name)]["per_unit"] for c in contexts])
        pub = np.nanmean(np.array([boots[(c, name)] for c in contexts]), axis=0)
        pooled = {"per_unit": float(np.nanmean(pus)), **dict(zip(("per_unit_lo", "per_unit_hi"), _ci(pub)))}
        if REFERENCE in anchors:
            ref_sum = sum(per_ctx[(c, REFERENCE)]["per_unit"] for c in contexts)
            ref_b = np.sum([boots[(c, REFERENCE)] for c in contexts], axis=0)
            a_b = np.sum([np.nan_to_num(boots[(c, name)]) for c in contexts], axis=0)
            pooled["score"] = REFERENCE_SCORE * float(np.nansum(pus)) / ref_sum
            pooled["score_lo"], pooled["score_hi"] = _ci(REFERENCE_SCORE * a_b / ref_b)
        roles = Counter()
        for c in contexts:
            roles.update(per_ctx[(c, name)]["roles"])
        pooled["roles"] = dict(sorted(roles.items()))
        entry["pooled"] = pooled
        out[name] = entry
    return out


def calibration_fingerprint() -> dict:
    from sim.policies import calibration
    return calibration.fingerprint()


def _hand() -> dict:
    from sim.policies import value
    return value.HAND


def residual(anchor: Anchor) -> float:
    """The hand-weight value of the gift ability's effects other than the one calibrated
    (benefits minus drawbacks, for a fighter so no role multiplier applies)."""
    if anchor.residual_of is None:
        return 0.0
    from sim.engine.gifts import death_ward_ability
    from sim.policies import value
    from sim.rules.compile import build_rules
    rules = build_rules()
    ab = death_ward_ability(rules) if anchor.residual_of == "gift-death-ward" else rules.abilities[anchor.residual_of]
    kind = anchor.calibrates.split(".", 1)[1]
    with value.hand_weights():
        parts = value.breakdown(ab, "fighter", rules=rules)
        kinds = {e.id: e.kind for e in ab.effects}
        return float(sum(c for i, _, c in parts if kinds.get(i) != kind))


def assemble(summary: dict, contexts, anchors, meta: dict, fingerprint: dict | None = None) -> dict:
    """The calibration document. `fingerprint`: what the games were played under (default: now)."""
    from sim.policies import calibration
    doc = {
        "about": "Measured value of the usefulness score's anchor weights (sim/analyze/calibrate.py). "
                 "Each anchor is given to team 0 and the change in its result is measured against the "
                 "same seeds without it; value.py derives its weights from this file "
                 "(sim/policies/calibration.py).",
        "date": time.strftime("%Y-%m-%d"),
        "fingerprint": fingerprint or calibration.fingerprint(),
        "valuation_during_measurement": "hand weights (SIM_CALIBRATION=off)",
        "reference": {"anchor": REFERENCE, "score": REFERENCE_SCORE, "weight": "kind.death.cause"},
        "recipients": f"{SHARE:.0%} of the eligible players of team 0, rounded up, at least one "
                      "(a State: that many applications on random enemies); changes are per unit",
        "result": "team 0: win 1, draw 0.5, loss 0; paired by seed",
        "map_flags": MAP_FLAGS,
        "contexts": {c: {"preset": CONTEXTS[c][0], "game_type": CONTEXTS[c][1],
                         "games": summary[anchors[0]]["per_context"][c]["pairs"]} for c in contexts},
        **meta,
        "anchors": {},
    }
    for name in anchors:
        a = BY_NAME[name]
        s = summary[name]
        res = residual(a)
        pooled = s["pooled"]
        w = None
        if a.calibrates and "score" in pooled:
            w = {"value": pooled["score"] - res, "lo": pooled["score_lo"] - res, "hi": pooled["score_hi"] - res}
        doc["anchors"][name] = {
            "gift": gift_of(a), "unit": a.unit, "calibrates": a.calibrates, "map": a.map, "why": a.why,
            "residual": res, "weight": w, "pooled": pooled, "per_context": s["per_context"],
        }
    return doc


# ---------------------------------------------------------------- reporting

def table(doc: dict) -> str:
    ctxs = list(doc["contexts"])
    head = f"{'anchor':16s} {'map':14s} {'per unit, pooled [95%]':30s} {'score [95%]':24s} " + \
        " ".join(f"{c[:11]:>11s}" for c in ctxs)
    rows = [head]
    for name, a in doc["anchors"].items():
        p = a["pooled"]
        pu = f"{p['per_unit']:+.4f} [{p['per_unit_lo']:+.4f}, {p['per_unit_hi']:+.4f}]"
        sc = f"{p.get('score', float('nan')):6.2f} [{p.get('score_lo', float('nan')):6.2f}, {p.get('score_hi', float('nan')):6.2f}]"
        per = " ".join(f"{a['per_context'][c].get('score', float('nan')):11.2f}" for c in ctxs)
        rows.append(f"{name:16s} {a['map']:14s} {pu:30s} {sc:24s} {per}")
    return "\n".join(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--contexts", default="", help="comma-separated (default: all six)")
    ap.add_argument("--anchors", default="", help="comma-separated (default: all; the reference is always run)")
    ap.add_argument("--scale", type=float, default=1.0, help="multiply every context's game count")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--out", default=str(CALIBRATION_JSON))
    ap.add_argument("--raw", default=str(RAW_JSON), help="where the per-pair results are saved")
    ap.add_argument("--from-raw", action="store_true",
                    help="summarize the saved per-pair results (--raw) again instead of playing")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--report", default="", help="print the table of an existing calibration file and exit")
    ap.add_argument("--weights", action="store_true",
                    help="print every weight value.py uses (hand, in use, source) with SIM_CALIBRATION=on and exit")
    args = ap.parse_args(argv)
    if args.weights:
        from sim.policies import calibration
        print(calibration.describe(calibration.tables(_hand(), calibration.load(how="on"))))
        return 0
    if args.report:
        print(table(json.loads(open(args.report).read())))
        return 0
    contexts = [c for c in args.contexts.split(",") if c] or list(CONTEXTS)
    anchors = [a for a in args.anchors.split(",") if a] or [a.name for a in ANCHORS]
    bad = [c for c in contexts if c not in CONTEXTS] + [a for a in anchors if a not in BY_NAME]
    if bad:
        ap.error(f"unknown: {', '.join(bad)}")
    if REFERENCE not in anchors:
        anchors = [REFERENCE, *anchors]
    if args.from_raw:
        raw, meta = load_raw(args.raw)
        contexts = [c for c in contexts if (c, "") in raw]
        anchors = [a for a in anchors if all((c, a) in raw for c in contexts)]
    else:
        est = estimate_seconds(contexts, anchors, args.scale, args.workers or os.cpu_count() or 1)
        games = sum(max(20, int(CONTEXTS[c][2] * args.scale)) for c in contexts) * (1 + len(anchors))
        print(f"{len(anchors)} anchors x {len(contexts)} contexts: {games} games, about {est / 60:.0f} min")
        if args.dry_run:
            return 0
        t0 = time.perf_counter()
        raw = run(contexts, anchors, args.scale, args.seed, args.workers or None)
        wall = time.perf_counter() - t0
        from sim.policies import calibration
        meta = {"seed": args.seed, "scale": args.scale, "wall_seconds": round(wall), "games": games,
                "fingerprint": calibration.fingerprint()}
        OUT.mkdir(parents=True, exist_ok=True)
        save_raw(raw, args.raw, meta)
    games, wall = meta["games"], meta["wall_seconds"]
    summary = summarize(raw, contexts, anchors)
    doc = assemble(summary, contexts, anchors, {k: meta[k] for k in ("seed", "scale", "wall_seconds", "games")},
                   meta.get("fingerprint"))
    with open(args.out, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=False)
        fh.write("\n")
    print(table(doc))
    print(f"\nwrote {args.out} ({games} games in {wall / 60:.1f} min)")
    if doc["fingerprint"] != calibration_fingerprint():
        print("warning: the games were played under another fingerprint than the current one: the file is stale")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
