const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const ch = Object.assign(JSON.parse(require('fs').readFileSync('/home/claude/site/assets/cs/cyrus.json')), {level: 16});
ch.boosts.ancestry = ['str', 'int']; ch.boosts.background = ['str', 'con']; ch.boosts.class = 'str'; ch.boosts[1] = ['str', 'dex', 'con', 'int']; ch.boosts[15] = ['con', 'int', 'str', 'dex'];
const r = eng.compute(ch);
const f = x => (x >= 0 ? '+' : '') + x;
console.log(r.attributes, 'HP', r.hp.total, 'AC', r.ac.total, Object.values(r.saves).map(s => f(s.total)), 'perc', f(r.perception.total), 'init', f(r.initiative.total));
console.log(r.strikes.map(s => s.name + ' ' + s.map.map(f).join('/') + ' ' + s.formula));
console.log('pending', r.pending.filter(p => p.value == null).map(p => p.item.r.n + ': ' + p.prompt));
for (const s of r.slots) if (s.kind !== 'boost' && s.kind !== 'increase') { const ff = ch.feats[s.id]; if (ff) { const rr = db.e[ff.k]; const pr = eng.prereqs(r, rr).filter(p => p.ok === false); if (pr.length) console.log('prereq', s.id, rr.n, pr.map(p => p.text)); } }
console.log('skills', Object.entries(r.skills).filter(([k, v]) => v.rank).map(([k, v]) => k + f(v.total)).join(' '));
