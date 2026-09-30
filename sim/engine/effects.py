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

from sim.engine.state import ARMS, INF, LEGS, LOCATIONS, Buff, Ench, Player, Restriction
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


# on-wound: Wound Triggers (Game._wound_trigger); on-choice: Gift of Air / Song of Survival options
# (Game._insubstantial_choice); on-strip: a strip spent to cast (Game._complete); on-removal: an
# Enchantment is removed (Game.remove_enchantment)
INSTANT_TIMINGS = frozenset({"on-cast", "on-struck", "on-kill", "on-death", "on-expiry", "on-wound", "on-choice",
                             "on-strip", "on-removal"})
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
    # caused by the player themself or by an Enchantment they carry (Song of Freedom's exception)
    own = p is ctx.caster or (ctx.ench is not None and ctx.bearer is p)
    if eff.duration_type == "timed" and eff.seconds:
        until = g.t + eff.seconds
    elif eff.duration_type == "until-arrival" and _returns_to_base(ctx.ability, eff):
        # Insubstantial while returning to base, ended on arrival (Gift of Air / Song of Survival option 2)
        until = g.arrival_time(p)
    elif state == "insubstantial" and p is ctx.caster and eff.duration_type in ("until-removed", "until-arrival"):
        # self-imposed Insubstantial: the policy ends it after a while (assumption), but not before
        # an exit-early lock (Martyr, Gift of Air option 2) allows it
        until = max(g.t + g.rules.a("policy.self_insubstantial_seconds"), p.exit_lock_until)
    else:
        until = INF
    return g.apply_state(p, state, until, own=own)


def h_state_prevent(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """Planar Grounding: the target may not become Insubstantial for 30 seconds."""
    p = subject(eff, ctx)
    if p is None or not p.alive or eff.duration_type != "timed":
        return False
    for s in eff.params.get("states") or ():
        p.prevented[s] = max(p.prevented.get(s, -1.0), g.t + (eff.seconds or 0.0))
    return True


def _returns_to_base(ab: Ability, eff: Effect) -> bool:
    return any(e.kind == "move.to-base" and e.timing == eff.timing and e.duration_type == "until-arrival"
               for e in ab.effects)


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
    # an object-destroying ability: only equipment that cannot be destroyed at all (Imbue) resists it
    if p.shield_usable() and not g.equipment_protection(p, "shield", object_destroying=True):
        p.shield_hits = 3
    elif p.weapon_ok and not g.equipment_protection(p, "weapon", object_destroying=True):
        p.weapon_ok = False
    else:
        return False
    return True


def h_enchantment_remove(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    p = subject(eff, ctx)
    scope = eff.params.get("scope", "all")
    if p is not None and scope == "auto-insubstantial-only":
        # Planar Grounding: registered with its prevention; Game.hit / Game.kill remove Gift of Air or
        # Song of Survival if they activate while the target may not become Insubstantial
        return p.prevented.get("insubstantial", -1.0) > g.t
    if p is None or not p.enchantments:
        return False
    if scope == "chosen-to-meet-limit":
        # Attuned, Essence Graft, Phoenix Tears removed: the bearer drops (m) Enchantments to meet the
        # new limit, keeping the ones worth most to them (Phoenix Tears' extra one may go, phoenix-tears#2)
        dropped = False
        while p.magical_enchantment_count() > p.ench_slots:
            pool = [e for e in p.enchantments if e.magical and not e.trait
                    and "exempt-from-enchantment-limit" not in e.ability.properties]
            if not pool:
                break
            g.remove_enchantment(p, min(pool, key=lambda e: (g.value(e.ability, p), e.ability.slug)))
            dropped = True
        return dropped
    if scope == "all":
        keep = [e for e in p.enchantments if "cannot-be-removed" in e.ability.properties]
        if ctx.ability.slug == "dispel-magic":
            # Sleight of Mind: Dispel Magic (from any source) removes only Sleight of Mind itself
            # (ruling sleight-of-mind#1)
            som = next((e for e in p.enchantments if e.ability.effects_of("enchantment.protect")), None)
            if som is not None:
                keep = [e for e in p.enchantments if e is not som]
                g.applied[(som.ability.slug, "enchantment.protect")] += 1
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
    if eff.params.get("on") == "bearer-melee-weapons":
        return h_buff(g, eff, ctx)      # Rage: the caster's melee weapons, for a time
    return eff.params.get("on") in ("this-magic-ball", "this-arrow")


def h_buff(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """An Ongoing Effect of a Verbal that Game queries like a worn one: timed (Rage, 7 s, ended by
    starting an Incantation) or lasting while its subject stays Insubstantial (Circle of Protection)."""
    p = subject(eff, ctx)
    if p is None or not p.alive:
        return False
    if eff.duration_type == "timed" and eff.seconds:
        until, rides = g.t + eff.seconds, None
    elif eff.timing == "while-active" and p.has_state("insubstantial", g.t):
        until, rides = INF, "insubstantial"
    else:
        return False
    p.buffs.append(Buff(ctx.ability.slug, eff, until, rides, "begins-incantation" in ctx.ability.termination))
    return True


def h_negate_lethal(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    # The lethal event is ignored: Game.kill already stopped the death before running on-death effects.
    return eff.params.get("from") == "lethal-event"


def h_death_prevent(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    # Game.kill already chose to prevent the death before running the on-death effects.
    return True


def h_equipment_disable(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """Heat Weapon: the target's weapon may not be wielded for 30 seconds; a player Immune to Flame
    may keep wielding it (E2; Game.blocked already stops the ability on them)."""
    p = ctx.target
    if p is None or not p.alive or eff.params.get("what") != "weapon":
        return False
    p.weapon_hot_until = max(p.weapon_hot_until, g.t + (eff.seconds or 0.0))
    p.target = None
    return True


def h_declare_instead(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """Elemental Barrage: the Magic Balls the caster carries now may be thrown by declaring their name
    instead of incanting (Game.start_cast), until the caster picks up a ball or begins casting another
    Magical ability (ruling elemental-barrage#1: only the balls carried at the time)."""
    p = ctx.caster
    carried = {s: u.left for s, u in sorted(p.uses.items())
               if u.ability.delivery == "magic-ball" and u.left and u.granted_by is None}
    p.barrage = carried or None
    return bool(carried)


def h_ability_grant(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """Blood and Thunder: on a kill the caster becomes enchanted with Blessing Against Wounds (ex).
    It lasts as that Enchantment does: until it stops a wound, or is removed (ruling
    blood-and-thunder#1). A player may not wear two (ex) Enchantments of the same name."""
    p = subject(eff, ctx)
    slug = g.rules.by_name.get(str(eff.params.get("ability", "")).lower())
    if p is None or not p.alive or slug is None or slug in g.ablate:
        return False
    granted = g.rules.abilities[slug]
    if granted.delivery != "enchantment" or any(e.ability.slug == slug for e in p.enchantments):
        return False
    magical = "(m)" in str(eff.params.get("frequency", ""))
    ench = Ench(granted, ctx.caster.pid, magical, granted.strips, "persistent" in granted.properties)
    p.enchantments.append(ench)
    g._activate(p, ench)
    return True


def h_action_restrict(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """Awe, Terror, Insult: the target may not attack or cast at (or only at) the caster, enforced by
    Game.can_attack / Game.can_cast_at. Martyr's exit-early locks the caster's transferred State."""
    p = subject(eff, ctx)
    if p is None or not p.alive:
        return False
    what = eff.params.get("what")
    if eff.duration_type == "timed":
        until = g.t + (eff.seconds or 0.0)
    elif eff.duration_type == "until-arrival" and _returns_to_base(ctx.ability, eff):
        until = g.arrival_time(p)
    else:
        until = INF
    if what == "exit-early":
        p.exit_lock_until = max(p.exit_lock_until, until)
        return True
    if what not in TARGET_RESTRICTS:
        return False
    term = ctx.ability.termination
    p.restrictions = [r for r in p.restrictions if not (r.slug == ctx.ability.slug and r.what == what)]
    p.restrictions.append(Restriction(
        what, ctx.caster.pid, until, ctx.ability.slug,
        negate_on_provoke="caster-attacks-or-casts-at-target" in term,
        ends_on_src_death=bool({"either-dies", "caster-dies"} & term)))
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
    "action.restrict": h_action_restrict,
    "ability.grant": h_ability_grant,
    "defense.unaffected": h_buff,
    "equipment.disable": h_equipment_disable,
    "state.prevent": h_state_prevent,
    "ability.declare-instead": h_declare_instead,
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
    "armor.limit", "equipment.permit", "economy.purchase-restrict", "economy.cost", "class.look-the-part",
})


# defense.unaffected variants Game checks (Game.unaffected, Game.blocked, Game.hit)
UNAFFECTED_BY = ("projectiles-except-magic-balls", "magical-abilities", "verbal-abilities",
                 "verbal-magical-beyond-touch", "schools", "blink", "forced-movement-except-banish")

# States a worn Enchantment/Trait imposes for as long as it is worn (a Chant is modeled as worn until
# removed, as for Song of Deflection)
PASSIVE_STATE_DURATIONS = ("while-worn", "permanent", "while-chanting")

# Parameter values the passive handlers in Game actually implement; other variants are no-ops.
PASSIVE_PARAMS: dict[str, Callable[[dict, Effect], bool]] = {
    "defense.negate-hit": lambda p, e: p.get("from") in ("hits-on-worn-armor", "weapons-and-arrows"),
    "defense.unaffected": lambda p, e: p.get("by") in UNAFFECTED_BY,
    "special-effect.grant": lambda p, e: (p.get("on") == "bearer-melee-weapons" and p.get("effect") in (
        "armor-breaking", "armor-destroying", "shield-crushing", "wounds-kill")) or (
        p.get("on") == "next-wound" and p.get("effect") == "wounds-kill"),   # Poison (Game._melee)
    "defense.resistance": lambda p, e: p.get("to") in ("next-source", "wounds", "chosen-school"),
    "state.apply": lambda p, e: e.duration_type in PASSIVE_STATE_DURATIONS,
    "ability.cast-via-strips": lambda p, e: bool(p.get("ability")),
}


_BECOMES_FREQ = re.compile(r"\bbecomes?\b.*\d+/(Life|Refresh)", re.I)
_SHIELDS = ("small-shield", "medium-shield", "large-shield")


def modify_change(change: str) -> str | None:
    """The loadout change an Archetype's `ability.modify` describes, normalized; None if it is not a
    frequency change the loadout applies."""
    if becomes_frequency(change):
        return "frequency"
    if "no longer chargeable" in change:
        return "no-charge"
    if m := re.search(r"becomes Charge x(\d+)", change):
        return f"charge-x{m.group(1)}"
    if re.search(r"\bbecomes? unlimited\b", change):
        return "unlimited"
    if m := re.search(r"becomes (\d+) Arrows? / Unlimited", change):
        return f"arrows-{m.group(1)}"
    if "double the uses" in change:
        return "double-uses"
    if "in place of Look the Part" in change:
        return "look-the-part"   # Raider; applied once, by the class.look-the-part record
    return None


# ability.modify changes the engine applies during play (Game), by a phrase of their text
ENGINE_MODIFIES = (
    "does not consume a use of Mend",                  # Artificer   (Game._complete)
    "Mend can remove a wound from the bearer",         # Golem       (Game._complete)
    "only one instance of Imbue may be active",        # Guardian    (Game.attach_enchantment)
    "combined total of five Undead Minion",            # Necromancer (Game.attach_enchantment)
    "works through their Cursed State",                # Vampirism   (Game._kill_trigger)
    "may only be used on Spirit abilities",            # Priest      (Game._meta_use)
)

# meta.modify-next modes the engine applies when a cast starts (Game._apply_meta_magic)
META_MODES = {"single-incantation": "swift", "extend-range-to-50ft": "extension",
              "persistent-enchantment": "persistent"}


def engine_modify(change: str) -> str | None:
    return next((k for k in ENGINE_MODIFIES if k in change), None)


def becomes_frequency(change: str) -> bool:
    """'X becomes 2/Life Charge x3': a new frequency for a named ability (not an example in passing,
    such as Legend's 'each purchase gives double the uses (e.g. 1/Life becomes 2/Life)')."""
    return bool(_BECOMES_FREQ.search(change)) and "e.g." not in change


# economy.frequency group scopes, as the metadata words them, and which of a player's uses each covers
FREQUENCY_GROUPS: dict[str, Callable] = {
    "each Verbal purchased": lambda u: u.purchased and u.ability.delivery == "verbal",
    "Extension (each purchase)": lambda u: u.purchased and u.ability.slug == "extension",
    "abilities in the Spirit School": lambda u: u.ability.school == "Spirit",
    "all abilities purchased in the Death School": lambda u: u.purchased and u.ability.school == "Death",
    "all Meta-Magics purchased": lambda u: u.purchased and u.ability.delivery == "meta-magic",
    "each type of Specialty Arrow ability": lambda u: u.ability.delivery == "specialty-arrow",
    "each Enchantment purchased": lambda u: u.purchased and u.ability.delivery == "enchantment",
    "all abilities purchased in the Protection School": lambda u: u.purchased and u.ability.school == "Protection",
    "Verbals and Magic Balls purchased in the Death and Flame Schools":
        lambda u: u.purchased and u.ability.delivery in ("verbal", "magic-ball") and u.ability.school in ("Death", "Flame"),
}
# Groups whose frequency is set outright, not just made chargeable: Priest "All Meta-Magics purchased
# become 1/Life Charge x3" (one use per purchase, ruling priest#1); Sniper "each type of Specialty Arrow
# ability becomes 1 Arrow / Life Charge x3" (one use per type, ruling sniper#1).
FREQUENCY_SET = {"all Meta-Magics purchased": "per-purchase", "each type of Specialty Arrow ability": "one"}
EXPERIENCED_SCOPES = {
    "a single purchased per-life Verbal of 4th level or lower": "life",
    "a single purchased per-refresh Verbal of 4th level or lower": "refresh",
}
# (scope, 'other') changes spelled out in the ability text (Brutal Strike: Raider's Look the Part use)
FREQUENCY_OTHER = ("Archer Specialty Arrows", "Ancestral Armor", "Brutal Strike")


def is_equipment(ab: Ability) -> bool:
    return ab.slug.startswith("equipment-")


# economy.purchase-restrict scopes: what a Magic User with the Archetype may not buy.
# Predicates take (class-table entry, ability, normalized range).
PURCHASE_RESTRICT: dict[str, Callable] = {
    "Enchantments and Magic Balls": lambda c, ab, rng: ab.delivery in ("enchantment", "magic-ball"),
    "Verbals with a range of 20' or 50'": lambda c, ab, rng: ab.delivery == "verbal" and rng in ("20'", "50'"),
    "Swift": lambda c, ab, rng: ab.slug == "swift",
    "any abilities from the Protection School": lambda c, ab, rng: ab.school == "Protection",
    "equipment beyond 2nd level": lambda c, ab, rng: is_equipment(ab) and min(c.levels) > 2,
    "any abilities from the Death, Command, or Subdual Schools":
        lambda c, ab, rng: ab.school in ("Death", "Command", "Subdual"),
    "Verbals or Magic Balls from any School other than the Death and Flame Schools":
        lambda c, ab, rng: ab.delivery in ("verbal", "magic-ball") and ab.school not in ("Death", "Flame"),
}
# economy.cost scopes and changes: point costs for a Magic User with the Archetype
COST_SCOPES: dict[str, Callable] = {
    "Equipment": is_equipment,
    "all available Equipment": is_equipment,
    "Heal": lambda ab: ab.slug == "heal",
    "Enchantments": lambda ab: ab.delivery == "enchantment",
}
COST_CHANGES = {"double": 2, "zero": 0}


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
        return named("ability") and modify_change(str(prm.get("change", ""))) is not None
    if eff.kind == "economy.frequency":
        change = str(prm.get("change", ""))
        scope = str(prm.get("scope", ""))
        if change == "other":
            return scope in FREQUENCY_OTHER
        if scope in EXPERIENCED_SCOPES:
            return bool(re.fullmatch(r"charge-x\d+", change))
        ok_change = change in ("double-uses", "unlimited") or bool(re.fullmatch(r"charge-x\d+", change))
        return ok_change and (scope in FREQUENCY_GROUPS or named("scope"))
    if eff.kind == "equipment.permit":
        return prm.get("what") in _SHIELDS + ("great-weapon", "bows", "any-number-of-specialty-arrows")
    if eff.kind == "armor.limit":
        return prm.get("change") in ("set", "increase")
    if eff.kind == "class.look-the-part":
        return prm.get("how") in ("extra-use-of", "replaced-by") and named("ability")
    if eff.kind == "economy.purchase-restrict":
        return prm.get("scope") in PURCHASE_RESTRICT        # loadout._magic_user
    if eff.kind == "economy.cost":
        return prm.get("scope") in COST_SCOPES and prm.get("change") in COST_CHANGES
    return False


# ---------------------------------------------------------------- explicit "not modeled" modes

# Effects Phase 1 cannot model honestly. They are counted apart from no-ops, each with its reason,
# so they are never hidden: the coverage report lists them, and at run time they are logged in the
# `noop` metric under the detail "<mode>:<kind>".
NEEDS_MAP = "needs-map"
OUT_OF_SCOPE = "out-of-scope"

# (kind, predicate on (ability, effect) or None for every instance, mode, reason)
UNMODELED_RULES: tuple = (
    ("team.alternate-base", None, NEEDS_MAP,
     "An Alternate Base only changes where Forced Movement to base may end; Phase 1 has no positions."),
    ("team.respawn-point", None, NEEDS_MAP,
     "A respawn point is a place on the field; Phase 1 respawns everyone at an abstract base."),
    ("action.restrict", lambda a, e: e.params.get("what") == "use-alternate-bases", NEEDS_MAP,
     "Forbids using Alternate Bases, which need positions to mean anything (see team.alternate-base)."),
    ("action.restrict", lambda a, e: e.params.get("what") == "move-from-start", NEEDS_MAP,
     "Forbids moving from a starting spot; Phase 1 has no positions."),
    ("action.restrict", lambda a, e: e.params.get("what") == "exit-early" and a.slug == "blink", NEEDS_MAP,
     "Blink may not be ended within 10' of a living enemy: a distance check between two players."),
    (None, lambda a, e: a.slug == "sanctuary", NEEDS_MAP,
     "Sanctuary protects only against hostile acts from within 20', and its limits (no approaching an "
     "enemy base, no game items, no impeding play, free movement, exit only at base after touching a "
     "weapon) are about positions and objectives; Sanctuary is not modeled at all."),
    ("action.restrict", lambda a, e: e.params.get("what") in ("wield-javelins", "wield-heavy-thrown", "wield-long-weapons"),
     OUT_OF_SCOPE, "Phase 1 has no thrown weapons and does not tell weapon lengths apart (only Great "
     "weapons), so there is nothing to forbid."),
    ("defense.negate-engulfing", lambda a, e: e.subject == "bearer-equipment", OUT_OF_SCOPE,
     "Imbue ignores Engulfing effects that hit the bearer's wielded equipment; Phase 1 resolves every "
     "projectile on a body location and never models a strike on carried equipment."),
    ("meta.modify-next", lambda a, e: e.params.get("mode") == "cast-while-moving", NEEDS_MAP,
     "Ambulant lets the next ability be cast while moving; Phase 1 has no movement, so casting "
     "already ignores it."),
    ("move.free", None, NEEDS_MAP,
     "Moving freely (Blink within 50', Reload retrieving arrows) is pure positioning."),
    ("move.keep-away", lambda a, e: e.params.get("from") == "combat", NEEDS_MAP,
     "Reload's 'stay at least 10' away from combat' is a distance from other players' fights."),
    ("life.set-death-location", None, NEEDS_MAP,
     "Summon Dead moves where a dead player counts as having died; Phase 1 has no positions."),
    ("casting.modify", lambda a, e: "empty hand" in str(e.params.get("change", "")), OUT_OF_SCOPE,
     "Phase 1 does not model hands or what they hold, so casting never needs an empty hand."),
    (None, lambda a, e: a.slug == "missile-block", OUT_OF_SCOPE,
     "Blocking projectiles with hands or weapons is a physical skill; Phase 1 has no chance-to-block "
     "assumption, so Missile Block would do nothing (its negate-hit was previously counted as handled "
     "but never applied)."),
    ("ability.cast-while-insubstantial", lambda a, e: a.slug == "circle-of-protection", OUT_OF_SCOPE,
     "Circle members acting on each other needs Circle's group targeting (caster plus up to five) and "
     "acting while Insubstantial; Phase 1 applies Circle to one target, and no scripted role casts it."),
    (None, lambda a, e: a.slug == "trickery", NEEDS_MAP,
     "Trickery chains positional escapes (Blink, Shadow Step, Teleport while already Insubstantial); "
     "without movement the chain has nothing to model."),
    ("equipment.permit", lambda a, e: e.params.get("what") == "carry-extras", OUT_OF_SCOPE,
     "Spare equipment only matters for replacing broken gear, and Phase 1 has no backup weapons or "
     "shields (a destroyed item stays destroyed until repaired or respawn)."),
    ("equipment.permit", lambda a, e: e.params.get("what") in ("hinged-weapon", "long-weapon", "short-weapon", "javelins"),
     OUT_OF_SCOPE, "Phase 1 tells only Great weapons apart from other melee weapons and has no thrown "
     "weapons, so permitting another weapon type changes nothing it models."),
    (None, lambda a, e: a.slug == "song-of-visit", OUT_OF_SCOPE,
     "Song of Visit is a non-combat visit (Stopped and Invulnerable while chanting, then an Invulnerable "
     "walk to base); ending the Chant is the Bard's choice and Phase 1 has no rule for when to stop, so "
     "modeling it would park the Bard for the rest of the game."),
)


def unmodeled(ability: Ability, eff: Effect) -> tuple[str, str] | None:
    """(mode, reason) when this effect is explicitly not modeled in Phase 1. A rule with kind None
    covers every effect of the abilities its predicate selects."""
    for kind, pred, mode, reason in UNMODELED_RULES:
        if (kind is None or eff.kind == kind) and (pred is None or pred(ability, eff)):
            return mode, reason
    return None


# ---------------------------------------------------------------- handled modes for newer kinds

# action.restrict variants and where the engine enforces them
TARGET_RESTRICTS = ("attack-caster", "cast-at-caster", "attack-anyone-but-caster", "cast-at-anyone-but-caster")
LOADOUT_RESTRICTS = ("wear-armor", "wield-great-weapons", "wield-shields", "wield-large-shields", "wield-bows")
PASSIVE_RESTRICTS = ("wield-weapons", "wield-shields", "fire-normal-arrows", "wear-others-magical-enchantments")


def h_meta(g: "Game", eff: Effect, ctx: Ctx) -> bool:
    """A Meta-Magic stated on its own modifies the caster's next ability (Game._apply_meta_magic)."""
    mode = eff.params.get("mode")
    if mode not in META_MODES:
        return False
    ctx.caster.meta_armed.add(META_MODES[mode])
    return True


INSTANT["meta.modify-next"] = h_meta


def _meta_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    return "instant" if eff.params.get("mode") in META_MODES and eff.timing == "on-cast" else None


def _restrict_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    what = eff.params.get("what")
    if eff.timing == "on-cast" and (what in TARGET_RESTRICTS or what == "exit-early"):
        return "instant"      # Game.can_attack / can_cast_at; exit-early locks the caster's State
    if eff.timing == "on-choice" and what == "exit-early":
        return "instant"      # Game._insubstantial_choice, option 2
    if eff.timing == "while-active":
        if ab.delivery in ("archetype", "trait") and what in LOADOUT_RESTRICTS:
            return "loadout"  # sim/engine/loadout.py strips the forbidden equipment
        if ab.delivery in PASSIVE_DELIVERIES and what in PASSIVE_RESTRICTS:
            return "passive"  # Game.barred
        if ab.delivery == "enchantment" and what == "use-other-sources-of-ability":
            return "passive"  # Game._meta_use (Amplification, Silver Tongue)
    return None


# "As per X" grants: the bearer is treated as wearing X's while-active effects (Game._passive_effects),
# except Ancestral Armor, which applies to the granting Enchantment's own Magic Armor (Game.hit).
AS_PER_EXPAND = ("Enlightened Soul", "Regeneration")
AS_PER_MAGIC_ARMOR = "Ancestral Armor"


def _named_ok(prm: dict, key: str = "ability") -> bool:
    return bool(re.fullmatch(r"[A-Z][A-Za-z' ]+", str(prm.get(key, ""))))


def _grant_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    prm = eff.params
    if eff.timing == "while-active":
        if ab.delivery in ("archetype", "trait"):
            return "loadout" if loadout_handled(eff, names) else None
        if ab.delivery != "enchantment" or not (_named_ok(prm) if names is None
                                                 else str(prm.get("ability", "")).lower() in names):
            return None
        if prm.get("how") == "as-per":
            what = prm.get("ability")
            if what in AS_PER_EXPAND:
                return "passive"
            if what == "Harden" and ab.slug in AS_PER_HARDEN:
                return "passive"     # Game.equipment_protection
            if what == AS_PER_MAGIC_ARMOR and ab.effects_of("armor.magic"):
                return "passive"
            return None
        return "passive"   # Game._activate adds the granted uses; Game.remove_enchantment takes them away
    if eff.timing == "on-kill" and _named_ok(prm):
        return "instant"   # h_ability_grant (Blood and Thunder)
    return None


def _modify_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    prm = eff.params
    if eff.timing != "while-active":
        return None
    change = str(prm.get("change", ""))
    if engine_modify(change) and ab.delivery in PASSIVE_DELIVERIES:
        return "passive"
    if ab.delivery in ("archetype", "trait"):
        return "loadout" if loadout_handled(eff, names) else None
    if ab.delivery != "enchantment":
        return None
    # modifiers of an ability the same Enchantment grants: applied to the granted uses in Game._grant
    if prm.get("requirement") or "only be cast with the bearer as the target" in change \
            or "ignores the requirement that the target has not moved" in change:
        return "passive"
    return None


def _wound_heal_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    if eff.timing == "while-active":
        # Golem: the bearer's wound is removed by Mend (Game._complete), paired with its ability.modify
        mend = any(e.kind == "ability.modify" and engine_modify(str(e.params.get("change", ""))) ==
                   "Mend can remove a wound from the bearer" for e in ab.effects)
        return "passive" if mend and ab.delivery in PASSIVE_DELIVERIES else None
    return "instant" if eff.timing in INSTANT_TIMINGS else None


# "As per Harden" grants and what each covers (Harden itself: weapons or shield, the bearer's choice)
AS_PER_HARDEN = {"gift-of-earth": "weapons-or-shield", "greater-harden": "weapons-and-shields",
                 "sacred-blades": "weapons"}


def _equipment_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    """equipment.protect / armor.protect / defense.negate-engulfing / weapon.ignore-protections on worn
    Enchantments: Game queries them where equipment, armor and wounds are hit."""
    if eff.timing != "while-active" or ab.delivery not in PASSIVE_DELIVERIES:
        return None
    return "passive"


def _passive_ok(ab: Ability, eff: Effect) -> bool:
    check = PASSIVE_PARAMS.get(eff.kind)
    return ab.delivery in PASSIVE_DELIVERIES and (check is None or check(eff.params, eff))


def _unaffected_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    by = eff.params.get("by")
    if eff.timing == "while-active":
        if ab.delivery in PASSIVE_DELIVERIES:
            return "passive" if _passive_ok(ab, eff) else None
        # Circle of Protection: registered on its targets at cast, lasting while they stay Insubstantial
        return "instant" if by in ("blink", "forced-movement-except-banish") else None
    if eff.timing == "on-cast" and eff.duration_type == "timed" and by in UNAFFECTED_BY:
        return "instant"   # Rage (h_buff)
    return None


def _special_mode(ab: Ability, eff: Effect, names: set[str] | None = None) -> str | None:
    on = eff.params.get("on")
    if eff.timing == "while-active":
        return "passive" if _passive_ok(ab, eff) else None
    if eff.timing == "on-cast" and on == "bearer-melee-weapons" and eff.duration_type == "timed":
        return "instant"   # Rage (h_buff)
    return "instant" if on in ("this-magic-ball", "this-arrow") and eff.timing in INSTANT_TIMINGS else None


# Kinds whose handled mode is decided by a rule function (None = no-op for that instance).
MODE_RULES: dict[str, Callable[..., str | None]] = {
    "action.restrict": _restrict_mode,
    "ability.grant": _grant_mode,
    "ability.modify": _modify_mode,
    "wound.heal": _wound_heal_mode,
    "defense.unaffected": _unaffected_mode,
    "special-effect.grant": _special_mode,
    "equipment.protect": _equipment_mode,
    "armor.protect": _equipment_mode,
    "defense.negate-engulfing": _equipment_mode,
    "weapon.ignore-protections": _equipment_mode,
    "meta.modify-next": _meta_mode,
    "state.prevent": lambda ab, eff, names=None: (
        "instant" if eff.timing == "on-cast" and eff.duration_type == "timed"
        else "passive" if eff.timing == "while-active" and ab.delivery in PASSIVE_DELIVERIES else None),
    "ability.charge-faster": _equipment_mode,      # Game.start_charge (Song of Power)
    "ability.declare-instead": lambda ab, eff, names=None: (
        "passive" if ab.delivery == "enchantment" and eff.timing == "while-active"     # Mass Healing
        else "instant" if ab.delivery == "verbal" and eff.timing == "while-active"     # Elemental Barrage
        else None),
    # read by Game: respawn (make-persistent, prevent-respawn) and h_enchantment_remove (protect)
    "enchantment.make-persistent": _equipment_mode,
    "enchantment.protect": _equipment_mode,
    "life.prevent-respawn": _equipment_mode,
    "enchantment.remove": lambda ab, eff, names=None: (
        "instant" if (eff.timing in INSTANT_TIMINGS or eff.params.get("scope") == "auto-insubstantial-only")
        else None),
}


def _legacy_handled(ability: Ability, eff: Effect, names: set[str] | None) -> bool:
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


def _handled_mode(ability: Ability, eff: Effect, names: set[str] | None) -> str | None:
    rule = MODE_RULES.get(eff.kind)
    if rule is not None:
        return rule(ability, eff, names)
    if not _legacy_handled(ability, eff, names):
        return None
    if eff.timing == "while-active":
        return "loadout" if eff.kind in LOADOUT and ability.delivery in ("archetype", "trait") else "passive"
    return "instant"


def is_handled(ability: Ability, eff: Effect, names: set[str] | None = None) -> bool:
    if unmodeled(ability, eff) is not None:
        return False
    return _handled_mode(ability, eff, names) is not None


def handling(ability: Ability, eff: Effect, names: set[str] | None = None) -> str:
    """'instant' / 'passive' / 'loadout' / 'needs-map' / 'out-of-scope' / 'no-op' (coverage report)."""
    um = unmodeled(ability, eff)
    if um is not None:
        return um[0]
    return _handled_mode(ability, eff, names) or "no-op"


def runtime_noop_detail(ability: Ability, eff: Effect) -> str:
    """Detail for the run-time `noop` counter: the kind, prefixed by the mode when the effect is
    explicitly not modeled, so needs-map / out-of-scope stay separable from true no-ops."""
    um = unmodeled(ability, eff)
    return f"{um[0]}:{eff.kind}" if um else eff.kind
