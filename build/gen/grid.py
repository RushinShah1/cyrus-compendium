"""Grid diagrams for the atlas and combat pages: geometry (PF2e area and flanking rules) and one SVG style."""
import html as H

S = 30  # pixels per 5-foot square
COL = dict(cell='#26262b', line='#3c3c43', bg='#1d1d21', reach='#33405a', flank='#2b3d31', area='#3b3550',
           range='#363642', tgt_f='#57452a', tgt_s='#d9a35b', src_f='#24413f', src_s='#8fd3c4',
           C='#a6bdf0', A='#9fd5a4', E='#e9d88f', T='#ee8f8f', gold='#e3c37b', ink='#ebe6de', dark='#17171a', grey='#8a857d')


# ───────────── geometry ─────────────
def dist_sq(dx, dy):
    """Distance in squares by the PF2e alternating-diagonal rule (each value is a count of squares moved)."""
    a, b = sorted((abs(dx), abs(dy)))
    return b + a // 2


def ft(dx, dy):
    return 5 * dist_sq(dx, dy)


def space(x, y, size=1):
    return {(x + i, y + j) for i in range(size) for j in range(size)}


def cheb_to_space(p, sp):
    return min(max(abs(p[0] - q[0]), abs(p[1] - q[1])) for q in sp)


def in_reach10(p, sp):
    """10-foot reach includes two squares diagonally."""
    return cheb_to_space(p, sp) <= 2


def burst(gx, gy, r):
    """Squares in a burst of radius r feet centred on grid point (gx, gy)."""
    n = r // 5
    out = set()
    for i in range(gx - n - 1, gx + n + 1):
        for j in range(gy - n - 1, gy + n + 1):
            dx = i - gx + 1 if i >= gx else gx - i
            dy = j - gy + 1 if j >= gy else gy - j
            if 5 * dist_sq(dx, dy) <= r:
                out.add((i, j))
    return out


DIRS = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0), 'NE': (1, -1), 'NW': (-1, -1), 'SE': (1, 1), 'SW': (-1, 1)}


def corner_cone(L):
    """Straight cones of 30 feet and more start from a grid corner in the Player Core areas diagram (2, 4, 6... squares wide)."""
    return L > 15


def cone(src, d, L, side=1):
    """Squares of a cone of length L aimed in direction d from source square src (the source is not included).
    A 15-foot straight cone starts at the middle of the source square's edge; longer straight cones start at the
    corner of that edge on the given side (+1 or -1), matching the published diagram."""
    sx, sy = src
    dx, dy = DIRS[d]
    n = L // 5
    out = set()
    if dx == 0 or dy == 0:
        for f in range(1, n + 1):
            if corner_cone(L):
                lats = [k - 1 for k in range(1, f + 1) if dist_sq(f, k) <= n] + [-k for k in range(1, f + 1) if dist_sq(f, k) <= n]
                lats = [l + (1 if side > 0 else 0) for l in lats]
            else:
                lats = [l for l in range(-(f - 1), f) if dist_sq(f, l) <= n]
            for lat in lats:
                if dx == 0:
                    out.add((sx + lat, sy + dy * f))
                else:
                    out.add((sx + dx * f, sy + lat))
    else:
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                if 5 * dist_sq(a, b) <= L:
                    out.add((sx + dx * a, sy + dy * b))
    return out


def line(src, d, L):
    sx, sy = src
    dx, dy = DIRS[d]
    out = set()
    k = 1
    while 5 * dist_sq(k * dx, k * dy) <= L:
        out.add((sx + dx * k, sy + dy * k))
        k += 1
    return out


def origin_point(src, d, L=0, side=1):
    """Where the area starts: the middle of the source square's edge, its corner for a diagonal, or the edge's corner
    for straight cones longer than 15 feet."""
    sx, sy = src
    dx, dy = DIRS[d]
    if (dx == 0 or dy == 0) and L and corner_cone(L):
        off = 1 if side > 0 else 0
        return (sx + off, sy + .5 + dy * .5) if dx == 0 else (sx + .5 + dx * .5, sy + off)
    return (sx + .5 + dx * .5, sy + .5 + dy * .5)


def flanks(c, a, sp):
    """True if the line between the centres of c and a passes through opposite sides or corners of space sp."""
    x0 = min(p[0] for p in sp); x1 = max(p[0] for p in sp) + 1
    y0 = min(p[1] for p in sp); y1 = max(p[1] for p in sp) + 1
    P = (c[0] + .5, c[1] + .5); Q = (a[0] + .5, a[1] + .5)
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, P[0] - x0), (dx, x1 - P[0]), (-dy, P[1] - y0), (dy, y1 - P[1])):
        if abs(p) < 1e-12:
            if q < 0:
                return False
            continue
        t = q / p
        if p < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t1 - t0 < 1e-9:
        return False

    def sides(t):
        x, y = P[0] + dx * t, P[1] + dy * t
        s = set()
        if abs(x - x0) < 1e-9: s.add('L')
        if abs(x - x1) < 1e-9: s.add('R')
        if abs(y - y0) < 1e-9: s.add('T')
        if abs(y - y1) < 1e-9: s.add('B')
        return s
    e, x = sides(t0), sides(t1)
    return ('L' in e and 'R' in x) or ('R' in e and 'L' in x) or ('T' in e and 'B' in x) or ('B' in e and 'T' in x)


def flank_squares(tsp, ally, bounds, blocked=()):
    """Squares within 10-foot reach of the target from which Cyrus flanks with the ally. Returns {square: 5 or 10}."""
    (bx0, by0, bx1, by1) = bounds
    out = {}
    for x in range(bx0, bx1):
        for y in range(by0, by1):
            p = (x, y)
            if p in tsp or p == ally or p in blocked or not in_reach10(p, tsp):
                continue
            if flanks(p, ally, tsp):
                out[p] = 5 if cheb_to_space(p, tsp) == 1 else 10
    return out


# ───────────── drawing ─────────────
class Grid:
    def __init__(self, cols, rows, title=''):
        self.cols, self.rows, self.title = cols, rows, title
        self.fill = {}
        self.labels = {}
        self.extra = []
        self.mid = []
        self.top = []

    def shade(self, squares, colour):
        for p in squares:
            if 0 <= p[0] < self.cols and 0 <= p[1] < self.rows:
                self.fill[p] = colour
        return self

    def label(self, p, text, colour):
        self.labels[p] = (text, colour)
        return self

    def target(self, x, y, size=1):
        self.shade(space(x, y, size), COL['tgt_f'])
        self.extra.append(f'<rect x="{x * S + 1}" y="{y * S + 1}" width="{size * S - 2}" height="{size * S - 2}" rx="2" fill="none" '
                          f'stroke="{COL["tgt_s"]}" stroke-width="2"/>')
        self.token(x + (size - 1) / 2, y + (size - 1) / 2, 'T', size=size)
        return self

    def token(self, x, y, letter, colour=None, ghost=False, size=1):
        """A creature: an outlined circle with its letter, spanning its whole space."""
        c = colour or COL.get(letter, COL['ink'])
        if ghost:
            c = COL['grey']
        cx, cy = x * S + S / 2, y * S + S / 2
        r = size * S / 2 - 4
        fs = {1: 14, 2: 19}.get(size, 14 + 8 * (size - 1))
        ly = cy + (S / 2 if size % 2 == 0 else 0)  # keep the letter off the corner at the centre of an even-sized space
        self.top.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="{2 if size == 1 else 2.4}"'
                        + (' stroke-dasharray="4 3"' if ghost else '') + '/>'
                        f'<text x="{cx}" y="{ly + .5}" text-anchor="middle" dominant-baseline="central" font-size="{fs}" font-weight="700" fill="{c}">{letter}</text>')
        return self

    def source(self, x, y):
        self.fill[(x, y)] = COL['src_f']
        self.extra.append(f'<rect x="{x * S + 2}" y="{y * S + 2}" width="{S - 4}" height="{S - 4}" rx="2" fill="none" stroke="{COL["src_s"]}" stroke-width="2"/>')
        return self

    def diamond(self, px, py):
        """Origin marker at grid coordinates (corner = integers, edge centre = half-integers)."""
        X, Y, r = px * S, py * S, 6.5
        self.top.append(f'<path d="M{X} {Y - r}L{X + r} {Y}L{X} {Y + r}L{X - r} {Y}Z" fill="{COL["ink"]}" stroke="{COL["dark"]}" stroke-width="1.6"/>')
        return self

    def ring(self, px, py, ok):
        X, Y = px * S, py * S
        c = COL['A'] if ok else COL['grey']
        s = f'<circle cx="{X}" cy="{Y}" r="5.5" fill="{COL["bg"]}" stroke="{c}" stroke-width="1.8"/>'
        if not ok:
            s += f'<path d="M{X - 3} {Y - 3}L{X + 3} {Y + 3}M{X + 3} {Y - 3}L{X - 3} {Y + 3}" stroke="{c}" stroke-width="1.5"/>'
        self.mid.append(s)
        return self

    def arrow(self, x1, y1, x2, y2, colour=None, dash=False):
        c = colour or COL['gold']
        mid = 'ah' + c.strip('#')
        self.extra.append(f'<path d="M{x1 * S} {y1 * S}L{x2 * S} {y2 * S}" stroke="{c}" stroke-width="2" fill="none" marker-end="url(#{mid})"'
                          + (' stroke-dasharray="5 4"' if dash else '') + '/>')
        self._markers = getattr(self, '_markers', set()) | {c}
        return self

    def seg(self, x1, y1, x2, y2, colour, dash=True):
        self.extra.append(f'<path d="M{x1 * S} {y1 * S}L{x2 * S} {y2 * S}" stroke="{colour}" stroke-width="2" fill="none"'
                          + (' stroke-dasharray="5 4"' if dash else '') + '/>')
        return self

    def box(self, x, y, w, h, colour, dash=True):
        self.extra.append(f'<rect x="{x * S + 1.5}" y="{y * S + 1.5}" width="{w * S - 3}" height="{h * S - 3}" rx="3" fill="none" stroke="{colour}" stroke-width="2"'
                          + (' stroke-dasharray="5 4"' if dash else '') + '/>')
        return self

    def svg(self):
        W, Hh = self.cols * S, self.rows * S
        o = [f'<rect width="{W}" height="{Hh}" fill="{COL["cell"]}"/>']
        for (x, y), f in self.fill.items():
            o.append(f'<rect x="{x * S}" y="{y * S}" width="{S}" height="{S}" fill="{f}"/>')
        for i in range(self.cols + 1):
            o.append(f'<path d="M{i * S} 0V{Hh}" stroke="{COL["line"]}"/>')
        for j in range(self.rows + 1):
            o.append(f'<path d="M0 {j * S}H{W}" stroke="{COL["line"]}"/>')
        for (x, y), (t, c) in self.labels.items():
            o.append(f'<text x="{x * S + S / 2}" y="{y * S + S / 2 + .5}" text-anchor="middle" dominant-baseline="central" font-size="12.5" font-weight="700" fill="{c}">{t}</text>')
        o += self.extra + self.mid + self.top
        marks = ''.join(f'<marker id="ah{c.strip("#")}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                        f'<path d="M0 0L10 5L0 10Z" fill="{c}"/></marker>' for c in getattr(self, '_markers', ()))
        return (f'<svg class="dg" viewBox="-2 -2 {W + 4} {Hh + 4}" width="{W + 4}" role="img" aria-label="{H.escape(self.title)}" '
                f'xmlns="http://www.w3.org/2000/svg" font-family="Alegreya Sans, sans-serif"><defs>{marks}</defs>{"".join(o)}</svg>')


WARN = ('<span class="ff" role="img" aria-label="Friendly fire: the ally is in the area" title="Friendly fire: the ally is in the area">'
        '<svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="#5a2e35" stroke="#ee8f8f" stroke-width="1.6"/>'
        '<path d="M10 5v6.2" stroke="#ee8f8f" stroke-width="2.4" stroke-linecap="round"/><circle cx="10" cy="14.6" r="1.4" fill="#ee8f8f"/></svg></span>')


def fig(grid, title, cap='', warn=False):
    return (f'<figure class="fig gfig"><figcaption><b>{H.escape(title)}</b>{WARN if warn else ""}</figcaption>{grid.svg()}'
            + (f'<p>{cap}</p>' if cap else '') + '</figure>')
