"""A rough, hand-set usefulness score per ability, used by Magic Users to buy spells and by
policies to pick which ability to use. Only effects the engine handles score anything, so an
ability whose effects are all no-ops is never bought or cast deliberately."""
from __future__ import annotations

from sim.engine.effects import is_handled
from sim.rules.compile import Ability

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
}

HEALING = {"life.revive", "wound.heal", "death.prevent", "state.remove", "armor.repair"}
OFFENSE = {"death.cause", "wound.inflict", "move.to-base", "armor.destroy", "enchantment.remove"}


def value(ability: Ability, role: str) -> float:
    total = 0.0
    for eff in ability.effects:
        if not is_handled(ability, eff):
            continue
        if eff.kind == "state.apply":
            w = STATE_WEIGHT.get(eff.params.get("state", ""), 1)
            if eff.polarity != "harm" and eff.subject in ("caster", "bearer"):
                w = 0.5  # a State on yourself is usually a cost, not a benefit
        elif eff.kind == "armor.magic":
            w = 2 * int(eff.params.get("points", 1))
        else:
            w = KIND_WEIGHT.get(eff.kind, 0.5)
        if role == "support" and eff.kind in HEALING:
            w *= 1.5
        if role == "caster" and eff.kind in OFFENSE:
            w *= 1.3
        total += w
    return total
