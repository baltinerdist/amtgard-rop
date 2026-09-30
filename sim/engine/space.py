"""Where players are: the one interface every distance question goes through (sim/PHASE2.md).

Phase 1 answered "is the target in range?", "is a teammate close enough to Touch?", "who fights
whom?" and "how long until a respawned player is back?" with probabilities from
sim/data/assumptions.json (`range.*`, `engagement.*`, `respawn.rejoin_seconds`). Every one of those
questions is now a method of a `Space`:

- `NullSpace` (`--space off`) is Phase 1. Each method draws the same probability from the same
  random stream in the same order as the code it replaced, so a seed plays bit-for-bit as before
  (tests/sim/test_space.py compares game digests recorded before the change).
- `FieldSpace` (`--space on`) is geometric: continuous positions on a rectangle with a base at each
  short end, movement at walking and running speed, geometric 20', 50', Touch and melee reach, and
  engagement from proximity. Its numbers are the `space` group of sim/data/assumptions.json.

The engine and the policies (the "brain": `decide`, utilities, songs) ask the space; they never
look at positions themselves. Movement is a separate step (`Space.move`): each tick, after the
brain has chosen what to do, every player who may move steps toward where their play style wants
them (`FieldSpace._want`). The rules of that step:

| Who | Where they want to be |
| --- | --- |
| everyone | nowhere new while incanting or Charging (feet may not move; a Chant may move), while Stopped, Frozen, Stunned or Insubstantial (states.md), dead, or at base |
| a leg wound | crawls on the knees (`crawl_speed_mps`) with a living enemy within 20'; otherwise hobbles, one step a second (`hobble_speed_mps`) (combat-rules.md, Hit Locations notes 4 and 6) |
| engaged in melee | stays; steps in if the melee target is beyond the player's reach |
| a teammate is incanting a Touch or Other ability on them | stays (a willing target stands still), unless retreating |
| line fighters (fighter role, battle play, an archer without a bow) | take a slot in the team's line and walk forward with it; charge at a run when an enemy is within `charge_distance_m`: the enemy they can reach soonest (`_goal`). Nobody starts a melee with a player inside their own base zone (`base_zone_m`) |
| strikers, controllers | `preferred_distance_m` from the nearest enemy, but at least `behind_line_m` behind their own line |
| medics | run to the nearest teammate out of melee who is wounded (or dead, holding a revive); otherwise as a striker, farther back |
| enchanters | run to the nearest free teammate with an open Enchantment slot while they hold an Enchantment for them; otherwise just behind the line |
| archers (with a bow) | keep `preferred_distance_m.archer` from the nearest enemy |
| any non-line player | retreats at a run, and starts no incantation (`retreating`), while an enemy line fighter who is free to attack them is within `retreat_trigger_m` |

Walking speed is for taking position (the line's advance, keeping distance, walking back from
base); running is for charging, retreating and reaching a wounded teammate.

Not spatial yet (stage 2): distance curves for Magic Balls and arrows (stage 1 keeps the flat hit
chances, thrown only within `throw_range_m` / `bow_range_m`), where thrown balls land, forced
movement (Shove, Throw, Lost, Banish, keep-away still use Phase 1's `kept_away_until` timer and
`send_to_base`), Teleport, Blink's 10', Summon Dead, Ambulant beyond the Uses flag, alternate bases
and respawn points, Heart of the Swarm, Sanctuary; and the value score (`policies/value.py`) still
prices range and mobility with the Phase 1 tables.
"""
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING

from sim.engine.state import LEGS, Player, Uses

if TYPE_CHECKING:
    from sim.engine.game import Game

FOOT = 0.3048                  # metres; ranges in the rules are in feet
MODES = ("off", "on")
INF = math.inf
_IMMOBILE = ("stopped", "frozen", "stunned", "insubstantial")   # may not move their feet (states.md)
_LEGS = frozenset(LEGS)


def make_space(g: "Game", mode: str | None) -> "Space":
    mode = (mode or "off").lower()
    if mode not in MODES:
        raise ValueError(f"space must be one of {', '.join(MODES)}, not {mode!r}")
    return FieldSpace(g) if mode == "on" else NullSpace(g)


class Space:
    """The interface. Methods that roll in NullSpace are geometric in FieldSpace; `p` is the player
    asking, `q` the other player, `u` the ability (its range label, or a Magic Ball's or Specialty
    Arrow's throw or bow range)."""
    spatial = False
    mode = "off"

    def __init__(self, g: "Game"):
        self.g = g
        self.tick_seconds = g.rules.a("time.tick_seconds")
        self.decide_seconds = 1

    # --- the proxies (NullSpace draws, FieldSpace measures)
    def roll_in_range(self, p: Player, q: Player, u: Uses) -> bool: ...
    def roll_touch(self, p: Player, q: Player, u: Uses | None = None) -> bool: ...
    def in_range_filter(self, p: Player, qs: list, u: Uses | None = None, label: str = "") -> list: ...
    def touch_filter(self, p: Player, qs: list, u: Uses | None = None) -> list: ...
    def p_in_range(self, p: Player, q: Player, label: str) -> float: ...
    def p_touch(self, p: Player, q: Player) -> float: ...
    def p_any_in_range(self, p: Player, u: Uses) -> float: ...
    def expected_in_range(self, p: Player, qs: list, label: str, weights: list | None = None) -> float: ...
    def roll_beyond_20(self, p: Player, q: Player | None) -> bool: ...
    def roll_song_near(self, singer: Player, p: Player) -> bool: ...
    def enemy_within(self, p: Player, feet: float) -> bool: ...
    def completes_in_range(self, p: Player, q: Player, label: str, delivery: str) -> bool: ...
    def can_reach(self, p: Player, q: Player) -> bool: ...
    def arrival_time(self, p: Player) -> float: ...
    def send_to_base(self, p: Player) -> None: ...
    def respawn(self, p: Player) -> None: ...
    def team_wiped(self, team: int) -> None: ...
    def retreating(self, p: Player) -> bool: ...
    def thinks(self, p: Player) -> bool: ...
    def deploy(self) -> None: ...
    def move(self) -> None: ...
    def engage(self) -> None: ...
    def stats(self) -> dict | None: ...


# ====================================================================== Phase 1

class NullSpace(Space):
    """Phase 1 exactly: every answer is the old probability, drawn from `Game.rng` where the old code
    drew it. Methods that had no draw draw nothing."""

    def roll_in_range(self, p, q, u):
        return self.g.rng.random() < self.g.rules.a("range.p_in_range").get(u.range, 0.5)

    def roll_touch(self, p, q, u=None):
        return self.g.rng.random() < self.g.rules.a("range.p_ally_nearby_for_touch")

    def in_range_filter(self, p, qs, u=None, label=""):
        return qs

    def touch_filter(self, p, qs, u=None):
        return qs

    def p_in_range(self, p, q, label):
        return self.g.rules.a("range.p_in_range").get(label, 0.5)

    def p_touch(self, p, q):
        return self.g.rules.a("range.p_ally_nearby_for_touch")

    def p_any_in_range(self, p, u):
        return self.g.rules.a("range.p_in_range").get(u.range, 0.5)

    def expected_in_range(self, p, qs, label, weights=None):
        v = self.g.rules.a("range.p_in_range").get(label, 0.5)
        if weights is None:
            return len(qs) * v
        total = 0.0
        for w in weights:
            total += w
        return total * v

    def roll_beyond_20(self, p, q):
        table = self.g.rules.a("range.p_in_range")
        return self.g.rng.random() >= table["20'"] / table["50'"]

    def roll_song_near(self, singer, p):
        return self.g.rng.random() < self.g.rules.a("range.p_in_range")["20'"]

    def enemy_within(self, p, feet):
        return p.target is not None or bool(self.g.attackers_of(p))

    def completes_in_range(self, p, q, label, delivery):
        return True

    def can_reach(self, p, q):
        return True

    def arrival_time(self, p):
        return self.g.t + self.g.rules.a("respawn.rejoin_seconds")

    def send_to_base(self, p):
        p.at_base_until = self.g.t + self.g.rules.a("respawn.rejoin_seconds")

    def respawn(self, p):
        p.at_base_until = self.g.t + self.g.rules.a("respawn.rejoin_seconds")

    def team_wiped(self, team):
        pass

    def retreating(self, p):
        return False

    def thinks(self, p):
        return True

    def deploy(self):
        pass

    def move(self):
        pass

    def stats(self):
        return None

    def engage(self) -> None:
        """Phase 1's engagement draw (formerly Game._engage), unchanged."""
        g = self.g
        t = g.t
        a = g.rules.a
        p_engage = a("engagement.p_engage_per_second")
        backline = a("engagement.backline_factor")
        caster_w = a("engagement.caster_weight_when_choosing_melee_target")
        p_dis = a("engagement.p_disengage_per_second")
        # Shuffled like _melee: walking the roster in order let team 0 always choose targets first
        # and team 1 always react, which tilted even ability-free games.
        order = list(g.players)
        g.rng.shuffle(order)
        for p in order:
            if not p.can_act(t) or not p.on_field(t) or g.barred(p, "wield-weapons") or p.weapon_hot_until > t:
                p.target = None
                continue
            if p.target is not None:
                q = g.players[p.target]
                if not g.targetable(q) or not g.can_attack(p, q) or g.rng.random() < p_dis:
                    p.target = None
                continue
            if p.casting is not None or p.kept_away_until > t:
                continue
            attackers = [q for q in g.attackers_of(p) if g.targetable(q) and g.can_attack(p, q)]
            if attackers:
                p.target = g.rng.choice(attackers).pid
                continue
            if p.role != "fighter" and p.play != "battle" and not (p.role == "archer" and not p.has_bow):
                continue
            if g.rng.random() >= p_engage:
                continue
            foes = [q for q in g.enemies(p) if g.targetable(q) and q.kept_away_until <= t
                    and g.can_attack(p, q)]
            if not foes:
                continue
            weights = [(backline * caster_w) if q.backline else 1.0 for q in foes]
            p.target = g.rng.choices(foes, weights=weights)[0].pid


# ====================================================================== the field

def style(p: Player) -> str:
    """How p takes position: line, caster, medic, enchanter or archer."""
    if p.role == "fighter" or p.play == "battle" or ((p.role == "archer" or p.play == "archer") and not p.has_bow
                                                     and p.role != "caster"):
        return "line"
    if p.has_bow and (p.role == "archer" or p.play == "archer"):
        return "archer"
    if p.play in ("medic", "enchanter"):
        return p.play
    if p.play in ("striker", "controller", "archer"):
        return "caster"
    return "medic" if p.role == "support" else "caster"


class FieldSpace(Space):
    """Positions on a rectangle: x along the length (team 0's base at x = 0, team 1's at x = L), y
    across it. `u` below is a player's forward coordinate: distance from their own base end."""
    spatial = True
    mode = "on"

    def __init__(self, g: "Game"):
        super().__init__(g)
        a = lambda k: g.rules.a(f"space.{k}")      # noqa: E731
        if g.n_teams != 2:
            raise ValueError("the field (space on) has two bases; this scenario has "
                             f"{g.n_teams} teams")
        self.tick_seconds = float(a("tick_seconds"))
        self.decide_seconds = float(a("decide_seconds"))
        self._every = max(1, round(self.decide_seconds / self.tick_seconds))
        self.L, self.W = float(a("field_length_m")), float(a("field_width_m"))
        self.walk, self.run = float(a("walk_speed_mps")), float(a("run_speed_mps"))
        self.hobble, self.crawl = float(a("hobble_speed_mps")), float(a("crawl_speed_mps"))
        self.touch_m = float(a("touch_m"))
        self.reach_m = dict(a("reach_m"))
        self.throw_m, self.bow_m = float(a("throw_range_m")), float(a("bow_range_m"))
        self.deploy_m = float(a("deploy_depth_m"))
        self.base_zone_m = float(a("base_zone_m"))
        self.spacing = float(a("line_spacing_m"))
        self.charge_m = float(a("charge_distance_m"))
        self.retreat_m = float(a("retreat_trigger_m"))
        self.pref = dict(a("preferred_distance_m"))
        self.behind = dict(a("behind_line_m"))
        self.crowd_s = float(a("crowd_penalty_seconds"))
        self.caster_s = float(a("caster_priority_seconds"))
        self.horizon_s = float(a("reach_horizon_seconds"))
        self.rng = random.Random(f"{g.seed}:space")   # its own stream: jitter only, never Game.rng
        n = len(g.players)
        self.x = [0.0] * n
        self.y = [0.0] * n
        self._d: list | None = None                   # distance matrix, rebuilt lazily after moves
        self.style = [style(p) for p in g.players]
        self.reach = [self._reach_of(p) for p in g.players]
        self.goal: list[int | None] = [None] * n       # the enemy a charging line fighter runs at
        self.line_u = [self.deploy_m, self.deploy_m]    # each team's formation line, forward coordinate
        self.front_u = [self.deploy_m, self.deploy_m]   # where each team's line fighters actually are
        self._arrive: dict[int, float] = {}            # pid -> arrival at base (send_to_base)
        self._retreat: dict[int, float] = {}           # pid -> tick the retreat check was made for
        self._retreat_v: dict[int, bool] = {}
        self._respawned: dict[int, float] = {}         # pid -> respawn time, until they rejoin
        self._fresh: set[int] = set()                  # pids at base who haven't left it since arriving
        self.rejoins: list[float] = []                 # seconds from respawn to within 50' of an enemy
        self.moved_m = [0.0] * n

    # ------------------------------------------------------------ geometry

    def _reach_of(self, p: Player) -> float:
        if p.great_weapon:
            return float(self.reach_m["great"])
        return float(self.reach_m["short" if p.role != "fighter" and p.play != "battle" else "standard"])

    def base_x(self, team: int) -> float:
        return 0.0 if team == 0 else self.L

    def fwd(self, team: int) -> float:
        return 1.0 if team == 0 else -1.0

    def u_of(self, pid: int, team: int) -> float:
        return self.x[pid] if team == 0 else self.L - self.x[pid]

    def x_of(self, u: float, team: int) -> float:
        return u if team == 0 else self.L - u

    def in_base(self, q: Player) -> bool:
        """Still in their own base zone (within `base_zone_m` of their base end) since arriving there
        (the game's start, a respawn, a forced return), where enemies don't start a melee. Leaving
        the zone ends it: running back into base later is no refuge."""
        if q.pid not in self._fresh:
            return False
        if self.u_of(q.pid, q.team) <= self.base_zone_m:
            return True
        self._fresh.discard(q.pid)
        return False

    def _matrix(self) -> list:
        d = self._d
        if d is None:
            import numpy as np
            x, y = np.asarray(self.x), np.asarray(self.y)
            d = self._d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :]).tolist()
        return d

    def distance(self, p: Player, q: Player) -> float:
        return self._matrix()[p.pid][q.pid]

    def metres(self, label: str, delivery: str = "") -> float:
        """A range label in metres: Touch and Other `touch_m`, 20' and 50' by the foot, a Magic Ball's
        or Specialty Arrow's (no range label) the throw or bow range."""
        if label in ("Touch", "Other"):
            return self.touch_m
        if label == "Self":
            return 0.0
        if label == "Unlimited":
            return INF
        if label.endswith("'"):
            try:
                return float(label[:-1]) * FOOT
            except ValueError:
                pass
        if delivery == "magic-ball" or label == "throw":
            return self.throw_m
        if delivery == "specialty-arrow" or label == "bow":
            return self.bow_m
        return 20 * FOOT

    def _range_m(self, u: Uses | None, label: str = "") -> float:
        if u is None:
            return self.metres(label or "Touch")
        return self.metres(u.range, u.ability.delivery)

    def in_range(self, p: Player, q: Player, metres: float) -> bool:
        return p is q or self.distance(p, q) <= metres

    def within(self, p: Player, metres: float, team: int | None = None) -> list[Player]:
        """Living players (of `team`, if given) other than p within this distance."""
        row = self._matrix()[p.pid]
        return [q for q in self.g.players if q is not p and q.alive and (team is None or q.team == team)
                and row[q.pid] <= metres]

    def move_toward(self, p: Player, x: float, y: float, metres: float) -> tuple[float, float, float]:
        """p's position after moving up to `metres` toward (x, y), kept on the field; and the metres moved."""
        px, py = self.x[p.pid], self.y[p.pid]
        dx, dy = x - px, y - py
        dist = math.hypot(dx, dy)
        if dist < 1e-9:
            return px, py, 0.0
        step = min(dist, metres)
        nx = min(self.L, max(0.0, px + dx / dist * step))
        ny = min(self.W, max(0.0, py + dy / dist * step))
        return nx, ny, math.hypot(nx - px, ny - py)

    def move_away(self, p: Player, x: float, y: float, metres: float, back: float = 0.5) -> tuple[float, float, float]:
        """p's position after moving up to `metres` away from (x, y), bent toward p's own base by
        `back` (a retreat heads for its own side, not along the field's width)."""
        px, py = self.x[p.pid], self.y[p.pid]
        d = max(math.hypot(px - x, py - y), 1e-6)
        dx, dy = (px - x) / d - back * self.fwd(p.team), (py - y) / d
        n = math.hypot(dx, dy) or 1.0
        return self.move_toward(p, px + dx / n * 100.0, py + dy / n * 100.0, metres)

    def nearest(self, p: Player, candidates) -> Player | None:
        row = self._matrix()[p.pid]
        best, bd = None, INF
        for q in candidates:
            d = row[q.pid]
            if d < bd:
                best, bd = q, d
        return best

    # ------------------------------------------------------------ the proxies, measured

    def roll_in_range(self, p, q, u):
        return self.in_range(p, q, self._range_m(u))

    def roll_touch(self, p, q, u=None):
        if self._together_at_base(p, q):
            return True
        return self.in_range(p, q, self._range_m(u) if u is not None and u.range not in ("", "Self")
                             else self.touch_m)

    def in_range_filter(self, p, qs, u=None, label=""):
        m = self._range_m(u, label)
        row = self._matrix()[p.pid]
        return [q for q in qs if row[q.pid] <= m]          # p itself is at distance 0

    def touch_filter(self, p, qs, u=None):
        m = self._range_m(u) if u is not None and u.range not in ("", "Self") else self.touch_m
        row = self._matrix()[p.pid]
        if p.at_base_until > self.g.t:
            return [q for q in qs if row[q.pid] <= m or self._together_at_base(p, q)]
        return [q for q in qs if row[q.pid] <= m]

    def _p_within(self, p: Player, q: Player, m: float) -> float:
        """Expectation (no draw): 1 in range now, falling linearly to 0 at what a run covers in
        `reach_horizon_seconds` beyond it."""
        if p is q:
            return 1.0
        d = self.distance(p, q) - m
        return 1.0 if d <= 0 else max(0.0, 1.0 - d / (self.run * self.horizon_s))

    def p_in_range(self, p, q, label):
        return self._p_within(p, q, self.metres(label))

    def p_touch(self, p, q):
        return self._p_within(p, q, self.touch_m)

    def p_any_in_range(self, p, u):
        m = self._range_m(u)
        g = self.g
        return max((self._p_within(p, q, m) for q in g.enemies(p) if g.targetable(q)), default=0.0)

    def expected_in_range(self, p, qs, label, weights=None):
        m = self.metres(label)
        ws = weights if weights is not None else [1.0] * len(qs)
        return sum(w * self._p_within(p, q, m) for q, w in zip(qs, ws))

    def roll_beyond_20(self, p, q):
        return q is not None and q is not p and self.distance(p, q) > 20 * FOOT

    def roll_song_near(self, singer, p):
        return self.distance(singer, p) <= 20 * FOOT

    def enemy_within(self, p, feet):
        m = feet * FOOT
        row = self._matrix()[p.pid]
        return any(q.alive and q.team != p.team and q.on_field(self.g.t) and row[q.pid] <= m for q in self.g.players)

    def completes_in_range(self, p, q, label, delivery):
        """Rule: "Complete the incantation while within range of the target. If the incantation is
        completed and the target is not in range, the ability fails but is still expended."
        A Magic Ball or Specialty Arrow is thrown or shot only within throw or bow range."""
        if q is p or label == "Self":
            return True
        if self._together_at_base(p, q):
            return True
        return self.distance(p, q) <= self.metres(label, delivery)

    def _together_at_base(self, p: Player, q: Player) -> bool:
        """Both off the field at base (the pregame, a forced return): base is one small place where
        teammates gather, so Touch is met there, as in Phase 1's at-base enchanting."""
        t = self.g.t
        return p.team == q.team and p.at_base_until > t and q.at_base_until > t

    def can_reach(self, p, q):
        return self.distance(p, q) <= self.reach[p.pid] + 1e-9

    # ------------------------------------------------------------ bases, respawn, deployment

    def _base_spot(self, p: Player, depth: float | None = None) -> tuple[float, float]:
        u = self.rng.uniform(0.5, depth if depth is not None else 2.0)
        return self.x_of(u, p.team), self.rng.uniform(0.25 * self.W, 0.75 * self.W)

    def deploy(self):
        """Each team forms near its own base: line fighters in front, everyone else behind them."""
        g = self.g
        for team in (0, 1):
            members = [p for p in g.players if p.team == team]
            line = [p for p in members if self.style[p.pid] == "line"]
            rest = [p for p in members if self.style[p.pid] != "line"]
            for i, p in enumerate(line):
                self.x[p.pid] = self.x_of(self.deploy_m, team)
                self.y[p.pid] = self._slot_y(i, len(line))
            for p in rest:
                self.x[p.pid] = self.x_of(self.rng.uniform(1.0, max(1.5, self.deploy_m - 2.0)), team)
                self.y[p.pid] = self.rng.uniform(0.3 * self.W, 0.7 * self.W)
        self._fresh = {p.pid for p in g.players}
        self._d = None

    def _slot_y(self, i: int, n: int) -> float:
        y = self.W / 2 + (i - (n - 1) / 2) * self.spacing
        return min(self.W - 0.5, max(0.5, y))

    def _walk_seconds_to_base(self, p: Player) -> float:
        return self.u_of(p.pid, p.team) / self.walk

    def arrival_time(self, p):
        when = self._arrive.get(p.pid)
        if when is not None and when > self.g.t:
            return when
        return self.g.t + self._walk_seconds_to_base(p)

    def send_to_base(self, p):
        """Forced movement to base (stage 1: kept as Phase 1's "gone until back" window): the player
        leaves the field for the walk to base, then stands at base and walks back."""
        when = self.arrival_time(p)
        self._arrive[p.pid] = when
        p.at_base_until = when
        self.x[p.pid], self.y[p.pid] = self._base_spot(p)
        self.goal[p.pid] = None
        self._fresh.add(p.pid)
        self._d = None

    def respawn(self, p):
        """Respawn at base and walk back (no rejoin timer)."""
        p.at_base_until = self.g.t
        self.x[p.pid], self.y[p.pid] = self._base_spot(p)
        self.goal[p.pid] = None
        self._respawned[p.pid] = self.g.t
        self._fresh.add(p.pid)
        self._d = None

    def team_wiped(self, team):
        """Mutual Annihilation: "all players are set to their bases" (battlegames.md)."""
        self.deploy()
        self.line_u = [self.deploy_m, self.deploy_m]
        self.front_u = [self.deploy_m, self.deploy_m]
        self.goal = [None] * len(self.goal)

    def stats(self):
        return {"rejoin_n": len(self.rejoins), "rejoin_sum": round(sum(self.rejoins), 3),
                "moved_m": round(sum(self.moved_m), 1)}

    # ------------------------------------------------------------ who may move, how fast

    def _speed_cap(self, p: Player) -> float:
        t = self.g.t
        if p.casting is not None and not (p.casting.uses is not None and p.casting.uses.ambulant):
            return 0.0            # "Not move their feet during the incantation" (and the Charge)
        if p.states and any(p.states.get(s, -1.0) > t for s in _IMMOBILE):
            return 0.0
        if p.wounds and (p.wounds & _LEGS):
            # kneel (move on the knees) with a living enemy within 20'; else hobble, one step a second
            return self.crawl if self.enemy_within(p, 20) else self.hobble
        return self.run

    def _threat(self, q: Player) -> bool:
        """An enemy who could close to melee: a line fighter, able to act and move, not in melee."""
        t = self.g.t
        return (self.style[q.pid] == "line" and q.can_act(t) and q.on_field(t) and q.target is None
                and not q.has_state("stopped", t) and self.g.weapon_usable(q))

    def _threats_near(self, p: Player, m: float) -> list[Player]:
        row = self._matrix()[p.pid]
        return [q for q in self.g.players if q.team != p.team and q.alive and row[q.pid] <= m and self._threat(q)]

    def thinks(self, p):
        """Whether p's brain (`decide`) runs this tick: every `decide_seconds`, staggered by player."""
        return (round(self.g.t / self.tick_seconds) + p.pid) % self._every == 0

    def retreating(self, p):
        """A non-line player backs off, and starts no incantation, while a free enemy line fighter
        is within `retreat_trigger_m` and nobody is attacking them yet."""
        if self.style[p.pid] == "line" or p.target is not None:
            return False
        t = self.g.t
        if self._retreat.get(p.pid) == t:
            return self._retreat_v[p.pid]
        v = p.on_field(t) and self._speed_cap(p) > 0 and not self.g.attackers_of(p) \
            and bool(self._threats_near(p, self.retreat_m))
        self._retreat[p.pid], self._retreat_v[p.pid] = t, v
        return v

    # ------------------------------------------------------------ the movement step

    def _update_lines(self) -> None:
        """Each team's formation line (`line_u`, where unengaged line fighters take their slots)
        walks forward, waiting for its fighters and stopping `charge_distance_m` short of the
        nearest enemy. The front (`front_u`, what casters stay behind) is where the team's line
        fighters actually are: the median of those within 15 m of the most forward one."""
        g = self.g
        t = g.t
        for team in (0, 1):
            line = [p for p in g.players if p.team == team and p.alive and self.style[p.pid] == "line"]
            mine = sorted(self.u_of(p.pid, team) for p in line if p.on_field(t))
            if not line:
                self.line_u[team] = self.front_u[team] = self.L      # no line: casters aren't held back
                continue
            if not mine:
                continue                                              # pregame, or all walking back
            foes = [self.u_of(q.pid, team) for q in g.players
                    if q.team != team and q.alive and q.on_field(t) and not self.in_base(q)]
            u = min(self.line_u[team] + self.walk * self.tick_seconds, mine[len(mine) // 2] + 1.0)
            if foes:
                u = min(u, min(foes) - self.charge_m)
            self.line_u[team] = max(self.deploy_m, min(u, self.L - self.deploy_m))
            fwd = [m for m in mine if m >= mine[-1] - 15.0]
            self.front_u[team] = max(self.line_u[team], fwd[len(fwd) // 2])

    def _tick_context(self) -> None:
        """What every player's movement looks at this tick, gathered once: who is attacked, each
        team's line fighters in pid order, the enemies on the field (and outside their base), and
        how many of each team are on each enemy (fighting it or running at it)."""
        g = self.g
        t = g.t
        players = g.players
        self._attacked = {q.target for q in players if q.alive and q.target is not None}
        self._line = [[], []]
        self._field = [[], []]          # [team] -> living players of that team on the field
        on = [{}, {}]
        for q in players:
            if not q.alive:
                continue
            if self.style[q.pid] == "line":
                self._line[q.team].append(q.pid)
            if q.on_field(t):
                self._field[q.team].append(q)
            k = q.target if q.target is not None else self.goal[q.pid]
            if k is not None:
                on[q.team][k] = on[q.team].get(k, 0) + 1
        self._slot = [{pid: i for i, pid in enumerate(line)} for line in self._line]
        self._on = on
        # teammates being touched: a willing player stands still for a teammate's Touch or Other incantation
        self._held = {q.casting.target for q in players
                      if q.casting is not None and q.casting.kind == "cast" and q.casting.target is not None
                      and q.casting.target != q.pid and (q.casting.range or q.casting.uses.range) in ("Touch", "Other")
                      and players[q.casting.target].team == q.team}
        self._chargeable = [[q for q in self._field[team] if not self.in_base(q)] for team in (0, 1)]

    def _goal(self, p: Player) -> Player | None:
        """The enemy p can reach soonest: running time, plus `crowd_penalty_seconds` per teammate
        already on them, less `caster_priority_seconds` for a caster, healer or archer."""
        g = self.g
        t = g.t
        row = self._matrix()[p.pid]
        on = self._on[p.team]
        mine = self.goal[p.pid] if p.target is None else p.target
        best, bs = None, INF
        for q in self._chargeable[1 - p.team]:
            if not g.targetable(q) or q.kept_away_until > t or not g.can_attack(p, q):
                continue
            n = on.get(q.pid, 0) - (1 if q.pid == mine else 0)
            s = row[q.pid] / self.run + self.crowd_s * n - (self.caster_s if q.backline else 0.0)
            if s < bs:
                best, bs = q, s
        return best

    def _behind_line(self, p: Player, x: float, style_: str) -> float:
        """x clamped to at least `behind_line_m` behind p's own line (while it has line fighters)."""
        cap = self.x_of(self.front_u[p.team] - self.behind.get(style_, 2.0), p.team)
        return min(x, cap) if p.team == 0 else max(x, cap)

    def _keep_distance(self, p: Player, style_: str) -> tuple[float, float, bool] | None:
        """Stand `preferred_distance_m` from the nearest enemy on the field, behind the line."""
        foes = self._field[1 - p.team]
        want = self.pref.get(style_, 5.5)
        if not foes:
            tx = self._behind_line(p, self.x[p.pid] + self.fwd(p.team) * 100, style_)
            return tx, self.y[p.pid], False
        q = self.nearest(p, foes)
        d = self.distance(p, q)
        if abs(d - want) < 0.5 and self._behind_line(p, self.x[p.pid], style_) == self.x[p.pid]:
            return None
        if d < 1e-6:
            dx, dy = -self.fwd(p.team), 0.0
        else:
            dx, dy = (self.x[p.pid] - self.x[q.pid]) / d, (self.y[p.pid] - self.y[q.pid]) / d
        tx, ty = self.x[q.pid] + dx * want, self.y[q.pid] + dy * want
        return self._behind_line(p, tx, style_), ty, False

    def _helpable(self, p: Player, kind: str) -> Player | None:
        """The nearest teammate a medic or enchanter would walk to."""
        g = self.g
        t = g.t
        if kind == "medic":
            revive = any(u.available() and u.ability.effects_of("life.revive")
                         and "after-dying" not in u.ability.requirements for u in p.uses.values())
            heal = any(u.available() and u.ability.effects_of("wound.heal") and u.range != "Self"
                       for u in p.uses.values())
            if not heal and not revive:
                return None
            cands = [q for q in g.players if q.team == p.team and q is not p and (
                (heal and q.alive and q.wounds and q.on_field(t) and q.target is None and q.pid not in self._attacked)
                or (revive and not q.alive and not q.out))]
        else:
            if not any(u.available() and u.ability.delivery == "enchantment" and u.range not in ("Self", "")
                       for u in p.uses.values()):
                return None
            cands = [q for q in g.players if q.team == p.team and q is not p and q.alive and q.on_field(t)
                     and q.target is None and q.magical_enchantment_count() < q.ench_slots]
        return self.nearest(p, cands)

    def _want(self, p: Player) -> tuple[float, float, bool] | None:
        """(x, y, urgent) where p wants to be, or None to stand. Urgent moves are at a run."""
        g = self.g
        pid = p.pid
        s = self.style[pid]
        if p.target is not None:
            q = g.players[p.target]
            if self.distance(p, q) > self.reach[pid]:
                return self.x[q.pid], self.y[q.pid], True
            return None
        if pid in self._attacked:
            return None
        if pid in self._held and not self.retreating(p):
            return None               # standing still for a teammate's Touch incantation
        if s == "line":
            goal = None
            if p.kept_away_until <= g.t and not g.barred(p, "wield-weapons") and g.weapon_usable(p):
                near = self.nearest(p, self._chargeable[1 - p.team])
                if near is not None and self.distance(p, near) <= self.charge_m:
                    goal = self._goal(p)
            self.goal[pid] = goal.pid if goal is not None else None
            if goal is not None:
                return self.x[goal.pid], self.y[goal.pid], True
            line = self._line[p.team]
            return self.x_of(self.line_u[p.team], p.team), self._slot_y(self._slot[p.team][pid], len(line)), False
        q = self.nearest(p, self._threats_near(p, self.retreat_m)) if self.retreating(p) else None
        if q is not None:
            x, y, _ = self.move_away(p, self.x[q.pid], self.y[q.pid], 10.0)
            return x, y, True
        if s in ("medic", "enchanter"):
            q = self._helpable(p, s)
            if q is not None:
                if self.distance(p, q) <= 0.8 * self.touch_m:
                    return None
                return self.x[q.pid], self.y[q.pid], True
        return self._keep_distance(p, s)

    def move(self) -> None:
        g = self.g
        t = g.t
        dt = self.tick_seconds
        self._update_lines()
        self._tick_context()
        nx, ny = list(self.x), list(self.y)
        for p in g.players:
            if not p.alive or p.at_base_until > t:
                continue
            cap = self._speed_cap(p)
            if cap <= 0:
                continue
            want = self._want(p)
            if want is None:
                continue
            tx, ty, urgent = want
            nx[p.pid], ny[p.pid], step = self.move_toward(p, tx, ty, min(cap, self.run if urgent else self.walk) * dt)
            self.moved_m[p.pid] += step
        self.x, self.y = nx, ny
        self._d = None
        if self._respawned:
            for pid, since in list(self._respawned.items()):
                p = g.players[pid]
                if not p.alive:
                    del self._respawned[pid]
                    continue
                row = self._matrix()[pid]
                if any(g.targetable(q) and row[q.pid] <= 50 * FOOT for q in self._field[1 - p.team]):
                    self.rejoins.append(t - since)
                    del self._respawned[pid]

    # ------------------------------------------------------------ engagement from proximity

    def engage(self) -> None:
        """Who fights whom, from where they stand. A pair stays engaged while within the longer of
        their two reaches (plus half a metre); an attacked player strikes back at the nearest
        attacker; a line fighter engages its goal, or else the nearest enemy, within its reach."""
        g = self.g
        t = g.t
        players = g.players
        by_target: dict[int, set] = {}          # target pid -> pids of living players attacking them
        for q in players:
            if q.alive and q.target is not None:
                by_target.setdefault(q.target, set()).add(q.pid)

        def retarget(p: Player, new: int | None) -> None:
            if p.target is not None and p.alive:
                by_target.get(p.target, set()).discard(p.pid)
            p.target = new
            if new is not None and p.alive:
                by_target.setdefault(new, set()).add(p.pid)

        order = list(players)
        g.rng.shuffle(order)
        for p in order:
            if not p.can_act(t) or not p.on_field(t) or g.barred(p, "wield-weapons") or p.weapon_hot_until > t:
                retarget(p, None)
                continue
            if p.target is not None:
                q = players[p.target]
                if not g.targetable(q) or not g.can_attack(p, q) \
                        or self.distance(p, q) > max(self.reach[p.pid], self.reach[q.pid]) + 0.5:
                    retarget(p, None)
                continue
            if p.casting is not None or p.kept_away_until > t:
                continue
            attackers = [players[a] for a in sorted(by_target.get(p.pid, ()))]
            attackers = [q for q in attackers if g.targetable(q) and g.can_attack(p, q)]
            if attackers:
                retarget(p, self.nearest(p, attackers).pid)
                continue
            if self.style[p.pid] != "line":
                continue
            row = self._matrix()[p.pid]
            r = self.reach[p.pid]
            foes = [q for q in players if q.team != p.team and row[q.pid] <= r and g.targetable(q)
                    and q.kept_away_until <= t and g.can_attack(p, q) and not self.in_base(q)]
            if not foes:
                continue
            goal = self.goal[p.pid]
            pick = next((q for q in foes if q.pid == goal), None) or self.nearest(p, foes)
            retarget(p, pick.pid)
