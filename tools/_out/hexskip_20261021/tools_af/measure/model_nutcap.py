# 2026-10-02 (new masters, group NUTS-CAPS): OCP rebuild of the 0304 cap nut / 0306 locknut configurations from the generator's OWN
# geometry - the DRIVE vertex chain of every configuration (checks/allcfg_check.straight_chain = what the macro draws), revolved about the
# axis, hex-cut (common with a hex prism of HEXB across flats over the whole length, as HEXCUT), and for 0306 the through bore BORECUT_A
# (cylinder of DA = the thread minor over DEPTH = W). Threads are not modelled (the saved masters keep THD_* suppressed).
#   python tools/measure/model_nutcap.py <root> [part numbers ...]   (no part numbers = every configuration)
#     -> <out>/MODEL_<pn>.stp + one JSON line per configuration: volume, then the SAME extractor as on the Brennan STEP (capnut.py /
#        locknut.py) run on the rebuild = the closed loop (the extractor must return the table values)
#   python tools/measure/model_nutcap.py --replica <pilot json> <pilot STEP>
#     -> rebuild of the PILOT from its own measured profile, incl. the hex corner chamfers (not in the model): its volume must equal the
#        Brennan STEP volume - proves the measured description is complete (validation of the measurement)
# OCP_OUT (env) = output folder (default tools/_out/scratch).
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _os.path.join(_TOOLS, 'checks'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GS_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
MM = 25.4


def face(pts):
    poly = BRepBuilderAPI_MakePolygon()
    for p in pts: poly.Add(gp_Pnt(*[c * MM for c in p]))
    poly.Close()
    return BRepBuilderAPI_MakeFace(poly.Wire()).Face()


def vol(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass() / MM ** 3


def nsolids(s):
    n = 0; ex = TopExp_Explorer(s, TopAbs_SOLID)
    while ex.More(): n += 1; ex.Next()
    return n


def revolve(V):
    """profile (x, r) in the XY plane, revolved about X"""
    return BRepPrimAPI_MakeRevol(face([(x, r, 0.0) for x, r in V]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), 2 * math.pi).Shape()


def hex_prism(af, x0, x1):
    Rc = af / math.sqrt(3); h = af / 2
    q = [(0, Rc, 0), (0, Rc / 2, h), (0, -Rc / 2, h), (0, -Rc, 0), (0, -Rc / 2, -h), (0, Rc / 2, -h)]   # corners on Y, flats normal to Z
    return BRepPrimAPI_MakePrism(face([(x0, y, z) for _, y, z in q]), gp_Vec((x1 - x0) * MM, 0, 0)).Shape()


def build_cfg(cols, EA, EB, L, hexb, rB):
    from allcfg_check import straight_chain
    V = straight_chain(EA, EB, L, rB)
    S = revolve(V)
    S = BRepAlgoAPI_Common(S, hex_prism(hexb, -0.1, L + 0.1)).Shape()
    if 'DA@BORE_A' in cols:
        S = BRepAlgoAPI_Cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), cols['DA@BORE_A'] / 2 * MM, cols['DEPTH@BORECUT_A'] * MM).Shape()).Shape()
    return S, V


def write(S, path):
    w = STEPControl_Writer(); w.Transfer(S, STEPControl_AsIs); w.Write(path)


def replica(pj, step):
    """the pilot rebuilt from its measured profile (capnut.py / locknut.py JSON), hex corner chamfers included"""
    m = json.load(open(pj))
    if 'cavity' in m:      # cap: crown at a = 0, open face at a = L (pilot orientation)
        L = m['L']; ch = m['corner_chamfers']; Rc = m['corner_R']
        out = [(0.0, 0.0), (0.0, ch['A']['face_r']), (ch['A']['axial'], Rc), (L - ch['B']['axial'], Rc), (L, ch['B']['face_r'])]
        cav = []
        for e in m['cavity']:
            if e[0] == 'cyl': cav += [(L - e[2], e[1]), (L - e[3], e[1])]
            elif e[0] == 'cone': cav += [(L - e[2][0], e[2][1]), (L - e[3][0], e[3][1])]
            elif e[0] == 'step': cav += [(L - e[1], e[2]), (L - e[1], e[3])]
        V = out + cav
        V2 = [V[0]]
        for p in V[1:]:
            if abs(p[0] - V2[-1][0]) > 1e-9 or abs(p[1] - V2[-1][1]) > 1e-9: V2.append(p)
        S = revolve(V2)
        af = m['AF']
    else:                  # locknut: ring profile
        W = m['W']; ch = m['corner_chamfers']; Rc = m['corner_R']; a, b = m['csk_A'], m['csk_B']
        V2 = [(0.0, a['face_r']), (0.0, ch['A']['face_r']), (ch['A']['axial'], Rc), (W - ch['B']['axial'], Rc), (W, ch['B']['face_r']),
              (W, b['face_r']), (W - b['axial'], m['minor_r']), (a['axial'], m['minor_r'])]
        S = revolve(V2)
        af = m['AF']
    L_ = max(p[0] for p in V2)
    S = BRepAlgoAPI_Common(S, hex_prism(af, -0.1, L_ + 0.1)).Shape()
    from section import load
    B = load(step)
    return dict(replica_volume=round(vol(S), 5), brennan_volume=round(vol(B), 5), diff_pct=round(100 * (vol(S) - vol(B)) / vol(B), 3), profile=V2), S


if __name__ == '__main__':
    out = os.environ.get('OCP_OUT', OP.SCRATCH); os.makedirs(out, exist_ok=True)
    if sys.argv[1] == '--replica':
        r, S = replica(sys.argv[2], sys.argv[3])
        p = os.path.join(out, 'REPLICA_' + os.path.basename(sys.argv[3]).replace('BRENNAN_', ''))
        write(S, p); r['step'] = p; print(json.dumps(r))
        if os.environ.get('OCP_LOG'): open(os.environ['OCP_LOG'], 'a').write(json.dumps(r) + '\n')
        sys.exit(0)
    import gen_straight2 as G
    from capnut import measure_cap
    from locknut import measure_nut
    root = sys.argv[1]; pns = sys.argv[2:]
    built, _ = G.build_rows(root)
    for cols, EA, EB, L, hexb, rB, body, chk in built:
        pn = cols['$PRP@PartNo']
        if chk or (pns and pn not in pns): continue
        S, V = build_cfg(cols, EA, EB, L, hexb, rB)
        p = os.path.join(out, f'MODEL_{pn}.stp'); write(S, p)
        res = dict(pn=pn, volume=round(vol(S), 5), solids=nsolids(S), step=p)
        m = measure_cap(p) if root == '0304' else measure_nut(p)
        if root == '0304':
            want = dict(L=L, AF=hexb, minor_r=cols['JCAPB_MINR@DRIVE'], seat_start_depth=cols['JCAPB_MINL@DRIVE'], seat_angle=37.0,
                        seat_end_r=cols['JCAPB_PKR@DRIVE'], pocket_len=cols['JCAPB_PKL@DRIVE'], crown=round(L - EB['bottom'], 4))
            got = dict(L=m['L'], AF=m['AF'], minor_r=m['minor_r'], seat_start_depth=m['seat_start']['depth'], seat_angle=m['seat_angle'],
                       seat_end_r=m['seat_end']['r'], pocket_len=round(m['pocket']['bottom_depth'] - m['pocket']['from_depth'], 4), crown=m['crown'])
        else:
            want = dict(W=L, AF=hexb, minor_r=cols['NUTCSA_MINR@DRIVE'], cskA_r=cols['NUTCSA_CSR@DRIVE'], cskB_r=cols['NUTCSB_CSR@DRIVE'], csk_angle=45.0)
            got = dict(W=m['W'], AF=m['AF'], minor_r=m['minor_r'], cskA_r=m['csk_A']['face_r'], cskB_r=m['csk_B']['face_r'],
                       csk_angle=round((m['csk_A']['angle'] + m['csk_B']['angle']) / 2, 2))
        # lengths: within 6e-4 in (the extractor rounds to 4 places); angles: within 0.1 deg (computed from 4-place rounded points)
        bad = {k: (want[k], got[k]) for k in want if abs(float(want[k]) - float(got[k])) > (0.1 if 'angle' in k else 6e-4)}
        res.update(closed_loop='PASS' if not bad else 'FAIL', mismatches=bad, measured=got)
        print(json.dumps(res), flush=True)
        if os.environ.get('OCP_LOG'): open(os.environ['OCP_LOG'], 'a').write(json.dumps(res) + '\n')
