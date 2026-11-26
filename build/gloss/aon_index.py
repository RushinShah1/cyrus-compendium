import json, glob, os, re, pickle
D = '/home/claude/ext/aon/2e/data'
CACHE = '/home/claude/build/gloss/aon_index.pkl'
KEEP = ('id', 'name', 'url', 'markdown', 'category', 'type', 'summary', 'remaster_id', 'legacy_id', 'primary_source', 'rarity',
        'release_date', 'trait_raw', 'level', 'actions')
# when several documents share one Archives of Nethys URL, the page's own entry wins over sidebars, class features shown on a
# class page, item-bonus catalogue rows and category pages
SECONDARY = {'sidebar': 5, 'item-bonus': 4, 'class-feature': 3, 'category-page': 2, 'class-sample': 3, 'class-kit': 3}
VARIANT = re.compile(r'\((?:lesser|minor|moderate|greater|major|true|standard|grand|supreme|type [ivx]+|\d+(?:st|nd|rd|th)[- ]rank)\)\s*$', re.I)


def norm(u):
    u = u.replace('https://2e.aonprd.com', '')
    m = re.match(r'/?([A-Za-z]+)\.aspx\?(?:ID|Id|id)=(\d+)', u)
    if m:
        return f'{m.group(1).lower()}-{m.group(2)}'
    return u.lower()


def _rank(x):
    n = re.findall(r'\d+', x.get('id') or '')
    return (SECONDARY.get(x.get('category'), 0), 1 if VARIANT.search(x.get('name') or '') else 0, int(n[0]) if n else 0)


def load():
    """by_url: key -> document. Keys are the normalised URL for each URL's main document and 'd:<id>' for every other
    document that shares a URL (equipment variants, sidebars, class features). by_name: lower name -> keys. by_id: id -> key."""
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE, 'rb'))
    groups = {}
    for f in sorted(glob.glob(D + '/*.json')):
        if f.endswith('manifest.json'):
            continue
        try:
            docs = json.load(open(f))
        except Exception:
            continue
        if not isinstance(docs, list):
            continue
        for x in docs:
            u = x.get('url')
            if not u:
                continue
            groups.setdefault(norm(u), []).append({k: x.get(k) for k in KEEP})
    by_url, by_name, by_id = {}, {}, {}
    for uk, docs in groups.items():
        docs.sort(key=_rank)
        for i, d in enumerate(docs):
            key = uk if i == 0 else 'd:' + (d.get('id') or f'{uk}-{i}')
            by_url[key] = d
            by_name.setdefault((d.get('name') or '').lower(), []).append(key)
            if d.get('id'):
                by_id[d['id']] = key
    pickle.dump((by_url, by_name, by_id), open(CACHE, 'wb'))
    return by_url, by_name, by_id
