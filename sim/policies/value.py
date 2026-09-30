"""A rough, hand-set usefulness score per ability, used by Magic Users to buy spells and by
policies to pick which ability to use. Only effects the engine handles score anything, so an
ability whose effects are all no-ops is never bought or cast deliberately.

Benefits add to the score and **drawbacks subtract** from it. A drawback is a harmful effect on
the user's own side: on the caster or bearer (Gift of Air's "may not wield weapons", Berserker's
"may not wear armor", Martyr taking the State), or on an ally the ability is meant to help (the
States Raise Dead leaves on the raised player). A harmful effect on an enemy is the point of the
ability and counts as a benefit.

**Direct effects** (a kill, a wound, a heal, a State on an enemy, Magic Armor) score from the flat
tables below (`KIND_WEIGHT`, `STATE_WEIGHT`, `SPECIAL_WEIGHT`, `EQUIPMENT_WEIGHT`).

**Enablers are valued by what they enable** (compositional). Their value is the value of the
abilities they act on, computed with this same function, so it follows its target:

| Effect | Worth |
| --- | --- |
| `ability.grant` (gains) | the granted ability's value to the one who receives it, times `frequency_factor` of the granted frequency: uses count like copies (copy k is worth `COPY_DECAY ** k`), Unlimited (not ammunition) is worth `UNLIMITED_FACTOR`, a Charge adds `CHARGE_GAIN`. The same rules the buyer (`buy.py`) uses for copies, Unlimited purchases and frequency changes |
| `ability.grant` (as per) | the named ability's value (the bearer is treated as wearing it) |
| a modifier of the granted ability on the same Enchantment | folded into the grant: "can only be cast with the bearer as the target" makes an Unlimited grant worth one copy (Undead Minion: one player's deaths bound the uses); the others (a waived or added requirement) are left to the grant and the drawbacks |
| `ability.modify`, `economy.frequency` | the gain on the abilities affected: their value times `frequency_gain` (double uses, Unlimited, Charge), best per ability. A change the engine applies but that is not a frequency (Golem's Mend removing a wound) keeps the flat `UNPRICED_WEIGHT` |
| `ability.charge` | the value of the ability it refills: the named spent ability when the context gives one (`Ctx.spent`), otherwise the mean over the recipient's chargeable abilities (Empower, Confidence and Restoration excluded, rule text) |
| `ability.restore-uses` | one use: the mean over the recipient's per-life abilities (Empower); all uses: `RESTORE_ALL_USES` of them (Restoration); a named ability: its value (Rogue's Coup de Grace) |
| `enchantment.extra-slot` | the best Enchantments that could fill the slots, k-th slot times `COPY_DECAY ** k`: for an Enchantment cast on another player, the caster's own Enchantments castable on another (any, Protection school only for Phoenix Tears, the caster's (m) for Essence Graft); for a Self one (Evolution), any teammate's, times the share of classes that are Magic Users (the bearer can't fill it; only a teammate's cast can) |
| `ability.charge-faster` | Song of Power: the Charge seconds saved on a typical chargeable ability (the mean over every class list's chargeable entries: xN becomes x(N // 2), minimum 1) times `policy.value_per_threat_second` times the chance the teammate is within 20', for one Charge per song. The songs' own exchange rate: a teammate Charging is one threat unit per second (`songs.py`) |
| `meta.modify-next` | Extension: `1 - p(20') / p(50')` (the share of casts it makes possible, as `Game._apply_meta_magic` rolls it) of the mean value of the holder's own 20' Verbals. Swift: the mean incantation seconds it saves on the holder's Touch, Other, Self and Magic Ball abilities, times `policy.value_per_threat_second`. Persistent: `PERSISTENT_SHARE` of the mean value of the holder's non-Persistent Enchantments |
| `ability.cast-via-strips` | the ability's value times `held_worth(strips)` |
| a refill offered as a choice (Steal Life Essence: "Caster may heal a wound or instantly Charge an ability") | the better of the two options, not both |

An enabled ability counts at its value floored at 0: one not worth using is simply not used
(Guardian grants Martyr, whose drawbacks outweigh it).

**Drawbacks are priced in context**: by what the one who bears them actually loses. Each rule
comes from the ability's text (`rules/magic-and-abilities/<slug>.md`):

| Drawback | Cost |
| --- | --- |
| `action.restrict` on equipment (armor, shields, weapons, bows) | `restrict_cost`: what the bearer actually carries, or a typical player of the role |
| `action.restrict` "may not utilize other sources" (Amplification, Silver Tongue: "Other sources of Extension may not be utilized while Amplification is worn") | the bearer's own copies of the granted ability, valued like any held copies; nothing for a bearer without one (the typical bearer, without context) |
| `state.apply` Stopped on the bearer of a Self Enchantment while it is worn or chanted (Song of Power: "Bearer is Stopped"; Heart of the Swarm) | the mechanic requires it; it costs the Stopped weight times `MOBILITY` of the bearer: full for a player who fights in the line (fighter role or battle play), little for a backline caster, who in Phase 1 (no map) loses only the chance to step away |
| `enchantment.remove` on removal, "chosen to meet limit" (Attuned, Essence Graft, Phoenix Tears: "If Attuned is removed, the bearer chooses which (m) Enchantments to lose") | nothing at cast: it only takes back what the slot allowed |
| `life.prevent-respawn` (Undead Minion: "Bearer ... cannot Respawn", while "the caster gains Raise Dead (Unlimited)") | the respawn it replaces: a revive's weight times the chance the caster doesn't raise the bearer before the respawn would have come, `(respawn.rejoin_seconds + Raise Dead's incantation) / the game type's respawn seconds` (150 s in annihilation, 60 s in attrition; without a game type, the mixed preset's shares) |
| `ability.remove` | the removed ability's value if the player holds it, else nothing; without context the flat weight |
| any other | the flat `STATE_WEIGHT` / `DRAWBACK_WEIGHT` |

**Context** (`Ctx`): the holder's and the bearer's kits (`Kit`: abilities with copies and
frequency, role, play, equipment), the spent ability a refill is for, the game type and the
ablated abilities. Without it each missing kit is a *typical player of the role*: the abilities on
the class lists of classes of that role (only those that list the ability, for its holder), each
once. With it, the actual kit. A Self ability's bearer is its holder.

Values are memoized per rules object and context. A loop (Troll Blood as per Regeneration is
fine; Empower on Empower, an Enchantment filling its own slot) counts as nothing, and a value
computed through a loop cut is not memoized unless the cut lies inside its own computation, so
results don't depend on call order.
"""
from __future__ import annotations

import math
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Iterable

from sim.engine.effects import EXPERIENCED_SCOPES, FREQUENCY_GROUPS, is_handled
from sim.policies import calibration
from sim.rules import frequency as freqmod
from sim.rules.compile import Ability, Effect

if TYPE_CHECKING:
    from sim.engine.state import Player
    from sim.rules.compile import Rules

# ---------------------------------------------------------------- anchor weights
#
# The HAND_* tables are the hand-set weights. They are the fallback, and the value of every weight
# the calibration doesn't measure. The tables in use (KIND_WEIGHT, STATE_WEIGHT, ...) come from
# sim/policies/calibration.py: the measured weight where sim/data/value-calibration.json has one
# (see "Calibration" in the module docstring), the hand weight otherwise; TABLES.sources says which.

HAND_STATE_WEIGHT = {"stunned": 6, "frozen": 4, "stopped": 4, "suppressed": 3, "fragile": 4,
                     "insubstantial": 3, "cursed": 2}

HAND_KIND_WEIGHT = {
    "death.cause": 10, "life.revive": 9, "death.prevent": 7, "wound.inflict": 5, "wound.heal": 4,
    "defense.immunity": 3, "defense.resistance": 3, "defense.negate-hit": 4, "defense.unaffected": 3,
    "armor.repair": 2, "armor.destroy": 3, "armor.damage": 1, "enchantment.remove": 3,
    "move.to-base": 3, "move.push": 2, "move.keep-away": 2, "move.to-location": 2, "move.to-caster": 1,
    "state.remove": 2, "equipment.repair": 1, "equipment.destroy": 2, "special-effect.grant": 2,
    # Elemental Barrage and the like: every carried Magic Ball thrown with a word, not an incantation
    "ability.declare-instead": 4,
}

# Special effects granted to weapons or carried by a ball or arrow. Wounds Kill turns every limb hit
# into a kill, so it is worth far more than breaking a point of armor.
HAND_SPECIAL_WEIGHT = {"wounds-kill": 6, "armor-destroying": 3, "armor-breaking": 2, "phasing": 2,
                  "shield-crushing": 1.5, "weapon-destroying": 1, "shield-destroying": 1}

# What a drawback costs, by kind, when it isn't a State or a restriction and nothing in the
# context prices it (module docstring).
DRAWBACK_WEIGHT = {
    "ability.remove": 2, "economy.purchase-restrict": 1, "economy.cost": 1, "enchantment.remove": 2,
    "armor.damage": 1, "life.prevent-respawn": 3, "defense.unaffected": 2, "state.transfer": 2,
    "armor.limit": 2, "economy.frequency": 1, "ability.modify": 1,
}

HEALING = {"life.revive", "wound.heal", "death.prevent", "state.remove", "armor.repair"}
OFFENSE = {"death.cause", "wound.inflict", "move.to-base", "armor.destroy", "enchantment.remove"}

# Equipment a Magic User can buy: a shield blocks blows in melee, a Great weapon is Armor Breaking
# and Shield Crushing. A larger shield permit also permits the smaller, so only the best counts.
HAND_EQUIPMENT_WEIGHT = {"small-shield": 2.0, "medium-shield": 3.0, "large-shield": 3.5, "great-weapon": 2.0,
                         "bows": 4.0}

# Per-unit weights. charge_second None: `policy.value_per_threat_second` (sim/data/assumptions.json).
HAND_SCALAR_WEIGHT = {
    "armor_point": 2.0,          # a point of worn armor on every location (armor.limit increase)
    "armor_loss_point": 2.0,     # a point of worn armor taken away ("may not wear armor")
    "magic_armor_point": 2.0,    # a point of Magic Armor (armor.magic)
    "charge_second": None,       # a second of Charge incantation saved (Song of Power)
}
# Factors on compositional values (module docstring, "Calibration").
HAND_FACTOR = {
    "stack_share": 0.5,          # share of a filler Enchantment an extra slot adds: the filler could
                                 # usually go on another teammate; the slot adds it when none is free
    "refill_factor": 1.0,        # share of the refilled ability an instant Charge is worth
    "fighter_heal": 1.0,         # share of a Heal's weight a fighter gets from it
}
HAND = {"kind": HAND_KIND_WEIGHT, "state": HAND_STATE_WEIGHT, "special": HAND_SPECIAL_WEIGHT,
        "equipment": HAND_EQUIPMENT_WEIGHT, "scalar": HAND_SCALAR_WEIGHT, "factor": HAND_FACTOR}

TABLES = calibration.tables(HAND, calibration.load())


def _install(t: "calibration.Tables") -> None:
    global TABLES, KIND_WEIGHT, STATE_WEIGHT, SPECIAL_WEIGHT, EQUIPMENT_WEIGHT, SCALAR_WEIGHT, FACTOR
    TABLES = t
    KIND_WEIGHT, STATE_WEIGHT = t.weights["kind"], t.weights["state"]
    SPECIAL_WEIGHT, EQUIPMENT_WEIGHT = t.weights["special"], t.weights["equipment"]
    SCALAR_WEIGHT, FACTOR = t.weights["scalar"], t.weights["factor"]


_install(TABLES)


@contextmanager
def hand_weights():
    """Value with the hand tables for the duration (the calibration harness's residuals). Values
    are memoized per rules object: use a rules object of your own (build_rules())."""
    saved = TABLES
    _install(calibration.tables(HAND, None))
    try:
        yield
    finally:
        _install(saved)


@contextmanager
def using(doc: dict | None):
    """Value with the tables built from this calibration document (None: hand) for the duration.
    Use a rules object of your own, as for hand_weights()."""
    saved = TABLES
    _install(calibration.tables(HAND, doc))
    try:
        yield
    finally:
        _install(saved)

# ---------------------------------------------------------------- frequency (shared with buy.py)

COPY_DECAY = 0.6        # each further copy (or use) of an ability is worth 0.6 of the previous one
UNLIMITED_FACTOR = 2.0  # an Unlimited ability that isn't ammunition is worth two copies
CHARGE_GAIN = 0.3       # a use that can be Charged back is worth 30% more

# Enabler assumptions (module docstring). Hand-set, like the weights above.
UNPRICED_WEIGHT = 0.5    # an engine-applied text change the valuation can't price (Golem's Mend)
RESTORE_ALL_USES = 2     # per-life uses Restoration gives back when it is worth casting
PERSISTENT_SHARE = 0.5   # share of an Enchantment's value Persistent adds: it outlives about one death in two
# How much a self-imposed Stopped costs, by how the bearer fights: a line fighter can't close to
# melee; a backline caster or healer mostly stands anyway (no map in Phase 1).
MOBILITY = {"line": 1.0, "archer": 0.5, "backline": 0.25}

ENABLER_KINDS = frozenset({
    "ability.grant", "ability.modify", "economy.frequency", "ability.charge", "ability.restore-uses",
    "enchantment.extra-slot", "ability.charge-faster", "meta.modify-next", "ability.cast-via-strips"})
# drawbacks whose price depends on the context (`_context_drawback`)
CONTEXT_DRAWBACKS = frozenset({"action.restrict", "life.prevent-respawn", "ability.remove"})
# refills can't refill these (Empower, Restoration: "Does not function on Empower, Confidence, or Restoration")
_REFILLS = ("ability.charge", "ability.restore-uses")


def held_worth(copies: int) -> float:
    """Copies (or uses) of one ability, in units of one copy's value: copy k is worth COPY_DECAY ** k."""
    return sum(COPY_DECAY ** k for k in range(max(0, copies)))


def frequency_gain(change: str, copies: int) -> float:
    """A frequency change to an ability held `copies` times, in units of that ability's value and
    on the same scale as the build score (copy k is worth COPY_DECAY ** k): doubling adds copies
    n..2n-1, Unlimited is worth what an Unlimited purchase is, a Charge adds CHARGE_GAIN."""
    held = held_worth(copies)
    change = change.lower()
    if "unlimited" in change:
        return (UNLIMITED_FACTOR - 1.0) * held
    if "double" in change:
        return sum(COPY_DECAY ** k for k in range(copies, 2 * copies))
    if "charge" in change:
        return CHARGE_GAIN * held
    return 0.0


def frequency_factor(f: freqmod.Frequency) -> float:
    """What holding an ability at frequency f is worth, in units of one copy's value: its uses count
    like copies, Unlimited (not ammunition) is UNLIMITED_FACTOR, a Charge adds CHARGE_GAIN."""
    w = held_worth(f.uses or 1)
    if f.per == "unlimited" and not f.unit:
        w *= UNLIMITED_FACTOR
    if f.charge:
        w *= 1.0 + CHARGE_GAIN
    return w


# ---------------------------------------------------------------- context

@dataclass(frozen=True)
class Held:
    """One ability in a kit."""
    slug: str
    copies: int = 1
    charge: int | None = None     # Charge xN, if chargeable
    per: str | None = None        # life / refresh / unlimited
    range: str = ""               # as held (a class table may narrow it: "(Self)")
    magical: bool = True
    purchased: bool = False


@dataclass(frozen=True)
class Kit:
    """What one player holds. Equipment fields None: a typical player of the role."""
    role: str
    held: tuple[Held, ...] = ()
    play: str = ""
    armor_max: int | None = None
    shield: str | None = None
    great_weapon: bool | None = None
    has_bow: bool | None = None

    def copies(self, slug: str) -> int:
        return sum(h.copies for h in self.held if h.slug == slug)

    @classmethod
    def of(cls, p: "Player") -> "Kit":
        """The player's own abilities (not those an Enchantment grants for a while) and equipment."""
        held = tuple(sorted(
            (Held(u.slug, u.copies, u.charge, u.per, u.base_range or u.range, u.magical, u.purchased)
             for u in p.uses.values() if u.granted_by is None and u.ench is None),
            key=lambda h: (h.slug, h.range)))
        held += tuple(Held(t.slug, p.trait_copies.get(t.slug, 1)) for t in sorted(p.traits, key=lambda t: t.slug))
        return cls(p.role, held, p.play, p.armor_max, p.shield, p.great_weapon, p.has_bow)

    @classmethod
    def build(cls, role: str, owned: dict[str, int], entries: Iterable, play: str = "") -> "Kit":
        """A Magic User's kit at loadout: `owned` (slug -> copies) with frequencies from the class
        table `entries` (ClassAbility)."""
        info = {c.slug: c for c in entries}
        held = []
        for slug, n in sorted(owned.items()):
            c = info.get(slug)
            if c is None:
                held.append(Held(slug, n))
            else:
                held.append(Held(slug, n, c.freq.charge, c.freq.per, c.range, c.freq.magical is not False, True))
        return cls(role, tuple(held), play)


@dataclass(frozen=True)
class Ctx:
    """Who holds and who receives the ability. Anything left None is a typical player."""
    holder: Kit | None = None       # who holds and casts it
    bearer: Kit | None = None       # who wears it or is its target (a Self ability: the holder)
    spent: str | None = None        # the ability a Charge or restore refills
    game_type: str | None = None    # 'annihilation' / 'attrition'; None: the mixed preset's shares
    ablate: frozenset = frozenset()


def _sub(ctx: Ctx | None, kit: Kit | None) -> Ctx | None:
    """The context for valuing an ability that `kit` holds (a grant, a filler, a refill target)."""
    if ctx is None or (kit is None and ctx.game_type is None and not ctx.ablate):
        return None
    return Ctx(holder=kit, game_type=ctx.game_type, ablate=ctx.ablate)


# ---------------------------------------------------------------- drawbacks

_OWN_SIDE = ("caster", "bearer", "bearer-equipment", "group")


def is_drawback(ability: Ability, eff: Effect) -> bool:
    if eff.polarity != "harm":
        return False
    if eff.subject in _OWN_SIDE:
        return True
    return eff.subject in ("target", "dead-target") and ability.beneficiary in ("ally", "self", "team")


def restrict_cost(what: str, role: str, p: "Player | Kit | None" = None) -> float:
    """What a restriction on the bearer's equipment costs. With a player (or a kit that knows its
    equipment), the cost is what that player would actually lose (their armor, their shield);
    without one, a typical player of the role."""
    melee = role in ("fighter", "archer")

    def known(attr: str):
        return getattr(p, attr, None) if p is not None else None

    if what == "wield-weapons":
        return 8.0 if melee else 2.0
    if what in ("fire-normal-arrows", "wield-bows"):
        bow = known("has_bow")
        return (8.0 if bow else 0.0) if bow is not None else (8.0 if role == "archer" else 0.0)
    if what == "wear-armor":
        armor = known("armor_max")
        per = SCALAR_WEIGHT["armor_loss_point"]
        return per * armor if armor is not None else per * (2.0 if melee else 0.25)
    if what == "wield-shields":
        shield = known("shield")
        typical = EQUIPMENT_WEIGHT["small-shield"] * (1.0 if melee else 0.25)
        return EQUIPMENT_WEIGHT.get(f"{shield}-shield", 0.0) if shield is not None else typical
    if what == "wield-large-shields":
        shield = known("shield")
        return (0.5 if shield == "large" else 0.0) if shield is not None else 0.5
    if what == "wield-great-weapons":
        great = known("great_weapon")
        return (2.0 if great else 0.0) if great is not None else 1.0
    return 1.0


def mobility(role: str, kit: Kit | None) -> float:
    """MOBILITY for the bearer: 'line' for a fighter or a battle-play caster."""
    role = kit.role if kit is not None else role
    play = kit.play if kit is not None else ""
    if role == "fighter" or play == "battle":
        return MOBILITY["line"]
    return MOBILITY["archer"] if role == "archer" else MOBILITY["backline"]


# ---------------------------------------------------------------- typical kits

_ROLE_BY_CLASS: dict | None = None


def _role_by_class() -> dict:
    global _ROLE_BY_CLASS
    if _ROLE_BY_CLASS is None:
        from sim.engine.loadout import ROLE_BY_CLASS    # loadout imports buy imports this module
        _ROLE_BY_CLASS = ROLE_BY_CLASS
    return _ROLE_BY_CLASS


def _held_from(entries: Iterable) -> tuple[Held, ...]:
    seen, out = set(), []
    for c in entries:
        key = (c.slug, c.freq.charge, c.freq.per, c.range)
        if c.kind == "archetype" or key in seen:
            continue
        seen.add(key)
        out.append(Held(c.slug, 1, c.freq.charge, c.freq.per, c.range, c.freq.magical is not False,
                        c.kind == "spell"))
    return tuple(sorted(out, key=lambda h: (h.slug, h.range, h.charge or 0, h.per or "")))


def _memo(rules: "Rules") -> dict:
    m = rules.__dict__.get("_value_memo")
    if m is None:
        m = rules.__dict__["_value_memo"] = {}
    return m


def typical_kit(rules: "Rules", role: str, listing: str | None = None) -> Kit:
    """A typical player of the role: every ability on the class lists of classes of that role
    (only classes that list `listing`, if any do), once each."""
    key = ("typical", role, listing)
    memo = _memo(rules)
    if key not in memo:
        rbc = _role_by_class()
        names = sorted(n for n in rules.classes if rbc.get(n) == role) or sorted(rules.classes)
        if listing is not None:
            listed = [n for n in names if any(c.slug == listing for c in rules.classes[n].abilities)]
            names = listed or names
        entries = [c for n in names for c in rules.classes[n].abilities]
        memo[key] = Kit(role, _held_from(entries))
    return memo[key]


def team_kit(rules: "Rules") -> Kit:
    """Every class list: what a teammate might hold (Song of Power's Charges, Evolution's filler)."""
    key = ("team",)
    memo = _memo(rules)
    if key not in memo:
        memo[key] = Kit("", _held_from(c for n in sorted(rules.classes) for c in rules.classes[n].abilities))
    return memo[key]


# ---------------------------------------------------------------- the valuation

def _self_range(ab: Ability) -> bool:
    return ab.delivery in ("trait", "archetype", "meta-magic") or ab.range == "Self"


_DEPENDS: dict[int, tuple[Ability, bool]] = {}


def _context_drawback(ab: Ability, eff: Effect) -> bool:
    return eff.kind in CONTEXT_DRAWBACKS or _self_stopped(ab, eff)


def _self_stopped(ab: Ability, eff: Effect) -> bool:
    """Stopped on the bearer of a Self ability while it is worn or chanted: the mechanic's own cost."""
    return eff.kind == "state.apply" and eff.params.get("state") == "stopped" and _self_range(ab) \
        and eff.duration_type in ("while-chanting", "while-worn")


def depends_on_context(ab: Ability) -> bool:
    """Whether the ability's value can depend on the context (enablers, context-priced drawbacks)."""
    hit = _DEPENDS.get(id(ab))
    if hit is None or hit[0] is not ab:
        dep = any(is_handled(ab, e) and (e.kind in ENABLER_KINDS or (is_drawback(ab, e) and _context_drawback(ab, e)))
                  for e in ab.effects)
        hit = _DEPENDS[id(ab)] = (ab, dep)
    return hit[1]


class _Eval:
    """One top-level valuation: the recursion stack and loop cuts (see the module docstring)."""

    def __init__(self, rules: "Rules"):
        self.rules = rules
        self.memo = _memo(rules)
        self.stack: list[str] = []
        self.min_cut = math.inf      # shallowest stack depth a loop was cut at, in the current subtree

    # ---------------------------------------------------------- recursion
    def value(self, ab: Ability, role: str, ctx: Ctx | None) -> float:
        if ctx is not None and not depends_on_context(ab):
            ctx = None
        key = ("value", ab.slug, role, ctx)
        if key in self.memo:
            return self.memo[key]
        if ab.slug in self.stack:
            self.min_cut = min(self.min_cut, self.stack.index(ab.slug))
            return 0.0
        depth = len(self.stack)
        outer, self.min_cut = self.min_cut, math.inf
        self.stack.append(ab.slug)
        try:
            b = sum(c for *_, c in self.benefits(ab, role, ctx))
            v = b - sum(c for *_, c in self.drawbacks(ab, role, ctx)) if b > 0 else 0.0
        finally:
            self.stack.pop()
        sub, self.min_cut = self.min_cut, min(outer, self.min_cut)
        if sub >= depth:            # no loop cut above this frame: the result doesn't depend on the path
            if len(self.memo) > 200_000:
                self.memo.clear()
            self.memo[key] = v
        return v

    def enabled(self, ab: Ability, role: str, ctx: Ctx | None) -> float:
        """The value of an ability another one enables (or takes away): never below 0, since an
        ability not worth using is simply not used (Guardian's Martyr)."""
        return max(0.0, self.value(ab, role, ctx))

    def named(self, name, ctx: Ctx | None) -> Ability | None:
        slug = self.rules.by_name.get(str(name or "").lower())
        if slug is None or (ctx is not None and slug in ctx.ablate):
            return None
        return self.rules.abilities.get(slug)

    def recipient(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[Kit | None, str]:
        """Who receives the effect: the holder (caster, Self abilities) or the bearer or target."""
        if ctx is None:
            return None, role
        kit = ctx.holder if (eff.subject in ("caster", "caster-of-enchantment") or _self_range(ab)) else ctx.bearer
        return kit, (kit.role if kit is not None else role)

    def kit_or_typical(self, kit: Kit | None, role: str, listing: str | None) -> Kit:
        return kit if kit is not None else typical_kit(self.rules, role, listing)

    def mean_value(self, abilities: Iterable[Ability], role: str, ctx: Ctx | None) -> float:
        vals = [v for a in abilities if (v := self.value(a, role, ctx)) > 0]
        return sum(vals) / len(vals) if vals else 0.0

    def held_abilities(self, kit: Kit, ctx: Ctx | None, keep) -> list[tuple[Held, Ability]]:
        out = []
        for h in kit.held:
            ab = self.rules.abilities.get(h.slug)
            if ab is not None and (ctx is None or h.slug not in ctx.ablate) and keep(h, ab):
                out.append((h, ab))
        return out

    # ---------------------------------------------------------- benefits
    def benefits(self, ab: Ability, role: str, ctx: Ctx | None) -> list[tuple[str, str, float]]:
        """(effect id, label, contribution) per handled, non-drawback effect."""
        out: list[tuple[str, str, float]] = []
        equipment: tuple[str, str, float] | None = None
        freq_best: dict[str, tuple[str, str, float]] = {}   # a frequency change is often recorded twice
        granted = {str(e.params.get("ability", "")) for e in ab.effects if e.kind == "ability.grant"}
        for eff in ab.effects:
            if not is_handled(ab, eff) or is_drawback(ab, eff):
                continue
            if eff.kind == "equipment.permit":
                w = EQUIPMENT_WEIGHT.get(eff.params.get("what", ""), 0.0)
                if equipment is None or w > equipment[2]:
                    equipment = (eff.id, f"permit {eff.params.get('what')}", w)
                continue
            if eff.kind in ("ability.modify", "economy.frequency"):
                if eff.kind == "ability.modify" and str(eff.params.get("ability", "")) in granted:
                    continue        # a modifier of this Enchantment's own grant: folded into the grant
                for slug, label, w in self.frequency_change(ab, eff, role, ctx):
                    if slug not in freq_best or w > freq_best[slug][2]:
                        freq_best[slug] = (eff.id, label, w)
                continue
            out.append((eff.id, *self.effect_benefit(ab, eff, role, ctx)))
        if "has-choice" in ab.properties:
            out = self.choose_refill(ab, out)
        out.extend(freq_best[s] for s in sorted(freq_best))
        if equipment is not None:
            out.append(equipment)
        return out

    @staticmethod
    def choose_refill(ab: Ability, out: list) -> list:
        """A refill offered as a choice beside another effect on the same player at the same moment
        (Steal Life Essence: "Caster may heal a wound or instantly Charge an ability") is worth
        the better option, not both: the refill adds only what it beats the alternative by."""
        effs = {e.id: e for e in ab.effects}
        res = []
        for i, label, c in out:
            e = effs.get(i)
            if e is not None and e.kind in _REFILLS:
                alt = max((c2 for i2, _, c2 in out if i2 != i and effs.get(i2) is not None
                           and effs[i2].kind not in _REFILLS and effs[i2].subject == e.subject
                           and effs[i2].timing == e.timing), default=None)
                if alt is not None:
                    res.append((i, f"{label} (or the alternative: +{max(0.0, c - alt):.2f})", max(0.0, c - alt)))
                    continue
            res.append((i, label, c))
        return res

    def effect_benefit(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        k = eff.kind
        if k == "ability.grant":
            return self.grant(ab, eff, role, ctx)
        if k in _REFILLS:
            return self.refill_value(ab, eff, role, ctx)
        if k == "enchantment.extra-slot":
            return self.extra_slot(ab, eff, role, ctx)
        if k == "ability.charge-faster":
            return self.charge_faster(ab, eff, role, ctx)
        if k == "meta.modify-next":
            return self.meta(ab, eff, role, ctx)
        if k == "ability.cast-via-strips":
            target = self.named(eff.params.get("ability"), ctx)
            if target is None:
                return "strips of an unknown ability", 0.0
            kit, r = self.recipient(ab, eff, role, ctx)
            v = self.enabled(target, r, _sub(ctx, kit)) * held_worth(ab.strips or 1)
            return f"{target.slug} x{ab.strips or 1} strips", v
        return k, direct_benefit(ab, eff, role)

    def grant(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        prm = eff.params
        target = self.named(prm.get("ability"), ctx)
        if target is None:
            return "grant of an unknown ability", 0.0
        kit, r = self.recipient(ab, eff, role, ctx)
        v = self.enabled(target, r, _sub(ctx, kit))
        if prm.get("how") == "as-per":
            return f"as per {target.slug}", v
        f = freqmod.parse(str(prm.get("frequency", "")))
        factor = frequency_factor(f)
        one_target = any(m.kind == "ability.modify" and m.params.get("ability") == prm.get("ability")
                         and is_handled(ab, m) and "only be cast with the bearer as the target" in str(m.params.get("change", ""))
                         for m in ab.effects)
        if one_target and f.per == "unlimited" and not f.unit:
            factor /= UNLIMITED_FACTOR      # one player's deaths bound the uses: worth one copy
        return f"grant {target.slug} x{factor:.2f}", v * factor

    def frequency_change(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> list[tuple[str, str, float]]:
        """(target slug, label, gain) for each ability a frequency change or modify acts on."""
        key = "scope" if eff.kind == "economy.frequency" else "ability"
        scope = str(eff.params.get(key, ""))
        change = str(eff.params.get("change", ""))
        holder = ctx.holder if ctx is not None else None
        group = FREQUENCY_GROUPS.get(scope)
        if scope in EXPERIENCED_SCOPES:     # "a single purchased per-life Verbal of 4th level or lower"
            per = EXPERIENCED_SCOPES[scope]
            group = lambda u, per=per: u.ability.delivery == "verbal" and u.per == per   # noqa: E731
        if frequency_gain(change, 1) == 0.0:
            # a change the engine applies that isn't a frequency (Golem's Mend removing a wound)
            return [(f"{eff.id}:text", f"unpriced change to {scope}", UNPRICED_WEIGHT)]
        sub = _sub(ctx, holder)
        if group is not None:
            kit = self.kit_or_typical(holder, role, ab.slug)
            members = self.held_abilities(kit, ctx, lambda h, a: group(_UsesView(a, h.purchased or holder is None, h.per)))
            if holder is None or scope in EXPERIENCED_SCOPES:   # a typical member; Experienced: a single one
                if holder is not None:
                    best = max((self.enabled(a, role, sub) for _, a in members), default=0.0)
                    return [(f"group:{scope}", f"{change} on the best of {scope}", best * frequency_gain(change, 1))]
                mean = self.mean_value((a for _, a in members), role, sub)
                return [(f"group:{scope}", f"{change} on {scope}", mean * frequency_gain(change, 1))]
            return [(h.slug, f"{change} on {h.slug}", self.enabled(a, role, sub) * frequency_gain(change, h.copies))
                    for h, a in members]
        target = self.named(scope, ctx)
        if target is None:
            return []
        copies = holder.copies(target.slug) if holder is not None else 1
        return [(target.slug, f"{change} on {target.slug}",
                 self.enabled(target, role, sub) * frequency_gain(change, copies))]

    def refill(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        kit, r = self.recipient(ab, eff, role, ctx)
        sub = _sub(ctx, kit)
        named = self.named(eff.params.get("ability"), ctx)
        if named is not None:
            return f"refill {named.slug}", self.enabled(named, r, sub)
        if ctx is not None and ctx.spent:
            spent = self.rules.abilities.get(ctx.spent)
            if spent is not None:
                return f"refill {spent.slug}", self.enabled(spent, r, sub)
        listing = ab.slug if kit is None and eff.subject == "caster" else None
        pool = self.kit_or_typical(kit, r, listing)

        def ok(h: Held, a: Ability) -> bool:
            if a.slug == ab.slug or any(e.kind in _REFILLS for e in a.effects):
                return False
            return bool(h.charge) if eff.kind == "ability.charge" else h.per == "life"

        mean = self.mean_value((a for _, a in self.held_abilities(pool, ctx, ok)), r, sub)
        if eff.kind == "ability.restore-uses" and eff.params.get("amount") == "all":
            return f"restore {RESTORE_ALL_USES} per-life uses", mean * RESTORE_ALL_USES
        return ("charge" if eff.kind == "ability.charge" else "restore") + " a typical use", mean

    def refill_value(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        """`refill`, with an instant Charge scaled by what one is worth in play (`refill_factor`)."""
        label, v = self.refill(ab, eff, role, ctx)
        if eff.kind == "ability.charge":
            f = refill_factor(self.rules)
            if f != 1.0:
                return f"{label} x{f:.2f} (instant Charge in play)", v * f
        return label, v

    def chargeable_mean(self, role: str) -> float:
        """What refilling a typical chargeable ability is worth to a typical player of the role."""
        kit = typical_kit(self.rules, role)
        return self.mean_value((a for h, a in self.held_abilities(kit, None, lambda h, a: bool(h.charge)
                                                                       and not any(e.kind in _REFILLS for e in a.effects))),
                               role, None)

    def extra_slot(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        """An extra Enchantment slot adds only the stacking: the Enchantment that fills it could
        usually have gone on another teammate instead. So it is worth the best fillers times
        `stack_share`, the share of a filler's value a slot adds (measured by giving fighters an
        extra slot; module docstring)."""
        only = str(eff.params.get("only", "any"))
        count = int(eff.params.get("count", 1) or 1)
        holder = ctx.holder if ctx is not None else None
        fill = 1.0
        if _self_range(ab):
            # teammates fill it (Evolution), and only a Magic User teammate who picks this bearer
            pool, sub = team_kit(self.rules), _sub(ctx, None)
            fill = mu_share(self.rules)
        else:
            pool, sub = self.kit_or_typical(holder, role, ab.slug), _sub(ctx, holder)
        share = stack_share(self.rules)
        v = fill * share * self.slot_fillers(pool, sub, ctx, role, only, count, ab.slug)
        return (f"{count} slot(s) for the best Enchantments ({only}) x{share:.2f} stacking"
                + (f", filled {fill:.2f}" if fill < 1 else "")), v

    def slot_fillers(self, pool: Kit, sub: Ctx | None, ctx: Ctx | None, role: str, only: str, count: int,
                     own: str = "") -> float:
        """The best `count` Enchantments in `pool` that could fill an extra slot, k-th times COPY_DECAY ** k."""
        def fills(h: Held, a: Ability) -> bool:
            if a.delivery != "enchantment" or a.slug == own or "exempt-from-enchantment-limit" in a.properties:
                return False
            if a.effects_of("enchantment.extra-slot") or (h.range or a.range) == "Self":
                return False          # "not in conjunction with ... similar abilities"; cast on another
            if only == "protection-school":
                return a.school == "Protection"
            if only == "magical-from-this-caster":
                return h.magical
            return True

        cands = {a.slug: a for _, a in self.held_abilities(pool, ctx, fills)}
        vals = sorted((self.value(a, role, sub) for a in cands.values()), reverse=True)[:count]
        return sum(x * COPY_DECAY ** k for k, x in enumerate(vals) if x > 0)

    def charge_faster(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        rules = self.rules
        per_rep = rules.a("time.charge_incantation_words") / rules.a("time.speech_words_per_second")
        charges = sorted({h.charge for h in team_kit(rules).held if h.charge})
        entries = [h.charge for h in team_kit(rules).held if h.charge]
        if not entries:
            return "no chargeable abilities", 0.0
        saved = sum((n - max(1, n // 2)) * per_rep for n in entries) / len(entries)
        v = saved * charge_second(rules) * rules.a("range.p_in_range")["20'"]
        return f"{saved:.0f} s saved per Charge (x{charges})", v

    def meta(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        mode = eff.params.get("mode")
        kit, r = self.recipient(ab, eff, role, ctx)
        pool = self.kit_or_typical(kit, r, ab.slug if kit is None else None)
        sub = _sub(ctx, kit)
        rules = self.rules
        own = lambda h: h.slug != ab.slug     # noqa: E731
        if mode == "extend-range-to-50ft":
            table = rules.a("range.p_in_range")
            share = 1.0 - table["20'"] / table["50'"]
            cands = self.held_abilities(pool, ctx, lambda h, a: own(h) and a.delivery == "verbal"
                                        and (h.range or a.range) == "20'")
            return f"{share:.2f} of a 20' Verbal", share * self.mean_value((a for _, a in cands), r, sub)
        if mode == "single-incantation":
            wps = rules.a("time.speech_words_per_second")
            saved = []
            for h, a in self.held_abilities(pool, ctx, lambda h, a: own(h) and (
                    (h.range or a.range) in ("Touch", "Other", "Self") or a.delivery == "magic-ball")):
                full = a.cast_seconds(wps)
                single = max(1.0, float(round(a.words / wps)))
                if full > single and self.value(a, r, sub) > 0:
                    saved.append(full - single)
            s = sum(saved) / len(saved) if saved else 0.0
            return f"{s:.1f} s of incantation saved", s * rules.a("policy.value_per_threat_second")
        if mode == "persistent-enchantment":
            cands = self.held_abilities(pool, ctx, lambda h, a: own(h) and a.delivery == "enchantment"
                                        and "persistent" not in a.properties)
            return "a Persistent Enchantment", PERSISTENT_SHARE * self.mean_value((a for _, a in cands), r, sub)
        return f"meta {mode}", 0.0

    # ---------------------------------------------------------- drawbacks
    def drawbacks(self, ab: Ability, role: str, ctx: Ctx | None) -> list[tuple[str, str, float]]:
        out = []
        for eff in ab.effects:
            if is_handled(ab, eff) and is_drawback(ab, eff):
                out.append((eff.id, *self.drawback(ab, eff, role, ctx)))
        return out

    def drawback(self, ab: Ability, eff: Effect, role: str, ctx: Ctx | None) -> tuple[str, float]:
        kit, r = self.recipient(ab, eff, role, ctx)
        k, prm = eff.kind, eff.params
        if k == "action.restrict":
            what = str(prm.get("what", ""))
            if what == "use-other-sources-of-ability":
                if kit is None:
                    return "no other source (typical bearer)", 0.0
                cost = 0.0
                for g in ab.effects_of("ability.grant"):
                    other = self.named(g.params.get("ability"), ctx)
                    if other is not None and kit.copies(other.slug):
                        cost += self.enabled(other, r, _sub(ctx, kit)) * held_worth(kit.copies(other.slug))
                return "the bearer's own copies unusable", cost
            return f"may not {what}", restrict_cost(what, r, kit)
        if k == "state.apply":
            state = prm.get("state", "")
            if _self_stopped(ab, eff):
                m = mobility(r, kit)
                return f"self-imposed Stopped (mobility {m})", STATE_WEIGHT["stopped"] * m
            return f"state {state}", STATE_WEIGHT.get(state, 1)
        if k == "enchantment.remove" and eff.timing == "on-removal":
            return "drops Enchantments only when it ends", 0.0
        if k == "life.prevent-respawn":
            late = self.late_share(ctx)
            return f"respawn replaced ({late:.2f} late)", KIND_WEIGHT["life.revive"] * late
        if k == "ability.remove" and kit is not None:
            gone = self.named(prm.get("ability"), ctx)
            n = kit.copies(gone.slug) if gone is not None else 0
            return f"loses {prm.get('ability')}", self.enabled(gone, r, _sub(ctx, kit)) * held_worth(n) if n else 0.0
        return k, DRAWBACK_WEIGHT.get(k, 1)

    def late_share(self, ctx: Ctx | None) -> float:
        """Chance the Undead Minion's caster doesn't raise the bearer before a respawn would have
        come: (the walk back + Raise Dead's incantation) / the game type's respawn seconds."""
        from sim.scenarios import GAME_TYPES, PRESETS
        rd = self.rules.abilities.get("raise-dead")
        raise_s = self.rules.a("respawn.rejoin_seconds") + (
            rd.cast_seconds(self.rules.a("time.speech_words_per_second")) if rd else 0.0)
        shares = {ctx.game_type: 1.0} if ctx is not None and ctx.game_type else PRESETS["mixed"]["game_types"]
        total = sum(shares.values())
        return sum(w / total * min(1.0, raise_s / GAME_TYPES[gt]["respawn_seconds"])
                   for gt, w in sorted(shares.items()) if gt in GAME_TYPES)


def mu_share(rules: "Rules") -> float:
    """Share of classes that are Magic Users: the chance a teammate can fill a Self extra slot."""
    return sum(c.magic_user for c in rules.classes.values()) / max(1, len(rules.classes))


def charge_second(rules: "Rules") -> float:
    """Value of a second of Charge incantation saved: calibrated, else `policy.value_per_threat_second`."""
    w = SCALAR_WEIGHT.get("charge_second")
    return w if w is not None else rules.a("policy.value_per_threat_second")


def _factor(rules: "Rules", name: str, compositional) -> float:
    """A calibrated factor: the measured score over the compositional value, in [0, 1]; the hand
    factor when the calibration has none. Computed once per rules object."""
    measured = TABLES.measured.get(f"factor.{name}")
    if measured is None:
        return FACTOR[name]
    key = ("factor", name, id(TABLES))
    memo = _memo(rules)
    if key not in memo:
        c = compositional(_Eval(rules))
        memo[key] = min(1.0, max(0.0, measured / c)) if c > 0 else FACTOR[name]
    return memo[key]


def stack_share(rules: "Rules") -> float:
    """The share of a filler Enchantment an extra slot adds. Calibrated: the measured value of an
    extra slot on a fighter, whom teammates fill, over the compositional value of that slot (the
    best Enchantment on the class lists times the Magic User share)."""
    return _factor(rules, "stack_share", lambda ev: mu_share(rules) * ev.slot_fillers(
        team_kit(rules), None, None, "fighter", "any", 1))


def refill_factor(rules: "Rules") -> float:
    """The share of the refilled ability an instant Charge (Momentum, Steal Life Essence, Empower's
    kind) is worth in play. Calibrated: the measured value of an instant Charge per life over the
    mean value of a typical chargeable ability of the recipients' roles."""
    roles = TABLES.roles.get("factor.refill_factor") or {"fighter": 1}

    def comp(ev: "_Eval") -> float:
        n = sum(roles.values())
        return sum(k / n * ev.chargeable_mean(r) for r, k in roles.items() if r) if n else 0.0
    return _factor(rules, "refill_factor", comp)


class _UsesView:
    """What FREQUENCY_GROUPS reads from a use."""
    __slots__ = ("ability", "purchased", "per")

    def __init__(self, ability: Ability, purchased: bool, per: str | None = None):
        self.ability, self.purchased, self.per = ability, purchased, per


# ---------------------------------------------------------------- public API

def direct_benefit(ability: Ability, eff: Effect, role: str) -> float:
    """A handled, non-drawback effect's flat contribution (the tables at the top)."""
    if eff.kind == "armor.limit" and eff.params.get("change") == "increase":
        return SCALAR_WEIGHT["armor_point"] * int(eff.params.get("points", 1))  # worn armor: it can be repaired
    if eff.kind == "state.apply":
        w = STATE_WEIGHT.get(eff.params.get("state", ""), 1)
        if eff.subject in ("caster", "bearer"):
            w = 0.5  # a State on yourself is usually a cost, not a benefit
    elif eff.kind == "armor.magic":
        w = SCALAR_WEIGHT["magic_armor_point"] * int(eff.params.get("points", 1))
    elif eff.kind == "special-effect.grant":
        w = SPECIAL_WEIGHT.get(eff.params.get("effect", ""), 2)
        if eff.params.get("on") == "next-wound":
            w *= 0.5    # one blow, not every blow
    else:
        w = KIND_WEIGHT.get(eff.kind, UNPRICED_WEIGHT)
    if role == "support" and eff.kind in HEALING:
        w *= 1.5
    if role == "fighter" and eff.kind == "wound.heal":
        w *= FACTOR["fighter_heal"]     # how much of a Heal a fighter uses (calibration)
    if role == "caster" and eff.kind in OFFENSE:
        w *= 1.3
    return w


def _rules(rules: "Rules | None") -> "Rules":
    if rules is None:
        from sim.rules.compile import default_rules
        rules = default_rules()
    return rules


def effect_benefit(ability: Ability, eff: Effect, role: str, ctx: Ctx | None = None,
                   rules: "Rules | None" = None) -> float:
    """One handled, non-drawback effect's contribution to the score (enablers by what they enable)."""
    if eff.kind not in ENABLER_KINDS:
        return direct_benefit(ability, eff, role)
    ev = _Eval(_rules(rules))
    if eff.kind in ("ability.modify", "economy.frequency"):
        return max((w for *_, w in ev.frequency_change(ability, eff, role, ctx)), default=0.0)
    return ev.effect_benefit(ability, eff, role, ctx)[1]


def benefit(ability: Ability, role: str, ctx: Ctx | None = None, rules: "Rules | None" = None) -> float:
    return sum(c for *_, c in _Eval(_rules(rules)).benefits(ability, role, ctx))


def drawback_cost(ability: Ability, role: str, p: "Player | None" = None, ctx: Ctx | None = None,
                  rules: "Rules | None" = None) -> float:
    """What the ability's drawbacks cost. `p`: the player who would bear them (as the holder of a
    Self ability, else as the bearer), when no fuller context is given."""
    if ctx is None and p is not None:
        kit = Kit.of(p)
        ctx = Ctx(holder=kit, bearer=kit)
    return sum(c for *_, c in _Eval(_rules(rules)).drawbacks(ability, role, ctx))


def value(ability: Ability, role: str, ctx: Ctx | None = None, rules: "Rules | None" = None) -> float:
    """Benefits minus drawbacks. Zero or less: not worth buying or casting as a matter of course."""
    return _Eval(_rules(rules)).value(ability, role, ctx)


def breakdown(ability: Ability, role: str, ctx: Ctx | None = None,
              rules: "Rules | None" = None) -> list[tuple[str, str, float]]:
    """(effect id, label, signed contribution): benefits positive, drawbacks negative."""
    ev = _Eval(_rules(rules))
    return ev.benefits(ability, role, ctx) + [(i, l, -c) for i, l, c in ev.drawbacks(ability, role, ctx)]


def player_ctx(g, p: "Player") -> Ctx:
    """The context for p's own abilities in a game: p's kit, the game type, the ablated abilities.
    Built once per player and game (Game._value_cache)."""
    key = ("ctx", p.pid)
    c = g._value_cache.get(key)
    if c is None:
        c = g._value_cache[key] = Ctx(holder=Kit.of(p), game_type=g.sc.get("game_type"),
                                      ablate=frozenset(g.ablate))
    return c


def value_for(g, ability: Ability, p: "Player") -> float:
    """`value` of p's ability in game g, in p's context (Game.value), cached for the game."""
    key = (ability.slug, p.pid)
    v = g._value_cache.get(key)
    if v is None:
        ctx = player_ctx(g, p) if depends_on_context(ability) else None
        v = g._value_cache[key] = value(ability, p.role, ctx, g.rules)
    return v
