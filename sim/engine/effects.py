"""Effect handlers, keyed by the metadata's effect `kind`.

Three kinds of handling:
  INSTANT  - run when an ability resolves (on-cast, on-struck, on-kill, on-death, on-expiry timings)
  PASSIVE  - `while-active` effects of Enchantments, Traits and Archetypes; the engine queries them
  LOADOUT  - Archetype/Trait effects applied once when a player's loadout is built

Anything else is a logged no-op: the engine counts it per (ability, kind) and the coverage
report lists it. Nothing is dropped silently.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from sim.engine.state import ARMS, INF, LEGS, LOCATIONS, Ench, Player
from sim.rules.compile import Ability, Effect

if TYPE_CHECKING:
    from sim.engine.game import Game


@dataclass(slots=True)
class Ctx:
    ability: Ability
    caster: Player
    target: Player | None
    bearer: Player | None = None       # for enchantment/trait effects
    ench: Ench | None = None
    location: str | None = None        # struck location for balls/arrows
    specials: frozenset = frozenset()  # special effects carried by this ball/arrow


INSTANT_TIMINGS = frozenset({"on-cast", "on-struck", "on-kill", "on-death", "on-expiry"})
PASSIVE_DELIVERIES = frozenset({"enchantment", "trait", "archetype"})

HARMFUL_STATE_ORDER = ("stunned", "frozen", "stopped", "suppressed", "fragile", "insubstantial", "cursed")


def subject(eff: Effect, ctx: Ctx) -> Player | None:
    s = eff.subject
    if s in ("caster",):
        return ctx.caster
    if s in ("bearer", "bearer-equipment"):
        return ctx.bearer or ctx.target or ctx.caster
    if s == "caster-of-enchantment":
        return ctx.caster
    return ctx.target


# ---------------------------------------------------------------- instant handlers

def h_death_cause(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or not p.alive:
        return False
    g.kill(p, ctx.caster, ctx.ability.slug)
    return True


def h_wound_inflict(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or not p.alive:
        return False
    if eff.params.get("location") == "struck":
        g.hit(p, ctx.caster, ctx.ability.slug, location=ctx.location, specials=ctx.specials)
    else:  # chosen by caster (Wounding): an unwounded leg, then an arm
        loc = next((l for l in LEGS + ARMS if l not in p.wounds), "torso")
        g.wound(p, loc, ctx.caster, ctx.ability.slug, specials=ctx.specials)
    return True


def h_state_apply(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    state = eff.params.get("state")
    if p is None or not state:
        return False
    if not p.alive and state != "cursed":
        return False
    if eff.duration_type == "timed" and eff.seconds:
        g.apply_state(p, state, g.t + eff.seconds)
    elif state == "insubstantial" and p is ctx.caster and eff.duration_type in ("until-removed", "until-arrival"):
        # self-imposed Insubstantial: the policy ends it after a while (assumption)
        g.apply_state(p, state, g.t + g.rules.a("policy.self_insubstantial_seconds"))
    else:
        g.apply_state(p, state, INF)
    return True


def h_state_remove(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None:
        return False
    what = eff.params.get("what", "")
    except_ = set(eff.params.get("except") or ())
    if what == "specific-state":
        return p.states.pop(eff.params.get("state", ""), None) is not None
    harmful = [s for s in HARMFUL_STATE_ORDER if p.has_state(s, g.t) and s not in except_]
    if what in ("all-states-and-effects", "chosen-states-and-effects", "same-source-states-and-effects"):
        for s in harmful:
            p.states.pop(s, None)
        return bool(harmful)
    if harmful:
        p.states.pop(harmful[0], None)
        return True
    return False


def h_wound_heal(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or not p.wounds:
        return False
    if eff.params.get("amount") == "all":
        p.wounds.clear()
    else:
        p.wounds.discard(next(iter(sorted(p.wounds))))
    return True


def h_life_revive(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or p.alive or p.out:
        return False
    g.revive(p, ctx.caster, ctx.ability.slug)
    return True


def _worst_armor_location(p: Player) -> str | None:
    gaps = [(p.armor_max - p.armor.get(l, 0), l) for l in LOCATIONS]
    gap, loc = max(gaps)
    return loc if gap > 0 else None


def h_armor_repair(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or p.armor_max <= 0:
        return False
    amount = eff.params.get("amount", "")
    if amount in ("all-armor",):
        changed = any(p.armor[l] < p.armor_max for l in LOCATIONS)
        p.armor = {l: p.armor_max for l in LOCATIONS}
        return changed
    if amount == "one-point-each-location":
        changed = False
        for l in LOCATIONS:
            if p.armor[l] < p.armor_max:
                p.armor[l] += 1
                changed = True
        return changed
    loc = _worst_armor_location(p)
    if loc is None:
        return False
    p.armor[loc] = p.armor_max if amount == "all-points-one-location" else p.armor[loc] + 1
    return True


def h_armor_destroy(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None:
        return False
    loc = max(LOCATIONS, key=lambda l: p.armor.get(l, 0))
    if p.armor.get(loc, 0) <= 0:
        return False
    p.armor[loc] = 0
    return True


def h_armor_damage(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    loc = ctx.location or "torso"
    if p is None or p.armor.get(loc, 0) <= 0:
        return False
    p.armor[loc] = max(0, p.armor[loc] - int(eff.params.get("points", 1)))
    return True


def h_equipment_repair(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or (p.weapon_ok and p.shield_hits == 0):
        return False
    p.weapon_ok = True
    p.shield_hits = 0
    return True


def h_equipment_destroy(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None:
        return False
    if p.shield_usable():
        p.shield_hits = 3
    else:
        p.weapon_ok = False
    return True


def h_enchantment_remove(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or not p.enchantments:
        return False
    scope = eff.params.get("scope", "all")
    if scope == "all":
        keep = [e for e in p.enchantments if "cannot-be-removed" in e.ability.properties]
    elif scope in ("non-persistent", "non-persistent-others"):
        keep = [e for e in p.enchantments if e.persistent or (scope == "non-persistent-others" and e is ctx.ench)]
    else:
        return False
    removed = [e for e in p.enchantments if e not in keep]
    for e in removed:
        g.remove_enchantment(p, e)
    return bool(removed)


def h_move_to_base(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or not p.alive:
        return False
    g.send_to_base(p)
    return True


def h_move_away(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None or not p.alive:
        return False
    g.disengage(p)
    p.kept_away_until = max(p.kept_away_until, g.t + (eff.seconds or g.rules.a("policy.forced_move_seconds")))
    return True


def h_ability_charge(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None:
        return False
    spent = [u for u in p.uses.values() if u.charge and u.left is not None and u.max and u.left < u.max]
    if not spent:
        return False
    best = max(spent, key=lambda u: g.value(u.ability, p))
    best.restore(1)
    return True


def h_ability_restore(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    if p is None:
        return False
    changed = False
    for u in p.uses.values():
        if u.per == "life" and u.left is not None and u.max and u.left < u.max:
            u.left = u.max
            changed = True
    return changed


def h_spend_strip(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    if ctx.ench is None or ctx.ench.strips is None:
        return False
    ctx.ench.strips -= int(eff.params.get("n", 1))
    if ctx.ench.strips <= 0 and ctx.bearer is not None:
        g.remove_enchantment(ctx.bearer, ctx.ench)
    return True


def h_special_effect(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    # Specials on this ball/arrow are read by Game.hit through Ctx.specials; nothing else to do.
    return eff.params.get("on") in ("this-magic-ball", "this-arrow")


def h_negate_lethal(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    # The lethal event is ignored: Game.kill already stopped the death before running on-death effects.
    return eff.params.get("from") == "lethal-event"


def h_death_prevent(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    # Game.kill already chose to prevent the death before running the on-death effects.
    return True


INSTANT: dict[str, Callable] = {
    "death.prevent": h_death_prevent,
    "death.cause": h_death_cause,
    "wound.inflict": h_wound_inflict,
    "state.apply": h_state_apply,
    "state.remove": h_state_remove,
    "wound.heal": h_wound_heal,
    "life.revive": h_life_revive,
    "armor.repair": h_armor_repair,
    "armor.destroy": h_armor_destroy,
    "armor.damage": h_armor_damage,
    "equipment.repair": h_equipment_repair,
    "equipment.destroy": h_equipment_destroy,
    "enchantment.remove": h_enchantment_remove,
    "enchantment.spend-strip": h_spend_strip,
    "move.to-base": h_move_to_base,
    "move.push": h_move_away,
    "move.keep-away": h_move_away,
    "move.to-location": h_move_away,
    "move.to-caster": h_move_away,
    "ability.charge": h_ability_charge,
    "ability.restore-uses": h_ability_restore,
    "special-effect.grant": h_special_effect,
    "defense.negate-hit": h_negate_lethal,
}

# while-active effects the engine reads directly from worn Enchantments, Traits and Archetypes.
PASSIVE = frozenset({
    "armor.magic",              # Game.attach_enchantment adds Magic Armor points
    "defense.immunity",         # Game.immune
    "defense.resistance",       # Game.consume_resistance
    "defense.negate-hit",       # Game.hit (Ancestral Armor, Gift of Air, Missile Block)
    "defense.unaffected",       # Game.unaffected
    "death.prevent",            # Game.kill
    "special-effect.grant",     # Game.melee_specials (bearer-melee-weapons)
    "ability.cast-via-strips",  # Game.attach_enchantment grants strip-limited uses
    "enchantment.extra-slot",   # Game.attach_enchantment raises the limit
    "state.apply",              # while-worn States (e.g. Contagion's Fragile)
})

# Archetype/Trait effects applied when the loadout is built (sim/engine/loadout.py).
LOADOUT = frozenset({
    "ability.grant", "ability.remove", "ability.modify", "economy.frequency",
    "armor.limit", "equipment.permit",
})


# Parameter values the passive handlers in Game actually implement; other variants are no-ops.
PASSIVE_PARAMS: dict[str, Callable[[dict, Effect], bool]] = {
    "defense.negate-hit": lambda p, e: p.get("from") in ("hits-on-worn-armor", "weapons-and-arrows"),
    "defense.unaffected": lambda p, e: p.get("by") in (
        "projectiles-except-magic-balls", "magical-abilities", "verbal-abilities", "verbal-magical-beyond-touch"),
    "special-effect.grant": lambda p, e: p.get("on") == "bearer-melee-weapons" and p.get("effect") in (
        "armor-breaking", "armor-destroying", "shield-crushing", "wounds-kill"),
    "defense.resistance": lambda p, e: p.get("to") in ("next-source", "wounds", "chosen-school"),
    "state.apply": lambda p, e: e.duration_type in ("while-worn", "permanent"),
    "ability.cast-via-strips": lambda p, e: bool(p.get("ability")),
}


_BECOMES_FREQ = re.compile(r"\bbecomes?\b.*\d+/(Life|Refresh)", re.I)
_SHIELDS = ("small-shield", "medium-shield", "large-shield")


def loadout_handled(eff: Effect, names: set[str] | None = None) -> bool:
    """Whether sim/engine/loadout.py applies this Archetype/Trait effect. `names` (lower-case
    ability names) lets the coverage report check that the named ability resolves."""
    prm = eff.params

    def named(key: str) -> bool:
        v = str(prm.get(key, ""))
        return v.lower() in names if names is not None else bool(re.fullmatch(r"[A-Z][A-Za-z' ]+", v))

    if eff.kind == "ability.grant":
        return prm.get("how") != "as-per" and named("ability")
    if eff.kind == "ability.remove":
        return named("ability")
    if eff.kind == "ability.modify":
        return named("ability") and bool(_BECOMES_FREQ.search(str(prm.get("change", ""))))
    if eff.kind == "economy.frequency":
        change = str(prm.get("change", ""))
        return named("scope") and (change in ("double-uses", "unlimited") or bool(re.fullmatch(r"charge-x\d+", change)))
    if eff.kind == "equipment.permit":
        return prm.get("what") in _SHIELDS + ("great-weapon",)
    if eff.kind == "armor.limit":
        return prm.get("change") in ("set", "increase")
    return False


def is_handled(ability: Ability, eff: Effect, names: set[str] | None = None) -> bool:
    if eff.timing == "while-active":
        if ability.delivery in ("archetype", "trait") and eff.kind in LOADOUT:
            return loadout_handled(eff, names)
        if eff.kind not in PASSIVE or ability.delivery not in PASSIVE_DELIVERIES:
            return False
        check = PASSIVE_PARAMS.get(eff.kind)
        return check is None or check(eff.params, eff)
    if eff.kind == "special-effect.grant":
        return eff.params.get("on") in ("this-magic-ball", "this-arrow")
    if eff.kind in ("defense.negate-hit", "death.prevent") and eff.timing == "on-death":
        # Game.kill only checks worn Enchantments for death prevention (not Chants like Song of Survival)
        return ability.delivery == "enchantment" and (eff.kind == "death.prevent" or eff.params.get("from") == "lethal-event")
    return eff.kind in INSTANT and eff.timing in INSTANT_TIMINGS


def handling(ability: Ability, eff: Effect, names: set[str] | None = None) -> str:
    """'instant' / 'passive' / 'loadout' / 'no-op' for the coverage report."""
    if not is_handled(ability, eff, names):
        return "no-op"
    if eff.timing == "while-active":
        return "loadout" if eff.kind in LOADOUT and ability.delivery in ("archetype", "trait") else "passive"
    return "instant"
