"""measure_c0319.py (group C, 2026-10-21): the compression sleeve half-section on the nine Brennan C0319 STEPs (-08 in the repo since
2026-10-21 morning; -04 -06 -10 -12 -16 -20 -24 -32 = user upload 2026-10-21 (PARTcommunity briefcase), copied to 09_STEP_FILES).
Section through the axis (X), the closed outline chained from the front bore corner (x = 0, r = bore) along the outside: 14 lines
P0..P13 (front face, 40deg nose, 60deg back of the nose, groove, step, 40deg chamfer, collar, 45deg chamfer, spigot, 10deg tail chamfer,
rear face, rear inner bore, 15deg inner step, front bore). Writes measure/c0319_profile.csv (points + angles) and compares the record
letters (A B N G M C D D1 E H K) with the points."""
import os, sys, math, csv
H = os.path.dirname(os.path.abspath(__file__)); STAGE = os.path.dirname(H)
sys.path.insert(0, os.path.join(STAGE, 'tools_c', 'measure')); sys.path.insert(0, H)
import prof
import records as R
ROOT = R.ROOT
DASHES = (4, 6, 8, 10, 12, 16, 20, 24, 32)
NAMES = ['P%d' % i for i in range(14)]


def outline(path):
    E = prof.leg_edges(path, 0, 1, 2, a0=-1)
    segs = [((round(P[0][0], 5), round(P[0][1], 5)), (round(P[-1][0], 5), round(P[-1][1], 5))) for k, P in E if k == 'L']
    assert len(segs) == 14 and len(E) == 14, (path, len(segs), len(E))
    start = min({p for s in segs for p in s}, key=lambda p: (p[0], p[1]))      # (0, bore)
    pts = [start]; left = list(segs); cur = start
    # first step: up the front face
    while left:
        nxt = None
        for s in left:
            if math.dist(s[0], cur) < 1e-4: nxt = s[1]; left.remove(s); break
            if math.dist(s[1], cur) < 1e-4: nxt = s[0]; left.remove(s); break
        assert nxt is not None
        if len(pts) == 1 and abs(nxt[0] - cur[0]) > 1e-4:      # went along the bore first: walk the other way
            left.append((cur, nxt)); left = [s for s in left]; 
            cand = [s for s in left if (math.dist(s[0], cur) < 1e-4 or math.dist(s[1], cur) < 1e-4) and s != (cur, nxt)]
            s = cand[0]; left.remove(s); nxt = s[1] if math.dist(s[0], cur) < 1e-4 else s[0]
            left.remove((cur, nxt)) if (cur, nxt) in left else None
        if math.dist(nxt, start) < 1e-4: break
        pts.append(nxt); cur = nxt
    assert len(pts) == 14, (path, len(pts))
    return pts


def ang(p, q):
    return math.degrees(math.atan2(abs(q[1] - p[1]), abs(q[0] - p[0])))


def main():
    rows = []
    rec = R.records()
    for d in DASHES:
        pn = f'C0319-{d:02d}'; P = outline(os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp'))
        a = {f'a{i}': round(ang(P[i], P[(i + 1) % 14]), 3) for i in range(14)}
        row = dict(part=pn, **{f'x{i}': P[i][0] for i in range(14)}, **{f'r{i}': P[i][1] for i in range(14)}, **a)
        g = lambda k: R.num(rec[pn].get(k))
        rec_cmp = dict(A=(g('A') / 2, P[0][1]), B=(g('B') / 2, P[1][1]), N=(g('N') / 2, P[3][1]), G=(g('G'), P[3][0]), M=(g('M'), P[4][0]),
                       C=(g('C') / 2, P[6][1]), D=(g('D') / 2, P[8][1]), D1=(g('D1') / 2, P[10][1]), E=(g('E') / 2, P[11][1]), H=(g('H'), P[10][0]),
                       K=(g('K'), P[10][0] - P[9][0]))
        row['record_check'] = ' '.join(f'{k}:{"=" if abs(v[0] - v[1]) < 0.0006 else "%+.4f" % (v[1] - v[0])}' for k, v in rec_cmp.items())
        rows.append(row)
        print(pn, ' '.join(f'({P[i][0]:.4f},{P[i][1]:.4f})' for i in range(14)))
        print('   angles', ' '.join(f'{a[f"a{i}"]:.1f}' for i in range(14)), '| record', row['record_check'])
    with open(os.path.join(STAGE, 'measure', 'c0319_profile.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == '__main__':
    main()
