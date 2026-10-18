import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math
from section import section, edges
from prof import shape
p = sys.argv[1]; ang = math.radians(float(sys.argv[2])); amin = float(sys.argv[3])
c, s_ = math.cos(ang), math.sin(ang)
E = edges(section(shape(p), (0, 0, 1)))
rows = []
for kind, pts in E:
    P = [(q[0] * c + q[1] * s_, -q[0] * s_ + q[1] * c) for q in pts]
    if max(a for a, r in P) < amin: continue
    (a1, r1), (a2, r2) = P[0], P[-1]
    k = 'L' if kind == 'L' else ('C' if isinstance(kind, tuple) else 'S')
    extra = f' R={kind[2]:.4f} ctr=({kind[1][0]:.3f},{kind[1][1]:.3f})' if isinstance(kind, tuple) else ''
    rows.append((min(a1, a2), f'{k} ({a1:7.4f},{r1:7.4f}) -> ({a2:7.4f},{r2:7.4f}){extra}'))
for _, t in sorted(rows): print(t)
