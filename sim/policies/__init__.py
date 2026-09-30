"""Scripted per-role behavior. Called once per tick for each player who is alive, able to act
and not already incanting. Melee targeting itself happens in Game._engage.

Roles (from sim/engine/loadout.py ROLE_BY_CLASS):
  fighter - closes to melee; sometimes uses an offensive ability first; heals self when free
  caster  - stays back; offensive abilities first, then support
  support - stays back; revives, heals, enchants allies, then offense
  archer  - stays back; shoots (Specialty Arrows first), fights with a short weapon if engaged
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from sim.engine.state import Player, Uses
from sim.policies.value import benefit, drawback_cost

if TYPE_CHECKING:
    from sim.engine.game import Game

HARM_KINDS = {"death.cause", "wound.inflict", "state.apply", "move.to-base", "move.push", "move.keep-away",
              "armor.destroy", "enchantment.remove", "equipment.destroy", "move.to-location", "move.to-caster"}


TRIGGERED = {"immediately-after-kill", "after-dying", "immediately-after-wound"}


def _usable(g: "Game", p: Player) -> list[Uses]:
    """Abilities the policy may choose to cast now (triggered ones fire on their own)."""
    return [u for u in p.uses.values() if u.available() and g.value(u.ability, p) > 0
            and not (u.ability.requirements & TRIGGERED) and "kill-trigger" not in u.ability.properties]


def _in_range(g: "Game", u: Uses) -> bool:
    table = g.rules.a("range.p_in_range")
    return g.rng.random() < table.get(u.range, 0.5)


def _engaged(g: "Game", p: Player) -> bool:
    return p.target is not None or bool(g.attackers_of(p))


def _is_offensive(u: Uses) -> bool:
    ab = u.ability
    if ab.beneficiary == "enemy":
        return True
    return ab.delivery in ("magic-ball", "specialty-arrow") or any(
        e.polarity == "harm" and e.kind in HARM_KINDS and e.subject in ("target", "struck-player") for e in ab.effects)


def _is_revive(u: Uses) -> bool:
    return bool(u.ability.effects_of("life.revive")) and "after-dying" not in u.ability.requirements


def _is_heal(u: Uses) -> bool:
    return (bool(u.ability.effects_of("wound.heal")) and not _is_revive(u) and not _is_offensive(u)
            and not u.ability.requirements & {"target-dead", "target-dead-at-start"})


def _enemy_for(g: "Game", p: Player, u: Uses) -> Player | None:
    """A random enemy this ability can legally start on right now."""
    reqs = u.ability.requirements
    t = g.t
    if reqs & {"target-dead", "target-dead-at-start"}:
        foes = [q for q in g.enemies(p) if not q.alive and not q.out]
    elif "target-frozen" in reqs:
        foes = [q for q in g.enemies(p) if q.alive and q.has_state("frozen", t)]
    elif "target-insubstantial" in reqs:
        foes = [q for q in g.enemies(p) if q.on_field(t) and q.has_state("insubstantial", t)]
    else:
        foes = [q for q in g.enemies(p) if g.targetable(q)]
    foes = [q for q in foes if g.check_requirements(u.ability, p, q, start=True) is None]
    return g.rng.choice(foes) if foes else None


def _try_offense(g: "Game", p: Player) -> bool:
    engaged = _engaged(g, p)
    options = sorted((u for u in _usable(g, p) if _is_offensive(u)), key=lambda u: -g.value(u.ability, p))
    for u in options:
        if u.range == "Self":
            continue
        if engaged and not g.rules.a("casting.engaged_casting_allowed"):
            continue
        target = _enemy_for(g, p, u)
        if target is None or not _in_range(g, u):
            continue
        if g.start_cast(p, u, target):
            return True
    return False


def _can_receive(g: "Game", u: Uses, p: Player, q: Player) -> bool:
    """Whether a helpful ability from p would take effect on q. Cursed (Immune to Spirit),
    Frozen, Insubstantial and Protection from Magic are all declared or visible, so a veteran
    doesn't spend an incantation on an ally who can't receive it. Mirrors the target checks in
    Game.blocked without its side effect (spending a Resistance)."""
    ab, t = u.ability, g.t
    works_on_states = ({"target-frozen", "target-insubstantial"} & ab.requirements
                       or ab.effects_of("state.remove") or "bypass-states" in ab.properties)
    if not works_on_states and (q.has_state("frozen", t) or (q is not p and q.has_state("insubstantial", t))):
        return False
    if ab.delivery != "enchantment" and "bypass-immunities" not in ab.properties and g.immune(q, ab.school):
        return False
    return q is p or not (u.magical and g.unaffected(q, "magical-abilities"))


def _try_revive(g: "Game", p: Player) -> bool:
    if _engaged(g, p):
        return False
    dead = [q for q in g.allies(p) if not q.alive and not q.out and q is not p
            and not _being_helped(g, q, p, _is_revive)]
    if not dead:
        return False
    for u in (u for u in _usable(g, p) if _is_revive(u)):
        q = g.rng.choice(dead)
        if g.check_requirements(u.ability, p, q, start=True) or not _can_receive(g, u, p, q):
            continue
        if g.rng.random() < g.rules.a("range.p_ally_nearby_for_touch") and g.start_cast(p, u, q):
            return True
    return False


def _being_helped(g: "Game", q: Player, by: Player, kind) -> bool:
    """Someone other than `by` is already incanting an ability of this kind (_is_heal,
    _is_revive) on q: a second caster would only waste the incantation."""
    return any(o is not by and o.casting is not None and o.casting.kind == "cast" and o.casting.uses is not None
               and o.casting.target == q.pid and kind(o.casting.uses) for o in g.players)


def _heal_candidates(g: "Game", p: Player) -> list[Player]:
    """Wounded allies an experienced healer would start on: themselves, or an ally who is out of
    melee (Touch range means standing next to them for the whole incantation, so a healer heals
    behind the line, not in it) and whom no one else is already healing."""
    return [q for q in g.allies(p) if q.alive and q.wounds and q.on_field(g.t)
            and (q is p or not _engaged(g, q)) and not _being_helped(g, q, p, _is_heal)]


def _try_heal(g: "Game", p: Player) -> bool:
    if _engaged(g, p):
        return False
    hurt = _heal_candidates(g, p)
    if not hurt:
        return False
    for u in (u for u in _usable(g, p) if _is_heal(u)):
        able = [q for q in hurt if _can_receive(g, u, p, q)]
        if u.range == "Self":
            if p in able and g.start_cast(p, u, p):
                return True
            continue
        if not able:
            continue
        q = p if p in able else g.rng.choice(able)
        if (q is p or g.rng.random() < g.rules.a("range.p_ally_nearby_for_touch")) and g.start_cast(p, u, q):
            return True
    return False


def _crippled(ab, q: Player) -> bool:
    """The Enchantment's drawbacks would cost this player more than it gives them: Gift of Air
    ("may not wield weapons or shields") on a fighter, say. A veteran puts it on someone else."""
    cost = drawback_cost(ab, q.role, q)
    return cost > 0 and cost >= benefit(ab, q.role)


def _enchant_targets(g: "Game", p: Player, u: Uses, at_base: bool) -> list[Player]:
    if u.range == "Self":
        pool = [p]
    else:
        pool = [q for q in g.allies(p) if q.alive and (q.at_base_until > g.t) == at_base]
    if u.range == "Other":
        pool = [q for q in pool if q is not p]
    return [q for q in pool if all(e.ability.slug != u.slug for e in q.enchantments)
            and (not u.magical or q.magical_enchantment_count() < q.ench_slots)
            and not _crippled(u.ability, q)]


def _try_enchant(g: "Game", p: Player, at_base: bool) -> bool:
    for u in sorted(_usable(g, p), key=lambda u: -g.value(u.ability, p)):
        if u.ability.delivery != "enchantment" or _is_offensive(u):
            continue
        targets = _enchant_targets(g, p, u, at_base)
        if not targets:
            continue
        q = g.rng.choice(targets)
        if not at_base and q is not p and g.rng.random() >= g.rules.a("range.p_ally_nearby_for_touch"):
            continue
        if g.start_cast(p, u, q):
            return True
    return False


def _charge_seconds(g: "Game", u: Uses) -> float:
    return math.ceil(u.charge * g.rules.a("time.charge_incantation_words") / g.words_per_second)


def _would_use(g: "Game", p: Player, u: Uses) -> bool:
    """A recharged use would plausibly be spent: an Enchantment needs someone to wear it."""
    if u.ability.delivery == "enchantment" and not _is_offensive(u):
        return bool(_enchant_targets(g, p, u, False) or _enchant_targets(g, p, u, True))
    return True


def _lull(g: "Game", p: Player) -> bool:
    """No enemy is on the field to fight (all dead, at base or out of reach)."""
    return not any(g.targetable(q) for q in g.enemies(p))


def _try_charge(g: "Game", p: Player) -> bool:
    """Recharge the spent ability with the most value per second of Charging, among those that
    would be used. Standing still for a long Charge is only worth it in a lull; fighters and archers
    would rather fight, so they Charge only in a lull at all."""
    if _engaged(g, p) or g.rng.random() >= g.rules.a("policy.p_charge_when_safe"):
        return False
    lull = _lull(g, p)
    if p.role in ("fighter", "archer") and not lull:
        return False
    longest = math.inf if lull else g.rules.a("policy.max_field_charge_seconds")
    spent = [u for u in p.uses.values() if u.charge and u.max and u.left is not None and u.left < u.max
             and g.value(u.ability, p) > 0 and _charge_seconds(g, u) <= longest and _would_use(g, p, u)]
    if not spent:
        return False
    return g.start_charge(p, max(spent, key=lambda u: g.value(u.ability, p) / _charge_seconds(g, u)))


def _try_shoot(g: "Game", p: Player) -> bool:
    if not p.has_bow or _engaged(g, p) or p.next_shot_at > g.t:
        return False
    for u in _usable(g, p):
        if u.ability.delivery == "specialty-arrow":
            target = _enemy_for(g, p, u)
            if target is not None and g.start_cast(p, u, target):
                return True
    foes = [q for q in g.enemies(p) if g.targetable(q)]
    if foes:
        g.shoot(p, g.rng.choice(foes))
        return True
    return False


def keep_casting(g: "Game", p: Player) -> bool:
    """Asked each tick of a player mid-incantation or mid-Charge. An attacked player stops
    talking and defends unless the incantation finishes this tick: standing still while being
    hit only ends in a wound. (Before this hook the engine never asked, so casters kept
    incanting under attack and never struck back.)"""
    c = p.casting
    if c is None or not g.attackers_of(p):
        return True
    return c.remaining <= g.dt or not g.rules.a("policy.abandon_cast_when_attacked")


def decide(g: "Game", p: Player) -> None:
    t = g.t
    if p.at_base_until > t:
        _try_enchant(g, p, at_base=True)
        return
    if p.has_state("stopped", t) and p.role != "fighter":
        pass  # Stopped players can still cast and fight; nothing special in Phase 1
    if p.role == "support":
        if g.rules.a("policy.revive_priority") and _try_revive(g, p):
            return
        if _try_heal(g, p) or (g.rng.random() < g.rules.a("policy.p_enchant_ally_on_field") and _try_enchant(g, p, False)):
            return
        if _try_offense(g, p) or _try_charge(g, p):
            return
    elif p.role == "caster":
        if _try_offense(g, p) or _try_revive(g, p) or _try_heal(g, p):
            return
        if g.rng.random() < g.rules.a("policy.p_enchant_ally_on_field") and _try_enchant(g, p, False):
            return
        _try_charge(g, p)
    elif p.role == "archer":
        if _try_shoot(g, p) or _try_heal(g, p):
            return
        _try_charge(g, p)
    else:
        if p.target is None and g.rng.random() < g.rules.a("policy.p_use_offensive_ability_when_free"):
            if _try_offense(g, p):
                return
        if p.target is None and (_try_heal(g, p) or _try_revive(g, p)):
            return
        if p.target is None:
            _try_charge(g, p)
