import sys,re; sys.path.insert(0,'/home/claude/build/gen')
import spell_evals as se
src=open('/home/claude/build/gen/spell_evals9.py').read()
names=[n for _,n in re.findall(r'^w\((["\'])(.+?)\1,',src,re.M)]
bad=r"\b(payload|the party|party|rider|job|earns?|feeds?|floor|ceiling|pick|picks|direct cast|cast directly|staple|default|dead weight|tax|niche|silver bullet|buff|debuff|setup|opener|striker|brute|skirmisher|blast|crit|crits|combo|genuinely|honestly|straightforward|shines?|toolkit|workhorse|bread|GM|ruling|build)\b|—|;"
imp=r'(?:(?<=[.] )|^|(?<=\n))(Prepare|Learn|Keep|Skip|Carry|Take|Scribe|Leave|Use|Buy|Cast|Save|Pair|Do not|Hold|Treat|Pass|Bring|Think|Consider|Choose|Pick)\b'
n=0
for nm in names:
    t=se.E[nm][2]
    hits=set(m.group(0) for m in re.finditer(bad,t))|set(m.group(0) for m in re.finditer(imp,t))
    short=[s for s in re.split(r'(?<=[.!?])\s+',t) if len(s.split())<=5]
    if not t.startswith(nm.split("’")[0][:4]) and not re.match(r'(In |As |When |Cyrus|His |From |With |Against )',t): hits.add('OPEN:'+t[:30])
    if hits or short: n+=1; print(nm,'|',sorted(hits),'|',short)
print(n,'flagged of',len(names),'words',sum(len(se.E[x][2].split()) for x in names))
