import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, json, math
from nwo import nwo_params
import nwo_chamfer as C
from prof import shape
from OCP.GProp import GProp_GProps
from OCP.BRepGProp import BRepGProp
def vol(p):
    g = GProp_GProps(); BRepGProp.VolumeProperties_s(shape(p), g); return g.Mass() / 25.4 ** 3
for pn in sys.argv[1:]:
    B = OP.step(pn); M = _os.path.join(OP.SCRATCH, f'MODEL_{pn}.stp')      # run nwo_model.py first
    for tag, p in (('BRENNAN', B), ('MODEL  ', M)):
        try:
            P = nwo_params(p)
            P2, ch = C.chamfer(p)
            c = ch[0] if ch else {}
            print(pn, tag, 'vol %.4f' % vol(p), {k: P[k] for k in ('tip', 'I3', 'THDL', 'UR', 'WR', 'WT', 'NUTR', 'NUTT', 'NECKR', 'NECKL', 'BODYR', 'TM')},
                  'chamfer', c.get('corner_r'), c.get('wash_side'), c.get('neck_side'), c.get('ang_w'), c.get('ang_n'))
        except Exception as ex:
            print(pn, tag, 'ERR', ex)
