"""Compiler, frequency parser and rulings loader."""
import json

from sim.rules import frequency
from sim.rules.compile import build_rules, load_records
from sim.rules.rulings import load, question_ids


def test_frequency_parse():
    f = frequency.parse("1/Life Charge x3 (m) (Ambulant)")
    assert (f.uses, f.per, f.charge, f.magical, f.ambulant) == (1, "life", 3, True, True)
    f = frequency.parse("3 Balls / Unlimited")
    assert (f.uses, f.per, f.unit) == (3, "unlimited", "balls")
    f = frequency.parse("(Self) 3/Refresh Charge x10 (ex) (Swift)")
    assert (f.uses, f.per, f.charge, f.magical, f.swift) == (3, "refresh", 10, False, True)
    assert frequency.parse("Unlimited (ex)").per == "unlimited"
    assert frequency.parse("").per is None


def test_all_records_compile(rules):
    assert len(rules.abilities) == len(load_records()) == 183


def test_cast_time_from_words(rules):
    heal = rules.abilities["heal"]          # 8 words x5
    assert heal.cast_seconds(2.5) == 16
    assert rules.abilities["scavenge"].cast_seconds(2.5) == 1


def test_strip_counts(rules):
    assert rules.abilities["troll-blood"].strips == 3
    assert rules.abilities["phoenix-tears"].strips == 2
    assert rules.abilities["heal"].strips is None


def test_87_open_questions():
    assert len(question_ids(load_records())) == 87


def test_rulings_missing_file_falls_back(tmp_path):
    rs = load(tmp_path / "none.json", load_records())
    assert not rs.source_ok and len(rs.fallback_ids) == 87


def test_rulings_partial_and_unknown(tmp_path):
    path = tmp_path / "r.json"
    path.write_text(json.dumps([
        {"id": "adaptive-blessing#1", "slug": "adaptive-blessing", "question": "q", "ruling": "caster", "status": "answered"},
        {"id": "no-such#9", "slug": "x", "question": "q", "ruling": "r", "status": "assumed"},
    ]))
    rs = load(path, load_records())
    assert rs.source_ok and "adaptive-blessing#1" in rs.by_id
    assert len(rs.fallback_ids) == 86 and rs.unknown_ids == ["no-such#9"]


def test_rulings_garbage_file_tolerated(tmp_path):
    path = tmp_path / "r.json"
    path.write_text("{not json")
    rs = load(path, load_records())
    assert not rs.source_ok and len(rs.fallback_ids) == 87


def test_sim_block_changes_ability(tmp_path):
    qid = next(iter(question_ids([r for r in load_records() if r["slug"] == "adaptive-blessing"])))
    path = tmp_path / "r.json"
    path.write_text(json.dumps([{"id": qid, "slug": "adaptive-blessing", "question": "", "ruling": "",
                                 "status": "answered", "sim": {"add_requirements": ["target-wounded"]}}]))
    r = build_rules(rulings_path=path)
    assert "target-wounded" in r.abilities["adaptive-blessing"].requirements
