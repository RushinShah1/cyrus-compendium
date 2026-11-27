import sys
from aonrules import *
r=int(sys.argv[1]); N=int(sys.argv[2]); O=int(sys.argv[3]) if len(sys.argv)>3 else 0; only=set(sys.argv[4].split(',')) if len(sys.argv)>4 else None
for n in RANKS[r]:
    if n not in E or (only and E[n][1][0] not in only): continue
    i=info(n)
    print(f"\n## {n} [{E[n][1]} {E[n][0]}] {i['actions']} | {', '.join(i['traits'])} | save {i['save']} | area {i['area']} | range {i['range']} | targets {i['targets']} | dur {i['duration']} | {i['book']}")
    print('  RULES:', i['text'][:N])
    if O: print('  OLD:', E[n][2][:O])
