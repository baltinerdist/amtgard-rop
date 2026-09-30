"""Face-validity checks (sim/analyze/validity.py) as tests.

Statistical and seeded: each check plays a fixed set of games and compares the result with a
tolerance that scales with the number of games. Runs at half the script's game counts by
default (about 2.5 minutes on 10 cores); set SIM_VALIDITY_SCALE=1 for the full counts.

A check with a `known_limit` is a documented structural gap of the Phase 1 model (for example,
no map), so its failure is reported as an expected failure rather than hidden or tuned away.
"""
import os

import pytest

from sim.analyze import validity

SCALE = float(os.environ.get("SIM_VALIDITY_SCALE", "0.5"))


@pytest.mark.parametrize("check", validity.CHECKS, ids=lambda c: c.name)
def test_validity(check):
    (res,) = validity.run_checks({check.name}, SCALE)
    msg = f"{res.name}: {res.measured} (expected {res.expected}). {res.rationale}"
    if not res.passed and check.known_limit:
        pytest.xfail(f"{msg} Known limit: {check.known_limit}")
    assert res.passed, msg


def test_checks_have_rationales():
    names = [c.name for c in validity.CHECKS]
    assert len(names) == len(set(names))
    for c in validity.CHECKS:
        assert c.rationale.strip() and c.games > 0


def test_checks_are_deterministic():
    """The same check at the same scale replays exactly (fixed seeds, serial vs parallel)."""
    a = validity.run_checks({"skill"}, 0.1, workers=1)[0]
    b = validity.run_checks({"skill"}, 0.1, workers=2)[0]
    assert (a.passed, a.measured) == (b.passed, b.measured)
