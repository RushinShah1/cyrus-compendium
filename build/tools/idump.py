import sys; sys.path.insert(0,'/home/claude/build/gen')
import item_data as d
src=d.I if sys.argv[1]=='i' else d.C
ks=list(src)
a=int(sys.argv[2]); b=int(sys.argv[3])
for n in ks[a:b]:
    v=src[n]
    print(f"## {n} [{v['g']}] {v.get('cat','')} {v.get('plan','')}\n{v['ev']}\n")
