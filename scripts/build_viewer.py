#!/usr/bin/env python3
"""Assemble the publishable viewer: viewer/template.html + viewer/wiki-data.json
-> viewer/amtgard-rules-viewer.html

Run scripts/build_viewer_data.py first (it regenerates wiki-data.json), then this.

Every rule here exists because breaking it produced a real defect at some point:
 - the JSON is embedded inside <script type="application/json">, so any literal "</script>" or
   "<!--" in the data would terminate or comment out the block and blank the page;
 - the artifact host supplies <head>, so there is no charset declaration and a single non-ASCII
   byte renders as mojibake (this shipped once as "V8.7 Â· VIEWER");
 - __DATA__ must be substituted exactly once.
"""
import json, os, sys, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(BASE, "viewer", "template.html")
DATA = os.path.join(BASE, "viewer", "wiki-data.json")
OUT = os.path.join(BASE, "viewer", "amtgard-rules-viewer.html")

def main():
    tpl = open(TEMPLATE, encoding="utf-8").read()
    raw = open(DATA, encoding="utf-8").read()

    if tpl.count("__DATA__") != 1:
        sys.exit(f"FAIL: template must contain exactly one __DATA__ (found {tpl.count('__DATA__')})")

    # neutralise sequences that would break out of the <script type="application/json"> block
    data = raw.replace("</script>", "<\\/script>").replace("<!--", "<\\!--")
    if json.loads(data.replace("<\\/script>", "</script>").replace("<\\!--", "<!--")) is None:
        sys.exit("FAIL: data is not valid JSON")

    out = tpl.replace("__DATA__", data)

    if "__DATA__" in out:
        sys.exit("FAIL: __DATA__ survived substitution")
    bad = [(i, c) for i, c in enumerate(out) if ord(c) > 127]
    if bad:
        ctx = out[max(0, bad[0][0] - 60):bad[0][0] + 60]
        sys.exit(f"FAIL: artifact must be pure ASCII; first offender {bad[0][1]!r} "
                 f"at {bad[0][0]} of {len(bad)}\n  ...{ctx}...")
    # the only </script> left must be the template's own closing tags, not data
    head = out.split("__DATA__")[0]
    if out.count("</script>") != tpl.count("</script>"):
        sys.exit(f"FAIL: data introduced {out.count('</script>') - tpl.count('</script>')} "
                 f"stray </script>")

    open(OUT, "w", encoding="utf-8").write(out)

    pages = json.loads(raw)["pages"]
    print(f"wrote {OUT}")
    print(f"  {len(out):,} bytes  |  {len(pages)} pages  |  pure ASCII  |  1 __DATA__ substitution")

if __name__ == "__main__":
    main()
