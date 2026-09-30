"""Caster doctrines: the build plans in sim/data/doctrines.json, loaded and checked against the
class lists.

    .venv/bin/python -m sim.rules.doctrines          # validate the file; prints each problem

A doctrine is how a Magic User builds a spell list: a stance (what the caster is for on the field),
a play style (how the simulator plays it, sim/policies), an ordered core list bought first, spells
it leans toward (`prefer`) or away from (`avoid`), and set-up-and-finish combos. Archetype
doctrines exist only at 6th level. How a player draws a doctrine and buys toward it is in
sim/policies/buy.py.

`validate` checks what the buyer relies on:
  - every class is a Magic User class in sim/data/classes.json, and doctrine ids are unique per class
  - stances and play styles are ones the file defines
  - base doctrines have a positive `share`; Archetype doctrines a positive `share_at_6`, and the
    shares at 6th level add up to at most 1 per class
  - every slug in core, prefer, avoid and combos is a purchasable spell on that class's list, and
    an Archetype is an Archetype on it
  - levels: every listed spell is available by 6th level, an Archetype doctrine's Archetype is a
    6th-level entry, and core copies do not exceed the entry's Max (or the copy cap)
  - an Archetype doctrine's core and prefer lists obey that Archetype's purchase restrictions
    (sim/engine/loadout.py `_archetype_purchase_rules`)
  - a combo's finisher can take the set-up's State: it requires that State (Stopped, Frozen,
    Insubstantial), or the State is Fragile and the finisher wounds or kills
Anything the file says beyond slugs, costs and Archetype rules is an assumption about real players.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

from sim.paths import DOCTRINES_JSON

if TYPE_CHECKING:
    from sim.rules.compile import Rules

# a finisher's requirement, by the State its set-up applies
FINISHER_REQUIREMENT = {"stopped": "target-stopped", "frozen": "target-frozen",
                        "insubstantial": "target-insubstantial"}


@dataclass(frozen=True)
class Doctrine:
    cls: str
    id: str
    name: str
    stance: str
    play: str
    core: tuple[tuple[str, int], ...]      # (slug, copies), bought first in this order
    prefer: frozenset
    avoid: frozenset
    combos: tuple[tuple[str, str], ...]    # (set-up, finisher)
    share: float = 0.0                     # base doctrines: share of the class's players
    archetype: str | None = None           # Archetype doctrines: bought first, 6th level only
    share_at_6: float = 0.0                # Archetype doctrines: share of the class's 6th-level players
    why: str = ""

    @property
    def key(self) -> str:
        return f"{self.cls}:{self.id}"


@dataclass(frozen=True)
class DoctrineBook:
    stances: dict
    play_styles: dict
    by_class: dict[str, tuple[Doctrine, ...]]

    def get(self, cls: str, doctrine_id: str) -> Doctrine | None:
        return next((d for d in self.by_class.get(cls, ()) if d.id == doctrine_id), None)

    def all(self) -> list[Doctrine]:
        return [d for docs in self.by_class.values() for d in docs]


def _doctrine(cls: str, raw: dict) -> Doctrine:
    return Doctrine(
        cls=cls, id=raw["id"], name=raw.get("name", raw["id"]), stance=raw.get("stance", ""),
        play=raw.get("play", ""),
        core=tuple((str(s), int(n)) for s, n in raw.get("core") or ()),
        prefer=frozenset(raw.get("prefer") or ()), avoid=frozenset(raw.get("avoid") or ()),
        combos=tuple((str(a), str(b)) for a, b in raw.get("combos") or ()),
        share=float(raw.get("share") or 0.0), archetype=raw.get("archetype"),
        share_at_6=float(raw.get("share_at_6") or 0.0), why=raw.get("why", ""))


def parse(data: dict) -> DoctrineBook:
    by_class = {cls: tuple(_doctrine(cls, d) for d in docs) for cls, docs in (data.get("classes") or {}).items()}
    return DoctrineBook(dict(data.get("stances") or {}), dict(data.get("play_styles") or {}), by_class)


def load(path=DOCTRINES_JSON) -> DoctrineBook:
    return parse(json.loads(open(path).read()))


def _state_applied(ab) -> set[str]:
    return {str(e.params.get("state")) for e in ab.effects
            if e.kind == "state.apply" and e.subject in ("target", "struck-player")}


def _wounds_or_kills(ab) -> bool:
    return bool(ab.effects_of("wound.inflict", "death.cause"))


def validate(book: DoctrineBook, rules: "Rules") -> list[str]:
    """Every problem found, as readable lines; an empty list means the file is usable."""
    from sim.engine.loadout import _archetype_purchase_rules   # engine imports rules: import late
    problems: list[str] = []
    cap = rules.a("loadout.magic_user_copy_cap")
    for cls, docs in book.by_class.items():
        sheet = rules.classes.get(cls)
        if sheet is None or not sheet.magic_user:
            problems.append(f"{cls}: not a Magic User class")
            continue
        entries = {c.slug: c for c in sheet.abilities if c.kind in ("spell", "archetype") and c.cost is not None}
        ids = [d.id for d in docs]
        if len(ids) != len(set(ids)):
            problems.append(f"{cls}: duplicate doctrine ids")
        if not any(d.archetype is None and d.share > 0 for d in docs):
            problems.append(f"{cls}: no base doctrine with a positive share")
        at6 = sum(d.share_at_6 for d in docs if d.archetype)
        if at6 > 1.0 + 1e-9:
            problems.append(f"{cls}: Archetype doctrine shares at 6th level add up to {at6:.2f} > 1")
        for d in docs:
            where = d.key
            if d.stance not in book.stances:
                problems.append(f"{where}: unknown stance {d.stance!r}")
            if d.play not in book.play_styles:
                problems.append(f"{where}: unknown play style {d.play!r}")
            if not d.core:
                problems.append(f"{where}: empty core list")
            cost, allowed = (lambda c: c.cost), (lambda c: True)
            if d.archetype is not None:
                a = entries.get(d.archetype)
                if a is None or a.kind != "archetype":
                    problems.append(f"{where}: {d.archetype} is not an Archetype on the {cls} list")
                    continue
                if min(a.levels) != 6:
                    problems.append(f"{where}: Archetype {d.archetype} is not a 6th-level entry")
                if d.share_at_6 <= 0:
                    problems.append(f"{where}: Archetype doctrine without a positive share_at_6")
                cost, allowed = _archetype_purchase_rules(rules.abilities[d.archetype], rules)
            elif d.share <= 0:
                problems.append(f"{where}: base doctrine without a positive share")

            def spell(slug: str, what: str):
                c = entries.get(slug)
                if c is None or c.kind != "spell" or slug not in rules.abilities:
                    problems.append(f"{where}: {what} {slug} is not a purchasable spell on the {cls} list")
                    return None
                if min(c.levels) > 6:
                    problems.append(f"{where}: {what} {slug} is not available by 6th level")
                return c

            for slug, n in d.core:
                c = spell(slug, "core")
                if c is None:
                    continue
                top = c.max if c.max is not None else cap
                if not 1 <= n <= top:
                    problems.append(f"{where}: core {slug} x{n}, but at most {top} may be bought")
                if not allowed(c):
                    problems.append(f"{where}: core {slug} is forbidden by {d.archetype}")
            for slug in sorted(d.prefer):
                c = spell(slug, "prefer")
                if c is not None and not allowed(c):
                    problems.append(f"{where}: preferred {slug} is forbidden by {d.archetype}")
            for slug in sorted(d.avoid):
                spell(slug, "avoid")
            core = {s for s, _ in d.core}
            for slug in sorted((core | d.prefer) & d.avoid):
                problems.append(f"{where}: {slug} is both wanted and avoided")
            for setup, finisher in d.combos:
                a, b = spell(setup, "combo set-up"), spell(finisher, "combo finisher")
                if a is None or b is None:
                    continue
                states = _state_applied(rules.abilities[setup])
                reqs = rules.abilities[finisher].requirements
                if not any(FINISHER_REQUIREMENT.get(s) in reqs or (s == "fragile" and _wounds_or_kills(rules.abilities[finisher]))
                           for s in states):
                    problems.append(f"{where}: combo {setup} -> {finisher}: the finisher cannot use "
                                    f"what the set-up applies ({', '.join(sorted(states)) or 'no State'})")
    return problems


def main(argv=None) -> int:
    from sim.rules.compile import default_rules
    rules = default_rules()
    problems = validate(rules.doctrines, rules)
    for line in problems:
        print(line)
    n = len(rules.doctrines.all())
    print(f"{n} doctrines, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
