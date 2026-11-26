// Pull the rune tables out of the Foundry source as plain data.
const fs = require('fs');
const src = fs.readFileSync('/home/claude/pf2e/src/module/item/physical/runes.ts', 'utf8');
function grab(name){
  const i = src.indexOf('const ' + name);
  const eq = src.indexOf('= {', i) + 2;
  let depth = 0, j = eq;
  for (; j < src.length; j++){ const c = src[j]; if (c === '{') depth++; else if (c === '}') { depth--; if (!depth) break; } }
  let body = src.slice(eq, j + 1);
  body = body.replace(/ as const/g, '').replace(/satisfies [^,\n]+/g, '')
    .replace(/\(([^()]*)\)\s*:\s*[\w<>| ]+\s*=>/g, (m, a) => '(' + a.split(',').map(x => x.split(':')[0]).join(',') + ') =>')
    .replace(/\)\s+as\s+\w+/g, ')');
  return body;
}
function Predicate(...a){ return a.length === 1 && Array.isArray(a[0]) ? a[0] : a; }
const out = {};
for (const n of ['FUNDAMENTAL_ARMOR_RUNE_DATA', 'FUNDAMENTAL_WEAPON_RUNE_DATA', 'FUNDAMENTAL_SHIELD_RUNE_DATA', 'ARMOR_PROPERTY_RUNES', 'WEAPON_PROPERTY_RUNES']) {
  const body = grab(n);
  try { out[n] = eval('(' + body + ')'); }
  catch (e) { console.error(n, e.message); }
}
fs.writeFileSync('runes.json', JSON.stringify(out));
console.log(Object.fromEntries(Object.entries(out).map(([k, v]) => [k, Object.keys(v).length])));
console.log(JSON.stringify(out.FUNDAMENTAL_WEAPON_RUNE_DATA).slice(0, 600));
