import json,re,sys
sys.path.insert(0,'/home/claude/scratch')
from rate import *
def area_class(i,head):
    a=plain(i['area'] or '').lower(); t=(i['targets'] or '').lower()
    if not a:
        m=re.search(r'\d+-foot[- ]+(?:burst|cone|line|emanation)',head)
        a=m.group(0).lower() if m else ''
    m=re.search(r'(\d+)-foot[- ]+(burst|cone|line|emanation)',a)
    if m:
        size=int(m.group(1)); sh=m.group(2)
        if sh=='burst': return 0 if size<=5 else 1 if size<=10 else 2
        if sh=='cone': return 1 if size<=30 else 2
        if sh=='line': return 1
        if sh=='emanation': return 0 if size<=5 else 1 if size<=15 else 2
    if 'any number' in t or 'all creatures' in t: return 2
    if re.search(r'1 or 2|up to (two|three|2|3)|1 or more|two targets',t): return 1
    if a and ('cube' in a or 'square' in a): return 0
    return 1 if a else 0
def star(ratio):
    return 6 if ratio>1.6 else 5 if ratio>=1.2 else 4 if ratio>1.05 else 3 if ratio>=0.8 else 2 if ratio>=0.45 else 1 if ratio>0 else 0
rows=[]
for which,src in (('A',RANKS),('O',OCCULT)):
    for rank in range(0,10):
        for n in src.get(rank,[]):
            if n not in E: continue
            cur=int(E[n][0][0])
            try: i,d,srcx,attack,basic,out,head,h=feat(n)
            except Exception as ex: print('ERR',n); continue
            basic = basic or 'half' in out.get('Success','').lower()
            per=(d[0]+2*d[1])*(1.0 if (attack or basic) else 0.85)
            bench=7*rank if rank>0 else 5.5
            ratio=per/bench; ac=area_class(i,head)
            ns=min(6,star(ratio)+ac) if ratio>0 else 0
            if cur>0 or ns>0:
                rows.append((rank,which,n,cur,d,ratio,ac,ns,plain(i['area'] or '')[:22],(i['targets'] or '')[:20],'A' if attack else ('b' if basic else 'n')))
import collections
for r in rows:
    rank,which,n,cur,d,ratio,ac,ns,a,t,k=r
    if ns!=cur: print(f"{rank}{which} {n:<27} cur{cur} {d[0]:>3.0f}+{d[1]:.0f}p {k} r={ratio:.2f} a{ac} -> {ns}  |{a}|{t}")
