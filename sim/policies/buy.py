"""How a player builds a loadout (called from sim/engine/loadout.py): what a Magic User buys with
magic points, and which Archetype, if any, a 6th-level player takes.

A real Magic User builds around what they think is useful, and two players of the same class and
level rarely buy the same list:

1. **Candidates.** Spells and equipment the class can buy at this level with at least one effect
   that helps the user's side in the engine (`effective`). Abilities that would do nothing, or
   only harm the buyer (Battlemage bought for its restriction), are never bought.
2. **Favorites.** Each player has a few favorites (one at 1st level, growing to
   `loadout.favorite_spells` at 6th, as the list of spells to like grows), drawn uniformly among
   their candidates, and buys one copy of each first: the spell a player builds around because
   they like it, whatever the usefulness score says (Contagion, whose Fragile drawback the score
   weighs above its benefit, is still somebody's favorite).
3. **Taste, then greedy.** Each candidate whose usefulness score (benefits minus drawbacks,
   `sim/policies/value.py`) is positive is scored, doubled for an Unlimited ability that isn't
   ammunition (Heal, Bardic songs: one purchase is worth what several copies of a 1/Life spell
   would be), is multiplied by a personal taste factor drawn once per player and spell
   (log-normal, sd `loadout.spell_taste_sd`). The player buys greedily by score per point, each
   further copy of a spell scoring 0.6 of the previous one, up to the spell's Max (or
   `loadout.magic_user_copy_cap`). A spell that costs nothing (Priest's Heal) is taken at its Max.
4. **Archetype, by value.** At 6th level a player who considers an Archetype at all
   (`loadout.archetype_share`) builds the best list without one and under each Archetype the
   class offers (paying for it, and obeying its purchase restrictions and cost changes), adds
   what the Archetype itself gives (`archetype_gain`, times the player's taste for it), and keeps
   the best total. An Archetype that makes the build worse is not taken. Martial players compare
   each Archetype's gain for their own kit (the armor Berserker would take away, the abilities it
   removes) with taking none.

Every random draw happens for every entry on the class list in a fixed order, whether or not it
is a candidate, so ablating one spell changes no other player's draws (paired ablations stay
aligned).
"""
from __future__ import annotations

import heapq
import math
import random
from types import SimpleNamespace
from typing import TYPE_CHECKING, Callable

from sim.engine import effects as fx
from sim.engine.effects import is_handled
from sim.policies.value import (DRAWBACK_WEIGHT, EQUIPMENT_WEIGHT, effect_benefit, is_drawback,
                                restrict_cost, value)

if TYPE_CHECKING:
    from sim.engine.state import Player
    from sim.rules.compile import Ability, ClassAbility, Rules

COPY_DECAY = 0.6
UNLIMITED_FACTOR = 2.0
# Loadout effects that act on another named ability: they do something only if that ability does.
_NAMED = {"ability.grant": "ability", "ability.modify": "ability", "ability.remove": "ability",
          "economy.frequency": "scope"}
CHARGE_GAIN = 0.3      # a use that can be Charged back is worth 30% more


def _frequency_gain(change: str, copies: int) -> float:
    """A frequency change to an ability held `copies` times, in units of that ability's value and
    on the same scale as the build score (copy k is worth COPY_DECAY ** k): doubling adds copies
    n..2n-1, Unlimited is worth what an Unlimited purchase is, a Charge adds CHARGE_GAIN."""
    held = sum(COPY_DECAY ** k for k in range(copies))
    if "unlimited" in change:
        return (UNLIMITED_FACTOR - 1.0) * held
    if "double" in change:
        return sum(COPY_DECAY ** k for k in range(copies, 2 * copies))
    if "charge" in change:
        return CHARGE_GAIN * held
    return 0.0

PurchaseRules = Callable[[str], tuple[Callable, Callable]]   # archetype slug -> (cost(c), allowed(c))


def effective(ab: "Ability", rules: "Rules") -> bool:
    """At least one effect the engine executes that helps the user's side. Drawbacks don't count
    (Battlemage's purchase restriction alone is no reason to buy it), and neither does an effect
    that only modifies an ability the engine can't use."""
    for e in ab.effects:
        if not is_handled(ab, e) or is_drawback(ab, e):
            continue
        key = _NAMED.get(e.kind) if ab.delivery in ("archetype", "trait") else None
        if key is None:
            return True
        scope = str(e.params.get(key, ""))
        if e.kind == "economy.frequency" and scope in fx.FREQUENCY_GROUPS:
            return True
        slug = rules.by_name.get(scope.lower())
        if slug and slug != ab.slug and effective(rules.abilities[slug], rules):
            return True
    return False


def _frequency_targets(e, rules: "Rules", owned: dict[str, int]) -> list[str]:
    key = _NAMED.get(e.kind, "ability")
    scope = str(e.params.get(key, ""))
    group = fx.FREQUENCY_GROUPS.get(scope)
    if group is not None:
        return [s for s in owned if group(SimpleNamespace(purchased=True, ability=rules.abilities[s]))]
    slug = rules.by_name.get(scope.lower())
    return [slug] if slug in owned else []


def archetype_gain(arch: "Ability", rules: "Rules", role: str, owned: dict[str, int],
                   p: "Player | None" = None) -> float:
    """What an Archetype adds to a player who holds `owned` (slug -> copies): abilities it grants,
    frequency changes to abilities held, minus its drawbacks for this player. Purchase
    restrictions and cost changes are not counted here; the Magic User buyer prices them by
    rebuilding the list."""
    gain = 0.0
    best: dict[str, float] = {}    # a frequency change is often recorded twice; count it once
    equipment = 0.0
    for e in arch.effects:
        if not is_handled(arch, e):
            continue
        if is_drawback(arch, e):
            if e.kind in ("economy.purchase-restrict", "economy.cost"):
                continue
            if e.kind == "action.restrict":
                gain -= restrict_cost(str(e.params.get("what", "")), role, p)
            elif e.kind == "ability.remove":
                slug = rules.by_name.get(str(e.params.get("ability", "")).lower())
                gain -= value(rules.abilities[slug], role) if slug in owned else 0.0
            else:
                gain -= DRAWBACK_WEIGHT.get(e.kind, 1)
            continue
        if e.kind == "ability.grant":
            slug = rules.by_name.get(str(e.params.get("ability", "")).lower())
            if slug:
                unlimited = "unlimited" in str(e.params.get("frequency", "")).lower()
                gain += value(rules.abilities[slug], role) * (UNLIMITED_FACTOR if unlimited else 1.0)
        elif e.kind in ("economy.frequency", "ability.modify"):
            change = str(e.params.get("change", "")).lower()
            for slug in _frequency_targets(e, rules, owned):
                v = value(rules.abilities[slug], role) * _frequency_gain(change, owned[slug])
                best[slug] = max(best.get(slug, 0.0), v)
        elif e.kind == "equipment.permit":
            equipment = max(equipment, EQUIPMENT_WEIGHT.get(str(e.params.get("what", "")), 0.0))
        elif e.kind not in ("economy.cost", "ability.range-change", "class.look-the-part"):
            gain += effect_benefit(arch, e, role)
    return gain + sum(best.values()) + equipment


def _draw_tastes(entries: list, rules: "Rules", rng: random.Random) -> dict[str, float]:
    sd = rules.a("loadout.spell_taste_sd")
    return {c.slug: math.exp(sd * rng.gauss(0.0, 1.0)) for c in entries}


def choose(cands: list["ClassAbility"], level: int, role: str, pools: dict[int, int], rules: "Rules",
           rng: random.Random, ablate: frozenset = frozenset(),
           purchase_rules: PurchaseRules | None = None) -> dict[str, int]:
    """Copies bought per slug, the Archetype included. `cands` is the class's purchasable list
    (spells and Archetypes with a cost); `pools` maps level -> points and is not modified.
    `purchase_rules(arch)` gives an Archetype's (cost, allowed) functions over class-table entries."""
    # draws for every listed entry, in slug order, before anything is filtered
    ordered = sorted(cands, key=lambda c: (c.slug, c.kind))
    taste = _draw_tastes(ordered, rules, rng)
    fav_key = {c.slug: rng.random() for c in ordered}
    consider_archetype = rng.random() < rules.a("loadout.archetype_share")

    def eligible(c: "ClassAbility") -> bool:
        ab = rules.abilities.get(c.slug)
        return ab is not None and c.slug not in ablate and min(c.levels) <= level and effective(ab, rules)

    spells = [c for c in ordered if c.kind != "archetype" and eligible(c)]
    options: list = [None]
    if level >= 6 and consider_archetype:
        options += [c for c in ordered if c.kind == "archetype" and eligible(c)]

    best, best_score = {}, -math.inf
    for arch in options:
        cost, allowed = (purchase_rules(arch.slug) if (arch is not None and purchase_rules)
                         else (lambda c: c.cost, lambda c: True))
        bought, score = _build(arch, [c for c in spells if allowed(c)], cost, dict(pools), role, rules,
                               taste, fav_key, level)
        if arch is not None:
            if not bought.get(arch.slug):
                continue
            score += archetype_gain(rules.abilities[arch.slug], rules, role, bought) * taste[arch.slug]
        if score > best_score + 1e-9:
            best, best_score = bought, score
    return best


def favorites(level: int, rules: "Rules") -> int:
    """Favorite spells grow with level: one at 1st, `loadout.favorite_spells` at 6th."""
    return max(1, round(rules.a("loadout.favorite_spells") * level / 6))


def _build(arch, spells: list, cost, pools: dict[int, int], role: str, rules: "Rules",
           taste: dict[str, float], fav_key: dict[str, float], level: int = 6) -> tuple[dict[str, int], float]:
    """One greedy build (optionally under an Archetype, paid first). Returns (bought, total score)."""
    bought: dict[str, int] = {}
    total = 0.0

    def pay(c, worth: float) -> bool:
        nonlocal total
        due = cost(c)
        eligible = sorted(l for l in pools if l >= min(c.levels))
        if sum(pools[l] for l in eligible) < due:
            return False
        for l in eligible:
            take = min(due, pools[l])
            pools[l] -= take
            due -= take
            if due == 0:
                break
        bought[c.slug] = bought.get(c.slug, 0) + 1
        total += worth
        return True

    if arch is not None and not pay(arch, 0.0):
        return {}, -math.inf

    cap = rules.a("loadout.magic_user_copy_cap")

    def worth(c) -> float:
        freq = UNLIMITED_FACTOR if (c.freq.per == "unlimited" and not c.freq.unit) else 1.0
        return value(rules.abilities[c.slug], role) * freq * taste[c.slug]

    for c in [c for c in spells if cost(c) == 0 and worth(c) > 0]:   # free: take them all
        n = c.max if c.max is not None else cap
        bought[c.slug] = n
        total += sum(worth(c) * COPY_DECAY ** k for k in range(n))
    paid = [c for c in spells if cost(c) > 0]
    for c in sorted(paid, key=lambda c: fav_key[c.slug])[:favorites(level, rules)]:
        if not bought.get(c.slug):
            pay(c, max(worth(c), 0.0))

    heap = []
    for i, c in enumerate(c for c in paid if worth(c) > 0):
        heapq.heappush(heap, (-worth(c) / cost(c), c.slug, i, c))
    while heap:
        negv, slug, i, c = heapq.heappop(heap)
        n = bought.get(slug, 0)
        if n >= (c.max if c.max is not None else cap):
            continue
        if pay(c, worth(c) * COPY_DECAY ** n):
            heapq.heappush(heap, (negv * COPY_DECAY, slug, i, c))
    return bought, total


def choose_archetype(p: "Player", options: list[str], rules: "Rules", rng: random.Random,
                     ablate: frozenset = frozenset()) -> str | None:
    """A 6th-level martial player's Archetype: the one that adds most to their own kit, or none if
    none adds anything. Draws the same numbers whatever is ablated."""
    options = sorted(options)
    consider = rng.random() < rules.a("loadout.archetype_share")
    taste = _draw_tastes([SimpleNamespace(slug=s) for s in options], rules, rng)
    if not consider:
        return None
    owned = {s: 1 for s in p.uses} | {t.slug: 1 for t in p.traits}
    best, best_gain = None, 0.0
    for slug in options:
        ab = rules.abilities.get(slug)
        if ab is None or slug in ablate or not effective(ab, rules):
            continue
        g = archetype_gain(ab, rules, p.role, owned, p) * taste[slug]
        if g > best_gain:
            best, best_gain = slug, g
    return best
