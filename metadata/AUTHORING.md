# Writing an ability record

One JSON file per entry: `metadata/source/records/<slug>.json`. Vocabulary: `scripts/meta_vocab.py` (read it; every id there has a
definition). Rules semantics: `metadata/glossary/glossary.json`. Validate with:

```bash
python3 scripts/meta_check.py metadata/source/records/<slug>.json        # or a directory, or several files
```

The identity, class availability, frequency, incantation, materials and the numbered sentences are **not** written by you: they are
built from the markdown (`scripts/meta_source.py`) and shown in your input packet. You cite sentence ids (`E1`, `L2`, `N1`).

## The one hard rule: account for every sentence

Every sentence id of the entry must be cited by at least one item (effect, requirement, restriction, termination, property, reference
or clarification). A sentence that restates a general rule or explains an interaction still gets a `clarification`. The validator
fails otherwise. Do not skip anything because it seems minor: the reader wants all of it.

## Shape

```json
{
  "slug": "lightning-bolt",
  "summary": "Magic Ball: wounds the hit location and Stops the player struck for 60 seconds; Weapon Destroying and Armor Breaking.",
  "effects": [
    {"id": "e1", "kind": "special-effect.grant", "subject": "struck-player", "polarity": "harm",
     "params": {"effect": "weapon-destroying", "on": "this-magic-ball"}, "duration": {"type": "instant"}, "timing": "on-struck", "evidence": ["E1"]},
    {"id": "e3", "kind": "wound.inflict", "subject": "struck-player", "polarity": "harm", "params": {"location": "struck"},
     "duration": {"type": "instant"}, "timing": "on-struck", "evidence": ["E2"]},
    {"id": "e4", "kind": "state.apply", "subject": "struck-player", "polarity": "harm", "params": {"state": "stopped"},
     "duration": {"type": "timed", "seconds": 60}, "timing": "on-struck", "evidence": ["E3"]}
  ],
  "requirements": [],
  "restrictions": [],
  "termination": [],
  "properties": [{"kind": "engulfing", "evidence": ["E4"]}],
  "references": [{"target": "state", "name": "stopped", "relation": "mentions", "evidence": ["E3"]},
                 {"target": "special-effect", "name": "weapon-destroying", "relation": "mentions", "evidence": ["E1"]}],
  "clarifications": [],
  "roles": ["offense", "control", "equipment"],
  "beneficiary": "enemy",
  "open_questions": []
}
```

Item shapes (all take an optional `"note"` with plain text):

* **effect**: `id` (e1, e2, ...), `kind`, `subject`, `polarity`, `params` (only the params listed for the kind), `duration`
  (`{"type": ..., "seconds": n}`; seconds only for `timed`), `timing` (a TIMING id; for `after-delay` also give `"delay_seconds": n`
  on the effect), `conditions` (list of CONDITIONS ids),
  `choice` (`{"group": "g1", "option": "1"}` when the subject picks one of several outcomes), `evidence` (sentence ids).
* **requirement / restriction / termination / property**: `{"kind": ..., "evidence": [...]}`, optional `"n"` (a number such as a
  maximum count), optional `"note"`.
* **reference**: `{"target": "ability" | "state" | "special-effect" | "mechanic", "name": ..., "relation": ..., "evidence": [...]}`.
  `name` is the exact ability title, a state id, a special-effect id, or a mechanic id from the vocabulary.
* **clarification**: `{"text": "<short plain restatement>", "evidence": [...]}`.
* `roles`: one or more ROLES ids. `beneficiary`: one BENEFICIARY id. `open_questions`: plain strings for anything ambiguous.

## Conventions

1. **Literal.** Record what the text says, nothing more. Do not import knowledge from other abilities or play experience. If a sentence
   is ambiguous, encode the plainer reading and add an `open_questions` entry.
2. **One effect per distinct outcome.** "Player hit dies and is Cursed" is two effects. A sentence can support several items.
3. **Subject is who or what the effect lands on.** Enchantment and Trait effects land on the `bearer`. A Verbal on another player:
   `target`. Magic Ball or arrow: `struck-player`. A dead target: `dead-target`. Equipment as the target: `target-equipment`.
   What an Enchantment gives its *caster* when worn by someone else: `caster-of-enchantment`.
4. **Polarity is from the subject's point of view.** A drawback on the bearer of a helpful ability (Heart of the Swarm makes the bearer
   Stopped; Contagion makes the bearer Fragile; Raise Dead Curses the revived player) is `harm`. That is how drawbacks become searchable.
5. **Durations.** "for 30 seconds" is `timed` 30. Enchantment effects that simply hold are `while-worn`. Traits and Archetypes are
   `permanent`. Instant results (dies, is healed, is destroyed) are `instant`. "The next wound/source" is `until-used`.
6. **Timing.** Default `on-cast`. Enchantment effects that hold continuously are `while-active`. Use `on-death`, `on-kill`, `on-wound`,
   `on-struck`, `on-strip`, `on-expiry`, `on-removal`, `on-arrival`, `after-delay`, `on-choice` as the text says.
7. **Conditions vs requirements.** A *requirement* must be met to cast the ability at all (target must be willing / dead / wounded;
   no enemy within 20'). A *condition* gates one effect of an ability that otherwise works. When the whole ability only works on,
   for example, a Frozen target ("Target Frozen player dies"), use the requirement `target-frozen`.
8. **Granted abilities are not expanded.** "Bearer gains Heal (Self) Unlimited (m)" is one `ability.grant` with `ability: "Heal"` and
   `frequency: "(Self) Unlimited (m)"`. "Affected as per X" is `ability.grant` with `how: "as-per"`. Strip casting is
   `ability.cast-via-strips` plus the property `uses-strips` and the termination `last-strip`.
9. **States.** `state.apply` with `params.state`. Removal: `state.remove` with `what` and, if one State, `state`. Prevention:
   `state.prevent` with `states`. A State that is only a requirement (Shatter's Frozen target) is a requirement, not an effect.
10. **Movement.** Insubstantial travel is two effects: `state.apply insubstantial` + `move.to-base` / `move.to-location` / `move.free`.
    Banish (target already Insubstantial) is only `move.to-base` with requirement `target-insubstantial`. Stay-away effects are
    `move.keep-away` with `feet` and `from`.
11. **Restrictions on the subject's own actions** (Awe, Terror, Insult; drawbacks like "Bearer may not wield weapons or Shields") are
    `action.restrict` effects with the right subject and polarity.
12. **Properties** hold for the whole ability: Forced Movement, Engulfing, Chant, Kill/Wound Trigger, castable while moving, works while
    Suppressed, no verbal targeting, Persistent, active while dead, exempt from the Enchantment limit, uses strips, count aloud, bypasses
    (armor, Magic Armor, Enchantments, Immunities, Traits, States, Resistances, Cursed), caster always benefits, has a choice.
13. **References.** Every ability, State, Special Effect or mechanic *named* in the text gets a reference with the right relation.
    States and Special Effects that the record already encodes as effects still get a `mentions` reference: it keeps the index complete.
14. **Archetypes** (class options) use: `ability.grant`, `ability.remove`, `ability.modify` (with `change`), `economy.frequency`,
    `economy.cost`, `economy.purchase-restrict`, `equipment.permit`, `action.restrict` (e.g. may not wield shields, may not wear armor),
    `armor.limit`, `casting.modify`, `ability.range-change`. Subject `bearer`, duration `permanent`, timing `while-active`.
15. **Equipment traits** (Equipment: Weapon, Short ...) use `equipment.permit` or `armor.limit`.
16. **Meta-Magic** uses `meta.modify-next` (Ambulant, Extension, Swift, Persistent) or `ability.charge` (Innate). Their limits are
    requirements (`only-verbals-20ft`, `only-touch-other-self-or-balls`, `not-on-charge-incantation`).
17. **Summary**: one plain sentence, at most 25 words, with the numbers, in the reader's words ("Kills a target within 20'").
18. **Roles and beneficiary**: pick all roles that apply; beneficiary is who the ability is for.
19. Use `other` only when nothing fits; explain in `note` and add an open question.

## Conventions settled by the pilot

20. **Beneficiary** is who the ability is *used for*: `self` if it only ever helps the user; `ally` if it can be put on another friendly
    player (even if some classes cast it on Self only); `enemy` if it is used against an enemy, even when the point is to protect the
    user (Awe, Terror); `any` if it is used on friend or foe (Release, Dispel Magic); `team` if it helps several allies at once.
21. **Polarity of choices.** An outcome the subject chooses for themselves is `benefit` (Gift of Air's return to base). Use `neutral`
    only when it is genuinely neither (acting as a respawn point).
22. **Triggered results.** The duration of a triggered effect is the duration of its *result*: an ignored hit is `instant`, the Frozen
    that follows is `timed`. Do not use `while-worn` for something that happens at a moment.
23. **Prevented death.** `death.prevent` with `instead`; if it can only happen once use duration `until-used` and termination
    `activates-once`; if it repeats while strips last use `while-worn` plus `enchantment.spend-strip` and `last-strip`. If the text
    says the killing event has no effect, add `defense.negate-hit` with `from: "lethal-event"`.
24. **Exceptions** to an ignored hit ("Siege, Armor Breaking ... affect the bearer as normal") go in `defense.negate-hit`
    `except_effects` (Special Effect ids), plus `mentions` references for each Special Effect.
25. **Replacement.** "Replace X with Y" is one `ability.replace` (`ability` X, `with` Y). "Lose all instances of X" is `ability.remove`.
    "X becomes ..." is `ability.modify`. A Meta-Magic tag on a granted ability ("(Swift)") goes in `ability.grant` `meta`.
26. **Strips.** Each activation removing a strip: `enchantment.spend-strip`. Enchantment removed when the last strip goes: termination
    `last-strip`. Both with the property `uses-strips`.
27. **"Persistent" the rule vs Persistent the Meta-Magic.** When text says an Enchantment "is Persistent" or talks about persistent
    Enchantments, reference the **mechanic** `persistent`, not the ability. Only reference the ability Persistent when the Meta-Magic is meant.
28. **Drawbacks on the caster** ("the caster may not use Alternate Bases") are both a restriction (for filtering) and an
    `action.restrict` effect with polarity `harm` (so it shows as a drawback).
29. **Roles**: `healing` only for wound healing; `revival` only for returning to life; `mobility` only when the user or an ally moves by
    choice; `resource` only for charges, uses, slots or points; `equipment` when weapons, shields or armor are affected; `anti-magic`
    when it removes or blocks abilities or Enchantments; `class-modifier` for archetypes and Equipment traits; `team` when several allies benefit.
30. **Contradictions in the text** (for example E says "may not exit early" and N says "may end at any time"): encode both as written
    with notes and add an open question. Never resolve a contradiction silently.
31. **Up to N targets**: put `"max_targets": N` on the effect.

## Added after the extraction round

32. New ids (use them instead of `other` or notes): `life.set-death-location`, `class.look-the-part`, `weapon.ignore-protections`;
    `action.restrict` values for single weapon types and Large shields (`wield-great-weapons`, `wield-javelins`, `wield-heavy-thrown`,
    `wield-long-weapons`, `wield-bows`, `wield-large-shields`), `use-other-sources-of-ability`, `wear-others-magical-enchantments`, `exit-early`;
    `equipment.permit` `per_instance: "yes"`; `defense.negate-hit` `from: "blocked-projectiles"`; `move.keep-away` `from: "combat"`;
    conditions `killed-with-thrown-weapon`, `caster-alive`; requirements `caster-alive`, `only-enchantments`, `only-enchantments-balls-verbals`;
    restrictions `not-against-own-effects`, `no-exit-near-enemy` (n), `no-exit-early`, `magical-enchantments-only-from-caster`;
    property `personal-protections-do-not-cover-equipment`.
33. Requirements, restrictions and termination items may carry `"conditions": [...]` (for example `exit-at-will` only when `cast-on-self`).
34. "X becomes ..." about uses or frequency of a named ability is `ability.modify` (it changes that ability); "each purchase gives double the
    uses" of a group is `economy.frequency`. When an archetype changes one named ability's frequency, record `ability.modify` **and**
    `economy.frequency` with that scope, so both kinds of search find it.
35. A weapon-type or shield restriction is `action.restrict` with the specific value, never plain `wield-weapons` unless all weapons are meant.

## Settled by the topic audits (these override any finding that conflicts)

36. **Cursed with no stated duration** is `until-respawn` (the Cursed definition: "persists after death but is removed on respawn").
    Cursed imparted by an Enchantment is `while-worn` (with the clarification that it is not removed with the Enchantment when the text
    says so). "Cursed indefinitely" (Brutal Strike) is `until-respawn` with a note quoting "indefinitely". Drop open questions that only
    asked this.
37. **Self-cast variants.** When the text says "if cast on self ...", add a separate effect on `caster` with condition `cast-on-self`
    (polarity from the caster's view), and give the matching target effect the condition `cast-on-other`. Do not use the property
    `affects-caster-and-target` for this; that property is only for abilities that affect the caster and others at once (Circle of Protection).
38. **Kill Trigger** always means the property `kill-trigger`, the requirement `immediately-after-kill` and timing `on-kill` on the effects.
    Wound Trigger: property `wound-trigger`, the requirement `immediately-after-wound` and timing `on-wound`.
39. **Limits on a granted ability** (Regeneration's Heal may not be used within 10' of an enemy) are an `ability.modify` harm effect on the
    granted ability plus a `modifies` reference, never a requirement of the granting ability. When the limit is one of the requirement ids (no living enemy within 10'), also put that id in the effect's `requirement` parameter.
40. **Strip-casting Enchantments** carry `ability.cast-via-strips`, `enchantment.spend-strip`, termination `last-strip`, properties
    `uses-strips` and `materials-required`, and a `mentions` reference to the `enchantments` mechanic.
41. **Type references.** Every Trait has a `mentions` reference to mechanic `traits`; every Archetype to mechanic `archetype`, citing the
    first sentence (or the sentence that shows it).
42. **Declarations.** Text that requires saying something aloud gets `must-declare` (words in the note); add `declaration-not-incantation`
    when the text says the declaration is not an incantation.
43. **Equipment coverage.** `defense.resistance` always sets `covers_equipment` (`yes` only when the text extends it to carried equipment).
    When any other protection explicitly covers equipment, add a second effect of the same kind on `bearer-equipment` (as Flame Blade does).
44. **Weapon Special Effects from an Enchantment** use subject `bearer` (a Self Verbal uses `caster`), with the weapons in `on`.
45. **Reference relations.** A State required of the target: `requires`. A State in a "fails if / does not work on" rule: `mentions`.
    Something a protection names as protected against: `protects-against`. An ability removed by an archetype: `removes`. An ability or
    mechanic an archetype changes: `modifies`. The Charge mechanic when only frequency changes: `mentions`. Abilities excluded by
    `not-on-certain-abilities`: `excludes`.
46. **Set frequencies.** When an archetype *sets* a frequency (which can mean fewer uses for some abilities) use polarity `neutral` and an
    open question. When it only adds uses or Charge, `benefit`.
47. **Per named ability.** Convention 34 applies per named ability: an archetype changing Blink and Shadow Step gets one `ability.modify`
    and one `economy.frequency` for each.
48. **Polarity `depends`**: an effect on another player that helps an ally and hinders an enemy equally (Astral Intervention cast on
    another player). Use it sparingly; most abilities have an intended use.
49. **Archetype roles** include the roles of the abilities they grant (Hunter, Corruptor, Infernal, Artificer).
50. **`max-active-per-caster`** always gives `n` and a note saying whether it caps or raises the normal limit.
