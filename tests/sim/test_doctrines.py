"""Caster doctrines (sim/data/doctrines.json, sim/rules/doctrines.py)."""
import copy
import json

from sim.paths import DOCTRINES_JSON
from sim.rules import doctrines


def test_doctrine_file_validates(rules):
    book = rules.doctrines
    assert doctrines.validate(book, rules) == []
    assert set(book.by_class) == {"Wizard", "Healer", "Druid", "Bard"}
    for cls, docs in book.by_class.items():
        base = [d for d in docs if d.archetype is None]
        assert abs(sum(d.share for d in base) - 1.0) < 1e-6, cls
        assert sum(d.share_at_6 for d in docs if d.archetype) <= 1.0


def test_validation_catches_problems(rules):
    data = json.loads(DOCTRINES_JSON.read_text())
    bad = copy.deepcopy(data)
    wiz = bad["classes"]["Wizard"]
    wiz[0]["core"].append(["heal", 1])                     # not on the Wizard list
    wiz[0]["play"] = "juggler"                             # no such play style
    warlock = next(d for d in wiz if d.get("archetype") == "warlock")
    warlock["core"].append(["entangle", 1])                # a Magic Ball outside Death/Flame
    wiz[0]["combos"] = [["force-bolt", "shatter"]]          # Force Bolt doesn't Freeze
    problems = doctrines.validate(doctrines.parse(bad), rules)
    text = "\n".join(problems)
    assert "core heal is not a purchasable spell" in text
    assert "unknown play style 'juggler'" in text
    assert "core entangle is forbidden by warlock" in text
    assert "combo force-bolt -> shatter" in text
