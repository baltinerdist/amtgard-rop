"""Load answers to the metadata's open questions from sim/data/rulings.json.

Schema (a JSON list): {"id": "<slug>#<n>", "slug", "question", "ruling", "status"}.
n is the 1-based index into that ability's `open_questions` in metadata/abilities.json.

Rulings are prose, so by default the engine keeps the reading the metadata already encodes and
only records which rulings are assumed. A ruling may carry an optional machine-actionable
`sim` block that the compiler applies to the ability:

    "sim": {"drop_effects": ["e2"], "set_params": {"e1": {"seconds": 30}},
            "add_requirements": ["target-wounded"], "remove_requirements": ["target-stopped"]}

A missing, unreadable or partial file is tolerated: every open question without an entry falls
back to the metadata's encoded reading, and that fallback is reported.
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass
class Ruling:
    id: str
    slug: str
    question: str
    ruling: str
    status: str
    sim: dict = field(default_factory=dict)


@dataclass
class RulingSet:
    by_id: dict[str, Ruling]
    fallback_ids: list[str]          # open questions with no entry in the file
    unknown_ids: list[str]           # entries whose id matches no open question
    source_ok: bool                  # False if the file was missing or unreadable

    def for_slug(self, slug: str) -> list[Ruling]:
        return [r for r in self.by_id.values() if r.slug == slug]


def question_ids(records: list[dict]) -> dict[str, tuple[str, str]]:
    """Every open question in the metadata as id -> (slug, question)."""
    out = {}
    for r in records:
        for n, q in enumerate(r.get("open_questions") or [], start=1):
            out[f"{r['slug']}#{n}"] = (r["slug"], q)
    return out


def load(path: Path, records: list[dict]) -> RulingSet:
    expected = question_ids(records)
    entries: list = []
    ok = True
    try:
        entries = json.loads(path.read_text())
        if isinstance(entries, dict):
            entries = entries.get("rulings", [])
    except FileNotFoundError:
        ok = False
        log.info("rulings file %s not found; using the metadata's encoded reading for all %d open questions",
                 path, len(expected))
    except (json.JSONDecodeError, OSError) as exc:
        ok = False
        log.warning("rulings file %s unreadable (%s); using the metadata's encoded reading", path, exc)
    by_id: dict[str, Ruling] = {}
    unknown = []
    for e in entries if isinstance(entries, list) else []:
        if not isinstance(e, dict) or "id" not in e:
            continue
        rid = e["id"]
        if rid not in expected:
            unknown.append(rid)
            continue
        slug, question = expected[rid]
        by_id[rid] = Ruling(rid, e.get("slug", slug), e.get("question", question),
                            e.get("ruling", ""), e.get("status", "assumed"), e.get("sim") or {})
    fallback = sorted(set(expected) - set(by_id))
    if ok and fallback:
        log.info("%d open questions have no ruling; falling back to the metadata's encoded reading", len(fallback))
    if unknown:
        log.warning("%d rulings match no open question: %s", len(unknown), ", ".join(unknown[:5]))
    return RulingSet(by_id, fallback, unknown, ok)
