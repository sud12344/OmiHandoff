# Pilot measurements for the new masters 2504 / 2505 / 2606 / 2611 (2026-10-02) with the validated forged.py extractor
# (forged_validate.py: 0 FAIL on 2650-08 / 5605-08 / 5600-16 / 6502-08 and the 2403 -08 JIC chain).
#   python tools/measure/forged_pilots.py [<step dir>] > pilot_measurements.json
# Leg angles are the directions of the legs in the Brennan STEP (XY plane, flats normal to Z), found from the bounding box and the sections:
#   2504-08-08-FG     : JIC 180 deg, JIC 45 deg (45 deg elbow, legs 135 deg apart)
#   2505-08-08-FG     : JIC 180 deg, female pipe 45 deg
#   2606-08-08-08-FG  : JIC 180 deg (run), female pipe 0 deg (run), JIC 90 deg (branch)
#   2611-06-06-06-FG  : JIC 180 deg (run), male pipe 0 deg (run), female pipe 90 deg (branch)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP
import sys, json
import forged as F
from section import load
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

PILOTS = {
    '2504-08-08-FG': [('JICM', 180, -1), ('JICM', 45, 1)],
    '2505-08-08-FG': [('JICM', 180, -1), ('NPTFF', 45, 1)],
    '2606-08-08-08-FG': [('JICM', 180, -1), ('NPTFF', 0, -1), ('JICM', 90, 1)],
    '2611-06-06-06-FG': [('JICM', 180, -1), ('NPTFM', 0, -1), ('NPTFF', 90, 1)],
}


def whole(p):
    s = load(p); g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g)
    n = 0; e = TopExp_Explorer(s, TopAbs_SOLID)
    while e.More(): n += 1; e.Next()
    b = Bnd_Box(); BRepBndLib.AddOptimal_s(s, b, False, False)
    return dict(solids=n, volume_in3=round(g.Mass() / 25.4 ** 3, 5), bbox_optimal=[round(v / 25.4, 4) for v in (b.CornerMin().X(), b.CornerMin().Y(), b.CornerMin().Z(), b.CornerMax().X(), b.CornerMax().Y(), b.CornerMax().Z())])


if __name__ == '__main__':
    sd = sys.argv[1] if len(sys.argv) > 1 else OP.STEP_DIR
    out = {}
    for pn, legs in PILOTS.items():
        p = _os.path.join(sd, f'BRENNAN_{pn}.stp')
        out[pn] = dict(step=p, whole=whole(p), corner_arcs=F.corner_arcs(p), legs=[F.KIND[k](p, th, side) for k, th, side in legs])
    print(json.dumps(out, indent=1))
