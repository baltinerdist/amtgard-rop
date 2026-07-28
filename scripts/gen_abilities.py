#!/usr/bin/env python3
"""Deterministically split the Amtgard 'Magic and Abilities' section (PDF pp 62-78)
into one verbatim markdown file per ability. Uses column-cropped pdftotext output so
two-column reading order is exact. Dry-run by default; pass --write to emit files."""
import re, subprocess, sys, os, unicodedata

PDF = "/Users/averykrouse/Downloads/Amtgard Rules of Play.pdf"
ROOT = "/Users/averykrouse/GitHub/amtgard-rop"
OUT = os.path.join(ROOT, "rules/magic-and-abilities")
PAGES = range(62, 79)  # PDF pages 62..78 inclusive

CLASS = {"Ap":"Anti-Paladin","Ar":"Archer","As":"Assassin","Bn":"Barbarian",
         "Bd":"Bard","Dr":"Druid","He":"Healer","Mk":"Monk","Pa":"Paladin",
         "Sc":"Scout","Wa":"Warrior","Wi":"Wizard"}
CODE = r'(?:Ap|Ar|As|Bn|Bd|Dr|He|Mk|Pa|Sc|Wa|Wi)\s+[1-6]'
CODES_ONLY = re.compile(r'^\s*(?:'+CODE+r')(?:\s*,\s*'+CODE+r')*\s*,?\s*$')
CODE_TOKEN = re.compile(r'\b('+ '|'.join(CLASS) + r')\s+([1-6])\b')
FURNITURE = re.compile(r'^\s*(Amtgard 8\b.*|07-26-2025|\d{1,3})\s*$')
FIELD = re.compile(r'\b([TSRIMELN]):\s')

def extract_lines():
    lines = []
    for p in PAGES:
        for x0 in (0, 306):
            out = subprocess.run(
                ["pdftotext","-layout","-x",str(x0),"-y","0","-W","306","-H","792",
                 "-f",str(p),"-l",str(p),PDF,"-"],
                capture_output=True, text=True).stdout
            for ln in out.split("\n"):
                if ln.strip() == "\x0c" or ln == "\x0c": continue
                ln = ln.replace("\x0c","")
                if FURNITURE.match(ln): continue
                lines.append((p, ln.rstrip()))
    return lines

def is_field(l):     return bool(re.match(r'^\s*[TSRIMELN]:\s', l)) or l.strip().startswith("- ")
def has_code_tail(l):return bool(re.search(r'(?:'+CODE+r')\s*,?\s*$', l)) and not is_field(l)

def _name_index(lines, ti):
    """Given a T: line index, return (name_line_index, wrapped_code_tail)."""
    j = ti - 1
    while j >= 0 and not lines[j][1].strip():
        j -= 1
    code_tail = ""
    if j >= 0 and CODES_ONLY.match(lines[j][1]):  # class codes wrapped onto their own line
        code_tail = " " + lines[j][1].strip()
        j -= 1
        while j >= 0 and not lines[j][1].strip():
            j -= 1
    return j, code_tail

def find_blocks(lines):
    # anchor on T: lines; exclude the format-key line 'T: Type S: School' on p62
    t_idx = [i for i,(_,l) in enumerate(lines)
             if re.match(r'^\s*T:\s', l) and "S: School" not in l]
    names = [_name_index(lines, ti) for ti in t_idx]          # (name_idx, code_tail) per ability
    # allow 1+ space before the trailing class-code run; tolerate a trailing comma
    code_re = re.compile(r'\s+((?:'+CODE+r')(?:\s*,\s*'+CODE+r')*)\s*,?\s*$')
    blocks = []
    for k, ti in enumerate(t_idx):
        name_idx, code_tail = names[k]
        page, raw = lines[name_idx]
        header = raw.strip() + code_tail
        m = code_re.search(header)
        if m:
            codes = m.group(1).strip().rstrip(',').strip()
            name = header[:m.start()].strip()
        else:
            codes, name = "", header.strip()
        # body runs from this T: line up to the NEXT ability's name line (trims header bleed)
        end = names[k+1][0] if k+1 < len(names) else len(lines)
        body = [l for (_,l) in lines[ti:end]]
        while body and not body[-1].strip(): body.pop()
        blocks.append(dict(name=name, codes=codes, page=page, body=body))
    return blocks, (names[0][0] if names else len(lines))

def parse_fields(body):
    """body includes the T: line first. Return ordered [(label,text)]."""
    text = "\n".join(body)
    # normalize: split into field chunks on inline labels
    # first join wrapped lines: a line not starting with a field label continues previous
    fields = []
    cur_label, cur_val = None, []
    LAB = {"T":"Type","S":"School","R":"Range","I":"Incantation",
           "M":"Materials","E":"Effect","L":"Limitations","N":"Note"}
    for raw in body:
        # tolerate a stray leading punctuation glitch before a field label, e.g. ".    E: ..."
        m0 = re.match(r'^\s*[.,;:]+\s+([TSRIMELN]:\s.*)$', raw)
        if m0: raw = m0.group(1)
        s = raw.strip()
        if not s:
            if cur_label: cur_val.append("")
            continue
        # a line may contain multiple inline labels (T: .. S: .. R: ..)
        parts = list(FIELD.finditer(raw))
        if parts and re.match(r'^\s*[TSRIMELN]:\s', raw):
            # split this line by labels
            idxs = [pp.start() for pp in parts] + [len(raw)]
            labs = [pp.group(1) for pp in parts]
            for n,lab in enumerate(labs):
                seg = raw[idxs[n]:idxs[n+1]]
                seg = re.sub(r'^\s*[TSRIMELN]:\s*','',seg).strip()
                if cur_label: fields.append((cur_label, " ".join(x for x in cur_val).strip()))
                cur_label, cur_val = lab, [seg]
        else:
            cur_val.append(s)
    if cur_label: fields.append((cur_label, " ".join(x for x in cur_val).strip()))
    return [(LAB[l], v) for l,v in fields]

def norm(s):
    return (s.replace("“",'"').replace("”",'"')
             .replace("‘","'").replace("’","'"))

def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii","ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+","-", s).strip("-").lower()
    return s

def render(b):
    fields = parse_fields(b["body"])
    avail = [f"{CLASS[c]} {lvl}" for c,lvl in CODE_TOKEN.findall(b["codes"])]
    fm = ["---",
          f'title: "{norm(b["name"])}"',
          "section: Magic and Abilities",
          f'pdf_page: {b["page"]}',
          f'printed_page: {b["page"]-3}',
          f'class_availability: [{", ".join(chr(34)+a+chr(34) for a in avail)}]',
          'rulebook_version: V8.7 "Soupy"',
          "rulebook_date: 2025-07-26",
          "source: Amtgard Rules of Play Version 8",
          "---",""]
    out = fm + [f'# {norm(b["name"])}', ""]
    if avail:
        out += [f'**Available to:** {", ".join(avail)}', ""]
    for lab,val in fields:
        out.append(f'**{lab}:** {norm(val)}')
        out.append("")
    out += ["---",
            f'*Source: Amtgard Rules of Play V8.7, Magic and Abilities, PDF p. {b["page"]} '
            f'(printed p. {b["page"]-3}). Verbatim.*',""]
    return "\n".join(out)

def render_overview(lines, first_name_idx):
    body = [l for (_,l) in lines[:first_name_idx]]
    while body and not body[0].strip(): body.pop(0)
    while body and not body[-1].strip(): body.pop()
    text = "\n".join(l.strip() for l in body if l.strip())
    fm = ["---","title: Magic and Abilities — Overview","section: Magic and Abilities",
          "pdf_pages: 62","printed_pages: 59",'rulebook_version: V8.7 "Soupy"',
          "rulebook_date: 2025-07-26","source: Amtgard Rules of Play Version 8","---","",
          "# Magic and Abilities — Overview",""]
    return "\n".join(fm) + text + "\n\n> **Note:** Individual abilities are in one file each in this directory.\n"

def main():
    write = "--write" in sys.argv
    lines = extract_lines()
    blocks, first_name_idx = find_blocks(lines)
    print(f"Total ability blocks (== T: anchors): {len(blocks)}")
    # anomaly checks
    bad = [b for b in blocks if not b["name"] or CODES_ONLY.match(b["name"]) or len(b["name"])>40]
    dupes = {}
    for b in blocks: dupes.setdefault(slug(b["name"]),[]).append(b["name"])
    dup = {k:v for k,v in dupes.items() if len(v)>1}
    print(f"Suspicious names: {len(bad)} -> {[b['name'] for b in bad]}")
    print(f"Duplicate slugs: {dup}")
    if not write:
        print("\n--- SAMPLE: first 2 rendered files ---\n")
        for b in blocks[:2]:
            print(f"### FILE: {slug(b['name'])}.md")
            print(render(b)); print()
        # print just the name list for review
        print("--- ALL NAMES ("+str(len(blocks))+") ---")
        print(", ".join(b["name"] for b in blocks))
        return
    os.makedirs(OUT, exist_ok=True)
    n=0
    for b in blocks:
        with open(os.path.join(OUT, slug(b["name"])+".md"),"w") as f:
            f.write(render(b)); n+=1
    with open(os.path.join(OUT,"_overview.md"),"w") as f:
        f.write(render_overview(lines, first_name_idx))
    print(f"WROTE {n} ability files + _overview.md to {OUT}")

if __name__=="__main__":
    main()
