# ORFS (SAE J1453 face seal) extractors for Brennan STEPs - WP2 of tools/_out/orfs_modeltype_20261016/PLAN.md (2026-10-20, staging).
# Read-only on the STEPs; uses the live tools/measure section helpers (prof.leg_edges, swiv.seg_list).
#
# Every leg is read on its half section (plane through the leg axis, the half away from the other legs), in leg coordinates
# a = distance from the crossing / part origin along the leg, r = distance from the leg axis; s = face - a (distance from the end face).
# A boundary CHAIN is walked from a known corner (bore x end face) outward, edge by edge, and the end is read off the chain in order.
#
# Brennan models the O-rings fused into the solid (face-seal O-ring in the face groove, ORB O-ring in the stud undercut): an arc of
# radius 0.03 - 0.06 sweeping > 180 deg in the chain is read as an O-ring (reported for the check against FS4000 / 3-9xx) and the walls it
# hides are taken as straight and the groove corner as sharp (ASSUMPTION: the corner is hidden under the O-ring).
# Our end library does not model O-rings (as the existing ORB / NWO ends): the O-ring values are checks only.
import os, sys, math
_HERE = os.path.dirname(os.path.abspath(__file__))
_LIVE = os.path.normpath(os.path.join(_HERE, '..', '..', '..', 'measure'))          # tools/measure (live, batch 16)
for _p in (_LIVE, os.path.join(os.path.dirname(_LIVE), 'generators'), os.path.dirname(_LIVE)):
    if _p not in sys.path: sys.path.insert(0, _p)
from prof import leg_edges, bbox
from swiv import seg_list

TOL = 2e-3


def ang(s):
    """inclination of a straight segment from the leg axis, degrees (0 = cylinder, 90 = radial face)"""
    return math.degrees(math.atan2(abs(s['r2'] - s['r1']), abs(s['a2'] - s['a1']) + 1e-12))


def half(p, axis, sign, pn=2, others=(), a0=-9.0):
    """segments of the leg half section; `others` = (axis, sign) of the other legs: the half away from them is taken"""
    o = [k for k in (0, 1, 2) if k not in (axis, pn)][0]
    s_o = {sg for a_, sg in others if a_ == o}
    if len(s_o) > 1: raise ValueError('other legs on both halves of this section plane')
    rside = -s_o.pop() if s_o else 1
    return [s for s in seg_list(leg_edges(p, axis, sign, pn, a0=a0, rside=rside)) if min(s['r1'], s['r2']) > -1e-6]


def _pts(s):
    return (s['a1'], s['r1']), (s['a2'], s['r2'])


def _same(p, q, t=TOL):
    return abs(p[0] - q[0]) < t and abs(p[1] - q[1]) < t


def chain(S, start, first, n=80, stop=None):
    """walk the boundary from point `start`; `first(seg)` picks the first edge. Returns oriented edges
    dict(k, p, q, s=seg) with p the start point. stop(edge) ends the walk after that edge."""
    used, out, cur = set(), [], start
    cand = [i for i, s in enumerate(S) if any(_same(x, cur) for x in _pts(s)) and first(S[i])]
    if not cand: raise ValueError(f'no first edge at {cur}')
    i = cand[0]
    for _ in range(n):
        s = S[i]; a, b = _pts(s)
        p, q = (a, b) if _same(a, cur) else (b, a)
        e = dict(k=s['k'], p=p, q=q, s=s)
        out.append(e); used.add(i); cur = q
        if stop and stop(e): break
        nxt = [j for j, t in enumerate(S) if j not in used and any(_same(x, cur) for x in _pts(t))]
        if not nxt: break
        i = nxt[0]
    return out


def is_ring(e):
    """a fused O-ring: an arc of radius 0.03-0.06 that sweeps more than 180 deg"""
    if e['k'] != 'C': return False
    P = e['s']['P']
    (a0, r0), (am, rm) = P[0], P[len(P) // 2]
    R = _arcR(P)
    return 0.025 < R < 0.065 and math.hypot(am - a0, rm - r0) > 1.2 * R


def _arcR(P):
    (x1, y1), (x2, y2), (x3, y3) = P[0], P[len(P) // 2], P[-1]
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-12: return 1e9
    ux = ((x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)) / d
    uy = ((x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)) / d
    return math.hypot(x1 - ux, y1 - uy)


def ring_of(e):
    P = e['s']['P']
    (x1, y1), (x2, y2), (x3, y3) = P[0], P[len(P) // 2], P[-1]
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    ux = ((x1 * x1 + y1 * y1) * (y2 - y3) + (x2 * x2 + y2 * y2) * (y3 - y1) + (x3 * x3 + y3 * y3) * (y1 - y2)) / d
    uy = ((x1 * x1 + y1 * y1) * (x3 - x2) + (x2 * x2 + y2 * y2) * (x1 - x3) + (x3 * x3 + y3 * y3) * (x2 - x1)) / d
    return ux, uy, math.hypot(x1 - ux, y1 - uy)


def simplify(E):
    """drop zero-length edges, take O-ring arcs out (returned separately), merge consecutive collinear horizontals / verticals"""
    rings, out = [], []
    for e in E:
        if is_ring(e):
            rings.append(ring_of(e)); continue
        if _same(e['p'], e['q'], 1e-6): continue
        if out and e['k'] == 'L' and out[-1]['k'] == 'L':
            f = out[-1]
            for i in (0, 1):                       # i = 1: horizontal (same r); i = 0: vertical (same a)
                if abs(f['p'][i] - f['q'][i]) < TOL and abs(e['p'][i] - e['q'][i]) < TOL and abs(f['p'][i] - e['p'][i]) < TOL:
                    out[-1] = dict(k='L', p=f['p'], q=e['q'], s=None); break
            else:
                out.append(e)
            continue
        out.append(e)
    # a ring between two pieces of one line leaves them non-adjacent in `out` only if a zero edge sat between; merge again
    return out, rings


def H(e):  return e['k'] == 'L' and abs(e['p'][1] - e['q'][1]) < TOL and abs(e['p'][0] - e['q'][0]) > TOL
def V(e):  return e['k'] == 'L' and abs(e['p'][0] - e['q'][0]) < TOL and abs(e['p'][1] - e['q'][1]) > TOL
def A(e):
    if e['k'] != 'L': return None
    return round(math.degrees(math.atan2(abs(e['q'][1] - e['p'][1]), abs(e['q'][0] - e['p'][0]) + 1e-12)), 1)


def R4(x): return round(x, 4)


def face_corner(S):
    """the end face x bore corner: the bore = the smallest-radius horizontal reaching the far end; the face = the vertical at the
    largest a that starts at the bore radius"""
    hz = [s for s in S if s['k'] == 'L' and abs(s['r1'] - s['r2']) < TOL and s['a2'] - s['a1'] > 0.05]
    # the bore of THIS end: among the smallest-radius horizontals, the one reaching furthest out (a part with a bore step has two bores;
    # 2026-10-20: the smallest bore overall can belong to the other end)
    rlow = min(min(s['r1'], s['r2']) for s in hz)
    cand = [s for s in hz if min(s['r1'], s['r2']) < rlow + 0.15]
    amax = max(s['a2'] for s in cand)
    bs = min((s for s in cand if s['a2'] > amax - TOL), key=lambda s: min(s['r1'], s['r2']))     # (the groove walls also reach the face)
    rb = min(bs['r1'], bs['r2'])
    vs = [s for s in S if s['k'] == 'L' and abs(s['a1'] - s['a2']) < TOL and abs(min(s['r1'], s['r2']) - rb) < TOL and abs(s['a1'] - bs['a2']) < TOL]
    af = max(s['a1'] for s in vs)
    return af, rb


def _fmt(E):
    return [(e['k'], A(e), (R4(e['p'][0]), R4(e['p'][1])), (R4(e['q'][0]), R4(e['q'][1]))) for e in E]


# ------------------------------------------------------------------------------------------------------------------------------ FSM
def measure_fsm(p, axis, sign, others=(), pn=2, bulkhead=False):
    """male face-seal end (and, bulkhead=True, the bulkhead end FSBH: the same nose, a long thread, relief, step, collar).
    Returns the face groove, land, chamfer, thread major + length, run-out and the end length, distances s from the seal face."""
    S = half(p, axis, sign, pn, others)
    af, rb = face_corner(S)
    s_ = lambda a: R4(af - a)
    # walk up the face from the bore; stop once the profile has risen above the thread and turned back (the body)
    E = chain(S, (af, rb), first=lambda s: abs(s['a1'] - s['a2']) < TOL and abs(min(s['a1'], s['a2']) - af) < TOL, n=40)
    E, rings = simplify(E)
    out = dict(face_a=R4(af), BORER=R4(rb))
    i = 0
    assert V(E[i]) and abs(E[i]['p'][0] - af) < TOL, ('face', _fmt(E[:3]))
    out['GI'] = R4(E[i]['q'][1]); i += 1
    assert H(E[i]) and E[i]['q'][0] < af, ('groove inner wall', _fmt(E[i:i + 2]))
    gb = E[i]['q'][0]; out['GD'] = s_(gb); i += 1
    assert V(E[i]) and abs(E[i]['p'][0] - gb) < TOL, ('groove bottom', _fmt(E[i:i + 2]))
    i += 1
    fil = None
    if E[i]['k'] == 'C':                                   # a real bottom fillet (none found on the pilots: the O-ring hides the corner)
        fil = R4(_arcR(E[i]['s']['P'])); i += 1
    while V(E[i]) and abs(E[i]['p'][0] - gb) < TOL: i += 1   # bottom split by the O-ring
    assert H(E[i]) and abs(E[i]['q'][0] - af) < TOL, ('groove outer wall', _fmt(E[i:i + 2]))
    out['GO'] = R4(E[i]['q'][1]); out['GROOVE_FILLET'] = fil; i += 1
    assert V(E[i]) and abs(E[i]['p'][0] - af) < TOL, ('land', _fmt(E[i:i + 2]))
    out['FR'] = R4(E[i]['q'][1]); i += 1
    e = E[i]; assert e['k'] == 'L' and 30 < A(e) < 60 and e['q'][1] > e['p'][1], ('nose chamfer', _fmt(E[i:i + 2]))
    out['CH'] = s_(e['q'][0]); out['CH_ANG'] = A(e); i += 1
    e = E[i]; assert H(e), ('thread major', _fmt(E[i:i + 2]))
    out['RMAJ'] = R4(e['p'][1]); out['THD_END'] = s_(e['q'][0]); out['THDL'] = R4(e['p'][0] - e['q'][0]); i += 1
    # run-out: (a) 60 deg flank down to a relief, relief to a radial shoulder (straights, bulkhead), or
    #          (b) a radial step down at the thread end, then the body (forged legs)
    e = E[i]
    if e['k'] == 'L' and 50 < A(e) < 70 and e['q'][1] < e['p'][1]:
        out['RUNOUT'] = 'flank'; out['FLANK_ANG'] = A(e); out['RELR'] = R4(e['q'][1]); i += 1
        assert H(E[i]), ('relief', _fmt(E[i:i + 2]))
        out['REL_END'] = s_(E[i]['q'][0]); out['RELL'] = R4(E[i]['p'][0] - E[i]['q'][0]); i += 1
        out['ENDL'] = out['REL_END']
        e = E[i]
        assert V(e) and e['q'][1] > e['p'][1], ('shoulder', _fmt(E[i:i + 2]))
        out['SHOULDER_R'] = R4(e['q'][1]); i += 1
    elif V(e) and e['q'][1] < e['p'][1]:
        out['RUNOUT'] = 'step'; out['STEPR'] = R4(e['q'][1]); out['ENDL'] = out['THD_END']; i += 1
    else:
        raise AssertionError(('run-out', _fmt(E[i:i + 2])))
    if bulkhead:
        # FSBH: after the relief, steps up to the collar (Air-Way d17 x i4); record each radial step and cylinder until the body
        steps = []
        while i < len(E) and len(steps) < 6:
            e = E[i]
            if H(e): steps.append(('cyl', R4(e['p'][1]), s_(e['p'][0]), s_(e['q'][0])))
            elif V(e): steps.append(('face', s_(e['p'][0]), R4(e['p'][1]), R4(e['q'][1])))
            else: steps.append((e['k'], A(e), s_(e['p'][0]), R4(e['p'][1]), s_(e['q'][0]), R4(e['q'][1])))
            i += 1
        out['BH_STEPS'] = steps
    else:
        out['AFTER'] = _fmt(E[i:i + 3])
    out['RINGS'] = [dict(s=R4(af - x), rc=R4(y), W=R4(2 * R)) for x, y, R in rings]
    return out


# ----------------------------------------------------------------------------------------------------------------------------- FSSW
def measure_fssw(p, axis, sign, others=(), pn=2):
    """female face-seal swivel: the stem's flat seal face, the nut (cavity: mouth countersink, thread minor, relief, inner lip; outside:
    hex, chamfers, rear skirt), the neck behind the nut and the body face. All from the crossing (a) and from the nut face (s)."""
    S = half(p, axis, sign, pn, others)
    # the stem seal face: a radial edge starting at the bore radius, below the nut face
    hz = [s for s in S if s['k'] == 'L' and abs(s['r1'] - s['r2']) < TOL and s['a2'] - s['a1'] > 0.05]
    rb = min(min(s['r1'], s['r2']) for s in hz)
    vs = [s for s in S if s['k'] == 'L' and abs(s['a1'] - s['a2']) < TOL and abs(min(s['r1'], s['r2']) - rb) < TOL]
    aseal = max(s['a1'] for s in vs)
    E = chain(S, (aseal, rb), first=lambda s: abs(s['a1'] - s['a2']) < TOL and abs(s['a1'] - aseal) < TOL, n=60)
    E, rings = simplify(E)
    o = dict(BORER=R4(rb), SEAL_a=R4(aseal))
    i = 0
    assert V(E[i]); o['STEMR'] = R4(E[i]['q'][1]); i += 1                     # seal face up to the stem head radius
    assert H(E[i]) and E[i]['q'][0] < aseal; o['HEAD_REAR_a'] = R4(E[i]['q'][0]); i += 1
    while V(E[i]) and E[i]['q'][1] > E[i]['p'][1] and abs(E[i]['q'][1] - E[i]['p'][1]) < 0.01: i += 1   # stem / nut gap step
    # nut cavity going out: lip front (cone or face) -> relief -> thread minor -> mouth countersink -> nut face
    cav = []
    while not (V(E[i]) and E[i]['q'][1] > E[i]['p'][1] + 0.02 and E[i]['p'][0] > aseal):    # the nut face: radial, rising, past the seal
        cav.append(E[i]); i += 1
    o['CAVITY'] = _fmt(cav)
    mn = [e for e in cav if H(e) and e['p'][0] > aseal]
    mn = max(mn, key=lambda e: abs(e['q'][0] - e['p'][0]))
    o['MINR'] = R4(mn['p'][1]); o['MIN_a'] = (R4(min(mn['p'][0], mn['q'][0])), R4(max(mn['p'][0], mn['q'][0])))
    nf = E[i]; anut = nf['p'][0]; o['NUTFACE_a'] = R4(anut)
    o['SEAL_TO_NUTFACE'] = R4(anut - aseal)
    s_ = lambda a: R4(anut - a)
    cs = cav[-1]; o['MOUTH_R'] = R4(cs['q'][1]); o['MOUTH_DEPTH'] = s_(cs['p'][0]); o['MOUTH_ANG'] = A(cs)
    o['TE'] = s_(o['MIN_a'][0])                                                # nut face -> end of the minor
    rel = [e for e in cav if e['k'] == 'L' and e['p'][0] < o['MIN_a'][0] + TOL and e is not mn]
    o['CAV_REL'] = [(A(e), s_(e['p'][0]), R4(e['p'][1]), s_(e['q'][0]), R4(e['q'][1])) for e in rel]
    # nut outside from the nut face back: face, chamfer, hex corners, chamfer, rear skirt ..., nut rear face
    outside = []
    i_out0 = i
    while True:
        e = E[i]; outside.append(e); i += 1
        if V(e) and e['q'][1] < e['p'][1] - 0.03 and e['p'][0] < anut - 0.2: break      # the nut rear face (radial, falling)
    o['NUT_OUTSIDE'] = [(e['k'], A(e), s_(e['p'][0]), R4(e['p'][1]), s_(e['q'][0]), R4(e['q'][1])) for e in outside]
    corner = max(outside, key=lambda e: max(e['p'][1], e['q'][1]))
    o['NUT_CORNER_R'] = R4(max(corner['p'][1], corner['q'][1]))
    hx = [e for e in outside if H(e) and abs(e['p'][1] - o['NUT_CORNER_R']) < TOL]
    o['NUT_HEX_s'] = (s_(hx[0]['p'][0]), s_(hx[0]['q'][0])) if hx else None
    o['NUT_REAR_s'] = s_(outside[-1]['p'][0]); o['NUTL'] = o['NUT_REAR_s']
    o['NUT_REAR_R'] = (R4(outside[-1]['q'][1]), R4(outside[-1]['p'][1]))
    # lip bore and the neck to the body face
    e = E[i]; assert H(e), ('lip bore', _fmt(E[i:i + 2])); o['LIPR'] = R4(e['p'][1]); o['LIP_s'] = (s_(e['p'][0]), s_(e['q'][0])); i += 1
    while V(E[i]) and abs(E[i]['q'][1] - E[i]['p'][1]) < 0.01: i += 1
    e = E[i]; assert H(e), ('neck', _fmt(E[i:i + 2])); o['NECKR'] = R4(e['p'][1]); o['BODYFACE_a'] = R4(e['q'][0]); i += 1
    o['AFTER'] = _fmt(E[i:i + 3])
    o['RINGS'] = [dict(a=R4(x), rc=R4(y), W=R4(2 * R)) for x, y, R in rings]
    return o


# ------------------------------------------------------------------------------------------------------------------------- studs
def measure_stud(p, axis, sign, others=(), pn=2, model=False):
    """straight-thread (SAE J1926) stud on an FS part: fixed (ends at the hex face) or adjustable (washer, lock nut). From the tip.
    model=True (closed loop on OUR rebuild): the library ORB end has no tip chamfer and a radial step instead of the 60deg flank."""
    S = half(p, axis, sign, pn, others)
    at, rb = face_corner(S)
    s_ = lambda a: R4(at - a)
    E = chain(S, (at, rb), first=lambda s: abs(s['a1'] - s['a2']) < TOL and abs(s['a1'] - at) < TOL, n=40)
    E, rings = simplify(E)
    o = dict(BORER=R4(rb), tip_a=R4(at)); i = 0
    assert V(E[i]); i += 1
    e = E[i]
    if model and H(e): o['TIPCH'] = 0.0; o['TIPCH_ANG'] = None
    else:
        assert e['k'] == 'L' and 30 < A(e) < 60; o['TIPCH'] = s_(e['q'][0]); o['TIPCH_ANG'] = A(e); i += 1
    e = E[i]; assert H(e); o['RMAJ'] = R4(e['p'][1]); o['THD_END'] = s_(e['q'][0]); i += 1
    e = E[i]
    assert e['k'] == 'L' and ((50 < A(e) < 70) or (model and V(e))) and e['q'][1] < e['p'][1]; o['FLANK_ANG'] = A(e); i += 1
    fl_end = s_(E[i - 1]['q'][0])
    e = E[i]; assert H(e); o['UCR'] = R4(e['p'][1]); i += 1
    # the shoulder (hex face of a fixed stud, washer face of an adjustable one) = the next radial face; where the O-ring sits in the
    # undercut / shoulder corner, the undercut line stops short of it (corner hidden, taken as sharp)
    while not V(E[i]): i += 1
    o['SHOULDER'] = s_(E[i]['p'][0]); o['UC_END'] = o['SHOULDER']; o['UCL'] = R4(o['SHOULDER'] - fl_end); o['FLANK_END'] = fl_end
    o['AFTER'] = [(e['k'], A(e), s_(e['p'][0]), R4(e['p'][1]), s_(e['q'][0]), R4(e['q'][1])) for e in E[i:i + 8]]
    o['RINGS'] = [dict(s=R4(at - x), rc=R4(y), W=R4(2 * R)) for x, y, R in rings]
    return o


# --------------------------------------------------------------------------------------------------- loose nut / lock nut / sleeve
def _axial_profile(p, axis=0):
    """all edges of the half section of a loose part (axis along `axis`, from its a = 0 face), two planes (flats and corners)"""
    res = {}
    for pn in [k for k in (0, 1, 2) if k != axis]:
        res[pn] = [s for s in seg_list(leg_edges(p, axis, 1, pn, a0=-9.0)) if min(s['r1'], s['r2']) > -1e-6]
    return res


def _hex(planes):
    """hex across flats + corner radius from the two section planes (one through the corners, one through the flats, 30 deg apart or
    90 deg: for a hex 90 deg apart = one through a corner, one through a flat)"""
    rr = sorted(max(max(s['r1'], s['r2']) for s in S) for S in planes.values())
    return dict(AF=R4(2 * rr[0]), CORNER_R=R4(rr[1]), AF_from_corner=R4(2 * rr[1] * math.cos(math.radians(30))))


def measure_nut(p, axis=0):
    """FS0318 nut / FS0306 lock nut: hex, length, end chamfers, mouth countersinks, thread minor + length, relief, inner lip and bore"""
    planes = _axial_profile(p, axis)
    o = _hex(planes)
    b = bbox(p); o['L'] = R4(b[3 + axis] - b[axis])
    S = max(planes.values(), key=lambda S: max(max(s['r1'], s['r2']) for s in S))            # the corner plane
    inner = sorted([s for s in S if s['k'] == 'L' and max(s['r1'], s['r2']) < o['AF'] / 2 - 0.02], key=lambda s: s['a1'])
    o['INNER'] = [(A(dict(k='L', p=(s['a1'], s['r1']), q=(s['a2'], s['r2']))), R4(s['a1']), R4(s['r1']), R4(s['a2']), R4(s['r2'])) for s in inner]
    hz = [s for s in inner if abs(s['r1'] - s['r2']) < TOL]
    mn = max(hz, key=lambda s: s['a2'] - s['a1'])
    o['MINR'] = R4(mn['r1']); o['MIN_a'] = (R4(mn['a1']), R4(mn['a2'])); o['TE'] = R4(mn['a2'])
    cs = [s for s in inner if 40 < ang(s) < 50]
    o['MOUTH'] = [(R4(s['a1']), R4(s['r1']), R4(s['a2']), R4(s['r2'])) for s in cs]
    o['BORES'] = sorted({(R4(s['r1']), R4(s['a1']), R4(s['a2'])) for s in hz})
    outer = [s for s in S if s['k'] == 'L' and max(s['r1'], s['r2']) >= o['AF'] / 2 - 0.02]
    o['END_CHAMFERS'] = [(round(ang(s), 1), R4(s['a1']), R4(s['r1']), R4(s['a2']), R4(s['r2'])) for s in outer if 5 < ang(s) < 85]
    return o


def measure_sleeve(p, axis=0):
    """FS0319 braze sleeve: every edge of the half section, then the named readings"""
    S = _axial_profile(p, axis)[2]
    b = bbox(p); L = R4(b[3 + axis] - b[axis])
    E = sorted(S, key=lambda s: (s['a1'], s['r1']))
    o = dict(L=L, EDGES=[(s['k'], round(ang(s), 1) if s['k'] == 'L' else None, R4(s['a1']), R4(s['r1']), R4(s['a2']), R4(s['r2'])) for s in E])
    hz = [s for s in E if s['k'] == 'L' and abs(s['r1'] - s['r2']) < TOL]
    o['OD_R'] = R4(max(s['r1'] for s in hz))
    coll = [s for s in hz if abs(s['r1'] - o['OD_R']) < TOL][0]; o['COLLAR_a'] = (R4(coll['a1']), R4(coll['a2'])); o['COLLARL'] = R4(coll['a2'] - coll['a1'])
    o['BORE_R'] = R4(max((s for s in hz if s['a2'] - s['a1'] > 0.2 and s['r1'] < o['OD_R'] - 0.05), key=lambda s: s['a2'] - s['a1'])['r1'])
    o['STOP_R'] = R4(min(s['r1'] for s in hz))
    sp = [s for s in hz if o['BORE_R'] + 0.02 < s['r1'] < o['OD_R'] - 0.01]
    o['SPIGOT'] = [(R4(s['r1']), R4(s['a1']), R4(s['a2'])) for s in sp]
    return o
