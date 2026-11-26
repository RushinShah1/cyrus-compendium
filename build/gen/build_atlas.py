"""Tactical grid atlas: flanking and Expansive Spellstrike areas, computed from the PF2e rules and drawn in one style."""
import html as H
from kit import ic
from build_items import rules_box, table
from grid import (Grid, fig, COL, space, flank_squares, burst, cone, line, origin_point, DIRS, in_reach10, corner_cone)


# ───────────── keys ─────────────
def sw(kind, label):
    g = {
        'C': f'<circle cx="10" cy="10" r="8" fill="none" stroke="{COL["C"]}" stroke-width="1.8"/><text x="10" y="10.5" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="700" fill="{COL["C"]}">C</text>',
        'A': f'<circle cx="10" cy="10" r="8" fill="none" stroke="{COL["A"]}" stroke-width="1.8"/><text x="10" y="10.5" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="700" fill="{COL["A"]}">A</text>',
        'E': f'<circle cx="10" cy="10" r="8" fill="none" stroke="{COL["E"]}" stroke-width="1.8"/><text x="10" y="10.5" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="700" fill="{COL["E"]}">E</text>',
        'T': f'<rect x="1" y="1" width="18" height="18" rx="2" fill="{COL["tgt_f"]}" stroke="{COL["tgt_s"]}" stroke-width="1.6"/><circle cx="10" cy="10" r="7.5" fill="none" stroke="{COL["T"]}" stroke-width="1.5"/><text x="10" y="10.5" text-anchor="middle" dominant-baseline="central" font-size="9" font-weight="700" fill="{COL["T"]}">T</text>',
        'f5': f'<rect x="1" y="1" width="18" height="18" rx="2" fill="{COL["flank"]}"/><text x="10" y="10.5" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="700" fill="{COL["A"]}">5</text>',
        'f10': f'<rect x="1" y="1" width="18" height="18" rx="2" fill="{COL["reach"]}"/><text x="10" y="10.5" text-anchor="middle" dominant-baseline="central" font-size="9" font-weight="700" fill="{COL["C"]}">10</text>',
        'warn': '<circle cx="10" cy="10" r="8.5" fill="#5a2e35" stroke="#ee8f8f" stroke-width="1.5"/><path d="M10 5.2v6" stroke="#ee8f8f" stroke-width="2.2" stroke-linecap="round"/><circle cx="10" cy="14.4" r="1.3" fill="#ee8f8f"/>',
        'reachsq': f'<rect x="1" y="1" width="18" height="18" rx="2" fill="{COL["reach"]}"/>',
        'flanksq': f'<rect x="1" y="1" width="18" height="18" rx="2" fill="{COL["flank"]}"/>',
        'range': f'<rect x="1.5" y="1.5" width="17" height="17" rx="2" fill="{COL["range"]}" stroke="#4a4a55"/>',
        'area': f'<rect x="1" y="1" width="18" height="18" rx="2" fill="{COL["area"]}"/>',
        'src': f'<rect x="2" y="2" width="16" height="16" rx="2" fill="{COL["src_f"]}" stroke="{COL["src_s"]}" stroke-width="1.8"/>',
        'dia': f'<path d="M10 3.5L16.5 10L10 16.5L3.5 10Z" fill="{COL["ink"]}" stroke="{COL["dark"]}" stroke-width="1.4"/>',
        'arrow': f'<path d="M3 17L13.5 6.5" stroke="{COL["gold"]}" stroke-width="1.8"/><path d="M17 3L9.6 5.6L14.4 10.4Z" fill="{COL["gold"]}"/>',
        'ring': f'<circle cx="10" cy="10" r="5.5" fill="#1d1d21" stroke="{COL["A"]}" stroke-width="1.8"/>',
        'xring': f'<circle cx="10" cy="10" r="5.5" fill="#1d1d21" stroke="{COL["grey"]}" stroke-width="1.8"/><path d="M7 7L13 13M13 7L7 13" stroke="{COL["grey"]}" stroke-width="1.5"/>',
    }[kind]
    return f'<span class="lg"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" font-family="Alegreya Sans,sans-serif">{g}</svg>{label}</span>'


def key(*items):
    return '<div class="keyrow">' + ''.join(sw(a, b) for a, b in items) + '</div>'


TOKENS = (('C', 'Cyrus'), ('A', 'Ally'), ('T', 'Strike target and its space'), ('E', 'Other enemy'))


def sub(t, body=''):
    return f'<h3 class="ah">{t}</h3>' + (f'<p class="prose">{body}</p>' if body else '')


def figs(items, cols):
    return f'<div class="figs c{cols}">{"".join(items)}</div>'


# ───────────── flanking ─────────────
def flank_fig(size, ally, title, ally_desc):
    m = 3
    tx = ty = m
    n = size + 2 * m
    tsp = space(tx, ty, size)
    ax, ay = tx + ally[0], ty + ally[1]
    fs = flank_squares(tsp, (ax, ay), (0, 0, n, n))
    g = Grid(n, n, title)
    for p, r in fs.items():
        g.shade([p], COL['flank'] if r == 5 else COL['reach']).label(p, str(r), COL['A'] if r == 5 else COL['C'])
    g.target(tx, ty, size).token(ax, ay, 'A')
    return fig(g, title, f'{ally_desc} {len(fs)} flanking squares.')


def flank_section():
    med = [flank_fig(1, (1, 0), 'Ally beside an edge', 'Ally adjacent on the east.'),
           flank_fig(1, (1, -1), 'Ally at a corner', 'Ally diagonal to the target.'),
           flank_fig(1, (2, 0), 'Ally with reach', 'Ally 10 feet east.')]
    lg = [flank_fig(2, (2, 0), 'Ally beside an edge', 'Ally adjacent on the east, upper row.'),
          flank_fig(2, (2, -1), 'Ally at a corner', 'Ally diagonal to the target.')]
    hg = [flank_fig(3, (3, 1), 'Ally at the middle of an edge', 'Ally adjacent on the east, middle row.'),
          flank_fig(3, (3, 0), 'Ally at the end of an edge', 'Ally adjacent on the east, top row.'),
          flank_fig(3, (3, -1), 'Ally at a corner', 'Ally diagonal to the target.')]
    return f'''<h2 id="at-flank">{ic("flank")}Flanking at 10-foot reach</h2>
<p class="prose">Coloured squares are where Cyrus flanks with the ally shown, numbered by the reach he needs. Rotate or mirror a grid to match the ally's side.</p>
{key(('f5', 'Flank at 5 ft'), ('f10', 'Flank at 10 ft'), ('A', 'Ally'), ('T', 'Target and its space'))}
{sub("Medium or smaller")}{figs(med, 3)}
{sub("Large")}{figs(lg, 3)}
{sub("Huge")}{figs(hg, 3)}
{rules_box(2375, "Flanking")}'''


# ───────────── bursts ─────────────
def corners(tsp):
    xs = [p[0] for p in tsp]; ys = [p[1] for p in tsp]
    return [(x, y) for x in range(min(xs), max(xs) + 2) for y in range(min(ys), max(ys) + 2)]


def clean_corners(tsp, keep, r):
    return [c for c in corners(tsp) if not (burst(*c, r) & set(keep))]


def burst_fig(size, cpos, apos, r, title, enemies=(), ally=True):
    m = r // 5 + 2
    tx = ty = m
    n = size + 2 * m
    tsp = space(tx, ty, size)
    C = (tx + cpos[0], ty + cpos[1]); A = (tx + apos[0], ty + apos[1])
    keep = [C, A] if ally else [C]
    ok = clean_corners(tsp, keep, r)
    spare_c = clean_corners(tsp, [C], r)
    pool = ok or spare_c or corners(tsp)
    chosen = max(pool, key=lambda c: (abs(c[0] + .0 - C[0] - .5) + abs(c[1] - C[1] - .5)))
    area = burst(*chosen, r)
    g = Grid(n, n, title)
    g.shade(area, COL['area'])
    g.target(tx, ty, size).token(*C, 'C')
    if ally:
        g.token(*A, 'A')
    for e in enemies:
        g.token(tx + e[0], ty + e[1], 'E')
    for c in corners(tsp):
        if c != chosen:
            g.ring(c[0], c[1], c in ok)
    g.diamond(*chosen)
    warn = ally and A in area
    who = 'Cyrus and the ally' if ally else 'Cyrus'
    cap = f'{len(ok)} of {len(corners(tsp))} corners keep {who} out.'
    if warn:
        cap += ' The corner shown spares Cyrus but catches the ally.'
    return fig(g, title, cap, warn=warn)


def clean_corners(tsp, keep, r):
    return [c for c in corners(tsp) if not (burst(*c, r) & set(keep))]


BURST_CASES = [
    ('Medium target, straight line', 1, (-2, 0), (1, 0), 10, [(1, 1)]),
    ('Medium target, Cyrus off the line', 1, (-2, -1), (1, 0), 10, [(1, 1)]),
    ('Medium target, diagonal', 1, (-2, -2), (1, 1), 10, [(1, -1)]),
    ('Large target, straight line', 2, (-2, 0), (2, 0), 10, [(1, 2)]),
    ('Huge target, straight line', 3, (-2, 1), (3, 1), 15, [(3, 4)]),
]


def burst_section():
    t, size, c, a, r, en = BURST_CASES[0]
    pair = (f'<h4 class="th">{t}, {r}-foot burst</h4>'
            + figs([burst_fig(size, c, a, r, 'Without an ally', enemies=en, ally=False),
                    burst_fig(size, c, a, r, 'With a flanking ally', enemies=en, ally=True)], 2))
    singles = figs([burst_fig(size, c, a, r, f'{t}, {r}-foot burst', enemies=en, ally=True)
                    for t, size, c, a, r, en in BURST_CASES[1:]], 2)
    rows = []
    for name, size, c, a, _, _ in BURST_CASES:
        tsp = space(10, 10, size)
        C = (10 + c[0], 10 + c[1]); A = (10 + a[0], 10 + a[1])
        rows.append([name] + [f'{len(clean_corners(tsp, [C], r))} / {len(clean_corners(tsp, [C, A], r))} / {len(corners(tsp))}' for r in (10, 15, 20, 30)])
    tbl = table(['Position', '10-ft', '15-ft', '20-ft', '30-ft'], rows, num=(1, 2, 3, 4))
    return f'''<h2 id="at-burst">{ic("burst")}Expansive Spellstrike: bursts</h2>
<p class="prose">The burst centres on any corner of the target's space. Rings mark every corner; the diamond is the corner shown. In a straight flank an adjacent ally touches both far corners, so the corner that spares Cyrus catches the ally; stepping off the line opens clean corners.</p>
{key(*TOKENS, ('dia', 'Corner shown'), ('ring', 'Corner that spares everyone shown'), ('xring', 'Corner that catches Cyrus or the ally'), ('area', 'Area'), ('warn', 'Friendly fire'))}
{pair}
<h4 class="th">With a flanking ally</h4>{singles}
<h4 class="th">Clean corners: sparing Cyrus / sparing Cyrus and the ally / total</h4>{tbl}
{rules_box(2385, "Burst")}'''


# ───────────── cones and lines ─────────────
def placements(tsp, kind, L, keep, bounds):
    """All (source, direction) placements that include the target; returns (safe, total)."""
    srcs = {(x, y) for (px, py) in tsp for x in range(px - 1, px + 2) for y in range(py - 1, py + 2)} - tsp
    tot, safe = [], []
    for s in srcs:
        for d in DIRS:
            straight = d in ('N', 'S', 'E', 'W')
            sides = (1, -1) if kind == 'cone' and straight and corner_cone(L) else (1,)
            for side in sides:
                a = cone(s, d, L, side) if kind == 'cone' else line(s, d, L)
                if not (a & tsp):
                    continue
                tot.append((s, d, side))
                if not (a & set(keep)) and s not in keep:
                    safe.append((s, d, side, a))
    return safe, tot


def area_fig(kind, size, cpos, apos, L, title, src, d, enemies=(), n=None, pad=1, side=1):
    tx = ty = pad + 2
    tsp = space(tx, ty, size)
    S0 = (tx + src[0], ty + src[1])
    area = cone(S0, d, L, side) if kind == 'cone' else line(S0, d, L)
    C = (tx + cpos[0], ty + cpos[1]); A = (tx + apos[0], ty + apos[1])
    assert area & tsp, title
    assert not (area & {C, A}), title
    allp = area | tsp | {C, A, S0}
    w = n[0] if n else max(p[0] for p in allp) + 2
    h = n[1] if n else max(p[1] for p in allp) + 2
    g = Grid(w, h, title)
    g.shade(area, COL['area']).source(*S0)
    g.target(tx, ty, size).token(*C, 'C').token(*A, 'A')
    for e in enemies:
        g.token(tx + e[0], ty + e[1], 'E')
    ox, oy = origin_point(S0, d, L if kind == 'cone' else 0, side)
    g.diamond(ox, oy)
    dx, dy = DIRS[d]
    g.arrow(ox + dx * .12, oy + dy * .12, ox + dx * .62, oy + dy * .62)
    return fig(g, title)


def shape_fig(kind, d, L):
    f = (cone if kind == 'cone' else line)
    s0 = (0, 0)
    a = cone(s0, d, L) if kind == 'cone' else line(s0, d, L)
    pts = a | {s0}
    x0 = min(p[0] for p in pts) - 1; y0 = min(p[1] for p in pts) - 1
    a = {(p[0] - x0, p[1] - y0) for p in a}
    S0 = (-x0, -y0)
    w = max(p[0] for p in a | {S0}) + 2; h = max(p[1] for p in a | {S0}) + 2
    g = Grid(w, h, f'{L}-foot {kind}')
    g.shade(a, COL['area']).source(*S0)
    ox, oy = origin_point(S0, d, L if kind == 'cone' else 0)
    g.diamond(ox, oy)
    return fig(g, f'{L} ft, {"straight" if d in ("N", "S", "E", "W") else "diagonal"}', f'{len(a)} squares')


def count_table(kind, lengths):
    rows = []
    for name, size, c, a in [('Medium', 1, (-2, 0), (1, 0)), ('Large', 2, (-2, 0), (2, 0)), ('Huge', 3, (-2, 1), (3, 1))]:
        tsp = space(20, 20, size)
        C = (20 + c[0], 20 + c[1]); A = (20 + a[0], 20 + a[1])
        rows.append([name] + [f'{len(placements(tsp, kind, L, [C, A], None)[0])} / {len(placements(tsp, kind, L, [C, A], None)[1])}' for L in lengths])
    return table(['Target'] + [f'{L}-ft {kind}' for L in lengths], rows, num=tuple(range(1, len(lengths) + 1)))


def cone_section():
    shapes = [shape_fig('cone', 'S', 15), shape_fig('cone', 'S', 30), shape_fig('cone', 'SE', 15), shape_fig('cone', 'SE', 30)]
    ex = [area_fig('cone', 1, (-2, 0), (1, 0), 15, 'Medium target, 15-foot cone from the north', (0, -1), 'S', enemies=[(1, 2)]),
          area_fig('cone', 1, (-2, 0), (1, 0), 30, 'Medium target, 30-foot cone from the north', (0, -1), 'S', enemies=[(1, 3), (-1, 4)], side=-1),
          area_fig('cone', 2, (-2, 0), (2, 0), 30, 'Large target, straight cone from the north', (0, -1), 'S', enemies=[(-2, 3), (3, 2)]),
          area_fig('cone', 2, (-2, 0), (2, 0), 30, 'Large target, diagonal cone from the west', (-1, 0), 'SE', enemies=[(2, 3), (0, 5)]),
          area_fig('cone', 3, (-2, 1), (3, 1), 30, 'Huge target, straight cone from the north', (1, -1), 'S', enemies=[(3, 3), (-2, 4)], side=-1),
          area_fig('cone', 3, (-2, 1), (3, 1), 30, 'Huge target, diagonal cone from the west', (-1, 1), 'SE', enemies=[(2, 4), (4, 3)])]
    return f'''<h2 id="at-cone">{ic("cone")}Expansive Spellstrike: cones</h2>
<p class="prose">At 10 feet of reach the cone comes from a source square adjacent to the target, and it must include one of the target's squares. Shapes follow the Player Core areas diagram: a 15-foot straight cone starts at the middle of the source square's edge, longer straight cones start at a corner of that edge, and diagonal cones start at the source square's corner. On a grid a cone is aimed straight or diagonally; there are no angles in between.</p>
{key(('src', 'Source square'), ('dia', 'Point of origin'), ('arrow', 'Aim'), ('area', 'Area'))}
{sub("Shapes")}{figs(shapes, 4)}
{sub("Placements that spare Cyrus and the ally", "Cyrus is two squares west of the target and the ally is adjacent on the east, so they flank.")}
{key(*TOKENS)}
{figs(ex, 2)}
<h4 class="th">Safe placements out of all that include the target</h4>{count_table('cone', (15, 30, 60))}
{rules_box(2386, "Cone")}'''


def sprint_fig():
    # Cyrus starts west, moves east through two enemies and the target's space, and ends 10 feet past it.
    g = Grid(14, 5, 'Sprinting Spellstrike with Expansive Spellstrike')
    path = {(x, 2) for x in range(1, 10)}
    g.shade(path, COL['area'])
    g.target(8, 2, 1)
    g.token(0, 2, 'C', ghost=True).token(3, 2, 'E').token(5, 2, 'E').token(10, 2, 'C').token(9, 1, 'A')
    g.diamond(1, 2.5)
    g.arrow(1.05, 2.5, 10.1, 2.5)
    return fig(g, 'Sprinting Spellstrike', 'Cyrus Strides in a straight line through both enemies and the target, ending 10 feet past it. With Expansive Spellstrike the line follows his movement, so everything he passed through is in the area.')


def line_section():
    shapes = [shape_fig('line', 'S', 30), shape_fig('line', 'SE', 30), shape_fig('line', 'S', 60), shape_fig('line', 'SE', 60)]
    ex = [area_fig('line', 1, (-2, 0), (1, 0), 60, 'Medium target, line from the north', (0, -1), 'S', enemies=[(0, 3), (0, 6)], n=(6, 15)),
          area_fig('line', 2, (-2, 0), (2, 0), 60, 'Large target, diagonal line', (-1, -1), 'SE', enemies=[(3, 3), (5, 5)])]
    return f'''<h2 id="at-line">{ic("line")}Lines</h2>
<p class="prose">A line is 5 feet wide unless the spell says otherwise. Through Expansive Spellstrike it starts from a source square adjacent to the target and must pass through one of the target's squares.</p>
{key(('src', 'Source square'), ('dia', 'Point of origin'), ('arrow', 'Aim'), ('area', 'Area'))}
{sub("Shapes")}{figs(shapes, 4)}
{sub("Expansive Spellstrike lines")}
{key(*TOKENS)}
{figs(ex, 2)}
<h4 class="th">Safe placements out of all that include the target</h4>{count_table('line', (30, 60, 120))}
{sub("Sprinting Spellstrike")}
{figs([sprint_fig()], 1)}
{rules_box(2388, "Line")}{rules_box(2381, "Areas")}
<p class="muted small">Foundry may highlight slightly different squares from these diagrams; discuss with the DM which area templates will be used.</p>'''


def atlas_page():
    nav = ''.join(f'<a href="#" data-to="{a}">{b}</a>' for a, b in [('at-flank', 'Flanking'), ('at-burst', 'Bursts'), ('at-cone', 'Cones'), ('at-line', 'Lines')])
    page = f'''<div class="page doc" data-page="atlas">
<header class="ph"><h1>Tactical grid atlas</h1>
<p class="lede">Flanking squares at Aspera's 10-foot reach, and placements for Expansive Spellstrike areas that hit the target and spare the party. Every grid square is 5 feet.</p></header>
<nav class="jumpbar scroll">{nav}</nav>
{flank_section()}
{burst_section()}
{cone_section()}
{line_section()}
</div>'''
    open('/home/claude/site/pages/atlas.html', 'w').write(page)


if __name__ == '__main__':
    atlas_page()
    print('ok')
