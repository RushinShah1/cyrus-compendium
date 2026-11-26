import re, glob, html, collections, sys
from urllib.parse import unquote_plus
import aon_index
bu, bn, bid = aon_index.load()
LINK = re.compile(r'\]\((/[A-Za-z]+\.aspx\?ID=\d+)[^)]*\)|url="(/[A-Za-z]+\.aspx\?ID=\d+)"', re.I)
SKIP = {'sources'}
def links_in(doc):
    out=set()
    for a,b in LINK.findall(doc.get('markdown') or ''):
        k=aon_index.norm(a or b)
        if k.split('-')[0] not in SKIP: out.add(k)
    return out
def seeds():
    s=set(); q=set()
    for f in glob.glob('/home/claude/site/pages/*.html'):
        h=open(f).read()
        for u in re.findall(r'href="https://2e\.aonprd\.com(/[^"]+)"', h):
            u=html.unescape(u)
            if 'Search.aspx' in u:
                m=re.search(r'q=([^&]+)',u); q.add(unquote_plus(m.group(1)) if m else '')
            else:
                s.add(aon_index.norm(u))
    return s,q
if __name__=='__main__':
    s,q=seeds(); print('direct',len(s),'search',len(q))
    miss=[k for k in s if k not in bu]; print('unresolved direct',len(miss),collections.Counter(k.split('-')[0] for k in miss))
    level=set(k for k in s if k in bu); seen=set(level)
    for d in range(1,5):
        nxt=set()
        for k in level: nxt|=links_in(bu[k])
        nxt={k for k in nxt if k in bu}-seen
        seen|=nxt; level=nxt
        size=sum(len(bu[k]['markdown'] or '') for k in seen)
        print('depth',d,'new',len(nxt),'total',len(seen),'MB',round(size/1e6,1),collections.Counter(k.split('-')[0] for k in nxt).most_common(8))
