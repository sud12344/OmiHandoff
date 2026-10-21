import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math, json
from prof import leg_edges, bbox
from swiv import legs_of, seg_list

def key(p): return (round(p[0], 4), round(p[1], 4))

def walk(S, start, stop_a, tol=2e-3):
    # follow the outer boundary from `start`, always taking an unused edge that touches the current point (within tol)
    ends = []
    for i, s in enumerate(S):
        ends.append((i, (s['a1'], s['r1']), (s['a2'], s['r2'])))
    pts = [start]; used = set(); cur = start
    for _ in range(80):
        nxt = []
        for i, a, b in ends:
            if i in used: continue
            if abs(a[0] - cur[0]) < tol and abs(a[1] - cur[1]) < tol: nxt.append((i, key(b)))
            elif abs(b[0] - cur[0]) < tol and abs(b[1] - cur[1]) < tol: nxt.append((i, key(a)))
        if not nxt: break
        # prefer the edge that does not go to the bore (the smallest radius) - i.e. the one with the larger radius end
        i, q = max(nxt, key=lambda t: t[1][1])
        used.add(i); pts.append(q); cur = q
        if q[0] <= stop_a: break
    return pts

def measure_nwo(p, orb_leg=None):
    legs = legs_of(p)
    res = []
    for (axis, sign), ext in legs:
        other = [k for k in (0, 1, 2) if k != axis]
        for pn in other:
            S = [s for s in seg_list(leg_edges(p, axis, sign, pn, a0=0.05)) if min(s['r1'], s['r2']) > -1e-6]
            at = max(max(s['a1'], s['a2']) for s in S)
            face = [s for s in S if abs(s['a1'] - at) < 1e-3 and abs(s['a2'] - at) < 1e-3]
            if not face: continue
            rstart = max(max(s['r1'], s['r2']) for s in face)
            pts = walk(S, key((at, rstart)), 0.06)
            res.append(((axis, sign, pn), at, pts))
    return res

def parse(at, pts):
    # pts: from the tip-face outer point along the outer boundary toward the crossing
    # segments as (a1, r1) -> (a2, r2) with a decreasing
    segs = list(zip(pts, pts[1:]))
    H = [(a1, a2, r1) for (a1, r1), (a2, r2) in segs if abs(r1 - r2) < 1e-4 and abs(a1 - a2) > 1e-4]   # horizontal runs (a1 > a2)
    # merge consecutive horizontals at the same radius (split by the O-ring arc)
    M = []
    for h in H:
        if M and abs(M[-1][2] - h[2]) < 1e-4 and abs(M[-1][1] - h[0]) < 0.08: M[-1] = (M[-1][0], h[1], h[2])
        else: M.append(h)
    return M

if __name__ == '__main__':
    for p in sys.argv[1:]:
        for leg, at, pts in measure_nwo(p):
            M = parse(at, pts)
            print(p.split('/')[-1], leg, 'tip', round(at, 4), 'runs (a_hi, a_lo, r):', [(round(a, 4), round(b, 4), round(r, 4)) for a, b, r in M][:9])

def nwo_params(p):
    best = None
    for leg, at, pts in measure_nwo(p):
        if leg[2] == 2 and leg[0] != 2 and False: pass
        M = parse(at, pts)
        if len(M) < 6: continue
        t, u, w, n, k, b = M[:6]
        # NWO pattern: undercut below the thread, washer above the undercut, nut, neck below the nut, body above the neck
        if not (u[2] < t[2] and w[2] > u[2] and n[2] < w[2] + 0.2 and k[2] < n[2] and b[2] > k[2] - 0.05): continue
        cand = dict(leg=leg, tip=round(at, 4), TM=round(2 * t[2], 4), UR=round(u[2], 4), THDL=round(at - u[0], 4), UL=round(u[0] - u[1], 4),
                    WR=round(w[2], 4), WT=round(w[0] - w[1], 4), NUTR=round(n[2], 4), NUTT=round(n[0] - n[1], 4),
                    NECKR=round(k[2], 4), NECKL=round(k[0] - k[1], 4), I3=round(at - k[1], 4), BODYR=round(b[2], 4))
        # keep the flats-plane reading (the smaller nut radius) - that is the nut AF/2
        if best is None or cand['NUTR'] < best['NUTR']: best = cand
    return best

if __name__ == '__main__' and '--params' in sys.argv:
    pass
