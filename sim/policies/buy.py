"""How a player builds a loadout (called from sim/engine/loadout.py): what a Magic User buys with
magic points, and which Archetype, if any, a 6th-level martial player takes.

A Magic User builds to a plan, a **doctrine** (sim/data/doctrines.json, loaded by
sim/rules/doctrines.py), not to whatever scores well alone. Much of a caster's list exists to help
fighters: Enchantments that arm or armor teammates, control that locks enemies down for a teammate
to kill.

1. **Doctrine.** Below 6th level a caster draws a base doctrine by `share`. At 6th level each
   Archetype doctrine is drawn by its `share_at_6` (0.4 in total per class) and the rest draw a
   base doctrine by `share` (`draw_doctrine`). The doctrine is recorded on the Player
   (`doctrine`, `play`, `combos`) and in the `players` table.
2. **Archetype first.** An Archetype doctrine buys its Archetype before anything else, and the
   rest of the list obeys its purchase restrictions and cost changes.
3. **Core, in order.** Each core entry is bought up to its listed copies, skipping entries above
   the player's level, forbidden by the Archetype, ablated, or disliked: a player skips a core entry
   when their taste for it is in the bottom `DOCTRINE_WEIGHTS["core_skip_share"]`. Core entries are
   bought even when the engine models nothing about them (a weapon, Ambulant): the plan pays for
   them in points.
4. **Fill, as before.** Candidates are spells the class can buy at this level with at least one
   effect that helps the user's side in the engine (`effective`). Free spells (Priest's Heal) are
   taken at their Max. A few favorites (one at 1st level, growing to `loadout.favorite_spells` at
   6th), drawn uniformly among the candidates the doctrine doesn't avoid, get one copy. Then the
   player buys greedily by score per point, each further copy scoring 0.6 of the previous one, up
   to the spell's Max (or `loadout.magic_user_copy_cap`). The score is the usefulness score
   (benefits minus drawbacks, `sim/policies/value.py`), doubled for an Unlimited ability that isn't
   ammunition, times the player's taste (log-normal, sd `loadout.spell_taste_sd`, drawn once per
   player and spell; for core spells `taste ** DOCTRINE_WEIGHTS["core_taste"]`, so taste varies
   them less), times the doctrine weight (`doctrine_weight`): ×1.6 for a preferred or core spell,
   ×0.25 for an avoided one, ×1.25 when the spell's metadata roles match the stance
   (`STANCE_ROLES`). All of these are the `DOCTRINE_WEIGHTS` dict.
5. **Martial Archetypes, by value.** A 6th-level martial player who considers an Archetype at all
   (`loadout.archetype_share`) compares each Archetype's gain for their own kit (`archetype_gain`:
   the armor Berserker would take away, the abilities it removes) with taking none.

Every random draw happens in a fixed order for every entry on the class list, whether or not it is
a candidate, and the doctrine draw comes last; ablating a spell changes no draw. An ablated core
spell is skipped and its points are spent in the fill step; an ablated Archetype leaves the player
on the same doctrine without it (paired ablations stay aligned).
"""
from __future__ import annotations

import heapq
import math
import random
from statistics import NormalDist
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


# How a doctrine changes what a Magic User buys (see the module docstring). One dict, so the
# weights are easy to find and change; sim/analyze/doctrines.py reports what they produce.
DOCTRINE_WEIGHTS = {
    "prefer": 1.6,           # fill-step score of a spell on the doctrine's prefer list (core spells count too)
    "avoid": 0.25,           # fill-step score of a spell on its avoid list
    "stance": 1.25,          # fill-step score of a spell whose metadata roles match the stance (STANCE_ROLES)
    "core_taste": 0.5,       # a core spell's taste factor is taste ** this: half the spread on the log scale
    "core_skip_share": 0.1,  # a player skips a core entry when their taste for it is in the bottom 10%
}
# Metadata roles (metadata/abilities.json "roles") that fit each stance in sim/data/doctrines.json.
STANCE_ROLES = {
    "offense": frozenset({"offense"}),
    "control": frozenset({"control", "debuff"}),
    "support": frozenset({"defense", "team", "resource"}),
    "sustain": frozenset({"healing", "revival"}),
    "hybrid": frozenset({"defense", "equipment"}),
}


def draw_doctrine(docs, level: int, u: float):
    """The doctrine for a uniform draw u in [0, 1). Below 6th level: a base doctrine by `share`.
    At 6th: each Archetype doctrine by its `share_at_6`, the remainder a base doctrine by `share`."""
    base = [d for d in docs if d.archetype is None and d.share > 0]
    if level >= 6:
        acc = 0.0
        for d in (d for d in docs if d.archetype is not None):
            acc += d.share_at_6
            if u < acc:
                return d
        u = (u - acc) / (1.0 - acc) if acc < 1.0 else 0.0
    total = sum(d.share for d in base)
    acc = 0.0
    for d in base:
        acc += d.share / total
        if u < acc:
            return d
    return base[-1] if base else None


def _taste_z(taste: float, rules: "Rules") -> float:
    sd = rules.a("loadout.spell_taste_sd")
    return math.log(taste) / sd if sd > 0 else 0.0


def choose(cands: list["ClassAbility"], level: int, role: str, pools: dict[int, int], rules: "Rules",
           rng: random.Random, ablate: frozenset = frozenset(),
           purchase_rules: PurchaseRules | None = None, cls: str | None = None):
    """(copies bought per slug, the Archetype included; the Doctrine or None). `cands` is the
    class's purchasable list (spells and Archetypes with a cost); `pools` maps level -> points and
    is not modified. `purchase_rules(arch)` gives an Archetype's (cost, allowed) functions over
    class-table entries. A class with no doctrines (or `cls` None) gets a plain greedy build."""
    # draws for every listed entry, in slug order, before anything is filtered, then one for the
    # doctrine: the same draws whatever is ablated
    ordered = sorted(cands, key=lambda c: (c.slug, c.kind))
    taste = _draw_tastes(ordered, rules, rng)
    fav_key = {c.slug: rng.random() for c in ordered}
    pick = rng.random()
    docs = rules.doctrines.by_class.get(cls, ()) if cls else ()
    doctrine = draw_doctrine(docs, level, pick) if docs else None

    by_slug = {c.slug: c for c in ordered if c.kind != "archetype"}
    arch = None
    if doctrine is not None and doctrine.archetype and doctrine.archetype not in ablate and level >= 6:
        arch = next((c for c in ordered if c.kind == "archetype" and c.slug == doctrine.archetype
                     and min(c.levels) <= level), None)
    cost, allowed = (purchase_rules(arch.slug) if (arch is not None and purchase_rules)
                     else (lambda c: c.cost, lambda c: True))

    def eligible(c: "ClassAbility") -> bool:
        ab = rules.abilities.get(c.slug)
        return ab is not None and c.slug not in ablate and min(c.levels) <= level and effective(ab, rules)

    spells = [c for c in ordered if c.kind != "archetype" and eligible(c) and allowed(c)]
    core: list = []
    if doctrine is not None:
        skip_z = NormalDist().inv_cdf(DOCTRINE_WEIGHTS["core_skip_share"])
        for slug, n in doctrine.core:
            c = by_slug.get(slug)
            # the plan is bought even where the engine models nothing (a weapon, Ambulant): it is
            # what the player pays for; the fill step below only buys what the engine uses
            if c is None or slug in ablate or min(c.levels) > level or not allowed(c) \
                    or slug not in rules.abilities or _taste_z(taste[slug], rules) < skip_z:
                continue
            core.append((c, n))
    bought, _ = _build(arch, spells, cost, dict(pools), role, rules, taste, fav_key, level,
                       doctrine=doctrine, core=core)
    return bought, doctrine


def favorites(level: int, rules: "Rules") -> int:
    """Favorite spells grow with level: one at 1st, `loadout.favorite_spells` at 6th."""
    return max(1, round(rules.a("loadout.favorite_spells") * level / 6))


def doctrine_weight(slug: str, doctrine, rules: "Rules") -> float:
    """The doctrine's multiplier on a spell's fill-step score (DOCTRINE_WEIGHTS)."""
    if doctrine is None:
        return 1.0
    w = 1.0
    if slug in doctrine.prefer or any(s == slug for s, _ in doctrine.core):
        w *= DOCTRINE_WEIGHTS["prefer"]
    if slug in doctrine.avoid:
        w *= DOCTRINE_WEIGHTS["avoid"]
    ab = rules.abilities.get(slug)
    if ab is not None and ab.roles & STANCE_ROLES.get(doctrine.stance, frozenset()):
        w *= DOCTRINE_WEIGHTS["stance"]
    return w


def _build(arch, spells: list, cost, pools: dict[int, int], role: str, rules: "Rules",
           taste: dict[str, float], fav_key: dict[str, float], level: int = 6,
           doctrine=None, core: list = ()) -> tuple[dict[str, int], float]:
    """One build: the Archetype (if any) paid first, then the doctrine's core entries in order
    (each up to its copies), then free spells, favorites and a greedy fill by score per point.
    Returns (bought, total score)."""
    bought: dict[str, int] = {}
    total = 0.0
    core_slugs = {c.slug for c, _ in core} | ({s for s, _ in doctrine.core} if doctrine else set())

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
        t = taste[c.slug] ** DOCTRINE_WEIGHTS["core_taste"] if c.slug in core_slugs else taste[c.slug]
        return value(rules.abilities[c.slug], role) * freq * t * doctrine_weight(c.slug, doctrine, rules)

    for c, n in core:
        for _ in range(n - bought.get(c.slug, 0)):
            if not pay(c, max(worth(c), 0.0) * COPY_DECAY ** bought.get(c.slug, 0)):
                break
    for c in [c for c in spells if cost(c) == 0 and worth(c) > 0]:   # free: take them all
        n = c.max if c.max is not None else cap
        bought[c.slug] = n
        total += sum(worth(c) * COPY_DECAY ** k for k in range(n))
    paid = [c for c in spells if cost(c) > 0]
    liked = [c for c in paid if doctrine is None or c.slug not in doctrine.avoid]
    for c in sorted(liked, key=lambda c: fav_key[c.slug])[:favorites(level, rules)]:
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
