const {loadDB, E} = require('./load.js');
const db = loadDB(); const eng = new E.Engine(db);
const ch = JSON.parse(require('fs').readFileSync('/home/claude/site/assets/cs/cyrus.json'));
for (const L of [16, 17]) { ch.level = L; const r = eng.compute(ch); console.log(L, 'arcana', r.skills.arcana.total, (r.skills.arcana.mods||[]).filter(m=>/Aspera/.test(m.label||'')).map(m=>m.label+':'+m.value+(m.enabled===false?' off':'')), 'society', r.skills.society.total); }
