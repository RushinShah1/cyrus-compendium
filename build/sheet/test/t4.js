const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const ch = JSON.parse(require('fs').readFileSync('/home/claude/site/assets/cs/cyrus.json'));
ch.level = 20; ch.boosts.ancestry = ['str', 'int']; ch.boosts.background = ['str', 'con']; ch.boosts.class = 'str'; ch.boosts[1] = ['str', 'dex', 'con', 'int'];
for (const v of [undefined, 'system.perception.rank']) {
  ch.choices['background>ft:canny-acumen'] = v ? {cannyAcumen: v} : {};
  const r = eng.compute(ch);
  console.log(v, 'perception rank', r.perception.rank, r.perception.total, r.pending.filter(p => p.flag === 'cannyAcumen').map(p => p.uid + '=' + p.value));
}
