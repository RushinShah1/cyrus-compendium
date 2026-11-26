import re
rows=[l.rstrip('\n').split('\t') for l in open('/home/claude/build/allspells.tsv')]
def dur_class(d):
    d=d.lower()
    if re.search(r'hour|day|unlimited|permanent|until (your|the) next (daily )?prep|until the next time you make', d): return 'long'
    if re.search(r'10 minutes|20 minutes|minutes', d): return 'mid'
    return 'short'
def default(rk,n,trad,codes,dur,r,g,ss):
    if rk=='0': return None
    R=[int(c) for c in r]; Dm,Ct,Db,Bf,Ps,Ut=R
    codes=codes.split(); dc=dur_class(dur)
    top=max(R)
    if codes==['r']: return ('D','D')
    combat = max(Dm,Ct,Db) >= max(Bf,Ut) and max(Dm,Ct,Db)>0
    if 'long' in codes and codes==['long']:
        v=max(Ut,Bf,Ps)
        s={5:'A',6:'A',4:'A',3:'B',2:'C'}.get(v,'D')
        w='B' if (dc=='long' and v>=3) else ('C' if v>=2 else 'D')
        return (s,w)
    if not combat:
        if Ut>=max(Bf,Ps) and Ut>0:
            s={6:'A',5:'A',4:'A',3:'B',2:'C'}.get(Ut,'D')
            w='B' if dc=='long' and Ut>=3 else 'C' if Ut>=2 else 'D'
            return (s,w)
        if Bf>=Ps:
            if Bf<=1: return ('D','D')
            if dc=='long': return ('B' if Bf>=4 else 'C','A' if Bf>=3 else 'B')
            if dc=='mid': return ('B' if Bf>=3 else 'C','B' if Bf>=4 else 'C')
            return ('C' if Bf>=4 else 'D','C' if Bf>=5 else 'D')
        # positioning
        if dc in ('mid','long'): return ('B','C')
        return ('C','D')
    if Dm>=max(Ct,Db): return ('D','D')
    return ('C','C') if max(Ct,Db)>=5 else ('D','D')
OV_S={ # scroll overrides
 'Gentle Breeze':'C',
 'Translocate':'B','Time Beacon':'D','Roar of Freedom':'C','Sure Strike':'D','Wall of Wind':'B','Dispelling Globe':'B','Darkvision':'C',
 'Mystic Armor':'D','Darkness':'D','Sleep':'B',
 'Gentle Landing':'C','Gust of Wind':'A','Earthbind':'A','Revealing Light':'A','Dispel Magic':'A','See the Unseen':'A',
 'Ghostly Weapon':'A','Water Breathing':'A','Knock':'A','Translate':'A','Illusory Disguise':'A','Illusory Object':'A',
 'Pest Form':'A','Clairvoyance':'A','Sending':'A','Teleport':'A','Magic Passage':'A','Banishment':'A','Shared Invisibility':'A',
 'Clear Mind':'A','Cleanse Affliction':'B','Sound Body':'A','Shock to the System':'S','Truesight':'A','Unfettered Movement':'B',
 'Spell Immunity':'B','Wall of Force':'B','Wall of Stone':'B','Synesthesia':'B','Mind Reading':'A','Locate':'B','Scrying':'A',
 'Pinpoint':'A','Mind Probe':'A','Truespeech':'A','Retrocognition':'A','Interplanar Teleport':'A','Hallucination':'A',
 'Suggestion':'B','Charm':'B','Humanoid Form':'B','Creation':'B','Fly':'B','Helpful Steps':'A','Friendfetch':'B',
 'Ethereal Jaunt':'A','Silence':'A','Calm':'B','Sanctuary':'B','Death Ward':'B','Tortoise and the Hare':'B',
 'Invisibility':'A','Darkvision':'C','Planar Tether':'B','Dream Message':'B','Telepathic Bond':'B','Umbral Journey':'B',
 'Resist Energy':'B','Heroism':'B','Mountain Resilience':'B','Energy Aegis':'C','Dimensional Anchor':'B',
 'Hypercognition':'B','Status':'C','Augury':'B','Read Omens':'B','Honeyed Words':'B',
}
OV_W={
 'Time Beacon':'D','Roar of Freedom':'C','Sure Strike':'D','Spell Immunity':'B',
 'Mystic Armor':'D','Darkness':'D',
 'Tailwind':'S','Lucky Number':'A','False Vitality':'A','Energy Aegis':'A','See the Unseen':'A','Darkvision':'A','Alarm':'A',
 'Environmental Endurance':'B','Pocket Library':'A','Gentle Breeze':'A','Soothe':'B','Mountain Resilience':'B','Resist Energy':'B',
 'Heroism':'B','Translate':'B','Invisibility':'B','Illusory Disguise':'B','Synesthesia':'B','Hypercognition':'A',
 'Haste':'C','Slow':'C','Fear':'C','Sound Body':'B','Shock to the System':'A','Protection':'C','Liberating Command':'C',
 'Zealous Conviction':'B','Status':'B','Water Breathing':'C','Fleet Step':'C','Clear Mind':'C','Pest Form':'B',
}
out={}
for row in rows:
    d=default(*row)
    if d is None: continue
    n=row[1]; s,w=d
    s=OV_S.get(n,s); w=OV_W.get(n,w)
    out[n]=(s,w)
if __name__=='__main__':
    for row in rows:
        n=row[1]
        if n in out:
            old=row[6][1:3]; new=''.join(out[n])
            print(f"{row[0]} {n:32} {row[5]} {row[4][:14]:14} {row[3]:6} old {old} new {new}{'  *' if old!=new else ''}")
