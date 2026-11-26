// ───────── filters and sorting for search-and-add panels ─────────
let GR = {sp: {}, ft: {}, it: {}};
const gkey = n => String(n || '').replace(/’/g, "'").trim().toLowerCase();
const gradeOf = (kind, r) => (r && ((GR[kind] || {})[gkey(r.n)] || (r.now && (GR[kind] || {})[gkey(r.now)]))) || null;
const grBadge = gr => gr ? ` <span class="gr gr-${gr[0]}" title="Compendium grade ${gr[0]}">${gr[0]}</span>` : '';
const gOrd = gr => gr ? 'SABCDF'.indexOf(gr[0]) : 9;
const FX = {};
const ROLE_NAMES = ['Damage', 'Control', 'Debuff', 'Buff or heal', 'Positioning', 'Utility'];
const actCodes = t => {
  t = String(t == null ? '' : t).toLowerCase();
  if (!t || t === 'null') return ['passive'];
  if (t === 'reaction' || t === 'free') return [t];
  const m = t.match(/^(\d)(?: (?:to|or) (\d))?$/);
  if (m) { const o = []; for (let i = +m[1]; i <= +(m[2] || m[1]); i++) o.push(String(i)); return o; }
  if (/^single action to/.test(t)) return ['1', '2', '3'];
  return ['long'];
};
const actCost = t => { const c = actCodes(t)[0]; return {free: 0, reaction: 0.5, passive: -1, long: 9}[c] ?? Number(c); };
const fxOpts = (vals, label = v => cap(String(v).replace(/-/g, ' '))) => vals.map(v => [v, esc(label(v))]);
const countVals = (items, f) => { const c = new Map(); for (const it of items) for (const v of [].concat(f(it) || [])) if (v !== '' && v != null) c.set(v, (c.get(v) || 0) + 1); return c; };
// facet builders: val(it) returns the item's value or values for the facet
const FX_RAR = {k: 'rar', label: 'Rarity', type: 'chips', opts: [['common', 'Common'], ['uncommon', 'Uncommon'], ['rare', 'Rare'], ['unique', 'Unique']], val: it => (it.rec && it.rec.rar) || 'common'};
const FX_TR = {k: 'tr', label: 'Traits', type: 'traits', val: it => (it.rec && it.rec.tr) || []};
const FX_LEG = {k: 'leg', type: 'toggle', text: 'Hide legacy printings renamed in the remaster', def: true, test: it => !(it.rec && it.rec.leg)};
const fxSrc = items => { const c = countVals(items, it => it.rec && it.rec.src); return {k: 'src', label: 'Source', type: 'select', opts: [...c.keys()].sort().map(v => [v, `${v} (${c.get(v)})`]), val: it => (it.rec && it.rec.src) || ''}; };
const fxLv = (label, lo, hi, min = 0, max = 25) => ({k: 'lv', label, type: 'range', min, max, def: [lo, hi], val: it => it.rec && it.rec.lv});
const fxGrade = () => ({k: 'gr', label: 'Compendium grade', type: 'chips', opts: [...'SABCDF'].map(x => [x, x]).concat([['none', 'Not graded']]), cls: v => v === 'none' ? '' : 'g-' + v, val: it => it.gr ? it.gr[0] : 'none'});
const fxActs = get => ({k: 'act', label: 'Actions', type: 'chips', opts: [['1', act('1')], ['2', act('2')], ['3', act('3')], ['reaction', act('reaction') + ' Reaction'], ['free', act('free') + ' Free'], ['long', 'Longer'], ['passive', 'No action']], val: it => actCodes(get(it))});
const SO_NAME = ['name', 'Name', (a, b) => a.label.localeCompare(b.label), true];
const SO_LV = ['lv', 'Level, lowest first', (a, b) => ((a.rec && a.rec.lv) || 0) - ((b.rec && b.rec.lv) || 0)];
const SO_LVD = ['lv-', 'Level, highest first', (a, b) => ((b.rec && b.rec.lv) || 0) - ((a.rec && a.rec.lv) || 0)];
const SO_GR = ['grade', 'Compendium grade', (a, b) => gOrd(a.gr) - gOrd(b.gr)];
const fxClone = o => JSON.parse(JSON.stringify(o));
function fxDefaults(spec, sorts, init = {}) {
  const st = {q: '', sel: {}, rng: {}, tog: {}, tr: [], tm: 'any', sort: sorts.length ? sorts[0][0] : '', open: true};
  for (const f of spec) {
    if (f.type === 'chips' || f.type === 'select') st.sel[f.k] = f.def || [];
    if (f.type === 'range') st.rng[f.k] = f.def || [f.min, f.max];
    if (f.type === 'toggle') st.tog[f.k] = !!f.def;
  }
  return Object.assign(st, fxClone(init));
}
function fxMatch(spec, st, it) {
  for (const f of spec) {
    if (f.type === 'chips' || f.type === 'select') {
      const s = st.sel[f.k];
      if (s && s.length) { const vs = [].concat(f.val(it)).map(String); if (!vs.some(v => s.includes(v))) return false; }
    } else if (f.type === 'range') {
      const v = f.val(it), [lo, hi] = st.rng[f.k];
      if (v != null && (v < lo || v > hi)) return false;
    } else if (f.type === 'toggle') {
      if (st.tog[f.k] && !f.test(it)) return false;
    } else if (f.type === 'traits' && st.tr.length) {
      const t = f.val(it) || [];
      if (st.tm === 'all' ? !st.tr.every(x => t.includes(x)) : !st.tr.some(x => t.includes(x))) return false;
    }
  }
  return true;
}
function fxHTML(spec, st, sorts) {
  const rows = spec.filter(f => f.type !== 'toggle').map(f => {
    let c = '';
    if (f.type === 'chips') c = f.opts.map(([v, l, t]) => { const on = (st.sel[f.k] || []).includes(v); return `<button type="button" class="chip mini${on ? ' on' : ''}${f.cls && f.cls(v) ? ' ' + f.cls(v) : ''}" data-fk="${f.k}" data-v="${esc(v)}" aria-pressed="${on}"${t ? ` title="${esc(t)}"` : ''}>${l}</button>`; }).join('');
    else if (f.type === 'select') c = `<select data-fs="${f.k}" aria-label="${esc(f.label)}"><option value="">Any</option>${f.opts.map(([v, l]) => `<option value="${esc(v)}"${(st.sel[f.k] || [])[0] === v ? ' selected' : ''}>${esc(l)}</option>`).join('')}</select>`;
    else if (f.type === 'range') { const [lo, hi] = st.rng[f.k]; c = `<span class="cs-range"><input type="number" data-fr="${f.k}" data-e="0" min="${f.min}" max="${f.max}" value="${lo}" aria-label="${esc(f.label)}, lowest"> to <input type="number" data-fr="${f.k}" data-e="1" min="${f.min}" max="${f.max}" value="${hi}" aria-label="${esc(f.label)}, highest"></span>`; }
    else if (f.type === 'traits') c = `<div class="cs-tsel"><button type="button" class="chip mini" data-tt="1" aria-expanded="false">Choose traits ▾</button><span class="cs-tpills"></span><div class="cs-tpanel" hidden><div class="cs-thead"><input type="search" class="cs-tq" placeholder="Find a trait" aria-label="Find a trait"><span class="cs-tmode" role="group" aria-label="How to match traits"><button type="button" class="chip mini${st.tm !== 'all' ? ' on' : ''}" data-tm="any" title="Has any of the chosen traits">Any</button><button type="button" class="chip mini${st.tm === 'all' ? ' on' : ''}" data-tm="all" title="Has all of the chosen traits">All</button></span></div><div class="cs-tlist"></div></div></div>`;
    return `<div class="cs-fr"${f.hint ? ` title="${esc(f.hint)}"` : ''}><span class="cs-fl">${esc(f.label)}</span><div class="cs-fc">${c}</div></div>`;
  }).join('');
  const togs = spec.filter(f => f.type === 'toggle').map(f => `<label class="cs-tog"><input type="checkbox" data-ft="${f.k}"${st.tog[f.k] ? ' checked' : ''}> ${esc(f.text)}</label>`).join('');
  const sort = sorts.length > 1 ? `<div class="cs-fr"><span class="cs-fl">Sort</span><div class="cs-fc"><select data-fsort aria-label="Sort by">${sorts.map(([k, l]) => `<option value="${k}"${st.sort === k ? ' selected' : ''}>${esc(l)}</option>`).join('')}</select></div></div>` : '';
  return `<details class="cs-fx"${st.open ? ' open' : ''}><summary>Filters and sorting<span class="cs-fxn"></span></summary><div class="cs-fxb">${rows}${togs ? `<div class="cs-fr"><span class="cs-fl">Show</span><div class="cs-fc">${togs}</div></div>` : ''}${sort}<div class="cs-fr"><span class="cs-fl"></span><div class="cs-fc"><button type="button" class="chip mini" data-fclear="1">Clear filters</button></div></div></div></details>`;
}
// wires the controls in box to st; redraw() is called after every change
function fxBind(box, spec, st, defs, items, sorts, redraw) {
  const host = () => box.querySelector('.cs-fx');
  const tf = spec.find(f => f.type === 'traits');
  const tcount = tf ? countVals(items, tf.val) : new Map();
  const tnames = [...tcount.keys()].sort();
  const changed = () => {
    const n = spec.filter(f => (f.type === 'traits' ? st.tr.length > 0
      : JSON.stringify(f.type === 'range' ? st.rng[f.k] : f.type === 'toggle' ? st.tog[f.k] : st.sel[f.k]) !== JSON.stringify(f.type === 'range' ? defs.rng[f.k] : f.type === 'toggle' ? defs.tog[f.k] : defs.sel[f.k]))).length;
    const el = box.querySelector('.cs-fxn'); if (el) el.textContent = n ? ` · ${n} active` : '';
  };
  const pills = () => {
    const p = box.querySelector('.cs-tpills'); if (!p) return;
    p.innerHTML = st.tr.map(t => `<button type="button" class="chip mini on" data-trx="${esc(t)}" title="Remove this trait">${esc(t.replace(/-/g, ' '))} ×</button>`).join('');
    const b = box.querySelector('[data-tt]'); if (b) b.firstChild.textContent = st.tr.length ? `Traits (${st.tm === 'all' ? 'all of' : 'any of'} ${st.tr.length}) ▾` : 'Choose traits ▾';
  };
  const tlist = () => {
    const l = box.querySelector('.cs-tlist'); if (!l) return;
    const q = (box.querySelector('.cs-tq').value || '').trim().toLowerCase();
    const ns = tnames.filter(t => !q || t.includes(q));
    l.innerHTML = ns.slice(0, 300).map(t => `<label class="cs-topt"><input type="checkbox" value="${esc(t)}"${st.tr.includes(t) ? ' checked' : ''}><span>${esc(t.replace(/-/g, ' '))}</span><span class="tn">${tcount.get(t)}</span></label>`).join('') || '<p class="small muted">No trait matches.</p>';
  };
  const go = () => { changed(); redraw(); };
  box.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b || !host() || !host().contains(b)) return;
    if (b.dataset.fk) {
      const f = spec.find(x => x.k === b.dataset.fk), s = st.sel[f.k] = st.sel[f.k] || [], v = b.dataset.v, i = s.indexOf(v);
      if (f.single) st.sel[f.k] = i >= 0 ? [] : [v]; else if (i >= 0) s.splice(i, 1); else s.push(v);
      host().querySelectorAll(`[data-fk="${f.k}"]`).forEach(x => { const on = st.sel[f.k].includes(x.dataset.v); x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); });
      go(); return;
    }
    if (b.dataset.tt) { const p = box.querySelector('.cs-tpanel'); p.hidden = !p.hidden; b.setAttribute('aria-expanded', !p.hidden); if (!p.hidden) { tlist(); box.querySelector('.cs-tq').focus({preventScroll: true}); } return; }
    if (b.dataset.tm) { st.tm = b.dataset.tm; box.querySelectorAll('[data-tm]').forEach(x => x.classList.toggle('on', x === b)); pills(); go(); return; }
    if (b.dataset.trx) { st.tr = st.tr.filter(t => t !== b.dataset.trx); pills(); tlist(); go(); return; }
    if (b.dataset.fclear) {
      const keepQ = st.q, open = st.open;
      Object.keys(st).forEach(k => delete st[k]); Object.assign(st, fxClone(defs), {q: keepQ, open});
      host().outerHTML = fxHTML(spec, st, sorts); pills(); go();
    }
  });
  box.addEventListener('input', e => {
    const t = e.target;
    if (t.classList.contains('cs-tq')) { tlist(); return; }
    if (t.dataset.fr != null) { const f = spec.find(x => x.k === t.dataset.fr), v = Number(t.value); if (t.value === '' || isNaN(v)) return; st.rng[f.k][+t.dataset.e] = v; go(); }
  });
  box.addEventListener('change', e => {
    const t = e.target; if (!host() || !host().contains(t)) return;
    if (t.dataset.fs != null) { st.sel[t.dataset.fs] = t.value ? [t.value] : []; go(); }
    else if (t.dataset.ft != null) { st.tog[t.dataset.ft] = t.checked; go(); }
    else if (t.dataset.fsort != null) { st.sort = t.value; go(); }
    else if (t.closest('.cs-tlist')) { const v = t.value; st.tr = t.checked ? [...new Set([...st.tr, v])] : st.tr.filter(x => x !== v); pills(); go(); }
  });
  box.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('cs-fx')) st.open = e.target.open; }, true);
  pills(); changed();
}
// filter, search and sort; search matches the name, traits and source, every word in any order
function fxApply(items, spec, st, sorts, extra) {
  const toks = String(st.q || '').trim().toLowerCase().split(/\s+/).filter(Boolean);
  const m = items.filter(it => {
    if (it.hay == null) it.hay = [it.label, ...((it.rec && it.rec.tr) || []), (it.rec && it.rec.src) || '', it.hayx || ''].join(' ').toLowerCase().replace(/-/g, ' ');
    return toks.every(t => it.hay.includes(t.replace(/-/g, ' '))) && fxMatch(spec, st, it) && (!extra || extra(it));
  });
  const so = sorts.find(s => s[0] === st.sort) || sorts[0];
  if (so) m.sort((a, b) => so[2](a, b) || a.label.localeCompare(b.label));
  if (toks.length && (!so || so[3])) m.sort((a, b) => a.label.toLowerCase().startsWith(toks[0]) ? (b.label.toLowerCase().startsWith(toks[0]) ? 0 : -1) : (b.label.toLowerCase().startsWith(toks[0]) ? 1 : 0));
  return m;
}

// ───────── pickers ─────────
function picker(title, kicker, items, onPick, opts = {}) {
  const box = document.createElement('div');
  box.className = 'cs-picker';
  const spec = opts.facets || [], sorts = opts.sorts || [SO_NAME];
  const key = opts.key || 'picker:' + title;
  const defs = fxDefaults(spec, sorts, opts.init || {});
  const st = FX[key] || (FX[key] = fxClone(defs));
  box.innerHTML = `<label class="search"><input type="search" placeholder="${esc(opts.placeholder || 'Search names, traits and sources')}" aria-label="Search" value="${esc(st.q || '')}"></label>${opts.filters || ''}${spec.length || sorts.length > 1 ? fxHTML(spec, st, sorts) : ''}<p class="small muted cs-pc"></p><ul class="cs-plist"></ul>`;
  const q = box.querySelector('input'), list = box.querySelector('.cs-plist'), count = box.querySelector('.cs-pc');
  let lim = 150;
  const draw = () => {
    st.q = q.value;
    const m = fxApply(items, spec, st, sorts, opts.filter ? it => opts.filter(it, box) : null);
    count.textContent = `${m.length.toLocaleString()} to choose from` + (m.length < items.length ? ` (of ${items.length.toLocaleString()})` : '');
    list.innerHTML = m.slice(0, lim).map(it => `<li><button type="button" class="chip mini" data-i="${items.indexOf(it)}">${esc(opts.verb || 'Choose')}</button>${opts.verb2 ? `<button type="button" class="chip mini" data-i2="${items.indexOf(it)}">${esc(opts.verb2)}</button>` : ''}<span class="n">${it.rec ? g(it.rec, it.label) + legTag(it.rec) : esc(it.label)}${grBadge(it.gr)}${it.tag || ''}</span>${it.sub ? `<small>${it.sub}</small>` : ''}</li>`).join('')
      + (m.length > lim ? `<li><button type="button" class="chip" data-more="1">Show more</button></li>` : '')
      + (m.length ? '' : '<li class="muted">Nothing matches. Clear a filter or widen the search.</li>');
  };
  let t;
  q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { lim = 150; draw(); }, 120); });
  // the search box redraws on input; a change event from it (fired when it loses focus to a Choose button) must not
  // redraw the list under the pointer, or the click is lost
  box.addEventListener('change', e => { if (e.target !== q && !e.target.closest('.cs-fx')) draw(); });
  fxBind(box, spec, st, defs, items, sorts, () => { lim = 150; draw(); });
  box.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b || b.closest('.cs-fx')) return;
    if (b.dataset.more) { lim += 150; draw(); return; }
    if (b.dataset.i != null) { onPick(items[+b.dataset.i], 1); if (!opts.keepOpen) A.popPanel(); else { toast('Added ' + items[+b.dataset.i].label + '.'); if (opts.redrawOnPick) { opts.redrawOnPick(items[+b.dataset.i]); draw(); } } }
    if (b.dataset.i2 != null) { onPick(items[+b.dataset.i2], 2); if (!opts.keepOpen) A.popPanel(); }
  });
  draw();
  A.pushPanel(kicker, title, box, 'picker:' + title);
  setTimeout(() => q.focus({preventScroll: true}), 50);
}
const recSub = r => [r.lv != null ? (r.t === 'spell' ? ((r.tr || []).includes('cantrip') ? 'Cantrip' : 'Rank ' + r.lv) : 'Level ' + r.lv) : '', (r.tr || []).filter(t => !['general', 'skill'].includes(t)).slice(0, 5).join(', '), r.src || '', r.leg ? 'renamed in the remaster as ' + r.now : ''].filter(Boolean).map(esc).join(' · ');
const ATTRS = [['str', 'Strength'], ['dex', 'Dexterity'], ['con', 'Constitution'], ['int', 'Intelligence'], ['wis', 'Wisdom'], ['cha', 'Charisma']];
const SKILL_LIST = ['acrobatics', 'arcana', 'athletics', 'crafting', 'deception', 'diplomacy', 'intimidation', 'medicine', 'nature', 'occultism', 'performance', 'religion', 'society', 'stealth', 'survival', 'thievery'];
function pickDeity() {
  const rs = Object.values(db.e).filter(r => r.t === 'deity');
  const pans = [...new Set(rs.filter(r => r.fr).map(r => r.pan))].sort();
  const items = rs.map(r => ({label: r.n, rec: r, fr: !!r.fr, pan: r.pan || '',
    sub: r.fr ? esc(`${cap(r.title || '')} · ${r.pan} · Forgotten Realms, proposed conversion`) : recSub(r)}))
    .sort((a, b) => a.label.localeCompare(b.label));
  const doms = [...countVals(items, it => [...((it.rec.domains || {}).primary || []), ...((it.rec.domains || {}).alternate || [])]).keys()].sort();
  const facets = [
    {k: 'set', label: 'Setting', type: 'select', opts: [['fr', 'Forgotten Realms deities'], ...pans.map(p => ['pan:' + p, p]), ['pf', 'Pathfinder deities']], def: ['fr'], val: it => it.fr ? ['fr', 'pan:' + it.pan] : ['pf']},
    {k: 'font', label: 'Divine font', type: 'chips', opts: [['heal', 'Heal'], ['harm', 'Harm']], val: it => it.rec.font || []},
    {k: 'sanct', label: 'Sanctification', type: 'chips', opts: [['holy', 'Holy'], ['unholy', 'Unholy'], ['none', 'None']], val: it => ((it.rec.sanct || {}).what || []).length ? it.rec.sanct.what : ['none']},
    {k: 'dom', label: 'Domain', type: 'select', opts: fxOpts(doms), val: it => [...((it.rec.domains || {}).primary || []), ...((it.rec.domains || {}).alternate || [])]},
    {k: 'sk', label: 'Divine skill', type: 'chips', opts: fxOpts(SKILL_LIST), val: it => it.rec.skill || []},
    fxSrc(items)];
  picker('Choose a deity', 'Build', items, it => { ch.deity = it.rec.k; commit(); }, {key: 'deity', facets, sorts: [SO_NAME]});
}
function pickOrigin(kind) {
  if (kind === 'deity') return pickDeity();
  let rs = Object.values(db.e).filter(r => r.t === kind);
  if (kind === 'heritage') { const a = res.S.anc; rs = rs.filter(r => !r.anc || (a && r.anc === a.sl)); }
  const items = rs.map(r => ({label: r.n, rec: r, sub: recSub(r) + (kind === 'heritage' && !r.anc ? ' · versatile heritage' : '')})).sort((a, b) => a.label.localeCompare(b.label));
  const boostVal = it => [...new Set((it.rec.boosts || []).filter(b => b.length < 6).flat())];
  const facets = [];
  if (kind === 'class') facets.push({k: 'key', label: 'Key attribute', type: 'chips', opts: ATTRS, val: it => it.rec.key || []},
    {k: 'sc', label: 'Spellcasting', type: 'chips', opts: [['1', 'Spellcaster'], ['0', 'No spellcasting']], val: it => String(it.rec.sc ? 1 : 0)},
    {k: 'hp', label: 'Hit Points', type: 'chips', opts: [['6', '6'], ['8', '8'], ['10', '10'], ['12', '12']], val: it => String(it.rec.hp)});
  if (kind === 'ancestry') facets.push({k: 'boost', label: 'Attribute boost', type: 'chips', opts: ATTRS, val: boostVal},
    {k: 'hp', label: 'Hit Points', type: 'chips', opts: [['6', '6'], ['8', '8'], ['10', '10'], ['12', '12']], val: it => String(it.rec.hp)},
    {k: 'size', label: 'Size', type: 'chips', opts: [['tiny', 'Tiny'], ['sm', 'Small'], ['med', 'Medium'], ['lg', 'Large']], val: it => it.rec.size || ''},
    {k: 'vis', label: 'Vision', type: 'chips', opts: [['normal', 'Normal'], ['low-light-vision', 'Low-light'], ['darkvision', 'Darkvision']], val: it => it.rec.vision || 'normal'});
  if (kind === 'background') facets.push({k: 'boost', label: 'Attribute boost', type: 'chips', opts: ATTRS, val: boostVal},
    {k: 'sk', label: 'Trained skill', type: 'chips', opts: fxOpts(SKILL_LIST), val: it => ((it.rec.skills || {}).value) || []});
  if (kind === 'heritage') facets.push({k: 'vh', label: 'Heritage', type: 'chips', opts: [['own', 'For this ancestry'], ['versatile', 'Versatile']], val: it => it.rec.anc ? 'own' : 'versatile'});
  facets.push(FX_RAR, FX_TR, fxSrc(items), FX_LEG);
  picker('Choose ' + (kind === 'class' ? 'a class' : kind === 'ancestry' ? 'an ancestry' : 'a ' + kind), 'Build', items, it => {
    ch[kind] = it.rec.k;
    if (kind === 'ancestry') { ch.heritage = null; ch.boosts.ancestry = []; }
    if (kind === 'background') ch.boosts.background = [];
    if (kind === 'class') { ch.boosts.class = null; ch.spells.entries = (ch.spells.entries || []).filter(e => e.id !== 'class'); }
    commit();
  }, {key: 'origin:' + kind, facets, sorts: [SO_NAME, ['rar', 'Rarity', (a, b) => FX_RAR.opts.findIndex(o => o[0] === FX_RAR.val(a)) - FX_RAR.opts.findIndex(o => o[0] === FX_RAR.val(b))]]});
}
function pickFeat(slotId) {
  const slot = res.slots.find(s => s.id === slotId) || {id: slotId, lv: Number(slotId.split('-').pop()) || 1, kind: slotId.split('-')[0]};
  const rs = eng.featOptions(res, slot);
  const taken = new Set(Object.entries(ch.feats).filter(([k]) => k !== slotId).map(([, f]) => f && f.k));
  const own = res.S.cls ? res.S.cls.sl : '';
  const items = rs.map(r => {
    const bad = eng.prereqs(res, r).some(p => p.ok === false);
    return {label: r.n, rec: r, gr: gradeOf('ft', r), bad, taken: taken.has(r.k) && !r.max, hayx: (r.pre || []).join(' '),
      sub: recSub(r) + (r.pre ? ` · <span class="${bad ? 'cs-warn' : ''}">${esc(r.pre.join('; '))}</span>` : '') + (taken.has(r.k) && !r.max ? ' · already taken' : '')};
  });
  const sug = (a, b) => ((b.rec.tr || []).includes(own) - (a.rec.tr || []).includes(own)) || (gOrd(a.gr) - gOrd(b.gr)) || ((b.rec.lv || 0) - (a.rec.lv || 0));
  items.sort((a, b) => sug(a, b) || a.label.localeCompare(b.label));
  const fcat = it => (it.rec.tr || []).includes('archetype') || (it.rec.tr || []).includes('dedication') ? 'archetype' : ['class', 'ancestry', 'skill', 'general'].includes(it.rec.cat) ? it.rec.cat : 'other';
  const facets = [
    fxLv('Level', 1, slot.lv, 1, 20),
    {k: 'cat', label: 'Kind', type: 'chips', opts: [['class', 'Class'], ['archetype', 'Archetype'], ['ancestry', 'Ancestry'], ['skill', 'Skill'], ['general', 'General'], ['other', 'Other']], val: fcat},
    fxActs(it => it.rec.act),
    {k: 'sk', label: 'Skill in prerequisites', type: 'select', opts: fxOpts(SKILL_LIST), val: it => SKILL_LIST.filter(s => (it.rec.pre || []).join(' ').toLowerCase().includes(s))},
    fxGrade(), FX_RAR, FX_TR, fxSrc(items),
    {k: 'met', type: 'toggle', text: "Hide feats whose prerequisites aren't met", def: true, test: it => !it.bad},
    {k: 'tk', type: 'toggle', text: 'Hide feats already taken', def: false, test: it => !it.taken},
    FX_LEG];
  if (FX['feat:' + slot.kind]) FX['feat:' + slot.kind].rng.lv = [Math.min(FX['feat:' + slot.kind].rng.lv[0], slot.lv), slot.lv];
  picker(slot.label || 'Choose a feat', 'Level ' + slot.lv, items, it => { ch.feats[slotId] = {k: it.rec.k}; commit(); },
    {key: 'feat:' + slot.kind, facets, init: {rng: {lv: [1, slot.lv]}}, sorts: [['sug', 'Suggested: own class, then grade, then level', sug, true], SO_NAME, SO_LVD, SO_LV, SO_GR]});
}
function pickChoice(uid, flag) {
  const p = res.pending.find(x => x.uid === uid && x.flag === flag);
  if (!p) return;
  const items = eng.choices(res.S, p).map(o => ({label: o.label, rec: o.rec, value: o.value, sub: o.rec ? recSub(o.rec) : ''}));
  const recs = items.filter(it => it.rec).length > 12;
  const facets = recs ? [FX_RAR, FX_TR, fxSrc(items), FX_LEG] : [];
  if (recs && items.some(it => it.rec && it.rec.lv != null)) facets.unshift(fxLv('Level', 0, 25));
  picker(p.prompt, p.item.r.n, items, it => { (ch.choices[uid] = ch.choices[uid] || {})[flag] = it.value; commit(); },
    {key: 'choice:' + flag, facets, sorts: recs ? [SO_NAME, SO_LV, SO_LVD] : [SO_NAME]});
}
function addEffect(k) { const rounds = effectRounds(rec(k)); ch.effects[k] = rounds != null ? {on: true, rounds} : true; }
function pickEffect() {
  const kindOf = r => (r.n.match(/^(Effect|Spell Effect|Stance)/) || ['Effect'])[0];
  const items = Object.values(db.e).filter(r => r.t === 'effect').map(r => ({label: r.n.replace(/^(Effect|Spell Effect|Stance): /, ''), rec: r, on: !!ch.effects[r.k], sub: esc(kindOf(r)) + (r.src ? ' · ' + esc(r.src) : '') + (effectRounds(r) != null ? ` · ${effectRounds(r)} rounds` : '')}));
  items.sort((a, b) => a.label.localeCompare(b.label));
  const unit = it => { const d = it.rec.dur || {}; return d.sustained ? 'sustained' : d.unit === 'unlimited' || d.value === -1 ? 'unlimited' : d.unit || 'other'; };
  const facets = [
    {k: 'kind', label: 'Kind', type: 'chips', opts: [['Spell Effect', 'Spell effects'], ['Effect', 'Other effects'], ['Stance', 'Stances']], val: it => kindOf(it.rec)},
    {k: 'dur', label: 'Duration', type: 'chips', opts: [['rounds', 'Rounds'], ['minutes', 'Minutes'], ['hours', 'Hours'], ['days', 'Days'], ['sustained', 'Sustained'], ['unlimited', 'Unlimited'], ['encounter', 'Encounter']], val: unit},
    fxLv('Level', 0, 25), FX_RAR, FX_TR, fxSrc(items),
    {k: 'on', type: 'toggle', text: 'Hide effects already on', def: false, test: it => !ch.effects[it.rec.k]}];
  picker('Add an effect', 'Sheet', items, it => { addEffect(it.rec.k); commit(); }, {key: 'effect', facets, sorts: [SO_NAME, SO_LV, SO_LVD, ['src', 'Source', (a, b) => (a.rec.src || '').localeCompare(b.rec.src || '')]]});
}
