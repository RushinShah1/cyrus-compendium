"""Check each evaluation's dice, areas, conditions and saves against the Archives of Nethys text."""
import sys
from aonrules import *
COND=['blinded','clumsy','concealed','confused','controlled','dazzled','deafened','doomed','drained','enfeebled','fascinated','fatigued','fleeing','frightened','grabbed','immobilized','off-guard','paralyzed','petrified','prone','quickened','restrained','sickened','slowed','stunned','stupefied','unconscious','wounded','invisible','hidden']
ranks=[int(x) for x in sys.argv[1].split(',')] if len(sys.argv)>1 else sorted(RANKS)
tot=0
for r in ranks:
    for n in RANKS[r]:
        if n not in E: continue
        i=info(n); rules=(i['text']+' '+plain(str(i['area']))+' '+str(i['save'])+' '+str(i['range'])+' '+str(i['duration'])+' '+str(i['targets'])).lower().replace('- foot','-foot'); ev=E[n][2]; evl=ev.lower()
        f=[]
        for d in set(re.findall(r'\b\d+d\d+\b',evl)):
            if d not in rules: f.append('dice '+d)
        for a in set(re.findall(r'\b(\d+)-foot (burst|cone|line|emanation)',evl)):
            if f'{a[0]}-foot {a[1]}' not in rules and f'{a[0]}-foot-{a[1]}' not in rules: f.append(f'area {a[0]}-foot {a[1]}')
        for c in COND:
            if re.search(r'\b'+c+r'\b',evl) and c not in rules: f.append('cond '+c)
        for sv in ('fortitude','reflex','will'):
            if re.search(r'\b'+sv+r'\b',evl) and sv not in rules: f.append('save '+sv)
        for m in re.findall(r'\b(\d+) feet\b',evl):
            if m+' feet' not in rules and m+'-foot' not in rules and m+' foot' not in rules: f.append('dist '+m)
        if f: tot+=1; print(f'r{r} {n} [{E[n][1]}]:', '; '.join(sorted(set(f))))
print(tot,'cards flagged')
