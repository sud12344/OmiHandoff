"""regen_all.py (group D): every gen_straight2 / gen_tee root with tools_af (old) and tools_gd (new), on the brennancad stage tables,
then compare the outputs (scripts/cmp_out.py logic per root). gen_bent is new in tools_gd (its roots are compared separately:
regen/test_baseline vs regen/test_new). Output: regen/all_old, regen/all_new (git-ignored), regen/all_cmp.txt."""
import os, re, sys, subprocess, filecmp
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE = os.path.abspath(os.path.join(H, '..', 'brennancad_20261021', 'stage'))
TOOLS = {'old': os.path.join(H, '..', 'airway_first_20261020', 'tools_af'), 'new': os.path.join(H, 'tools_gd')}


def spec(g):
    code = open(g, encoding='utf-8').read(); m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    k = set(re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M)) if m else set()
    return sorted(k | set(re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M)))


lines = []
for gen in ('gen_straight2.py', 'gen_tee.py'):
    roots = spec(os.path.join(TOOLS['new'], 'generators', gen))
    assert roots == spec(os.path.join(TOOLS['old'], 'generators', gen))
    for r in roots:
        res = {}
        for k, t in TOOLS.items():
            o = os.path.join(H, 'regen', f'all_{k}', r); os.makedirs(o, exist_ok=True)
            env = dict(os.environ, OMI_ROOT=STAGE, GS_OUT=o, GT_OUT=o)
            p = subprocess.run([sys.executable, '-I', '-B', os.path.join(t, 'generators', gen), r], env=env, capture_output=True, text=True)
            res[k] = (p.returncode, sorted(os.listdir(o)))
        same = res['old'] == res['new']
        if same:
            for f in res['old'][1]:
                a, b = os.path.join(H, 'regen', 'all_old', r, f), os.path.join(H, 'regen', 'all_new', r, f)
                if f.endswith('.xlsx'):          # the xlsx zip carries its creation time: compare the cells
                    import openpyxl
                    ca = [list(x) for x in openpyxl.load_workbook(a).active.iter_rows(values_only=True)]
                    cb = [list(x) for x in openpyxl.load_workbook(b).active.iter_rows(values_only=True)]
                    if ca != cb:
                        same = False
                elif not filecmp.cmp(a, b, shallow=False):
                    same = False
        lines.append(f'{gen:16} {r:8} rc {res["old"][0]}/{res["new"][0]} files {len(res["old"][1])} {"IDENTICAL" if same else "DIFFER"}')
        print(lines[-1], flush=True)
n = sum('IDENTICAL' in l for l in lines)
lines.append(f'{n} of {len(lines)} roots identical (byte for byte, every output file)')
open(os.path.join(H, 'regen', 'all_cmp.txt'), 'w').write('\n'.join(lines) + '\n')
print(lines[-1])
