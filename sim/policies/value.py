"""A rough, hand-set usefulness score per ability, used by Magic Users to buy spells and by
policies to pick which ability to use. Only effects the engine handles score anything, so an
ability whose effects are all no-ops is never bought or cast deliberately.

Benefits add to the score and **drawbacks subtract** from it. A drawback is a harmful effect on
the user's own side: on the caster or bearer (Gift of Air's "may not wield weapons", Berserker's
"may not wear armor", Martyr taking the State), or on an ally the ability is meant to help (the
States Raise Dead leaves on the raised player). A harmful effect on an enemy is the point of the
ability and counts as a benefit."""
from __future__ import annotations

from typing import TYPE_CHECKING

from sim.engine.effects import is_handled
from sim.rules.compile import Ability, Effect

if TYPE_CHECKING:
    from sim.engine.state import Player

STATE_WEIGHT = {"stunned": 6, "frozen": 4, "stopped": 4, "suppressed": 3, "fragile": 4,
                "insubstantial": 3, "cursed": 2}

KIND_WEIGHT = {
    "death.cause": 10, "life.revive": 9, "death.prevent": 7, "wound.inflict": 5, "wound.heal": 4,
    "defense.immunity": 3, "defense.resistance": 3, "defense.negate-hit": 4, "defense.unaffected": 3,
    "armor.repair": 2, "armor.destroy": 3, "armor.damage": 1, "enchantment.remove": 3,
    "move.to-base": 3, "move.push": 2, "move.keep-away": 2, "move.to-location": 2, "move.to-caster": 1,
    "ability.charge": 2, "ability.restore-uses": 2, "state.remove": 2, "equipment.repair": 1,
    "equipment.destroy": 2, "special-effect.grant": 2, "ability.cast-via-strips": 4,
    "enchantment.extra-slot": 1,
    # Elemental Barrage and the like: every carried Magic Ball thrown with a word, not an incantation
    "ability.declare-instead": 4,
}

# Special effects granted to weapons or carried by a ball or arrow. Wounds Kill turns every limb hit
# into a kill, so it is worth far more than breaking a point of armor.
SPECIAL_WEIGHT = {"wounds-kill": 6, "armor-destroying": 3, "armor-breaking": 2, "phasing": 2,
                  "shield-crushing": 1.5, "weapon-destroying": 1, "shield-destroying": 1}

# What a drawback costs, by kind, when it isn't a State or a restriction.
DRAWBACK_WEIGHT = {
    "ability.remove": 2, "economy.purchase-restrict": 1, "economy.cost": 1, "enchantment.remove": 2,
    "armor.damage": 1, "life.prevent-respawn": 3, "defense.unaffected": 2, "state.transfer": 2,
    "armor.limit": 2, "economy.frequency": 1, "ability.modify": 1,
}

HEALING = {"life.revive", "wound.heal", "death.prevent", "state.remove", "armor.repair"}
OFFENSE = {"death.cause", "wound.inflict", "move.to-base", "armor.destroy", "enchantment.remove"}


# Equipment a Magic User can buy: a shield blocks blows in melee, a Great weapon is Armor Breaking
# and Shield Crushing. A larger shield permit also permits the smaller, so only the best counts.
EQUIPMENT_WEIGHT = {"small-shield": 2.0, "medium-shield": 3.0, "large-shield": 3.5, "great-weapon": 2.0,
                    "bows": 4.0}

_OWN_SIDE = ("caster", "bearer", "bearer-equipment", "group")


def is_drawback(ability: Ability, eff: Effect) -> bool:
    if eff.polarity != "harm":
        return False
    if eff.subject in _OWN_SIDE:
        return True
    return eff.subject in ("target", "dead-target") and ability.beneficiary in ("ally", "self", "team")


def restrict_cost(what: str, role: str, p: "Player | None" = None) -> float:
    """What a restriction on the bearer costs. With a player, the cost is what that player would
    actually lose (their armor, their shield); without one, a typical player of the role."""
    melee = role in ("fighter", "archer")
    if what == "wield-weapons":
        return 8.0 if melee else 2.0
    if what in ("fire-normal-arrows", "wield-bows"):
        return (8.0 if p.has_bow else 0.0) if p is not None else (8.0 if role == "archer" else 0.0)
    if what == "wear-armor":
        return 2.0 * p.armor_max if p is not None else (4.0 if melee else 0.5)
    if what == "wield-shields":
        return EQUIPMENT_WEIGHT.get(f"{p.shield}-shield", 0.0) if p is not None else (2.0 if melee else 0.5)
    if what == "wield-large-shields":
        return (0.5 if p.shield == "large" else 0.0) if p is not None else 0.5
    if what == "wield-great-weapons":
        return (2.0 if p.great_weapon else 0.0) if p is not None else 1.0
    return 1.0


def drawback_cost(ability: Ability, role: str, p: "Player | None" = None) -> float:
    total = 0.0
    for eff in ability.effects:
        if not is_handled(ability, eff) or not is_drawback(ability, eff):
            continue
        if eff.kind == "action.restrict":
            total += restrict_cost(str(eff.params.get("what", "")), role, p)
        elif eff.kind == "state.apply":
            total += STATE_WEIGHT.get(eff.params.get("state", ""), 1)
        else:
            total += DRAWBACK_WEIGHT.get(eff.kind, 1)
    return total


def effect_benefit(ability: Ability, eff: Effect, role: str) -> float:
    """One handled, non-drawback effect's contribution to the score."""
    if eff.kind == "armor.limit" and eff.params.get("change") == "increase":
        return 2.0 * int(eff.params.get("points", 1))  # like Magic Armor, but it can be repaired
    if eff.kind == "state.apply":
        w = STATE_WEIGHT.get(eff.params.get("state", ""), 1)
        if eff.subject in ("caster", "bearer"):
            w = 0.5  # a State on yourself is usually a cost, not a benefit
    elif eff.kind == "armor.magic":
        w = 2 * int(eff.params.get("points", 1))
    elif eff.kind == "special-effect.grant":
        w = SPECIAL_WEIGHT.get(eff.params.get("effect", ""), 2)
        if eff.params.get("on") == "next-wound":
            w *= 0.5    # one blow, not every blow
    else:
        w = KIND_WEIGHT.get(eff.kind, 0.5)
    if role == "support" and eff.kind in HEALING:
        w *= 1.5
    if role == "caster" and eff.kind in OFFENSE:
        w *= 1.3
    return w


def benefit(ability: Ability, role: str) -> float:
    total = 0.0
    equipment = 0.0
    for eff in ability.effects:
        if not is_handled(ability, eff) or is_drawback(ability, eff):
            continue
        if eff.kind == "equipment.permit":
            equipment = max(equipment, EQUIPMENT_WEIGHT.get(eff.params.get("what", ""), 0.0))
            continue
        total += effect_benefit(ability, eff, role)
    return total + equipment


def value(ability: Ability, role: str) -> float:
    """Benefits minus drawbacks. Zero or less: not worth buying or casting as a matter of course."""
    b = benefit(ability, role)
    return b - drawback_cost(ability, role) if b > 0 else 0.0
