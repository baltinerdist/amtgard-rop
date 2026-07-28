#!/usr/bin/env python3
"""Generate a printable one-page-per-class Level 1 reference (front/back OK).
Pulls ability/spell definitions from the verified rules/magic-and-abilities/*.md files
and level-1 kits from the class progression tables. Outputs level1-class-cards.html."""
import re, os, glob
ROOT="/Users/averykrouse/GitHub/amtgard-rop"
MA=os.path.join(ROOT,"rules/magic-and-abilities")
CLASSDIR=os.path.join(ROOT,"rules/classes")

def slug(name):
    return re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')

def load_ability(name):
    """Return dict of fields for an ability by name, from its md file."""
    p=os.path.join(MA,slug(name)+".md")
    if not os.path.exists(p): return None
    t=open(p).read()
    d={}
    for m in re.finditer(r'^\*\*([A-Za-z]+):\*\*\s(.*)$',t,re.M):
        d[m.group(1)]=m.group(2).strip()
    return d

def immune_def(school):
    return {"School":school,"Category":"Trait (T)",
            "Effect":f"Always on: you are unaffected by abilities from the {school} School. "
                     f"As a Trait it cannot be removed and needs no incantation."}

# ---- level-1 spell tables for magic users (parsed from class files) ----
def magic_table(cls):
    t=open(os.path.join(CLASSDIR,cls+".md")).read()
    seg=re.search(r'### 1st Level\n(.*?)(?:\n### |\n## |\Z)',t,re.S)
    rows=[]
    for line in seg.group(1).splitlines():
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(c)<7 or c[0] in ("Name","---","") or set(c[0])<=set('-'): continue
        name=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',c[0])
        rows.append(dict(name=name,cost=c[1],mx=c[2],freq=c[3],typ=c[4],school=c[5],rng=c[6]))
    return rows

# ---- static per-class metadata (all verbatim-verified from source) ----
META={
"Anti-Paladin":dict(cat="Martial",garb="Metallic silver sash",ltp="Terror 1/Life (m)",
  req="Must be 6th level in at least one class.",armor="4 pts",shields="Large",weapons="All Melee, Javelins",
  role="Aggressive front-line combat — offense and disrupting enemies.",
  kit=[("Immune to Command","Trait (T)","Command"),("Immune to Flame","Trait (T)","Flame")],
  ltp_refs=["Terror"]),
"Archer":dict(cat="Martial",garb="Orange sash",ltp="Pick one arrow: Destruction / Poison / Pinning — 1 Arrow / Unlimited (ex)",
  req=None,armor="2 pts",shields="None",weapons="Dagger, Short, Bow",
  role="Ranged combat — strategic use of enhanced arrows.",
  kit=[("Reload 1/Refresh Charge x3 (ex)","","Reload"),
       ("Pick two of three (1 Arrow / Unlimited, ex):","choice",None),
       ("• Destruction Arrow","sub","Destruction Arrow"),
       ("• Pinning Arrow","sub","Pinning Arrow"),
       ("• Poison Arrow","sub","Poison Arrow")],
  ltp_refs=[]),
"Assassin":dict(cat="Martial",garb="Black sash",ltp="Pick one: Poison (Self) 1/Life Charge x3 (ex)  OR  Poison Arrow 1 Arrow/Unlimited (ex)",
  req=None,armor="2 pts",shields="None",weapons="Dagger, Short, Long, Light Thrown, Heavy Thrown, Bow",
  role="High-mobility, stealth-based play — precision and hit-and-run.",
  kit=[("Trickery","Trait (T)","Trickery"),
       ("Assassinate Unlimited (ex) (Ambulant)","","Assassinate"),
       ("Shadow Step 2/Life (ex)","","Shadow Step")],
  ltp_refs=["Poison","Poison Arrow"]),
"Barbarian":dict(cat="Martial",garb="White sash",ltp="Rage 1/Refresh Charge x10 (ex) (Ambulant)",
  req=None,armor="3 pts",shields="Medium",weapons="All Melee, Javelins, Rocks",
  role="Aggressive front-line fighting — melee and endurance.",
  kit=[("Berserk","Trait (T)","Berserk"),("Immune to Command","Trait (T)","Command"),
       ("Immune to Subdual","Trait (T)","Subdual")],
  ltp_refs=["Rage"]),
"Monk":dict(cat="Martial",garb="Gray sash",ltp="Heal 1/Life (ex)",
  req=None,armor="1 pt",shields="None",weapons="All Melee, Heavy Thrown",
  role="Support and skirmishing — melee combat and supporting allies.",
  kit=[("Enlightened Soul","Trait (T)","Enlightened Soul"),("Missile Block","Trait (T)","Missile Block")],
  ltp_refs=["Heal"]),
"Paladin":dict(cat="Martial",garb="Metallic gold sash (Knights: white belt + white phoenix symbol)",ltp="Awe 1/Life (m)",
  req=None,armor="4 pts",shields="Large",weapons="All Melee, Javelins",
  role="Support and tank — defense and healing.",
  kit=[("Immune to Command","Trait (T)","Command"),("Immune to Death","Trait (T)","Death")],
  ltp_refs=["Awe"]),
"Scout":dict(cat="Martial",garb="Green sash",ltp="Heal 1/Life (ex)",
  req=None,armor="3 pts",shields="Small",weapons="Dagger, Short, Long, Heavy Thrown, Bow",
  role="Versatile support and control — mobility and disruption.",
  kit=[("Tracking 2/Life Charge x3 (ex) (Ambulant)","","Tracking")],
  ltp_refs=["Heal"]),
"Warrior":dict(cat="Martial",garb="Purple sash",ltp="Insult 1/Life (m) (Ambulant)",
  req=None,armor="6 pts",shields="Large",weapons="All Melee, Javelins",
  role="Frontline combat and resilience — durability and disruption.",
  kit=[("Harden (Self) 1/Life (ex)","","Harden")],
  ltp_refs=["Insult"]),
"Bard":dict(cat="Magic User",garb="Light blue sash",ltp="+1 magic point at your highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Battlefield control — enhancing itself and allies while hindering enemies."),
"Druid":dict(cat="Magic User",garb="Brown sash",ltp="+1 magic point at your highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Versatile support and fighting — empowering allies and hindering enemies."),
"Healer":dict(cat="Magic User",garb="Red sash",ltp="+1 magic point at your highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Support and protection — restoring and fortifying allies."),
"Wizard":dict(cat="Magic User",garb="Yellow sash",ltp="+1 magic point at your highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Powerful ranged offense and battlefield control — damaging and disrupting enemies."),
}
ORDER=["Anti-Paladin","Archer","Assassin","Barbarian","Monk","Paladin","Scout","Warrior",
       "Bard","Druid","Healer","Wizard"]

def esc(s): return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def ability_block(name, d):
    if not d: return f'<div class="ab"><div class="abn">{esc(name)}</div><div class="abe"><em>See rulebook.</em></div></div>'
    meta=" · ".join(x for x in [d.get("School"),d.get("Range"),d.get("Category")] if x)
    inc=f'<div class="inc">“{esc(d["Incantation"].strip(chr(34)))}”</div>' if d.get("Incantation") else ""
    mat=f'<span class="mat">Materials: {esc(d["Materials"])}</span> ' if d.get("Materials") else ""
    eff=f'<div class="abe">{esc(d.get("Effect",""))}</div>' if d.get("Effect") else ""
    lim=f'<div class="lim"><b>Limits:</b> {esc(d["Limitations"])}</div>' if d.get("Limitations") else ""
    note=f'<div class="lim"><b>Note:</b> {esc(d["Note"])}</div>' if d.get("Note") else ""
    return (f'<div class="ab"><div class="abn">{esc(name)}'
            f'{f"<span class=abmeta>{esc(meta)}</span>" if meta else ""}</div>'
            f'{inc}{eff}{mat}{lim}{note}</div>')

def card(cls):
    m=META[cls]; magic=(m["cat"]=="Magic User")
    # collect kit rows + reference names
    ref_names=[]  # (display name, def dict)
    kit_html=[]
    if magic:
        rows=magic_table(cls)
        kit_html.append('<p class="kitnote">You have <b>5 magic points</b>. Buy from the 1st-level list below '
                        '(Cost = points; Max = how many you may own; Frequency = uses). '
                        'Unused points can roll down from higher levels.</p>')
        kit_html.append('<table class="spt"><tr><th>Spell</th><th>Cost</th><th>Max</th><th>Frequency</th><th>School</th><th>Range</th></tr>')
        for r in rows:
            kit_html.append(f'<tr><td>{esc(r["name"])}</td><td>{esc(r["cost"])}</td><td>{esc(r["mx"])}</td>'
                            f'<td>{esc(r["freq"])}</td><td>{esc(r["school"])}</td><td>{esc(r["rng"])}</td></tr>')
        kit_html.append('</table>')
        for r in rows: ref_names.append((r["name"], load_ability(r["name"])))
    else:
        kit_html.append('<ul class="kit">')
        for label,tag,ref in m["kit"]:
            cls_attr=' class="sub"' if tag=="sub" else (' class="choice"' if tag=="choice" else '')
            tagtxt=f' <span class="tt">{tag}</span>' if tag in("Trait (T)",) else ''
            kit_html.append(f'<li{cls_attr}>{esc(label)}{tagtxt}</li>')
            if ref:
                d=immune_def(ref) if ref in ("Command","Flame","Subdual","Death") and label.startswith("Immune") else load_ability(ref)
                ref_names.append((label.split(" (")[0].replace("• ",""), d))
        kit_html.append('</ul>')
        # look the part granted abilities
        for rn in m.get("ltp_refs",[]):
            ref_names.append((rn, load_ability(rn)))
    # dedupe reference by display name, keep order
    seen=set(); refs=[]
    for n,d in ref_names:
        if n in seen: continue
        seen.add(n); refs.append((n,d))
    ability_html="".join(ability_block(n,d) for n,d in refs)
    req_html=f'<span class="req">⚑ Requirement: {esc(m["req"])}</span>' if m.get("req") else ''
    return f"""
<section class="cardpage {'magic' if magic else 'martial'}">
  <header class="chead">
    <div class="ctitle"><h1>{esc(cls)}</h1><span class="badge">{m['cat']} · Level 1</span></div>
    <p class="role">{esc(m['role'])}</p>
  </header>
  <div class="stats">
    <div><span>Armor</span>{esc(m['armor'])}</div>
    <div><span>Shields</span>{esc(m['shields'])}</div>
    <div class="wide"><span>Weapons</span>{esc(m['weapons'])}</div>
    <div class="wide"><span>Garb</span>{esc(m['garb'])}</div>
    <div class="wide"><span>Look The Part (lvl 1 bonus)</span>{esc(m['ltp'])}</div>
  </div>
  {f'<div class="reqbar">{req_html}</div>' if req_html else ''}
  <h2>Your Level 1 Kit</h2>
  {''.join(kit_html)}
  <h2>Ability &amp; Magic Reference</h2>
  <div class="refs">{ability_html}</div>
</section>"""

CSS="""
@page { size: letter portrait; margin: 0.45in; }
*{box-sizing:border-box}
body{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;color:#1a1614;font-size:9.4pt;line-height:1.32;margin:0}
.cardpage{page-break-after:always;padding:0}
.cardpage:last-child{page-break-after:auto}
.chead{border-bottom:2.5px solid #6b1f2a;padding-bottom:4px;margin-bottom:7px}
.ctitle{display:flex;align-items:baseline;gap:10px}
h1{font-family:Georgia,'Times New Roman',serif;font-size:23pt;margin:0;color:#6b1f2a;letter-spacing:.3px}
.badge{font-size:8pt;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:#fff;background:#6b1f2a;padding:2px 7px;border-radius:9px}
.magic .chead{border-color:#28407a}.magic h1{color:#28407a}.magic .badge{background:#28407a}
.role{margin:3px 0 0;font-style:italic;color:#4a4340}
.stats{display:flex;flex-wrap:wrap;gap:0;border:1px solid #d9cfc7;border-radius:5px;overflow:hidden;margin-bottom:6px}
.stats>div{flex:1 1 30%;min-width:120px;padding:4px 8px;border-right:1px solid #ece5df;border-bottom:1px solid #ece5df}
.stats>div.wide{flex:1 1 46%}
.stats span{display:block;font-size:6.8pt;text-transform:uppercase;letter-spacing:.6px;color:#8a7f77;font-weight:700}
.reqbar{margin:0 0 6px}.req{font-size:8.4pt;font-weight:700;color:#8a5a00;background:#fbf1dd;border:1px solid #e6d3a8;padding:2px 8px;border-radius:4px}
h2{font-family:Georgia,serif;font-size:11pt;color:#3a322e;margin:9px 0 4px;padding-bottom:2px;border-bottom:1px solid #d9cfc7}
.kitnote{margin:2px 0 5px;font-size:8.8pt;color:#4a4340}
ul.kit{margin:2px 0 0;padding-left:16px}
ul.kit li{margin-bottom:1.5px}
ul.kit li.sub{list-style:none;margin-left:6px}
ul.kit li.choice{list-style:none;font-weight:700;margin-top:3px}
.tt{font-size:6.6pt;font-weight:700;color:#6b1f2a;background:#f3e6e2;padding:0 4px;border-radius:3px;vertical-align:1px}
table.spt{width:100%;border-collapse:collapse;font-size:8.5pt;margin-top:2px}
table.spt th{background:#eef1f7;text-align:left;padding:2.5px 5px;border:1px solid #d3d9e6;font-size:7.4pt;text-transform:uppercase;letter-spacing:.4px}
table.spt td{padding:2.5px 5px;border:1px solid #e2e6ef}
table.spt tr:nth-child(even) td{background:#f7f8fb}
.refs{column-count:2;column-gap:14px;margin-top:2px}
.ab{break-inside:avoid;margin-bottom:5px;padding-left:6px;border-left:2px solid #d9cfc7}
.magic .ab{border-color:#c3cde3}
.abn{font-weight:700;font-size:9.2pt;color:#2a2320}
.abmeta{font-weight:400;font-size:7.2pt;color:#8a7f77;margin-left:5px;text-transform:uppercase;letter-spacing:.3px}
.inc{font-style:italic;color:#6b1f2a;margin:1px 0}
.magic .inc{color:#28407a}
.abe{margin:1px 0}
.mat{font-size:7.8pt;color:#6a615b}
.lim{font-size:8pt;color:#4a4340}
.legend{page-break-after:always;padding:4px}
.legend h1{font-size:16pt;color:#3a322e}
.legend dt{font-weight:700;margin-top:4px}
"""

def legend_page():
    items=[("1/Life","Uses per life; refills each time you respawn."),
           ("1/Refresh","Uses per Refresh; refilled only when a Reeve calls a Refresh."),
           ("Charge xN","Reusable, but must be re-Charged after the initial N uses are spent."),
           ("Unlimited","May be used any number of times."),
           ("(T) Trait","Always on; cannot be removed; needs no incantation."),
           ("(ex) Extraordinary","Non-magical ability."),
           ("(m) Magical","Magical ability; Enchantments count toward your limit."),
           ("(Ambulant)","May be incanted while moving."),
           ("(A) Archetype","A level-6 build-defining choice (shown for context; not a level-1 option)."),
           ("Incantation","The “quoted” phrase you must say (×N = repeat that many times) to activate the ability."),
           ("Death","Any two wounds, or one wound to the torso, kills you.")]
    dl="".join(f"<dt>{esc(k)}</dt><dd>{esc(v)}</dd>" for k,v in items)
    return (f'<section class="legend"><h1>Amtgard Level 1 — How to Read These Cards</h1>'
            f'<p>One card per class (front &amp; back). Everything you need to play that class at level 1: '
            f'equipment, your starting abilities, and full ability/spell definitions. Notation:</p>'
            f'<dl>{dl}</dl></section>')

def main():
    body=legend_page()+ "".join(card(c) for c in ORDER)
    html=f"<style>{CSS}</style>\n{body}"
    out=os.path.join(ROOT,"level1-class-cards.html")
    open(out,"w").write(html)
    print("wrote",out)

if __name__=="__main__": main()
