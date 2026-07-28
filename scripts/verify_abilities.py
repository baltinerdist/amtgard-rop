#!/usr/bin/env python3
"""Verify the 180 generated ability files are token-for-token faithful to the source
PDF text. For each ability: take the raw source block (its T:/S:/R:/I:/M:/E:/L:/N: field
text) and compare, token by token, against the concatenation of the rendered field VALUES
in the md file. Any mismatch => the parser dropped/altered/merged content. Reports every
non-equal token run so it can be inspected."""
import importlib.util, re, os, glob, difflib, unicodedata

spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__),"gen_abilities.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
MA = os.path.join(g.ROOT, "rules/magic-and-abilities")

TOK = re.compile(r"[a-z0-9][a-z0-9/.'%\"-]*")
def toks(s):
    s = g.norm(s).lower()
    return TOK.findall(s)

def source_body_tokens(block):
    """tokens of the field text (strip the single-letter field labels only)."""
    text = "\n".join(block["body"])
    text = re.sub(r'\b([TSRIMELN]):\s', ' ', text)     # drop field-label markers
    text = text.replace("- ", " ")                       # bullet markers in L: lists
    return toks(text)

def md_value_tokens(block):
    fields = g.parse_fields(block["body"])               # same parser the generator uses
    return toks(" ".join(v for _,v in fields))

def main():
    lines = g.extract_lines()
    blocks, _ = g.find_blocks(lines)
    total_issues = 0
    perfect = 0
    for b in blocks:
        src = source_body_tokens(b)
        # read the ACTUAL written md file and pull field values from it (end-to-end check)
        path = os.path.join(MA, g.slug(b["name"])+".md")
        if not os.path.exists(path):
            print(f"[MISSING FILE] {b['name']} -> {path}"); total_issues+=1; continue
        md = open(path).read()
        # field values = lines like **Label:** value  (skip 'Available to')
        vals=[]
        for m in re.finditer(r'^\*\*([A-Za-z]+):\*\*\s(.*)$', md, re.M):
            if m.group(1)=="Available": continue
            vals.append(m.group(2))
        mdtok = toks(" ".join(vals))
        sm = difflib.SequenceMatcher(a=src, b=mdtok, autojunk=False)
        diffs=[]
        for op,i1,i2,j1,j2 in sm.get_opcodes():
            if op=='equal': continue
            diffs.append((op, src[i1:i2], mdtok[j1:j2]))
        if diffs:
            total_issues+=1
            print(f"\n### {b['name']}  (source p{b['page']})")
            for op,s,m2 in diffs:
                print(f"   {op:7s} source={s}  md={m2}")
        else:
            perfect+=1
    print(f"\n==== {perfect}/{len(blocks)} abilities: token-for-token IDENTICAL (field text) ====")
    print(f"==== {total_issues} abilities with any discrepancy ====")

if __name__=="__main__":
    main()
