import os as _os, sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__)); _TOOLS = _os.path.dirname(_HERE)
for _p in (_os.path.join(_TOOLS, 'generators'), _TOOLS, _HERE):   # tools/measure, tools/, tools/generators (portable, 2026-09-25)
    if _p not in _sys.path: _sys.path.insert(0, _p)
import omi_paths as OP     # (named OP: these scripts use P as a variable)
import sys, json
from nwo import nwo_params
for p in sys.argv[1:]:
    m = nwo_params(p)
    if m: m['AF'] = round(2 * m.pop('NUTR'), 4); m['Y'] = round(2 * m.pop('BODYR'), 4)
    print(p.split('/')[-1].replace('.stp', ''), json.dumps(m))
