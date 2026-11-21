{
const DOCS = ['home','sheet','spells','feats','aspera','items','consumables','combat','atlas','rules','glossary'];
const main = document.getElementById('main');
const cache = {};
let current = null;

function setActive(name){
  document.querySelectorAll('.rail a.doc').forEach(a => a.classList.toggle('on', a.dataset.doc === name));
}

async function load(name){
  if (!DOCS.includes(name)) name = 'home';
  if (current === name) return;
  current = name;
  setActive(name);
  try {
    if (!cache[name]) {
      const r = await fetch('pages/' + name + '.html');
      cache[name] = await r.text();
    }
    closeAll();
    main.innerHTML = cache[name];
  } catch (e) {
    main.innerHTML = '<p class="muted">This page could not be loaded. Reload to try again.</p>';
    return;
  }
  window.scrollTo(0, 0);
  if (name === 'spells') initSpells();
  if (name === 'items' || name === 'consumables') initCatalog();
  if (name === 'glossary') initGlossary();
  if (name === 'rules') initRules();
  if (name === 'home') initAppSettings();
  if (name === 'sheet') initSheet();
  document.title = (main.querySelector('h1')?.textContent || 'Aspera') + ' · Aspera';
}

function route(){ load((location.hash || '#home').slice(1)); }
window.addEventListener('hashchange', route);

// ───────── stacked detail panels ─────────
// Cards and rules glossary entries open in panels that stack: side panels on wide screens, bottom sheets on phones.
const stack = document.createElement('div');
stack.className = 'pstack';
const scrim = document.createElement('div');
scrim.className = 'pscrim'; scrim.hidden = true;
document.body.append(scrim, stack);
const panels = [];
const MAXP = 15;
// The glossary is an index of names and types plus text shards that load when an entry is opened.
let GIDX = null;
const SHARDS = {};
function loadIndex(){
  if (!GIDX) GIDX = fetch('assets/g/index.json').then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).catch(e => { GIDX = null; throw e; });
  return GIDX;
}
function loadShard(i){
  if (!SHARDS[i]) SHARDS[i] = fetch('assets/g/s' + i + '.json').then(r => { if (!r.ok) throw new Error(r.status); return r.json(); }).catch(e => { delete SHARDS[i]; throw e; });
  return SHARDS[i];
}
function gname(I, k){ return I.e[k] ? I.e[k][0] : ''; }
async function getEntry(key){
  const I = await loadIndex();
  const r = I.e[key];
  if (!r) return null;
  let src = key, row = r, guard = 0;
  while (typeof row[2] === 'string' && guard++ < 4) { src = row[2]; row = I.e[src]; if (!row) return null; }
  const sh = await loadShard(row[2]);
  const t = sh[src];
  if (!t) return null;
  return [r[0], I.t[r[1]], t[0], r[3] ? 'legacy' : '', t[1] || null];
}
function esc(t){ return String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
const AONPATH = {traits:'Traits',conditions:'Conditions',rules:'Rules',actions:'Actions',spells:'Spells',equipment:'Equipment',feats:'Feats',
  skills:'Skills',weapons:'Weapons',classes:'Classes',relics:'Relics',hybridstudies:'HybridStudies',backgrounds:'Backgrounds',heritages:'Heritages',mythicspells:'MythicSpells'};
const FRT = 'Deity (Forgotten Realms)';
function aonUrl(key, name){
  if (key.startsWith('fr:')) return null;   // Forgotten Realms deities are not on Archives of Nethys
  const m = key.match(/^([a-z]+)-(\d+)$/);
  if (m && AONPATH[m[1]]) return `https://2e.aonprd.com/${AONPATH[m[1]]}.aspx?ID=${m[2]}`;
  return 'https://2e.aonprd.com/Search.aspx?q=' + encodeURIComponent(name);
}
function layout(){
  const n = panels.length;
  panels.forEach((p, i) => {
    const d = n - 1 - i;
    p.style.setProperty('--d', Math.min(d, 4));
    p.classList.toggle('top', d === 0);
    p.classList.toggle('hidden-deep', d > 3);
    p.setAttribute('aria-hidden', d === 0 ? 'false' : 'true');
    p.querySelector('.pback').hidden = n < 2 || d !== 0;
    p.querySelector('.pall').hidden = n < 2 || d !== 0;
  });
  document.body.classList.toggle('ps-open', n > 0);
  scrim.hidden = n === 0;
}
function pushPanel(kicker, title, node, key, ext){
  const top = panels[panels.length - 1];
  if (key && top && top.dataset.key === key) return;
  const p = document.createElement('aside');
  p.className = 'spanel'; p.setAttribute('role', 'dialog'); p.setAttribute('aria-label', title);
  if (key) p.dataset.key = key;
  p.innerHTML = '<div class="pbar"><button class="pback" type="button">Back</button><div class="ptitle"><span class="pk"></span><b class="pn"></b></div>'
    + '<button class="pall" type="button">Close all</button><button class="px" type="button" aria-label="Close">Close</button></div><div class="pbody"></div>';
  p.querySelector('.pk').textContent = kicker || '';
  p.querySelector('.pn').textContent = title || '';
  const body = p.querySelector('.pbody');
  body.appendChild(node);
  if (ext) {
    const f = document.createElement('p'); f.className = 'pext muted small';
    f.innerHTML = `<a href="${ext}" target="_blank" rel="noopener">Open on Archives of Nethys</a> (needs a connection)`;
    body.appendChild(f);
  }
  panels.push(p); stack.appendChild(p);
  while (panels.length > MAXP) panels.shift().remove();
  layout();
  requestAnimationFrame(() => p.classList.add('in'));
  p.querySelector('.px').focus({preventScroll: true});
  swipe(p);
}
function popPanel(){ const p = panels.pop(); if (p) p.remove(); layout(); if (panels.length) panels[panels.length-1].querySelector('.px').focus({preventScroll:true}); }
function closeAll(){ while (panels.length) panels.pop().remove(); layout(); }
function closeDrawer(){ closeAll(); }
stack.addEventListener('click', e => {
  const p = e.target.closest('.spanel');
  if (!p) return;
  if (!p.classList.contains('top')) {           // a panel peeking underneath: bring it back to the top
    e.preventDefault(); e.stopPropagation();
    while (panels.length && panels[panels.length - 1] !== p) popPanel();
    return;
  }
  if (e.target.closest('.px')) popPanel();
  else if (e.target.closest('.pback')) popPanel();
  else if (e.target.closest('.pall')) closeAll();
}, true);
scrim.addEventListener('click', popPanel);
document.addEventListener('keydown', e => { if (e.key === 'Escape' && panels.length) popPanel(); });
function swipe(p){
  const bar = p.querySelector('.pbar'); let y0 = null, dy = 0;
  bar.addEventListener('touchstart', e => { if (!matchMedia('(max-width: 760px)').matches) return; y0 = e.touches[0].clientY; dy = 0; p.style.transition = 'none'; }, {passive: true});
  bar.addEventListener('touchmove', e => { if (y0 === null) return; dy = Math.max(0, e.touches[0].clientY - y0); p.style.transform = `translateY(${dy}px)`; }, {passive: true});
  bar.addEventListener('touchend', () => { if (y0 === null) return; p.style.transition = ''; p.style.transform = ''; if (dy > 90) popPanel(); y0 = null; });
}
function openCard(card){
  const c = card.cloneNode(true);
  c.removeAttribute('id'); c.classList.remove('hide', 'flash');
  const kick = c.querySelector('.kick')?.textContent || 'Compendium';
  const name = c.querySelector('h3.cn, h3')?.textContent?.trim() || '';
  pushPanel(kick, name, c, 'card:' + card.id);
}
async function openGloss(key, fallbackHref, replace){
  let e;
  try { e = await getEntry(key); } catch (err) { e = null; }
  if (!e) { if (fallbackHref) window.open(fallbackHref, '_blank', 'noopener'); return; }
  const d = document.createElement('div'); d.className = 'gentry rt';
  const nav = e[4];
  let crumbs = '', sections = '', pager = '';
  if (nav) {
    const I = await loadIndex();
    const name = k => gname(I, k);
    const chain = []; let p = nav.p, guard = 0;
    const navOf = async k => { const x = await getEntry(k).catch(() => null); return x && x[4]; };
    while (p && guard++ < 12) { chain.unshift(p); const n2 = await navOf(p); p = n2 ? n2.p : null; }
    crumbs = `<nav class="gcrumbs" aria-label="Location"><span>${esc(nav.b)}</span>` + chain.map(k => ` › <a href="#" data-g="${k}">${esc(name(k))}</a>`).join('') + '</nav>';
    if (nav.c && nav.c.length) sections = '<h5 class="sub">Sections</h5><ul class="gsections">' + nav.c.map(k => `<li><a href="#" data-g="${k}">${esc(name(k))}</a></li>`).join('') + '</ul>';
    const pv = nav.pv && I.e[nav.pv] ? `<button type="button" class="chip" data-gr="${nav.pv}">‹ ${esc(name(nav.pv))}</button>` : '<span></span>';
    const nx = nav.nx && I.e[nav.nx] ? `<button type="button" class="chip" data-gr="${nav.nx}">${esc(name(nav.nx))} ›</button>` : '<span></span>';
    pager = `<div class="gpager">${pv}${nx}</div>`;
  }
  d.innerHTML = crumbs + e[2] + sections + pager;
  if (replace && panels.length) { const t = panels.pop(); t.remove(); }
  pushPanel(e[1] + (e[3] ? ' · legacy printing' : ''), e[0], d, key, aonUrl(key, e[0]));
}

// cards that live on another page open in a panel too
const parsed = {};
async function findElsewhere(id){
  for (const d of DOCS){
    if (!parsed[d]){
      if (!cache[d]) { try { cache[d] = await (await fetch('pages/' + d + '.html')).text(); } catch (e) { continue; } }
      parsed[d] = new DOMParser().parseFromString(cache[d], 'text/html');
    }
    const c = parsed[d].getElementById(id);
    if (c && c.classList.contains('card')) return c;
  }
  return null;
}

document.addEventListener('click', ev => {
  const r = ev.target.closest('[data-gr]');
  if (r) { ev.preventDefault(); openGloss(r.dataset.gr, null, true); return; }
  const g = ev.target.closest('a[data-g]');
  if (g) { ev.preventDefault(); openGloss(g.dataset.g, g.href); return; }
  const a = ev.target.closest('a[data-to]');
  if (!a) return;
  ev.preventDefault();
  const el = document.getElementById(a.dataset.to);
  const inPanel = a.closest('.spanel');
  if (!el || inPanel) { (el && el.classList.contains('card') ? Promise.resolve(el) : findElsewhere(a.dataset.to)).then(c => { if (c) openCard(c); }); return; }
  if (el.classList.contains('card')) { openCard(el); return; }
  el.classList.remove('hide');
  el.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'});
});

// ───────── home-screen app ─────────
const SW_OK = 'serviceWorker' in navigator && (/github\.io$/.test(location.hostname) || location.hostname === 'localhost');
if (SW_OK) navigator.serviceWorker.register('sw.js').catch(() => {});
function setIcon(k){
  try { localStorage.setItem('cyrus-icon', k); } catch (e) {}
  document.getElementById('app-touch-icon')?.setAttribute('href', 'icons/' + k + '-180.png');
  document.getElementById('app-favicon')?.setAttribute('href', 'icons/' + k + '-180.png');
  document.getElementById('app-manifest')?.setAttribute('href', 'manifests/' + k + '.webmanifest');
}
function setLook(v){
  try { localStorage.setItem('cyrus-look', v); } catch (e) {}
  if (v === 'basic') document.documentElement.setAttribute('data-look', 'basic'); else document.documentElement.removeAttribute('data-look');
}
function initAppSettings(){
  const lp = main.querySelector('.lookpick');
  if (lp) {
    const cur = document.documentElement.getAttribute('data-look') === 'basic' ? 'basic' : 'illustrated';
    lp.querySelectorAll('[data-look]').forEach(b => { b.classList.toggle('on', b.dataset.look === cur); b.setAttribute('aria-checked', b.dataset.look === cur); });
    lp.addEventListener('click', e => {
      const b = e.target.closest('[data-look]'); if (!b) return;
      setLook(b.dataset.look);
      lp.querySelectorAll('[data-look]').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-checked', x === b); });
    });
  }
  const box = main.querySelector('#iconpick'), status = main.querySelector('#offline-status');
  if (!box) return;
  let cur = 'charcoal-gold';
  try { cur = localStorage.getItem('cyrus-icon') || cur; } catch (e) {}
  fetch('icons/icons.json').then(r => r.json()).then(list => {
    box.innerHTML = list.map(i => `<button type="button" role="radio" class="ipick${i.key === cur ? ' on' : ''}" aria-checked="${i.key === cur}" data-icon="${i.key}"><img src="icons/${i.key}-180.png" alt="" width="72" height="72"><span>${i.label}</span></button>`).join('');
  });
  box.addEventListener('click', e => {
    const b = e.target.closest('[data-icon]'); if (!b) return;
    box.querySelectorAll('.ipick').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-checked', x === b); });
    setIcon(b.dataset.icon);
  });
  const standalone = matchMedia('(display-mode: standalone)').matches || navigator.standalone;
  if (!SW_OK) status.textContent = 'Offline use works from the GitHub Pages copy of this compendium, not from this page.';
  else {
    const show = (d, t) => {
      status.textContent = d >= t ? (standalone ? 'Running as an app. Everything is saved for offline use.' : 'Everything is saved for offline use on this device.')
        : `Saving for offline use: ${d} of ${t} files. Keep the app open until this finishes.`;
    };
    status.textContent = 'Checking the offline copy…';
    navigator.serviceWorker.addEventListener('message', e => { const m = e.data || {}; if (m.type === 'progress' || m.type === 'status') show(m.done, m.total); if (m.type === 'ready') navigator.serviceWorker.controller?.postMessage('status'); });
    navigator.serviceWorker.ready.then(reg => (reg.active || navigator.serviceWorker.controller)?.postMessage('status'));
  }
}

// ───────── character sheet ─────────
window.Aspera = {pushPanel, popPanel, closeAll, openGloss: (k) => openGloss(k), getEntry};
let sheetScripts = null;
function loadScript(src){ return new Promise((ok, no) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = no; document.head.appendChild(s); }); }
function initSheet(){
  const el = main.querySelector('#cs-root');
  if (!el) return;
  if (!sheetScripts) sheetScripts = loadScript('assets/cs/engine.js').then(() => loadScript('assets/cs/sheet.js')).catch(e => { sheetScripts = null; throw e; });
  sheetScripts.then(() => window.AsperaSheet.init(el)).catch(() => { el.innerHTML = '<p class="muted">The character sheet could not be loaded. Reload to try again.</p>'; });
}

// ───────── core rules contents ─────────
function initRules(){
  const q = main.querySelector('#toc-q'), count = main.querySelector('#toc-count');
  const items = [...main.querySelectorAll('.toc li')];
  const chapters = [...main.querySelectorAll('details.toc-ch')];
  loadIndex().catch(() => {});                     // warm the cache so the first panel opens quickly
  let tmr;
  q.addEventListener('input', () => { clearTimeout(tmr); tmr = setTimeout(run, 120); });
  function run(){
    const s = q.value.trim().toLowerCase();
    if (!s) { items.forEach(li => li.hidden = false); chapters.forEach(c => { c.hidden = false; c.open = false; }); count.textContent = ''; return; }
    let n = 0;
    items.forEach(li => li.hidden = true);
    items.forEach(li => {
      const a = li.querySelector(':scope > a');
      if (a && a.textContent.toLowerCase().includes(s)) {
        n++;
        let x = li;
        while (x && x.tagName === 'LI') { x.hidden = false; x = x.parentElement.closest('li'); }
        li.querySelectorAll('li').forEach(c => c.hidden = false);
      }
    });
    chapters.forEach(c => { const any = c.querySelector('li:not([hidden])'); c.hidden = !any; c.open = !!any; });
    count.textContent = n + ' matching sections';
  }
}

// ───────── rules glossary page ─────────
function initGlossary(){
  const list = main.querySelector('#g-list'), q = main.querySelector('#g-q'), count = main.querySelector('#g-count');
  const full = main.querySelector('#g-full'), types = new Set();
  let rows = null, limit = 200, I = null, run = 0;
  const texts = {};                                  // key -> lower-case plain text, filled as shards load for full-text search
  loadIndex().then(idx => {
    I = idx;
    rows = [];
    const seen = new Set();
    for (const [k, r] of Object.entries(I.e)) {
      if (!r[0]) continue;
      const sig = r[0] + '|' + r[1] + '|' + (typeof r[2] === 'string' ? r[2] : k);
      if (seen.has(sig)) continue;
      seen.add(sig); if (typeof r[2] !== 'string') seen.add(r[0] + '|' + r[1] + '|' + k);
      if (typeof r[2] === 'string') { const t = I.e[r[2]]; if (t && t[0] === r[0] && t[1] === r[1]) continue; }
      rows.push({k, n: r[0], t: I.t[r[1]], lg: r[3], now: r[4] || '', low: r[0].toLowerCase(), src: typeof r[2] === 'string' ? r[2] : k});
    }
    rows.sort((a, b) => a.low.localeCompare(b.low));
    const tc = {}; rows.forEach(r => tc[r.t] = (tc[r.t] || 0) + 1);
    const box = main.querySelector('#g-types');
    // the campaign's Forgotten Realms deities always have their own filter at the front
    const order = Object.keys(tc).sort((a, b) => (b === FRT) - (a === FRT) || tc[b] - tc[a]);
    const chip = t => `<button class="chip mini${t === FRT ? ' fr' : ''}" type="button" data-gt="${esc(t)}">${esc(t)} <small>${tc[t]}</small></button>`;
    box.innerHTML = order.slice(0, 14).map(chip).join('') + `<button class="chip mini" type="button" id="g-more" aria-expanded="false">More types (${order.length - 14})</button><span class="gmoretypes" hidden>${order.slice(14).sort().map(chip).join('')}</span>`;
    box.querySelector('#g-more').addEventListener('click', e => { const sp = box.querySelector('.gmoretypes'); sp.hidden = !sp.hidden; e.currentTarget.setAttribute('aria-expanded', !sp.hidden); e.currentTarget.textContent = sp.hidden ? `More types (${order.length - 14})` : 'Fewer types'; });
    render();
  }).catch(err => { console.error(err); list.innerHTML = '<p class="muted">The glossary could not be loaded. Reload to try again.</p>'; });
  async function deepLoad(my){
    for (let i = 0; i < I.n; i++) {
      if (my !== run) return;
      if (texts['#' + i]) continue;
      try {
        const sh = await loadShard(i);
        for (const [k, v] of Object.entries(sh)) texts[k] = v[0].replace(/<[^>]+>/g, ' ').toLowerCase();
        texts['#' + i] = 1;
      } catch (e) {}
      if (i % 8 === 7) render(true);
    }
    render(true);
  }
  function render(fromDeep){
    if (!rows) return;
    const s = q.value.trim().toLowerCase(), deep = full.getAttribute('aria-pressed') === 'true';
    if (deep && s && !fromDeep) { run++; deepLoad(run); }
    let m = rows.filter(r => (!types.size || types.has(r.t)) && (!s || r.low.includes(s) || (deep && texts[r.src] && texts[r.src].includes(s))));
    if (s) m.sort((a, b) => (b.low.startsWith(s) - a.low.startsWith(s)) || a.low.localeCompare(b.low));
    let loaded = 0; for (let i = 0; i < I.n; i++) if (texts['#' + i]) loaded++;
    count.textContent = m.length + ' entries' + (deep && s && loaded < I.n ? ` (searched ${Math.round(100 * loaded / I.n)}% of the text so far)` : '');
    const frag = m.slice(0, limit).map(r => `<a href="#" class="gitem" data-g="${r.k}"><span>${esc(r.n)}</span><small>${esc(r.t)}${r.now ? ' · legacy, remastered as ' + esc(r.now) : r.lg ? ' · legacy' : ''}</small></a>`).join('');
    list.innerHTML = (frag || '<p class="muted">No entries match.</p>') + (m.length > limit ? `<button class="chip gmore" type="button">Show ${Math.min(200, m.length - limit)} more of ${m.length - limit}</button>` : '');
  }
  let tmr;
  q.addEventListener('input', () => { clearTimeout(tmr); tmr = setTimeout(() => { limit = 200; render(); }, 150); });
  full.addEventListener('click', () => { full.setAttribute('aria-pressed', full.getAttribute('aria-pressed') === 'true' ? 'false' : 'true'); full.classList.toggle('on'); render(); });
  main.querySelector('#g-types').addEventListener('click', e => {
    const b = e.target.closest('[data-gt]'); if (!b) return;
    types.has(b.dataset.gt) ? types.delete(b.dataset.gt) : types.add(b.dataset.gt); b.classList.toggle('on'); limit = 200; render();
  });
  main.querySelector('#g-clear').addEventListener('click', () => { run++; q.value = ''; types.clear(); full.setAttribute('aria-pressed','false'); full.classList.remove('on'); main.querySelectorAll('[data-gt].on').forEach(b => b.classList.remove('on')); limit = 200; render(); });
  list.addEventListener('click', e => { if (e.target.closest('.gmore')) { limit += 200; render(); } });
}

function initSpells(){
  const DEF = () => ({q:'', def:'all', role:'all', trad:'all', acc:'all', ss:false, stars:new Set(['4','5','6']), grades:new Set(['S','A']), acts:new Set(), ranks:new Set(), traits:new Set(), tmode:'any'});
  let st = DEF();
  const cards = [...main.querySelectorAll('.card[data-rank]')];
  const ranks = [...main.querySelectorAll('section.rank')];
  const count = main.querySelector('#spell-count');
  const starsRow = main.querySelector('#stars-row'), gradesRow = main.querySelector('#grades-row');
  const fbox = main.querySelector('#spell-filters'), fact = main.querySelector('#fact');
  const tsel = main.querySelector('#tsel'), tbtn = tsel.querySelector('.tbtn'), tpanel = tsel.querySelector('.tpanel');
  const tpills = main.querySelector('#tpills'), tlab = tsel.querySelector('.tlab');
  const tfind = tpanel.querySelector('input[type=search]');
  const MULTI_EMPTY_ALL = new Set(['acts', 'ranks', 'traits']);
  if (matchMedia('(max-width: 720px)').matches) fbox.open = false;
  function activeCount(){
    let n = 0;
    if (st.q) n++; if (st.def !== 'all') n++; if (st.role !== 'all') n++; if (st.trad !== 'all') n++;
    if (st.acc !== 'all') n++; if (st.ss) n++; n += st.acts.size ? 1 : 0; n += st.ranks.size ? 1 : 0; n += st.traits.size ? 1 : 0;
    return n;
  }
  function apply(){
    let n = 0;
    for (const c of cards){
      const d = c.dataset;
      let ok = true;
      if (st.q && !d.name.includes(st.q)) ok = false;
      if (ok && st.ranks.size && !st.ranks.has(d.rank)) ok = false;
      if (ok && st.def !== 'all' && !d.def.split(' ').includes(st.def)) ok = false;
      if (ok && st.role !== 'all' && !st.stars.has(d.r[+st.role])) ok = false;
      if (ok && st.trad !== 'all' && d.trad !== st.trad) ok = false;
      if (ok && st.acc !== 'all' && !st.grades.has(d.g[+st.acc])) ok = false;
      if (ok && st.ss && d.ss !== '1') ok = false;
      if (ok && st.acts.size && !d.act.split(' ').some(a => st.acts.has(a))) ok = false;
      if (ok && st.traits.size){
        const t = new Set((d.traits || '').split('|'));
        ok = st.tmode === 'all' ? [...st.traits].every(x => t.has(x)) : [...st.traits].some(x => t.has(x));
      }
      c.classList.toggle('hide', !ok);
      if (ok) n++;
    }
    starsRow.classList.toggle('off', st.role === 'all');
    gradesRow.classList.toggle('off', st.acc === 'all');
    const k = activeCount();
    ranks.forEach(r => {
      const any = r.querySelector('.card:not(.hide)');
      r.style.display = any ? '' : 'none';
      r.querySelectorAll('.picks, .considered').forEach(p => { p.style.display = k ? 'none' : ''; });
    });
    fact.textContent = k ? k + ' active, ' + n + ' spells' : n + ' spells';
    count.textContent = k ? n + ' of ' + cards.length + ' spells shown' : cards.length + ' spells';
    // trait button and pills
    tlab.textContent = st.traits.size ? st.traits.size + ' trait' + (st.traits.size > 1 ? 's' : '') + ' (' + (st.tmode === 'all' ? 'all' : 'any') + ')' : 'Choose traits';
    tpills.innerHTML = '';
    [...st.traits].sort().forEach(t => {
      const lab = tpanel.querySelector(`.topt[data-n="${CSS.escape(t)}"] span`).textContent;
      const b = document.createElement('button'); b.type = 'button'; b.className = 'chip mini pill'; b.dataset.t = t;
      b.innerHTML = '<span></span><span class="x" aria-hidden="true">×</span>'; b.firstChild.textContent = lab;
      b.setAttribute('aria-label', 'Remove trait ' + lab);
      tpills.appendChild(b);
    });
  }
  function syncChips(){
    main.querySelectorAll('.controls .chip[data-f]').forEach(b => {
      const f = b.dataset.f;
      b.classList.toggle('on', f === 'ss' ? st.ss : st[f] === b.dataset.v);
    });
    main.querySelectorAll('.controls .chip[data-m]').forEach(b => b.classList.toggle('on', st[b.dataset.m].has(b.dataset.v)));
    tpanel.querySelectorAll('input[type=checkbox]').forEach(i => { i.checked = st.traits.has(i.value); });
    tpanel.querySelectorAll('[data-tm]').forEach(b => b.classList.toggle('on', b.dataset.tm === st.tmode));
  }
  main.querySelector('#spell-q').addEventListener('input', e => { st.q = e.target.value.trim().toLowerCase(); apply(); });
  main.querySelectorAll('.controls .chip[data-f]').forEach(b => b.addEventListener('click', () => {
    const f = b.dataset.f;
    if (f === 'ss') st.ss = !st.ss; else st[f] = b.dataset.v;
    syncChips(); apply();
  }));
  main.querySelectorAll('.controls .chip[data-m]').forEach(b => b.addEventListener('click', () => {
    const m = b.dataset.m, set = st[m], v = b.dataset.v;
    if (set.has(v)) { if (set.size > 1 || MULTI_EMPTY_ALL.has(m)) set.delete(v); } else set.add(v);
    syncChips(); apply();
  }));
  // trait dropdown
  const openT = o => { tpanel.hidden = !o; tbtn.setAttribute('aria-expanded', o ? 'true' : 'false'); if (o) { tfind.value = ''; filterT(''); tfind.focus({preventScroll:true}); } };
  const filterT = q => tpanel.querySelectorAll('.topt').forEach(l => { l.hidden = q && !l.dataset.n.includes(q); });
  tbtn.addEventListener('click', () => openT(tpanel.hidden));
  tfind.addEventListener('input', () => filterT(tfind.value.trim().toLowerCase()));
  tpanel.querySelectorAll('input[type=checkbox]').forEach(i => i.addEventListener('change', () => { i.checked ? st.traits.add(i.value) : st.traits.delete(i.value); apply(); }));
  tpanel.querySelectorAll('[data-tm]').forEach(b => b.addEventListener('click', () => { st.tmode = b.dataset.tm; syncChips(); apply(); }));
  tpanel.querySelector('#tclear').addEventListener('click', () => { st.traits.clear(); syncChips(); apply(); });
  tpanel.querySelector('#tdone').addEventListener('click', () => { openT(false); tbtn.focus(); });
  tpills.addEventListener('click', e => { const b = e.target.closest('.pill'); if (!b) return; st.traits.delete(b.dataset.t); syncChips(); apply(); });
  document.addEventListener('click', e => { if (!tpanel.hidden && !tsel.contains(e.target)) openT(false); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !tpanel.hidden) { openT(false); tbtn.focus(); } });
  main.querySelector('#fclear').addEventListener('click', () => {
    st = DEF(); main.querySelector('#spell-q').value = ''; syncChips(); apply();
  });
  const tog = main.querySelector('#compact');
  let compact = false;
  try { compact = localStorage.getItem('cyrus-compact') === '1'; } catch (e) {}
  const setC = v => { compact = v; document.body.classList.toggle('compact', v); tog.classList.toggle('on', v);
    try { localStorage.setItem('cyrus-compact', v ? '1' : '0'); } catch (e) {} };
  setC(compact);
  tog.addEventListener('click', () => setC(!compact));
  syncChips(); apply();
  initSort(main.querySelector('#spell-sort'), cards, () => ranks, () => apply());
}

route();

// ── multi-level sort shared by spells, items and consumables ──
const GRADE_ORDER = 'SABCDF-';
function sortValue(card, key){
  const d = card.dataset, [t, a, b] = key.split(':');
  if (t === 'num') { const v = parseFloat((d[a] || '').split(' ')[0]); return isNaN(v) ? Infinity : v; }
  if (t === 'str') return (d[a] || '').toLowerCase();
  if (t === 'grade') { const ch = (d[a] || '-')[+b || 0] || '-'; const i = GRADE_ORDER.indexOf(ch); return i < 0 ? 9 : i; }
  if (t === 'rating') return -(+((d[a] || '')[+b] || 0));
  if (t === 'act') { const m = {'f': 0, 'r': 0.5, '1': 1, '2': 2, '3': 3, 'long': 9}; const v = (d.act || 'long').split(' ').map(x => m[x] ?? 9); return Math.min(...v); }
  return 0;
}
function initSort(bar, cards, groups, after){
  if (!bar) return;
  const list = document.createElement('div'); list.className = 'sorted-list'; list.hidden = true;
  const firstGroup = groups()[0];
  firstGroup.parentNode.insertBefore(list, firstGroup);
  const slots = cards.map(c => { const p = document.createElement('span'); p.className = 'card-slot'; p.hidden = true; c.before(p); return p; });
  const sels = [...bar.querySelectorAll('select')], dirs = [...bar.querySelectorAll('.sdir')];
  function run(){
    const keys = sels.map((s, i) => [s.value, dirs[i].dataset.d === 'desc' ? -1 : 1]).filter(k => k[0] !== 'default');
    bar.classList.toggle('on', keys.length > 0);
    if (!keys.length){
      list.hidden = true; groups().forEach(g => g.classList.remove('sorted-away'));
      cards.forEach((c, i) => slots[i].after(c));
    } else {
      const order = cards.map((c, i) => [c, i]).sort((x, y) => {
        for (const [k, dir] of keys){
          const a = sortValue(x[0], k), b = sortValue(y[0], k);
          if (a < b) return -dir; if (a > b) return dir;
        }
        return x[1] - y[1];
      });
      order.forEach(([c]) => list.appendChild(c));
      list.hidden = false; groups().forEach(g => g.classList.add('sorted-away'));
    }
    if (after) after();
  }
  sels.forEach((s, i) => s.addEventListener('change', () => {
    if (s.value === 'default') for (let j = i + 1; j < sels.length; j++) sels[j].value = 'default';
    sels.forEach((x, j) => { x.disabled = j > 0 && sels[j - 1].value === 'default'; dirs[j].disabled = x.disabled || x.value === 'default'; });
    run();
  }));
  dirs.forEach(b => b.addEventListener('click', () => {
    b.dataset.d = b.dataset.d === 'desc' ? 'asc' : 'desc';
    b.textContent = b.dataset.d === 'desc' ? '↓' : '↑';
    b.setAttribute('aria-label', b.dataset.d === 'desc' ? 'Descending' : 'Ascending');
    run();
  }));
  sels.forEach((x, j) => { x.disabled = j > 0; dirs[j].disabled = true; });
  bar.querySelector('.sclear')?.addEventListener('click', () => { sels.forEach(x => x.value = 'default'); sels[0].dispatchEvent(new Event('change')); });
  bar._reset = () => { sels.forEach(x => x.value = 'default'); sels[0].dispatchEvent(new Event('change')); };
}

// ── item and consumable catalogue filters ──
function initCatalog(){
  const root = main.querySelector('.catalog');
  if (!root) return;
  const cards = [...main.querySelectorAll('.card[data-cat]')];
  const groups = () => [...main.querySelectorAll('.catgroup')];
  const count = main.querySelector('#cat-count'), fact = main.querySelector('#fact');
  const fbox = main.querySelector('.fbox');
  if (matchMedia('(max-width: 720px)').matches) fbox.open = false;
  const DEF = () => ({q: '', single: {}, multi: {}, stars: new Set(['4', '5', '6']), traits: new Set(), tmode: 'any'});
  let st = DEF();
  root.querySelectorAll('.chip[data-mode="single"].on').forEach(b => { st.single[b.dataset.k] = b.dataset.v; });
  const defaults = {...st.single};
  const tsel = root.querySelector('.tsel'), tpanel = tsel?.querySelector('.tpanel'), tbtn = tsel?.querySelector('.tbtn'), tpills = tsel?.querySelector('.tpills'), tlab = tsel?.querySelector('.tlab'), tfind = tpanel?.querySelector('input[type=search]');
  const starsRow = root.querySelector('.stars-row');
  function matches(c){
    const d = c.dataset;
    if (st.q && !d.name.includes(st.q)) return false;
    for (const [k, v] of Object.entries(st.single)){
      if (v === 'all') continue;
      if (k === 'role') { if (!st.stars.has((d.r || '')[+v])) return false; continue; }
      if (k === 'plan') { if (v === 'plan' && !d.plan) return false; if (v === 'core' && !(d.plan || '').startsWith('core')) return false; continue; }
      if ((d[k] || '') !== v) return false;
    }
    for (const [k, set] of Object.entries(st.multi)){
      if (!set.size) continue;
      if (k === 'lvl') { const l = +d.lvl; if (![...set].some(r => { const [a, b] = r.split('-').map(Number); return l >= a && l <= b; })) return false; continue; }
      const toks = (d[k] || '').split(' ');
      if (![...set].some(v => toks.includes(v))) return false;
    }
    if (st.traits.size){
      const t = new Set((d.traits || '').split('|'));
      if (st.tmode === 'all' ? ![...st.traits].every(x => t.has(x)) : ![...st.traits].some(x => t.has(x))) return false;
    }
    return true;
  }
  function active(){
    let n = st.q ? 1 : 0;
    for (const [k, v] of Object.entries(st.single)) if (v !== (defaults[k] || 'all')) n++;
    for (const s of Object.values(st.multi)) if (s.size) n++;
    if (st.traits.size) n++;
    return n;
  }
  function apply(){
    let n = 0;
    cards.forEach(c => { const ok = matches(c); c.classList.toggle('hide', !ok); if (ok) n++; });
    groups().forEach(g => { g.style.display = g.querySelector('.card:not(.hide)') ? '' : 'none'; });
    if (starsRow) starsRow.classList.toggle('off', (st.single.role || 'all') === 'all');
    const k = active();
    fact.textContent = k ? k + ' active, ' + n + ' shown' : n + ' items';
    count.textContent = k ? n + ' of ' + cards.length + ' shown' : cards.length + ' items';
    if (tsel){
      tlab.textContent = st.traits.size ? st.traits.size + ' trait' + (st.traits.size > 1 ? 's' : '') + ' (' + st.tmode + ')' : 'Choose traits';
      tpills.innerHTML = '';
      [...st.traits].sort().forEach(t => {
        const lab = tpanel.querySelector(`.topt[data-n="${CSS.escape(t)}"] span`).textContent;
        const b = document.createElement('button'); b.type = 'button'; b.className = 'chip mini pill'; b.dataset.t = t;
        b.innerHTML = '<span></span><span class="x" aria-hidden="true">×</span>'; b.firstChild.textContent = lab;
        b.setAttribute('aria-label', 'Remove trait ' + lab); tpills.appendChild(b);
      });
    }
  }
  function sync(){
    root.querySelectorAll('.chip[data-mode="single"]').forEach(b => b.classList.toggle('on', (st.single[b.dataset.k] || 'all') === b.dataset.v));
    root.querySelectorAll('.chip[data-mode="multi"]').forEach(b => b.classList.toggle('on', (st.multi[b.dataset.k] || new Set()).has(b.dataset.v)));
    root.querySelectorAll('.chip[data-m="stars"]').forEach(b => b.classList.toggle('on', st.stars.has(b.dataset.v)));
    tpanel?.querySelectorAll('input[type=checkbox]').forEach(i => { i.checked = st.traits.has(i.value); });
    tpanel?.querySelectorAll('[data-tm]').forEach(b => b.classList.toggle('on', b.dataset.tm === st.tmode));
  }
  root.querySelector('.cq').addEventListener('input', e => { st.q = e.target.value.trim().toLowerCase(); apply(); });
  root.querySelectorAll('.chip[data-mode="single"]').forEach(b => b.addEventListener('click', () => { st.single[b.dataset.k] = b.dataset.v; sync(); apply(); }));
  root.querySelectorAll('.chip[data-mode="multi"]').forEach(b => b.addEventListener('click', () => {
    const s = st.multi[b.dataset.k] || (st.multi[b.dataset.k] = new Set());
    s.has(b.dataset.v) ? s.delete(b.dataset.v) : s.add(b.dataset.v); sync(); apply();
  }));
  root.querySelectorAll('.chip[data-m="stars"]').forEach(b => b.addEventListener('click', () => {
    const v = b.dataset.v; if (st.stars.has(v)) { if (st.stars.size > 1) st.stars.delete(v); } else st.stars.add(v); sync(); apply();
  }));
  if (tsel){
    const openT = o => { tpanel.hidden = !o; tbtn.setAttribute('aria-expanded', o ? 'true' : 'false'); if (o) { tfind.value = ''; filterT(''); tfind.focus({preventScroll: true}); } };
    const filterT = q => tpanel.querySelectorAll('.topt').forEach(l => { l.hidden = q && !l.dataset.n.includes(q); });
    tbtn.addEventListener('click', () => openT(tpanel.hidden));
    tfind.addEventListener('input', () => filterT(tfind.value.trim().toLowerCase()));
    tpanel.querySelectorAll('input[type=checkbox]').forEach(i => i.addEventListener('change', () => { i.checked ? st.traits.add(i.value) : st.traits.delete(i.value); apply(); }));
    tpanel.querySelectorAll('[data-tm]').forEach(b => b.addEventListener('click', () => { st.tmode = b.dataset.tm; sync(); apply(); }));
    tpanel.querySelector('.tclear').addEventListener('click', () => { st.traits.clear(); sync(); apply(); });
    tpanel.querySelector('.tdone').addEventListener('click', () => { openT(false); tbtn.focus(); });
    tpills.addEventListener('click', e => { const b = e.target.closest('.pill'); if (!b) return; st.traits.delete(b.dataset.t); sync(); apply(); });
    document.addEventListener('click', e => { if (!tpanel.hidden && !tsel.contains(e.target)) openT(false); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && !tpanel.hidden) { openT(false); tbtn.focus(); } });
  }
  root.querySelector('.fclear').addEventListener('click', () => { st = DEF(); Object.assign(st.single, defaults); root.querySelector('.cq').value = ''; sync(); apply(); });
  sync(); apply();
  initSort(main.querySelector('.sortbar'), cards, groups, apply);
}
}
