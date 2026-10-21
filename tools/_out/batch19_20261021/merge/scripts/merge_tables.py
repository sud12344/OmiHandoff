"""merge_tables.py (batch 19, 2026-10-21): root19/04_DESIGN_TABLES = the live 04_DESIGN_TABLES + every review table one of the five staging
agents changed (A_answered, B_newspec, C_ownstep, D_geom, E_gen). A table changed by two agents stops the merge. Writes merge/tables_merged.txt."""
import filecmp, os, shutil, sys
H = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
B = os.path.join(H, 'tools', '_out', 'batch19_20261021')
LIVE = os.path.join(H, '04_DESIGN_TABLES')
SRC = {'A_answered': 'root', 'B_newspec': '', 'C_ownstep': 'root', 'D_geom': 'root', 'E_gen': 'root'}
OUT = os.path.join(B, 'merge', 'root19', '04_DESIGN_TABLES')
shutil.rmtree(os.path.dirname(OUT), ignore_errors=True)
shutil.copytree(LIVE, OUT, dirs_exist_ok=True)
seen, lines = {}, []
for ag, sub in SRC.items():
    d = os.path.join(B, ag, sub, '04_DESIGN_TABLES')
    assert os.path.isdir(d), d
    for f in sorted(os.listdir(d)):
        if not (f.startswith('DesignTable_') and f.endswith('.xlsx')) or '_SW2' in f:
            continue
        live = os.path.join(LIVE, f)
        if os.path.exists(live) and filecmp.cmp(os.path.join(d, f), live, shallow=False):
            continue
        if f in seen:
            sys.exit(f'CONFLICT: {f} changed by {seen[f]} and {ag}')
        seen[f] = ag
        shutil.copy2(os.path.join(d, f), os.path.join(OUT, f))
        lines.append(f'{ag:11} {"NEW " if not os.path.exists(live) else "edit"} {f}')
open(os.path.join(B, 'merge', 'tables_merged.txt'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines)); print(len(lines), 'tables')
