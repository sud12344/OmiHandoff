"""Batch 17: judge the SolidWorks dry runs (RUN ON THE PC after the dryrun/calls files; reads dryrun/out/NN_<root>.txt = call.py output,
dryrun/<root>/Build_<root>_report.txt). Per root:
  macro    run_macro ok, report 0 FAIL lines, the "Master left in its reference configuration" trace present (= the new module ran)
  sweep    every configuration of the regenerated SW2 present in the dry-run part, each rebuilds with 1 solid body (Default ignored)
  old      configurations also in the 11_MASTERS master: volume and size identical (1e-5) - EXCEPT the configurations whose SW2 values
           batch 17 changes on purpose (dimchg_cells.csv: A19 / A20 / A21 OMi values) and 6400 (A6: the generator replaces the hand-built
           master), which are listed with their change for review; roots with a pre-2026-09-25 macro in 03_SCRIPTS are flagged REVIEW
           on any difference (their masters were built by the old macros)
Writes dryrun/VERDICT.txt. Usage: python cmp_dryrun_b17.py"""
import os, re, json, csv, glob, collections
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cs = json.load(open(os.path.join(H, 'changeset.json')))
expect = collections.defaultdict(set)
for r in csv.DictReader(open(os.path.join(H, 'dimchg_cells.csv'), encoding='utf-8')):
    expect[r['root']].add(r['config'])


def calls_of(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'=== (\w+) (.*?)\n(.*?)\n--- [\d.]+s', t, re.S):
        try: yield m.group(1), json.loads(m.group(3))
        except ValueError: yield m.group(1), m.group(3)


def sw2_configs(r):
    import openpyxl
    ws = openpyxl.load_workbook(os.path.join(H, 'regen/b17', cs[r]['kind'], f'DesignTable_{r}_SW2.xlsx'), data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    hi = next(i for i, x in enumerate(rows) if sum(v is not None for v in x) > 3)
    return [x[0] for x in rows[hi + 1:] if x and x[0]]


def same(a, b):
    return (a['volume'] is not None and b['volume'] is not None and abs(a['volume'] - b['volume']) < 1e-5
            and all(abs(x - y) < 1e-5 for x, y in zip(a['size'] or [], b['size'] or [])))


out, verdict = [], collections.Counter()
for p in sorted(glob.glob(os.path.join(H, 'dryrun/out/*_*.txt'))):
    r = os.path.basename(p)[3:-4]
    if r not in cs: continue
    calls = list(calls_of(p)); probs, notes = [], []
    rm = [c for n, c in calls if n == 'run_macro']
    sweeps = [c for n, c in calls if n == 'sweep_configs' and isinstance(c, dict)]
    if not rm or not isinstance(rm[0], dict) or not rm[0].get('ok'): probs.append(f'run_macro not ok: {str(rm[:1])[:300]}')
    else:
        rep = rm[0].get('report') or {}
        if rep.get('fail'): probs.append(f'{rep["fail"]} FAIL lines: {rep.get("fail_lines", [])[:5]}')
        if rm[0].get('msgbox'): notes.append(f'msgbox: {rm[0]["msgbox"][:3]}')
    rp = os.path.join(H, 'dryrun', r, f'Build_{r}_report.txt')
    if not (os.path.exists(rp) and 'Master left in its reference configuration' in open(rp, encoding='latin-1').read()):
        probs.append('report missing or without the reference-configuration trace')
    after = {x['config']: x for x in (sweeps[-1]['rows'] if sweeps else []) if x['config'] != 'Default'}
    want = sw2_configs(r)
    miss = [c for c in want if c not in after]
    if miss: probs.append(f'{len(miss)} configurations missing in the dry-run part: {miss[:6]}')
    nok = [c for c, x in after.items() if not x['ok']]
    if nok: probs.append(f'{len(nok)} configurations not ok (errors / bodies != 1): {[(c, after[c]["bodies"], after[c].get("errors", [])[:2]) for c in nok[:4]]}')
    if len(sweeps) >= 2:
        before = {x['config']: x for x in sweeps[0]['rows'] if x['config'] != 'Default'}
        both = sorted(set(before) & set(after))
        diff = [c for c in both if not same(before[c], after[c])]
        exp = [c for c in diff if c in expect.get(r, ()) or r == '6400']
        une = [c for c in diff if c not in exp]
        notes.append(f'old configurations {len(both)}: identical {len(both) - len(diff)}, changed on purpose {len(exp)}'
                     + (f' {[(c, round(after[c]["volume"] - before[c]["volume"], 5)) for c in exp[:8]]}' if exp else ''))
        if une:
            (notes if False else probs).append(f'{"REVIEW (pre-fix macro)" if cs[r]["prefix_macro"] else "UNEXPECTED"} change in {len(une)} old '
                                              f'configurations: {[(c, round(after[c]["volume"] - before[c]["volume"], 5)) for c in une[:8]]}')
    v = 'OK' if not probs else 'REVIEW' if all(x.startswith('REVIEW') for x in probs) else 'FAIL'
    verdict[v] += 1
    out.append(f'{v:6s} {r:8s} configs {len(after)}/{len(want)}  ' + ' | '.join(probs + notes))
done = {os.path.basename(p)[3:-4] for p in glob.glob(os.path.join(H, 'dryrun/out/*_*.txt'))}
todo = [r for r, v in cs.items() if v['status'] != 'unchanged' and r not in done]
out.append(f'\n{dict(verdict)}; not run yet: {len(todo)} {sorted(todo)}')
open(os.path.join(H, 'dryrun/VERDICT.txt'), 'w').write('\n'.join(out) + '\n'); print('\n'.join(out))
