"""How a Magic User spends magic points (called from sim/engine/loadout.py).

A real Magic User builds around what they think is useful, and two players of the same class and
level rarely buy the same list. The buyer models that in three steps:

1. **Candidates.** Spells and equipment the class can buy at this level whose effects the engine
   actually executes (`effective`). Abilities that would do nothing in the simulation are never
   bought: that would be a wasted point, not a build.
2. **Archetype.** At 6th level, with the same chance as martial classes
   (`loadout.archetype_share`), the player takes one Archetype, uniformly among the effective
   ones, and pays for it first. Never more than one.
3. **Favorites.** Each player has `loadout.favorite_spells` favorites, drawn uniformly among
   their candidates, and buys one copy of each first: the spell a player builds around because
   they like it, whatever the usefulness score says.
4. **Taste, then greedy.** Each candidate's usefulness score (`sim/policies/value.py`), doubled
   for an Unlimited ability that isn't ammunition (Heal, Bardic songs: one purchase is worth what
   several copies of a 1/Life spell would be), is multiplied by a personal taste factor drawn once per player and spell (log-normal, sd
   `loadout.spell_taste_sd`). The player then buys greedily by score per point, each further
   copy of a spell scoring 0.6 of the previous one, up to the spell's Max (or
   `loadout.magic_user_copy_cap`).

Every random draw happens for every spell on the class list in a fixed order, whether or not the
spell is a candidate, so ablating one spell changes no other player's draws (paired ablations
stay aligned).
"""
from __future__ import annotations

import heapq
import math
import random
from typing import TYPE_CHECKING

from sim.engine.effects import is_handled
from sim.policies.value import value

if TYPE_CHECKING:
    from sim.rules.compile import Ability, ClassAbility, Rules

COPY_DECAY = 0.6
UNLIMITED_FACTOR = 2.0
# Loadout effects that act on another named ability: they do something only if that ability does.
_NAMED = {"ability.grant": "ability", "ability.modify": "ability", "ability.remove": "ability",
          "economy.frequency": "scope"}


def effective(ab: "Ability", rules: "Rules") -> bool:
    """At least one effect the engine executes that changes play. An Archetype whose only handled
    effects modify abilities the engine can't use (Battlemage and Ambulant, Evoker and Elemental
    Barrage) is inert here."""
    for e in ab.effects:
        if not is_handled(ab, e):
            continue
        key = _NAMED.get(e.kind) if ab.delivery in ("archetype", "trait") else None
        if key is None:
            return True
        slug = rules.by_name.get(str(e.params.get(key, "")).lower())
        if slug and slug != ab.slug and effective(rules.abilities[slug], rules):
            return True
    return False


def choose(cands: list["ClassAbility"], level: int, role: str, pools: dict[int, int], rules: "Rules",
           rng: random.Random, ablate: frozenset = frozenset()) -> dict[str, int]:
    """Copies bought per slug. `cands` is the class's purchasable list (spells and Archetypes with
    a cost); `pools` maps level -> points and is spent in place."""
    sd = rules.a("loadout.spell_taste_sd")
    # draws for every listed ability, in slug order, before anything is filtered
    ordered = sorted(cands, key=lambda c: (c.slug, c.kind))
    taste = {c.slug: math.exp(sd * rng.gauss(0.0, 1.0)) for c in ordered}
    fav_key = {c.slug: rng.random() for c in ordered}
    take_archetype = rng.random() < rules.a("loadout.archetype_share")
    arch_pick = rng.random()

    def ok(c: "ClassAbility") -> bool:
        ab = rules.abilities.get(c.slug)
        return (ab is not None and c.slug not in ablate and min(c.levels) <= level
                and value(ab, role) > 0 and effective(ab, rules))

    usable = [c for c in ordered if ok(c)]
    bought: dict[str, int] = {}

    def pay(c: "ClassAbility") -> bool:
        eligible = sorted(l for l in pools if l >= min(c.levels))
        if sum(pools[l] for l in eligible) < c.cost:
            return False
        due = c.cost
        for l in eligible:
            take = min(due, pools[l])
            pools[l] -= take
            due -= take
            if due == 0:
                break
        bought[c.slug] = bought.get(c.slug, 0) + 1
        return True

    archetypes = [c for c in usable if c.kind == "archetype"]
    if level >= 6 and archetypes and take_archetype:
        pay(archetypes[int(arch_pick * len(archetypes)) % len(archetypes)])

    spells = [c for c in usable if c.kind != "archetype"]
    for c in sorted(spells, key=lambda c: fav_key[c.slug])[:rules.a("loadout.favorite_spells")]:
        if not bought.get(c.slug):
            pay(c)

    cap = rules.a("loadout.magic_user_copy_cap")
    heap = []
    for i, c in enumerate(spells):
        freq = UNLIMITED_FACTOR if (c.freq.per == "unlimited" and not c.freq.unit) else 1.0
        score = value(rules.abilities[c.slug], role) * freq * taste[c.slug] / c.cost
        heapq.heappush(heap, (-score, c.slug, i, c))
    while heap:
        negv, slug, i, c = heapq.heappop(heap)
        if bought.get(slug, 0) >= (c.max if c.max is not None else cap):
            continue
        if pay(c):
            heapq.heappush(heap, (negv * COPY_DECAY, slug, i, c))
    return bought
