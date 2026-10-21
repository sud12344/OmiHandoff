import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math, json
from prof import leg_edges, bbox
from swiv import seg_list, near

def ang(s): return math.degrees(math.atan2(abs(s['r2'] - s['r1']), abs(s['a2'] - s['a1']) + 1e-12))

def ends_of(p):
    b = bbox(p); spans = [b[3] - b[0], b[4] - b[1], b[5] - b[2]]
    # the fitting axis is the odd one out (the two cross-section spans are equal or close)
    ax = max(range(3), key=lambda k: abs(spans[k] - sum(spans[j] for j in range(3) if j != k) / 2))
    return [(ax, -1), (ax, 1)]

def face_edges(p, axis, sign):
    E = leg_edges(p, axis, sign, [k for k in (0, 1, 2) if k != axis][-1], a0=-99)
    S = [s for s in seg_list(E) if min(s['r1'], s['r2']) > -1e-6]
    af = max(max(s['a1'], s['a2']) for s in S)
    return S, af

def measure_orbf(p):
    for axis, sign in ends_of(p):
        S, af = face_edges(p, axis, sign)
        ch = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 9 < ang(s) < 18]
        if not ch: continue
        ch = ch[0]; RF, RC = ch['r2'], ch['r1']
        # 45deg lead-in to the minor, then the long minor bore, ending where the drill point starts
        horiz = [s for s in S if near(s['r1'], s['r2'], 1e-3) and s['a2'] - s['a1'] > 0.05 and s['a2'] < ch['a1'] + 0.06 and s['r1'] < RC - 0.005]
        mn = max(horiz, key=lambda s: s['a2'])
        return dict(end=(axis, sign), face=round(af, 4), RF=round(RF, 4), RC=round(RC, 4), CHANG=round(ang(ch), 1), MINR=round(mn['r1'], 4), P=round(af - mn['a1'], 4), chamf_len=round(af - ch['a1'], 4))
    return None

def measure_jicf(p):
    for axis, sign in ends_of(p):
        S, af = face_edges(p, axis, sign)
        cs = [s for s in S if near(s['a2'], af) and s['a1'] < af - 1e-3 and s['r2'] > s['r1'] and 40 < ang(s) < 50]
        if not cs: continue
        cs = cs[0]
        horiz = [s for s in S if near(s['r1'], s['r2'], 1e-3) and near(s['a2'], cs['a1']) and near(s['r1'], cs['r1'])]
        if not horiz: continue
        mn = horiz[0]
        seat = [s for s in S if near(s['a2'], mn['a1']) and near(s['r2'], mn['r1']) and 34 < ang(s) < 40]
        return dict(end=(axis, sign), face=round(af, 4), RCS=round(cs['r2'], 4), MINR=round(mn['r1'], 4), P=round(af - mn['a1'], 4), seat=bool(seat))
    return None

if __name__ == '__main__':
    kind = sys.argv[1]
    for p in sys.argv[2:]:
        m = measure_orbf(p) if kind == 'orbf' else measure_jicf(p)
        print(p.split('/')[-1], json.dumps(m))
