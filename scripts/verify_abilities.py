#!/usr/bin/env python3
"""Verify the 180 generated ability files against the source PDF.

Four independent checks:
  1. BODY TEXT   - for each ability, the raw source field text (T:/S:/R:/I:/M:/E:/L:/N:)
                   compared token by token against the field values actually written in
                   the md file. Any mismatch => the parser dropped/altered/merged content.
  2. AVAILABILITY- each file's class_availability frontmatter and **Available to:** line
                   compared against the class codes on the source's ability header line.
  3. COMPLETENESS- every spell listed in the four magic-user spell tables (Bard, Druid,
                   Healer, Wizard) maps to an ability file that claims that class at that
                   level, and vice versa.
  4. COUNT       - reconcile the section's T: type-lines against the file count.
Exit status is non-zero if any check fails.
"""
import importlib.util, re, os, glob, difflib, sys

spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__),"gen_abilities.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
MA = os.path.join(g.ROOT, "rules/magic-and-abilities")
CLASSES_DIR = os.path.join(g.ROOT, "rules/classes")
MAGIC_USERS = ["bard", "druid", "healer", "wizard"]

TOK = re.compile(r"[a-z0-9][a-z0-9/.'%\"-]*")
def toks(s):
    s = g.norm(s).lower().replace("`", "")
    return TOK.findall(s)

def source_body_tokens(block):
    """tokens of the field text (strip the single-letter field labels only).

    Lines are rejoined with the generator's own rule so a token the PDF wrapped
    mid-word ('Meta-' / 'Magics') is compared as the one token it really is."""
    text = g.flatten(block["body"])
    text = re.sub(g.FIELD, ' ', text)                    # drop field-label markers
    text = text.replace("- ", " ")                       # bullet markers in L: lists
    return toks(text)

def md_value_tokens(md):
    """All rule text written in the file: everything between the frontmatter and the
    trailing source note, minus the H1, the Available-to line, and markdown scaffolding."""
    body = md.split("\n---\n", 1)[1] if "\n---\n" in md else md
    body = re.split(r'^---$', body, flags=re.M)[0]      # drop the trailing source note
    keep = []
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith("# ") or s.startswith("**Available to:**"): continue
        s = re.sub(r'^\*\*[A-Za-z]+:\*\*\s*', '', s)     # field label
        s = re.sub(r'^-\s+', '', s)                      # bullet marker
        keep.append(s)
    return toks(" ".join(keep))

def frontmatter(md):
    m = re.search(r'^---\n(.*?)\n---', md, re.S)
    d = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                d[k.strip()] = v.strip().strip('"')
    return d

def class_tables():
    """{class name: {ability name: {levels}}} parsed from the magic-user spell tables.
    A class may list the same ability at more than one level (Bard buys
    'Equipment: Armor, 1 Point' at both 2 and 6), so levels are a set."""
    out = {}
    for slug in MAGIC_USERS:
        path = os.path.join(CLASSES_DIR, slug + ".md")
        txt = open(path).read()
        spells, lvl = {}, None
        for line in txt.split("\n"):
            m = re.match(r'^###\s+(\d)(?:st|nd|rd|th)\s+Level', line)
            if m: lvl = int(m.group(1)); continue
            if lvl and line.startswith("|"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if not cells or cells[0] in ("Name", "") or set(cells[0]) <= set("-"): continue
                name = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', cells[0]).strip()
                spells.setdefault(name, set()).add(lvl)
        out[frontmatter(txt).get("title", slug)] = spells
    return out

def main():
    lines = g.extract_lines()
    blocks, _ = g.find_blocks(lines)
    fails = 0

    # ---- 1 & 2: body text and availability, per ability ----------------------
    perfect = avail_ok = 0
    availability = {}      # ability name -> {class: level}
    for b in blocks:
        path = os.path.join(MA, g.slug(b["name"])+".md")
        if not os.path.exists(path):
            print(f"[MISSING FILE] {b['name']} -> {path}"); fails += 1; continue
        md = open(path).read()

        src, mdtok = source_body_tokens(b), md_value_tokens(md)
        sm = difflib.SequenceMatcher(a=src, b=mdtok, autojunk=False)
        diffs = [(op, src[i1:i2], mdtok[j1:j2])
                 for op,i1,i2,j1,j2 in sm.get_opcodes() if op != 'equal']
        if diffs:
            fails += 1
            print(f"\n### BODY {b['name']}  (source p{b['page']})")
            for op,s,m2 in diffs:
                print(f"   {op:7s} source={s}  md={m2}")
        else:
            perfect += 1

        # availability: source header codes vs frontmatter vs the Available-to line
        want = [f"{g.CLASS[c]} {lvl}" for c,lvl in g.CODE_TOKEN.findall(b["codes"])]
        fm = frontmatter(md)
        got_fm = re.findall(r'"([^"]+)"', fm.get("class_availability", "[]"))
        m = re.search(r'^\*\*Available to:\*\*\s*(.+)$', md, re.M)
        got_line = [x.strip() for x in m.group(1).split(",")] if m else []
        if want != got_fm or (want and want != got_line):
            fails += 1
            print(f"\n### AVAIL {b['name']}: source={want} frontmatter={got_fm} line={got_line}")
        else:
            avail_ok += 1
        avail = {}
        for c in want:
            cls, lvl = c.rsplit(" ", 1)
            avail.setdefault(cls, set()).add(int(lvl))
        availability[b["name"]] = avail

    # ---- 3: completeness against the four magic-user spell tables ------------
    tables = class_tables()
    counts = []
    for cls, spells in sorted(tables.items()):
        counts.append(f"{cls} {sum(len(v) for v in spells.values())}")
        for name, lvls in sorted(spells.items()):
            if name not in availability:
                print(f"\n### TABLE {cls}: '{name}' has no ability file"); fails += 1
            elif availability[name].get(cls, set()) != lvls:
                print(f"\n### TABLE {cls} {sorted(lvls)}: '{name}' file says "
                      f"{sorted(availability[name].get(cls, set()))}"); fails += 1
    for name, avail in sorted(availability.items()):
        for cls, lvls in avail.items():
            if cls in tables and tables[cls].get(name, set()) != lvls:
                print(f"\n### FILE '{name}' claims {cls} {sorted(lvls)}, table says "
                      f"{sorted(tables[cls].get(name, set()))}"); fails += 1

    # ---- 4: count reconciliation --------------------------------------------
    t_lines = sum(1 for l in lines if l[2] and re.match(r'^\s*T:\s', l[2]))
    n_files = len(glob.glob(os.path.join(MA, "*.md"))) - 2      # _overview.md, INDEX.md
    print(f"\n==== {perfect}/{len(blocks)} abilities: token-for-token IDENTICAL (field text) ====")
    print(f"==== {avail_ok}/{len(blocks)} abilities: class availability correct ====")
    print(f"==== spell tables complete both ways: {', '.join(counts)} ====")
    print(f"==== count: {t_lines} T: lines - 1 format key = {t_lines-1}; "
          f"{len(blocks)} blocks; {n_files} files on disk ====")
    if t_lines - 1 != len(blocks) or n_files != len(blocks):
        print("### COUNT MISMATCH"); fails += 1
    print(f"==== {fails} failure(s) ====")
    return 1 if fails else 0

if __name__=="__main__":
    sys.exit(main())
