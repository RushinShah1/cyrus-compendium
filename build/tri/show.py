import sys, re
sys.path.insert(0,'/home/claude/build/gen')
from entries import entry
t=lambda s: re.sub(r'\s+',' ',re.sub('<[^>]+>',' ',s or '')).strip()
for n in sys.argv[1].split(';'):
    n=n.strip()
    try: e=entry(n,'spell')
    except Exception as x: print('!!',n,x); continue
    tr=[a for a,_ in e.get('traits',[]) if a not in ('Concentrate','Manipulate')]
    f='; '.join(f'{a}: {t(b)}' for a,b in e.get('fields',[]))
    print(f"## {n} [{e.get('action_text') or e.get('action')}] {','.join(tr)} | {f}\n{t(e.get('body'))[:int(sys.argv[2]) if len(sys.argv)>2 else 650]}\nH: {t(e.get('heightened'))[:260]}\n")
