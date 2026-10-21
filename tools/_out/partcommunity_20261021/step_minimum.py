"""step_minimum.py (2026-10-21): the smallest Brennan STEP download set, now that Brennan's CAD parameter records may be used as Brennan
values (user 2026-10-21). A record is a list of family-specific letter codes; one real STEP of a family is enough to map its codes, after
which every size of that family can come from its record. So:
  NEEDED   = one file per Brennan CAD family that has not-ready parts and no STEP in 09_STEP_FILES yet (pc_results_repo_steps.csv gives the
             families of the STEPs on disk). Picked: a size the PC's download list already names (STEP_CHECKLIST.csv), else the -08 size,
             else the smallest.
  CHECK    = per-size files the PC asked for because the generator measures END detail per dash (face-seal male end FSM_MEAS, bulkhead leg
             FSBH_MEAS, FS adjustable stud NWO_FS) or a tap drill (A9). Whether the record carries that detail shows only once the family is
             mapped - download them only if it does not.
  Everything else on the 240-file list is optional (its sizes come from the record).
Writes STEP_MINIMUM.md / .csv."""
import os, re, csv, collections

H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(H, '..', '..', '..'))
fam_on_disk = {r['family'] for r in csv.DictReader(open(os.path.join(H, 'pc_results_repo_steps.csv'), encoding='utf-8')) if r['found'] == 'yes'}
F = [r for r in csv.DictReader(open(os.path.join(H, 'pc_final.csv'), encoding='utf-8')) if r['match'] in ('exact', 'alias')]
ck = list(csv.DictReader(open(os.path.join(ROOT, 'tools', '_out', 'sources_20261021', 'STEP_CHECKLIST.csv'), encoding='utf-8')))
listed = {r['brennan_pn'] for r in ck if r['brennan_cad'] == 'yes'}
bpn = lambda r: r['tried_as'] or r['part']          # the Brennan number that answered

by_fam = collections.defaultdict(list)
for r in F:
    by_fam[r['family']].append(r)

CHECK_GROUPS = ('ORFS shared shape files', 'Quick wins')   # FS2403 / FS2701 / FS6801 per dash + the A9 tap-drill pair
check = [r for r in ck if r['group'] in CHECK_GROUPS and r['brennan_cad'] == 'yes']

rows = []
for fam, rs in sorted(by_fam.items(), key=lambda t: -len(t[1])):
    if fam in fam_on_disk:
        continue
    pref = [r for r in rs if bpn(r) in listed] or rs
    pick = sorted(pref, key=lambda r: (0 if re.search(r'-08(-|$)', bpn(r)) else 1, bpn(r)))[0]
    rows.append(dict(family=fam, file=f'BRENNAN_{bpn(pick)}.stp', on_pc_list='yes' if bpn(pick) in listed else '',
                     unlocks=len(rs), parts=' '.join(r['part'] for r in rs)))
with open(os.path.join(H, 'STEP_MINIMUM.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
check_new = [r for r in check if f"BRENNAN_{r['brennan_pn']}.stp" not in {x['file'] for x in rows}]

md = ['# Brennan STEPs: the minimum download (2026-10-21)', '',
      'Brennan\'s CAD records may now be used as Brennan values (user 2026-10-21). One STEP per Brennan CAD family maps that family\'s',
      'letter codes; then every size in the family comes from its record. Save as `09_STEP_FILES/BRENNAN_<part number>.stp`.', '',
      f'- **Needed: {len(rows)} files** - one per family with no STEP on disk yet; together they unlock {sum(r["unlocks"] for r in rows)} parts '
      f'({sum(1 for r in rows if r["on_pc_list"])} of them are already on the PC\'s list).',
      f'- **Maybe: {len(check_new)} files** - per-size end detail / tap drill; download only if the mapped record lacks it (I will say).',
      f'- The other files of the 240-file list (`tools/_out/sources_20261021/STEP_CHECKLIST.md`) are optional now.',
      f'- {len(fam_on_disk & set(by_fam))} families already have a STEP on disk ({sum(len(by_fam[f]) for f in fam_on_disk & set(by_fam))} parts): '
      'no download needed.', '',
      '## Needed (one per family)', '', '| | File | Brennan CAD family | Parts it unlocks |', '|---|---|---|---:|']
md += [f"| [ ] | `{r['file']}` | {r['family'].split('/')[-1]} | {r['unlocks']} |" for r in rows]
md += ['', '## Maybe (download only if I ask)', '', '| | File | Why |', '|---|---|---|']
def why(pn):
    if pn.startswith('5405-'): return '-24 / -32 female pipe tap drill (A9) - a record has no tap drill'
    if pn.startswith('FS2403-'): return 'male face-seal END detail of this dash (groove, land, chamfer) for every FS straight / flange'
    if pn.startswith('FS2701-'): return 'bulkhead leg detail of this dash (FS2701 ... FS2704, -LN)'
    if pn.startswith('FS6801-'): return 'FS adjustable stud detail of this dash (FS6801 ... FS6804)'
    return 'end detail of this size'
md += [f"| [ ] | `{r['file_name']}` | {why(r['brennan_pn'])} |" for r in check_new]
open(os.path.join(H, 'STEP_MINIMUM.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
print(len(rows), 'needed,', sum(r['unlocks'] for r in rows), 'parts;', len(check_new), 'maybe')
