#!/usr/bin/env python3
"""Build the full-ruleset wiki corpus.

Every file under rules/ becomes a page. Headings inside the prose pages become anchors
AND link targets, so rules text can point at the exact clause it depends on. Cross-links
are applied to EVERY occurrence of a term (not just the first), guarded so the same target
is not re-linked within a short span."""
import re, os, json, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MA = os.path.join(ROOT, "rules/magic-and-abilities")
OUT = os.path.join(ROOT, "viewer", "wiki-data.json")

TERM_FILES = [("rules/magic-states-effects/states.md", "State"),
              ("rules/magic-states-effects/special-effects.md", "Special Effect"),
              ("rules/magic-states-effects/mechanics-and-definitions.md", "Mechanic")]
# a term file's parent page belongs in the same rail group as the terms it defines, not in
# Mechanics by default: "States Defined" is the page that explains what the States group is.
TERM_GROUP = {"State": "States", "Special Effect": "Special effects", "Mechanic": "Mechanics"}
SECTION_ORDER = ["Getting started", "Core rules", "Equipment", "Play", "Classes",
                 "Abilities", "States", "Special effects", "Mechanics", "Reference"]
PROSE_SECTION = {
  "introduction": "Getting started", "this-rulebook-made-easy": "Getting started",
  "amtgard-the-organization": "Getting started", "roleplaying-in-amtgard": "Getting started",
  "combat-rules": "Core rules", "armor": "Equipment", "weapons": "Equipment",
  "weapon-types-shields-equipment": "Equipment", "equipment-checking": "Equipment",
  "battlegames": "Play", "magic-items": "Play",
  "rules-revision-process": "Reference", "appendix-a-award-standards": "Reference",
  "appendix-b-kingdom-boundaries": "Reference", "amtgard-international-policies": "Reference",
}

# surface forms that are too generic or ambiguous to autolink at all.
# NOTE: equipment sections that ARE real rulebook headings (Melee, Shields, Bows, Arrows,
# Projectiles, Ammunition) are deliberately NOT here - a class equipment line must not mix
# linked and unlinked siblings. Only genuinely ambiguous words stay.
STOP = {"Ability", "Abilities", "Death", "Notes", "Overview", "Equipment", "Safety",
        "Classes", "States", "Special Effects", "Weapons", "Monster", "Peasant",
        "General Note", "Change Log", "Credits and Levels", "Quests",
        "Cloth", "Plate", "Trinkets", "Scenario Rules",
        # generic single-word headings whose capitalised form occurs in ordinary prose
        "General", "Heads", "Covers"}
# extra surface forms -> canonical name
INFLECT = {"Enchantment": "Enchantments", "Trait": "Traits", "Magic Ball": "Magic Balls",
           "Specialty Arrow": "Specialty Arrows", "Meta-Magics": "Meta-Magic",
           "Javelin": "Javelins", "Magic Staves": "Magic Staff", "Reeve": "Reeves",
           "Kingdom": "Kingdoms", "Park": "Parks",
           "Bow": "Bows", "Arrow": "Arrows", "Shield": "Shields"}

# hand-curated surface form -> (page id, anchor). Applied last, so these win over the
# automatic passes. They point the corpus's most-cited prose at the exact clause instead of
# the top of a chapter, and give the combat rules the inbound edges the autolinker cannot
# make (Death is too ambiguous to link from prose, but "Dead" and "dead players" are not).
CURATED = {
  "Strike-Legal":     ("page:weapons", "weapon-definitions"),
  "Stabbing Tip":     ("page:weapons", "weapon-definitions"),
  "Stabbing Tips":    ("page:weapons", "weapon-definitions"),
  "Double-Ended":     ("page:weapons", "weapon-definitions"),
  "Courtesy Padding": ("page:weapons", "weapon-definitions"),
  "Heavy Padding":    ("page:weapons", "weapon-definitions"),
  "Total Length":     ("page:weapons", "weapon-definitions"),
  "Armor Point":      ("page:armor", "armor-rating-and-safety"),
  "Armor Points":     ("page:armor", "armor-rating-and-safety"),
  "Armor Type":       ("page:armor", "armor-types-and-modifiers"),
  "Armor Types":      ("page:armor", "armor-types-and-modifiers"),
  "Hit Location":     ("page:combat-rules", "hit-locations"),
  "Hit Locations":    ("page:combat-rules", "hit-locations"),
  "Dead":             ("page:combat-rules", "death"),
  "dead players":     ("page:combat-rules", "death"),
  "wounded":          ("page:combat-rules", "inflicting-wounds"),
  "wounds":           ("page:combat-rules", "inflicting-wounds"),
  "unwielded":        ("page:combat-rules", "combat-notes"),
  # the only prose reference to the checking chapter anywhere in the book
  "checked for legality": ("page:equipment-checking", "checking-process"),
  "Weapon Type":      ("page:weapon-types-shields-equipment", None),
  "Weapon Types":     ("page:weapon-types-shields-equipment", None),
  # shield sizes: the sizes live in a numbered list, not a heading, so they have no
  # automatic target and "Medium" would otherwise resolve to the Monk archetype ability
  "Small":            ("page:weapon-types-shields-equipment", "shields"),
  "Large":            ("page:weapon-types-shields-equipment", "shields"),
  # "Shields" is a heading on two pages; construction rules beat the checking checklist
  "Shield":           ("page:weapon-types-shields-equipment", "shields"),
  "Shields":          ("page:weapon-types-shields-equipment", "shields"),
}
SHIELD_SIZE = ("Small", "Medium", "Large")      # "Medium" stays the Monk ability by default
SHIELD_TARGET = ("page:weapon-types-shields-equipment", "shields")
# a size word is a shield size when "shield" follows it closely, in the same sentence:
# "a Medium shield", "Small, Medium, or Large shield requirements"
SIZE_CTX = re.compile(r'[^.]{0,26}?shields?(?![\w-])', re.I)
# "1 Arrow / Unlimited" is a frequency notation, not a reference to the arrow rules
NUM_NOISE = {"Arrow", "Arrows"}

def read(p): return open(os.path.join(ROOT, p)).read()
def slugify(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    d = {}
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                d[k.strip()] = v.strip().strip('"')
    return d, (text[m.end():] if m else text)

def strip_note(b): return re.split(r'\n---\n\*Source:', b)[0].rstrip()

# ---- printed/PDF page interpolation ------------------------------------------------------
# A file that declares "printed_pages: 24-30" and is then split into 21 term pages must not
# hand all 21 the same seven-page range: the provenance rail is the artifact's verifiability
# claim, and "check pages 24-30" is not a check. Sections are split at fixed offsets in the
# body, so the offset maps linearly onto the declared span. Interpolated values are marked
# approx=True and the prov string says "~".
def parse_range(v):
    if not v: return None
    m = re.match(r'^\s*(\d+)\s*(?:[-\u2013]\s*(\d+))?\s*$', str(v))
    return (int(m.group(1)), int(m.group(2) or m.group(1))) if m else None

def interp(rng, a, b, total):
    """rng=(lo,hi) declared span; [a,b) = character offsets of the slice inside a `total`-
    character body. Returns (p0,p1) or None when there is nothing to narrow."""
    if not rng or total <= 0: return None
    lo, hi = rng
    n = hi - lo + 1
    if n <= 1: return None
    at = lambda off: lo + min(n - 1, max(0, int(off * n / total)))
    return (at(a), at(max(a, b - 1)))

def pagestr(t): return str(t[0]) if t[0] == t[1] else "%d-%d" % t

def prov(printed, pdf, approx):
    """Preformatted provenance line. 'p.' for one page, 'pp.' for a span, no page number at
    all for the unnumbered front-matter page, '~' when the value was interpolated."""
    tilde = "~" if approx else ""
    def half(label, v):
        if not v: return None
        r = parse_range(v)
        if not r: return "%s page %s" % (label, v)     # "unnumbered"
        return "%s %s%s %s" % (label, tilde, "p." if r[0] == r[1] else "pp.", v)
    parts = [x for x in (half("printed", printed), half("PDF", pdf)) if x]
    return " \u00b7 ".join(parts)

# the conversion inserted repo-navigation sentences that mean nothing in a viewer.
# Match the invariant part (the repo path / INDEX.md / "in this directory"), drop only the
# offending SENTENCE so trailing clauses on the same line survive, and substitute a
# viewer-appropriate sentence when the whole line was navigation.
REPO_NAV = re.compile(r'\.\./magic-and-abilities/|/rules/magic-and-abilities/|INDEX\.md'
                      r'|in this directory|its individual file')
VIEWER_SENT = "Every ability name links to its full definition."

def devnav(md):
    out = []
    for line in md.split("\n"):
        # table rows are rule content: their repo-relative links are resolved by the link
        # renderer, never rewritten as prose
        if line.lstrip().startswith("|") or not REPO_NAV.search(line):
            out.append(line); continue
        pre = re.match(r'^(\s*>\s?|\s*)', line).group(1)
        rest = line[len(pre):]
        # sentence boundary = a period followed by whitespace or end of line; periods inside
        # `../magic-and-abilities/` and `INDEX.md` are followed by non-space, so they don't split
        sents = re.split(r'(?<=\.)(?=\s|$)', rest)
        kept = [x for x in sents if not REPO_NAV.search(x)]
        body = "".join(kept).strip()
        out.append(pre + (body if body else VIEWER_SENT))
    return "\n".join(out)

LABEL_RE = re.compile(r'^\*\*([A-Za-z]+):\*\*')

def parse_fields(lines):
    """`**Label:** value` runs -> stat fields. Used by ability files AND by the identical
    stat blocks embedded in the martial class pages."""
    fields, i = [], 0
    while i < len(lines):
        m = re.match(r'^\*\*([A-Za-z]+):\*\*\s*(.*)$', lines[i].strip())
        if m and m.group(1) != "Available":
            label, val, items, tail, ordered = m.group(1), m.group(2), [], [], False
            j = i + 1
            while j < len(lines):
                s = lines[j].strip()
                if not s: j += 1; continue
                if LABEL_RE.match(s): break
                mi = re.match(r'^(\d+\.|-)\s+(.*)$', s)
                if mi:
                    ordered = ordered or mi.group(1)[0].isdigit(); items.append(mi.group(2))
                elif items: tail.append(s)
                else: val += " " + s
                j += 1
            fields.append(dict(label=label, value=val.strip(), items=items,
                               ordered=ordered, tail=" ".join(tail)))
            i = j
        else: i += 1
    return fields

RECORDS = {}   # id -> record
def rec(**kw):
    RECORDS[kw["id"]] = kw
    return kw

# ---------------------------------------------------------------- abilities
for path in sorted(glob.glob(os.path.join(MA, "*.md"))):
    base = os.path.basename(path)
    if base in ("_overview.md", "INDEX.md"): continue
    fm, body = frontmatter(open(path).read())
    body, name = strip_note(body), fm.get("title", "")
    fields = parse_fields(body.split("\n"))
    rec(id="ability:" + slugify(name), kind="ability", group="Abilities", title=name,
        fields=fields, avail=re.findall(r'"([^"]+)"', fm.get("class_availability", "[]")),
        pdf=fm.get("pdf_page"), printed=fm.get("printed_page"),
        file="rules/magic-and-abilities/" + base, headings=[])

# ---------------------------------------------------------------- term pages + their parents
for rel, kindlabel in TERM_FILES:
    fm, body = frontmatter(read(rel))
    body = strip_note(body)
    total = len(body)
    prng, drng = parse_range(fm.get("printed_pages")), parse_range(fm.get("pdf_pages"))
    heads = list(re.finditer(r'^### (.*)$', body, re.M))
    intro = body[:heads[0].start()].rstrip() if heads else body
    # parent page keeps the intro prose
    pid = "page:" + slugify(os.path.basename(rel)[:-3])
    ip, id_ = interp(prng, 0, heads[0].start() if heads else total, total), \
              interp(drng, 0, heads[0].start() if heads else total, total)
    rec(id=pid, kind="page", group=TERM_GROUP[kindlabel], title=fm.get("title", rel), md=intro,
        pdf=pagestr(id_) if id_ else fm.get("pdf_pages"),
        printed=pagestr(ip) if ip else fm.get("printed_pages"),
        approx=bool(ip or id_), file=rel, headings=[], children=[])
    for k, h in enumerate(heads):
        nm = h.group(1).strip()
        end = heads[k + 1].start() if k + 1 < len(heads) else total
        txt = body[h.end():end].strip()
        if not txt: continue
        tid = "term:" + slugify(nm)
        tp, td = interp(prng, h.start(), end, total), interp(drng, h.start(), end, total)
        rec(id=tid, kind="term", group=TERM_GROUP[kindlabel],
            subkind=kindlabel, title=nm, md=txt, parent=pid,
            pdf=pagestr(td) if td else fm.get("pdf_pages"),
            printed=pagestr(tp) if tp else fm.get("printed_pages"),
            approx=bool(tp or td), file=rel, headings=[])
        RECORDS[pid]["children"].append(tid)

# ---------------------------------------------------------------- classes
for path in sorted(glob.glob(os.path.join(ROOT, "rules/classes/*.md"))):
    base = os.path.basename(path)
    fm, body = frontmatter(open(path).read())
    body = strip_note(body)
    title = fm.get("title", base[:-3])
    rec(id=("class:" + base[:-3]) if base != "_overview.md" else "page:classes-overview",
        kind="class" if base != "_overview.md" else "page", group="Classes", title=title,
        md=body, pdf=fm.get("pdf_pages"), printed=fm.get("printed_pages"),
        file="rules/classes/" + base, headings=[])

# ---------------------------------------------------------------- prose pages
for path in sorted(glob.glob(os.path.join(ROOT, "rules/*.md"))):
    base = os.path.basename(path)
    fm, body = frontmatter(open(path).read())
    slug = base[:-3]
    rec(id="page:" + slug, kind="page", group=PROSE_SECTION.get(slug, "Reference"),
        title=fm.get("title", slug), md=strip_note(body),
        pdf=fm.get("pdf_pages") or fm.get("pdf_page"),
        printed=fm.get("printed_pages") or fm.get("printed_page"),
        file="rules/" + base, headings=[])

fm, body = frontmatter(open(os.path.join(MA, "_overview.md")).read())
rec(id="page:abilities-overview", kind="page", group="Abilities",
    title=fm.get("title", "Magic and Abilities \u2014 Overview"), md=strip_note(body),
    pdf=fm.get("pdf_pages"), printed=fm.get("printed_pages"),
    file="rules/magic-and-abilities/_overview.md", headings=[])

# ---------------------------------------------------------------- V8.7 change log -> own page
# The change log is 34 sub-headings covering every rules change in the release - the highest
# value apparatus in the book - buried at the bottom of a policies page and reachable only by
# scrolling past three unrelated policies. Split it out so it earns an index entry of its own.
# The text moves; it is not copied, so nothing is duplicated in search or backlinks.
_pol = RECORDS["page:amtgard-international-policies"]
_cut = re.search(r'^## Change Log\s*$', _pol["md"], re.M)
if _cut:
    _full, _tot = _pol["md"], len(_pol["md"])
    _pr, _pd = parse_range(_pol["printed"]), parse_range(_pol["pdf"])
    _a, _b = interp(_pr, 0, _cut.start(), _tot), interp(_pd, 0, _cut.start(), _tot)
    _pol["md"] = _full[:_cut.start()].rstrip()
    if _a: _pol["printed"] = pagestr(_a)
    if _b: _pol["pdf"] = pagestr(_b)
    _pol["approx"] = bool(_a or _b)
    _c, _d = interp(_pr, _cut.start(), _tot, _tot), interp(_pd, _cut.start(), _tot, _tot)
    rec(id="page:change-log", kind="page", group="Reference", title='V8.7 "Soupy" Change Log',
        md=_full[_cut.start():],
        printed=pagestr(_c) if _c else _pol["printed"], pdf=pagestr(_d) if _d else _pol["pdf"],
        approx=bool(_c or _d), file=_pol["file"], headings=[])
    STOP.add('V8.7 "Soupy" Change Log')

# ---------------------------------------------------------------- drop repo-navigation sentences
for r in RECORDS.values():
    if r.get("md"): r["md"] = devnav(r["md"])

# ---------------------------------------------------------------- headings -> anchors + aliases
ALIAS = {}          # surface form -> (page_id, anchor|None)
def alias(name, pid, anchor=None, force=False):
    # the length filter exists to keep incidental short words out of the heading-derived pass;
    # a canonical title ("Awe", "Spy") must never be dropped by it
    if name in STOP or len(name) < (3 if force else 4): return
    if name in ALIAS and not force: return
    ALIAS[name] = (pid, anchor)

for r in RECORDS.values():
    md = r.get("md")
    if not md: continue
    in_changelog = False
    for line in md.split("\n"):
        m = re.match(r'^(#{2,4})\s+(.*)$', line.strip())
        if not m: continue
        text = m.group(2).strip()
        if text == "Change Log": in_changelog = True
        r["headings"].append({"level": len(m.group(1)), "text": text, "slug": slugify(text)})
        if not in_changelog and r["kind"] == "page":
            alias(text, r["id"], slugify(text))

# page/term/class/ability titles win over section headings
for r in RECORDS.values():
    if r["kind"] in ("ability", "term", "class"):
        alias(r["title"], r["id"], force=True)
for r in RECORDS.values():
    if r["kind"] == "page":
        alias(r["title"], r["id"], force=True)
for surface, canon in INFLECT.items():
    if canon in ALIAS and surface not in ALIAS: ALIAS[surface] = ALIAS[canon]

CURATED_CLOBBER = {k: ALIAS[k] for k in CURATED if k in ALIAS}
for surface, target in CURATED.items():
    assert target[0] in RECORDS, surface
    ALIAS[surface] = target

NAMES = sorted(ALIAS, key=len, reverse=True)
LINK_RE = re.compile(r'(?<![\w-])(' + "|".join(re.escape(n) for n in NAMES) + r')(?![\w-])')

# ---------------------------------------------------------------- rendering
def esc(s): return html.escape(s, quote=False)

MARK = re.compile(r'^(\s*)(\d+\.|[a-z]\.|-)\s+(.*)$')

def autolink(text, self_id, state):
    """Link the first occurrence of each target in every block (paragraph, list item, table
    cell, stat field). Resetting at block boundaries is a rule a reader can see: no linked and
    unlinked copies of the same term a few words apart, and no link repeated inside a sentence."""
    if state.get("nolink"): return text
    out, pos = [], 0
    for m in LINK_RE.finditer(text):
        name = m.group(1)
        if name in NUM_NOISE and re.search(r'\d+\s*$', text[:m.start()]):
            continue                                   # "1 Arrow / Unlimited" is a frequency
        if name in SHIELD_SIZE and (state.get("ctx") == "shields"
                                    or SIZE_CTX.match(text[m.end():])):
            pid, anchor = SHIELD_TARGET                # a shield size, not the Monk archetype
        else:
            pid, anchor = ALIAS[name]
        if pid == self_id: continue
        key = pid + (anchor or "")
        if key in state["seen"]: continue
        state["seen"].add(key)
        href = pid + ("$" + anchor if anchor else "")
        state["links"].add(pid)
        out.append(text[pos:m.start()])
        out.append(f'<a class="xl" href="#{href}" data-id="{href}">{m.group(1)}</a>')
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)

# markdown [label](target); target restricted to path-shaped strings so bracketed prose
# such as "Name [Frequency] ([Category])" can never be mistaken for a link
MDLINK = re.compile(r'\[([^\]\n]+)\]\((\.{0,2}[\w./#-]*)\)')
BACKSLASH = re.compile(r'\\([\\`*_{}\[\]()#+\-.!<>|])')

def resolve_link(target):
    """repo-relative markdown target -> viewer route id, or None if it does not resolve."""
    t = target.strip().split("#")[0]
    if not t: return None
    stem = os.path.basename(t.rstrip("/"))
    if stem.endswith(".md"): stem = stem[:-3]
    if "magic-and-abilities" in t:
        if t.endswith("/") or stem in ("magic-and-abilities", "INDEX", "_overview"):
            return "page:abilities-overview"
        cand = "ability:" + slugify(stem)
    elif "classes" in t:
        cand = "page:classes-overview" if stem == "_overview" else "class:" + stem
    elif stem in ("INDEX",):
        return "page:abilities-overview"
    else:
        cand = "page:" + slugify(stem)
    return cand if cand in RECORDS else None

def mdlink(m, self_id, state):
    label, pid = m.group(1), resolve_link(m.group(2))
    if not pid or pid == self_id: return label          # never let a URL reach the page
    if state.get("nolink"): return label
    state["links"].add(pid)
    return f'<a class="xl" href="#{pid}" data-id="{pid}">{label}</a>'

# `**Field:**` is a label, not a reference: linking the word "School" in "**School:** Command"
# underlines the scaffolding and leaves the value inert. Bold that is not label-shaped
# (archetype names such as **Corruptor**) still autolinks normally.
BOLD_LABEL = re.compile(r'\*\*[^*]*:\*\*')
LEAD_LABEL = re.compile(r'^\*\*([A-Za-z][A-Za-z /-]*):\*\*')

def inline(s, self_id, state, link=True):
    s = BACKSLASH.sub(r'\1', s)                          # markdown escapes: \< -> <
    s = esc(s)
    s = re.sub(r'&lt;br\s*/?&gt;', '<br>', s)            # the one tag the source uses in cells
    s = re.sub(r'`([^`]+)`', lambda m: f'<code>{m.group(1)}</code>', s)
    s = MDLINK.sub(lambda m: mdlink(m, self_id, state), s)
    if link:
        state["seen"] = set()                            # one link per target per block
        lab = LEAD_LABEL.match(s)
        state["ctx"] = lab.group(1).strip().lower() if lab else None
        parts = re.split(r'(<code>.*?</code>|<a class="xl".*?</a>|\*\*[^*]*:\*\*)', s)
        s = "".join(p if (p.startswith(("<code>", '<a class="xl"')) or BOLD_LABEL.fullmatch(p))
                    else autolink(p, self_id, state) for p in parts)
        state["ctx"] = None
    return re.sub(r'\*\*([^*]+)\*\*', lambda m: f'<strong>{m.group(1)}</strong>', s)

def md_to_html(md, self_id, state):
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        s = lines[i].strip()
        if not s: i += 1; continue
        h = re.match(r'^(#{1,4})\s+(.*)$', s)
        if h:
            if len(h.group(1)) == 1: i += 1; continue
            # everything from "## Change Log" on is a summary of changes in the log's own
            # shorthand, not normative rules text: it must neither create links nor appear in
            # any other page's "Referenced by" list
            if h.group(2).strip() == "Change Log": state["nolink"] = True
            lvl = len(h.group(1))          # ## -> h2, ### -> h3, #### -> h4
            state["h"] = h.group(2).strip() # nearest preceding heading, for table captions
            out.append(f'<h{lvl} id="sec-{slugify(h.group(2))}">'
                       f'{inline(h.group(2), self_id, state, link=False)}</h{lvl}>')
            i += 1; continue
        if s.startswith("|"):
            rows, j = [], i
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append([c.strip() for c in lines[j].strip().strip("|").split("|")]); j += 1
            body = [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            hdr = [c.strip() for c in rows[0]]
            th = "".join(f"<th>{inline(c, self_id, state, link=False)}</th>" for c in hdr)
            trs = "".join("<tr>" + "".join(f"<td>{cell(c, hdr[k] if k < len(hdr) else '', self_id, state)}</td>"
                                           for k, c in enumerate(r)) + "</tr>" for r in body)
            # a table needs an accessible name of its own: in table-navigation mode the heading
            # above it is not announced. The caption is visually hidden because the heading is
            # already on screen; the wrapper is focusable so a keyboard-only reader can scroll it.
            name = state.get("h") or state.get("title") or "Table"
            cap = f'<caption class="vh">{inline(name, self_id, state, link=False)}</caption>'
            out.append(f'<div class="tw" role="group" tabindex="0" aria-label="{html.escape(name)}, table">'
                       f'<table>{cap}<thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')
            i = j; continue
        if s.startswith(">"):
            buf, j = [], i
            while j < len(lines) and lines[j].strip().startswith(">"):
                buf.append(re.sub(r'^\s*>\s?', '', lines[j])); j += 1
            while buf and not buf[0].strip(): buf.pop(0)
            cls, lab = "", ""
            if buf:
                # "Made Easy", "Classes Made Easy", ... - keep the source's own phrase as label
                m6 = re.match(r'^\*\*([A-Za-z ]*Made Easy)\*\*', buf[0].strip())
                if m6:
                    cls = ' class="made"'
                    lab = f'<span class="mlabel">{esc(m6.group(1))}</span>'
                    rest0 = buf[0].strip()[m6.end():].strip()
                    if rest0: buf[0] = rest0
                    else: buf.pop(0)
            # recurse so paragraphs, lists and bold labels inside the callout survive
            inner = md_to_html("\n".join(buf), self_id, state)
            out.append(f'<blockquote{cls}>{lab}{inner}</blockquote>')
            i = j; continue
        if re.match(r'^(\d+\.|-)\s', s):
            j, stack = i, []
            while j < len(lines):
                m2 = MARK.match(lines[j])
                if not m2:
                    # a wrapped continuation line belongs to the item above it
                    if stack and lines[j][:1] in (" ", "\t") and lines[j].strip():
                        ind, mark, txt = stack[-1]
                        stack[-1] = (ind, mark, txt + " " + lines[j].strip()); j += 1; continue
                    break
                ind, mark = len(m2.group(1)), m2.group(2)
                # a lettered marker is only a list item when it is indented under one
                if mark[0].isalpha() and mark != "-" and ind == 0: break
                stack.append((ind, mark, m2.group(3))); j += 1
            base = min(x[0] for x in stack)
            ordered = stack[0][1][0].isdigit()
            buf, sub = [], None
            for ind, mark, txt in stack:
                if ind > base:
                    if sub is None:
                        sub = '<ol type="a">' if mark[0].isalpha() and mark != "-" else "<ul>"
                        buf.append(sub)
                    buf.append(f'<li>{inline(txt, self_id, state)}</li>')
                else:
                    if sub is not None:
                        buf.append(("</ol>" if sub.startswith("<ol") else "</ul>") + "</li>"); sub = None
                    elif buf: buf.append("</li>")
                    buf.append(f'<li>{inline(txt, self_id, state)}')
            if sub is not None: buf.append(("</ol>" if sub.startswith("<ol") else "</ul>") + "</li>")
            elif buf: buf.append("</li>")
            tag = "ol" if ordered else "ul"
            out.append(f'<{tag}>{"".join(buf)}</{tag}>')
            i = j; continue
        if LABEL_RE.match(s):
            # the martial class pages carry the same **Type:**/**School:**/... stat blocks as
            # the ability files; render them with the identical dl.stat/.field markup
            j = i
            while j < len(lines) and lines[j].strip() and \
                  not re.match(r'^(#|\||>)', lines[j].strip()):
                j += 1
            blk = lines[i:j]
            if sum(1 for x in blk if LABEL_RE.match(x.strip())) >= 2:
                out.append(render_fields(parse_fields(blk), self_id, state))
                i = j; continue
        buf, j = [], i
        while j < len(lines) and lines[j].strip() and \
              not re.match(r'^\s*(#|\||>|-\s|\d+\.\s)', lines[j].strip()):
            buf.append(lines[j].strip()); j += 1
        out.append(f'<p>{inline(" ".join(buf), self_id, state)}</p>')
        i = j
    return "".join(out)

# stat-block labels are the one place a reader can ask "what IS a School / a Range?" - give
# them the definition. These are navigation chrome, so they deliberately do NOT register as
# references: 180 identical edges would drown the real backlinks on the term pages.
# only the dl.stat group: linking one label out of the .field group (Incantation but not
# Materials/Effect/Limitations) would be exactly the half-linked label group this pass exists
# to remove
STAT_LABEL_LINK = {"Type": "page:abilities-overview$abilities-format-key",
                   "School": "term:school", "Range": "term:range"}
SCHOOLS = ("Command", "Death", "Flame", "Neutral", "Protection", "Sorcery", "Spirit", "Subdual")
SCHOOL_RE = re.compile(r'(?<![\w-])(' + "|".join(SCHOOLS) + r')(?![\w-])')

def schip(v):
    """The eight school colours already exist as theme tokens and are used on exactly one 6px
    dot. A class spell list is six tables of sixty rows; colouring the School column turns
    'find the Death spells' from a linear read into a glance."""
    return ('<span class="schip"><span class="dot" data-school="%s"></span>%s</span>'
            % (v.lower(), esc(v)))

def cell(c, header, self_id, state):
    if header == "School" and c.strip() in SCHOOLS: return schip(c.strip())
    return inline(c, self_id, state)

def label_html(label):
    t = STAT_LABEL_LINK.get(label)
    return f'<a class="xl" href="#{t}" data-id="{t}">{label}</a>' if t else label

def school_html(v):
    """The eight school names get a target only inside a School field, so the Death school
    never collides with the death rules in ordinary prose."""
    if "<a " in v: return v
    return SCHOOL_RE.sub(lambda m: '<a class="xl" href="#term:school" data-id="term:school">'
                                   f'{m.group(1)}</a>', v)

def render_fields(fields, self_id, state):
    stat = [f for f in fields if f["label"] in ("Type", "School", "Range")]
    rest = [f for f in fields if f["label"] not in ("Type", "School", "Range")]
    out = []
    if stat:
        out.append('<dl class="stat">')
        for f in stat:
            v = inline(f["value"], self_id, state)
            if f["label"] == "School" and self_id != "term:school": v = school_html(v)
            out.append(f'<dt>{label_html(f["label"])}</dt><dd>{v}</dd>')
        out.append("</dl>")
    for f in rest:
        before = set(state["links"])
        out.append(f'<div class="field"><span class="flabel">{label_html(f["label"])}</span><div class="fval">'
                   f'<p>{inline(f["value"], self_id, state)}</p>')
        if f["items"]:
            tag = "ol" if f["ordered"] else "ul"
            out.append(f'<{tag}>' + "".join(f'<li>{inline(x, self_id, state)}</li>'
                                            for x in f["items"]) + f'</{tag}>')
        if f["tail"]: out.append(f'<p>{inline(f["tail"], self_id, state)}</p>')
        out.append("</div></div>")
        # which field named a term decides how a state page files the backlink: a term named in
        # an Effect is INFLICTED by that ability; anywhere else it is merely mentioned.
        state.setdefault("fieldlinks", {}).setdefault(f["label"], set()).update(
            set(state["links"]) - before)
    return "".join(out)

def render_ability(r, state):
    return render_fields(r["fields"], r["id"], state)

# ---------------------------------------------------------------- purchase economics (cost/max/frequency)
# "What does a Wizard 4 pay for Fireball and how often does it refresh?" is the commonest
# mid-game question, and the numbers live only in the class tables. Join them onto the ability.
ORD = {"1st": 1, "2nd": 2, "3rd": 3, "4th": 4, "5th": 5, "6th": 6}
ABILITY_TITLES = sorted({r["title"] for r in RECORDS.values() if r["kind"] == "ability"},
                        key=len, reverse=True)
ABILITY_SET = set(ABILITY_TITLES)
PICK_RE = re.compile(r'^(?:Optional\s*[\u2013\u2014-]\s*)?Pick\s[^:]*:\s*', re.I)

def demark(s):
    """table/list cell -> plain ability notation: markdown links, bold and code stripped."""
    s = MDLINK.sub(lambda m: m.group(1), s)
    return re.sub(r'\*\*|\*|`', '', s).strip()

def split_entries(cell_text):
    return [x.strip() for x in re.split(r'<br\s*/?>|;', cell_text) if x.strip()]

def match_ability(entry):
    """'Harden (Self) 1/Life (ex)' -> ('Harden', '(Self) 1/Life (ex)'). The remainder is the
    book's own notation, kept verbatim."""
    e = PICK_RE.sub("", demark(entry)).strip()
    if not e or e.endswith(":"): return None
    for t in ABILITY_TITLES:
        if e == t or e.startswith(t + " ") or e.startswith(t + " -"):
            freq = re.sub(r'^[-\u2013]\s*', '', e[len(t):].strip()).strip()
            # "Destruction Arrow, Poison Arrow, Pinning Arrow" is a choice of three abilities,
            # not one ability with a frequency: refuse rather than invent a notation.
            if freq.startswith(","): return None
            return t, freq
    return None

PURCHASE = {}
def add_purchase(name, cls, level, cost, mx, freq):
    if name not in ABILITY_SET or not level: return
    row = dict(cls=cls, level=level, cost=cost, max=mx, frequency=freq or None)
    rows = PURCHASE.setdefault(name, [])
    if row not in rows: rows.append(row)

for _c in [x for x in RECORDS.values() if x["kind"] == "class"]:
    lines, level, in_prog = _c["md"].split("\n"), None, False
    hdr = None
    # Look The Part grants an ability at first level; the ability's own "Available to" line
    # counts it, so without this the two halves of the page disagree.
    for k, ln in enumerate(lines):
        lt = re.match(r'^\s*-?\s*\*\*Look The Part:\*\*\s*(.*)$', ln)
        if not lt: continue
        ents, k2 = split_entries(lt.group(1)), k + 1
        while k2 < len(lines) and lines[k2].strip() and lines[k2][:1] in (" ", "\t"):
            ents.append(re.sub(r'^\s*-\s*', '', lines[k2])); k2 += 1
        for e in ents:
            got = match_ability(e)
            if got:
                add_purchase(got[0], _c["title"], 1, None, None,
                             ("Look The Part: " + got[1]) if got[1] else "Look The Part")
        break
    for ln in lines:
        s = ln.strip()
        m = re.match(r'^(#{2,4})\s+(.*)$', s)
        if m:
            t = m.group(2).strip()
            in_prog = in_prog or t in ("Level Progression", "Spell List")
            if t == "Abilities" and len(m.group(1)) == 2: in_prog = False
            lm = re.match(r'^(\d(?:st|nd|rd|th))\s+Level$', t)
            if lm: level = ORD.get(lm.group(1))
            hdr = None
            continue
        if not in_prog: continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells): continue
            if hdr is None and ("Name" in cells or "Level" in cells): hdr = cells; continue
            if hdr and "Name" in hdr:                       # magic-user spell table
                d = dict(zip(hdr, cells))
                nm = demark(d.get("Name", ""))
                add_purchase(nm, _c["title"], level, d.get("Cost"), d.get("Max"),
                             d.get("Frequency"))
            elif hdr:                                       # Level | Ability progression table
                if cells[0] and cells[0] in ORD: level = ORD[cells[0]]
                for e in split_entries(cells[1] if len(cells) > 1 else ""):
                    got = match_ability(e)
                    if got: add_purchase(got[0], _c["title"], level, None, None, got[1])
            continue
        lm = re.match(r'^-\s+\*\*(\d(?:st|nd|rd|th))\*\*\s*$', s)
        if lm: level = ORD[lm.group(1)]; continue
        lm = re.search(r'\bAt\s+(\d(?:st|nd|rd|th))\s+level\b', s)
        if lm: level = ORD[lm.group(1)]
        if re.match(r'^[-*]\s+', s):
            got = match_ability(re.sub(r'^[-*]\s+', '', s))
            if got: add_purchase(got[0], _c["title"], level, None, None, got[1])

# Archetypes grant abilities in a prose Effect sentence ("Gain Martyr (Other) 2/Life Charge x3
# (ex)."), never in a table, so Martyr, Momentum and Sacred Blades had no economics at all and a
# further ten listed a class under "Available to" with no matching row. The grant sentence carries
# the book's own frequency notation verbatim; the archetype that confers it is named, because the
# ability is not purchasable without it.
SECHEAD_RE = re.compile(r'^###\s+(.*)$', re.M)
ARCH_TYPE_RE = re.compile(r'^\*\*Type:\*\*\s*Archetype\s*$', re.M)
GRANT_RE = re.compile(r'\bGain\s+(.+)$')
SEP_RE = re.compile(r',\s*(?:and\s+)?|\s+and\s+')
# an ability title may itself contain a separator ("Blood and Thunder", "Equipment: Shield,
# Medium"); hide those before splitting the grant list so they survive intact
AMBIG_TITLES = [t for t in ABILITY_TITLES if SEP_RE.search(t)]

def grant_entries(sentence):
    m = GRANT_RE.search(sentence)
    if not m: return []
    s = m.group(1).rstrip(".")
    for k, t in enumerate(AMBIG_TITLES): s = s.replace(t, "\x00%d\x00" % k)
    parts = SEP_RE.split(s)
    return [re.sub(r'\x00(\d+)\x00', lambda mm: AMBIG_TITLES[int(mm.group(1))], p)
            for p in parts if p and p.strip()]

for _c in [x for x in RECORDS.values() if x["kind"] == "class"]:
    secs = list(SECHEAD_RE.finditer(_c["md"]))
    for k, h in enumerate(secs):
        nm = h.group(1).strip()
        blk = _c["md"][h.end():secs[k + 1].start() if k + 1 < len(secs) else len(_c["md"])]
        if not ARCH_TYPE_RE.search(blk): continue
        # the level is the one the class table already records for the archetype itself
        lvl = next((x["level"] for x in PURCHASE.get(nm, []) if x["cls"] == _c["title"]), None)
        if not lvl: continue
        eff = next((f["value"] for f in parse_fields(blk.split("\n")) if f["label"] == "Effect"), "")
        for sent in re.split(r'(?<=\.)\s+', eff):
            for ent in grant_entries(sent):
                got = match_ability(ent)
                if got:
                    add_purchase(got[0], _c["title"], lvl, None, None,
                                 nm + (": " + got[1] if got[1] else ""))

for r in RECORDS.values():
    if r["kind"] == "ability":
        r["purchase"] = sorted(PURCHASE.get(r["title"], []),
                               key=lambda x: (x["cls"], x["level"]))

pages, back = [], {}
for r in RECORDS.values():
    state = {"seen": set(), "links": set(), "title": r["title"]}
    r["_html"] = render_ability(r, state) if r["kind"] == "ability" else md_to_html(r["md"], r["id"], state)
    r["_links"] = sorted(state["links"])
    r["_nlinks"] = r["_html"].count('class="xl"')
    r["_efflinks"] = state.get("fieldlinks", {}).get("Effect", set())

# a class also links every ability that lists it
for r in RECORDS.values():
    if r["kind"] == "class":
        extra = [a["id"] for a in RECORDS.values()
                 if a["kind"] == "ability" and any(x.rsplit(" ", 1)[0] == r["title"] for x in a["avail"])]
        r["_links"] = sorted(set(r["_links"]) | set(extra))
for r in RECORDS.values():
    for o in r["_links"]:
        if o != r["id"]: back.setdefault(o, set()).add(r["id"])

# ---------------------------------------------------------------- faceted abilities index
# Every facet a reader wants (class+level, school, type) is already in the payload but only
# ever shown as a chip on a page you have already found. The overview page - 1.3kB of format
# key - becomes the way in. Index links carry `class="xl ix"`: styled like any cross-link, not
# counted as prose links (nlinks matches the literal class="xl"), and CSS-targetable via .ix.
ORDSUF = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}

def ability_index():
    abil = sorted([r for r in RECORDS.values() if r["kind"] == "ability"], key=lambda a: a["title"])
    def ln(pid, label):
        return f'<a class="xl ix" href="#{pid}" data-id="{pid}">{esc(label)}</a>'
    def row(label, items, anchor=None):
        head = ln(anchor, label) if anchor else f"<b>{esc(label)}</b>"
        return f'<li>{head} <span class="ixn">{len(items)}</span> ' + \
               ", ".join(ln(a["id"], a["title"]) for a in items) + "</li>"
    out, heads = [], []

    heads.append("Abilities by class and level")
    out.append('<h2 id="sec-abilities-by-class-and-level">Abilities by class and level</h2>'
               '<div class="facet facet-class">')
    for c in sorted([r for r in RECORDS.values() if r["kind"] == "class"], key=lambda x: x["title"]):
        lis = []
        for lv in range(1, 7):
            got = [a for a in abil
                   if any(x.rsplit(" ", 1)[0] == c["title"] and x.rsplit(" ", 1)[-1] == str(lv)
                          for x in a["avail"])]
            if got: lis.append(row(ORDSUF[lv], got))
        if lis:
            out.append(f'<div class="fgrp"><h3>{ln(c["id"], c["title"])}</h3>'
                       f'<ul class="flist">{"".join(lis)}</ul></div>')
    out.append("</div>")

    for title, key, order in (("Abilities by school", "school", SCHOOLS),
                              ("Abilities by type", "atype", ())):
        buckets = {}
        for a in abil:
            v = next((f["value"] for f in a["fields"] if f["label"] == ("School" if key == "school" else "Type")), None)
            buckets.setdefault(v or "Not specified", []).append(a)
        keys = [k for k in order if k in buckets] + sorted(k for k in buckets if k not in order)
        heads.append(title)
        out.append(f'<h2 id="sec-{slugify(title)}">{esc(title)}</h2>'
                   f'<div class="facet facet-{key}"><ul class="flist">'
                   + "".join(row(k, buckets[k]) for k in keys) + "</ul></div>")
    return "".join(out), heads

_ov = RECORDS.get("page:abilities-overview")
if _ov:
    _ix, _hs = ability_index()
    _ov["_html"] += _ix
    for _t in _hs: _ov["headings"].append({"level": 2, "text": _t, "slug": slugify(_t)})

# a state/special-effect page's backlinks answer two different questions. Split them: an
# ability whose *Effect* names the term is what INFLICTS it; everything else merely mentions it.
def split_backlinks(r, bl):
    if r["kind"] != "term" or r.get("subkind") not in ("State", "Special Effect"):
        return [], list(bl)
    inf = [b for b in bl if r["id"] in RECORDS[b].get("_efflinks", ())]
    return inf, [b for b in bl if b not in set(inf)]

# search corpus: rendered HTML with tags stripped, entities decoded, whitespace collapsed and
# lowercased. Searching p.html matches "class"/"href" on almost every page and can never match
# a phrase an inline <a> splits in half.
INLINE_TAG = re.compile(r'</?(?:a|span|strong|em|b|i|u|code|sup|sub|small|abbr)(?:\s[^>]*)?>')
def detag(h):
    """Inline tags close up (so "<a>Kingdom</a>'s" stays one word and a phrase an <a> splits
    is still findable); block tags become a space so cells and paragraphs do not run together."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', INLINE_TAG.sub('', h)))).strip()

def plaintext(h): return detag(h).lower()

for r in RECORDS.values():
    bl = sorted(back.get(r["id"], []))
    inf, men = split_backlinks(r, bl)
    pages.append(dict(
        id=r["id"], kind=r["kind"], subkind=r.get("subkind"), group=r["group"], title=r["title"],
        html=r["_html"], text=plaintext(r["_html"]),
        links=[l for l in r["_links"] if l != r["id"]],
        backlinks=bl, inflictedBy=inf, mentionedBy=men, nlinks=r["_nlinks"],
        avail=r.get("avail", []), parent=r.get("parent"), children=r.get("children", []),
        purchase=r.get("purchase", []),
        headings=[h for h in r["headings"] if h["level"] <= 4],
        school=next((f["value"] for f in r.get("fields", []) if f["label"] == "School"), None),
        atype=next((f["value"] for f in r.get("fields", []) if f["label"] == "Type"), None),
        pdf=r.get("pdf"), printed=r.get("printed"), approx=bool(r.get("approx")),
        prov=prov(r.get("printed"), r.get("pdf"), bool(r.get("approx"))), file=r["file"]))

# a section's own introduction leads its group; it does not sort alphabetically among the
# pages it introduces ("Classes - Overview" belongs above Bard, not between Bard and Druid).
def lead(p): return 0 if p["id"].endswith("-overview") or p["children"] else 1
pages.sort(key=lambda p: (SECTION_ORDER.index(p["group"]) if p["group"] in SECTION_ORDER else 99,
                          lead(p), p["title"]))

# render invariants: no markdown/source-repo syntax may survive into a rendered page
for p in pages:
    for bad in ("](", "magic-and-abilities/", "INDEX.md", "&lt;br", "\\<", "\\>"):
        assert bad not in p["html"], (p["id"], bad)

# ---------------------------------------------------------------- link audit (stdout only)
def audit():
    """The conversion hand-authored 50 verified links in the class tables. Treat them as
    ground truth and check the heuristic autolinker against them; also check that every
    curated anchor exists on the page it points at."""
    print("-- audit: curated anchors")
    bad = [(s, t) for s, t in CURATED.items()
           if t[1] and t[1] not in [h["slug"] for h in RECORDS[t[0]]["headings"]]]
    assert not bad, bad
    print("   %d curated aliases, all anchors resolve" % len(CURATED))
    if CURATED_CLOBBER:
        print("   overrode automatic aliases:",
              ", ".join(f"{k} ({v[0]}{'$'+v[1] if v[1] else ''})"
                        for k, v in sorted(CURATED_CLOBBER.items())))
    print("-- audit: hand-authored source links vs autolinker")
    total = miss = wrong = partial = 0
    for r in sorted(RECORDS.values(), key=lambda x: x["id"]):
        if not r.get("md"): continue
        srclinks = [(m.group(1), m.group(2)) for m in MDLINK.finditer(r["md"])]
        if not srclinks: continue
        unresolved = [t for lbl, t in srclinks if not resolve_link(t)]
        assert not unresolved, (r["id"], unresolved)
        m_, w_, p_ = [], [], []
        for lbl, t in srclinks:
            total += 1
            want = resolve_link(t)
            got = ALIAS.get(lbl)
            if got is None: m_.append(lbl)
            elif got[0] != want: w_.append(f"{lbl} -> {got[0]} (source says {want})")
            # and would the autolinker really wrap the whole label, or would a longer alias
            # swallow part of it?
            out = autolink(lbl, "", {"seen": set(), "links": set()})
            if out != f'<a class="xl" href="#{want}" data-id="{want}">{lbl}</a>':
                p_.append(f"{lbl} => {out}")
        miss += len(m_); wrong += len(w_); partial += len(p_)
        print(f"   {r['id']}: {len(srclinks)} source links, "
              f"{len(m_)} not in alias table, {len(w_)} disagree, {len(p_)} render differently")
        if m_: print("     autolinker would miss:", ", ".join(m_))
        if w_: print("     disagreement:", "; ".join(w_))
        for x in p_: print("     renders as:", x)
    print(f"   TOTAL {total} ground-truth links: {miss} missing, {wrong} mistargeted, "
          f"{partial} rendered differently")
    # The hand-authored links in the source markdown are ground truth. If the autolinker
    # disagrees with one, that is a real defect in the alias table, not a warning to scroll
    # past - fail the build rather than shipping a link that points somewhere the editor
    # of the conversion did not intend.
    if wrong:
        raise SystemExit(f"FAIL: autolinker mistargets {wrong} hand-authored link(s); "
                         f"see 'disagreement:' lines above")
audit()

# ---------------------------------------------------------------- fidelity verification
# Counts cannot see dropped or garbled text. This pass compares the rendered corpus back
# against the source markdown word for word, and checks the structural promises the viewer
# relies on. stdout only - it changes no page - but it exits non-zero on any failure.
WORD = re.compile(r"[a-z0-9]+(?:['\u2019][a-z0-9]+)*")
CAPTION_RE = re.compile(r'<caption class="vh">.*?</caption>')
GENERATED_RE = re.compile(r'<h2 id="sec-abilities-by-class-and-level">.*$', re.S)
VOID = {"br", "hr", "img", "input", "meta", "link"}

def wordbag(s):
    from collections import Counter
    return Counter(WORD.findall(s.lower()))

def source_words(path):
    """The source file reduced to the words the renderer is supposed to carry through."""
    fm, body = frontmatter(read(path))
    body = devnav(strip_note(body))
    body = BACKSLASH.sub(r'\1', body)
    body = MDLINK.sub(lambda m: m.group(1), body)            # keep labels, drop targets
    body = re.sub(r'^#\s+.*$', '', body, flags=re.M)         # the H1 repeats the page title
    body = re.sub(r'^\s*(?:-\s*)?\*\*Available to:\*\*.*$', '', body, flags=re.M)
    body = re.sub(r'<br\s*/?>', ' ', body)
    # list markers become <ol>/<ul> structure; the marker glyph is not body text. A lettered
    # marker only counts when it is indented under one - at column 0 the renderer keeps it as
    # prose (the change log's "a. Typo ... fixes" lines), so the check must keep it too.
    body = re.sub(r'^(?:[ \t]*>[ \t]?)*[ \t]*(?:\d+\.|-)[ \t]+', '', body, flags=re.M)
    body = re.sub(r'^(?:[ \t]*>[ \t]?)*[ \t]+(?:[a-z]|[ivx]{1,4})\.[ \t]+', '', body, flags=re.M)
    return wordbag(body), fm

def page_words(p):
    h = p["html"]
    if p["id"] == "page:abilities-overview": h = GENERATED_RE.sub("", h)   # built, not sourced
    h = CAPTION_RE.sub("", h)                                             # a11y chrome
    return wordbag(detag(h))

def verify():
    fails = []
    # (b) no markdown or source-repo residue survived into a rendered page
    for p in pages:
        for tok in ("](", "magic-and-abilities/", "INDEX.md", "&lt;br", "\\<", "\\>", "**", "`"):
            if tok in p["html"]: fails.append("residue %r in %s" % (tok, p["id"]))
    # (c) ids unique per page, exported headings anchored, every $anchor href resolves,
    #     and the emitted HTML is tag-balanced
    secs = {p["id"]: set(re.findall(r'\sid="(sec-[^"]+)"', p["html"])) for p in pages}
    for p in pages:
        got = re.findall(r'\sid="([^"]+)"', p["html"])
        dup = {x for x in got if got.count(x) > 1}
        if dup: fails.append("duplicate id(s) %s on %s" % (sorted(dup), p["id"]))
        for h in p["headings"]:
            if "sec-" + h["slug"] not in secs[p["id"]]:
                fails.append("heading %r has no anchor on %s" % (h["text"], p["id"]))
        for href in re.findall(r'href="#([^"]+)"', p["html"]):
            tid, _, anc = href.partition("$")
            if tid not in secs: fails.append("dead link %s from %s" % (href, p["id"]))
            elif anc and "sec-" + anc not in secs[tid]:
                fails.append("dead anchor %s from %s" % (href, p["id"]))
        stack = []
        for m in re.finditer(r'<(/?)([a-z0-9]+)[^>]*?(/?)>', p["html"]):
            if m.group(2) in VOID or m.group(3): continue
            if m.group(1):
                if not stack or stack.pop() != m.group(2):
                    fails.append("unbalanced </%s> on %s" % (m.group(2), p["id"])); break
            else: stack.append(m.group(2))
        else:
            if stack: fails.append("unclosed %s on %s" % (stack, p["id"]))
    # (a) word-for-word: every source file against the pages built from it
    bysrc = {}
    for p in pages: bysrc.setdefault(p["file"], []).append(p)
    lost = gained = 0
    for path, ps in sorted(bysrc.items()):
        src, _ = source_words(path)
        # a term page's title IS its "### " heading in the source; the heading became the page
        # title and so is not repeated in the body
        for p in ps:
            if p["kind"] == "term": src.subtract(wordbag(p["title"]))
        src = +src
        ren = sum((page_words(p) for p in ps), wordbag(""))
        missing = {w: n for w, n in (src - ren).items()}
        extra = {w: n for w, n in (ren - src).items()}
        if missing:
            lost += sum(missing.values())
            fails.append("%s: %d source word(s) not rendered: %s"
                         % (path, sum(missing.values()), sorted(missing.items())[:8]))
        if extra:
            gained += sum(extra.values())
            fails.append("%s: %d rendered word(s) absent from source: %s"
                         % (path, sum(extra.values()), sorted(extra.items())[:8]))
    # (d) advisory only: the purchase join is data, not text, so no word check can see it break.
    # A class/level pair that an ability's frontmatter claims but no class table confirms is a
    # discrepancy in the SOURCE, not in the build - report it, never fail on it.
    nofreq = [p["id"] for p in pages if p["kind"] == "ability" and not p["purchase"]]
    disagree = ["%s: frontmatter says %s, class tables say %s" %
                (p["title"], x, sorted({"%s %d" % (r["cls"], r["level"]) for r in p["purchase"]
                                        if r["cls"] == x.rsplit(" ", 1)[0]}) or "nothing")
                for p in pages if p["kind"] == "ability" for x in p["avail"]
                if not any(r["cls"] == x.rsplit(" ", 1)[0] and str(r["level"]) == x.rsplit(" ", 1)[-1]
                           for r in p["purchase"])]
    print("-- verify: purchase join: %d/%d abilities priced, %d avail pair(s) unconfirmed"
          % (sum(1 for p in pages if p["kind"] == "ability" and p["purchase"]),
             sum(1 for p in pages if p["kind"] == "ability"), len(disagree)))
    for x in nofreq: print("    no purchase row at all:", x)
    for x in disagree: print("    source disagrees:", x)
    print("-- verify: %d files, %d pages, %d words lost, %d words invented"
          % (len(bysrc), len(pages), lost, gained))
    if fails:
        print("-- VERIFY FAILED (%d):" % len(fails))
        for f in fails[:40]: print("   ", f)
        raise SystemExit(1)
    print("   residue clean, ids unique, anchors resolve, tags balanced, text verbatim")
verify()

json.dump({"pages": pages, "groupOrder": SECTION_ORDER},
          open(OUT, "w"), separators=(",", ":"))

g = {}
for p in pages: g[p["group"]] = g.get(p["group"], 0) + 1
print("pages:", len(pages), g)
print("alias targets:", len(ALIAS))
print("total inline links:", sum(p["nlinks"] for p in pages))
print("bytes:", os.path.getsize(OUT))
print("most-linked:", sorted(((len(p["backlinks"]), p["title"]) for p in pages), reverse=True)[:8])
