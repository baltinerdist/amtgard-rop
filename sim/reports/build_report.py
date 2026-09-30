"""Build sim/out/report.html from sim/out/cut.json (and sim/out/sensitivity.json if present).

    .venv/bin/python -m sim.analyze.cut --games 300
    .venv/bin/python -m sim.analyze.sensitivity            # optional
    .venv/bin/python -m sim.reports.build_report

The page is sim/reports/report-template.html with the data inlined (the same approach as
scripts/build_meta_explorer.py), so it opens from disk with no server.
"""
from __future__ import annotations

import argparse
import json
import math
import os

from sim.analyze import complexity as cx
from sim.analyze import impact
from sim.paths import OUT, SIM

TPL = SIM / "reports" / "report-template.html"


def _clean(x):
    """JSON-safe copy: NaN/inf become null."""
    if isinstance(x, float):
        return None if math.isnan(x) or math.isinf(x) else x
    if isinstance(x, dict):
        return {str(k): _clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_clean(v) for v in x]
    return x


def build(cut_path, sens_path, out_path) -> str:
    cut = json.load(open(cut_path))
    sens = json.load(open(sens_path)) if sens_path and os.path.exists(sens_path) else None
    titles = {r["slug"]: r["title"] for r in cx.load_records()}
    data = {
        "cut": cut, "sensitivity": sens, "titles": titles,
        "definitions": {"complexity_weights": cut["meta"].get("complexity_weights", cx.WEIGHTS),
                        "distance_weights": impact.DISTANCE_WEIGHTS,
                        "complexity_doc": (cx.__doc__ or "").strip(), "impact_doc": (impact.__doc__ or "").strip()},
    }
    blob = json.dumps(_clean(data), separators=(",", ":"), ensure_ascii=True).replace("</", "<\\/")
    tpl = TPL.read_text(encoding="utf-8")
    assert tpl.count("__DATA__") == 1
    html = tpl.replace("__DATA__", blob)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return html


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the cut-analysis HTML report")
    ap.add_argument("--cut", default=str(OUT / "cut.json"))
    ap.add_argument("--sensitivity", default=str(OUT / "sensitivity.json"))
    ap.add_argument("--out", default=str(OUT / "report.html"))
    args = ap.parse_args(argv)
    if not os.path.exists(args.cut):
        ap.error(f"{args.cut} not found; run python -m sim.analyze.cut first")
    html = build(args.cut, args.sensitivity, args.out)
    print(f"wrote {args.out} ({len(html) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
