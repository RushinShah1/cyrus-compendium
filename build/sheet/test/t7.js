const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const ch = JSON.parse(require('fs').readFileSync('/mnt/user-data/uploads/c4e43c8b-cyrus-valdira.aspera.json'));
const R = ['U', 'T', 'E', 'M', 'L'];
for (const L of [8, 9, 12, 13, 16, 17, 20]) {
  ch.level = L; const r = eng.compute(ch);
  console.log(L, ['arcana', 'society', 'diplomacy', 'athletics', 'occultism', 'acrobatics'].map(k => k + ' ' + R[r.skills[k].rank]).join(', '), '| perception', R[r.perception.rank]);
}
