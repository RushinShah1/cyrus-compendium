const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const ch = JSON.parse(require('fs').readFileSync('/home/claude/site/assets/cs/cyrus.json'));
Object.assign(ch, {level: 9}); ch.boosts.ancestry = ['str', 'int']; ch.boosts.background = ['str', 'con']; ch.boosts.class = 'str'; ch.boosts[1] = ['str', 'dex', 'con', 'int'];
ch.effects = {'fe:stance-arcane-cascade': true};
for (const og of [false, true]) {
  ch.toggles = {'target:condition:off-guard': og};
  const r = eng.compute(ch);
  for (const s of r.strikes) console.log('off-guard', og, s.name, s.formula, s.damage.mods.map(m => m.label + ' ' + m.value + (m.applied ? '' : '(x)')).join(', '));
}
console.log(eng.spellDamage(db.e['sp:gouging-claw'], 5), eng.spellDamage(db.e['sp:heal'], 3));
