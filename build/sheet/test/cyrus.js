const {loadDB, E} = require('./load.js');
const db = loadDB();
const k = (pre, name) => { const s = pre + ':' + E.slugify(name); if (!db.e[s]) throw new Error('missing ' + s); return s; };
const ch = {
  name: 'Cyrus Val\'Dira', level: Number(process.argv[2] || 5),
  ancestry: k('an', 'Human'), heritage: k('he', 'Versatile Human'), background: k('bg', 'Relentless Dedication'), class: k('cl', 'Magus'),
  boosts: {ancestry: ['str', 'int'], background: ['str', 'con'], class: 'str', 1: ['str', 'dex', 'con', 'int'], 5: ['str', 'con', 'int', 'wis']},
  trained: ['athletics', 'acrobatics', 'society'], lores: ['Academia Lore'], increases: {3: 'athletics', 5: 'arcana', 7: 'athletics'},
  feats: {'ancestry-1': {k: k('ft', 'Natural Ambition')}, 'class-2': {k: k('ft', 'Force Fang')}, 'skill-2': {k: k('ft', 'Additional Lore')},
    'general-3': {k: k('ft', 'Toughness')}, 'class-4': {k: k('ft', 'Expansive Spellstrike')}, 'skill-4': {k: k('ft', "Kreighton's Cognitive Crossover")},
    'ancestry-5': {k: k('ft', 'General Training')}},
  choices: {
    'class>cf:hybrid-study': {hybridStudy: '@' + k('cf', 'Laughing Shadow')},
    'heritage': {versatileHeritage: '@' + k('ft', 'Fleet')},
    'feat:ancestry-1': {naturalAmbition: '@' + k('ft', "Magus's Analysis")},
  },
  inventory: [{id: 'a1', k: k('eq', 'Guisarme'), eq: 'held2', runes: {potency: 1, striking: 1, property: ['fearsome']}},
              {id: 'a2', k: k('eq', 'Lattice Armor'), eq: 'worn', runes: {potency: 1}}],
  conditions: {}, effects: {}, toggles: {},
};
const eng = new E.Engine(db);
const r = eng.compute(ch);
const f = x => (x >= 0 ? '+' : '') + x;
console.log('attrs', r.attributes, 'HP', r.hp.total, 'AC', r.ac.total, 'speed', r.speed.total);
console.log('perc', f(r.perception.total), 'saves', Object.entries(r.saves).map(([k, v]) => k + ' ' + f(v.total)).join(', '));
console.log('skills', Object.entries(r.skills).map(([k, v]) => k + ' ' + f(v.total) + '(' + v.rank + ')').join(', '));
console.log('classDC', Object.values(r.classDCs).map(c => c.total));
for (const s of r.strikes) console.log('strike', s.name, s.map.map(f).join('/'), s.formula, s.extraDice.map(d => `${d.n}${d.d} ${d.type || ''}${d.critical ? ' crit' : ''} [${d.from}]`).join('; '), s.traits.join(','));
console.log('items', r.items.map(i => i.r.n).join(' | '));
console.log('pending', r.pending.map(p => `${p.uid}.${p.flag}=${p.value}`).join('; '));
console.log('toggles', r.toggles.map(t => t.key || t.option).join(', '));
console.log('AC mods', r.ac.mods.map(m => `${m.label} ${m.value}${m.applied ? '' : '(x)'}`).join(', '));
console.log('speed mods', r.speed.mods.map(m => `${m.label} ${m.value}${m.applied ? '' : '(x)'}${m.situational ? '(sit)' : ''}`).join(', '));
console.log('athletics mods', r.skills.athletics.mods.map(m => `${m.label} ${m.value}${m.applied ? '' : '(x)'}`).join(', '));
console.log('warnings', r.warnings);
module.exports = {ch, eng, r, db};
