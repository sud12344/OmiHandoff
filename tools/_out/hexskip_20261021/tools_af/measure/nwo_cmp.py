import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, json, openpyxl
from nwo import nwo_params
from swiv import legs_of
ws = openpyxl.load_workbook(OP.review_table('6801'), read_only=True).active
rows = list(ws.iter_rows(values_only=True)); h = rows[1]
AW = {r[0]: dict(zip(h, r)) for r in rows[2:] if r[0]}
out = {}
import glob
for p in sorted(glob.glob(_os.path.join(OP.STEP_DIR, 'BRENNAN_6801-*-NWO-FG.stp'))):
    pn = _os.path.basename(p).replace('.stp', '').replace('BRENNAN_', '')
    P = nwo_params(p)
    L = legs_of(p)
    ext = {(a, s): e for (a, s), e in L}
    orb_ax = P['leg'][:2]
    jic = [e for k, e in ext.items() if k != orb_ax]
    b = dict(LEG_ORB=P['tip'], LEG_JIC=round(max(jic), 4) if jic else None, I3=P['I3'], THDL=P['THDL'], C4=P['AF'] if 'AF' in P else round(2 * P['NUTR'], 4),
             Y=round(2 * P['BODYR'], 4), UR=P['UR'], TM=P['TM'])
    a = AW.get(pn, {})
    aw = dict(LEG_ORB=a.get('LEG_ORB@DRIVE'), LEG_JIC=a.get('LEG_JIC@DRIVE'), I3=a.get('ORB_I3@DRIVE'), THDL=a.get('ORB_THDL@DRIVE'), C4=a.get('HEXB@HEX'), Y=a.get('Y@REF'),
              UR=(a.get('ORB_GRVDIA@DRIVE') or 0) / 2 or None, TM=a.get('THDMAJ_B@DRIVE'))
    diffs = {k: (aw[k], b[k]) for k in b if aw[k] is not None and b[k] is not None and abs(aw[k] - b[k]) > 0.006}
    out[pn] = dict(brennan=b, airway=aw, diffs=diffs, scope=a.get('$PRP@ScopeAction'))
    print(pn, a.get('$PRP@ScopeAction'), 'DIFFS:', diffs)
_os.makedirs(OP.SCRATCH, exist_ok=True); json.dump(out, open(_os.path.join(OP.SCRATCH, 'cmp6801.json'), 'w'), indent=1)
