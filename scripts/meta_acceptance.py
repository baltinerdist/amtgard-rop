#!/usr/bin/env python3
"""Run the acceptance battery (metadata/acceptance.json) against the platform and write metadata/ACCEPTANCE.md.

Each question has a canonical scripts/meta_query.py query and an expected answer built independently from the rule text. Question 40
checks similarity pairs instead. Exits 1 if any question fails (known gaps are reported but do not fail the run).
Run after scripts/meta_build.py:  python3 scripts/meta_acceptance.py
"""
import json, os, shlex, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rop_version as RV

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "metadata")


def run_query(q):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "meta_query.py"), *shlex.split(q), "--json"], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"query failed: {q}\n{r.stderr}")
    return {x["slug"] for x in json.loads(r.stdout)}


def main():
    A = json.load(open(os.path.join(MD, "acceptance.json")))
    D = json.load(open(os.path.join(MD, "abilities.json")))
    pairs = {(p["a"], p["b"]): p["relation"] for p in D["pairs"]}

    def rel(a, b):
        if (a, b) in pairs:
            return pairs[(a, b)]
        r = pairs.get((b, a))
        return None if r is None else r if r in ("identical", "same-effects", "same-effects-different-numbers", "overlap") else "reverse-" + r

    rows, fails, gaps = [], 0, 0
    o = ["---", 'title: "Acceptance test"', "section: Ability Metadata", f"rulebook_version: {RV.NAME}", "generated_by: scripts/meta_acceptance.py", "---", "",
         "# Acceptance test", "",
         "Questions the platform must answer, each with an answer built independently from the rule text by four agents who did not see the "
         "platform's output. Where a later check of the rule text showed a tester was wrong, the expected answer was corrected and the reason is "
         "listed. `scripts/meta_acceptance.py` reruns every question and rewrites this page; it fails if any answer changes.", ""]
    body = []
    for q in A["questions"]:
        if "pairs" in q:
            bad, known = [], []
            for p in q["pairs"]:
                r = rel(p["a"], p["b"])
                ok = r is not None and (p["relation"] == "any" or r in p["relation"].split("|"))
                if not ok:
                    (known if p.get("known_gap") else bad).append(f"{p['a']} {p['relation']} {p['b']} (found: {r or 'no pair'})" +
                                                                  (f" — known gap: {p['known_gap']}" if p.get("known_gap") else ""))
            for p in q["forbidden"]:
                if rel(p["a"], p["b"]) == p["relation"]:
                    bad.append(f"{p['a']} must not be {p['relation']} {p['b']}: {p['reason']}")
            status = "FAIL" if bad else "pass"
            fails += bool(bad)
            gaps += len(known)
            rows.append((q["id"], status, f"{len(q['pairs']) - len(bad) - len(known)}/{len(q['pairs'])} pairs, {len(q['forbidden'])} forbidden checked"))
            body += [f"## {q['id']}. {q['question']}", "", q["note"], "", f"**{status}**: {rows[-1][2]}.", ""]
            body += [f"- {p['a']} **{p['relation']}** {p['b']}" for p in q["pairs"]] + [""]
            body += ["Must not be reported:", ""] + [f"- {p['a']} {p['relation']} {p['b']}: {p['reason']}" for p in q["forbidden"]] + [""]
            if bad:
                body += ["Failures:", ""] + [f"- {b}" for b in bad] + [""]
            if known:
                body += ["Known gaps:", ""] + [f"- {k}" for k in known] + [""]
            continue
        got, exp = run_query(q["query"]), set(q["expected"])
        miss, extra = sorted(exp - got), sorted(got - exp)
        status = "pass" if not miss and not extra else "FAIL"
        fails += status == "FAIL"
        rows.append((q["id"], status, f"{len(got & exp)}/{len(exp)}" + (f", missing {', '.join(miss)}" if miss else "") + (f", extra {', '.join(extra)}" if extra else "")))
        body += [f"## {q['id']}. {q['question']}", "", f"`python3 scripts/meta_query.py {q['query']}`", "", f"**{status}**: {rows[-1][2]}.", "",
                 "Expected: " + ", ".join(q["expected"]), ""]
        if q["corrections"]:
            body += ["Corrections to the tester's answer:", ""] + [f"- {c['change']} **{c['slug']}**: {c['reason']}" for c in q["corrections"]] + [""]
    o += [f"**{sum(r[1] == 'pass' for r in rows)} of {len(rows)} pass**" + (f"; {gaps} known gap(s) listed under question 40." if gaps else "."), "",
          "| # | Result | Detail |", "| --- | --- | --- |"] + [f"| {i} | {s} | {d} |" for i, s, d in rows] + [""] + body
    open(os.path.join(MD, "ACCEPTANCE.md"), "w").write("\n".join(o))
    for i, s, d in rows:
        if s != "pass":
            print(f"Q{i}: {s} {d}")
    print(f"{sum(r[1] == 'pass' for r in rows)}/{len(rows)} pass, {gaps} known gap(s); wrote metadata/ACCEPTANCE.md")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
