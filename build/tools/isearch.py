import json,re,sys
sys.path.insert(0,'/home/claude/build/gen')
D='/home/claude/ext/aon/2e/data/'
eq=json.load(open(D+'equipment.json'))
from item_data import I
have={n.lower() for n in I}
CATS={'Worn Items','Held Items','Runes','Spellhearts','Tattoos','Grimoires','Apex Items','Staves','Wands','Customizations','Shrouds','Grafts','Other','Censer'}
def cur(d): return d.get('remaster_id') in ('','[]',None) and d.get('exclude_from_search')!='True'
def base(n): return re.sub(r'\s*\((lesser|moderate|greater|major|true|minor|type [iv]+|standard)[^)]*\)','',n,flags=re.I).strip().lower()
def rows(pat,cats=None,lmax=20,lmin=0,new=True):
    rx=re.compile(pat,re.I); out=[]
    for d in eq:
        if d.get('item_category') not in (cats or CATS): continue
        if not cur(d): continue
        try: lv=int(d.get('level') or 0)
        except: lv=0
        if lv>lmax or lv<lmin: continue
        t=d.get('text','')
        if not rx.search(t): continue
        if new and base(d['name']) in have: continue
        out.append((lv,d))
    return sorted(out,key=lambda x:(x[0],x[1]['name']))
if __name__=='__main__':
    pat=sys.argv[1]; cats=set(sys.argv[2].split('|')) if len(sys.argv)>2 and sys.argv[2]!='-' else None
    n=int(sys.argv[3]) if len(sys.argv)>3 else 260
    for lv,d in rows(pat,cats):
        t=d['text']; m=re.search(pat,t,re.I); s=max(0,m.start()-n//2)
        print(f"{lv:>2} {d['name']} [{d['item_category']}; {d['rarity']}; {d['primary_source']}; {d.get('price_raw','')}] …{t[s:s+n]}…")
