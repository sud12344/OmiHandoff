import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math
from prof import shape
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
MM = 25.4
def vol(s):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return g.Mass() / MM ** 3
def box(x0, y0, x1, y1):
    return BRepPrimAPI_MakeBox(gp_Pnt(x0 * MM, y0 * MM, -9 * MM), gp_Pnt(x1 * MM, y1 * MM, 9 * MM)).Shape()
pn = sys.argv[1]; cut = float(sys.argv[2])
for tag, p in (('BRENNAN', OP.step(pn)), ('MODEL', _os.path.join(OP.SCRATCH, f'MODEL_{pn}.stp'))):
    S = shape(p)
    # which axis is the ORB leg in this file: the model has JIC along +X and ORB along +Y
    parts = {'x>cut (leg +X)': box(cut, -9, 9, 9), 'y>cut (leg +Y)': box(-9, cut, 9, 9), 'corner': box(-9, -9, cut, cut)}
    print(tag, {k: round(vol(BRepAlgoAPI_Common(S, b).Shape()), 4) for k, b in parts.items()}, 'total', round(vol(S), 4))
