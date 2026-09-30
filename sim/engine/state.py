"""Mutable per-game state: players, ability uses, enchantments, casts."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from sim.rules.compile import Ability

LOCATIONS = ("torso", "left_arm", "right_arm", "left_leg", "right_leg")
ARMS = ("left_arm", "right_arm")
LEGS = ("left_leg", "right_leg")
INF = math.inf

# States that stop a player acting at all this tick.
NO_ACTION_STATES = ("frozen", "stunned", "insubstantial", "invulnerable")


@dataclass(slots=True)
class Uses:
    ability: Ability
    per: str | None             # life / refresh / unlimited / None (trait/archetype)
    max: int | None             # None = unlimited
    left: int | None
    charge: int | None
    unit: str | None            # balls / arrows
    magical: bool
    ambulant: bool = False
    swift: bool = False
    range: str = ""
    ench: "Ench | None" = None   # set when the use comes from an Enchantment's strips
    granted_by: "Ench | None" = None   # granted while an Enchantment is worn (tracked separately)
    extra_reqs: frozenset = frozenset()  # requirements added by the granting ability (Regeneration)
    drop_reqs: frozenset = frozenset()   # requirements the granting ability waives (Undead Minion)
    only_target: int | None = None       # may only be cast on this player (Undead Minion's Raise Dead)
    base_range: str = ""                 # range before Extension is offered (Game._offer_extension)
    declare_words: int | None = None     # cast by a declaration, not an incantation (Mass Healing)
    purchased: bool = False              # bought with Magic User points (Archetype group scopes)
    copies: int = 1                      # purchases or picks merged into this use

    @property
    def slug(self) -> str:
        return self.ability.slug

    def available(self) -> bool:
        return self.left is None or self.left > 0

    def spend(self) -> None:
        if self.left is not None:
            self.left -= 1

    def restore(self, n: int = 1) -> None:
        if self.left is not None and self.max is not None:
            self.left = min(self.max, self.left + n)


@dataclass(slots=True)
class Ench:
    ability: Ability
    caster: int
    magical: bool
    strips: int | None          # uses/strips left where the ability counts them; None = not counted
    persistent: bool = False
    choice: str | None = None    # chosen School for abilities that let the caster pick one
    trait: bool = False          # an Enchantment held as a class Trait: always on, never removed


@dataclass(slots=True)
class Restriction:
    """An Ongoing Effect limiting whom a player may attack or cast at (Awe, Terror, Insult)."""
    what: str                    # attack-caster / cast-at-caster / attack-anyone-but-caster / cast-at-anyone-but-caster
    src: int                     # pid of the player who imposed it
    until: float
    slug: str
    negate_on_provoke: bool = False   # Awe/Terror: ends if the caster attacks or casts at the target
    ends_on_src_death: bool = False
    allowed: set = field(default_factory=set)  # Insult: others who attacked or cast on the target


@dataclass(slots=True)
class Buff:
    """An Ongoing Effect from a Verbal that the engine queries like a worn one (Rage's Verbal
    immunity and weapon specials; Circle of Protection's protections while its Insubstantial lasts)."""
    slug: str
    effect: object               # the compiled Effect
    until: float
    rides_state: str | None = None   # ends when this State ends
    ends_on_incantation: bool = False


@dataclass(slots=True)
class Cast:
    uses: Uses | None           # None for a Charge
    target: int | None
    remaining: float
    kind: str = "cast"          # cast / charge
    charge_for: Uses | None = None
    persistent: bool = False    # the Persistent Meta-Magic was stated for this Enchantment
    declared: bool = False      # a declaration, not an incantation: not stopped by Suppressed


@dataclass(slots=True)
class Player:
    pid: int
    team: int
    cls: str
    level: int
    skill: float
    role: str                   # fighter / caster / support / archer
    armor_max: int = 0
    shield: str = "none"
    great_weapon: bool = False
    has_bow: bool = False
    uses: dict[str, Uses] = field(default_factory=dict)
    traits: list[Ability] = field(default_factory=list)       # traits and archetypes, always on
    trait_copies: dict[str, int] = field(default_factory=dict)  # Traits bought more than once (Experienced)
    ltp: tuple | None = None    # Look the Part bonus added at build: (slug, uses added, created the use)
    ench_slots: int = 1                                         # magical enchantments allowed
    doctrine: str = ""          # a Magic User's build plan (sim/data/doctrines.json id); "" for martial classes
    play: str = ""              # the doctrine's play style (sim/policies): striker, controller, enchanter, ...
    combos: tuple = ()          # the doctrine's (set-up, finisher) pairs
    bought: dict = field(default_factory=dict)   # a Magic User's purchases: slug -> copies

    # per-life state
    alive: bool = True
    out: bool = False                                           # no lives left
    lives_left: int | None = None                               # None = unlimited
    dead_until: float = 0.0
    at_base_until: float = 0.0
    kept_away_until: float = 0.0
    armor: dict[str, int] = field(default_factory=dict)
    magic_armor: dict[str, int] = field(default_factory=dict)
    wounds: set[str] = field(default_factory=set)
    states: dict[str, float] = field(default_factory=dict)     # state -> expiry time (INF = indefinite)
    state_src: dict[str, int] = field(default_factory=dict)    # state -> pid of the enemy who applied it
    control_seen: dict[int, float] = field(default_factory=dict)  # enemy pid -> last tick p was under their control
    enchantments: list[Ench] = field(default_factory=list)
    resist: list[dict] = field(default_factory=list)
    restrictions: list[Restriction] = field(default_factory=list)
    buffs: list[Buff] = field(default_factory=list)
    exit_lock_until: float = 0.0                                # may not voluntarily end a State before this
    meta_armed: set = field(default_factory=set)                # Meta-Magics stated for the next ability
    prevented: dict[str, float] = field(default_factory=dict)  # States p may not gain until then (Planar Grounding)
    once_used: set = field(default_factory=set)  # once-per-life abilities already activated this life (Song of Survival)
    barrage: dict[str, int] | None = None   # Elemental Barrage: carried Magic Balls usable by declaration
    casting: Cast | None = None
    target: int | None = None                                   # melee target pid
    weapon_ok: bool = True
    weapon_hot_until: float = 0.0                               # Heat Weapon: may not wield it until then
    shield_hits: int = 0
    balls_retrieve_at: dict[str, float] = field(default_factory=dict)
    next_shot_at: float = 0.0

    # stats
    kills: int = 0
    deaths: int = 0
    time_dead: float = 0.0
    enchant_assists: int = 0    # teammates' kills made while wearing this player's Enchantment
    control_assists: int = 0    # teammates' kills of an enemy under this player's control (Game._credit_assists)
    saves: int = 0              # teammates' deaths prevented, revives, wounds healed

    @property
    def backline(self) -> bool:
        return self.role in ("caster", "support", "archer") and self.play != "battle"

    def has_state(self, s: str, now: float) -> bool:
        return self.states.get(s, -1.0) > now

    def can_act(self, now: float) -> bool:
        return self.alive and not any(self.states.get(s, -1.0) > now for s in NO_ACTION_STATES)

    def on_field(self, now: float) -> bool:
        return self.alive and self.at_base_until <= now

    def shield_usable(self) -> bool:
        return self.shield != "none" and self.shield_hits < 3 and not ({"left_arm"} & self.wounds)

    def wearable_enchantments(self) -> int:
        return self.ench_slots

    def chants(self) -> list["Ench"]:
        """Worn Enchantments sustained by p's own Chant (the Bardic songs)."""
        return [e for e in self.enchantments if "chant" in e.ability.properties and not e.trait]

    def magical_enchantment_count(self) -> int:
        return sum(1 for e in self.enchantments if e.magical and "exempt-from-enchantment-limit" not in e.ability.properties)
