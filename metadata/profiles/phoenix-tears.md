---
title: "Phoenix Tears"
section: Ability Metadata
rulebook_version: V8.08 "Spongy"
generated_by: scripts/meta_build.py
---

# Phoenix Tears

> Instead of dying, bearer heals all wounds and is Frozen 30s; then loses Cursed, non-persistent Enchantments and a strip, repairs equipment; +1 Persistent Protection Enchantment.

| | |
| --- | --- |
| Type | Enchantment (enchantment) |
| School | Spirit |
| Range | Self (Wa) Other (He) |
| Incantation | "May the tears of the phoenix wash over thee" x3 |
| Materials | Two white strips |
| Magical | yes, (m) for at least one class |
| Roles | defense, healing, equipment, resource · for: ally |
| Capabilities | cleanses, extra-enchantments, has-drawback, heals, more-uses, repairs, survives-death |
| Drawbacks from limits | may not be used or worn with named abilities (list them in references with relation 'excludes') |
| Rule text | [rules/magic-and-abilities/phoenix-tears.md](../../rules/magic-and-abilities/phoenix-tears.md) · [interoperability](../../interoperability/abilities/phoenix-tears.md) |

## Who has it

| Class | Level | Cost | Max | Frequency | Uses | Per | Charge | (m)/(ex) | Range | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Healer | 6th | 1 | - | 1/Refresh | 1 | refresh | - | (m) | Other | - |
| Warrior | 6th | - | - | - | - | - | - | - | - | - |

## What it does

| # | Effect | On | For them | Details | From |
| --- | --- | --- | --- | --- | --- |
| e1 | **Prevents death** | bearer | benefit | instead heal-and-frozen; while worn; when the subject would die — Bearer does not die as normal; instead removes all wounds and becomes Frozen for 30 seconds. | E1, E2 |
| e2 | **Heals wounds** | bearer | benefit | amount all; instant; when the subject would die | E2 |
| e3 | **Freezes** | bearer | harm | 30 s; when the subject would die — Part of the save; recorded as harm because the bearer is out of action for 30 seconds. | E2 |
| e4 | **Ends Cursed** | bearer | benefit | what specific-state; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment — When the Frozen State elapses or is removed, if still enchanted: remove Cursed, if Cursed. | E3, E4 |
| e5 | **Repairs equipment** | bearer-equipment | benefit | what all-carried-equipment; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment | E3, E5 |
| e6 | **Removes Enchantments** | bearer | harm | scope non-persistent-others; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment — All non-persistent Enchantments other than Phoenix Tears are removed. | E3, E6 |
| e7 | **Uses up a strip** | bearer | neutral | n 1; instant; when an earlier State from this ability ends; only if the bearer still has the Enchantment — Step 4: remove a strip each time the save resolves. | E3, E7 |
| e8 | **Allows extra Enchantments** | bearer | benefit | count 1; only protection-school; while worn; continuously while it is worn, chanted or in effect | E8 |
| e9 | **Makes Enchantments Persistent** | bearer | benefit | which the-extra-enchantment; while worn; continuously while it is worn, chanted or in effect — Persistent only as long as Phoenix Tears is present. | E9 |
| e10 | **Removes Enchantments** | bearer | harm | scope chosen-to-meet-limit; instant; when the Enchantment is removed — If necessary, when Phoenix Tears is removed the bearer chooses which (m) Enchantments to lose to meet the new Enchantment limit. | N1 |

**Drawbacks:** Freezes (bearer); Removes Enchantments (bearer); Removes Enchantments (bearer)

## Restrictions

- **not-with-abilities**: may not be used or worn with named abilities (list them in references with relation 'excludes') — May not be worn with Attuned or Essence Graft. *(L1)*

## How it ends early

- **last-strip**: removed when the last strip is removed — A strip is removed each time it resolves (step 4); removed when the last strip is removed. *(E7, N1)*

## Properties

- **uses-strips**: tracked with enchantment strips — Two white strips; one is removed per activation (E7). *(E7, N1)*
- **bypass-cursed**: works on (or removes) Cursed — Removes the Cursed State (step 1). *(E4)*
- **has-choice**: the subject chooses between options — When Phoenix Tears is removed, the bearer chooses which (m) Enchantments to lose to meet the limit. *(N1)*

## Clarifications in the text

- Steps 1-4 happen only if the bearer is still enchanted when the Frozen State elapses or is removed. *(E3)*
- The extra Protection Enchantment is not removed when Phoenix Tears is removed. *(E10)*
- When Phoenix Tears is removed, the bearer chooses which (m) Enchantments to lose to meet their new Enchantment limit, if necessary. *(N1)*

## Names in the text

- ability **[Attuned](attuned.md)**: excludes *(L1)*
- ability **[Essence Graft](essence-graft.md)**: excludes *(L1)*
- state **frozen**: mentions *(E2, E3)*
- state **cursed**: mentions *(E4)*
- mechanic **persistent**: mentions *(E6, E9)*
- mechanic **enchantments**: mentions *(E6, E8, E10)*
- mechanic **enchantment-limit**: mentions *(N1)*
- mechanic **school**: mentions *(E8)*
- mechanic **strips**: mentions *(E7, N1)*

## Similar abilities

| Relation | Ability | Differences |
| --- | --- | --- |
| is given by | [Juggernaut](juggernaut.md) | only Phoenix Tears: Prevents death (bearer, while worn); only Phoenix Tears: Heals wounds (bearer, amount all, instant); only Phoenix Tears: Freezes (bearer, 30 s); only Phoenix Tears: Ends Cursed (bearer, instant, if still-enchanted); only Phoenix Tears: Repairs equipment (bearer-equipment, instant, if still-enchanted); only Phoenix Tears: Removes Enchantments (bearer, instant, if still-enchanted); only Phoenix Tears: Uses up a strip (bearer, instant, if still-enchanted); only Phoenix Tears: Allows extra Enchantments (bearer, count 1, while worn) |

## Open questions

- N1 is two sentences run together in the source (missing period after 'removed'); segmentation treats them as one.
- E10 vs N1: the extra Enchantment is kept after Phoenix Tears is removed, yet the bearer may then have to drop (m) Enchantments to meet the limit; unclear whether the kept extra one can be the one dropped.

## Rule text, sentence by sentence

Every sentence and the items that cite it.

| Id | Sentence | Captured as |
| --- | --- | --- |
| E1 | Bearer does not die as normal. | effect e1 (Prevents death) |
| E2 | When the bearer would otherwise die they instead remove all wounds and become Frozen for 30 seconds. | effect e1 (Prevents death); effect e2 (Heals wounds); effect e3 (Freezes); names frozen |
| E3 | If the bearer is still enchanted when the Frozen State elapses or is removed: | effect e4 (Ends Cursed); effect e5 (Repairs equipment); effect e6 (Removes Enchantments); effect e7 (Uses up a strip); names frozen; clarification |
| E4 | 1. Remove the Cursed state, if Cursed | effect e4 (Ends Cursed); property bypass-cursed; names cursed |
| E5 | 2. Repair all carried equipment. | effect e5 (Repairs equipment) |
| E6 | 3. Remove all non-persistent enchantments other than Phoenix Tears. | effect e6 (Removes Enchantments); names persistent; names enchantments |
| E7 | 4. Remove a strip. | effect e7 (Uses up a strip); ends when last-strip; property uses-strips; names strips |
| E8 | Additionally, Phoenix Tears allows the bearer to wear an extra Enchantment from the Protection School. | effect e8 (Allows extra Enchantments); names enchantments; names school |
| E9 | This extra enchantment is considered Persistent as long as Phoenix Tears is present. | effect e9 (Makes Enchantments Persistent); names persistent |
| E10 | The additional Enchantment is not removed once Phoenix Tears is removed. | names enchantments; clarification |
| L1 | May not be worn with Attuned or Essence Graft. | restriction not-with-abilities; names Attuned; names Essence Graft |
| N1 | Phoenix Tears is removed when the last strip is removed If Phoenix Tears is removed, the bearer chooses which (m) Enchantments to lose to meet their new Enchantment limit, if necessary. | effect e10 (Removes Enchantments); ends when last-strip; property uses-strips; property has-choice; names enchantment-limit; names strips; clarification |

---
*Generated by `scripts/meta_build.py` from `metadata/source/records/phoenix-tears.json` and the V8.08 "Spongy" rules.*
