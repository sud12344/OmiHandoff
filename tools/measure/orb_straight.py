"""orb_straight.py - measure the ORB ends of a Brennan STEP (2026-10-02, new master 3474: adjustable ORB x fixed ORB straight).

    python tools/measure/orb_straight.py 09_STEP_FILES/BRENNAN_3474-12-12-NWO.stp            # a straight: both ends + body + bore
    python tools/measure/orb_straight.py --leg 1 1 09_STEP_FILES/BRENNAN_6801-12-12-NWO-FG.stp  # one leg (axis 1, +), adjustable end
    python tools/measure/orb_straight.py --fixed 0 -1 09_STEP_FILES/BRENNAN_6410-12-08-O.stp     # one leg, fixed ORB end

A plane section through the fitting axis (tools/measure/section.py), in two planes 90 deg apart (one through the hex flats, one
through the hex corners). The outer outline is walked from a tip face inward, keeping every edge's kind (line / arc), and read as:

  ADJUSTABLE ORB end (nut, washer, O-ring - the NWO end of 6801): from the tip: [45deg tip chamfer] thread major (TM) -> [60deg run-out]
  undercut root (UR; THDL = tip to the start of the root run, the convention of NWO_MEAS / nwo.py) -> [O-ring: arcs, skipped] -> washer
  (WR, WT) -> locknut (flats plane: AF/2; corners plane: 15deg chamfer cones + corner run; NUTT) -> neck (NECKR, NECKL) -> body face
  (I3 = tip to the body face).
  FIXED ORB end: from the tip: [45deg chamfer] thread major -> [60deg run-out] groove root (GD/2; THDL = tip to the start of the root run,
  the convention of the ORB dict) -> [O-ring arcs, skipped] -> hex face = the first radial line rising above the thread major
  (GW = hex face - THDL; end length = THDL + GW).
  STRAIGHT body: the hex between the adjustable end's body face and the fixed end's hex face (flats-plane radius = AF/2, corner-plane
  chamfer cones), and the through bore (innermost line along the whole part).

The same edge-walk is used on the Brennan part and on our OCP rebuild (closed loop). Validation (evidence/measure_validation.txt):
the adjustable-end reader reproduces NWO_MEAS (gen_tee.py, measured with nwo.py) on the Brennan 6801 STEPs, the fixed-end reader
reproduces the ORB dict ends (gen_straight2.py) and the Brennan overall / hex lengths on 6410-12-08-O, 6400-14-14-O and 6400-32-32-O.
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, math, json
from section import section, edges
from prof import shape, bbox

TOL = 2e-3


def _ang(s):
    """angle of a line segment to the axis, deg (0 = horizontal / cylinder, 90 = radial face)"""
    return math.degrees(math.atan2(abs(s['r2'] - s['r1']), abs(s['a2'] - s['a1']) + 1e-12))


def leg_segments(p, axis, sign, plane_normal, a_tip):
    """edges of the section by the plane through the axis normal to `plane_normal`, as a = distance inward from the tip face at
    coordinate a_tip along `axis` (a = sign * (a_tip - x)), r = distance from the axis (half with r >= 0 only)"""
    n = [0, 0, 0]; n[plane_normal] = 1
    other = [k for k in (0, 1, 2) if k not in (axis, plane_normal)][0]
    out = []
    for kind, pts in edges(section(shape(p), tuple(n))):
        P = [(sign * (a_tip - q[axis]), q[other]) for q in pts]
        if min(r for a, r in P) < -1e-6: continue
        (a1, r1), (a2, r2) = P[0], P[-1]
        k = 'L' if kind == 'L' else 'C' if isinstance(kind, tuple) else 'S'
        if k == 'S':
            # a B-spline / other curve that is in fact straight (some STEP sections come out this way): read it as a line
            dx, dy = a2 - a1, r2 - r1; ln = math.hypot(dx, dy)
            if ln > 1e-7 and max(abs((a - a1) * dy - (r - r1) * dx) / ln for a, r in P) < 1e-5: k = 'L'
        if k == 'L' and abs(a2 - a1) + abs(r2 - r1) < 1e-7: continue
        out.append(dict(a1=a1, r1=r1, a2=a2, r2=r2, k=k, R=kind[2] if isinstance(kind, tuple) else None,
                        rtop=max(r for a, r in P), P=P))
    return out


def walk(S, a_stop=None):
    """walk the OUTER outline from the outermost point of the tip face (a = 0) inward: at every vertex take the unused edge that
    leaves it toward the larger radius (the outer boundary); stop past a_stop or when no edge continues. Returns the edges in order,
    each oriented (a1, r1) -> (a2, r2) along the walk."""
    face = [s for s in S if s['k'] == 'L' and abs(s['a1']) < TOL and abs(s['a2']) < TOL]
    if not face: raise ValueError('no tip face at a = 0')
    cur = max(((0.0, max(s['r1'], s['r2'])) for s in face), key=lambda t: t[1])
    used = set(); path = []
    for _ in range(400):
        cand = []
        for i, s in enumerate(S):
            if i in used: continue
            if abs(s['a1'] - cur[0]) < TOL and abs(s['r1'] - cur[1]) < TOL: cand.append((i, (s['a2'], s['r2']), False))
            elif abs(s['a2'] - cur[0]) < TOL and abs(s['r2'] - cur[1]) < TOL: cand.append((i, (s['a1'], s['r1']), True))
        cand = [c for c in cand if not (abs(c[1][0]) < TOL and S[c[0]]['k'] == 'L' and abs(S[c[0]]['a1'] - S[c[0]]['a2']) < TOL)]   # not back down the tip face
        if not cand: break
        i, q, flip = max(cand, key=lambda c: (c[1][1] + (S[c[0]]['rtop'] - max(S[c[0]]['r1'], S[c[0]]['r2'])), c[1][0]))
        s = dict(S[i])
        if flip: s.update(a1=S[i]['a2'], r1=S[i]['r2'], a2=S[i]['a1'], r2=S[i]['r1'])
        used.add(i); path.append(s); cur = q
        if a_stop is not None and cur[0] >= a_stop - 1e-9: break
    return path


def runs(path, dr=1e-4):
    """horizontal line runs along the walk, consecutive ones at the same radius merged: (a_start, a_end, r, index of the first edge)"""
    out = []
    for i, s in enumerate(path):
        if s['k'] != 'L' or abs(s['r1'] - s['r2']) > dr or abs(s['a2'] - s['a1']) < 1e-4: continue
        if out and abs(out[-1][2] - s['r1']) < dr and abs(out[-1][1] - s['a1']) < TOL: out[-1] = (out[-1][0], s['a2'], out[-1][2], out[-1][3])
        else: out.append((s['a1'], s['a2'], s['r1'], i))
    return out


def parse_thread(path):
    """tip chamfer, thread major, run-out and the root run that follows (adjustable undercut or fixed groove)"""
    R = runs(path)
    t = R[0]                                                   # thread major: the first horizontal run
    root = next(x for x in R[1:] if x[2] < t[2] - 0.01)        # the next run below the major
    i_t = t[3]
    ch = [s for s in path[:i_t] if s['k'] == 'L' and 5 < _ang(s) < 85]
    ro = [s for s in path[t[3]:root[3]] if s['k'] == 'L' and 5 < _ang(s) < 85]
    return dict(TM=round(2 * t[2], 4), THD_A0=round(t[0], 4), THD_A1=round(t[1], 4), ROOTR=round(root[2], 4), THDL=round(root[0], 4),
                tip_chamfer=(round(_ang(ch[0]), 1), round(ch[0]['a2'] - ch[0]['a1'], 4), round(ch[0]['r1'], 4)) if ch else None,
                runout=(round(_ang(ro[0]), 1), round(ro[0]['a2'] - ro[0]['a1'], 4)) if ro else None), R, root


def orings(path, a0, a1):
    return [dict(R=round(s['R'], 4), a=(round(s['a1'], 4), round(s['a2'], 4)), r=round(s['r1'], 4), rtop=round(s['rtop'], 4))
            for s in path if s['k'] == 'C' and a0 - TOL <= min(s['a1'], s['a2']) and max(s['a1'], s['a2']) <= a1 + TOL]


def parse_adjustable(path_f, path_c=None):
    """adjustable ORB end from two walks from the same tip: path_f through the hex FLATS, path_c through the hex CORNERS (optional)"""
    th, R, root = parse_thread(path_f)
    k = R.index(root)
    # washer: the first run above the thread major after the root run; nut: the runs right after it (flats plane: AF/2, with the
    # Brennan 0.002 marking dips merged); neck: the next run below the nut flats; body face: where the neck run ends
    w = next(x for x in R[k + 1:] if x[2] > th['TM'] / 2 + 0.02)
    kw = R.index(w)
    nut = []
    for x in R[kw + 1:]:
        if nut and x[2] < nut[0][2] - 0.01: break          # the neck: the first run clearly below the nut
        nut.append(x)
    nk = R[kw + 1 + len(nut)]
    af2 = max(x[2] for x in nut)
    out = dict(th, UR=th['ROOTR'], UL=round(w[0] - th['THDL'], 4), WR=round(w[2], 4), WT=round(w[1] - w[0], 4), wA=round(w[0], 4),
               NUTT=round(nk[0] - w[1], 4), AF=round(2 * af2, 4), NUT_DIPS=sorted({round(x[2], 4) for x in nut if x[2] < af2 - 1e-6}),
               NECKR=round(nk[2], 4), NECKL=round(nk[1] - nk[0], 4), I3=round(nk[1], 4),
               ORING=orings(path_f, th['THDL'], w[0]))
    out.pop('ROOTR')
    if path_c is not None:
        Rc = runs(path_c)
        cr = [x for x in Rc if w[1] - TOL <= x[0] and x[1] <= nk[0] + TOL and x[2] > af2 + 0.01]
        if cr:
            c = max(cr, key=lambda x: x[2])
            cones = [s for s in path_c if s['k'] == 'L' and 60 < _ang(s) < 85 and w[1] - TOL <= min(s['a1'], s['a2']) and max(s['a1'], s['a2']) <= nk[0] + TOL]
            out['NUT_CORNER_R'] = round(c[2], 4)
            out['NUT_CHAMFERS'] = [dict(ang_to_face=round(90 - _ang(s), 2), r_start=round(min(s['r1'], s['r2']), 4), a=(round(s['a1'], 4), round(s['a2'], 4))) for s in cones]
    return out


def parse_fixed(path):
    """fixed ORB end; also returns the walk index of the hex face"""
    th, R, root = parse_thread(path)
    i0 = root[3]
    hf = next(i for i in range(i0, len(path)) if path[i]['k'] == 'L' and _ang(path[i]) > 85 and max(path[i]['r1'], path[i]['r2']) > th['TM'] / 2 + 0.03)
    a_h = path[hf]['a1']
    out = dict(th, GD=round(2 * th['ROOTR'], 4), GW=round(a_h - th['THDL'], 4), ENDL=round(a_h, 4), ORING=orings(path, th['THDL'], a_h))
    out.pop('ROOTR')
    return out, hf


def straight_axis(p):
    b = bbox(p); spans = [b[3] - b[0], b[4] - b[1], b[5] - b[2]]
    ax = max(range(3), key=lambda k: abs(spans[k] - sum(spans[j] for j in range(3) if j != k) / 2))
    return ax, b[ax], b[ax + 3]


def bore_radius(p, axis, plane_normal, L):
    S = leg_segments(p, axis, 1, plane_normal, 0.0)
    lines = [s for s in S if s['k'] == 'L' and abs(s['r1'] - s['r2']) < 1e-4 and abs(s['a2'] - s['a1']) > 0.3 * L]
    return round(min(s['r1'] for s in lines), 4) if lines else None


def measure_straight(p):
    """both ends of a straight with an adjustable ORB end and a fixed ORB end, the body hex between them and the bore"""
    ax, xmin, xmax = straight_axis(p); L = xmax - xmin
    planes = [k for k in (0, 1, 2) if k != ax]
    res = dict(file=_os.path.basename(p), axis=ax, L=round(L, 4))
    # per tip and plane: walk; the plane with the smaller nut / hex radius is the flats plane
    walks = {}
    for tip, sign, a_tip in (('-', -1, xmin), ('+', 1, xmax)):
        for pn in planes:
            S = leg_segments(p, ax, sign, pn, a_tip)          # a = sign * (a_tip - x): inward from that tip
            walks[(tip, pn)] = walk(S)
    # which end is adjustable: past the thread root, the first run above the thread major is the backup WASHER on an adjustable end - a round
    # disc, the same radius in both section planes - and the body HEX on a fixed end (flats radius in one plane, corner radius in the other)
    ends = {}
    for tip in ('-', '+'):
        first = []
        for pn in planes:
            th, R, root = parse_thread(walks[(tip, pn)])
            first.append(next(x[2] for x in R[R.index(root) + 1:] if x[2] > th['TM'] / 2 + 0.02))
        ends[tip] = 'adjustable' if abs(first[0] - first[1]) < 0.003 else 'fixed'
    res['ends'] = ends
    for tip in ('-', '+'):
        Pa, Pb = walks[(tip, planes[0])], walks[(tip, planes[1])]
        if ends[tip] == 'adjustable':
            A0 = parse_adjustable(Pa); A1 = parse_adjustable(Pb)
            flats, corners = (Pa, Pb) if A0['AF'] <= A1['AF'] else (Pb, Pa)
            res['adjustable'] = dict(parse_adjustable(flats, corners), tip=tip, flats_plane=planes[0] if flats is Pa else planes[1])
        else:
            F0, _ = parse_fixed(Pa)
            res['fixed'] = dict(F0, tip=tip)
    # body: between the two ends, in the flats and the corners plane (walk from the adjustable tip)
    adj = res.get('adjustable'); fix = res.get('fixed')
    if adj and fix:
        a_body0 = adj['I3']; a_body1 = L - fix['ENDL']
        res['body'] = dict(a0=round(a_body0, 4), a1=round(a_body1, 4), length=round(a_body1 - a_body0, 4))
        for pn in planes:
            P = walks[(adj['tip'], pn)]
            Rb = [x for x in runs(P) if min(x[0], x[1]) >= a_body0 - TOL and max(x[0], x[1]) <= a_body1 + TOL]
            cones = [s for s in P if s['k'] == 'L' and 60 < _ang(s) < 85 and a_body0 - TOL <= min(s['a1'], s['a2']) and max(s['a1'], s['a2']) <= a_body1 + TOL]
            res['body'][f'plane{pn}'] = dict(rmax=round(max(x[2] for x in Rb), 4) if Rb else None,
                                             dips=sorted({round(x[2], 4) for x in Rb if Rb and x[2] < max(y[2] for y in Rb) - 1e-6}),
                                             chamfers=[dict(ang_to_face=round(90 - _ang(s), 2), r_start=round(min(s['r1'], s['r2']), 4), a=(round(s['a1'], 4), round(s['a2'], 4))) for s in cones])
        rr = sorted(res['body'][f'plane{pn}']['rmax'] for pn in planes)
        res['body']['AF'] = round(2 * rr[0], 4); res['body']['corner_r'] = rr[1]
    res['bore_r'] = bore_radius(p, ax, planes[0], L)
    return res


def measure_leg(p, axis, sign, kind='adjustable'):
    """one leg of an elbow / tee or one end of a straight (validation on 6801 / 6410 / 6400 STEPs)"""
    b = bbox(p); a_tip = b[axis + 3] if sign > 0 else b[axis]
    planes = [k for k in (0, 1, 2) if k != axis]
    P = [walk(leg_segments(p, axis, sign, pn, a_tip)) for pn in planes]
    if kind == 'adjustable':
        A = [parse_adjustable(x) for x in P]
        f = 0 if A[0]['AF'] <= A[1]['AF'] else 1
        return parse_adjustable(P[f], P[1 - f])
    F, hf = parse_fixed(P[0])
    return F


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] in ('--leg', '--fixed'):
        kind = 'adjustable' if a[0] == '--leg' else 'fixed'
        axis, sign = int(a[1]), int(a[2])
        for p in a[3:]: print(_os.path.basename(p), json.dumps(measure_leg(p, axis, sign, kind)))
    else:
        for p in a: print(json.dumps(measure_straight(p), indent=1))
