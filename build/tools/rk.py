"""Compact view of a rank for rewriting: fields, Archives of Nethys text, and the start of the old evaluation."""
import sys
from aonrules import *
r=int(sys.argv[1]); lo=int(sys.argv[2]) if len(sys.argv)>2 else 0; hi=int(sys.argv[3]) if len(sys.argv)>3 else 999
A={'Single Action':'1a','Two Actions':'2a','Three Actions':'3a','Reaction':'R','Free Action':'F'}
names=[n for n in RANKS[r] if n in E]
print(f'rank {r}: {len(names)} cards; showing {lo}-{min(hi,len(names))}')
for n in names[lo:hi]:
    i=info(n); g=E[n][1]; top=g[0] in 'SAB'
    tr=', '.join(t for t in i['traits'] if t not in ('Concentrate','Manipulate','Cantrip'))
    act=i['actions'] or ''
    for k,v in A.items(): act=act.replace(k,v)
    f=[act,tr,'save '+str(i['save']) if i['save'] else '', 'area '+plain(str(i['area'])) if i['area'] else '', i['range'] or '', 'T: '+i['targets'] if i['targets'] else '', 'dur '+i['duration'] if i['duration'] else '', 'LEGACY' if i['legacy'] else '']
    print(f"\n## {n} [{g} {E[n][0]}] "+' | '.join(x for x in f if x))
    print('  R:', i["text"][:(400 if top else 190)])
    print('  O:', E[n][2][:(200 if top else 110)])
