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


@pytest.mark.parametrize("cls", ["Bard", "Druid", "Healer", "Wizard"])
def test_magic_user_budget(rules, cls):
    """Purchases never exceed 5 points per level (+1 for Look The Part)."""
    sheet = rules.classes[cls]
    costs = {ca.slug: ca.cost for ca in sheet.abilities if ca.cost}
    for level in range(1, 7):
        for seed in range(20):
            p = build_player(rules, 0, 0, cls, level, 0.0, random.Random(seed))
            spent = 0
            for slug, u in p.uses.items():
                ca = next(c for c in sheet.abilities if c.slug == slug and c.cost)
                per = ca.freq.uses or 1
                copies = (u.max // per) if u.max else 1
                spent += costs[slug] * copies
            spent += sum(costs.get(t.slug, 0) for t in p.traits)
            assert 0 < spent <= 5 * level + 1, (cls, level, seed, spent)
