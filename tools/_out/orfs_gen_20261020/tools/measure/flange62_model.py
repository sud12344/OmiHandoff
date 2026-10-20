# OCP rebuild of gen_straight2 configurations with a code 62 flange end (2026-10-02, FLANGE62: 1800 / 1824) from the generator's OWN
# data, in the macro's feature order: DRIVE outline (the emit() vertex chain, checks/allcfg_check.straight_chain) revolved about X; for a
# 'flats' SPEC the two wrench flats = everything outside |y| <= WAF/2 removed over x = START..START+DEPTH (FLATCUT, flats normal to Y as the
# macro's Right-Plane rectangle); bores BORE_A / BORE_B (mode 'mid'). Threads are not modelled (masters are saved with THD_* suppressed),
# so the volumes are the ones sweep_configs reports on a saved master.
#
#   python tools/measure/flange62_model.py <root> [<pn> ...]       -> <GS_OUT or scratch>/MODEL_<pn>.stp + one line per configuration
#   (OMI_ROOT selects the review tables, e.g. the FLANGE62 TEST scratch root)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE, _os.path.join(_TOOLS, 'checks')):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, json, math
os.environ.setdefault('GS_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Ax2, gp_Dir
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID, TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Plane
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from nwo_model import face, vol, fuse, cut, write, MM
from allcfg_check import straight_chain


def nsolids(S):
    n = 0; e = TopExp_Explorer(S, TopAbs_SOLID)
    while e.More(): n += 1; e.Next()
    return n


def flats_faces(S):
    """2026-10-02 (review FLANGE62 round 2): the same reading of the wrench flats as the macro's FlatsAcross - planar faces parallel to the
    axis (X) that do not contain it: count, how many are parallel to the first, distance between the outermost two along their normal,
    axial extent (tight face boxes). Inches."""
    n = npar = 0; n0 = None; dl, dh = 1e30, -1e30; x0, x1 = 1e30, -1e30
    e = TopExp_Explorer(S, TopAbs_FACE)
    while e.More():
        f = TopoDS.Face(e.Current()); a = BRepAdaptor_Surface(f)
        if a.GetType() == GeomAbs_Plane:
            pl = a.Plane(); d_ = pl.Axis().Direction(); o_ = pl.Location()
            nx, ny, nz = d_.X(), d_.Y(), d_.Z()
            if abs(nx) < 1e-4:
                sg = -1.0 if (ny < -1e-4 or (abs(ny) <= 1e-4 and nz < 0)) else 1.0
                d = sg * (ny * o_.Y() + nz * o_.Z()) / MM
                if abs(d) > 0.0005 / 0.0254:
                    n += 1
                    if n0 is None: n0 = (sg * ny, sg * nz)
                    if abs(sg * ny * n0[0] + sg * nz * n0[1] - 1) < 1e-4: npar += 1
                    dl, dh = min(dl, d), max(dh, d)
                    bb = Bnd_Box(); BRepBndLib.AddOptimal_s(f, bb, False, False)
                    x0, x1 = min(x0, bb.CornerMin().X() / MM), max(x1, bb.CornerMax().X() / MM)
        e.Next()
    return dict(n=n, parallel=npar, across=round(dh - dl, 6) if n else None, x0=round(x0, 6) if n else None, x1=round(x1, 6) if n else None)


def build(b, sp):
    cols, EA, EB, L, hexb, rB, body, chk = b
    V = straight_chain(EA, EB, L, rB)
    S = BRepPrimAPI_MakeRevol(face([(x, r, 0) for x, r in V]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), 2 * math.pi).Shape()
    v_rev = vol(S)
    v_flats = None
    if sp.get('flats'):
        x0, dep, af = cols['START@FLATCUT'], cols['DEPTH@FLATCUT'], cols['WAF@FLATS']; BIG = 10.0
        v0 = vol(S)
        for y0, y1 in ((af / 2, BIG), (-BIG, -af / 2)):
            S = cut(S, BRepPrimAPI_MakeBox(gp_Pnt(x0 * MM, y0 * MM, -BIG * MM), gp_Pnt((x0 + dep) * MM, y1 * MM, BIG * MM)).Shape())
        v_flats = v0 - vol(S)
    mode = sp['bore'][0]
    if mode == 'mid':
        dA, sA = cols['DA@BORE_A'], cols['DEPTH@BORECUT_A']; dB, sB = cols['DB@BORE_B'], cols['DEPTH@BORECUT_B']
        S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), dA / 2 * MM, sA * MM).Shape())
        S = cut(S, BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(L * MM, 0, 0), gp_Dir(-1, 0, 0)), dB / 2 * MM, sB * MM).Shape())
    elif mode != 'none':
        raise NotImplementedError(f'bore mode {mode}')
    return S, dict(v_revolve=round(v_rev, 6), v_flats_removed=round(v_flats, 6) if v_flats is not None else None,
                   flats_faces=flats_faces(S) if sp.get('flats') else None)


if __name__ == '__main__':
    import gen_straight2 as G
    root = sys.argv[1]; pns = sys.argv[2:]; sp = G.SPEC[root]
    built, skipped = G.build_rows(root)
    od = os.environ['GS_OUT']; os.makedirs(od, exist_ok=True)
    for b in built:
        pn = b[0]['$PRP@PartNo']
        if b[7] or (pns and pn not in pns): continue
        S, info = build(b, sp)
        p = os.path.join(od, f'MODEL_{pn}.stp'); write(S, p)
        print(json.dumps(dict(pn=pn, solids=nsolids(S), volume_in3=round(vol(S), 6), **info, step=p)))
