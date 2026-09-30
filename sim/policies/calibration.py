"""The measured anchor weights for the usefulness score (`sim/policies/value.py`).

`sim/analyze/calibrate.py` measures what each anchor (a kill, a heal, a point of armor, a State,
...) is worth in play and writes `sim/data/value-calibration.json`. This module loads that file and
builds the weight tables value.py uses: a calibrated weight where the file has one, the hand-set
weight everywhere else. Every weight carries its source (`Tables.sources`):

- `calibrated`: measured
- `calibrated (floor)`: measured, used only above the hand weight (map flag `may-understate`)
- `hand (floor)`: measured below the hand weight, which is kept as a floor
- `hand (needs map)`: measured, but the engine gives the anchor no effect without a map
- `calibrated (at the minimum)`: measured at or below `MIN_WEIGHT`, which is used instead
- `hand`: not calibrated

**Staleness.** A calibration is only valid for the assumptions and the engine it was measured
under. The file records `fingerprint()`: the SHA-256 of `sim/data/assumptions.json` and
`sim.engine.ENGINE_VERSION`. If either differs, loading fails loudly (`StaleCalibration`). Rerun
`python -m sim.analyze.calibrate`, or set the environment variable `SIM_CALIBRATION`:

- `on` (default): use the file; stale raises; a missing file falls back to the hand weights (with a warning)
- `stale-ok`: use a stale file anyway, with a warning
- `off`: hand weights only (the calibration harness plays under these)

Assumption overrides at run time (`--assume`, `--set`) don't change the file on disk and don't
trigger the check.

    python -m sim.analyze.calibrate --weights  # every weight: hand, in use, source
"""
from __future__ import annotations

import hashlib
import json
import os
import warnings
from dataclasses import dataclass, field

from sim.paths import ASSUMPTIONS_JSON, DATA

CALIBRATION_JSON = DATA / "value-calibration.json"
MODES = ("on", "stale-ok", "off")
# The least a calibrated per-use weight can be: value.UNPRICED_WEIGHT, what an effect the valuation
# can't price is worth. A measured weight at or below zero (noise, or a model limit such as wounds
# costing little) would otherwise make every ability with that effect worthless, and policies never
# cast an ability worth nothing. Rates (a second of Charge saved) have no minimum.
MIN_WEIGHT = 0.5
NO_MINIMUM = frozenset({"scalar.charge_second"})


class StaleCalibration(RuntimeError):
    pass


def fingerprint(assumptions_path=ASSUMPTIONS_JSON) -> dict:
    from sim.engine import ENGINE_VERSION
    digest = hashlib.sha256(open(assumptions_path, "rb").read()).hexdigest()
    return {"assumptions_sha256": digest, "engine_version": ENGINE_VERSION}


def stale_reasons(doc: dict, current: dict | None = None) -> list[str]:
    current = current or fingerprint()
    got = doc.get("fingerprint") or {}
    out = []
    if got.get("assumptions_sha256") != current["assumptions_sha256"]:
        out.append("sim/data/assumptions.json has changed since the calibration was measured")
    if got.get("engine_version") != current["engine_version"]:
        out.append(f"measured under engine version {got.get('engine_version')}, "
                   f"the engine is now version {current['engine_version']}")
    return out


def mode() -> str:
    m = os.environ.get("SIM_CALIBRATION", "on").strip().lower() or "on"
    if m not in MODES:
        raise ValueError(f"SIM_CALIBRATION must be one of {', '.join(MODES)}, not {m!r}")
    return m


def load(path=CALIBRATION_JSON, how: str | None = None, current: dict | None = None) -> dict | None:
    """The calibration document, or None for the hand weights (mode off, or no file)."""
    how = how or mode()
    if how == "off":
        return None
    if not os.path.exists(path):
        warnings.warn(f"no value calibration at {path}: using the hand weights "
                      "(python -m sim.analyze.calibrate measures them)", stacklevel=2)
        return None
    doc = json.loads(open(path).read())
    why = stale_reasons(doc, current)
    if why:
        msg = (f"the value calibration {path} is stale: " + "; ".join(why) + ". Rerun "
               "`python -m sim.analyze.calibrate` (about 90 min), or set SIM_CALIBRATION=stale-ok "
               "to use it anyway or SIM_CALIBRATION=off for the hand weights.")
        if how != "stale-ok":
            raise StaleCalibration(msg)
        warnings.warn(msg, stacklevel=2)
    return doc


@dataclass
class Tables:
    weights: dict                  # table -> {key: weight in use}
    sources: dict                  # "table.key" -> source (module docstring)
    hand: dict                     # the hand tables, for reference
    measured: dict = field(default_factory=dict)   # "table.key" -> measured score (factors and floors)
    roles: dict = field(default_factory=dict)      # "table.key" -> recipient roles of the anchor
    doc: dict | None = None


def tables(hand: dict, doc: dict | None) -> Tables:
    """Weight tables: `hand` ({table: {key: weight}}) overridden by the calibration `doc`."""
    weights = {t: dict(v) for t, v in hand.items()}
    sources = {f"{t}.{k}": "hand" for t, v in hand.items() for k in v}
    out = Tables(weights, sources, {t: dict(v) for t, v in hand.items()}, doc=doc)
    if doc is None:
        return out
    anchors = doc.get("anchors", {})
    for name, a in anchors.items():
        target, w = a.get("calibrates"), a.get("weight")
        if not target or not w or w.get("value") is None:
            continue
        table, key = target.split(".", 1)
        measured = float(w["value"])
        out.measured[target] = measured
        out.roles[target] = (a.get("pooled") or {}).get("roles", {})
        if table == "factor":
            sources[target] = "calibrated"
            continue
        if table not in weights:
            continue
        h = hand.get(table, {}).get(key)
        flag = a.get("map", "fair")
        if flag == "needs-map" and h is not None:
            sources[target] = "hand (needs map)"
            continue
        if flag == "may-understate" and h is not None and measured < h:
            sources[target] = "hand (floor)"
            continue
        low = 0.0 if target in NO_MINIMUM else MIN_WEIGHT
        weights[table][key] = max(low, measured)
        sources[target] = "calibrated (floor)" if flag == "may-understate" else "calibrated"
        if measured < low:
            sources[target] = "calibrated (at the minimum)"
    return out


def describe(t: Tables) -> str:
    rows = [f"{'weight':34s} {'hand':>8s} {'in use':>8s}  source"]
    for table in t.weights:
        for key in sorted(t.weights[table]):
            h, w = t.hand[table].get(key), t.weights[table][key]
            fmt = lambda x: "   -    " if x is None else f"{x:8.2f}"     # noqa: E731
            rows.append(f"{table + '.' + key:34s} {fmt(h)} {fmt(w)}  {t.sources.get(f'{table}.{key}', 'hand')}")
    return "\n".join(rows)

