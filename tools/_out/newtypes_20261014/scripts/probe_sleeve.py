"""probe_sleeve.py (2026-10-14): half-section of a revolved part's STEP (a sleeve), for its SHAPE only (user 2026-10-08:
"shape is fine" from Brennan 3D files; sizes come from Air-Way / OMi). Prints the bounding box, the axis it finds (the box
direction whose cross extents are equal) and every edge of the section through that axis with r >= 0, as (a, r) in inches.

python probe_sleeve.py <step>"""
import os, sys
sys.path.insert(0, r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\measure')
import prof   # noqa: E402  (tools/measure/prof.py: bbox, leg_edges)

p = sys.argv[1]
b = prof.bbox(p)
ext = [round(b[3 + k] - b[k], 4) for k in range(3)]
print('box', b, 'extents', ext)
# axis = the direction whose two cross extents are equal (round part)
cands = []
for ax in range(3):
    o = [k for k in range(3) if k != ax]
    cands.append((abs(ext[o[0]] - ext[o[1]]), ax))
ax = min(cands)[1]
pn = [k for k in range(3) if k != ax][0]
print('axis', 'XYZ'[ax], 'section plane normal', 'XYZ'[pn])
E = prof.leg_edges(p, ax, +1, plane_normal=pn, a0=-99)
rows = []
for kind, P in E:
    (a1, r1), (a2, r2) = P[0], P[-1]
    if min(r1, r2) < -1e-6:
        continue
    rows.append((round(min(a1, a2), 4), kind, round(a1, 4), round(r1, 4), round(a2, 4), round(r2, 4), P))
for row in sorted(rows):
    kind, a1, r1, a2, r2, P = row[1:]
    extra = ''
    if kind != 'L':
        mid = P[len(P) // 2]
        extra = f'  mid ({mid[0]:.4f}, {mid[1]:.4f})'
    print(f'{str(kind)[:46]:46s} ({a1:8.4f}, {r1:7.4f}) -> ({a2:8.4f}, {r2:7.4f}){extra}')
