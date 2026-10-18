# leg profile tool: section through the leg axis, edges expressed as (a = distance along the leg from the crossing, r = distance from the axis)
import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math
from section import load, section, edges
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib

_cache = {}
def shape(p):
    if p not in _cache: _cache[p] = load(p)
    return _cache[p]

def bbox(p):
    b = Bnd_Box(); BRepBndLib.Add_s(shape(p), b)
    return [round(v / 25.4, 4) for v in (b.CornerMin().X(), b.CornerMin().Y(), b.CornerMin().Z(), b.CornerMax().X(), b.CornerMax().Y(), b.CornerMax().Z())]

def leg_edges(p, axis, sign, plane_normal=2, a0=-9.0, rside=1):
    """edges of the section by the plane normal to `plane_normal` (through the origin), in leg coordinates.
    Only the half with the radial coordinate >= 0 (the other in-plane axis, positive side) is returned.
    rside=-1 (2026-10-02): the NEGATIVE side of the other in-plane axis instead (the side away from an elbow's other leg)."""
    n = [0, 0, 0]; n[plane_normal] = 1
    E = edges(section(shape(p), tuple(n)))
    other = [k for k in (0, 1, 2) if k not in (axis, plane_normal)][0]
    out = []
    for kind, pts in E:
        P = [(sign * q[axis], rside * q[other]) for q in pts]
        if max(r for a, r in P) < -1e-6: continue          # the negative half
        if min(r for a, r in P) < -1e-6 and max(r for a, r in P) > 1e-6: pass
        if max(a for a, r in P) < a0: continue
        out.append((kind, P))
    return out

def fmt(E, amin=-9, rmin=-1e-6):
    rows = []
    for kind, P in E:
        (a1, r1), (a2, r2) = P[0], P[-1]
        if min(r1, r2) < rmin: continue
        if max(a1, a2) < amin: continue
        k = 'L' if kind == 'L' else ('C' if isinstance(kind, tuple) else kind)
        if abs(a2 - a1) + abs(r2 - r1) < 1e-7 and k == 'L': continue
        ang = math.degrees(math.atan2(abs(r2 - r1), abs(a2 - a1))) if k == 'L' else None
        extra = f' R={kind[2]:.4f}' if isinstance(kind, tuple) else ''
        rows.append((min(a1, a2), f'{k:2} ({a1:8.4f},{r1:7.4f}) -> ({a2:8.4f},{r2:7.4f})' + (f'  ang {ang:5.1f}' if ang is not None else '') + extra))
    return [s for _, s in sorted(rows)]

if __name__ == '__main__':
    p = sys.argv[1]; axis = int(sys.argv[2]); sign = int(sys.argv[3]); pn = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    amin = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    print('bbox', bbox(p))
    for s in fmt(leg_edges(p, axis, sign, pn), amin=amin): print(s)
