#!/usr/bin/env python3
"""Multiset (bag) source-vs-markdown verifier for the LLM-converted prose/class files.
Order- and table-independent: extracts full-page source text (tables stay intact),
normalizes both to token bags, and reports:
  - coverage = fraction of source content tokens present in the md
  - OMITTED spans: maximal runs of consecutive source tokens absent from the md
      (these are flavor text [expected] OR real dropped rules [must fix])
  - EXTRA tokens: md tokens absent from the source
      (markdown headings we added [expected] OR hallucinated content [must fix])
Usage: verify_prose.py [file.md ...]  (defaults to all non-ability converted files)
"""
import re, sys, os, glob, subprocess
from collections import Counter
ROOT="/Users/averykrouse/GitHub/amtgard-rop"
PDF="/Users/averykrouse/Downloads/Amtgard Rules of Play.pdf"
FURN=re.compile(r'^\s*(Amtgard 8\b.*|07-26-2025|\d{1,3})\s*$')
TOK=re.compile(r"[a-z0-9][a-z0-9/.'%\"-]*")
# words we deliberately add as structure/boilerplate (won't be in source) -> ignore as EXTRA
STRUCT={'available','to','source','flavor','text','omitted','verbatim','made','easy',
        'spell','list','level','progression','abilities','equipment','overview','note',
        'type','school','range','incantation','materials','effect','limitations',
        'printed','pdf','pp','p','section','full','definitions','live','in'}

def norm(s):
    return (s.replace("“",'"').replace("”",'"').replace("‘","'").replace("’","'").lower())

def src_tokens(pages):
    out=[]
    for p in pages:
        t=subprocess.run(["pdftotext","-layout","-f",str(p),"-l",str(p),PDF,"-"],
                         capture_output=True,text=True).stdout
        for ln in t.split("\n"):
            if FURN.match(ln): continue
            out.append(ln)
    return TOK.findall(norm("\n".join(out)))

def md_tokens(path):
    t=open(path).read()
    t=re.sub(r'^---\n.*?\n---\n','',t,flags=re.S)
    t=re.sub(r'^\*Source:.*$','',t,flags=re.M)
    t=re.sub(r'`[^`]*`','',t)
    t=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',t)
    return TOK.findall(norm(t))

def pages_of(path):
    m=re.search(r'pdf_pages?:\s*([0-9]+)(?:\s*-\s*([0-9]+))?',open(path).read())
    if not m: return []
    a=int(m.group(1)); b=int(m.group(2)) if m.group(2) else a
    return list(range(a,b+1))

def review(path):
    pages=pages_of(path)
    if not pages: print(f"!! no pdf_pages in {path}"); return
    s=src_tokens(pages); m=md_tokens(path)
    sc=Counter(s); mc=Counter(m)
    missing=sc-mc                     # source tokens not covered by md (by count)
    extra=mc-sc                       # md tokens not in source
    covered=sum((sc&mc).values())
    cov=covered/max(1,sum(sc.values()))
    # localize omitted spans: runs of consecutive source tokens that are (still) missing
    missbag=Counter(missing)
    spans=[]; cur=[]
    for tok in s:
        if missbag.get(tok,0)>0:
            cur.append(tok); missbag[tok]-=1
        else:
            if len(cur)>=3: spans.append(cur)
            cur=[]
    if len(cur)>=3: spans.append(cur)
    extra_content=[(t,c) for t,c in extra.items() if t not in STRUCT and len(t)>2]
    print(f"\n{'='*80}\n{os.path.relpath(path,ROOT)}  (src pp {pages[0]}-{pages[-1]}; "
          f"{sum(sc.values())} src tok; coverage {cov:.3f})")
    print(f"  omitted spans(>=3): {len(spans)} | distinct extra content tokens: {len(extra_content)}")
    for sp in spans:
        tag="  -OMITTED"
        print(f"{tag}({len(sp)})  {' '.join(sp)[:240]!r}")
    if extra_content:
        ex=sorted(extra_content,key=lambda x:-x[1])
        print(f"  +EXTRA content tokens: {', '.join(f'{t}x{c}' if c>1 else t for t,c in ex[:40])}")

def main():
    args=sys.argv[1:]
    if not args:
        args=sorted(glob.glob(f"{ROOT}/rules/*.md")+
                    glob.glob(f"{ROOT}/rules/magic-states-effects/*.md")+
                    glob.glob(f"{ROOT}/rules/classes/*.md"))
    for a in args: review(a)

if __name__=="__main__": main()
