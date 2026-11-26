import json,re,sys,glob,os
D='/home/claude/pf2e/packs/pf2e/equipment'
IDX={}
for f in glob.glob(D+'/*.json'):
    if os.path.basename(f).startswith('_'): continue
    try: d=json.load(open(f))
    except: continue
    IDX[d['name'].lower()]=d
def clean(t): return re.sub(r'\s+',' ',re.sub(r'@\w+\[[^\]]*\]\{([^}]*)\}',r'\1',re.sub(r'@UUID\[[^\]]*\.([^\].]*)\](?!\{)',r'\1',re.sub(r'@(Check|Damage|Template)\[([^\]|]*)[^\]]*\]',r'\2',re.sub('<[^>]+>',' ',t)))))
n=int(sys.argv[1]); 
for name in sys.argv[2:]:
    d=IDX.get(name.lower())
    if not d: print('##',name,'MISSING'); continue
    s=d['system']; pub=s.get('publication',{})
    print(f"## {d['name']} | L{s['level']['value']} | {s.get('price',{}).get('value')} | {s['traits'].get('rarity')} | {(s.get('usage') or {}).get('value')} | {'R' if pub.get('remaster') else 'L'} {pub.get('title','')} | {','.join(s['traits']['value'])}")
    print(clean(s['description']['value'])[:n]); print()
