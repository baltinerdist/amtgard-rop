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
class Cast:
    uses: Uses | None           # None for a Charge
    target: int | None
    remaining: float
    kind: str = "cast"          # cast / charge
    charge_for: Uses | None = None


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
    ench_slots: int = 1                                         # magical enchantments allowed

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
    enchantments: list[Ench] = field(default_factory=list)
    resist: list[dict] = field(default_factory=list)
    restrictions: list[Restriction] = field(default_factory=list)
    exit_lock_until: float = 0.0                                # may not voluntarily end a State before this
    casting: Cast | None = None
    target: int | None = None                                   # melee target pid
    weapon_ok: bool = True
    shield_hits: int = 0
    balls_retrieve_at: dict[str, float] = field(default_factory=dict)
    next_shot_at: float = 0.0

    # stats
    kills: int = 0
    deaths: int = 0
    time_dead: float = 0.0

    @property
    def backline(self) -> bool:
        return self.role in ("caster", "support", "archer")

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

    def magical_enchantment_count(self) -> int:
        return sum(1 for e in self.enchantments if e.magical and "exempt-from-enchantment-limit" not in e.ability.properties)
