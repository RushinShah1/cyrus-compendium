import re,html,sys
def cards(p):
    s=open(p).read(); out={}
    for m in re.finditer(r'<article class="card" id="(sp-[^"]*)"([^>]*)>(.*?)</article>',s,flags=re.S):
        attrs=dict(re.findall(r'(data-[a-z]+)="([^"]*)"',m.group(2))); body=m.group(3)
        name=html.unescape(attrs.get('data-name',''))
        url=re.search(r'<h3 class="cn"><a href="([^"]*)"',body)
        bds=re.findall(r'class="bd (b-[a-z]+)"',body)
        tr=[html.unescape(x) for x in re.findall(r'<a class="trait[^"]*"[^>]*>([^<]*)</a>',body)]
        src=re.search(r'<span class="src">(?:<svg.*?</svg>)?([^<]*)</span>',body,flags=re.S)
        rules=re.search(r'<section class="rt">(.*?)</section>',body,flags=re.S)
        out[m.group(1)]=dict(name=name,attrs=attrs,url=url.group(1) if url else None,bds=bds,traits=tr,src=src.group(1) if src else '',
                             text=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',rules.group(1)))).strip() if rules else '', raw=body)
    return out
if __name__=='__main__':
    a=cards(sys.argv[1]); b=cards(sys.argv[2])
    print(len(a),len(b),'only before:',set(a)-set(b),'only after:',set(b)-set(a))
    ks=sorted(set(a[next(iter(a))]['attrs'])|set(b[next(iter(b))]['attrs'])); print(ks)
    from collections import Counter
    c=Counter()
    for k in a:
        if k not in b: continue
        x,y=a[k],b[k]
        for at in ks:
            if at=='data-traits': continue
            if x['attrs'].get(at)!=y['attrs'].get(at): c[at]+=1; print(f"{x['name']}: {at}: {x['attrs'].get(at)!r} -> {y['attrs'].get(at)!r}")
        if x['bds']!=y['bds']: c['badges']+=1; print(f"{x['name']}: badges {x['bds']} -> {y['bds']}")
    print(c)
