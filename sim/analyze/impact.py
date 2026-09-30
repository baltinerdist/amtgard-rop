"""How much does removing (or merging) abilities change the game? Paired over seeds.

`compare(base, variant, removed)` takes two lists of game results over the **same seeds** (from
sim.run.run_games) and measures six things, each as a signed, dimensionless *component*:

| component     | measure (per run)                                       | standardised by                      |
| ------------- | ------------------------------------------------------- | ------------------------------------ |
| holder_win    | holder team's result, variant - base (win 1, draw .5)   | 0.5 (the sd of a fair coin)          |
| duration      | mean game length, seconds                               | baseline sd of game length           |
| time_dead     | mean share of player-time spent dead                    | baseline sd of that share over games |
| kills         | mean kills per player per game                          | baseline sd over games               |
| class_spread  | sd across classes of class win rates (decisive games)   | the baseline class spread            |
| use_mix       | total variation distance between the ability-use mixes  | none (already 0..1)                  |

The holder team is the team that started with more copies of the removed abilities (games where
the teams hold equally many are left out of holder_win). use_mix is the share of all casts that
would have to move for the two cast distributions to match, so it includes the removed abilities'
own casts disappearing: an ability nobody uses scores ~0, a staple scores its share of casts.

**Gameplay change distance** D is the weighted root-mean-square of the components:

    D = sqrt( sum_k W_k * c_k^2 / sum_k W_k )        W = DISTANCE_WEIGHTS below

so D = 0.1 reads as "on average each measure moved a tenth of its typical spread". Every
component (and D) gets a 95% **paired bootstrap** interval: seeds are resampled with replacement
and the base and variant game of a seed always travel together. The holder_win delta also gets a
normal interval over the seed pairs (`holder_win_delta`).

Point estimates of |c_k| are biased upward by noise, so the output also has `noise` (the D you
would expect from sampling noise alone, sqrt(sum W_k var_boot(c_k) / sum W_k)) and
`distance_adj` = sqrt(max(0, D^2 - noise^2)), the bias-corrected distance the cut ranking uses.
"""
from __future__ import annotations

import math

import numpy as np

from sim.analyze.stats import bootstrap_weights, paired_ci, percentile_ci

# weight of each component in the distance D; edit here (0 drops a component from D)
DISTANCE_WEIGHTS: dict[str, float] = {
    "holder_win": 1.0,
    "duration": 1.0,
    "time_dead": 1.0,
    "kills": 1.0,
    "class_spread": 1.0,
    "use_mix": 1.0,
}
COMPONENTS = tuple(DISTANCE_WEIGHTS)
N_BOOT = 400


def _score(res: dict, team: int) -> float:
    return 0.5 if res["winner"] == -1 else float(res["winner"] == team)


def holder_team(res: dict, removed) -> int | None:
    """Team that started with the most copies of the removed abilities, or None (tie / nobody)."""
    totals = None
    for slug in removed:
        held = res["holdings"].get(slug)
        if held:
            totals = list(held) if totals is None else [a + b for a, b in zip(totals, held)]
    if not totals or sum(totals) == 0:
        return None
    top = max(totals)
    return None if totals.count(top) > 1 else totals.index(top)


def _game_arrays(results: list[dict], classes: list[str], slugs: list[str]) -> dict:
    ci = {c: i for i, c in enumerate(classes)}
    si = {s: i for i, s in enumerate(slugs)}
    g = len(results)
    dur, dead, kills = np.zeros(g), np.zeros(g), np.zeros(g)
    wins, n = np.zeros((g, len(classes))), np.zeros((g, len(classes)))
    casts = np.zeros((g, len(slugs)))
    for k, r in enumerate(results):
        ps = r["players"]
        dur[k] = r["duration"]
        dead[k] = sum(p["time_dead"] for p in ps) / (len(ps) * r["duration"]) if ps and r["duration"] else 0.0
        kills[k] = sum(p["kills"] for p in ps) / len(ps) if ps else 0.0
        if r["winner"] >= 0:
            for p in ps:
                n[k, ci[p["cls"]]] += 1
                wins[k, ci[p["cls"]]] += p["won"]
        for s, c in r["casts"].items():
            casts[k, si[s]] += c
    return {"duration": dur, "time_dead": dead, "kills": kills, "wins": wins, "n": n, "casts": casts}


def _wmean(wt: np.ndarray, x: np.ndarray) -> np.ndarray:
    return (wt @ x) / wt.sum(axis=1)


def _class_spread(wt: np.ndarray, wins: np.ndarray, n: np.ndarray, valid: np.ndarray) -> np.ndarray:
    tot = wt @ n
    with np.errstate(invalid="ignore", divide="ignore"):
        rate = (wt @ wins) / tot
    rate = np.where(valid & (tot > 0), rate, np.nan)
    with np.errstate(invalid="ignore"):
        return np.nanstd(rate, axis=1)


def _mix(wt: np.ndarray, casts: np.ndarray) -> np.ndarray:
    tot = (wt @ casts)
    s = tot.sum(axis=1, keepdims=True)
    return np.divide(tot, s, out=np.zeros_like(tot), where=s > 0)


def compare(base: list[dict], variant: list[dict], removed, n_boot: int = N_BOOT, boot_seed: int = 0,
            weights: dict[str, float] | None = None) -> dict:
    """Paired comparison of `variant` against `base` (same seeds, same order). See module doc."""
    weights = DISTANCE_WEIGHTS if weights is None else weights
    removed = sorted(set(removed))
    if len(base) != len(variant) or any(b["seed"] != v["seed"] for b, v in zip(base, variant)):
        raise ValueError("base and variant must cover the same seeds in the same order")
    g = len(base)
    classes = sorted({p["cls"] for r in (*base, *variant) for p in r["players"]})
    slugs = sorted({s for r in (*base, *variant) for s in r["casts"]})
    ab, av = _game_arrays(base, classes, slugs), _game_arrays(variant, classes, slugs)

    # holder team per seed (from the baseline's starting holdings)
    h_base, h_var, mask, casts_present, present = [], [], np.zeros(g, bool), [], 0
    for k, (b, v) in enumerate(zip(base, variant)):
        if any(sum(b["holdings"].get(s, ())) for s in removed):
            present += 1
            casts_present.append(sum(b["casts"].get(s, 0) for s in removed))
        team = holder_team(b, removed)
        if team is not None:
            mask[k] = True
            h_base.append(_score(b, team))
            h_var.append(_score(v, team))
    h = np.zeros(g)
    h[mask] = np.array(h_var) - np.array(h_base)

    wt = np.vstack([np.ones((1, g)), bootstrap_weights(g, n_boot, boot_seed)]) if g > 1 else np.ones((1, g))
    comps: dict[str, np.ndarray] = {}
    measures: dict[str, dict] = {}

    def record(name, base_v, var_v, comp):
        comps[name] = comp
        delta = var_v - base_v
        lo, hi = percentile_ci(delta[1:])
        clo, chi = percentile_ci(comp[1:])
        measures[name] = {"base": float(base_v[0]), "variant": float(var_v[0]), "delta": float(delta[0]),
                          "lo": lo, "hi": hi, "component": float(comp[0]), "c_lo": clo, "c_hi": chi}

    for name in ("duration", "time_dead", "kills"):
        sd = float(np.std(ab[name], ddof=1)) if g > 1 else 0.0
        mb, mv = _wmean(wt, ab[name]), _wmean(wt, av[name])
        record(name, mb, mv, (mv - mb) / sd if sd > 0 else np.zeros_like(mb))

    valid = (ab["n"].sum(axis=0) > 0) & (av["n"].sum(axis=0) > 0)
    sb = _class_spread(wt, ab["wins"], ab["n"], valid)
    sv = _class_spread(wt, av["wins"], av["n"], valid)
    ref = sb[0] if sb[0] > 0 else float("nan")
    record("class_spread", sb, sv, (sv - sb) / ref if ref == ref else np.zeros_like(sb))

    mix_b, mix_v = _mix(wt, ab["casts"]), _mix(wt, av["casts"])
    tvd = 0.5 * np.abs(mix_v - mix_b).sum(axis=1)
    record("use_mix", np.zeros_like(tvd), tvd, tvd)

    if mask.any():
        wm = wt[:, mask]
        hw = (wm @ h[mask]) / np.maximum(wm.sum(axis=1), 1e-12)
        hw = np.where(wm.sum(axis=1) > 0, hw, np.nan)
        hb = (wm @ np.array(h_base)) / np.maximum(wm.sum(axis=1), 1e-12)
        record("holder_win", hb, hb + hw, hw / 0.5)
    else:
        nan = np.full(wt.shape[0], np.nan)
        record("holder_win", nan, nan, nan)

    wsum = sum(weights.get(k, 0.0) for k in COMPONENTS) or 1.0
    sq = sum(weights.get(k, 0.0) * np.nan_to_num(comps[k]) ** 2 for k in COMPONENTS)
    dist = np.sqrt(sq / wsum)
    noise2 = 0.0
    for k in COMPONENTS:
        boots = comps[k][1:]
        if len(boots) > 1 and np.isfinite(boots).any():
            noise2 += weights.get(k, 0.0) * float(np.nanvar(boots))
    noise2 /= wsum
    d_lo, d_hi = percentile_ci(dist[1:])
    hold = paired_ci(h_base, h_var)
    return {
        "removed": removed,
        "games": g,
        "games_present": present,
        "games_with_holder": int(mask.sum()),
        "casts_per_game_present": (sum(casts_present) / len(casts_present)) if casts_present else 0.0,
        "holder_win_delta": hold["est"], "holder_ci_low": hold["lo"], "holder_ci_high": hold["hi"],
        "distance": float(dist[0]), "distance_lo": d_lo, "distance_hi": d_hi,
        "noise": math.sqrt(noise2), "distance_adj": math.sqrt(max(0.0, float(dist[0]) ** 2 - noise2)),
        "measures": measures,
    }


def run_summary(results: list[dict]) -> dict:
    """Coverage-relevant totals for a set of games: no-op rate, draws, mean length."""
    applied = sum(sum(r["applied"].values()) for r in results)
    noops = sum(sum(r["noops"].values()) for r in results)
    casts = sum(sum(r["casts"].values()) for r in results)
    noop_slugs: dict[str, int] = {}
    for r in results:
        for key, n in r["noops"].items():
            slug = key.split("|", 1)[0]
            noop_slugs[slug] = noop_slugs.get(slug, 0) + n
    g = len(results) or 1
    return {
        "games": len(results),
        "draws": sum(1 for r in results if r["winner"] == -1),
        "mean_seconds": sum(r["duration"] for r in results) / g,
        "casts_per_game": casts / g,
        "effects_applied": applied, "effects_noop": noops,
        "noop_rate": noops / (applied + noops) if applied + noops else 0.0,
        "top_noop_abilities": sorted(noop_slugs.items(), key=lambda kv: -kv[1])[:10],
    }


def flat(row: dict) -> dict:
    """compare() output flattened to one CSV-friendly dict."""
    out = {k: v for k, v in row.items() if k != "measures"}
    out["removed"] = ",".join(row["removed"])
    for name, m in row["measures"].items():
        for k, v in m.items():
            out[f"{name}_{k}"] = v
    return out
