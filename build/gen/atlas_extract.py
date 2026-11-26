"""Extract diagram panels from the old atlas PDF as SVG with the new palette (geometry kept exactly)."""
import pymupdf as fitz, html as H, json

PDF = '/mnt/user-data/uploads/3c3cd73e-Cyrus_Tactical_Grid_Atlas.pdf'
MAP = {
    # fills
    '#2f556a': '#3b3550', '#4d3743': '#4a2f33', '#1f2c39': '#26262b', '#1b2731': '#1d1d21', '#ffd38b': '#e3c37b', '#234a44': '#2b3d31',
    '#2c4666': '#33405a', '#131c24': '#17171a', '#612c3d': '#5a2e35', '#285246': '#2f4a3a', '#243d60': '#2e3b55', '#744653': '#6b4248',
    '#51432f': '#4f4430', '#6f3e4a': '#643f45', '#5d4a31': '#5a4a30', '#4b3441': '#4a3238', '#253e50': '#2f3640', '#47363b': '#463539',
    # strokes
    '#394d5f': '#3c3c43', '#e0a3af': '#e8a3a3', '#a1e2b8': '#9fd5a4', '#f0aab8': '#f1a7a3', '#aec5d2': '#b9b3aa', '#96c5ff': '#a6bdf0',
    '#ffa496': '#ee9f8e', '#9ba0ac': '#8a857d', '#92d9e4': '#8fd3c4', '#dca1ae': '#e0a0a0', '#a9cdff': '#a6bdf0',
    # text
    '#b7c9d8': '#b9b3aa', '#eff5fa': '#ebe6de', '#93d9e5': '#8fd3c4', '#a2e3b8': '#9fd5a4', '#add0ff': '#a6bdf0', '#ffd48c': '#e3c37b',
    '#e1a4b0': '#e8a3a3', '#97c5ff': '#a6bdf0', '#141c25': '#17171a',
}


def hx(c):
    if c is None:
        return None
    return '#%02x%02x%02x' % tuple(int(v * 255) for v in c[:3])


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def near_map(h):
    if h in MAP:
        return MAP[h]
    r = _rgb(h)
    best, bd = None, 1e9
    for k, v in MAP.items():
        d = sum((a - b) ** 2 for a, b in zip(r, _rgb(k)))
        if d < bd:
            best, bd = v, d
    return best if bd < 200 else h


def col(c):
    h = hx(c)
    return near_map(h) if h else 'none'


def path_d(items):
    d, cur = [], None
    def mv(pt):
        nonlocal cur
        if cur is None or abs(cur.x - pt.x) > .01 or abs(cur.y - pt.y) > .01:
            d.append(f'M{pt.x:.2f} {pt.y:.2f}')
    for it in items:
        k = it[0]
        if k == 'l':
            a, b = it[1], it[2]
            mv(a); d.append(f'L{b.x:.2f} {b.y:.2f}'); cur = b
        elif k == 'c':
            a, b, c, e = it[1], it[2], it[3], it[4]
            mv(a); d.append(f'C{b.x:.2f} {b.y:.2f} {c.x:.2f} {c.y:.2f} {e.x:.2f} {e.y:.2f}'); cur = e
        elif k == 're':
            r = it[1]
            d.append(f'M{r.x0:.2f} {r.y0:.2f}H{r.x1:.2f}V{r.y1:.2f}H{r.x0:.2f}Z'); cur = None
        elif k == 'qu':
            q = it[1]
            d.append(f'M{q.ul.x:.2f} {q.ul.y:.2f}L{q.ur.x:.2f} {q.ur.y:.2f}L{q.lr.x:.2f} {q.lr.y:.2f}L{q.ll.x:.2f} {q.ll.y:.2f}Z'); cur = None
    return ''.join(d)


def panels(pno):
    doc = fitz.open(PDF)
    p = doc[pno]
    dr = p.get_drawings()
    def near(c, t=(0.106, 0.153, 0.196)):
        return c is not None and all(abs(a - b) < 0.01 for a, b in zip(c[:3], t))
    pans = [d['rect'] for d in dr if near(d.get('fill')) and d.get('color') and d['rect'].width > 60 and d['rect'].height > 60]
    return p, dr, pans


RED, AMBER_F, AMBER_S, YEL, BLUE, GREEN, INK, BG = '#ee8f8f', '#57452a', '#d9a35b', '#e9d88f', '#a6bdf0', '#9fd5a4', '#ebe6de', '#1d1d21'
PINKS = {'#f1a7a3', '#e8a3a3', '#e0a0a0', '#ee9f8e'}
PINKFILLS = {'#4a3238', '#6b4248', '#4a2f33', '#5a2e35', '#643f45', '#463539'}
TOKCOL = {'C': BLUE, 'A': GREEN, 'E': YEL, 'K': GREEN}


def _inside(r, box, tol=1.5):
    return r.x0 >= box.x0 - tol and r.y0 >= box.y0 - tol and r.x1 <= box.x1 + tol and r.y1 <= box.y1 + tol


def svg_for(p, dr, rect, pad=2, flank=False):
    paths, texts = [], []
    for d in dr:
        r = d['rect']
        if not _inside(r, rect, 1):
            continue
        if abs(r.x0 - rect.x0) < 1.5 and abs(r.y0 - rect.y0) < 1.5 and abs(r.x1 - rect.x1) < 1.5 and abs(r.y1 - rect.y1) < 1.5:
            continue  # panel background itself
        dash = d.get('dashes') or ''
        dash_attr = ''
        if dash and dash not in ('[] 0', '[ ] 0'):
            nums = dash.strip('[] ').split(']')[0].split()
            if nums:
                dash_attr = f' stroke-dasharray="{" ".join(nums)}"'
        paths.append(dict(d=path_d(d['items']), fill=col(d.get('fill')) if d.get('fill') else 'none',
                          stroke=col(d.get('color')) if d.get('color') else 'none', w=d.get('width') or 1,
                          fo=d.get('fill_opacity') or 1, so=d.get('stroke_opacity') or 1, dash=dash_attr, r=r,
                          types={i[0] for i in d['items']}))
    for b in p.get_text('dict', clip=rect)['blocks']:
        for l in b.get('lines', []):
            for sp in l['spans']:
                if sp['text'].strip():
                    x0, y0, x1, y1 = sp['bbox']
                    texts.append(dict(t=sp['text'], x=sp['origin'][0], y=sp['origin'][1], size=sp['size'],
                                      c=near_map('#%06x' % sp['color']), bold='Bold' in sp['font'], cx=(x0 + x1) / 2, cy=(y0 + y1) / 2))
    extra = []
    # flanking squares that work through a corner: teal, so amber can mean the target
    if flank:
        for q in paths:
            if q['fill'] == '#4f4430':
                q['fill'], q['stroke'] = '#24413f', '#8fd3c4'
    circles = [q for q in paths if 'c' in q['types'] and abs(q['r'].width - q['r'].height) < 1 and 8 < q['r'].width < 30]
    rads = sorted(q['r'].width / 2 for q in circles)
    for t in texts:
        L = t['t'].strip()
        if L in TOKCOL and t['bold'] or (L in TOKCOL and len(L) == 1):
            hit = [q for q in circles if q['r'].contains(fitz.Point(t['cx'], t['cy']))]
            if hit:
                q = min(hit, key=lambda q: q['r'].width)
                q['stroke'], q['fill'] = TOKCOL[L], BG
                t['c'] = TOKCOL[L]
        elif L == 'S':
            t['c'] = '#8fd3c4'
        elif L == 'T':
            pt = fitz.Point(t['cx'], t['cy'])
            bound = [q for q in paths if q['stroke'] in PINKS and 'c' not in q['types'] and max(q['r'].width, q['r'].height) >= 8]
            if bound:
                bx = fitz.Rect(min(q['r'].x0 for q in bound), min(q['r'].y0 for q in bound),
                               max(q['r'].x1 for q in bound), max(q['r'].y1 for q in bound))
                for q in bound:
                    q['stroke'] = AMBER_S
                for q in paths:
                    if q['fill'] in PINKFILLS and _inside(q['r'], bx) and 'c' not in q['types']:
                        q['fill'] = AMBER_F
                    if q['stroke'] in PINKS and 're' in q['types'] and _inside(q['r'], bx):
                        q['stroke'] = AMBER_S
            xs = sorted({round(q['r'].x0, 1) for q in paths if q['stroke'] == '#3c3c43' and q['r'].width < .5})
            gaps = [b - a for a, b in zip(xs, xs[1:]) if b - a > 4]
            cell = min(gaps) if gaps else 20
            rr = (rads[len(rads) // 2] if rads else t['size'] * .85)
            rr = min(max(rr, t['size'] * .75), cell * .36)
            extra.append(f'<circle cx="{t["cx"]:.2f}" cy="{t["cy"]:.2f}" r="{rr:.2f}" fill="{BG}" stroke="{RED}" stroke-width="1.6"/>')
            t['c'] = RED
    # corner markers and leftovers in pink: grey
    for q in paths:
        if q['stroke'] in PINKS and (('c' in q['types'] and q['r'].width < 12) or max(q['r'].width, q['r'].height) < 7):
            q['stroke'] = '#8a857d'
        # origin dots and burst corners: light fill, dark outline
        if q['fill'] == '#e3c37b' and q['stroke'] == '#17171a' and max(q['r'].width, q['r'].height) < 15:
            q['fill'] = INK
    out = []
    for q in paths:
        out.append(f'<path d="{q["d"]}" fill="{q["fill"]}" stroke="{q["stroke"]}" stroke-width="{q["w"]:.2f}"'
                   f'{" fill-opacity=%.2f" % q["fo"] if q["fo"] < 1 else ""}{" stroke-opacity=%.2f" % q["so"] if q["so"] < 1 else ""}{q["dash"]} stroke-linejoin="round"/>')
    out += extra
    for t in texts:
        out.append(f'<text x="{t["x"]:.2f}" y="{t["y"]:.2f}" font-size="{t["size"]:.2f}" fill="{t["c"]}"'
                   f'{" font-weight=700" if t["bold"] else ""}>{H.escape(t["t"])}</text>')
    vb = f'{rect.x0 - pad:.2f} {rect.y0 - pad:.2f} {rect.width + 2 * pad:.2f} {rect.height + 2 * pad:.2f}'
    return (f'<svg class="dg" viewBox="{vb}" width="{rect.width * 1.6:.0f}" xmlns="http://www.w3.org/2000/svg" '
            f'font-family="Alegreya Sans, sans-serif">{"".join(out)}</svg>')


if __name__ == '__main__':
    import sys
    pno = int(sys.argv[1])
    p, dr, pans = panels(pno)
    print(pno, [(round(r.x0), round(r.y0), round(r.width), round(r.height)) for r in pans])
