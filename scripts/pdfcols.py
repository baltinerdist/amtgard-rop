#!/usr/bin/env python3
"""Two-column-aware page extraction.

The rulebook is typeset with mirrored (recto/verso) margins, so the gutter between the two
text columns is NOT at a fixed x: V8.7 happened to split cleanly at x=306, but in V8.08
odd pages put the right column at x~296 and even pages at x~320, with class-code tails on the
left column's header lines running past x=306. A fixed crop therefore either chops a word
("Warlock" -> "Wa" | "rlock") or drops a class code ("Bd" | "1").

`gutter(pdf, page)` finds the widest word-free vertical band in the middle of the page.
`columns(pdf, page)` returns (left_text, right_text), each cropped at that gutter.
CLI: pdfcols.py [--pdf PATH] FIRST [LAST]  -> left col then right col, page by page.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_PDF = os.path.join(ROOT, "Amtgard Rules of Play.pdf")
_WORD = re.compile(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">')

def _words(pdf, page):
    out = subprocess.run(["pdftotext", "-bbox", "-f", str(page), "-l", str(page), pdf, "-"],
                         capture_output=True, text=True).stdout
    return [tuple(map(float, m.groups())) for m in _WORD.finditer(out)]

_cache = {}
def gutter(pdf, page, lo=240.0, hi=372.0):
    """x at the middle of the widest vertical band in [lo, hi] that no word overlaps."""
    key = (pdf, page)
    if key in _cache: return _cache[key]
    spans = sorted((x0, x1) for x0, _, x1, _ in _words(pdf, page) if x1 > lo and x0 < hi)
    best, cur = (0.0, 306.0), lo
    for x0, x1 in spans:
        if x0 - cur > best[0]: best = (x0 - cur, (x0 + cur) / 2)
        cur = max(cur, x1)
    if hi - cur > best[0]: best = (hi - cur, (hi + cur) / 2)
    _cache[key] = best[1]
    return best[1]

def _crop(pdf, page, x0, w):
    return subprocess.run(["pdftotext", "-layout", "-x", str(int(x0)), "-y", "0", "-W", str(int(w)),
                           "-H", "792", "-f", str(page), "-l", str(page), pdf, "-"],
                          capture_output=True, text=True).stdout

def columns(pdf, page):
    g = gutter(pdf, page)
    return _crop(pdf, page, 0, g), _crop(pdf, page, g, 612 - g)

if __name__ == "__main__":
    a = sys.argv[1:]; pdf = DEFAULT_PDF
    if a and a[0] == "--pdf": pdf, a = a[1], a[2:]
    first = int(a[0]); last = int(a[1]) if len(a) > 1 else first
    for p in range(first, last + 1):
        l, r = columns(pdf, p)
        print(f"===== PDF p{p} (gutter x={gutter(pdf, p):.0f}) — LEFT column =====\n{l}\n===== PDF p{p} — RIGHT column =====\n{r}")
