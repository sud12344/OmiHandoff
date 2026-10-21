import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, math, json, glob
from nwo import measure_nwo, nwo_params
# nut chamfer on the adjustable ORB locknut: in the section through the hex CORNERS the nut outline is
# face (radial) -> chamfer cone -> corner line (radius = A/C/2) -> chamfer cone -> face.  Report, per STEP,
# the chamfer start radius at each nut face, the corner radius and the cone angle to the face plane.
def chamfer(p):
    P = nwo_params(p)
    out = []
    for leg, at, pts in measure_nwo(p):
        if abs(at - P['tip']) > 1e-3 or leg[:2] != P['leg'][:2]: continue
        segs = list(zip(pts, pts[1:]))
        # corner line: horizontal run at radius > nut flats radius (AF/2) + 0.02, between the washer and the neck
        AF2 = P['AF'] / 2 if 'AF' in P else P['NUTR']
        for k, ((a1, r1), (a2, r2)) in enumerate(segs):
            n0 = P['tip'] - P['I3'] + P['NECKL']; w0 = n0 + P['NUTT']
            if abs(r1 - r2) < 1e-4 and r1 > AF2 + 0.01 and n0 - 1e-3 < min(a1, a2) and max(a1, a2) < w0 + 1e-3 and 0 < k < len(segs) - 1:
                (b1, s1), _ = segs[k - 1]          # segment before (from the washer side)
                _, (c2, t2) = segs[k + 1]          # segment after (toward the neck)
                ang_w = math.degrees(math.atan2(abs(b1 - a1), abs(s1 - r1)))   # angle of the cone to the face plane
                ang_n = math.degrees(math.atan2(abs(c2 - a2), abs(t2 - r2)))
                out.append(dict(leg=leg, corner_r=round(r1, 4), run=(round(a1, 4), round(a2, 4)), wash_side=(round(b1, 4), round(s1, 4)), neck_side=(round(c2, 4), round(t2, 4)),
                                ang_w=round(ang_w, 2), ang_n=round(ang_n, 2)))
    return P, out
if __name__ == '__main__':
  for p in sys.argv[1:]:
    P, out = chamfer(p)
    AF = P.get('AF') or 2 * P['NUTR']
    print(p.split('/')[-1].replace('.stp', ''), 'AF(flats x2)', round(2 * P['NUTR'], 4), 'A/C/2', round(P['NUTR'] / math.cos(math.radians(30)), 4), 'n0', round(P['tip'] - P['I3'] + P['NECKL'], 4),
          'w0', round(P['tip'] - P['I3'] + P['NECKL'] + P['NUTT'], 4))
    for o in out: print('   ', o)
