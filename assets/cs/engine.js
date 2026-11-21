/* Aspera character engine.
   Works out a Pathfinder 2e character's statistics from their build choices, using the rule elements of the Foundry PF2e
   system's data (FlatModifier, ActiveEffectLike, GrantItem, ChoiceSet, RollOption and others), applied the way that system
   applies them. Runs in the browser and in Node for tests. */
(function (root) {
'use strict';

const ATTRS = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
const ATTR_NAME = {str: 'Strength', dex: 'Dexterity', con: 'Constitution', int: 'Intelligence', wis: 'Wisdom', cha: 'Charisma'};
const SKILLS = {acrobatics: 'dex', arcana: 'int', athletics: 'str', crafting: 'int', deception: 'cha', diplomacy: 'cha', intimidation: 'cha',
  medicine: 'wis', nature: 'wis', occultism: 'int', performance: 'cha', religion: 'wis', society: 'int', stealth: 'dex', survival: 'wis', thievery: 'dex'};
const SAVES = {fortitude: 'con', reflex: 'dex', will: 'wis'};
const RANKS = ['Untrained', 'Trained', 'Expert', 'Master', 'Legendary'];
const WEAPON_CATS = ['simple', 'martial', 'advanced', 'unarmed'];
const ARMOR_CATS = ['unarmored', 'light', 'medium', 'heavy'];
const CASTING = {   // class: [tradition, kind, attribute]
  bard: ['occult', 'spontaneous', 'cha'], cleric: ['divine', 'prepared', 'wis'], druid: ['primal', 'prepared', 'wis'],
  magus: ['arcane', 'prepared', 'int'], oracle: ['divine', 'spontaneous', 'cha'], psychic: ['occult', 'spontaneous', 'int'],
  sorcerer: [null, 'spontaneous', 'cha'], summoner: [null, 'spontaneous', 'cha'], witch: [null, 'prepared', 'int'],
  wizard: ['arcane', 'prepared', 'int'], animist: ['divine', 'prepared', 'wis'], necromancer: ['occult', 'prepared', 'int'],
};
const AE_PRIORITY = {multiply: 10, add: 20, subtract: 20, remove: 20, downgrade: 30, upgrade: 40, override: 50};

const slugify = s => String(s || '').toLowerCase().replace(/[’']/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
const prof = (rank, level) => rank > 0 ? rank * 2 + level : 0;
const clone = o => JSON.parse(JSON.stringify(o));
const fmt = n => (n >= 0 ? '+' : '') + n;
function getProp(o, path) {
  if (o == null) return undefined;
  for (const p of String(path).split('.')) { if (o == null) return undefined; o = o[p]; }
  return o;
}
function setProp(o, path, v) {
  const ps = String(path).split('.');
  for (let i = 0; i < ps.length - 1; i++) { if (o[ps[i]] == null || typeof o[ps[i]] !== 'object') o[ps[i]] = {}; o = o[ps[i]]; }
  o[ps[ps.length - 1]] = v;
}

// ───────── predicates ─────────
function testPred(pred, opts) {
  if (pred == null) return true;
  if (!Array.isArray(pred)) pred = [pred];
  return pred.every(s => isTrue(s, opts));
}
function numVals(op, d) {
  const n = Number(op);
  if (!Number.isNaN(n)) return [n];
  const out = [], pre = op + ':';
  for (const s of d) if (s.startsWith(pre)) { const rest = s.slice(pre.length); if (!rest.includes(':')) { const v = Number(rest); if (!Number.isNaN(v)) out.push(v); } }
  return out.length ? out : [NaN];
}
function isTrue(s, d) {
  if (typeof s === 'string') return d.has(s);
  if (!s || typeof s !== 'object') return false;
  if ('and' in s) return s.and.every(x => isTrue(x, d));
  if ('or' in s) return s.or.some(x => isTrue(x, d));
  if ('nand' in s) return !s.nand.every(x => isTrue(x, d));
  if ('nor' in s) return !s.nor.some(x => isTrue(x, d));
  if ('not' in s) return !isTrue(s.not, d);
  if ('xor' in s) return s.xor.filter(x => isTrue(x, d)).length === 1;
  if ('if' in s) return !(isTrue(s.if, d) && !isTrue(s.then, d));
  if ('iff' in s) return s.iff.every(x => isTrue(x, d)) || s.iff.every(x => !isTrue(x, d));
  if ('eq' in s) return typeof s.eq[1] === 'string' ? s.eq[0] === s.eq[1] : d.has(`${s.eq[0]}:${s.eq[1]}`);
  for (const op of ['gt', 'gte', 'lt', 'lte']) if (op in s) {
    const L = numVals(s[op][0], d), R = numVals(s[op][1], d);
    const f = {gt: (a, b) => a > b, gte: (a, b) => a >= b, lt: (a, b) => a < b, lte: (a, b) => a <= b}[op];
    return L.some(l => R.every(r => f(l, r)));
  }
  return false;
}
// a predicate that refers to the target, to the roll itself or to a toggle that isn't set can't be known in advance
function situational(pred) {
  const t = JSON.stringify(pred || []);
  return /"(target|origin|item:proficiency|check:|outcome|damaging-effect|action:|ranged|melee|attack|spellshape|area-effect)[:"]/.test(t);
}

// ───────── formulas ─────────
const FN = {
  ternary: (c, a, b) => c ? a : b, max: Math.max, min: Math.min, floor: Math.floor, ceil: Math.ceil, abs: Math.abs, round: Math.round,
  gte: (a, b) => a >= b, gt: (a, b) => a > b, lte: (a, b) => a <= b, lt: (a, b) => a < b, eq: (a, b) => a === b, ne: (a, b) => a !== b,
  sign: Math.sign, trunc: Math.trunc,
};
function evalFormula(expr) {
  const src = String(expr).replace(/\s+/g, ' ');
  if (!/^[0-9+\-*/()., a-z<>=!&|?:]*$/i.test(src)) return NaN;
  const names = src.match(/[a-z_]+/gi) || [];
  if (names.some(n => !(n in FN) && n !== 'true' && n !== 'false')) return NaN;
  try { return Function(...Object.keys(FN), '"use strict"; return (' + src + ');')(...Object.values(FN)); } catch (e) { return NaN; }
}

// ───────── item roll options ─────────
function itemOptions(r, prefix = 'item', extra) {
  const o = [`${prefix}:${r.sl}`, `${prefix}:slug:${r.sl}`, `${prefix}:type:${r.t}`];
  if (r.lv != null) o.push(`${prefix}:level:${r.lv}`);
  for (const t of r.tr || []) o.push(`${prefix}:trait:${t}`);
  for (const t of r.tags || []) o.push(`${prefix}:tag:${t}`);
  o.push(`${prefix}:rarity:${r.rar || 'common'}`);
  if (r.cat) o.push(`${prefix}:category:${r.cat}`);
  if (r.grp) o.push(`${prefix}:group:${r.grp}`);
  if (r.base) o.push(`${prefix}:base:${r.base}`);
  if (r.t === 'spell') { o.push(`${prefix}:rank:${r.lv}`); for (const t of r.trad || []) o.push(`${prefix}:trait:${t}`); }
  if (extra) o.push(...extra);
  return o;
}
const effectSlug = sl => sl.replace(/^(?:[a-z]+-)?(?:effect|stance)-/, '');

// ───────── the engine ─────────
class Engine {
  constructor(db) { this.db = db; this.lang = db.lang || {}; }
  rec(k) { if (!k) return null; if (k[0] === '@') k = k.slice(1); return this.db.e[k] || null; }
  // an inventory entry: a catalogue item, or a custom item (such as a relic) described in the entry itself
  invRec(inv) {
    if (!inv) return null;
    if (inv.custom) {
      const c = inv.custom;
      const r = Object.assign({k: 'custom:' + inv.id, sl: slugify(c.n || 'item'), t: 'equipment', tr: [], bulk: 0, cp: 0}, c);
      if (c.relic && this.level) r.lv = this.level;      // a relic's level always matches its owner's (GM Core)
      return r;
    }
    return this.rec(inv.k);
  }
  t(s) { return (typeof s === 'string' && this.lang[s]) || s; }

  compute(ch) {
    const db = this.db;
    const S = {ch, level: Math.max(1, Math.min(20, ch.level || 1)), items: [], byUid: {}, opts: new Set(), sys: {}, pending: [], warnings: [],
      mods: [], adjust: [], notes: [], dice: [], strikesRE: [], resist: [], weak: [], immune: [], senses: [], speeds: {}, toggles: [], effects: [],
      martial: [], dexCaps: [], tempHP: [], rollTwice: [], degree: [], critSpec: [], languagesGranted: [], actions: []};
    const L = S.level;
    this.S = S; this.level = L;
    const cls = this.rec(ch.class), anc = this.rec(ch.ancestry), her = this.rec(ch.heritage), bg = this.rec(ch.background), dei = this.rec(ch.deity);
    S.cls = cls; S.anc = anc; S.her = her; S.bg = bg; S.dei = dei;

    // base actor data, before rule elements
    const sys = S.sys = {
      skills: {}, saves: {}, perception: {rank: cls ? cls.perc : 0},
      proficiencies: {attacks: {}, defenses: {}, spellcasting: {rank: cls && cls.sc ? 1 : 0}, classDCs: {}},
      attributes: {ancestryhp: anc ? anc.hp : 0, classhp: cls ? cls.hp : 0, dying: {recoveryDC: 10, max: 4}, speed: {value: anc ? anc.speed : 25}},
      resources: {focus: {max: 0, cap: 3}, heroPoints: {max: 3}, investiture: {max: 10}},
      build: {languages: {value: 0, max: 0, granted: []}}, details: {class: cls ? {trait: cls.sl, slug: cls.sl} : {}, level: {value: L}},
      traits: {size: anc ? anc.size : 'med', value: []},
    };
    S.flags = {system: {rulesSelections: {}}};
    for (const s in SKILLS) sys.skills[s] = {rank: 0};
    for (const s in SAVES) sys.saves[s] = {rank: cls ? cls.saves[s] : 0};
    for (const c of WEAPON_CATS) sys.proficiencies.attacks[c] = {rank: cls ? (cls.atk[c] || 0) : 0};
    for (const c of ARMOR_CATS) sys.proficiencies.defenses[c] = {rank: cls ? (cls.dfn[c] || 0) : 0};
    if (cls) sys.proficiencies.classDCs[cls.sl] = {rank: 1, attribute: ch.boosts && ch.boosts.class || cls.key[0] || 'int', primary: true};
    if (cls && cls.atk.other && cls.atk.other.rank && cls.atk.other.name) S.warnings.push('Class proficiency in ' + cls.atk.other.name + ' is not applied automatically.');

    // attributes from boosts
    this.attributes(S);

    // skills from class, background and choices
    this.skillRanks(S);

    // actor roll options from the build itself
    const O = S.opts;
    O.add(`self:level:${L}`);
    if (cls) { O.add(`class:${cls.sl}`); O.add(`self:class:${cls.sl}`); }
    if (anc) { O.add(`ancestry:${anc.sl}`); for (const t of anc.tr || []) { O.add(`self:trait:${t}`); sys.traits.value.push(t); } }
    if (her) { O.add(`heritage:${her.sl}`); for (const t of her.tr || []) { O.add(`self:trait:${t}`); sys.traits.value.push(t); } }
    if (bg) O.add(`background:${bg.sl}`);
    if (dei) { O.add(`deity:primary:${dei.sl}`); O.add(`deity:${dei.sl}`); }
    for (const [k, v] of Object.entries(ch.toggles || {})) if (v === true) O.add(k); else if (typeof v === 'string' && v) { O.add(k); O.add(`${k}:${v}`); }
    for (const [k, v] of Object.entries(ch.conditions || {})) if (v) { O.add(`self:condition:${k}`); if (typeof v === 'number') O.add(`self:condition:${k}:${v}`); }

    // items: build, feats, inventory, effects; grant and choice rule elements are followed as items are added
    this.collect(S);

    // equipment roll options
    this.equipmentOptions(S);

    // active-effect-like changes, in priority order
    this.applyAE(S);
    this.replaySkills(S);
    sys.attributes.speed.value = sys.attributes.speed.value || 25;
    // numeric roll options after proficiency changes
    this.numericOptions(S);

    // everything else: modifiers and other synthetics
    for (const it of S.items) this.applySynthetics(S, it);

    return this.statistics(S);
  }

  // ───── attributes ─────
  attributes(S) {
    const ch = S.ch, b = ch.boosts || {}, A = {};
    for (const a of ATTRS) A[a] = 0;
    const boost = a => { if (A[a] == null) return; A[a] += A[a] >= 4 ? 0.5 : 1; };
    const L = S.level;
    S.boostInfo = {};
    if (ch.manualAttributes) { for (const a of ATTRS) A[a] = Number(ch.manualAttributes[a]) || 0; }
    else {
      const anc = S.anc;
      if (anc) {
        if (ch.altBoosts) (b.ancestry || []).slice(0, 2).forEach(boost);
        else {
          const fixed = anc.boosts.filter(o => o.length === 1).map(o => o[0]);
          fixed.forEach(boost);
          (b.ancestry || []).forEach(boost);
          anc.flaws.filter(o => o.length === 1).forEach(o => { A[o[0]] -= 1; });
          (b.flaws || []).forEach(a => { A[a] -= 1; });
        }
      }
      (b.background || []).forEach(boost);
      if (b.class) boost(b.class);
      for (const lv of [1, 5, 10, 15, 20]) if (L >= lv) (b[lv] || []).slice(0, 4).forEach(boost);
    }
    S.attr = {};
    for (const a of ATTRS) S.attr[a] = {mod: A[a], base: Math.trunc(A[a])};
  }

  // ───── skill ranks from the build ─────
  skillRanks(S) {
    const ch = S.ch, sys = S.sys, L = S.level;
    const up = (s, r) => { if (!sys.skills[s]) sys.skills[s] = {rank: 0, lore: true}; sys.skills[s].rank = Math.max(sys.skills[s].rank, r); };
    S.loreNames = {};
    const addLore = name => { const k = slugify(name); if (!k) return null; S.loreNames[k] = name; up(k, 1); sys.skills[k].lore = true; return k; };
    if (S.cls) for (const s of S.cls.skills.value || []) up(s, 1);
    if (S.bg) { for (const s of S.bg.skills.value || []) up(s, 1); for (const l of S.bg.skills.lore || []) addLore(l); }
    for (const s of ch.trained || []) { if (SKILLS[s]) up(s, 1); else addLore(s); }
    for (const l of ch.lores || []) addLore(l);
    const inc = ch.increases || {};
    S.skillBase = {}; S.skillInc = [];
    for (const [k, v] of Object.entries(sys.skills)) S.skillBase[k] = v.rank;
    // class skill increases are keyed by level; bonus increases come from bonus slots of kind 'increase'
    const incList = Object.keys(inc).map(Number).map(lv => ({lv, s: inc[lv], id: 'inc-' + lv}))
      .concat((ch.bonusSlots || []).filter(b => b.kind === 'increase').map(b => ({lv: b.lv, s: (ch.bonusInc || {})[b.id], id: b.id, bonus: true})))
      .sort((a, b) => a.lv - b.lv || (a.bonus ? 1 : 0) - (b.bonus ? 1 : 0));
    for (const {lv, s, id} of incList) {
      if (lv > L) continue;
      if (!s) continue;
      const k = SKILLS[s] ? s : (S.loreNames[s] ? s : addLore(s));
      if (!k) continue;
      if (!(k in S.skillBase)) S.skillBase[k] = 0;
      const cap = lv >= 15 ? 4 : lv >= 7 ? 3 : 2;
      S.skillInc.push({k, lv, cap, id});
      sys.skills[k].rank = Math.min(Math.max(sys.skills[k].rank, 0) + 1, cap);
    }
    for (const [lv, s] of Object.entries(ch.intTrained || {})) if (s) { if (SKILLS[s]) up(s, 1); else addLore(s); }
    // Additional Lore: trained in the chosen Lore, rising to expert at 3rd level, master at 7th and legendary at 15th
    for (const [id, f] of Object.entries(ch.feats || {})) {
      if (!f || f.k !== 'ft:additional-lore' || !f.lore) continue;
      const lv = Number(id.split('-').pop()) || 1;
      if (lv > L) continue;
      const k = addLore(/lore$/i.test(f.lore) ? f.lore : f.lore + ' Lore');
      if (k) sys.skills[k].rank = Math.max(sys.skills[k].rank, L >= 15 ? 4 : L >= 7 ? 3 : L >= 3 ? 2 : 1);
    }
  }

  // ───── item collection ─────
  addItem(S, r, uid, extra = {}) {
    if (!r || S.byUid[uid]) return null;
    const it = Object.assign({uid, r, sel: (S.ch.choices || {})[uid] || {}, lvl: extra.lvl || r.lv || 1}, extra);
    S.byUid[uid] = it;
    S.items.push(it);
    const O = S.opts;
    if (r.t === 'feat') {
      const cat = r.cat;
      if (cat === 'classfeature' || cat === 'ancestryfeature') O.add(`feature:${r.sl}`);
      else O.add(`feat:${r.sl}`);
      if (r.sub && r.sub.proficiencies) this.subfeatures(S, r.sub.proficiencies);
      if (r.sub && r.sub.senses) for (const [k, v] of Object.entries(r.sub.senses)) S.senses.push({type: k, ...v, from: r.n});
      if (r.sub && r.sub.keyOptions) S.keyOptions = r.sub.keyOptions;
      if (r.sub && r.sub.languages) S.languagesGranted.push(...((r.sub.languages.granted) || []));
    }
    if (r.t === 'effect' || r.t === 'condition') O.add(`self:${r.t === 'condition' ? 'condition' : 'effect'}:${effectSlug(r.sl)}`);
    if (r.t === 'action' || (r.t === 'feat' && r.act)) S.actions.push(it);
    if (r.se) S.toggles.push({key: r.se, from: it});
    this.processGrants(S, it);
    return it;
  }
  subfeatures(S, p) {
    const sys = S.sys;
    for (const [k, v] of Object.entries(p)) {
      const rank = v.rank || 0;
      if (k === 'perception') sys.perception.rank = Math.max(sys.perception.rank, rank);
      else if (SAVES[k]) sys.saves[k].rank = Math.max(sys.saves[k].rank, rank);
      else if (WEAPON_CATS.includes(k)) sys.proficiencies.attacks[k].rank = Math.max(sys.proficiencies.attacks[k].rank, rank);
      else if (ARMOR_CATS.includes(k)) sys.proficiencies.defenses[k].rank = Math.max(sys.proficiencies.defenses[k].rank, rank);
      else if (k === 'spellcasting') sys.proficiencies.spellcasting.rank = Math.max(sys.proficiencies.spellcasting.rank, rank);
      else {
        const c = sys.proficiencies.classDCs[k] || (sys.proficiencies.classDCs[k] = {rank: 0, attribute: v.attribute || null});
        c.rank = Math.max(c.rank, rank);
        if (v.attribute) c.attribute = v.attribute;
      }
    }
  }
  itemCtx(S, it) {
    const r = it.r;
    const sel = it.sel || {};
    return {id: it.uid, _id: it.uid, name: r.n, slug: r.sl, level: it.lvl, badge: {value: it.badge || 1}, timesTaken: 1,
      flags: {system: {rulesSelections: sel}, pf2e: {rulesSelections: sel}}, system: {level: {value: it.lvl}, runes: (it.inv && it.inv.runes) || r.runes || {}},
      origin: null, isOfType: () => false};
  }
  inject(S, v, it) {
    if (typeof v !== 'string' || !v.includes('{')) return v;
    return v.replace(/\{(actor|item|rule)\|([^}]+)\}/g, (m, who, path) => {
      let val;
      if (who === 'item') val = getProp(this.itemCtx(S, it), path);
      else if (who === 'actor') val = this.actorProp(S, path);
      return val == null ? m : String(val);
    });
  }
  actorProp(S, path) {
    const p = path.replace(/^system\./, '');
    if (p === 'level') return S.level;
    if (p.startsWith('details.class.trait') || p === 'class.slug') return S.cls ? S.cls.sl : '';
    if (p.startsWith('abilities.') || p.startsWith('attributes.') && /^(attributes)\.(str|dex|con|int|wis|cha)/.test(p)) {
      const m = p.match(/(str|dex|con|int|wis|cha)\.mod/); if (m) return S.attr[m[1]].mod;
    }
    if (p.startsWith('flags.')) return getProp(S.flags, p.slice(6));
    const v = getProp(S.sys, p);
    return v;
  }
  resolve(S, v, it, def = 0, extra) {
    if (v == null) return def;
    if (typeof v === 'number' || typeof v === 'boolean') return v;
    if (typeof v === 'object' && !Array.isArray(v)) {
      if (Array.isArray(v.brackets)) {
        const f = v.field || 'actor|level';
        const [who, path] = f.split('|');
        const x = who === 'item' ? getProp(this.itemCtx(S, it), path) : who === 'actor' ? this.actorProp(S, path) : S.level;
        const n = Number(x);
        const b = v.brackets.find(b => (b.start == null || n >= b.start) && (b.end == null || n <= b.end));
        return b ? this.resolve(S, b.value, it, def, extra) : def;
      }
      return v;
    }
    if (typeof v !== 'string') return v;
    let s = this.inject(S, v.trim(), it);
    if (/^-?\d+(\.\d+)?$/.test(s)) return Number(s);
    if (!s.includes('@')) return s;
    let bad = false;
    s = s.replace(/@([a-zA-Z_][\w.]*)/g, (m, path) => {
      let val;
      if (path.startsWith('actor.')) {
        const p = path.slice(6);
        if (p === 'level') val = S.level;
        else if (/^(system\.)?abilities\.(\w+)\.mod$/.test(p)) val = S.attr[p.match(/abilities\.(\w+)\.mod/)[1]].mod;
        else if (p.startsWith('conditions.')) { const c = p.split('.')[1]; val = (S.ch.conditions || {})[c] || 0; }
        else if (p.startsWith('flags.')) val = getProp(S.flags, p.slice(6));
        else val = getProp({system: S.sys}, p.startsWith('system.') ? p : 'system.' + p);
        if (val && typeof val === 'object' && 'value' in val) val = val.value;
      } else if (path.startsWith('item.')) {
        val = getProp(this.itemCtx(S, it), path.slice(5));
        if (path === 'item.level') val = it.lvl;
      } else if (extra && path.split('.')[0] in extra) {
        val = getProp(extra, path);
      } else if (path.startsWith('armor.')) {
        const a = S.armor; val = a ? getProp({system: {runes: a.runes || {}, acBonus: a.r.ac}}, path.slice(6)) : 0;
      }
      if (val == null || typeof val === 'object') { bad = true; return '0'; }
      return typeof val === 'boolean' ? String(val) : String(val);
    });
    if (bad) return def;
    const n = evalFormula(s);
    return Number.isNaN(n) ? def : n;
  }

  processGrants(S, it) {
    for (const [i, rule] of (it.r.rules || []).entries()) {
      if (rule.key === 'ChoiceSet') this.choiceSet(S, it, rule, i);
      else if (rule.key === 'GrantItem') {
        if (rule.predicate && !testPred(this.injectDeep(S, rule.predicate, it), S.opts)) continue;
        const u = this.inject(S, rule.uuid, it);
        const g = this.rec(u);
        if (!g) { if (/\{/.test(u) === false && u && !u.startsWith('@')) {} continue; }
        const uid = it.uid + '>' + g.k;
        if (!rule.allowDuplicate && S.items.some(x => x.r.k === g.k && x.r.t !== 'effect' && x.r.t !== 'condition')) continue;
        this.addItem(S, g, uid, {parent: it.uid, granted: true, lvl: it.lvl});
      }
    }
  }
  injectDeep(S, v, it) {
    if (typeof v === 'string') return this.inject(S, v, it);
    if (Array.isArray(v)) return v.map(x => this.injectDeep(S, x, it));
    if (v && typeof v === 'object') { const o = {}; for (const k in v) o[k] = this.injectDeep(S, v[k], it); return o; }
    return v;
  }
  choiceSet(S, it, rule, i) {
    if (rule.predicate && !testPred(this.injectDeep(S, rule.predicate, it), S.opts)) return;
    const flag = rule.flag || slugify(it.r.n).replace(/-([a-z])/g, (m, c) => c.toUpperCase());
    let val = it.sel[flag];
    if (val == null && rule.selection != null) val = rule.selection;
    const entry = {uid: it.uid, item: it, flag, rule, index: i, value: val ?? null, prompt: (() => { const t = this.t(rule.prompt); return t && !/^PF2E\./.test(t) ? t : 'Choose an option for ' + it.r.n; })()};
    S.pending.push(entry);
    if (val == null) return;
    if (rule.actorFlag) setProp(S.flags, `system.${flag}`, val);
    if (rule.rollOption) { S.opts.add(rule.rollOption); S.opts.add(`${rule.rollOption}:${typeof val === 'string' ? val.replace(/^@\w+:/, '') : val}`); }
    // a selection that is a feat or item is reflected in roll options for predicates that test it
    const r = typeof val === 'string' ? this.rec(val) : null;
    if (r && r.t === 'feat') { /* granted separately by a GrantItem rule */ }
  }
  // the options a ChoiceSet offers, for the builder
  choices(S, entry) {
    const rule = entry.rule, it = entry.item, ch = rule.choices, out = [];
    const O = S.opts;
    if (Array.isArray(ch)) {
      for (const c of ch) {
        if (c.predicate && !testPred(this.injectDeep(S, c.predicate, it), O)) continue;
        const v = this.injectDeep(S, c.value, it);
        const rr = typeof v === 'string' ? this.rec(v) : null;
        out.push({value: v, label: rr ? rr.n : this.t(this.inject(S, c.label || String(v), it)), rec: rr});
      }
    } else if (ch && typeof ch === 'object' && ch.filter) {
      const filt = this.injectDeep(S, ch.filter, it);
      const type = ch.itemType || 'feat';
      const actor = [...O];
      for (const r of Object.values(this.db.e)) {
        if (r.t !== type && !(type === 'feat' && r.t === 'feat')) continue;
        if (type === 'feat' && r.t !== 'feat') continue;
        const d = new Set(actor.concat(itemOptions(r)));
        if (!testPred(filt, d)) continue;
        out.push({value: ch.slugsAsValues ? r.sl : '@' + r.k, label: r.n, rec: r});
      }
      out.sort((a, b) => a.label.localeCompare(b.label));
    } else if (ch && typeof ch === 'object' && ch.config) {
      const cfg = ch.config;
      const list = cfg === 'skills' ? Object.keys(SKILLS) : cfg === 'saves' ? Object.keys(SAVES) : cfg === 'attributes' ? ATTRS : [];
      for (const v of list) {
        if (ch.predicate) { const p = this.injectDeep(S, JSON.parse(JSON.stringify(ch.predicate).replace(/\{choice\|value\}/g, v)), it); if (!testPred(p, O)) continue; }
        out.push({value: v, label: v.replace(/^\w/, c => c.toUpperCase())});
      }
    } else if (ch && typeof ch === 'object' && ch.ownedItems) {
      for (const inv of S.ch.inventory || []) {
        const r = this.invRec(inv); if (!r || !(ch.types || []).includes(r.t)) continue;
        out.push({value: inv.id, label: inv.name || r.n});
      }
    } else if (ch === 'weaponGroups') {
      for (const g of ['axe', 'bomb', 'bow', 'brawling', 'club', 'crossbow', 'dart', 'firearm', 'flail', 'hammer', 'knife', 'pick', 'polearm', 'shield', 'sling', 'spear', 'sword'])
        out.push({value: g, label: g.replace(/^\w/, c => c.toUpperCase())});
    }
    return out;
  }

  collect(S) {
    const ch = S.ch, L = S.level;
    const roots = [];
    if (S.anc) roots.push(['ancestry', S.anc]);
    if (S.her) roots.push(['heritage', S.her]);
    if (S.bg) roots.push(['background', S.bg]);
    if (S.cls) roots.push(['class', S.cls]);
    if (S.dei) roots.push(['deity', S.dei]);
    for (const [uid, r] of roots) this.addItem(S, r, uid, {lvl: 1});
    if (S.anc) for (const k of S.anc.items || []) this.addItem(S, this.rec(k), 'ancestry>' + k, {lvl: 1});
    if (S.bg) for (const k of S.bg.items || []) this.addItem(S, this.rec(k), 'background>' + k, {lvl: 1});
    if (S.cls) for (const [lv, k] of S.cls.items) if (lv <= L) this.addItem(S, this.rec(k), 'class>' + k, {lvl: lv});
    // feats in their slots, lowest level first so that prerequisites granted earlier are present
    const slots = Object.entries(ch.feats || {}).map(([id, f]) => [id, f, Number(id.split('-').pop()) || 1]).sort((a, b) => a[2] - b[2]);
    for (const [id, f, lv] of slots) if (lv <= L && f && f.k) this.addItem(S, this.rec(f.k), 'feat:' + id, {lvl: lv, slot: id});
    // inventory items with rules apply when equipped and, if they need it, invested
    for (const inv of ch.inventory || []) {
      const r = this.invRec(inv); if (!r) continue;
      const it = {uid: 'inv:' + inv.id, r, inv, sel: (ch.choices || {})['inv:' + inv.id] || {}, lvl: r.lv || 0};
      S.byUid[it.uid] = it;
      if (!this.itemActive(r, inv)) continue;
      S.items.push(it);
      this.processGrants(S, it);
    }
    // effects and conditions switched on in the sheet
    for (const [k, v] of Object.entries(ch.effects || {})) {
      if (!v) continue;
      const r = this.rec(k); if (!r) continue;
      this.addItem(S, r, 'effect:' + k, {badge: typeof v === 'number' ? v : (v.badge || 1), lvl: (v && v.lvl) || S.level});
    }
    const bk = this.bulk(S);
    S.autoEncumbered = false;
    if (bk.value > bk.encumbered && !(ch.conditions || {}).encumbered) {
      S.autoEncumbered = true;
      this.addItem(S, this.rec('co:encumbered'), 'cond:encumbered-auto', {badge: 1});
    }
    for (const [k, v] of Object.entries(ch.conditions || {})) {
      if (!v) continue;
      const r = this.rec('co:' + k); if (!r) continue;
      this.addItem(S, r, 'cond:' + k, {badge: typeof v === 'number' ? v : 1});
    }
    // granted items whose predicates depended on later items: one more pass
    for (const it of S.items.slice()) {
      for (const rule of it.r.rules || []) {
        if (rule.key !== 'GrantItem' || !rule.predicate) continue;
        if (!testPred(this.injectDeep(S, rule.predicate, it), S.opts)) continue;
        const g = this.rec(this.inject(S, rule.uuid, it));
        if (!g) continue;
        if (!rule.allowDuplicate && S.items.some(x => x.r.k === g.k)) continue;
        this.addItem(S, g, it.uid + '>' + g.k, {parent: it.uid, granted: true, lvl: it.lvl});
      }
    }
  }
  itemActive(r, inv) {
    const st = inv.eq || 'stowed';
    if (inv.qty === 0) return false;
    const invested = (r.tr || []).includes('invested');
    if (invested && !inv.inv) return false;
    if (r.t === 'armor') return st === 'worn';
    if (r.t === 'weapon' || r.t === 'shield') return st === 'held1' || st === 'held2' || st === 'worn';
    if (r.t === 'consumable' || r.t === 'treasure') return false;
    const use = r.use || '';
    if (use.startsWith('worn')) return st === 'worn' || invested;
    if (use.startsWith('held')) return st === 'held1' || st === 'held2';
    if (use.startsWith('affixed') || use.startsWith('attached') || use.startsWith('etched')) return st !== 'dropped';
    return st === 'worn' || st === 'held1' || st === 'held2';
  }

  equipmentOptions(S) {
    const O = S.opts, ch = S.ch;
    let armor = null, shield = null, hands = 0, reallyHands = 0;
    for (const inv of ch.inventory || []) {
      const r = this.invRec(inv); if (!r) continue;
      const st = inv.eq || 'stowed';
      if (r.t === 'armor' && st === 'worn' && (!armor || r.cat !== 'unarmored')) armor = {r, inv, runes: Object.assign({potency: 0, resilient: 0, property: []}, r.runes || {}, inv.runes || {})};
      if (r.t === 'shield' && (st === 'held1' || st === 'held2')) shield = {r, inv};
      const h = st === 'held2' ? 2 : st === 'held1' ? 1 : 0;
      reallyHands += h;
      if (r.t !== 'shield' && !(r.tr || []).includes('free-hand')) hands += h;
    }
    S.armor = armor; S.shield = shield;
    if (armor) {
      O.add('self:armored');
      for (const o of itemOptions(armor.r, 'armor')) O.add(o);
      if (armor.r.cat === 'unarmored') O.delete('self:armored');
      if (typeof armor.r.str === 'number' && S.attr.str.mod >= armor.r.str) O.add('armor:strength-requirement-met');
    }
    if (shield) { O.add('self:shield:equipped'); if ((ch.toggles || {})['shield-raised']) O.add('self:shield:raised'); }
    S.handsFree = Math.max(0, 2 - hands); S.handsReallyFree = Math.max(0, 2 - reallyHands);
  }

  applyAE(S) {
    const list = [];
    for (const it of S.items) for (const rule of it.r.rules || []) {
      if (rule.key !== 'ActiveEffectLike') continue;
      list.push({it, rule, pr: rule.priority ?? AE_PRIORITY[rule.mode] ?? 50});
    }
    list.sort((a, b) => a.pr - b.pr);
    for (const {it, rule} of list) {
      if (rule.predicate && !testPred(this.injectDeep(S, rule.predicate, it), S.opts)) continue;
      let path = this.inject(S, rule.path, it);
      if (/\{/.test(path)) continue;
      let target, p;
      if (path.startsWith('system.')) { target = S.sys; p = path.slice(7); }
      else if (path.startsWith('flags.')) { target = S.flags; p = path.slice(6); }
      else continue;
      const v = this.resolve(S, rule.value, it, null);
      if (v == null) continue;
      // proficiency paths for skills that don't exist yet (lore) and for other weapon or armour groupings
      if (/^skills\.[\w-]+\.rank$/.test(p) && !getProp(target, p.replace(/\.rank$/, ''))) setProp(target, p.replace(/\.rank$/, ''), {rank: 0, lore: !SKILLS[p.split('.')[1]]});
      if (/^proficiencies\.attacks\.[\w-]+\.rank$/.test(p) && !getProp(target, p.replace(/\.rank$/, ''))) setProp(target, p.replace(/\.rank$/, ''), {rank: 0, custom: true});
      const cur = getProp(target, p);
      // skill ranks granted by the build at a given level (Skill Mastery, Canny Acumen and the like)
      const sm = p.match(/^skills\.([\w-]+)\.rank$/);
      if (sm && rule.mode === 'upgrade' && target === S.sys && !/^(effect:|cond:|inv:)/.test(it.uid)) (S.skillUps = S.skillUps || []).push({k: sm[1], lv: it.lvl || 1, v: Number(v)});
      let nv = cur;
      switch (rule.mode) {
        case 'add': nv = Array.isArray(cur) ? cur.concat([v]) : (Number(cur) || 0) + Number(v); break;
        case 'subtract': nv = (Number(cur) || 0) - Number(v); break;
        case 'multiply': nv = (Number(cur) || 0) * Number(v); break;
        case 'upgrade': nv = Math.max(Number(cur) || 0, Number(v)); break;
        case 'downgrade': nv = Math.min(cur == null ? Infinity : Number(cur), Number(v)); break;
        case 'override': nv = v; break;
        case 'remove': nv = Array.isArray(cur) ? cur.filter(x => x !== v) : cur; break;
      }
      setProp(target, p, nv);
      if (p.startsWith('build.languages.granted') && Array.isArray(nv)) S.languagesGranted = S.languagesGranted.concat(nv.map(x => (x && x.slug) || x));
    }
  }

  // Skill increases add one rank to whatever the skill is at that level, so a rank a feat grants
  // earlier (Skill Mastery at 9) must count before a later increase (13). Replay both in level order.
  replaySkills(S) {
    const ups = S.skillUps || [];
    S.wastedInc = [];
    for (const k of new Set(ups.map(u => u.k).concat((S.skillInc || []).map(i => i.k)))) {
      const ev = ups.filter(u => u.k === k).map(u => ({lv: u.lv, up: u.v}))
        .concat((S.skillInc || []).filter(i => i.k === k).map(i => ({lv: i.lv, inc: true, cap: i.cap, id: i.id})))
        .sort((a, b) => a.lv - b.lv || (a.inc ? 1 : 0) - (b.inc ? 1 : 0));
      let r = (S.skillBase || {})[k] || 0;
      for (const e of ev) {
        if (e.inc && r >= e.cap) S.wastedInc.push({lv: e.lv, k, rank: r, cap: e.cap, id: e.id});
        r = e.inc ? Math.min(r + 1, e.cap) : Math.max(r, e.up);
      }
      const sk = S.sys.skills[k];
      if (sk) sk.rank = Math.max(sk.rank, r);
    }
  }

  numericOptions(S) {
    const O = S.opts, sys = S.sys;
    O.add(`perception:rank:${sys.perception.rank}`);
    for (const a of ATTRS) O.add(`attribute:${a}:mod:${Math.trunc(S.attr[a].mod)}`);
    for (const [k, v] of Object.entries(sys.skills)) O.add(`skill:${k}:rank:${v.rank}`);
    for (const c of WEAPON_CATS) O.add(`attack:${c}:rank:${sys.proficiencies.attacks[c].rank}`);
    for (const c of ARMOR_CATS) O.add(`defense:${c}:rank:${sys.proficiencies.defenses[c].rank}`);
    for (const s in SAVES) O.add(`save:${s}:rank:${sys.saves[s].rank}`);
    O.add(`hands-free:${S.handsFree}`); O.add(`hands-free:but-really:${S.handsReallyFree}`);
    if (sys.resources.focus.max > 0) O.add('self:focus-pool');
  }

  applySynthetics(S, it) {
    for (const rule of it.r.rules || []) {
      const k = rule.key;
      const pred = rule.predicate ? this.injectDeep(S, rule.predicate, it) : null;
      const from = it.r.n;
      if (k === 'FlatModifier') {
        let sel = this.injectDeep(S, rule.selector || rule.selectors, it);
        sel = Array.isArray(sel) ? sel : [sel];
        const value = this.resolve(S, rule.value, it, 0);
        const ability = rule.ability || null;
        S.mods.push({sel, value, type: rule.type || (ability ? 'ability' : 'untyped'), slug: rule.slug || slugify(from), label: this.t(rule.label) || from,
          pred, from, it, ability, rawValue: rule.value, damageType: rule.damageType, critical: rule.critical, hide: rule.hideIfDisabled});
      } else if (k === 'AdjustModifier') {
        S.adjust.push({sel: [].concat(rule.selectors || rule.selector || []), slug: rule.slug, mode: rule.mode, value: this.resolve(S, rule.value, it, 0), pred, from, suppress: rule.suppress, relabel: this.t(rule.relabel),
          pr: rule.priority ?? ({override: 10, upgrade: 20, downgrade: 20, add: 30, subtract: 30, multiply: 40}[rule.mode] || 30)});
      } else if (k === 'Note') {
        S.notes.push({sel: [].concat(this.injectDeep(S, rule.selector, it)), text: this.inject(S, this.t(rule.text), it), title: this.t(this.inject(S, rule.title || '', it)) || from, pred, outcome: rule.outcome, from});
      } else if (k === 'DamageDice') {
        S.dice.push({sel: [].concat(this.injectDeep(S, rule.selector || rule.selectors, it)), n: this.resolve(S, rule.diceNumber, it, 0), d: rule.dieSize, type: rule.damageType, cat: rule.category,
          critical: rule.critical, pred, from, label: this.t(rule.label) || from, override: rule.override});
      } else if (k === 'RollOption') {
        if (rule.itemOnly) continue;
        if (pred && !testPred(pred, S.opts) && !rule.toggleable) continue;
        const opt = this.inject(S, rule.option, it);
        if (rule.toggleable) {
          S.toggles.push({option: opt, label: this.t(rule.label) || from, from: it, suboptions: rule.suboptions, disabledIf: rule.disabledIf});
          const tv = (S.ch.toggles || {})[opt];
          if (tv) { S.opts.add(opt); if (typeof tv === 'string') S.opts.add(`${opt}:${tv}`); }
          else if (tv == null && rule.value === true && !rule.alwaysActive) { /* default off in the sheet */ }
        } else S.opts.add(opt);
      } else if (k === 'BaseSpeed') {
        if (pred && !testPred(pred, S.opts)) continue;
        const v = this.resolve(S, rule.value, it, 0);
        const t = rule.selector || 'land';
        S.speeds[t] = Math.max(S.speeds[t] || 0, Number(v) || 0);
      } else if (k === 'Sense') {
        if (pred && !testPred(pred, S.opts)) continue;
        S.senses.push({type: rule.selector, acuity: rule.acuity, range: this.resolve(S, rule.range, it, null), from});
      } else if (k === 'Resistance' || k === 'Weakness' || k === 'Immunity') {
        if (pred && !testPred(pred, S.opts)) continue;
        const list = k === 'Resistance' ? S.resist : k === 'Weakness' ? S.weak : S.immune;
        list.push({type: [].concat(rule.type || []).join(', '), value: rule.value != null ? this.resolve(S, rule.value, it, 0) : null, except: rule.exceptions, from});
      } else if (k === 'Strike') {
        if (pred && !testPred(pred, S.opts)) continue;
        S.strikesRE.push({rule, it});
      } else if (k === 'MartialProficiency') {
        S.martial.push({def: this.injectDeep(S, rule.definition, it), rank: this.resolve(S, rule.value, it, 1), label: this.t(rule.label), from});
      } else if (k === 'DexterityModifierCap') {
        if (pred && !testPred(pred, S.opts)) continue;
        S.dexCaps.push({value: this.resolve(S, rule.value, it, 99), from});
      } else if (k === 'TempHP') {
        S.tempHP.push({value: this.resolve(S, rule.value, it, 0), from});
      } else if (k === 'RollTwice') {
        S.rollTwice.push({sel: [].concat(rule.selector), keep: rule.keep, pred, from});
      } else if (k === 'AdjustDegreeOfSuccess') {
        S.degree.push({sel: rule.selector, adj: rule.adjustment, pred, from});
      } else if (k === 'CriticalSpecialization') {
        S.critSpec.push({pred, from});
      } else if (k === 'CreatureSize') {
        if (pred && !testPred(pred, S.opts)) continue;
        S.sys.traits.size = rule.value;
      }
    }
  }

  // ───── modifiers for a statistic ─────
  collectMods(S, domains, base, opts, extra) {
    const D = new Set(domains);
    const O = opts || S.opts;
    const mods = base.slice();
    for (const m of S.mods) {
      if (!m.sel.some(s => D.has(s))) continue;
      let value = m.value;
      if (extra && typeof m.rawValue === 'string' && m.rawValue.includes('@')) value = this.resolve(S, m.rawValue, m.it, 0, extra);
      if (m.ability) value = S.attr[m.ability] ? Math.trunc(S.attr[m.ability].mod) : value;
      const known = !m.pred || testPred(m.pred, O);
      const sit = !known && situational(m.pred);
      if (!known && !sit) continue;
      mods.push({label: m.label, value: Number(value) || 0, type: m.type, slug: m.slug, enabled: known, situational: sit, from: m.from, damageType: m.damageType, critical: m.critical});
    }
    for (const a of S.adjust.slice().sort((x, y) => x.pr - y.pr)) {
      if (!a.sel.some(s => D.has(s) || s === 'all')) continue;
      if (a.pred && !testPred(a.pred, O)) continue;
      for (const m of mods) if (m.slug === a.slug) {
        if (a.suppress) m.enabled = false;
        else if (a.mode === 'upgrade') m.value = Math.max(m.value, a.value);
        else if (a.mode === 'downgrade') m.value = Math.min(m.value, a.value);
        else if (a.mode === 'override') m.value = a.value;
        else if (a.mode === 'add') m.value += a.value;
        else if (a.mode === 'subtract') m.value -= a.value;
        else if (a.mode === 'multiply') m.value *= a.value;
        if (a.relabel && !a.suppress) m.label = a.relabel;
      }
    }
    return this.stack(mods);
  }
  stack(mods) {
    const best = {}, worst = {};
    let ability = null;
    for (const m of mods) {
      if (m.enabled === false) { m.applied = false; continue; }
      if (m.type === 'ability') { if (!ability || m.value > ability.value) ability = m; continue; }
    }
    let total = 0;
    for (const m of mods) {
      if (m.enabled === false) { m.applied = false; continue; }
      if (m.type === 'ability') { m.applied = m === ability; if (m.applied) total += m.value; continue; }
      if (m.type === 'untyped' || !m.type) { m.applied = true; total += m.value; continue; }
      const T = m.type === 'potency' ? 'item' : m.type;
      const tab = m.value < 0 ? worst : best;
      const ex = tab[T];
      if (!ex) { tab[T] = m; m.applied = true; total += m.value; }
      else if ((m.value < 0 && m.value < ex.value) || (m.value >= 0 && m.value > ex.value)) { ex.applied = false; total += m.value - ex.value; tab[T] = m; m.applied = true; }
      else m.applied = false;
    }
    return {total, mods};
  }
  stat(S, label, domains, base, opts, extra) {
    const r = this.collectMods(S, domains, base, opts, extra);
    return {label, total: r.total, mods: r.mods, situational: r.mods.filter(m => m.situational)};
  }
  attrMod(S, a, label) { return {label: label || ATTR_NAME[a], value: Math.trunc(S.attr[a].mod), type: 'ability', slug: a, enabled: true}; }
  profMod(S, rank) { return {label: RANKS[rank], value: prof(rank, S.level), type: 'proficiency', slug: 'proficiency', enabled: true}; }

  // ───── final statistics ─────
  statistics(S) {
    const sys = S.sys, L = S.level, out = {S, level: L};
    // attributes after rule elements
    out.attributes = {};
    for (const a of ATTRS) out.attributes[a] = Math.trunc(S.attr[a].mod);
    // hit points
    const hpBase = [{label: 'Ancestry', value: sys.attributes.ancestryhp, type: 'untyped', enabled: true},
      {label: 'Class', value: sys.attributes.classhp * L, type: 'untyped', enabled: true},
      {label: 'Constitution', value: Math.trunc(S.attr.con.mod) * L, type: 'ability', slug: 'con', enabled: true}];
    out.hp = this.stat(S, 'Hit Points', ['hp'], hpBase);
    const perLevel = this.collectMods(S, ['hp-per-level'], []);
    if (perLevel.total) { out.hp.total += perLevel.total * L; out.hp.mods.push({label: 'Per level', value: perLevel.total * L, type: 'untyped', applied: true}); }
    // perception
    const pr = sys.perception.rank;
    out.perception = this.stat(S, 'Perception', ['perception', 'wis-based', 'all', 'check'], [this.attrMod(S, 'wis'), this.profMod(S, pr)]);
    out.perception.rank = pr;
    // saves
    out.saves = {};
    for (const [s, a] of Object.entries(SAVES)) {
      const r = sys.saves[s].rank;
      out.saves[s] = this.stat(S, s[0].toUpperCase() + s.slice(1), [s, `${a}-based`, 'saving-throw', 'all', 'check'], [this.attrMod(S, a), this.profMod(S, r)]);
      out.saves[s].rank = r;
      out.saves[s].degree = S.degree.filter(d => d.sel === s || d.sel === 'saving-throw').map(d => d.from);
    }
    // skills, with armour check penalty
    out.skills = {};
    const armor = S.armor;
    for (const [s, v] of Object.entries(sys.skills)) {
      const lore = !SKILLS[s];
      const a = lore ? 'int' : SKILLS[s];
      const base = [this.attrMod(S, a), this.profMod(S, v.rank)];
      if ((a === 'str' || a === 'dex') && armor && (armor.r.chk || 0) < 0) {
        const met = S.opts.has('armor:strength-requirement-met');
        const flex = (armor.r.tr || []).includes('flexible');
        let applies = !met;
        if (s === 'acrobatics' || s === 'athletics') applies = !(met || flex);
        if (s === 'stealth' && (armor.r.tr || []).includes('noisy')) applies = true;
        if (applies) base.push({label: 'Armour check penalty', value: armor.r.chk, type: 'untyped', slug: 'armor-check-penalty', enabled: true});
      }
      if (v.rank === 0 && !lore && (S.ch.options || {}).untrainedImprov) {}
      const st = this.stat(S, lore ? (S.loreNames[s] || s) : s[0].toUpperCase() + s.slice(1),
        [s, `${a}-based`, 'skill-check', `${a}-skill-check`, 'all', 'check'].concat(lore ? ['lore-skill-check'] : []), base);
      st.rank = v.rank; st.attr = a; st.lore = lore;
      out.skills[s] = st;
    }
    // class DCs
    out.classDCs = {};
    for (const [slug, c] of Object.entries(sys.proficiencies.classDCs)) {
      const a = c.attribute || (S.cls && slug === S.cls.sl ? ((S.ch.boosts || {}).class || S.cls.key[0] || 'int') : 'str');
      const st = this.stat(S, 'Class DC', ['class', slug, `${a}-based`, 'all'], [this.attrMod(S, a), this.profMod(S, c.rank)]);
      st.total += 10; st.rank = c.rank; st.attr = a; st.primary = !!c.primary;
      out.classDCs[slug] = st;
    }
    // armour class
    const dexCaps = [Infinity, ...S.dexCaps.map(x => x.value)];
    if (armor && armor.r.dex != null) dexCaps.push(armor.r.dex);
    const cap = Math.min(...dexCaps);
    const dex = Math.trunc(S.attr.dex.mod);
    const acRank = armor ? sys.proficiencies.defenses[armor.r.cat] ? sys.proficiencies.defenses[armor.r.cat].rank : 0 : sys.proficiencies.defenses.unarmored.rank;
    const acBase = [{label: 'Dexterity' + (dex > cap ? ` (capped at ${fmt(cap)})` : ''), value: Math.min(dex, cap), type: 'ability', slug: 'dex', enabled: true}, this.profMod(S, acRank)];
    if (armor) {
      const pot = armor.runes.potency || 0;
      acBase.push({label: armor.inv.name || armor.r.n, value: (armor.r.ac || 0) + pot, type: 'item', slug: 'armor', enabled: true});
    }
    if (S.shield && S.opts.has('self:shield:raised')) acBase.push({label: 'Raised shield', value: S.shield.r.ac || 0, type: 'circumstance', slug: 'raised-shield', enabled: true});
    out.ac = this.stat(S, 'Armour Class', ['ac', 'dex-based', 'all'], acBase);
    out.ac.total += 10; out.ac.rank = acRank;
    // speeds
    const land = S.speeds.land || (S.anc ? S.anc.speed : 25);
    const spBase = [{label: 'Base', value: land, type: 'untyped', enabled: true}];
    if (armor && armor.r.spd) {
      const met = typeof armor.r.str === 'number' && S.attr.str.mod >= armor.r.str;
      const pen = Math.min(met ? Math.min(armor.r.spd + 5, 0) : armor.r.spd, 0);
      if (pen) spBase.push({label: (armor.inv.name || armor.r.n) + ' speed penalty', value: pen, type: 'untyped', enabled: true});
    }
    if (S.shield && S.shield.r.spd) spBase.push({label: S.shield.r.n, value: S.shield.r.spd, type: 'untyped', enabled: true});
    if (armor && (armor.r.tr || []).includes('hindering')) spBase.push({label: 'Hindering', value: -5, type: 'untyped', enabled: true});
    out.speed = this.stat(S, 'Speed', ['land-speed', 'speed', 'all-speeds'], spBase);
    out.otherSpeeds = {};
    for (const [t, v] of Object.entries(S.speeds)) if (t !== 'land') {
      const st = this.stat(S, t[0].toUpperCase() + t.slice(1) + ' Speed', [`${t}-speed`, 'speed', 'all-speeds'], [{label: 'Base', value: v, type: 'untyped', enabled: true}]);
      out.otherSpeeds[t] = st;
    }
    // initiative uses Perception unless a choice says otherwise
    const initSkill = (S.ch.initiative && out.skills[S.ch.initiative]) ? S.ch.initiative : null;
    const initBase = initSkill ? out.skills[initSkill].mods.filter(m => m.type === 'ability' || m.type === 'proficiency').map(m => ({...m})) : [this.attrMod(S, 'wis'), this.profMod(S, pr)];
    out.initiative = this.stat(S, 'Initiative', ['initiative', initSkill || 'perception', 'all', 'check'], initBase);
    // spellcasting
    out.spellcasting = this.spellcasting(S, out);
    // strikes
    out.strikes = this.strikes(S);
    // resources
    out.focusMax = Math.min(sys.resources.focus.max || 0, sys.resources.focus.cap || 3);
    out.heroMax = sys.resources.heroPoints.max;
    out.dyingMax = 4 - ((S.ch.conditions || {}).doomed || 0);
    out.recoveryDC = sys.attributes.dying.recoveryDC;
    out.resist = S.resist; out.weak = S.weak; out.immune = S.immune;
    out.senses = S.senses; out.size = sys.traits.size; out.traits = sys.traits.value;
    out.languages = this.languages(S);
    out.bulk = this.bulk(S, out);
    out.tempHP = S.tempHP;
    out.notes = S.notes; out.degree = S.degree; out.rollTwice = S.rollTwice;
    out.wastedInc = S.wastedInc || [];
    out.items = S.items; out.pending = S.pending; out.toggles = S.toggles; out.actions = S.actions;
    out.slots = this.slots(S);
    out.trainCount = this.trainCount(S);
    out.warnings = S.warnings;
    out.boostsAllowed = this.boostsAllowed(S);
    return out;
  }

  languages(S) {
    const out = new Set((S.anc && S.anc.langs) || []);
    for (const l of S.languagesGranted) if (l) out.add(typeof l === 'string' ? l : l.slug);
    for (const l of S.ch.languages || []) out.add(l);
    const extraMax = (S.anc ? (S.anc.addl && S.anc.addl.count) || 0 : 0) + Math.max(0, Math.trunc(S.attr.int.mod)) + (S.sys.build.languages.max || 0);
    return {list: [...out], extraMax, chosen: (S.ch.languages || []).length};
  }
  trainCount(S) {
    // number of skills a character chooses to train at level 1, from class and Intelligence (remastered rules)
    const n = (S.cls ? S.cls.skills.additional || 0 : 0) + Math.max(0, Math.trunc(S.attr.int.mod));
    return n;
  }
  boostsAllowed(S) {
    return {1: 4, 5: S.level >= 5 ? 4 : 0, 10: S.level >= 10 ? 4 : 0, 15: S.level >= 15 ? 4 : 0, 20: S.level >= 20 ? 4 : 0};
  }

  // feat and choice slots by level
  slots(S) {
    const out = [], cls = S.cls, L = 20, ch = S.ch;
    const anc = cls && cls.lv ? cls.lv.ancestryFeatLevels : [1, 5, 9, 13, 17];
    const add = (lv, kind, label) => out.push({id: `${kind}-${lv}`, lv, kind, label});
    for (const lv of anc) add(lv, 'ancestry', 'Ancestry feat');
    if (cls) {
      if (!cls.lv.classFeatLevels.includes(1) && ['fighter', 'ranger', 'rogue', 'monk', 'swashbuckler', 'investigator', 'gunslinger', 'inventor', 'commander', 'guardian', 'exemplar', 'kineticist', 'thaumaturge', 'alchemist', 'barbarian', 'champion', 'animist', 'runesmith'].includes(cls.sl) === false) {}
      for (const lv of cls.lv.classFeatLevels) add(lv, 'class', 'Class feat');
      for (const lv of cls.lv.skillFeatLevels) add(lv, 'skill', 'Skill feat');
      for (const lv of cls.lv.generalFeatLevels) add(lv, 'general', 'General feat');
      for (const lv of cls.lv.skillIncreaseLevels) out.push({id: `inc-${lv}`, lv, kind: 'increase', label: 'Skill increase'});
    }
    if ((ch.options || {}).freeArchetype) for (let lv = 2; lv <= 20; lv += 2) add(lv, 'archetype', 'Free archetype feat');
    for (const b of ch.bonusSlots || []) out.push({id: b.id, lv: b.lv, kind: b.kind, label: b.label || 'Bonus feat', bonus: true});
    for (const lv of [5, 10, 15, 20]) out.push({id: `boost-${lv}`, lv, kind: 'boost', label: 'Attribute boosts'});
    out.sort((a, b) => a.lv - b.lv || ORDER.indexOf(a.kind) - ORDER.indexOf(b.kind));
    return out;
  }

  // ───── feats a slot can take ─────
  featOptions(res, slot) {
    const S = res.S, kind = slot.kind, lv = slot.lv;
    const traits = new Set([...(S.sys.traits.value || [])]);
    const cls = S.cls;
    const out = [];
    for (const r of Object.values(this.db.e)) {
      if (r.t !== 'feat') continue;
      const cat = r.cat, tr = r.tr || [];
      if ((r.lv || 1) > lv) continue;
      let ok = false;
      if (kind === 'ancestry') ok = cat === 'ancestry' && tr.some(t => traits.has(t));
      else if (kind === 'class') ok = cat === 'class' && ((cls && tr.includes(cls.sl)) || tr.includes('archetype'));
      else if (kind === 'archetype') ok = (cat === 'class' || cat === 'skill') && tr.includes('archetype');
      else if (kind === 'skill') ok = cat === 'skill';
      else if (kind === 'general') ok = cat === 'general' || cat === 'skill';
      else if (kind === 'bonus') ok = ['ancestry', 'class', 'skill', 'general'].includes(cat);
      if (ok) out.push(r);
    }
    return out.sort((a, b) => (b.lv || 0) - (a.lv || 0) || a.n.localeCompare(b.n));
  }
  // a rough reading of prerequisite text, for a warning only
  prereqs(res, r) {
    const S = res.S, out = [];
    for (const p of r.pre || []) {
      const t = p.toLowerCase().trim();
      let ok = null;
      let m;
      if ((m = t.match(/^(trained|expert|master|legendary) in ([a-z' -]+?)$/))) {
        const need = ['untrained', 'trained', 'expert', 'master', 'legendary'].indexOf(m[1]);
        const what = m[2].trim();
        if (what === 'perception') ok = S.sys.perception.rank >= need;
        else if (SKILLS[what]) ok = S.sys.skills[what].rank >= need;
        else if (/lore$/.test(what)) { const k = slugify(what); ok = (what === 'at least one lore' || what === 'lore' || what === 'a lore') ? Object.values(S.sys.skills).some(v => v.lore && v.rank >= need) : (S.sys.skills[k] ? S.sys.skills[k].rank >= need : false); }
        else if (/^(fortitude|reflex|will) saves?$/.test(what)) ok = S.sys.saves[what.split(' ')[0]].rank >= need;
      } else if ((m = t.match(/^(strength|dexterity|constitution|intelligence|wisdom|charisma) \+(\d)$/))) {
        const a = {strength: 'str', dexterity: 'dex', constitution: 'con', intelligence: 'int', wisdom: 'wis', charisma: 'cha'}[m[1]];
        ok = Math.trunc(S.attr[a].mod) >= Number(m[2]);
      } else {
        const sl = slugify(p);
        const sl2 = sl.replace(/-(hybrid-study|muse|instinct|racket|doctrine|mystery|patron|bloodline|order|way|methodology|style|school|arcane-school|research-field|implement|innovation|cause|focus-spell)$/, '');
        for (const x of [sl, sl2]) {
          if (ok !== null) break;
          if (Object.values(this.db.e).some(r => (r.t === 'feat' || r.t === 'action') && r.sl === x)) ok = S.opts.has('feat:' + x) || S.opts.has('feature:' + x) || S.items.some(i => i.r.sl === x);
        }
      }
      out.push({text: p, ok});
    }
    return out;
  }

  // ───── spellcasting ─────
  spellcasting(S, out) {
    const ch = S.ch, L = S.level, list = [];
    const rank = S.sys.proficiencies.spellcasting.rank;
    const entries = (ch.spells && ch.spells.entries) || [];
    for (const e of entries) {
      const a = e.attr || 'int';
      const r = e.prof === 'manual' ? (e.rank || 0) : rank;
      const trad = e.trad || 'arcane';
      const atk = this.stat(S, 'Spell attack', ['spell-attack', 'spell-attack-roll', `${trad}-spell-attack`, 'attack', 'attack-roll', `${a}-based`, 'all', 'check'], [this.attrMod(S, a), this.profMod(S, r)]);
      const dc = this.stat(S, 'Spell DC', ['spell-dc', `${trad}-spell-dc`, `${a}-based`, 'all'], [this.attrMod(S, a), this.profMod(S, r)]);
      dc.total += 10;
      let slots = null, charges = null;
      if (e.archetype) {
        const has = n => S.opts.has(`feat:${n}-${e.archetype}-spellcasting`);
        slots = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        const add = (rk, lv, f) => { if (has(f) && L >= lv) slots[rk] = 1; };
        add(1, 4, 'basic'); add(2, 6, 'basic'); add(3, 8, 'basic'); add(4, 12, 'expert'); add(5, 14, 'expert'); add(6, 16, 'expert'); add(7, 18, 'master'); add(8, 20, 'master');
      } else if (e.kind === 'prepared' || e.kind === 'spontaneous') {
        const tab = e.table && this.db.slots[e.table] ? this.db.slots[e.table][0] : null;
        if (tab && tab.rows[L]) slots = tab.rows[L].slice();
        if (e.slotAdjust) slots = (slots || []).map((n, i) => n + (Number(e.slotAdjust[i]) || 0));
        if (e.slotsManual) slots = e.slotsManual.slice();
      }
      list.push({e, attack: atk, dc, rank: r, slots, charges, cantripRank: Math.max(1, Math.ceil(L / 2))});
    }
    // a staff gains charges equal to the rank of the highest spell slot, plus one expended slot's rank
    const top = Math.max(0, ...list.filter(x => x.slots).map(x => x.slots.reduce((m, n, i) => n > 0 && i > 0 ? i : m, 0)));
    for (const x of list) if (x.e.kind === 'staff') x.charges = {max: top + (Number(x.e.extra) || 0), used: Math.min(x.e.used || 0, top + (Number(x.e.extra) || 0)), top};
    S.topSlot = top;
    return list;
  }
  // spellcasting archetypes the character has taken a dedication for
  dedications(res) {
    const out = [];
    for (const c of Object.keys(CASTING)) if (res.S.opts.has(`feat:${c}-dedication`) && !(res.S.cls && res.S.cls.sl === c)) out.push(c);
    return out;
  }
  archetypeEntry(c) {
    const cs = CASTING[c], cls = this.rec('cl:' + c);
    return {id: 'arch:' + c, name: (cls ? cls.n : c) + ' archetype spells', trad: cs[0] || (c === 'witch' ? 'occult' : 'arcane'), kind: cs[1], attr: cs[2], archetype: c, prof: 'class', known: [], prepared: {}, used: {}};
  }
  // damage of a spell cast at a rank, with interval or fixed heightening applied
  spellDamage(r, rank) {
    if (!r || !r.dmg) return [];
    const out = [];
    const base = r.lv || 1;
    for (const [id, d] of Object.entries(r.dmg)) {
      let f = d.f;
      if (r.hti && r.hti[1][id] && rank > base) {
        const steps = Math.floor((rank - base) / (r.hti[0] || 1));
        for (let i = 0; i < steps; i++) f += '+' + r.hti[1][id];
      }
      if (r.htf) { const lv = Object.keys(r.htf).map(Number).filter(x => x <= rank).sort((a, b) => b - a)[0]; if (lv && r.htf[lv][id]) f = r.htf[lv][id]; }
      out.push({f: simplify(f), t: d.t, c: d.c, heal: d.h});
    }
    return out;
  }
  defaultEntry(cls) {
    if (!cls || !cls.sc || !this.db.slots[cls.sl]) return null;
    const c = CASTING[cls.sl] || [null, 'prepared', cls.key[0] || 'int'];
    return {id: 'class', name: cls.n + ' spells', trad: c[0] || 'arcane', kind: c[1], attr: c[2], table: cls.sl, prof: 'class', known: [], prepared: {}, used: {}};
  }

  // ───── strikes ─────
  strikes(S) {
    const out = [], ch = S.ch;
    const weapons = [];
    for (const inv of ch.inventory || []) {
      const r = this.invRec(inv); if (!r || r.t !== 'weapon') continue;
      if (inv.eq === 'dropped' || inv.qty === 0) continue;
      weapons.push({r, inv, held: inv.eq === 'held1' || inv.eq === 'held2'});
    }
    weapons.sort((a, b) => b.held - a.held);
    for (const w of weapons) out.push(this.strike(S, w.r, w.inv, w.held));
    for (const {rule, it} of S.strikesRE) {
      const b = (rule.damage && rule.damage.base) || {};
      const r = {k: 'strike:' + (rule.slug || slugify(rule.label || it.r.n)), n: this.t(rule.label) || it.r.n, sl: rule.slug || slugify(this.t(rule.label) || it.r.n), t: 'weapon',
        cat: rule.category || 'unarmed', grp: rule.group || 'brawling', base: rule.baseType || null, tr: (rule.traits || []).concat(rule.category === 'unarmed' ? ['unarmed'] : []),
        dmg: {dice: b.dice || 1, die: b.die || 'd4', damageType: b.damageType || 'bludgeoning'}, rng: rule.range && rule.range.increment ? rule.range.increment : (typeof rule.range === 'number' ? rule.range : null), runes: {potency: 0, striking: 0, property: []}};
      out.push(this.strike(S, r, null, true, true));
    }
    if (!(ch.options || {}).hideFist) {
      const fist = {k: 'strike:fist', n: 'Fist', sl: 'fist', t: 'weapon', cat: 'unarmed', grp: 'brawling', base: 'fist', tr: ['agile', 'finesse', 'nonlethal', 'unarmed'],
        dmg: {dice: 1, die: 'd4', damageType: 'bludgeoning'}, runes: {potency: 0, striking: 0, property: []}};
      // handwraps of mighty blows give their runes to unarmed attacks
      const hw = (ch.inventory || []).find(i => { const r = this.invRec(i); return r && /handwraps-of-mighty/.test(r.sl) && i.inv; });
      if (hw) fist.runes = Object.assign({potency: 0, striking: 0, property: []}, (this.invRec(hw) || {}).runes || {}, hw.runes || {});
      if (!S.strikesRE.some(x => (x.rule.slug || '') === 'fist')) out.push(this.strike(S, fist, null, true, true));
    }
    return out;
  }
  weaponRank(S, r, opts) {
    const at = S.sys.proficiencies.attacks;
    let rank = (at[r.cat] || {rank: 0}).rank;
    if (r.grp && at[`weapon-group-${r.grp}`]) rank = Math.max(rank, at[`weapon-group-${r.grp}`].rank);
    if (r.base && at[`weapon-base-${r.base}`]) rank = Math.max(rank, at[`weapon-base-${r.base}`].rank);
    for (const m of S.martial) if (testPred(m.def, opts)) rank = Math.max(rank, Number(m.rank) || 0);
    for (const [k, v] of Object.entries(at)) if (v && v.custom && v.definition && testPred(v.definition, opts)) rank = Math.max(rank, v.rank);
    return rank;
  }
  strike(S, r, inv, held, natural) {
    const L = S.level;
    const runes = Object.assign({potency: 0, striking: 0, property: []}, r.runes || {}, (inv && inv.runes) || {});
    const traits = new Set(r.tr || []);
    for (const p of runes.property || []) { const pr = (this.db.runes.WEAPON_PROPERTY_RUNES || {})[p]; if (pr) for (const t of pr.traits || []) if (t !== 'magical') traits.add(t); }
    if (runes.potency || (runes.property || []).length) traits.add('magical');
    const thrownMelee = false;
    const ranged = !!(r.rng && !traits.has('thrown')) && !(r.cat === 'unarmed' && !r.rng);
    const isRanged = r.rng && !(traits.has('thrown') && !ranged) ? true : false;
    const melee = !isRanged;
    const slug = r.sl, id = inv ? inv.id : r.k;
    const iopts = itemOptions(Object.assign({}, r, {tr: [...traits]}), 'item', [`item:${melee ? 'melee' : 'ranged'}`, held ? 'item:hands-held:' + (inv && inv.eq === 'held2' ? 2 : 1) : 'item:hands-held:0',
      `item:damage:die:faces:${String(r.dmg.die || 'd4').replace('d', '')}`, 'item:equipped', runes.potency ? 'item:magical' : '']);
    const opts = new Set([...S.opts, ...iopts, 'attack', 'strike', melee ? 'melee' : 'ranged']);
    for (const rule of r.rules || []) if (rule.key === 'RollOption' && rule.itemOnly && (!rule.predicate || testPred(rule.predicate, opts))) opts.add(rule.option);
    const rank = this.weaponRank(S, r, opts);
    opts.add(`item:proficiency:rank:${rank}`);
    for (let i = 0; i <= rank; i++) opts.add(`item:proficiency:rank:${i}`);
    const unarmedOrWeapon = r.cat === 'unarmed' ? 'unarmed' : 'weapon', mr = melee ? 'melee' : 'ranged';
    const domains = [r.base ? `${r.base}-base-attack-roll` : null, r.grp ? `${r.grp}-group-attack-roll` : null, `${id}-attack`, `${slug}-attack`, `${slug}-attack-roll`,
      `${unarmedOrWeapon}-attack-roll`, `${mr}-attack-roll`, `${mr}-strike-attack-roll`, 'strike-attack-roll', 'attack-roll', 'attack', 'check', 'all',
      `${['untrained', 'trained', 'expert', 'master', 'legendary'][rank]}-attack`].filter(Boolean);
    // attribute: Strength for melee, Dexterity for ranged; finesse uses the better of the two
    let attr = melee ? 'str' : 'dex';
    if (melee && traits.has('finesse') && S.attr.dex.mod > S.attr.str.mod) attr = 'dex';
    const base = [this.attrMod(S, attr), this.profMod(S, rank)];
    if (runes.potency) base.push({label: 'Weapon potency', value: runes.potency, type: 'item', slug: 'potency', enabled: true});
    if (r.bonus) base.push({label: 'Item bonus', value: r.bonus, type: 'item', enabled: true});
    const atk = this.stat(S, r.n, domains.concat(attr + '-based'), base, opts, {weapon: {system: {damage: {dice: r.dmg.dice + (runes.striking || 0)}, runes}}});
    const agile = traits.has('agile');
    const map = [atk.total, atk.total - (agile ? 4 : 5), atk.total - (agile ? 8 : 10)];
    // damage
    const dice = (r.dmg.dice || 1) + (runes.striking || 0);
    const dmgDomains = [`${id}-damage`, `${id}-${mr}-damage`, `${slug}-damage`, `${mr}-strike-damage`, `${mr}-damage`, `${unarmedOrWeapon}-damage`,
      r.grp ? `${r.grp}-weapon-group-damage` : null, r.base ? `${r.base}-base-damage` : null, 'attack-damage', 'strike-damage', 'damage',
      r.base ? `${r.base}-base-type-damage` : null, `${['untrained', 'trained', 'expert', 'master', 'legendary'][rank]}-damage`].filter(Boolean);
    const dBase = [];
    const strMod = Math.trunc(S.attr.str.mod);
    if (melee || traits.has('thrown')) dBase.push({label: 'Strength', value: strMod, type: 'ability', slug: 'str', enabled: true});
    else if (traits.has('propulsive')) dBase.push({label: 'Strength (propulsive)', value: strMod > 0 ? Math.floor(strMod / 2) : strMod, type: 'ability', slug: 'str', enabled: true});
    if (r.bdmg) dBase.push({label: 'Bonus damage', value: r.bdmg, type: 'untyped', enabled: true});
    const dmg = this.stat(S, 'Damage', dmgDomains.concat(['str-damage']), dBase, opts, {weapon: {system: {damage: {dice}, runes}}});
    // extra dice: property runes and rule elements
    const extraDice = [];
    for (const p of runes.property || []) {
      const pr = (this.db.runes.WEAPON_PROPERTY_RUNES || {})[p]; if (!pr) continue;
      for (const a of ((pr.damage || {}).additional || [])) if (a.diceNumber) extraDice.push({n: a.diceNumber, d: a.dieSize, type: a.damageType, cat: a.category, critical: a.critical, from: this.t(pr.name), pred: a.predicate});
    }
    const D = new Set(dmgDomains);
    for (const x of S.dice) {
      if (!x.sel.some(s => D.has(s))) continue;
      const known = !x.pred || testPred(x.pred, opts);
      if (!known && !situational(x.pred)) continue;
      if (x.override) continue;
      if (!x.n || !x.d) continue;
      extraDice.push({n: x.n, d: x.d, type: x.type, cat: x.cat, critical: x.critical, from: x.label, situational: !known});
    }
    const traitsList = [...traits].sort();
    for (const t of traitsList) {
      let m;
      if ((m = t.match(/^deadly-(d\d+)$/))) extraDice.push({n: (runes.striking >= 3 ? 3 : runes.striking >= 2 ? 2 : 1), d: m[1], type: r.dmg.damageType, critical: true, from: 'Deadly'});
      if ((m = t.match(/^fatal-(d\d+)$/))) extraDice.push({n: 1, d: m[1], type: r.dmg.damageType, critical: true, from: 'Fatal (and the weapon die becomes ' + m[1] + ' on a critical hit)'});
    }
    const formula = `${dice}${r.dmg.die} ${dmg.total ? fmt(dmg.total) + ' ' : ''}${r.dmg.damageType || ''}`.replace(/\s+/g, ' ').trim();
    const notes = S.notes.filter(n => n.sel.some(s => domains.includes(s) || D.has(s)) && (!n.pred || testPred(n.pred, opts) || situational(n.pred)));
    for (const p of runes.property || []) {
      const pr = (this.db.runes.WEAPON_PROPERTY_RUNES || {})[p]; if (!pr) continue;
      for (const n of (((pr.damage || {}).notes) || []).concat(pr.attack && pr.attack.notes || [])) notes.push({title: this.t(n.title), text: this.t(n.text), outcome: n.outcome, from: this.t(pr.name)});
    }
    for (const ab of r.abil || []) notes.push({title: ab.n, text: ab.text, from: r.n});
    return {r, inv, name: (inv && inv.name) || r.n, held, natural: !!natural, rank, attack: atk, map, damage: dmg, formula, dice, die: r.dmg.die, dtype: r.dmg.damageType,
      extraDice, traits: traitsList, notes, range: r.rng || null, melee, critSpec: S.critSpec.some(c => !c.pred || testPred(c.pred, opts)) || rank >= 0 && false};
  }

  // ───── bulk ─────
  bulk(S, out) {
    let light = 0, total = 0;
    for (const inv of S.ch.inventory || []) {
      const r = this.invRec(inv); if (!r || inv.eq === 'dropped') continue;
      const q = inv.qty == null ? 1 : inv.qty;
      let b = r.bulk || 0;
      if (r.t === 'armor' && inv.eq === 'worn') b = r.bulk || 0;
      else if (r.t === 'armor') b = (r.bulk || 0) + 1;
      if (b === 0.1) light += q; else total += b * q;
    }
    // coins: 1,000 coins are 1 Bulk
    const c = S.ch.coins || {};
    const coins = (c.pp || 0) + (c.gp || 0) + (c.sp || 0) + (c.cp || 0);
    total += Math.floor(coins / 1000);
    total += Math.floor(light / 10);
    const str = Math.trunc(S.attr.str.mod);
    const capMods = this.collectMods(S, ['inventory-bulk'], []).total;
    return {value: total, light: light % 10, encumbered: 5 + str + (S.sys.inventory ? 0 : 0), max: 10 + str};
  }
}
// combine like dice: 2d6+1d6+1d6 becomes 4d6
function simplify(f) {
  const dice = {}, rest = [];
  let k = 0;
  for (const t of String(f).replace(/\s+/g, '').replace(/-/g, '+-').split('+').filter(Boolean)) {
    const m = t.match(/^(\d*)d(\d+)$/);
    if (m) dice[m[2]] = (dice[m[2]] || 0) + Number(m[1] || 1);
    else if (/^-?\d+$/.test(t)) k += Number(t);
    else rest.push(t);
  }
  const parts = Object.keys(dice).sort((a, b) => b - a).map(d => dice[d] + 'd' + d).concat(rest);
  if (k) parts.push(String(k));
  return parts.join('+').replace(/\+-/g, '-') || '0';
}
const ORDER = ['ancestry', 'class', 'archetype', 'skill', 'general', 'increase', 'boost', 'bonus'];

const api = {Engine, simplify, testPred, itemOptions, slugify, prof, SKILLS, SAVES, ATTRS, ATTR_NAME, RANKS, CASTING, fmt, effectSlug};
if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.CSEngine = api;
})(typeof self !== 'undefined' ? self : this);
