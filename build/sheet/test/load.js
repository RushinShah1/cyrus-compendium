const fs = require('fs');
const D = '/home/claude/site/assets/cs/';
function loadDB(){
  const db = {e: {}};
  for (const f of ['core', 'feats', 'actions', 'items', 'spells', 'effects']) {
    const j = JSON.parse(fs.readFileSync(D + f + '.json', 'utf8'));
    Object.assign(db.e, j.e);
    if (f === 'core') { db.slots = j.slots; db.runes = j.runes; db.lang = j.lang; }
  }
  return db;
}
module.exports = {loadDB, E: require(D + 'engine.js')};
