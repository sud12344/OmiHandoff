"""regen.py (2026-10-21): regenerate the roots the Brennan CAD cells touch, control vs stage, same tools.
  non-FS roots: tools_af (= live tools + the 6410 reference line, airway_first_20261020), control OMI_ROOT = the Air-Way-first stage,
                stage OMI_ROOT = ../stage
  FS roots:     the ORFS staging tools (orfs_gen_20261020/tools), OMI_ROOT = repo, OMI_REV_EXTRA = the ORFS stage tables (control) /
                ../stage/orfs_tables (stage)
Folded tables go to their master: 2404L -> 2404, 2501LL -> 2501, 6801L -> 6801. Roots with no generator SPEC are listed, not run.
Writes regen/{control,stage}/... and regen/cmp.txt: per root configurations control / stage, NEW, LOST, changed, and whether every
change belongs to a touched row (rows.csv)."""
import os, sys, re, csv, subprocess, collections, openpyxl

H = os.path.dirname(os.path.abspath(__file__)); A = os.path.dirname(H)
ROOT = os.path.normpath(os.path.join(A, '..', '..', '..'))
J = lambda *a: os.path.join(ROOT, *a)
AF = J('tools', '_out', 'airway_first_20261020'); OR = J('tools', '_out', 'orfs_gen_20261020', 'tools')
GEN_AF = os.path.join(AF, 'tools_af', 'generators'); GEN_OR = os.path.join(OR, 'generators')
OUT = os.path.join(A, 'regen')
FOLD = {'2404L': '2404', '2501LL': '2501', '6801L': '6801'}


def spec(g):
    code = open(g, encoding='utf-8').read(); m = re.search(r'^SPEC\s*=\s*\{', code, re.M)
    k = set(re.findall(r"^\s*'([0-9A-Z]{3,8})'\s*:\s*dict\(", code[m.end():], re.M)) if m else set()
    return k | set(re.findall(r"^SPEC\['([0-9A-Z]{3,8})'\]\s*=", code, re.M))


rows = list(csv.DictReader(open(os.path.join(A, 'rows.csv'), encoding='utf-8')))
touched = collections.defaultdict(set)
for r in rows:
    touched[FOLD.get(r['root'], r['root'])].add(r['part'])
gs, gt = spec(os.path.join(GEN_AF, 'gen_straight2.py')), spec(os.path.join(GEN_AF, 'gen_tee.py'))
ogs, ogt = spec(os.path.join(GEN_OR, 'gen_straight2.py')), spec(os.path.join(GEN_OR, 'gen_tee.py'))


def run(sub, r, g, gen, env_extra):
    o = os.path.join(OUT, sub); os.makedirs(o, exist_ok=True)
    env = dict(os.environ, GS_OUT=os.path.join(o, 'straight'), GT_OUT=os.path.join(o, 'tee'), **env_extra)
    p = subprocess.run([sys.executable, '-I', '-B', os.path.join(gen, g), r], env=env, capture_output=True, text=True)
    open(os.path.join(o, f'{r}_stdout.txt'), 'w', encoding='utf-8').write(p.stdout + '\n--- stderr ---\n' + p.stderr)
    return p.returncode


def load(p):
    if not os.path.exists(p):
        return {}
    rs = list(openpyxl.load_workbook(p, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)); h = rs[0]
    return {r[0]: dict(zip(h, r)) for r in rs[1:] if r and r[0]}


lines = []
for r in sorted(touched):
    if r.startswith('FS'):
        if r in ogs: g, sub = 'gen_straight2.py', 'straight'
        elif r in ogt: g, sub = 'gen_tee.py', 'tee'
        else: lines.append(f'{r:8} NO GENERATOR SPEC - cells staged as data only'); print(lines[-1]); continue
        rc_c = run('control', r, g, GEN_OR, dict(OMI_ROOT=ROOT, OMI_REV_EXTRA=J('tools', '_out', 'brennan_yes_20261018', 'stage_orfs', '04_DESIGN_TABLES')))
        rc_s = run('stage', r, g, GEN_OR, dict(OMI_ROOT=ROOT, OMI_REV_EXTRA=os.path.join(A, 'stage', 'orfs_tables')))
    else:
        if r in gs: g, sub = 'gen_straight2.py', 'straight'
        elif r in gt: g, sub = 'gen_tee.py', 'tee'
        else: lines.append(f'{r:8} NO GENERATOR SPEC - cells staged as data only'); print(lines[-1]); continue
        rc_c = run('control', r, g, GEN_AF, dict(OMI_ROOT=os.path.join(AF, 'stage')))
        rc_s = run('stage', r, g, GEN_AF, dict(OMI_ROOT=os.path.join(A, 'stage')))
    c = load(os.path.join(OUT, 'control', sub, f'DesignTable_{r}_SW2.xlsx'))
    s = load(os.path.join(OUT, 'stage', sub, f'DesignTable_{r}_SW2.xlsx'))
    key = lambda k, d: re.sub(r'\s+', '-', str(d.get('$PRP@OMiSKU') or d.get('$PRP@PartNo') or k)).upper()
    new = sorted(set(s) - set(c)); lost = sorted(set(c) - set(s))
    chg = sorted(k for k in set(c) & set(s) if c[k] != s[k])
    untraced = [k for k in new + chg if key(k, s[k]) not in touched[r]]
    lines.append(f'{r:8} [{sub}] rc {rc_c}/{rc_s} | configs control {len(c):3d} stage {len(s):3d} | NEW {len(new)} {new} | LOST {lost} | '
                 f'changed {chg} | untraced {untraced}')
    print(lines[-1], flush=True)
open(os.path.join(OUT, 'cmp.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
