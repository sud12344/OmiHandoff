# SAE code 61 / code 62 FLANGE parts (2026-10-02, new masters 1800 / 1824): plane sections through the part axis of a Brennan STEP,
# read as an outline in (a, r) = (distance from the end opposite the flange face, distance from the axis).
#
#   python tools/measure/flange62.py straight <step> [...]   JIC x flange straight (1700 / 1800): JIC end length, round collar dia,
#                                                           two wrench flats (A/F, zone length from the collar face), 30deg collar
#                                                           chamfer, collar face to neck start (= gen_straight2 COLLARL), neck
#                                                           dia / length, flange head (OD, thickness, face O-ring groove), through
#                                                           bore, overall length
#   python tools/measure/flange62.py plug <step> [...]      flange plug (1724 / 1824): head + round stub, overall length, edge chamfers
#   python tools/measure/flange62.py head <step> [...]      the flange head only (any part whose axis is the bbox's odd axis)
#
# How: tools/measure/prof.leg_edges cuts the plane through the axis (normal to each of the two cross axes) and returns the edges
# with r >= 0; the OUTER silhouette r(a) is the largest radius of any non-vertical edge over a (sampled between edge ends, so
# every corner is an exact edge end point). The plane in which the collar reads SMALLER is the plane normal to the wrench flats.
# Validation (NOTES.md, evidence/measure/): on the Brennan 1700-08/-12/-16/-20/-24/-32 STEPs the head returns FLG61_MEAS
# (gen_straight2) and tools/measure/flange.py exactly, and overall length / wrench flats return BRENNAN_1700 (gen_straight2)
# and the Brennan Flange catalog p.3 1700 table (L, A/F).
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, json, math
from prof import leg_edges, bbox

TOL = 2e-4      # same-coordinate tolerance (the STEPs are exact to 1e-4 in)


def axis_of(p):
    b = bbox(p); spans = [b[3] - b[0], b[4] - b[1], b[5] - b[2]]
    return max(range(3), key=lambda k: abs(spans[k] - sum(spans[j] for j in range(3) if j != k) / 2)), b


def segs(p, axis, sign, pn):
    out = []
    for kind, P in leg_edges(p, axis, sign, pn, a0=-99):
        if min(r for a, r in P) < -1e-6: continue
        pts = sorted(P)
        out.append(dict(P=pts, a1=pts[0][0], a2=pts[-1][0], line=(kind == 'L')))
    return out


def r_at(S, a):
    """outer silhouette radius at a (largest radius of any non-vertical edge spanning a)"""
    best = None
    for s in S:
        if s['a2'] - s['a1'] < 1e-6 or not (s['a1'] - 1e-9 <= a <= s['a2'] + 1e-9): continue
        P = s['P']
        for (x1, r1), (x2, r2) in zip(P, P[1:]):
            if x2 - x1 < 1e-12 or not (x1 - 1e-9 <= a <= x2 + 1e-9): continue
            r = r1 + (r2 - r1) * (a - x1) / (x2 - x1)
            best = r if best is None else max(best, r)
    return best


def silhouette(S, a0, a1):
    """outer outline between a0 and a1 as intervals (lo, hi, r_lo, r_hi), merged where collinear"""
    xs = sorted({round(x, 6) for s in S for (x, r) in s['P'] if a0 - 1e-9 <= x <= a1 + 1e-9} | {a0, a1})
    iv = []
    for lo, hi in zip(xs, xs[1:]):
        if hi - lo < 1e-6: continue
        e = 1e-6
        rl, rh = r_at(S, lo + e), r_at(S, hi - e)
        if rl is None or rh is None: continue
        sl = (rh - rl) / (hi - lo - 2 * e)
        rl, rh = rl - sl * e, rh + sl * e
        if iv:
            plo, phi, prl, prh = iv[-1]
            psl = (prh - prl) / (phi - plo)
            if abs(phi - lo) < 1e-6 and abs(prh - rl) < TOL and abs(psl - sl) < 1e-3:
                iv[-1] = (plo, hi, prl, rh); continue
        iv.append((lo, hi, rl, rh))
    return iv


def ang(iv):
    lo, hi, rl, rh = iv; return math.degrees(math.atan2(abs(rh - rl), hi - lo))


def head(S, af):
    """flange head at the face af: O-ring groove (vertical bottom line between two horizontals that reach the face), head OD and
    thickness from the silhouette (edge chamfers at the face rim / back are allowed and reported)"""
    vert = [s for s in S if s['line'] and abs(s['a2'] - s['a1']) < TOL]
    hor = [s for s in S if s['line'] and abs(s['P'][0][1] - s['P'][-1][1]) < TOL and s['a2'] - s['a1'] > 0.01]
    g = None
    for v in vert:
        av = v['a1']
        if abs(av - af) < TOL or av < af - 0.3: continue
        lo, hi = sorted((v['P'][0][1], v['P'][-1][1]))
        hl = [h for h in hor if abs(h['a1'] - av) < TOL and abs(h['a2'] - af) < TOL and abs(h['P'][0][1] - lo) < TOL]
        hh = [h for h in hor if abs(h['a1'] - av) < TOL and abs(h['a2'] - af) < TOL and abs(h['P'][0][1] - hi) < TOL]
        if hl and hh: g = dict(GI=lo, GO=hi, GD=af - av); break
    if g is None: return None
    sil = silhouette(S, af - 1.5, af)
    rO = max(max(i[2], i[3]) for i in sil)
    run = [i for i in sil if max(i[2], i[3]) > rO - 0.03]          # the head (with any edge chamfer) is the last run near rO
    k = len(sil) - 1
    while k >= 0 and max(sil[k][2], sil[k][3]) > rO - 0.03: k -= 1
    a_back = sil[k + 1][0]
    flat = [i for i in sil[k + 1:] if abs(i[2] - rO) < TOL and abs(i[3] - rO) < TOL]
    ch_face = af - flat[-1][1] if flat else None
    ch_back = flat[0][0] - a_back if flat else None
    return dict(face=round(af, 4), O=round(2 * rO, 4), TH=round(af - a_back, 4), GI=round(g['GI'], 4), GO=round(g['GO'], 4), GD=round(g['GD'], 4),
                head_chamfer_face=round(ch_face, 4), head_chamfer_back=round(ch_back, 4), back=round(a_back, 4))


def bore(S, a0, af):
    """smallest-radius long horizontal line (the through bore) and a chamfer at the flange face"""
    hor = [s for s in S if s['line'] and abs(s['P'][0][1] - s['P'][-1][1]) < TOL and s['a2'] - s['a1'] > 0.5 * (af - a0)]
    if not hor: return None
    b = min(hor, key=lambda s: s['P'][0][1]); rb = b['P'][0][1]
    ch = [s for s in S if s['line'] and abs(s['a2'] - af) < TOL and abs(s['a1'] - b['a2']) < TOL and s['a2'] - s['a1'] > 1e-4]
    out = dict(D=round(2 * rb, 4), from_a=round(b['a1'], 4), to_a=round(b['a2'], 4))
    if ch:
        c = ch[0]; r2 = max(c['P'][0][1], c['P'][-1][1])
        out.update(face_chamfer_len=round(c['a2'] - c['a1'], 4), face_chamfer_dia=round(2 * r2, 4),
                   face_chamfer_ang=round(math.degrees(math.atan2(r2 - rb, c['a2'] - c['a1'])), 1))
    return out


def measure_straight(p):
    ax, b = axis_of(p)
    pns = [k for k in (0, 1, 2) if k != ax]
    best = None
    for sign in (1, -1):
        S0 = segs(p, ax, sign, pns[-1])
        a_lo = min(s['a1'] for s in S0); a_hi = max(s['a2'] for s in S0)
        h = head(S0, a_hi)
        if h: best = (sign, a_lo, a_hi, h); break
    assert best, 'no flange head found at either end'
    sign, a0, af, H = best
    out = dict(step=_os.path.basename(p), axis='XYZ'[ax], sign=sign, L=round(af - a0, 4), head=H)
    planes = {}
    for pn in pns:
        S = segs(p, ax, sign, pn)
        sil = silhouette(S, a0, af)
        planes[pn] = (S, sil)
    # JIC end: from the tip to the collar face = the LAST big step up (> 0.05) before the head back in the ROUND plane (the plane whose outline
    # reaches the larger radius before the head = the collar; the flats plane may step up again at the neck start).
    # 2026-10-18 (genfeat flange): was the FIRST step up in one plane - on a model JIC end of -12 and up the land -> thread major step is a
    # vertical step of (TM - CD)/2 > 0.05 (Brennan draws a 45deg chamfer there), so the first step was the thread start, not the collar face;
    # and where the flats equal the thread major (1700-20-16) the flats plane shows no step at the collar face at all. Re-validated on the 9
    # Brennan 1700 STEPs and the 1800-08-08 pilot (identical readings: genfeat_20261018/flange/test/ocp/flange62_revalidation.txt).
    def _rmax(pn_):
        return max(max(i[2], i[3]) for i in planes[pn_][1] if i[1] <= H['back'] + 5e-4)
    sil = planes[max(pns, key=_rmax)][1]
    a_col = None
    for i0, i1 in zip(sil, sil[1:]):
        if i1[2] - i0[3] > 0.05 and i1[0] < H['back'] - 5e-4: a_col = i1[0]
    out['jic_end_len'] = round(a_col - a0, 4)
    # in each plane the outline between the collar face and the head back
    res = {}
    for pn, (S, sil) in planes.items():
        mid = [i for i in sil if i[0] >= a_col - 1e-6 and i[1] <= H['back'] + 5e-4]
        res[pn] = mid
    # the plane with the smaller first radius after the collar face carries the flats
    first = {pn: res[pn][0][2] for pn in pns}
    pf = min(pns, key=lambda k: first[k]); pr = max(pns, key=lambda k: first[k])
    rnd, flt = res[pr], res[pf]
    # round plane: collar (horizontal at RC), chamfer (slanted down), neck (horizontal at RN) up to the head back
    rc = rnd[0]; assert abs(rc[2] - rc[3]) < TOL, ('collar not cylindrical', rc)
    out['collar_dia'] = round(2 * rc[2], 4); out['collar_round_len'] = round(rc[1] - rc[0], 4)
    ch = rnd[1]; out['collar_chamfer_ang'] = round(ang(ch), 1); out['collar_chamfer_len'] = round(ch[1] - ch[0], 4)
    nk = rnd[2]; assert abs(nk[2] - nk[3]) < TOL, ('neck not cylindrical', nk)
    out['neck_dia'] = round(2 * nk[2], 4); out['neck_len'] = round(nk[1] - nk[0], 4)
    out['neck_start_from_tip'] = round(nk[0] - a0, 4)
    # 2026-10-02 (review FLANGE62, finding 4): the collar length = collar face to the neck start (round collar + 30deg chamfer), read in the
    # ROUND plane - this is gen_straight2's COLLARL@DRIVE (the flats cut runs to the neck start). It is NOT the flats zone length below:
    # the two are equal only where the flats are narrower than the neck (1800-08-08: a step face at the neck start); where the flats are
    # wider than the neck they run out in the chamfer cone before the neck starts (all 9 Brennan 1700 STEPs).
    out['collar_face_to_neck_start'] = round(nk[0] - rc[0], 4)
    assert abs(out['collar_face_to_neck_start'] - (out['collar_round_len'] + out['collar_chamfer_len'])) < 2 * TOL, ('collar + chamfer != neck start', out)
    assert abs(rc[0] - a_col) < TOL, ('round-plane collar face is not the collar face', rc[0], a_col)
    assert abs(nk[1] - (af - H['TH'])) < 2 * TOL or len(rnd) > 3, ('neck does not reach the head back', nk, af - H['TH'])
    # flats plane: horizontal at A/F/2 from the collar face; the flats zone ends where the outline leaves that radius
    f0 = flt[0]; assert abs(f0[2] - f0[3]) < TOL, ('flat not flat', f0)
    out['flats_AF'] = round(2 * f0[2], 4); out['flats_zone_len'] = round(f0[1] - f0[0], 4)
    out['flats_end_vs_neck_start'] = round(f0[1] - nk[0], 4)
    out['flats_end'] = ('step face at the neck start (flats narrower than the neck)' if abs(f0[1] - nk[0]) < TOL else
                        'run-out in the 30deg chamfer before the neck start (flats wider than the neck)' if f0[1] < nk[0] else 'beyond the neck start (?)')
    out['flats_plane_normal'] = 'XYZ'[[k for k in (0, 1, 2) if k not in (ax, pf)][0]]
    out['bore'] = bore(planes[pns[-1]][0], a0, af)
    out['check_sum_L'] = round(out['jic_end_len'] + out['collar_round_len'] + out['collar_chamfer_len'] + out['neck_len'] + H['TH'], 4)
    return out


def measure_plug(p):
    ax, b = axis_of(p)
    pns = [k for k in (0, 1, 2) if k != ax]
    for sign in (1, -1):
        S = segs(p, ax, sign, pns[-1])
        a0 = min(s['a1'] for s in S); af = max(s['a2'] for s in S)
        H = head(S, af)
        if H: break
    assert H, 'no flange head found'
    out = dict(step=_os.path.basename(p), axis='XYZ'[ax], sign=sign, L=round(af - a0, 4), head=H)
    for pn in pns:
        sil = silhouette(segs(p, ax, sign, pn), a0, af)
        st = [i for i in sil if i[1] <= af - H['TH'] + 5e-4]
        cyl = max(st, key=lambda i: i[1] - i[0])
        out[f'stub_dia_plane_{"XYZ"[pn]}'] = round(2 * cyl[2], 4)
        out['stub_len'] = round(af - H['TH'] - a0, 4)
        out['stub_back_chamfer'] = round(cyl[0] - a0, 4)
        out['stub_front_end'] = round(cyl[1] - a0, 4)
    return out


def measure_head(p):
    ax, b = axis_of(p)
    pns = [k for k in (0, 1, 2) if k != ax]
    for sign in (1, -1):
        S = segs(p, ax, sign, pns[-1])
        H = head(S, max(s['a2'] for s in S))
        if H: return dict(step=_os.path.basename(p), axis='XYZ'[ax], sign=sign, **H)
    return None


if __name__ == '__main__':
    mode = sys.argv[1]; fn = dict(straight=measure_straight, plug=measure_plug, head=measure_head)[mode]
    for p in sys.argv[2:]: print(json.dumps(fn(p)))
