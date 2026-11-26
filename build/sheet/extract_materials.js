// Pull the precious material price, level, Hardness and HP tables out of the Foundry source.
const fs = require('fs');
const src = fs.readFileSync('/home/claude/pf2e/src/module/item/physical/materials.ts', 'utf8');
function grab(name) {
  const i = src.indexOf('const ' + name);
  const eq = src.indexOf('= {', i) + 2;
  let depth = 0, j = eq;
  for (; j < src.length; j++) { const c = src[j]; if (c === '{') depth++; else if (c === '}') { depth--; if (!depth) break; } }
  return eval('(' + src.slice(eq, j + 1) + ')');
}
const out = {weapon: grab('WEAPON_MATERIAL_VALUATION_DATA'), armor: grab('ARMOR_MATERIAL_VALUATION_DATA'),
  shield: grab('SHIELD_MATERIAL_VALUATION_DATA'), buckler: grab('BUCKLER_MATERIAL_VALUATION_DATA'), tower: grab('TOWER_SHIELD_MATERIAL_VALUATION_DATA')};
for (const t of Object.values(out)) { delete t['']; for (const [k, v] of Object.entries(t)) if (!Object.values(v).some(Boolean)) delete t[k]; }
fs.writeFileSync('materials.json', JSON.stringify(out));
console.log(Object.fromEntries(Object.entries(out).map(([k, v]) => [k, Object.keys(v).join(',')])));
