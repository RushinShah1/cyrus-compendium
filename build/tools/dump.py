import sys; sys.path.insert(0,'/home/claude/build/gen')
import spell_evals as se, spell_list as sl
E=se.E
arg=sys.argv[1]
if arg=='occ':
    names=[k for k in E if not any(k in l for l in sl.RANKS.values())]
else:
    names=sl.RANKS[int(arg)]
a=int(sys.argv[2]) if len(sys.argv)>2 else 0; b=int(sys.argv[3]) if len(sys.argv)>3 else 999
for n in names[a:b]:
    r,g,t=E[n]
    print(f'## {n} [{g}] {r}\n{t}\n')
