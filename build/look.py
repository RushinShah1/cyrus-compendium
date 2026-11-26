import pickle,json,sys,re
idx=pickle.load(open('/home/claude/build/idx.pkl','rb'))
def get(name,pack=None,remaster=None):
    out=[]
    for p,f in idx.get(name.lower(),[]):
        if pack and p!=pack: continue
        d=json.load(open(f)); out.append(d)
    return out
if __name__=='__main__':
    for n in sys.argv[1:]:
        for d in get(n):
            s=d['system']; pub=s.get('publication',{})
            print('##',d['name'],d['type'],'L',s.get('level',{}).get('value'),pub.get('title'),'remaster' if pub.get('remaster') else 'legacy', s.get('traits',{}).get('value'), s.get('traits',{}).get('traditions'))
            print('  prereq:',[x.get('value') for x in s.get('prerequisites',{}).get('value',[])] if isinstance(s.get('prerequisites'),dict) else '')
            print('  ',re.sub('<[^>]+>','',s['description']['value'])[:700].replace('\n',' '))
