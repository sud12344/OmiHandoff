"""EXPERIMENT (2026-10-20): generate one gen_tee root with a different reference row, nothing else changed.
usage (GT_OUT, OMI_ROOT, OMI_REV_EXTRA set): python gen_ref.py <root> <ref part number>"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.normpath(os.path.join(HERE, '..', '..', 'orfs_gen_20261020', 'tools'))
sys.path[:0] = [os.path.join(T, 'generators'), T]
root, ref = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0]]
import gen_tee as g
g.SPEC[root]['ref'] = ref
built, skipped = g.build_rows(root)
hdr, ok, refrow = g.write_sw2(root, built)
print(g.emit(root, hdr, ok, refrow), 'ref', refrow['pn'], len(ok), 'configs')
