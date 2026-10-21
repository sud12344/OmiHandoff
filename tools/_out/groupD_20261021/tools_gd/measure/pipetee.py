# 2026-10-02 (new masters wave 1, PIPE-TEES): forged PIPE TEE / CROSS extractor (Brennan 56xx-FG STEPs and their OCP rebuilds).
# The body lies as gen_tee draws it: legs on +X / -X / +Y (/ -Y), hex bars with flats normal to Z, centred on the axis crossing.
# Per leg, from two sections through the leg axis (flats plane: radial = z; corner plane: radial = the other in-plane axis):
#   face   leg length = crossing to the leg's end face
#   BR/AF  hex flats radius / across flats (flats-plane outer radius over the hex arm), AC = corner radius (corner plane)
#   hexl   where the hex arm ends (corner plane: the step down from the corner radius, largest one on the leg)
#   female (port): collar (round, its radius and length = face - hexl), port mouth chamfer, tapered port (depth, radii,
#          half-angle), the drill below it (radius, from where to where along the leg)
#   male:  relief ring (radius, length), thread cone (start / end radius and position, half-angle), tip chamfer, tip face radii,
#          bore mouth countersink, bore (radius, how far toward the crossing)
# Boundaries come from the section EDGES (exact); the inside / outside of the axis point comes from the OCP solid classifier.
#   python tools/measure/pipetee.py <step> [<step> ...]            -> one JSON line per file (legs keyed '+X', '-X', '+Y', '-Y')
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, math, json
from prof import shape, bbox
from section import section, edges
from OCP.BRepClass3d import BRepClass3d_SolidClassifier
from OCP.TopAbs import TopAbs_IN
from OCP.gp import gp_Pnt
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp

IN = 25.4
EPS = 1e-4


def volume(p):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(shape(p), g); return g.Mass() / IN ** 3


def inside(p, xyz):
    c = BRepClass3d_SolidClassifier(shape(p), gp_Pnt(*[v * IN for v in xyz]), 1e-6)
    return c.State() == TopAbs_IN


def leg_segments(p, axis, sign, plane_normal):
    """section edges by the plane through the origin normal to `plane_normal`, as (a, r) polylines in leg coordinates
    (a = sign * coordinate along `axis`, r = the remaining coordinate, r >= 0 half only)"""
    n = [0, 0, 0]; n[plane_normal] = 1
    other = [k for k in (0, 1, 2) if k not in (axis, plane_normal)][0]
    out = []
    for kind, pts in edges(section(shape(p), tuple(n))):
        P = [(sign * q[axis], q[other]) for q in pts]
        if min(r for a, r in P) < -1e-6: continue
        out.append(P)
    return out


def crossings(segs, a):
    """radii where the section boundary crosses the line at axial a (non-vertical pieces only)"""
    rs = []
    for P in segs:
        for (a1, r1), (a2, r2) in zip(P, P[1:]):
            if abs(a2 - a1) < 1e-9: continue
            lo, hi = min(a1, a2), max(a1, a2)
            if lo - 1e-9 <= a <= hi + 1e-9:
                rs.append(r1 + (r2 - r1) * (a - a1) / (a2 - a1))
    return sorted(set(round(r, 7) for r in rs))


def pieces(segs, a_lo, a_hi):
    """boundary pieces (a1, r1, a2, r2), a1 < a2, inside [a_lo, a_hi] - lines and sampled curves split at their vertices"""
    out = []
    for P in segs:
        for (a1, r1), (a2, r2) in zip(P, P[1:]):
            if max(a1, a2) < a_lo - 1e-9 or min(a1, a2) > a_hi + 1e-9: continue
            if a1 > a2: a1, r1, a2, r2 = a2, r2, a1, r1
            out.append((a1, r1, a2, r2))
    return out


def profile(p, axis, sign, plane_normal, a_lo, a_hi):
    """outer and inner boundary of the leg wall between a_lo and a_hi: lists of (a1, r1, a2, r2, angle_deg) sorted by a,
    merged where collinear; vertical steps listed separately as (a, r_lo, r_hi)"""
    segs = leg_segments(p, axis, sign, plane_normal)
    other = [k for k in (0, 1, 2) if k not in (axis, plane_normal)][0]
    outer, inner, steps = [], [], []
    for (a1, r1, a2, r2) in pieces(segs, a_lo, a_hi):
        if a2 - a1 < 1e-7:
            steps.append((round(a1, 4), round(min(r1, r2), 4), round(max(r1, r2), 4))); continue
        am = (a1 + a2) / 2; rm = (r1 + r2) / 2
        rs = crossings(segs, am)
        q = [0, 0, 0]; q[axis] = sign * am
        axis_in = inside(p, q)
        if not rs: continue
        if abs(rm - rs[-1]) < 1e-5: outer.append((a1, r1, a2, r2))
        elif not axis_in and abs(rm - rs[0]) < 1e-5: inner.append((a1, r1, a2, r2))
    def merge(L):
        L = sorted(L); M = []
        for s in L:
            if M:
                a1, r1, a2, r2 = M[-1]
                ang0 = math.atan2(r2 - r1, a2 - a1); ang1 = math.atan2(s[3] - s[1], s[2] - s[0])
                if abs(s[0] - a2) < 1e-6 and abs(s[1] - r2) < 1e-6 and abs(ang0 - ang1) < 1e-4:
                    M[-1] = (a1, r1, s[2], s[3]); continue
            M.append(s)
        return [tuple(round(v, 4) for v in s) + (round(math.degrees(math.atan2(s[3] - s[1], s[2] - s[0])), 2),) for s in M]
    return merge(outer), merge(inner), sorted(set(steps))


def legs_of(p):
    b = bbox(p); ext = {'+X': b[3], '-X': -b[0], '+Y': b[4], '-Y': -b[1]}
    zf = max(b[5], -b[2])
    # a direction carries a leg when the body reaches clearly past the hex corner radius there (2 * the z extent bounds it)
    return {k: v for k, v in ext.items() if v > 1.25 * zf}, ext, zf


AX = {'+X': (0, 1), '-X': (0, -1), '+Y': (1, 1), '-Y': (1, -1)}


def measure_leg(p, key, face, zf):
    axis, sign = AX[key]
    pn_flats = 1 if axis == 0 else 0
    # corner plane: the hex arm end = the last step down from the corner radius
    # the other legs lie in the corner plane: look at this leg only beyond the crossing region (the largest hex corner radius the
    # z extent allows, + 0.01)
    a_min = zf / math.cos(math.radians(30)) + 0.01
    o_c, i_c, st_c = profile(p, axis, sign, 2, a_min, face + 1e-6)
    o_f, i_f, st_f = profile(p, axis, sign, pn_flats, 0.0, face + 1e-6)
    flat_c = [s for s in o_c if abs(s[4]) < 0.01 and s[2] > a_min + 1e-4]
    AC = max(s[3] for s in flat_c) if flat_c else None
    # the outer boundary at the corner radius that reaches farthest along this leg (beyond the crossing region)
    corner_runs = [s for s in flat_c if abs(s[1] - AC) < 2e-3]
    hexl = max(s[2] for s in corner_runs) if corner_runs else None
    BR = max(s[3] for s in o_f if abs(s[4]) < 0.01 and hexl is not None and s[0] < hexl - 1e-3) if hexl else None
    d = dict(face=round(face, 4), AC=AC, BR=BR, AF=round(2 * BR, 4) if BR else None, hexl=hexl)
    # beyond the hex arm: outer (flats plane) and inner (bore / port) boundary pieces
    out_end = [s for s in o_f if s[2] > hexl + 1e-4] if hexl else o_f
    in_leg = [s for s in i_f if s[2] > 1e-4]
    d['outer_end'] = out_end; d['inner'] = in_leg; d['steps_flats'] = [s for s in st_f if s[0] > 1e-3]
    # female or male: a female port opens to more than half the flats radius at the face
    mouth = max([s[3] for s in in_leg if abs(s[2] - face) < 1e-3] + [0.0])
    tip_outer = max([s[3] for s in o_f if abs(s[2] - face) < 1e-3] + [0.0])
    female = bool(BR) and abs(tip_outer - BR) < 2e-3
    d['kind'] = 'female' if female else 'male'
    if female:
        coll = [s for s in out_end if abs(s[4]) < 0.01]
        d['collar_r'] = coll[-1][3] if coll else None
        d['collar_len'] = round(face - hexl, 4) if hexl else None
        cham = [s for s in in_leg if abs(s[2] - face) < 1e-3 and 40 < s[4] < 50]
        d['mouth_r'] = round(mouth, 4)
        d['chamfer'] = dict(len=round(face - cham[0][0], 4), r0=cham[0][1], ang=cham[0][4]) if cham else None
        tap = [s for s in in_leg if 1.0 < s[4] < 2.6]
        d['taper'] = dict(a0=tap[0][0], r0=tap[0][1], a1=tap[0][2], r1=tap[0][3], halfang=tap[0][4], depth=round(face - tap[0][0], 4)) if tap else None
        dr = [s for s in in_leg if abs(s[4]) < 0.01]
        # the drill = the flat inner piece that reaches farthest out along the leg (directly below the taper, or the whole pocket)
        if dr:
            top = max(dr, key=lambda s: s[2])
            # follow the same radius down toward the crossing
            lo = min(s[0] for s in dr if abs(s[1] - top[1]) < 2e-4)
            d['drill'] = dict(r=top[1], dia=round(2 * top[1], 4), a_from=round(max(lo, 0.0), 4), a_to=top[2], to_crossing=lo < 1e-4)
        else: d['drill'] = None
    else:
        rel = [s for s in out_end if abs(s[4]) < 0.01 and abs(s[0] - hexl) < 1e-3]
        d['relief'] = dict(r=rel[0][1], dia=round(2 * rel[0][1], 4), a0=rel[0][0], a1=rel[0][2], len=round(rel[0][2] - rel[0][0], 4)) if rel else None
        cone = [s for s in out_end if -2.6 < s[4] < -1.0]
        d['cone'] = dict(a0=cone[0][0], r0=cone[0][1], a1=cone[0][2], r1=cone[0][3], halfang=-cone[0][4], from_tip=round(face - cone[0][0], 4)) if cone else None
        ch = [s for s in out_end if -50 < s[4] < -40 and abs(s[2] - face) < 1e-3]
        d['tip_chamfer'] = dict(len=round(face - ch[0][0], 4), r_tip=ch[0][3]) if ch else None
        cs = [s for s in in_leg if 20 < s[4] < 40 and abs(s[2] - face) < 1e-3]
        d['countersink'] = dict(len=round(face - cs[0][0], 4), r_mouth=cs[0][3], ang=cs[0][4]) if cs else None
        bo = [s for s in in_leg if abs(s[4]) < 0.01]
        if bo:
            top = max(bo, key=lambda s: s[2]); lo = min(s[0] for s in bo if abs(s[1] - top[1]) < 2e-4)
            d['bore'] = dict(r=top[1], dia=round(2 * top[1], 4), a_from=round(max(lo, 0.0), 4), a_to=top[2], to_crossing=lo < 1e-4)
        else: d['bore'] = None
    return d


def measure(p):
    legs, ext, zf = legs_of(p)
    res = dict(file=_os.path.basename(p), volume=round(volume(p), 5), bbox=bbox(p), legs={})
    for k in ('+X', '-X', '+Y', '-Y'):
        if k in legs: res['legs'][k] = measure_leg(p, k, legs[k], zf)
    res['no_leg_extent'] = {k: round(v, 4) for k, v in ext.items() if k not in legs}
    return res


def brief(m):
    """the values a gen_tee configuration carries, one line per leg"""
    out = []
    for k, d in m['legs'].items():
        if d['kind'] == 'female':
            t = d.get('taper') or {}
            out.append(f"{k} female: face {d['face']:.4f} AF {d['AF']} AC {d['AC']} hexl {d['hexl']} collar r {d['collar_r']} len {d['collar_len']} "
                       f"mouth r {d['mouth_r']} chamfer {d['chamfer']} taper depth {t.get('depth')} r {t.get('r0')}..{t.get('r1')} halfang {t.get('halfang')} "
                       f"drill {d['drill']}")
        else:
            out.append(f"{k} male: face {d['face']:.4f} AF {d['AF']} AC {d['AC']} hexl {d['hexl']} (end length {d['face'] - d['hexl']:.4f}) relief {d['relief']} "
                       f"cone {d['cone']} tip chamfer {d['tip_chamfer']} countersink {d['countersink']} bore {d['bore']}")
    return out


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    for p in args:
        m = measure(p)
        if '--brief' in sys.argv:
            print(m['file'], 'volume', m['volume'], 'bbox', m['bbox'], 'no leg:', m['no_leg_extent'])
            for s in brief(m): print('   ' + s)
        else:
            print(json.dumps(m))
