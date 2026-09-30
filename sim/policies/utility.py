"""Situational utility: what an ability is worth *now*, in this game state, to this caster and
target. The rest of the policies use the fixed usefulness score in `value.py`, which is the same
whatever is happening on the field.

This is a pilot, used only by the Bardic songs (`sim/policies/songs.py`). The pattern is meant to
extend to other abilities one at a time:

    @register("song-of-battle")
    def _battle(g, caster, target) -> float: ...

    utility(g, caster, ability, target)     # None when the ability has no utility function

**Units.** A utility is in *threat units*: the enemies (or teammates) the ability acts against or
for, each weighted by how likely it is to matter to the target soon (`reach`). So utilities of
different abilities can be compared with each other. Where a policy has to weigh a utility against
a fixed value.py score, `value_of` converts seconds of utility into value points at the rate
`policy.value_per_threat_second` (sim/data/assumptions.json).

Utility functions must not draw from the game's random stream: they are read many times a tick and
must not change the play. Results are cached for the tick in `Game.policy_cache`.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from sim.engine.game import Game
    from sim.engine.state import Player
    from sim.rules.compile import Ability

UtilityFn = Callable[["Game", "Player", "Player | None"], float]
UTILITY: dict[str, UtilityFn] = {}


def register(*slugs: str):
    """Decorator: the utility function for these abilities."""
    def wrap(fn: UtilityFn) -> UtilityFn:
        for s in slugs:
            UTILITY[s] = fn
        return fn
    return wrap


def has_utility(ability: "Ability") -> bool:
    return ability.slug in UTILITY


def utility(g: "Game", caster: "Player", ability: "Ability", target: "Player | None" = None) -> float | None:
    """The ability's situational utility for this caster and target now, or None if it has none
    (the caller falls back to the fixed score)."""
    fn = UTILITY.get(ability.slug)
    if fn is None:
        return None
    key = ("utility", ability.slug, caster.pid, target.pid if target is not None else None)
    v = g.policy_cache.get(key)
    if v is None:
        v = g.policy_cache[key] = float(fn(g, caster, target))
    return v


def cached(g: "Game", key: tuple, fn: Callable[[], object]):
    """Compute once per tick (Game.policy_cache is cleared every step)."""
    v = g.policy_cache.get(key)
    if v is None:
        v = g.policy_cache[key] = fn()
    return v


def value_of(g: "Game", threat_seconds: float) -> float:
    """Value points (value.py's scale) of this many threat-unit seconds of utility."""
    return threat_seconds * g.rules.a("policy.value_per_threat_second")


# ---------------------------------------------------------------- shared weights

def living(players) -> list["Player"]:
    return [q for q in players if q.alive and not q.out]


def in_melee(p: "Player", q: "Player") -> bool:
    return p.target == q.pid or q.target == p.pid


def engaged(g: "Game", q: "Player") -> bool:
    """In melee with anyone (q attacking, or attacked)."""
    return q.target is not None or bool(cached(g, ("attacked", q.pid), lambda: bool(g.attackers_of(q))))


def reach(g: "Game", p: "Player", q: "Player") -> float:
    """How likely enemy q is to cast or shoot at p soon: 0 while q is in melee (engaged players
    start no incantation at range and don't shoot, `casting.engaged_casting_allowed`), otherwise
    1 / (p's living teammates, p included), q's chance of picking p among them. A threat in melee
    is counted by the ability's own utility (attackers on p, p's melee target)."""
    if engaged(g, q):
        return 0.0
    n = cached(g, ("mates", p.team), lambda: len(living(g.allies(p))))
    return 1.0 / max(1, n)
