#!/usr/bin/env python3
"""Deterministically split the Amtgard 'Magic and Abilities' section (PDF pp 62-78)
into one verbatim markdown file per ability. Uses column-cropped pdftotext output so
two-column reading order is exact. Dry-run by default; pass --write to emit files."""
import re, subprocess, sys, os, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, "Amtgard Rules of Play.pdf")
OUT = os.path.join(ROOT, "rules/magic-and-abilities")
PAGES = range(62, 79)  # PDF pages 62..78 inclusive

CLASS = {"Ap":"Anti-Paladin","Ar":"Archer","As":"Assassin","Bn":"Barbarian",
         "Bd":"Bard","Dr":"Druid","He":"Healer","Mk":"Monk","Pa":"Paladin",
         "Sc":"Scout","Wa":"Warrior","Wi":"Wizard"}
CODE = r'(?:Ap|Ar|As|Bn|Bd|Dr|He|Mk|Pa|Sc|Wa|Wi)\s+[1-6]'
CODES_ONLY = re.compile(r'^\s*(?:'+CODE+r')(?:\s*,\s*'+CODE+r')*\s*,?\s*$')
CODE_TOKEN = re.compile(r'\b('+ '|'.join(CLASS) + r')\s+([1-6])\b')
FURNITURE = re.compile(r'^\s*(Amtgard 8\b.*|07-26-2025|\d{1,3})\s*$')
# a field label is "X:" followed by a space OR immediately by its value (source has "N:If ...")
FIELD = re.compile(r'\b([TSRIMELN]):(?:\s|(?=[A-Z"“]))')

def extract_lines():
    """Return [(page, column_x, text)] in true reading order: each page's left column
    top-to-bottom, then its right column.

    Page furniture (running header, date stamp, page number) is kept as a text=None
    marker rather than dropped. It has to stay: a running header interrupts a column
    mid-sentence and leaves blank lines on both sides, which is indistinguishable from
    a real layout gap once the header line itself is gone. _body_end needs to tell those
    apart. Every other consumer skips None."""
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
                lines.append((p, x0, None if FURNITURE.match(ln) else ln.rstrip()))
    return lines

def is_field(l):     return bool(re.match(r'^\s*[TSRIMELN]:', l)) or l.strip().startswith("- ")
def has_code_tail(l):return bool(re.search(r'(?:'+CODE+r')\s*,?\s*$', l)) and not is_field(l)

def _blank(lines, j):
    return lines[j][2] is None or not lines[j][2].strip()

def _name_index(lines, ti):
    """Given a T: line index, return (name_line_index, wrapped_code_tail)."""
    j = ti - 1
    while j >= 0 and _blank(lines, j):
        j -= 1
    code_tail = ""
    if j >= 0 and CODES_ONLY.match(lines[j][2]):  # class codes wrapped onto their own line
        code_tail = " " + lines[j][2].strip()
        j -= 1
        while j >= 0 and _blank(lines, j):
            j -= 1
    return j, code_tail

def _body_end(lines, ti, hard_end):
    """Where this ability's stat block really stops, at or before `hard_end`.

    The book sets in-world flavor vignettes and 'Did you Know?' sidebars in the page-foot
    frame. pdftotext emits them as ordinary text after the last stat block in the column,
    so a naive block boundary swallows them into the final field. Two structural cuts,
    each verified against the source to fire only on genuine spillover:

      1. **Column cut** — a stat block is typeset inside one column and never continues
         into another. Any line whose (page, column) differs from the T: line's belongs to
         a different frame. (Exactly one ability in the section trips this: the p.73
         'Discovering Answers' vignette that opens the right column after Rogue.)
      2. **Gap cut** — a run of >=2 blank lines followed by more text means the layout
         put a separate frame below the block. The catch: a running header or date stamp
         also interrupts a column, leaving blank lines on both sides of itself, and that
         gap is NOT a block boundary — the sentence resumes right after it. So a blank
         run that ends at a furniture marker is a page break to skip, and only a blank
         run that ends at real text is a cut.
    """
    home = (lines[ti][0], lines[ti][1])
    run_start = None
    for i in range(ti, hard_end):
        page, col, text = lines[i]
        if (page, col) != home:                 # cut 1: left the column
            return i
        if text is None:                        # furniture: the gap was a page break
            run_start = None
            continue
        if not text.strip():
            if run_start is None: run_start = i
            continue
        if run_start is not None and i - run_start >= 2:
            return run_start                    # cut 2: a separate frame starts here
        run_start = None
    return hard_end

def find_blocks(lines):
    # anchor on T: lines; exclude the format-key line 'T: Type S: School' on p62
    t_idx = [i for i,l in enumerate(lines)
             if l[2] is not None and re.match(r'^\s*T:\s', l[2]) and "S: School" not in l[2]]
    names = [_name_index(lines, ti) for ti in t_idx]          # (name_idx, code_tail) per ability
    # allow 1+ space before the trailing class-code run; tolerate a trailing comma
    code_re = re.compile(r'\s+((?:'+CODE+r')(?:\s*,\s*'+CODE+r')*)\s*,?\s*$')
    blocks = []
    for k, ti in enumerate(t_idx):
        name_idx, code_tail = names[k]
        page, _col, raw = lines[name_idx][0], lines[name_idx][1], lines[name_idx][2]
        header = raw.strip() + code_tail
        m = code_re.search(header)
        if m:
            codes = m.group(1).strip().rstrip(',').strip()
            name = header[:m.start()].strip()
        else:
            codes, name = "", header.strip()
        # body runs from this T: line up to the NEXT ability's name line (trims header
        # bleed), then back off any page-foot flavor the layout put below the block
        hard_end = names[k+1][0] if k+1 < len(names) else len(lines)
        end = _body_end(lines, ti, hard_end)
        body = [l[2] for l in lines[ti:end] if l[2] is not None]
        while body and not body[-1].strip(): body.pop()
        blocks.append(dict(name=name, codes=codes, page=page, body=body))
    return blocks, (names[0][0] if names else len(lines))

def parse_fields(body):
    """body includes the T: line first. Return ordered [(label, [lines])] — the value is
    kept as its source lines so the renderer can rebuild lists that the PDF set as
    indented items. Use flatten() for a single-string value."""
    fields = []
    cur_label, cur_val = None, []
    LAB = {"T":"Type","S":"School","R":"Range","I":"Incantation",
           "M":"Materials","E":"Effect","L":"Limitations","N":"Note"}
    for raw in body:
        # tolerate a stray leading punctuation glitch before a field label, e.g. ".    E: ..."
        m0 = re.match(r'^\s*[.,;:]+\s+([TSRIMELN]:.*)$', raw)
        if m0: raw = m0.group(1)
        s = raw.strip()
        if not s:
            continue
        # a line may contain multiple inline labels (T: .. S: .. R: ..)
        parts = list(FIELD.finditer(raw))
        if parts and re.match(r'^\s*[TSRIMELN]:', raw):
            # split this line by labels
            idxs = [pp.start() for pp in parts] + [len(raw)]
            labs = [pp.group(1) for pp in parts]
            for n,lab in enumerate(labs):
                seg = raw[idxs[n]:idxs[n+1]]
                seg = re.sub(r'^\s*[TSRIMELN]:\s*','',seg).strip()
                if cur_label: fields.append((cur_label, cur_val))
                cur_label, cur_val = lab, [seg]
        else:
            # keep leading whitespace: split_items reads the source indentation to tell a
            # list item's wrapped lines from a flush sentence that follows the list
            cur_val.append(raw.rstrip())
    if cur_label: fields.append((cur_label, cur_val))
    return [(LAB[l], v) for l,v in fields]

def flatten(vlines):
    """Join a field's source lines back into one string.

    The PDF wraps mid-token: a line ending in '-' or '/' continues without a space
    ('Meta-' + 'Magics', '3/' + 'Refresh'). Everything else joins with one space, and
    runs of whitespace left by column breaks collapse."""
    out = ""
    for seg in vlines:
        seg = seg.strip()
        if not seg: continue
        if out and not out.endswith(("-", "/")):
            out += " "
        out += seg
    return re.sub(r'\s{2,}', ' ', out).strip()

_NUM_ITEM = re.compile(r'^\d+\.\s')
def split_items(vlines):
    """Return (lead_in, [items], tail) if the field holds a list the PDF set as indented
    items, else (None, None, None). Items are numbered ('1.', '2.', ...) or bulleted
    ('-'), and are recognised from the SOURCE line starts, not from the joined text."""
    starts = [i for i, s in enumerate(vlines)
              if _NUM_ITEM.match(s.strip()) or re.match(r'^-\s*\S', s.strip())]
    if len(starts) < 2:
        return None, None, None
    numbered = bool(_NUM_ITEM.match(vlines[starts[0]].strip()))
    if numbered:
        nums = [int(re.match(r'^(\d+)\.', vlines[i].strip()).group(1)) for i in starts]
        if nums != list(range(1, len(nums)+1)):     # must be a real 1..n run
            return None, None, None
    lead = flatten(vlines[:starts[0]])
    if not lead.endswith(":"):                      # a list always follows a "…:" lead-in
        return None, None, None
    items, tail = [], ""
    for n, i in enumerate(starts):
        stop = starts[n+1] if n+1 < len(starts) else len(vlines)
        chunk = list(vlines[i:stop])
        chunk[0] = re.sub(r'^\s*(?:\d+\.|-)\s*', '', chunk[0])
        # a trailing sentence that is not part of the last item (it is set flush, not indented)
        if n == len(starts)-1:
            ind = len(vlines[i]) - len(vlines[i].lstrip())
            for m2 in range(1, len(chunk)):
                src = vlines[i+m2]
                if len(src) - len(src.lstrip()) < ind:
                    tail = flatten(vlines[i+m2:stop]); chunk = chunk[:m2]; break
        items.append(flatten(chunk))
    return lead, items, tail

def norm(s):
    return (s.replace("“",'"').replace("”",'"')
             .replace("‘","'").replace("’","'"))

def esc(s):
    """Code-span the book's literal <Player> / <armor location> placeholders so markdown
    renderers do not swallow them as HTML tags."""
    return re.sub(r'<([A-Za-z][A-Za-z ]*)>', r'`<\1>`', s)

def slug(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii","ignore").decode()
    s = re.sub(r"[^A-Za-z0-9]+","-", s).strip("-").lower()
    return s

def render_field(label, vlines):
    lead, items, tail = split_items(vlines)
    if items is None:
        return [f'**{label}:** {esc(norm(flatten(vlines)))}', ""]
    numbered = bool(_NUM_ITEM.match(vlines[0].strip())) or any(
        _NUM_ITEM.match(s.strip()) for s in vlines)
    out = [f'**{label}:** {esc(norm(lead))}', ""]
    for n, it in enumerate(items, 1):
        out.append(f'{n}. {esc(norm(it))}' if numbered else f'- {esc(norm(it))}')
    out.append("")
    if tail:
        out += [esc(norm(tail)), ""]
    return out

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
        out += render_field(lab, val)
    out += ["---",
            f'*Source: Amtgard Rules of Play V8.7, printed p. {b["page"]-3} '
            f'(PDF p. {b["page"]}). Flavor text omitted.*',""]
    return "\n".join(out)

def render_overview(lines, first_name_idx):
    """The section intro (PDF p.62): a lead paragraph, then two side-by-side boxes
    ('Abilities Format Key' and 'Classes and Levels'). The gutter puts both box headings
    on one extracted line, so split them and re-flow the wrapped prose."""
    body = [l[2] for l in lines[:first_name_idx] if l[2] and l[2].strip()]
    # drop the section title repeated as body text under the H1
    if body and body[0].strip() == "Magic and Abilities": body.pop(0)
    intro, key = [], []
    for l in body:
        s = l.strip()
        if re.match(r'^Abilities Format Key', s):
            key.append("SPLIT"); continue
        (key if key else intro).append(s)
    key = [k for k in key if k != "SPLIT"]
    fm = ["---",'title: Magic and Abilities — Overview',"section: Magic and Abilities",
          "pdf_pages: 62","printed_pages: 59",'rulebook_version: V8.7 "Soupy"',
          "rulebook_date: 2025-07-26","source: Amtgard Rules of Play Version 8","---","",
          "# Magic and Abilities — Overview",""]
    out = fm + [norm(flatten(intro)), "", "## Abilities Format Key", ""]
    for k in key:
        # the first key line packs three entries: "T: Type S: School R: Range (if any)"
        for entry in re.split(r'\s+(?=[TSRIMELN]:\s)', k.strip()):
            m = re.match(r'^([TSRIMELN]):\s*(.+)$', entry)
            if m:
                out.append(f'- **{m.group(1)}:** {norm(m.group(2).strip())}')
    out += ["", "## Classes and Levels", "",
            "Each ability's class availability and level are printed to the right of its "
            "name in the source; here they are carried in each file's `class_availability` "
            "frontmatter and its **Available to:** line.", "",
            "> **Note:** Individual abilities are in one file each in this directory. "
            "See [`INDEX.md`](INDEX.md) for the full list.", "",
            "---",
            "*Source: Amtgard Rules of Play V8.7, printed p. 59 (PDF p. 62). "
            "Flavor text omitted.*", ""]
    return "\n".join(out)

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
