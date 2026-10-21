"""apply_all.py (group B): re-create the group B stage edits from scratch - copy this group's review tables fresh from the Brennan-CAD
stage (tools/_out/brennancad_20261021/stage), then run every edit_<series>.py in order. CHANGES.csv is rewritten."""
import os, shutil, importlib, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import tabedit as T
SRC = os.path.join(T.ROOT, 'tools', '_out', 'brennancad_20261021', 'stage')
EDITS = ['edit_6900', 'edit_elbows']
TABLES = {'04_DESIGN_TABLES': ['6900', '6901', '6805', '6806', '6809', '6815', '6832', '6835', '6801L', '6801LL', '3051', '6425', '4005'],
          'orfs_tables': ['FS1700', 'FS1704', 'FS1800', 'FS1804', 'FS2408', 'FS2700', 'FS2700-LN', 'FS6402', 'FS6809', 'FS6400-L', 'FS6801-L', 'FS7202']}
if __name__ == '__main__':
    for sub, roots in TABLES.items():
        for r in roots:
            f = f'DesignTable_{r}.xlsx'
            if os.path.exists(os.path.join(SRC, sub, f)): shutil.copy2(os.path.join(SRC, sub, f), os.path.join(T.A, 'stage', sub, f))
    if os.path.exists(T.LOG): os.remove(T.LOG)
    for e in EDITS:
        print('==', e); importlib.import_module(e).main()
