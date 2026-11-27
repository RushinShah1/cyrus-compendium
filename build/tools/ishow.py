import sys,re
from isearch import *
def show(name,n=1100):
    c=[d for d in eq if d['name'].lower()==name.lower() and cur(d)] or [d for d in eq if d['name'].lower()==name.lower()]
    if not c: print('== MISSING',name); return
    d=c[0]; t=d['text']
    print(f"== {d['name']} | L{d['level']} | {d.get('price_raw','')} | {d['rarity']} | {d['primary_source']} | {d['item_category']}{' | LEGACY-ONLY' if not cur(d) else ''}\n   {t[:n]}")
if __name__=='__main__':
    n=1100
    for a in sys.argv[1:]:
        if a.isdigit(): n=int(a); continue
        show(a,n)
