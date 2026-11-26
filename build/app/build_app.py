"""Home-screen app files: icon set, per-icon manifests, service worker with a full precache list."""
import re, os, json, hashlib, asyncio, glob
SITE = '/home/claude/site'
GI = '/home/claude/ext/game-icons'
ICONS = [
    ('charcoal-gold', 'Charcoal and gold', 'lorc/spinning-sword', 'radial-gradient(circle at 50% 38%, #34323a 0%, #1b1b1f 62%, #121215 100%)', '#e2c27d', '#e2c27d33'),
    ('violet-shadow', 'Violet shadow', 'lorc/domino-mask', 'linear-gradient(160deg, #3b2d57 0%, #1d1729 55%, #0f0c16 100%)', '#cbb8f0', '#cbb8f02e'),
    ('midnight-blue', 'Midnight blue', 'delapouite/glaive', 'radial-gradient(circle at 30% 25%, #2b3d5c 0%, #172236 55%, #0c121d 100%)', '#b9cce6', '#b9cce62b'),
    ('parchment', 'Parchment', 'delapouite/glaive', 'radial-gradient(circle at 50% 40%, #f3ead6 0%, #e4d5b4 70%, #cdb98f 100%)', '#3a2f22', '#3a2f2224'),
    ('crimson', 'Crimson', 'lorc/crescent-blade', 'linear-gradient(150deg, #5a1d22 0%, #35111a 60%, #1c090e 100%)', '#ecc98b', '#ecc98b2e'),
    ('emerald', 'Emerald', 'lorc/ink-swirl', 'radial-gradient(circle at 50% 35%, #1f4a3d 0%, #12302a 60%, #0a1c18 100%)', '#a9e0c8', '#a9e0c82b'),
]


def glyph(path):
    svg = open(f'{GI}/{path}.svg').read()
    body = re.sub(r'^<svg[^>]*>|</svg>\s*$', '', svg.strip()).replace('<path d="M0 0h512v512H0z"/>', '')
    return re.sub(r'\sfill="#fff"', '', body)


def icon_html(bg, fill, ring, g, size):
    return f'''<div id="ic" style="width:{size}px;height:{size}px;background:{bg};display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden">
<div style="position:absolute;inset:{size*0.1}px;border-radius:50%;border:{max(2,size*0.012)}px solid {ring}"></div>
<svg viewBox="0 0 512 512" width="{size*0.56}" height="{size*0.56}" style="fill:{fill};filter:drop-shadow(0 {size*0.012}px {size*0.03}px rgba(0,0,0,.35))">{g}</svg></div>'''


async def render_icons():
    from playwright.async_api import async_playwright
    os.makedirs(SITE + '/icons', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 600, 'height': 600})
        for key, label, gp, bg, fill, ring in ICONS:
            g = glyph(gp)
            for size in (180, 512):
                await pg.set_content(f'<html><body style="margin:0;background:transparent">{icon_html(bg, fill, ring, g, size)}</body></html>')
                await pg.locator('#ic').screenshot(path=f'{SITE}/icons/{key}-{size}.png')
        await b.close()


def manifests():
    os.makedirs(SITE + '/manifests', exist_ok=True)
    for key, label, *_ in ICONS:
        m = {'name': 'Aspera', 'short_name': 'Aspera', 'start_url': '../index.html#home', 'scope': '../',
             'display': 'standalone', 'background_color': '#1b1b1f', 'theme_color': '#1b1b1f',
             'icons': [{'src': f'../icons/{key}-180.png', 'sizes': '180x180', 'type': 'image/png'},
                       {'src': f'../icons/{key}-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'}]}
        json.dump(m, open(f'{SITE}/manifests/{key}.webmanifest', 'w'), indent=1)
    d = json.load(open(f'{SITE}/manifests/{ICONS[0][0]}.webmanifest'))
    d['start_url'] = 'index.html#home'; d['scope'] = './'
    for i in d['icons']:
        i['src'] = i['src'].replace('../', '')
    json.dump(d, open(f'{SITE}/manifest.webmanifest', 'w'), indent=1)
    json.dump([{'key': k, 'label': l} for k, l, *_ in ICONS], open(f'{SITE}/icons/icons.json', 'w'))


SW_TEMPLATE = r'''// Offline cache for Aspera. Each file is cached under its own content hash, so an update downloads only the files
// that changed. Version @VER@.
const FILES = @FILES@;
const CACHE = 'aspera-files';
const SCOPE = new URL('./', self.location).pathname;
const key = p => new URL(p + '?v=' + FILES[p], self.location).href;
async function tell(msg){
  const cs = await self.clients.matchAll({includeUncontrolled: true});
  cs.forEach(c => c.postMessage(msg));
}
self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    const paths = Object.keys(FILES), todo = [];
    let done = 0;
    for (const p of paths) { if (await c.match(key(p))) done++; else todo.push(p); }
    const total = paths.length;
    tell({type: 'progress', done, total});
    let i = 0, failed = 0;
    async function worker(){
      while (i < todo.length) {
        const p = todo[i++];
        let ok = false;
        for (let t = 0; t < 3 && !ok; t++) {
          try { const r = await fetch(p, {cache: 'no-cache'}); if (r.ok) { await c.put(key(p), r); ok = true; } } catch (err) {}
        }
        if (!ok) failed++;
        done++;
        if (done % 5 === 0 || done === total) tell({type: 'progress', done, total});
      }
    }
    await Promise.all(Array.from({length: 6}, worker));
    if (failed) throw new Error(failed + ' files could not be saved');
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', e => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k !== CACHE) await caches.delete(k);
    const c = await caches.open(CACHE), keep = new Set(Object.keys(FILES).map(key));
    for (const req of await c.keys()) if (!keep.has(req.url)) await c.delete(req);
    await self.clients.claim();
    tell({type: 'ready'});
  })());
});
self.addEventListener('message', e => { if (e.data === 'status') e.waitUntil((async () => {
  const c = await caches.open(CACHE); let n = 0;
  for (const p of Object.keys(FILES)) if (await c.match(key(p))) n++;
  e.source.postMessage({type: 'status', done: n, total: Object.keys(FILES).length});
})()); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin || !url.pathname.startsWith(SCOPE)) return;
  let rel = decodeURIComponent(url.pathname.slice(SCOPE.length)) || './';
  if (e.request.mode === 'navigate') rel = 'index.html';
  if (!FILES[rel]) return;
  e.respondWith(caches.open(CACHE).then(c => c.match(key(rel))).then(hit => hit || fetch(e.request)));
});
'''


def service_worker():
    files = {}
    for f in sorted(glob.glob(SITE + '/**/*', recursive=True)):
        if os.path.isfile(f) and not f.endswith('sw.js') and '/.git' not in f:
            rel = os.path.relpath(f, SITE)
            files[rel] = hashlib.sha256(open(f, 'rb').read()).hexdigest()[:10]
    files['./'] = files['index.html']
    ver = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()[:12]
    sw = SW_TEMPLATE.replace('@VER@', ver).replace('@FILES@', json.dumps(files, separators=(',', ':')))
    open(SITE + '/sw.js', 'w').write(sw)
    print('sw version', ver, 'files', len(files), 'MB', round(sum(os.path.getsize(SITE + '/' + f) for f in files if f != './') / 1e6, 1))


if __name__ == '__main__':
    import sys
    if '--icons' in sys.argv or not os.path.exists(SITE + '/icons/charcoal-gold-180.png'):
        asyncio.run(render_icons())
    manifests()
    service_worker()
