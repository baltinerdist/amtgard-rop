"""Scripted per-role behavior. Called once per tick for each player who is alive, able to act
and not already incanting. Melee targeting itself happens in Game._engage.

Martial roles (from sim/engine/loadout.py ROLE_BY_CLASS):
  fighter - closes to melee; buffs self (Rage); when wounded and not under attack, steps back out
            of melee and heals themselves if they can (`_try_step_back_heal`); sometimes uses an
            offensive ability first; heals, cleanses and mends when free
  archer  - stays back; shoots (Specialty Arrows first), fights with a short weapon if engaged
Magic Users play their doctrine's play style (sim/data/doctrines.json `play_styles`, PLAY_ROUTINES):
  striker    - stays back; self-buffs, finishers, its own set-ups (combos), then offense; support last
  controller - stays back; finishers, then locks down the enemy most dangerous to a teammate
               (`_try_control`: one engaged with an ally first, then the most kill potential in
               range; never one already locked down or immune); kills only when nothing needs
               locking down
  enchanter  - enchants teammates at base and, out of melee, on the field (weapon Enchantments to
               the best melee fighters, armor and protection to the front line), refills their uses
               (Empower, Restoration, Confidence), then heals and cleanses; casts at enemies last
  medic      - revives, heals, cleanses from behind the line (the old support routine)
  battle     - starts melee like a fighter (Game._engage) and is not treated as backline; keeps
               self-buffs up and casts when free
  archer     - shoots with a bow (Ranger) and casts between shots; a striker without a bow
Every Magic User at base enchants by the same priorities. Anyone attacked in melee who is not a
fighter (or battle caster), or is already wounded, uses an escape (Blink) if they have one.

Finishers: a caster holding an ability that requires a Stopped, Frozen or Insubstantial target
(Dragged Below, Shatter, Dimensional Rift), or any wounding ability against a Fragile one, uses it
on such a target first, preferring one whose State the caster applied (`Player.state_src`). A
doctrine with combos casts a set-up whose finisher it holds before other offense.

Abilities are recognised by what their effects do, not by name (_kind_of): a self-buff, an
escape, a cleanse (removes a harmful State), a repair (armor or equipment).

Bardic songs are chosen by situational utility, not the fixed score (sim/policies/songs.py,
_try_song): a battle Bard sings first, the other play styles when they have nothing better to cast.
Any other incantation ends the song, so `_usable`, `_of_kind` (not escapes) and `_try_charge` only
offer a singing Bard what is worth the song time it costs (songs.keeps_song), and a Bard turns down
a teammate's Enchantment worth less than a song (songs.declines, in `_enchant_targets`).
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from sim.engine.effects import is_handled
from sim.engine.state import Player, Uses
from sim.policies import enablers, songs
from sim.policies.enablers import name_refill  # noqa: F401  (the engine's refill hook, Game.name_refill)
from sim.policies.utility import has_utility
from sim.policies.value import Ctx, benefit, drawback_cost, is_drawback, player_ctx

if TYPE_CHECKING:
    from sim.engine.game import Game

HARM_KINDS = {"death.cause", "wound.inflict", "state.apply", "move.to-base", "move.push", "move.keep-away",
              "armor.destroy", "enchantment.remove", "equipment.destroy", "move.to-location", "move.to-caster"}


TRIGGERED = {"immediately-after-kill", "after-dying", "immediately-after-wound"}


def _usable(g: "Game", p: Player) -> list[Uses]:
    """Abilities the policy may choose to cast now (triggered ones fire on their own), and worth the
    song their incantation would end (songs.keeps_song). An ability with a utility function
    (enablers.py) is weighed by it, song included (enablers.time_cost), not by its fixed score."""
    return [u for u in p.uses.values() if u.available()
            and not (u.ability.requirements & TRIGGERED) and "kill-trigger" not in u.ability.properties
            and (has_utility(u.ability) or (g.value(u.ability, p) > 0 and songs.keeps_song(g, p, u)))]


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
    revives = [u for u in _usable(g, p) if _is_revive(u)]
    if not revives or _engaged(g, p):
        return False
    dead = [q for q in g.allies(p) if not q.alive and not q.out and q is not p
            and not _being_helped(g, q, p, _is_revive)]
    if not dead:
        return False
    for u in revives:
        # a granted revive may be tied to one player (Undead Minion's Raise Dead: only its bearer)
        pool = dead if u.only_target is None else [q for q in dead if q.pid == u.only_target]
        if not pool:
            continue
        q = g.rng.choice(pool)
        if g.check_requirements(u.ability, p, q, start=True, uses=u) or not _can_receive(g, u, p, q):
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
        able = [q for q in hurt if _can_receive(g, u, p, q) and g.can_cast_at(p, q, u)]
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


def _try_step_back_heal(g: "Game", p: Player) -> bool:
    """A wounded melee player who holds a heal they can cast on themselves (Gift of Water's and
    Regeneration's Heal (Self), a Scout's Heal) and whom nobody is attacking steps back out of
    melee and heals: they drop their own target and start the heal on themselves. Real play: a
    wounded fighter backs off a step and heals, because a second wound kills. One who is under
    attack keeps fighting (they can't step away in Phase 1), and one a teammate is already
    healing waits for it."""
    if not p.wounds or g.attackers_of(p) or _being_helped(g, p, p, _is_heal):
        return False
    heals = [u for u in _usable(g, p) if _is_heal(u) and u.range in ("Self", "Touch")
             and _can_receive(g, u, p, p) and g.can_cast_at(p, p, u)]
    if not heals:
        return False
    had = p.target
    p.target = None                     # step back: Regeneration's Heal needs no enemy within 10'
    for u in sorted(heals, key=lambda u: (u.left is not None, -g.value(u.ability, p), u.slug)):
        if g.start_cast(p, u, p):
            return True
    p.target = had
    return False


def _crippled(g: "Game", p: Player, ab, q: Player) -> bool:
    """The Enchantment gives this player nothing, or its drawbacks would cost them more than it
    gives them: Gift of Air ("may not wield weapons or shields") on a fighter, Amplification on a
    player with no 20' Verbal or with their own Extension. Priced with both kits
    (`value.Ctx`: the caster p holds it, q bears it). A veteran puts it on someone else."""
    ctx = Ctx(holder=player_ctx(g, p).holder, bearer=player_ctx(g, q).holder, game_type=g.sc.get("game_type"),
              ablate=frozenset(g.ablate))
    gain = benefit(ab, q.role, ctx, g.rules)
    cost = drawback_cost(ab, q.role, ctx=ctx, rules=g.rules)
    return gain <= 0 or (cost > 0 and cost >= gain)


def _enchant_targets(g: "Game", p: Player, u: Uses, at_base: bool) -> list[Player]:
    if u.range == "Self":
        pool = [p]
    else:
        pool = [q for q in g.allies(p) if q.alive and (q.at_base_until > g.t) == at_base]
    if u.range == "Other":
        pool = [q for q in pool if q is not p]
    return [q for q in pool if all(e.ability.slug != u.slug for e in q.enchantments)
            and (not u.magical or "exempt-from-enchantment-limit" in u.ability.properties
                 or q.magical_enchantment_count() < q.ench_slots)
            and (has_utility(u.ability) or not _crippled(g, p, u.ability, q))    # a utility counts drawbacks
            and (q is p or not songs.declines(g, q, u))]


def _try_enchant(g: "Game", p: Player, at_base: bool, prioritized: bool = False, free_only: bool = False) -> bool:
    """`prioritized`: weapon Enchantments to the best melee fighters, armor and protection to the
    front line (_enchant_priority); otherwise a random eligible ally. `free_only`: only allies out
    of melee (an enchanter re-enchants between fights). An Enchantment with a utility function
    (enablers.py: extra slots, grants, Undead Minion, Self strips aimed at enemies) goes to the
    teammate it is worth most to, only when that beats the time the cast costs, and is tried in
    order of that utility among the others' fixed scores."""
    opts = []
    for i, u in enumerate(_usable(g, p)):
        util = has_utility(u.ability)
        if u.ability.delivery != "enchantment" or (_is_offensive(u) and not util) or songs.is_song(u.ability):
            continue            # songs are chosen by the situation (_try_song)
        if not util:
            opts.append((-g.value(u.ability, p), i, u, None))
            continue
        q, x = enablers.best_target(g, p, u, _field_targets(g, p, u, at_base, free_only))
        if q is not None and enablers.worth_casting(g, p, u, x, at_base):
            opts.append((-x, i, u, q))
    for _, _, u, q in sorted(opts, key=lambda o: o[:2]):
        if q is None:
            targets = _field_targets(g, p, u, at_base, free_only)
            if not targets:
                continue
            q = _enchant_priority(g, u, targets) if prioritized else g.rng.choice(targets)
        if not at_base and q is not p and g.rng.random() >= g.rules.a("range.p_ally_nearby_for_touch"):
            continue
        if g.start_cast(p, u, q):
            return True
    return False


def _field_targets(g: "Game", p: Player, u: Uses, at_base: bool, free_only: bool) -> list[Player]:
    targets = _enchant_targets(g, p, u, at_base)
    return [q for q in targets if q is p or not _engaged(g, q)] if free_only else targets


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
    if (p.role in ("fighter", "archer") or p.play == "battle") and not lull:
        return False
    longest = math.inf if lull else g.rules.a("policy.max_field_charge_seconds")
    spent = [u for u in p.uses.values() if u.charge and u.max and u.left is not None and u.left < u.max
             and g.value(u.ability, p) > 0 and _charge_seconds(g, u) <= longest and _would_use(g, p, u)
             and g.value(u.ability, p) >= songs.song_loss(g, p, _charge_seconds(g, u))]
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
    if not g.can_fire_normal_arrows(p) or not g.weapon_usable(p):
        return False
    foes = [q for q in g.enemies(p) if g.targetable(q) and g.can_attack(p, q)]
    if foes:
        g.shoot(p, g.rng.choice(foes))
        return True
    return False


# ---------------------------------------------------------------- abilities by what they do

_BUFF_KINDS = {"special-effect.grant", "defense.unaffected", "ability.declare-instead"}
_REMOVABLE = ("stunned", "frozen", "stopped", "suppressed", "fragile", "cursed")
_KIND_CACHE: dict[str, str] = {}


def _kind_of(ab) -> str:
    """'escape', 'buff', 'cleanse', 'repair' or '' from the ability's handled, non-drawback effects."""
    k = _KIND_CACHE.get(ab.slug)
    if k is not None:
        return k
    effs = [e for e in ab.effects if is_handled(ab, e) and not is_drawback(ab, e)]
    kinds = {e.kind for e in effs}
    self_only = ab.range == "Self"
    if self_only and any(e.kind == "state.apply" and e.subject == "caster"
                         and e.params.get("state") == "insubstantial" for e in effs):
        k = "escape"
    elif "state.remove" in kinds and ab.delivery == "verbal" and ab.beneficiary != "enemy" \
            and not kinds & {"life.revive", "wound.heal"} \
            and not any(e.polarity == "harm" and e.subject in ("target", "struck-player") for e in ab.effects):
        k = "cleanse"
    elif self_only and ab.delivery == "verbal" and effs and kinds <= _BUFF_KINDS \
            and all(e.subject == "caster" for e in effs):
        k = "buff"
    elif kinds & {"armor.repair", "equipment.repair"} and not kinds & {"life.revive", "wound.heal"}:
        k = "repair"
    else:
        k = ""
    _KIND_CACHE[ab.slug] = k
    return k


def _of_kind(g: "Game", p: Player, kind: str) -> list[Uses]:
    """Usable abilities of this kind; an escape is taken whatever song it ends."""
    return [u for u in p.uses.values() if u.available() and _kind_of(u.ability) == kind
            and not (u.ability.requirements & TRIGGERED) and "kill-trigger" not in u.ability.properties
            and (kind == "escape" or songs.keeps_song(g, p, u))]


def _loaded_balls(p: Player) -> int:
    return sum(u.left or 0 for u in p.uses.values() if u.ability.delivery == "magic-ball" and u.unit)


def _try_self_buff(g: "Game", p: Player) -> bool:
    """Rage before a fight, Elemental Barrage with balls in hand: a Self buff not already on."""
    buffs = _of_kind(g, p, "buff")
    if not buffs or _lull(g, p):
        return False
    for u in buffs:
        ab = u.ability
        if ab.effects_of("ability.declare-instead"):
            if p.barrage is not None or _loaded_balls(p) < 2 or _engaged(g, p):
                continue
        elif any(b.slug == u.slug for b in g._buffs(p)):
            continue
        if g.start_cast(p, u, p):
            return True
    return False


def _try_escape(g: "Game", p: Player) -> bool:
    """Blink out of a fight you are losing: attacked, and either not a fighter or already wounded."""
    if (p.role == "fighter" or p.play == "battle") and not p.wounds:
        return False
    escapes = _of_kind(g, p, "escape")
    if not escapes or not g.attackers_of(p):
        return False
    return any(g.start_cast(p, u, p) for u in escapes)


def _afflicted(g: "Game", q: Player) -> list[str]:
    """Harmful States on q that a cleanse could lift (not those a worn Enchantment imposes)."""
    if not q.states:
        return []
    held = [s for s in _REMOVABLE if q.has_state(s, g.t)]
    return [s for s in held if s not in g.enchantment_states(q)] if held else []


def _is_cleanse(u: Uses) -> bool:
    return _kind_of(u.ability) == "cleanse"


def _try_cleanse(g: "Game", p: Player) -> bool:
    """Lift a harmful State from yourself or from an ally out of melee whom no one else is helping.
    Martyr moves the State onto the caster, so only a non-fighter uses it, and only for a fighter
    or archer."""
    options = _of_kind(g, p, "cleanse")
    if not options:
        return False
    needy = [q for q in g.allies(p) if q.alive and q.states and q.on_field(g.t) and _afflicted(g, q)]
    if not needy:
        return False
    engaged = _engaged(g, p)
    options.sort(key=lambda u: (drawback_cost(u.ability, p.role), u.ability.cast_seconds(g.words_per_second)))
    for u in options:
        martyr = drawback_cost(u.ability, p.role) > 0
        if u.range == "Self":
            pool = [p] if p in needy else []
        elif engaged:
            continue
        else:
            pool = [q for q in needy if (q is p or not _engaged(g, q)) and not _being_helped(g, q, p, _is_cleanse)]
            if u.range == "Other" or martyr:
                pool = [q for q in pool if q is not p]
        if martyr:
            if p.role in ("fighter", "archer"):
                continue
            pool = [q for q in pool if q.role in ("fighter", "archer")]
        pool = [q for q in pool if _can_receive(g, u, p, q) and g.can_cast_at(p, q, u)
                and g.check_requirements(u.ability, p, q, start=True) is None]
        if not pool:
            continue
        q = p if p in pool else g.rng.choice(pool)
        if q is not p and not _in_reach(g, u):
            continue
        if g.start_cast(p, u, q):
            return True
    return False


def _needs_repair(q: Player) -> bool:
    return (not q.weapon_ok or q.shield_hits > 0
            or (q.armor_max > 0 and any(v < q.armor_max for v in q.armor.values())))


def _try_repair(g: "Game", p: Player) -> bool:
    """Mend armor or broken equipment: your own, or an ally's out of melee."""
    options = _of_kind(g, p, "repair")
    if not options:
        return False
    needy = [q for q in g.allies(p) if q.alive and q.on_field(g.t) and _needs_repair(q)]
    if not needy or _engaged(g, p):
        return False
    for u in options:
        pool = ([p] if p in needy else []) if u.range == "Self" else \
            [q for q in needy if q is p or not _engaged(g, q)]
        if u.range == "Other":
            pool = [q for q in pool if q is not p]
        pool = [q for q in pool if g.can_cast_at(p, q, u) and _can_receive(g, u, p, q)
                and not _being_helped(g, q, p, lambda v: _kind_of(v.ability) == "repair")]
        if not pool:
            continue
        q = p if p in pool else g.rng.choice(pool)
        if q is not p and not _in_reach(g, u):
            continue
        if g.start_cast(p, u, q):
            return True
    return False


def _in_reach(g: "Game", u: Uses) -> bool:
    if u.range in ("Touch", "Other"):
        return g.rng.random() < g.rules.a("range.p_ally_nearby_for_touch")
    return _in_range(g, u)


def keep_casting(g: "Game", p: Player) -> bool:
    """Asked each tick of a player mid-incantation or mid-Charge. An attacked player stops
    talking and defends unless the incantation finishes this tick, or it is the escape they are
    casting because they are attacked: standing still while being hit only ends in a wound.
    (Before this hook the engine never asked, so casters kept incanting under attack and never
    struck back.)"""
    c = p.casting
    if c is None or not g.attackers_of(p):
        return True
    if c.kind == "cast" and c.uses is not None and _kind_of(c.uses.ability) == "escape":
        return True
    return c.remaining <= g.dt or not g.rules.a("policy.abandon_cast_when_attacked")


# ---------------------------------------------------------------- doctrine play styles

CONTROL_STATES = ("stunned", "frozen", "stopped", "suppressed", "fragile", "insubstantial")
_LOCKED = ("stunned", "frozen", "stopped", "insubstantial")       # already out of the fight
_FINISH_REQ = {"target-stopped": "stopped", "target-frozen": "frozen", "target-insubstantial": "insubstantial"}
_CONTROL_MOVES = {"move.to-base", "move.push", "move.keep-away", "move.to-location", "move.to-caster"}
# how likely an enemy is to kill a teammate, by role: fighters most (see _threat)
ROLE_THREAT = {"fighter": 2.0, "archer": 1.5, "caster": 1.0, "support": 0.5}
_WEAPON_KINDS = {"weapon.ignore-protections"}
_ARMOR_KINDS = {"armor.magic", "armor.limit", "armor.protect", "defense.resistance", "defense.immunity",
                "defense.negate-hit", "defense.unaffected", "defense.negate-engulfing", "death.prevent",
                "equipment.protect"}
_SLUG_CACHE: dict[tuple, object] = {}


def _cached(tag: str, ab, fn):
    key = (tag, ab.slug)
    v = _SLUG_CACHE.get(key)
    if v is None:
        v = _SLUG_CACHE[key] = fn(ab)
    return v


def control_states(ab) -> frozenset:
    """Control States this ability puts on an enemy."""
    return _cached("states", ab, lambda ab: frozenset(
        str(e.params.get("state")) for e in ab.effects
        if e.kind == "state.apply" and e.subject in ("target", "struck-player")
        and e.params.get("state") in CONTROL_STATES and is_handled(ab, e)))


def _is_control(u: Uses) -> bool:
    """Takes an enemy out of the fight without killing: a control State, a restriction (Awe,
    Insult), forced movement or a disabled weapon."""
    def calc(ab) -> bool:
        if ab.effects_of("death.cause"):
            return False
        return any(is_handled(ab, e) and e.subject in ("target", "struck-player", "target-equipment") and (
            (e.kind == "state.apply" and e.params.get("state") in CONTROL_STATES)
            or e.kind in ("action.restrict", "equipment.disable") or e.kind in _CONTROL_MOVES) for e in ab.effects)
    return _is_offensive(u) and _cached("control", u.ability, calc)


def finish_states(ab) -> frozenset:
    """States that make a target this ability's to finish: those its requirements name (Dragged
    Below: Stopped), or Fragile for anything that wounds or kills with no such requirement."""
    def calc(ab) -> frozenset:
        req = {_FINISH_REQ[r] for r in ab.requirements if r in _FINISH_REQ}
        if req:
            return frozenset(req)
        if ab.effects_of("wound.inflict", "death.cause") and not ab.requirements & {"target-dead", "target-dead-at-start"}:
            return frozenset({"fragile"})
        return frozenset()
    return _cached("finish", ab, calc)


def _threat(q: Player) -> float:
    """Kill potential: role (fighters and battle casters first), skill, and kills so far."""
    role = "fighter" if q.play == "battle" else q.role
    return ROLE_THREAT.get(role, 1.0) + q.skill + 0.5 * q.kills


def _engaged_with_team(g: "Game", p: Player) -> set[int]:
    """Enemies in melee with one of p's teammates (either side started it)."""
    mates = {q.pid for q in g.allies(p) if q is not p and q.alive}
    out = {q.pid for q in g.enemies(p) if q.alive and q.target in mates}
    out.update(q.target for q in g.allies(p) if q.pid in mates and q.target is not None)
    return out


def _resists(g: "Game", u: Uses, q: Player) -> bool:
    """q would shrug this off (declared or visible): Immune to its School, unaffected by Magic or
    Verbals, Void Touched. Mirrors Game.blocked without spending a Resistance."""
    ab = u.ability
    if ab.delivery != "enchantment" and "bypass-immunities" not in ab.properties and g.immune(q, ab.school):
        return True
    if u.magical and (g.unaffected(q, "magical-abilities") or g.unaffected_by_school(q, ab.school) is not None):
        return True
    return ab.delivery == "verbal" and g.unaffected(q, "verbal-abilities")


def _can_hit(g: "Game", p: Player, u: Uses, q: Player) -> bool:
    return (g.check_requirements(u.ability, p, q, start=True, uses=u) is None and g.can_cast_at(p, q, u)
            and not _resists(g, u, q))


def _locked(g: "Game", q: Player, u: Uses) -> bool:
    """Already locked down, or already under everything this ability would do. Suppressing only
    matters to someone who casts."""
    t = g.t
    states = control_states(u.ability)
    if states == {"suppressed"}:
        casts = any(v.magical and v.available() for v in q.uses.values())
        return not casts or q.has_state("suppressed", t) or q.has_state("stunned", t)
    if any(q.has_state(s, t) for s in _LOCKED):
        return True
    if states and all(q.has_state(s, t) for s in states):
        return True
    return any(r.slug == u.slug and r.until > t for r in q.restrictions)


def _first_in_range(g: "Game", u: Uses, ranked: list[Player]) -> Player | None:
    """The first enemy in priority order who turns out to be in range (each rolled independently)."""
    for q in ranked:
        if _in_range(g, u):
            return q
    return None


def _control_order(g: "Game", p: Player, foes: list[Player]) -> list[Player]:
    """Enemies engaged with a teammate first, then the most kill potential."""
    fighting = _engaged_with_team(g, p)
    return sorted(foes, key=lambda q: (q.pid not in fighting, -_threat(q), q.pid))


def _may_cast_now(g: "Game", p: Player) -> bool:
    return not _engaged(g, p) or g.rules.a("casting.engaged_casting_allowed")


def _try_control(g: "Game", p: Player) -> bool:
    """Lock down the enemy most dangerous to a teammate (see the module docstring)."""
    if not _may_cast_now(g, p):
        return False
    options = sorted((u for u in _usable(g, p) if _is_control(u) and u.range != "Self"),
                     key=lambda u: -g.value(u.ability, p))
    for u in options:
        foes = [q for q in g.enemies(p) if g.targetable(q) and not _locked(g, q, u) and _can_hit(g, p, u, q)]
        q = _first_in_range(g, u, _control_order(g, p, foes)) if foes else None
        if q is not None and g.start_cast(p, u, q):
            return True
    return False


def _meets(g: "Game", q: Player, states: frozenset) -> str | None:
    """The finishing State q is in, if any."""
    t = g.t
    for s in states:
        if not q.has_state(s, t):
            continue
        if s == "frozen" and q.alive and q.on_field(t):
            return s
        if s == "insubstantial" and q.on_field(t):
            return s
        if s in ("stopped", "fragile") and g.targetable(q):
            return s
    return None


def _try_finish(g: "Game", p: Player) -> bool:
    """Use a finisher on a target in its State: the caster's own set-up first, then the enemy
    engaged with a teammate, then the most kill potential."""
    if not _may_cast_now(g, p):
        return False
    options = sorted((u for u in _usable(g, p) if _is_offensive(u) and u.range != "Self" and finish_states(u.ability)),
                     key=lambda u: -g.value(u.ability, p))
    fighting = None
    for u in options:
        fs = finish_states(u.ability)
        foes = [(q, s) for q in g.enemies(p) if (s := _meets(g, q, fs)) and _can_hit(g, p, u, q)]
        if not foes:
            continue
        if fighting is None:
            fighting = _engaged_with_team(g, p)
        foes.sort(key=lambda qs: (qs[0].state_src.get(qs[1]) != p.pid, qs[0].pid not in fighting,
                                  -_threat(qs[0]), qs[0].pid))
        q = _first_in_range(g, u, [q for q, _ in foes])
        if q is not None and g.start_cast(p, u, q):
            return True
    return False


def _try_setup(g: "Game", p: Player) -> bool:
    """A doctrine's combo: cast a set-up whose finisher the caster also holds, on the enemy a
    controller would pick; _try_finish follows it up."""
    if not p.combos or not _may_cast_now(g, p):
        return False
    held = {}
    for u in _usable(g, p):
        held.setdefault(u.slug, u)
    for setup, finisher in p.combos:
        su, fu = held.get(setup), held.get(finisher)
        if su is None or fu is None or su.range == "Self":
            continue
        foes = [q for q in g.enemies(p) if g.targetable(q) and not _locked(g, q, su)
                and _can_hit(g, p, su, q) and not _resists(g, fu, q)]
        q = _first_in_range(g, su, _control_order(g, p, foes)) if foes else None
        if q is not None and g.start_cast(p, su, q):
            return True
    return False


def _enchant_kind(ab) -> str:
    """'weapon' (arms the bearer's blows: Flame Blade, Poison), 'armor' (armor, Resistances,
    Immunities, death prevention, equipment protection) or ''."""
    def calc(ab) -> str:
        effs = [e for e in ab.effects if is_handled(ab, e) and not is_drawback(ab, e)]
        if any(e.kind in _WEAPON_KINDS or (e.kind == "special-effect.grant"
               and e.params.get("on") in ("bearer-melee-weapons", "next-wound")) for e in effs):
            return "weapon"
        return "armor" if any(e.kind in _ARMOR_KINDS for e in effs) else ""
    return _cached("ench", ab, calc)


def _melee_rank(q: Player) -> tuple:
    return (q.role == "fighter" or q.play == "battle", q.skill, -q.pid)


def _enchant_priority(g: "Game", u: Uses, targets: list[Player]) -> Player:
    """The teammate who benefits most: weapon Enchantments to the best melee fighter, armor and
    protection to the front line (not backline, then skill); anything else to a random one."""
    kind = _enchant_kind(u.ability)
    if kind == "weapon":
        return max(targets, key=_melee_rank)
    if kind == "armor":
        return max(targets, key=lambda q: (not q.backline, q.skill, -q.pid))
    return g.rng.choice(targets)


def _try_refill(g: "Game", p: Player) -> bool:
    """Give back a spent use (Empower, Restoration, Confidence to a teammate out of melee; Innate to
    oneself) where it is worth most: the refill and teammate with the highest utility
    (enablers.py), if it beats the time the cast costs. The ability refilled is named when the
    cast resolves (Game.name_refill)."""
    if _engaged(g, p):
        return False
    best = None
    for u in _usable(g, p):
        if not enablers.is_refill(u.ability):
            continue
        if u.range in ("Self", "") or enablers.self_refill(u.ability):
            pool = [p]
        else:
            pool = [q for q in g.allies(p) if q.alive and q.on_field(g.t) and not (q is p and u.range == "Other")
                    and (q is p or not _engaged(g, q))]
        pool = [q for q in pool if _can_receive(g, u, p, q) and g.can_cast_at(p, q, u)
                and (q is p or not _resists(g, u, q))     # Void Touched, Rage (unaffected by Verbals), ...
                and g.check_requirements(u.ability, p, q, start=True, uses=u) is None]
        q, x = enablers.best_target(g, p, u, pool)
        if q is not None and (best is None or x > best[0]):
            best = (x, u, q)
    if best is None or not enablers.worth_casting(g, p, best[1], best[0]):
        return False
    _, u, q = best
    return (q is p or _in_reach(g, u)) and g.start_cast(p, u, q)


def _enchant_on_field(g: "Game", p: Player) -> bool:
    return g.rng.random() < g.rules.a("policy.p_enchant_ally_on_field") and _try_enchant(g, p, False, prioritized=True)


def _try_song(g: "Game", p: Player) -> bool:
    """Sing, or switch to, the song the situation needs (sim/policies/songs.py)."""
    return songs.try_song(g, p)


def _play_striker(g: "Game", p: Player) -> None:
    if _try_self_buff(g, p) or _try_finish(g, p) or _try_setup(g, p) or _try_refill(g, p) or _try_offense(g, p) \
            or _try_revive(g, p) or _try_heal(g, p) or _try_cleanse(g, p) or _enchant_on_field(g, p) \
            or _try_repair(g, p) or _try_shoot(g, p) or _try_song(g, p):
        return
    _try_charge(g, p)


def _play_controller(g: "Game", p: Player) -> None:
    if _try_self_buff(g, p) or _try_finish(g, p) or _try_control(g, p) or _try_refill(g, p) or _try_offense(g, p) \
            or _try_revive(g, p) or _try_heal(g, p) or _try_cleanse(g, p) or _enchant_on_field(g, p) \
            or _try_repair(g, p) or _try_shoot(g, p) or _try_song(g, p):
        return
    _try_charge(g, p)


def _play_enchanter(g: "Game", p: Player) -> None:
    if _try_enchant(g, p, False, prioritized=True, free_only=True) or _try_refill(g, p) \
            or _try_revive(g, p) or _try_heal(g, p) or _try_cleanse(g, p) or _try_repair(g, p) \
            or _try_finish(g, p) or _try_offense(g, p) or _try_shoot(g, p) or _try_song(g, p):
        return
    _try_charge(g, p)


def _play_medic(g: "Game", p: Player) -> None:
    if g.rules.a("policy.revive_priority") and _try_revive(g, p):
        return
    if _try_heal(g, p) or _try_cleanse(g, p) or _try_refill(g, p) or _enchant_on_field(g, p) or _try_repair(g, p) \
            or _try_offense(g, p) or _try_shoot(g, p) or _try_song(g, p):
        return
    _try_charge(g, p)


def _play_battle(g: "Game", p: Player) -> None:
    """Like a fighter: self-buffs and its song first, a step back to heal when wounded, then casts
    only when not in melee."""
    if _try_self_buff(g, p) or _try_song(g, p) or _try_step_back_heal(g, p):
        return
    if p.target is None and g.rng.random() < g.rules.a("policy.p_use_offensive_ability_when_free"):
        if _try_finish(g, p) or _try_setup(g, p) or _try_offense(g, p):
            return
    if p.target is None and (_try_heal(g, p) or _try_revive(g, p) or _try_refill(g, p) or _try_cleanse(g, p)
                             or _try_repair(g, p)):
        return
    if p.target is None:
        _try_charge(g, p)


def _play_archer(g: "Game", p: Player) -> None:
    """Shoot; between shots, cast. Without a bow (the Ranger Archetype ablated) play a striker."""
    if not p.has_bow:
        _play_striker(g, p)
        return
    if _try_shoot(g, p) or _try_finish(g, p) or _try_refill(g, p) or _try_offense(g, p) or _try_heal(g, p) \
            or _try_cleanse(g, p) or _try_song(g, p):
        return
    _try_charge(g, p)


PLAY_ROUTINES = {"striker": _play_striker, "controller": _play_controller, "enchanter": _play_enchanter,
                 "medic": _play_medic, "battle": _play_battle, "archer": _play_archer}


def decide(g: "Game", p: Player) -> None:
    t = g.t
    if p.at_base_until > t:
        _try_enchant(g, p, at_base=True, prioritized=bool(p.play)) or _try_song(g, p)
        return
    if _try_escape(g, p):
        return
    routine = PLAY_ROUTINES.get(p.play)
    if routine is not None:
        routine(g, p)
        return
    if p.role == "support":
        if g.rules.a("policy.revive_priority") and _try_revive(g, p):
            return
        if _try_heal(g, p) or _try_cleanse(g, p) or _try_refill(g, p):
            return
        if g.rng.random() < g.rules.a("policy.p_enchant_ally_on_field") and _try_enchant(g, p, False):
            return
        if _try_repair(g, p) or _try_offense(g, p) or _try_shoot(g, p) or _try_charge(g, p):
            return
    elif p.role == "caster":
        if _try_self_buff(g, p) or _try_refill(g, p) or _try_offense(g, p) or _try_revive(g, p) \
                or _try_heal(g, p) or _try_cleanse(g, p):
            return
        if g.rng.random() < g.rules.a("policy.p_enchant_ally_on_field") and _try_enchant(g, p, False):
            return
        if _try_repair(g, p) or _try_shoot(g, p) or _try_song(g, p):
            return
        _try_charge(g, p)
    elif p.role == "archer":
        if _try_shoot(g, p) or _try_heal(g, p) or _try_cleanse(g, p) or _try_refill(g, p):
            return
        _try_charge(g, p)
    else:
        if _try_self_buff(g, p) or _try_step_back_heal(g, p):
            return
        if p.target is None and g.rng.random() < g.rules.a("policy.p_use_offensive_ability_when_free"):
            if _try_offense(g, p):
                return
        if p.target is None and (_try_heal(g, p) or _try_revive(g, p) or _try_refill(g, p) or _try_cleanse(g, p)
                                 or _try_repair(g, p)):
            return
        if p.target is None:
            _try_charge(g, p)
