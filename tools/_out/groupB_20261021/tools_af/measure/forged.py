# forged tee / 45 deg elbow leg extractor (2026-10-02, new masters 2504 / 2505 / 2606 / 2611): OCP plane sections through one leg of a
# forged body (legs in the XY plane, hex flats normal to Z - the gen_tee convention) and the leg's end expressed in the generator's terms.
#
#   python tools/measure/forged.py <step> <leg angle deg> <kind JICM|NPTFF|NPTFM> [side +1|-1]
#
# Two sections per leg (a = distance along the leg from the axis crossing, r = distance from the leg axis):
#   AX : the plane through the leg axis and Z  -> r = z >= 0: the hex arm shows its FLATS (A/F / 2), the revolved end shows its profile
#   LP : the leg plane z = 0, one side (side)  -> r = in-plane distance: the hex arm shows its CORNERS (A/F / sqrt 3), a round collar
#        shows its radius, so the hex -> collar step of a female port is visible here only
# The outline is WALKED from the leg's own tip / face inward along shared end points (no other leg's lines can enter), and the walk is
# read per end kind (every value is a section line end point; nothing is assumed):
#   JICM  : 37deg seat (tip dia, cone dia), land, 45deg thread chamfer, thread major and its run, relief + ramp if any, hex face (shoulder)
#   NPTFF : face, round collar (radius, start = end of the hex arm, length), mouth chamfer, port taper (radii, run), drill behind it
#   NPTFM : tip radius, thread taper (L2), relief radius, hex face (end length)
#   all   : hex A/F from the flats in AX (the highest line of the walk next to the hex face), the corner radius in LP, bore at the tip
# Validated by forged_validate.py on the values measured before (2650-08-08-08-08-FG, 5605-08-08-08-FG, 5600-16-16-16-FG, 6502-08-08-FG,
# the 2403 -08 JIC chain) - see evidence/forged_validate.txt.
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, math, json
from section import section, edges
from prof import shape

TOL = 2e-4


def outline(p, theta, plane, side=1):
    """section lines of the STEP p in leg coordinates (a, r) for the leg at angle theta (deg, in the XY plane)"""
    t = math.radians(theta); u = (math.cos(t), math.sin(t)); w = (-math.sin(t), math.cos(t))
    n = (w[0], w[1], 0.0) if plane == 'AX' else (0.0, 0.0, 1.0)
    out = []
    for kind, pts in edges(section(shape(p), n)):
        P = [(q[0] * u[0] + q[1] * u[1], q[2] if plane == 'AX' else side * (q[0] * w[0] + q[1] * w[1])) for q in pts]
        if min(r for a, r in P) < -1e-6: continue          # the other half
        (a1, r1), (a2, r2) = P[0], P[-1]
        straight = all(abs((a2 - a1) * (rr - r1) - (r2 - r1) * (aa - a1)) < 1e-5 for aa, rr in P)
        out.append(dict(p=(a1, r1), q=(a2, r2), ang=math.degrees(math.atan2(abs(r2 - r1), abs(a2 - a1))) if straight else None,
                        R=kind[2] if isinstance(kind, tuple) else None))
    return out


def walk(L, start, first=None, n=40):
    """follow the outline from point `start` (optionally leaving along the line `first`): list of (line, from, to)"""
    path = []; cur = start; prev = None
    for _ in range(n):
        cand = [l for l in L if l is not prev and (math.dist(l['p'], cur) < TOL or math.dist(l['q'], cur) < TOL)]
        if first is not None and not path: cand = [first]
        if not cand: break
        if len(cand) > 1: cand.sort(key=lambda l: (l['ang'] is None, -abs((l['q'][0] if math.dist(l['p'], cur) < TOL else l['p'][0]) - cur[0])))
        l = cand[0]; nxt = l['q'] if math.dist(l['p'], cur) < TOL else l['p']
        path.append((l, cur, nxt)); prev = l; cur = nxt
    return path


def seg(s):
    l, f, t = s
    return dict(a0=round(f[0], 4), r0=round(f[1], 4), a1=round(t[0], 4), r1=round(t[1], 4), ang=None if l['ang'] is None else round(l['ang'], 2))


def kind_of(s):
    l, f, t = s
    if l['ang'] is None: return 'curve'
    if l['ang'] < 0.05: return 'H'
    if abs(l['ang'] - 90) < 0.05: return 'V'
    return 'A%.0f' % l['ang']


def r4(x): return None if x is None else round(x, 4)


def tip_of(L): return max(max(l['p'][0], l['q'][0]) for l in L)


def jicm(p, theta, side=1):
    out = {}
    for pl in ('AX', 'LP'):
        L = outline(p, theta, pl, side); tip = tip_of(L)
        seat = [l for l in L if l['ang'] is not None and abs(l['ang'] - 37) < 0.3 and abs(max(l['p'][0], l['q'][0]) - tip) < TOL]
        assert len(seat) == 1, (pl, 'one 37deg seat at the tip', seat)
        s = seat[0]; start = s['p'] if s['p'][0] > s['q'][0] else s['q']
        W = walk(L, start, first=s)
        k = [kind_of(x) for x in W]
        # seat, (V step), land H, V step, 45deg chamfer, thread H (one or more lines), then relief / hex face
        rT, rC = W[0][1][1], W[0][2][1]; a_seat = W[0][2][0]
        i = 1
        if k[i] == 'V': i += 1
        assert k[i] == 'H', (pl, 'land', k); a_land = W[i][2][0]; i += 1
        while k[i] == 'V': i += 1
        if k[i] == 'A45':                                   # Brennan: 45deg thread chamfer from the land step up to the thread major
            a_t1 = W[i][2][0]; rM = W[i][2][1]; i += 1
        else:                                               # gen_tee model: a radial step from the cone dia straight to the thread major
            assert k[i - 1] == 'V' and k[i] == 'H', (pl, '45deg chamfer or radial step', k)
            a_t1 = W[i - 1][2][0]; rM = W[i - 1][2][1]
        a_t0 = a_t1
        while i < len(W) and k[i] == 'H' and abs(W[i][2][1] - rM) < TOL and (pl == 'LP' or True):
            a_t0 = W[i][2][0]; i += 1
            if pl == 'AX': break          # in AX the flats may continue the thread line when A/F = thread major (2650): stop at the first line end
        rest = [seg(x) for x in W[i:i + 6]]
        out[pl] = dict(tip=r4(tip), tip_dia=r4(2 * rT), CD=r4(2 * rC), SL=r4(tip - a_seat), LL=r4(a_seat - a_land), chamfer45=r4(a_land - a_t1),
                       TM=r4(2 * rM), thread_from=r4(a_t0), thread_to=r4(a_t1), TZ_incl_chamfer=r4(a_land - a_t0), after_thread=rest)
    # hex face: in LP (corners) the thread / relief stops at the hex arm
    lp = out['LP']; nx = lp['after_thread']
    relief = None
    if nx and nx[0]['ang'] == 90.0 and nx[0]['r1'] < nx[0]['r0']:      # down from the thread major: 60deg ramp drawn as V? (not expected)
        pass
    if nx and nx[0]['ang'] is not None and 5 < nx[0]['ang'] < 85 and nx[0]['r1'] < nx[0]['r0']:
        # thread -> ramp down -> relief line -> hex face
        relief = dict(ramp=nx[0], line=nx[1] if len(nx) > 1 else None)
        hexface = nx[1]['a1'] if len(nx) > 1 else None
    else:
        hexface = lp['thread_from']
    L = outline(p, theta, 'AX', side)
    flats = max((max(l['p'][1], l['q'][1]) for l in L if l['ang'] is not None and l['ang'] < 0.05 and min(l['p'][0], l['q'][0]) < hexface - 0.01
                 and max(l['p'][0], l['q'][0]) > 0.0 and max(l['p'][0], l['q'][0]) <= hexface + TOL), default=None)
    # hex corner radius: the first horizontal line of the LP walk past the hex face standing above the thread major
    corner = next((s_['r0'] for s_ in lp['after_thread'] if s_['ang'] == 0.0 and s_['r0'] > lp['TM'] / 2 + 0.005), None)
    bore = [l for l in L if l['ang'] is not None and l['ang'] < 0.05 and abs(max(l['p'][0], l['q'][0]) - lp['tip']) < TOL]
    return dict(kind='JICM', theta=theta, tip=lp['tip'], hex_face=r4(hexface), end_length=r4(lp['tip'] - hexface), relief=relief,
                AF_flats=r4(2 * flats) if flats else None, corner_r=r4(corner), bore_dia=r4(2 * min(max(l['p'][1], l['q'][1]) for l in bore)) if bore else None,
                chain=dict(TM=lp['TM'], CD=lp['CD'], SL=lp['SL'], LL=lp['LL'], chamfer45=lp['chamfer45'], TZ_incl_chamfer=lp['TZ_incl_chamfer'],
                           thread_from=lp['thread_from'], thread_to=lp['thread_to'], tip_dia=lp['tip_dia']),
                AX_chain_same=all(out['AX'][k_] == lp[k_] for k_ in ('TM', 'CD', 'SL', 'LL', 'chamfer45', 'tip_dia', 'thread_to')),
                LP_after_thread=lp['after_thread'][:4])


def nptff(p, theta, side=1):
    LP = outline(p, theta, 'LP', side); AX = outline(p, theta, 'AX', side); face = tip_of(AX)
    # LP: the collar line ends at the face; walk inward from its face end
    col = [l for l in LP if l['ang'] is not None and l['ang'] < 0.05 and abs(max(l['p'][0], l['q'][0]) - face) < TOL]
    c = max(col, key=lambda l: l['p'][1]); start = c['p'] if c['p'][0] > c['q'][0] else c['q']
    W = [seg(x) for x in walk(LP, start, first=c, n=6)]
    collar_r = W[0]['r0']; collar_from = W[0]['a1']
    # AX: the face line (vertical at the face), walked from its lower end into the port
    fl = [l for l in AX if l['ang'] is not None and abs(l['ang'] - 90) < 0.05 and abs(l['p'][0] - face) < TOL]
    f = min(fl, key=lambda l: min(l['p'][1], l['q'][1])); lo = f['p'] if f['p'][1] < f['q'][1] else f['q']; hi = f['q'] if lo is f['p'] else f['p']
    P = [seg(x) for x in walk(AX, lo, n=12) if x[0] is not f]
    k = [s['ang'] for s in P]
    i = 0; mouth = None; taper = None; drill = []
    if P and P[0]['ang'] is not None and abs(P[0]['ang'] - 45) < 1: mouth = P[0]; i = 1
    if i < len(P) and P[i]['ang'] is not None and abs(P[i]['ang'] - 1.79) < 0.15: taper = P[i]; i += 1
    steps = []
    while i < len(P) and P[i]['ang'] == 90.0: steps.append(P[i]); i += 1
    while i < len(P) and P[i]['ang'] == 0.0 and (not drill or abs(P[i]['r0'] - drill[0]['r0']) < TOL): drill.append(P[i]); i += 1
    flats = max((max(l['p'][1], l['q'][1]) for l in AX if l['ang'] is not None and l['ang'] < 0.05 and min(l['p'][0], l['q'][0]) < collar_from
                 and max(l['p'][0], l['q'][0]) > collar_from - 0.3), default=None)
    return dict(kind='NPTFF', theta=theta, face=r4(face), face_r_out=r4(hi[1]), collar_r=collar_r, collar_from=collar_from, collar_len=r4(face - collar_from),
                after_collar_LP=W[1:4], AF_flats=r4(2 * flats) if flats else None,
                mouth=mouth, taper=taper, taper_depth_from_face=r4(face - taper['a1']) if taper else None, steps=steps,
                drill=dict(dia=r4(2 * drill[0]['r0']), from_face=r4(face - drill[0]['a0']), to=drill[-1]['a1'], to_from_face=r4(face - drill[-1]['a1'])) if drill else None,
                port_rest=P[i:i + 3])


def nptfm(p, theta, side=1):
    AX = outline(p, theta, 'AX', side); tip = tip_of(AX)
    tl = [l for l in AX if l['ang'] is not None and abs(l['ang'] - 90) < 0.05 and abs(l['p'][0] - tip) < TOL]
    f = max(tl, key=lambda l: max(l['p'][1], l['q'][1])); hi = f['p'] if f['p'][1] > f['q'][1] else f['q']; lo = f['q'] if hi is f['p'] else f['p']
    P = [seg(x) for x in walk(AX, hi, n=8) if x[0] is not f]
    tch = None
    if P[0]['ang'] is not None and abs(P[0]['ang'] - 45) < 1: tch = P.pop(0)          # 45deg tip chamfer (Brennan 5600-16-16-16-FG)
    assert P[0]['ang'] is not None and abs(P[0]['ang'] - 1.79) < 0.15, ('taper at the tip', P[:2])
    tp = P[0]; i = 1
    # after the taper: an optional small radial step (Brennan: the taper ends a little below the pipe OD), the relief (horizontal), then the
    # hex face (vertical up to the flats in AX)
    stepr = None
    if i < len(P) and P[i]['ang'] == 90.0 and abs(P[i]['r1'] - P[i]['r0']) < 0.02: stepr = P[i]; i += 1
    rel = P[i] if i < len(P) and P[i]['ang'] == 0.0 else None
    if rel: i += 1
    face = P[i] if i < len(P) and P[i]['ang'] == 90.0 else None
    hexf = rel['a1'] if rel else tp['a1']
    return dict(kind='NPTFM', theta=theta, tip=r4(tip), tip_face_r=r4(hi[1]), tip_chamfer=tch, taper_r_start=tp['r0'], bore_dia=r4(2 * lo[1]),
                taper_len=r4(tp['a0'] - tp['a1']), taper_r_end=tp['r1'], taper_end_step=stepr,
                relief_dia=r4(2 * rel['r0']) if rel else None, relief_len=r4(rel['a0'] - rel['a1']) if rel else None,
                hex_face=hexf, end_length=r4(tip - hexf), flats_at_face=r4(2 * face['r1']) if face else None, after_relief=P[i:i + 3])


def corner_arcs(p, rmax=3.0):
    """radii of circle arcs of the z = 0 section centred on the axis crossing (the 30deg corner puck about Z shows as an arc of radius AC)"""
    out = []
    for kind, pts in edges(section(shape(p), (0, 0, 1))):
        if isinstance(kind, tuple):
            c = kind[1]
            if abs(c[0]) < 1e-3 and abs(c[1]) < 1e-3 and kind[2] < rmax: out.append(round(kind[2], 4))
    return sorted(set(out))


KIND = dict(JICM=jicm, NPTFF=nptff, NPTFM=nptfm)

if __name__ == '__main__':
    a = sys.argv[1:]
    side = int(a[3]) if len(a) > 3 else 1
    print(json.dumps(KIND[a[2]](a[0], float(a[1]), side)))
