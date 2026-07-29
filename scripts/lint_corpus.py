#!/usr/bin/env python3
"""Structural lint for the converted corpus. Asserts the conventions in STYLE.md that are
cheap to check and easy to drift on:

  - every file under rules/ has complete YAML frontmatter
  - frontmatter title matches the file's H1
  - printed page(s) == PDF page(s) - 3   (front matter, which has no printed number, is exempt)
  - every file ends with a `---` rule followed by a one-line source note
  - the source note's page numbers agree with the frontmatter
  - single-page notes use "p." not "pp." and never a degenerate range ("pp. 1-1")
  - every markdown link inside rules/ and README.md resolves to a file that exists
  - no PDF page carrying rules content is left unclaimed

Exit status is non-zero if anything fails.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ["title", "section", "rulebook_version", "rulebook_date", "source"]
# PDF pages deliberately not converted: cover, TOC/credits/copyright, the printed Index
SKIP_PAGES = {1, 3, 87}
LAST_PAGE = 96

def frontmatter(text):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m: return None
    d = {}
    for line in m.group(1).split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip()] = v.strip().strip('"')
    return d

def pages(val):
    """'16-21' -> [16..21]; '62' -> [62]; non-numeric (front matter) -> []"""
    val = val.strip()
    if not re.match(r'^\d+(-\d+)?$', val): return []
    a, _, b = val.partition("-")
    return list(range(int(a), int(b or a) + 1))

def main():
    fails = []
    claimed = {}
    files = sorted(glob.glob(os.path.join(ROOT, "rules/**/*.md"), recursive=True))
    for path in files:
        rel = os.path.relpath(path, ROOT)
        text = open(path).read()
        fm = frontmatter(text)
        if fm is None:
            fails.append(f"{rel}: no YAML frontmatter"); continue
        for k in REQUIRED:
            if k not in fm: fails.append(f"{rel}: frontmatter missing '{k}'")

        h1 = re.search(r'^#\s+(.+)$', text, re.M)
        if not h1:
            fails.append(f"{rel}: no H1")
        elif fm.get("title", "").strip() != h1.group(1).strip():
            fails.append(f"{rel}: title {fm.get('title')!r} != H1 {h1.group(1)!r}")

        pdf = fm.get("pdf_pages") or fm.get("pdf_page") or ""
        printed = fm.get("printed_pages") or fm.get("printed_page") or ""
        pdf_l, pr_l = pages(pdf), pages(printed)
        if not pdf_l:
            fails.append(f"{rel}: no usable pdf page(s) ({pdf!r})")
        if pr_l and [p - 3 for p in pdf_l] != pr_l:
            fails.append(f"{rel}: printed {printed!r} != pdf {pdf!r} - 3")
        for p in pdf_l:
            claimed.setdefault(p, []).append(rel)

        note = re.search(r'\n---\n(\*Source: .+\*)\s*$', text)
        if not note:
            fails.append(f"{rel}: missing trailing '---' + source note")
        else:
            n = note.group(1)
            if re.search(r'pp\. (\d+)[-–]\1\b', n):
                fails.append(f"{rel}: degenerate range in source note: {n}")
            m = re.search(r'PDF (pp?)\. (\d+)(?:[-–](\d+))?', n)
            if not m:
                fails.append(f"{rel}: source note names no PDF page: {n}")
            elif pdf_l:
                lo, hi = int(m.group(2)), int(m.group(3) or m.group(2))
                if [lo, hi] != [pdf_l[0], pdf_l[-1]]:
                    fails.append(f"{rel}: source note PDF pp. {lo}-{hi} "
                                 f"!= frontmatter {pdf_l[0]}-{pdf_l[-1]}")
                single = len(pdf_l) == 1
                if single and m.group(1) == "pp":
                    fails.append(f"{rel}: single-page file uses 'pp.': {n}")
                if not single and m.group(1) == "p":
                    fails.append(f"{rel}: multi-page file uses 'p.': {n}")

    # link resolution
    for path in files + [os.path.join(ROOT, "README.md")]:
        rel = os.path.relpath(path, ROOT)
        base = os.path.dirname(path)
        for m in re.finditer(r'\[[^\]]*\]\(([^)#]+)\)', open(path).read()):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")): continue
            root = ROOT if rel == "README.md" else base
            if not os.path.exists(os.path.join(root, target)):
                fails.append(f"{rel}: broken link -> {target}")

    # page coverage
    for p in range(1, LAST_PAGE + 1):
        if p in SKIP_PAGES: continue
        if p not in claimed:
            fails.append(f"PDF p.{p}: not claimed by any file")

    print(f"checked {len(files)} files under rules/ + README.md")
    print(f"PDF pages claimed: {len(claimed)} (deliberately skipped: {sorted(SKIP_PAGES)})")
    for f in fails: print("  FAIL", f)
    print(f"==== {len(fails)} problem(s) ====")
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
