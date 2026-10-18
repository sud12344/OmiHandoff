"""step_overall.py: overall length (bounding box along the fitting axis) of the own Brennan STEPs of the straight-group rows, as a
cross-check of the catalog L (no value from here is written to cells.csv). -> ../measure/step_overall.json"""
import os, sys, json, hashlib
ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
MT = os.path.join(ROOT, r'tools\_out\puckfix_20261009\tools_new\measure')
sys.dont_write_bytecode = True
sys.path[:0] = [MT, os.path.dirname(MT), os.path.join(os.path.dirname(MT), 'generators')]
os.environ.setdefault('OMI_ROOT', os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\base_root'))
from prof import bbox
res = {}
for pn in ('2404-L-32-32', '2406-03-04', '5000-40-40', '5404-40-40', '5406-40-32', '6400-14-14-O', '6400-32-32-O', '6410-04-02-O', '6420-08-08'):
    p = os.path.join(ROOT, '09_STEP_FILES', f'BRENNAN_{pn}.stp')
    b = bbox(p); sp = [round(b[3] - b[0], 4), round(b[4] - b[1], 4), round(b[5] - b[2], 4)]
    ax = max(range(3), key=lambda k: abs(sp[k] - sum(sp[j] for j in range(3) if j != k) / 2))
    res[pn] = dict(sha256=hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16], spans=sp, overall=sp[ax])
    print(pn, res[pn])
json.dump(res, open(os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\wave2\straight\measure\step_overall.json'), 'w'), indent=1)
