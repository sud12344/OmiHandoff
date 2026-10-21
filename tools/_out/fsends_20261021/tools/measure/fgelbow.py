# 2026-10-02 (new master 1502): FORGED 90 deg ELBOW extractor - body hex, 30deg corner puck, hex-arm ends, round collar and the female
# NPTF port of a Brennan forged elbow STEP (gen_tee 2500HX pattern: two legs on two principal axes, crossing at the origin, hex flats
# normal to Z). Every value is read off exact section edges (OCP), never fitted.
#
#   python tools/measure/fgelbow.py <step> [<step> ...]             body + every leg (port / bore) as JSON
#   python tools/measure/fgelbow.py --port AXIS,SIGN <step> [...]   only the female pipe port along that leg (straights too, e.g. 5405)
#   python tools/measure/fgelbow.py --model ...                     closed loop on OUR model (OCP rebuild / SolidWorks export): the port is
#                                                                   the plain tap-drill cylinder of the macro (no mouth chamfer, no taper)
#
# Per leg (leg coordinates: a along the leg from the crossing, r away from the axis on the side AWAY from the other leg, in the Z = 0
# plane = the plane through the hex corners):
#   face     a of the leg's end face (largest extent)
#   AC, hexl corner line of the hex arm (r = hex corner radius) from the crossing to the arm end (body face / collar start)
#   step_r   radius right after the arm end (round collar of a female leg, or the swivel neck)
#   collar   (female legs) collar radius and length (arm end -> port face)
#   AF       hex across flats, from a cross-section normal to the leg inside its arm (edge distances from the axis), and whether the
#            flats are normal to Z
#   port     (female legs) the inner outline walked from the mouth ('chain'), named: mouth chamfer, thread-zone minor cone (start / end
#            dia, angle, depth from the face), step, the tap drill (dia, from / to depth) and how it ends (cone point / arc / nothing)
#            + ball_arcs_on_axis (circle edges centred on the leg axis: a drill's ball end)
#   bore     smallest-radius straight bore line of the leg (the through-bore of a swivel / male leg)
# Body: puck = arcs about the Z axis in slices z = const: R(z) vs AC - |z| tan 30 (the 2500HX corner), plus the max deviation.
#
# Validated 2026-10-02 (tools/_out/newmasters_20261002/work/1502/evidence/measure_validation.txt) on sizes measured before:
#   Brennan 2500-06-06-FG: A/F 0.562, hex arms to 0.504, corner radius 0.3245, legs 1.06 (= the 2500HX SW2 row 2500-06-06-FG, built from that
#                          STEP: HEXAF 0.5625, HEXL 0.504 / 0.504, PUCK_XC 0.3248, M 1.06); corner = 30deg double cone within 0.0001
#   Brennan 5504-08-08-FG (both legs), 5502-04-04 / -08-08 / -16-16-FG, 2502-06-04-FG: collar 0.260 (gen_tee COLLAR_L, measured 2026-09-24)
#   Brennan 5405-08-08:    tap drill 0.718, thread taper depth 0.750, drill depth 0.900, drill point 120 deg (gen_straight2 SPEC 5405 note)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import sys, math, json
from section import section, edges
from prof import shape, bbox
from swiv import seg_list, near, legs_of

T30 = math.tan(math.radians(30))


def ang(s): return math.degrees(math.atan2(abs(s['r2'] - s['r1']), abs(s['a2'] - s['a1']) + 1e-12))


def plane_segs(p, axis, sign, oaxis, osign, z=0.0):
    """edges of the section z = const in leg coordinates of leg (axis, sign); r = -osign * q[oaxis] (the side away from the other leg
    (oaxis, osign)); only segments lying on that side (r >= 0)"""
    E = edges(section(shape(p), (0, 0, 1), (0, 0, z * 25.4)))
    out = []
    for kind, P in E:
        Q = [(sign * q[axis], -osign * q[oaxis]) for q in P]
        if min(r for a, r in Q) < -1e-6: continue
        out.append((kind, Q))
    return [s for s in seg_list(out)]


def hex_xsec(p, axis, a, sign):
    """cross-section normal to the leg at a: straight outer edges -> (flats distance, normal-to-Z flag, corner radius)"""
    n = [0, 0, 0]; n[axis] = 1; o = [0, 0, 0]; o[axis] = sign * a * 25.4
    E = edges(section(shape(p), tuple(n), tuple(o)))
    oth = [k for k in (0, 1, 2) if k != axis]
    best = []; rmax = 0.0
    for kind, P in E:
        for q in P: rmax = max(rmax, math.hypot(q[oth[0]], q[oth[1]]))
        if kind != 'L': continue
        (x1, y1), (x2, y2) = (P[0][oth[0]], P[0][oth[1]]), (P[-1][oth[0]], P[-1][oth[1]])
        L_ = math.hypot(x2 - x1, y2 - y1)
        if L_ < 0.05: continue
        d = abs(x1 * y2 - x2 * y1) / L_
        dirz = abs(math.degrees(math.atan2(y2 - y1, x2 - x1))) % 180      # 0 / 180 = parallel to the in-plane axis -> flat normal to Z
        best.append((d, L_, dirz))
    if not best: return None
    dmax = max(d for d, _, _ in best)
    flats = [b for b in best if near(b[0], dmax, 2e-3)]
    return dict(flat_d=round(dmax, 4), n_flats=len(flats), flats_normal_to_Z=any(min(b[2], 180 - b[2]) < 0.5 for b in flats), rmax=round(rmax, 4))


def puck(p, AC, BR, n=5):
    """slices z = k/n * 0.95 BR: the arc about the Z axis on the outer corner and its radius vs AC - z tan30"""
    res = []
    for k in range(n + 1):
        z = round(0.95 * BR * k / n, 4)
        E = edges(section(shape(p), (0, 0, 1), (0, 0, z * 25.4)))
        arcs = [kind[2] for kind, P in E if isinstance(kind, tuple) and math.hypot(kind[1][0], kind[1][1]) < 1e-4 and abs(kind[2] - (AC - z * T30)) < 0.05]
        R = max(arcs) if arcs else None
        res.append((z, round(R, 4) if R else None, round(AC - z * T30, 4)))
    dev = max(abs(R - e) for z, R, e in res if R is not None) if any(R for _, R, _ in res) else None
    return dict(slices=res, max_dev=round(dev, 4) if dev is not None else None)


def port(S, face, model=False):
    """female NPTF port along the leg from its face (S = segments in leg coordinates, r >= 0): walk the inner outline from the mouth
    inward segment by segment, then name the pieces - mouth chamfer (~45deg), thread-zone minor cone (0.5..4deg), step, tap drill
    (straight), drill end (cone point / arc / nothing)"""
    fl = [s for s in S if near(s['a1'], face) and near(s['a2'], face) and abs(s['r2'] - s['r1']) > 0.01]
    rmouth = min(min(s['r1'], s['r2']) for s in fl)
    out = dict(face=round(face, 4), mouth_r=round(rmouth, 4))
    chain = []; cur = (face, rmouth); used = set(id(s) for s in fl)
    for _ in range(12):
        nx = []
        for s in S:
            if id(s) in used: continue
            for (pa, pr), (qa, qr) in (((s['a1'], s['r1']), (s['a2'], s['r2'])), ((s['a2'], s['r2']), (s['a1'], s['r1']))):
                if near(pa, cur[0], 5e-4) and near(pr, cur[1], 5e-4) and (qa < pa - 1e-5 or (near(qa, pa, 1e-5) and qr < pr)):
                    nx.append((s, (qa, qr)))
        if not nx: break
        s, end = nx[0]; used.add(id(s))
        chain.append(dict(k=s['k'], a0=cur[0], r0=cur[1], a1=end[0], r1=end[1], ang=ang(s)))
        cur = end
        if cur[1] < 1e-4: break
    out['chain'] = [(c['k'], round(face - c['a0'], 4), round(c['r0'], 4), round(face - c['a1'], 4), round(c['r1'], 4), round(c['ang'], 2)) for c in chain]
    i = 0
    if not model and i < len(chain) and 30 < chain[i]['ang'] < 60:
        c = chain[i]; out['chamfer'] = dict(ang=round(c['ang'], 1), r_in=round(c['r1'], 4), depth=round(face - c['a1'], 4)); i += 1
    if not model and i < len(chain) and 0.5 < chain[i]['ang'] < 4:
        c = chain[i]; out['taper'] = dict(ang=round(c['ang'], 3), d_start=round(2 * c['r0'], 4), d_end=round(2 * c['r1'], 4), depth=round(face - c['a1'], 4)); i += 1
    if i < len(chain) and chain[i]['ang'] > 4 and abs(chain[i]['r1'] - chain[i]['r0']) < 0.06 and i + 1 < len(chain) and chain[i + 1]['ang'] < 0.05:
        c = chain[i]; out['step'] = dict(ang=round(c['ang'], 1), to_r=round(c['r1'], 4)); i += 1
    if i < len(chain) and chain[i]['ang'] < 0.05:
        c = chain[i]
        out['drill'] = dict(dia=round(2 * c['r0'], 4), from_depth=round(face - c['a0'], 4), to_depth=round(face - c['a1'], 4), end_a=round(c['a1'], 4))
        i += 1
        if i < len(chain):
            e = chain[i]
            out['drill']['end'] = (dict(kind='arc', to=(round(e['a1'], 4), round(e['r1'], 4))) if e['k'] == 'C' else
                                   dict(kind='cone', ang_to_axis=round(e['ang'], 1), point_incl=round(2 * e['ang'], 1), to=(round(e['a1'], 4), round(e['r1'], 4))))
        else:
            out['drill']['end'] = dict(kind='none (runs into the crossing / another bore)')
    return out


def ball_arcs(p, axis, sign):
    """circle edges of the section z = 0 centred on the leg axis (ball end of a drill): (centre a, R)"""
    E = edges(section(shape(p), (0, 0, 1), (0, 0, 0)))
    oth = [k for k in (0, 1) if k != axis][0]
    out = []
    for kind, P in E:
        if isinstance(kind, tuple) and abs(kind[1][oth]) < 1e-4 and abs(kind[1][2]) < 1e-4:
            out.append((round(sign * kind[1][axis], 4), round(kind[2], 4)))
    return sorted(set(out))


def measure_leg(p, axis, sign, oaxis, osign, model=False):
    S = plane_segs(p, axis, sign, oaxis, osign)
    face = max(max(s['a1'], s['a2']) for s in S)
    # hex corner line: the long horizontal at the largest r starting at the crossing (a ~ 0)
    hz = [s for s in S if s['k'] == 'L' and near(s['r1'], s['r2'], 1e-4) and s['a1'] < 0.02 and s['a2'] - s['a1'] > 0.1]
    cl = max(hz, key=lambda s: s['r1'])
    AC, hexl = cl['r1'], cl['a2']
    res = dict(leg=(axis, sign), face=round(face, 4), AC=round(AC, 4), hexl=round(hexl, 4))
    # what follows the arm end: a vertical step down to r1
    st = [s for s in S if s['k'] == 'L' and near(s['a1'], hexl) and near(s['a2'], hexl) and near(max(s['r1'], s['r2']), AC)]
    if st:
        r1 = min(st[0]['r1'], st[0]['r2']); res['step_r'] = round(r1, 4)
        col = [s for s in S if s['k'] == 'L' and near(s['r1'], r1) and near(s['r2'], r1) and near(s['a1'], hexl) and near(s['a2'], face)]
        if col: res['collar'] = dict(r=round(r1, 4), dia=round(2 * r1, 4), length=round(face - hexl, 4))
    # hex across flats inside the arm, beyond the puck (a between AC and hexl) - or the middle of the arm
    # (an arm that ends inside the corner puck radius has no clean hex section of its own: its A/F is read on the other arm)
    if hexl > AC + 0.02:
        a_x = (AC + hexl) / 2
        hx = hex_xsec(p, axis, a_x, sign)
        if hx: res['AF'] = round(2 * hx['flat_d'], 4); res['hex_xsec'] = dict(at=round(a_x, 4), **hx)
    else: res['AF'] = None; res['hex_xsec'] = f'arm ends inside the corner puck (hexl {hexl:.4f} <= AC {AC:.4f} + 0.02): A/F read on the other arm'
    # bores: the smallest-radius horizontal inner line of length > 0.1 inside the leg
    br = [s for s in S if near(s['r1'], s['r2'], 1e-4) and 0.01 < s['r1'] < AC - 0.05 and s['a2'] - s['a1'] > 0.1 and s['a2'] <= face + 1e-6
          and not ('step_r' in res and near(s['r1'], res['step_r']))]
    if br: b = min(br, key=lambda s: s['r1']); res['bore'] = dict(dia=round(2 * b['r1'], 4), a=(round(b['a1'], 4), round(b['a2'], 4)))
    if 'collar' in res:
        try: res['port'] = port(S, face, model=model)
        except (ValueError, IndexError, KeyError) as ex: res['port'] = f'not read: {type(ex).__name__} {ex}'
        res['ball_arcs_on_axis'] = ball_arcs(p, axis, sign)
    return res


def measure_elbow(p, model=False):
    (l1, e1), (l2, e2) = legs_of(p)
    assert l1[0] != l2[0] and 2 not in (l1[0], l2[0]), ('not a 90 deg elbow in the XY plane', l1, l2)
    legs = [measure_leg(p, *l1, *l2, model=model), measure_leg(p, *l2, *l1, model=model)]
    AC = max(L['AC'] for L in legs); AF = [L.get('AF') for L in legs]
    BR = max(a for a in AF if a) / 2
    return dict(file=_os.path.basename(p), bbox=bbox(p), AC_expected_from_AF=round(BR / math.cos(math.radians(30)), 4), legs=legs, puck=puck(p, AC, BR))


def measure_port_only(p, axis, sign, model=False):
    oax = [k for k in (0, 1) if k != axis][0]
    S = plane_segs(p, axis, sign, oax, -1)
    face = max(max(s['a1'], s['a2']) for s in S)
    return dict(file=_os.path.basename(p), leg=(axis, sign), port=port(S, face, model=model))


if __name__ == '__main__':
    args = sys.argv[1:]; model = '--model' in args
    if model: args.remove('--model')
    if args and args[0] == '--port':
        ax, sg = [int(v) for v in args[1].split(',')]
        for p in args[2:]: print(json.dumps(measure_port_only(p, ax, sg, model=model)))
    else:
        for p in args: print(json.dumps(measure_elbow(p, model=model)))
