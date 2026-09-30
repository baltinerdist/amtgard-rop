"""Class sheets agree with the class markdown and the metadata."""
import re

import pytest

from sim.engine.loadout import build_player
from sim.paths import CLASSES_DIR
from sim.rules.build_classes import CLASS_FILES, build

import random


def test_twelve_classes(rules):
    assert set(rules.classes) == set(CLASS_FILES)


def test_magic_users(rules):
    assert {c for c, s in rules.classes.items() if s.magic_user} == {"Bard", "Druid", "Healer", "Wizard"}


@pytest.mark.parametrize("cls,fname", sorted(CLASS_FILES.items()))
def test_equipment_matches_markdown(rules, cls, fname):
    text = (CLASSES_DIR / fname).read_text()
    armor = re.search(r"\*\*Armor:\*\*\s*(\S+)", text).group(1)
    expected = int(re.match(r"\d+", armor).group()) if armor[0].isdigit() else 0
    assert rules.classes[cls].armor == expected
    shield = re.search(r"\*\*Shields:\*\*\s*(\S+)", text).group(1).lower()
    assert rules.classes[cls].shield == shield


def test_class_json_is_current():
    """sim/data/classes.json matches a fresh build (re-run sim.rules.build_classes if not)."""
    import json
    from sim.paths import CLASSES_JSON
    assert json.loads(CLASSES_JSON.read_text()) == json.loads(json.dumps(build()))


def test_every_class_ability_exists(rules):
    for sheet in rules.classes.values():
        for ca in sheet.abilities:
            assert ca.slug in rules.abilities, (sheet.name, ca.slug)


def test_martial_classes_gain_something_each_level(rules):
    for sheet in rules.classes.values():
        if sheet.magic_user:
            continue
        levels = {lv for ca in sheet.abilities if ca.kind == "level" for lv in ca.levels}
        assert levels == {1, 2, 3, 4, 5, 6}, sheet.name


def test_traits_flagged(rules):
    pal = {ca.slug: ca for ca in rules.classes["Paladin"].abilities}
    assert pal["immune-to-death"].trait and pal["immune-to-command"].trait
    assert not pal["greater-heal"].trait


def _price(rules, sheet, p):
    """Point cost per slug for this player: list price, changed by their Archetype's economy.cost
    (Dervish, Priest, Ranger)."""
    from sim.engine.loadout import _archetype_purchase_rules
    arch = next((t for t in p.traits if t.delivery == "archetype"), None)
    cost = _archetype_purchase_rules(arch, rules)[0] if arch is not None else (lambda c: c.cost)
    return {ca.slug: cost(ca) for ca in sheet.abilities if ca.cost}


@pytest.mark.parametrize("cls", ["Bard", "Druid", "Healer", "Wizard"])
def test_magic_user_budget(rules, cls):
    """Purchases never exceed 5 points per level (+1 for Look The Part)."""
    sheet = rules.classes[cls]
    for level in range(1, 7):
        for seed in range(20):
            p = build_player(rules, 0, 0, cls, level, 0.0, random.Random(seed))
            costs = _price(rules, sheet, p)
            spent = 0
            for slug, u in p.uses.items():
                if not u.purchased:
                    continue      # granted by an Archetype, not bought
                # copies bought, as recorded: Archetypes such as Dervish or Warlock double the uses,
                # so the uses can't be divided back into purchases
                spent += costs[slug] * u.copies
            spent += sum(costs.get(t.slug, 0) for t in p.traits)
            assert 0 < spent <= 5 * level + 1, (cls, level, seed, spent)
