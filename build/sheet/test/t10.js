const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const ch = {level: 5, ancestry: 'an:human', heritage: 'he:versatile-human', background: 'bg:acolyte', class: 'cl:cleric', deity: 'de:desna', boosts: {}, feats: {}, choices: {}, inventory: [], spells: {entries: []}, trained: [], increases: {}};
const r = eng.compute(ch);
for (const p of r.pending.filter(p => p.value == null)) console.log(p.uid, p.flag, '|', p.prompt, '|', eng.choices(r.S, p).length, JSON.stringify(p.rule.choices).slice(0, 300));
