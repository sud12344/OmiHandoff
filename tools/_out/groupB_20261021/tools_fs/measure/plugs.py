"""plugs.py - measure Brennan plug STEPs (2026-10-02, work group PLUGS): socket-head ORB plug 6408-Hnn-O, hollow-hex pipe
plug 5406-HP-nn, square-head pipe plug 5406-SHP-nn - and, for validation, the hex-head cored ORB plug 6408-nn-O and the male
NPTF end of a hex bushing 5406-aa-bb (sizes measured before with other scripts: PLUG_HOLE_MEAS, the ORB library, the 5404 ENDL).

    python tools/measure/plugs.py socket    09_STEP_FILES/BRENNAN_6408-H08-O.stp    (round head + internal hex socket + ORB end)
    python tools/measure/plugs.py socket    09_STEP_FILES/BRENNAN_5406-HP-08.stp    (internal hex socket + male NPTF)
    python tools/measure/plugs.py square    09_STEP_FILES/BRENNAN_5406-SHP-08.stp   (square head + male NPTF)
    python tools/measure/plugs.py hexplug   09_STEP_FILES/BRENNAN_6408-08-O.stp     (validation: hex head + cored hole + ORB end)
    python tools/measure/plugs.py nptf      09_STEP_FILES/BRENNAN_5406-08-04.stp    (validation: male NPTF end of a hex bushing)

Method (OpenCascade, section.py): the part axis is the bounding-box axis whose two cross spans are equal (X on every Brennan STEP so
far); the thread tip is the end whose face is a full disc closed on the axis. Two kinds of section:
  * axial: the plane through the axis at angle theta (theta 0 = the X-Y plane); every straight edge as (a, r) with a = distance from
    the thread tip, r = signed distance from the axis. Through the socket CORNERS and through its FLATS (the angle is searched).
  * radial: the plane normal to the axis at a given a; the straight edges of a polygon give the across-flats (2 x the mean distance
    of the edge lines from the axis) and the corner radius (largest vertex distance) - for the hex socket, the hex head and the
    square head.
All values in inches; printed rounded to 0.0001 (the STEP geometry is exact to ~1e-6).
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, math, json
from section import load, section, edges
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

IN = 25.4
_cache = {}


def shape(p):
    if p not in _cache: _cache[p] = load(p)
    return _cache[p]


def volume(p):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(shape(p), g); return g.Mass() / IN ** 3


def frame(p):
    """axis index, tip coordinate, head coordinate, sign (+1: a grows with the model coordinate)"""
    b = Bnd_Box(); BRepBndLib.Add_s(shape(p), b)
    lo = [b.CornerMin().X() / IN, b.CornerMin().Y() / IN, b.CornerMin().Z() / IN]
    hi = [b.CornerMax().X() / IN, b.CornerMax().Y() / IN, b.CornerMax().Z() / IN]
    sp = [hi[k] - lo[k] for k in range(3)]
    ax = max(range(3), key=lambda k: abs(sp[k] - sum(sp[j] for j in range(3) if j != k) / 2))
    assert ax == 0, f'axis {ax}: only X-axis Brennan STEPs handled'
    # tip = the thread end: its radial section 0.02 in from the face is round (circles only), while the head end shows straight edges
    # (hex, square, hex socket); if both or neither do, the end reaching the SMALLER radius (the other is the head / the larger end of the
    # NPTF cone). Checked on all five Brennan STEP kinds handled here and on the generator rebuilds (plug_model.py).
    def reach(x):
        E = radial(p, 0.0, x, +1)
        return (any(e[0] == 'L' for e in E), max([max(e[2], e[3]) for e in E] or [0.0]))
    # the bounding box is enlarged by the shape tolerance (~0.0001 in): take the exact end planes from the axial section's vertices
    xs = [q[0] for kind, pts in edges(section(shape(p), (0, 0, 1))) for q in (pts[0], pts[-1])]
    x0, x1 = min(xs), max(xs)
    (l0, r0), (l1, r1) = reach(x0 + 0.02), reach(x1 - 0.02)
    if l0 != l1: return (ax, x0, x1, +1) if l1 else (ax, x1, x0, -1)
    if r0 < r1: return ax, x0, x1, +1
    return ax, x1, x0, -1


def axial(p, theta_deg, tip, sgn):
    """straight edges of the plane section through the X axis at angle theta: (a1, r1, a2, r2) with a = sgn * (x - tip)"""
    th = math.radians(theta_deg)
    n = (0.0, -math.sin(th), math.cos(th)); u = (math.cos(th), math.sin(th))
    out = []
    for kind, pts in edges(section(shape(p), n)):
        P = [(sgn * (q[0] - tip), q[1] * u[0] + q[2] * u[1]) for q in pts]
        if kind != 'L' and not isinstance(kind, tuple) and len(P) > 2:
            # a B-spline section edge that is straight (OCC sometimes returns a cone / plane intersection that way): treat it as a line
            (xa, ya), (xb, yb) = P[0], P[-1]; Lq = math.hypot(xb - xa, yb - ya)
            if Lq > 1e-9 and max(abs((x - xa) * (yb - ya) - (y - ya) * (xb - xa)) / Lq for x, y in P) < 1e-6: kind = 'L'
        if kind != 'L':
            out.append((P[0][0], P[0][1], P[-1][0], P[-1][1], kind)); continue
        (a1, r1), (a2, r2) = P[0], P[-1]
        if a1 > a2: a1, r1, a2, r2 = a2, r2, a1, r1
        out.append((a1, r1, a2, r2, 'L'))
    return out


def radial(p, a, tip, sgn):
    """the polygon edges of the section normal to the axis at a from the tip: list of (dist of the line from the axis, |p1|, |p2|)"""
    x = tip + sgn * a
    res = []
    for kind, pts in edges(section(shape(p), (1, 0, 0), (x * IN, 0, 0))):
        (y1, z1), (y2, z2) = (pts[0][1], pts[0][2]), (pts[-1][1], pts[-1][2])
        if kind == 'L':
            L_ = math.hypot(y2 - y1, z2 - z1)
            d = abs(y1 * (z2 - z1) - z1 * (y2 - y1)) / L_ if L_ > 1e-9 else None
            res.append(('L', d, math.hypot(y1, z1), math.hypot(y2, z2), math.degrees(math.atan2(z2 - z1, y2 - y1))))
        else:
            rr = [math.hypot(q[1], q[2]) for q in pts]
            res.append(('C' if isinstance(kind, tuple) else str(kind), kind[2] if isinstance(kind, tuple) else None, min(rr), max(rr), None))
    return res


def polygon(p, a, tip, sgn, rmax):
    """across flats / corner radius / number of sides of the polygon of straight edges lying within rmax of the axis at a"""
    E = [e for e in radial(p, a, tip, sgn) if e[0] == 'L' and max(e[2], e[3]) <= rmax + 1e-6]
    if not E: return None
    # the flats = the largest group of lines at one distance from the axis (a marking slot or a split flat adds short lines at other
    # distances - Brennan 6408-20-O has a 0.002 deep slot on one hex flat); the sides = the distinct directions of the outward normals
    groups = {}
    for e in E: groups.setdefault(round(e[1], 3), []).append(e)
    d0 = max(groups, key=lambda k: (len(groups[k]), k))
    G = [e for e in E if abs(e[1] - d0) < 6e-4]
    ds = [e[1] for e in G]
    sides = sorted({round(e[4] % 360, 0) % 360 for e in G})
    return dict(n=len(sides), af=round(2 * sum(ds) / len(ds), 4), af_spread=round(2 * (max(ds) - min(ds)), 5), corner_r=round(max(max(e[2], e[3]) for e in G), 4),
                edge_dirs=sides, other_lines=len(E) - len(G))


def crossing(S):
    """vertical lines that cross the axis (faces closed on the axis): their a"""
    return sorted(round(s[0], 4) for s in S if s[4] == 'L' and abs(s[0] - s[2]) < 1e-6 and min(s[1], s[3]) < -1e-3 and max(s[1], s[3]) > 1e-3)


def upper(S):
    """edges on the r > 0 side, sorted by a"""
    return sorted([s for s in S if min(s[1], s[3]) > -1e-6], key=lambda s: (s[0], s[2]))


def ang(s): return math.degrees(math.atan2(abs(s[3] - s[1]), abs(s[2] - s[0]) + 1e-12))


def socket_at_head(p, tip, sgn, L, af_guess_rmax):
    """hex socket in the head face (a = L): flats / corners from radial sections, depth = the closed face nearest to the head,
    mouth countersink from the axial section through a corner"""
    pol = [polygon(p, L - d, tip, sgn, af_guess_rmax) for d in (0.05, 0.08)]
    pol = [q for q in pol if q and q['n'] == 6]
    assert pol, 'no 6-sided socket found'
    m = pol[0]
    # the axial plane through a socket corner: corners lie along the edge directions + 60deg; search theta
    best = None
    for k in range(0, 180, 1):
        S = axial(p, k, tip, sgn)
        inner = [s for s in S if s[4] == 'L' and abs(s[1] - s[3]) < 1e-6 and 0 < s[1] < m['corner_r'] + 1e-3 and s[2] > L - 0.02]
        if inner:
            r_ = max(s[1] for s in inner)
            if best is None or r_ > best[0] + 1e-6: best = (r_, k, S)
    r_c, th_c, S = best
    cr = crossing(S)
    depth_faces = [a_ for a_ in cr if a_ > 1e-3 and a_ < L - 1e-3]
    bottom = max(depth_faces)
    # countersink: the line from the corner flat line up to the face
    cs = [s for s in upper(S) if s[4] == 'L' and abs(s[2] - L) < 1e-4 and s[0] < L - 1e-4 and s[3] > s[1] and 30 < ang(s) < 60 and s[1] < m['corner_r'] + 1e-3]
    csk = dict(angle=round(ang(cs[0]), 1), mouth_dia=round(2 * cs[0][3], 4), depth_at_corner=round(L - cs[0][0], 4)) if cs else None
    return dict(af=m['af'], af_spread=m['af_spread'], corner_r=m['corner_r'], corner_theta=th_c, depth=round(L - bottom, 4), bottom_flat=True,
                countersink=csk)


def round_head(p, tip, sgn, L):
    """largest horizontal (cylindrical) line touching the head end: radius, axial span, and the step face below it"""
    S = upper(axial(p, 0.0, tip, sgn))
    hor = [s for s in S if s[4] == 'L' and abs(s[1] - s[3]) < 1e-6]
    top = max(hor, key=lambda s: s[1])
    # chamfers at both ends of the head cylinder
    ch = [s for s in S if s[4] == 'L' and 30 < ang(s) < 60 and abs(max(s[1], s[3]) - top[1]) < 1e-4]
    starts = [s for s in S if s[4] == 'L' and abs(s[0] - s[2]) < 1e-6 and max(s[1], s[3]) < top[1] + 1e-6 and min(s[1], s[3]) > 0.05 and s[0] < top[0] + 1e-6 and s[0] > top[0] - 0.05]
    x_head = min(s[0] for s in starts) if starts else top[0]
    return dict(head_r=round(top[1], 4), head_dia=round(2 * top[1], 4), head_from=round(x_head, 4), head_len=round(L - x_head, 4),
                chamfers=[dict(a=round(min(s[0], s[2]), 4), size=round(abs(s[2] - s[0]), 4), angle=round(ang(s), 1)) for s in ch])


def orb_end(p, tip, sgn):
    """male ORB end: tip chamfer, thread major (r, end), ramp to the groove root, groove root r, groove end (= head face)"""
    S = upper(axial(p, 0.0, tip, sgn))
    ln = [s for s in S if s[4] == 'L']
    tipch = [s for s in ln if s[0] < 1e-4 and 30 < ang(s) < 60]
    thd = max([s for s in ln if abs(s[1] - s[3]) < 1e-6 and s[0] < 0.2], key=lambda s: s[1])
    ramp = [s for s in ln if abs(min(s[0], s[2]) - thd[2]) < 1e-4 and ang(s) > 20 and min(s[1], s[3]) < thd[1] - 0.005]
    rp = ramp[0]
    groove = [s for s in ln if abs(s[1] - s[3]) < 1e-6 and abs(s[1] - min(rp[1], rp[3])) < 1e-4]
    g_end = max(s[2] for s in groove)
    oring = [s for s in S if s[4] != 'L']
    return dict(tip_chamfer=(round(tipch[0][2], 4), round(ang(tipch[0]), 1)) if tipch else None, thd_r=round(thd[1], 4), thd_dia=round(2 * thd[1], 4),
                thd_cyl_end=round(thd[2], 4), ramp_angle=round(ang(rp), 1), THDL=round(rp[2], 4), groove_r=round(min(rp[1], rp[3]), 4),
                GD=round(2 * min(rp[1], rp[3]), 4), groove_end=round(g_end, 4), GW=round(g_end - rp[2], 4), oring_arcs=len(oring))


def nptf_male(p, tip, sgn):
    """male NPTF end: 45deg tip chamfer (Brennan; None on a generator rebuild), the 1.8deg cone (start / end radius and position), the
    cylinder after it (Brennan: the pipe OD collar after a small step; generator rebuild: the D blank the capped cone runs into)"""
    S = upper(axial(p, 0.0, tip, sgn))
    ln = [s for s in S if s[4] == 'L']
    tipch = [s for s in ln if s[0] < 1e-4 and 30 < ang(s) < 60]
    a0 = tipch[0][2] if tipch else 0.0
    cone = [s for s in ln if 1.0 < ang(s) < 3.0 and abs(s[0] - a0) < 1e-4][0]
    r_tip_extrap = cone[1] - cone[0] * math.tan(math.radians(ang(cone)))
    collar = [s for s in ln if abs(s[1] - s[3]) < 1e-6 and abs(s[0] - cone[2]) < 1e-4 and s[1] > cone[3] - 1e-6]
    tipch = tipch[0] if tipch else (0.0, cone[1], 0.0, cone[1], 'none')
    return dict(tip_r=round(tipch[1], 4), chamfer_len=round(tipch[2], 4), chamfer_angle=round(ang(tipch), 1), cone_r0=round(cone[1], 4),
                cone_r1=round(cone[3], 4), cone_end=round(cone[2], 4), cone_angle=round(ang(cone), 3), cone_dia_at_tip_extrap=round(2 * r_tip_extrap, 4),
                step_at=round(cone[2], 4), collar_r=round(collar[0][1], 4) if collar else None, collar_dia=round(2 * collar[0][1], 4) if collar else None,
                collar_end=round(collar[0][2], 4) if collar else None)


def run(kind, p):
    ax, tip, head, sgn = frame(p); L = round(abs(head - tip), 4)
    out = dict(step=_os.path.basename(p), L=L, volume_in3=round(volume(p), 5), tip_x=round(tip, 4), head_x=round(head, 4))
    out['tip_faces_closed_on_axis'] = crossing(axial(p, 0.0, tip, sgn))
    if kind == 'socket':
        rh = round_head(p, tip, sgn, L); out['head'] = rh
        out['socket'] = socket_at_head(p, tip, sgn, L, rh['head_r'] * 0.8)
        try: out['orb'] = orb_end(p, tip, sgn)
        except Exception as ex: out['orb'] = f'not an ORB end ({type(ex).__name__})'
        try: out['nptf'] = nptf_male(p, tip, sgn)
        except Exception as ex: out['nptf'] = f'not an NPTF end ({type(ex).__name__})'
    elif kind == 'square':
        out['nptf'] = nptf_male(p, tip, sgn)
        sh_ = out['nptf']['collar_end']
        out['square'] = dict(polygon(p, (sh_ + L) / 2, tip, sgn, 9.0), shoulder_a=sh_, head_len=round(L - sh_, 4))
        S = upper(axial(p, 45.0, tip, sgn))
        out['square']['corner_r_axial45'] = round(max(s[1] for s in S if s[4] == 'L' and abs(s[1] - s[3]) < 1e-6 and s[0] > sh_ - 1e-4), 4)
    elif kind == 'hexplug':
        out['orb'] = orb_end(p, tip, sgn)
        out['hex'] = polygon(p, (out['orb']['groove_end'] + L) / 2, tip, sgn, 9.0)
        S = axial(p, 0.0, tip, sgn); U = upper(S)
        hole = [s for s in U if s[4] == 'L' and abs(s[1] - s[3]) < 1e-6 and s[0] < 1e-4 and s[1] < out['orb']['groove_r'] - 0.02]
        if hole:
            h_ = hole[0]; pt = [s for s in U if s[4] == 'L' and abs(s[0] - h_[2]) < 1e-4 and 50 < ang(s) < 70]
            out['hole'] = dict(dia=round(2 * h_[1], 4), full_dia_depth=round(h_[2], 4), drill_apex=round(max(pt[0][0], pt[0][2]), 4) if pt else None,
                               point_angle=round(2 * ang(pt[0]), 1) if pt else None)
    elif kind == 'nptf':
        out['nptf'] = nptf_male(p, tip, sgn)
        U = upper(axial(p, 0.0, tip, sgn))
        hexface = [s for s in U if s[4] == 'L' and abs(s[0] - s[2]) < 1e-6 and s[0] > out['nptf']['cone_end'] - 1e-4 and max(s[1], s[3]) > out['nptf']['collar_r'] + 0.01]
        out['end_length_to_hex_face'] = round(min(s[0] for s in hexface), 4) if hexface else None
    return out


if __name__ == '__main__':

    kind = sys.argv[1]
    for p in sys.argv[2:]:
        print(json.dumps(run(kind, p), indent=1))
