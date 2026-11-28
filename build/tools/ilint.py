import sys,re; sys.path.insert(0,'/home/claude/build/gen')
import item_data as d
I=d.I
C=getattr(d,'C',None) or getattr(d,'CONS',None)
bad=r"\b(payload|party|rider|riders|job|earns?|feeds?|floor|ceiling|pick|picks|staple|by default|dead weight|tax|taxes|niche|silver bullet|buffs?|debuffs?|setup|opener|striker|strikers|brute|brutes|skirmisher|skirmishers|blast|blasts|crit|crits|combo|genuinely|honestly|straightforward|shines?|toolkit|workhorse|GM|Alex|ruling|ruled|build|stopgap|standing|ThrabenU|sweep|handoff|chat|discussed|agreed|decided|we|payoff|pays off|swingy|the plan|plan)\b|—"
imp=r'(?:(?<=[.] )|^)(Prepare|Learn|Keep|Skip|Carry|Take|Scribe|Leave|Use|Buy|Save|Pair|Do not|Hold|Treat|Pass|Bring|Think|Consider|Choose|Pick)\b'
def sents(t): return re.split(r'(?<=[.!?])\s+',t)
verb=r"\b(is|are|was|were|has|have|had|does|do|did|can|could|will|would|may|might|must|should|gives?|lets?|makes?|adds?|needs?|costs?|works?|takes?|turns?|keeps?|puts?|covers?|grants?|allows?|means?|removes?|deals?|lasts?|ends?|stops?|applies|competes?|helps?|uses?|suits?|matters?|saves?|comes?|goes|stays?|becomes?|sits?|leaves?|fits?|protects?|replaces?|raises?|lowers?|reduces?|increases?|prevents?|casts?|holds?|offers?|provides?|depends?|triggers?|refreshes|stacks?|scales?|overlaps?|doubles?|halves|ignores?|extends?|restores?|heals?|counts?|sets?|opens?|asks?|buys?|wants?|gets?|loses?|wins?|pays?|carries|brings?|shares?|serves?|answers?|solves?|outperforms?|beats?|returns?|moves?|follows?|rolls?|hits?|strikes?|fails?|succeeds?|passes|lands?|arrives?|happens?|exists?|remains?|belongs?|wastes?|spends?|frees?|locks?|blocks?|hides?|shows?|reveals?|tells?|knows?|learns?|finds?|reaches|reads?|stores?|creates?|produces?|draws?|drops?|picks?|outlasts?|supplies|converts?|trades?|rewards?|punishes|forces?|denies|risks?|duplicates?|matches|trails?|lags?|falls?|rises?|grows?|shrinks?|fades?|runs?|flies|climbs?|swims?|sees?|senses?|hears?|speaks?|says?|states?|reaches)\b"
which=sys.argv[1] if len(sys.argv)>1 else 'all'
tot=0;fl=0
src=dict(I)
for n,v in src.items():
    t=v['ev']; tot+=1
    hits=sorted(set(m.group(0) for m in re.finditer(bad,t))|set(m.group(0) for m in re.finditer(imp,t)))
    frag=[s for s in sents(t) if not re.search(verb,s)]
    if hits or frag:
        fl+=1
        if which!='count': print(n,'|',hits,'|',frag)
print(fl,'of',tot,'words',sum(len(v['ev'].split()) for v in src.values()))
print([k for k in dir(d) if not k.startswith('_')])
