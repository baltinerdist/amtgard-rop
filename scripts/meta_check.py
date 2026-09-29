#!/usr/bin/env python3
"""Validate Ability Metadata Platform records (metadata/source/records/<slug>.json).

  meta_check.py [PATH ...]      files or directories (default: metadata/source/records)
  meta_check.py --quiet ...     errors and totals only
  meta_check.py --snapshot      record the current rule sentences in metadata/source/sentences.json (after records are updated)

ERRORS (must be fixed): unknown vocabulary, wrong shapes or parameter values, evidence ids that do not exist, and any sentence of
the rule text that no item cites (every sentence must be accounted for).
WARNINGS (read each): numbers, States, Special Effects, abilities and key phrases in the text that no item seems to carry.
Exit status is non-zero when there are errors.
"""
import glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meta_source as MS
import meta_vocab as V

ROOT = MS.ROOT
REC_DIR = os.path.join(ROOT, "metadata", "source", "records")
TOP = {"slug", "summary", "effects", "requirements", "restrictions", "termination", "properties", "references", "clarifications",
       "roles", "beneficiary", "open_questions"}
EFFECT_KEYS = {"id", "kind", "subject", "polarity", "params", "duration", "timing", "conditions", "choice", "evidence", "note", "delay_seconds", "max_targets"}


def _load_entries():
    return MS.load()


def check(rec, ent, titles):
    errs, warns = [], []
    slug = ent["slug"]
    sids = {s["id"]: s["text"] for s in ent["sentences"]}
    cited = set()

    def ev(item, where):
        e = item.get("evidence")
        if not isinstance(e, list) or not e:
            errs.append(f"{where}: evidence must be a non-empty list of sentence ids")
            return
        for x in e:
            if x not in sids:
                errs.append(f"{where}: evidence {x!r} is not a sentence id of {slug} ({', '.join(sids) or 'none'})")
            else:
                cited.add(x)

    if not isinstance(rec, dict):
        return [f"{slug}: record is not an object"], []
    missing = TOP - set(rec)
    extra = set(rec) - TOP - {"note"}
    if missing:
        errs.append(f"missing keys {sorted(missing)}")
    if extra:
        errs.append(f"unknown keys {sorted(extra)}")
    if missing:
        return errs, warns
    if rec["slug"] != slug:
        errs.append(f"slug {rec['slug']!r} does not match {slug!r}")
    if not isinstance(rec["summary"], str) or not rec["summary"].strip():
        errs.append("summary is empty")
    elif len(rec["summary"].split()) > 30:
        warns.append(f"summary is long ({len(rec['summary'].split())} words)")

    # effects
    ids = set()
    for i, e in enumerate(rec["effects"]):
        w = f"effect[{i}]"
        if not isinstance(e, dict):
            errs.append(f"{w}: not an object"); continue
        bad = set(e) - EFFECT_KEYS
        if bad:
            errs.append(f"{w}: unknown keys {sorted(bad)}")
        for k in ("id", "kind", "subject", "polarity", "duration", "timing", "evidence"):
            if k not in e:
                errs.append(f"{w}: missing {k}")
        if e.get("id") in ids:
            errs.append(f"{w}: duplicate id {e.get('id')}")
        ids.add(e.get("id"))
        k = e.get("kind")
        if k not in V.EFFECTS:
            errs.append(f"{w}: unknown kind {k!r}")
        else:
            spec = V.EFFECTS[k]["params"]
            for pk, pv in (e.get("params") or {}).items():
                if pk not in spec:
                    errs.append(f"{w} ({k}): param {pk!r} not allowed (allowed: {sorted(spec) or 'none'})")
                    continue
                allowed = spec[pk]
                if allowed == "int":
                    if not isinstance(pv, int):
                        errs.append(f"{w} ({k}): {pk} must be an integer")
                elif allowed == "ability":
                    if pv not in titles:
                        errs.append(f"{w} ({k}): {pk} {pv!r} is not an ability title")
                elif allowed == "abilities":
                    for x in (pv if isinstance(pv, list) else [pv]):
                        if x not in titles:
                            errs.append(f"{w} ({k}): {pk} {x!r} is not an ability title")
                elif allowed == "states":
                    for x in (pv if isinstance(pv, list) else [pv]):
                        if x not in V.STATES:
                            errs.append(f"{w} ({k}): {pk} {x!r} is not a State")
                elif allowed == "special-effects":
                    for x in (pv if isinstance(pv, list) else [pv]):
                        if x not in V.SPECIAL_EFFECTS:
                            errs.append(f"{w} ({k}): {pk} {x!r} is not a Special Effect")
                elif allowed == "schools":
                    for x in (pv if isinstance(pv, list) else [pv]):
                        if x not in V.SCHOOLS:
                            errs.append(f"{w} ({k}): {pk} {x!r} is not a School")
                elif allowed == "text":
                    if not isinstance(pv, str):
                        errs.append(f"{w} ({k}): {pk} must be text")
                    elif k == "ability.modify" and pk == "requirement" and pv not in V.REQUIREMENTS:
                        errs.append(f"{w} ({k}): requirement {pv!r} is not a requirement id")
                elif isinstance(allowed, list) and pv not in allowed:
                    errs.append(f"{w} ({k}): {pk} {pv!r} not in {allowed}")
            if k == "state.apply" and "state" not in (e.get("params") or {}):
                errs.append(f"{w}: state.apply needs params.state")
            if k == "other":
                warns.append(f"{w}: uses 'other' ({(e.get('params') or {}).get('text', '')!r}); make sure an open question explains it")
        if e.get("subject") not in V.SUBJECTS:
            errs.append(f"{w}: subject {e.get('subject')!r} not in {list(V.SUBJECTS)}")
        if e.get("polarity") not in V.POLARITY:
            errs.append(f"{w}: polarity {e.get('polarity')!r} not in {list(V.POLARITY)}")
        d = e.get("duration") or {}
        if not isinstance(d, dict) or d.get("type") not in V.DURATION:
            errs.append(f"{w}: duration.type must be one of {list(V.DURATION)}")
        elif d.get("type") == "timed" and not isinstance(d.get("seconds"), int):
            errs.append(f"{w}: timed duration needs integer seconds")
        elif d.get("type") != "timed" and "seconds" in d:
            errs.append(f"{w}: only timed durations take seconds")
        if set(d) - {"type", "seconds"}:
            errs.append(f"{w}: duration has unknown keys {sorted(set(d) - {'type', 'seconds'})}")
        if e.get("timing") not in V.TIMING:
            errs.append(f"{w}: timing {e.get('timing')!r} not in {list(V.TIMING)}")
        if e.get("timing") == "after-delay" and not isinstance(e.get("delay_seconds"), int):
            errs.append(f"{w}: after-delay needs integer delay_seconds")
        for c in e.get("conditions") or []:
            if c not in V.CONDITIONS:
                errs.append(f"{w}: condition {c!r} not in CONDITIONS")
        ch = e.get("choice")
        if ch is not None and not (isinstance(ch, dict) and set(ch) == {"group", "option"}):
            errs.append(f"{w}: choice must be {{group, option}}")
        ev(e, w)
        if k == "state.apply" and e.get("polarity") == "benefit" and e.get("subject") in ("target", "struck-player") \
                and (e.get("params") or {}).get("state") not in ("insubstantial", "invulnerable"):
            warns.append(f"{w}: a harmful State on a target is marked benefit")

    for key, vocab in (("requirements", V.REQUIREMENTS), ("restrictions", V.RESTRICTIONS), ("termination", V.TERMINATION),
                       ("properties", V.PROPERTIES)):
        for i, it in enumerate(rec[key]):
            w = f"{key}[{i}]"
            if not isinstance(it, dict) or it.get("kind") not in vocab:
                errs.append(f"{w}: kind {it.get('kind') if isinstance(it, dict) else it!r} not in {key} vocabulary")
                continue
            bad = set(it) - {"kind", "evidence", "note", "n", "conditions"}
            if bad:
                errs.append(f"{w}: unknown keys {sorted(bad)}")
            for c in it.get("conditions") or []:
                if c not in V.CONDITIONS:
                    errs.append(f"{w}: condition {c!r} not in CONDITIONS")
            ev(it, w)
    for i, r in enumerate(rec["references"]):
        w = f"references[{i}]"
        if r.get("target") not in V.REF_TARGETS:
            errs.append(f"{w}: target {r.get('target')!r} not in {V.REF_TARGETS}")
        elif r["target"] == "ability" and r.get("name") not in titles:
            errs.append(f"{w}: ability {r.get('name')!r} is not an ability title")
        elif r["target"] == "state" and r.get("name") not in V.STATES:
            errs.append(f"{w}: state {r.get('name')!r} not in {V.STATES}")
        elif r["target"] == "special-effect" and r.get("name") not in V.SPECIAL_EFFECTS:
            errs.append(f"{w}: special effect {r.get('name')!r} not in {V.SPECIAL_EFFECTS}")
        elif r["target"] == "mechanic" and r.get("name") not in V.MECHANICS:
            errs.append(f"{w}: mechanic {r.get('name')!r} not in MECHANICS")
        if r.get("relation") not in V.REF_RELATIONS:
            errs.append(f"{w}: relation {r.get('relation')!r} not in {list(V.REF_RELATIONS)}")
        bad = set(r) - {"target", "name", "relation", "evidence", "note"}
        if bad:
            errs.append(f"{w}: unknown keys {sorted(bad)}")
        ev(r, w)
    for i, c in enumerate(rec["clarifications"]):
        w = f"clarifications[{i}]"
        if not isinstance(c, dict) or not isinstance(c.get("text"), str) or not c["text"].strip():
            errs.append(f"{w}: needs text")
            continue
        ev(c, w)
    for r in rec["roles"]:
        if r not in V.ROLES:
            errs.append(f"role {r!r} not in {list(V.ROLES)}")
    if not rec["roles"]:
        errs.append("roles is empty")
    if rec["beneficiary"] not in V.BENEFICIARY:
        errs.append(f"beneficiary {rec['beneficiary']!r} not in {list(V.BENEFICIARY)}")
    if not isinstance(rec["open_questions"], list):
        errs.append("open_questions must be a list")

    # coverage: every sentence accounted for
    for sid in sids:
        if sid not in cited:
            errs.append(f"sentence {sid} is not cited by any item: {sids[sid][:90]!r}")

    # heuristics
    text = " ".join(t for t in sids.values() if not t.startswith("Example"))
    low = text.lower()
    nums_secs = {int(x) for x in re.findall(r"(\d+)\s*(?:seconds|s\b)", text)}
    have_secs = {(e.get("duration") or {}).get("seconds") for e in rec["effects"]} | {e.get("delay_seconds") for e in rec["effects"]}
    for n in sorted(nums_secs - have_secs):
        warns.append(f"text says {n} seconds but no effect duration or delay carries {n}")
    feet = {int(x) for x in re.findall(r"(\d+)'", text)}
    blob = json.dumps(rec)
    for n in sorted(feet):
        if f'"feet": {n}' not in blob and f"{n}ft" not in blob and f"{n}'" not in blob and f"{n} " not in blob:
            warns.append(f"text mentions {n}' but no item carries it (feet param, a requirement like no-enemy-within-{n}ft, or a note)")
    carried_states = set()
    for e in rec["effects"]:
        p = e.get("params") or {}
        for k in ("state", "states", "except"):
            v = p.get(k)
            carried_states.update(v if isinstance(v, list) else [v] if v else [])
    carried_states.update(r["name"] for r in rec["references"] if r.get("target") == "state")
    for s in V.STATES:
        if re.search(r"\b" + s + r"\b(?! by)", low) and s not in carried_states:
            warns.append(f"text mentions the State {s!r} but no effect or reference carries it")
    se_names = {"armor breaking": "armor-breaking", "armor destroying": "armor-destroying", "phasing": "phasing", "shield crushing": "shield-crushing",
                "shield destroying": "shield-destroying", "siege": "siege", "weapon destroying": "weapon-destroying", "wounds kill": "wounds-kill"}
    carried_se = {(e.get("params") or {}).get("effect") for e in rec["effects"]} | {r["name"] for r in rec["references"] if r.get("target") == "special-effect"}
    for phrase, sid_ in se_names.items():
        if phrase in low and sid_ not in carried_se:
            warns.append(f"text mentions {phrase!r} but no effect or reference carries {sid_}")
    props = {p["kind"] for p in rec["properties"]}
    for phrase, prop in (("is a forced movement effect", "forced-movement"), ("as a forced movement effect", "forced-movement"), ("kill trigger", "kill-trigger"), ("wound trigger", "wound-trigger"),
                         ("engulfing.", "engulfing"), ("must chant", "chant"), ("does not count towards", "exempt-from-enchantment-limit"),
                         ("this enchantment is persistent", "persistent"), ("does not require verbal targeting", "no-verbal-targeting"),
                         ("may be cast while moving", "castable-while-moving"), ("ignores armor", "bypass-armor"),
                         ("regardless of", None), ("strip", "uses-strips")):
        if phrase in low and prop and prop not in props:
            warns.append(f"text contains {phrase!r}: check the property {prop!r}")
    for m in re.finditer(r"(?<!who are )Immune to (?:the )?([A-Z]\w+)", text):
        sch = m.group(1)
        if sch in V.SCHOOLS and not any(e.get("kind") == "defense.immunity" and (e.get("params") or {}).get("school") == sch for e in rec["effects"]) \
                and not any(sch in json.dumps(e.get("params")) for e in rec["effects"]):
            warns.append(f"text says 'Immune to {sch}' but no defense.immunity effect carries it")
    named = {r["name"] for r in rec["references"] if r.get("target") == "ability"} | \
            {(e.get("params") or {}).get("ability") for e in rec["effects"]}
    own = ent["title"]
    masked = re.sub(re.escape(own), " ", text)
    for t in sorted(titles, key=len, reverse=True):
        if t == own or len(t) < 4:
            continue
        if re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])(?! shield)", masked):
            masked = re.sub(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", " ", masked)
            if t not in named and not (t == "Persistent" and any(r.get("name") == "persistent" for r in rec["references"])):
                warns.append(f"text names the ability {t!r} but no reference or effect names it")
    # conventions (AUTHORING.md 36-47): checked on every record
    kinds = [e.get("kind") for e in rec["effects"]]
    reqk = {r["kind"] for r in rec["requirements"]}
    termk = {t["kind"] for t in rec["termination"]}
    refm = {(r.get("target"), r.get("name")) for r in rec["references"]}
    for e in rec["effects"]:
        p = e.get("params") or {}
        if e.get("kind") == "state.apply" and p.get("state") == "cursed" and (e.get("duration") or {}).get("type") == "until-removed" \
                and ent["type"] != "Enchantment":
            warns.append(f"conv 36: Cursed with no stated duration should be until-respawn ({e.get('id')})")
        if e.get("kind") == "defense.resistance" and "covers_equipment" not in p:
            warns.append(f"conv 43: defense.resistance must set covers_equipment ({e.get('id')})")
        if e.get("kind") == "special-effect.grant" and e.get("subject") == "bearer-equipment":
            warns.append(f"conv 44: weapon Special Effects use subject bearer (or caster), not bearer-equipment ({e.get('id')})")
        if "cast-on-self" in (e.get("conditions") or []) and not any("cast-on-other" in (x.get("conditions") or []) for x in rec["effects"]):
            warns.append("conv 37: a cast-on-self effect exists, so the matching target effect needs cast-on-other")
    if "kill-trigger" in props and ("immediately-after-kill" not in reqk or not any(e.get("timing") == "on-kill" for e in rec["effects"])):
        warns.append("conv 38: Kill Trigger needs the requirement immediately-after-kill and on-kill timing")
    if "ability.cast-via-strips" in kinds:
        miss = [x for x, ok in (("enchantment.spend-strip", "enchantment.spend-strip" in kinds), ("last-strip", "last-strip" in termk),
                                ("uses-strips", "uses-strips" in props), ("materials-required", "materials-required" in props),
                                ("enchantments reference", ("mechanic", "enchantments") in refm)) if not ok]
        if miss:
            warns.append("conv 40: strip-casting Enchantment is missing " + ", ".join(miss))
    if ent["type"] == "Trait" and ("mechanic", "traits") not in refm:
        warns.append("conv 41: Traits reference the mechanic traits")
    if ent["type"] == "Archetype" and ("mechanic", "archetype") not in refm:
        warns.append("conv 41: Archetypes reference the mechanic archetype")
    return errs, warns


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quiet = "--quiet" in sys.argv
    paths = []
    for a in args or [REC_DIR]:
        paths += sorted(glob.glob(os.path.join(a, "*.json"))) if os.path.isdir(a) else [a]
    ents = _load_entries()
    titles = {e["title"] for e in ents.values()}
    snap_path = os.path.join(ROOT, "metadata", "source", "sentences.json")
    if "--snapshot" in sys.argv:
        json.dump({s: {x["id"]: x["text"] for x in e["sentences"]} for s, e in sorted(ents.items())}, open(snap_path, "w"), indent=1, ensure_ascii=False)
        print(f"snapshot of {sum(len(e['sentences']) for e in ents.values())} sentences written to {snap_path}")
        return 0
    snap = json.load(open(snap_path)) if os.path.exists(snap_path) else {}
    n_err = n_warn = 0
    for p in paths:
        try:
            rec = json.load(open(p))
        except Exception as ex:
            print(f"ERROR {os.path.basename(p)}: not valid JSON ({ex})"); n_err += 1; continue
        slug = os.path.basename(p)[:-5]
        if slug not in ents:
            print(f"ERROR {slug}: not an entry in scope"); n_err += 1; continue
        errs, warns = check(rec, ents[slug], titles)
        if snap:
            now = {x["id"]: x["text"] for x in ents[slug]["sentences"]}
            old = snap.get(slug, {})
            for sid in sorted(set(now) | set(old)):
                if now.get(sid) != old.get(sid):
                    errs.append(f"rule text changed since the record was checked: {sid} was {old.get(sid)!r}, now {now.get(sid)!r} "
                                 f"(update the record, then run meta_check.py --snapshot)")
        for x in errs:
            print(f"ERROR {slug}: {x}")
        if not quiet:
            for x in warns:
                print(f"warn  {slug}: {x}")
        n_err += len(errs); n_warn += len(warns)
    print(f"==== {len(paths)} records, {n_err} error(s), {n_warn} warning(s) ====")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
