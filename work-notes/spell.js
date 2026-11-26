// spell facets shared by the add-a-spell panel and the Spellstrike chooser
const spellDef = r => (r.tr || []).includes('attack') ? 'attack' : (r.dfn && r.dfn.save && r.dfn.save.statistic) || 'none';
const spellArea = r => { const a = r.area && r.area.type; return !a ? 'none' : ['burst', 'cone', 'line', 'emanation'].includes(a) ? a : 'other'; };
const spellDmg = r => [...new Set(Object.values(r.dmg || {}).map(d => d && d.t).filter(Boolean))];
function spellFacets(items, get = it => it.rec) {
  const dts = countVals(items, it => spellDmg(get(it)));
  return {
    def: {k: 'def', label: 'Defense', type: 'chips', opts: [['attack', 'Spell attack (AC)'], ['fortitude', 'Fortitude'], ['reflex', 'Reflex'], ['will', 'Will'], ['none', 'No roll']], val: it => spellDef(get(it))},
    area: {k: 'area', label: 'Area', type: 'chips', opts: [['burst', 'Burst'], ['cone', 'Cone'], ['line', 'Line'], ['emanation', 'Emanation'], ['other', 'Other area'], ['none', 'No area']], val: it => spellArea(get(it)), hint: 'Expansive Spellstrike restores bursts, cones and lines'},
    dmg: {k: 'dmg', label: 'Damage type', type: 'chips', opts: [...dts.keys()].sort().map(v => [v, esc(cap(v))]).concat([['none', 'No damage']]), val: it => { const d = spellDmg(get(it)); return d.length ? d : ['none']; }},
    role: {k: 'role', label: 'Role', type: 'chips', opts: ROLE_NAMES.map((l, i) => [String(i), esc(l)]), hint: 'Rated 3 stars or more for that role on the Spells page', val: it => it.gr ? [...it.gr[1]].map((x, i) => +x >= 3 ? String(i) : null).filter(Boolean) : []},
  };
}
const roleSorts = () => ROLE_NAMES.map((l, i) => [`role${i}`, `${l} rating`, (a, b) => (+((b.gr || [])[1] || '000000')[i]) - (+((a.gr || [])[1] || '000000')[i])]);
function pickSpell(eid, max) {
  const e = ch.spells.entries.find(x => x.id === eid);
  const known = () => new Set(e.known || []);
  const items = Object.values(db.e).filter(r => r.t === 'spell' && !r.ritual).map(r => ({label: r.n, rec: r, gr: gradeOf('sp', r), hayx: [spellArea(r), spellDef(r), ...spellDmg(r)].join(' '), sub: recSub(r) + ' · ' + esc((r.trad || []).join(', '))}));
  const isC = r => (r.tr || []).includes('cantrip'), isF = r => (r.tr || []).includes('focus');
  const sf = spellFacets(items);
  const TRADS = ['arcane', 'divine', 'occult', 'primal'];
  const facets = [
    {k: 'rank', label: 'Rank', type: 'chips', opts: [['0', 'Cantrip'], ...Array.from({length: 10}, (_, i) => [String(i + 1), String(i + 1)])], cls: () => 'rk', val: it => isC(it.rec) ? '0' : String(it.rec.lv || 1)},
    {k: 'kind', label: 'Kind', type: 'chips', opts: [['cantrip', 'Cantrips'], ['focus', 'Focus spells'], ['spell', 'Other spells']], val: it => [isC(it.rec) ? 'cantrip' : '', isF(it.rec) ? 'focus' : '', !isC(it.rec) && !isF(it.rec) ? 'spell' : ''].filter(Boolean)},
    {k: 'trad', label: 'Tradition', type: 'chips', opts: TRADS.map(t => [t, cap(t)]), def: TRADS.includes(e.trad) ? [e.trad] : [], hint: 'Focus spells belong to no tradition and always match', val: it => (it.rec.trad || []).length ? it.rec.trad : TRADS},
    fxActs(it => it.rec.time), sf.def, sf.area, sf.dmg, sf.role, fxGrade(), FX_RAR, FX_TR, fxSrc(items),
    {k: 'cast', type: 'toggle', text: `Rank ${Math.max(1, max)} or lower`, def: true, test: it => isC(it.rec) || (it.rec.lv || 1) <= Math.max(1, max)},
    {k: 'ss', type: 'toggle', text: 'Works with Spellstrike', def: false, test: it => ssEligible(it.rec)},
    {k: 'kn', type: 'toggle', text: 'Hide spells already added', def: false, test: it => !known().has(it.rec.k)},
    FX_LEG];
  const sorts = [SO_NAME, ['rank', 'Rank, lowest first', (a, b) => (isC(a.rec) ? 0 : a.rec.lv || 1) - (isC(b.rec) ? 0 : b.rec.lv || 1)], ['rank-', 'Rank, highest first', (a, b) => (isC(b.rec) ? 0 : b.rec.lv || 1) - (isC(a.rec) ? 0 : a.rec.lv || 1)],
    SO_GR, ...roleSorts(), ['act', 'Action cost', (a, b) => actCost(a.rec.time) - actCost(b.rec.time)], ['def', 'Defense', (a, b) => spellDef(a.rec).localeCompare(spellDef(b.rec))]];
  for (const it of items) it.tag = '';
  const mark = () => { const kn = known(); for (const it of items) it.tag = kn.has(it.rec.k) ? ' <span class="cs-badge">Added</span>' : ''; };
  mark();
  picker('Add a spell', e.name, items, it => { e.known = e.known || []; if (!e.known.includes(it.rec.k)) e.known.push(it.rec.k); commit(); },
    {verb: 'Add', keepOpen: true, key: 'spell:' + eid, facets, sorts, redrawOnPick: mark, placeholder: 'Search names, traits and sources, such as fire cone'});
}
