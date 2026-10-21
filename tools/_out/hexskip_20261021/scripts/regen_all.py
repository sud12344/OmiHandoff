"""regen_all.py (2026-10-21): every gen_tee and gen_straight2 SPEC root, old toolset vs the hex-skip toolset, same inputs.
  python regen_all.py <set>   set = af_stage   : tools_af old (airway_first_20261020/tools_af) vs new (tools_af), OMI_ROOT = the Brennan CAD stage (fixed 6810)
                                    af_unfixed : the same tools, OMI_ROOT = a copy of that stage with the ORIGINAL 6810 table (old_files)
                                    b19_live   : live tools/ vs tools_b19, OMI_ROOT = repo (live 04_DESIGN_TABLES)
Writes regen/<set>/{old,new}/... and regen/<set>/cmp.txt: per root return codes + every output file compared byte for byte."""
import os, sys, re, shutil, subprocess, filecmp, openpyxl
H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
STAGE = J('tools', '_out', 'brennancad_20261021', 'stage')
SETS = {'af_stage': (J('tools', '_out', 'airway_first_20261020', 'tools_af'), os.path.join(A, 'tools_af'), STAGE),
        'af_unfixed': (J('tools', '_out', 'airway_first_20261020', 'tools_af'), os.path.join(A, 'tools_af'), os.path.join(A, 'regen', 'stage_unfixed')),
        'b19_live': (J('tools'), os.path.join(A, 'tools_b19'), ROOT)}
s = sys.argv[1]; old, new, omi = SETS[s]
if s == 'af_unfixed':
    if os.path.exists(omi): shutil.rmtree(omi)
    shutil.copytree(STAGE, omi)
    shutil.copy(os.path.join(A, 'old_files', 'DesignTable_6810.xlsx'), os.path.join(omi, '04_DESIGN_TABLES'))


def spec(g):
    code = open(g, encoding='utf-8').read(); m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    k = set(re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M)) if m else set()
    return k | set(re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M))


# an .xlsx is a zip with time stamps: compared by every cell value of every sheet; everything else byte for byte
def same(x, y):
    if not x.endswith('.xlsx'):
        return filecmp.cmp(x, y, shallow=False)
    v = lambda p: [(ws.title, list(ws.iter_rows(values_only=True))) for ws in openpyxl.load_workbook(p, data_only=False).worksheets]
    return v(x) == v(y)


# stdout / traceback: the toolset path and gen_tee line numbers (+4 lines in the new file) are not differences
norm = lambda t, tools: re.sub(r'line \d+', 'line N', t.replace(tools, '<TOOLS>'))
OUT = os.path.join(A, 'regen', s); lines = []
for g in ('gen_tee.py', 'gen_straight2.py'):
    roots = sorted(spec(os.path.join(old, 'generators', g)) | spec(os.path.join(new, 'generators', g)))
    for r in roots:
        rc = {}
        for side, t in (('old', old), ('new', new)):
            o = os.path.join(OUT, side, r); os.makedirs(o, exist_ok=True)
            env = dict(os.environ, OMI_ROOT=omi, GS_OUT=o, GT_OUT=o)
            p = subprocess.run([sys.executable, '-I', '-B', os.path.join(t, 'generators', g), r], env=env, capture_output=True, text=True)
            open(os.path.join(OUT, side, f'{r}_stdout.txt'), 'w', encoding='utf-8').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
            rc[side] = p.returncode
        a, b = os.path.join(OUT, 'old', r), os.path.join(OUT, 'new', r)
        fa, fb = sorted(os.listdir(a)), sorted(os.listdir(b))
        diff = sorted(set(fa) ^ set(fb)) + [f for f in sorted(set(fa) & set(fb)) if not same(os.path.join(a, f), os.path.join(b, f))]
        so = norm(open(os.path.join(OUT, 'old', f'{r}_stdout.txt'), encoding='utf-8').read(), old) == norm(open(os.path.join(OUT, 'new', f'{r}_stdout.txt'), encoding='utf-8').read(), new)
        lines.append(f"{r:9} [{g[:-3]}] rc {rc['old']}/{rc['new']} | files {len(fa)}/{len(fb)} | {'IDENTICAL' if not diff else 'DIFF ' + ', '.join(diff)} | stdout {'same' if so else 'differs'}")
        print(lines[-1], flush=True)
open(os.path.join(OUT, 'cmp.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
