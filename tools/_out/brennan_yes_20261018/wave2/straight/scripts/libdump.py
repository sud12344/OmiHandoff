"""libdump.py: print the batch-16 gen_straight2 end-library keys used by the straight group (read-only import against the base tables)"""
import os, sys
ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
W2 = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\wave2\straight')
os.environ['OMI_ROOT'] = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\base_root')
os.environ['GS_OUT'] = os.path.join(W2, r'test\_libimport'); os.environ['GT_OUT'] = os.environ['GS_OUT']
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(ROOT, r'tools\_out\puckfix_20261009\tools_new\generators'))
import gen_straight2 as G
for n in ('NPTF', 'ENDL', 'FPT', 'JIC', 'ORB', 'ORBF_MEAS', 'JICF_MEAS', 'JICF_CS_MEAS', 'SWIV_MEAS', 'NPSM_MEAS', 'MS51531'):
    d = getattr(G, n, None)
    print(n, sorted(d) if isinstance(d, dict) else d)
print('FPT', {k: (v['thr'], v.get('TD'), v.get('P1')) for k, v in G.FPT.items()})
print('ENDL', G.ENDL)
print('JIC4', G.JIC[4]); print('JIC24', G.JIC[24])
