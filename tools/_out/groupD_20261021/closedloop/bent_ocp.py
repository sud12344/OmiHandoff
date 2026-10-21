"""bent_ocp.py (group D, 2026-10-21): OCP closed loop of the bent-tube masters against the Brennan family STEPs.

For a configuration, the solid is rebuilt in OCP from gen_bent's OWN numbers (build_rows on the stage tables: the end-piece chain
end1_profile, the PATH points of geom(), the head half-section of vba_head incl. the hub / the swivel half-section of vba_swivel, the
hex cuts, the bore) - i.e. what the macro builds, threads suppressed. The Brennan STEP is moved into the model frame (JIC tip at the
origin, JIC axis +X, leg 2 toward +Y) and both are compared: volume, box, bend torus (R, tube dia), the symmetric difference
(volume of A - B and B - A, OCP booleans) and the cylinders / planes that carry the table values.

    OMI_ROOT=<brennancad stage> GS_OUT=<scratch> GB_REV=stage python bent_ocp.py   -> closedloop/closedloop.txt
"""
import math, os, sys, importlib.util
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax1, gp_Ax2, gp_Vec, gp_Trsf, gp_Circ, gp_Pln
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Transform,
                                BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire)
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeSphere
from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_SOLID
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Torus, GeomAbs_Cylinder

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.abspath(os.path.join(H, '..', '..', '..'))
MM = 25.4
IN = 1.0            # the OCP model is built in inches; STEPs (mm) are scaled to inches on load
FACE = getattr(TopoDS, 'Face', None) or TopoDS.Face_s


def load_gb():
    s = importlib.util.spec_from_file_location('gen_bent', os.path.join(H, 'tools_gd', 'generators', 'gen_bent.py'))
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
    return m


def P3(x, y, z=0.0):
    return gp_Pnt(x, y, z)


def poly_face(pts):
    mp = BRepBuilderAPI_MakePolygon()
    for x, y in pts:
        mp.Add(P3(x, y))
    mp.Close()
    return BRepBuilderAPI_MakeFace(mp.Wire()).Face()


def revolve(pts, axis_p, axis_d):
    return BRepPrimAPI_MakeRevol(poly_face(pts), gp_Ax1(P3(*axis_p), gp_Dir(axis_d[0], axis_d[1], 0)), 2 * math.pi).Shape()


def fuse(a, b):
    return BRepAlgoAPI_Fuse(a, b).Shape()


def cut(a, b):
    return BRepAlgoAPI_Cut(a, b).Shape()


def vol(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass()


def box(s):
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    BRepMesh_IncrementalMesh(s, 0.0002, False, 0.05, True)       # box from a fine mesh: the analytic Add_s box is loose on tori
    b = Bnd_Box(); BRepBndLib.Add_s(s, b, True); lo, hi = b.CornerMin(), b.CornerMax()
    return (lo.X(), lo.Y(), lo.Z(), hi.X(), hi.Y(), hi.Z())


def cyl(p, d, r, h):
    return BRepPrimAPI_MakeCylinder(gp_Ax2(P3(*p), gp_Dir(d[0], d[1], 0)), r, h).Shape()


def tube(path, r):
    """solid of radius r along S -> T1 (X axis), arc centre Cb (radius RB, bend th), T2 -> E"""
    S, T1, Cb, RB, th, T2, E = path
    s = cyl((S[0], 0), (1, 0), r, T1[0] - S[0])
    # torus about Z through Cb, swept th from the -Y direction (the bend start T1 is straight below Cb)
    ax = gp_Ax2(P3(Cb[0], Cb[1]), gp_Dir(0, 0, 1), gp_Dir(0, -1, 0))
    s = fuse(s, BRepPrimAPI_MakeTorus(ax, RB, r, math.radians(th)).Shape())
    L2 = math.hypot(E[0] - T2[0], E[1] - T2[1])
    s = fuse(s, cyl(T2, ((E[0] - T2[0]) / L2, (E[1] - T2[1]) / L2), r, L2))
    return s


def hex_prism_x(x0, length, af):
    """hexagonal prism along X (flats normal to Y, as gen_bent's ZoneHexCut / expected_box: y = +-af/2, corners in Z)"""
    R = af / math.sqrt(3)
    pts = [(0.0, R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for a in range(90, 450, 60)]
    mp = BRepBuilderAPI_MakePolygon()
    for _, y, z in pts:
        mp.Add(gp_Pnt(x0, y, z))
    mp.Close()
    f = BRepBuilderAPI_MakeFace(mp.Wire()).Face()
    return BRepPrimAPI_MakePrism(f, gp_Vec(length, 0, 0)).Shape()


def hex_prism_y(cx, y0, length, af):
    """nut hex on the vertical leg 2 (6701): flats normal to X? - gen_bent's NUTHEXSK: polygon with one line horizontal in the
    NUTPLN sketch -> flats normal to Z; prism from y0 down (-Y) over length"""
    R = af / math.sqrt(3)
    mp = BRepBuilderAPI_MakePolygon()
    for a in range(0, 360, 60):
        mp.Add(gp_Pnt(cx + R * math.cos(math.radians(a)), y0, R * math.sin(math.radians(a))))
    mp.Close()
    f = BRepBuilderAPI_MakeFace(mp.Wire()).Face()
    return BRepPrimAPI_MakePrism(f, gp_Vec(0, -length, 0)).Shape()


def model(gb, X, cols):
    c, g, J, lib, S = X['c'], X['g'], X['J'], X['lib'], X['S']
    V, rB = gb.end1_profile(c, J)
    # the macro: round body BODYR = hex corner radius from endlen to LJ, hex-cut over the whole of it (ZoneHexCut START endlen, DEPTH
    # HEXL, LJ = endlen + HEXL) = exactly a hex prism there. OCP: JIC chain revolved up to endlen + the prism (a boolean on the
    # corner edges tangent to the round body made invalid solids)
    assert abs(V[-3][0] - J['endlen']) < 1e-9 and abs(V[-2][0] - J['endlen'] - c['HEXL']) < 1e-6
    body = revolve(V[:-3] + [(J['endlen'], 0.0)], (0, 0), (1, 0))
    body = fuse(body, hex_prism_x(J['endlen'], c['HEXL'], c['CHEX']))
    rt = c['TUBEOD'] / 2
    th = c['BEND']
    E = g['E']
    s = fuse(body, tube(((c['S'], 0), g['T1'], g['Cb'], c['RB'], th, g['T2'], E), rt))
    F, u, n = g['F'], g['u'], g['n']
    if S is None:          # flange head (+ hub)
        A = lambda a, r: (F[0] - a * u[0] + r * n[0], F[1] - a * u[1] + r * n[1])
        rO = c['O'] / 2
        pts = [A(0, 0), A(0, lib['GI']), A(lib['GD'], lib['GI']), A(lib['GD'], lib['GO']), A(0, lib['GO']), A(0, rO), A(lib['TH'], rO)]
        pts += [A(lib['TH'], c['HUBD'] / 2), A(c['HUBL'], c['HUBD'] / 2), A(c['HUBL'], 0)] if 'HUBD' in c else [A(lib['TH'], 0)]
        s = fuse(s, revolve(pts, F, u))
    else:                  # 6701 swivel: the vba_swivel half-section + the nut hex
        m = S['m']
        Pf = lambda a, r: (F[0] - a * u[0] + r * n[0], F[1] - a * u[1] + r * n[1])
        rb = c['D'] / 2
        seat_end = S['s_nt'] + (m['SEATR'] - rb) / gb.gs.TAN37
        Wl = [(seat_end, 0.0), (seat_end, rb), (S['s_nt'], m['SEATR']), (S['s_nt'], m['NOSER']), (m['FLOOR'], m['NOSER']),
              (m['FLOOR'], m['RELR']), (S['scb0'], m['RELR']), (m['TE'], S['rmin']), (S['cs'], S['rmin']), (0.0, S['rcs']), (0.0, S['Rn']),
              (m['HEXL'], S['Rn']), (m['HEXL'], m['SKF']), (m['SKS'], m['SKR']), (m['NUTL'], m['SKR']), (m['NUTL'], m['NECKR']),
              (m['BODYS'], m['NECKR']), (m['BODYS'], 0.0)]
        s = fuse(s, revolve([Pf(a, r) for a, r in Wl], F, u))
        zone = cyl((F[0], F[1] - m['HEXL']), (0, 1), S['Rn'] + 0.5, m['HEXL'])
        s = cut(s, cut(zone, hex_prism_y(F[0], F[1], m['HEXL'], S['nut_af'])))
    # bore: the PATHX centre line from BX before the tip to BX past the face
    BX = gb.BX
    s = cut(s, tube(((-BX, 0), g['T1'], g['Cb'], c['RB'], th, g['T2'], g['FX']), c['D'] / 2))
    return s


def common_fuzzy(a, b, tol=0.001):
    try:
        from OCP.TopTools import TopTools_ListOfShape as LS          # OCP 7.x
    except ImportError:
        from OCP.collections import List_TopoDS_Shape as LS         # OCP 8
    op = BRepAlgoAPI_Common()
    la, lb = LS(), LS()
    la.Append(a); lb.Append(b)
    op.SetArguments(la); op.SetTools(lb); op.SetFuzzyValue(tol); op.Build()
    return op.Shape()


def load_step(p):
    r = STEPControl_Reader(); assert r.ReadFile(p) == IFSelect_RetDone; r.TransferRoots(); return r.OneShape()


def to_model_frame(sh, dx, flip_y):
    t = gp_Trsf(); t.SetScaleFactor(1 / MM)
    sh = BRepBuilderAPI_Transform(sh, t, True).Shape()
    if flip_y:
        m = gp_Trsf(); m.SetMirror(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(0, 1, 0)))   # mirror in the XZ plane: y -> -y
        sh = BRepBuilderAPI_Transform(sh, m, True).Shape()
    t2 = gp_Trsf(); t2.SetTranslation(gp_Vec(dx, 0, 0))
    return BRepBuilderAPI_Transform(sh, t2, True).Shape()


def tori(sh):
    out = []
    ex = TopExp_Explorer(sh, TopAbs_FACE)
    while ex.More():
        a = BRepAdaptor_Surface(FACE(ex.Current()))
        if a.GetType() == GeomAbs_Torus:
            t = a.Torus(); q = t.Axis().Location()
            out.append((round(t.MajorRadius(), 4), round(2 * t.MinorRadius(), 4), round(q.X(), 4), round(q.Y(), 4)))
        ex.Next()
    return sorted(set(out))


def cyls(sh):
    out = set()
    ex = TopExp_Explorer(sh, TopAbs_FACE)
    while ex.More():
        a = BRepAdaptor_Surface(FACE(ex.Current()))
        if a.GetType() == GeomAbs_Cylinder:
            out.add(round(2 * a.Cylinder().Radius(), 3))
        ex.Next()
    return sorted(out)


CASES = [  # (root, config, STEP, dx to move the STEP's JIC tip to the origin, mirror y)
    ('1704T', '1704-08-08-Tube', 'BRENNAN_1704-08-08.stp', 0.657, True),
    ('1704T', '1804-08-08-Tube', 'BRENNAN_1804-08-08.stp', 0.657, True),
    ('1703T', '1703-08-08-Tube', 'BRENNAN_1703-08-08.stp', 0.657, True),
    ('1703T', '1803-12-12-Tube', 'BRENNAN_1803-12-12.stp', 0.864, True),
    ('6701', '6701-08-08', 'BRENNAN_6701-08-08.stp', 1.770, False),
]


def main():
    gb = load_gb()
    lines = [__doc__.split('\n')[0], '']
    built = {}
    for root, cfg, stp, dx, fl in CASES:
        if root not in built:
            built[root] = {b[0]['$PRP@PartNo']: b for b in gb.build_rows(root)[0] if not b[1]}
        b = built[root][cfg]
        A = model(gb, b[2], b[0])
        B = to_model_frame(load_step(os.path.join(ROOT, '09_STEP_FILES', stp)), dx, fl)
        va, vb = vol(A), vol(B)
        # plain Common first; fuzzy where it fails (the 6701 STEP sits 0.0001 off the model: tip x -1.7701) - and fuzzy failed on 1803
        cm = vol(BRepAlgoAPI_Common(A, B).Shape())
        if cm < 0.5 * min(va, vb):
            cm = vol(common_fuzzy(A, B))
        amb, bma = va - cm, vb - cm
        ba, bb = box(A), box(B)
        lines.append(f'== {cfg} (master {root}) vs {stp}')
        lines.append(f'   volume model {va:.4f} in^3, STEP {vb:.4f} in^3 ({100 * (va - vb) / vb:+.1f} %); model - STEP {amb:.4f}, STEP - model {bma:.4f} '
                     f'(symmetric difference {100 * (amb + bma) / vb:.1f} % of the STEP)')
        lines.append('   box  model ' + ' '.join(f'{v:+.4f}' for v in ba))
        lines.append('   box  STEP  ' + ' '.join(f'{v:+.4f}' for v in bb))
        lines.append('   box  diff  ' + ' '.join(f'{x - y:+.4f}' for x, y in zip(ba, bb)))
        lines.append(f'   bend torus (R, tube dia, centre x, y): model {[t for t in tori(A) if t[0] > 0.2]}')
        lines.append(f'                                         STEP  {[t for t in tori(B) if t[0] > 0.2 and t[1] > 0.1]}')
        lines.append(f'   cylinder dias model {cyls(A)}')
        lines.append(f'                 STEP  {cyls(B)}')
        lines.append('')
        print('\n'.join(lines[-9:]))
    open(os.path.join(H, 'closedloop', 'closedloop.txt'), 'w').write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    main()
