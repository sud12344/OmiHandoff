"""stage_orfs.py: the ORFS stage (2026-10-18). Copies the 51 staged ORFS review tables (orfs_airway_20261015/review_tables, unchanged
there) to brennan_yes_20261018/stage_orfs/04_DESIGN_TABLES, then applies
  - wave3/orfs/cells.csv (Brennan = yes, marked BRENNAN),
  - wave3/orfs/cells_proposed.csv as approved: user 2026-10-18 "Q-FS-XFER yes: take the per-dash bores and stud lengths from Air-Way's
    rows where they agree (the 154 proposed cells)" -> written to wave3/orfs/cells_xfer_APPROVED.csv with the source reworded,
and sets DataStatus ASSUMED on rows that are then complete (rows.csv 'DATA COMPLETE', or every missing column covered by the transfer).
No ORFS generator exists yet, so nothing is generated."""
import os, csv, shutil, subprocess, sys

BY = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\brennan_yes_20261018'
SRC = r'C:\Users\sudha\OneDrive\Desktop\OMi_Handoff\tools\_out\orfs_airway_20261015\review_tables'
ST = os.path.join(BY, 'stage_orfs')
W = os.path.join(BY, 'wave3', 'orfs')
if os.path.exists(ST):
    raise SystemExit('exists: ' + ST)
os.makedirs(os.path.join(ST, '04_DESIGN_TABLES'))
n = 0
for f in os.listdir(SRC):
    if f.startswith('DesignTable_FS') and f.endswith('.xlsx'):
        shutil.copy2(os.path.join(SRC, f), os.path.join(ST, '04_DESIGN_TABLES', f)); n += 1
print('copied', n, 'FS tables')

prop = list(csv.DictReader(open(os.path.join(W, 'cells_proposed.csv'), encoding='utf-8-sig')))
for c in prop:
    c['source'] = c['source'].replace('PROPOSED per-dash bore transfer (Q-FS-XFER, not approved)', 'per-dash transfer, user 2026-10-18 Q-FS-XFER yes') \
                             .replace('(Q-FS-XFER, not approved)', '(user 2026-10-18 Q-FS-XFER yes)').replace('PROPOSED', 'approved')
with open(os.path.join(W, 'cells_xfer_APPROVED.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(prop[0])); w.writeheader(); w.writerows(prop)

xfer = {}
for c in prop:
    xfer.setdefault((c['table'], c['config']), set()).add(c['column'])
rows = list(csv.DictReader(open(os.path.join(W, 'rows.csv'), encoding='utf-8-sig')))
out = []
for r in rows:
    miss = {m.strip() for m in r['missing_columns'].replace(';', ',').split(',') if m.strip()}
    complete = r['notes'].startswith('DATA COMPLETE') or (miss and miss <= xfer.get((r['table'], r['config']), set()))
    held = r['config'] == 'FS0319-24' or 'held' in r['notes'].lower()[:40]
    out.append(dict(table=r['table'], config=r['config'], ready='yes' if complete and not held else 'no'))
with open(os.path.join(W, 'rows_after_xfer.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['table', 'config', 'ready']); w.writeheader(); w.writerows(out)
print('complete after Q-FS-XFER:', sum(1 for o in out if o['ready'] == 'yes'), 'of', len(out))

subprocess.run([sys.executable, '-I', os.path.join(BY, 'scripts', 'apply_brennan.py'), ST, os.path.join(W, 'cells.csv'),
                os.path.join(W, 'cells_xfer_APPROVED.csv'), '--rows', os.path.join(W, 'rows_after_xfer.csv')], check=True)
