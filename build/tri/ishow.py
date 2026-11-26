import sys, re
sys.path.insert(0,'/home/claude/build/gen')
from entries import entry
t=lambda s: re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s or '')).strip()
for n in sys.argv[1].split(';'):
    n=n.strip()
    try: e=entry(n,'item',foundry_kind='item')
    except Exception as x:
        try: e=entry(n,'item',foundry_kind='any')
        except Exception as y: print('!!',n,y); continue
    tr=[a for a,_ in e.get('traits',[])]
    f='; '.join(f'{a}: {t(b)}' for a,b in e.get('fields',[]))
    print(f"## {n} | {e.get('level')} | {','.join(tr)} | {f}\n{t(e.get('body'))[:int(sys.argv[2]) if len(sys.argv)>2 else 900]}\n")
