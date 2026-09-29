"""Parse the frequency notation used in class tables, e.g. '1/Life Charge x3 (m) (Ambulant)'."""
from __future__ import annotations

import re
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class Frequency:
    raw: str
    uses: int | None       # uses per period; None = unlimited or not stated
    per: str | None        # 'life', 'refresh', 'unlimited' or None
    charge: int | None     # Charge xN repetitions, if chargeable
    unit: str | None       # 'balls' / 'arrows' for material-limited abilities
    magical: bool | None   # (m) -> True, (ex) -> False, not stated -> None
    swift: bool = False
    ambulant: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


_MATERIAL = re.compile(r"(\d+)\s*(Balls?|Arrows?)\s*/\s*(Unlimited|\d+/(?:Life|Refresh))", re.I)
_PER = re.compile(r"(\d+)\s*/\s*(Life|Refresh)", re.I)
_CHARGE = re.compile(r"Charge\s*x\s*(\d+)", re.I)


def parse(raw: str | None) -> Frequency:
    text = (raw or "").strip()
    magical = True if "(m)" in text else False if "(ex)" in text else None
    charge = int(m.group(1)) if (m := _CHARGE.search(text)) else None
    swift = "swift" in text.lower()
    ambulant = "ambulant" in text.lower()
    if m := _MATERIAL.search(text):
        unit = "balls" if m.group(2).lower().startswith("ball") else "arrows"
        return Frequency(text, int(m.group(1)), "unlimited", charge, unit, magical, swift, ambulant)
    if m := _PER.search(text):
        return Frequency(text, int(m.group(1)), m.group(2).lower(), charge, None, magical, swift, ambulant)
    if re.search(r"\bunlimited\b", text, re.I):
        return Frequency(text, None, "unlimited", charge, None, magical, swift, ambulant)
    return Frequency(text, None, None, charge, None, magical, swift, ambulant)
