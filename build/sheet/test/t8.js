const {loadDB, E} = require('./load.js');
const eng = new E.Engine(loadDB());
const ch = JSON.parse(require('fs').readFileSync('/mnt/user-data/uploads/c4e43c8b-cyrus-valdira.aspera.json'));
const R = ['U', 'T', 'E', 'M', 'L'];
ch.bonusSlots.push({id: 'inc-bx-15', lv: 15, kind: 'increase', label: 'Bonus skill increase'}, {id: 'inc-by-5', lv: 5, kind: 'increase', label: 'Bonus skill increase'});
ch.bonusInc = {'inc-bx-15': 'arcana', 'inc-by-5': 'arcana'};
const r = eng.compute(ch);
console.log('arcana', R[r.skills.arcana.rank], 'wasted', r.wastedInc, 'slots', r.slots.filter(s => s.kind === 'increase' && s.bonus));
