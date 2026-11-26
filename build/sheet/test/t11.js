const {loadDB, E} = require('./load.js');
const eng = new E.Engine(loadDB());
const ch = JSON.parse(require('fs').readFileSync('/mnt/user-data/uploads/c4e43c8b-cyrus-valdira.aspera.json'));
const show = (lab) => { const r = eng.compute(ch); console.log(lab, 'INT', r.attributes.int, 'STR', r.attributes.str, 'apex', r.apex && r.apex.name, 'extra', r.apexExtra, 'arcana', r.skills.arcana.total, 'HP', r.hp.total); };
show('none');
ch.inventory.push({id: 'a1', k: 'eq:sash-of-books', qty: 1, eq: 'worn', inv: true}); show('sash invested');
ch.inventory.push({id: 'a2', k: 'eq:bracers-of-hammers', qty: 1, eq: 'worn', inv: true}); show('+bracers');
ch.inventory.find(i => i.id === 'a1').inv = false; show('sash uninvested');
ch.level = 1; ch.inventory.find(i => i.id === 'a1').inv = true; ch.inventory.find(i => i.id === 'a2').inv = false; show('level 1 sash');
