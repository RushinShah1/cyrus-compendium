const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const fr = Object.values(db.e).filter(r => r.fr);
console.log('FR deities in data', fr.length);
for (const [cls, dei] of [['cl:cleric', 'de:fr-selune'], ['cl:champion', 'de:fr-torm'], ['cl:cleric', 'de:fr-lolth'], ['cl:cleric', 'de:fr-silvanus']]) {
  const ch = {level: 5, ancestry: 'an:human', heritage: 'he:versatile-human', background: 'bg:acolyte', class: cls, deity: dei, boosts: {}, feats: {}, choices: {}, inventory: [], spells: {entries: []}, trained: [], increases: {}};
  const r = eng.compute(ch);
  console.log(cls, dei, 'warnings', r.warnings, 'pending', r.pending.filter(p => p.value == null).map(p => p.prompt + ': ' + eng.choices(r.S, p).length + ' options').slice(0, 6));
}
