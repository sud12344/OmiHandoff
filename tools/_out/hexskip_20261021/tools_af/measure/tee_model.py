# OCP rebuild of gen_tee tees and 45 deg elbows with JIC / male pipe / female pipe legs (2026-10-02, new masters 2504 / 2505 / 2606 / 2611),
# from the generator's OWN data (build_rows), in the macro's feature order: LEGi revolves (tee: leg 1 +X, leg 2 -X, leg 3 +Y; 45 deg elbow:
# leg 1 +X, leg 2 on the 135 deg axis), hex bars (tee: RUN through the crossing from -HEXL2 to +HEXL1 + the HEX3 branch arm; elbow: HEX1 / HEX2
# arms + the 30deg double-cone corner PUCK about Z), flats normal to Z; then POCKETi (female port tap drill, from the face to its pocket depth),
# BOREi (connecting drill where the leg has one) and the bores of the other legs (face to the crossing). Threads are not modelled (the saved
# masters carry every THD_ feature suppressed), so the volume is the one sweep_configs reports on a saved master.
#
#   python tools/measure/tee_model.py <root> <pn> [<pn> ...]     -> <out>/MODEL_<pn>.stp + volume
#   python tools/measure/tee_model.py --all <root>               -> every configuration: one solid?, volume (EXPECTED.md)
#   python tools/measure/tee_model.py --relief <root>            -> per configuration: corner material standing in each JIC thread relief groove
#   python tools/measure/tee_model.py --cmp <root> <pn>          -> closed loop vs the Brennan STEP of <pn>: the model placed like the STEP
#                                                                  (mirror / rotation about Z), both forged.py readings, symmetric difference
#                                                                  split into its connected pieces (where and how much)
#   python tools/measure/tee_model.py --sections <root> <pn>     -> key sections, Brennan STEP vs the model placed like it: area of the leg
#                                                                  plane z = 0, of each leg's axial half-plane (leg axis + Z) and of two planes
#                                                                  normal to each leg (middle of its end zone; 0.03 behind its hex face /
#                                                                  collar start) -> sec_<pn>.json
# Output folder: $TEE_MODEL_OUT or tools/_out/scratch. Brennan STEPs: $BRENNAN_STEP_DIR or 09_STEP_FILES (omi_paths).
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GT_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Vec, gp_Trsf, gp_Ax2 as _Ax2
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from nwo_model import face, vol, fuse, cut, write, MM

OUTD = os.environ.get('TEE_MODEL_OUT', OP.SCRATCH)
U135 = (math.cos(math.radians(135)), math.sin(math.radians(135)))


def axes(sp, n):
    if sp.get('e45'): return [(1.0, 0.0), U135]
    if sp.get('elbow'): return [(1.0, 0.0), (0.0, 1.0)]
    return [(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)][:n]


def revolve_leg(V, u):
    ux, uy = u; nx, ny = -uy, ux
    return BRepPrimAPI_MakeRevol(face([(a * ux + r * nx, a * uy + r * ny, 0) for a, r in V]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(ux, uy, 0)), 2 * math.pi).Shape()


def hex_prism(u, af, a0, a1):
    """hexagon A/F af normal to the axis u (in the XY plane), flats normal to Z, from a0 to a1 along u"""
    ux, uy = u; nx, ny = -uy, ux; Rc = af / math.sqrt(3); h = af / 2; v = (a1 - a0) * MM
    q = [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]
    return BRepPrimAPI_MakePrism(face([(a0 * ux + p * nx, a0 * uy + p * ny, z) for p, z in q]), gp_Vec(v * ux, v * uy, 0)).Shape()


def cyl(u, r, a0, a1):
    ux, uy = u
    return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(a0 * ux * MM, a0 * uy * MM, 0), gp_Dir(ux, uy, 0)), r * MM, (a1 - a0) * MM).Shape()


def nsolids(S):
    n = 0; e = TopExp_Explorer(S, TopAbs_SOLID)
    while e.More(): n += 1; e.Next()
    return n


def build(sp, b):
    legs = b['legs']; BR = b['BR']; AC = b['AC']; AF = b['AF']; U = axes(sp, len(legs))
    S = None
    for lg, u in zip(legs, U):
        s = revolve_leg(lg['V'], u); S = s if S is None else fuse(S, s)
    if sp.get('elbow'):
        for lg, u in zip(legs, U): S = fuse(S, hex_prism(u, AF, 0.0, lg['hexl']))
        h = BR; r1 = AC - BR * math.tan(math.radians(30))
        S = fuse(S, BRepPrimAPI_MakeRevol(face([(0, 0, -h), (r1, 0, -h), (AC, 0, 0), (r1, 0, h), (0, 0, h)]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), 2 * math.pi).Shape())
    else:
        S = fuse(S, hex_prism((1.0, 0.0), AF, -legs[1]['hexl'], legs[0]['hexl']))
        if sp.get('cross'): S = fuse(S, hex_prism((0.0, 1.0), AF, -legs[3]['hexl'], legs[2]['hexl']))
        else: S = fuse(S, hex_prism((0.0, 1.0), AF, 0.0, legs[2]['hexl']))
    for lg, u in zip(legs, U):          # macro order: every leg's pocket / bore, from its face
        M = lg.get('Mtip', lg['V'][-1][0])
        if lg['kind'] == 'NPTFF':
            S = cut(S, cyl(u, lg['td'] / 2, M - lg['pocket'], M))
            if not lg['to_centre']: S = cut(S, cyl(u, lg['conn'] / 2, 0.0, M))
        else:
            S = cut(S, cyl(u, lg['bore'] / 2, 0.0, M))
    return S


# how each Brennan pilot STEP lies relative to the model (legs in the XY plane): a mirror x -> -x or a rotation about Z
PLACE_LIKE_BRENNAN = {'2504-08-08-FG': ('mirror_x',), '2606-08-08-08-FG': ('mirror_x',), '2611-06-06-06-FG': ('mirror_x',), '2505-08-08-FG': ('rot_z', 45.0)}
# the leg angles of the model in its own frame (for forged.py on the model STEP), per root: (kind, angle, side)
MODEL_LEGS = {'2504': [('JICM', 0, -1), ('JICM', 135, 1)], '2505': [('NPTFF', 0, -1), ('JICM', 135, 1)],
              '2606': [('JICM', 0, -1), ('NPTFF', 180, -1), ('JICM', 90, 1)], '2611': [('JICM', 0, -1), ('NPTFM', 180, -1), ('NPTFF', 90, 1)]}
# model leg -> Brennan leg (index in forged_pilots.PILOTS[pn])
MODEL_TO_BRENNAN_LEG = {'2504': [0, 1], '2505': [1, 0], '2606': [0, 1, 2], '2611': [0, 1, 2]}


def place(S, how):
    t = gp_Trsf()
    if how[0] == 'mirror_x': t.SetMirror(_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)))
    else: t.SetRotation(gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(0, 0, 1)), math.radians(how[1]))
    return BRepBuilderAPI_Transform(S, t, True).Shape()


def pieces(S):
    out = []; e = TopExp_Explorer(S, TopAbs_SOLID)
    while e.More():
        s = e.Current(); g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); c = g.CentreOfMass()
        v = g.Mass() / MM ** 3
        if v > 1e-7: out.append(dict(volume=round(v, 6), centre=[round(c.X() / MM, 3), round(c.Y() / MM, 3), round(c.Z() / MM, 3)]))
        e.Next()
    return sorted(out, key=lambda d: -d['volume'])


def relief_fill(sp, b, S=None):
    """volume of forged-corner material (the 45 deg elbow's corner PUCK or the other legs' hex) standing inside each male JIC leg's thread
    relief groove (from the hex face to the thread start, between the leg's own profile and the thread major): the model fuses the puck
    after the leg revolves, so where the hex arm ends inside the puck radius the puck fills part of the groove (Brennan turns the relief
    through it - 2505-08-08-FG). {leg number: in^3}; 0 = the groove is clean"""
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    if S is None: S = build(sp, b)
    out = {}
    for i, (lg, u) in enumerate(zip(b['legs'], axes(sp, len(b['legs']))), 1):
        if lg['kind'] != 'JICM': continue
        V = lg['V']; sh, rC = V[2][0], V[3][1]; x2, rM = V[5]
        groove = revolve_leg([(sh, rC), (V[4][0], rC), (x2, rM), (sh, rM)], u)
        out[i] = round(vol(BRepAlgoAPI_Common(S, groove).Shape()), 6)
    return out


def beyond_face(sp, b, S=None):
    """volume of material standing OUTSIDE each male JIC leg's own end profile beyond its hex face (a > hex face): on a clean part 0 - the
    JIC end is turned from the hex face to the tip. Catches the corner puck / the other legs' hex arms of a forged elbow reaching past a
    JIC hex face (the groove fill of relief_fill is part of it). {leg number: in^3}"""
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    if S is None: S = build(sp, b)
    out = {}
    for i, (lg, u) in enumerate(zip(b['legs'], axes(sp, len(b['legs']))), 1):
        if lg['kind'] != 'JICM': continue
        V = lg['V']; big = 4 * b['AC'] + 1.0
        prof = [p_ for p_ in V[3:-1]]                      # (sh, rC) ... (M, rT): the end profile from the hex face to the tip
        tool = revolve_leg(prof + [(V[-2][0], big), (V[3][0], big)], u)
        out[i] = round(vol(BRepAlgoAPI_Common(S, tool).Shape()), 6)
    return out


def plane_area(S, o, n, xd, u0, u1, v0, v1):
    """area (in^2) of the solid S cut by the bounded plane through o (in) with normal n, local X along xd, u in [u0, u1], v in [v0, v1]
    (in): the common of S with the planar face (a Boolean of different dimensions = the face part inside the solid)"""
    from OCP.gp import gp_Ax3, gp_Pln
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    pl = gp_Pln(gp_Ax3(gp_Pnt(*[c * MM for c in o]), gp_Dir(*n), gp_Dir(*xd)))
    f = BRepBuilderAPI_MakeFace(pl, u0 * MM, u1 * MM, v0 * MM, v1 * MM).Face()
    c = BRepAlgoAPI_Common(S, f); c.Build()
    g = GProp_GProps(); BRepGProp.SurfaceProperties_s(c.Shape(), g)
    return g.Mass() / MM ** 2


def key_sections(B, Sb, legs_b):
    """key sections of the Brennan STEP B and the model Sb (placed like B); legs_b = forged.py readings of B's legs (theta in B's frame)"""
    out = [dict(plane='leg plane z = 0 (every leg)', B=plane_area(B, (0, 0, 0), (0, 0, 1), (1, 0, 0), -5, 5, -5, 5),
                M=plane_area(Sb, (0, 0, 0), (0, 0, 1), (1, 0, 0), -5, 5, -5, 5))]
    for i, L in enumerate(legs_b, 1):
        t = math.radians(L['theta']); u = (math.cos(t), math.sin(t), 0.0); w = (-math.sin(t), math.cos(t), 0.0)
        R = L['AF_flats'] / math.sqrt(3) + 0.02 if L.get('AF_flats') else 1.0
        out.append(dict(plane=f'leg {i} ({L["kind"]} at {L["theta"]} deg) axial half-plane (axis + Z)', B=plane_area(B, (0, 0, 0), w, u, 0, 5, -5, 5),
                        M=plane_area(Sb, (0, 0, 0), w, u, 0, 5, -5, 5)))
        if L['kind'] == 'NPTFF': s0, s1 = L['collar_from'], L['face']
        else: s0, s1 = L['hex_face'], L['tip']
        for what, a in (('end zone middle', (s0 + s1) / 2), ('0.03 behind the ' + ('collar start' if L['kind'] == 'NPTFF' else 'hex face'), s0 - 0.03)):
            o = (a * u[0], a * u[1], 0.0)
            out.append(dict(plane=f'leg {i} ({L["kind"]}) normal at a = {a:.4f} ({what})', B=plane_area(B, o, u, (0, 0, 1), -R, R, -R, R),
                            M=plane_area(Sb, o, u, (0, 0, 1), -R, R, -R, R)))
    for d in out:
        d['B'] = round(d['B'], 5); d['M'] = round(d['M'], 5); d['M_minus_B'] = round(d['M'] - d['B'], 5)
        d['pct'] = round(100 * (d['M'] - d['B']) / d['B'], 2) if d['B'] else None
    return out


if __name__ == '__main__':
    import gen_tee as T
    a = sys.argv[1:]
    os.makedirs(OUTD, exist_ok=True)
    if a[0] == '--relief':
        root = a[1]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        for b in built:
            if b['chk']: continue
            S = build(sp, b)
            print(json.dumps(dict(pn=b['pn'], AC=round(b['AC'], 4), hexl=[L['hexl'] for L in b['legs']], relief_filled_in3=relief_fill(sp, b, S),
                                  outside_jic_profile_beyond_hex_face_in3=beyond_face(sp, b, S))))
    elif a[0] == '--all':
        root = a[1]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        for b in built:
            if b['chk']: continue
            S = build(sp, b)
            print(json.dumps(dict(pn=b['pn'], solids=nsolids(S), volume_in3=round(vol(S), 5))))
    elif a[0] == '--cmp':
        import forged as F
        root, pn = a[1], a[2]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        b = [x for x in built if x['pn'] == pn and not x['chk']][0]
        S = build(sp, b); pm = os.path.join(OUTD, f'MODEL_{pn}.stp'); write(S, pm)
        res = dict(pn=pn, model_step=pm, model_volume=round(vol(S), 5), model_solids=nsolids(S), model_legs=[F.KIND[k](pm, th, sd) for k, th, sd in MODEL_LEGS[root]])
        bp = os.path.join(os.environ.get('BRENNAN_STEP_DIR', OP.STEP_DIR), f'BRENNAN_{pn}.stp')
        B = F.shape(bp); Sb = place(S, PLACE_LIKE_BRENNAN[pn])
        import forged_pilots as FP          # the Brennan readings in the model's leg order (closed loop: model reading vs pilot reading)
        res['brennan_legs'] = [F.KIND[k](bp, th, sd) for k, th, sd in (FP.PILOTS[pn][j] for j in MODEL_TO_BRENNAN_LEG[root])]
        res['brennan_volume'] = round(vol(B), 5)
        res['brennan_minus_model'] = round(vol(cut(B, Sb)), 5); res['model_minus_brennan'] = round(vol(cut(Sb, B)), 5)
        res['pieces_brennan_only'] = pieces(cut(B, Sb)); res['pieces_model_only'] = pieces(cut(Sb, B))
        json.dump(res, open(os.path.join(OUTD, f'cmp_{pn}.json'), 'w'), indent=1)      # (the OCP STEP writer prints its statistics to stdout)
        print('written', os.path.join(OUTD, f'cmp_{pn}.json'))
    elif a[0] == '--sections':
        import forged as F, forged_pilots as FP
        root, pn = a[1], a[2]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        b = [x for x in built if x['pn'] == pn and not x['chk']][0]
        bp = os.path.join(os.environ.get('BRENNAN_STEP_DIR', OP.STEP_DIR), f'BRENNAN_{pn}.stp')
        B = F.shape(bp); Sb = place(build(sp, b), PLACE_LIKE_BRENNAN[pn])
        legs_b = [F.KIND[k](bp, th, sd) for k, th, sd in FP.PILOTS[pn]]
        res = dict(pn=pn, frame='Brennan STEP frame (model placed like the STEP: ' + ' '.join(map(str, PLACE_LIKE_BRENNAN[pn])) + ')',
                   sections=key_sections(B, Sb, legs_b))
        json.dump(res, open(os.path.join(OUTD, f'sec_{pn}.json'), 'w'), indent=1)
        for d in res['sections']: print(f'{pn}  {d["plane"]:70s} Brennan {d["B"]:8.5f}  model {d["M"]:8.5f}  diff {d["M_minus_B"]:+8.5f} in^2 ({d["pct"]:+.2f} %)')
    else:
        root = a[0]; built, _ = T.build_rows(root); sp = T.SPEC[root]
        for b in built:
            if b['pn'] not in a[1:] or b['chk']: continue
            S = build(sp, b); p = os.path.join(OUTD, f'MODEL_{b["pn"]}.stp'); write(S, p)
            print(b['pn'], 'solids', nsolids(S), 'volume %.5f in^3' % vol(S), '->', p)
