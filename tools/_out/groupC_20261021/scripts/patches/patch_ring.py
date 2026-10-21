"""patch_ring.py: GROUP C addition to gen_ring.py (copied verbatim from tools/_out/orfs_gen_20261020/tools/generators/gen_ring.py):
the CSLEEVE model type (compression sleeve C0319, 14-line half-section, all-linear DRIVE dimensions) - one inserted block, one inserted
build_rows branch, and the emit dispatch line extended."""
import sys
p = sys.argv[1]; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)

import os
BLOCK = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ring_block.py')).read()
rep("\n\ndef load_review(root):\n", BLOCK + "\n\ndef load_review(root):\n")
rep("""            else:
                vals = {k: r.get(f'{k}@DRIVE') for k in SLEEVE_DIMS}""",
"""            elif sp['kind'] == 'CSLEEVE':     # GROUP C (compression sleeve C0319)
                names = [nm for _, nm, _ in CSLEEVE_DIMS]
                vals = {k: r.get(f'{k}@DRIVE') for k in names}
                miss = [k for k, v in vals.items() if not num(v)]
                if miss:
                    skipped.append(f'{pn}: no {"/".join(miss)}')
                    continue
                cols = {f'{k}@DRIVE': round(v, 6) for k, v in vals.items()}
                why = csleeve_why(cols)
                cols.update({'$PRP@PartNo': pn, '$PRP@Description': f'{sp["desc"]}, {r.get("$PRP@TubeOD") or ""} in tube'.replace(',  in tube', ''),
                             '$PRP@GeometryRoot': root, '$PRP@OD': f'{2 * vals["COLLARR"]:.3f}', '$PRP@ID': f'{2 * vals["BORER"]:.3f}',
                             '$PRP@Length': f'{vals["L"]:.3f}', '$PRP@DataStatus': r['$PRP@DataStatus'],
                             '$PRP@AxialSource': f'{r["$PRP@AxialSource"]} | MODEL: {sp["assume"]}', '$COMMENT': r.get('$COMMENT'),
                             '$PRP@OMiSKU': r.get('$PRP@OMiSKU')})
            else:
                vals = {k: r.get(f'{k}@DRIVE') for k in SLEEVE_DIMS}""")
rep("    k = (parts_oring if sp['kind'] == 'ORING' else parts_sleeve)(ok, refrow)\n",
    "    k = parts_csleeve(ok, refrow) if sp['kind'] == 'CSLEEVE' else (parts_oring if sp['kind'] == 'ORING' else parts_sleeve)(ok, refrow)     # GROUP C: CSLEEVE\n")
open(p, 'w').write(s); print('patched', p)
