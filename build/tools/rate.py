"""Rating reference: one compact block per spell card, with figures taken from the Archives of Nethys text."""
import sys, re, json
from aonrules import *
from occult_list import OCCULT
DICE = re.compile(r'(\d+)d(\d+)(?:\s*\+\s*(\d+))?')
COND = ['blinded','clumsy','confused','controlled','dazzled','deafened','doomed','drained','enfeebled','fascinated','fatigued','fleeing','frightened','grabbed','immobilized','off-guard','paralyzed','petrified','prone','restrained','sickened','slowed','stunned','stupefied','unconscious','concealed','hidden','invisible','quickened','persistent','pushed','pulled','difficult terrain','temporary Hit Points','resistance','weakness','teleport','status bonus','circumstance bonus','status penalty','circumstance penalty','Speed','fly','can\'t use reactions','reaction','wall','heal','regain','counteract']
def avg(s):
    return sum(int(a)*(int(b)+1)/2+int(c or 0) for a,b,c in DICE.findall(s))
def dmg_of(seg):
    """(instant, persistent) from sentences mentioning damage"""
    inst=pers=0.0
    for m in DICE.finditer(seg):
        tail=seg[m.end():m.end()+45]; 
        if 'damage' not in tail and 'damage' not in seg[max(0,m.start()-25):m.start()]: continue
        v=int(m.group(1))*(int(m.group(2))+1)/2+int(m.group(3) or 0)
        if re.match(r'\s*persistent',tail) or 'persistent' in tail[:22]: pers+=v
        else: inst+=v
    return inst,pers
def conds(seg):
    return ','.join(c for c in COND if re.search(r'\b'+re.escape(c),seg,re.I))
def feat(n):
    i=info(n); t=i['text']; body,_,h=t.partition('Heightened')
    # action versions
    two=body
    if '[Two Actions]' in body and ('[Single Action]' in body or '[Three Actions]' in body):
        m=re.search(r'\[Two Actions\](.*?)(?=\[Three Actions\]|\[Single Action\]|$)',body)
        two=body[:body.find('[')]+' '+(m.group(1) if m else '')
    parts=re.split(r'(Critical Success|Critical Failure|Success|Failure)(?= )',two)
    head=parts[0]; out={}
    for k in range(1,len(parts)-1,2): out.setdefault(parts[k],parts[k+1])
    attack='Attack' in i['traits'] or (i['save'] or '')=='AC'
    basic='basic' in (i['save'] or '').lower() or 'basic' in head.lower()
    hd=dmg_of(head)
    if attack and 'Success' in out and sum(dmg_of(out['Success'])): d=dmg_of(out['Success']); src='hit'
    elif not attack and 'Failure' in out and sum(dmg_of(out['Failure'])) and not sum(hd): d=dmg_of(out['Failure']); src='fail'
    else: d=hd; src='text'
    return i,d,src,attack,basic,out,head,h
def area_factor(a):
    a=plain(a or '').lower()
    m=re.search(r'(\d+)-foot[- ]+(burst|cone|line|emanation)',a)
    if not m: return 1.0
    size=int(m.group(1)); sh=m.group(2)
    if sh=='burst': return 1.5 if size<=10 else 2.0 if size<=20 else 2.5
    if sh=='cone': return 1.5 if size<=15 else 2.0 if size<=30 else 2.5
    if sh=='line': return 1.5 if size<=30 else 1.75
    return 1.5 if size<=10 else 2.0
def show(n, rank):
    try: i,d,src,attack,basic,out,head,h=feat(n)
    except Exception as ex: print('##',n,'ERR',ex); return
    r,g,_=E[n]
    A={'Single Action':'1','Two Actions':'2','Three Actions':'3','Reaction':'R','Free Action':'F',' to ':'-',' or ':'/'}
    act=i['actions'] or ''
    for k,v in A.items(): act=act.replace(k,v)
    af=area_factor(i['area'] or ''); 
    if af==1.0 and not i['area']:
        m=re.search(r'\d+-foot[- ]+(?:burst|cone|line|emanation)',head)
        if m: af=area_factor(m.group(0))
    eff=(d[0]+2*d[1])*af*(1.0 if (attack or basic) else 0.85)
    bench=7*max(rank,1) if rank>0 else 5.5
    ratio=eff/bench
    star=5 if ratio>=1.6 else 4 if ratio>=1.15 else 3 if ratio>=0.8 else 2 if ratio>=0.45 else 1 if ratio>0 else 0
    tr=','.join(t for t in i['traits'] if t not in ('Concentrate','Manipulate','Cantrip','Uncommon','Rare'))
    def short(x,k): 
        x=str(x or ''); return x if len(x)<=k else x[:k-1]+'~'
    oc=' | '.join(f"{'S' if k=='Success' else 'F' if k=='Failure' else 'CF'}: {conds(v)}" for k,v in out.items() if k!='Critical Success' and conds(v))
    print(f"## {n} [{r} {g}] {act}a|{short(tr,34)}|{('AC' if attack else i['save'] or '-')}{' basic' if basic and 'basic' not in (i['save'] or '') else ''}|{short(i['area'],22)}|{short(i['range'],9)}|{short(i['targets'],26)}|{short(i['duration'],14)}")
    print(f"   D {d[0]:.0f}+{d[1]:.0f}p x{af}={ratio:.2f}>{star} H:{h[:48].strip()} :: {conds(head)}" + (f" || {oc}" if oc else ''))
if __name__=='__main__':
    rank=int(sys.argv[1]); which=sys.argv[2] if len(sys.argv)>2 else 'arcane'
    names=[n for n in (RANKS[rank] if which=='arcane' else OCCULT[rank]) if n in E]
    lo=int(sys.argv[3]) if len(sys.argv)>3 else 0; hi=int(sys.argv[4]) if len(sys.argv)>4 else 999
    print(f'rank {rank} {which}: {len(names)}')
    for n in names[lo:hi]: show(n,rank)
