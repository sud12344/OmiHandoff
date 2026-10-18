"""marker_test.py: does an extra review-table column $PRP@DimSource change what the generators write? Copies the staged 1405 / 1502 / 6410
tables (omi_answers_20261018) into a scratch root, appends the column (values BRENNAN / OMI / AIRWAY on a few rows), regenerates with the
batch-16 tools and compares the macros + SW2 with the generation without the column (omi_answers_20261018/gen)."""
import os, sys, shutil, subprocess, filecmp, openpyxl

ROOT = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff'
SRC = os.path.join(ROOT, r'tools\_out\omi_answers_20261018')
W = os.path.join(ROOT, r'tools\_out\brennan_yes_20261018\marker_test')
TOOLS = os.path.join(ROOT, r'tools\_out\puckfix_20261009\tools_new')
if os.path.exists(W):
    raise SystemExit('exists: ' + W)
dt = os.path.join(W, 'root', '04_DESIGN_TABLES')
shutil.copytree(os.path.join(SRC, 'scratch_root', '04_DESIGN_TABLES'), dt)
for t in ('1405', '1502', '6410'):
    p = os.path.join(dt, f'DesignTable_{t}.xlsx')
    wb = openpyxl.load_workbook(p); ws = wb.active
    c = ws.max_column + 1
    ws.cell(2, c, '$PRP@DimSource')
    for r in range(3, ws.max_row + 1):
        if ws.cell(r, 1).value:
            ws.cell(r, c, ('BRENNAN', 'OMI', 'AIRWAY')[r % 3])
    wb.save(p)
env = dict(os.environ, OMI_ROOT=os.path.join(W, 'root'), GS_OUT=os.path.join(W, 'gen', 'straight'), GT_OUT=os.path.join(W, 'gen', 'tee'))
for g, roots in (('gen_straight2.py', ('1405', '6410')), ('gen_tee.py', ('1502',))):
    for r in roots:
        out = subprocess.run([sys.executable, '-I', os.path.join(TOOLS, 'generators', g), r], env=env, capture_output=True, text=True)
        print(r, out.stdout.strip().splitlines()[0] if out.stdout.strip() else out.stderr[-800:])


def norm(p):
    return [l for l in open(p, encoding='latin-1').read().replace('\r\n', '\n').split('\n') if 'Generated' not in l and '2026-' not in l]


def cells(p):
    ws = openpyxl.load_workbook(p, data_only=True).active
    return [[c.value for c in row] for row in ws.iter_rows()]


for sub, files in (('straight', ('Build_1405_MASTER.bas', 'DesignTable_1405_SW2.xlsx', 'Build_6410_MASTER.bas', 'DesignTable_6410_SW2.xlsx')),
                   ('tee', ('Build_1502_MASTER.bas', 'DesignTable_1502_SW2.xlsx'))):
    for f in files:
        a, b = os.path.join(SRC, 'gen', sub, f), os.path.join(W, 'gen', sub, f)
        same = norm(a) == norm(b) if f.endswith('.bas') else cells(a) == cells(b)
        print(f, 'IDENTICAL' if same else 'DIFFERS')
