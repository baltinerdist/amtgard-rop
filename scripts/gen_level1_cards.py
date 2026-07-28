#!/usr/bin/env python3
"""Generate a printable Level 1 class reference as HALF-PAGE cards, two per page.
Compact merged layout: each ability/spell is one dense entry (inline cost/frequency/
school/range + incantation + effect). Pulls definitions from the verified
rules/magic-and-abilities/*.md files. Outputs level1-class-cards.html."""
import re, os
ROOT="/Users/averykrouse/GitHub/amtgard-rop"
MA=os.path.join(ROOT,"rules/magic-and-abilities")
CLASSDIR=os.path.join(ROOT,"rules/classes")

def slug(name): return re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')

def load_ability(name):
    p=os.path.join(MA,slug(name)+".md")
    if not os.path.exists(p): return {}
    d={}
    for m in re.finditer(r'^\*\*([A-Za-z]+):\*\*\s(.*)$',open(p).read(),re.M):
        d[m.group(1)]=m.group(2).strip()
    return d

def immune_def(school):
    return {"School":school,"Effect":f"Always on: unaffected by abilities from the {school} School. "
            "Cannot be removed; needs no incantation."}

def magic_rows(cls):
    t=open(os.path.join(CLASSDIR,cls+".md")).read()
    seg=re.search(r'### 1st Level\n(.*?)(?:\n### |\n## |\Z)',t,re.S)
    rows=[]
    for line in seg.group(1).splitlines():
        c=[x.strip() for x in line.strip().strip('|').split('|')]
        if len(c)<7 or c[0] in ("Name","") or set(c[0])<=set('-'): continue
        rows.append(dict(name=re.sub(r'\[([^\]]*)\]\([^)]*\)',r'\1',c[0]),
                         cost=c[1],mx=c[2],freq=c[3],school=c[5],rng=c[6]))
    return rows

# martial entries: (display, meta-prefix [freq/category], ref) ; ref = ability name or ("immune",School)
META={
"Anti-Paladin":dict(cat="Martial",garb="Metallic silver sash",ltp="Terror 1/Life (m)",
  req="Must be 6th level in another class",armor="4 pts",shields="Large",weapons="All Melee, Javelins",
  role="Aggressive front-line offense &amp; disruption.",
  summary="<b>Traits:</b> Immune to Command, Immune to Flame. <b>Look&nbsp;The&nbsp;Part:</b> Terror.",
  entries=[("Immune to Command","Trait",("immune","Command")),
           ("Immune to Flame","Trait",("immune","Flame")),
           ("Terror","LTP · 1/Life · (m)","Terror")]),
"Archer":dict(cat="Martial",garb="Orange sash",ltp="Pick one arrow (1 Arrow/Unlim, ex)",
  req=None,armor="2 pts",shields="None",weapons="Dagger, Short, Bow",
  role="Ranged combat with enhanced arrows.",
  summary="<b>Get:</b> Reload + <b>pick two</b> of three arrows. <b>Look&nbsp;The&nbsp;Part:</b> pick one arrow.",
  entries=[("Reload","1/Refresh Charge x3 · (ex)","Reload"),
           ("Destruction Arrow","1 Arrow/Unlim · (ex)","Destruction Arrow"),
           ("Pinning Arrow","1 Arrow/Unlim · (ex)","Pinning Arrow"),
           ("Poison Arrow","1 Arrow/Unlim · (ex)","Poison Arrow")]),
"Assassin":dict(cat="Martial",garb="Black sash",ltp="Pick one: Poison or Poison Arrow",
  req=None,armor="2 pts",shields="None",weapons="Dagger, Short, Long, Light/Heavy Thrown, Bow",
  role="High-mobility stealth; precision hit-and-run.",
  summary="<b>Trait:</b> Trickery. <b>Get:</b> Assassinate, Shadow Step. <b>Look&nbsp;The&nbsp;Part:</b> pick one below.",
  entries=[("Trickery","Trait","Trickery"),
           ("Assassinate","Unlimited · (ex) · Ambulant","Assassinate"),
           ("Shadow Step","2/Life · (ex)","Shadow Step"),
           ("Poison","LTP option · 1/Life Charge x3 · (ex)","Poison"),
           ("Poison Arrow","LTP option · 1 Arrow/Unlim · (ex)","Poison Arrow")]),
"Barbarian":dict(cat="Martial",garb="White sash",ltp="Rage 1/Refresh Charge x10 (ex)",
  req=None,armor="3 pts",shields="Medium",weapons="All Melee, Javelins, Rocks",
  role="Aggressive melee bruiser; endurance.",
  summary="<b>Traits:</b> Berserk, Immune to Command, Immune to Subdual. <b>Look&nbsp;The&nbsp;Part:</b> Rage.",
  entries=[("Berserk","Trait","Berserk"),
           ("Immune to Command","Trait",("immune","Command")),
           ("Immune to Subdual","Trait",("immune","Subdual")),
           ("Rage","LTP · 1/Refresh Charge x10 · (ex) · Ambulant","Rage")]),
"Monk":dict(cat="Martial",garb="Gray sash",ltp="Heal 1/Life (ex)",
  req=None,armor="1 pt",shields="None",weapons="All Melee, Heavy Thrown",
  role="Support skirmisher; melee &amp; ally support.",
  summary="<b>Traits:</b> Enlightened Soul, Missile Block. <b>Look&nbsp;The&nbsp;Part:</b> Heal.",
  entries=[("Enlightened Soul","Trait","Enlightened Soul"),
           ("Missile Block","Trait","Missile Block"),
           ("Heal","LTP · 1/Life · (ex)","Heal")]),
"Paladin":dict(cat="Martial",garb="Metallic gold sash",ltp="Awe 1/Life (m)",
  req=None,armor="4 pts",shields="Large",weapons="All Melee, Javelins",
  role="Support tank; defense &amp; healing.",
  summary="<b>Traits:</b> Immune to Command, Immune to Death. <b>Look&nbsp;The&nbsp;Part:</b> Awe.",
  entries=[("Immune to Command","Trait",("immune","Command")),
           ("Immune to Death","Trait",("immune","Death")),
           ("Awe","LTP · 1/Life · (m)","Awe")]),
"Scout":dict(cat="Martial",garb="Green sash",ltp="Heal 1/Life (ex)",
  req=None,armor="3 pts",shields="Small",weapons="Dagger, Short, Long, Heavy Thrown, Bow",
  role="Versatile support &amp; control; mobility.",
  summary="<b>Get:</b> Tracking. <b>Look&nbsp;The&nbsp;Part:</b> Heal.",
  entries=[("Tracking","2/Life Charge x3 · (ex) · Ambulant","Tracking"),
           ("Heal","LTP · 1/Life · (ex)","Heal")]),
"Warrior":dict(cat="Martial",garb="Purple sash",ltp="Insult 1/Life (m)",
  req=None,armor="6 pts",shields="Large",weapons="All Melee, Javelins",
  role="Durable frontline; resilience &amp; disruption.",
  summary="<b>Get:</b> Harden. <b>Look&nbsp;The&nbsp;Part:</b> Insult.",
  entries=[("Harden","1/Life · (ex)","Harden"),
           ("Insult","LTP · 1/Life · (m) · Ambulant","Insult")]),
"Bard":dict(cat="Magic User",garb="Light blue sash",ltp="+1 magic point at highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Battlefield control; buff allies, hinder foes."),
"Druid":dict(cat="Magic User",garb="Brown sash",ltp="+1 magic point at highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Versatile support &amp; fighting; empower/hinder."),
"Healer":dict(cat="Magic User",garb="Red sash",ltp="+1 magic point at highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Support &amp; protection; restore/fortify allies."),
"Wizard":dict(cat="Magic User",garb="Yellow sash",ltp="+1 magic point at highest level",
  req=None,armor="None",shields="None",weapons="Dagger, Magic Staff",
  role="Ranged offense &amp; battlefield control."),
}
ORDER=["Anti-Paladin","Archer","Assassin","Barbarian","Monk","Paladin","Scout","Warrior",
       "Bard","Druid","Healer","Wizard"]

def esc(s): return (s or "").replace("&amp;","\0AMP\0").replace("&","&amp;").replace("\0AMP\0","&amp;").replace("<","&lt;").replace(">","&gt;")

def entry(name, meta_prefix, d, cost=None):
    school=d.get("School",""); rng=d.get("Range","")
    parts=[p for p in [cost, meta_prefix, school, rng] if p]
    meta=" · ".join(parts)
    inc=d.get("Incantation","").strip()
    inc_html=f'<i class="ei">“{esc(inc.strip(chr(34)))}”</i> ' if inc else ""
    eff=esc(d.get("Effect",""))
    lim=f' <span class="el">Limits: {esc(d["Limitations"])}</span>' if d.get("Limitations") else ""
    note=f' <span class="el">Note: {esc(d["Note"])}</span>' if d.get("Note") else ""
    return (f'<div class="e"><span class="en">{esc(name)}</span> '
            f'<span class="em">{esc(meta)}</span><br>{inc_html}{eff}{lim}{note}</div>')

def card(cls):
    m=META[cls]; magic=(m["cat"]=="Magic User")
    if magic:
        rows=magic_rows(cls)
        summary=('You have <b>5 magic points</b> — buy any 1st-level abilities below '
                 '(cost in pts). <b>Look&nbsp;The&nbsp;Part:</b> +1 point at highest level.')
        ent="".join(entry(r["name"],r["freq"],load_ability(r["name"]),cost=f'{r["cost"]}pt') for r in rows)
    else:
        summary=m["summary"]
        seen=set(); ent=""
        for name,meta,ref in m["entries"]:
            if name in seen: continue
            seen.add(name)
            d=immune_def(ref[1]) if isinstance(ref,tuple) else load_ability(ref)
            ent+=entry(name,meta,d)
    req=f'<span class="req">⚑ {esc(m["req"])}</span>' if m.get("req") else ''
    strip=(f'<b>Armor</b> {esc(m["armor"])} &nbsp;·&nbsp; <b>Shields</b> {esc(m["shields"])} '
           f'&nbsp;·&nbsp; <b>Weapons</b> {esc(m["weapons"])} &nbsp;·&nbsp; <b>Garb</b> {esc(m["garb"])} '
           f'&nbsp;·&nbsp; <b>Look&nbsp;The&nbsp;Part</b> {esc(m["ltp"])}')
    return f"""<div class="card {'magic' if magic else 'martial'}">
  <div class="hd"><span class="cn">{esc(cls)}</span><span class="bd">{m['cat']} · Lvl 1</span>
    <span class="ro">{m['role']}</span>{req}</div>
  <div class="strip">{strip}</div>
  <div class="sum">{summary}</div>
  <div class="body">{ent}</div>
</div>"""

def legend_card():
    items=[("1/Life","per life; refills on respawn"),("1/Refresh","per Refresh; refilled on reeve's Refresh"),
           ("Charge&nbsp;xN","reusable after re-Charging the initial N uses"),("Unlimited","any number of times"),
           ("(T)&nbsp;Trait","always on; no incantation; can't be removed"),("(ex)","non-magical"),
           ("(m)","magical (Enchantments count to your limit)"),("Ambulant","may incant while moving"),
           ("“…”&nbsp;×N","incantation you must say N times to activate"),
           ("Death","two wounds, or one to the torso, kills you")]
    body="".join(f'<div class="e"><span class="en">{k}</span> {v}</div>' for k,v in items)
    return (f'<div class="card legend"><div class="hd"><span class="cn">Level&nbsp;1 Cards</span>'
            f'<span class="bd">How to read</span>'
            f'<span class="ro">One half-card per class — equipment, your level-1 kit, and full ability defs.</span></div>'
            f'<div class="sum">Notation:</div><div class="body">{body}</div></div>')

CSS="""
@page{size:letter portrait;margin:0.32in}
*{box-sizing:border-box}
html,body{margin:0}
body{font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;color:#1a1614;font-size:8.6pt;line-height:1.3}
.sheet{height:10.3in;display:flex;flex-direction:column;gap:0.12in;page-break-after:always}
.sheet:last-child{page-break-after:auto}
.card{flex:1 1 0;min-height:0;border:0.8pt solid #cfc6bd;border-radius:6px;padding:7px 9px;overflow:hidden;position:relative}
.card.magic{--ac:#28407a}.card.martial,.card.legend{--ac:#6b1f2a}
.hd{border-bottom:1.8pt solid var(--ac);padding-bottom:2px;margin-bottom:3px;line-height:1.1}
.cn{font-family:Georgia,serif;font-size:15pt;font-weight:700;color:var(--ac);vertical-align:middle}
.bd{font-size:6.6pt;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#fff;background:var(--ac);padding:1.5px 6px;border-radius:8px;margin-left:6px;vertical-align:middle}
.ro{font-style:italic;color:#5a524d;margin-left:8px;font-size:8pt}
.req{float:right;font-size:6.8pt;font-weight:700;color:#8a5a00;background:#fbf1dd;border:0.6pt solid #e6d3a8;padding:0 6px;border-radius:4px;margin-top:2px}
.strip{font-size:7.7pt;color:#3a332e;margin-bottom:3px;line-height:1.35}
.strip b{color:#8a7f77;text-transform:uppercase;font-size:6.7pt;letter-spacing:.4px}
.sum{font-size:8pt;color:#2a2320;background:#f6f2ee;border-left:2.5px solid var(--ac);padding:2px 6px;margin-bottom:4px;border-radius:0 3px 3px 0}
.sum b{color:var(--ac)}
.body{column-count:3;column-gap:12px;font-size:8.2pt}
.legend .body{column-count:2}
.e{break-inside:avoid;margin-bottom:4px;line-height:1.28}
.en{font-weight:700;color:#2a2320}
.em{font-size:6.7pt;color:#8a7f77;text-transform:uppercase;letter-spacing:.2px}
.ei{color:var(--ac)}
.el{color:#6a615b;font-size:7.4pt}
.cut{height:0;border-top:0.5pt dashed #c4bab0}
"""

def main():
    cards=[legend_card()]+[card(c) for c in ORDER]   # 13 half-cards
    sheets=[]
    for i in range(0,len(cards),2):
        pair=cards[i:i+2]
        sheets.append('<div class="sheet">'+("".join(pair))+'</div>')
    html=f"<style>{CSS}</style>\n"+"\n".join(sheets)
    out=os.path.join(ROOT,"level1-class-cards.html")
    open(out,"w").write(html); print("wrote",out,"—",len(cards),"half-cards")

if __name__=="__main__": main()
