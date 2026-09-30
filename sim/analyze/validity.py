"""Face-validity suite: statistical scenarios a veteran Amtgard player would call obviously true.

    .venv/bin/python -m sim.analyze.validity                  # all checks, pass/fail table
    .venv/bin/python -m sim.analyze.validity --only mirror,skill --scale 2

Every check uses fixed seeds, so a result replays exactly. Each check states its tolerance: a
check fails only when the model is clearly on the wrong side of the expectation, not on noise.
Rosters are built directly (not by sim.scenarios) so each check controls exactly what differs
between the two sides. Where fairness matters, the two teams are mirror images: the same
classes, levels and skills.

A failing check means an assumption or a policy is implausible, or the model is missing
something (see `known_limit` on a check). It does not mean the check should be tuned to pass.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from dataclasses import dataclass, field
from multiprocessing import Pool
from typing import Callable

from sim.engine.game import Game
from sim.engine.state import LOCATIONS
from sim.paths import ASSUMPTIONS_JSON
from sim.rules.compile import Rules, build_rules

GAME_TYPES = {
    "annihilation": {"game_type": "annihilation", "lives": 4, "respawn_seconds": 150, "refresh_seconds": None,
                     "max_seconds": 1800},
    "attrition": {"game_type": "attrition", "lives": None, "respawn_seconds": 60, "refresh_seconds": 900,
                  "max_seconds": 1200},
}
FIGHTERS = ("Anti-Paladin", "Barbarian", "Paladin", "Warrior")
CASTERS = ("Bard", "Druid", "Healer", "Wizard")
CONTROL_STATES = {"stunned", "frozen", "stopped", "suppressed", "fragile", "insubstantial"}
CONTROL_MOVES = {"move.to-base", "move.push", "move.keep-away", "move.to-location", "move.to-caster"}

_RULES: Rules | None = None
_OVERRIDES: dict = {}


def _set_overrides(overrides: dict) -> None:
    """Assumption overrides ("group.name" -> value) for sensitivity runs; also a Pool initializer."""
    global _OVERRIDES, _RULES
    _OVERRIDES, _RULES = dict(overrides), None


def _rules() -> Rules:
    global _RULES
    if _RULES is None:
        a = json.loads(ASSUMPTIONS_JSON.read_text())
        for key, v in _OVERRIDES.items():
            group, name = key.split(".", 1)
            a[group][name]["value"] = v
        _RULES = build_rules(assumptions=a)
    return _RULES


# ------------------------------------------------------------------ rosters and one game

def roster(rng: random.Random, n: int, classes=None, levels=None, skill_sd: float = 1.0) -> list[dict]:
    """n players; classes and levels drawn uniformly from the given tuples (default: all, 1-6)."""
    classes = classes or tuple(sorted(_rules().classes))
    levels = levels or (1, 2, 3, 4, 5, 6)
    return [{"cls": rng.choice(classes), "level": rng.choice(levels), "skill": rng.gauss(0.0, skill_sd)}
            for _ in range(n)]


def shifted(team: list[dict], **changes) -> list[dict]:
    """A copy of a team with fields replaced or (for skill) shifted: shifted(t, skill=+1.0)."""
    out = []
    for pl in team:
        q = dict(pl)
        for k, v in changes.items():
            q[k] = q[k] + v if k == "skill" else v
        out.append(q)
    return out


def scenario(team0: list[dict], team1: list[dict], game_type: str = "annihilation", **over) -> dict:
    return {**GAME_TYPES[game_type], **over, "teams": [team0, team1]}


def control_slugs(rules: Rules) -> frozenset:
    """Abilities that disable or displace an enemy: harmful States and forced movement."""
    out = set()
    for slug, ab in rules.abilities.items():
        for e in ab.effects:
            if e.subject not in ("target", "struck-player") or e.polarity != "harm":
                continue
            if (e.kind == "state.apply" and e.params.get("state") in CONTROL_STATES) or e.kind in CONTROL_MOVES:
                out.add(slug)
    return frozenset(out)


def _apply_mod(g: Game, mod: str, team: int) -> None:
    rules = g.rules
    for p in g.players:
        if p.team != team:
            continue
        if mod == "no-armor":
            p.armor_max = 0
            p.armor = {l: 0 for l in LOCATIONS}
        elif mod == "full-armor":
            p.armor_max = max(p.armor_max, rules.classes[p.cls].armor or 0)
            p.armor = {l: p.armor_max for l in LOCATIONS}
        elif mod == "no-heal":
            for slug in [s for s, u in p.uses.items() if u.ability.effects_of("wound.heal")
                         and not u.ability.effects_of("life.revive")]:
                del p.uses[slug]
        elif mod == "no-control":
            for slug in control_slugs(rules) & set(p.uses):
                del p.uses[slug]
        else:
            raise ValueError(mod)


class _Watched(Game):
    """Counts policy behavior: heal starts on allies in melee or already being healed, and
    seconds spent incanting while under melee attack."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.heal_starts = self.heal_on_engaged = self.heal_dogpile = 0
        self.cast_seconds = self.cast_seconds_attacked = 0

    def start_cast(self, p, uses, target):
        heal = bool(uses.ability.effects_of("wound.heal")) and not uses.ability.effects_of("life.revive")
        if heal and target is not None and target is not p and p.casting is None and uses.available():
            engaged = target.target is not None or bool(self.attackers_of(target))
            dog = any(o.casting is not None and o.casting.target == target.pid and o.casting.uses is not None
                      and o.casting.uses.ability.effects_of("wound.heal") for o in self.players if o is not p)
        ok = super().start_cast(p, uses, target)
        if ok and heal and target is not None and target is not p:
            self.heal_starts += 1
            self.heal_on_engaged += engaged
            self.heal_dogpile += dog
        return ok

    def step(self):
        w = super().step()
        for p in self.players:
            if p.casting is not None and p.on_field(self.t):
                self.cast_seconds += 1
                if self.attackers_of(p):
                    self.cast_seconds_attacked += 1
        return w


def play_job(job: tuple) -> dict:
    """(seed, scenario, ablate, mods, watch) -> summary. mods: ((mod, team), ...)."""
    seed, sc, ablate, mods, watch = job
    rules = _rules()
    g = (_Watched if watch else Game)(rules, sc, seed, frozenset(ablate))
    for mod, team in mods:
        _apply_mod(g, mod, team)
    res = g.run()
    kills = [0, 0]
    archer_kills, archers = [0, 0], [0, 0]
    for pl in res["players"]:
        kills[pl["team"]] += pl["kills"]
        if pl["cls"] == "Archer":
            archer_kills[pl["team"]] += pl["kills"]
            archers[pl["team"]] += 1
    out = {"seed": seed, "winner": res["winner"], "duration": res["duration"], "kills": kills,
           "archer_kills": archer_kills, "archers": archers,
           "cls_won": [(pl["cls"], pl["won"]) for pl in res["players"]]}
    if watch:
        out.update(heal_starts=g.heal_starts, heal_on_engaged=g.heal_on_engaged, heal_dogpile=g.heal_dogpile,
                   cast_seconds=g.cast_seconds, cast_seconds_attacked=g.cast_seconds_attacked)
    return out


# ------------------------------------------------------------------ running and scoring

@dataclass
class Result:
    name: str
    passed: bool
    measured: str
    expected: str
    rationale: str
    known_limit: str = ""
    seconds: float = 0.0


@dataclass
class Check:
    name: str
    rationale: str
    fn: Callable[["Runner", int], tuple[bool, str, str]]
    games: int
    known_limit: str = ""        # set when a failure is a structural limit of Phase 1, not a bug


@dataclass
class Runner:
    workers: int | None = None
    _pool: object = field(default=None, repr=False)

    def play(self, jobs: list[tuple]) -> list[dict]:
        if self.workers == 1 or len(jobs) < 8:
            return [play_job(j) for j in jobs]
        if self._pool is None:
            self._pool = Pool(self.workers or os.cpu_count() or 1, _set_overrides, (_OVERRIDES,))
        n = self.workers or os.cpu_count() or 1
        return self._pool.map(play_job, jobs, chunksize=max(1, len(jobs) // (n * 6)))

    def close(self) -> None:
        if self._pool is not None:
            self._pool.close()
            self._pool.join()
            self._pool = None


def score(results: list[dict], team: int = 0) -> float:
    """Mean result for `team`: win 1, draw 0.5, loss 0."""
    return sum(0.5 if r["winner"] == -1 else float(r["winner"] == team) for r in results) / len(results)


def se(p: float, n: int) -> float:
    return math.sqrt(max(p * (1 - p), 0.01) / n)


def band(n: int, z: float = 3.0, floor: float = 0.03) -> float:
    """Half-width for "≈ 50%": three standard errors of a fair coin, at least 3 points."""
    return max(floor, z * 0.5 / math.sqrt(n))


def _mirror_jobs(n: int, seed0: int, size: tuple[int, int], game_types=("annihilation", "attrition"),
                 make=None, ablate=(), mods=(), watch=False, **over) -> list[tuple]:
    """n mirrored games; `make(rng, team)` returns (team0, team1) from a base team."""
    jobs = []
    for i in range(n):
        seed = seed0 + i
        rng = random.Random(f"validity:{seed0}:{i}")
        k = rng.randint(*size)
        base = roster(rng, k)
        t0, t1 = make(rng, base) if make else (base, [dict(p) for p in base])
        gt = game_types[i % len(game_types)]
        jobs.append((seed, scenario(t0, t1, gt, **over), tuple(ablate), tuple(mods), watch))
    return jobs


# ------------------------------------------------------------------ the checks

def c_mirror(run: Runner, n: int):
    res = run.play(_mirror_jobs(n, 1000, (5, 15)))
    p, b = score(res), band(n)
    return abs(p - 0.5) <= b, f"team 0 {p:.3f} (n={n})", f"0.5 ± {b:.3f}"


def c_mirror_seat_swap(run: Runner, n: int):
    """Same random (non-mirrored) rosters played twice with the team order swapped."""
    jobs = []
    for i in range(n // 2):
        rng = random.Random(f"validity:seat:{i}")
        k = rng.randint(5, 15)
        a, b = roster(rng, k), roster(rng, k)
        gt = ("annihilation", "attrition")[i % 2]
        jobs.append((2000 + i, scenario(a, b, gt), (), (), False))
        jobs.append((2000 + i, scenario(b, a, gt), (), (), False))
    res = run.play(jobs)
    # a's result in both seatings; if seating matters this drifts from the a-vs-b truth
    first = score(res[0::2], 0)
    second = score(res[1::2], 1)
    d = first - second
    lim = 3 * math.sqrt(0.5 / (n // 2))
    return abs(d) <= lim, f"same roster as team 0 vs team 1: {first:.3f} vs {second:.3f}", f"difference ≤ {lim:.3f}"


def c_skill(run: Runner, n: int):
    res = run.play(_mirror_jobs(n, 3000, (3, 6), ("annihilation",),
                                make=lambda rng, t: (shifted(t, skill=1.0), [dict(p) for p in t])))
    p = score(res)
    return p >= 0.75, f"+1 sd team {p:.3f} (6-12 players)", "≥ 0.75"


def _fighter_stack(rng, t):
    """Same seats, skills and levels; the second side swaps every class for a heavy-melee class."""
    return [dict(p) for p in t], [dict(p, cls=rng.choice(FIGHTERS)) for p in t]


def c_skill_vs_class(run: Runner, n: int):
    """A +1 sd team of ordinary mixed classes against an average team stacked with melee classes."""
    def skilled_mixed(rng, t):
        a, b = _fighter_stack(rng, t)
        return shifted(a, skill=1.0), b
    p = score(run.play(_mirror_jobs(n, 4000, (3, 6), ("annihilation",), make=skilled_mixed)))
    return p >= 0.5, f"+1 sd mixed team vs average fighter-stacked team {p:.3f}", "≥ 0.5"


def c_class_stack(run: Runner, n: int):
    stacked = 1.0 - score(run.play(_mirror_jobs(n, 4000, (3, 6), ("annihilation",), make=_fighter_stack)))
    return 0.5 <= stacked <= 0.8, f"fighter-stacked team vs mixed team, equal skill: {stacked:.3f}", "0.5 to 0.8"


def c_healer_added(run: Runner, n: int):
    def add_healer(rng, t):
        extra = {"cls": "Healer", "level": rng.choice((1, 2, 3, 4, 5, 6)), "skill": rng.gauss(0, 1)}
        return [dict(p) for p in t] + [extra], [dict(p) for p in t]
    res = run.play(_mirror_jobs(n, 5000, (5, 12), ("attrition",), make=add_healer))
    p = score(res)
    lim = 2 * se(0.5, n)
    return p >= 0.5 - lim, f"side with the added Healer {p:.3f}", f"≥ 0.5 - {lim:.3f}"


def c_heal_not_harmful(run: Runner, n: int):
    """Mirrored rosters that each include Healers; only team 1 loses its healing Verbals."""
    def with_healers(rng, t):
        t = [dict(p) for p in t]
        for i in rng.sample(range(len(t)), 2):
            t[i]["cls"] = "Healer"
        return t, [dict(p) for p in t]
    out = []
    for gt, seed0 in (("attrition", 6000), ("annihilation", 6500)):
        res = run.play(_mirror_jobs(n // 2, seed0, (5, 12), (gt,), make=with_healers, mods=(("no-heal", 1),)))
        out.append((gt, score(res)))
    lim = 2 * se(0.5, n // 2)
    ok = all(p >= 0.5 - lim for _, p in out)
    return ok, "; ".join(f"{gt}: with Heal {p:.3f}" for gt, p in out), f"each ≥ 0.5 - {lim:.3f}"


def c_archers_vs_armor(run: Runner, n: int):
    def archers(rng, t):
        a = [dict(p) for p in t]
        for i in range(min(3, len(a))):
            a[i]["cls"] = "Archer"
        return a, [dict(p) for p in t]
    jobs_bare = _mirror_jobs(n, 7000, (6, 12), make=archers, mods=(("no-armor", 1),))
    jobs_armored = _mirror_jobs(n, 7000, (6, 12), make=archers, mods=(("full-armor", 1),))
    bare, armored = run.play(jobs_bare), run.play(jobs_armored)
    kb = sum(r["archer_kills"][0] for r in bare) / sum(r["archers"][0] for r in bare)
    ka = sum(r["archer_kills"][0] for r in armored) / sum(r["archers"][0] for r in armored)
    return kb > ka * 1.1, f"kills per archer: vs unarmored {kb:.2f}, vs armored {ka:.2f}", \
        "unarmored > armored × 1.1"


def c_control_scales(run: Runner, n: int):
    """Value of control abilities (one side keeps them) in small vs large games."""
    vals = {}
    for label, size, seed0 in (("small (8-12)", (4, 6), 8000), ("large (50-70)", (25, 35), 8500)):
        m = n if label.startswith("small") else max(60, n // 3)
        res = run.play(_mirror_jobs(m, seed0, size, ("annihilation",), mods=(("no-control", 1),)))
        vals[label] = (score(res) - 0.5, m)
    (ls, (vs, ns)), (ll, (vl, nl)) = vals.items()
    lim = se(0.5, ns) + se(0.5, nl)
    return vl > vs - lim, f"control edge small {vs:+.3f}, large {vl:+.3f}", f"large ≥ small - {lim:.3f}"


def c_lives_duration(run: Runner, n: int):
    means = []
    for lives in (1, 2, 4):
        res = run.play(_mirror_jobs(n, 9000, (5, 10), ("annihilation",), lives=lives))
        means.append((lives, sum(r["duration"] for r in res) / len(res)))
    ok = all(b[1] > a[1] * 1.15 for a, b in zip(means, means[1:]))
    return ok, ", ".join(f"{lv} lives {m:.0f} s" for lv, m in means), "each step ≥ 15% longer"


def c_no_abilities(run: Runner, n: int):
    everything = tuple(sorted(_rules().abilities))
    jobs = []
    for i in range(n):
        rng = random.Random(f"validity:noab:{i}")
        k = rng.randint(5, 15)
        gt = ("annihilation", "attrition")[i % 2]
        jobs.append((10000 + i, scenario(roster(rng, k), roster(rng, k), gt), everything, (), False))
    res = run.play(jobs)
    p, b = score(res), band(n)
    return abs(p - 0.5) <= b, f"team 0 {p:.3f}", f"0.5 ± {b:.3f}"


def c_numbers(run: Runner, n: int):
    def plus_two(rng, t):
        return [dict(p) for p in t] + roster(rng, 2), [dict(p) for p in t]
    p = score(run.play(_mirror_jobs(n, 11000, (5, 8), ("annihilation",), make=plus_two)))
    return p >= 0.7, f"side with 2 extra players {p:.3f} (10-16 per side)", "≥ 0.7"


def c_armor_helps(run: Runner, n: int):
    def armored_classes(rng, t):
        t = [dict(p, cls=rng.choice(("Warrior", "Paladin", "Anti-Paladin", "Barbarian", "Scout"))) for p in t]
        return t, [dict(p) for p in t]
    p = score(run.play(_mirror_jobs(n, 12000, (5, 10), make=armored_classes,
                                    mods=(("full-armor", 0), ("no-armor", 1)))))
    return p >= 0.6, f"armored side {p:.3f}", "≥ 0.6"


def c_level(run: Runner, n: int):
    p = score(run.play(_mirror_jobs(n, 13000, (5, 10),
                                    make=lambda rng, t: (shifted(t, level=6), shifted(t, level=1)))))
    return p >= 0.6, f"6th-level side {p:.3f} vs same classes at 1st", "≥ 0.6"


def c_healer_behavior(run: Runner, n: int):
    res = run.play(_mirror_jobs(n, 14000, (8, 15), watch=True))
    hs = sum(r["heal_starts"] for r in res)
    eng = sum(r["heal_on_engaged"] for r in res) / max(hs, 1)
    dog = sum(r["heal_dogpile"] for r in res) / max(hs, 1)
    cs = sum(r["cast_seconds"] for r in res)
    att = sum(r["cast_seconds_attacked"] for r in res) / max(cs, 1)
    ok = eng <= 0.05 and dog <= 0.05 and att <= 0.05
    return ok, f"heals on allies in melee {eng:.1%}, on allies already being healed {dog:.1%}, " \
               f"incanting while attacked {att:.1%} of cast time", "each ≤ 5%"


CHECKS: list[Check] = [
    Check("mirror", "Identical rosters on both sides: nothing but luck should separate them.", c_mirror, 1200),
    Check("seat-swap", "Which side is listed first must not matter.", c_mirror_seat_swap, 1200),
    Check("no-abilities", "With every ability removed it is a pure stick fight, and random teams are still a coin flip.",
          c_no_abilities, 1200),
    Check("skill", "A team a full sd more skilled wins most small games.", c_skill, 600),
    Check("skill-vs-class", "In small games, player skill matters more than class choice: a clearly better "
          "mixed team beats an average team that stacked melee classes.", c_skill_vs_class, 600),
    Check("class-stack", "Stacking heavy-melee classes helps in a small game, but a mixed team of equal skill "
          "is still competitive.", c_class_stack, 600,
          known_limit="Casters can't use distance: no map to kite on, Stopped and action restrictions "
                      "don't stop anyone reaching them, and skill doesn't affect ranged accuracy. Melee "
                      "decides most games (about 95% of kills in fighters-vs-casters games)."),
    Check("numbers", "Two extra bodies on one side of a small game usually decide it.", c_numbers, 600),
    Check("armor", "Among armor-wearing classes, the side in armor beats the side without.", c_armor_helps, 600),
    Check("level", "6th-level players beat the same classes at 1st level.", c_level, 600),
    Check("healer-added", "Adding a Healer to one side of a long attrition game doesn't hurt that side.",
          c_healer_added, 800),
    Check("heal-not-harmful", "Having Heal is never worse than not having it, in lives or attrition games.",
          c_heal_not_harmful, 1600),
    Check("archers-vs-armor", "Arrows kill more when the opponents wear little armor.", c_archers_vs_armor, 600),
    Check("control-scales", "Control effects are worth at least as much in large games as in small ones.",
          c_control_scales, 600,
          known_limit="Phase 1 has no space: no lines to break, no clumps for area effects to hit."),
    Check("more-lives", "More lives means longer games.", c_lives_duration, 300),
    Check("healer-behavior", "Healers heal behind the line, don't dogpile a target, and nobody incants while being hit.",
          c_healer_behavior, 300),
]


def run_checks(names=None, scale: float = 1.0, workers: int | None = None) -> list[Result]:
    run = Runner(workers)
    out = []
    try:
        for c in CHECKS:
            if names and c.name not in names:
                continue
            n = max(20, int(c.games * scale))
            t0 = time.perf_counter()
            ok, measured, expected = c.fn(run, n)
            out.append(Result(c.name, ok, measured, expected, c.rationale, c.known_limit,
                              time.perf_counter() - t0))
    finally:
        run.close()
    return out


def table(results: list[Result]) -> str:
    rows = []
    for r in results:
        status = "PASS" if r.passed else ("FAIL (known limit)" if r.known_limit else "FAIL")
        rows.append(f"{status:18s} {r.name:17s} {r.measured}  [expect {r.expected}] ({r.seconds:.0f} s)\n"
                    f"{'':37s}{r.rationale}"
                    + (f"\n{'':37s}limit: {r.known_limit}" if r.known_limit and not r.passed else ""))
    return "\n".join(rows)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Face-validity checks (pass/fail table).")
    ap.add_argument("--only", default="", help="comma-separated check names")
    ap.add_argument("--scale", type=float, default=1.0, help="multiply every check's game count")
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--set", action="append", default=[], metavar="GROUP.NAME=VALUE",
                    help="override an assumption for this run (JSON value), e.g. time.speech_words_per_second=3.5")
    args = ap.parse_args(argv)
    _set_overrides({k: json.loads(v) for k, v in (s.split("=", 1) for s in args.set)})
    names = {s for s in args.only.split(",") if s} or None
    results = run_checks(names, args.scale, args.workers or None)
    print(table(results))
    hard = [r for r in results if not r.passed and not r.known_limit]
    print(f"\n{sum(r.passed for r in results)}/{len(results)} passed"
          + (f"; unexpected failures: {', '.join(r.name for r in hard)}" if hard else ""))
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
