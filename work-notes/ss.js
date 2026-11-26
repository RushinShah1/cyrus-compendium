function ssPick(i) {
  const st0 = res.strikes[i]; if (!st0) return;
  const opts = ssOptions();
  const box = document.createElement('div');
  box.className = 'cs-picker cs-ss';
  const mapIdx = ch.enc.on ? Math.min(ch.enc.attacks, 2) : 0;
  const items = opts.map((o, j) => ({label: o.s.n, rec: o.s, o, j, gr: gradeOf('sp', o.s), hayx: [o.src, spellArea(o.s), spellDef(o.s), ...spellDmg(o.s)].join(' ')}));
  const avg = o => eng.spellDamage(o.s, o.rank).reduce((t, x) => t + String(x.f || '').split('+').reduce((u, p) => { const m = p.trim().match(/^(\d+)d(\d+)$/); return u + (m ? m[1] * (+m[2] + 1) / 2 : Number(p) || 0); }, 0), 0);
  const sf = spellFacets(items);
  const spec = [
    {k: 'how', label: 'Paid with', type: 'chips', opts: [['cantrip', 'Cantrip'], ['prep', 'Prepared slot'], ['spont', 'Spell slot'], ['staff', 'Stave charges'], ['focus', 'Focus Point'], ['innate', 'Innate']].filter(([v]) => items.some(it => it.o.how.type === v)), val: it => it.o.how.type},
    sf.def, sf.area, sf.dmg, sf.role, fxGrade()];
  const sorts = [['rank-', 'Rank, highest first', (a, b) => b.o.rank - a.o.rank], ['dmg', 'Average damage, highest first', (a, b) => avg(b.o) - avg(a.o)], SO_NAME, SO_GR, ...roleSorts()];
  const defs = fxDefaults(spec, sorts, {open: false});
  const st = FX.ss || (FX.ss = fxClone(defs));
  box.innerHTML = `<p class="small">Two actions. Cast a spell and make a melee Strike with ${esc(st0.name)} at ${fmt(st0.map[mapIdx])}. The Strike gains the arcane trait and counts as two attacks for your multiple attack penalty, applied after the Strike.</p>
${opts.length ? `<label class="search"><input type="search" placeholder="Search spells, damage types and areas" aria-label="Search spells" value="${esc(st.q || '')}"></label>${fxHTML(spec, st, sorts)}<p class="small muted cs-pc"></p>` : ''}<ul class="cs-sslist"></ul>`;
  const list = box.querySelector('.cs-sslist'), q = box.querySelector('input[type=search]'), count = box.querySelector('.cs-pc');
  const draw = () => {
    if (!opts.length) { list.innerHTML = '<li class="muted">No spell you can cast right now qualifies. Spellstrike needs a spell of 1 or 2 actions with a spell attack roll or a saving throw, and a slot, charge or Focus Point to cast it.</li>'; return; }
    st.q = q.value;
    const m = fxApply(items, spec, st, sorts);
    count.textContent = `${m.length} of ${items.length} spells`;
    list.innerHTML = m.map(it => {
      const o = it.o, dmg = eng.spellDamage(o.s, o.rank);
      return `<li><div class="t">${g(o.s)}${legTag(o.s)}${grBadge(it.gr)}<span class="cs-badge">${(o.s.tr || []).includes('cantrip') ? 'Cantrip, rank ' + o.rank : 'Rank ' + o.rank}</span></div>
<div class="m"><span>${esc(o.src)}</span><span>${esc(ssDefence(o))}</span>${o.s.area ? `<span>${esc(o.s.area.value + '-foot ' + o.s.area.type)}</span>` : ''}${dmg.length ? `<span>${esc(dmg.map(x => x.f + (x.t ? ' ' + x.t : '')).join(' + '))}</span>` : ''}</div>
<button type="button" class="chip hi" data-j="${it.j}">Spellstrike with ${esc(o.s.n)}</button></li>`;
    }).join('') || '<li class="muted">Nothing matches. Clear a filter or widen the search.</li>';
  };
  if (q) { let t; q.addEventListener('input', () => { clearTimeout(t); t = setTimeout(draw, 120); }); fxBind(box, spec, st, defs, items, sorts, draw); }
  box.addEventListener('click', e => {
    const b = e.target.closest('button[data-j]'); if (!b) return;
    A.popPanel(); doSpellstrike(i, opts[+b.dataset.j]); commit();
  });
  draw();
  A.pushPanel('Spellstrike', 'Choose a spell', box, 'ss:' + i);
}
