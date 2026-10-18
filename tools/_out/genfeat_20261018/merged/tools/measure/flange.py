import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, json
from prof import leg_edges
from swiv import seg_list, near
from ports import ends_of

def measure_flange(p):
    for axis, sign in ends_of(p):
        S = [s for s in seg_list(leg_edges(p, axis, sign, [k for k in (0, 1, 2) if k != axis][-1], a0=-99)) if min(s['r1'], s['r2']) > -1e-6]
        af = max(max(s['a1'], s['a2']) for s in S)
        verts = [s for s in S if near(s['a1'], s['a2'])]
        horiz = [s for s in S if near(s['r1'], s['r2']) and s['a2'] - s['a1'] > 0.01]
        # groove bottom: a vertical line inside the face, joined at both ends by horizontals that reach the face
        for v in verts:
            if near(v['a1'], af) or v['a1'] < af - 0.3: continue
            lo, hi = min(v['r1'], v['r2']), max(v['r1'], v['r2'])
            hl = [h for h in horiz if near(h['a1'], v['a1']) and near(h['a2'], af) and near(h['r1'], lo)]
            hh = [h for h in horiz if near(h['a1'], v['a1']) and near(h['a2'], af) and near(h['r1'], hi)]
            if hl and hh:
                head = [h for h in horiz if near(h['a2'], af) and h['r1'] > hi + 0.02]
                head = max(head, key=lambda h: h['r1'])
                return dict(end=(axis, sign), face=round(af, 4), TH=round(af - head['a1'], 4), GI=round(lo, 4), GO=round(hi, 4), GD=round(af - v['a1'], 4), O=round(2 * head['r1'], 4))
    return None

if __name__ == '__main__':
    for p in sys.argv[1:]: print(p.split('/')[-1], json.dumps(measure_flange(p)))
