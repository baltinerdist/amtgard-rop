"""Compile metadata/abilities.json, sim/data/classes.json and sim/data/rulings.json into
immutable rule objects the engine executes."""
from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from functools import lru_cache

from sim.paths import ABILITIES_JSON, ASSUMPTIONS_JSON, CLASSES_JSON, RULINGS_JSON
from sim.rules import frequency as freqmod
from sim.rules import rulings as rulingsmod


@dataclass(frozen=True)
class Effect:
    id: str
    kind: str
    subject: str
    polarity: str
    params: dict
    duration_type: str
    seconds: float | None
    timing: str
    conditions: tuple


@dataclass(frozen=True)
class Ability:
    slug: str
    name: str
    delivery: str               # verbal, enchantment, magic-ball, specialty-arrow, trait, archetype, meta-magic
    school: str
    range: str
    words: int
    repetitions: int
    special: str                # e.g. 'immediately after dying'
    effects: tuple[Effect, ...]
    requirements: frozenset
    restrictions: frozenset
    termination: frozenset
    properties: frozenset
    beneficiary: str            # self / ally / enemy / any / team
    roles: frozenset
    rulings: tuple[str, ...]    # ids of open questions attached to this ability
    strips: int | None = None   # enchantment strips (uses) for abilities with the uses-strips property

    def has(self, prop: str) -> bool:
        return prop in self.properties

    def effects_of(self, *kinds: str) -> list[Effect]:
        return [e for e in self.effects if e.kind in kinds]

    def cast_seconds(self, words_per_second: float) -> float:
        if self.delivery in ("trait", "archetype"):
            return 0.0
        return max(1.0, round(self.words * max(1, self.repetitions) / words_per_second))


@dataclass(frozen=True)
class ClassAbility:
    slug: str
    kind: str                   # level / spell / archetype / granted
    levels: tuple[int, ...]
    freq: freqmod.Frequency
    cost: int | None
    max: int | None
    range: str
    option: str
    trait: bool = False         # listed with (T) in the class table: always on


@dataclass(frozen=True)
class ClassSheet:
    name: str
    magic_user: bool
    armor: int
    shield: str
    weapons: tuple[str, ...]
    look_the_part: dict
    abilities: tuple[ClassAbility, ...]

    @property
    def all_melee(self) -> bool:
        return "All Melee" in self.weapons

    @property
    def has_bow(self) -> bool:
        return "Bow" in self.weapons


@dataclass
class Rules:
    abilities: dict[str, Ability]
    by_name: dict[str, str]
    classes: dict[str, ClassSheet]
    rulings: rulingsmod.RulingSet
    assumptions: dict
    records: list[dict] = field(repr=False)
    # caster doctrines (sim/data/doctrines.json), loaded on first use; not an init field, so a
    # dataclasses.replace() variant (other assumptions or class lists) loads its own copy
    _doctrines: object = field(default=None, init=False, repr=False, compare=False)

    @property
    def doctrines(self):
        """The caster build plans, sim.rules.doctrines.DoctrineBook (validate() checks them)."""
        if self._doctrines is None:
            from sim.rules import doctrines
            self._doctrines = doctrines.load()
        return self._doctrines

    def a(self, key: str):
        """Assumption value by dotted key, e.g. rules.a('melee.base_hit_per_second')."""
        group, name = key.split(".", 1)
        return self.assumptions[group][name]["value"]


def _effect(e: dict) -> Effect:
    d = e.get("duration") or {}
    return Effect(e["id"], e["kind"], e["subject"], e.get("polarity", ""), dict(e.get("params") or {}),
                  d.get("type", "instant"), d.get("seconds"), e.get("timing", "on-cast"),
                  tuple(e.get("conditions") or ()))


def _apply_sim_ruling(rec: dict, sim: dict) -> dict:
    rec = copy.deepcopy(rec)
    drop = set(sim.get("drop_effects") or ())
    rec["effects"] = [e for e in rec["effects"] if e["id"] not in drop]
    for eid, params in (sim.get("set_params") or {}).items():
        for e in rec["effects"]:
            if e["id"] == eid:
                if "seconds" in params:
                    e.setdefault("duration", {})["seconds"] = params["seconds"]
                e["params"] = {**e.get("params", {}), **{k: v for k, v in params.items() if k != "seconds"}}
    reqs = [r for r in rec["requirements"] if r["kind"] not in set(sim.get("remove_requirements") or ())]
    reqs += [{"kind": k} for k in sim.get("add_requirements") or ()]
    rec["requirements"] = reqs
    return rec


_NUMBER_WORDS = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
                 "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def _strip_count(rec: dict) -> int | None:
    if not any(p["kind"] == "uses-strips" for p in rec.get("properties") or ()):
        return None
    raw = ((rec.get("materials") or {}).get("raw") or "").lower()
    m = re.match(r"\s*(\d+|[a-z]+)\b", raw)
    if m and m.group(1).isdigit():
        return int(m.group(1))
    return _NUMBER_WORDS.get(m.group(1), 1) if m else 1


def compile_ability(rec: dict, ruling_ids: tuple[str, ...] = ()) -> Ability:
    inc = rec.get("incantation") or {}
    return Ability(
        slug=rec["slug"], name=rec["title"], delivery=rec.get("delivery") or "",
        school=rec.get("school") or "", range=rec.get("range") or "",
        words=int(inc.get("words") or 0), repetitions=int(inc.get("repetitions") or 1),
        special=inc.get("special") or "none",
        effects=tuple(_effect(e) for e in rec.get("effects") or ()),
        requirements=frozenset(r["kind"] for r in rec.get("requirements") or ()),
        restrictions=frozenset(r["kind"] for r in rec.get("restrictions") or ()),
        termination=frozenset(r["kind"] for r in rec.get("termination") or ()),
        properties=frozenset(p["kind"] for p in rec.get("properties") or ()),
        beneficiary=rec.get("beneficiary") or "",
        roles=frozenset(rec.get("roles") or ()),
        rulings=ruling_ids,
        strips=_strip_count(rec),
    )


def _class_sheet(c: dict) -> ClassSheet:
    abilities = tuple(
        ClassAbility(a["slug"], a["kind"], tuple(a["levels"]), freqmod.Frequency(**a["frequency"]),
                     a["cost"], a["max"], a["range"], a["option"], a.get("trait", False))
        for a in c["abilities"])
    return ClassSheet(c["name"], c["magic_user"]["value"], c["armor"]["value"], c["shield"]["value"],
                      tuple(c["weapons"]["value"]), c["look_the_part"], abilities)


def load_records() -> list[dict]:
    data = json.loads(ABILITIES_JSON.read_text())
    recs = data["abilities"]
    return list(recs.values()) if isinstance(recs, dict) else recs


def build_rules(assumptions: dict | None = None, rulings_path=RULINGS_JSON) -> Rules:
    records = load_records()
    ruling_set = rulingsmod.load(rulings_path, records)
    abilities = {}
    for rec in records:
        ids = tuple(i for i in rulingsmod.question_ids([rec]))
        for r in ruling_set.for_slug(rec["slug"]):
            if r.sim:
                rec = _apply_sim_ruling(rec, r.sim)
        abilities[rec["slug"]] = compile_ability(rec, ids)
    classes = {k: _class_sheet(v) for k, v in json.loads(CLASSES_JSON.read_text())["classes"].items()}
    if assumptions is None:
        assumptions = json.loads(ASSUMPTIONS_JSON.read_text())
    by_name = {a.name.lower(): a.slug for a in abilities.values()}
    return Rules(abilities, by_name, classes, ruling_set, assumptions, records)


@lru_cache(maxsize=1)
def default_rules() -> Rules:
    return build_rules()
