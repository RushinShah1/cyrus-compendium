import sys
from aonrules import *
import occult_list as O
A={'Single Action':'1a','Two Actions':'2a','Three Actions':'3a','Reaction':'R','Free Action':'F'}
lo=int(sys.argv[1]); hi=int(sys.argv[2])
allr={n for r in RANKS for n in RANKS[r]}
names=[(r,n) for r in sorted(O.OCCULT) for n in O.OCCULT[r] if n not in allr and n in E]
print(len(names))
for r,n in names[lo:hi]:
    i=info(n); g=E[n][1]; top=g[0] in 'SAB'
    tr=', '.join(t for t in i['traits'] if t not in ('Concentrate','Manipulate','Cantrip'))
    act=i['actions'] or ''
    for k,v in A.items(): act=act.replace(k,v)
    f=[act,tr,'save '+str(i['save']) if i['save'] else '', 'area '+plain(str(i['area'])) if i['area'] else '', i['range'] or '', 'T: '+i['targets'] if i['targets'] else '', 'dur '+i['duration'] if i['duration'] else '']
    print(f"\n## r{r} {n} [{g} {E[n][0]}] "+' | '.join(x for x in f if x))
    print('  R:', i['text'][:(380 if top else 180)])
    print('  O:', E[n][2][:(200 if top else 110)])
