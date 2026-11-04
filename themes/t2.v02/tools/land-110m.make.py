# world-atlas land-110m(TopoJSON, Natural Earth 공용 도메인) → 등장방형 SVG path (viewBox 0 0 360 180)
import json, sys, re
src, out = sys.argv[1], sys.argv[2]
txt = open(src).read()
js = txt[txt.index('{'):txt.rindex('}') + 1]
topo = json.loads(js)
sx, sy = topo['transform']['scale']; tx, ty = topo['transform']['translate']
arcs = []
for a in topo['arcs']:
    x = y = 0; pts = []
    for dx, dy in a:
        x += dx; y += dy
        pts.append((x * sx + tx, y * sy + ty))
    arcs.append(pts)
def arc(i):
    return arcs[i] if i >= 0 else arcs[~i][::-1]
def ring(idx):
    pts = []
    for i in idx:
        a = arc(i)
        pts.extend(a if not pts else a[1:])
    return pts
def area(r):
    return 0.5 * abs(sum(r[i][0] * r[i - 1][1] - r[i - 1][0] * r[i][1] for i in range(len(r))))
paths = []
tol = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
for g in topo['objects']['land']['geometries']:
    polys = g['arcs'] if g['type'] == 'MultiPolygon' else [g['arcs']]
    for poly in polys:
        for k, rr in enumerate(poly):
            r = ring(rr)
            pr = [(lon + 180, 90 - lat) for lon, lat in r]
            # 날짜변경선(±180°)을 넘는 고리(러시아 동단 등)는 이어 붙이고, 왼쪽에 360° 옮긴 사본을 더 그린다(남극은 제외)
            copies = [pr]
            if min(lat for _, lat in r) > -60 and any(abs(pr[i][0] - pr[i - 1][0]) > 180 for i in range(1, len(pr))):
                un, off = [pr[0]], 0
                for i in range(1, len(pr)):
                    dx = pr[i][0] - pr[i - 1][0]
                    off += -360 if dx > 180 else (360 if dx < -180 else 0)
                    un.append((pr[i][0] + off, pr[i][1]))
                copies = [un, [(x - 360, y) for x, y in un]] if max(x for x, _ in un) > 360 else [un, [(x + 360, y) for x, y in un]]
            for pr in copies:
                if area(pr) < 2.5:          # 아주 작은 섬은 뺀다
                    continue
                keep = [pr[0]]
                for p in pr[1:]:
                    if abs(p[0] - keep[-1][0]) + abs(p[1] - keep[-1][1]) >= tol:
                        keep.append(p)
                if len(keep) < 4 or max(x for x, _ in keep) < 0 or min(x for x, _ in keep) > 360:
                    continue
                d = 'M' + 'L'.join(f'{x:.1f} {y:.1f}' for x, y in keep) + 'Z'
                d = re.sub(r'\.0(?=[ LZ])', '', d)
                paths.append(d)
d = ''.join(paths)
open(out, 'w').write(d)
print(len(paths), 'rings', len(d), 'bytes')
