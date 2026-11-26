const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const f = x => (x >= 0 ? '+' : '') + x;
for (const c of Object.values(db.e).filter(r => r.t === 'class')) {
  for (const L of [1, 10, 20]) {
    const ch = {level: L, ancestry: 'an:dwarf', heritage: null, background: 'bg:acolyte', class: c.k, boosts: {ancestry: [], background: ['wis', 'str'], class: c.key[0], 1: ['str', 'dex', 'con', 'wis'], 5: ['str', 'dex', 'con', 'wis'], 10: ['str', 'dex', 'con', 'wis'], 15: ['str', 'dex', 'con', 'wis'], 20: ['str', 'dex', 'con', 'wis']},
      trained: [], feats: {}, choices: {}, inventory: [], conditions: {}, effects: {}, toggles: {}, spells: {entries: []}};
    try {
      const r = eng.compute(ch);
      const sc = eng.defaultEntry(c);
      if (L === 20) console.log(c.n.padEnd(14), 'HP', r.hp.total, 'AC', r.ac.total, 'saves', Object.values(r.saves).map(s => f(s.total)).join('/'), 'perc', f(r.perception.total), 'DC', Object.values(r.classDCs).map(x => x.total).join(','), 'strikes', r.strikes.map(s => f(s.map[0])).join(','), 'pending', r.pending.length, sc ? 'casting ' + sc.table + ' ' + JSON.stringify((db.slots[sc.table] || [{rows: {}}])[0].rows[20] || null) : '');
    } catch (e) { console.log('ERROR', c.n, L, e.stack.split('\n').slice(0, 3).join(' | ')); }
  }
}
