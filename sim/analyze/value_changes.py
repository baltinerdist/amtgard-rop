"""How the usefulness score (sim/policies/value.py) changed against an earlier revision: one row per
ability, for the role of its typical holder, with the effect that moved most.

    python -m sim.analyze.value_changes                 # against f736d6a (before compositional values)
    python -m sim.analyze.value_changes --base HEAD~3

Writes sim/out/value-changes.csv (slug, role, old_value, new_value, delta, reason) and prints the
abilities whose sign changed and the biggest moves.
"""
from __future__ import annotations

import argparse
import csv
import dataclasses
import subprocess
import types
from collections import Counter

from sim.engine.effects import is_handled
from sim.engine.loadout import ROLE_BY_CLASS
from sim.paths import OUT, REPO
from sim.policies import value as new
from sim.rules.compile import Ability, Rules, default_rules

BASE = "f736d6a"
ROLE_ORDER = ("caster", "support", "fighter", "archer")


def load_base(rev: str) -> types.ModuleType:
    src = subprocess.run(["git", "show", f"{rev}:sim/policies/value.py"], cwd=REPO, check=True,
                         capture_output=True, text=True).stdout
    mod = types.ModuleType("value_base")
    exec(compile(src, f"{rev}:sim/policies/value.py", "exec"), mod.__dict__)
    return mod


def holder_role(rules: Rules, slug: str) -> str:
    """The role of the classes that list the ability most often (ties: caster, support, fighter, archer)."""
    roles = Counter(ROLE_BY_CLASS[n] for n, c in rules.classes.items() if any(a.slug == slug for a in c.abilities))
    if not roles:
        return "caster"
    return max(ROLE_ORDER, key=lambda r: (roles.get(r, 0), -ROLE_ORDER.index(r)))


def old_parts(old, ab: Ability, role: str) -> dict[str, float]:
    """Signed per-effect contributions under the base module (equipment permits: the best one)."""
    parts: dict[str, float] = {}
    best_eq = None
    for eff in ab.effects:
        if not is_handled(ab, eff):
            continue
        if old.is_drawback(ab, eff):
            parts[eff.id] = -old.drawback_cost(dataclasses.replace(ab, effects=(eff,)), role)
        elif eff.kind == "equipment.permit":
            w = old.EQUIPMENT_WEIGHT.get(eff.params.get("what", ""), 0.0)
            if best_eq is None or w > parts.get(best_eq, -1):
                best_eq = eff.id
                parts[eff.id] = w
        else:
            parts[eff.id] = old.effect_benefit(ab, eff, role)
    return parts


def reason(old, ab: Ability, role: str, rules: Rules, v_old: float, v_new: float) -> str:
    if abs(v_new - v_old) < 1e-9:
        return "unchanged"
    before = old_parts(old, ab, role)
    after: dict[str, tuple[str, float]] = {}
    for i, label, c in new.breakdown(ab, role, rules=rules):
        after[i] = (label, after.get(i, ("", 0.0))[1] + c)
    kinds = {e.id: e.kind for e in ab.effects}
    ids = sorted(set(before) | set(after), key=lambda i: -abs(after.get(i, ("", 0.0))[1] - before.get(i, 0.0)))
    if not ids:
        return "no handled effects"
    i = ids[0]
    label, c_new = after.get(i, ("", 0.0))
    text = f"{kinds.get(i, i)} ({label}): {before.get(i, 0.0):+.2f} -> {c_new:+.2f}"
    b_new = sum(c for _, c in after.values() if c > 0)
    if v_new == 0.0 and b_new <= 0:
        text += "; no benefit left, clamped to 0"
    return text


def main(argv=None) -> list[dict]:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--base", default=BASE, help="git revision of the old value.py")
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args(argv)
    rules = default_rules()
    old = load_base(args.base)
    rows = []
    for slug in sorted(rules.abilities):
        ab = rules.abilities[slug]
        role = holder_role(rules, slug)
        v_old, v_new = old.value(ab, role), new.value(ab, role, rules=rules)
        rows.append({"slug": slug, "role": role, "old_value": round(v_old, 3), "new_value": round(v_new, 3),
                     "delta": round(v_new - v_old, 3), "reason": reason(old, ab, role, rules, v_old, v_new)})
    out = OUT / "value-changes.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    def sign(x: float) -> int:
        return (x > 1e-9) - (x < -1e-9)

    flips = [r for r in rows if sign(r["old_value"]) != sign(r["new_value"])]
    print(f"{len(rows)} abilities, {sum(r['delta'] != 0 for r in rows)} changed; wrote {out}")
    print(f"\nSign changed ({len(flips)}):")
    for r in flips:
        print(f"  {r['slug']:24} {r['role']:8} {r['old_value']:7.2f} -> {r['new_value']:7.2f}  {r['reason']}")
    print(f"\nBiggest moves (top {args.top}):")
    for r in sorted(rows, key=lambda r: -abs(r["delta"]))[:args.top]:
        print(f"  {r['slug']:24} {r['role']:8} {r['old_value']:7.2f} -> {r['new_value']:7.2f}  {r['reason']}")
    return rows


if __name__ == "__main__":
    main()
