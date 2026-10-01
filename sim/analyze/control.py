"""What casters do on the field, by play style: a diagnostic for "control looks harmful" (sim/PHASE2.md).

    .venv/bin/python -m sim.analyze.control                       # mixed preset, 300 games, space on
    .venv/bin/python -m sim.analyze.control --games 600 --space off
    .venv/bin/python -m sim.analyze.control --scenario control-scales   # validity's large control-scales games

Plays instrumented games (a `Game` subclass that only observes) and reports, per kind of player
(each Magic User play style, Archers with a bow, fighters):

  time        share of time alive on the field spent incanting, Charging, in melee, retreating,
              otherwise moving, or standing
  casts       incantations started and completed per minute alive; how started incantations ended
              (completed, interrupted by death, by being struck, abandoned, by a State, ...); how
              completed ones resolved (took effect, out of range, missed, other failures)
  deaths      per minute alive, and the share that came while incanting
  targets     for control casts (Stopped, Frozen, Stunned, Suppressed, Insubstantial States,
              Awe/Terror/Insult restrictions, forced movement) started on an enemy: distance at the
              start, whether the target was in melee with a teammate, already held still, or running
              at the caster, and its kind
  lockdowns   each control State that landed on an enemy line fighter: how far the holder moved
              while it lasted (Stopped, Frozen and Stunned must be 0), whether it was running at
              someone when it landed, and whether it reached a caster while held

With `--scenario control-scales` the games are validity's large control-scales mirrors (team 1
loses its control abilities) and every row is split by team: with control / without.
"""
from __future__ import annotations

import argparse
import os
import random
from collections import Counter, defaultdict
from multiprocessing import Pool

from sim.engine.game import Game
from sim.policies import _is_control

HOLD_STATES = ("stopped", "frozen", "stunned")
ACTIVITIES = ("incanting", "charging", "melee", "retreating", "moving", "standing")


def kind_of(p) -> str:
    if p.play:
        return "archer (bow)" if p.play == "archer" and p.has_bow else p.play
    if p.role == "archer":
        return "archer (bow)" if p.has_bow else "archer (no bow)"
    return p.role


class Probe(Game):
    """Observes; never draws from Game.rng, so the game plays as it would unobserved."""

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.c: Counter = Counter()           # (team_tag, kind, metric) -> count or seconds
        self.dist: defaultdict = defaultdict(list)
        self._held: dict = {}                 # pid -> [state, until, x, y, was_charging, reached]
        self.team_tag = ("", "")

    def _k(self, p, metric):
        return (self.team_tag[p.team], kind_of(p), metric)

    def start_cast(self, p, uses, target):
        ok = super().start_cast(p, uses, target)
        if not ok:
            return ok
        self.c[self._k(p, "cast-start")] += 1
        if target is not None and target.team != p.team and _is_control(uses):
            k = self._k(p, "control-start")
            self.c[k] += 1
            sp = self.space
            if sp.spatial:
                self.dist[k].append(sp.distance(p, target))
            t = self.t
            fighting = target.target is not None and self.players[target.target].team == p.team \
                or any(a.team == p.team for a in self.attackers_of(target))
            self.c[self._k(p, "control-target-in-melee")] += fighting
            self.c[self._k(p, "control-target-held")] += any(target.has_state(s, t) for s in HOLD_STATES)
            charging = target.target == p.pid or (sp.spatial and sp.goal[target.pid] == p.pid)
            self.c[self._k(p, "control-target-at-me")] += charging
            self.c[self._k(p, f"control-target:{kind_of(target)}")] += 1
        return ok

    def _complete(self, p):
        c = p.casting
        before = Counter(self.fails) if c is not None and c.kind == "cast" else None
        super()._complete(p)
        if before is None:
            return
        new = [k for k in self.fails if self.fails[k] > before.get(k, 0)]
        if not new:
            self.c[self._k(p, "complete:effect")] += 1
        else:
            why = new[0][1]
            if why.startswith("interrupted"):
                why = "other"
            self.c[self._k(p, f"complete:{why}")] += 1
        self.c[self._k(p, "cast-complete")] += 1

    def interrupt(self, p, why):
        if p.casting is not None and p.casting.kind == "cast":
            self.c[self._k(p, f"interrupted:{why}")] += 1
        super().interrupt(p, why)

    def kill(self, p, src, slug):
        casting = p.alive and p.casting is not None and p.casting.kind == "cast"
        was = p.alive
        super().kill(p, src, slug)
        if was and not p.alive:
            self.c[self._k(p, "deaths")] += 1
            self.c[self._k(p, "deaths-incanting")] += casting
            if src is not None:
                self.c[self._k(p, f"killed-by:{kind_of(src)}")] += 1
                self.c[self._k(src, "kills")] += 1
                # killed by an enemy this player had Insulted (it may attack only them)
                self.c[self._k(p, "deaths-by-insulted")] += any(
                    r.src == p.pid and r.what == "attack-anyone-but-caster" for r in src.restrictions)

    def apply_state(self, p, state, until, own=True, src=None):
        sp = self.space
        watch = state in HOLD_STATES and src is not None and src.team != p.team and sp.spatial \
            and sp.style[p.pid] == "line" and not p.has_state(state, self.t)
        if watch:       # before the State lands: Frozen and Stunned end every melee the player is in
            charging = sp.goal[p.pid] is not None and p.target is None
            in_melee = p.target is not None or bool(self.attackers_of(p))
            fighting_it = sum(1 for a in self.players if a.team == src.team and a.alive and a.target == p.pid)
        ok = super().apply_state(p, state, until, own, src)
        if ok and watch:
            if in_melee:
                self.c[self._k(src, f"lockdown-in-melee:{state}")] += 1
                self.c[self._k(src, f"lockdown-freed:{state}")] += fighting_it
            # [state, x and y at the end of the last tick held, metres moved while held, charging, reached, tag]
            self._held[p.pid] = [state, sp.x[p.pid], sp.y[p.pid], 0.0, charging, False, self._k(src, "")]
            self.c[self._k(src, f"lockdown:{state}")] += 1
            self.c[self._k(src, f"lockdown-charging:{state}")] += charging
        return ok

    def step(self):
        sp = self.space
        before = list(sp.moved_m) if sp.spatial else None
        w = super().step()
        t, dt = self.t, self.dt
        for p in self.players:
            if not p.alive or not p.on_field(t):
                continue
            if p.casting is not None:
                a = "incanting" if p.casting.kind == "cast" else "charging"
            elif p.target is not None or self.attackers_of(p):
                a = "melee"
            elif sp.spatial and sp.retreating(p):
                a = "retreating"
            elif sp.spatial and sp.moved_m[p.pid] > before[p.pid] + 1e-9:
                a = "moving"
            else:
                a = "standing"
            self.c[self._k(p, f"time:{a}")] += dt
            self.c[self._k(p, "time")] += dt
        for pid, h in list(self._held.items()):
            q = self.players[pid]
            state, x0, y0, moved, charging, reached, tag = h
            if not q.alive or not q.on_field(t) or not q.has_state(state, t):
                # ended (or the player died or was sent to base) before this tick's movement mattered
                self.c[tag[:2] + (f"lockdown-moved-m:{state}",)] += moved
                self.c[tag[:2] + (f"lockdown-reached-caster:{state}",)] += reached
                del self._held[pid]
                continue
            # still held at the end of this tick, and held through its movement step: any step counts
            step = ((sp.x[pid] - x0) ** 2 + (sp.y[pid] - y0) ** 2) ** 0.5
            if step <= sp.run * dt + 1e-6:      # longer jumps are a team wipe's return to base, not a step
                h[3] += step
            h[1], h[2] = sp.x[pid], sp.y[pid]
            if q.target is not None and self.players[q.target].backline:
                h[5] = True
        return w


def _job(args):
    seed, sc, mods, space, tags = args
    from sim.analyze import validity as v
    rules = v._rules()
    g = Probe(rules, sc, seed, space=space)
    g.team_tag = tags
    for mod, team in mods:
        v._apply_mod(g, mod, team)
    g.run()
    return g.c, {k: list(x) for k, x in g.dist.items()}


def jobs_for(scenario: str, n: int, space: str) -> list[tuple]:
    from sim.analyze import validity as v
    from sim.rules.compile import default_rules
    from sim.scenarios import generate, load_config
    if scenario == "control-scales":
        out = []
        for seed, sc, _abl, mods, _w in v._mirror_jobs(n, 8500, (25, 35), ("annihilation",),
                                                       mods=(("no-control", 1),)):
            out.append((seed, sc, mods, space, ("with control", "without")))
        return out
    rules = default_rules()
    cfg = load_config(scenario)
    return [(s, generate(s, cfg, rules), (), space, ("", "")) for s in range(1, n + 1)]


def run(scenario: str, n: int, space: str, workers: int | None = None):
    from sim.analyze import validity as v
    jobs = jobs_for(scenario, n, space)
    total: Counter = Counter()
    dist: defaultdict = defaultdict(list)
    with Pool(workers or os.cpu_count() or 1, v._set_overrides, ({}, space)) as pool:
        for c, d in pool.imap_unordered(_job, jobs, chunksize=max(1, len(jobs) // 60)):
            total.update(c)
            for k, x in d.items():
                dist[k].extend(x)
    return total, dist


def report(total: Counter, dist) -> str:
    rows = sorted({(tag, kind) for tag, kind, _ in total})
    lines = []

    def g(tag, kind, m):
        return total.get((tag, kind, m), 0)
    for tag, kind in rows:
        secs = g(tag, kind, "time")
        if secs <= 0:
            continue
        mins = secs / 60
        head = f"{tag + ': ' if tag else ''}{kind}"
        lines.append(f"\n{head}  ({mins:,.0f} player-minutes alive on the field)")
        lines.append("  time   " + "  ".join(f"{a} {g(tag, kind, 'time:' + a) / secs:5.1%}" for a in ACTIVITIES))
        started, done = g(tag, kind, "cast-start"), g(tag, kind, "cast-complete")
        if started:
            ends = Counter({m.split(":", 1)[1]: n for (t2, k2, m), n in total.items()
                            if t2 == tag and k2 == kind and m.startswith("interrupted:")})
            res = Counter({m.split(":", 1)[1]: n for (t2, k2, m), n in total.items()
                           if t2 == tag and k2 == kind and m.startswith("complete:")})
            lines.append(f"  casts  started {started / mins:.2f}/min, completed {done / mins:.2f}/min "
                         f"({done / started:.0%} of starts)")
            lines.append("         ended early: " + ", ".join(f"{k} {n / started:.1%}" for k, n in ends.most_common(6)))
            if done:
                lines.append("         completed: " + ", ".join(f"{k} {n / done:.1%}" for k, n in res.most_common(6)))
        deaths = g(tag, kind, "deaths")
        lines.append(f"  kills {g(tag, kind, 'kills') / mins:.3f}/min alive; deaths {deaths / mins:.3f}/min alive, "
                     f"by an enemy they had Insulted {g(tag, kind, 'deaths-by-insulted') / max(1, deaths):.1%}, "
                     f"{g(tag, kind, 'deaths-incanting') / max(1, deaths):.1%} "
                     f"while incanting; killed by " + ", ".join(
                         f"{m.split(':', 1)[1]} {n / max(1, deaths):.0%}" for (t2, k2, m), n in
                         sorted(total.items(), key=lambda kv: -kv[1]) if t2 == tag and k2 == kind
                         and m.startswith("killed-by:"))[:200])
        cs = g(tag, kind, "control-start")
        if cs:
            d = dist.get((tag, kind, "control-start"), [])
            md = f"mean distance {sum(d) / len(d):.1f} m, " if d else ""
            tk = Counter({m.split(":", 1)[1]: n for (t2, k2, m), n in total.items()
                          if t2 == tag and k2 == kind and m.startswith("control-target:")})
            lines.append(f"  control casts started {cs / mins:.2f}/min: {md}target in melee with a teammate "
                         f"{g(tag, kind, 'control-target-in-melee') / cs:.0%}, already held "
                         f"{g(tag, kind, 'control-target-held') / cs:.0%}, running at the caster "
                         f"{g(tag, kind, 'control-target-at-me') / cs:.0%}; targets " +
                         ", ".join(f"{k} {n / cs:.0%}" for k, n in tk.most_common(4)))
        for s in HOLD_STATES:
            n = g(tag, kind, f"lockdown:{s}")
            if n:
                lines.append(f"  {s} landed on a line fighter {n / mins:.2f}/min: in melee "
                             f"{g(tag, kind, f'lockdown-in-melee:{s}') / n:.0%} (teammates fighting it: "
                             f"{g(tag, kind, f'lockdown-freed:{s}') / n:.2f} each), running at someone "
                             f"{g(tag, kind, f'lockdown-charging:{s}') / n:.0%}, moved while {s} "
                             f"{g(tag, kind, f'lockdown-moved-m:{s}') / n:.2f} m on average, reached a "
                             f"caster/archer while {s} {g(tag, kind, f'lockdown-reached-caster:{s}') / n:.0%}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--games", type=int, default=300)
    ap.add_argument("--scenario", default="mixed", help="a sim/scenarios config, or control-scales")
    ap.add_argument("--space", default="on", choices=("on", "off"))
    ap.add_argument("--workers", type=int, default=None)
    args = ap.parse_args(argv)
    random.seed(0)
    total, dist = run(args.scenario, args.games, args.space, args.workers)
    print(f"{args.games} {args.scenario} games, space {args.space}")
    print(report(total, dist))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
