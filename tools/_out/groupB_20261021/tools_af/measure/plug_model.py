"""plug_model.py - closed loop for the PLUGS masters (2026-10-02): rebuild configurations of 6408HHP / 5406HHP / 5406SHP from the
generator's OWN geometry with OCP - the DRIVE vertex chain revolved (checks/allcfg_check.straight_chain, the chain emit() draws), the
internal hex socket cut (SocketCut: hex prism, across flats SOCKAF, DEPTH from the head face, flat bottom) and the square head cut
(ZoneSquareCut: everything outside the square removed over the head length); threads are not modelled (suppressed in the saved masters) -
write each as a STEP, measure it with tools/measure/plugs.py (the extractor validated on the Brennan STEPs) and compare with the table
values the configuration must carry. With --pilot it also compares the pilot configuration with the Brennan pilot STEP (volume and the
key sections) and rebuilds the Brennan details the model leaves out, so that the volume difference is accounted for.

    OMI_ROOT=<root> GS_OUT=<dir> python tools/measure/plug_model.py <spec root> <out dir> [--pilot]
"""
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _os.path.join(_TOOLS, 'checks'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, os, math, json
os.environ.setdefault('GS_OUT', OP.SCRATCH)
from OCP.gp import gp_Pnt, gp_Ax1, gp_Dir, gp_Vec
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakeRevol, BRepPrimAPI_MakePrism
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
MM = 25.4


def face(pts3):
    poly = BRepBuilderAPI_MakePolygon()
    for p in pts3: poly.Add(gp_Pnt(*[c * MM for c in p]))
    poly.Close()
    return BRepBuilderAPI_MakeFace(poly.Wire()).Face()


def vol(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass() / MM ** 3


def nsolids(s):
    n = 0; ex = TopExp_Explorer(s, TopAbs_SOLID)
    while ex.More(): n += 1; ex.Next()
    return n


def revolve(V):
    return BRepPrimAPI_MakeRevol(face([(a, r, 0) for a, r in V]), gp_Ax1(gp_Pnt(0, 0, 0), gp_Dir(1, 0, 0)), 2 * math.pi).Shape()


def prism(poly_yz, x0, x1):
    return BRepPrimAPI_MakePrism(face([(x0, y, z) for y, z in poly_yz]), gp_Vec((x1 - x0) * MM, 0, 0)).Shape()


def hexagon(af):
    # flats normal to z (one flat "horizontal" in a sketch whose x axis is the model y axis); circumradius af / sqrt 3
    Rc = af / math.sqrt(3); h = af / 2
    return [(Rc, 0), (Rc / 2, h), (-Rc / 2, h), (-Rc, 0), (-Rc / 2, -h), (Rc / 2, -h)]


def square(af):
    h = af / 2
    return [(h, h), (-h, h), (-h, -h), (h, -h)]


def cut(a, b): return BRepAlgoAPI_Cut(a, b).Shape()
def fuse(a, b): return BRepAlgoAPI_Fuse(a, b).Shape()


def build(b):
    """the configuration as the macro builds it (threads suppressed)"""
    from allcfg_check import straight_chain
    cols, EA, EB, L, hexb, rB, body, chk = b
    S = revolve(straight_chain(EA, EB, L, rB))
    if EB.get('socket'):
        so = EB['socket']; S = cut(S, prism(hexagon(so['af']), L - so['depth'], L + 0.05))
    if EB['kind'] == 'SQHEAD':
        big = 2 * rB + 1.0
        ring = cut(prism(square(big), L - EB['H'], L + 0.05), prism(square(EB['af']), L - EB['H'] - 0.01, L + 0.06))
        S = cut(S, ring)
    return S


def write(s, path):
    w = STEPControl_Writer(); w.Transfer(s, STEPControl_AsIs); w.Write(path)


def expect(root, b):
    cols, EA, EB, L, hexb, rB, body, chk = b
    e = dict(L=L)
    if root == '6408HHP':
        o = EA['o']
        e.update(head_dia=2 * rB, head_len=round(L - EA['endlen'], 4), sock_af=EB['socket']['af'], sock_depth=EB['socket']['depth'],
                 THDL=o['THDL'], GD=o['GD'], GW=o['GW'], thd_dia=o['TM'])
    elif root == '5406HHP':
        e.update(blank_dia=2 * rB, sock_af=EB['socket']['af'], sock_depth=EB['socket']['depth'], cone_r0=round(EA['rS'], 4), cone_end=round(EA['endlen'], 4))
    else:
        e.update(blank_dia=2 * rB, sq_af=EB['af'], head_len=EB['H'], shoulder=round(L - EB['H'], 4), cone_r0=round(EA['rS'], 4), cone_end=round(EA['endlen'], 4))
    return e


def measured(root, m):
    if root == '6408HHP':
        return dict(L=m['L'], head_dia=m['head']['head_dia'], head_len=m['head']['head_len'], sock_af=m['socket']['af'], sock_depth=m['socket']['depth'],
                    THDL=m['orb']['THDL'], GD=m['orb']['GD'], GW=m['orb']['GW'], thd_dia=m['orb']['thd_dia'])
    if root == '5406HHP':
        return dict(L=m['L'], blank_dia=m['head']['head_dia'], sock_af=m['socket']['af'], sock_depth=m['socket']['depth'], cone_r0=m['nptf']['cone_r0'], cone_end=m['nptf']['cone_end'])
    return dict(L=m['L'], blank_dia=m['nptf']['collar_dia'], sq_af=m['square']['af'], head_len=m['square']['head_len'], shoulder=m['square']['shoulder_a'],
                cone_r0=m['nptf']['cone_r0'], cone_end=m['nptf']['cone_end'])


def brennan_details(root, b):
    """the model PLUS the pilot details it leaves out (measured on the pilot STEP) - its volume must come close to the STEP's;
    returns (solid, list of what was added)"""
    import gen_straight2 as G
    cols, EA, EB, L, hexb, rB, body, chk = b
    S = build(b); added = []
    def chamfer_ring(xf, r_out, c, inward):     # 45deg x c chamfer on the outer edge of a face at xf (material side inward = -1 / +1 along x)
        x1 = xf + inward * c
        return revolve([(xf, r_out - c), (xf, r_out + 0.01), (x1, r_out + 0.01), (x1, r_out)]) if inward > 0 else revolve([(x1, r_out), (x1, r_out + 0.01), (xf, r_out + 0.01), (xf, r_out - c)])
    if root == '6408HHP':
        o = EA['o']; rM = o['TM'] / 2; rG = o['GD'] / 2
        S = cut(S, revolve([(0, rM - 0.0475), (0, rM + 0.01), (0.0475, rM + 0.01), (0.0475, rM)])); added.append('ORB tip chamfer 0.0475 x 45deg')
        dx = (rM - rG) / math.tan(math.radians(60))
        S = cut(S, revolve([(o['THDL'] - dx, rM), (o['THDL'] - dx, rM + 0.01), (o['THDL'], rM + 0.01), (o['THDL'], rG)])); added.append('60deg thread run-out instead of the step')
        S = cut(S, chamfer_ring(EA['endlen'], rB, 0.0087, +1)); S = cut(S, chamfer_ring(L, rB, 0.0087, -1)); added.append('head edge chamfers 45deg x 0.0087 (both)')
        rm = G.PLUG_PILOT[root]['csk_dia'] / 2         # 90deg countersink: cone from dia csk at the face to the axis rm deep
        S = cut(S, revolve([(L - rm, 0), (L, rm), (L + 0.01, rm), (L + 0.01, 0)]))
        added.append('socket mouth countersink 90deg to dia 0.375')
    else:
        # Brennan male NPTF blank: 0.0626 x 45deg tip chamfer, cone dia 0.7912 at the tip (extrapolated) at 1.788deg up to the measured cone end,
        # then the D collar; replaces the model's ASME crest cone (the D blank is the same)
        m = G.PLUG_PILOT[root]; t = math.tan(math.radians(1.788)); r0 = 0.7912 / 2; ce = m['cone_end']
        x_sh = L if root == '5406HHP' else m['shoulder']
        brennan = revolve([(0, 0), (0, 0.335), (0.0626, 0.335 + 0.0626), (ce, r0 + ce * t), (ce, rB), (x_sh, rB), (x_sh, 0)])
        model_part = revolve([(0, 0), (0, rB + 0.2), (x_sh, rB + 0.2), (x_sh, 0)])
        S = fuse(cut(S, model_part), brennan)
        if EB.get('socket'):     # the blank replaced the whole 5406HHP body: cut the same socket again
            so = EB['socket']; S = cut(S, prism(hexagon(so['af']), L - so['depth'], L + 0.05))
        added.append(f'Brennan blank: tip chamfer 0.0626 x 45deg, cone dia 0.7912 (tip, extrapolated) at 1.788deg to {ce}, D collar - instead of the ASME crest cone capped at D')
        if root == '5406HHP':
            rm = m['csk_dia'] / 2
            S = cut(S, revolve([(L - rm, 0), (L, rm), (L + 0.01, rm), (L + 0.01, 0)])); added.append(f'socket mouth countersink 90deg to dia {m["csk_dia"]}')
    return S, added


if __name__ == '__main__':
    import gen_straight2 as G
    import plugs as PL
    root, outd = sys.argv[1], sys.argv[2]; pilot = '--pilot' in sys.argv
    os.makedirs(outd, exist_ok=True)
    built, skipped = G.build_rows(root)
    ok = [b for b in built if not b[7]]
    kind = 'square' if root == '5406SHP' else 'socket'
    res = []
    for b in ok:
        pn = b[0]['$PRP@PartNo']; S = build(b); f = os.path.join(outd, pn.replace(' ', '_') + '.stp'); write(S, f)
        m = PL.run(kind, f); PL._cache.clear()
        e = expect(root, b); mm = measured(root, m)
        dev = {k: round(mm[k] - e[k], 4) for k in e if k in mm}
        res.append(dict(pn=pn, volume_in3=round(vol(S), 5), solids=nsolids(S), expected=e, measured=mm, max_abs_dev=max(abs(v) for v in dev.values()), dev=dev))
        print(f"{pn:22} vol {vol(S):.5f} in3  solids {nsolids(S)}  max |measured - table| {max(abs(v) for v in dev.values()):.4f}  {dev}")
    out = dict(root=root, configs=res)
    if pilot:
        pp = G.PLUG_PILOT[root]; stp = os.path.join(OP.STEP_DIR if os.path.isdir(OP.STEP_DIR) else r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\09_STEP_FILES', pp['step'])
        if not os.path.exists(stp): stp = os.path.join(r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\09_STEP_FILES', pp['step'])
        bp = [b for b in ok if b[0]['$PRP@PartNo'].startswith(pp['pn'])]
        if bp:
            b = bp[0]; S = build(b); vm = vol(S)
            ms = PL.run(kind, stp); PL._cache.clear()
            D, added = brennan_details(root, b); vd = vol(D)
            fD = os.path.join(outd, 'PILOT_model_plus_brennan_details.stp'); write(D, fD)
            md = PL.run(kind, fD); PL._cache.clear()
            out['pilot'] = dict(step=pp['step'], pn=b[0]['$PRP@PartNo'], step_volume=ms['volume_in3'], model_volume=round(vm, 5),
                                model_vs_step=round(vm - ms['volume_in3'], 5), model_vs_step_pct=round(100 * (vm - ms['volume_in3']) / ms['volume_in3'], 2),
                                model_plus_details_volume=round(vd, 5), details_vs_step=round(vd - ms['volume_in3'], 5), details_added=added,
                                step_measured=measured(root, ms), model_measured=[r for r in res if r['pn'] == b[0]['$PRP@PartNo']][0]['measured'],
                                details_measured=measured(root, md))
            print(json.dumps(out['pilot'], indent=1))
    json.dump(out, open(os.path.join(outd, f'closed_loop_{root}.json'), 'w'), indent=1)
