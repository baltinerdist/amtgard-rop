# Ability Metadata Platform

A complete, structured description of every ability, spell, trait, archetype, Meta-Magic and Equipment trait in the
Amtgard Rules of Play (V8.08), plus the four class immunity traits: 183 entries in all. It exists so questions about the rules have exact,
checkable answers, such as:

* *Every ability that causes death.*
* *Every ability that holds a player in place.*
* *Which Druid spells do the same thing as another spell, trait or ability?*
* *What stops Icy Blast?*

The rules markdown in `../rules/` stays verbatim and is the source of truth. This folder only adds to it.

## How complete is it

Every entry's rule text is split into numbered sentences, and **every one of the 575 sentences is tied to at least one fact**. The validator
refuses a record that leaves a sentence out. Each fact cites its sentence ids, and every profile ends with a table showing each sentence
and what it was captured as. Magic Items and Quest Abilities are out of scope.

## What is recorded for each entry

| Facet | Contents |
| --- | --- |
| Identity | type, School, range (per class), delivery, Magical (m) or Extraordinary (ex) per class |
| Availability | every class listing: level, cost, max, frequency parsed into uses / per life, refresh or unlimited / Charge xN / balls or arrows, Look The Part, pick-one groups |
| Casting | incantation text and repetitions, materials and strip colors |
| Effects | each outcome with a plain label ("Causes death", "Freezes", "Pushes away"), who it lands on, whether that is good or bad for them (drawbacks are bad for the user), numbers, duration, timing, conditions, choices |
| Requirements | what must be true to cast it (willing, dead, wounded, Frozen or Stopped target; no enemy within 10' or 20'; only after a kill) |
| Restrictions | limits on using or combining it (no other Protection Enchantments, one active per caster, may not be ended near an enemy) |
| How it ends early | exit at will, arrival, caster attacks or dies, another Forced Movement, last strip, Chant stops |
| Properties | Forced Movement, Engulfing, Chant, Kill or Wound Trigger, castable while moving, Persistent, exempt from the Enchantment limit, bypasses (armor, Enchantments, Immunities, Traits, Resistances, Cursed) |
| Names | every ability, State, Special Effect and rule mechanic named in the text, with how it is named (grants, as per, modifies, removes, excludes, requires ...) |
| Clarifications | sentences that explain an interaction rather than add an effect |
| Roles and use | offense, control, defense, healing, revival, mobility, anti-magic, equipment, resource, team; who it is used on |
| Derived | plain capabilities (causes death, holds in place, silences, makes Insubstantial, heals, revives, dispels, resists, defeats armor, castable while moving, has a drawback ...), States applied, removed, prevented or required, what can stop it, similar abilities |
| Through grants | everything an entry gives its user, followed through every level (Corruptor → Void Touched → Shadow Step and Steal Life Essence), including Enchantments that cast a spell from strips and Look The Part changes. An ability that works "as per" another counts that ability's effects as its own |
| Open questions | ambiguities and contradictions in the rule text, never silently resolved |

The capabilities come from a small **rules glossary**: [`glossary/`](glossary/README.md), which also lists every capability with the exact rule that derives it. It says what each State, Special Effect and core
mechanic does. For example, Frozen means the player cannot move, speak or act, and only abilities that work on States in general or on Frozen
affect them. "Holds a player in place" therefore means a Frozen, Stopped or Stunned State put on another player, applied the same way everywhere.

## Using it

```bash
python3 scripts/meta_query.py "causes death"                 # plain words: a label or facet value first, then synonyms, then whole words
python3 scripts/meta_query.py --cap holds-in-place            # a derived capability
python3 scripts/meta_query.py --cap heals --include-granted   # count what granted abilities can do (works with every filter)
python3 scripts/meta_query.py --facet "Property=kill-trigger|wound-trigger"   # "|" = any of these values, "*" = any value
python3 scripts/meta_query.py --facet Requirement=target-willing --facet Class=Druid
python3 scripts/meta_query.py --state frozen                  # applies, removes, prevents or requires Frozen
python3 scripts/meta_query.py --list Effect                   # every value of a facet, with counts
python3 scripts/meta_query.py --explain phoenix-tears         # the full profile
python3 scripts/meta_query.py --similar hold-person           # twins and near-twins
python3 scripts/meta_query.py --countered-by icy-blast        # what can stop it
python3 scripts/meta_query.py --dedupe Druid                  # the Druid duplicate report
```

| Path | What it is |
| --- | --- |
| [`profiles/<slug>.md`](profiles/) | Everything about one entry, ending with its rule text sentence by sentence |
| [`index/`](index/) | Every facet value with the entries that have it (capabilities, effects, States, requirements, classes ...) |
| [`SIMILARITY.md`](SIMILARITY.md) | Identical abilities, same effects with different numbers or limits, "same plus a drawback", "does less than" and "gives its user" pairs, each with plain-language and word-level differences |
| [`dedupe/<class>.md`](dedupe/) | Each class list checked against the whole rulebook |
| [`glossary/`](glossary/) | States, Special Effects and mechanics as used by the platform |
| [`abilities.json`](abilities.json) | The whole database (entries, derived facets, similar pairs, vocabulary, glossary) |
| [`STATS.md`](STATS.md) | Counts |
| [`ACCEPTANCE.md`](ACCEPTANCE.md) | The 40-question battery, its expected answers and the current result (`acceptance.json` holds the questions) |
| `../viewer/ability-explorer.html` | Interactive explorer (filters, profiles, similar pairs, side-by-side compare, rules) |

## How it was built

See [`PLAN.md`](PLAN.md). In short:

* **Code** builds everything that can be parsed mechanically: sentences, identity, availability, frequency, incantation and materials (`scripts/meta_source.py`).
* **Agents** wrote the facts that need reading, one JSON file per entry in [`source/records/`](source/records/), following [`AUTHORING.md`](AUTHORING.md) and the vocabulary in `scripts/meta_vocab.py`. The process ran in stages:
  1. A two-agent pilot on 18 hard entries set the conventions.
  2. 10 agents did the extraction.
  3. 10 different agents reviewed and corrected every record, sharded differently, changing 83 of 183 records.
  4. 12 topic auditors checked consistency across the whole corpus and found 129 issues, which 8 agents applied.
  5. A 40-question acceptance test compared the platform with answers built independently from the rule text by four more agents. Its
     findings fixed six records and the derivation (grants followed through every level, "as per", drawbacks from limits, armor, moving),
     the similarity rules and the query tool. It is now an automatic regression: `scripts/meta_acceptance.py`.
* **The validator** (`scripts/meta_check.py`) enforces the vocabulary, evidence, full sentence coverage and the settled conventions.
* **The build** (`scripts/meta_build.py`) derives everything else. The explorer is built by `scripts/build_meta_explorer.py`.

## Maintaining it

When the rulebook changes, rerun `scripts/gen_abilities.py --write`, then `scripts/meta_check.py`. Every sentence whose wording changed, and every sentence
added or removed, is reported as an error on its record (the check compares against `source/sentences.json`). Fix those records, run
`scripts/meta_check.py --snapshot`, then `scripts/meta_build.py`, `scripts/meta_acceptance.py` (fails if any tested answer changed) and
`scripts/build_meta_explorer.py`.
