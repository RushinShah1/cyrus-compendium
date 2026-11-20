/* Aspera character sheet: builder, sheet, inventory and gold, spells, feats and notes. Saved on this device. */
(function () {
'use strict';
const E = window.CSEngine;
const {Engine, SKILLS, SAVES, ATTRS, ATTR_NAME, RANKS, CASTING, slugify, fmt} = E;
const A = window.Aspera;                      // panels and glossary from app.js
const esc = t => String(t == null ? '' : t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const cap = s => String(s || '').replace(/^\w/, c => c.toUpperCase());
const RANK_L = ['U', 'T', 'E', 'M', 'L'];
const ACT = {'1': 'One action', '2': 'Two actions', '3': 'Three actions', reaction: 'Reaction', free: 'Free action'};
const GLYPH = {'1': '1', '2': '2', '3': '3', reaction: 'R', free: 'F'};
const STORE = 'aspera-chars-v1', PRE = 'aspera-char:';
const CONDITIONS = ['blinded', 'clumsy', 'concealed', 'confused', 'controlled', 'dazzled', 'deafened', 'doomed', 'drained', 'dying', 'enfeebled', 'fascinated',
  'fatigued', 'fleeing', 'frightened', 'grabbed', 'hidden', 'immobilized', 'invisible', 'off-guard', 'paralyzed', 'persistent-damage', 'petrified', 'prone',
  'quickened', 'restrained', 'sickened', 'slowed', 'stunned', 'stupefied', 'unconscious', 'undetected', 'wounded'];

let db = null, eng = null, ch = null, res = null, root = null, tab = 'sheet', store = {cur: null, ids: []};

// ───────── data ─────────
async function loadDB(progress) {
  if (db) return db;
  const parts = ['core', 'feats', 'actions', 'items', 'spells', 'effects'];
  const out = {e: {}};
  let n = 0;
  await Promise.all(parts.map(async p => {
    const r = await fetch('assets/cs/' + p + '.json');
    if (!r.ok) throw new Error(p);
    const j = await r.json();
    Object.assign(out.e, j.e);
    if (p === 'core') { out.slots = j.slots; out.runes = j.runes; out.lang = j.lang; }
    progress && progress(++n, parts.length);
  }));
  db = out; eng = new Engine(db);
  return db;
}
const rec = k => eng.rec(k);

// ───────── storage ─────────
function loadStore() {
  try { store = JSON.parse(localStorage.getItem(STORE)) || {cur: null, ids: []}; } catch (e) { store = {cur: null, ids: []}; }
}
function saveStore() { try { localStorage.setItem(STORE, JSON.stringify(store)); } catch (e) {} }
function getChar(id) { try { return JSON.parse(localStorage.getItem(PRE + id)); } catch (e) { return null; } }
function putChar(c) {
  c.updated = Date.now();
  try { localStorage.setItem(PRE + c.id, JSON.stringify(c)); }
  catch (e) { toast('This device has run out of space for saved characters. Export a copy and delete one you no longer need.'); }
}
const newId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
function blank(name) {
  return {format: 'aspera-character', v: 1, id: newId(), name: name || 'New character', level: 1, ancestry: null, heritage: null, background: null, class: null, deity: null,
    boosts: {ancestry: [], background: [], class: null, 1: [], 5: [], 10: [], 15: [], 20: []}, trained: [], lores: [], increases: {}, intTrained: {}, languages: [],
    feats: {}, choices: {}, inventory: [], coins: {pp: 0, gp: 15, sp: 0, cp: 0}, ledger: [], hp: {damage: 0, temp: 0}, heroPoints: 1, focusUsed: 0,
    conditions: {}, effects: {}, toggles: {}, custom: [], spells: {entries: []}, notes: {}, options: {freeArchetype: false}, bonusSlots: []};
}

// ───────── compute and render ─────────
function recompute() { res = eng.compute(ch); }
function commit(rerender = true) { putChar(ch); recompute(); if (rerender) render(); }
function toast(msg) {
  let t = document.querySelector('.cs-toast');
  if (!t) { t = document.createElement('div'); t.className = 'cs-toast'; t.setAttribute('role', 'status'); document.body.appendChild(t); }
  t.textContent = msg; t.classList.add('on');
  clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove('on'), 3500);
}
const g = (r, label) => r ? (r.g ? `<a href="#" data-g="${esc(r.g)}">${esc(label || r.n)}</a>` : esc(label || r.n)) : '';
const act = a => a ? `<span class="pf" title="${ACT[a] || a}">${GLYPH[a] || ''}</span>` : '';
const rankTag = r => `<span class="cs-rank r${r}" title="${RANKS[r]}">${RANK_L[r]}</span>`;
function statBtn(key, label, val, sub) {
  return `<button type="button" class="cs-stat" data-act="breakdown" data-k="${esc(key)}"><span class="l">${esc(label)}</span><b>${esc(val)}</b>${sub ? `<small>${esc(sub)}</small>` : ''}</button>`;
}

function render() {
  if (!root) return;
  const y = window.scrollY;
  root.innerHTML = head() + `<nav class="cs-tabs" role="tablist">${['sheet', 'build', 'inventory', 'spells', 'feats', 'notes'].map(t =>
    `<button type="button" role="tab" aria-selected="${t === tab}" class="${t === tab ? 'on' : ''}" data-act="tab" data-t="${t}">${{sheet: 'Sheet', build: 'Build', inventory: 'Inventory', spells: 'Spells', feats: 'Feats', notes: 'Notes'}[t]}</button>`).join('')}</nav>`
    + `<div class="cs-body">${({sheet: tabSheet, build: tabBuild, inventory: tabInventory, spells: tabSpells, feats: tabFeats, notes: tabNotes})[tab]()}</div>`;
  window.scrollTo(0, y);
}

function head() {
  const opts = store.ids.map(id => { const c = id === ch.id ? ch : getChar(id); return c ? `<option value="${esc(id)}"${id === ch.id ? ' selected' : ''}>${esc(c.name)} (level ${c.level})</option>` : ''; }).join('');
  const cls = res.S.cls, anc = res.S.anc, her = res.S.her, bg = res.S.bg;
  const hs = res.S.items.find(i => i.uid === 'class>cf:hybrid-study') ;
  const line = [anc ? (her ? her.n : anc.n) : 'No ancestry', bg ? bg.n : 'No background', cls ? cls.n : 'No class'].join(' · ');
  const hp = res.hp.total, cur = Math.max(0, hp - (ch.hp.damage || 0)), temp = ch.hp.temp || 0;
  const pct = hp ? Math.round(100 * cur / hp) : 0;
  const saves = Object.entries(res.saves).map(([k, v]) => statBtn('save:' + k, v.label, fmt(v.total), RANKS[v.rank])).join('');
  const cdc = Object.values(res.classDCs).find(c => c.primary);
  const dots = (n, max, k) => `<span class="cs-dots" role="group" aria-label="${k}">${Array.from({length: max}, (_, i) => `<button type="button" class="${i < n ? 'on' : ''}" data-act="dots" data-k="${k}" data-n="${i + 1}" aria-label="${k} ${i + 1}"></button>`).join('')}</span>`;
  const step = (k, v, max) => `<span class="cs-step"><button type="button" data-act="cond" data-k="${k}" data-d="-1" aria-label="Lower ${k}">−</button><b>${v || 0}</b><button type="button" data-act="cond" data-k="${k}" data-d="1" aria-label="Raise ${k}">+</button></span>`;
  const c = ch.conditions || {};
  return `<div class="cs-top">
<label class="cs-pick"><span class="sr">Character</span><select data-act="switch">${opts}</select></label>
<button type="button" class="chip" data-act="new">New</button><button type="button" class="chip" data-act="dup">Duplicate</button>
<button type="button" class="chip" data-act="export">Export</button><label class="chip cs-file">Import<input type="file" accept=".json,application/json" data-act="import" hidden></label>
<button type="button" class="chip" data-act="delete">Delete</button></div>
<header class="cs-head"><div class="cs-id"><input class="cs-name" value="${esc(ch.name)}" data-field="name" aria-label="Character name">
<div class="cs-line">Level <span class="cs-step"><button type="button" data-act="level" data-d="-1" aria-label="Lower level">−</button><b>${ch.level}</b><button type="button" data-act="level" data-d="1" aria-label="Raise level">+</button></span> · ${esc(line)}</div></div>
<div class="cs-hp"><div class="cs-hpbar"><span style="width:${pct}%"></span></div>
<div class="cs-hpnum"><button type="button" class="cs-stat bare" data-act="breakdown" data-k="hp"><b>${cur}</b><small>of ${hp} HP</small></button>${temp ? `<span class="cs-temp">+${temp} temporary</span>` : ''}</div>
<div class="cs-hpin"><input type="number" inputmode="numeric" min="0" placeholder="Amount" aria-label="Amount" id="cs-hpamt"><button type="button" class="chip" data-act="hp" data-m="dmg">Damage</button><button type="button" class="chip" data-act="hp" data-m="heal">Heal</button><button type="button" class="chip" data-act="hp" data-m="temp">Temporary</button></div></div>
</header>
<div class="cs-vitals">${statBtn('ac', 'AC', res.ac.total, RANKS[res.ac.rank])}${saves}${statBtn('perception', 'Perception', fmt(res.perception.total), RANKS[res.perception.rank])}
${statBtn('speed', 'Speed', res.speed.total + ' ft', Object.entries(res.otherSpeeds).map(([k, v]) => k + ' ' + v.total).join(', '))}${cdc ? statBtn('classdc', 'Class DC', cdc.total, RANKS[cdc.rank]) : ''}${statBtn('initiative', 'Initiative', fmt(res.initiative.total), ch.initiative ? cap(ch.initiative) : 'Perception')}</div>
<div class="cs-res"><span><b>Hero Points</b>${dots(ch.heroPoints || 0, res.heroMax, 'hero')}</span>${res.focusMax ? `<span><b>Focus Points</b>${dots(res.focusMax - (ch.focusUsed || 0), res.focusMax, 'focus')}</span>` : ''}
<span><b>Dying</b>${step('dying', c.dying, res.dyingMax)}</span><span><b>Wounded</b>${step('wounded', c.wounded)}</span><span><b>Doomed</b>${step('doomed', c.doomed)}</span>
${res.S.shield ? `<label class="cs-tog"><input type="checkbox" data-act="toggle" data-k="shield-raised"${(ch.toggles || {})['shield-raised'] ? ' checked' : ''}> Shield raised</label>` : ''}</div>`;
}

// ───────── Sheet tab ─────────
function tabSheet() {
  const c = ch.conditions || {};
  const active = Object.entries(c).filter(([k, v]) => v && !['dying', 'wounded', 'doomed'].includes(k));
  const cond = active.map(([k, v]) => {
    const r = rec('co:' + k);
    const valued = r && r.val;
    return `<span class="cs-cond">${g(r, cap(k.replace(/-/g, ' ')))}${valued ? ` <span class="cs-step"><button type="button" data-act="cond" data-k="${k}" data-d="-1" aria-label="Lower">−</button><b>${v}</b><button type="button" data-act="cond" data-k="${k}" data-d="1" aria-label="Raise">+</button></span>` : ''}<button type="button" class="x" data-act="cond-off" data-k="${k}" aria-label="Remove ${k}">×</button></span>`;
  }).join('');
  const condSel = `<select data-act="cond-add" aria-label="Add a condition"><option value="">Add a condition…</option>${CONDITIONS.filter(k => !c[k]).map(k => `<option value="${k}">${cap(k.replace(/-/g, ' '))}</option>`).join('')}</select>`;
  // stances, effects and toggles
  const seen = new Set();
  const tg = [];
  for (const t of res.toggles) {
    if (t.key) {
      if (seen.has(t.key)) continue; seen.add(t.key);
      const r = rec(t.key); if (!r) continue;
      tg.push(`<label class="cs-tog"><input type="checkbox" data-act="effect" data-k="${esc(t.key)}"${(ch.effects || {})[t.key] ? ' checked' : ''}> ${esc(r.n.replace(/^(Effect|Stance|Spell Effect): /, ''))} <small>${esc(t.from.r.n)}</small></label>`);
    } else if (t.option) {
      if (seen.has(t.option)) continue; seen.add(t.option);
      tg.push(`<label class="cs-tog"><input type="checkbox" data-act="toggle" data-k="${esc(t.option)}"${(ch.toggles || {})[t.option] ? ' checked' : ''}> ${esc(eng.t(t.label))} <small>${esc(t.from.r.n)}</small></label>`);
    }
  }
  const other = Object.entries(ch.effects || {}).filter(([k, v]) => v && !seen.has(k)).map(([k]) => { const r = rec(k); return r ? `<span class="cs-cond">${g(r, r.n.replace(/^(Effect|Stance|Spell Effect): /, ''))}<button type="button" class="x" data-act="effect-off" data-k="${esc(k)}" aria-label="Remove">×</button></span>` : ''; }).join('');
  // choices that effects and stances ask for (such as Arcane Cascade's damage type)
  const effChoices = res.pending.filter(p => p.uid.startsWith('effect:')).map(p => choiceUI(p)).join('');
  const strikes = res.strikes.map(s => {
    const ex = s.extraDice.map(d => `<span class="${d.situational ? 'sit' : ''}">${d.critical ? 'critical: ' : ''}+${d.n}${d.d} ${esc(d.type || '')}${d.cat === 'persistent' ? ' persistent' : ''} <small>(${esc(d.from)})</small></span>`).join('');
    const notes = s.notes.map(n => `<li><b>${esc(n.title)}</b>${n.outcome ? ` <small>(${esc([].concat(n.outcome).map(o => o.replace(/([A-Z])/g, ' $1').toLowerCase()).join(', '))})</small>` : ''}: ${esc(stripTags(n.text))}</li>`).join('');
    const sit = s.attack.situational.concat(s.damage.situational).map(m => `${esc(m.label)} ${fmt(m.value)}`).join('; ');
    return `<div class="cs-strike${s.held ? '' : ' idle'}"><div class="h"><b>${s.inv && !s.inv.custom ? g(s.r, s.name) : esc(s.name)}</b>${s.held ? '' : ' <small>not held</small>'}<span class="cs-trs">${s.traits.map(t => `<span class="trait">${esc(t.replace(/-/g, ' '))}</span>`).join('')}</span></div>
<div class="cs-atk">${s.map.map((m, i) => `<button type="button" class="cs-stat bare" data-act="breakdown" data-k="strike:${res.strikes.indexOf(s)}"><b>${fmt(m)}</b><small>${['First', 'Second', 'Third'][i]}</small></button>`).join('')}
<button type="button" class="cs-stat bare dmg" data-act="breakdown" data-k="damage:${res.strikes.indexOf(s)}"><b>${esc(s.formula)}</b><small>Damage${s.range ? ` · range ${s.range} ft` : ''}</small></button></div>
${ex ? `<div class="cs-ex">${ex}</div>` : ''}${sit ? `<p class="small muted">Situational: ${sit}</p>` : ''}${notes ? `<ul class="cs-notes">${notes}</ul>` : ''}</div>`;
  }).join('');
  const skills = Object.entries(res.skills).sort((a, b) => (a[1].lore - b[1].lore) || a[1].label.localeCompare(b[1].label)).map(([k, v]) =>
    `<button type="button" class="cs-skill" data-act="breakdown" data-k="skill:${esc(k)}">${rankTag(v.rank)}<span>${esc(v.label)}</span><small>${v.attr.toUpperCase()}</small><b>${fmt(v.total)}</b></button>`).join('');
  const acts = [];
  const seenA = new Set();
  for (const it of res.actions) { const r = it.r; if (seenA.has(r.n) || !r.act || r.act === 'passive') continue; seenA.add(r.n); acts.push(`<li>${act(r.act)} ${g(r)}</li>`); }
  const def = [];
  if (res.resist.length) def.push(`<p><b>Resistances</b> ${res.resist.map(r => esc(`${r.type} ${r.value ?? ''}`)).join(', ')}</p>`);
  if (res.weak.length) def.push(`<p><b>Weaknesses</b> ${res.weak.map(r => esc(`${r.type} ${r.value ?? ''}`)).join(', ')}</p>`);
  if (res.immune.length) def.push(`<p><b>Immunities</b> ${res.immune.map(r => esc(r.type)).join(', ')}</p>`);
  const senses = res.senses.map(s => esc(cap(String(s.type || '').replace(/-/g, ' ')) + (s.range ? ` ${s.range} ft` : ''))).join(', ');
  return `<section class="cs-sec"><h2>Conditions and effects</h2><div class="cs-conds">${cond || '<span class="muted small">No conditions.</span>'} ${condSel}</div>
${tg.length ? `<div class="cs-togs">${tg.join('')}</div>` : ''}${effChoices ? `<div class="cs-choices">${effChoices}</div>` : ''}
<div class="cs-conds">${other}<button type="button" class="chip" data-act="effect-pick">Add an effect from a spell or item</button></div></section>
<section class="cs-sec"><h2>Strikes</h2><div class="cs-strikes">${strikes || '<p class="muted">Add a weapon on the Inventory tab.</p>'}</div></section>
<section class="cs-sec"><h2>Skills</h2><div class="cs-skills">${skills}</div></section>
<section class="cs-sec cs-2"><div><h2>Actions</h2><ul class="cs-acts">${acts.join('') || '<li class="muted">None yet.</li>'}</ul></div>
<div><h2>Senses, languages and defences</h2><p><b>Size</b> ${esc({tiny: 'Tiny', sm: 'Small', med: 'Medium', lg: 'Large', huge: 'Huge', grg: 'Gargantuan'}[res.size] || res.size)}</p>
${senses ? `<p><b>Senses</b> ${senses}</p>` : ''}<p><b>Languages</b> ${esc(res.languages.list.map(l => cap(l)).join(', ') || 'None')}</p>${def.join('')}
<p><b>Bulk</b> ${res.bulk.value}${res.bulk.light ? ', ' + res.bulk.light + ' L' : ''} of ${res.bulk.encumbered} before encumbered, ${res.bulk.max} maximum</p></div></section>`;
}
const stripTags = t => String(t || '').replace(/<[^>]+>/g, '').replace(/@\w+\[[^\]]*\]\{([^}]*)\}/g, '$1').replace(/@\w+\[([^\]]*)\]/g, '$1');

// ───────── Build tab ─────────
function origin(kind, label, r, extra) {
  return `<div class="cs-orig"><span class="l">${label}</span><span class="v">${r ? g(r) : '<span class="muted">Not chosen</span>'}</span><button type="button" class="chip" data-act="pick-origin" data-k="${kind}">${r ? 'Change' : 'Choose'}</button>${extra || ''}</div>`;
}
function choiceUI(p) {
  const opts = eng.choices(res.S, p);
  const cur = p.value;
  const curR = typeof cur === 'string' ? rec(cur) : null;
  const label = curR ? g(curR) : cur != null ? esc(labelFor(opts, cur)) : '<span class="muted">Not chosen</span>';
  const who = p.item.r.n;
  if (opts.length && opts.length <= 16 && !opts.some(o => o.rec)) {
    return `<div class="cs-choice"><span class="l">${esc(who)}: ${esc(p.prompt)}</span><select data-act="choice" data-uid="${esc(p.uid)}" data-flag="${esc(p.flag)}"><option value="">Choose…</option>${opts.map(o => `<option value="${esc(o.value)}"${String(o.value) === String(cur) ? ' selected' : ''}>${esc(o.label)}</option>`).join('')}</select></div>`;
  }
  return `<div class="cs-choice"><span class="l">${esc(who)}: ${esc(p.prompt)}</span><span class="v">${label}</span><button type="button" class="chip" data-act="choice-pick" data-uid="${esc(p.uid)}" data-flag="${esc(p.flag)}">${cur != null ? 'Change' : 'Choose'}</button></div>`;
}
const labelFor = (opts, v) => (opts.find(o => String(o.value) === String(v)) || {label: String(v)}).label;
function boostRow(label, key, options, chosen, n, fixed) {
  const cells = ATTRS.map(a => {
    const on = chosen.includes(a), allowed = options.includes(a);
    const fx = (fixed || []).includes(a);
    return `<td>${fx ? '<span class="cs-fixed" title="Fixed boost">+</span>' : allowed ? `<button type="button" class="cs-bst${on ? ' on' : ''}" data-act="boost" data-k="${key}" data-a="${a}" aria-pressed="${on}" aria-label="${label}: ${ATTR_NAME[a]}">${on ? '+' : ''}</button>` : ''}</td>`;
  }).join('');
  return `<tr><th>${label}<small>${chosen.length} of ${n}</small></th>${cells}</tr>`;
}
function tabBuild() {
  const S = res.S, b = ch.boosts, anc = S.anc, bg = S.bg, cls = S.cls;
  const L = ch.level;
  // attributes
  let rows = '';
  if (anc) {
    if (ch.altBoosts) rows += boostRow('Ancestry (two free boosts)', 'ancestry', ATTRS, b.ancestry, 2);
    else {
      const free = anc.boosts.filter(o => o.length > 1).length;
      const fixed = anc.boosts.filter(o => o.length === 1).map(o => o[0]);
      rows += boostRow('Ancestry', 'ancestry', ATTRS.filter(a => !fixed.includes(a)), b.ancestry, free, fixed);
      const flaws = anc.flaws.filter(o => o.length === 1).map(o => o[0]);
      if (flaws.length) rows += `<tr><th>Ancestry flaw</th>${ATTRS.map(a => `<td>${flaws.includes(a) ? '<span class="cs-fixed flaw">−</span>' : ''}</td>`).join('')}</tr>`;
    }
  }
  if (bg) {
    const opts = (bg.boosts[0] || []);
    rows += boostRow('Background', 'background', ATTRS, b.background, 2);
    rows += `<tr><td colspan="7" class="small muted">${esc(bg.n)}: one boost to ${opts.map(a => ATTR_NAME[a]).join(' or ')}, and one free boost.</td></tr>`;
  }
  if (cls) rows += boostRow('Class key attribute', 'class', cls.key.length ? cls.key : (S.keyOptions || ATTRS), b.class ? [b.class] : [], 1);
  rows += boostRow('Level 1', '1', ATTRS, b[1] || [], 4);
  for (const lv of [5, 10, 15, 20]) if (L >= lv) rows += boostRow('Level ' + lv, String(lv), ATTRS, b[lv] || [], 4);
  rows += `<tr class="tot"><th>Modifier</th>${ATTRS.map(a => `<td><b>${fmt(res.attributes[a])}</b></td>`).join('')}</tr>`;
  const attrs = `<div class="cs-scroll"><table class="cs-boosts"><thead><tr><th></th>${ATTRS.map(a => `<th>${a.toUpperCase()}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>
<label class="cs-tog"><input type="checkbox" data-act="opt" data-k="altBoosts"${ch.altBoosts ? ' checked' : ''}> Use two free ancestry boosts and no flaws instead</label>`;
  // skills
  const tc = res.trainCount, trained = ch.trained || [];
  const fromBuild = new Set([...(cls ? cls.skills.value || [] : []), ...(bg ? bg.skills.value || [] : [])]);
  const skillChips = Object.keys(SKILLS).map(s => {
    const fixed = fromBuild.has(s), on = trained.includes(s);
    return `<button type="button" class="chip mini${on || fixed ? ' on' : ''}" ${fixed ? 'disabled title="Trained by class or background"' : `data-act="train" data-k="${s}" aria-pressed="${on}"`}>${cap(s)}</button>`;
  }).join('');
  const lores = (ch.lores || []).map((l, i) => `<span class="cs-cond">${esc(l)}<button type="button" class="x" data-act="lore-del" data-i="${i}" aria-label="Remove">×</button></span>`).join('');
  const bgLore = bg ? (bg.skills.lore || []).join(', ') : '';
  const skillOpts = sel => Object.keys(res.skills).map(s => `<option value="${esc(s)}"${s === sel ? ' selected' : ''}>${esc(res.skills[s].label)}</option>`).join('');
  // levels
  const slots = res.slots;
  const feats = ch.feats || {};
  const featuresAt = lv => cls ? cls.items.filter(x => x[0] === lv).map(x => rec(x[1])).filter(Boolean) : [];
  const pendingFor = uidStart => res.pending.filter(p => p.uid === uidStart || p.uid.startsWith(uidStart + '>'));
  let levels = '';
  for (let lv = 1; lv <= 20; lv++) {
    const here = slots.filter(s => s.lv === lv);
    const fts = featuresAt(lv);
    const parts = [];
    if (lv === 1) {
      parts.push(origin('ancestry', 'Ancestry', anc) + origin('heritage', 'Heritage', S.her) + origin('background', 'Background', bg) + origin('class', 'Class', cls) + origin('deity', 'Deity', S.dei, S.dei ? '<button type="button" class="chip" data-act="clear-deity">Remove</button>' : ''));
      for (const u of ['ancestry', 'heritage', 'background', 'class', 'deity']) for (const p of pendingFor(u)) if (!p.uid.startsWith('class>')) parts.push(choiceUI(p));
    }
    if (fts.length) {
      parts.push(`<div class="cs-feat"><span class="l">Class features</span><span class="v">${fts.map(r => g(r)).join(', ')}</span></div>`);
      for (const r of fts) for (const p of pendingFor('class>' + r.k)) parts.push(choiceUI(p));
    }
    for (const s of here) {
      if (s.kind === 'boost') continue;
      if (s.kind === 'increase') {
        parts.push(`<div class="cs-feat"><span class="l">Skill increase</span><select data-act="inc" data-lv="${lv}" aria-label="Skill increase at level ${lv}"><option value="">Choose…</option>${skillOpts((ch.increases || {})[lv])}</select></div>`);
        continue;
      }
      const f = feats[s.id], r = f ? rec(f.k) : null;
      let warn = '';
      if (r) { const pr = eng.prereqs(res, r).filter(p => p.ok === false); if (pr.length) warn = `<small class="cs-warn">Prerequisite not met: ${esc(pr.map(p => p.text).join('; '))}</small>`; }
      parts.push(`<div class="cs-feat"><span class="l">${esc(s.label)}</span><span class="v">${r ? g(r) + ` <small>${r.lv || ''}</small>` : '<span class="muted">Empty</span>'}${warn}</span><button type="button" class="chip" data-act="pick-feat" data-s="${esc(s.id)}">${r ? 'Change' : 'Choose'}</button>${r ? `<button type="button" class="chip" data-act="clear-feat" data-s="${esc(s.id)}" aria-label="Remove">×</button>` : ''}</div>`);
      if (r && r.k === 'ft:additional-lore') parts.push(`<div class="cs-choice"><span class="l">Additional Lore: which Lore</span><input type="text" value="${esc(f.lore || '')}" placeholder="Academia" data-field="featlore" data-s="${esc(s.id)}" aria-label="Lore for Additional Lore"></div>`);
      for (const p of pendingFor('feat:' + s.id)) parts.push(choiceUI(p));
    }
    const dim = lv > L ? ' planned' : '';
    levels += `<section class="cs-lv${dim}"><h3>Level ${lv}${lv > L ? ' <small>planned</small>' : ''}</h3>${parts.join('')}</section>`;
  }
  const intExtra = Math.max(0, res.attributes.int - intAtOne());
  let intRows = '';
  for (let i = 0; i < intExtra; i++) { const key = 'x' + i; intRows += `<select data-act="int-train" data-k="${key}" aria-label="Extra trained skill ${i + 1}"><option value="">Choose…</option>${Object.keys(SKILLS).map(s => `<option value="${s}"${(ch.intTrained || {})[key] === s ? ' selected' : ''}>${cap(s)}</option>`).join('')}</select>`; }
  const langs = res.languages;
  return `<section class="cs-sec"><h2>Options</h2><div class="cs-togs"><label class="cs-tog"><input type="checkbox" data-act="opt" data-k="freeArchetype"${ch.options.freeArchetype ? ' checked' : ''}> Free archetype</label>
<button type="button" class="chip" data-act="bonus-slot">Add a bonus feat slot</button></div>
${(ch.bonusSlots || []).length ? `<p class="small muted">Bonus slots: ${ch.bonusSlots.map((b, i) => `${esc(b.label)} at level ${b.lv} <button type="button" class="chip mini" data-act="bonus-del" data-i="${i}">Remove</button>`).join(' ')}</p>` : ''}</section>
<section class="cs-sec"><h2>Attributes</h2>${attrs}</section>
<section class="cs-sec"><h2>Skills</h2><p class="small muted">Train ${tc} skills at level 1 from your class and Intelligence (${trained.length} chosen). Skills your class or background already trains are marked.</p>
<div class="cs-chips">${skillChips}</div>
${intExtra ? `<p class="small muted">Your Intelligence has increased since level 1, which trains ${intExtra} more skill${intExtra > 1 ? 's' : ''}.</p><div class="cs-chips">${intRows}</div>` : ''}
<p><b>Lore</b> ${bgLore ? esc(bgLore) + ' (background) ' : ''}${lores}</p>
<div class="cs-inline"><input type="text" placeholder="Add a Lore, such as Academia Lore" id="cs-lore" aria-label="New Lore skill"><button type="button" class="chip" data-act="lore-add">Add</button></div>
<p><b>Initiative</b> <select data-act="init" aria-label="Initiative skill"><option value="">Perception</option>${Object.keys(res.skills).map(s => `<option value="${esc(s)}"${ch.initiative === s ? ' selected' : ''}>${esc(res.skills[s].label)}</option>`).join('')}</select></p></section>
<section class="cs-sec"><h2>Languages</h2><p class="small muted">${esc(langs.list.map(cap).join(', ') || 'None')}. You can choose ${langs.extraMax} more (${langs.chosen} chosen).</p>
<div class="cs-inline"><input type="text" placeholder="Add a language" id="cs-lang" aria-label="New language"><button type="button" class="chip" data-act="lang-add">Add</button>${(ch.languages || []).map((l, i) => `<span class="cs-cond">${esc(cap(l))}<button type="button" class="x" data-act="lang-del" data-i="${i}" aria-label="Remove">×</button></span>`).join('')}</div></section>
<section class="cs-sec"><h2>Levels</h2><p class="small muted">Choices above your current level are kept as a plan and apply when you level up.</p>${levels}</section>`;
}
function intAtOne() {
  const c = JSON.parse(JSON.stringify(ch)); c.level = 1;
  const r = eng.compute(c); return r.attributes.int;
}

// ───────── Inventory tab ─────────
const coinTotal = c => (c.pp || 0) * 1000 + (c.gp || 0) * 100 + (c.sp || 0) * 10 + (c.cp || 0);
const money = cp => { const gp = Math.floor(cp / 100), sp = Math.floor(cp % 100 / 10), c = cp % 10; return [gp ? gp.toLocaleString() + ' gp' : '', sp ? sp + ' sp' : '', c ? c + ' cp' : ''].filter(Boolean).join(' ') || '0 gp'; };
const STATES = [['held1', 'Held in one hand'], ['held2', 'Held in two hands'], ['worn', 'Worn'], ['stowed', 'Stowed'], ['dropped', 'Dropped']];
function tabInventory() {
  const c = ch.coins;
  const coins = ['pp', 'gp', 'sp', 'cp'].map(k => `<label class="cs-coin"><span>${k}</span><input type="number" inputmode="numeric" min="0" value="${c[k] || 0}" data-field="coin" data-k="${k}"></label>`).join('');
  const ledger = (ch.ledger || []).slice(-12).reverse().map(l => `<li><span>${new Date(l.t).toLocaleDateString()}</span><b class="${l.d < 0 ? 'neg' : 'pos'}">${l.d < 0 ? '−' : '+'}${money(Math.abs(l.d))}</b><span>${esc(l.note || '')}</span></li>`).join('');
  const groups = {held: [], worn: [], stowed: [], dropped: []};
  for (const inv of ch.inventory) groups[(inv.eq || 'stowed').startsWith('held') ? 'held' : (inv.eq || 'stowed')].push(inv);
  const invested = ch.inventory.filter(i => i.inv).length;
  const row = inv => {
    const r = eng.invRec(inv); if (!r) return '';
    const name = inv.custom ? esc(inv.custom.n) : g(r, inv.name || r.n);
    const canInvest = (r.tr || []).includes('invested');
    const runes = (r.t === 'weapon' || r.t === 'armor' || r.t === 'shield') ? `<button type="button" class="chip mini" data-act="runes" data-id="${esc(inv.id)}">Runes${runeSummary(r, inv)}</button>` : '';
    return `<li class="cs-item"><div class="n">${name} <small>${esc(typeLabel(r))}${r.lv ? ', level ' + r.lv : ''}</small></div>
<div class="c"><span class="cs-step"><button type="button" data-act="qty" data-id="${esc(inv.id)}" data-d="-1" aria-label="Fewer">−</button><b>${inv.qty ?? 1}</b><button type="button" data-act="qty" data-id="${esc(inv.id)}" data-d="1" aria-label="More">+</button></span>
<select data-act="state" data-id="${esc(inv.id)}" aria-label="Where it is">${STATES.map(([k, l]) => `<option value="${k}"${(inv.eq || 'stowed') === k ? ' selected' : ''}>${l}</option>`).join('')}</select>
${canInvest ? `<label class="cs-tog"><input type="checkbox" data-act="invest" data-id="${esc(inv.id)}"${inv.inv ? ' checked' : ''}> Invested</label>` : ''}${runes}
<span class="small muted">${r.bulk === 0.1 ? 'L' : r.bulk || '—'}</span><button type="button" class="chip mini" data-act="sell" data-id="${esc(inv.id)}">Sell</button><button type="button" class="x" data-act="remove" data-id="${esc(inv.id)}" aria-label="Remove">×</button></div></li>`;
  };
  const sec = (k, t) => groups[k].length ? `<h3>${t}</h3><ul class="cs-items">${groups[k].map(row).join('')}</ul>` : '';
  return `<section class="cs-sec"><h2>Money</h2><div class="cs-coins">${coins}<span class="cs-worth">Total ${money(coinTotal(c))}</span></div>
<div class="cs-inline"><input type="number" inputmode="decimal" min="0" step="any" placeholder="Amount" id="cs-mamt" aria-label="Amount"><select id="cs-munit" aria-label="Unit"><option value="gp">gp</option><option value="sp">sp</option><option value="cp">cp</option><option value="pp">pp</option></select>
<input type="text" placeholder="What for" id="cs-mnote" aria-label="Note"><button type="button" class="chip" data-act="money" data-d="1">Receive</button><button type="button" class="chip" data-act="money" data-d="-1">Spend</button></div>
${ledger ? `<ul class="cs-ledger">${ledger}</ul>` : ''}</section>
<section class="cs-sec"><h2>Items</h2><p class="small muted">Bulk ${res.bulk.value}${res.bulk.light ? ' and ' + res.bulk.light + ' light' : ''}: encumbered above ${res.bulk.encumbered}, maximum ${res.bulk.max}. Invested ${invested} of 10.</p>
${sec('held', 'Held')}${sec('worn', 'Worn')}${sec('stowed', 'Stowed')}${sec('dropped', 'Dropped')}${ch.inventory.length ? '' : '<p class="muted">No items yet.</p>'}
<div class="cs-togs"><button type="button" class="chip" data-act="item-pick">Add or buy an item</button><button type="button" class="chip" data-act="custom-item">Add a custom item</button></div></section>`;
}
function typeLabel(r) { return {weapon: 'Weapon', armor: 'Armour', shield: 'Shield', consumable: 'Consumable', equipment: 'Item', treasure: 'Treasure', backpack: 'Container', kit: 'Kit', ammo: 'Ammunition'}[r.t] || 'Item'; }
function runeSummary(r, inv) {
  const R = Object.assign({}, r.runes || {}, inv.runes || {});
  const p = [];
  if (R.potency) p.push('+' + R.potency);
  if (R.striking) p.push(['', 'striking', 'greater striking', 'major striking'][R.striking]);
  if (R.resilient) p.push(['', 'resilient', 'greater resilient', 'major resilient'][R.resilient]);
  if (R.reinforcing) p.push('reinforcing ' + R.reinforcing);
  for (const x of R.property || []) p.push(eng.t(((db.runes.WEAPON_PROPERTY_RUNES[x] || db.runes.ARMOR_PROPERTY_RUNES[x]) || {}).name || x));
  return p.length ? ': ' + esc(p.join(', ')) : '';
}

// ───────── Spells tab ─────────
function ensureClassEntry() {
  const cls = res.S.cls;
  if (!cls || !cls.sc) return;
  if ((ch.spells.entries || []).some(e => e.id === 'class')) return;
  const e = eng.defaultEntry(cls);
  if (e) { ch.spells.entries.unshift(e); putChar(ch); recompute(); }
}
function tabSpells() {
  ensureClassEntry();
  const out = [];
  for (const sc of res.spellcasting) {
    const e = sc.e;
    const known = (e.known || []).map(k => rec(k)).filter(Boolean);
    const cantrips = known.filter(r => (r.tr || []).includes('cantrip'));
    const maxRank = sc.slots ? sc.slots.reduce((m, n, i) => n > 0 && i > 0 ? i : m, 0) : Math.ceil(ch.level / 2);
    let body = '';
    if (sc.slots) {
      const rows = [];
      for (let rk = 1; rk < sc.slots.length; rk++) {
        const n = sc.slots[rk]; if (!n) continue;
        const cells = [];
        if (e.kind === 'prepared') {
          const prep = (e.prepared || {})[rk] || [];
          for (let i = 0; i < n; i++) {
            const k = prep[i], r = k ? rec(k) : null, used = ((e.used || {})[rk] || []).includes(i);
            cells.push(`<span class="cs-slot${used ? ' used' : ''}"><select data-act="prep" data-e="${esc(e.id)}" data-r="${rk}" data-i="${i}" aria-label="Rank ${rk} slot ${i + 1}"><option value="">Empty</option>${known.filter(s => !(s.tr || []).includes('cantrip') && (s.lv || 1) <= rk).map(s => `<option value="${esc(s.k)}"${s.k === k ? ' selected' : ''}>${esc(s.n)}${s.lv < rk ? ' (heightened)' : ''}</option>`).join('')}</select>${r ? g(r, 'Text') : ''}<label class="cs-tog"><input type="checkbox" data-act="cast" data-e="${esc(e.id)}" data-r="${rk}" data-i="${i}"${used ? ' checked' : ''}> Cast</label></span>`);
          }
        } else {
          const usedN = (e.usedN || {})[rk] || 0;
          cells.push(`<span class="cs-step"><button type="button" data-act="castn" data-e="${esc(e.id)}" data-r="${rk}" data-d="1" aria-label="Use a slot">−</button><b>${n - usedN}</b><button type="button" data-act="castn" data-e="${esc(e.id)}" data-r="${rk}" data-d="-1" aria-label="Restore a slot">+</button></span> <small>of ${n} left</small> `
            + known.filter(s => (s.lv || 1) === rk && !(s.tr || []).includes('cantrip')).map(s => g(s)).join(', '));
        }
        rows.push(`<tr><th>Rank ${rk}</th><td>${cells.join('')}</td></tr>`);
      }
      body += `<table class="cs-slots"><tbody><tr><th>Cantrips <small>rank ${sc.cantripRank}</small></th><td>${cantrips.map(r => g(r)).join(', ') || '<span class="muted">Add cantrips to the list below</span>'}</td></tr>${rows.join('')}</tbody></table>`;
      body += `<div class="cs-togs"><button type="button" class="chip" data-act="rest" data-e="${esc(e.id)}">Rest: clear cast slots</button></div>`;
    } else if (e.kind === 'focus') {
      body += `<p class="small muted">Focus spells cost 1 Focus Point. Your pool is ${res.focusMax}.</p>`;
    } else if (e.kind === 'innate') {
      body += `<p class="small muted">Innate spells: track uses in the notes on each spell.</p>`;
    }
    const list = known.slice().sort((a, b) => (a.lv || 0) - (b.lv || 0) || a.n.localeCompare(b.n)).map(s => `<li>${act(s.time && /^[123]$/.test(s.time) ? s.time : s.time === 'reaction' ? 'reaction' : s.time === 'free' ? 'free' : null)} ${g(s)} <small>${(s.tr || []).includes('cantrip') ? 'cantrip' : 'rank ' + s.lv}</small><button type="button" class="x" data-act="spell-del" data-e="${esc(e.id)}" data-k="${esc(s.k)}" aria-label="Remove">×</button></li>`).join('');
    const kindName = {prepared: e.id === 'class' && (ch.class === 'cl:wizard' || ch.class === 'cl:magus') ? 'Spellbook' : 'Spells you can prepare', spontaneous: 'Repertoire', focus: 'Focus spells', innate: 'Innate spells'}[e.kind] || 'Spells';
    out.push(`<section class="cs-sec cs-entry"><div class="cs-ehead"><input class="cs-ename" value="${esc(e.name)}" data-field="ename" data-e="${esc(e.id)}" aria-label="Name">
<select data-act="etrad" data-e="${esc(e.id)}" aria-label="Tradition">${['arcane', 'divine', 'occult', 'primal'].map(t => `<option value="${t}"${e.trad === t ? ' selected' : ''}>${cap(t)}</option>`).join('')}</select>
<select data-act="eattr" data-e="${esc(e.id)}" aria-label="Attribute">${ATTRS.map(a => `<option value="${a}"${e.attr === a ? ' selected' : ''}>${ATTR_NAME[a]}</option>`).join('')}</select>
${e.id !== 'class' ? `<button type="button" class="x" data-act="entry-del" data-e="${esc(e.id)}" aria-label="Remove this spellcasting">×</button>` : ''}</div>
<div class="cs-vitals small">${statBtn('spellatk:' + e.id, 'Spell attack', fmt(sc.attack.total), RANKS[sc.rank])}${statBtn('spelldc:' + e.id, 'Spell DC', sc.dc.total, RANKS[sc.rank])}</div>
${body}<h3>${kindName}</h3><ul class="cs-spells">${list || '<li class="muted">None yet.</li>'}</ul>
<button type="button" class="chip" data-act="spell-add" data-e="${esc(e.id)}" data-max="${maxRank}">Add a spell</button></section>`);
  }
  return out.join('') + `<section class="cs-sec"><h2>Add spellcasting</h2><p class="small muted">For an archetype's spellcasting, innate spells, focus spells or a staff.</p>
<div class="cs-inline"><select id="cs-newkind" aria-label="Kind"><option value="prepared">Prepared</option><option value="spontaneous">Spontaneous</option><option value="focus">Focus</option><option value="innate">Innate</option></select>
<select id="cs-newtrad" aria-label="Tradition">${['arcane', 'divine', 'occult', 'primal'].map(t => `<option value="${t}">${cap(t)}</option>`).join('')}</select>
<select id="cs-newattr" aria-label="Attribute">${ATTRS.map(a => `<option value="${a}"${a === 'int' ? ' selected' : ''}>${ATTR_NAME[a]}</option>`).join('')}</select>
<select id="cs-newtable" aria-label="Spell slots"><option value="">No slot table</option>${Object.keys(db.slots).map(k => `<option value="${k}">${cap(k)} slots</option>`).join('')}</select>
<button type="button" class="chip" data-act="entry-add">Add</button></div></section>`;
}

// ───────── Feats tab ─────────
function tabFeats() {
  const groups = {};
  const put = (k, it) => (groups[k] = groups[k] || []).push(it);
  for (const it of res.S.items) {
    const r = it.r;
    if (r.t !== 'feat') continue;
    const k = r.cat === 'classfeature' ? 'Class features' : r.cat === 'ancestryfeature' ? 'Ancestry features' : r.cat === 'ancestry' ? 'Ancestry feats' : r.cat === 'class' ? ((r.tr || []).includes('archetype') ? 'Archetype feats' : 'Class feats') : r.cat === 'skill' ? 'Skill feats' : r.cat === 'general' ? 'General feats' : 'Other';
    put(k, it);
  }
  const order = ['Ancestry feats', 'Class feats', 'Archetype feats', 'Skill feats', 'General feats', 'Class features', 'Ancestry features', 'Other'];
  return order.filter(k => groups[k]).map(k => `<section class="cs-sec"><h2>${k}</h2><ul class="cs-featlist">${groups[k].sort((a, b) => (a.lvl || 0) - (b.lvl || 0)).map(it =>
    `<li><span class="lv">${it.lvl || ''}</span>${act(it.r.act)} ${g(it.r)}${it.granted ? ` <small>from ${esc((res.S.byUid[it.parent] || {r: {n: ''}}).r.n)}</small>` : ''}</li>`).join('')}</ul></section>`).join('') || '<p class="muted">Choose an ancestry and class on the Build tab.</p>';
}

// ───────── Notes tab ─────────
function tabNotes() {
  const n = ch.notes || {};
  const f = (k, l, area) => area ? `<label class="cs-field"><span>${l}</span><textarea data-field="note" data-k="${k}" rows="6">${esc(n[k] || '')}</textarea></label>`
    : `<label class="cs-field"><span>${l}</span><input type="text" data-field="note" data-k="${k}" value="${esc(n[k] || '')}"></label>`;
  return `<section class="cs-sec cs-fields">${f('player', 'Player')}${f('xp', 'Experience points')}${f('age', 'Age')}${f('pronouns', 'Pronouns')}${f('height', 'Height')}${f('weight', 'Weight')}${f('ethnicity', 'Ethnicity or nationality')}${f('birthplace', 'Birthplace')}</section>
<section class="cs-sec">${f('appearance', 'Appearance', true)}${f('personality', 'Personality', true)}${f('allies', 'Allies and contacts', true)}${f('notes', 'Notes', true)}</section>
<section class="cs-sec"><h2>Saved data</h2><p class="small muted">Characters are saved on this device. Use Export to copy one to another device or keep a backup, and Import to load it.</p></section>`;
}

// ───────── pickers ─────────
function picker(title, kicker, items, onPick, opts = {}) {
  const box = document.createElement('div');
  box.className = 'cs-picker';
  box.innerHTML = `<label class="search"><input type="search" placeholder="Search" aria-label="Search"></label>${opts.filters || ''}<p class="small muted cs-pc"></p><ul class="cs-plist"></ul>`;
  const q = box.querySelector('input'), list = box.querySelector('.cs-plist'), count = box.querySelector('.cs-pc');
  let lim = 150;
  const draw = () => {
    const s = q.value.trim().toLowerCase();
    let m = items.filter(it => (!s || it.label.toLowerCase().includes(s)) && (!opts.filter || opts.filter(it, box)));
    if (s) m.sort((a, b) => (b.label.toLowerCase().startsWith(s) - a.label.toLowerCase().startsWith(s)));
    count.textContent = m.length + ' to choose from';
    list.innerHTML = m.slice(0, lim).map((it, i) => `<li><button type="button" class="chip mini" data-i="${items.indexOf(it)}">${esc(opts.verb || 'Choose')}</button>${opts.verb2 ? `<button type="button" class="chip mini" data-i2="${items.indexOf(it)}">${esc(opts.verb2)}</button>` : ''}<span class="n">${it.rec ? g(it.rec, it.label) : esc(it.label)}</span>${it.sub ? `<small>${it.sub}</small>` : ''}</li>`).join('')
      + (m.length > lim ? `<li><button type="button" class="chip" data-more="1">Show more</button></li>` : '');
  };
  let t;
  q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(() => { lim = 150; draw(); }, 120); });
  box.addEventListener('change', () => draw());
  box.addEventListener('click', e => {
    const b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.more) { lim += 150; draw(); return; }
    if (b.dataset.i != null) { onPick(items[+b.dataset.i], 1); if (!opts.keepOpen) A.popPanel(); else toast('Added ' + items[+b.dataset.i].label + '.'); }
    if (b.dataset.i2 != null) { onPick(items[+b.dataset.i2], 2); if (!opts.keepOpen) A.popPanel(); else toast('Bought ' + items[+b.dataset.i2].label + '.'); }
  });
  draw();
  A.pushPanel(kicker, title, box, 'picker:' + title);
  setTimeout(() => q.focus({preventScroll: true}), 50);
}
const recSub = r => [r.lv != null ? (r.t === 'spell' ? ((r.tr || []).includes('cantrip') ? 'Cantrip' : 'Rank ' + r.lv) : 'Level ' + r.lv) : '', (r.tr || []).filter(t => !['general', 'skill'].includes(t)).slice(0, 5).join(', '), r.src || ''].filter(Boolean).map(esc).join(' · ');

function pickOrigin(kind) {
  const type = {ancestry: 'ancestry', heritage: 'heritage', background: 'background', class: 'class', deity: 'deity'}[kind];
  let rs = Object.values(db.e).filter(r => r.t === type);
  if (kind === 'heritage') { const a = res.S.anc; rs = rs.filter(r => !r.anc || (a && r.anc === a.sl)); }
  const items = rs.map(r => ({label: r.n, rec: r, sub: recSub(r) + (kind === 'heritage' && !r.anc ? ' · versatile heritage' : '')})).sort((a, b) => a.label.localeCompare(b.label));
  picker('Choose ' + (kind === 'class' ? 'a class' : kind === 'ancestry' ? 'an ancestry' : 'a ' + kind), 'Build', items, it => {
    ch[kind] = it.rec.k;
    if (kind === 'ancestry') { ch.heritage = null; ch.boosts.ancestry = []; }
    if (kind === 'background') ch.boosts.background = [];
    if (kind === 'class') { ch.boosts.class = null; ch.spells.entries = (ch.spells.entries || []).filter(e => e.id !== 'class'); }
    commit();
  });
}
function pickFeat(slotId) {
  const slot = res.slots.find(s => s.id === slotId) || {id: slotId, lv: Number(slotId.split('-').pop()) || 1, kind: slotId.split('-')[0]};
  const rs = eng.featOptions(res, slot);
  const taken = new Set(Object.entries(ch.feats).filter(([k]) => k !== slotId).map(([, f]) => f && f.k));
  const items = rs.map(r => {
    const pr = eng.prereqs(res, r);
    const bad = pr.some(p => p.ok === false);
    return {label: r.n, rec: r, sub: recSub(r) + (r.pre ? ` · <span class="${bad ? 'cs-warn' : ''}">${esc(r.pre.join('; '))}</span>` : '') + (taken.has(r.k) && !r.max ? ' · already taken' : ''), bad};
  });
  const own = res.S.cls ? res.S.cls.sl : '';
  items.sort((a, b) => ((b.rec.tr || []).includes(own) - (a.rec.tr || []).includes(own)) || ((b.rec.lv || 0) - (a.rec.lv || 0)) || a.label.localeCompare(b.label));
  const filters = `<div class="cs-togs"><label class="cs-tog"><input type="checkbox" class="f-met" checked> Hide feats whose prerequisites aren't met</label></div>`;
  picker(slot.label || 'Choose a feat', 'Level ' + slot.lv, items, it => { ch.feats[slotId] = {k: it.rec.k}; commit(); },
    {filters, filter: (it, box) => !(box.querySelector('.f-met').checked && it.bad)});
}
function pickChoice(uid, flag) {
  const p = res.pending.find(x => x.uid === uid && x.flag === flag);
  if (!p) return;
  const opts = eng.choices(res.S, p);
  const items = opts.map(o => ({label: o.label, rec: o.rec, value: o.value, sub: o.rec ? recSub(o.rec) : ''}));
  picker(p.prompt, p.item.r.n, items, it => { (ch.choices[uid] = ch.choices[uid] || {})[flag] = it.value; commit(); });
}
function pickEffect() {
  const items = Object.values(db.e).filter(r => r.t === 'effect').map(r => ({label: r.n.replace(/^(Effect|Spell Effect|Stance): /, ''), rec: r, sub: esc((r.n.match(/^(Effect|Spell Effect|Stance)/) || ['Effect'])[0]) + (r.src ? ' · ' + esc(r.src) : '')}));
  items.sort((a, b) => a.label.localeCompare(b.label));
  picker('Add an effect', 'Sheet', items, it => { ch.effects[it.rec.k] = true; commit(); });
}
function pickItem() {
  const types = ['weapon', 'armor', 'shield', 'equipment', 'consumable', 'treasure', 'backpack', 'kit', 'ammo'];
  const items = Object.values(db.e).filter(r => types.includes(r.t)).map(r => ({label: r.n, rec: r, sub: `${esc(typeLabel(r))} · level ${r.lv || 0} · ${money(r.cp || 0)}` + (r.src ? ' · ' + esc(r.src) : '')}));
  items.sort((a, b) => a.label.localeCompare(b.label));
  const filters = `<div class="cs-inline"><select class="f-type" aria-label="Type"><option value="">All types</option>${types.map(t => `<option value="${t}">${typeLabel({t})}</option>`).join('')}</select>
<label class="cs-tog"><input type="checkbox" class="f-lv" checked> Level ${ch.level} or lower</label></div>`;
  picker('Add or buy an item', 'Inventory', items, (it, how) => {
    if (how === 2) {
      const cost = it.rec.cp || 0;
      if (coinTotal(ch.coins) < cost) { toast('Not enough money for ' + it.label + '.'); return; }
      spend(cost, 'Bought ' + it.label);
    }
    addInv(it.rec);
    commit();
  }, {verb: 'Add', verb2: 'Buy', keepOpen: true, filters, filter: (it, box) => {
    const t = box.querySelector('.f-type').value, lv = box.querySelector('.f-lv').checked;
    return (!t || it.rec.t === t) && (!lv || (it.rec.lv || 0) <= ch.level);
  }});
}
function addInv(r, extra) {
  const inv = Object.assign({id: newId(), k: r.k, qty: r.qty || 1, eq: r.t === 'armor' ? 'worn' : 'stowed'}, extra || {});
  if (r.t === 'kit' && r.kit) { for (const [k, q] of r.kit) { const x = rec(k); if (x) ch.inventory.push({id: newId(), k: x.k, qty: q || 1, eq: 'stowed'}); } return; }
  ch.inventory.push(inv);
}
function spend(cp, note) {
  let total = coinTotal(ch.coins) - cp;
  if (total < 0) total = 0;
  // keep platinum as it is when possible, and give change in gold, silver and copper
  const c = ch.coins;
  let pp = c.pp || 0;
  let rest = total - pp * 1000;
  if (rest < 0) { pp = Math.floor(total / 1000); rest = total - pp * 1000; }
  ch.coins = {pp, gp: Math.floor(rest / 100), sp: Math.floor(rest % 100 / 10), cp: rest % 10};
  ch.ledger.push({t: Date.now(), d: -cp, note});
}
function receive(cp, note) {
  ch.coins.gp = (ch.coins.gp || 0) + Math.floor(cp / 100);
  ch.coins.sp = (ch.coins.sp || 0) + Math.floor(cp % 100 / 10);
  ch.coins.cp = (ch.coins.cp || 0) + cp % 10;
  ch.ledger.push({t: Date.now(), d: cp, note});
}
function pickSpell(eid, max) {
  const e = ch.spells.entries.find(x => x.id === eid);
  const items = Object.values(db.e).filter(r => r.t === 'spell' && !r.ritual).map(r => ({label: r.n, rec: r, sub: recSub(r) + ' · ' + esc((r.trad || []).join(', '))}));
  items.sort((a, b) => a.label.localeCompare(b.label));
  const filters = `<div class="cs-inline"><label class="cs-tog"><input type="checkbox" class="f-trad" checked> ${cap(e.trad)} spells only</label>
<label class="cs-tog"><input type="checkbox" class="f-rank" checked> Rank ${max} or lower</label><select class="f-kind" aria-label="Kind"><option value="">Any</option><option value="cantrip">Cantrips</option><option value="focus">Focus spells</option><option value="spell">Other spells</option></select></div>`;
  picker('Add a spell', e.name, items, it => { e.known = e.known || []; if (!e.known.includes(it.rec.k)) e.known.push(it.rec.k); commit(); }, {verb: 'Add', keepOpen: true, filters, filter: (it, box) => {
    const r = it.rec, tr = r.tr || [];
    if (box.querySelector('.f-trad').checked && !(r.trad || []).includes(e.trad) && !(tr.includes('focus'))) return false;
    if (box.querySelector('.f-rank').checked && (r.lv || 1) > Math.max(1, max) && !tr.includes('cantrip')) return false;
    const k = box.querySelector('.f-kind').value;
    if (k === 'cantrip' && !tr.includes('cantrip')) return false;
    if (k === 'focus' && !tr.includes('focus')) return false;
    if (k === 'spell' && (tr.includes('cantrip') || tr.includes('focus'))) return false;
    return true;
  }});
}
function runesPanel(id) {
  const inv = ch.inventory.find(i => i.id === id); if (!inv) return;
  const r = eng.invRec(inv);
  const R = Object.assign({potency: 0, striking: 0, resilient: 0, reinforcing: 0, property: []}, r.runes || {}, inv.runes || {});
  const box = document.createElement('div');
  box.className = 'cs-runes';
  const sel = (k, n, labels) => `<label class="cs-field"><span>${labels[0]}</span><select data-k="${k}">${Array.from({length: n}, (_, i) => `<option value="${i}"${R[k] === i ? ' selected' : ''}>${labels[i + 1]}</option>`).join('')}</select></label>`;
  let html = '';
  const isW = r.t === 'weapon', isA = r.t === 'armor';
  if (isW || isA) html += sel('potency', 5, ['Potency', 'None', '+1', '+2', '+3', '+4']);
  if (isW) html += sel('striking', 4, ['Striking', 'None', 'Striking', 'Greater striking', 'Major striking']);
  if (isA) html += sel('resilient', 4, ['Resilient', 'None', 'Resilient', 'Greater resilient', 'Major resilient']);
  if (r.t === 'shield') html += sel('reinforcing', 7, ['Reinforcing', 'None', 'Minor', 'Lesser', 'Moderate', 'Greater', 'Major', 'Supreme']);
  const table = isW ? db.runes.WEAPON_PROPERTY_RUNES : isA ? db.runes.ARMOR_PROPERTY_RUNES : null;
  if (table) {
    const names = Object.entries(table).map(([k, v]) => [k, eng.t(v.name), v.level]).sort((a, b) => a[1].localeCompare(b[1]));
    const slots = R.potency || 0;
    for (let i = 0; i < Math.max(slots, (R.property || []).length); i++) {
      html += `<label class="cs-field"><span>Property rune ${i + 1}${i >= slots ? ' (no slot)' : ''}</span><select data-prop="${i}"><option value="">None</option>${names.map(([k, n, lv]) => `<option value="${k}"${(R.property || [])[i] === k ? ' selected' : ''}>${esc(n)} (level ${lv})</option>`).join('')}</select></label>`;
    }
  }
  box.innerHTML = html + `<p class="small muted">Property rune slots equal the potency rune's value.</p><button type="button" class="chip" data-save="1">Save</button>`;
  box.addEventListener('click', e => {
    if (!e.target.closest('[data-save]')) return;
    const nr = {};
    box.querySelectorAll('select[data-k]').forEach(s => nr[s.dataset.k] = Number(s.value));
    nr.property = [...box.querySelectorAll('select[data-prop]')].map(s => s.value).filter(Boolean);
    inv.runes = nr; commit(); A.popPanel();
  });
  A.pushPanel('Runes', inv.name || r.n, box, 'runes:' + id);
}
function customItem() {
  const box = document.createElement('div');
  box.className = 'cs-runes';
  box.innerHTML = `<p class="small muted">For relics and other items that aren't in the rules. Weapons and armour get Strikes and AC from these numbers.</p>
<label class="cs-field"><span>Name</span><input type="text" data-k="n" value=""></label>
<label class="cs-field"><span>Type</span><select data-k="t"><option value="weapon">Weapon</option><option value="armor">Armour</option><option value="equipment">Other item</option></select></label>
<label class="cs-field"><span>Level</span><input type="number" data-k="lv" value="0"></label>
<label class="cs-field"><span>Traits, separated by commas</span><input type="text" data-k="tr" placeholder="reach, trip, deadly-d10"></label>
<label class="cs-field"><span>Bulk (0.1 for light)</span><input type="number" step="0.1" data-k="bulk" value="1"></label>
<fieldset class="w"><legend>Weapon</legend><label class="cs-field"><span>Category</span><select data-k="cat"><option>simple</option><option selected>martial</option><option>advanced</option><option>unarmed</option></select></label>
<label class="cs-field"><span>Group</span><input type="text" data-k="grp" value="polearm"></label>
<label class="cs-field"><span>Damage die</span><select data-k="die"><option>d4</option><option>d6</option><option selected>d8</option><option>d10</option><option>d12</option></select></label>
<label class="cs-field"><span>Damage type</span><select data-k="dtype"><option>slashing</option><option>piercing</option><option>bludgeoning</option></select></label>
<label class="cs-field"><span>Range increment in feet (blank for melee)</span><input type="number" data-k="rng"></label></fieldset>
<fieldset class="a"><legend>Armour</legend><label class="cs-field"><span>Category</span><select data-k="acat"><option>light</option><option selected>medium</option><option>heavy</option><option>unarmored</option></select></label>
<label class="cs-field"><span>AC bonus</span><input type="number" data-k="ac" value="0"></label><label class="cs-field"><span>Dex cap</span><input type="number" data-k="dex" value="5"></label>
<label class="cs-field"><span>Check penalty</span><input type="number" data-k="chk" value="0"></label><label class="cs-field"><span>Speed penalty</span><input type="number" data-k="spd" value="0"></label>
<label class="cs-field"><span>Strength</span><input type="number" data-k="str" value="0"></label></fieldset>
<button type="button" class="chip" data-save="1">Add</button>`;
  box.addEventListener('click', e => {
    if (!e.target.closest('[data-save]')) return;
    const v = k => box.querySelector(`[data-k="${k}"]`).value;
    const t = v('t');
    const c = {n: v('n') || 'Custom item', t, lv: Number(v('lv')) || 0, tr: v('tr').split(',').map(s => slugify(s)).filter(Boolean), bulk: Number(v('bulk')) || 0};
    if (t === 'weapon') Object.assign(c, {cat: v('cat'), grp: slugify(v('grp')) || null, dmg: {dice: 1, die: v('die'), damageType: v('dtype')}, rng: Number(v('rng')) || null, runes: {potency: 0, striking: 0, property: []}});
    if (t === 'armor') Object.assign(c, {cat: v('acat'), ac: Number(v('ac')) || 0, dex: Number(v('dex')), chk: Number(v('chk')) || 0, spd: Number(v('spd')) || 0, str: Number(v('str')) || null, runes: {potency: 0, resilient: 0, property: []}});
    ch.inventory.push({id: newId(), custom: c, qty: 1, eq: t === 'armor' ? 'worn' : t === 'weapon' ? 'held2' : 'stowed'});
    commit(); A.popPanel();
  });
  A.pushPanel('Inventory', 'Custom item', box, 'custom-item');
}
function bonusSlot() {
  const box = document.createElement('div');
  box.className = 'cs-runes';
  box.innerHTML = `<label class="cs-field"><span>Kind of feat</span><select data-k="kind"><option value="skill">Skill feat</option><option value="general">General feat</option><option value="class">Class feat</option><option value="ancestry">Ancestry feat</option><option value="archetype">Archetype feat</option><option value="bonus">Any feat</option></select></label>
<label class="cs-field"><span>Level</span><input type="number" data-k="lv" value="${ch.level}" min="1" max="20"></label><label class="cs-field"><span>Label</span><input type="text" data-k="label" value="Bonus feat"></label>
<button type="button" class="chip" data-save="1">Add</button>`;
  box.addEventListener('click', e => {
    if (!e.target.closest('[data-save]')) return;
    const v = k => box.querySelector(`[data-k="${k}"]`).value;
    const lv = Math.max(1, Math.min(20, Number(v('lv')) || 1));
    ch.bonusSlots.push({id: `${v('kind')}-b${newId()}-${lv}`, lv, kind: v('kind'), label: v('label') || 'Bonus feat'});
    commit(); A.popPanel();
  });
  A.pushPanel('Build', 'Add a bonus feat slot', box, 'bonus-slot');
}

// ───────── breakdowns ─────────
function breakdown(k) {
  let st = null, title = '';
  if (k === 'ac') st = res.ac; else if (k === 'hp') st = res.hp; else if (k === 'perception') st = res.perception; else if (k === 'speed') st = res.speed;
  else if (k === 'initiative') st = res.initiative; else if (k === 'classdc') st = Object.values(res.classDCs).find(c => c.primary);
  else if (k.startsWith('save:')) st = res.saves[k.slice(5)]; else if (k.startsWith('skill:')) st = res.skills[k.slice(6)];
  else if (k.startsWith('strike:')) st = res.strikes[+k.slice(7)].attack; else if (k.startsWith('damage:')) st = res.strikes[+k.slice(7)].damage;
  else if (k.startsWith('spellatk:') || k.startsWith('spelldc:')) { const id = k.split(':')[1]; const sc = res.spellcasting.find(s => s.e.id === id); st = k.startsWith('spellatk') ? sc.attack : sc.dc; }
  if (!st) return;
  title = st.label;
  const base = /^(ac|classdc|spelldc)/.test(k) ? 10 : 0;
  const rows = (base ? [`<tr><td>Base</td><td>10</td><td></td></tr>`] : []).concat(st.mods.map(m => `<tr class="${m.applied ? '' : 'off'}"><td>${esc(m.label)}${m.situational ? ' <small>situational</small>' : ''}</td><td>${fmt(m.value)}</td><td><small>${esc(m.type || 'untyped')}${m.applied ? '' : m.situational ? '' : ', does not stack'}</small></td></tr>`));
  const box = document.createElement('div');
  box.className = 'cs-bd';
  const extra = k.startsWith('save:') && st.degree && st.degree.length ? `<p class="small">Successes are critical successes, from ${esc(st.degree.join(', '))}.</p>` : '';
  box.innerHTML = `<p class="cs-bdt"><b>${k === 'speed' ? st.total + ' feet' : base ? st.total : k === 'hp' ? st.total : fmt(st.total)}</b></p><table class="tbl"><tbody>${rows.join('')}</tbody></table>${extra}
<p class="small muted">Situational modifiers apply only when their condition holds, for example against an off-guard target.</p>`;
  A.pushPanel('Breakdown', title, box, 'bd:' + k);
}

// ───────── events ─────────
function onClick(e) {
  const b = e.target.closest('[data-act]');
  if (!b || b.tagName === 'SELECT' || (b.tagName === 'INPUT' && b.type !== 'button')) return;
  const a = b.dataset.act, d = b.dataset;
  if (a === 'tab') { tab = d.t; render(); return; }
  if (a === 'new') { const c = blank(); store.ids.push(c.id); store.cur = c.id; saveStore(); putChar(c); ch = c; recompute(); tab = 'build'; render(); return; }
  if (a === 'dup') { const c = JSON.parse(JSON.stringify(ch)); c.id = newId(); c.name += ' (copy)'; store.ids.push(c.id); store.cur = c.id; saveStore(); putChar(c); ch = c; recompute(); render(); toast('Duplicated.'); return; }
  if (a === 'delete') {
    if (!confirmInline(b, 'Delete ' + ch.name + '?')) return;
    localStorage.removeItem(PRE + ch.id); store.ids = store.ids.filter(i => i !== ch.id);
    if (!store.ids.length) { const c = blank(); store.ids.push(c.id); putChar(c); }
    store.cur = store.ids[0]; saveStore(); ch = getChar(store.cur); recompute(); render(); return;
  }
  if (a === 'export') { exportChar(); return; }
  if (a === 'level') { ch.level = Math.max(1, Math.min(20, ch.level + Number(d.d))); commit(); return; }
  if (a === 'hp') {
    const n = Math.max(0, Number(document.getElementById('cs-hpamt').value) || 0); if (!n) return;
    const hp = ch.hp;
    if (d.m === 'dmg') { const fromTemp = Math.min(hp.temp || 0, n); hp.temp = (hp.temp || 0) - fromTemp; hp.damage = Math.min(res.hp.total, (hp.damage || 0) + n - fromTemp); }
    else if (d.m === 'heal') hp.damage = Math.max(0, (hp.damage || 0) - n);
    else hp.temp = Math.max(hp.temp || 0, n);
    commit(); return;
  }
  if (a === 'dots') {
    const n = Number(d.n);
    if (d.k === 'hero') ch.heroPoints = ch.heroPoints === n ? n - 1 : n;
    else { const cur = res.focusMax - (ch.focusUsed || 0); ch.focusUsed = res.focusMax - (cur === n ? n - 1 : n); }
    commit(); return;
  }
  if (a === 'cond') { const c = ch.conditions; c[d.k] = Math.max(0, (Number(c[d.k]) || 0) + Number(d.d)); if (!c[d.k]) delete c[d.k]; commit(); return; }
  if (a === 'cond-off') { delete ch.conditions[d.k]; commit(); return; }
  if (a === 'effect-off') { delete ch.effects[d.k]; commit(); return; }
  if (a === 'effect-pick') { pickEffect(); return; }
  if (a === 'breakdown') { breakdown(d.k); return; }
  if (a === 'pick-origin') { pickOrigin(d.k); return; }
  if (a === 'clear-deity') { ch.deity = null; commit(); return; }
  if (a === 'pick-feat') { pickFeat(d.s); return; }
  if (a === 'clear-feat') { delete ch.feats[d.s]; commit(); return; }
  if (a === 'choice-pick') { pickChoice(d.uid, d.flag); return; }
  if (a === 'boost') { toggleBoost(d.k, d.a); return; }
  if (a === 'train') { const t = ch.trained; const i = t.indexOf(d.k); if (i >= 0) t.splice(i, 1); else t.push(d.k); commit(); return; }
  if (a === 'lore-add') { const v = document.getElementById('cs-lore').value.trim(); if (v) { ch.lores.push(/lore$/i.test(v) ? v : v + ' Lore'); commit(); } return; }
  if (a === 'lore-del') { ch.lores.splice(Number(d.i), 1); commit(); return; }
  if (a === 'lang-add') { const v = document.getElementById('cs-lang').value.trim(); if (v) { ch.languages.push(v.toLowerCase()); commit(); } return; }
  if (a === 'lang-del') { ch.languages.splice(Number(d.i), 1); commit(); return; }
  if (a === 'bonus-slot') { bonusSlot(); return; }
  if (a === 'bonus-del') { const s = ch.bonusSlots.splice(Number(d.i), 1)[0]; if (s) delete ch.feats[s.id]; commit(); return; }
  if (a === 'qty') { const inv = ch.inventory.find(i => i.id === d.id); inv.qty = Math.max(0, (inv.qty ?? 1) + Number(d.d)); commit(); return; }
  if (a === 'remove') { ch.inventory = ch.inventory.filter(i => i.id !== d.id); commit(); return; }
  if (a === 'sell') {
    const inv = ch.inventory.find(i => i.id === d.id); const r = eng.invRec(inv);
    const v = Math.floor((r.cp || 0) / 2);
    receive(v, 'Sold ' + (inv.name || r.n) + ' for half price');
    if ((inv.qty ?? 1) > 1) inv.qty -= 1; else ch.inventory = ch.inventory.filter(i => i.id !== d.id);
    commit(); toast('Sold for ' + money(v) + '.'); return;
  }
  if (a === 'runes') { runesPanel(d.id); return; }
  if (a === 'item-pick') { pickItem(); return; }
  if (a === 'custom-item') { customItem(); return; }
  if (a === 'money') {
    const amt = Number(document.getElementById('cs-mamt').value) || 0; if (!amt) return;
    const unit = document.getElementById('cs-munit').value, note = document.getElementById('cs-mnote').value.trim();
    const cp = Math.round(amt * {pp: 1000, gp: 100, sp: 10, cp: 1}[unit]);
    if (Number(d.d) < 0) { if (coinTotal(ch.coins) < cp) { toast('Not enough money.'); return; } spend(cp, note || 'Spent'); }
    else receive(cp, note || 'Received');
    commit(); return;
  }
  if (a === 'spell-add') { pickSpell(d.e, Number(d.max) || 1); return; }
  if (a === 'spell-del') { const e2 = ch.spells.entries.find(x => x.id === d.e); e2.known = (e2.known || []).filter(k => k !== d.k); commit(); return; }
  if (a === 'castn') { const e2 = ch.spells.entries.find(x => x.id === d.e); e2.usedN = e2.usedN || {}; const sc = res.spellcasting.find(s => s.e.id === d.e); const n = sc.slots[d.r]; e2.usedN[d.r] = Math.max(0, Math.min(n, (e2.usedN[d.r] || 0) + Number(d.d))); commit(); return; }
  if (a === 'rest') { const e2 = ch.spells.entries.find(x => x.id === d.e); e2.used = {}; e2.usedN = {}; ch.focusUsed = 0; commit(); toast('Slots restored.'); return; }
  if (a === 'entry-add') {
    const kind = document.getElementById('cs-newkind').value, trad = document.getElementById('cs-newtrad').value, attr = document.getElementById('cs-newattr').value, table = document.getElementById('cs-newtable').value;
    ch.spells.entries.push({id: newId(), name: cap(trad) + ' ' + kind + ' spells', trad, kind, attr, table: table || null, prof: 'class', known: [], prepared: {}, used: {}});
    commit(); return;
  }
  if (a === 'entry-del') { ch.spells.entries = ch.spells.entries.filter(x => x.id !== d.e); commit(); return; }
}
function confirmInline(b, msg) {
  if (b.dataset.armed) { delete b.dataset.armed; return true; }
  b.dataset.armed = '1'; const t = b.textContent; b.textContent = 'Select again to delete';
  setTimeout(() => { if (b.isConnected) { delete b.dataset.armed; b.textContent = t; } }, 4000);
  toast(msg + ' Select Delete again to confirm.');
  return false;
}
function toggleBoost(key, a) {
  const b = ch.boosts;
  if (key === 'class') { b.class = b.class === a ? null : a; commit(); return; }
  const arr = b[key] = b[key] || [];
  const i = arr.indexOf(a);
  if (i >= 0) { arr.splice(i, 1); commit(); return; }
  const anc = res.S.anc;
  const limit = key === 'ancestry' ? (ch.altBoosts ? 2 : anc ? anc.boosts.filter(o => o.length > 1).length : 0) : key === 'background' ? 2 : 4;
  if (arr.length >= limit) { toast('All of these boosts are already chosen. Remove one first.'); return; }
  if (key === 'background') {
    const opts = res.S.bg ? res.S.bg.boosts[0] || [] : [];
    if (arr.length === 1 && !opts.includes(arr[0]) && !opts.includes(a)) { toast('One background boost must go to ' + opts.map(x => ATTR_NAME[x]).join(' or ') + '.'); return; }
  }
  arr.push(a); commit();
}
function onChange(e) {
  const t = e.target, d = t.dataset;
  if (d.field === 'name') { ch.name = t.value.trim() || 'Unnamed'; commit(false); renderHeadOnly(); return; }
  if (d.field === 'coin') { ch.coins[d.k] = Math.max(0, Math.floor(Number(t.value) || 0)); commit(); return; }
  if (d.field === 'featlore') { const f = ch.feats[d.s]; if (f) { f.lore = t.value.trim(); commit(); } return; }
  if (d.field === 'note') { ch.notes[d.k] = t.value; putChar(ch); return; }
  if (d.field === 'ename') { const e2 = ch.spells.entries.find(x => x.id === d.e); e2.name = t.value; putChar(ch); return; }
  const a = d.act;
  if (a === 'switch') { store.cur = t.value; saveStore(); ch = getChar(store.cur); recompute(); render(); return; }
  if (a === 'import') { importFile(t.files[0]); t.value = ''; return; }
  if (a === 'cond-add') { if (t.value) { ch.conditions[t.value] = 1; commit(); } return; }
  if (a === 'effect') { if (t.checked) ch.effects[d.k] = true; else delete ch.effects[d.k]; commit(); return; }
  if (a === 'toggle') { ch.toggles[d.k] = t.checked; commit(); return; }
  if (a === 'choice') { (ch.choices[d.uid] = ch.choices[d.uid] || {})[d.flag] = t.value || undefined; if (!t.value) delete ch.choices[d.uid][d.flag]; commit(); return; }
  if (a === 'opt') { if (d.k === 'altBoosts') { ch.altBoosts = t.checked; ch.boosts.ancestry = []; } else ch.options[d.k] = t.checked; commit(); return; }
  if (a === 'inc') { ch.increases[d.lv] = t.value || undefined; if (!t.value) delete ch.increases[d.lv]; commit(); return; }
  if (a === 'int-train') { ch.intTrained[d.k] = t.value; commit(); return; }
  if (a === 'init') { ch.initiative = t.value || null; commit(); return; }
  if (a === 'state') { const inv = ch.inventory.find(i => i.id === d.id); inv.eq = t.value; commit(); return; }
  if (a === 'invest') {
    const inv = ch.inventory.find(i => i.id === d.id);
    if (t.checked && ch.inventory.filter(i => i.inv).length >= 10) { t.checked = false; toast('You can invest only 10 items.'); return; }
    inv.inv = t.checked; if (t.checked && (!inv.eq || inv.eq === 'stowed')) inv.eq = 'worn'; commit(); return;
  }
  if (a === 'prep') { const e2 = ch.spells.entries.find(x => x.id === d.e); e2.prepared = e2.prepared || {}; const arr = e2.prepared[d.r] = e2.prepared[d.r] || []; arr[Number(d.i)] = t.value || null; commit(); return; }
  if (a === 'cast') { const e2 = ch.spells.entries.find(x => x.id === d.e); e2.used = e2.used || {}; const arr = e2.used[d.r] = e2.used[d.r] || []; const i = Number(d.i); if (t.checked) { if (!arr.includes(i)) arr.push(i); } else e2.used[d.r] = arr.filter(x => x !== i); commit(); return; }
  if (a === 'etrad') { ch.spells.entries.find(x => x.id === d.e).trad = t.value; commit(); return; }
  if (a === 'eattr') { ch.spells.entries.find(x => x.id === d.e).attr = t.value; commit(); return; }
}
function renderHeadOnly() { const s = root.querySelector('.cs-pick select'); if (s) s.innerHTML = store.ids.map(id => { const c = id === ch.id ? ch : getChar(id); return c ? `<option value="${esc(id)}"${id === ch.id ? ' selected' : ''}>${esc(c.name)} (level ${c.level})</option>` : ''; }).join(''); }

async function exportChar() {
  const data = JSON.stringify(ch, null, 1);
  const name = slugify(ch.name) + '.aspera.json';
  const file = new File([data], name, {type: 'application/json'});
  if (navigator.canShare && navigator.canShare({files: [file]})) {
    try { await navigator.share({files: [file], title: ch.name}); return; } catch (e) { if (e.name === 'AbortError') return; }
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(file); a.download = name; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
}
function importFile(f) {
  if (!f) return;
  const rd = new FileReader();
  rd.onload = () => {
    try {
      const c = JSON.parse(rd.result);
      if (c.format !== 'aspera-character') throw new Error('format');
      const base = blank();
      const merged = Object.assign(base, c);
      if (store.ids.includes(merged.id)) merged.id = newId();
      store.ids.push(merged.id); store.cur = merged.id; saveStore(); putChar(merged); ch = merged; recompute(); render(); toast('Imported ' + merged.name + '.');
    } catch (e) { toast('That file is not an exported Aspera character.'); }
  };
  rd.readAsText(f);
}

async function init(el) {
  root = el;
  el.innerHTML = '<p class="muted" id="cs-load">Loading the rules data…</p>';
  try { await loadDB((n, t) => { const p = document.getElementById('cs-load'); if (p) p.textContent = `Loading the rules data (${n} of ${t})…`; }); }
  catch (e) { el.innerHTML = '<p class="muted">The rules data could not be loaded. Reload to try again.</p>'; return; }
  loadStore();
  store.ids = store.ids.filter(id => localStorage.getItem(PRE + id));
  if (!store.ids.length) {
    try {
      const r = await fetch('assets/cs/cyrus.json');
      const c = Object.assign(blank(), await r.json());
      c.id = newId(); store.ids.push(c.id); putChar(c);
    } catch (e) { const c = blank(); store.ids.push(c.id); putChar(c); }
  }
  if (!store.ids.includes(store.cur)) store.cur = store.ids[0];
  saveStore();
  ch = getChar(store.cur);
  for (const [k, v] of Object.entries(blank())) if (ch[k] == null) ch[k] = v;
  recompute();
  render();
  el.addEventListener('click', onClick);
  el.addEventListener('change', onChange);
}
window.AsperaSheet = {init};
})();
