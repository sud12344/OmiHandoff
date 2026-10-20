import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, os
os.environ.setdefault('GT_OUT', OP.SCRATCH)
import nwo_model as NM
import gen_tee as T
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_SOLID
root = sys.argv[1]
built, _ = T.build_rows(root)
bad = 0
for b in built:
    if b['chk']: continue
    S, removed = NM.build(b, e45=bool(T.SPEC[root].get('e45')))
    n = 0; e = TopExp_Explorer(S, TopAbs_SOLID)
    while e.More(): n += 1; e.Next()
    exp = {i + 1: T.nwo_nut_removed(lg['nut']) for i, lg in enumerate(b['legs']) if lg['kind'] == 'NWO'}
    okv = all(abs(removed[k] - exp[k]) < 0.005 * exp[k] + 1e-7 for k in exp)
    if n != 1 or not okv: bad += 1
    print(b['pn'], 'solids', n, 'vol', round(NM.vol(S), 4), 'nut cut', {k: round(v, 5) for k, v in removed.items()}, 'expected', {k: round(v, 5) for k, v in exp.items()}, '' if (n == 1 and okv) else '<<<< PROBLEM')
print('configs', sum(1 for b in built if not b['chk']), 'problems', bad)
