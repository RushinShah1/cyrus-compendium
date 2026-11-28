import sys
P='/home/claude/build/gen/item_data.py'
def apply(pairs):
    s=open(P).read(); n=0
    for a,b in pairs:
        if s.count(a)!=1: print('!! count',s.count(a),'for:',a[:70]); continue
        s=s.replace(a,b); n+=1
    open(P,'w').write(s); print('applied',n,'of',len(pairs))
