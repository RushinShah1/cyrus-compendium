/* Aspera character sheet: builder, play sheet with dice and encounter tracking, inventory and gold, spellcasting, feats
   and notes. Characters are saved on this device. */
(function () {
'use strict';
const E = window.CSEngine;
const {Engine, SKILLS, ATTRS, ATTR_NAME, RANKS, slugify, fmt} = E;
const A = window.Aspera;
const esc = t => String(t == null ? '' : t).replace(/[&<>"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]));
const cap = s => String(s || '').replace(/^\w/, c => c.toUpperCase());
const RANK_L = ['U', 'T', 'E', 'M', 'L'];
const ACT = {'1': 'One action', '2': 'Two actions', '3': 'Three actions', reaction: 'Reaction', free: 'Free action'};
const GLYPH = {'1': '1', '2': '2', '3': '3', reaction: 'R', free: 'F'};
const STORE = 'aspera-chars-v1', PRE = 'aspera-char:';
const TRADS = ['arcane', 'divine', 'occult', 'primal'];
const KIND_NAME = {prepared: 'Prepared', spontaneous: 'Spontaneous', focus: 'Focus', innate: 'Innate', staff: 'Staff'};
const KIND_ICON = {prepared: 'book', spontaneous: 'mind', focus: 'eye', innate: 'ghost', staff: 'staff'};
const CONDITIONS = ['blinded', 'clumsy', 'concealed', 'confused', 'controlled', 'dazzled', 'deafened', 'drained', 'enfeebled', 'fascinated',
  'fatigued', 'fleeing', 'frightened', 'grabbed', 'hidden', 'immobilized', 'invisible', 'off-guard', 'paralyzed', 'persistent-damage', 'petrified', 'prone',
  'quickened', 'restrained', 'sickened', 'slowed', 'stunned', 'stupefied', 'unconscious', 'undetected'];
const ic = n => `<svg class="ic" aria-hidden="true"><use href="#i-${n}"/></svg>`;
const DEGREES = ['Critical failure', 'Failure', 'Success', 'Critical success'];

let db = null, eng = null, ch = null, res = null, root = null, tab = 'sheet', store = {cur: null, ids: []}, trayOpen = false;

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
  try { const r = await fetch('assets/cs/grades.json'); if (r.ok) GR = await r.json(); } catch (e) { /* grades are optional */ }
  db = out; eng = new Engine(db);
  return db;
}
const rec = k => eng.rec(k);

// ───────── storage ─────────
function loadStore() { try { store = JSON.parse(localStorage.getItem(STORE)) || {cur: null, ids: []}; } catch (e) { store = {cur: null, ids: []}; } }
function saveStore() { try { localStorage.setItem(STORE, JSON.stringify(store)); } catch (e) {} }
function getChar(id) { try { return JSON.parse(localStorage.getItem(PRE + id)); } catch (e) { return null; } }
function putChar(c) {
  c.updated = Date.now();
  try { localStorage.setItem(PRE + c.id, JSON.stringify(c)); }
  catch (e) { toast('This device has run out of space for saved characters. Export a copy and delete one you no longer need.'); }
}
const newId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
function blank(name) {
  return {format: 'aspera-character', v: 1, mig: 4, id: newId(), name: name || 'New character', level: 1, ancestry: null, heritage: null, background: null, class: null, deity: null,
    boosts: {ancestry: [], background: [], class: null, 1: [], 5: [], 10: [], 15: [], 20: []}, trained: [], lores: [], increases: {}, intTrained: {}, languages: [],
    feats: {}, choices: {}, inventory: [], coins: {pp: 0, gp: 15, sp: 0, cp: 0}, ledger: [], hp: {damage: 0, temp: 0}, heroPoints: 1, focusUsed: 0,
    conditions: {}, effects: {}, toggles: {}, spells: {entries: []}, notes: {}, options: {freeArchetype: false}, bonusSlots: [], bonusInc: {},
    log: [], enc: {on: false, round: 0, actions: 3, reaction: true, attacks: 0}, target: {dc: null}, uses: {}, trackers: {}, rollMode: 'normal'};
}
// bring characters saved by earlier versions up to date
const STAVE = [['time-sense', 0, 8], ['figment', 0, 8], ['sure-strike', 1, 8], ['befuddle', 1, 8], ['illusory-object', 1, 8], ['loose-times-arrow', 2, 8], ['invisibility', 2, 8],
  ['embed-message', 2, 8], ['time-jump', 3, 8], ['slow', 3, 8], ['illusory-disguise', 3, 8], ['wall-of-mirrors', 4, 10], ['vision-of-death', 4, 10], ['space-fold-gate', 5, 12],
  ['synesthesia', 5, 12], ['cast-into-time', 6, 14], ['mislead', 6, 14], ['clairvoyance', 4, 16], ['haste', 7, 16], ['true-target', 7, 16]];
const ASPERA_RELIC = {relic: true, aspects: ['Time', 'Mind'], page: 'aspera',
  desc: "Cyrus's relic polearm. Reach 10 feet, including two squares diagonally.",
  abil: [{n: 'Shadow Synthesis', text: "Aspera counts as leaving a hand free for Laughing Shadow's extra damage against off-guard targets while you hold it in both hands."}],
  gifts: [{n: 'Repository of Knowledge', g: 'relics-174', lv: 3, kind: 'First minor gift'}, {n: 'Sands of the Hourglass', g: 'relics-216', lv: 5, kind: 'Second minor gift'},
    {n: 'Precognition', g: 'relics-217', lv: 9, kind: 'First major gift'}, {n: 'Temporal Pulse', g: 'relics-218', lv: 13, kind: 'Second major gift'}, {n: 'Unrestricted Quickening', lv: 17, kind: 'Grand gift', text: "While you're wielding the relic, you can use the extra action from the quickened condition for any action, or as part of any activity, regardless of the restrictions of the effect that made you quickened. Quick Start: when you roll initiative, you become quickened until the end of your first turn."},
    {n: 'Unravelling Strike', lv: 17, kind: 'Relic ability', text: "Free action (concentrate), once per hour. Trigger: you hit a creature with a Strike using the relic, including a Strike made as part of Spellstrike. Effect: the relic attempts to counteract one spell or magical effect on the target, chosen by you. If you don't know what effects are on the target, it attempts to counteract the effect with the highest rank."},
    {n: 'Arcane Persuasion', lv: 17, kind: 'Relic ability', text: "While the relic is on your person, you gain a +2 item bonus to Arcana and Society checks. When you interact with spellcasters or creatures with magical traits, or the subject is magic, you can use Arcana in place of Diplomacy to Make an Impression or Request, and in place of Deception to Lie."}]};
function asperaStave() {
  return {id: 'staff-aspera', name: "Aspera's stave", kind: 'staff', trad: 'arcane', attr: 'int', prof: 'class', known: [], used: 0, extra: 0,
    staff: STAVE.map(([s, rank, lv]) => ({k: 'sp:' + s, rank, lv})), note: 'Cast through Aspera with Fused Staff. Synesthesia needs occult spellcasting.'};
}
function migrate(c) {
  for (const [k, v] of Object.entries(blank())) if (c[k] == null) c[k] = v;
  if ((c.mig || 1) < 2) {
    const asp = c.inventory.find(i => i.id === 'aspera' && i.custom);
    if (asp && !asp.custom.rules) {
      asp.custom.rules = [{key: 'RollOption', option: 'hands-free:but-really:1', itemOnly: true}];
      asp.custom.abil = [{n: 'Shadow Synthesis', text: "Aspera counts as leaving a hand free for Laughing Shadow's extra damage against off-guard targets while you hold it in both hands."}];
    }
    if (asp && !c.spells.entries.some(e => e.kind === 'staff')) c.spells.entries.push(asperaStave());
    c.mig = 2;
  }
  if (c.mig < 3) {
    const asp = c.inventory.find(i => i.id === 'aspera' && i.custom);
    if (asp) {
      // the plan takes Perception with Canny Acumen; earlier versions of the preset left it unchosen
      const k = 'background>ft:canny-acumen', cur = c.choices[k] || {};
      if (!cur.cannyAcumen) c.choices[k] = Object.assign(cur, {cannyAcumen: 'system.perception.rank'});
      Object.assign(asp.custom, Object.assign({}, ASPERA_RELIC, {abil: asp.custom.abil || ASPERA_RELIC.abil}));
    }
    c.mig = 3;
  }
  if (c.mig < 4) {
    // Aspera's fifth gift is now a custom grand gift with two relic abilities
    const asp = c.inventory.find(i => i.id === 'aspera' && i.custom);
    if (asp && asp.custom.relic) {
      asp.custom.gifts = ASPERA_RELIC.gifts.map(x => Object.assign({}, x));
      asp.custom.rules = (asp.custom.rules || []).filter(r => r.label !== 'Aspera (Arcane Persuasion)')
        .concat([{key: 'FlatModifier', selector: ['arcana', 'society'], type: 'item', value: 2, label: 'Aspera (Arcane Persuasion)', predicate: [{gte: ['self:level', 17]}]}]);
    }
    c.mig = 4;
  }
  return c;
}

// ───────── compute and render ─────────
function recompute() { res = eng.compute(ch); resPlan = null; }
// the build computed at level 20, so choices on feats and features planned above the current level can be made now
let resPlan = null;
function planRes() { return resPlan || (resPlan = eng.compute(Object.assign(JSON.parse(JSON.stringify(ch)), {level: 20}))); }
function findPending(uid, flag) { return res.pending.find(x => x.uid === uid && x.flag === flag) || planRes().pending.find(x => x.uid === uid && x.flag === flag); }
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
const legTag = r => r && r.leg ? ` <span class="cs-leg" title="Legacy printing, renamed in the remaster as ${esc(r.now)}">legacy</span>` : '';
function statBtn(key, label, val, sub, roll) {
  const k = esc(key);
  return `<div class="cs-stat${roll ? ' rollable' : ''}"><button type="button" class="cs-sl" data-act="breakdown" data-k="${k}" title="How ${esc(label)} is made up">${esc(label)}</button>
<button type="button" class="cs-sv" data-act="${roll ? 'roll' : 'breakdown'}" data-k="${k}" aria-label="${roll ? 'Roll ' + esc(label) : esc(label) + ' breakdown'}">${roll ? ic('dice') : ''}<b>${esc(val)}</b></button>${sub ? `<small>${esc(sub)}</small>` : ''}</div>`;
}

function render() {
  if (!root) return;
  ensureEntries();   // class and archetype spellcasting must exist for staff charges and Spellstrike
  const y = window.scrollY;
  const tabs = [['sheet', 'Sheet'], ['build', 'Build'], ['inventory', 'Inventory'], ['spells', 'Spells'], ['feats', 'Feats'], ['notes', 'Notes']];
  const todo = openChoices().length + (res.wastedInc || []).length;
  root.innerHTML = head() + encounterBar()
    + `<div class="cs-bar">${mini()}<nav class="cs-tabs" role="tablist">${tabs.map(([t, l]) => `<button type="button" role="tab" aria-selected="${t === tab}" class="${t === tab ? 'on' : ''}" data-act="tab" data-t="${t}">${l}${t === 'build' && todo ? ` <span class="cs-count" title="${todo} choice${todo > 1 ? 's' : ''} to make">${todo}</span>` : ''}</button>`).join('')}</nav></div>`
    + `<div class="cs-body">${({sheet: tabSheet, build: tabBuild, inventory: tabInventory, spells: tabSpells, feats: tabFeats, notes: tabNotes})[tab]()}</div>` + tray();
  window.scrollTo(0, y);
}

const RANK_NAMES = ['untrained', 'trained', 'expert', 'master', 'legendary'];
function wastedText(w) {
  const name = (res.skills[w.k] && res.skills[w.k].label) || cap(w.k);
  return `The skill increase at level ${w.lv} (${name}) has no effect: ${name} is already ${RANK_NAMES[w.rank]} by then${w.cap === 2 ? ', and master needs level 7' : w.cap === 3 ? ', and legendary needs level 15' : ''}.`;
}

// choices the rules leave open at or below the current level
function openChoices() {
  const out = res.pending.filter(p => p.value == null && !p.uid.startsWith('effect:')).map(p => ({p}));
  const b = ch.boosts || {}, anc = res.S.anc;
  const need = [['ancestry', 'ancestry', ch.altBoosts ? 2 : anc ? anc.boosts.filter(o => o.length > 1).length : 0, 1], ['background', 'background', res.S.bg ? 2 : 0, 1], ['class', 'class key attribute', res.S.cls ? 1 : 0, 1],
    ['1', 'level 1', 4, 1], ['5', 'level 5', 4, 5], ['10', 'level 10', 4, 10], ['15', 'level 15', 4, 15], ['20', 'level 20', 4, 20]];
  for (const [k, l, n, lv] of need) {
    const have = k === 'class' ? (b.class ? 1 : 0) : (b[k] || []).length;
    if (lv <= ch.level && have < n) out.push({slot: {label: `Attribute boosts for ${l} (${have} of ${n})`, lv, boost: true}});
  }
  for (const sl of res.slots) {
    if (sl.lv > ch.level || sl.kind === 'boost') continue;
    if (sl.kind === 'increase') { if (!(sl.bonus ? (ch.bonusInc || {})[sl.id] : (ch.increases || {})[sl.lv])) out.push({slot: sl}); continue; }
    const f = (ch.feats || {})[sl.id];
    if (!f || !rec(f.k)) out.push({slot: sl});
  }
  return out;
}
function todoSection() {
  const open = openChoices(), wasted = res.wastedInc || [];
  if (!open.length && !wasted.length) return '';
  const ch1 = open.filter(o => o.p).map(o => choiceUI(o.p)).join('');
  const sl = open.filter(o => o.slot);
  const slots = sl.length ? `<p class="small">${sl.length === 1 ? 'One build choice is' : sl.length + ' build choices are'} still open: ${esc(sl.map(o => o.slot.boost ? o.slot.label : `${o.slot.label} at level ${o.slot.lv}`).join(', '))}. <button type="button" class="chip mini" data-act="tab" data-t="build">Open the Build tab</button></p>` : '';
  const wl = wasted.map(w => `<p class="small">${esc(wastedText(w))} <button type="button" class="chip mini" data-act="tab" data-t="build">Change it on the Build tab</button></p>`).join('');
  return `<section class="cs-sec cs-todo"><h2>Choices to make</h2><p class="small muted">These affect your numbers and are not chosen yet, or have no effect as chosen.</p>${ch1 ? `<div class="cs-choices">${ch1}</div>` : ''}${slots}${wl}</section>`;
}

// a compact bar that stays at the top while scrolling
const pips = (n, max) => Array.from({length: max}, (_, i) => `<i class="${i < n ? 'on' : ''}"></i>`).join('');
function maxActions() {
  const c = ch.conditions || {};
  return Math.max(0, 3 + (c.quickened || (ch.effects || {})['se:spell-effect-haste'] ? 1 : 0) - (Number(c.slowed) || 0) - (Number(c.stunned) || 0));
}
function mini() {
  const hp = res.hp.total, cur = Math.max(0, hp - (ch.hp.damage || 0));
  const e = ch.enc;
  return `<div class="cs-mini" aria-label="Summary"><b class="n">${esc(ch.name)}</b>
<span class="hp"><span class="bar"><span style="width:${hp ? Math.round(100 * cur / hp) : 0}%"></span></span>${cur}/${hp} HP${ch.hp.temp ? ` +${ch.hp.temp}` : ''}</span>
<span>AC ${res.ac.total}</span>${res.S.opts.has('feature:spellstrike') ? `<span class="${ch.trackers.spellstrike !== false ? 'ok' : 'muted'}">Spellstrike ${ch.trackers.spellstrike !== false ? 'charged' : 'expended'}</span>` : ''}${e.on ? `<span>Round ${e.round}</span><span class="pips">${pips(e.actions, maxActions())}</span>` : ''}</div>`;
}

function head() {
  const opts = store.ids.map(id => { const c = id === ch.id ? ch : getChar(id); return c ? `<option value="${esc(id)}"${id === ch.id ? ' selected' : ''}>${esc(c.name)} (level ${c.level})</option>` : ''; }).join('');
  const cls = res.S.cls, anc = res.S.anc, her = res.S.her, bg = res.S.bg;
  const line = [anc ? (her ? her.n : anc.n) : 'No ancestry', bg ? bg.n : 'No background', cls ? cls.n : 'No class'].join(' · ');
  const hp = res.hp.total, cur = Math.max(0, hp - (ch.hp.damage || 0)), temp = ch.hp.temp || 0;
  const pct = hp ? Math.round(100 * cur / hp) : 0;
  const saves = Object.entries(res.saves).map(([k, v]) => statBtn('save:' + k, v.label, fmt(v.total), RANKS[v.rank], true)).join('');
  const cdc = Object.values(res.classDCs).find(c => c.primary);
  const dots = (n, max, k) => `<span class="cs-dots" role="group" aria-label="${k}">${Array.from({length: max}, (_, i) => `<button type="button" class="${i < n ? 'on' : ''}" data-act="dots" data-k="${k}" data-n="${i + 1}" aria-label="${k} ${i + 1}"></button>`).join('')}</span>`;
  const step = (k, v) => `<span class="cs-step"><button type="button" data-act="cond" data-k="${k}" data-d="-1" aria-label="Lower ${k}">−</button><b>${v || 0}</b><button type="button" data-act="cond" data-k="${k}" data-d="1" aria-label="Raise ${k}">+</button></span>`;
  const c = ch.conditions || {};
  const dying = c.dying || 0, dead = dying >= res.dyingMax;
  return `<div class="cs-top">
<label class="cs-pick"><span class="sr">Character</span><select data-act="switch">${opts}</select></label>
<button type="button" class="chip" data-act="new">New</button><button type="button" class="chip" data-act="dup">Duplicate</button>
<button type="button" class="chip" data-act="export">Export</button><label class="chip cs-file">Import<input type="file" accept=".json,application/json" data-act="import" hidden></label>
<button type="button" class="chip" data-act="delete">Delete</button></div>
<header class="cs-head"><div class="cs-id"><input class="cs-name" value="${esc(ch.name)}" data-field="name" aria-label="Character name">
<div class="cs-line">Level <span class="cs-step"><button type="button" data-act="level" data-d="-1" aria-label="Lower level">−</button><b>${ch.level}</b><button type="button" data-act="level" data-d="1" aria-label="Raise level">+</button></span> · ${esc(line)}</div>
<div class="cs-rest"><button type="button" class="chip" data-act="rest-night">${ic('rest')}Rest for the night</button>${res.focusMax ? '<button type="button" class="chip" data-act="refocus">Refocus</button>' : ''}</div></div>
<div class="cs-hp${dying ? ' dying' : ''}"><div class="cs-hpbar"><span style="width:${pct}%"></span>${temp ? `<span class="t" style="width:${Math.min(100, Math.round(100 * temp / hp))}%"></span>` : ''}</div>
<div class="cs-hpnum"><button type="button" class="cs-sv bare" data-act="breakdown" data-k="hp"><b>${cur}</b><small>of ${hp} Hit Points</small></button>${temp ? `<span class="cs-temp">+${temp} temporary</span>` : ''}
${dying ? `<span class="cs-dying">${dead ? 'Dead' : 'Dying ' + dying}</span>` : ''}</div>
<div class="cs-hpin"><input type="number" inputmode="numeric" min="0" placeholder="Amount" aria-label="Amount" id="cs-hpamt"><button type="button" class="chip" data-act="hp" data-m="dmg">Damage</button><button type="button" class="chip" data-act="hp" data-m="heal">Heal</button><button type="button" class="chip" data-act="hp" data-m="temp">Temporary</button>
${dying && !dead ? `<button type="button" class="chip warn" data-act="recovery">Recovery check (DC ${10 + dying})</button>` : ''}</div></div>
</header>
<div class="cs-vitals">${statBtn('ac', 'AC', res.ac.total, RANKS[res.ac.rank])}${saves}${statBtn('perception', 'Perception', fmt(res.perception.total), RANKS[res.perception.rank], true)}
${statBtn('speed', 'Speed', res.speed.total + ' ft', Object.entries(res.otherSpeeds).map(([k, v]) => k + ' ' + v.total).join(', '))}${cdc ? statBtn('classdc', 'Class DC', cdc.total, RANKS[cdc.rank]) : ''}${statBtn('initiative', 'Initiative', fmt(res.initiative.total), ch.initiative ? cap(ch.initiative) : 'Perception', true)}</div>
<div class="cs-attrs" role="group" aria-label="Attribute modifiers">${ATTRS.map(a => { const ap = res.apex && res.apex.attr === a;
  return `<button type="button" class="cs-attr${ap ? ' apex' : ''}" data-act="breakdown" data-k="attr:${a}" title="${esc(ATTR_NAME[a] || a)}${ap ? ', raised by ' + esc(res.apex.name) : ''}"><span>${a.toUpperCase()}</span><b>${fmt(res.attributes[a])}</b>${ap ? '<small>Apex</small>' : ''}</button>`; }).join('')}</div>
${(res.apexExtra || []).length ? `<p class="small cs-warn">Only one apex item can raise an attribute at a time. ${esc(res.apexExtra.join(', '))} ${res.apexExtra.length > 1 ? 'are' : 'is'} invested but not raising an attribute.</p>` : ''}
<div class="cs-res"><span><b>Hero Points</b>${dots(ch.heroPoints || 0, res.heroMax, 'hero')}</span>${res.focusMax ? `<span><b>Focus Points</b>${dots(res.focusMax - (ch.focusUsed || 0), res.focusMax, 'focus')}</span>` : ''}
<span><b>Dying</b>${step('dying', c.dying)}</span><span><b>Wounded</b>${step('wounded', c.wounded)}</span><span><b>Doomed</b>${step('doomed', c.doomed)}</span>
${res.S.autoEncumbered ? '<span class="cs-warn">Encumbered by Bulk</span>' : ''}</div>`;
}

function encounterBar() {
  const e = ch.enc;
  if (!e.on) return `<div class="cs-enc off"><button type="button" class="chip" data-act="enc-start">${ic('combat')}Start an encounter</button><span class="small muted">Rolls initiative, then tracks rounds, actions, the multiple attack penalty, conditions that wear off and effect durations.</span></div>`;
  const max = maxActions();
  const map = Math.min(e.attacks, 2);
  return `<div class="cs-enc"><b>Round ${e.round}</b>
<span class="cs-acts3" role="group" aria-label="Actions">${Array.from({length: max}, (_, i) => `<button type="button" class="${i < e.actions ? 'on' : ''}" data-act="enc-action" data-n="${i + 1}" aria-label="Action ${i + 1}"></button>`).join('')}</span>
<button type="button" class="cs-react${e.reaction ? ' on' : ''}" data-act="enc-react" aria-pressed="${e.reaction}">Reaction ${e.reaction ? 'ready' : 'used'}</button>
<span class="small">Attacks this turn: ${e.attacks} (next is the ${['first', 'second', 'third'][map]})</span>
<button type="button" class="chip" data-act="enc-end">End turn</button><button type="button" class="chip" data-act="enc-stop">End encounter</button></div>`;
}

// ───────── dice ─────────
const die = n => 1 + Math.floor(Math.random() * n);
function rollFormula(f) {
  const terms = String(f).replace(/\s+/g, '').replace(/-/g, '+-').split('+').filter(Boolean);
  const parts = [];
  let total = 0, k = 0;
  for (const t of terms) {
    const m = t.match(/^(-?)(\d*)d(\d+)$/i);
    if (m) {
      const n = Math.min(Number(m[2] || 1), 200), faces = Number(m[3]);
      if (!faces) return null;
      const rolls = Array.from({length: n}, () => die(faces));
      const sum = rolls.reduce((a, b) => a + b, 0) * (m[1] ? -1 : 1);
      parts.push({die: 'd' + faces, rolls, neg: !!m[1]}); total += sum;
    } else if (/^-?\d+$/.test(t)) { k += Number(t); total += Number(t); }
    else return null;
  }
  return {total, parts, k};
}
function degreeOf(total, nat, dc) {
  if (dc == null || dc === '' || Number.isNaN(Number(dc))) return null;
  dc = Number(dc);
  let dg = total >= dc + 10 ? 3 : total >= dc ? 2 : total <= dc - 10 ? 0 : 1;
  if (nat === 20) dg = Math.min(3, dg + 1);
  if (nat === 1) dg = Math.max(0, dg - 1);
  return dg;
}
function pushLog(entry) {
  entry.t = Date.now(); entry.id = newId();
  ch.log = (ch.log || []).concat([entry]).slice(-60);
  trayOpen = true;
}
function check(label, mod, opts = {}) {
  const mode = opts.mode || ch.rollMode || 'normal';
  const a = die(20), b = mode !== 'normal' ? die(20) : null;
  const nat = b == null ? a : mode === 'twice-high' ? Math.max(a, b) : Math.min(a, b);
  const total = nat + mod;
  const dc = 'dc' in opts ? opts.dc : ch.target.dc;
  let dg = degreeOf(total, nat, dc);
  if (dg === 2 && opts.successUp) dg = 3;
  const entry = {kind: 'check', label, mod, d20: b == null ? [a] : [a, b], nat, total, dc: dc == null || dc === '' ? null : Number(dc), dg, mode, ctx: opts.ctx || null, sub: opts.sub || ''};
  pushLog(entry);
  if (!opts.mode) ch.rollMode = 'normal';
  return entry;
}
function damageRoll(label, parts, crit, ctx) {
  // ordinary damage is doubled on a critical hit; critical-only dice (deadly, fatal, rune effects) are added once
  const out = [];
  let total = 0;
  for (const p of parts) {
    if (p.critOnly && !crit) continue;
    const r = rollFormula(p.f);
    if (!r) continue;
    const mult = crit && !p.critOnly ? 2 : 1;
    out.push({f: p.f, t: p.t, c: p.c, from: p.from, rolls: r.parts, sub: r.total, v: r.total * mult, mult, heal: p.heal});
    total += r.total * mult;
  }
  const entry = {kind: 'damage', label: label + (crit ? ' (critical)' : ''), parts: out, total, ctx: ctx || null, basic: ctx && ctx.basic};
  pushLog(entry);
  return entry;
}
function strikeDamageParts(s, crit) {
  const parts = [];
  let dieSize = s.die;
  const fatal = s.traits.find(t => /^fatal-d\d+$/.test(t));
  if (crit && fatal) dieSize = fatal.split('-')[1];
  const mods = s.damage.mods.filter(m => m.applied !== false && m.enabled !== false && !m.situational).reduce((a, m) => a + m.value, 0);
  parts.push({f: `${s.dice}${dieSize}${mods ? (mods > 0 ? '+' : '') + mods : ''}`, t: s.dtype});
  for (const x of s.extraDice) {
    if (x.situational) continue;
    if (x.from === 'Deadly' || /^Fatal/.test(x.from)) { parts.push({f: `${x.n}${x.d}`, t: x.type, critOnly: true}); continue; }
    parts.push({f: `${x.n}${x.d}`, t: x.type, c: x.cat, critOnly: !!x.critical});
  }
  return parts;
}
function tray() {
  const log = (ch.log || []).slice().reverse();
  const last = log[0];
  const dcv = ch.target.dc == null ? '' : ch.target.dc;
  const mode = ch.rollMode || 'normal';
  return `<aside class="cs-tray${trayOpen ? ' open' : ''}" aria-label="Dice">
<button type="button" class="cs-trayhead" data-act="tray">${ic('dice')}<span>${last ? esc(lastLine(last)) : 'Dice'}</span><small>${trayOpen ? 'Hide' : 'Show'}</small></button>
<div class="cs-traybody">${last ? logCard(last, true) : '<p class="muted small">Select any bonus on the sheet to roll it.</p>'}
<div class="cs-trayctl"><label class="cs-field"><span>Target AC or DC</span><input type="number" inputmode="numeric" value="${dcv}" data-field="target-dc" placeholder="None"></label>
<label class="cs-field"><span>Next roll</span><select data-act="rollmode"><option value="normal"${mode === 'normal' ? ' selected' : ''}>Normal</option><option value="twice-high"${mode === 'twice-high' ? ' selected' : ''}>Roll twice, keep higher</option><option value="twice-low"${mode === 'twice-low' ? ' selected' : ''}>Roll twice, keep lower</option></select></label></div>
<div class="cs-quick">${[4, 6, 8, 10, 12, 20, 100].map(n => `<button type="button" class="chip mini" data-act="qroll" data-f="1d${n}">d${n}</button>`).join('')}<button type="button" class="chip mini" data-act="flat">Flat check</button></div>
<div class="cs-inline"><input type="text" id="cs-formula" placeholder="Any formula, such as 2d6+4" aria-label="Dice formula"><button type="button" class="chip" data-act="froll">Roll</button></div>
<ol class="cs-log">${log.slice(1, 14).map(x => `<li>${logCard(x)}</li>`).join('')}</ol>${log.length ? '<button type="button" class="chip mini" data-act="log-clear">Clear the log</button>' : ''}</div></aside>`;
}
function lastLine(x) {
  if (x.kind === 'check') return `${x.label}: ${x.total}${x.dg != null ? ', ' + DEGREES[x.dg].toLowerCase() : ''}`;
  return `${x.label}: ${x.total}`;
}
function logCard(x, big) {
  const time = new Date(x.t).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'});
  if (x.kind === 'check') {
    const dice = x.d20.map(v => `<span class="cs-die${v === 20 ? ' n20' : v === 1 ? ' n1' : ''}${x.d20.length > 1 && v !== x.nat ? ' off' : ''}">${v}</span>`).join('');
    return `<div class="cs-roll${big ? ' big' : ''}"><div class="h"><b>${esc(x.label)}</b><small>${time}</small></div>
<div class="r">${dice}<span class="op">${fmt(x.mod)}</span><span class="eq">=</span><b class="tot">${x.total}</b>${x.dg != null ? `<span class="dg d${x.dg}">${DEGREES[x.dg]}</span>` : ''}</div>
${x.dc != null || x.sub || x.reroll ? `<small class="muted">${[x.dc != null ? 'Against ' + x.dc : '', x.sub, x.reroll ? 'rerolled with a Hero Point' : ''].filter(Boolean).map(esc).join(' · ')}</small>` : ''}${big ? actionsFor(x) : ''}</div>`;
  }
  if (x.kind === 'note') return `<div class="cs-roll${big ? ' big' : ''}"><div class="h"><b>${esc(x.label)}</b><small>${time}</small></div><div class="r"><b>${esc(x.total)}</b></div></div>`;
  const rows = (x.parts || []).map(p => `<div class="dp"><span class="dd">${p.rolls.map(r => r.rolls.map(v => `<span class="cs-die s">${v}</span>`).join('')).join('')}</span><span>${esc(p.f)}${p.mult > 1 ? ' ×2' : ''}</span><b>${p.v}</b><small>${esc([p.c, p.t].filter(Boolean).join(' '))}${p.from ? ` <i>${esc(p.from)}</i>` : ''}</small></div>`).join('');
  const basic = x.basic ? `<small class="muted">Basic save: critical success 0, success ${Math.floor(x.total / 2)}, failure ${x.total}, critical failure ${x.total * 2}</small>` : '';
  const heal = big && (x.parts || []).some(p => p.heal) ? `<div class="cs-rbtn"><button type="button" class="chip mini" data-act="apply-heal" data-n="${x.total}">Heal myself ${x.total}</button></div>` : '';
  return `<div class="cs-roll${big ? ' big' : ''}"><div class="h"><b>${esc(x.label)}</b><small>${time}</small></div>${rows}<div class="r"><span class="eq">Total</span><b class="tot">${x.total}</b></div>${basic}${heal}</div>`;
}
function actionsFor(x) {
  const b = [];
  const ss = x.ctx && x.ctx.ss;
  if (ss && res.strikes[x.ctx.strike]) {
    const sp = rec(ss.k);
    if (ss.atk) {
      b.push(`<button type="button" class="chip mini${x.dg === 2 ? ' hi' : ''}" data-act="ss-dmg" data-id="${x.id}">Damage: Strike and ${esc(sp.n)}</button>`);
      b.push(`<button type="button" class="chip mini${x.dg === 3 ? ' hi' : ''}" data-act="ss-dmg" data-id="${x.id}" data-crit="1">Critical damage: Strike and ${esc(sp.n)}</button>`);
      b.push(`<span class="small">${esc(sp.n)} uses the Strike's result${x.dg != null && x.dg < 2 ? ', so it misses as well' : ''}.</span>`);
    } else {
      b.push(`<button type="button" class="chip mini${x.dg === 2 ? ' hi' : ''}" data-act="strike-dmg" data-i="${x.ctx.strike}">Strike damage</button>`);
      b.push(`<button type="button" class="chip mini${x.dg === 3 ? ' hi' : ''}" data-act="strike-crit" data-i="${x.ctx.strike}">Critical Strike damage</button>`);
      if (eng.spellDamage(sp, ss.rank).length && x.dg !== 0) b.push(`<button type="button" class="chip mini" data-act="spell-dmg" data-k="${esc(sp.k)}" data-r="${ss.rank}"${ss.save && ss.save.basic ? ' data-basic="1"' : ''}>${esc(sp.n)} damage</button>`);
      b.push(`<span class="small">${x.dg === 0 ? `The Strike critically failed, so ${esc(sp.n)} has no effect.` : `The target attempts a ${ss.save.basic ? 'basic ' : ''}${esc(cap(ss.save.stat))} save against DC ${ss.save.dc}.`}</span>`);
    }
    if (!x.reroll && (ch.heroPoints || 0) > 0) b.push(`<button type="button" class="chip mini" data-act="hero-reroll" data-id="${x.id}">Reroll with a Hero Point</button>`);
    return `<div class="cs-rbtn">${b.join('')}</div>`;
  }
  if (x.ctx && x.ctx.strike != null && res.strikes[x.ctx.strike]) {
    b.push(`<button type="button" class="chip mini${x.dg === 2 ? ' hi' : ''}" data-act="strike-dmg" data-i="${x.ctx.strike}">Damage</button>`);
    b.push(`<button type="button" class="chip mini${x.dg === 3 ? ' hi' : ''}" data-act="strike-crit" data-i="${x.ctx.strike}">Critical damage</button>`);
  }
  if (x.ctx && x.ctx.spell) {
    b.push(`<button type="button" class="chip mini${x.dg === 2 ? ' hi' : ''}" data-act="spell-dmg" data-k="${esc(x.ctx.spell)}" data-r="${x.ctx.rank}">Damage</button>`);
    b.push(`<button type="button" class="chip mini${x.dg === 3 ? ' hi' : ''}" data-act="spell-dmg" data-k="${esc(x.ctx.spell)}" data-r="${x.ctx.rank}" data-crit="1">Critical damage</button>`);
  }
  if (!x.reroll && (ch.heroPoints || 0) > 0 && x.ctx && x.ctx.mod != null) b.push(`<button type="button" class="chip mini" data-act="hero-reroll" data-id="${x.id}">Reroll with a Hero Point</button>`);
  if (x.ctx && x.ctx.recovery) b.push(`<span class="small">${esc(x.ctx.recovery)}</span>`);
  return b.length ? `<div class="cs-rbtn">${b.join('')}</div>` : '';
}
function situationalText(st) { return st.situational.length ? 'not included: ' + st.situational.map(m => `${m.label} ${fmt(m.value)}`).join(', ') : ''; }
function rollKey(k) {
  let st = null, label = '';
  const opts = {};
  if (k.startsWith('save:')) { st = res.saves[k.slice(5)]; label = st.label + ' save'; if ((st.degree || []).length) opts.successUp = true; }
  else if (k === 'perception') { st = res.perception; label = 'Perception'; }
  else if (k === 'initiative') { st = res.initiative; label = 'Initiative'; opts.dc = null; }
  else if (k.startsWith('skill:')) { st = res.skills[k.slice(6)]; label = st.label; }
  else if (k.startsWith('spellatk:')) { const sc = res.spellcasting.find(s => s.e.id === k.split(':')[1]); st = sc.attack; label = sc.e.name + ': spell attack'; }
  if (!st) return;
  const last = k.split(':').pop();
  const fortune = res.rollTwice.some(r => [].concat(r.sel).some(s => s === last || s === 'all' || (k.startsWith('save:') && s === 'saving-throw') || (k.startsWith('skill:') && s === 'skill-check')));
  if (fortune && (ch.rollMode || 'normal') === 'normal') opts.mode = 'twice-high';
  check(label, st.total, Object.assign(opts, {sub: situationalText(st), ctx: {mod: st.total, key: k}}));
}
function rollStrike(i, mapIdx) {
  const s = res.strikes[i]; if (!s) return;
  const e = ch.enc;
  if (mapIdx == null || Number.isNaN(mapIdx)) mapIdx = e.on ? Math.min(e.attacks, 2) : 0;
  const mod = s.map[mapIdx];
  check(`${s.name}, ${['first', 'second', 'third'][mapIdx]} attack`, mod, {sub: situationalText(s.attack), ctx: {strike: i, mod}});
  if (e.on) { e.attacks += 1; e.actions = Math.max(0, e.actions - 1); }
}

// ───────── Spellstrike ─────────
// a spell of 1 or 2 actions with a spell attack roll or a saving throw (Impossible Magic)
const ssTime = t => /^[12]$/.test(t || '') || /^[12] (to|or) [123]$/.test(t || '') || /^single action to/.test(t || '');
const ssEligible = s => ssTime(s.time) && ((s.tr || []).includes('attack') || !!(s.dfn && s.dfn.save));
function ssOptions() {
  const out = [], seen = new Set();
  const add = (s, rank, sc, src, how) => {
    if (!s || !ssEligible(s)) return;
    const key = [s.k, rank, sc.e.id, how.type].join('|');
    if (seen.has(key)) return; seen.add(key);
    out.push({s, rank, sc, src, how});
  };
  for (const sc of res.spellcasting) {
    const e = sc.e, known = (e.known || []).map(k => rec(k)).filter(Boolean);
    const isC = s => (s.tr || []).includes('cantrip');
    if (e.kind === 'staff') {
      const left = sc.charges.max - sc.charges.used;
      for (const x of e.staff || []) {
        if (x.lv > ch.level) continue;
        const s = rec(x.k); if (!s) continue;
        if (isC(s)) add(s, sc.cantripRank, sc, `${e.name}, cantrip`, {type: 'cantrip'});
        else if (x.rank <= left) add(s, x.rank, sc, `${e.name}, ${x.rank} charge${x.rank > 1 ? 's' : ''} of ${left}`, {type: 'staff', e: e.id, cost: x.rank});
      }
    } else if (sc.slots) {
      for (const s of known.filter(isC)) add(s, sc.cantripRank, sc, `${e.name}, cantrip`, {type: 'cantrip'});
      for (let rk = sc.slots.length - 1; rk >= 1; rk--) {
        const n = sc.slots[rk]; if (!n) continue;
        if (e.kind === 'prepared') {
          const prep = (e.prepared || {})[rk] || [], used = (e.used || {})[rk] || [];
          for (let i = 0; i < n; i++) if (prep[i] && !used.includes(i)) add(rec(prep[i]), rk, sc, `${e.name}, prepared in a rank ${rk} slot`, {type: 'prep', e: e.id, r: rk, i});
        } else {
          const left = n - ((e.usedN || {})[rk] || 0);
          if (left > 0) for (const s of known) if (!isC(s) && (s.lv || 1) <= rk) add(s, rk, sc, `${e.name}, rank ${rk} slot, ${left} left`, {type: 'spont', e: e.id, r: rk});
        }
      }
    } else if (e.kind === 'focus') {
      const left = res.focusMax - (ch.focusUsed || 0);
      for (const s of known) {
        if (isC(s)) add(s, sc.cantripRank, sc, `${e.name}, focus cantrip`, {type: 'cantrip'});
        else if (left > 0) add(s, sc.cantripRank, sc, `${e.name}, 1 Focus Point`, {type: 'focus'});
      }
    } else for (const s of known) add(s, s.lv || 1, sc, `${e.name}, innate`, {type: 'innate', e: e.id});
  }
  return out.sort((a, b) => b.rank - a.rank || a.s.n.localeCompare(b.s.n));
}
function ssDefence(o) {
  const sv = o.s.dfn && o.s.dfn.save;
  if ((o.s.tr || []).includes('attack')) return "Uses the Strike's attack roll";
  return `${sv.basic ? 'Basic ' : ''}${cap(sv.statistic)} save, DC ${o.sc.dc.total}`;
}
function ssPick(i) {
  const st0 = res.strikes[i]; if (!st0) return;
  const opts = ssOptions();
  const box = document.createElement('div');
  box.className = 'cs-picker cs-ss';
  const mapIdx = ch.enc.on ? Math.min(ch.enc.attacks, 2) : 0;
  const items = opts.map((o, j) => ({label: o.s.n, rec: o.s, o, j, gr: gradeOf('sp', o.s), hayx: [o.src, spellArea(o.s), spellDef(o.s), ...spellDmg(o.s)].join(' ')}));
  const avg = o => eng.spellDamage(o.s, o.rank).reduce((t, x) => t + String(x.f || '').split('+').reduce((u, p) => { const m = p.trim().match(/^(\d+)d(\d+)$/); return u + (m ? m[1] * (+m[2] + 1) / 2 : Number(p) || 0); }, 0), 0);
  const sf = spellFacets(items);
  const spec = [
    {k: 'how', label: 'Paid with', type: 'chips', opts: [['cantrip', 'Cantrip'], ['prep', 'Prepared slot'], ['spont', 'Spell slot'], ['staff', 'Stave charges'], ['focus', 'Focus Point'], ['innate', 'Innate']].filter(([v]) => items.some(it => it.o.how.type === v)), val: it => it.o.how.type},
    sf.def, sf.area, sf.dmg, sf.role, fxGrade()].map(f => Object.assign({}, f, {opts: f.opts.filter(([v]) => items.some(it => [].concat(f.val(it)).map(String).includes(v)))})).filter(f => f.opts.length > 1);
  const sorts = [['rank-', 'Rank, highest first', (a, b) => b.o.rank - a.o.rank], ['dmg', 'Average damage, highest first', (a, b) => avg(b.o) - avg(a.o)], SO_NAME, SO_GR, ...roleSorts()];
  const defs = fxDefaults(spec, sorts, {open: false});
  const st = FX.ss || (FX.ss = fxClone(defs));
  box.innerHTML = `<p class="small">Two actions. Cast a spell and make a melee Strike with ${esc(st0.name)} at ${fmt(st0.map[mapIdx])}. The Strike gains the arcane trait and counts as two attacks for your multiple attack penalty, applied after the Strike.</p>
${opts.length ? `<label class="search"><input type="search" placeholder="Search spells, damage types and areas" aria-label="Search spells" value="${esc(st.q || '')}"></label>${fxHTML(spec, st, sorts)}<p class="small muted cs-pc"></p>` : ''}<ul class="cs-sslist"></ul>`;
  const list = box.querySelector('.cs-sslist'), q = box.querySelector('input[type=search]'), count = box.querySelector('.cs-pc');
  const draw = () => {
    if (!opts.length) { list.innerHTML = '<li class="muted">No spell you can cast right now qualifies. Spellstrike needs a spell of 1 or 2 actions with a spell attack roll or a saving throw, and a slot, charge or Focus Point to cast it.</li>'; return; }
    st.q = q.value;
    const m = fxApply(items, spec, st, sorts);
    count.textContent = `${m.length} of ${items.length} spells`;
    list.innerHTML = m.map(it => {
      const o = it.o, dmg = eng.spellDamage(o.s, o.rank);
      return `<li><div class="t">${g(o.s)}${legTag(o.s)}${grBadge(it.gr)}<span class="cs-badge">${(o.s.tr || []).includes('cantrip') ? 'Cantrip, rank ' + o.rank : 'Rank ' + o.rank}</span></div>
<div class="m"><span>${esc(o.src)}</span><span>${esc(ssDefence(o))}</span>${o.s.area ? `<span>${esc(o.s.area.value + '-foot ' + o.s.area.type)}</span>` : ''}${dmg.length ? `<span>${esc(dmg.map(x => x.f + (x.t ? ' ' + x.t : '')).join(' + '))}</span>` : ''}</div>
<button type="button" class="chip hi" data-j="${it.j}">Spellstrike with ${esc(o.s.n)}</button></li>`;
    }).join('') || '<li class="muted">Nothing matches. Clear a filter or widen the search.</li>';
  };
  if (q) { let t; q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(draw, 120); }); fxBind(box, spec, st, defs, items, sorts, draw); }
  box.addEventListener('click', e => {
    const b = e.target.closest('button[data-j]'); if (!b) return;
    A.popPanel(); doSpellstrike(i, opts[+b.dataset.j]); commit();
  });
  draw();
  A.pushPanel('Spellstrike', 'Choose a spell', box, 'ss:' + i);
}
function spendCast(how) {
  const E2 = id => ch.spells.entries.find(x => x.id === id);
  if (how.type === 'prep') { const x = E2(how.e); x.used = x.used || {}; const arr = x.used[how.r] = x.used[how.r] || []; if (!arr.includes(how.i)) arr.push(how.i); }
  else if (how.type === 'spont') { const x = E2(how.e); x.usedN = x.usedN || {}; x.usedN[how.r] = (x.usedN[how.r] || 0) + 1; }
  else if (how.type === 'staff') { const x = E2(how.e); x.used = (x.used || 0) + how.cost; }
  else if (how.type === 'focus') ch.focusUsed = (ch.focusUsed || 0) + 1;
  else if (how.type === 'innate') { const x = E2(how.e); x.innateUsed = x.innateUsed || {}; }
}
function doSpellstrike(i, o) {
  const st = res.strikes[i]; if (!st || !o) return;
  const e = ch.enc;
  const mapIdx = e.on ? Math.min(e.attacks, 2) : 0;
  const mod = st.map[mapIdx];
  spendCast(o.how);
  if (o.how.type === 'innate') { const x = ch.spells.entries.find(y => y.id === o.how.e); x.innateUsed[o.s.k] = (x.innateUsed[o.s.k] || 0) + 1; }
  const sv = o.s.dfn && o.s.dfn.save;
  const ss = {k: o.s.k, rank: o.rank, atk: (o.s.tr || []).includes('attack'), save: sv ? {stat: sv.statistic, basic: !!sv.basic, dc: o.sc.dc.total} : null};
  check(`Spellstrike: ${st.name} with ${o.s.n}`, mod, {sub: [`${['first', 'second', 'third'][mapIdx]} attack`, situationalText(st.attack)].filter(Boolean).join('; '), ctx: {strike: i, mod, ss}});
  if (e.on) { e.actions = Math.max(0, e.actions - 2); e.attacks += 2; }
  ch.trackers.spellstrike = false;
}

// ───────── Sheet tab ─────────
const freqText = f => `${f.max} per ${({day: 'day', round: 'round', turn: 'turn', PT1H: 'hour', PT10M: '10 minutes', PT1M: 'minute', P1W: 'week'}[f.per] || f.per)}`;
const stripTags = t => String(t || '').replace(/<[^>]+>/g, '').replace(/@\w+\[[^\]]*\]\{([^}]*)\}/g, '$1').replace(/@\w+\[([^\]]*)\]/g, '$1');
function roundsTag(k) { const v = (ch.effects || {})[k]; return v && typeof v === 'object' && v.rounds != null ? ` <small class="cs-left">${v.rounds} round${v.rounds === 1 ? '' : 's'} left</small>` : ''; }
function effectRounds(r) {
  const u = r && r.dur;
  if (!u || u.value == null || u.value < 0) return null;
  return {rounds: u.value, minutes: u.value * 10, hours: u.value * 600}[u.unit] ?? null;
}
function tabSheet() {
  const c = ch.conditions || {};
  const active = Object.entries(c).filter(([k, v]) => v && !['dying', 'wounded', 'doomed'].includes(k));
  const cond = active.map(([k, v]) => {
    const r = rec('co:' + k);
    const valued = r && r.val;
    return `<span class="cs-cond">${g(r, cap(k.replace(/-/g, ' ')))}${valued ? ` <span class="cs-step"><button type="button" data-act="cond" data-k="${k}" data-d="-1" aria-label="Lower">−</button><b>${v}</b><button type="button" data-act="cond" data-k="${k}" data-d="1" aria-label="Raise">+</button></span>` : ''}<button type="button" class="x" data-act="cond-off" data-k="${k}" aria-label="Remove ${k}">×</button></span>`;
  }).join('') + (res.S.autoEncumbered ? '<span class="cs-cond">Encumbered <small>from Bulk</small></span>' : '');
  const condSel = `<select data-act="cond-add" aria-label="Add a condition"><option value="">Add a condition…</option>${CONDITIONS.filter(k => !c[k]).map(k => `<option value="${k}">${cap(k.replace(/-/g, ' '))}</option>`).join('')}</select>`;
  const seen = new Set(), tg = [], targetTg = [];
  for (const t of res.toggles) {
    if (t.key) {
      if (seen.has(t.key)) continue; seen.add(t.key);
      const r = rec(t.key); if (!r) continue;
      const on = !!(ch.effects || {})[t.key];
      tg.push(`<label class="cs-tog${on ? ' on' : ''}"><input type="checkbox" data-act="effect" data-k="${esc(t.key)}"${on ? ' checked' : ''}> ${esc(r.n.replace(/^(Effect|Stance|Spell Effect): /, ''))} <small>${esc(t.from.r.n)}</small>${roundsTag(t.key)}</label>`);
    } else if (t.option) {
      if (seen.has(t.option)) continue; seen.add(t.option);
      const on = !!(ch.toggles || {})[t.option];
      const label = t.option === 'target:condition:off-guard' ? 'Target is off-guard' : eng.t(t.label);
      const html = `<label class="cs-tog${on ? ' on' : ''}"><input type="checkbox" data-act="toggle" data-k="${esc(t.option)}"${on ? ' checked' : ''}> ${esc(label)} <small>${esc(t.from.r.n)}</small></label>`;
      (t.option.startsWith('target:') ? targetTg : tg).push(html);
    }
  }
  if (!seen.has('target:condition:off-guard')) {
    const on = !!(ch.toggles || {})['target:condition:off-guard'];
    targetTg.unshift(`<label class="cs-tog${on ? ' on' : ''}"><input type="checkbox" data-act="toggle" data-k="target:condition:off-guard"${on ? ' checked' : ''}> Target is off-guard</label>`);
  }
  const other = Object.entries(ch.effects || {}).filter(([k, v]) => v && !seen.has(k)).map(([k]) => { const r = rec(k); return r ? `<span class="cs-cond">${g(r, r.n.replace(/^(Effect|Spell Effect|Stance): /, ''))}${roundsTag(k)}<button type="button" class="x" data-act="effect-off" data-k="${esc(k)}" aria-label="Remove">×</button></span>` : ''; }).join('');
  const effChoices = res.pending.filter(p => p.uid.startsWith('effect:')).map(p => choiceUI(p)).join('');
  const trackers = [];
  const ssOn = res.S.opts.has('feature:spellstrike'), charged = ch.trackers.spellstrike !== false;
  if (ssOn) {
    trackers.push(`<div class="cs-track${charged ? ' on' : ''}">${ic('spellstrike')}<span><b>Spellstrike ${charged ? 'charged' : 'expended'}</b><small>${charged
      ? 'Use the Spellstrike button on a melee Strike below. It expends the charge.'
      : 'Recharge Spellstrike takes 1 action. Casting a conflux spell of at least 1 action also recharges it.'}</small></span>
<span class="b">${charged ? '<button type="button" class="chip mini" data-act="spellstrike">Mark expended</button>' : '<button type="button" class="chip mini hi" data-act="ss-recharge">Recharge Spellstrike</button><button type="button" class="chip mini" data-act="spellstrike">Mark charged</button>'}</span></div>`);
  }
  let shield = '';
  if (res.S.shield) {
    const sh = res.S.shield, r = sh.r, inv = sh.inv;
    const max = r.hp || 0, dmg = inv.sdmg || 0, cur = Math.max(0, max - dmg), bt = Math.floor(max / 2);
    const raised = !!(ch.toggles || {})['shield-raised'];
    shield = `<div class="cs-shield"><div class="h"><b>${g(r, inv.name || r.n)}</b><small>Hardness ${r.hard}, Broken Threshold ${bt}</small></div>
<div class="cs-hpbar s"><span style="width:${max ? Math.round(100 * cur / max) : 0}%"></span></div><small>${cur} of ${max} HP${cur <= bt ? ' · broken' : ''}</small>
<div class="cs-inline"><label class="cs-tog${raised ? ' on' : ''}"><input type="checkbox" data-act="toggle" data-k="shield-raised"${raised ? ' checked' : ''}> Raised (+${r.ac} AC)</label>
<input type="number" inputmode="numeric" id="cs-block" placeholder="Damage" aria-label="Damage to block"><button type="button" class="chip" data-act="block">Shield Block</button><button type="button" class="chip mini" data-act="shield-repair">Repair</button></div></div>`;
  }
  const next = ch.enc.on ? Math.min(ch.enc.attacks, 2) : -1;
  const ssRanged = [...res.S.opts].some(o => /starlit-span/.test(o));
  const strikes = res.strikes.map((s, i) => {
    const ex = s.extraDice.map(dd => `<span class="${dd.situational ? 'sit' : ''}">${dd.critical ? 'critical: ' : ''}+${dd.n}${dd.d} ${esc(dd.type || '')}${dd.cat === 'persistent' ? ' persistent' : ''} <small>(${esc(dd.from)})</small></span>`).join('');
    const notes = s.notes.map(n => `<li><b>${esc(n.title)}</b>${n.outcome ? ` <small>(${esc([].concat(n.outcome).map(o => o.replace(/([A-Z])/g, ' $1').toLowerCase()).join(', '))})</small>` : ''}: ${esc(stripTags(n.text))}</li>`).join('');
    const sit = s.attack.situational.concat(s.damage.situational).map(m => `${esc(m.label)} ${fmt(m.value)}`).join('; ');
    return `<div class="cs-strike${s.held ? '' : ' idle'}"><div class="h"><b>${s.inv ? `<button type="button" class="cs-lnk" data-act="item" data-id="${esc(s.inv.id)}">${esc(s.name)}</button>` : g(s.r, s.name)}</b>${s.held ? '' : ' <small>not held</small>'}<span class="cs-trs">${s.traits.map(t => `<span class="trait">${esc(t.replace(/-/g, ' '))}</span>`).join('')}</span>
<button type="button" class="cs-info" data-act="breakdown" data-k="strike:${i}">Attack breakdown</button></div>
<div class="cs-atk">${s.map.map((m, j) => `<button type="button" class="cs-sv bare${j === next ? ' next' : ''}" data-act="strike" data-i="${i}" data-m="${j}" aria-label="Roll ${esc(s.name)} ${['first', 'second', 'third'][j]} attack"><b>${fmt(m)}</b><small>${['First', 'Second', 'Third'][j]}</small></button>`).join('')}
<button type="button" class="cs-sv bare dmg" data-act="strike-dmg" data-i="${i}" aria-label="Roll damage"><b>${esc(s.formula)}</b><small>Damage${s.range ? ` · range ${s.range} ft` : ''}</small></button>
<button type="button" class="chip mini" data-act="strike-crit" data-i="${i}">Critical</button>
${ssOn && (!s.range || ssRanged) ? (charged ? `<button type="button" class="chip mini ss" data-act="ss-pick" data-i="${i}">${ic('spellstrike')}Spellstrike</button>` : `<button type="button" class="chip mini" data-act="ss-recharge">Recharge Spellstrike</button>`) : ''}</div>
${ex ? `<div class="cs-ex">${ex}</div>` : ''}${sit ? `<p class="small muted">Situational: ${sit}</p>` : ''}${notes ? `<ul class="cs-notes">${notes}</ul>` : ''}</div>`;
  }).join('');
  const skills = Object.entries(res.skills).sort((a, b) => (a[1].lore - b[1].lore) || a[1].label.localeCompare(b[1].label)).map(([k, v]) =>
    `<div class="cs-skill"><button type="button" class="cs-sk" data-act="breakdown" data-k="skill:${esc(k)}" title="How ${esc(v.label)} is made up">${rankTag(v.rank)}<span>${esc(v.label)}</span><small>${v.attr.toUpperCase()}</small></button><button type="button" class="cs-skv" data-act="roll" data-k="skill:${esc(k)}" aria-label="Roll ${esc(v.label)}">${ic('dice')}<b>${fmt(v.total)}</b></button></div>`).join('');
  const acts = [];
  const seenA = new Set();
  for (const it of res.actions) {
    const r = it.r; if (seenA.has(r.n) || !r.act || r.act === 'passive') continue; seenA.add(r.n);
    let uses = '';
    if (r.freq && r.freq.max) {
      const used = (ch.uses || {})[r.k] || 0;
      uses = ` <span class="cs-uses" title="${esc(freqText(r.freq))}">${Array.from({length: r.freq.max}, (_, i) => `<button type="button" class="${i < used ? 'used' : ''}" data-act="use" data-k="${esc(r.k)}" data-n="${i + 1}" aria-label="Use ${i + 1}"></button>`).join('')}<small>${esc(freqText(r.freq))}</small></span>`;
    }
    acts.push(`<li>${act(r.act)} ${g(r)}${uses}</li>`);
  }
  const def = [];
  if (res.resist.length) def.push(`<p><b>Resistances</b> ${res.resist.map(r => esc(`${r.type} ${r.value ?? ''}`)).join(', ')}</p>`);
  if (res.weak.length) def.push(`<p><b>Weaknesses</b> ${res.weak.map(r => esc(`${r.type} ${r.value ?? ''}`)).join(', ')}</p>`);
  if (res.immune.length) def.push(`<p><b>Immunities</b> ${res.immune.map(r => esc(r.type)).join(', ')}</p>`);
  const senses = res.senses.map(s => esc(cap(String(s.type || '').replace(/-/g, ' ')) + (s.range ? ` ${s.range} ft` : ''))).join(', ');
  const consum = ch.inventory.filter(i => { const r = eng.invRec(i); return r && r.t === 'consumable' && (i.qty ?? 1) > 0; });
  const quick = consum.length ? `<section class="cs-sec"><h2>Consumables</h2><div class="cs-conds">${consum.map(i => { const r = eng.invRec(i); return `<span class="cs-cond">${g(r)} <small>×${i.qty ?? 1}</small><button type="button" class="chip mini" data-act="consume" data-id="${esc(i.id)}">Use</button></span>`; }).join('')}</div></section>` : '';
  return todoSection() + `<section class="cs-sec"><h2>Conditions and effects</h2><div class="cs-conds">${cond || '<span class="muted small">No conditions.</span>'} ${condSel}</div>
${tg.length ? `<div class="cs-togs">${tg.join('')}</div>` : ''}${effChoices ? `<div class="cs-choices">${effChoices}</div>` : ''}
<div class="cs-conds">${other}<button type="button" class="chip" data-act="effect-pick">Add an effect from a spell or item</button></div></section>
<section class="cs-sec cs-2"><div><h2>Target</h2><div class="cs-togs">${targetTg.join('')}</div>
<div class="cs-inline"><label class="cs-field inl"><span>AC or DC</span><input type="number" inputmode="numeric" value="${ch.target.dc ?? ''}" data-field="target-dc" placeholder="None"></label></div>
<p class="small muted">With a target AC or DC set, every roll shows its degree of success, including natural 20s and 1s.</p></div>
<div>${trackers.length || shield ? '<h2>Trackers</h2>' : ''}${trackers.join('')}${shield}</div></section>
<section class="cs-sec"><h2>Strikes</h2><div class="cs-strikes">${strikes || '<p class="muted">Add a weapon on the Inventory tab.</p>'}</div></section>
${quick}
<section class="cs-sec"><h2>Skills</h2><div class="cs-skills">${skills}</div></section>
<section class="cs-sec cs-2"><div><h2>Actions</h2><ul class="cs-acts">${acts.join('') || '<li class="muted">None yet.</li>'}</ul></div>
<div><h2>Senses, languages and defences</h2><p><b>Size</b> ${esc({tiny: 'Tiny', sm: 'Small', med: 'Medium', lg: 'Large', huge: 'Huge', grg: 'Gargantuan'}[res.size] || res.size)}</p>
${senses ? `<p><b>Senses</b> ${senses}</p>` : ''}<p><b>Languages</b> ${esc(res.languages.list.map(l => cap(l)).join(', ') || 'None')}</p>${def.join('')}
<p><b>Bulk</b> ${res.bulk.value}${res.bulk.light ? ', ' + res.bulk.light + ' L' : ''} of ${res.bulk.encumbered} before encumbered, ${res.bulk.max} maximum</p></div></section>`;
}

// ───────── Build tab ─────────
function origin(kind, label, r, extra) {
  return `<div class="cs-orig"><span class="l">${label}</span><span class="v">${r ? g(r) + (r.fr ? ' <span class="cs-badge">Forgotten Realms</span>' : '') : '<span class="muted">Not chosen</span>'}</span><button type="button" class="chip" data-act="pick-origin" data-k="${kind}">${r ? 'Change' : 'Choose'}</button>${extra || ''}</div>`;
}
const labelFor = (opts, v) => (opts.find(o => String(o.value) === String(v)) || {label: String(v)}).label;
function choiceUI(p, S = res.S) {
  const opts = eng.choices(S, p);
  const cur = p.value;
  const curR = typeof cur === 'string' ? rec(cur) : null;
  const label = curR ? g(curR) : cur != null ? esc(labelFor(opts, cur)) : '<span class="muted">Not chosen</span>';
  const who = p.item.r.n;
  if (opts.length && opts.length <= 16 && !opts.some(o => o.rec)) {
    return `<div class="cs-choice"><span class="l">${esc(who)}: ${esc(p.prompt)}</span><select data-act="choice" data-uid="${esc(p.uid)}" data-flag="${esc(p.flag)}"><option value="">Choose…</option>${opts.map(o => `<option value="${esc(o.value)}"${String(o.value) === String(cur) ? ' selected' : ''}>${esc(o.label)}</option>`).join('')}</select></div>`;
  }
  return `<div class="cs-choice"><span class="l">${esc(who)}: ${esc(p.prompt)}</span><span class="v">${label}</span><button type="button" class="chip" data-act="choice-pick" data-uid="${esc(p.uid)}" data-flag="${esc(p.flag)}">${cur != null ? 'Change' : 'Choose'}</button></div>`;
}
function boostRow(label, key, options, chosen, n, fixed) {
  const cells = ATTRS.map(a => {
    const on = chosen.includes(a), allowed = options.includes(a);
    const fx = (fixed || []).includes(a);
    return `<td>${fx ? '<span class="cs-fixed" title="Fixed boost">+</span>' : allowed ? `<button type="button" class="cs-bst${on ? ' on' : ''}" data-act="boost" data-k="${key}" data-a="${a}" aria-pressed="${on}" aria-label="${label}: ${ATTR_NAME[a]}">${on ? '+' : ''}</button>` : ''}</td>`;
  }).join('');
  return `<tr><th>${label}<small>${chosen.length} of ${n}</small></th>${cells}</tr>`;
}
function intAtOne() { const c = JSON.parse(JSON.stringify(ch)); c.level = 1; c.inventory = []; return eng.compute(c).attributes.int; }
function tabBuild() {
  const S = res.S, b = ch.boosts, anc = S.anc, bg = S.bg, cls = S.cls;
  const L = ch.level;
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
  const tc = res.trainCount, trained = ch.trained || [];
  const fromBuild = new Set([...(cls ? cls.skills.value || [] : []), ...(bg ? bg.skills.value || [] : [])]);
  const skillChips = Object.keys(SKILLS).map(s => {
    const fixed = fromBuild.has(s), on = trained.includes(s);
    return `<button type="button" class="chip mini${on || fixed ? ' on' : ''}" ${fixed ? 'disabled title="Trained by class or background"' : `data-act="train" data-k="${s}" aria-pressed="${on}"`}>${cap(s)}</button>`;
  }).join('');
  const lores = (ch.lores || []).map((l, i) => `<span class="cs-cond">${esc(l)}<button type="button" class="x" data-act="lore-del" data-i="${i}" aria-label="Remove">×</button></span>`).join('');
  const bgLore = bg ? (bg.skills.lore || []).join(', ') : '';
  const skillOpts = sel => Object.keys(res.skills).map(s => `<option value="${esc(s)}"${s === sel ? ' selected' : ''}>${esc(res.skills[s].label)}</option>`).join('');
  const slots = res.slots;
  const feats = ch.feats || {};
  const featuresAt = lv => cls ? cls.items.filter(x => x[0] === lv).map(x => rec(x[1])).filter(Boolean) : [];
  const pendingFor = (u, lv = 1) => (lv > L ? planRes() : res).pending.filter(p => p.uid === u || p.uid.startsWith(u + '>'));
  const choiceAt = (p, lv) => choiceUI(p, lv > L ? planRes().S : res.S);
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
      for (const r of fts) for (const p of pendingFor('class>' + r.k, lv)) parts.push(choiceAt(p, lv));
    }
    for (const s of here) {
      if (s.kind === 'boost') continue;
      if (s.kind === 'increase') {
        const wi = (res.wastedInc || []).find(w => w.id === (s.bonus ? s.id : 'inc-' + lv));
        const sel = s.bonus ? `<select data-act="inc-b" data-s="${esc(s.id)}" aria-label="${esc(s.label)} at level ${lv}"><option value="">Choose…</option>${skillOpts((ch.bonusInc || {})[s.id])}</select>`
          : `<select data-act="inc" data-lv="${lv}" aria-label="Skill increase at level ${lv}"><option value="">Choose…</option>${skillOpts((ch.increases || {})[lv])}</select>`;
        parts.push(`<div class="cs-feat"><span class="l">${esc(s.bonus ? s.label : 'Skill increase')}</span>${sel}${wi ? `<p class="small cs-warn">${esc(wastedText(wi))}</p>` : ''}</div>`);
        continue;
      }
      const f = feats[s.id], r = f ? rec(f.k) : null;
      let warn = '';
      if (r) { const pr = eng.prereqs(res, r).filter(p => p.ok === false); if (pr.length) warn = `<small class="cs-warn">Prerequisite not met: ${esc(pr.map(p => p.text).join('; '))}</small>`; }
      parts.push(`<div class="cs-feat"><span class="l">${esc(s.label)}</span><span class="v">${r ? g(r) + legTag(r) + ` <small>${r.lv || ''}</small>` : '<span class="muted">Empty</span>'}${warn}</span><button type="button" class="chip" data-act="pick-feat" data-s="${esc(s.id)}">${r ? 'Change' : 'Choose'}</button>${r ? `<button type="button" class="chip" data-act="clear-feat" data-s="${esc(s.id)}" aria-label="Remove">×</button>` : ''}</div>`);
      if (r && r.k === 'ft:additional-lore') parts.push(`<div class="cs-choice"><span class="l">Additional Lore: which Lore</span><input type="text" value="${esc(f.lore || '')}" placeholder="Academia" data-field="featlore" data-s="${esc(s.id)}" aria-label="Lore for Additional Lore"></div>`);
      for (const p of pendingFor('feat:' + s.id, lv)) parts.push(choiceAt(p, lv));
    }
    levels += `<section class="cs-lv${lv > L ? ' planned' : ''}"><h3>Level ${lv}${lv > L ? ' <small>planned</small>' : ''}</h3>${parts.join('')}</section>`;
  }
  const intExtra = Math.max(0, res.attributes.int - intAtOne());
  let intRows = '';
  for (let i = 0; i < intExtra; i++) { const key = 'x' + i; intRows += `<select data-act="int-train" data-k="${key}" aria-label="Extra trained skill ${i + 1}"><option value="">Choose…</option>${Object.keys(SKILLS).map(s => `<option value="${s}"${(ch.intTrained || {})[key] === s ? ' selected' : ''}>${cap(s)}</option>`).join('')}</select>`; }
  const langs = res.languages;
  return `<section class="cs-sec"><h2>Options</h2><div class="cs-togs"><label class="cs-tog"><input type="checkbox" data-act="opt" data-k="freeArchetype"${ch.options.freeArchetype ? ' checked' : ''}> Free archetype</label>
<button type="button" class="chip" data-act="bonus-slot">Add a bonus feat or skill increase</button></div>
${(ch.bonusSlots || []).length ? `<h3 class="cs-bh">Bonus feats and skill increases</h3><div class="cs-scroll"><table class="cs-bonus"><thead><tr><th>Level</th><th>Type</th><th>Label</th><th><span class="sr">Remove</span></th></tr></thead><tbody>${ch.bonusSlots.slice().sort((x, y) => x.lv - y.lv || String(x.label).localeCompare(String(y.label))).map(b2 => `<tr>
<td><input type="number" min="1" max="20" value="${b2.lv}" data-act="bonus-lv" data-id="${esc(b2.id)}" aria-label="Level for ${esc(b2.label)}"></td>
<td><select data-act="bonus-kind" data-id="${esc(b2.id)}" aria-label="Type for ${esc(b2.label)}">${BONUS_KINDS.map(([k, l]) => `<option value="${k}"${b2.kind === k ? ' selected' : ''}>${l}</option>`).join('')}</select></td>
<td><input type="text" value="${esc(b2.label)}" data-act="bonus-label" data-id="${esc(b2.id)}" aria-label="Label"></td>
<td><button type="button" class="chip mini" data-act="bonus-del" data-id="${esc(b2.id)}">Remove</button></td></tr>`).join('')}</tbody></table></div>` : ''}</section>
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

// ───────── Inventory tab ─────────
const coinTotal = c => (c.pp || 0) * 1000 + (c.gp || 0) * 100 + (c.sp || 0) * 10 + (c.cp || 0);
const money = cp => { const gp = Math.floor(cp / 100), sp = Math.floor(cp % 100 / 10), c = cp % 10; return [gp ? gp.toLocaleString() + ' gp' : '', sp ? sp + ' sp' : '', c ? c + ' cp' : ''].filter(Boolean).join(' ') || '0 gp'; };
const STATES = [['held1', 'Held in one hand'], ['held2', 'Held in two hands'], ['worn', 'Worn'], ['stowed', 'Stowed'], ['dropped', 'Dropped']];
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
function tabInventory() {
  const c = ch.coins;
  const coins = ['pp', 'gp', 'sp', 'cp'].map(k => `<label class="cs-coin"><span>${k}</span><input type="number" inputmode="numeric" min="0" value="${c[k] || 0}" data-field="coin" data-k="${k}"></label>`).join('');
  const ledger = (ch.ledger || []).slice(-12).reverse().map(l => `<li><span>${new Date(l.t).toLocaleDateString()}</span><b class="${l.d < 0 ? 'neg' : 'pos'}">${l.d < 0 ? '−' : '+'}${money(Math.abs(l.d))}</b><span>${esc(l.note || '')}</span></li>`).join('');
  const groups = {held: [], worn: [], stowed: [], dropped: []};
  for (const inv of ch.inventory) groups[(inv.eq || 'stowed').startsWith('held') ? 'held' : (inv.eq || 'stowed')].push(inv);
  const invested = ch.inventory.filter(i => i.inv).length;
  const row = inv => {
    const r = eng.invRec(inv); if (!r) return '';
    const name = inv.custom ? inv.custom.n : inv.name || r.n;
    const canInvest = eng.needsInvest(r, inv);
    const runes = (r.t === 'weapon' || r.t === 'armor' || r.t === 'shield') ? `<button type="button" class="chip mini" data-act="runes" data-id="${esc(inv.id)}">Runes${runeSummary(r, inv)}</button>` : '';
    const use = r.t === 'consumable' ? `<button type="button" class="chip mini" data-act="consume" data-id="${esc(inv.id)}">Use one</button>` : '';
    const meta = [typeLabel(r), `Level ${r.lv || 0}`, r.cp ? money(r.cp) : '', `Bulk ${bulkText(r.bulk)}`].filter(Boolean);
    return `<li class="cs-item"><div class="n"><button type="button" class="cs-iname" data-act="item" data-id="${esc(inv.id)}">${esc(name)}</button>${legTag(r)}${inv.custom && inv.custom.relic ? '<span class="cs-badge">Relic</span>' : ''}${inv.inv ? '<span class="cs-badge">Invested</span>' : ''}
<div class="meta">${meta.map(x => `<span>${esc(x)}</span>`).join('')}</div></div>
<div class="c"><span class="cs-qtyl">Quantity <span class="cs-step"><button type="button" data-act="qty" data-id="${esc(inv.id)}" data-d="-1" aria-label="Fewer">−</button><b>${inv.qty ?? 1}</b><button type="button" data-act="qty" data-id="${esc(inv.id)}" data-d="1" aria-label="More">+</button></span></span>
<select data-act="state" data-id="${esc(inv.id)}" aria-label="Where it is">${STATES.map(([k, l]) => `<option value="${k}"${(inv.eq || 'stowed') === k ? ' selected' : ''}>${l}</option>`).join('')}</select>
${canInvest ? `<label class="cs-tog"><input type="checkbox" data-act="invest" data-id="${esc(inv.id)}"${inv.inv ? ' checked' : ''}> Invested</label>` : ''}${runes}${use}
${canInvest && !inv.inv && r.t === 'armor' && inv.eq === 'worn' ? '<span class="small muted">Not invested: the armour still gives its AC, but resilient and property runes do nothing until it is.</span>' : ''}
${inv.custom ? '' : `<button type="button" class="chip mini" data-act="sell" data-id="${esc(inv.id)}">Sell for ${money(Math.floor((r.cp || 0) / 2))}</button>`}<button type="button" class="chip mini" data-act="remove" data-id="${esc(inv.id)}">Remove</button></div></li>`;
  };
  const sec = (k, t) => groups[k].length ? `<h3>${t}</h3><ul class="cs-items">${groups[k].map(row).join('')}</ul>` : '';
  const wealth = coinTotal(c) + ch.inventory.reduce((a, i) => { const r = eng.invRec(i); return a + (r ? (r.cp || 0) * (i.qty ?? 1) : 0); }, 0);
  return `<section class="cs-sec"><h2>Money</h2><div class="cs-coins">${coins}<span class="cs-worth">Coins ${money(coinTotal(c))} · wealth including items ${money(wealth)}</span></div>
<div class="cs-inline"><input type="number" inputmode="decimal" min="0" step="any" placeholder="Amount" id="cs-mamt" aria-label="Amount"><select id="cs-munit" aria-label="Unit"><option value="gp">gp</option><option value="sp">sp</option><option value="cp">cp</option><option value="pp">pp</option></select>
<input type="text" placeholder="What for" id="cs-mnote" aria-label="Note"><button type="button" class="chip" data-act="money" data-d="1">Receive</button><button type="button" class="chip" data-act="money" data-d="-1">Spend</button></div>
${ledger ? `<ul class="cs-ledger">${ledger}</ul>` : ''}</section>
<section class="cs-sec"><h2>Items</h2><div class="cs-togs"><button type="button" class="chip hi" data-act="item-pick">Add or buy items</button><button type="button" class="chip" data-act="custom-item">Add a custom item</button></div>
<p class="small muted">Select an item's name for its details and rules text. Bulk ${res.bulk.value}${res.bulk.light ? ' and ' + res.bulk.light + ' light' : ''}: encumbered above ${res.bulk.encumbered}, maximum ${res.bulk.max}. Invested ${invested} of 10.</p>
${sec('held', 'Held')}${sec('worn', 'Worn')}${sec('stowed', 'Stowed')}${sec('dropped', 'Dropped')}${ch.inventory.length ? '' : '<p class="muted">No items yet.</p>'}</section>`;
}

// ───────── Spells tab ─────────
function ensureEntries() {
  let changed = false;
  const cls = res.S.cls;
  if (cls && cls.sc && !(ch.spells.entries || []).some(e => e.id === 'class')) { const e = eng.defaultEntry(cls); if (e) { ch.spells.entries.unshift(e); changed = true; } }
  for (const c of eng.dedications(res)) if (!ch.spells.entries.some(e => e.id === 'arch:' + c) && !(ch.spells.dismissed || []).includes('arch:' + c)) { ch.spells.entries.push(eng.archetypeEntry(c)); changed = true; }
  if (changed) { putChar(ch); recompute(); }
}
function spellCard(s, opt) {
  const e = opt.entry, sc = res.spellcasting.find(x => x.e.id === e.id);
  const tr = s.tr || [];
  const rank = opt.rank;
  const heighten = rank && s.lv && rank > s.lv && !tr.includes('cantrip') ? `<span class="cs-badge">heightened to ${rank}</span>` : '';
  let def = '';
  const df = s.dfn || null;
  if (df && df.save) def = `<span class="cs-def">${df.save.basic ? 'Basic ' : ''}${cap(df.save.statistic)} DC ${sc.dc.total}</span>`;
  else if (tr.includes('attack')) def = `<span class="cs-def">Spell attack ${fmt(sc.attack.total)}</span>`;
  const drank = tr.includes('cantrip') ? sc.cantripRank : rank || s.lv || 1;
  const dmg = eng.spellDamage(s, drank);
  const btns = [];
  if (opt.castAct) btns.push(`<button type="button" class="chip mini cast" data-act="${opt.castAct}" data-e="${esc(e.id)}" data-k="${esc(s.k)}" data-r="${rank || 0}"${opt.extra || ''}${opt.disabled ? ' disabled' : ''}>${esc(opt.castLabel || 'Cast')}</button>`);
  if (tr.includes('attack')) btns.push(`<button type="button" class="chip mini" data-act="spell-atk" data-e="${esc(e.id)}" data-k="${esc(s.k)}" data-r="${drank}">Attack roll</button>`);
  if (dmg.length) btns.push(`<button type="button" class="chip mini" data-act="spell-dmg" data-k="${esc(s.k)}" data-r="${drank}"${df && df.save && df.save.basic ? ' data-basic="1"' : ''}>${dmg.some(x => x.heal === 1) ? 'Healing' : 'Damage'} ${esc(dmg.map(x => x.f).join(' + '))}</button>`);
  const time = s.time && /^[123]$/.test(s.time) ? s.time : s.time === 'reaction' ? 'reaction' : s.time === 'free' ? 'free' : null;
  return `<div class="cs-spell${opt.used ? ' used' : ''}"><div class="h">${act(time)}<b>${g(s)}</b>${legTag(s)}${heighten}</div>
<div class="m">${tr.filter(t => !['concentrate', 'manipulate', 'cantrip'].includes(t)).slice(0, 4).map(t => `<span class="trait">${esc(t)}</span>`).join('')}${def}${s.rng ? `<span class="cs-def">${esc(s.rng)}</span>` : ''}</div>
${btns.length ? `<div class="b">${btns.join('')}</div>` : ''}</div>`;
}
const pipline = (left, n) => `<span class="cs-pipline" aria-label="${left} of ${n} left">${Array.from({length: n}, (_, i) => `<i class="${i < left ? 'on' : ''}"></i>`).join('')}</span>`;
function tabSpells() {
  ensureEntries();
  const out = [];
  for (const sc of res.spellcasting) {
    const e = sc.e;
    const known = (e.known || []).map(k => rec(k)).filter(Boolean);
    const cantrips = known.filter(r => (r.tr || []).includes('cantrip'));
    const maxRank = sc.slots ? sc.slots.reduce((m, n, i) => n > 0 && i > 0 ? i : m, 0) : Math.ceil(ch.level / 2);
    let body = '';
    if (e.kind === 'staff') {
      const C = sc.charges, left = C.max - C.used;
      const list = (e.staff || []).filter(x => x.lv <= ch.level).map(x => ({s: rec(x.k), rank: x.rank})).filter(x => x.s);
      const ranks = [...new Set(list.map(x => x.rank))].sort((a, b) => a - b);
      body += `<div class="cs-charges"><span class="l">Charges</span>${pipline(left, C.max)}<b>${left} of ${C.max}</b>
<label class="cs-field inl"><span>Expended slot</span><select data-act="staff-extra" data-e="${esc(e.id)}">${Array.from({length: C.top + 1}, (_, i) => `<option value="${i}"${Number(e.extra || 0) === i ? ' selected' : ''}>${i ? 'Rank ' + i : 'None'}</option>`).join('')}</select></label>
<button type="button" class="chip mini" data-act="staff-prep" data-e="${esc(e.id)}">Prepare the staff</button></div>
<p class="small muted">${esc(e.note || '')} Charges equal your highest spell slot rank (${C.top}), plus the rank of one slot you expend when you prepare it. A spell costs charges equal to its rank; cantrips are free.</p>`;
      if (!list.length) body += `<p class="small muted">The staff's spells start at level ${Math.min(...(e.staff || [{lv: 1}]).map(x => x.lv))}.</p>`;
      for (const rk of ranks) {
        body += `<div class="cs-rankrow"><div class="rk">${rk ? 'Rank ' + rk : 'Cantrips'}</div><div class="cs-spellgrid">${list.filter(x => x.rank === rk).map(x =>
          spellCard(x.s, {entry: e, rank: rk || sc.cantripRank, castAct: rk ? 'staff-cast' : null, castLabel: rk ? `Cast for ${rk} charge${rk > 1 ? 's' : ''}` : null, disabled: rk > left})).join('')}</div></div>`;
      }
    } else if (sc.slots) {
      if (cantrips.length) body += `<div class="cs-rankrow"><div class="rk">Cantrips<small>rank ${sc.cantripRank}</small></div><div class="cs-spellgrid">${cantrips.map(s => spellCard(s, {entry: e, rank: sc.cantripRank})).join('')}</div></div>`;
      for (let rk = 1; rk < sc.slots.length; rk++) {
        const n = sc.slots[rk]; if (!n) continue;
        if (e.kind === 'prepared') {
          const prep = (e.prepared || {})[rk] || [];
          const usedArr = (e.used || {})[rk] || [];
          const cells = [];
          for (let i = 0; i < n; i++) {
            const k = prep[i], r = k ? rec(k) : null, used = usedArr.includes(i);
            const sel = `<select data-act="prep" data-e="${esc(e.id)}" data-r="${rk}" data-i="${i}" aria-label="Rank ${rk} slot ${i + 1}"><option value="">Empty slot</option>${known.filter(s => !(s.tr || []).includes('cantrip') && (s.lv || 1) <= rk).map(s => `<option value="${esc(s.k)}"${s.k === k ? ' selected' : ''}>${esc(s.n)}</option>`).join('')}</select>`;
            cells.push(`<div class="cs-pslot${used ? ' used' : ''}">${sel}${r ? spellCard(r, {entry: e, rank: rk, castAct: 'cast-prep', castLabel: used ? 'Cast already' : 'Cast', disabled: used, used, extra: ` data-i="${i}"`}) : ''}${used ? `<button type="button" class="chip mini" data-act="uncast" data-e="${esc(e.id)}" data-r="${rk}" data-i="${i}">Restore slot</button>` : ''}</div>`);
          }
          body += `<div class="cs-rankrow"><div class="rk">Rank ${rk}${pipline(n - usedArr.length, n)}</div><div class="cs-spellgrid">${cells.join('')}</div></div>`;
        } else {
          const usedN = (e.usedN || {})[rk] || 0, left = n - usedN;
          const rep = known.filter(s => !(s.tr || []).includes('cantrip') && (s.lv || 1) <= rk);
          body += `<div class="cs-rankrow"><div class="rk">Rank ${rk}${pipline(left, n)}<small>${left} of ${n}</small>${usedN ? `<button type="button" class="chip mini" data-act="castn" data-e="${esc(e.id)}" data-r="${rk}" data-d="-1">Restore one</button>` : ''}</div>
<div class="cs-spellgrid">${rep.map(s => spellCard(s, {entry: e, rank: rk, castAct: 'cast-spont', disabled: !left})).join('') || '<p class="small muted">Add spells to the repertoire below.</p>'}</div></div>`;
        }
      }
    } else if (e.kind === 'focus') {
      const left = res.focusMax - (ch.focusUsed || 0);
      body += `<div class="cs-charges"><span class="l">Focus Points</span>${pipline(left, res.focusMax)}<b>${left} of ${res.focusMax}</b></div>`;
      body += `<div class="cs-spellgrid">${known.map(s => spellCard(s, {entry: e, rank: sc.cantripRank, castAct: (s.tr || []).includes('cantrip') ? null : 'cast-focus', castLabel: 'Cast for 1 Focus Point', disabled: !left})).join('') || '<p class="small muted">Add focus spells below.</p>'}</div>`;
    } else {
      body += `<div class="cs-spellgrid">${known.map(s => { const used = ((e.innateUsed || {})[s.k]) || 0; return spellCard(s, {entry: e, rank: s.lv, castAct: 'cast-innate', castLabel: used ? `Cast (${used} today)` : 'Cast'}); }).join('') || '<p class="small muted">Add innate spells below.</p>'}</div>`;
    }
    const manageName = {prepared: e.id === 'class' && ['cl:wizard', 'cl:magus'].includes(ch.class) ? 'Spellbook' : 'Spells you can prepare', spontaneous: 'Repertoire', focus: 'Focus spells', innate: 'Innate spells'}[e.kind];
    const manage = e.kind === 'staff' ? '' : `<details class="cs-manage"><summary>${manageName} (${known.length})</summary>
<ul class="cs-spells">${known.slice().sort((a, b) => (a.lv || 0) - (b.lv || 0) || a.n.localeCompare(b.n)).map(s => `<li>${g(s)}${legTag(s)} <small>${(s.tr || []).includes('cantrip') ? 'cantrip' : 'rank ' + s.lv}</small><button type="button" class="x" data-act="spell-del" data-e="${esc(e.id)}" data-k="${esc(s.k)}" aria-label="Remove">×</button></li>`).join('')}</ul>
<button type="button" class="chip" data-act="spell-add" data-e="${esc(e.id)}" data-max="${maxRank}">Add a spell</button></details>`;
    const trad = TRADS.includes(e.trad) ? e.trad : 'arcane';
    out.push(`<section class="cs-sc t-${trad}"><header class="cs-schead"><span class="cs-trad" title="${cap(trad)}">${ic(trad)}</span>
<div class="cs-scid"><input class="cs-ename" value="${esc(e.name)}" data-field="ename" data-e="${esc(e.id)}" aria-label="Name"><div class="cs-scsub"><span class="cs-kind">${ic(KIND_ICON[e.kind] || 'book')}${KIND_NAME[e.kind] || cap(e.kind)}</span>
<select data-act="etrad" data-e="${esc(e.id)}" aria-label="Tradition">${TRADS.map(t => `<option value="${t}"${e.trad === t ? ' selected' : ''}>${cap(t)}</option>`).join('')}</select>
<select data-act="eattr" data-e="${esc(e.id)}" aria-label="Attribute">${ATTRS.map(a => `<option value="${a}"${e.attr === a ? ' selected' : ''}>${ATTR_NAME[a]}</option>`).join('')}</select>${e.archetype ? '<small>Slots come from Basic, Expert and Master Spellcasting feats.</small>' : ''}</div></div>
<div class="cs-scstats"><button type="button" class="cs-sv" data-act="roll" data-k="spellatk:${esc(e.id)}" aria-label="Roll spell attack"><span class="l">Spell attack</span><b>${fmt(sc.attack.total)}</b></button><button type="button" class="cs-sv" data-act="breakdown" data-k="spelldc:${esc(e.id)}"><span class="l">Spell DC</span><b>${sc.dc.total}</b></button><small>${RANKS[sc.rank]}</small></div>
${e.id !== 'class' ? `<button type="button" class="x" data-act="entry-del" data-e="${esc(e.id)}" aria-label="Remove this spellcasting">×</button>` : ''}</header>
<div class="cs-scbody">${body}${manage}</div></section>`);
  }
  return out.join('') + `<section class="cs-sec cs-add"><h2>Add spellcasting</h2><p class="small muted">Archetype spellcasting is added automatically when you take a spellcasting dedication. Add others here: innate spells, focus spells or a staff.</p>
<div class="cs-inline"><select id="cs-newkind" aria-label="Kind"><option value="prepared">Prepared</option><option value="spontaneous">Spontaneous</option><option value="focus">Focus</option><option value="innate">Innate</option><option value="staff">Staff</option></select>
<select id="cs-newtrad" aria-label="Tradition">${TRADS.map(t => `<option value="${t}">${cap(t)}</option>`).join('')}</select>
<select id="cs-newattr" aria-label="Attribute">${ATTRS.map(a => `<option value="${a}"${a === 'int' ? ' selected' : ''}>${ATTR_NAME[a]}</option>`).join('')}</select>
<select id="cs-newtable" aria-label="Spell slots"><option value="">No slot table</option>${Object.keys(db.slots).map(k => `<option value="${k}">${cap(k)} slots</option>`).join('')}</select>
<button type="button" class="chip" data-act="entry-add">Add</button></div></section>`;
}

// ───────── Feats tab ─────────
function tabFeats() {
  const groups = {};
  for (const it of res.S.items) {
    const r = it.r;
    if (r.t !== 'feat') continue;
    const k = r.cat === 'classfeature' ? 'Class features' : r.cat === 'ancestryfeature' ? 'Ancestry features' : r.cat === 'ancestry' ? 'Ancestry feats' : r.cat === 'class' ? ((r.tr || []).includes('archetype') ? 'Archetype feats' : 'Class feats') : r.cat === 'skill' ? 'Skill feats' : r.cat === 'general' ? 'General feats' : 'Other';
    (groups[k] = groups[k] || []).push(it);
  }
  const order = ['Ancestry feats', 'Class feats', 'Archetype feats', 'Skill feats', 'General feats', 'Class features', 'Ancestry features', 'Other'];
  return order.filter(k => groups[k]).map(k => `<section class="cs-sec"><h2>${k}</h2><ul class="cs-featlist">${groups[k].sort((a, b) => (a.lvl || 0) - (b.lvl || 0)).map(it =>
    `<li><span class="lv">${it.lvl || ''}</span>${act(it.r.act)} ${g(it.r)}${legTag(it.r)}${it.granted ? ` <small>from ${esc((res.S.byUid[it.parent] || {r: {n: ''}}).r.n)}</small>` : ''}</li>`).join('')}</ul></section>`).join('') || '<p class="muted">Choose an ancestry and class on the Build tab.</p>';
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
  const st = {q: '', sel: {}, rng: {}, tog: {}, tr: [], tm: 'any', sort: sorts.length ? sorts[0][0] : '', open: false};
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
function fxHTML(spec, st, sorts, title = 'Filters and sorting') {
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
  return `<details class="cs-fx"${st.open ? ' open' : ''}><summary><span class="cs-fxh">${esc(title)}</span><span class="cs-fxn"></span></summary><div class="cs-fxb">${rows}${togs ? `<div class="cs-fr"><span class="cs-fl">Show</span><div class="cs-fc">${togs}</div></div>` : ''}${sort}<div class="cs-fr"><span class="cs-fl"></span><div class="cs-fc"><button type="button" class="chip mini" data-fclear="1">Clear filters</button></div></div></div></details>`;
}
// wires the controls in box to st; redraw() is called after every change
function fxBind(box, spec, st, defs, items, sorts, redraw) {
  const host = () => box.querySelector('.cs-fx');
  const tf = spec.find(f => f.type === 'traits');
  const tcount = tf ? countVals(items, tf.val) : new Map();
  const tnames = [...tcount.keys()].sort();
  // the summary line names every filter in force, including the defaults, so a closed panel still shows them
  const strip = h => String(h).replace(/<[^>]+>/g, '').trim();
  const changed = () => {
    const parts = [];
    for (const f of spec) {
      if ((f.type === 'chips' || f.type === 'select') && (st.sel[f.k] || []).length) parts.push(st.sel[f.k].map(v => { const o = f.opts.find(x => x[0] === v); return o ? strip(o[1]).replace(/ \(\d+\)$/, '') || v : v; }).join(' or '));
      else if (f.type === 'range' && (st.rng[f.k][0] !== f.min || st.rng[f.k][1] !== f.max)) parts.push(`${f.label} ${st.rng[f.k][0]}–${st.rng[f.k][1]}`);
      else if (f.type === 'toggle' && st.tog[f.k]) parts.push(f.text);
      else if (f.type === 'traits' && st.tr.length) parts.push(st.tr.join(st.tm === 'all' ? ' and ' : ' or '));
    }
    const el = box.querySelector('.cs-fxn'); if (el) { el.textContent = parts.length ? parts.join(' · ') : 'None'; el.title = el.textContent; }
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
const ATTR_OPTS = ATTRS.map(a => [a, ATTR_NAME[a] || a]);
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
  if (kind === 'class') facets.push({k: 'key', label: 'Key attribute', type: 'chips', opts: ATTR_OPTS, val: it => it.rec.key || []},
    {k: 'sc', label: 'Spellcasting', type: 'chips', opts: [['1', 'Spellcaster'], ['0', 'No spellcasting']], val: it => String(it.rec.sc ? 1 : 0)},
    {k: 'hp', label: 'Hit Points', type: 'chips', opts: [['6', '6'], ['8', '8'], ['10', '10'], ['12', '12']], val: it => String(it.rec.hp)});
  if (kind === 'ancestry') facets.push({k: 'boost', label: 'Attribute boost', type: 'chips', opts: ATTR_OPTS, val: boostVal},
    {k: 'hp', label: 'Hit Points', type: 'chips', opts: [['6', '6'], ['8', '8'], ['10', '10'], ['12', '12']], val: it => String(it.rec.hp)},
    {k: 'size', label: 'Size', type: 'chips', opts: [['tiny', 'Tiny'], ['sm', 'Small'], ['med', 'Medium'], ['lg', 'Large']], val: it => it.rec.size || ''},
    {k: 'vis', label: 'Vision', type: 'chips', opts: [['normal', 'Normal'], ['low-light-vision', 'Low-light'], ['darkvision', 'Darkvision']], val: it => it.rec.vision || 'normal'});
  if (kind === 'background') facets.push({k: 'boost', label: 'Attribute boost', type: 'chips', opts: ATTR_OPTS, val: boostVal},
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
  const p = findPending(uid, flag);
  if (!p) return;
  const items = eng.choices(res.pending.includes(p) ? res.S : planRes().S, p).map(o => ({label: o.label, rec: o.rec, value: o.value, sub: o.rec ? recSub(o.rec) : ''}));
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

// ───────── item browser ─────────
const isRune = r => /^etched/.test(r.use || '');
const isStaff = r => (r.tr || []).includes('staff') || r.cat === 'wand';
const ICATS = [
  ['all', 'Everything', () => true],
  ['weapon', 'Weapons', r => r.t === 'weapon'],
  ['armor', 'Armour', r => r.t === 'armor'],
  ['shield', 'Shields', r => r.t === 'shield'],
  ['rune', 'Runes', r => r.t === 'equipment' && isRune(r)],
  ['staff', 'Staves and wands', r => r.t !== 'weapon' && isStaff(r)],
  ['worn', 'Worn items', r => r.t === 'equipment' && /^worn/.test(r.use || '') && !isStaff(r)],
  ['held', 'Held items', r => r.t === 'equipment' && /^(held|affixed-or-held|carried)/.test(r.use || '') && !isStaff(r)],
  ['consumable', 'Consumables', r => r.t === 'consumable' && r.cat !== 'wand'],
  ['ammo', 'Ammunition', r => r.t === 'ammo'],
  ['gear', 'Other gear', r => r.t === 'equipment' && !isRune(r) && !isStaff(r) && !/^(worn|held|affixed-or-held|carried)/.test(r.use || '')],
  ['backpack', 'Containers', r => r.t === 'backpack'],
  ['treasure', 'Treasure and kits', r => r.t === 'treasure' || r.t === 'kit'],
];
const SORTS = [['name', 'Name'], ['lv', 'Level, lowest first'], ['lv-', 'Level, highest first'], ['cp', 'Price, lowest first'], ['cp-', 'Price, highest first'], ['bulk', 'Bulk, lightest first'], ['grade', 'Compendium grade']];
const IB_SPEC = [Object.assign({}, FX_TR, {val: r => r.tr || []}), Object.assign(fxGrade(), {val: r => (gradeOf('it', r) || ['none'])[0]}),
  {k: 'use', label: 'Worn or held', type: 'chips', opts: [['worn', 'Worn'], ['held', 'Held'], ['etched', 'Etched (runes)'], ['affixed', 'Affixed'], ['other', 'Other']], val: r => { const u = r.use || ''; return /^worn/.test(u) ? 'worn' : /^held|^carried/.test(u) ? 'held' : /^etched/.test(u) ? 'etched' : /^affixed/.test(u) ? 'affixed' : 'other'; }},
  {k: 'src', label: 'Source', type: 'select', opts: [], val: r => r.src || ''}];
const useText = u => u ? cap(String(u).replace(/^worn(?=[a-z])/, 'worn ').replace(/-/g, ' ').replace(/\b1\b/, 'one').replace(/\b2\b/, 'two')) : '';
const bulkText = b => b === 0.1 ? 'L' : b ? String(b) : '—';
let ib = null;
function itemBrowser() {
  ib = ib || {q: '', cat: 'all', sub: '', lo: 0, hi: ch.level, afford: false, rar: '', leg: true, sort: 'name'};
  ib.hi = Math.max(ib.hi, 0);
  const all = Object.values(db.e).filter(r => ['weapon', 'armor', 'shield', 'equipment', 'consumable', 'treasure', 'backpack', 'kit', 'ammo'].includes(r.t));
  if (!IB_SPEC[3].opts.length) { const c = countVals(all, r => r.src); IB_SPEC[3].opts = [...c.keys()].sort().map(v => [v, `${v} (${c.get(v)})`]); }
  const ibDefs = fxDefaults(IB_SPEC, [], {open: false});
  ib.fx = ib.fx || fxClone(ibDefs);
  const box = document.createElement('div');
  box.className = 'cs-ib';
  box.innerHTML = `<div class="cs-ibtop"><label class="search"><input type="search" class="f-q" placeholder="Search names and traits, such as fire potion" aria-label="Search items" value="${esc(ib.q)}"></label>
<div class="cs-ibcats" role="group" aria-label="Category">${ICATS.map(([k, l]) => `<button type="button" class="chip mini${ib.cat === k ? ' on' : ''}" data-cat="${k}" aria-pressed="${ib.cat === k}">${l}</button>`).join('')}</div>
<div class="cs-ibf"><label class="cs-field inl f-subw"><span>Kind</span><select class="f-sub"></select></label>
<label class="cs-field inl"><span>Level</span><span class="cs-range"><input type="number" class="f-lo" min="0" max="30" value="${ib.lo}" aria-label="Lowest level"> to <input type="number" class="f-hi" min="0" max="30" value="${ib.hi}" aria-label="Highest level"></span></label>
<label class="cs-field inl"><span>Rarity</span><select class="f-rar"><option value="">Any</option><option value="common">Common</option><option value="uncommon">Uncommon</option><option value="rare">Rare</option><option value="unique">Unique</option></select></label>
<label class="cs-field inl"><span>Sort by</span><select class="f-sort">${SORTS.map(([k, l]) => `<option value="${k}"${ib.sort === k ? ' selected' : ''}>${l}</option>`).join('')}</select></label>
<label class="cs-tog"><input type="checkbox" class="f-aff"${ib.afford ? ' checked' : ''}> Only what I can afford</label>
<label class="cs-tog"><input type="checkbox" class="f-leg"${ib.leg ? ' checked' : ''}> Include legacy printings</label></div>
${fxHTML(IB_SPEC, ib.fx, [], 'More filters')}<p class="small muted cs-ibsum"></p></div><ul class="cs-iblist"></ul>`;
  box.querySelector('.f-rar').value = ib.rar;
  const list = box.querySelector('.cs-iblist'), sum = box.querySelector('.cs-ibsum'), subSel = box.querySelector('.f-sub');
  let lim = 60, shown = [];
  const subOf = r => r.t === 'weapon' ? (r.grp || '') : r.t === 'armor' ? (r.cat || '') : r.t === 'consumable' ? (r.cat || 'other') : r.t === 'equipment' && isRune(r) ? (/weapon/.test(r.use) ? 'weapon' : /armor/.test(r.use) ? 'armor' : 'other') : '';
  const subLabel = (k, v) => k === 'rune' ? {weapon: 'Weapon runes', armor: 'Armour runes', other: 'Other runes'}[v] || cap(v) : cap(v.replace(/-/g, ' '));
  const fillSub = () => {
    const pred = ICATS.find(c => c[0] === ib.cat)[2];
    const vals = [...new Set(all.filter(pred).map(subOf).filter(Boolean))].sort();
    subSel.innerHTML = `<option value="">All</option>` + vals.map(v => `<option value="${esc(v)}">${esc(subLabel(ib.cat, v))}</option>`).join('');
    if (!vals.includes(ib.sub)) ib.sub = '';
    subSel.value = ib.sub;
    box.querySelector('.f-subw').hidden = vals.length < 2 || ib.cat === 'all';
  };
  const owned = k => ch.inventory.filter(i => i.k === k).reduce((a, i) => a + (i.qty ?? 1), 0);
  const draw = () => {
    const toks = ib.q.trim().toLowerCase().split(/\s+/).filter(Boolean);
    const pred = ICATS.find(c => c[0] === ib.cat)[2];
    const purse = coinTotal(ch.coins);
    const m = all.filter(r => pred(r)
      && (!ib.sub || subOf(r) === ib.sub)
      && (r.lv || 0) >= ib.lo && (r.lv || 0) <= ib.hi
      && (!ib.rar || (r.rar || 'common') === ib.rar)
      && (ib.leg || !r.leg)
      && (!ib.afford || (r.cp || 0) <= purse)
      && fxMatch(IB_SPEC, ib.fx, r)
      && toks.every(t => r.n.toLowerCase().includes(t) || (r.tr || []).some(x => x.includes(t)) || (r.cat || '').includes(t) || (r.grp || '') === t));
    const by = ib.sort.replace('-', ''), dir = ib.sort.endsWith('-') ? -1 : 1;
    m.sort((a, b) => by === 'name' ? a.n.localeCompare(b.n) : by === 'grade' ? (gOrd(gradeOf('it', a)) - gOrd(gradeOf('it', b))) || a.n.localeCompare(b.n) : ((a[by] || 0) - (b[by] || 0)) * dir || a.n.localeCompare(b.n));
    if (toks.length && ib.sort === 'name') m.sort((a, b) => (b.n.toLowerCase().startsWith(toks[0]) - a.n.toLowerCase().startsWith(toks[0])));
    shown = m;
    sum.textContent = `${m.length.toLocaleString()} item${m.length === 1 ? '' : 's'}. You have ${money(purse)}.`;
    list.innerHTML = m.slice(0, lim).map((r, j) => {
      const have = owned(r.k);
      const meta = [`Level ${r.lv || 0}`, r.cp ? money(r.cp) : 'No price', `Bulk ${bulkText(r.bulk)}`, useText(r.use), r.rar && r.rar !== 'common' ? cap(r.rar) : ''].filter(Boolean);
      const extra = r.t === 'weapon' && r.dmg ? `${r.dmg.dice || 1}${r.dmg.die} ${r.dmg.damageType || ''}${r.rng ? `, range ${r.rng} ft` : ''}, ${r.cat || ''} ${r.grp || ''}` : r.t === 'armor' ? `AC +${r.ac || 0}, Dex cap ${r.dex ?? '—'}, ${r.cat || ''}` : r.t === 'shield' ? `AC +${r.ac || 0}, Hardness ${r.hard || 0}, ${r.hp || 0} HP` : '';
      return `<li class="cs-ires"><div class="t">${g(r)}${legTag(r)}${grBadge(gradeOf('it', r))}${have ? `<span class="cs-badge">You have ${have}</span>` : ''}</div>
<div class="m">${meta.map(x => `<span>${esc(x)}</span>`).join('')}</div>${extra ? `<div class="m">${esc(extra)}</div>` : ''}
${(r.tr || []).length ? `<div class="cs-trs">${r.tr.slice(0, 6).map(t => `<span class="trait">${esc(t.replace(/-/g, ' '))}</span>`).join('')}</div>` : ''}
<div class="b"><label class="cs-qty"><span class="sr">Quantity</span><input type="number" min="1" value="1" inputmode="numeric" data-q="${j}" aria-label="Quantity"></label>
<button type="button" class="chip mini" data-add="${j}">Add</button><button type="button" class="chip mini hi" data-buy="${j}"${(r.cp || 0) > purse ? ' disabled title="Not enough money"' : ''}>Buy${r.cp ? ' for ' + money(r.cp) : ''}</button></div></li>`;
    }).join('') + (m.length > lim ? `<li class="more"><button type="button" class="chip" data-more="1">Show ${Math.min(60, m.length - lim)} more</button></li>` : '')
      + (m.length ? '' : '<li class="muted">Nothing matches. Try a wider level range or another category.</li>');
  };
  const read = () => {
    ib.q = box.querySelector('.f-q').value; ib.sub = subSel.value;
    ib.lo = Math.max(0, Number(box.querySelector('.f-lo').value) || 0); ib.hi = Math.max(ib.lo, Number(box.querySelector('.f-hi').value || 30));
    ib.rar = box.querySelector('.f-rar').value; ib.sort = box.querySelector('.f-sort').value;
    ib.afford = box.querySelector('.f-aff').checked; ib.leg = box.querySelector('.f-leg').checked;
    lim = 60; draw();
  };
  let t;
  box.querySelector('.f-q').addEventListener('input', () => { clearTimeout(t); t = setTimeout(read, 120); });
  box.addEventListener('change', e => { if (!e.target.matches('[data-q], .f-q') && !e.target.closest('.cs-fx')) read(); });
  fxBind(box, IB_SPEC, ib.fx, ibDefs, all, [], () => { lim = 60; draw(); });
  box.addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.cat) { ib.cat = b.dataset.cat; box.querySelectorAll('[data-cat]').forEach(x => { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b); }); fillSub(); lim = 60; draw(); return; }
    if (b.dataset.more) { lim += 60; draw(); return; }
    const j = b.dataset.add ?? b.dataset.buy; if (j == null) return;
    const r = shown[+j]; if (!r) return;
    const qty = Math.max(1, Math.floor(Number(box.querySelector(`[data-q="${j}"]`).value) || 1));
    if (b.dataset.buy != null) {
      const cost = (r.cp || 0) * qty;
      if (coinTotal(ch.coins) < cost) { toast('Not enough money for ' + r.n + '.'); return; }
      spend(cost, `Bought ${qty > 1 ? qty + ' × ' : ''}${r.n}`);
    }
    addInv(Object.assign({}, r, {qty}));
    commit();
    toast(`${b.dataset.buy != null ? 'Bought' : 'Added'} ${qty > 1 ? qty + ' × ' : ''}${r.n}${b.dataset.buy != null && r.cp ? ' for ' + money((r.cp || 0) * qty) : ''}.`);
    draw();
  });
  fillSub(); draw();
  A.pushPanel('Inventory', 'Add or buy items', box, 'item-browser');
  setTimeout(() => box.querySelector('.f-q').focus({preventScroll: true}), 60);
}
function itemPanel(id) {
  const box = document.createElement('div');
  box.className = 'cs-itemp';
  const draw = () => {
    const inv = ch.inventory.find(i => i.id === id);
    if (!inv) { A.popPanel(); return false; }
    const r = eng.invRec(inv), c = inv.custom;
    const st = res.strikes.find(x => x.inv && x.inv.id === id);
    const R = Object.assign({}, r.runes || {}, inv.runes || {});
    const f = [['Type', typeLabel(r)], ['Level', `${r.lv || 0}${c && c.relic ? ', always equal to your level' : ''}`], ['Price', r.cp ? money(r.cp) : c ? 'Not for sale' : 'None'], ['Bulk', bulkText(r.bulk)], ['Usage', useText(r.use)], ['Rarity', r.rar ? cap(r.rar) : '']];
    if (r.t === 'weapon' && r.dmg) f.push(['Weapon', `${cap(r.cat || '')} ${r.grp || ''}`.trim()], ['Base damage', `${r.dmg.dice || 1}${r.dmg.die} ${r.dmg.damageType || ''}`], ['Range', r.rng ? r.rng + ' feet' : 'Melee']);
    if (st) f.push(['Attack', st.map.map(fmt).join(', ')], ['Damage', st.formula]);
    if (r.t === 'armor') f.push(['AC bonus', '+' + (r.ac || 0)], ['Dex cap', String(r.dex ?? 'None')], ['Check penalty', String(r.chk || 0)], ['Speed penalty', r.spd ? r.spd + ' feet' : 'None'], ['Strength', r.str != null ? String(r.str) : 'None']);
    if (r.t === 'shield') f.push(['AC bonus', '+' + (r.ac || 0)], ['Hardness', String(r.hard || 0)], ['Hit Points', String(r.hp || 0)]);
    if (['weapon', 'armor', 'shield'].includes(r.t)) f.push(['Runes', runeSummary(r, inv).replace(/^: /, '') || 'None']);
    if (r.apex) f.push(['Apex', `raises ${ATTR_NAME[r.apex]}${res.apex && res.apex.id === id ? ', active' : inv.inv ? ', not active: another apex item is' : ', when invested'}`]);
    const facts = `<dl class="cs-facts">${f.filter(x => x[1]).map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${v === runeSummary(r, inv).replace(/^: /, '') ? v : esc(v)}</dd></div>`).join('')}</dl>`;
    const traits = (r.tr || []).length ? `<div class="cs-trs">${r.tr.map(t => `<span class="trait">${esc(t.replace(/-/g, ' '))}</span>`).join('')}</div>` : '';
    const abil = (c && c.abil || []).map(a => `<p><b>${esc(a.n)}</b> ${esc(a.text)}</p>`).join('');
    let relic = '';
    if (c && c.relic) {
      relic = `<h3>Relic</h3>${(c.aspects || []).length ? `<p><b>Aspects</b> ${esc(c.aspects.join(' and '))}</p>` : ''}
<ul class="cs-gifts">${(c.gifts || []).map(gf => { const on = ch.level >= gf.lv; return `<li class="${on ? 'on' : ''}"><span class="lv">${gf.lv}</span><span>${gf.g ? `<a href="#" data-g="${esc(gf.g)}">${esc(gf.n)}</a>` : `<b>${esc(gf.n)}</b>`}<small>${esc(gf.kind)}</small>${gf.text ? `<small class="gt">${esc(gf.text)}</small>` : ''}</span><span class="st">${on ? 'Unlocked' : 'From level ' + gf.lv}</span></li>`; }).join('')}</ul>`;
    }
    const page = c && c.page ? `<p><a class="chip" href="#${esc(c.page)}" data-close-all="1">Open the ${esc(c.n)} page</a></p>` : '';
    const canInvest = eng.needsInvest(r, inv);
    const ctl = `<h3>On your sheet</h3><div class="cs-inline"><span class="cs-qtyl">Quantity <span class="cs-step"><button type="button" data-act="qty" data-id="${esc(id)}" data-d="-1" aria-label="Fewer">−</button><b>${inv.qty ?? 1}</b><button type="button" data-act="qty" data-id="${esc(id)}" data-d="1" aria-label="More">+</button></span></span>
<select data-act="state" data-id="${esc(id)}" aria-label="Where it is">${STATES.map(([k, l]) => `<option value="${k}"${(inv.eq || 'stowed') === k ? ' selected' : ''}>${l}</option>`).join('')}</select>
${canInvest ? `<label class="cs-tog"><input type="checkbox" data-act="invest" data-id="${esc(id)}"${inv.inv ? ' checked' : ''}> Invested</label>` : ''}
${['weapon', 'armor', 'shield'].includes(r.t) ? `<button type="button" class="chip mini" data-act="runes" data-id="${esc(id)}">Change runes</button>` : ''}
${r.t === 'consumable' ? `<button type="button" class="chip mini" data-act="consume" data-id="${esc(id)}">Use one</button>` : ''}
${c ? '' : `<button type="button" class="chip mini" data-act="sell" data-id="${esc(id)}">Sell for ${money(Math.floor((r.cp || 0) / 2))}</button>`}<button type="button" class="chip mini" data-act="remove" data-id="${esc(id)}">Remove</button></div>`;
    box.innerHTML = `${c && c.desc ? `<p>${esc(c.desc)}</p>` : ''}${facts}${traits}${abil}${relic}${page}${ctl}${!c && r.g ? '<h3>Rules text</h3><div class="cs-rules muted">Loading…</div>' : ''}`;
    if (!c && r.g && A.getEntry) A.getEntry(r.g).then(e => { const el = box.querySelector('.cs-rules'); if (el) { el.classList.remove('muted'); el.innerHTML = e ? e[2] : 'The rules text is not available offline yet.'; } }).catch(() => {});
    return true;
  };
  box.addEventListener('click', e => {
    if (e.target.closest('[data-close-all]')) { A.closeAll(); return; }
    if (!e.target.closest('[data-act]')) return;
    onClick(e); if (!e.target.closest('[data-act="runes"]')) draw();
  });
  box.addEventListener('change', e => { onChange(e); draw(); });
  if (!draw()) return;
  const inv = ch.inventory.find(i => i.id === id);
  A.pushPanel('Item', inv.custom ? inv.custom.n : inv.name || eng.invRec(inv).n, box, 'item:' + id);
}
function addInv(r) {
  if (r.t === 'kit' && r.kit) { for (const [k, q] of r.kit) { const x = rec(k); if (x) addInv(Object.assign({}, x, {qty: q || 1})); } return; }
  const same = (r.t === 'consumable' || r.t === 'ammo') ? ch.inventory.find(i => i.k === r.k) : null;
  if (same) { same.qty = (same.qty ?? 1) + (r.qty || 1); return; }
  ch.inventory.push({id: newId(), k: r.k, qty: r.qty || 1, eq: r.t === 'armor' ? 'worn' : 'stowed'});
}
function spend(cp, note) {
  let total = Math.max(0, coinTotal(ch.coins) - cp);
  let pp = ch.coins.pp || 0, rest = total - pp * 1000;
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
// spell facets shared by the add-a-spell panel and the Spellstrike chooser
const spellDef = r => (r.tr || []).includes('attack') ? 'attack' : (r.dfn && r.dfn.save && r.dfn.save.statistic) || 'none';
const spellArea = r => { const a = r.area && r.area.type; return !a ? 'none' : ['burst', 'cone', 'line', 'emanation'].includes(a) ? a : 'other'; };
const spellDmg = r => [...new Set(Object.values(r.dmg || {}).map(d => d && d.t).filter(Boolean))];
function spellFacets(items, get = it => it.rec) {
  const dts = countVals(items, it => spellDmg(get(it)));
  return {
    def: {k: 'def', label: 'Defense', type: 'chips', opts: [['attack', 'Spell attack (AC)'], ['fortitude', 'Fortitude'], ['reflex', 'Reflex'], ['will', 'Will'], ['none', 'No roll']], val: it => spellDef(get(it))},
    area: {k: 'area', label: 'Area', type: 'chips', opts: [['burst', 'Burst'], ['cone', 'Cone'], ['line', 'Line'], ['emanation', 'Emanation'], ['other', 'Other area'], ['none', 'No area']], val: it => spellArea(get(it)), hint: 'Expansive Spellstrike restores bursts, cones and lines'},
    dmg: {k: 'dmg', label: 'Damage type', type: 'chips', opts: [...dts.keys()].sort().map(v => [v, esc(cap(v))]).concat([['none', 'No damage']]), val: it => { const d = spellDmg(get(it)); return d.length ? d : ['none']; }},
    role: {k: 'role', label: 'Role', type: 'chips', opts: ROLE_NAMES.map((l, i) => [String(i), esc(l)]), hint: 'Rated 3 stars or more for that role on the Spells page', val: it => it.gr ? [...it.gr[1]].map((x, i) => +x >= 3 ? String(i) : null).filter(Boolean) : []},
  };
}
const roleSorts = () => ROLE_NAMES.map((l, i) => [`role${i}`, `${l} rating`, (a, b) => (+((b.gr || [])[1] || '000000')[i]) - (+((a.gr || [])[1] || '000000')[i])]);
function pickSpell(eid, max) {
  const e = ch.spells.entries.find(x => x.id === eid);
  const known = () => new Set(e.known || []);
  const items = Object.values(db.e).filter(r => r.t === 'spell' && !r.ritual).map(r => ({label: r.n, rec: r, gr: gradeOf('sp', r), hayx: [spellArea(r), spellDef(r), ...spellDmg(r)].join(' '), sub: recSub(r) + ' · ' + esc((r.trad || []).join(', '))}));
  const isC = r => (r.tr || []).includes('cantrip'), isF = r => (r.tr || []).includes('focus');
  const sf = spellFacets(items);
  const TRADS = ['arcane', 'divine', 'occult', 'primal'];
  const facets = [
    {k: 'rank', label: 'Rank', type: 'chips', opts: [['0', 'Cantrip'], ...Array.from({length: 10}, (_, i) => [String(i + 1), String(i + 1)])], cls: () => 'rk', val: it => isC(it.rec) ? '0' : String(it.rec.lv || 1)},
    {k: 'kind', label: 'Kind', type: 'chips', opts: [['cantrip', 'Cantrips'], ['focus', 'Focus spells'], ['spell', 'Other spells']], val: it => [isC(it.rec) ? 'cantrip' : '', isF(it.rec) ? 'focus' : '', !isC(it.rec) && !isF(it.rec) ? 'spell' : ''].filter(Boolean)},
    {k: 'trad', label: 'Tradition', type: 'chips', opts: TRADS.map(t => [t, cap(t)]), def: TRADS.includes(e.trad) ? [e.trad] : [], hint: 'Focus spells belong to no tradition and always match', val: it => (it.rec.trad || []).length ? it.rec.trad : TRADS},
    fxActs(it => it.rec.time), sf.def, sf.area, sf.dmg, sf.role, fxGrade(), FX_RAR, FX_TR, fxSrc(items),
    {k: 'cast', type: 'toggle', text: `Rank ${Math.max(1, max)} or lower`, def: true, test: it => isC(it.rec) || (it.rec.lv || 1) <= Math.max(1, max)},
    {k: 'ss', type: 'toggle', text: 'Works with Spellstrike', def: false, test: it => ssEligible(it.rec)},
    {k: 'kn', type: 'toggle', text: 'Hide spells already added', def: false, test: it => !known().has(it.rec.k)},
    FX_LEG];
  const sorts = [SO_NAME, ['rank', 'Rank, lowest first', (a, b) => (isC(a.rec) ? 0 : a.rec.lv || 1) - (isC(b.rec) ? 0 : b.rec.lv || 1)], ['rank-', 'Rank, highest first', (a, b) => (isC(b.rec) ? 0 : b.rec.lv || 1) - (isC(a.rec) ? 0 : a.rec.lv || 1)],
    SO_GR, ...roleSorts(), ['act', 'Action cost', (a, b) => actCost(a.rec.time) - actCost(b.rec.time)], ['def', 'Defense', (a, b) => spellDef(a.rec).localeCompare(spellDef(b.rec))]];
  for (const it of items) it.tag = '';
  const mark = () => { const kn = known(); for (const it of items) it.tag = kn.has(it.rec.k) ? ' <span class="cs-badge">Added</span>' : ''; };
  mark();
  picker('Add a spell', e.name, items, it => { e.known = e.known || []; if (!e.known.includes(it.rec.k)) e.known.push(it.rec.k); commit(); },
    {verb: 'Add', keepOpen: true, key: 'spell:' + eid, facets, sorts, redrawOnPick: mark, placeholder: 'Search names, traits and sources, such as fire cone'});
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
  box.innerHTML = html + `<p class="small muted">Property rune slots equal the potency rune's value. Change the potency rune and save to get more slots.</p><button type="button" class="chip" data-save="1">Save</button>`;
  box.addEventListener('click', e => {
    if (!e.target.closest('[data-save]')) return;
    const nr = {};
    box.querySelectorAll('select[data-k]').forEach(s => nr[s.dataset.k] = Number(s.value));
    nr.property = [...box.querySelectorAll('select[data-prop]')].map(s => s.value).filter(Boolean);
    if (inv.custom) inv.custom.runes = nr; else inv.runes = nr;
    commit(); A.popPanel();
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
<fieldset><legend>Weapon</legend><label class="cs-field"><span>Category</span><select data-k="cat"><option>simple</option><option selected>martial</option><option>advanced</option><option>unarmed</option></select></label>
<label class="cs-field"><span>Group</span><input type="text" data-k="grp" value="polearm"></label>
<label class="cs-field"><span>Damage die</span><select data-k="die"><option>d4</option><option>d6</option><option selected>d8</option><option>d10</option><option>d12</option></select></label>
<label class="cs-field"><span>Damage type</span><select data-k="dtype"><option>slashing</option><option>piercing</option><option>bludgeoning</option></select></label>
<label class="cs-field"><span>Range increment in feet (blank for melee)</span><input type="number" data-k="rng"></label></fieldset>
<fieldset><legend>Armour</legend><label class="cs-field"><span>Category</span><select data-k="acat"><option>light</option><option selected>medium</option><option>heavy</option><option>unarmored</option></select></label>
<label class="cs-field"><span>AC bonus</span><input type="number" data-k="ac" value="0"></label><label class="cs-field"><span>Dex cap</span><input type="number" data-k="dex" value="5"></label>
<label class="cs-field"><span>Check penalty</span><input type="number" data-k="chk" value="0"></label><label class="cs-field"><span>Speed penalty</span><input type="number" data-k="spd" value="0"></label>
<label class="cs-field"><span>Strength</span><input type="number" data-k="str" value="0"></label></fieldset>
<label class="cs-field"><span>Special ability, if any: its name, a colon, then what it does</span><textarea data-k="abil" rows="3"></textarea></label>
<label class="cs-field"><span>Apex item: the attribute it raises when invested</span><select data-k="apex"><option value="">Not an apex item</option>${ATTRS.map(a => `<option value="${a}">${ATTR_NAME[a]}</option>`).join('')}</select></label>
<button type="button" class="chip" data-save="1">Add</button>`;
  box.addEventListener('click', e => {
    if (!e.target.closest('[data-save]')) return;
    const v = k => box.querySelector(`[data-k="${k}"]`).value;
    const t = v('t');
    const c = {n: v('n') || 'Custom item', t, lv: Number(v('lv')) || 0, tr: v('tr').split(',').map(s => slugify(s)).filter(Boolean), bulk: Number(v('bulk')) || 0};
    if (v('apex')) { c.apex = v('apex'); for (const t2 of ['apex', 'invested']) if (!c.tr.includes(t2)) c.tr.push(t2); }
    if (t === 'weapon') Object.assign(c, {cat: v('cat'), grp: slugify(v('grp')) || null, dmg: {dice: 1, die: v('die'), damageType: v('dtype')}, rng: Number(v('rng')) || null, runes: {potency: 0, striking: 0, property: []}});
    if (t === 'armor') Object.assign(c, {cat: v('acat'), ac: Number(v('ac')) || 0, dex: Number(v('dex')), chk: Number(v('chk')) || 0, spd: Number(v('spd')) || 0, str: Number(v('str')) || null, runes: {potency: 0, resilient: 0, property: []}});
    const ab = v('abil').trim();
    if (ab) { const i = ab.indexOf(':'); c.abil = [{n: i > 0 ? ab.slice(0, i).trim() : 'Ability', text: i > 0 ? ab.slice(i + 1).trim() : ab}]; }
    ch.inventory.push({id: newId(), custom: c, qty: 1, eq: t === 'armor' ? 'worn' : t === 'weapon' ? 'held2' : 'stowed'});
    commit(); A.popPanel();
  });
  A.pushPanel('Inventory', 'Custom item', box, 'custom-item');
}
const BONUS_KINDS = [['skill', 'Skill feat'], ['general', 'General feat'], ['class', 'Class feat'], ['ancestry', 'Ancestry feat'], ['archetype', 'Archetype feat'], ['bonus', 'Any feat'], ['increase', 'Skill increase']];
// A bonus slot's id ends in its level, which the rules engine reads for the feat's level, so changing the level
// or type gives it a new id and carries over what was chosen in it (dropped when the new type can't hold it).
function editBonusSlot(id, patch) {
  const b = ch.bonusSlots.find(x => x.id === id); if (!b) return;
  const kind = patch.kind || b.kind, lv = Math.max(1, Math.min(20, Number(patch.lv ?? b.lv) || 1));
  const nid = `${kind === 'increase' ? 'inc' : kind}-b${newId()}-${lv}`;
  const wasInc = b.kind === 'increase', isInc = kind === 'increase';
  ch.bonusInc = ch.bonusInc || {};
  if (wasInc && isInc && ch.bonusInc[id]) ch.bonusInc[nid] = ch.bonusInc[id];
  delete ch.bonusInc[id];
  if (!wasInc && !isInc && ch.feats[id]) {
    ch.feats[nid] = ch.feats[id];
    for (const k of Object.keys(ch.choices)) if (k === 'feat:' + id || k.startsWith('feat:' + id + '>')) { ch.choices[k.replace('feat:' + id, 'feat:' + nid)] = ch.choices[k]; delete ch.choices[k]; }
  }
  delete ch.feats[id];
  if (wasInc !== isInc && ['Bonus feat', 'Bonus skill increase'].includes(b.label)) b.label = isInc ? 'Bonus skill increase' : 'Bonus feat';
  Object.assign(b, {id: nid, kind, lv});
  ch.bonusSlots.sort((x, y) => x.lv - y.lv);
}
function bonusSlot() {
  const box = document.createElement('div');
  box.className = 'cs-runes';
  box.innerHTML = `<label class="cs-field"><span>Kind</span><select data-k="kind"><option value="skill">Skill feat</option><option value="general">General feat</option><option value="class">Class feat</option><option value="ancestry">Ancestry feat</option><option value="archetype">Archetype feat</option><option value="bonus">Any feat</option><option value="increase">Skill increase</option></select></label>
<label class="cs-field"><span>Level</span><input type="number" data-k="lv" value="${ch.level}" min="1" max="20"></label><label class="cs-field"><span>Label</span><input type="text" data-k="label" value="Bonus feat"></label>
<button type="button" class="chip" data-save="1">Add</button>`;
  const lab = box.querySelector('[data-k="label"]');
  box.querySelector('[data-k="kind"]').addEventListener('change', e => {
    if (['Bonus feat', 'Bonus skill increase'].includes(lab.value)) lab.value = e.target.value === 'increase' ? 'Bonus skill increase' : 'Bonus feat';
  });
  box.addEventListener('click', e => {
    if (!e.target.closest('[data-save]')) return;
    const v = k => box.querySelector(`[data-k="${k}"]`).value;
    const lv = Math.max(1, Math.min(20, Number(v('lv')) || 1)), kind = v('kind');
    ch.bonusSlots.push({id: `${kind === 'increase' ? 'inc' : kind}-b${newId()}-${lv}`, lv, kind, label: v('label') || (kind === 'increase' ? 'Bonus skill increase' : 'Bonus feat')});
    ch.bonusSlots.sort((x, y) => x.lv - y.lv);
    commit(); A.popPanel();
  });
  A.pushPanel('Build', 'Add a bonus feat or skill increase', box, 'bonus-slot');
}

// ───────── breakdowns ─────────
function breakdown(k) {
  let st = null;
  if (k === 'ac') st = res.ac; else if (k === 'hp') st = res.hp; else if (k === 'perception') st = res.perception; else if (k === 'speed') st = res.speed;
  else if (k === 'initiative') st = res.initiative; else if (k === 'classdc') st = Object.values(res.classDCs).find(c => c.primary);
  else if (k.startsWith('save:')) st = res.saves[k.slice(5)]; else if (k.startsWith('skill:')) st = res.skills[k.slice(6)];
  else if (k.startsWith('strike:')) st = res.strikes[+k.slice(7)].attack; else if (k.startsWith('damage:')) st = res.strikes[+k.slice(7)].damage;
  else if (k.startsWith('spellatk:') || k.startsWith('spelldc:')) { const sc = res.spellcasting.find(s => s.e.id === k.split(':')[1]); st = k.startsWith('spellatk') ? sc.attack : sc.dc; }
  if (k.startsWith('attr:')) { attrBreakdown(k.slice(5)); return; }
  if (!st) return;
  const base = /^(ac|classdc|spelldc)/.test(k) ? 10 : 0;
  const rows = (base ? ['<tr><td>Base</td><td>10</td><td></td></tr>'] : []).concat(st.mods.map(m => `<tr class="${m.applied ? '' : 'off'}"><td>${esc(m.label)}${m.situational ? ' <small>situational</small>' : ''}</td><td>${fmt(m.value)}</td><td><small>${esc(m.type || 'untyped')}${m.applied ? '' : m.situational ? '' : ', does not stack'}</small></td></tr>`));
  const box = document.createElement('div');
  box.className = 'cs-bd';
  const extra = k.startsWith('save:') && st.degree && st.degree.length ? `<p class="small">Successes are critical successes, from ${esc(st.degree.join(', '))}.</p>` : '';
  const canRoll = /^(save:|skill:|perception|initiative|strike:|spellatk:)/.test(k);
  box.innerHTML = `<p class="cs-bdt"><b>${k === 'speed' ? st.total + ' feet' : base || k === 'hp' ? st.total : fmt(st.total)}</b></p><table class="tbl"><tbody>${rows.join('')}</tbody></table>${extra}
${canRoll ? `<button type="button" class="chip" data-roll="1">Roll</button>` : ''}<p class="small muted">Situational modifiers apply only when their condition holds, such as against an off-guard target.</p>`;
  box.addEventListener('click', e => { if (!e.target.closest('[data-roll]')) return; A.popPanel(); if (k.startsWith('strike:')) rollStrike(+k.slice(7)); else rollKey(k); commit(); });
  A.pushPanel('Breakdown', st.label, box, 'bd:' + k);
}

function attrBreakdown(a) {
  const box = document.createElement('div');
  box.className = 'cs-bd';
  const ap = res.apex && res.apex.attr === a ? res.apex : null;
  const from = ap ? Math.trunc(ap.before) : res.attributes[a];
  box.innerHTML = `<p class="cs-bdt"><b>${fmt(res.attributes[a])}</b></p><table class="tbl"><tbody>
<tr><td>Boosts and flaws from your build</td><td>${fmt(from)}</td><td></td></tr>
${ap ? `<tr><td>${esc(ap.name)} (apex item)</td><td>${fmt(res.attributes[a] - from)}</td><td><small>raises the modifier by 1 or to +4, whichever is higher</small></td></tr>` : ''}</tbody></table>
<p class="small muted">Boosts and flaws are chosen on the Build tab. An invested apex item raises one attribute; only one apex item can do so at a time.</p>
<button type="button" class="chip" data-go="1">Open the Build tab</button>`;
  box.addEventListener('click', e => { if (!e.target.closest('[data-go]')) return; A.popPanel(); tab = 'build'; render(); });
  A.pushPanel('Breakdown', ATTR_NAME[a] || a, box, 'bd:attr:' + a);
}

// ───────── upkeep ─────────
function applyDamage(n) {
  const hp = ch.hp, c = ch.conditions, max = res.hp.total;
  const fromTemp = Math.min(hp.temp || 0, n);
  hp.temp = (hp.temp || 0) - fromTemp;
  const before = max - (hp.damage || 0);
  hp.damage = Math.min(max, (hp.damage || 0) + n - fromTemp);
  if (max - hp.damage <= 0 && n - fromTemp > 0) {
    if (c.dying) { c.dying += 1; toast('Damage while dying raises dying to ' + c.dying + '.'); }
    else if (before > 0) { c.dying = 1 + (c.wounded || 0); toast('Knocked out at 0 Hit Points: dying ' + c.dying + '.'); }
  }
}
function applyHeal(n) {
  const hp = ch.hp, c = ch.conditions;
  hp.damage = Math.max(0, (hp.damage || 0) - n);
  if (c.dying && n > 0) { delete c.dying; c.wounded = (c.wounded || 0) + 1; toast('No longer dying. Wounded ' + c.wounded + '.'); }
}
function endTurn() {
  const c = ch.conditions, e = ch.enc;
  const notes = [];
  if (c.frightened) { c.frightened -= 1; if (!c.frightened) delete c.frightened; notes.push('frightened went down by 1'); }
  for (const [k, v] of Object.entries(ch.effects)) {
    if (v && typeof v === 'object' && v.rounds != null) { v.rounds -= 1; if (v.rounds <= 0) { delete ch.effects[k]; notes.push((rec(k) || {n: k}).n.replace(/^(Effect|Spell Effect|Stance): /, '') + ' ended'); } }
  }
  for (const k of Object.keys(ch.uses || {})) { const r = rec(k); if (r && r.freq && (r.freq.per === 'round' || r.freq.per === 'turn')) delete ch.uses[k]; }
  if (c['persistent-damage']) {
    const ent = check('Persistent damage: flat check to end it', 0, {dc: 15, mode: 'normal', sub: 'Take the persistent damage first'});
    if (ent.dg >= 2) { delete c['persistent-damage']; notes.push('persistent damage ended'); }
  }
  e.round += 1; e.actions = maxActions(); e.reaction = true; e.attacks = 0;
  toast('Round ' + e.round + '.' + (notes.length ? ' ' + cap(notes.join('; ')) + '.' : ''));
}
function restNight() {
  const c = ch.conditions;
  const con = Math.max(1, res.attributes.con);
  const healed = Math.min(ch.hp.damage || 0, con * ch.level);
  ch.hp.damage = Math.max(0, (ch.hp.damage || 0) - con * ch.level);
  delete c.fatigued;
  if (c.doomed) { c.doomed -= 1; if (!c.doomed) delete c.doomed; }
  if (c.drained) { c.drained -= 1; if (!c.drained) delete c.drained; }
  for (const e of ch.spells.entries) { e.innateUsed = {}; if (e.kind === 'staff') e.used = 0; else { e.used = {}; e.usedN = {}; } }
  ch.focusUsed = 0;
  for (const k of Object.keys(ch.uses || {})) { const r = rec(k); if (!r || !r.freq || r.freq.per === 'day' || /^P/.test(r.freq.per)) delete ch.uses[k]; }
  ch.trackers.spellstrike = true;
  pushLog({kind: 'note', label: 'Rested for the night', total: `Regained ${healed} Hit Points`});
  toast(`Rested: regained ${healed} Hit Points. Spell slots, Focus Points, staff charges and daily uses are restored.`);
}

// ───────── events ─────────
function onClick(e) {
  const b = e.target.closest('[data-act]');
  if (!b || b.tagName === 'SELECT' || (b.tagName === 'INPUT' && b.type !== 'button')) return;
  const a = b.dataset.act, d = b.dataset;
  const EN = id => ch.spells.entries.find(x => x.id === id);
  switch (a) {
    case 'tab': tab = d.t; render(); return;
    case 'tray': trayOpen = !trayOpen; render(); return;
    case 'new': { const c = blank(); store.ids.push(c.id); store.cur = c.id; saveStore(); putChar(c); ch = c; recompute(); tab = 'build'; render(); return; }
    case 'dup': { const c = JSON.parse(JSON.stringify(ch)); c.id = newId(); c.name += ' (copy)'; store.ids.push(c.id); store.cur = c.id; saveStore(); putChar(c); ch = c; recompute(); render(); toast('Duplicated.'); return; }
    case 'delete':
      if (!confirmInline(b, 'Delete ' + ch.name + '?')) return;
      localStorage.removeItem(PRE + ch.id); store.ids = store.ids.filter(i => i !== ch.id);
      if (!store.ids.length) { const c = blank(); store.ids.push(c.id); putChar(c); }
      store.cur = store.ids[0]; saveStore(); ch = migrate(getChar(store.cur)); recompute(); render(); return;
    case 'export': exportChar(); return;
    case 'level': ch.level = Math.max(1, Math.min(20, ch.level + Number(d.d))); commit(); return;
    case 'hp': {
      const n = Math.max(0, Number(document.getElementById('cs-hpamt').value) || 0); if (!n) return;
      if (d.m === 'dmg') applyDamage(n); else if (d.m === 'heal') applyHeal(n); else ch.hp.temp = Math.max(ch.hp.temp || 0, n);
      commit(); return;
    }
    case 'apply-heal': applyHeal(Number(d.n) || 0); commit(); return;
    case 'recovery': {
      const dy = ch.conditions.dying || 0;
      const ent = check('Recovery check', 0, {dc: 10 + dy, mode: 'normal'});
      const next = Math.max(0, dy + {3: -2, 2: -1, 1: 1, 0: 2}[ent.dg]);
      if (next) { ch.conditions.dying = next; ent.ctx = {recovery: `Dying is now ${next}.`}; }
      else { delete ch.conditions.dying; ch.conditions.wounded = (ch.conditions.wounded || 0) + 1; ent.ctx = {recovery: 'No longer dying; you stay unconscious at 0 Hit Points until healed or you wake.'}; }
      commit(); return;
    }
    case 'dots': {
      const n = Number(d.n);
      if (d.k === 'hero') ch.heroPoints = ch.heroPoints === n ? n - 1 : n;
      else { const cur = res.focusMax - (ch.focusUsed || 0); ch.focusUsed = res.focusMax - (cur === n ? n - 1 : n); }
      commit(); return;
    }
    case 'cond': { const c = ch.conditions; c[d.k] = Math.max(0, (Number(c[d.k]) || 0) + Number(d.d)); if (!c[d.k]) delete c[d.k]; commit(); return; }
    case 'cond-off': delete ch.conditions[d.k]; commit(); return;
    case 'effect-off': delete ch.effects[d.k]; commit(); return;
    case 'effect-pick': pickEffect(); return;
    case 'breakdown': breakdown(d.k); return;
    case 'roll': rollKey(d.k); commit(); return;
    case 'strike': rollStrike(Number(d.i), Number(d.m)); commit(); return;
    case 'strike-dmg': case 'strike-crit': {
      const s = res.strikes[Number(d.i)]; if (!s) return;
      damageRoll(s.name + ' damage', strikeDamageParts(s, a === 'strike-crit'), a === 'strike-crit'); commit(); return;
    }
    case 'hero-reroll': {
      const x = (ch.log || []).find(l => l.id === d.id); if (!x || !(ch.heroPoints > 0)) return;
      ch.heroPoints -= 1; x.reroll = true;
      const ent = check(x.label, x.ctx.mod, {dc: x.dc, mode: 'normal', sub: x.sub, ctx: Object.assign({}, x.ctx)});
      ent.reroll = true;
      commit(); return;
    }
    case 'qroll': case 'froll': {
      const f = a === 'qroll' ? d.f : (document.getElementById('cs-formula').value || '').trim(); if (!f) return;
      const r = rollFormula(f); if (!r) { toast('Use a formula such as 2d6+4 or 1d20+7.'); return; }
      pushLog({kind: 'damage', label: f, parts: [{f, rolls: r.parts, sub: r.total, v: r.total, mult: 1}], total: r.total}); commit(); return;
    }
    case 'flat': check('Flat check', 0, {dc: Number(ch.target.dc) || 5, mode: 'normal'}); commit(); return;
    case 'log-clear': ch.log = []; commit(); return;
    case 'enc-start': ch.enc = {on: true, round: 1, actions: maxActions(), reaction: true, attacks: 0}; rollKey('initiative'); commit(); return;
    case 'enc-action': { const n = Number(d.n); ch.enc.actions = ch.enc.actions >= n ? n - 1 : n; commit(); return; }
    case 'enc-react': ch.enc.reaction = !ch.enc.reaction; commit(); return;
    case 'enc-end': endTurn(); commit(); return;
    case 'enc-stop': ch.enc = {on: false, round: 0, actions: 3, reaction: true, attacks: 0}; commit(); toast('Encounter ended.'); return;
    case 'rest-night': restNight(); commit(); return;
    case 'refocus': ch.focusUsed = Math.max(0, (ch.focusUsed || 0) - 1); commit(); toast('Regained 1 Focus Point.'); return;
    case 'spellstrike': ch.trackers.spellstrike = ch.trackers.spellstrike === false; commit(); return;
    case 'ss-pick': ssPick(Number(d.i)); return;
    case 'ss-recharge':
      ch.trackers.spellstrike = true;
      if (ch.enc.on) ch.enc.actions = Math.max(0, ch.enc.actions - 1);
      commit(); toast('Spellstrike recharged' + (ch.enc.on ? ' (1 action).' : '.')); return;
    case 'ss-dmg': {
      const x = (ch.log || []).find(l => l.id === d.id); if (!x || !x.ctx || !x.ctx.ss) return;
      const st = res.strikes[x.ctx.strike], sp = rec(x.ctx.ss.k); if (!st || !sp) return;
      const crit = !!d.crit;
      const parts = strikeDamageParts(st, crit).map(q => Object.assign(q, {from: st.name}))
        .concat(eng.spellDamage(sp, x.ctx.ss.rank).map(q => ({f: q.f, t: q.t, c: q.c, from: sp.n})));
      damageRoll(`Spellstrike: ${st.name} and ${sp.n}`, parts, crit); commit(); return;
    }
    case 'item': itemPanel(d.id); return;
    case 'use': { const used = ch.uses[d.k] || 0, n = Number(d.n); ch.uses[d.k] = used >= n ? n - 1 : n; commit(); return; }
    case 'block': {
      const n = Math.max(0, Number(document.getElementById('cs-block').value) || 0); if (!n) return;
      const sh = res.S.shield, left = Math.max(0, n - (sh.r.hard || 0));
      const inv = ch.inventory.find(i => i.id === sh.inv.id); inv.sdmg = Math.min(sh.r.hp || 0, (inv.sdmg || 0) + left);
      applyDamage(left); if (ch.enc.on) ch.enc.reaction = false;
      toast(`Blocked ${Math.min(n, sh.r.hard || 0)}; you and the shield each take ${left}.`); commit(); return;
    }
    case 'shield-repair': { const inv = ch.inventory.find(i => i.id === res.S.shield.inv.id); inv.sdmg = 0; commit(); return; }
    case 'consume': {
      const inv = ch.inventory.find(i => i.id === d.id); const r = eng.invRec(inv);
      inv.qty = Math.max(0, (inv.qty ?? 1) - 1);
      if (r.dmgf && r.dmgf.formula) {
        const heal = r.dmgf.kind === 'healing';
        const ent = damageRoll(r.n, [{f: r.dmgf.formula, t: r.dmgf.type, heal: heal ? 1 : 0}], false);
        if (heal) { applyHeal(ent.total); toast(`${r.n}: healed ${ent.total}.`); }
      } else toast('Used ' + r.n + '.');
      if (ch.enc.on) ch.enc.actions = Math.max(0, ch.enc.actions - 1);
      if (!inv.qty) ch.inventory = ch.inventory.filter(i => i.id !== inv.id);
      commit(); return;
    }
    case 'pick-origin': pickOrigin(d.k); return;
    case 'clear-deity': ch.deity = null; commit(); return;
    case 'pick-feat': pickFeat(d.s); return;
    case 'clear-feat': delete ch.feats[d.s]; commit(); return;
    case 'choice-pick': pickChoice(d.uid, d.flag); return;
    case 'boost': toggleBoost(d.k, d.a); return;
    case 'train': { const t = ch.trained; const i = t.indexOf(d.k); if (i >= 0) t.splice(i, 1); else t.push(d.k); commit(); return; }
    case 'lore-add': { const v = document.getElementById('cs-lore').value.trim(); if (v) { ch.lores.push(/lore$/i.test(v) ? v : v + ' Lore'); commit(); } return; }
    case 'lore-del': ch.lores.splice(Number(d.i), 1); commit(); return;
    case 'lang-add': { const v = document.getElementById('cs-lang').value.trim(); if (v) { ch.languages.push(v.toLowerCase()); commit(); } return; }
    case 'lang-del': ch.languages.splice(Number(d.i), 1); commit(); return;
    case 'bonus-slot': bonusSlot(); return;
    case 'bonus-del': { const i = ch.bonusSlots.findIndex(b => b.id === d.id); const s = i < 0 ? null : ch.bonusSlots.splice(i, 1)[0]; if (s) { delete ch.feats[s.id]; if (ch.bonusInc) delete ch.bonusInc[s.id]; } commit(); return; }
    case 'qty': { const inv = ch.inventory.find(i => i.id === d.id); inv.qty = Math.max(0, (inv.qty ?? 1) + Number(d.d)); commit(); return; }
    case 'remove': ch.inventory = ch.inventory.filter(i => i.id !== d.id); commit(); return;
    case 'sell': {
      const inv = ch.inventory.find(i => i.id === d.id); const r = eng.invRec(inv);
      const v = Math.floor((r.cp || 0) / 2);
      receive(v, 'Sold ' + (inv.name || r.n) + ' for half price');
      if ((inv.qty ?? 1) > 1) inv.qty -= 1; else ch.inventory = ch.inventory.filter(i => i.id !== d.id);
      commit(); toast('Sold for ' + money(v) + '.'); return;
    }
    case 'runes': runesPanel(d.id); return;
    case 'item-pick': itemBrowser(); return;
    case 'custom-item': customItem(); return;
    case 'money': {
      const amt = Number(document.getElementById('cs-mamt').value) || 0; if (!amt) return;
      const unit = document.getElementById('cs-munit').value, note = document.getElementById('cs-mnote').value.trim();
      const cp = Math.round(amt * {pp: 1000, gp: 100, sp: 10, cp: 1}[unit]);
      if (Number(d.d) < 0) { if (coinTotal(ch.coins) < cp) { toast('Not enough money.'); return; } spend(cp, note || 'Spent'); }
      else receive(cp, note || 'Received');
      commit(); return;
    }
    case 'spell-add': pickSpell(d.e, Number(d.max) || 1); return;
    case 'spell-del': { const x = EN(d.e); x.known = (x.known || []).filter(k => k !== d.k); commit(); return; }
    case 'spell-atk': {
      const sc = res.spellcasting.find(s => s.e.id === d.e); const s = rec(d.k);
      const pen = ch.enc.on ? [0, 5, 10][Math.min(ch.enc.attacks, 2)] : 0;
      const mod = sc.attack.total - pen;
      check(`${s.n}: spell attack${pen ? ' with multiple attack penalty' : ''}`, mod, {ctx: {spell: s.k, rank: Number(d.r), mod}});
      if (ch.enc.on) ch.enc.attacks += 1;
      commit(); return;
    }
    case 'spell-dmg': {
      const s = rec(d.k); const rank = Number(d.r) || s.lv || 1;
      const parts = eng.spellDamage(s, rank).map(x => ({f: x.f, t: x.t, c: x.c, heal: x.heal}));
      damageRoll(`${s.n}${rank !== s.lv ? ' at rank ' + rank : ''}`, parts, !!d.crit, d.basic ? {basic: true} : null); commit(); return;
    }
    case 'cast-prep': {
      const x = EN(d.e); x.used = x.used || {}; const arr = x.used[d.r] = x.used[d.r] || []; const i = Number(d.i);
      if (!arr.includes(i)) arr.push(i);
      spendSpellActions(d.k); toast('Cast ' + rec(d.k).n + '.'); commit(); return;
    }
    case 'uncast': { const x = EN(d.e); x.used[d.r] = (x.used[d.r] || []).filter(v => v !== Number(d.i)); commit(); return; }
    case 'cast-spont': {
      const x = EN(d.e); x.usedN = x.usedN || {}; const sc = res.spellcasting.find(s => s.e.id === d.e);
      x.usedN[d.r] = Math.min(sc.slots[d.r], (x.usedN[d.r] || 0) + 1);
      spendSpellActions(d.k); toast(`Cast ${rec(d.k).n} at rank ${d.r}.`); commit(); return;
    }
    case 'castn': { const x = EN(d.e); x.usedN = x.usedN || {}; x.usedN[d.r] = Math.max(0, (x.usedN[d.r] || 0) + Number(d.d)); commit(); return; }
    case 'cast-focus': {
      if (res.focusMax - (ch.focusUsed || 0) <= 0) { toast('No Focus Points left. Refocus to regain one.'); return; }
      ch.focusUsed = (ch.focusUsed || 0) + 1; spendSpellActions(d.k);
      const fs = rec(d.k), conflux = (fs.tr || []).includes('magus') && /^[123]/.test(fs.time || '') && res.S.opts.has('feature:spellstrike');
      if (conflux) ch.trackers.spellstrike = true;
      toast('Cast ' + fs.n + '.' + (conflux ? ' Conflux spell: Spellstrike recharged.' : '')); commit(); return;
    }
    case 'cast-innate': { const x = EN(d.e); x.innateUsed = x.innateUsed || {}; x.innateUsed[d.k] = (x.innateUsed[d.k] || 0) + 1; spendSpellActions(d.k); commit(); return; }
    case 'staff-cast': {
      const x = EN(d.e); const sc = res.spellcasting.find(s => s.e.id === d.e); const rk = Number(d.r);
      if (sc.charges.max - (x.used || 0) < rk) { toast('Not enough charges.'); return; }
      x.used = (x.used || 0) + rk; spendSpellActions(d.k); toast(`Cast ${rec(d.k).n} from the staff for ${rk} charge${rk > 1 ? 's' : ''}.`); commit(); return;
    }
    case 'staff-prep': EN(d.e).used = 0; commit(); toast('Staff prepared.'); return;
    case 'entry-add': {
      const kind = document.getElementById('cs-newkind').value, trad = document.getElementById('cs-newtrad').value, attr = document.getElementById('cs-newattr').value, table = document.getElementById('cs-newtable').value;
      const n = {id: newId(), name: cap(trad) + ' ' + (kind === 'staff' ? 'staff' : kind + ' spells'), trad, kind, attr, table: table || null, prof: 'class', known: [], prepared: {}, used: kind === 'staff' ? 0 : {}};
      if (kind === 'staff') { n.staff = []; n.extra = 0; }
      ch.spells.entries.push(n); commit(); return;
    }
    case 'entry-del':
      ch.spells.entries = ch.spells.entries.filter(x => x.id !== d.e);
      if (d.e.startsWith('arch:')) { ch.spells.dismissed = (ch.spells.dismissed || []).concat([d.e]); }
      commit(); return;
  }
}
function spendSpellActions(k) {
  const s = rec(k); if (!ch.enc.on || !s) return;
  if (/^[123]$/.test(s.time || '')) ch.enc.actions = Math.max(0, ch.enc.actions - Number(s.time));
  if (s.time === 'reaction') ch.enc.reaction = false;
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
  if (d.field === 'name') { ch.name = t.value.trim() || 'Unnamed'; commit(); return; }
  if (d.field === 'coin') { ch.coins[d.k] = Math.max(0, Math.floor(Number(t.value) || 0)); commit(); return; }
  if (d.field === 'note') { ch.notes[d.k] = t.value; putChar(ch); return; }
  if (d.field === 'ename') { ch.spells.entries.find(y => y.id === d.e).name = t.value; putChar(ch); return; }
  if (d.field === 'featlore') { const f = ch.feats[d.s]; if (f) { f.lore = t.value.trim(); commit(); } return; }
  if (d.field === 'target-dc') { ch.target.dc = t.value === '' ? null : Number(t.value); commit(); return; }
  const EN = id => ch.spells.entries.find(x => x.id === id);
  switch (d.act) {
    case 'switch': store.cur = t.value; saveStore(); ch = migrate(getChar(store.cur)); recompute(); render(); return;
    case 'import': importFile(t.files[0]); t.value = ''; return;
    case 'cond-add': if (t.value) { ch.conditions[t.value] = 1; commit(); } return;
    case 'effect': if (t.checked) addEffect(d.k); else delete ch.effects[d.k]; commit(); return;
    case 'toggle': ch.toggles[d.k] = t.checked; commit(); return;
    case 'rollmode': ch.rollMode = t.value; commit(); return;
    case 'choice': (ch.choices[d.uid] = ch.choices[d.uid] || {})[d.flag] = t.value || undefined; if (!t.value) delete ch.choices[d.uid][d.flag]; commit(); return;
    case 'opt': if (d.k === 'altBoosts') { ch.altBoosts = t.checked; ch.boosts.ancestry = []; } else ch.options[d.k] = t.checked; commit(); return;
    case 'inc': if (t.value) ch.increases[d.lv] = t.value; else delete ch.increases[d.lv]; commit(); return;
    case 'inc-b': ch.bonusInc = ch.bonusInc || {}; if (t.value) ch.bonusInc[d.s] = t.value; else delete ch.bonusInc[d.s]; commit(); return;
    case 'bonus-lv': editBonusSlot(d.id, {lv: t.value}); commit(); return;
    case 'bonus-kind': editBonusSlot(d.id, {kind: t.value}); commit(); return;
    case 'bonus-label': { const b = ch.bonusSlots.find(x => x.id === d.id); if (b) b.label = t.value.trim() || b.label; commit(); return; }
    case 'int-train': ch.intTrained[d.k] = t.value; commit(); return;
    case 'init': ch.initiative = t.value || null; commit(); return;
    case 'state': { const inv = ch.inventory.find(i => i.id === d.id); inv.eq = t.value; commit(); return; }
    case 'invest': {
      const inv = ch.inventory.find(i => i.id === d.id);
      if (t.checked && ch.inventory.filter(i => i.inv).length >= 10) { t.checked = false; toast('You can invest only 10 items.'); return; }
      inv.inv = t.checked; if (t.checked && (!inv.eq || inv.eq === 'stowed')) inv.eq = 'worn'; commit(); return;
    }
    case 'prep': { const x = EN(d.e); x.prepared = x.prepared || {}; const arr = x.prepared[d.r] = x.prepared[d.r] || []; arr[Number(d.i)] = t.value || null; commit(); return; }
    case 'etrad': EN(d.e).trad = t.value; commit(); return;
    case 'eattr': EN(d.e).attr = t.value; commit(); return;
    case 'staff-extra': EN(d.e).extra = Number(t.value) || 0; commit(); return;
  }
}
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
      const merged = migrate(Object.assign(blank(), c));
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
    let c;
    try { const r = await fetch('assets/cs/cyrus.json'); c = Object.assign(blank(), await r.json()); c.mig = 1; } catch (e) { c = blank(); }
    c.id = newId(); store.ids.push(c.id); putChar(migrate(c));
  }
  if (!store.ids.includes(store.cur)) store.cur = store.ids[0];
  saveStore();
  ch = migrate(getChar(store.cur));
  putChar(ch);
  recompute();
  render();
  el.addEventListener('click', onClick);
  el.addEventListener('change', onChange);
}
window.AsperaSheet = {init};
})();
